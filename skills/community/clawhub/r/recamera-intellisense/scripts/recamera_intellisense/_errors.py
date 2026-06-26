"""Shared error type for all SDK-level failures."""

from __future__ import annotations


class RecameraError(RuntimeError):
    """Device / config / connectivity failure. Carries HTTP ``status``, device ``code``, raw ``body``."""

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        code: int | None = None,
        body: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.body = body[:2048] if isinstance(body, str) else body
