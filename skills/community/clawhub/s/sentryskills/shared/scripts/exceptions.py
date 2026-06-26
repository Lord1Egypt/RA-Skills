"""TrinityGuard exception hierarchy and error handling utilities."""

from __future__ import annotations

import functools
import logging
import traceback
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypeVar

# Configure logging
logger = logging.getLogger(__name__)

# Type variable for function decorators
F = TypeVar('F', bound=Callable[..., Any])


class TrinityGuardError(Exception):
    """Base exception for all TrinityGuard errors."""

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None
    ):
        """Initialize TrinityGuard error.

        Args:
            message: Human-readable error message
            details: Additional error details
            original_error: The original exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.original_error = original_error

    def __str__(self) -> str:
        """String representation."""
        base_msg = self.message
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            base_msg += f" ({details_str})"
        if self.original_error:
            base_msg += f" | Caused by: {type(self.original_error).__name__}: {self.original_error}"
        return base_msg

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging/serialization.

        Returns:
            Dictionary representation of the error
        """
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
            "original_error": str(self.original_error) if self.original_error else None,
        }


# Input/Validation Errors

class InputValidationError(TrinityGuardError):
    """Raised when input validation fails."""

    pass


class PolicyLoadError(TrinityGuardError):
    """Raised when policy loading fails."""

    pass


class PolicyValidationError(TrinityGuardError):
    """Raised when policy validation fails."""

    pass


# Detection Errors

class DetectionError(TrinityGuardError):
    """Base class for detection-related errors."""

    pass


class PatternCompilationError(DetectionError):
    """Raised when regex pattern compilation fails."""

    pass


class DetectionTimeoutError(DetectionError):
    """Raised when detection takes too long."""

    pass


# File/IO Errors

class FileReadError(TrinityGuardError):
    """Raised when file reading fails."""

    pass


class FileWriteError(TrinityGuardError):
    """Raised when file writing fails."""

    pass


class LogWriteError(TrinityGuardError):
    """Raised when log writing fails."""

    pass


# Resource Errors

class ResourceLimitError(TrinityGuardError):
    """Raised when resource limits are exceeded."""

    pass


class MemoryLimitError(ResourceLimitError):
    """Raised when memory limit is exceeded."""

    pass


class TimeoutError(TrinityGuardError):
    """Raised when operation times out."""

    pass


# Decorators for safe execution

def safe_execute(
    default_return: Any = None,
    error_type: Optional[Type[TrinityGuardError]] = None,
    log_errors: bool = True,
) -> Callable[[F], F]:
    """Decorator to safely execute a function with error handling.

    Args:
        default_return: Value to return if function fails
        error_type: Specific error type to convert to (default: DetectionError)
        log_errors: Whether to log errors

    Returns:
        Decorated function
    """
    if error_type is None:
        error_type = DetectionError

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TrinityGuardError:
                # Re-raise TrinityGuard errors as-is
                raise
            except Exception as e:
                # Convert other exceptions to specified type
                error = error_type(
                    f"Error in {func.__name__}: {str(e)}",
                    original_error=e
                )
                if log_errors:
                    logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
                if default_return is not None:
                    return default_return
                raise error
        return wrapper
    return decorator


def safe_detect(
    default_result: Optional[Dict[str, Any]] = None,
) -> Callable[[F], F]:
    """Decorator for detection functions to safely handle errors.

    Args:
        default_result: Default result to return on error

    Returns:
        Decorated function
    """
    if default_result is None:
        default_result = {"detected": False, "error": "Detection failed"}

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Detection error in {func.__name__}: {e}")
                return {
                    **default_result,
                    "error": str(e),
                    "function": func.__name__
                }
        return wrapper
    return decorator


def handle_file_errors(
    default_return: Any = None,
    operation: str = "file operation",
) -> Callable[[F], F]:
    """Decorator to handle file I/O errors.

    Args:
        default_return: Value to return if operation fails
        operation: Description of the operation

    Returns:
        Decorated function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError as e:
                error = FileReadError(
                    f"{operation} failed: file not found",
                    details={"path": str(e.filename) if e.filename else "unknown"},
                    original_error=e
                )
                logger.error(f"File not found in {func.__name__}: {e}")
                raise error
            except PermissionError as e:
                error = FileReadError(
                    f"{operation} failed: permission denied",
                    original_error=e
                )
                logger.error(f"Permission denied in {func.__name__}: {e}")
                raise error
            except OSError as e:
                error = FileReadError(
                    f"{operation} failed: I/O error",
                    details={"error_code": e.errno},
                    original_error=e
                )
                logger.error(f"I/O error in {func.__name__}: {e}")
                raise error
            except Exception as e:
                if isinstance(e, TrinityGuardError):
                    raise
                error = FileReadError(
                    f"{operation} failed: unexpected error",
                    original_error=e
                )
                logger.error(f"Unexpected error in {func.__name__}: {e}")
                if default_return is not None:
                    return default_return
                raise error
        return wrapper
    return decorator


# Error recovery utilities

class ErrorRecovery:
    """Utilities for error recovery and fallback strategies."""

    @staticmethod
    def get_fallback_policy(policy_path: Optional[Path]) -> Dict[str, Any]:
        """Get fallback policy when loading fails.

        Args:
            policy_path: Path that failed to load

        Returns:
            Default fallback policy
        """
        from self_guard_runtime_hook_template import DEFAULT_POLICY
        return dict(DEFAULT_POLICY)

    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize potentially malicious input.

        Args:
            text: Input text to sanitize

        Returns:
            Sanitized text
        """
        if not isinstance(text, str):
            return ""
        # Limit length
        if len(text) > 1_000_000:
            text = text[:1_000_000] + "... [truncated]"
        return text

    @staticmethod
    def validate_path(path: Path, must_exist: bool = False) -> bool:
        """Validate file path.

        Args:
            path: Path to validate
            must_exist: Whether path must exist

        Returns:
            True if valid

        Raises:
            FileReadError: If validation fails
        """
        if must_exist and not path.exists():
            raise FileReadError(
                f"Path does not exist: {path}",
                details={"path": str(path)}
            )
        return True


# Logging utilities

def log_error_with_context(
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    level: str = "ERROR"
) -> None:
    """Log error with additional context.

    Args:
        error: Exception to log
        context: Additional context information
        level: Log level (ERROR, WARNING, etc.)
    """
    log_func = getattr(logger, level.lower(), logger.error)

    if isinstance(error, TrinityGuardError):
        log_func(
            error.message,
            extra={
                "error_details": error.details,
                "context": context or {},
            }
        )
    else:
        log_func(
            f"Unexpected error: {type(error).__name__}: {error}",
            extra={"context": context or {}},
            exc_info=True
        )


def format_error_for_user(error: Exception) -> str:
    """Format error for user-facing display.

    Args:
        error: Exception to format

    Returns:
        User-friendly error message
    """
    if isinstance(error, TrinityGuardError):
        return error.message
    else:
        return "An unexpected error occurred. Please try again or contact support."
