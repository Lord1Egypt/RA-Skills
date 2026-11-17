"""Strict bool coercion for API boundaries: ``bool("false") is True`` must never happen.

Accepts real booleans, ``0``/``1``, and case-insensitive ``true/false``,
``yes/no``, ``on/off``, ``1``/``0``; rejects everything else loudly.
"""

from __future__ import annotations

from typing import Any

from ._errors import RecameraError

_TRUE = {"true", "1", "yes", "on"}
_FALSE = {"false", "0", "no", "off"}


def to_bool(value: Any, name: str = "value") -> bool:
    """Coerce *value* to ``bool`` or raise ``ValueError``."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value in (0, 1):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in _TRUE:
            return True
        if lowered in _FALSE:
            return False
    raise ValueError(
        f"{name} must be a boolean (true/false); got {value!r}."
    )


def require_confirm(confirm: Any, what: str) -> None:
    """Gate destructive operations: refuse unless explicitly confirmed."""
    if not to_bool(confirm, "confirm"):
        raise RecameraError(
            f"{what} is destructive and was NOT executed. "
            "Re-run with confirm=true only after explicit user approval."
        )
