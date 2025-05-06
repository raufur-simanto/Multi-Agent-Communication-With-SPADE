import asyncio
from useragent import UserAgent
from datavalidation_agent import DataValidationAgent
from storage_agent import StorageAgent

async def main():
    storage_agent = StorageAgent("storage@localhost", "storagepwd")
    await storage_agent.start()

    validation_agent = DataValidationAgent("datavalidation@localhost", "validationpwd")
    await validation_agent.start()

    # Wait to make sure behaviours are ready
    await asyncio.sleep(3)

    # Start user agent
    user_agent = UserAgent("user@localhost", "userpassword")
    await user_agent.start()

    print("[Main] Agents started. Running for 60 seconds...")
    await asyncio.sleep(60)

    await user_agent.stop()
    await validation_agent.stop()
    await storage_agent.stop()

if __name__ == "__main__":
    asyncio.run(main())

