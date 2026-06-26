from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from app.ingestion.models import IngestionStatus


@dataclass(slots=True)
class IngestRunCounts:
    discovered: int = 0
    fetched: int = 0
    stored_documents: int = 0
    stored_chunks: int = 0
    stored_reply_pairs: int = 0


@dataclass(slots=True)
class IngestRunContext:
    run_id: str
    source: str
    accounts: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


def start_ingest_run(connection: sqlite3.Connection, context: IngestRunContext) -> None:
    connection.execute(
        """
        INSERT INTO ingest_runs (
            run_id,
            source,
            accounts_json,
            started_at,
            status,
            metadata_json
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            context.run_id,
            context.source,
            json.dumps(list(context.accounts), sort_keys=True),
            _utc_now(),
            "started",
            json.dumps(context.metadata, sort_keys=True),
        ),
    )


def finish_ingest_run(
    connection: sqlite3.Connection,
    *,
    run_id: str,
    status: IngestionStatus,
    counts: IngestRunCounts,
    error_summary: str | None = None,
    error_detail: str | None = None,
) -> None:
    connection.execute(
        """
        UPDATE ingest_runs
        SET completed_at = ?,
            status = ?,
            discovered_count = ?,
            fetched_count = ?,
            stored_document_count = ?,
            stored_chunk_count = ?,
            stored_reply_pair_count = ?,
            error_summary = ?,
            error_detail = ?
        WHERE run_id = ?
        """,
        (
            _utc_now(),
            status,
            counts.discovered,
            counts.fetched,
            counts.stored_documents,
            counts.stored_chunks,
            counts.stored_reply_pairs,
            error_summary,
            error_detail,
            run_id,
        ),
    )


def _utc_now() -> str:
    return datetime.now(tz=UTC).isoformat().replace("+00:00", "Z")
