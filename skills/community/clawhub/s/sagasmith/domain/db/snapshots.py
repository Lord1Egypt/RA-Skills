"""Complete, campaign-scoped database snapshots and transactional restoration."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from .database import Database
from .models import (
    Campaign,
    CampaignEvent,
    CampaignSave,
    ChannelBinding,
    Character,
    Combat,
    ModuleChapter,
    Party,
    PlotSummary,
    SceneIndex,
    SceneState,
    StateRevision,
    ToolAudit,
    WorldState,
)

SNAPSHOT_FORMAT = "dnd-campaign-snapshot"
SNAPSHOT_SCHEMA_VERSION = 3
SUPPORTED_SNAPSHOT_SCHEMA_VERSIONS = {2, SNAPSHOT_SCHEMA_VERSION}


from .campaigns import CampaignNotFoundError


class SnapshotError(RuntimeError):
    """Base error for campaign snapshot operations."""


class SnapshotNotFoundError(SnapshotError):
    """The requested campaign save slot does not exist."""


class InvalidSnapshotError(SnapshotError):
    """The stored payload is not a supported complete campaign snapshot."""


@dataclass(frozen=True)
class SnapshotInfo:
    id: str
    campaign_id: str
    slot: int
    label: str
    chapter: str
    location: str
    snapshot_hash: str
    created_at: datetime


@dataclass(frozen=True)
class RestoreResult:
    campaign_id: str
    slot: int
    audit_id: str
    state_version: int


_CAMPAIGN_FIELDS = (
    "name",
    "system_version",
    "module_name",
    "engine_source",
    "engine_version",
    "status",
    "description",
    "config",
    "schema_version",
)

_STATE_MODELS: tuple[tuple[str, type, tuple[str, ...]], ...] = (
    (
        "world_states",
        WorldState,
        ("id", "campaign_id", "state_json", "schema_version", "state_version"),
    ),
    (
        "parties",
        Party,
        (
            "id",
            "campaign_id",
            "name",
            "location",
            "shared_gold",
            "state_json",
            "schema_version",
            "state_version",
        ),
    ),
    (
        "characters",
        Character,
        (
            "id",
            "campaign_id",
            "party_id",
            "name",
            "player_name",
            "class_name",
            "level",
            "hp",
            "max_hp",
            "armor_class",
            "sheet_json",
            "schema_version",
            "state_version",
        ),
    ),
    (
        "combats",
        Combat,
        (
            "id",
            "campaign_id",
            "name",
            "location",
            "round_number",
            "current_turn",
            "is_active",
            "result",
            "environment_json",
            "state_json",
            "schema_version",
            "state_version",
        ),
    ),
    (
        "plot_summaries",
        PlotSummary,
        (
            "id",
            "campaign_id",
            "scope",
            "scope_id",
            "summary",
            "open_threads",
            "schema_version",
        ),
    ),
    (
        "campaign_events",
        CampaignEvent,
        (
            "id",
            "campaign_id",
            "session_id",
            "event_type",
            "content",
            "actors",
            "visibility",
            "importance",
            "metadata_json",
            "created_at",
        ),
    ),
    (
        "scene_states",
        SceneState,
        (
            "id",
            "campaign_id",
            "scene_id",
            "current_room",
            "explored_percent",
            "state_json",
            "schema_version",
            "state_version",
        ),
    ),
    (
        "channel_bindings",
        ChannelBinding,
        (
            "id",
            "campaign_id",
            "channel",
            "external_user_id",
            "external_chat_id",
            "character_id",
            "display_name",
            "metadata_json",
        ),
    ),
)

_MODULE_CHILD_MODELS: tuple[tuple[str, type, tuple[str, ...]], ...] = (
    (
        "module_chapters",
        ModuleChapter,
        ("id", "module_id", "chapter_key", "title", "source_path", "order_index", "status", "metadata_json"),
    ),
    (
        "scene_indexes",
        SceneIndex,
        ("id", "chapter_id", "scene_key", "title", "start_line", "end_line", "headings", "keywords"),
    ),
)


def _json_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _row(model: Any, fields: tuple[str, ...]) -> dict[str, Any]:
    return {field: _json_value(getattr(model, field)) for field in fields}


def _snapshot_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _assert_active(campaign: Campaign) -> None:
    if campaign.status == "archived":
        raise SnapshotError(
            f"campaign is archived; reactivate before saving or loading: {campaign.id}"
        )


class CampaignSnapshotService:
    """Save and restore mutable campaign progress without copying module content."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def create(
        self,
        campaign_id: str,
        *,
        label: str = "",
        actor_id: str | None = None,
    ) -> SnapshotInfo:
        with self.database.transaction() as session:
            campaign = self._campaign(session, campaign_id, lock=True)
            _assert_active(campaign)
            return self._create_in_session(
                session, campaign_id, label=label, campaign_name=campaign.name,
                actor_id=actor_id,
            )

    def _create_in_session(
        self,
        session: Session,
        campaign_id: str,
        *,
        label: str = "",
        campaign_name: str = "",
        actor_id: str | None = None,
    ) -> SnapshotInfo:
        """Create a snapshot row inside an already-open *session*."""
        payload = self.capture_from_session(session, campaign_id)
        slot = int(
            session.scalar(
                select(func.coalesce(func.max(CampaignSave.slot), 0)).where(
                    CampaignSave.campaign_id == campaign_id
                )
            )
            or 0
        ) + 1
        world = payload["state"]["world_states"]
        world_json = world[0].get("state_json", {}) if world else {}
        party = payload["state"]["parties"]
        location = (party[0].get("location") if party else None) or world_json.get(
            "current_scene", ""
        )
        chapter = str(world_json.get("current_chapter", ""))
        save = CampaignSave(
            id=f"save_{uuid.uuid4().hex}",
            campaign_id=campaign_id,
            slot=slot,
            label=label or f"{campaign_name} #{slot}",
            chapter=chapter,
            location=location or "",
            snapshot_json=payload,
            snapshot_format=SNAPSHOT_FORMAT,
            snapshot_hash=_snapshot_hash(payload),
            created_by=actor_id,
            schema_version=SNAPSHOT_SCHEMA_VERSION,
            state_version=self._snapshot_state_version(payload),
        )
        session.add(save)
        session.flush()
        return self._info(save)

    def list(self, campaign_id: str) -> list[SnapshotInfo]:
        with self.database.transaction() as session:
            self._campaign(session, campaign_id)
            saves = session.scalars(
                select(CampaignSave)
                .where(CampaignSave.campaign_id == campaign_id)
                .order_by(CampaignSave.slot)
            )
            return [self._info(save) for save in saves]

    def get(self, campaign_id: str, slot: int) -> dict[str, Any]:
        with self.database.transaction() as session:
            save = self._save(session, campaign_id, slot)
            return self._validated_payload(save, campaign_id)

    def restore(
        self,
        campaign_id: str,
        slot: int,
        *,
        actor_id: str | None = None,
        session_id: str | None = None,
        request_id: str | None = None,
        auto_save: bool = True,
    ) -> RestoreResult:
        if auto_save:
            try:
                self.create(campaign_id, label="auto-before-restore", actor_id=actor_id)
            except Exception:
                pass  # Non-fatal if auto-save fails
        with self.database.transaction() as session:
            campaign = self._campaign(session, campaign_id, lock=True)
            _assert_active(campaign)
            save = self._save(session, campaign_id, slot)
            payload = self._validated_payload(save, campaign_id)
            before = self.capture_from_session(session, campaign_id)
            self.restore_in_session(session, payload, expected_campaign_id=campaign_id)
            after = self.capture_from_session(session, campaign_id)

            audit_id = f"audit_restore_{uuid.uuid4().hex}"
            revision_version = self.next_revision_version(session, campaign_id)
            session.add(
                ToolAudit(
                    id=audit_id,
                    request_id=request_id or f"snapshot-restore:{uuid.uuid4().hex}",
                    campaign_id=campaign_id,
                    session_id=session_id,
                    actor_id=actor_id,
                    tool_name="dnd_load_snapshot",
                    engine_function="database.snapshot.restore",
                    arguments_json={"slot": slot, "save_id": save.id},
                    result_json={"slot": slot, "snapshot_hash": save.snapshot_hash},
                    before_state_json={"snapshot_hash": _snapshot_hash(before)},
                    after_state_json={"snapshot_hash": _snapshot_hash(after)},
                    success=True,
                    state_version=revision_version,
                )
            )
            session.flush()
            session.add(
                StateRevision(
                    id=f"revision_restore_{uuid.uuid4().hex}",
                    campaign_id=campaign_id,
                    tool_audit_id=audit_id,
                    actor_id=actor_id,
                    aggregate_type="campaign_snapshot",
                    aggregate_key="default",
                    engine_function="database.snapshot.restore",
                    state_version=revision_version,
                    before_state_json=before,
                    after_state_json=after,
                )
            )
            return RestoreResult(campaign_id, slot, audit_id, revision_version)

    def delete(self, campaign_id: str, slot: int) -> None:
        with self.database.transaction() as session:
            self._campaign(session, campaign_id)
            save = self._save(session, campaign_id, slot)
            session.delete(save)

    def export(self, campaign_id: str, slot: int, output_path: str | Path) -> dict[str, Any]:
        payload = self.get(campaign_id, slot)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        return payload

    @classmethod
    def capture_from_session(cls, session: Session, campaign_id: str) -> dict[str, Any]:
        campaign = cls._campaign(session, campaign_id)
        state: dict[str, list[dict[str, Any]]] = {}
        for key, model, fields in _STATE_MODELS:
            state[key] = [
                _row(item, fields)
                for item in session.scalars(
                    select(model).where(model.campaign_id == campaign_id).order_by(model.id)
                )
            ]

        return {
            "format": SNAPSHOT_FORMAT,
            "schema_version": SNAPSHOT_SCHEMA_VERSION,
            "campaign_id": campaign_id,
            "captured_at": datetime.now(UTC).isoformat(),
            "campaign": {field: _json_value(getattr(campaign, field)) for field in _CAMPAIGN_FIELDS},
            "state": state,
        }

    @classmethod
    def restore_in_session(
        cls,
        session: Session,
        payload: dict[str, Any],
        *,
        expected_campaign_id: str | None = None,
    ) -> None:
        cls.validate(payload, expected_campaign_id=expected_campaign_id)
        campaign_id = payload["campaign_id"]
        campaign = cls._campaign(session, campaign_id, lock=True)
        for field in _CAMPAIGN_FIELDS:
            if field in payload["campaign"]:
                setattr(campaign, field, payload["campaign"][field])

        state = payload["state"]
        # Delete mutable progress in foreign-key order. Immutable module documents,
        # chapter metadata, and scene indexes are deliberately retained.
        session.execute(delete(ChannelBinding).where(ChannelBinding.campaign_id == campaign_id))
        session.execute(delete(SceneState).where(SceneState.campaign_id == campaign_id))
        session.execute(delete(CampaignEvent).where(CampaignEvent.campaign_id == campaign_id))
        session.execute(delete(PlotSummary).where(PlotSummary.campaign_id == campaign_id))
        session.execute(delete(Combat).where(Combat.campaign_id == campaign_id))
        session.execute(delete(Character).where(Character.campaign_id == campaign_id))
        session.execute(delete(Party).where(Party.campaign_id == campaign_id))
        session.execute(delete(WorldState).where(WorldState.campaign_id == campaign_id))

        model_by_key = {key: (model, fields) for key, model, fields in _STATE_MODELS}
        insert_order = (
            "world_states",
            "parties",
            "characters",
            "combats",
            "plot_summaries",
            "campaign_events",
            "scene_states",
            "channel_bindings",
        )
        for key in insert_order:
            model, fields = model_by_key[key]
            for raw in state[key]:
                values = {field: raw.get(field) for field in fields}
                if key == "campaign_events" and isinstance(values.get("created_at"), str):
                    values["created_at"] = datetime.fromisoformat(values["created_at"])
                session.add(model(**values))
            session.flush()

    @staticmethod
    def validate(
        payload: dict[str, Any], *, expected_campaign_id: str | None = None
    ) -> None:
        if payload.get("format") != SNAPSHOT_FORMAT:
            raise InvalidSnapshotError("unsupported snapshot format")
        schema_version = payload.get("schema_version")
        if schema_version not in SUPPORTED_SNAPSHOT_SCHEMA_VERSIONS:
            raise InvalidSnapshotError(
                f"unsupported snapshot schema version: {schema_version}"
            )
        campaign_id = payload.get("campaign_id")
        if not isinstance(campaign_id, str) or not campaign_id:
            raise InvalidSnapshotError("snapshot campaign_id is missing")
        if expected_campaign_id is not None and campaign_id != expected_campaign_id:
            raise InvalidSnapshotError("snapshot belongs to a different campaign")
        if not isinstance(payload.get("campaign"), dict) or not isinstance(
            payload.get("state"), dict
        ):
            raise InvalidSnapshotError("snapshot campaign state is malformed")
        required = {key for key, _, _ in _STATE_MODELS}
        if schema_version == 2:
            required |= {"module_sources"} | {
                key for key, _, _ in _MODULE_CHILD_MODELS
            }
        missing = required - payload["state"].keys()
        if missing:
            raise InvalidSnapshotError(
                "snapshot is missing state collections: " + ", ".join(sorted(missing))
            )
        if any(not isinstance(payload["state"][key], list) for key in required):
            raise InvalidSnapshotError("snapshot state collections must be arrays")

    @staticmethod
    def next_revision_version(session: Session, campaign_id: str) -> int:
        return int(
            session.scalar(
                select(func.coalesce(func.max(StateRevision.state_version), 0)).where(
                    StateRevision.campaign_id == campaign_id,
                    StateRevision.aggregate_type == "campaign_snapshot",
                    StateRevision.aggregate_key == "default",
                )
            )
            or 0
        ) + 1

    @staticmethod
    def _snapshot_state_version(payload: dict[str, Any]) -> int:
        versions = [
            int(row.get("state_version", 1))
            for rows in payload["state"].values()
            for row in rows
            if isinstance(row, dict) and row.get("state_version") is not None
        ]
        return max(versions, default=1)

    @staticmethod
    def _campaign(session: Session, campaign_id: str, *, lock: bool = False) -> Campaign:
        statement = select(Campaign).where(Campaign.id == campaign_id)
        if lock:
            statement = statement.with_for_update()
        campaign = session.scalar(statement)
        if campaign is None:
            raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
        return campaign

    @staticmethod
    def _save(session: Session, campaign_id: str, slot: int) -> CampaignSave:
        save = session.scalar(
            select(CampaignSave).where(
                CampaignSave.campaign_id == campaign_id,
                CampaignSave.slot == slot,
            )
        )
        if save is None:
            raise SnapshotNotFoundError(
                f"snapshot not found: campaign={campaign_id}, slot={slot}"
            )
        return save

    @classmethod
    def _validated_payload(
        cls, save: CampaignSave, campaign_id: str
    ) -> dict[str, Any]:
        payload = dict(save.snapshot_json)
        if save.snapshot_format != SNAPSHOT_FORMAT:
            raise InvalidSnapshotError("stored snapshot format metadata is unsupported")
        cls.validate(payload, expected_campaign_id=campaign_id)
        actual_hash = _snapshot_hash(payload)
        if not save.snapshot_hash or save.snapshot_hash != actual_hash:
            raise InvalidSnapshotError("snapshot checksum mismatch")
        return payload

    @staticmethod
    def _info(save: CampaignSave) -> SnapshotInfo:
        return SnapshotInfo(
            id=save.id,
            campaign_id=save.campaign_id,
            slot=save.slot,
            label=save.label,
            chapter=save.chapter,
            location=save.location,
            snapshot_hash=save.snapshot_hash,
            created_at=save.created_at,
        )
