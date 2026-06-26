"""Core types for the memory tree ingestion layer.

Port of OpenHuman's `src/openhuman/memory/tree/types.rs` (428 lines → ~130).

Defines the canonical Chunk representation produced by the ingestion
pipeline along with its provenance Metadata and back-pointer SourceRef.
"""

from __future__ import annotations

import datetime
import functools
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SourceKind(Enum):
    """Which kind of upstream source produced a chunk."""
    CHAT = "chat"
    EMAIL = "email"
    DOCUMENT = "document"

    def as_str(self) -> str:
        return self.value

    @staticmethod
    def parse(s: str) -> SourceKind:
        for k in SourceKind:
            if k.value == s:
                return k
        raise ValueError(f"unknown source kind: {s}")


class DataSource(Enum):
    """Concrete upstream provider the content came from."""
    DISCORD = "discord"
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"
    GMAIL = "gmail"
    OTHER_EMAIL = "other_email"
    NOTION = "notion"
    MEETING_NOTES = "meeting_notes"
    DRIVE_DOCS = "drive_docs"

    def as_str(self) -> str:
        return self.value

    @staticmethod
    def parse(s: str) -> DataSource:
        for k in DataSource:
            if k.value == s:
                return k
        raise ValueError(f"unknown data source: {s}")


# ---------------------------------------------------------------------------
# Data types (port of Rust structs)
# ---------------------------------------------------------------------------

@dataclass
class SourceRef:
    """Opaque provider-specific identifier for the exact source record."""
    value: str

    @staticmethod
    def new(value: str) -> SourceRef:
        return SourceRef(value)


@dataclass
class Metadata:
    """Provenance metadata captured per chunk at ingest time."""
    source_kind: SourceKind
    source_id: str
    owner: str
    timestamp: datetime.datetime
    time_range: Tuple[datetime.datetime, datetime.datetime]
    tags: List[str] = field(default_factory=list)
    source_ref: Optional[SourceRef] = None

    @staticmethod
    def point_in_time(
        source_kind: SourceKind,
        source_id: str,
        owner: str,
        timestamp: datetime.datetime,
    ) -> Metadata:
        """Convenience constructor: point timestamp, time_range = (ts, ts)."""
        return Metadata(
            source_kind=source_kind,
            source_id=source_id,
            owner=owner,
            timestamp=timestamp,
            time_range=(timestamp, timestamp),
            tags=[],
            source_ref=None,
        )


@dataclass
class Chunk:
    """A single ingested chunk — the atomic persistence unit.

    Chunk IDs are deterministic:
        sha256(source_kind | "\\0" | source_id | "\\0" | seq | "\\0" | content)
    hex-encoded, first 32 chars — same as OpenHuman's types::chunk_id.
    """
    id: str
    content: str
    metadata: Metadata
    token_count: int
    seq_in_source: int
    created_at: datetime.datetime
    partial_message: bool = False


# ---------------------------------------------------------------------------
# Deterministic chunk id
# ---------------------------------------------------------------------------

def chunk_id(
    source_kind: SourceKind,
    source_id: str,
    seq_in_source: int,
    content: str,
) -> str:
    """Deterministic chunk id.

    sha256(source_kind | "\\0" | source_id | "\\0" | seq_be_bytes | "\\0" | content)
    → first 32 hex chars.
    """
    h = hashlib.sha256()
    h.update(source_kind.as_str().encode("utf-8"))
    h.update(b"\0")
    h.update(source_id.encode("utf-8"))
    h.update(b"\0")
    h.update(seq_in_source.to_bytes(8, byteorder="big"))
    h.update(b"\0")
    h.update(content.encode("utf-8"))
    return h.hexdigest()[:32]


# ---------------------------------------------------------------------------
# Heuristic token counter (1 token ≈ 4 chars)
# ---------------------------------------------------------------------------

@functools.lru_cache(maxsize=None)
def approx_token_count(text: str) -> int:
    """Approximate GPT-family token count (1 token ≈ 4 chars).

    Matches OpenHuman's types::approx_token_count for Phase 1.
    """
    return max(1, len(text) // 4)
