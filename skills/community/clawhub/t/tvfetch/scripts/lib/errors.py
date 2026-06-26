"""
Centralized error handler for tvfetch skill scripts.

Translates Python exceptions to tagged output that SKILL.md's recovery logic reads.
Exit codes are stable — SKILL.md maps them to specific recovery strategies.
"""

from __future__ import annotations

import sys
import traceback

# Stable exit codes — do NOT change without updating SKILL.md
EXIT_OK = 0
EXIT_GENERAL = 1
EXIT_SYMBOL_NOT_FOUND = 2
EXIT_NO_DATA = 3
EXIT_CONNECTION = 4
EXIT_AUTH = 5
EXIT_RATE_LIMIT = 6
EXIT_TIMEOUT = 7
EXIT_CONFIG = 8


def handle_error(exc: Exception, symbol: str = "", timeframe: str = "") -> int:
    """
    Print tagged error block to stderr and return appropriate exit code.
    The tags are parsed by Claude via SKILL.md STEP 6 (Error Recovery).
    """
    from tvfetch.exceptions import (
        TvSymbolNotFoundError,
        TvNoDataError,
        TvConnectionError,
        TvAuthError,
        TvRateLimitError,
        TvTimeoutError,
    )

    error_type = type(exc).__name__
    error_msg = str(exc)

    if isinstance(exc, TvSymbolNotFoundError):
        code = EXIT_SYMBOL_NOT_FOUND
        hint = "Run search to find correct symbol format"
        # Extract bare query for search suggestion
        search_query = symbol.split(":")[-1] if ":" in symbol else symbol
        print(f"ERROR_TYPE: {error_type}", file=sys.stderr)
        print(f"ERROR_SYMBOL: {symbol}", file=sys.stderr)
        print(f"ERROR_MESSAGE: {error_msg}", file=sys.stderr)
        print(f"RECOVERY_HINT: {hint}", file=sys.stderr)
        print(f"SEARCH_SUGGESTION: {search_query}", file=sys.stderr)

    elif isinstance(exc, TvNoDataError):
        code = EXIT_NO_DATA
        # Suggest next higher timeframe
        escalation = {"1": "5", "5": "15", "15": "60", "60": "1D", "1D": "1W"}
        next_tf = escalation.get(timeframe, "1D")
        print(f"ERROR_TYPE: {error_type}", file=sys.stderr)
        print(f"ERROR_SYMBOL: {symbol}", file=sys.stderr)
        print(f"ERROR_TIMEFRAME: {timeframe}", file=sys.stderr)
        print(f"ERROR_MESSAGE: {error_msg}", file=sys.stderr)
        print(f"RECOVERY_HINT: Try timeframe {next_tf}", file=sys.stderr)
        print(f"SUGGESTED_TIMEFRAME: {next_tf}", file=sys.stderr)

    elif isinstance(exc, TvConnectionError):
        code = EXIT_CONNECTION
        print(f"ERROR_TYPE: {error_type}", file=sys.stderr)
        print(f"ERROR_MESSAGE: {error_msg}", file=sys.stderr)
        print(f"RECOVERY_HINT: Retry or use --fallback-only", file=sys.stderr)

    elif isinstance(exc, TvAuthError):
        code = EXIT_AUTH
        print(f"ERROR_TYPE: {error_type}", file=sys.stderr)
        print(f"ERROR_MESSAGE: {error_msg}", file=sys.stderr)
        print(f"RECOVERY_HINT: Run auth_mgr.py test, then fall back to anonymous", file=sys.stderr)

    elif isinstance(exc, TvRateLimitError):
        code = EXIT_RATE_LIMIT
        print(f"ERROR_TYPE: {error_type}", file=sys.stderr)
        print(f"ERROR_MESSAGE: {error_msg}", file=sys.stderr)
        print(f"RECOVERY_HINT: Wait 10 seconds then retry", file=sys.stderr)

    elif isinstance(exc, TvTimeoutError):
        code = EXIT_TIMEOUT
        print(f"ERROR_TYPE: {error_type}", file=sys.stderr)
        print(f"ERROR_SYMBOL: {symbol}", file=sys.stderr)
        print(f"ERROR_MESSAGE: {error_msg}", file=sys.stderr)
        print(f"RECOVERY_HINT: Retry with fewer bars", file=sys.stderr)

    elif isinstance(exc, ValueError):
        code = EXIT_GENERAL
        print(f"ERROR_TYPE: ValueError", file=sys.stderr)
        print(f"ERROR_MESSAGE: {error_msg}", file=sys.stderr)
        print(f"RECOVERY_HINT: Check arguments", file=sys.stderr)

    else:
        code = EXIT_GENERAL
        print(f"ERROR_TYPE: {error_type}", file=sys.stderr)
        print(f"ERROR_MESSAGE: {error_msg}", file=sys.stderr)
        print(f"RECOVERY_HINT: Unexpected error", file=sys.stderr)

    return code
