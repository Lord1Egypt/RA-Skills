"""Hierarchical rule ingestion and hybrid retrieval."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .embedding import BgeM3Embedder
    from .ingest import RuleIngestService
    from .search import RuleSearchService

__all__ = ["BgeM3Embedder", "RuleIngestService", "RuleSearchService"]


def __getattr__(name: str):
    if name == "BgeM3Embedder":
        from .embedding import BgeM3Embedder

        return BgeM3Embedder
    if name == "RuleIngestService":
        from .ingest import RuleIngestService

        return RuleIngestService
    if name == "RuleSearchService":
        from .search import RuleSearchService

        return RuleSearchService
    raise AttributeError(name)
