"""Thin LLM wrapper using litellm.

Supports any model string that litellm understands, e.g.:
  - openai/gpt-4o
  - anthropic/claude-sonnet-4-20250514
  - deepseek/deepseek-chat
  - openai/qwen2.5-72b-instruct  (vLLM-served, via OPENAI_API_BASE)

Environment variables (set in shell or .env file):
  PAPER2SPEC_MODEL   — default model (fallback: "openai/gpt-4o-mini")
  OPENAI_API_KEY     — required for OpenAI models
  ANTHROPIC_API_KEY  — required for Anthropic models
  DEEPSEEK_API_KEY   — required for DeepSeek models
  (litellm reads provider keys automatically)

A `.env` file in the project root is loaded automatically if python-dotenv
is installed.  The file is gitignored by default.
"""

import os
from typing import Optional

from paper2spec.config import load_project_env

# Auto-load .env from project root (best-effort; python-dotenv is optional)
load_project_env()

import litellm

DEFAULT_MODEL = os.getenv("PAPER2SPEC_MODEL", "openai/gpt-4o-mini")

# Suppress litellm's verbose logging unless DEBUG
litellm.suppress_debug_info = True


def chat(
    prompt: str,
    *,
    system: str = "",
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 4096,
) -> str:
    """Send a single prompt to the LLM and return the text response."""
    model = model or DEFAULT_MODEL
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = litellm.completion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


async def achat(
    prompt: str,
    *,
    system: str = "",
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 4096,
) -> str:
    """Async version of :func:`chat`."""
    model = model or DEFAULT_MODEL
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = await litellm.acompletion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
