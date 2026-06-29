"""Native D&D rule retrieval backed by the campaign rules database."""

from __future__ import annotations

import asyncio
from dataclasses import asdict
from typing import Any

from sqlalchemy import func, select

from nanobot.agent.tools.base import Tool, tool_parameters
from nanobot.agent.tools.context import current_request_context
from nanobot.dnd.db.database import Database
from nanobot.dnd.db.models import RuleChunk, RulePublication, RuleSet
from nanobot.dnd.rules.embedding import BgeM3Embedder
from nanobot.dnd.rules.search import RuleSearchService


@tool_parameters(
    {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["search", "expand", "status"],
                "description": "Search rules, expand a result, or inspect the rule index.",
            },
            "query": {"type": "string", "description": "Rule question or exact rule name."},
            "campaign_id": {
                "type": "string",
                "description": "Optional campaign whose pinned rule versions must be used.",
            },
            "chunk_id": {"type": "string", "description": "Chunk returned by search."},
            "top_k": {"type": "integer", "minimum": 1, "maximum": 10},
            "dense": {"type": "boolean"},
            "expand_mode": {
                "type": "string",
                "enum": ["chunk", "paragraph", "section", "section-with-children"],
            },
        },
        "required": ["action"],
    }
)
class DndRulesTool(Tool):
    """Search the indexed SRD without spawning a fresh Python process per query."""

    name = "dnd_rules"
    description = (
        "Search the versioned D&D rules database with exact, full-text, and BGE-M3 dense "
        "retrieval. Use campaign_id when adjudicating a campaign so only its pinned rules "
        "and supplements are searched. Expand a returned chunk before quoting a full rule."
    )
    _scopes = {"core", "subagent"}

    @classmethod
    def create(cls, ctx: Any) -> Tool:
        return cls(Database())

    def __init__(self, database: Database, *, migrate: bool = True) -> None:
        self.database = database
        self._migrate = migrate
        self._ready = False
        self.search_service = RuleSearchService(database, embedder=BgeM3Embedder())

    @property
    def read_only(self) -> bool:
        return True

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
        expand_mode: str,
    ) -> dict[str, Any]:
        self._ensure_ready()
        if action == "search":
            if not query:
                raise ValueError("query is required for search")
            hits = self.search_service.search(
                query,
                campaign_id=campaign_id or self._context_campaign_id(),
                top_k=top_k,
                dense=dense,
            )
            return {"query": query, "hits": [asdict(hit) for hit in hits]}
        if action == "expand":
            if not chunk_id:
                raise ValueError("chunk_id is required for expand")
            return self.search_service.expand(chunk_id, mode=expand_mode)
        with self.database.transaction() as session:
            return {
                "rule_sets": int(session.scalar(select(func.count()).select_from(RuleSet)) or 0),
                "publications": int(
                    session.scalar(select(func.count()).select_from(RulePublication)) or 0
                ),
                "chunks": int(session.scalar(select(func.count()).select_from(RuleChunk)) or 0),
                "embedded_chunks": int(
                    session.scalar(
                        select(func.count())
                        .select_from(RuleChunk)
                        .where(RuleChunk.embedding_json.is_not(None))
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
        expand_mode: str = "section",
    ) -> dict[str, Any]:
        return await asyncio.to_thread(
            self._execute_sync,
            action=action,
            query=query,
            campaign_id=campaign_id,
            chunk_id=chunk_id,
            top_k=top_k,
            dense=dense,
            expand_mode=expand_mode,
        )
