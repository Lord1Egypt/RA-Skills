"""Memory tree ingestion layer — selective OpenHuman memory architecture port.

Core types, SQLite store, chunker, and ingestion pipeline ported from
OpenHuman's `src/openhuman/memory/tree/` module (Rust).

This package is not a one-for-one OpenHuman clone.  It keeps the portable
storage, scoring, entity index, async job queue, and deterministic tree buffer
pieces that support agent lesson management, while leaving LLM-based topic
routing and content-management workflows outside this Python layer.

Public API:
    MemoryStore        — SQLite-backed persistence (all 9 tables)
    IngestResult       — Outcome of one ingest call
    ingest_markdown    — Top-level ingest pipeline
    chunk_markdown     — Slice markdown into bounded chunks
    Chunk, Metadata    — Core data model
"""

from .types import Chunk, Metadata, SourceRef, SourceKind, DataSource, chunk_id, approx_token_count
from .store import MemoryStore
from .chunker import ChunkerOptions, ChunkerInput, chunk_markdown
from .ingest import IngestResult, ingest_markdown

__all__ = [
    "Chunk", "Metadata", "SourceRef", "SourceKind", "DataSource",
    "chunk_id", "approx_token_count",
    "MemoryStore",
    "ChunkerOptions", "ChunkerInput", "chunk_markdown",
    "IngestResult", "ingest_markdown",
]
