#!/usr/bin/env python3
"""Retry utilities for HTTP and API calls."""

from __future__ import annotations

import time
from typing import Any, Callable, Optional


def request_with_retry(
    method: Callable,
    url: str,
    *,
    attempts: int = 3,
    backoff: float = 0.8,
    **kwargs,
) -> Any:
    """Call ``method(url, **kwargs)`` with exponential backoff retry."""
    last_exc: Optional[Exception] = None
    for i in range(attempts):
        try:
            resp = method(url, **kwargs)
            resp.raise_for_status()
            return resp
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if i == attempts - 1:
                break
            time.sleep(backoff * (2 ** i))
    raise last_exc or RuntimeError(f"Request failed after {attempts} attempts: {url}")


def _is_retriable_error(exc: Exception) -> bool:
    """Classify whether an error might succeed on retry."""
    msg = str(exc).lower()
    retriable_keywords = (
        "timeout", "timed out", "connection", "reset", "refused",
        "too many requests", "rate limit", "quota", "503", "502", "504",
        "temporary", "unavailable", "busy",
    )
    return any(kw in msg for kw in retriable_keywords)
