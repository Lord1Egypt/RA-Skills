"""Deterministic dice and tool execution audit records."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    event,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from .common import utc_now


class DiceRoll(Base):
    __tablename__ = "dice_rolls"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    request_id: Mapped[str | None] = mapped_column(String, index=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    character_id: Mapped[str | None] = mapped_column(
        ForeignKey("characters.id", ondelete="SET NULL"), index=True
    )
    formula: Mapped[str] = mapped_column(String)
    result: Mapped[int] = mapped_column(Integer)
    detail_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    context: Mapped[str] = mapped_column(Text, default="")
    tool_name: Mapped[str] = mapped_column(String, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class ToolAudit(Base):
    __tablename__ = "tool_audits"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    request_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    campaign_id: Mapped[str | None] = mapped_column(
        ForeignKey("campaigns.id", ondelete="SET NULL"), index=True
    )
    reverts_audit_id: Mapped[str | None] = mapped_column(
        ForeignKey("tool_audits.id", ondelete="RESTRICT"), unique=True, index=True
    )
    session_id: Mapped[str | None] = mapped_column(String, index=True)
    actor_id: Mapped[str | None] = mapped_column(String, index=True)
    tool_name: Mapped[str] = mapped_column(String, index=True)
    engine_function: Mapped[str | None] = mapped_column(String, index=True)
    arguments_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    result_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    before_state_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    after_state_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    success: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    error: Mapped[str | None] = mapped_column(Text)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    state_version: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


class StateRevision(Base):
    """Append-only record of state written after a bundled dnd_engine call."""

    __tablename__ = "state_revisions"
    __table_args__ = (
        UniqueConstraint(
            "campaign_id",
            "aggregate_type",
            "aggregate_key",
            "state_version",
            name="uq_state_revision_version",
        ),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    tool_audit_id: Mapped[str | None] = mapped_column(
        ForeignKey("tool_audits.id", ondelete="SET NULL"), index=True
    )
    actor_id: Mapped[str | None] = mapped_column(String, index=True)
    aggregate_type: Mapped[str] = mapped_column(String, index=True)
    aggregate_key: Mapped[str] = mapped_column(String, default="default")
    engine_function: Mapped[str] = mapped_column(String)
    state_version: Mapped[int] = mapped_column(Integer)
    before_state_json: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    after_state_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)


def _reject_audit_mutation(_mapper, _connection, target) -> None:
    raise RuntimeError(f"{type(target).__name__} records are append-only")


for _audit_model in (DiceRoll, ToolAudit, StateRevision):
    event.listen(_audit_model, "before_update", _reject_audit_mutation)
    event.listen(_audit_model, "before_delete", _reject_audit_mutation)
