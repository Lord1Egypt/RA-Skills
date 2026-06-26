# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
LiteLLM universal provider.

Wraps LiteLLM to support 100+ models (Anthropic, OpenAI, Mistral, Groq, etc.)
through a single interface. Model names pass through directly to LiteLLM.

Auth: set the appropriate env vars (ANTHROPIC_API_KEY, OPENAI_API_KEY, etc.)
or pass api_keys in the config.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

try:
    import litellm
    from litellm import completion
except ImportError as e:
    raise ImportError(
        "LiteLLM is required. Install it with: pip install litellm"
    ) from e

from quorum.providers.base import BaseProvider
from quorum.utils import extract_json_from_response

logger = logging.getLogger(__name__)


class LiteLLMProvider(BaseProvider):
    """
    Universal LLM provider via LiteLLM.

    Handles all models with one interface. API keys are read from env vars
    automatically by LiteLLM. You can also pass extra_kwargs for provider-
    specific parameters.
    """

    def __init__(
        self,
        api_keys: dict[str, str] | None = None,
        extra_kwargs: dict[str, Any] | None = None,
        cost_tracker: Any | None = None,
    ):
        """
        Args:
            api_keys: Optional dict of {env_var_name: key_value} pairs.
                      These are injected into the environment before each call.
            extra_kwargs: Additional kwargs passed to every litellm.completion() call.
            cost_tracker: Optional CostTracker for recording token usage and cost.
        """
        super().__init__(cost_tracker=cost_tracker)
        self._api_keys = api_keys or {}
        self._extra_kwargs = extra_kwargs or {}

        # Suppress LiteLLM's verbose logging unless debug mode is on
        litellm.suppress_debug_info = True
        litellm.set_verbose = False

        # Inject API keys into env now
        for key, value in self._api_keys.items():
            if value:
                os.environ[key] = value

    def complete(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> str:
        """Call any LiteLLM-supported model and return text."""
        logger.debug("Calling model=%s (temp=%.2f, max_tokens=%d)", model, temperature, max_tokens)
        try:
            response = completion(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **self._extra_kwargs,
            )
            text = response.choices[0].message.content or ""
        except Exception as e:
            logger.error("LLM call failed for model=%s: %s", model, e)
            raise

        # Track cost as a side effect — does not change return type
        if self._cost_tracker is not None:
            try:
                usage = getattr(response, "usage", None)
                if usage is not None:
                    prompt_tokens = getattr(usage, "prompt_tokens", 0) or 0
                    completion_tokens = getattr(usage, "completion_tokens", 0) or 0
                    try:
                        cost = litellm.completion_cost(completion_response=response)
                        if cost is None:
                            cost = 0.0
                    except Exception:
                        logger.warning(
                            "Could not calculate completion cost for model=%s — recording $0.00",
                            model,
                        )
                        cost = 0.0
                    self._cost_tracker.track(
                        call_name="complete",
                        model=model,
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                        cost=cost,
                    )
            except Exception as track_err:
                logger.warning("Cost tracking failed (non-fatal): %s", track_err)

        return text

    def complete_json(
        self,
        messages: list[dict[str, str]],
        model: str,
        schema: dict[str, Any],
        temperature: float = 0.1,
    ) -> dict[str, Any]:
        """
        Call LLM requesting JSON output, then parse and return.

        Strategy:
        1. Append a JSON instruction to the last user message
        2. Call complete()
        3. Extract and parse the JSON block from the response
        4. Raise ValueError if parsing fails
        """
        # Append JSON instruction to the system or last user message
        json_instruction = (
            "\n\nRespond with ONLY valid JSON matching this schema. "
            "No markdown fences, no explanation, just the JSON object:\n"
            f"{json.dumps(schema, indent=2)}"
        )

        augmented_messages = list(messages)
        # If there's a user message at the end, append to it
        if augmented_messages and augmented_messages[-1]["role"] == "user":
            augmented_messages[-1] = {
                **augmented_messages[-1],
                "content": augmented_messages[-1]["content"] + json_instruction,
            }
        else:
            augmented_messages.append({"role": "user", "content": json_instruction})

        raw = self.complete(
            messages=augmented_messages,
            model=model,
            temperature=temperature,
            max_tokens=8192,  # JSON responses may be large
        )

        return self._parse_json(raw, model)

    def _parse_json(self, raw: str, model: str) -> dict[str, Any]:
        """Extract and parse JSON from LLM response, handling markdown fences and other formatting issues."""
        # Use the utility function to extract clean JSON
        cleaned_text = extract_json_from_response(raw)

        # Try direct parse first (handles both clean and fence-stripped JSON)
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            pass

        # If that fails, try to find any JSON object or array in the response
        # Handle both objects {...} and arrays [...]
        for pattern in [r"\{.*\}", r"\[.*\]"]:
            match = re.search(pattern, cleaned_text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    continue

        # If all parsing attempts fail, provide detailed error information
        raise ValueError(
            f"Could not parse JSON from model={model} response. "
            f"Original length: {len(raw)}, cleaned length: {len(cleaned_text)}. "
            f"First 200 chars of cleaned: {cleaned_text[:200]!r}"
        )
