"""A deliberately rough token estimate: four characters per token."""

from __future__ import annotations


def estimate_tokens(text: str) -> int:
    return len(text) // 4
