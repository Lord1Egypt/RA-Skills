"""Native imported-module retrieval backed by campaign-scoped Dense indexes."""

from __future__ import annotations

import asyncio
from dataclasses import asdict
from typing import Any

from sqlalchemy import func, select

from nanobot.agent.tools.base import Tool, tool_parameters
from nanobot.agent.tools.context import current_request_context
from nanobot.dnd.db.database import Database
from nanobot.dnd.db.models import ModuleChunk, ModuleSource
from nanobot.dnd.db.module_content import ModuleImportService
from nanobot.dnd.db.module_progress import ModuleProgressService
from nanobot.dnd.modules.search import ModuleSearchService
from nanobot.dnd.rules.embedding import BgeM3Embedder


@tool_parameters(
    {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": [
                    "import",
                    "index",
                    "search",
                    "expand",
                    "set_scene",
                    "current",
                    "status",
                ],
            },
            "query": {"type": "string"},
            "campaign_id": {"type": "string"},
            "chunk_id": {"type": "string"},
            "top_k": {"type": "integer", "minimum": 1, "maximum": 10},
            "dense": {"type": "boolean"},
            "source_path": {"type": "string"},
            "module_name": {"type": "string"},
            "scene_id": {"type": "string"},
            "current_room": {"type": "string"},
            "explored_percent": {"type": "integer", "minimum": 0, "maximum": 100},
            "state_json": {"type": "object"},
        },
        "required": ["action"],
    }
)
class DndModuleTool(Tool):
    """Search imported module facts without loading whole chapters."""

    name = "dnd_module"
    description = (
        "Import channel attachments or local documents as campaign modules, inspect their "
        "indexes, search with lexical and BGE-M3 Dense retrieval, expand complete scenes, "
        "and persist current scene progress. "
        "BEFORE importing, always call action=index to check if the module already exists. "
        "If already imported (chapters > 0), skip import and use existing data. "
        "Only import when the module is genuinely missing or the user explicitly requests re-import."
    )
    _scopes = {"core", "subagent"}

    @classmethod
    def create(cls, ctx: Any) -> Tool:
        return cls(Database())

    def __init__(self, database: Database, *, migrate: bool = True) -> None:
        self.database = database
        self._migrate = migrate
        self._ready = False
        embedder = BgeM3Embedder()
        self.import_service = ModuleImportService(database, embedder=embedder)
        self.progress_service = ModuleProgressService(database)
        self.search_service = ModuleSearchService(database, embedder=embedder)

    @property
    def read_only(self) -> bool:
        return False

    def _ensure_ready(self) -> None:
        if not self._ready:
            if self._migrate:
                self.database.upgrade_schema()
            self._ready = True

    @staticmethod
    def _context_campaign_id() -> str | None:
        context = current_request_context()
        if context is None:
            return None
        value = context.metadata.get("campaign_id")
        return str(value) if value else None

    def _execute_sync(
        self,
        *,
        action: str,
        query: str | None,
        campaign_id: str | None,
        chunk_id: str | None,
        top_k: int,
        dense: bool,
        source_path: str | None,
        module_name: str | None,
        scene_id: str | None,
        current_room: str | None,
        explored_percent: int,
        state_json: dict[str, Any] | None,
    ) -> dict[str, Any]:
        self._ensure_ready()
        resolved_campaign = campaign_id or self._context_campaign_id()
        if action == "import":
            if not resolved_campaign:
                raise ValueError("campaign_id is required for module import")
            if not source_path and not query:
                raise ValueError("source_path or content is required for module import")
            result = self.import_service.import_path(
                resolved_campaign,
                source_path or "",
                name=module_name,
                content=query if not source_path else None,
                embed=dense,
            )
            self.search_service.clear_cache()
            return asdict(result)
        if action == "index":
            if not resolved_campaign:
                raise ValueError("campaign_id is required for module index")
            return {"modules": self.import_service.index(resolved_campaign)}
        if action == "search":
            if not resolved_campaign:
                raise ValueError("campaign_id is required for module search")
            if not query:
                raise ValueError("query is required for module search")
            hits = self.search_service.search(
                query,
                campaign_id=resolved_campaign,
                top_k=top_k,
                dense=dense,
            )
            return {"query": query, "hits": [asdict(hit) for hit in hits]}
        if action == "expand":
            if not resolved_campaign:
                raise ValueError("campaign_id is required for module expand")
            if not chunk_id:
                raise ValueError("chunk_id is required for expand")
            return self.search_service.expand(chunk_id, campaign_id=resolved_campaign)
        if action == "set_scene":
            if not resolved_campaign:
                raise ValueError("campaign_id is required for scene progress")
            if not scene_id:
                raise ValueError("scene_id is required for scene progress")
            return asdict(
                self.progress_service.set_scene(
                    resolved_campaign,
                    scene_id,
                    current_room=current_room,
                    explored_percent=explored_percent,
                    state_json=state_json,
                )
            )
        if action == "current":
            if not resolved_campaign:
                raise ValueError("campaign_id is required for current scene")
            current = self.progress_service.current(resolved_campaign)
            return {"current": asdict(current) if current else None}
        with self.database.transaction() as session:
            conditions = []
            if resolved_campaign:
                conditions.append(ModuleSource.campaign_id == resolved_campaign)
            return {
                "modules": int(
                    session.scalar(
                        select(func.count()).select_from(ModuleSource).where(*conditions)
                    )
                    or 0
                ),
                "chunks": int(
                    session.scalar(
                        select(func.count())
                        .select_from(ModuleChunk)
                        .join(ModuleSource, ModuleSource.id == ModuleChunk.module_id)
                        .where(*conditions)
                    )
                    or 0
                ),
                "embedded_chunks": int(
                    session.scalar(
                        select(func.count())
                        .select_from(ModuleChunk)
                        .join(ModuleSource, ModuleSource.id == ModuleChunk.module_id)
                        .where(*conditions, ModuleChunk.embedding_json.is_not(None))
                    )
                    or 0
                ),
            }

    async def execute(
        self,
        action: str,
        query: str | None = None,
        campaign_id: str | None = None,
        chunk_id: str | None = None,
        top_k: int = 5,
        dense: bool = True,
        source_path: str | None = None,
        module_name: str | None = None,
        scene_id: str | None = None,
        current_room: str | None = None,
        explored_percent: int = 0,
        state_json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await asyncio.to_thread(
            self._execute_sync,
            action=action,
            query=query,
            campaign_id=campaign_id,
            chunk_id=chunk_id,
            top_k=top_k,
            dense=dense,
            source_path=source_path,
            module_name=module_name,
            scene_id=scene_id,
            current_room=current_room,
            explored_percent=explored_percent,
            state_json=state_json,
        )
