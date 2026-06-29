"""Audit-backed restoration of D&D engine state."""

from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Database
from .models import (
    Character,
    Combat,
    Party,
    SceneState,
    StateRevision,
    ToolAudit,
    WorldState,
)

DEFAULT_UNDO_LIMIT = 20


class UndoError(RuntimeError):
    """Base error for audit-backed undo operations."""


class UndoLimitExceededError(UndoError):
    """Requested undo count exceeds the configured safety limit."""


class NothingToUndoError(UndoError):
    """No reversible audit records remain for the campaign."""


class UnsupportedAggregateError(UndoError):
    """A revision references a state aggregate the adapter cannot restore."""


@dataclass(frozen=True)
class UndoResult:
    reverted_audit_ids: tuple[str, ...]
    undo_audit_ids: tuple[str, ...]

    @property
    def count(self) -> int:
        return len(self.reverted_audit_ids)


class UndoManager:
    """Restore complete engine-owned JSON aggregates from append-only revisions."""

    def __init__(self, database: Database, *, max_undo: int | None = None) -> None:
        configured = os.environ.get("DND_AUDIT_UNDO_LIMIT")
        limit = max_undo if max_undo is not None else int(configured or DEFAULT_UNDO_LIMIT)
        if limit < 1:
            raise ValueError("max_undo must be at least 1")
        self.database = database
        self.max_undo = limit

    def undo(self, campaign_id: str, *, count: int = 1, actor_id: str | None = None) -> UndoResult:
        if count < 1:
            raise ValueError("count must be at least 1")
        if count > self.max_undo:
            raise UndoLimitExceededError(
                f"requested {count} undo operations, configured limit is {self.max_undo}"
            )

        reverted: list[str] = []
        undo_audits: list[str] = []
        with self.database.transaction() as session:
            candidates = self._reversible_audits(session, campaign_id, count)
            if not candidates:
                raise NothingToUndoError(
                    f"no reversible audits remain for campaign {campaign_id}"
                )

            for original in candidates:
                revisions = list(
                    session.scalars(
                        select(StateRevision)
                        .where(StateRevision.tool_audit_id == original.id)
                        .order_by(StateRevision.created_at.desc(), StateRevision.id.desc())
                    )
                )
                if not revisions:
                    continue

                undo_id = f"audit_undo_{uuid.uuid4().hex[:16]}"
                undo_request_id = f"undo:{uuid.uuid4().hex}"
                restored: list[dict[str, Any]] = []
                reverse_revisions: list[StateRevision] = []

                for revision in revisions:
                    current, next_version = self._restore_revision(session, revision)
                    reverse_revision = StateRevision(
                        id=f"revision_undo_{uuid.uuid4().hex[:16]}",
                        campaign_id=campaign_id,
                        tool_audit_id=undo_id,
                        actor_id=actor_id,
                        aggregate_type=revision.aggregate_type,
                        aggregate_key=revision.aggregate_key,
                        engine_function="audit.restore_state",
                        state_version=next_version,
                        before_state_json=current,
                        after_state_json=revision.before_state_json or {},
                    )
                    reverse_revisions.append(reverse_revision)
                    restored.append(
                        {
                            "aggregate_type": revision.aggregate_type,
                            "aggregate_key": revision.aggregate_key,
                            "state_version": next_version,
                        }
                    )

                session.add(
                    ToolAudit(
                        id=undo_id,
                        request_id=undo_request_id,
                        campaign_id=campaign_id,
                        reverts_audit_id=original.id,
                        actor_id=actor_id,
                        tool_name="dnd_undo",
                        engine_function="audit.restore_state",
                        arguments_json={"audit_id": original.id},
                        result_json={"restored": restored},
                        success=True,
                    )
                )
                session.flush()
                session.add_all(reverse_revisions)
                reverted.append(original.id)
                undo_audits.append(undo_id)

        if not reverted:
            raise NothingToUndoError(f"no reversible audits remain for campaign {campaign_id}")
        return UndoResult(tuple(reverted), tuple(undo_audits))

    @staticmethod
    def _reversible_audits(session: Session, campaign_id: str, count: int) -> list[ToolAudit]:
        reverted_ids = select(ToolAudit.reverts_audit_id).where(
            ToolAudit.reverts_audit_id.is_not(None)
        )
        statement = (
            select(ToolAudit)
            .join(StateRevision, StateRevision.tool_audit_id == ToolAudit.id)
            .where(
                ToolAudit.campaign_id == campaign_id,
                ToolAudit.success.is_(True),
                ToolAudit.reverts_audit_id.is_(None),
                ToolAudit.id.not_in(reverted_ids),
            )
            .distinct()
            .order_by(ToolAudit.created_at.desc(), ToolAudit.id.desc())
            .limit(count)
        )
        return list(session.scalars(statement))

    @staticmethod
    def _find_aggregate(session: Session, revision: StateRevision):
        model_by_type = {
            "world": WorldState,
            "party": Party,
            "character": Character,
            "combat": Combat,
            "scene": SceneState,
        }
        model = model_by_type.get(revision.aggregate_type)
        if model is None:
            raise UnsupportedAggregateError(
                f"unsupported aggregate type: {revision.aggregate_type}"
            )

        if revision.aggregate_key != "default":
            aggregate = session.get(model, revision.aggregate_key)
        elif model is Combat:
            aggregate = session.scalar(
                select(Combat).where(
                    Combat.campaign_id == revision.campaign_id,
                    Combat.is_active.is_(True),
                )
            )
        else:
            aggregate = session.scalar(
                select(model).where(model.campaign_id == revision.campaign_id)
            )
        if aggregate is None:
            raise UndoError(
                f"aggregate not found: {revision.aggregate_type}:{revision.aggregate_key}"
            )
        return aggregate

    def _restore_revision(
        self, session: Session, revision: StateRevision
    ) -> tuple[dict[str, Any], int]:
        if revision.aggregate_type == "campaign_snapshot":
            from .snapshots import CampaignSnapshotService

            current = CampaignSnapshotService.capture_from_session(
                session, revision.campaign_id
            )
            CampaignSnapshotService.restore_in_session(
                session,
                dict(revision.before_state_json or {}),
                expected_campaign_id=revision.campaign_id,
            )
            next_version = CampaignSnapshotService.next_revision_version(
                session, revision.campaign_id
            )
            session.flush()
            return current, next_version

        aggregate = self._find_aggregate(session, revision)
        payload = dict(revision.before_state_json or {})
        state_attribute = "sheet_json" if isinstance(aggregate, Character) else "state_json"
        current = dict(getattr(aggregate, state_attribute) or {})
        setattr(aggregate, state_attribute, payload)

        if isinstance(aggregate, Character):
            aggregate.name = payload.get("name", aggregate.name)
            aggregate.class_name = payload.get("class", aggregate.class_name)
            aggregate.level = int(payload.get("level", aggregate.level))
            aggregate.hp = int(payload.get("hp", aggregate.hp))
            aggregate.max_hp = int(payload.get("maxHp", aggregate.max_hp))
            aggregate.armor_class = int(payload.get("ac", aggregate.armor_class))
        elif isinstance(aggregate, Party):
            aggregate.location = payload.get("location", aggregate.location)
            aggregate.shared_gold = int(payload.get("gold", aggregate.shared_gold))
        elif isinstance(aggregate, Combat):
            aggregate.location = payload.get("location", aggregate.location)
            aggregate.round_number = int(payload.get("round", aggregate.round_number))
            aggregate.current_turn = int(payload.get("current_turn", aggregate.current_turn))
            aggregate.is_active = bool(payload.get("is_active", aggregate.is_active))
            aggregate.result = payload.get("result", aggregate.result)
            aggregate.environment_json = payload.get("environment", aggregate.environment_json)
        elif isinstance(aggregate, SceneState):
            aggregate.current_room = payload.get("current_room", aggregate.current_room)
            aggregate.explored_percent = int(
                payload.get("explored_percent", aggregate.explored_percent)
            )

        next_version = int(aggregate.state_version) + 1
        aggregate.state_version = next_version
        session.flush()
        return current, next_version
