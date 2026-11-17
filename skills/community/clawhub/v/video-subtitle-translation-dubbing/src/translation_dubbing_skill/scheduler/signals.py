"""Rate-limit / payload-overflow / transient-failure signals.

The adaptive scheduler (see :mod:`translation_dubbing_skill.scheduler.adaptive`)
interprets provider failures through a small closed set of signal exceptions:

- :class:`RateLimitError`      — upstream signalled rate limiting; the
  scheduler SHALL back off all three dimensions (batch_size / payload_size /
  concurrency) multiplicatively and retry after ``Retry-After`` or
  exponential backoff (R12.6, R12.7).
- :class:`PayloadTooLargeError` — upstream rejected the request because the
  aggregated text volume exceeded its limit (HTTP 413, LLM context-window
  overflow, provider-specific payload-too-large business code); the
  scheduler SHALL only shrink ``payload_size`` and re-slice the offending
  batch without consuming the retry budget (R12.12).
- :class:`TransientError`       — any other transient failure (timeout,
  5xx, partial-response parse error); the scheduler retries with backoff
  but does NOT down-tune any dimension (design §"TransientError 路径").

Providers raise the appropriate subclass directly; the detection helpers
:func:`is_rate_limited`, :func:`is_payload_too_large` and
:func:`retry_after_of` additionally recognise equivalent signals carried by
an ``httpx.HTTPStatusError`` when a provider forwards the raw HTTP error
without wrapping.

Design mapping: design §"限流信号 / 文本量度量", requirements R12.4, R12.6,
R12.7, R12.12, R12.15.
"""

from __future__ import annotations

from typing import Any


