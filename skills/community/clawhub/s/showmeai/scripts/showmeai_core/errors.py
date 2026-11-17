"""Stable error protocol shared by every CLI command."""

from __future__ import annotations

from typing import Any


class SkillError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        details: dict[str, Any] | None = None,
        retryable: bool = False,
        exit_code: int = 1,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}
        self.retryable = retryable
        self.exit_code = exit_code

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
            "retryable": self.retryable,
        }
        if self.details:
            payload["details"] = self.details
        return payload


class HttpError(SkillError):
    def __init__(self, status: int, message: str, *, body: str = "", retryable: bool = False) -> None:
        safe_body = body[:1200]
        super().__init__(
            "HTTP_ERROR",
            message,
            details={"status": status, "body": safe_body},
            retryable=retryable,
        )
        self.status = status
        self.body = safe_body


def error_result(error: Exception) -> dict[str, Any]:
    if isinstance(error, SkillError):
        return {"ok": False, "error": error.as_dict()}
    return {
        "ok": False,
        "error": {
            "code": "UNEXPECTED_ERROR",
            "message": "Unexpected internal error. Run `doctor`, verify the inputs, and retry.",
            "retryable": False,
            "details": {"type": type(error).__name__},
        },
    }
