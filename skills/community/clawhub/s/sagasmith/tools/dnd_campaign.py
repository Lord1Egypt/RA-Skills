"""Native campaign lifecycle management — create, list, start, and delete."""

from __future__ import annotations

import asyncio
from dataclasses import asdict
from typing import Any

from nanobot.agent.tools.base import Tool, tool_parameters
from nanobot.agent.tools.context import current_request_context
from nanobot.dnd.db.campaigns import (
    CampaignAlreadyExistsError,
    CampaignNotFoundError,
    CampaignService,
)
from nanobot.dnd.db.database import Database
from nanobot.dnd.db.module_content import ModuleImportError, ModuleImportService


@tool_parameters(
    {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["start", "create", "list", "show", "set_status", "delete"],
                "description": (
                    "start: one-shot create + initial save + optional module import. "
                    "create: only create campaign. list: list all campaigns. "
                    "show: campaign details with save count. "
                    "set_status: active/archived. delete: delete campaign."
                ),
            },
            "name": {"type": "string", "description": "Campaign display name."},
            "campaign_id": {"type": "string", "description": "Campaign ID."},
            "module_name": {"type": "string", "description": "Module label or import name."},
            "description": {"type": "string"},
            "source_path": {
                "type": "string",
                "description": "Optional module source path for start action.",
            },
            "status": {
                "type": "string",
                "enum": ["active", "archived"],
                "description": "Campaign status for set_status action.",
            },
        },
        "required": ["action"],
    }
)
class DndCampaignTool(Tool):
    """Create, inspect, and manage D&D campaign lifecycles directly (no CLI subprocess)."""

    name = "dnd_campaign"
    description = (
        "Create and manage D&D campaigns in the campaign database. "
        "Use 'start' to one-shot a new campaign (create + initial snapshot + optional module). "
        "Use 'show' to inspect campaign details including save count. "
        "Use 'set_status' to archive or reactivate a campaign."
    )
    _scopes = {"core", "subagent"}

    @classmethod
    def create(cls, ctx: Any) -> Tool:
        return cls(Database())

    def __init__(self, database: Database) -> None:
        self.database = database
        self._service = CampaignService(database)

    @property
    def read_only(self) -> bool:
        return False

    async def _execute(self, args: dict[str, Any]) -> dict[str, Any]:
        action = args["action"]
        ctx = current_request_context()

        if action == "start":
            try:
                info = self._service.start(
                    args["name"],
                    campaign_id=args.get("campaign_id"),
                    module_name=args.get("module_name"),
                    description=args.get("description"),
                    source_path=args.get("source_path"),
                )
            except CampaignAlreadyExistsError as exc:
                return {"error": "campaign_already_exists", "detail": str(exc)}
            return asdict(info)

        if action == "create":
            try:
                info = self._service.create(
                    args["name"],
                    campaign_id=args.get("campaign_id"),
                    module_name=args.get("module_name"),
                    description=args.get("description"),
                )
            except CampaignAlreadyExistsError as exc:
                return {"error": "campaign_already_exists", "detail": str(exc)}
            return asdict(info)

        if action == "list":
            status = args.get("status")
            return {
                "campaigns": [
                    asdict(info) for info in self._service.list(status=status)
                ]
            }

        if action == "show":
            try:
                info = self._service.get(args["campaign_id"])
            except CampaignNotFoundError as exc:
                return {"error": "campaign_not_found", "detail": str(exc)}
            return asdict(info)

        if action == "set_status":
            try:
                info = self._service.set_status(
                    args["campaign_id"], args["status"]
                )
            except (CampaignNotFoundError, ValueError) as exc:
                return {"error": type(exc).__name__, "detail": str(exc)}
            return asdict(info)

        if action == "delete":
            try:
                self._service.delete(args["campaign_id"])
            except CampaignNotFoundError as exc:
                return {"error": "campaign_not_found", "detail": str(exc)}
            return {"deleted": args["campaign_id"]}

        return {"error": "unknown_action", "detail": action}

    async def _execute_sync(self, args: dict[str, Any]) -> dict[str, Any]:
        return await self._execute(args)
