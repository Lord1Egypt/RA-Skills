"""Structured errors returned to the agent."""

from __future__ import annotations

from typing import Any, Dict, Optional

# Error codes. Keep this list stable: agents may branch on them.
INVALID_JSON = "INVALID_JSON"
INVALID_REQUEST = "INVALID_REQUEST"
UNKNOWN_OP = "UNKNOWN_OP"
INVALID_PARAM = "INVALID_PARAM"
INVALID_EXPRESSION = "INVALID_EXPRESSION"
INVALID_SELECTOR = "INVALID_SELECTOR"
OBJECT_NOT_FOUND = "OBJECT_NOT_FOUND"
NAME_CONFLICT = "NAME_CONFLICT"
DEPENDENCY = "DEPENDENCY"
RECOMPUTE_FAILED = "RECOMPUTE_FAILED"
GEOMETRY_INVALID = "GEOMETRY_INVALID"
EMPTY_RESULT = "EMPTY_RESULT"
EXPECTATION_FAILED = "EXPECTATION_FAILED"
EXPORT_FAILED = "EXPORT_FAILED"
PATH_NOT_ALLOWED = "PATH_NOT_ALLOWED"
UNSUPPORTED = "UNSUPPORTED"
FREECAD_NOT_FOUND = "FREECAD_NOT_FOUND"
FREECAD_CRASHED = "FREECAD_CRASHED"
TIMEOUT = "TIMEOUT"
DOCUMENT_BUSY = "DOCUMENT_BUSY"
FREECAD_VERSION = "FREECAD_VERSION"
LIBRARY_UNAVAILABLE = "LIBRARY_UNAVAILABLE"
INTERNAL = "INTERNAL"


class SkillError(Exception):
    """An error the agent can act on.

    ``hint`` tells the agent how to fix the request; ``details`` carries
    machine-readable context (available names, measured values, ...).
    """

    def __init__(
        self,
        code: str,
        message: str,
        hint: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.hint = hint
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"code": self.code, "message": self.message}
        if self.hint:
            out["hint"] = self.hint
        if self.details:
            out["details"] = self.details
        return out


def error_response(err: SkillError, **extra: Any) -> Dict[str, Any]:
    resp: Dict[str, Any] = {"status": "error", "error": err.to_dict()}
    resp.update(extra)
    return resp
