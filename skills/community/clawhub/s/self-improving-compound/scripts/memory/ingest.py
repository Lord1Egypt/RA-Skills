"""Ingest orchestrator for the memory-tree pipeline.

Port of OpenHuman's `src/openhuman/memory/tree/ingest.rs` (591 lines → ~100).

The hot path::
    chunk → persist chunks → enqueue extract jobs

The slower work (scoring, entity extraction, lifecycle transitions, and
deterministic summary-tree buffering) runs through the SQLite-backed jobs
queue.  Topic routing is intentionally lightweight: area/pattern-key/source
tags choose trees without an LLM router.
"""

from __future__ import annotations

import datetime
import json
from dataclasses import dataclass, field
from typing import List, Optional

from .chunker import ChunkerInput, ChunkerOptions, chunk_markdown
from .store import CHUNK_STATUS_PENDING_EXTRACTION, MemoryStore
from .types import Metadata, SourceKind


@dataclass
class IngestResult:
    """Outcome of one ingest call."""
    source_id: str
    chunks_written: int = 0
    chunks_dropped: int = 0
    chunk_ids: List[str] = field(default_factory=list)
    already_ingested: bool = False


def ingest_markdown(
    store: MemoryStore,
    source_kind: SourceKind,
    source_id: str,
    markdown: str,
    metadata: Metadata,
    chunker_opts: ChunkerOptions = ChunkerOptions(),
    *,
    dedup: bool = True,
) -> IngestResult:
    """Ingest canonical markdown into the memory tree store.

    Parameters
    ----------
    store:
        Open (or re-used) MemoryStore instance.
    source_kind:
        Which kind of source produced this content.
    source_id:
        Stable logical id for the ingestion group.
    markdown:
        Canonical Markdown content to chunk and persist.
    metadata:
        Provenance metadata.
    chunker_opts:
        Chunker tuning (max_tokens).
    dedup:
        When True, skip ingestion if ``(source_kind, source_id)`` has
        already been ingested (idempotency guard).  Default True.

    Returns
    -------
    IngestResult with chunk_ids, counts, and dedup status.
    """
    # Dedup check.
    if dedup and store.is_source_ingested(source_kind, source_id):
        return IngestResult(
            source_id=source_id,
            already_ingested=True,
        )

    # Chunk.
    inp = ChunkerInput(
        source_kind=source_kind,
        source_id=source_id,
        markdown=markdown,
        metadata=metadata,
    )
    chunks = chunk_markdown(inp, chunker_opts)

    if not chunks:
        return IngestResult(source_id=source_id)

    # Persist.
    store.claim_source_ingest(source_kind, source_id, chunk_count=len(chunks))
    store.upsert_chunks(chunks)

    # Mark each chunk pending_extraction so the async worker can score,
    # index, and route it into the deterministic summary tree.
    for c in chunks:
        store.set_chunk_lifecycle(c.id, CHUNK_STATUS_PENDING_EXTRACTION)

    # Enqueue an extract job per chunk.
    for c in chunks:
        store.enqueue_job(MemoryStore.JobRow(
            kind="extract_chunk",
            payload_json=json.dumps({
                "chunk_id": c.id,
                "source_kind": source_kind.as_str(),
                "source_id": source_id,
            }),
            priority=0,
            dedupe_key=f"extract:{c.id}",
        ))

    return IngestResult(
        source_id=source_id,
        chunks_written=len(chunks),
        chunk_ids=[c.id for c in chunks],
    )
