#!/usr/bin/env python3
"""
Error recovery framework for campaign execution.

Provides:
- Recoverable vs fatal error classification
- Retry logic with exponential backoff
- Error context preservation
"""

from __future__ import annotations

import time
from typing import Any, Callable, TypeVar, Optional

T = TypeVar("T")


class RecoverableError(Exception):
    """Error that can be retried."""
    pass


class FatalError(Exception):
    """Error that should not be retried."""
    pass


def execute_with_recovery(
    operation: Callable[[], T],
    max_retries: int = 3,
    backoff: float = 1.0,
    on_retry: Optional[Callable[[int, Exception], None]]= None,
) -> T:
    """Execute operation with retry logic.

    Parameters
    ----------
    operation : callable that returns T
    max_retries : maximum number of retry attempts
    backoff : initial backoff multiplier (exponential)
    on_retry : optional callback(attempt, error) for logging

    Returns
    -------
    Result of operation

    Raises
    ------
    RecoverableError : if all retries exhausted
    FatalError : immediately on fatal error
    """
    for attempt in range(max_retries):
        try:
            return operation()
        except FatalError:
            raise
        except RecoverableError as e:
            if attempt < max_retries - 1:
                if on_retry:
                    on_retry(attempt + 1, e)
                wait_time = backoff * (2 ** attempt)
                time.sleep(wait_time)
                continue
            raise
        except Exception as e:
            if attempt < max_retries - 1:
                if on_retry:
                    on_retry(attempt + 1, e)
                wait_time = backoff * (2 ** attempt)
                time.sleep(wait_time)
                continue
            raise RecoverableError(f"Operation failed after {max_retries} attempts") from e

    raise RecoverableError(f"Operation failed after {max_retries} attempts")


def classify_error(error: Exception) -> tuple[str, bool]:
    """Classify error as recoverable or fatal.

    Returns
    -------
    (error_type, is_recoverable)
    """
    if isinstance(error, FatalError):
        return ("fatal", False)
    if isinstance(error, RecoverableError):
        return ("recoverable", True)

    error_msg = str(error).lower()

    fatal_patterns = [
        "authentication",
        "unauthorized",
        "forbidden",
        "invalid_argument",
        "not_found",
    ]
    for pattern in fatal_patterns:
        if pattern in error_msg:
            return ("fatal", False)

    recoverable_patterns = [
        "timeout",
        "connection",
        "temporarily",
        "unavailable",
        "rate_limit",
    ]
    for pattern in recoverable_patterns:
        if pattern in error_msg:
            return ("recoverable", True)

    return ("unknown", True)
