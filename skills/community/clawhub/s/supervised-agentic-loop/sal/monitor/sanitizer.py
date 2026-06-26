"""Argument sanitization — credential leak prevention.

🔴 Dr. Neuron finding: Logger must NOT leak secrets to JSONL.
Every tool-call arg passes through sanitize_args() BEFORE logging.
"""

import re
from typing import Any

# Patterns to redact — compiled for performance
_REDACT_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"(sk-[a-zA-Z0-9]{20,})"), "sk-***REDACTED***"),
    (re.compile(r"(ghp_[a-zA-Z0-9]{36,})"), "ghp_***REDACTED***"),
    (re.compile(r"(gho_[a-zA-Z0-9]{36,})"), "gho_***REDACTED***"),
    (re.compile(r"(AKIA[A-Z0-9]{16})"), "AKIA***REDACTED***"),
    (re.compile(r"(-----BEGIN[A-Z ]*KEY-----)"), "***PEM_KEY_REDACTED***"),
    (re.compile(r"(Bearer\s+[a-zA-Z0-9._\-]{20,})"), "Bearer ***REDACTED***"),
    (re.compile(r"(?i)(password\s*[=:]\s*)\S+"), r"\1***REDACTED***"),
    (re.compile(r"(?i)(token\s*[=:]\s*)\S+"), r"\1***REDACTED***"),
    (re.compile(r"(?i)(api[_-]?key\s*[=:]\s*)\S+"), r"\1***REDACTED***"),
    (re.compile(r"(?i)(secret\s*[=:]\s*)\S+"), r"\1***REDACTED***"),
]

# Max size per field in args (bytes)
MAX_ARG_VALUE_LEN = 10_000


def _redact_string(value: str) -> str:
    """Apply all redaction patterns to a string."""
    for pattern, replacement in _REDACT_PATTERNS:
        value = pattern.sub(replacement, value)
    return value


def _truncate(value: str, max_len: int = MAX_ARG_VALUE_LEN) -> str:
    """Truncate long values with indicator."""
    if len(value) <= max_len:
        return value
    return value[:max_len] + f"...TRUNCATED({len(value)} chars)"


def sanitize_value(value: Any) -> Any:
    """Recursively sanitize a single value."""
    if isinstance(value, str):
        return _truncate(_redact_string(value))
    if isinstance(value, dict):
        return {k: sanitize_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [sanitize_value(item) for item in value]
    return value


def sanitize_args(args: dict) -> dict:
    """Deep-redact sensitive patterns from tool call arguments.

    Args:
        args: Raw tool-call arguments dict.

    Returns:
        Sanitized copy — no secrets, truncated large values.
    """
    if not isinstance(args, dict):
        return {}
    return {k: sanitize_value(v) for k, v in args.items()}


def contains_secret(text: str) -> bool:
    """Quick check: does text contain any known secret pattern?

    Useful for pre-check before logging or displaying.
    """
    for pattern, _ in _REDACT_PATTERNS:
        if pattern.search(text):
            return True
    return False
