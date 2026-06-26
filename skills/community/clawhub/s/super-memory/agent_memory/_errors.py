"""
_errors.py — User-friendly error messages and exception classes.

Replaces raw exceptions with clear, actionable error messages
for end users.
"""

from __future__ import annotations

import logging
import traceback
from typing import Any

logger = logging.getLogger(__name__)


class AgentMemoryError(Exception):
    """Base exception for Agent Memory errors."""
    def __init__(self, message: str, hint: str = ""):
        self.message = message
        self.hint = hint
        super().__init__(message)

    def __str__(self) -> str:
        if self.hint:
            return f"{self.message}\n💡 Hint: {self.hint}"
        return self.message


class DatabaseError(AgentMemoryError):
    """Database operation failed."""
    pass


class ConfigurationError(AgentMemoryError):
    """Configuration or setup error."""
    pass


class DependencyError(AgentMemoryError):
    """Missing required dependency."""
    def __init__(self, package: str, feature: str, install_hint: str = ""):
        hint = install_hint or f"pip install {package}"
        super().__init__(
            message=f"Required package '{package}' is not installed.",
            hint=f"Install with: {hint}\nThen restart your application.",
        )
        self.package = package
        self.feature = feature


class AuthenticationError(AgentMemoryError):
    """Authentication or authorization failed."""
    pass


class MemoryNotFoundError(AgentMemoryError):
    """Requested memory not found."""
    pass


class PermissionDeniedError(AgentMemoryError):
    """Permission denied for the requested operation."""
    pass


class RateLimitError(AgentMemoryError):
    """Rate limit exceeded."""
    pass


# ── Global error handler ───────────────────────────────────────────

_USER_ERROR_MESSAGE = "Something went wrong. Please try again or check the documentation."


def handle_exception(exc: Exception, context: str = "") -> dict[str, Any]:
    """Convert any exception to a user-friendly response dict.
    
    In production, this prevents leaking internal error details.
    In debug mode, it logs the full traceback.
    """
    import os

    if isinstance(exc, AgentMemoryError):
        return {
            "error": exc.message,
            "hint": exc.hint,
            "type": exc.__class__.__name__,
        }

    if os.environ.get("DEBUG"):
        logger.error("Exception in %s: %s", context, traceback.format_exc())
        return {
            "error": str(exc),
            "type": exc.__class__.__name__,
            "trace": traceback.format_exc(),
        }

    # Production: generic message + log details
    logger.error("Unhandled exception in %s: %s", context, traceback.format_exc())
    return {
        "error": _USER_ERROR_MESSAGE,
        "hint": "If this persists, check the logs or run with DEBUG=1 for details.",
        "type": exc.__class__.__name__,
    }


def safe_execute(func, *args, default=None, context: str = ""):
    """Execute a function with error handling.
    
    Usage:
        result = safe_execute(some_function, arg1, arg2, default="fallback")
    """
    try:
        return func(*args)
    except Exception as exc:
        result = handle_exception(exc, context)
        logger.warning("safe_execute failed in %s: %s", context, result.get("error"))
        return default