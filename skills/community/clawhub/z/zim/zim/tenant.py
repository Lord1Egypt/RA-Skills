"""Tenant model for the Zim Admin Control Plane."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class TenantSettings(BaseModel):
    """Per-tenant configuration knobs."""

    default_policy_id: Optional[str] = None
    default_currency: str = "USD"
    approval_required: bool = False
    max_trip_budget_usd: float = 10000.0
    # Fee schedule override — dict matching FeeSchedule fields.
    # If None, the system-wide DEFAULT_FEE_SCHEDULE applies.
    fee_config: Optional[dict[str, Any]] = None


class Tenant(BaseModel):
    """A Zim tenant (organisation / company account)."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    name: str
    domain: str = ""
    settings: TenantSettings = Field(default_factory=TenantSettings)
    is_deleted: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
