"""Campaign, world, party, and character aggregates."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from .common import TimestampMixin
from ...engine import ENGINE_SOURCE_ID


class Campaign(TimestampMixin, Base):
    __tablename__ = "campaigns"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    system_version: Mapped[str] = mapped_column(String, default="D&D 5e 2024")
    module_name: Mapped[str | None] = mapped_column(String)
    engine_source: Mapped[str] = mapped_column(String, default=ENGINE_SOURCE_ID)
    engine_version: Mapped[str | None] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="active", index=True)
    description: Mapped[str | None] = mapped_column(Text)
    config: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    schema_version: Mapped[int] = mapped_column(Integer, default=2)


class WorldState(TimestampMixin, Base):
    __tablename__ = "world_states"
    __table_args__ = (UniqueConstraint("campaign_id", name="uq_world_state_campaign"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    state_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    schema_version: Mapped[int] = mapped_column(Integer, default=1)
    state_version: Mapped[int] = mapped_column(Integer, default=1)


class Party(TimestampMixin, Base):
    __tablename__ = "parties"
    __table_args__ = (UniqueConstraint("campaign_id", name="uq_party_campaign"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String, default="Adventuring Party")
    location: Mapped[str] = mapped_column(String, default="")
    shared_gold: Mapped[int] = mapped_column(Integer, default=0)
    state_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    schema_version: Mapped[int] = mapped_column(Integer, default=1)
    state_version: Mapped[int] = mapped_column(Integer, default=1)


class Character(TimestampMixin, Base):
    __tablename__ = "characters"
    __table_args__ = (
        UniqueConstraint("campaign_id", "name", name="uq_character_campaign_name"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    party_id: Mapped[str | None] = mapped_column(
        ForeignKey("parties.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    player_name: Mapped[str | None] = mapped_column(String)
    class_name: Mapped[str] = mapped_column(String, default="")
    level: Mapped[int] = mapped_column(Integer, default=1)
    hp: Mapped[int] = mapped_column(Integer, default=10)
    max_hp: Mapped[int] = mapped_column(Integer, default=10)
    armor_class: Mapped[int] = mapped_column(Integer, default=10)
    sheet_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    schema_version: Mapped[int] = mapped_column(Integer, default=1)
    state_version: Mapped[int] = mapped_column(Integer, default=1)
