from __future__ import annotations

import os
import sys

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
DIM = "\033[2m"


def use_color(mode: str, *, is_tty: bool | None = None) -> bool:
    if mode == "always":
        return True
    if mode == "never":
        return False
    if os.environ.get("NO_COLOR"):
        return False
    if is_tty is None:
        is_tty = sys.stdout.isatty()
    return bool(is_tty)


def colorize(text: str, *codes: str, enabled: bool) -> str:
    if not enabled or not codes:
        return text
    return "".join(codes) + text + RESET


def severity_color(severity: str) -> str:
    return {
        "critical": RED,
        "high": RED,
        "medium": YELLOW,
        "low": BLUE,
    }.get(severity, CYAN)
