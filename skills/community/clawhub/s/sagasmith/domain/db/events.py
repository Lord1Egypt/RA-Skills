"""Campaign event journal persistence operations."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from sqlalchemy import select

from .campaigns import CampaignNotFoundError
from .database import Database
from .models import Campaign, CampaignEvent, ToolAudit


@dataclass(frozen=True)
class CampaignEventInfo:
    id: str
    campaign_id: str
    session_id: str | None
    event_type: str
    content: str
    actors: list[str]
    visibility: str
    importance: int
    metadata_json: dict[str, Any]
    created_at: datetime


class CampaignEventService:
    """Append and inspect campaign-scoped narrative events."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def create(
        self,
        campaign_id: str,
        event_type: str,
        content: str,
        *,
        actors: list[str] | None = None,
        visibility: str = "party",
        importance: int = 3,
        metadata_json: dict[str, Any] | None = None,
        session_id: str | None = None,
        actor_id: str | None = None,
    ) -> CampaignEventInfo:
        event_type = event_type.strip()
        content = content.strip()
        if not event_type:
            raise ValueError("event_type must not be empty")
        if not content:
            raise ValueError("content must not be empty")
        if not 1 <= importance <= 5:
            raise ValueError("importance must be between 1 and 5")

        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            event = CampaignEvent(
                id=f"event_{uuid.uuid4().hex[:16]}",
                campaign_id=campaign_id,
                session_id=session_id,
                event_type=event_type,
                content=content,
                actors=list(actors or []),
                visibility=visibility,
                importance=importance,
                metadata_json=dict(metadata_json or {}),
            )
            session.add(event)
            session.flush()
            session.add(
                ToolAudit(
                    id=f"audit_event_{uuid.uuid4().hex[:16]}",
                    request_id=f"event-create:{uuid.uuid4().hex}",
                    campaign_id=campaign_id,
                    session_id=session_id,
                    actor_id=actor_id,
                    tool_name="dnd_event_create",
                    engine_function="database.campaign_event.create",
                    arguments_json={
                        "event_type": event_type,
                        "actors": list(actors or []),
                        "visibility": visibility,
                        "importance": importance,
                    },
                    result_json={"event_id": event.id},
                    after_state_json={
                        "content": content,
                        "metadata": dict(metadata_json or {}),
                    },
                    success=True,
                )
            )
            return self._info(event)

    def list(self, campaign_id: str, *, limit: int = 50) -> list[CampaignEventInfo]:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            statement = (
                select(CampaignEvent)
                .where(CampaignEvent.campaign_id == campaign_id)
                .order_by(CampaignEvent.created_at.desc(), CampaignEvent.id.desc())
                .limit(limit)
            )
            return [self._info(event) for event in session.scalars(statement)]

    @staticmethod
    def _info(event: CampaignEvent) -> CampaignEventInfo:
        return CampaignEventInfo(
            id=event.id,
            campaign_id=event.campaign_id,
            session_id=event.session_id,
            event_type=event.event_type,
            content=event.content,
            actors=list(event.actors or []),
            visibility=event.visibility,
            importance=event.importance,
            metadata_json=dict(event.metadata_json or {}),
            created_at=event.created_at,
        )
