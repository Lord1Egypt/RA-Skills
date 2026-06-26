"""Structured error handling with semantic exit codes."""

import json
import sys
from enum import IntEnum
from typing import NoReturn

import typer


class ExitCode(IntEnum):
    SUCCESS = 0
    API_ERROR = 1
    CONFIG_ERROR = 2
    AUTH_ERROR = 3
    NOT_FOUND = 4
    VALIDATION_ERROR = 5


def handle_error(
    code: ExitCode,
    message: str,
    detail: str = "",
    hint: str = "",
    intuit_tid: str = "",
) -> NoReturn:
    """Print structured error JSON to stderr and exit with semantic code."""
    error_obj: dict = {
        "error": True,
        "code": code.value,
        "message": message,
    }
    if detail:
        error_obj["detail"] = detail
    if hint:
        error_obj["hint"] = hint
    if intuit_tid:
        error_obj["intuit_tid"] = intuit_tid

    typer.echo(json.dumps(error_obj, indent=2), err=True)
    raise SystemExit(code.value)
