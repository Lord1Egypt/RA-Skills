# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Abstract base class for LLM providers.
All LLM calls in Quorum go through this interface.
"""

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from quorum.cost import CostTracker


class BaseProvider(abc.ABC):
    """
    Minimal LLM provider interface.

    Two methods:
    - complete()      → raw text response
    - complete_json() → structured dict response

    Implementors handle auth, retry, rate limiting, etc.
    """

    def __init__(self, cost_tracker: "CostTracker | None" = None) -> None:
        self._cost_tracker = cost_tracker

    @abc.abstractmethod
    def complete(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> str:
        """
        Call the LLM and return the text response.

        Args:
            messages: List of {"role": "...", "content": "..."} dicts
            model:    Model identifier string (e.g. "claude-opus-4", "gpt-4o")
            temperature: Sampling temperature
            max_tokens:  Maximum response tokens

        Returns:
            The assistant's text response
        """
        ...

    @abc.abstractmethod
    def complete_json(
        self,
        messages: list[dict[str, str]],
        model: str,
        schema: dict[str, Any],
        temperature: float = 0.1,
    ) -> dict[str, Any]:
        """
        Call the LLM requesting structured JSON output matching the schema.

        Args:
            messages: List of {"role": "...", "content": "..."} dicts
            model:    Model identifier string
            schema:   JSON Schema dict describing the expected response structure
            temperature: Sampling temperature (lower = more deterministic)

        Returns:
            Parsed dict matching the schema. Raises ValueError if unparseable.
        """
        ...
