# This agent validates data received from the user and forwards it to the storage agent if valid.
# """DataValidationAgent for validating user data.


from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class DataValidationAgent(Agent):
    class ValidateBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=15)
            if msg:
                data = msg.body
                print(f"[Validator] Received: {data}")
                try:
                    name, age, sugar, bmi = data.split(",")
                except ValueError:
                    print("[Validator] Parsing error.")
                    return

                if not (isinstance(name, str) and 0 < int(age) < 120 and 70 <= float(sugar) <= 180 and 10 <= float(bmi) <= 50):
                    feedback = Message(to=str(msg.sender))
                    feedback.body = "Invalid data. Please re-enter correct values."
                    await self.send(feedback)
                else:
                    print("[Validator] Data is valid. Forwarding to Storage Agent.")
                    forward = Message(to="storage@localhost")
                    forward.body = data
                    await self.send(forward)

                    confirm = Message(to=str(msg.sender))
                    confirm.body = "Data validated and sent to storage."
                    await self.send(confirm)

                    reply = await self.receive(timeout=15)
                    if reply:
                        if "Success" in reply.body:
                            print("[Validator] Storage confirmation received.!!")
                        elif "Sorry" in reply.body:
                            print("[Validator] Storage error reported.!!")
                    else:
                        print("[Validator] Unexpected reply from storage.")

    async def setup(self):
        print("[DataValidationAgent] Starting...")
        self.add_behaviour(self.ValidateBehaviour())
