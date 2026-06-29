"""Native campaign snapshot management — save, list, verify, restore, export, delete."""

from __future__ import annotations

import asyncio
from dataclasses import asdict
from typing import Any

from nanobot.agent.tools.base import Tool, tool_parameters
from nanobot.agent.tools.context import current_request_context
from nanobot.dnd.db.campaigns import CampaignNotFoundError
from nanobot.dnd.db.database import Database
from nanobot.dnd.db.snapshots import (
    CampaignSnapshotService,
    InvalidSnapshotError,
    SnapshotNotFoundError,
)


@tool_parameters(
    {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["create", "list", "verify", "restore", "delete", "export"],
                "description": (
                    "create: save current campaign state. "
                    "list: list all saves for a campaign. "
                    "verify: check snapshot integrity. "
                    "restore: load a snapshot (auto-saves current state first). "
                    "delete: remove a snapshot slot. "
                    "export: dump snapshot to a JSON file."
                ),
            },
            "campaign_id": {"type": "string", "description": "Campaign ID."},
            "slot": {
                "type": "integer",
                "description": "Snapshot slot number for verify/restore/delete/export.",
            },
            "label": {"type": "string", "description": "Human-readable save label."},
            "output": {"type": "string", "description": "Output path for export action."},
            "auto_save": {
                "type": "boolean",
                "description": "Auto-save current state before restore (default true).",
            },
        },
        "required": ["action", "campaign_id"],
    }
)
class DndSaveTool(Tool):
    """Save and restore campaign snapshots without copying module content."""

    name = "dnd_save"
    description = (
        "Create, list, verify, restore, export, and delete campaign snapshots. "
        "Snapshots contain only mutable game state — module documents and embeddings "
        "are never duplicated. Restore auto-saves current state before loading."
    )
    _scopes = {"core", "subagent"}

    @classmethod
    def create(cls, ctx: Any) -> Tool:
        return cls(Database())

    def __init__(self, database: Database) -> None:
        self.database = database
        self._service = CampaignSnapshotService(database)

    @property
    def read_only(self) -> bool:
        return False

    async def _execute(self, args: dict[str, Any]) -> dict[str, Any]:
        action = args["action"]
        campaign_id = args["campaign_id"]
        ctx = current_request_context()

        if action == "create":
            result = self._service.create(
                campaign_id,
                label=args.get("label", ""),
                actor_id=ctx.actor_id if ctx else None,
            )
            return asdict(result)

        if action == "list":
            try:
                saves = self._service.list(campaign_id)
            except CampaignNotFoundError as exc:
                return {"error": "campaign_not_found", "detail": str(exc)}
            return {"saves": [asdict(s) for s in saves]}

        if action == "verify":
            try:
                payload = self._service.get(campaign_id, args["slot"])
            except (SnapshotNotFoundError, InvalidSnapshotError) as exc:
                return {"valid": False, "error": type(exc).__name__, "detail": str(exc)}
            except CampaignNotFoundError as exc:
                return {"valid": False, "error": "campaign_not_found", "detail": str(exc)}
            return {
                "valid": True,
                "campaign_id": payload["campaign_id"],
                "schema_version": payload["schema_version"],
                "captured_at": payload["captured_at"],
            }

        if action == "restore":
            try:
                result = self._service.restore(
                    campaign_id,
                    args["slot"],
                    actor_id=ctx.actor_id if ctx else None,
                    auto_save=args.get("auto_save", True),
                )
            except (SnapshotNotFoundError, InvalidSnapshotError, CampaignNotFoundError) as exc:
                return {"error": type(exc).__name__, "detail": str(exc)}
            return asdict(result)

        if action == "delete":
            try:
                self._service.delete(campaign_id, args["slot"])
            except (SnapshotNotFoundError, CampaignNotFoundError) as exc:
                return {"error": type(exc).__name__, "detail": str(exc)}
            return {"deleted": True, "campaign_id": campaign_id, "slot": args["slot"]}

        if action == "export":
            try:
                payload = self._service.export(campaign_id, args["slot"], args["output"])
            except (SnapshotNotFoundError, CampaignNotFoundError) as exc:
                return {"error": type(exc).__name__, "detail": str(exc)}
            return {"exported": True, "output": args["output"], "slot": args["slot"]}

        return {"error": "unknown_action", "detail": action}

    async def _execute_sync(self, args: dict[str, Any]) -> dict[str, Any]:
        return await self._execute(args)
