"""
Retry decorator for tvfetch functions.

Applies exponential backoff on TvRateLimitError and TvConnectionError.
"""

from __future__ import annotations

import functools
import logging
import time
from typing import Callable, TypeVar

from tvfetch.exceptions import TvRateLimitError, TvConnectionError

log = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable)


def with_retry(
    max_attempts: int = 3,
    base_delay: float = 2.0,
    retry_on: tuple = (TvRateLimitError, TvConnectionError),
) -> Callable[[F], F]:
    """
    Decorator that retries a function on transient errors with exponential backoff.

    Args:
        max_attempts: Maximum number of total attempts (default 3)
        base_delay:   Initial delay in seconds between retries (doubles each attempt)
        retry_on:     Tuple of exception types to retry on

    Example:
        @with_retry(max_attempts=3, base_delay=2.0)
        def my_fetch():
            return tvfetch.fetch("BINANCE:BTCUSDT", "1D")
    """
    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except retry_on as exc:
                    last_exc = exc
                    if attempt == max_attempts - 1:
                        break
                    delay = base_delay * (2 ** attempt)
                    log.warning(
                        "%s — retrying in %.1fs (attempt %d/%d): %s",
                        type(exc).__name__, delay, attempt + 1, max_attempts - 1, exc,
                    )
                    time.sleep(delay)
            raise last_exc
        return wrapper  # type: ignore[return-value]
    return decorator
