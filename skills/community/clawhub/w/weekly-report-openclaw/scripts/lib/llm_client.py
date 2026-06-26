"""LLM client implementation."""

from abc import ABC, abstractmethod
from typing import List, Optional

from openai import AsyncOpenAI


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
    ) -> str:
        """Generate a completion from the LLM."""
        pass

    @abstractmethod
    async def chat(
        self,
        messages: List[dict],
        temperature: float = 0.7,
        max_tokens: int = 4000,
    ) -> str:
        """Have a multi-turn chat with the LLM."""
        pass

    async def __aenter__(self) -> "BaseLLMClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass


class DeepSeekClient(BaseLLMClient):
    """DeepSeek client using OpenAI-compatible API."""

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com/v1",
    ):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return await self.chat(messages, temperature, max_tokens)

    async def chat(
        self,
        messages: List[dict],
        temperature: float = 0.7,
        max_tokens: int = 4000,
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def close(self) -> None:
        await self.client.close()


def create_llm_client(
    provider: str = "deepseek",
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    settings=None,
) -> BaseLLMClient:
    """Create an LLM client based on configuration."""
    if settings is not None:
        provider = provider or settings.llm.provider
        model = model or settings.llm.model
        base_url = base_url or settings.llm.base_url
        if api_key is None:
            api_key = settings.get_api_key()

    if provider == "deepseek":
        return DeepSeekClient(
            api_key=api_key,
            model=model or "deepseek-chat",
            base_url=base_url or "https://api.deepseek.com/v1",
        )
    elif provider == "openai":
        return DeepSeekClient(
            api_key=api_key,
            model=model or "gpt-4",
            base_url=base_url or "https://api.openai.com/v1",
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
