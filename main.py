from client.llm_client import LLMClient
import asyncio


async def main():
    client = LLMClient()
    messages = [{
        "role": "user",
        "content": "Hai"
    }]
    await client.chat_completion(messages, False)
    print("done")


asyncio.run(main())
