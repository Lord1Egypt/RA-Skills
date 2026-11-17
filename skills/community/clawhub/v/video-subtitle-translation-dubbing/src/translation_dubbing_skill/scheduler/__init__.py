"""Adaptive scheduler (batch size / payload size / concurrency auto-tuning).

Exposes the public surface coordinators talk to:

- :class:`AdaptiveScheduler` — the scheduler itself (task 5.3).
- :func:`make_batches`       — the pure batching function, also exposed
  so property tests can exercise it without an async runtime.
- :class:`SchedulerBatchFailure` — raised when a batch exhausts its
  retry budget; coordinators wrap this into ``TranslationError`` /
  ``TTSError`` with context.
- :class:`ProviderRateLimitConfig` — the AIMD knobs.
- Signal exceptions: :class:`RateLimitError`, :class:`PayloadTooLargeError`,
  :class:`TransientError`, plus the detection helpers
  :func:`is_rate_limited`, :func:`is_payload_too_large`,
  :func:`retry_after_of`.
- Sizing helpers re-exported for convenience:
  :func:`size_of_chars`, :func:`size_of_tokens`, :func:`size_of_for_unit`.
"""

from translation_dubbing_skill.scheduler.adaptive import (
    AdaptiveScheduler,
    SchedulerBatchFailure,
    make_batches,
)
from translation_dubbing_skill.scheduler.config import (
    PayloadUnit,
    ProviderRateLimitConfig,
)
from translation_dubbing_skill.scheduler.signals import (
    PayloadTooLargeError,
    RateLimitError,
    SchedulerSignalError,
    TransientError,
    is_payload_too_large,
    is_rate_limited,
    retry_after_of,
)
from translation_dubbing_skill.scheduler.sizing import (
    SizeOfFn,
    size_of_chars,
    size_of_for_unit,
    size_of_tokens,
)

__all__ = [
    # adaptive
    "AdaptiveScheduler",
    "SchedulerBatchFailure",
    "make_batches",
    # config
    "PayloadUnit",
    "ProviderRateLimitConfig",
    # signals
    "SchedulerSignalError",
    "RateLimitError",
    "PayloadTooLargeError",
    "TransientError",
    "is_rate_limited",
    "is_payload_too_large",
    "retry_after_of",
    # sizing
    "SizeOfFn",
    "size_of_chars",
    "size_of_tokens",
    "size_of_for_unit",
]
