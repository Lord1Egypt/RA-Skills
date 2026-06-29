"""External channel identities bound to campaign characters."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base
from .common import TimestampMixin


class ChannelBinding(TimestampMixin, Base):
    __tablename__ = "channel_bindings"
    __table_args__ = (
        UniqueConstraint(
            "campaign_id",
            "channel",
            "external_user_id",
            "character_id",
            name="uq_channel_binding_identity",
        ),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    campaign_id: Mapped[str] = mapped_column(
        ForeignKey("campaigns.id", ondelete="CASCADE"), index=True
    )
    channel: Mapped[str] = mapped_column(String, index=True)
    external_user_id: Mapped[str] = mapped_column(String, index=True)
    external_chat_id: Mapped[str | None] = mapped_column(String, index=True)
    character_id: Mapped[str] = mapped_column(
        ForeignKey("characters.id", ondelete="CASCADE"), index=True
    )
    display_name: Mapped[str | None] = mapped_column(String)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)
