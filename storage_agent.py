# """Storage Agent for storing data sent by users.
# This agent receives data from the DataValidationAgent and simulates storing it."""


from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class StorageAgent(Agent):
    class StoreBehaviour(CyclicBehaviour):
        async def run(self):
            try:
                msg = await self.receive(timeout=10)
                if msg:
                    print(f"[StorageAgent] Storing data: {msg.body}")
                    with open("storage.txt", "a") as f:
                        f.write(msg.body + "\n")
                    print("[StorageAgent] Data stored successfully.")
                    # Optionally notify the user of success
                    success_msg = Message(to="datavalidation@localhost")
                    success_msg.body = "Success, Your data has been successfully stored."
                    await self.send(success_msg)
            except Exception as e:
                print(f"[StorageAgent] Error: {e}")
                # Notify the user about the failure
                failure_msg = Message(to="datavalidation@localhost")
                failure_msg.body = "Sorry, there was an error storing your data. Please try again later."
                await self.send(failure_msg)
    async def setup(self):       
        print("[StorageAgent] Starting...")
        self.add_behaviour(self.StoreBehaviour())

