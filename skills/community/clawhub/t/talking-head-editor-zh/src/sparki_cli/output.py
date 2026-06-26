"""Unified JSON output formatter for all CLI commands."""

import json
import sys
from typing import Any

from sparki_cli.constants import ERROR_CODES


def success(data: dict[str, Any]) -> str:
    return json.dumps({"ok": True, "data": data, "error": None}, ensure_ascii=False)


def format_error(code: str, message: str | None = None) -> dict[str, str]:
    defaults = ERROR_CODES.get(code, {
        "message": "An unexpected error occurred",
        "action": "Please try again or contact support",
    })
    return {
        "code": code,
        "message": message or defaults["message"],
        "action": defaults["action"],
    }


def error(code: str, message: str | None = None) -> str:
    return json.dumps(
        {"ok": False, "data": None, "error": format_error(code, message)},
        ensure_ascii=False,
    )


def print_success(data: dict[str, Any]) -> None:
    print(success(data))


def print_error(code: str, message: str | None = None) -> None:
    print(error(code, message))


def log(msg: str) -> None:
    print(msg, file=sys.stderr)
