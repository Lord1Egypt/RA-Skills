"""Configuration model for the adaptive scheduler.

:class:`ProviderRateLimitConfig` carries the runtime knobs that drive the
three-dimensional AIMD (additive-increase / multiplicative-decrease)
strategy: batch-entry count, per-request payload volume, and concurrency.

Design mapping: design §"自适应调度器 · ProviderRateLimitConfig",
requirements R12.3, R12.4, R12.5, R12.11, R12.14.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PayloadUnit = Literal["chars", "tokens"]
"""Closed set of payload measurement units supported by the scheduler.

- ``"chars"``: Unicode code-point count. Common for web translation /
  TTS APIs priced per character.
- ``"tokens"``: Approximate LLM-tokenizer token count. Providers with
  access to a real tokenizer SHOULD override ``size_of`` on the provider
  protocol; the default heuristic (see
  :mod:`translation_dubbing_skill.providers.sizing`) is deliberately
  coarse.
"""


def _check_triple(
    name: str,
    minimum: int,
    initial: int,
    maximum: int,
    *,
    lower_bound: int = 1,
) -> None:
    """Validate a ``(min, initial, max)`` tuple of scheduler knobs.

    The scheduler's invariants require ``min <= initial <= max`` and all
    three values to be at least ``lower_bound`` (default ``1`` since
    every dimension must allow at least one unit).
    """
    for label, value in (("min", minimum), ("initial", initial), ("max", maximum)):
        if value < lower_bound:
            raise ValueError(
                f"{name}_{label} must be >= {lower_bound}, got {value}"
            )
    if not (minimum <= initial <= maximum):
        raise ValueError(
            f"{name} requires min <= initial <= max, got "
            f"min={minimum}, initial={initial}, max={maximum}"
        )


@dataclass
class ProviderRateLimitConfig:
    """Runtime configuration for :class:`~.adaptive.AdaptiveScheduler`.

    Attributes:
        batch_size_initial: Starting count of entries per batch request.
        batch_size_min: Floor the scheduler will never go below when
            down-tuning on rate-limit signals (R12.6).
        batch_size_max: Ceiling the scheduler will never exceed when
            up-tuning on sustained success (R12.5).
        payload_size_initial: Starting per-request text volume budget,
            measured in :attr:`payload_unit`.
        payload_size_min: Floor for payload down-tune (R12.6, R12.12).
        payload_size_max: Ceiling for payload up-tune (R12.5).
        payload_unit: Either ``"chars"`` or ``"tokens"`` — dictates how
            the scheduler (and provider's ``size_of``) measure volume.
        concurrency_initial: Starting count of concurrent in-flight
            batch requests.
        concurrency_min: Floor for concurrency down-tune.
        concurrency_max: Ceiling for concurrency up-tune. Applies
            uniformly to LLM and third-party network providers (R12.11).
        max_retries: Upper bound on retries for a single batch. The
            total request count for a given batch is therefore
            ``max_retries + 1`` (first attempt plus retries). Payload-
            too-large re-slices do NOT consume this budget (R12.12).
        backoff_base_ms: Base for exponential backoff when the provider
            does not advertise ``Retry-After``. The wait on attempt
            ``k`` (1-indexed) is
            ``base * 2**(k - 1) + U(0, jitter)``.
        backoff_jitter_ms: Maximum additive jitter in milliseconds.
            ``0`` disables jitter (useful for deterministic tests).
        probe_up_every_n_success: After this many consecutive successful
            batches, the scheduler attempts to up-tune all three
            dimensions by one step (AIMD additive-increase). Must be
            positive.
        supports_batch: Whether the provider issues true batched
            requests. When ``False`` the scheduler clamps ``batch_size``
            to ``1`` regardless of the ``batch_size_*`` triple, and
            only ``payload_size`` / ``concurrency`` are tuned (R12.14).
    """

    batch_size_initial: int
    batch_size_min: int
    batch_size_max: int
    payload_size_initial: int
    payload_size_min: int
    payload_size_max: int
    payload_unit: PayloadUnit
    concurrency_initial: int
    concurrency_min: int
    concurrency_max: int
    max_retries: int
    backoff_base_ms: int
    backoff_jitter_ms: int
    probe_up_every_n_success: int
    supports_batch: bool

    def __post_init__(self) -> None:
        """Validate every field so the scheduler can assume well-formed state.

        Catches the most common authoring mistakes at construction time:

        - inverted min/max, initial outside ``[min, max]`` (per dimension);
        - non-positive probe step (would divide by zero in the AIMD path);
        - negative retry count or non-positive backoff base;
        - unknown ``payload_unit``.
        """
        _check_triple(
            "batch_size",
            self.batch_size_min,
            self.batch_size_initial,
            self.batch_size_max,
        )
        _check_triple(
            "payload_size",
            self.payload_size_min,
            self.payload_size_initial,
            self.payload_size_max,
        )
        _check_triple(
            "concurrency",
            self.concurrency_min,
            self.concurrency_initial,
            self.concurrency_max,
        )
        if self.payload_unit not in ("chars", "tokens"):
            raise ValueError(
                f"payload_unit must be 'chars' or 'tokens', got "
                f"{self.payload_unit!r}"
            )
        if self.max_retries < 0:
            raise ValueError(f"max_retries must be >= 0, got {self.max_retries}")
        if self.backoff_base_ms <= 0:
            raise ValueError(
                f"backoff_base_ms must be > 0, got {self.backoff_base_ms}"
            )
        if self.backoff_jitter_ms < 0:
            raise ValueError(
                f"backoff_jitter_ms must be >= 0, got {self.backoff_jitter_ms}"
            )
        if self.probe_up_every_n_success <= 0:
            raise ValueError(
                f"probe_up_every_n_success must be > 0, got "
                f"{self.probe_up_every_n_success}"
            )
        # When the provider does not support batching, the batch-size
        # triple is effectively ignored. We do not force it to (1, 1, 1)
        # so the caller can keep one config shape for both cases; the
        # scheduler clamps at runtime (R12.14).


__all__ = ["PayloadUnit", "ProviderRateLimitConfig"]
