#!/usr/bin/env python3
"""
Template for adding a new archive source adapter to research-archive-query.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[3]


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


class NewArchiveAdapter(ArchiveSourceAdapter):
    SCRIPT_PATH = WORKSPACE_ROOT / "path/to/your/query_script.py"

    def __init__(self) -> None:
        super().__init__(name="new_archive", label="New Archive")

    def build_exact_command(self, request: SourceQueryRequest) -> list[str] | None:
        return [
            sys.executable,
            str(self.SCRIPT_PATH),
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
            str(self.SCRIPT_PATH),
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


def normalize_new_archive_item(item: dict, *, retrieval_mode: str) -> dict:
    content = str(item.get("content") or item.get("summary") or "")
    return {
        "source": "new_archive",
        "source_label": "New Archive",
        "doc_id": str(item.get("id") or item.get("doc_id") or ""),
        "title": str(item.get("title") or "未命名资料"),
        "content": content,
        "summary": content[:240],
        "timestamp": str(item.get("updated_at") or item.get("scraped_at") or ""),
        "time_label": str(item.get("time_label") or item.get("updated_at") or ""),
        "scope": str(item.get("scope") or "market_research"),
        "visibility": str(item.get("visibility") or "shared"),
        "container": str(item.get("source_name") or "new_archive"),
        "path": str(item.get("raw_file") or item.get("source_path") or ""),
        "retrieval_modes": [retrieval_mode],
        "exact_score": 1.0 if retrieval_mode == "exact" else 0.0,
        "vector_score": float(item.get("score") or 0.0) if retrieval_mode == "vector" else 0.0,
        "score": float(item.get("score") or 1.0 if retrieval_mode == "exact" else 0.0),
    }
