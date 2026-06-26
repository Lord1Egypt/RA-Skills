#!/usr/bin/env python3
"""
Registry of archive query adapters.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
ALPHAPAI_QUERY_SCRIPT = WORKSPACE_ROOT / "skills/alphapai-scraper/scripts/query_comments.py"
KB_ENGINE_SCRIPT = WORKSPACE_ROOT / "knowledge_bases/kb_engine.py"


@dataclass(frozen=True)
class SourceQueryRequest:
    query: str
    days: float
    limit: int
    include_private: bool = False
    exclude_kbs: tuple[str, ...] = ()


@dataclass(frozen=True)
class ArchiveSourceAdapter:
    name: str
    label: str
    supports_exact: bool = True
    supports_vector: bool = True

    def build_exact_command(self, request: SourceQueryRequest) -> list[str] | None:
        return None

    def build_vector_command(self, request: SourceQueryRequest) -> list[str] | None:
        return None


class AlphaPaiAdapter(ArchiveSourceAdapter):
    def __init__(self) -> None:
        super().__init__(name="alphapai", label="AlphaPai")

    def build_exact_command(self, request: SourceQueryRequest) -> list[str] | None:
        return [
            sys.executable,
            str(ALPHAPAI_QUERY_SCRIPT),
            "--query",
            request.query,
            "--days",
            str(request.days),
            "--limit",
            str(request.limit),
            "--mode",
            "exact",
            "--json",
        ]

    def build_vector_command(self, request: SourceQueryRequest) -> list[str] | None:
        return [
            sys.executable,
            str(ALPHAPAI_QUERY_SCRIPT),
            "--query",
            request.query,
            "--days",
            str(request.days),
            "--limit",
            str(request.limit),
            "--mode",
            "vector",
            "--json",
        ]


class KnowledgeBaseAdapter(ArchiveSourceAdapter):
    def __init__(self) -> None:
        super().__init__(name="knowledge_bases", label="Knowledge Bases")

    def build_exact_command(self, request: SourceQueryRequest) -> list[str] | None:
        command = [
            sys.executable,
            str(KB_ENGINE_SCRIPT),
            "exact-search",
            request.query,
            "--all",
            "--top",
            str(request.limit),
            "--json",
        ]
        if request.include_private:
            command.append("--include-private")
        for kb_name in request.exclude_kbs:
            command.extend(["--exclude-kb", kb_name])
        return command

    def build_vector_command(self, request: SourceQueryRequest) -> list[str] | None:
        command = [
            sys.executable,
            str(KB_ENGINE_SCRIPT),
            "search",
            request.query,
            "--all",
            "--top",
            str(request.limit),
            "--json",
        ]
        if request.include_private:
            command.append("--include-private")
        for kb_name in request.exclude_kbs:
            command.extend(["--exclude-kb", kb_name])
        return command


def default_registry() -> dict[str, ArchiveSourceAdapter]:
    return {
        "alphapai": AlphaPaiAdapter(),
        "knowledge_bases": KnowledgeBaseAdapter(),
    }


def select_adapters(sources: list[str] | None = None) -> list[ArchiveSourceAdapter]:
    registry = default_registry()
    if not sources:
        return list(registry.values())

    selected: list[ArchiveSourceAdapter] = []
    for name in sources:
        cleaned = name.strip()
        if not cleaned:
            continue
        adapter = registry.get(cleaned)
        if adapter:
            selected.append(adapter)
    return selected
