from __future__ import annotations
from typing import Any, AsyncGenerator
from agent.events import AgentEvent, AgentEventType
from client.llm_client import LLMClient
from client.response import StreamEventType

class Agent:
    def __init__(self) -> None:
        self.client = LLMClient()

    async def run(self, message: str):
        yield AgentEvent.agent_start(message)
        # add message to context

        async for event in self._agentic_loop():
            yield event

            if event.type == AgentEventType.TEXT_COMPLETE:
                final_respone = event.data.get("content")

        yield AgentEvent.agent_end(final_respone)

    async def _agentic_loop(self) -> AsyncGenerator[AgentEvent, None]:
        messages = [{
            "role": "user",
            "content": "Hai whatsup"
        }]
        response_text = ""

        async for event in self.client.chat_completion(messages, True):
            if event.type == StreamEventType.TEXT_DELTA:
                if event.text_delta:
                    content = event.text_delta.content
                    response_text += content
                    yield AgentEvent.text_delta(content)
            elif event.type == StreamEventType.ERROR:
                yield AgentEvent.agent_error(
                    event.error or "Unknown error occurred.",
                )

        if response_text:
            yield AgentEvent.text_complete(response_text)

    async def __aenter__(self) -> Agent:
            return self

    async def __aexit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:
        if self.client:
            await self.client.close()
            self.client = None
