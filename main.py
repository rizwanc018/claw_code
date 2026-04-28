from client.llm_client import LLMClient
import asyncio


async def main():
    client = LLMClient()
    messages = [{
        "role": "user",
        "content": "Hi, whats up"
    }]
    async for event in client.chat_completion(messages, True):
        print(event, "\n")
    print("done")


asyncio.run(main())