class SchedulerSignalError(Exception):
    """Base class for the three signal exceptions understood by the scheduler.

    All subclasses share the same shape so the scheduler can reason about
    them uniformly:

    - ``retry_after`` (seconds, optional): when the upstream explicitly
      specified a wait time (via ``Retry-After`` header or equivalent),
      the scheduler uses this instead of computing an exponential backoff
      (R12.7).
    - ``context`` (dict, optional): free-form diagnostic bag the provider
      may populate (e.g. upstream status code, business error code, size
      reported by the upstream). Never contains credentials.
    - ``__cause__`` (standard Python): the underlying exception the
      provider wrapped, if any, set via ``raise ... from exc``.

    The class deliberately does NOT inherit from :class:`SkillError` —
    these signals are internal to the provider ↔ scheduler contract and
    are translated into ``TranslationError`` / ``TTSError`` only after the
    retry budget is exhausted.
    """

    def __init__(
        self,
        reason: str,
        *,
        retry_after: float | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the signal.

        Args:
            reason: Short human-readable summary. Stored as ``args[0]``.
            retry_after: Optional wait time in seconds. Must be
                non-negative when set.
            context: Optional diagnostic bag. Copied defensively so the
                caller's dict is not aliased.

        Raises:
            ValueError: If ``retry_after`` is negative.
        """
        super().__init__(reason)
        if retry_after is not None and retry_after < 0:
            raise ValueError(
                f"retry_after must be non-negative, got {retry_after!r}"
            )
        self.reason: str = reason
        self.retry_after: float | None = retry_after
        self.context: dict[str, Any] = dict(context) if context else {}


class RateLimitError(SchedulerSignalError):
    """Upstream signalled rate limiting (HTTP 429 or equivalent).

    Providers raise this to trigger the scheduler's multiplicative down-tune
    on all three dimensions (R12.6). When ``retry_after`` is set, the
    scheduler waits at least that many seconds before retrying (R12.7);
    otherwise it falls back to exponential backoff + jitter.
    """


class PayloadTooLargeError(SchedulerSignalError):
    """Upstream rejected the request because the payload was too large.

    Encompasses HTTP 413, LLM context-window-exceeded errors, and any
    provider-specific "input too long" business code. The scheduler
    responds by shrinking ``payload_size`` only (batch_size and
    concurrency are untouched) and re-slicing the offending batch — this
    re-slice does NOT count against the retry budget (R12.12).
    """


class TransientError(SchedulerSignalError):
    """A retry-worthy failure that is neither rate-limit nor overflow.

    Covers network timeouts, 5xx responses, partial-response parse
    errors, etc. The scheduler retries with exponential backoff + jitter
    up to ``max_retries`` but does not down-tune any dimension.
    """


# ---------------------------------------------------------------------------
# Detection helpers
# ---------------------------------------------------------------------------
#
# The helpers below are pluggable — the scheduler accepts them as callables
# so tests can inject custom detectors. The default implementations handle:
#
# 1. Direct instances of the signal classes (the common path).
# 2. ``httpx.HTTPStatusError`` forwarded verbatim by a provider — 429 maps
#    to rate-limit, 413 / LLM context-window-exceeded maps to payload-
#    too-large. We do a soft import so the scheduler package does not hard-
#    depend on httpx being installed at import time of this module.
# 3. Exceptions chained via ``__cause__`` — providers sometimes wrap the
#    httpx error in a generic ``TransientError``; the helpers follow the
#    chain one level to discover an underlying 429/413.


def _status_code_of(exc: BaseException) -> int | None:
    """Return the HTTP status code embedded in ``exc`` if it's an httpx error.

    Imports ``httpx`` lazily so this module has no hard dependency on it.
    Returns ``None`` when httpx is unavailable or the exception is not an
    :class:`httpx.HTTPStatusError`.
    """
    try:
        import httpx  # type: ignore[import-not-found]
    except Exception:  # pragma: no cover - httpx is a project dependency
        return None
    if isinstance(exc, httpx.HTTPStatusError):
        response = exc.response
        if response is not None:
            return int(response.status_code)
    return None


def _retry_after_of_httpx(exc: BaseException) -> float | None:
    """Extract a ``Retry-After`` header (in seconds) from an httpx error.

    Only handles the delta-seconds form (``"30"``). HTTP-date form is
    uncommon for 429 responses and falls through to ``None``, where the
    scheduler's exponential-backoff path takes over.
    """
    try:
        import httpx  # type: ignore[import-not-found]
    except Exception:  # pragma: no cover
        return None
    if not isinstance(exc, httpx.HTTPStatusError):
        return None
    response = exc.response
    if response is None:
        return None
    raw = response.headers.get("Retry-After") if response.headers else None
    if raw is None:
        return None
    try:
        value = float(raw.strip())
    except (TypeError, ValueError):
        return None
    return value if value >= 0 else None


def _walk_chain(exc: BaseException) -> list[BaseException]:
    """Return ``exc`` followed by ``__cause__`` / ``__context__`` links.

    Bounded to a small depth to avoid pathological loops if someone ever
    constructs a cyclic chain.
    """
    seen: list[BaseException] = []
    current: BaseException | None = exc
    depth = 0
    while current is not None and depth < 8 and current not in seen:
        seen.append(current)
        nxt: BaseException | None = current.__cause__ or current.__context__
        current = nxt
        depth += 1
    return seen


def is_rate_limited(exc: BaseException) -> bool:
    """Return ``True`` iff ``exc`` (or its chain) is a rate-limit signal.

    Recognises:

    - :class:`RateLimitError` anywhere in the ``__cause__`` / ``__context__``
      chain.
    - :class:`httpx.HTTPStatusError` with status code ``429``.
    """
    for link in _walk_chain(exc):
        if isinstance(link, RateLimitError):
            return True
        if _status_code_of(link) == 429:
            return True
    return False


# Business-error substrings that providers commonly use for context-window
# or payload-size rejections. Matching is case-insensitive. Kept short and
# conservative — providers SHOULD prefer raising PayloadTooLargeError
# directly; the string match is the safety net for raw httpx errors.
_PAYLOAD_TOO_LARGE_HINTS: tuple[str, ...] = (
    "context_length_exceeded",
    "context length exceeded",
    "maximum context length",
    "input is too long",
    "input_too_long",
    "payload too large",
    "request entity too large",
)


def _message_mentions_payload_too_large(exc: BaseException) -> bool:
    """Return ``True`` if ``exc``'s message mentions a payload-size rejection."""
    try:
        text = str(exc)
    except Exception:  # pragma: no cover - defensive
        return False
    if not text:
        return False
    lowered = text.lower()
    return any(hint in lowered for hint in _PAYLOAD_TOO_LARGE_HINTS)


def is_payload_too_large(exc: BaseException) -> bool:
    """Return ``True`` iff ``exc`` (or its chain) signals payload overflow.

    Recognises:

    - :class:`PayloadTooLargeError` anywhere in the chain.
    - :class:`httpx.HTTPStatusError` with status code ``413``.
    - Messages containing well-known LLM "context window exceeded" /
      "input too long" hints (case-insensitive substring match on the
      signal exception's reason or the raw httpx response body string).
    """
    for link in _walk_chain(exc):
        if isinstance(link, PayloadTooLargeError):
            return True
        if _status_code_of(link) == 413:
            return True
        # Only inspect signal-like exceptions' messages; avoid matching on
        # unrelated ValueError text, which would be too permissive.
        if isinstance(link, SchedulerSignalError) and _message_mentions_payload_too_large(link):
            return True
    return False


def retry_after_of(exc: BaseException) -> float | None:
    """Return the explicit ``Retry-After`` wait (seconds) if present.

    Order of precedence:

    1. ``retry_after`` attribute on a :class:`SchedulerSignalError` in
       the exception chain.
    2. ``Retry-After`` response header on an :class:`httpx.HTTPStatusError`
       in the chain.

    Returns ``None`` when no explicit wait is advertised; the scheduler
    then falls back to exponential backoff + jitter.
    """
    for link in _walk_chain(exc):
        if isinstance(link, SchedulerSignalError) and link.retry_after is not None:
            return float(link.retry_after)
        header_value = _retry_after_of_httpx(link)
        if header_value is not None:
            return header_value
    return None


__all__ = [
    "SchedulerSignalError",
    "RateLimitError",
    "PayloadTooLargeError",
    "TransientError",
    "is_rate_limited",
    "is_payload_too_large",
    "retry_after_of",
]
