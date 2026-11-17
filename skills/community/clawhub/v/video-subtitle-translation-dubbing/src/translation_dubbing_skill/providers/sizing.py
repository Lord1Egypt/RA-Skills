"""Shared text-size measurement helpers for providers.

Providers declare a ``payload_unit`` (either ``"chars"`` or ``"tokens"``) and
expose a ``size_of(text) -> int`` method so the adaptive scheduler can split
inputs into batches that simultaneously honour a batch-entry-count limit and
a single-request text-volume limit.

This module exposes the generic measurement helpers that a provider's
default ``size_of`` implementation delegates to. A concrete provider MAY
override ``size_of`` with a more accurate estimate (e.g. a real tokenizer).

Corresponds to design section "自适应调度器" and requirements R12.12, R12.13.

Note:
    The authoritative copies of these helpers will live in
    ``translation_dubbing_skill.scheduler.sizing`` once the scheduler module
    (task 5.3) is introduced. They are kept here for now so the provider
    protocols can define a default ``size_of`` without taking a dependency
    on an as-yet-unwritten scheduler package. The implementations are
    intentionally simple and drop-in compatible.
"""

from __future__ import annotations

from typing import Literal

PayloadUnit = Literal["chars", "tokens"]


def size_of_chars(text: str) -> int:
    """Measure ``text`` size as the number of Unicode code points.

    Args:
        text: The text to measure.

    Returns:
        ``len(text)`` — the character count. Empty text has size ``0``.
    """
    return len(text)


def size_of_tokens(text: str) -> int:
    """Estimate ``text`` size as an approximate token count.

    Uses a coarse heuristic suitable for batching decisions: each Unicode
    code point is treated as ~0.5 tokens, i.e. ``ceil(len(text) / 2)``.
    Providers that have access to a real tokenizer SHOULD override
    ``size_of`` with a more accurate estimate.

    Args:
        text: The text to measure.

    Returns:
        A non-negative integer token estimate.
    """
    # ceil(len / 2) without importing math.
    return (len(text) + 1) // 2


def default_size_of(text: str, unit: PayloadUnit) -> int:
    """Return the size of ``text`` under the given ``payload_unit``.

    Dispatches to :func:`size_of_chars` for ``"chars"`` and
    :func:`size_of_tokens` for ``"tokens"``. Used by the default
    ``size_of`` implementation on provider protocols.

    Args:
        text: The text to measure.
        unit: The payload unit declared by the provider.

    Returns:
        The measured size under the requested unit.

    Raises:
        ValueError: If ``unit`` is neither ``"chars"`` nor ``"tokens"``.
    """
    if unit == "chars":
        return size_of_chars(text)
    if unit == "tokens":
        return size_of_tokens(text)
    raise ValueError(
        f"Unsupported payload_unit {unit!r}; expected 'chars' or 'tokens'."
    )


__all__ = [
    "PayloadUnit",
    "size_of_chars",
    "size_of_tokens",
    "default_size_of",
]
