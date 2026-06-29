"""Combat, save, summary, and event state."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from .common import TimestampMixin, utc_now


class Combat(TimestampMixin, Base):
    __tablename__ = "combats"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String, default="")
    round_number: Mapped[int] = mapped_column(Integer, default=1)
    current_turn: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    result: Mapped[str | None] = mapped_column(String)
    environment_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    state_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    schema_version: Mapped[int] = mapped_column(Integer, default=1)
    state_version: Mapped[int] = mapped_column(Integer, default=1)


class CampaignSave(TimestampMixin, Base):
    __tablename__ = "campaign_saves"
    __table_args__ = (
        UniqueConstraint("campaign_id", "slot", name="uq_campaign_save_slot"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    slot: Mapped[int] = mapped_column(Integer)
    label: Mapped[str] = mapped_column(String, default="")
    chapter: Mapped[str] = mapped_column(String, default="")
    location: Mapped[str] = mapped_column(String, default="")
    snapshot_json: Mapped[dict[str, Any]] = mapped_column(JSON)
    snapshot_format: Mapped[str] = mapped_column(
        String, default="dnd-campaign-snapshot"
    )
    snapshot_hash: Mapped[str] = mapped_column(String, default="")
    created_by: Mapped[str | None] = mapped_column(String, index=True)
    schema_version: Mapped[int] = mapped_column(Integer, default=2)
    state_version: Mapped[int] = mapped_column(Integer, default=1)


class PlotSummary(TimestampMixin, Base):
    __tablename__ = "plot_summaries"
    __table_args__ = (
        UniqueConstraint("campaign_id", "scope", "scope_id", name="uq_plot_summary_scope"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    scope: Mapped[str] = mapped_column(String, default="campaign")
    scope_id: Mapped[str | None] = mapped_column(String)
    summary: Mapped[str] = mapped_column(Text)
    open_threads: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    schema_version: Mapped[int] = mapped_column(Integer, default=1)


class CampaignEvent(Base):
    __tablename__ = "campaign_events"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    session_id: Mapped[str | None] = mapped_column(String, index=True)
    event_type: Mapped[str] = mapped_column(String, index=True)
    content: Mapped[str] = mapped_column(Text)
    actors: Mapped[list[str]] = mapped_column(JSON, default=list)
    visibility: Mapped[str] = mapped_column(String, default="party", index=True)
    importance: Mapped[int] = mapped_column(Integer, default=3)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)
