from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class SyncCursor(BaseModel):
    key: str
    value: str | None = None


class TicketSummary(BaseModel):
    id: str | int
    subject: str | None = None
    status: str | None = None
    priority: str | None = None
    category: str | None = None
    account_id: str | int | None = None
    user_id: str | int | None = None
    technician_id: str | int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    closed_at: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)
