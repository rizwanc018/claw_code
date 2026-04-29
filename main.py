from typing import Any

from client.llm_client import LLMClient
import asyncio
import click

async def run(messages: dict[str, Any]):
    client = LLMClient()
    async for event in client.chat_completion(messages, True): # type: ignore
        print(event, "\n")


@click.command()
@click.argument("prompt", required=False)
def main(prompt: str | None):
    messages = [{
        "role": "user",
        "content": prompt
    }]
    asyncio.run(run(messages)) # type: ignore
    print("done")

main()
# asyncio.run(main())
