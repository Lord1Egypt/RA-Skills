"""Text-size measurement helpers for the adaptive scheduler.

The scheduler enforces a per-request ``payload_size`` budget in addition
to the batch-entry-count limit (R12.13). Measuring the "size" of a
single input item requires a unit-aware function — hence the
:data:`SizeOfFn` callback injected into
:class:`~.adaptive.AdaptiveScheduler`.

This module provides the default implementations for the two supported
units:

- :func:`size_of_chars` — Unicode code-point count, for APIs priced per
  character (most third-party translation / TTS).
- :func:`size_of_tokens` — approximate LLM-tokenizer count (``ceil(len/2)``
  heuristic, i.e. 1 char ≈ 2 tokens reversed as ~0.5 tokens/char);
  providers with a real tokenizer SHOULD override their ``size_of`` on
  the provider protocol.

For backward compatibility with provider code written during task 5.1
(before the scheduler package existed), this module re-exports the
helpers from :mod:`translation_dubbing_skill.providers.sizing` — the
authoritative implementations live there and are imported verbatim so
the two call sites never drift.

Design mapping: design §"自适应调度器 · 文本量度量", requirements R12.12,
R12.13.
"""

from __future__ import annotations

from typing import Callable, TypeVar

from translation_dubbing_skill.providers.sizing import (
    PayloadUnit,
    default_size_of,
    size_of_chars,
    size_of_tokens,
)

_I = TypeVar("_I")

SizeOfFn = Callable[[_I], int]
"""Type alias for a provider-injected size measurement callback.

The scheduler is generic in the input type; providers pass a closure
that takes a single item (e.g. a ``SubtitleEntry`` or a raw string) and
returns a non-negative integer under the provider's declared
:attr:`~.config.ProviderRateLimitConfig.payload_unit`.
"""


def size_of_for_unit(unit: PayloadUnit) -> Callable[[str], int]:
    """Return the default text ``size_of`` function for ``unit``.

    Convenience wrapper used by provider coordinators that want to build
    a ``size_of`` closure without duplicating the dispatch logic::

        text_sizer = size_of_for_unit(rate_limit_config.payload_unit)
        size_of = lambda entry: text_sizer(entry.text)

    Args:
        unit: ``"chars"`` or ``"tokens"``.

    Returns:
        A ``str -> int`` callable implementing the default measurement.

    Raises:
        ValueError: If ``unit`` is neither ``"chars"`` nor ``"tokens"``.
    """

    def _sizer(text: str) -> int:
        return default_size_of(text, unit)

    return _sizer


__all__ = [
    "PayloadUnit",
    "SizeOfFn",
    "size_of_chars",
    "size_of_tokens",
    "default_size_of",
    "size_of_for_unit",
]
