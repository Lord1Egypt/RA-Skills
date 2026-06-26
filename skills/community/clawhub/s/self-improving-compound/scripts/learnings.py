#!/usr/bin/env python3
"""
learnings.py - Self-Improving Learning Log (SQLite-backed)

Powered by OpenHuman's memory architecture port (scripts/memory/).
All entries are stored as structured Chunks in SQLite with:
  - Deterministic content-addressed IDs (SHA256)
  - Scoring (token signal, metadata weight, source weight)
  - Entity indexing (Pattern-Keys → fast lookup)
  - Entity hotness tracking (frequency × recency)
  - Async job queue for background processing
  - Idempotent ingest deduplication

Commands:
  init            Initialize learning/ structure + SQLite DB
  status          Show memory statistics across all 9 tables
  search          Search across all learning records
  log             Backward-compatible generic log (COR/LRN/FTR/ERR)
  log-correction  Log a correction
  log-learning    Log a learning
  log-error       Log an error
  log-feature     Log a feature request
  process-jobs    Run queued async memory jobs
  maintain        Review and maintain memory lifecycle
  edit            Edit entry metadata
  promote         Promote entry to a target memory file
  forget          Forget an entry
  validate        Validate data integrity
  export          Export entries as markdown

Global options:
  --root PATH              Workspace root (default: OPENCLAW_WORKSPACE env, else cwd)
  --learning-root PATH     Learning store root (default: <workspace>/learning)
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# OpenHuman memory architecture port
from memory.store import (
    CHUNK_STATUS_ADMITTED,
    CHUNK_STATUS_DROPPED,
    CHUNK_STATUS_PENDING_EXTRACTION,
    CHUNK_STATUS_BUFFERED,
    CHUNK_STATUS_SEALED,
    ListChunksQuery,
    SearchChunksQuery,
    MemoryStore,
)
from memory.types import Chunk, Metadata, SourceKind, chunk_id, approx_token_count
from memory.chunker import ChunkerInput, ChunkerOptions, chunk_markdown
from memory.ingest import ingest_markdown, IngestResult


def get_now() -> datetime:
    source_date = os.environ.get("SOURCE_DATE_EPOCH")
    if source_date:
        return datetime.fromtimestamp(int(source_date), tz=timezone.utc).astimezone()
    return datetime.now().astimezone()


def resolve_root(args: argparse.Namespace) -> Optional[str]:
    return getattr(args, "local_root", None) or args.root


def resolve_learning_root(args: argparse.Namespace) -> Optional[str]:
    return (
        getattr(args, "local_learning_root", None)
        or getattr(args, "learning_root", None)
        or os.environ.get("SELF_IMPROVING_LEARNING_ROOT")
        or os.environ.get("SELF_IMPROVING_LEARNING_DIR")
    )


SUBDIR_NAME = "learning"

ID_PREFIXES = {
    "COR": "COR",
    "LRN": "LRN",
    "ERR": "ERR",
    "FTR": "FTR",
}

SECRET_PATTERNS = [
    re.compile(r'(?i)(api[_-]?key\s*[:=]\s*)["\']?[\w\-]{16,}["\']?', re.IGNORECASE),
    re.compile(r'(?i)(auth[_-]?token\s*[:=]\s*)["\']?[\w\-]{8,}["\']?', re.IGNORECASE),
    re.compile(r'(?i)(access[_-]?token\s*[:=]\s*)["\']?[\w\-]{8,}["\']?', re.IGNORECASE),
    re.compile(r'(?i)(password\s*[:=]\s*)["\']?[^\s"\']{4,}["\']?', re.IGNORECASE),
    re.compile(r'(?i)(secret\s*[:=]\s*)["\']?[\w\-]{8,}["\']?', re.IGNORECASE),
    re.compile(r'(?i)(client_secret\s*[:=]\s*)["\']?[\w\-]{8,}["\']?', re.IGNORECASE),
    re.compile(r'(?i)(authorization:\s*bearer\s+)[\w\-\.]+', re.IGNORECASE),
    re.compile(r'(?i)(authorization:\s*basic\s+)[\w\+/=]+', re.IGNORECASE),
    re.compile(r'(?i)(private[_-]?key\s*[:=]\s*)["\']?-----BEGIN[^\n]+', re.IGNORECASE),
    re.compile(r'(?i)(AKIA[0-9A-Z]{16})', re.IGNORECASE),
    re.compile(r'(?i)(sk-[a-zA-Z0-9]{20,})', re.IGNORECASE),
]

VOLATILE_PATTERNS = [
    re.compile(r'(?i)\b(pid|process\s+id)\s*[:=]?\s*\d+\b'),
    re.compile(r'(?i)\bsession[_-]?id\s*[:=]\s*[\w\-]{8,}\b'),
    re.compile(r'(?i)(?<![\w/])/tmp/[\w.-]+\b'),
    re.compile(r'(?i)\bcurrent\s+(timestamp|time|pid|session|dir|path)\b'),
    re.compile(r'\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b'),
]

ENTITY_TOKEN_RE = re.compile(r"\b[a-z][a-z0-9_-]{1,31}:[A-Za-z0-9][A-Za-z0-9._/\-]{1,96}\b")
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PATH_RE = re.compile(r"(?<![\w.-])(?:/[\w.@%+=:,~\-]+){2,}(?:\.[A-Za-z0-9]+)?")


def redact_secrets(text: str) -> str:
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(r'\1[REDACTED]', text)
    return text


def check_volatile_patterns(text: str) -> List[str]:
    warnings: List[str] = []
    for pattern in VOLATILE_PATTERNS:
        for match in pattern.finditer(text):
            warnings.append(f"Volatile pattern detected: '{match.group(0)}'")
    return warnings


def get_workspace_root(args_root: Optional[str]) -> Path:
    if args_root:
        return Path(args_root).expanduser().resolve()
    env_root = os.environ.get("OPENCLAW_WORKSPACE")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path.cwd().resolve()


def get_base_dir(args_root: Optional[str], learning_root: Optional[str] = None) -> Path:
    if learning_root:
        return Path(learning_root).expanduser().resolve()
    return get_workspace_root(args_root) / SUBDIR_NAME


def get_base_dir_for_args(args: argparse.Namespace) -> Path:
    return get_base_dir(resolve_root(args), resolve_learning_root(args))


def ensure_structure(base_dir: Path) -> None:
    dirs = [
        base_dir,
        base_dir / "projects",
        base_dir / "domains",
        base_dir / "archive",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def extract_pattern_keys(base_dir: Path) -> List[str]:
    """Extract unique Pattern-Keys from SQLite. Legacy markdown file scanning removed."""
    keys: List[str] = []
    db_path = base_dir / DB_SUBDIR / DB_FILE
    if db_path.exists():
        try:
            with MemoryStore(str(db_path)) as store:
                for c in store.list_chunks(ListChunksQuery(limit=10000)):
                    for tag in c.metadata.tags:
                        if tag.startswith("pattern-key:"):
                            keys.append(tag.split(":", 1)[1])
        except Exception:
            pass
    return list(sorted(set(keys)))


def update_index(base_dir: Path) -> None:
    """Generate index.md as a read-only snapshot of SQLite state."""
    today = get_now().strftime("%Y-%m-%d")

    # Aggregate from SQLite
    type_counts: Dict[str, int] = {}
    lifecycle_counts: Dict[str, int] = {}
    total = 0

    db_path = base_dir / DB_SUBDIR / DB_FILE
    if db_path.exists():
        try:
            with MemoryStore(str(db_path)) as store:
                for c in store.list_chunks(ListChunksQuery(limit=10000)):
                    total += 1
                    for tag in c.metadata.tags:
                        if tag in ("LRN", "ERR", "COR", "FTR"):
                            type_counts[tag] = type_counts.get(tag, 0) + 1
                    lc = store.get_chunk_lifecycle(c.id) or "admitted"
                    lifecycle_counts[lc] = lifecycle_counts.get(lc, 0) + 1
        except Exception:
            pass

    lines: List[str] = [
        "# Memory Index",
        "",
        "**Source of truth**: `memory_tree/chunks.db` (SQLite)",
        "",
        f"Generated: {today}",
        "",
    ]

    if total == 0:
        lines.append("_No entries yet. Use `learnings.py init` to get started._")
        lines.append("")
        (base_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")
        return

    lines.extend([
        "## Entries",
        "",
        f"Total: {total}",
        "",
        "| Type | Count |",
        "|------|-------|",
    ])
    for t in ("COR", "LRN", "ERR", "FTR"):
        lines.append(f"| {t} | {type_counts.get(t, 0)} |")

    if lifecycle_counts:
        lines.extend([
            "",
            "## Lifecycle",
            "",
            "| Tier | Count |",
            "|------|-------|",
        ])
        for lc in ("admitted", "buffered", "sealed", "dropped"):
            count = lifecycle_counts.get(lc, 0)
            if count:
                tier_label = {"admitted": "HOT", "buffered": "WARM", "sealed": "COLD", "dropped": "DROPPED"}.get(lc, lc)
                lines.append(f"| {tier_label} ({lc}) | {count} |")

    pattern_keys = extract_pattern_keys(base_dir)
    if pattern_keys:
        lines.extend([
            "",
            "## Pattern-Keys",
            "",
        ])
        for pk in pattern_keys:
            lines.append(f"- `{pk}`")

    lines.extend([
        "",
        "---",
        "",
        "_This index is auto-generated. Use `learnings.py` CLI to query and manage entries._",
        "",
    ])

    (base_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# New helpers: store, ingestion, scoring, entity indexing
# ---------------------------------------------------------------------------

DB_SUBDIR = Path("memory_tree")
DB_FILE = "chunks.db"
PROMOTION_QUEUE_FILE = "promotion-queue.json"


def get_store(args_root: Optional[str], learning_root: Optional[str] = None) -> MemoryStore:
    """Open the SQLite MemoryStore for the workspace root.

    DB lives at ``<base_dir>/memory_tree/chunks.db``, matching the
    OpenHuman convention.  Schema is applied lazily on first access.
    """
    base_dir = get_base_dir(args_root, learning_root)
    db_path = base_dir / DB_SUBDIR / DB_FILE
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return MemoryStore(str(db_path))


def get_store_for_args(args: argparse.Namespace) -> MemoryStore:
    return get_store(resolve_root(args), resolve_learning_root(args))


def _entry_fingerprint(
    entry_type: str,
    summary: str,
    details: str,
    pattern_key: str,
    area: str,
) -> str:
    normalized = "\0".join(
        [
            entry_type.strip().upper(),
            re.sub(r"\s+", " ", summary.strip().lower()),
            re.sub(r"\s+", " ", details.strip().lower()),
            pattern_key.strip().lower(),
            area.strip().lower(),
        ]
    )
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def _extract_entry_id(chunk: Chunk) -> str:
    for tag in chunk.metadata.tags:
        if tag.startswith("entry-id:"):
            return tag.split(":", 1)[1]
    m = re.search(r"^###\s+([A-Z]{3}-\d{8}-\d{3})\b", chunk.content, re.MULTILINE)
    return m.group(1) if m else chunk.id[:12]


def _extract_status(chunk: Chunk) -> str:
    for tag in chunk.metadata.tags:
        if tag.startswith("status:"):
            return tag.split(":", 1)[1]
    m = re.search(r"- \*\*Status\*\*:\s*(.+)", chunk.content)
    return m.group(1).strip() if m else "pending"


def _extract_recurrence_count(chunk: Chunk) -> int:
    m = re.search(r"- \*\*Recurrence-Count\*\*:\s*(\d+)", chunk.content)
    if not m:
        return 1
    try:
        return max(1, int(m.group(1)))
    except ValueError:
        return 1


def _extract_last_seen(chunk: Chunk) -> datetime:
    m = re.search(r"- \*\*Last-Seen\*\*:\s*([0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{8})", chunk.content)
    if m:
        parsed = _parse_date(m.group(1))
        if parsed:
            return parsed
    return chunk.metadata.timestamp


def _extract_field_value(chunk: Chunk, field: str, default: str = "") -> str:
    m = re.search(rf"- \*\*{re.escape(field)}\*\*:\s*(.+)", chunk.content)
    return m.group(1).strip() if m else default


def _replace_or_append_field(content: str, field: str, value: str) -> str:
    pattern = rf"- \*\*{re.escape(field)}\*\*:\s*.*"
    replacement = f"- **{field}**: {value}"
    if re.search(pattern, content):
        return re.sub(pattern, replacement, content)
    return content.rstrip() + f"\n{replacement}\n"


def _next_entry_id(store: MemoryStore, entry_type: str, now: datetime) -> str:
    date_part = now.strftime("%Y%m%d")
    prefix = f"{entry_type}-{date_part}-"
    max_seq = 0
    for chunk in store.list_chunks(ListChunksQuery(limit=10000)):
        entry_id = _extract_entry_id(chunk)
        if entry_id.startswith(prefix):
            try:
                max_seq = max(max_seq, int(entry_id.rsplit("-", 1)[1]))
            except (IndexError, ValueError):
                continue
    return f"{prefix}{max_seq + 1:03d}"


def _find_chunk_by_entry_id(store: MemoryStore, entry_id: str) -> Optional[Chunk]:
    wanted = entry_id.strip()
    for chunk in store.list_chunks(ListChunksQuery(limit=10000)):
        if chunk.id == wanted or chunk.id.startswith(wanted) or _extract_entry_id(chunk) == wanted:
            return chunk
    return None


def _chunk_for_entry(
    entry_type: str,
    entry_id_str: str,
    summary: str,
    details: str,
    pattern_key: str,
    area: str,
    fingerprint: str,
    now: datetime,
    owner: str = "user",
) -> Chunk:
    """Build a Chunk from structured log entry fields.

    The chunk content is the canonical markdown representation, same as
    the legacy format but stored in SQLite instead of .md files.
    """
    today_str = now.strftime("%Y-%m-%d")
    source_id = entry_id_str

    markdown = (
        f"### {entry_id_str} ({today_str})"
        + (f" [Pattern-Key: {pattern_key}]" if pattern_key else "")
        + f"\n- **Type**: {entry_type}"
        + f"\n- **Summary**: {summary}"
        + (f"\n- **Details**: {details}" if details else "")
        + (f"\n- **Area**: {area}" if area else "")
        + f"\n- **First-Seen**: {today_str}"
        + f"\n- **Last-Seen**: {today_str}"
        + f"\n- **Recurrence-Count**: 1"
        + f"\n- **Status**: pending"
        + f"\n- **Storage**: sqlite"
        + "\n"
    )

    tags = [entry_type, f"entry-id:{entry_id_str}", f"fingerprint:{fingerprint}", "status:pending"]
    if pattern_key:
        tags.append(f"pattern-key:{pattern_key}")
    if area:
        tags.append(f"area:{area}")

    meta = Metadata(
        source_kind=SourceKind.DOCUMENT,
        source_id=source_id,
        owner=owner,
        timestamp=now,
        time_range=(now, now),
        tags=tags,
        source_ref=None,
    )
    cid = chunk_id(SourceKind.DOCUMENT, source_id, 0, markdown)
    return Chunk(
        id=cid,
        content=markdown,
        metadata=meta,
        token_count=approx_token_count(markdown),
        seq_in_source=0,
        created_at=now,
    )


def _compute_entry_score(chunk: Chunk) -> MemoryStore.ScoreRow:
    """Compute a basic signal score for a log entry chunk.

    Scores mimic OpenHuman's admission gate:
      - token_count_signal: penalises very short (<50) or very long (>5000) entries
      - unique_words_signal: lexical diversity
      - metadata_weight: higher if tags/pattern-key present
      - source_weight: higher if summary is non-trivial
      - entity_density: pattern-key presence
      - total: weighted combination
    """
    content = chunk.content
    words = content.split()
    unique_words = len(set(w.lower() for w in words))
    word_count = max(1, len(words))
    char_count = max(1, len(content))

    # Token count signal: sigmoid-like, peaks at ~200-2000 chars
    tc_signal = min(1.0, char_count / 2000.0) * (1.0 if char_count >= 50 else 0.3)

    # Unique words signal: lexical diversity
    uw_signal = min(1.0, unique_words / max(1, word_count) * 2.0)

    # Metadata weight: pattern-key → useful signal
    has_pk = any("pattern-key" in t for t in chunk.metadata.tags)
    has_area = any("area" in t for t in chunk.metadata.tags)
    meta_weight = 0.3 + (0.4 if has_pk else 0.0) + (0.3 if has_area else 0.0)

    # Source weight: entry type signals usefulness
    entry_types = [t for t in chunk.metadata.tags if t in ("LRN", "ERR", "COR", "FTR")]
    type_bonus = {"COR": 1.0, "ERR": 0.9, "LRN": 0.8, "FTR": 0.6}
    src_weight = max(type_bonus.get(t, 0.5) for t in entry_types) if entry_types else 0.5

    # Interaction weight tracks explicit reuse. New entries start at zero so
    # maintenance does not confuse freshness with recurrence.
    interaction_weight = 0.0

    # Entity density: Pattern-Key plus deterministic entity extraction signal.
    extracted_entities = _extract_lightweight_entities(chunk)
    pk_chars = 0
    if has_pk:
        for tag in chunk.metadata.tags:
            if tag.startswith("pattern-key:"):
                pk_chars = len(tag)
    entity_density = min(1.0, (pk_chars / 200.0) + (len(extracted_entities) / 12.0))

    total = (
        tc_signal * 0.20
        + uw_signal * 0.15
        + meta_weight * 0.20
        + src_weight * 0.25
        + interaction_weight * 0.10
        + entity_density * 0.10
    )
    total = max(0.0, min(1.0, total))

    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    return MemoryStore.ScoreRow(
        chunk_id=chunk.id,
        total=total,
        token_count_signal=tc_signal,
        unique_words_signal=uw_signal,
        metadata_weight=meta_weight,
        source_weight=src_weight,
        interaction_weight=interaction_weight,
        entity_density=entity_density,
        dropped=0,
        computed_at_ms=now_ms,
    )


def _index_pattern_key(store: MemoryStore, chunk: Chunk, pattern_key: str) -> None:
    """Index a Pattern-Key in the entity index for fast lookup."""
    if not pattern_key:
        return
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    store.upsert_entity_index([
        MemoryStore.EntityIndexRow(
            entity_id=f"pattern-key:{pattern_key}",
            node_id=chunk.id,
            node_kind="chunk",
            entity_kind="pattern_key",
            surface=pattern_key,
            score=1.0,
            timestamp_ms=now_ms,
        ),
    ])


def _extract_lightweight_entities(chunk: Chunk) -> List[MemoryStore.EntityIndexRow]:
    """Extract deterministic entities without calling an LLM.

    The extractor is deliberately conservative: explicit Pattern-Keys and
    areas, entry IDs, namespaced tokens, email addresses, and durable paths.
    It gives the learning store an entity layer while preserving portability.
    """
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    rows: Dict[tuple, MemoryStore.EntityIndexRow] = {}

    def add(kind: str, surface: str, score: float = 0.7) -> None:
        surface = surface.strip().strip(".,;)]}")
        if not surface:
            return
        entity_id = f"{kind}:{surface.lower()}"
        key = (entity_id, chunk.id, "chunk")
        rows[key] = MemoryStore.EntityIndexRow(
            entity_id=entity_id,
            node_id=chunk.id,
            node_kind="chunk",
            entity_kind=kind,
            surface=surface,
            score=score,
            timestamp_ms=now_ms,
            tree_id=_chunk_tree_route(chunk)["tree_id"],
        )

    entry_id = _extract_entry_id(chunk)
    if entry_id:
        add("entry", entry_id, 1.0)

    for tag in chunk.metadata.tags:
        if tag.startswith("pattern-key:"):
            add("pattern-key", tag.split(":", 1)[1], 1.0)
        elif tag.startswith("area:"):
            add("area", tag.split(":", 1)[1], 0.85)
        elif tag in ("LRN", "ERR", "COR", "FTR"):
            add("type", tag, 0.4)

    for match in EMAIL_RE.finditer(chunk.content):
        add("email", match.group(0), 0.8)
    for match in PATH_RE.finditer(chunk.content):
        value = match.group(0)
        if not value.startswith("/tmp/"):
            add("path", value, 0.6)
    for match in ENTITY_TOKEN_RE.finditer(chunk.content):
        token = match.group(0)
        prefix, value = token.split(":", 1)
        if prefix not in {"http", "https", "mailto"}:
            add(prefix, value, 0.65)

    return list(rows.values())


def _index_extracted_entities(store: MemoryStore, chunk: Chunk) -> int:
    rows = _extract_lightweight_entities(chunk)
    return store.upsert_entity_index(rows) if rows else 0


def _update_hotness(store: MemoryStore, chunk: Chunk, pattern_key: str) -> None:
    """Update entity hotness for pattern-key usage."""
    if not pattern_key:
        return
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    entity_id = f"pattern-key:{pattern_key}"
    # Fetch existing hotness or compute fresh
    existing = store.top_entities(limit=1000)
    found = [e for e in existing if e.get("entity_id") == entity_id]
    if found:
        freq = float(found[0]["frequency"]) + 1.0
        score = float(found[0]["score"])
        # Decayed score: new_score = old * 0.9 + 0.1
        score = score * 0.9 + 1.0
    else:
        freq = 1.0
        score = 1.0
    store.upsert_entity_hotness(
        entity_id=entity_id,
        tree_id="default",
        frequency=freq,
        recency=1.0,
        score=score,
        last_seen_ms=now_ms,
    )


def _chunk_tree_route(chunk: Chunk) -> Dict[str, str]:
    """Return the deterministic summary tree for a chunk."""
    for tag in chunk.metadata.tags:
        if tag.startswith("area:"):
            area = tag.split(":", 1)[1]
            return {"tree_id": f"area:{area}", "tree_type": "area"}
    for tag in chunk.metadata.tags:
        if tag.startswith("pattern-key:"):
            pk = tag.split(":", 1)[1]
            return {"tree_id": f"pattern-key:{pk}", "tree_type": "pattern_key"}
    return {
        "tree_id": f"source:{chunk.metadata.source_kind.as_str()}:{chunk.metadata.source_id}",
        "tree_type": "source",
    }


def _chunk_summary_text(chunk: Chunk, max_chars: int = 280) -> str:
    summary_match = re.search(r"\*\*Summary\*\*:\s*(.+)", chunk.content)
    if summary_match:
        text = summary_match.group(1)
    else:
        lines = [line.strip("# ").strip() for line in chunk.content.splitlines() if line.strip()]
        text = lines[0] if lines else chunk.content
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_chars:
        return text[: max_chars - 3].rstrip() + "..."
    return text


def _summary_id(tree_id: str, level: int, key: str) -> str:
    digest = hashlib.sha256(f"{tree_id}\0{level}\0{key}".encode("utf-8")).hexdigest()[:24]
    return f"sum:{level}:{digest}"


def _maintenance_plan(store: MemoryStore) -> Dict[str, List[Dict[str, Any]]]:
    all_chunks = store.list_chunks(ListChunksQuery(limit=10000))
    now = get_now()

    stale_hot: List[Dict[str, Any]] = []
    stale_warm: List[Dict[str, Any]] = []
    promote_candidates: List[Dict[str, Any]] = []
    insufficient_metadata: List[Dict[str, Any]] = []

    for c in all_chunks:
        last_seen = _extract_last_seen(c)
        days_stale = (now - last_seen).days
        lifecycle = store.get_chunk_lifecycle(c.id) or CHUNK_STATUS_ADMITTED
        rc = _extract_recurrence_count(c)
        entry_id = _extract_entry_id(c)
        status = _extract_status(c).strip().lower()

        if lifecycle == CHUNK_STATUS_BUFFERED and days_stale >= 90:
            stale_warm.append({
                "id": entry_id,
                "chunk_id": c.id,
                "last_seen": last_seen.strftime("%Y-%m-%d"),
                "days_stale": days_stale,
                "target": "archive/",
            })
        elif lifecycle == CHUNK_STATUS_ADMITTED and days_stale >= 30:
            stale_hot.append({
                "id": entry_id,
                "chunk_id": c.id,
                "last_seen": last_seen.strftime("%Y-%m-%d"),
                "days_stale": days_stale,
                "target": "warm",
            })

        if rc >= 3 and status not in {"promoted", "promoted_to_skill", "resolved", "wont_fix"}:
            promote_candidates.append({
                "id": entry_id,
                "chunk_id": c.id,
                "recurrence_count": rc,
                "summary": _chunk_summary_text(c, max_chars=180),
                "suggested_target": _suggest_promotion_target(c),
            })

    return {
        "stale_hot": stale_hot,
        "stale_warm": stale_warm,
        "promote_candidates": promote_candidates,
        "insufficient_metadata": insufficient_metadata,
    }


def _apply_maintenance_plan(store: MemoryStore, plan: Dict[str, List[Dict[str, Any]]]) -> None:
    for r in plan["stale_hot"]:
        store.set_chunk_lifecycle(r["chunk_id"], CHUNK_STATUS_BUFFERED)
    for r in plan["stale_warm"]:
        store.set_chunk_lifecycle(r["chunk_id"], CHUNK_STATUS_SEALED)


def _process_extract_chunk_job(store: MemoryStore, payload: Dict[str, Any]) -> Dict[str, Any]:
    chunk_id_value = str(payload.get("chunk_id") or "")
    if not chunk_id_value:
        raise ValueError("extract_chunk payload missing chunk_id")
    chunk = store.get_chunk(chunk_id_value)
    if chunk is None:
        raise ValueError(f"chunk not found: {chunk_id_value}")

    score = _compute_entry_score(chunk)
    store.upsert_scores([score])
    entity_count = _index_extracted_entities(store, chunk)

    lifecycle = store.get_chunk_lifecycle(chunk.id)
    if lifecycle in (None, CHUNK_STATUS_PENDING_EXTRACTION):
        store.set_chunk_lifecycle(chunk.id, CHUNK_STATUS_ADMITTED)

    route = _chunk_tree_route(chunk)
    tree_id = route["tree_id"]
    now_ms = int(get_now().timestamp() * 1000)
    summary_text = _chunk_summary_text(chunk)
    root_id = _summary_id(tree_id, 1, "root")

    store.upsert_tree(
        tree_id=tree_id,
        root_id=root_id,
        status="open",
        tree_type=route["tree_type"],
        owner=chunk.metadata.owner,
        created_at_ms=now_ms,
    )
    store.append_buffer(
        tree_id=tree_id,
        chunk_id=chunk.id,
        seq=chunk.seq_in_source,
        content=summary_text,
        token_count=approx_token_count(summary_text),
        oldest_ts_ms=int(chunk.metadata.time_range[0].timestamp() * 1000),
        newest_ts_ms=int(chunk.metadata.time_range[1].timestamp() * 1000),
    )

    store.upsert_summary(MemoryStore.SummaryRow(
        id=_summary_id(tree_id, 0, chunk.id),
        tree_id=tree_id,
        tree_level=0,
        parent_id=root_id,
        content=summary_text,
        token_count=approx_token_count(summary_text),
        chunk_count=1,
        time_range_start_ms=int(chunk.metadata.time_range[0].timestamp() * 1000),
        time_range_end_ms=int(chunk.metadata.time_range[1].timestamp() * 1000),
        created_at_ms=now_ms,
        sealed_at_ms=now_ms,
    ))

    buffers = store.list_buffers(tree_id=tree_id, limit=20)
    rolling_lines = [f"- {b['content']}" for b in buffers[:20] if b.get("content")]
    rolling_content = "\n".join(rolling_lines) if rolling_lines else summary_text
    store.upsert_summary(MemoryStore.SummaryRow(
        id=root_id,
        tree_id=tree_id,
        tree_level=1,
        content=rolling_content,
        token_count=approx_token_count(rolling_content),
        chunk_count=len(buffers),
        time_range_start_ms=min(int(b["oldest_timestamp_ms"]) for b in buffers) if buffers else None,
        time_range_end_ms=max(int(b["newest_timestamp_ms"]) for b in buffers) if buffers else None,
        created_at_ms=now_ms,
    ))

    return {
        "chunk_id": chunk.id,
        "tree_id": tree_id,
        "summary": summary_text,
        "entities_indexed": entity_count,
    }


def _process_lifecycle_job(
    store: MemoryStore,
    base_dir: Path,
    dry_run: bool = False,
) -> Dict[str, Any]:
    plan = _maintenance_plan(store)
    if not dry_run:
        _apply_maintenance_plan(store, plan)
    _update_heartbeat_state(base_dir, plan, dry_run)
    return {
        "stale_hot": len(plan["stale_hot"]),
        "stale_warm": len(plan["stale_warm"]),
        "promote_candidates": len(plan["promote_candidates"]),
        "dry_run": dry_run,
    }


def _process_job(store: MemoryStore, base_dir: Path, job: Dict[str, Any]) -> Dict[str, Any]:
    try:
        payload = json.loads(job.get("payload_json") or "{}")
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid payload_json: {e}") from e

    kind = job["kind"]
    if kind == "extract_chunk":
        return _process_extract_chunk_job(store, payload)
    if kind == "maintain_lifecycle":
        return _process_lifecycle_job(store, base_dir, dry_run=bool(payload.get("dry_run", False)))
    raise ValueError(f"unknown job kind: {kind}")


def _ensure_lifecycle_job(store: MemoryStore) -> None:
    active = (
        store.count_jobs_by_kind("maintain_lifecycle", "pending")
        + store.count_jobs_by_kind("maintain_lifecycle", "running")
    )
    if active == 0:
        store.enqueue_job(MemoryStore.JobRow(
            kind="maintain_lifecycle",
            payload_json=json.dumps({"dry_run": False}),
            priority=-50,
            max_retries=1,
            dedupe_key="maintain:lifecycle",
        ))


def _ingest_entry(
    store: MemoryStore,
    entry_type: str,
    summary: str,
    details: str,
    pattern_key: str,
    area: str,
    *,
    force: bool = False,
) -> Optional[str]:
    """Core ingestion pipeline for a structured log entry.

    1. Build a Chunk from the entry fields
    2. Check dedup (unless --force)
    3. Compute score
    4. Persist chunk + score atomically
    5. Index pattern-key in entity_index
    6. Update entity hotness
    7. Enqueue background job for extraction

    Returns the human entry ID or None if dedup'd.
    """
    now = get_now()
    fingerprint = _entry_fingerprint(entry_type, summary, details, pattern_key, area)

    if not force:
        fingerprint_tag = f"fingerprint:{fingerprint}"
        for existing in store.list_chunks(ListChunksQuery(limit=10000)):
            if fingerprint_tag in existing.metadata.tags:
                return None

    entry_id = _next_entry_id(store, entry_type, now)
    chunk = _chunk_for_entry(entry_type, entry_id, summary, details, pattern_key, area, fingerprint, now)
    source_kind = chunk.metadata.source_kind
    source_id = chunk.metadata.source_id

    # Persist chunk
    store.claim_source_ingest(source_kind, source_id, chunk_count=1)
    store.upsert_chunks([chunk])

    # Compute and persist score
    score = _compute_entry_score(chunk)
    store.upsert_scores([score])

    # Mark lifecycle
    store.set_chunk_lifecycle(chunk.id, CHUNK_STATUS_ADMITTED)

    # Entity indexing
    if pattern_key:
        _index_pattern_key(store, chunk, pattern_key)
        _update_hotness(store, chunk, pattern_key)
    _index_extracted_entities(store, chunk)

    # Track area as entity too
    if area:
        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        store.upsert_entity_index([
            MemoryStore.EntityIndexRow(
                entity_id=f"area:{area}",
                node_id=chunk.id,
                node_kind="chunk",
                entity_kind="area",
                surface=area,
                score=0.5,
                timestamp_ms=now_ms,
            ),
        ])

    store.enqueue_job(MemoryStore.JobRow(
        kind="extract_chunk",
        payload_json=json.dumps({
            "chunk_id": chunk.id,
            "source_kind": source_kind.as_str(),
            "source_id": source_id,
        }),
        priority=0,
        dedupe_key=f"extract:{chunk.id}",
    ))

    return entry_id


def _render_chunk_as_markdown(chunk: Chunk) -> str:
    """Render a Chunk back to human-readable markdown."""
    ts = chunk.metadata.timestamp.strftime("%Y-%m-%d")
    entry_type = chunk.metadata.tags[0] if chunk.metadata.tags else "LRN"
    pk_tag = [t for t in chunk.metadata.tags if t.startswith("pattern-key:")]
    pk = pk_tag[0].split(":", 1)[1] if pk_tag else ""
    area_tag = [t for t in chunk.metadata.tags if t.startswith("area:")]
    area = area_tag[0].split(":", 1)[1] if area_tag else ""

    lines = [f"### {_extract_entry_id(chunk)} ({ts})"]
    if pk:
        lines[0] += f" [Pattern-Key: {pk}]"
    lines.append(f"- **Type**: {entry_type}")
    summary_match = re.search(r"\*\*Summary\*\*:\s*(.+)", chunk.content)
    if summary_match:
        lines.append(f"- **Summary**: {summary_match.group(1)}")
    details_match = re.search(r"\*\*Details\*\*:\s*(.+?)(?=\n- \*\*|\Z)", chunk.content, re.DOTALL)
    if details_match:
        lines.append(f"- **Details**: {details_match.group(1).strip()}")
    if area:
        lines.append(f"- **Area**: {area}")
    lines.append(f"- **First-Seen**: {_extract_field_value(chunk, 'First-Seen', ts)}")
    lines.append(f"- **Last-Seen**: {_extract_field_value(chunk, 'Last-Seen', ts)}")
    lines.append(f"- **Recurrence-Count**: {_extract_recurrence_count(chunk)}")
    lines.append(f"- **Status**: {_extract_status(chunk)}")
    promoted_match = re.search(r"- \*\*Promoted-To\*\*:\s*(.+)", chunk.content)
    if promoted_match:
        lines.append(f"- **Promoted-To**: {promoted_match.group(1).strip()}")
    lines.append(f"- **Token-Count**: {chunk.token_count}")
    lines.append(f"- **Chunk-ID**: `{chunk.id}`")
    lines.append("")
    return "\n".join(lines)


def cmd_init(args: argparse.Namespace) -> None:
    base_dir = get_base_dir_for_args(args)
    ensure_structure(base_dir)
    # Initialise the SQLite store
    store = get_store_for_args(args)
    store.open()
    store.close()
    print(f"[init] Learning structure ready at: {base_dir}")
    print(f"[init] MemoryStore : {base_dir / DB_SUBDIR / DB_FILE}")


def cmd_status(args: argparse.Namespace) -> None:
    base_dir = get_base_dir_for_args(args)
    ensure_structure(base_dir)

    fmt = getattr(args, "format", "text") or "text"
    store = get_store_for_args(args)
    with store:
        # Stats from all 9 tables
        total_chunks = store.count_chunks()

        # Entry type breakdown from tags
        all_chunks = store.list_chunks(ListChunksQuery(limit=10000))
        type_counts: Dict[str, int] = {}
        pk_count = 0
        area_counts: Dict[str, int] = {}
        lifecycle_counts: Dict[str, int] = {}
        total_score = 0.0
        scored_count = 0

        for c in all_chunks:
            for tag in c.metadata.tags:
                if tag in ("LRN", "ERR", "COR", "FTR"):
                    type_counts[tag] = type_counts.get(tag, 0) + 1
                elif tag.startswith("pattern-key:"):
                    pk_count += 1
                elif tag.startswith("area:"):
                    area_name = tag.split(":", 1)[1]
                    area_counts[area_name] = area_counts.get(area_name, 0) + 1

            # Lifecycle
            lc = store.get_chunk_lifecycle(c.id)
            lc = lc or "admitted"
            lifecycle_counts[lc] = lifecycle_counts.get(lc, 0) + 1

            # Score
            sc = store.get_score(c.id)
            if sc:
                total_score += sc.total
                scored_count += 1

        avg_score = total_score / max(1, scored_count)

        # Entity index stats
        idx_rows = store.query_entity_index(limit=10000)
        entity_type_counts: Dict[str, int] = {}
        for r in idx_rows:
            entity_type_counts[r.entity_kind] = entity_type_counts.get(r.entity_kind, 0) + 1

        # Entity hotness
        top_entities = store.top_entities(limit=5)

        # Job queue: status must remain read-only.
        pending_jobs = store.count_jobs(status="pending")

    if fmt == "json":
        out: Dict[str, Any] = {
            "workspace_root": str(get_workspace_root(resolve_root(args))),
            "learning_root": str(base_dir),
            "total_chunks": total_chunks,
            "entries_by_type": type_counts,
            "pattern_keys": pk_count,
            "areas": area_counts,
            "lifecycle": lifecycle_counts,
            "avg_score": round(avg_score, 3),
            "entity_index": entity_type_counts,
            "hot_entities": [
                {"entity_id": e["entity_id"], "score": e["score"]}
                for e in top_entities
            ],
            "pending_jobs": pending_jobs,
            "capabilities": {
                "sqlite_store": True,
                "fts_search": True,
                "entity_index": True,
                "async_jobs": True,
                "summary_tree_buffers": True,
                "promotion_queue": True,
                "topic_routing": "deterministic_area_or_pattern_key",
                "llm_scoring": False,
            },
        }
        print(json.dumps(out, indent=2))
        return

    print("[status] Memory Status (SQLite-backed)")
    print(f"  Workspace    : {get_workspace_root(resolve_root(args))}")
    print(f"  Learning Root: {base_dir}")
    print(f"  Chunks       : {total_chunks}")
    print(f"  Avg Score    : {avg_score:.3f}")
    print(f"  Pattern-Keys : {pk_count}")
    print(f"  Pending Jobs : {pending_jobs}")
    if type_counts:
        print("  Entries by type:")
        for k, v in sorted(type_counts.items()):
            print(f"    {k}: {v}")
    if lifecycle_counts:
        print("  Lifecycle:")
        for k, v in sorted(lifecycle_counts.items()):
            print(f"    {k}: {v}")
    if area_counts:
        print("  Areas:")
        for k, v in sorted(area_counts.items(), key=lambda x: -x[1])[:5]:
            print(f"    {k}: {v} entries")
    if top_entities:
        print("  Hottest entities:")
        for e in top_entities:
            print(f"    {e['entity_id']}: score={e['score']:.2f}")


def cmd_search(args: argparse.Namespace) -> None:
    base_dir = get_base_dir_for_args(args)
    query = args.query or ""
    if not query:
        print("[search] Error: query required", file=sys.stderr)
        sys.exit(1)

    fmt = getattr(args, "format", "text") or "text"

    store = get_store_for_args(args)
    with store:
        indexed_scores: Dict[str, float] = {}
        # Search via entity index first for exact Pattern-Key / entity lookup.
        if query.startswith("pk:") or query.startswith("entity:"):
            entity_id = (
                f"pattern-key:{query[3:]}"
                if query.startswith("pk:")
                else query.split(":", 1)[1]
            )
            idx_rows = store.query_entity_index(entity_id=entity_id)
            chunk_ids = [r.node_id for r in idx_rows]
            chunks = []
            for cid in chunk_ids:
                c = store.get_chunk(cid)
                if c:
                    chunks.append(c)
                    indexed_scores[c.id] = 0.95
        else:
            # Full-text chunk search via FTS5, with LIKE fallback in the store.
            limit = args.limit or 20
            matches = store.search_chunks(SearchChunksQuery(query=query, limit=limit))
            chunks = [c for c, _ in matches]
            indexed_scores = {c.id: score for c, score in matches}

        # Compute scores for ordering
        scored = []
        for c in chunks:
            score_row = store.get_score(c.id)
            memory_score = score_row.total if score_row else 0.5
            search_score = indexed_scores.get(c.id, 0.5)
            score_val = round((memory_score * 0.55) + (search_score * 0.45), 4)
            # Extract summary from content for display
            summary_match = re.search(r"\*\*Summary\*\*:\s*(.+)", c.content)
            summary_text = summary_match.group(1) if summary_match else c.content[:80]
            scored.append({
                "id": _extract_entry_id(c),
                "chunk_id": c.id,
                "summary": summary_text,
                "type": c.metadata.tags[0] if c.metadata.tags else "?",
                "date": c.metadata.timestamp.strftime("%Y-%m-%d"),
                "score": score_val,
                "content": c.content[:200],
            })

        if getattr(args, "touch", False):
            # Explicitly record reuse when the caller is acting on a result.
            # Plain search stays read-only so dedupe/review does not inflate recurrence.
            now = get_now()
            today = now.strftime("%Y-%m-%d")
            for c in chunks:
                current_rc = _extract_recurrence_count(c)
                c.content = _replace_or_append_field(c.content, "Last-Seen", today)
                c.content = _replace_or_append_field(c.content, "Recurrence-Count", str(current_rc + 1))
                c.metadata.timestamp = now
                c.metadata.time_range = (c.metadata.time_range[0], now)
                store.upsert_chunks([c])
                score_row = store.get_score(c.id)
                if score_row:
                    score_row.interaction_weight = max(score_row.interaction_weight + 0.1, (current_rc + 1) / 10.0)
                    score_row.computed_at_ms = int(now.timestamp() * 1000)
                    store.upsert_scores([score_row])
                for tag in [t for t in c.metadata.tags if t.startswith("pattern-key:")]:
                    pk = tag.split(":", 1)[1]
                    _update_hotness(store, c, pk)

    if fmt == "json":
        print(json.dumps(scored, indent=2, default=str))
        return

    if not scored:
        print(f"[search] No results for '{query}'")
        return

    # Sort by score descending
    scored.sort(key=lambda x: -x["score"])

    print(f"[search] Found {len(scored)} result(s) for '{query}':")
    for s in scored:
        print(f"  [{s['score']:.2f}] {s['date']} {s['type']} {s['id']} | {s['summary'][:80]}")


def append_block_to_file(path: Path, block_text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        text = path.read_text(encoding="utf-8")
        text = text.rstrip()
        if text:
            text += "\n\n"
        text += block_text.rstrip() + "\n"
    else:
        text = block_text.rstrip() + "\n"
    path.write_text(text, encoding="utf-8")


def append_block_to_file_once(path: Path, block_text: str, marker: str) -> bool:
    """Append a promoted block unless its stable entry marker is already present."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and marker and marker in path.read_text(encoding="utf-8"):
        return False
    append_block_to_file(path, block_text)
    return True


def remove_block_from_file(path: Path, block_text: str) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    idx = text.find(block_text)
    if idx == -1:
        return
    before = text[:idx]
    after = text[idx + len(block_text):]
    before = before.rstrip()
    after = after.lstrip()
    new_text = before
    if after:
        new_text += "\n\n" + after
    new_text = new_text.rstrip() + "\n"
    path.write_text(new_text, encoding="utf-8")


def _suggest_promotion_target(chunk: Chunk, override: str = "") -> str:
    if override:
        return override
    tags = set(chunk.metadata.tags)
    if "FTR" in tags:
        return "TOOLS.md"
    return "AGENTS.md"


def _resolve_promotion_target(workspace_root: Path, target_file: str) -> Path:
    target_path = (workspace_root / target_file).resolve()
    try:
        target_path.relative_to(workspace_root)
    except ValueError as e:
        raise ValueError(f"target must stay under workspace root: {target_file}") from e
    return target_path


def _promote_chunk(
    store: MemoryStore,
    workspace_root: Path,
    chunk: Chunk,
    target_file: str,
) -> Dict[str, Any]:
    entry_id = _extract_entry_id(chunk)
    target_path = _resolve_promotion_target(workspace_root, target_file)

    chunk.content = _replace_or_append_field(chunk.content, "Status", "promoted")
    chunk.content = _replace_or_append_field(chunk.content, "Promoted-To", target_file)
    chunk.metadata.tags = [t for t in chunk.metadata.tags if not t.startswith("status:")]
    chunk.metadata.tags.append("status:promoted")

    promoted_text = _render_chunk_as_markdown(chunk).rstrip()
    appended = append_block_to_file_once(target_path, promoted_text, entry_id)

    store.upsert_chunks([chunk])
    store.set_chunk_lifecycle(chunk.id, CHUNK_STATUS_SEALED)
    return {
        "id": entry_id,
        "chunk_id": chunk.id,
        "target": target_file,
        "appended": appended,
    }


def _write_promotion_queue(
    base_dir: Path,
    store: MemoryStore,
    candidates: List[Dict[str, Any]],
    target_override: str = "",
) -> List[Dict[str, Any]]:
    generated_at = get_now().isoformat()
    records: List[Dict[str, Any]] = []
    seen: Set[str] = set()
    for item in candidates:
        chunk = store.get_chunk(item["chunk_id"])
        if chunk is None:
            continue
        entry_id = item["id"]
        if entry_id in seen:
            continue
        seen.add(entry_id)
        records.append({
            "id": entry_id,
            "chunk_id": chunk.id,
            "summary": item.get("summary") or _chunk_summary_text(chunk, max_chars=180),
            "recurrence_count": item.get("recurrence_count", _extract_recurrence_count(chunk)),
            "suggested_target": _suggest_promotion_target(chunk, target_override),
            "status": _extract_status(chunk),
            "queued_at": generated_at,
        })

    queue_path = base_dir / PROMOTION_QUEUE_FILE
    queue_path.write_text(json.dumps({
        "generated_at": generated_at,
        "count": len(records),
        "items": records,
    }, indent=2), encoding="utf-8")
    return records



def _do_volatile_check(text: str, force: bool) -> bool:
    warnings = check_volatile_patterns(text)
    if warnings:
        print("[log] Warning: volatile state detected in entry:")
        for w in warnings[:3]:
            print(f"  - {w}")
        if len(warnings) > 3:
            print(f"  ... and {len(warnings) - 3} more")
        if not force:
            print("[log] Aborting. Use --force to log volatile content anyway.")
            return False
    return True


def _validate_pattern_key(pattern_key: str) -> None:
    """Warn if Pattern-Key lacks namespaced format (project:key or domain:key)."""
    if pattern_key and ":" not in pattern_key:
        print(
            f"[warning] Pattern-Key '{pattern_key}' lacks namespace. "
            f"Use 'project:key' or 'domain:key' format (e.g., 'db:migration' not 'migration').",
            file=sys.stderr,
        )


def cmd_log_correction(args: argparse.Namespace) -> None:
    base_dir = get_base_dir_for_args(args)
    ensure_structure(base_dir)

    summary = redact_secrets(args.summary or "")
    correct = redact_secrets(args.correct or "")
    pattern_key = args.pattern or ""
    _validate_pattern_key(pattern_key)
    area = getattr(args, "area", "") or ""

    if not summary:
        print("[log-correction] Error: --summary required", file=sys.stderr)
        sys.exit(1)
    if not correct:
        print("[log-correction] Error: --correct required", file=sys.stderr)
        sys.exit(1)

    search_term = f"{summary} {correct} {pattern_key}".strip()
    if not _do_volatile_check(search_term, args.force):
        return

    store = get_store_for_args(args)
    with store:
        details = f"What I got wrong: {summary}\nCorrect answer: {correct}"
        entry_id = _ingest_entry(
            store, "COR", summary, details, pattern_key, area, force=args.force,
        )
    if entry_id:
        print(f"[log-correction] Logged: {entry_id}")
        update_index(base_dir)
    else:
        print(f"[log-correction] Skipped (duplicate): {summary[:60]}...")


def cmd_log_learning(args: argparse.Namespace) -> None:
    base_dir = get_base_dir_for_args(args)
    ensure_structure(base_dir)

    summary = redact_secrets(args.summary or "")
    details = redact_secrets(args.details or "")
    pattern_key = args.pattern or ""
    _validate_pattern_key(pattern_key)
    area = getattr(args, "area", "") or ""

    if not summary:
        print("[log-learning] Error: --summary required", file=sys.stderr)
        sys.exit(1)

    search_term = f"{summary} {details} {pattern_key}".strip()
    if not _do_volatile_check(search_term, args.force):
        return

    store = get_store_for_args(args)
    with store:
        entry_id = _ingest_entry(
            store, "LRN", summary, details, pattern_key, area, force=args.force,
        )
    if entry_id:
        print(f"[log-learning] Logged: {entry_id}")
        update_index(base_dir)
    else:
        print(f"[log-learning] Skipped (duplicate): {summary[:60]}...")


def cmd_log_error(args: argparse.Namespace) -> None:
    base_dir = get_base_dir_for_args(args)
    ensure_structure(base_dir)

    summary = redact_secrets(args.summary or "")
    details = redact_secrets(args.details or "")
    pattern_key = args.pattern or ""
    _validate_pattern_key(pattern_key)
    area = getattr(args, "area", "") or ""

    if not summary:
        print("[log-error] Error: --summary required", file=sys.stderr)
        sys.exit(1)

    search_term = f"{summary} {details} {pattern_key}".strip()
    if not _do_volatile_check(search_term, args.force):
        return

    store = get_store_for_args(args)
    with store:
        entry_id = _ingest_entry(
            store, "ERR", summary, details, pattern_key, area, force=args.force,
        )
    if entry_id:
        print(f"[log-error] Logged: {entry_id}")
        update_index(base_dir)
    else:
        print(f"[log-error] Skipped (duplicate): {summary[:60]}...")


def cmd_log_feature(args: argparse.Namespace) -> None:
    base_dir = get_base_dir_for_args(args)
    ensure_structure(base_dir)

    summary = redact_secrets(args.summary or "")
    details = redact_secrets(args.details or "")
    pattern_key = args.pattern or ""
    _validate_pattern_key(pattern_key)
    area = getattr(args, "area", "") or ""

    if not summary:
        print("[log-feature] Error: --summary required", file=sys.stderr)
        sys.exit(1)

    search_term = f"{summary} {details} {pattern_key}".strip()
    if not _do_volatile_check(search_term, args.force):
        return

    store = get_store_for_args(args)
    with store:
        entry_id = _ingest_entry(
            store, "FTR", summary, details, pattern_key, area, force=args.force,
        )
    if entry_id:
        print(f"[log-feature] Logged: {entry_id}")
        update_index(base_dir)
    else:
        print(f"[log-feature] Skipped (duplicate): {summary[:60]}...")


def cmd_log(args: argparse.Namespace) -> None:
    base_dir = get_base_dir_for_args(args)
    ensure_structure(base_dir)

    log_type = (args.type or "LRN").upper()
    content = redact_secrets(args.content or "")
    pattern_key = args.pattern or ""
    _validate_pattern_key(pattern_key)
    correct = redact_secrets(args.correct or "")
    area = getattr(args, "area", "") or ""

    if not content:
        print("[log] Error: content required", file=sys.stderr)
        sys.exit(1)
    if log_type not in ID_PREFIXES:
        print("[log] Error: --type must be one of COR/LRN/FTR/ERR", file=sys.stderr)
        sys.exit(1)
    if log_type == "COR" and not correct:
        print("[log] Error: --correct required for --type COR", file=sys.stderr)
        sys.exit(1)

    search_term = f"{content} {correct} {pattern_key}".strip()
    if not _do_volatile_check(search_term, args.force):
        return

    if log_type == "COR":
        details = f"What I got wrong: {content}\nCorrect answer: {correct}"
        entry_type = "COR"
    else:
        prefix = ID_PREFIXES.get(log_type, "LRN")
        entry_type = prefix
        details = content

    store = get_store_for_args(args)
    with store:
        entry_id = _ingest_entry(
            store, entry_type, content, details, pattern_key, area, force=args.force,
        )
    if entry_id:
        print(f"[log] {entry_type} logged: {entry_id}")
        update_index(base_dir)
    else:
        print(f"[log] Skipped (duplicate): {content[:60]}...")


def _parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%Y%m%d"):
        try:
            return datetime.strptime(date_str.strip(), fmt).replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            continue
    return None


def _parse_entries(text: str) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    pattern = re.compile(
        r'^###\s+([A-Z]{3}-\d{8}-\d{3})\s+\(([^)]+)\)(?:\s*\[Pattern-Key:\s*([^\]]+)\])?\s*\n'
        r'(.*?)(?=^###\s+[A-Z]{3}-\d{8}-\d{3}|\Z)',
        re.MULTILINE | re.DOTALL,
    )
    for m in pattern.finditer(text):
        entry_id = m.group(1)
        date_str = m.group(2)
        pattern_key = (m.group(3) or "").strip()
        body = m.group(4)

        metadata: Dict[str, str] = {}
        for line in body.split("\n"):
            meta_match = re.match(r'- \*\*([^*]+)\*\*:\s*(.*)', line)
            if meta_match:
                key = meta_match.group(1).strip()
                value = meta_match.group(2).strip()
                metadata[key] = value

        first_seen = _parse_date(metadata.get("First-Seen", ""))
        last_seen = _parse_date(metadata.get("Last-Seen", ""))
        recurrence_count = 0
        try:
            recurrence_count = int(metadata.get("Recurrence-Count", "0"))
        except (ValueError, TypeError):
            pass

        entries.append({
            "id": entry_id,
            "date_str": date_str,
            "pattern_key": pattern_key,
            "body": body,
            "metadata": metadata,
            "first_seen": first_seen,
            "last_seen": last_seen,
            "recurrence_count": recurrence_count,
            "status": metadata.get("Status", ""),
            "area": metadata.get("Area", ""),
            "full_text": m.group(0),
            "start": m.start(),
            "end": m.end(),
        })
    return entries


def _remove_entries_from_text(text: str, entries_to_remove: List[Dict[str, Any]]) -> str:
    if not entries_to_remove:
        return text
    sorted_entries = sorted(entries_to_remove, key=lambda e: e["start"], reverse=True)
    result = text
    for entry in sorted_entries:
        result = result[:entry["start"]] + result[entry["end"]:]
    return result


def cmd_maintain(args: argparse.Namespace) -> None:
    base_dir = get_base_dir_for_args(args)
    ensure_structure(base_dir)

    dry_run = getattr(args, "dry_run", True)
    fmt = getattr(args, "format", "text") or "text"
    auto_promote = bool(getattr(args, "auto_promote", False))
    promotion_target = getattr(args, "promotion_target", "") or ""
    auto_promoted: List[Dict[str, Any]] = []

    store = get_store_for_args(args)
    with store:
        results = _maintenance_plan(store)
        if not dry_run:
            _apply_maintenance_plan(store, results)
            if auto_promote:
                workspace_root = get_workspace_root(resolve_root(args))
                for candidate in results["promote_candidates"]:
                    chunk = store.get_chunk(candidate["chunk_id"])
                    if chunk is None:
                        continue
                    target = _suggest_promotion_target(chunk, promotion_target)
                    auto_promoted.append(_promote_chunk(store, workspace_root, chunk, target))
                if auto_promoted:
                    results = _maintenance_plan(store)

        _update_heartbeat_state(base_dir, results, dry_run)
        queued_promotions = _write_promotion_queue(
            base_dir,
            store,
            results["promote_candidates"],
            promotion_target,
        )

        if fmt == "json":
            print(json.dumps({
                "stale_hot": [
                    {"id": r["id"], "days_stale": r["days_stale"], "action": "HOT_TO_WARM"}
                    for r in results["stale_hot"]
                ],
                "stale_warm": [
                    {"id": r["id"], "days_stale": r["days_stale"], "action": "WARM_TO_COLD"}
                    for r in results["stale_warm"]
                ],
                "promote_candidates": results["promote_candidates"],
                "promotions_queued": queued_promotions,
                "auto_promoted": auto_promoted,
                "insufficient_metadata": results["insufficient_metadata"],
            }, indent=2))
            return

        if dry_run:
            print("[maintain] DRY RUN (use --apply to execute)")
        else:
            print("[maintain] APPLYING changes")

        stale_hot = results["stale_hot"]
        stale_warm = results["stale_warm"]
        promote_candidates = results["promote_candidates"]
        insufficient_metadata = results["insufficient_metadata"]
        has_any = bool(stale_hot or stale_warm or promote_candidates or insufficient_metadata or auto_promoted)

        if fmt == "text":
            if stale_hot:
                print("HOT -> WARM (stale >= 30 days):")
                for r in stale_hot:
                    print(f"  - {r['id']}: Last-Seen {r['last_seen']} ({r['days_stale']} days ago)")
            if stale_warm:
                print("WARM -> COLD (stale >= 90 days):")
                for r in stale_warm:
                    print(f"  - {r['id']}: Last-Seen {r['last_seen']} ({r['days_stale']} days ago)")
            if promote_candidates:
                print("Promotion candidates:")
                for r in promote_candidates:
                    print(f"  - {r['id']}: Recurrence-Count={r['recurrence_count']} -> {r['suggested_target']}")
                print(f"  queued: {base_dir / PROMOTION_QUEUE_FILE}")
            if auto_promoted:
                print("Auto-promoted:")
                for r in auto_promoted:
                    suffix = "" if r["appended"] else " (already present)"
                    print(f"  - {r['id']}: {r['target']}{suffix}")
            if insufficient_metadata:
                print("Insufficient metadata:")
                for r in insufficient_metadata:
                    print(f"  - {r['id']}: {r['reason']}")
            if not has_any:
                print("  All entries healthy. No action needed.")


def cmd_promote(args: argparse.Namespace) -> None:
    """Promote an entry from its current tier to a target memory file."""
    base_dir = get_base_dir_for_args(args)
    ensure_structure(base_dir)
    entry_id = args.entry_id
    target_file = args.to or ""
    if not target_file:
        print("[promote] Error: --to TARGET is required", file=sys.stderr)
        sys.exit(1)

    store = get_store_for_args(args)
    with store:
        chunk = _find_chunk_by_entry_id(store, entry_id)
        if not chunk:
            print(f"[promote] Entry {entry_id} not found", file=sys.stderr)
            sys.exit(1)

        workspace_root = get_workspace_root(resolve_root(args))
        try:
            result = _promote_chunk(store, workspace_root, chunk, target_file)
        except ValueError as e:
            print(f"[promote] Error: {e}", file=sys.stderr)
            sys.exit(1)

    suffix = "" if result["appended"] else " (already present)"
    print(f"[promote] Promoted {result['id']} to {target_file}{suffix}")
    update_index(base_dir)


def cmd_export(args: argparse.Namespace) -> None:
    """Export all entries as human-readable markdown (backed by SQLite)."""
    base_dir = get_base_dir_for_args(args)
    fmt = getattr(args, "format", "text") or "text"
    store = get_store_for_args(args)
    with store:
        chunks = store.list_chunks(ListChunksQuery(limit=10000))

    rendered = [_render_chunk_as_markdown(c) for c in chunks]

    if fmt == "json":
        output_obj = [
            {
                "id": _extract_entry_id(c),
                "chunk_id": c.id,
                "type": c.metadata.tags[0] if c.metadata.tags else "LRN",
                "status": _extract_status(c),
                "content": _render_chunk_as_markdown(c),
            }
            for c in chunks
        ]
        output = json.dumps(output_obj, indent=2)
    else:
        output = "\n".join(["# Memory (SQLite-backed export)", ""] + rendered)

    file_path = args.output if hasattr(args, "output") and args.output else ""
    if file_path:
        Path(file_path).write_text(output, encoding="utf-8")
        print(f"[export] Wrote {len(chunks)} entries to {file_path}")
    else:
        print(output)


_SOURCE_KIND_MAP = {
    "chat": SourceKind.CHAT,
    "email": SourceKind.EMAIL,
    "document": SourceKind.DOCUMENT,
}


def cmd_ingest(args: argparse.Namespace) -> None:
    """Ingest external content through the full chunker pipeline."""
    base_dir = get_base_dir_for_args(args)
    ensure_structure(base_dir)

    kind = _SOURCE_KIND_MAP.get((args.kind or "").lower())
    if kind is None:
        print(f"[ingest] Error: unknown kind '{args.kind}'. Use one of: chat, email, document", file=sys.stderr)
        sys.exit(1)

    if args.file:
        try:
            content = Path(args.file).read_text(encoding="utf-8")
            source_id = args.source_id or f"file/{args.file}"
        except Exception as e:
            print(f"[ingest] Error reading {args.file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        content = sys.stdin.read()
        source_id = args.source_id or "stdin"

    if not content.strip():
        print("[ingest] Error: empty content", file=sys.stderr)
        sys.exit(1)

    owner = getattr(args, "owner", "") or "user"
    now = get_now()
    metadata = Metadata(
        source_kind=kind,
        source_id=source_id,
        owner=owner,
        timestamp=now,
        time_range=(now, now),
        tags=args.tags.split(",") if args.tags else [],
    )

    store = get_store_for_args(args)
    with store:
        result = ingest_markdown(
            store,
            source_kind=kind,
            source_id=source_id,
            markdown=content,
            metadata=metadata,
            dedup=not args.no_dedup,
        )

    if result.already_ingested:
        print(f"[ingest] Skipped (already ingested): {source_id}")
        return

    total = result.chunks_written + result.chunks_dropped
    print(f"[ingest] Wrote {result.chunks_written} chunk(s) from '{source_id}' "
          f"({result.chunks_dropped} dropped, {total} total)")
    if result.chunk_ids:
        for cid in result.chunk_ids[:5]:
            print(f"  {cid}")
        if len(result.chunk_ids) > 5:
            print(f"  ... and {len(result.chunk_ids) - 5} more")


def cmd_process_jobs(args: argparse.Namespace) -> None:
    """Run the SQLite-backed memory job worker."""
    base_dir = get_base_dir_for_args(args)
    ensure_structure(base_dir)

    fmt = getattr(args, "format", "text") or "text"
    daemon = bool(getattr(args, "daemon", False))
    max_jobs = int(getattr(args, "max_jobs", 100) or 0)
    idle_sleep = float(getattr(args, "idle_sleep", 5.0) or 0.1)
    maintenance_interval_ms = int(float(getattr(args, "maintenance_interval_seconds", 86400)) * 1000)
    kinds_text = getattr(args, "kinds", "") or ""
    kinds = [k.strip() for k in kinds_text.split(",") if k.strip()] or None
    include_maintenance = not bool(getattr(args, "no_maintenance", False))

    processed = 0
    completed = 0
    failed = 0
    results: List[Dict[str, Any]] = []

    store = get_store_for_args(args)
    try:
        with store:
            if include_maintenance and (kinds is None or "maintain_lifecycle" in kinds):
                _ensure_lifecycle_job(store)

            while True:
                if max_jobs > 0 and processed >= max_jobs:
                    break

                job = store.claim_next_job(kinds=kinds)
                if job is None:
                    if not daemon:
                        break
                    time.sleep(max(0.1, idle_sleep))
                    if include_maintenance and (kinds is None or "maintain_lifecycle" in kinds):
                        _ensure_lifecycle_job(store)
                    continue

                processed += 1
                item: Dict[str, Any] = {
                    "id": job["id"],
                    "kind": job["kind"],
                    "status": "completed",
                }
                try:
                    item["result"] = _process_job(store, base_dir, job)
                    store.complete_job(int(job["id"]))
                    completed += 1
                    if daemon and job["kind"] == "maintain_lifecycle":
                        store.enqueue_job(MemoryStore.JobRow(
                            kind="maintain_lifecycle",
                            payload_json=json.dumps({"dry_run": False}),
                            priority=-50,
                            max_retries=1,
                            scheduled_at_ms=int(get_now().timestamp() * 1000) + maintenance_interval_ms,
                            dedupe_key="maintain:lifecycle",
                        ))
                except Exception as e:
                    item["status"] = "failed"
                    item["error"] = str(e)
                    store.fail_job(int(job["id"]), str(e))
                    failed += 1
                results.append(item)

    except KeyboardInterrupt:
        pass

    with store:
        queue = store.job_status_counts()

    if fmt == "json":
        print(json.dumps({
            "processed": processed,
            "completed": completed,
            "failed": failed,
            "queue": queue,
            "jobs": results,
        }, indent=2, default=str))
        return

    print(f"[process-jobs] processed={processed} completed={completed} failed={failed}")
    if queue:
        print("[process-jobs] queue:")
        for status, count in sorted(queue.items()):
            print(f"  {status}: {count}")
    for item in results[:10]:
        suffix = ""
        if item.get("error"):
            suffix = f" error={item['error']}"
        print(f"  - #{item['id']} {item['kind']} {item['status']}{suffix}")


def cmd_edit(args: argparse.Namespace) -> None:
    """Edit metadata of an existing entry in-place."""
    base_dir = get_base_dir_for_args(args)
    ensure_structure(base_dir)
    entry_id = args.entry_id
    new_status = getattr(args, "status", None)
    new_last_seen = getattr(args, "last_seen", None)
    new_recurrence = getattr(args, "recurrence", None)

    if not any([new_status, new_last_seen, new_recurrence]):
        print("[edit] Error: at least one of --status, --last-seen, --recurrence is required", file=sys.stderr)
        sys.exit(1)

    store = get_store_for_args(args)
    with store:
        chunk = _find_chunk_by_entry_id(store, entry_id)
        if not chunk:
            print(f"[edit] Entry {entry_id} not found", file=sys.stderr)
            sys.exit(1)

        if new_status:
            chunk.content = _replace_or_append_field(chunk.content, "Status", new_status)
            chunk.metadata.tags = [t for t in chunk.metadata.tags if not t.startswith("status:")]
            chunk.metadata.tags.append(f"status:{new_status}")
            if new_status in {"promoted", "promoted_to_skill", "resolved"}:
                store.set_chunk_lifecycle(chunk.id, CHUNK_STATUS_SEALED)
        if new_last_seen:
            parsed = _parse_date(new_last_seen)
            if not parsed:
                print(f"[edit] Error: invalid --last-seen date: {new_last_seen}", file=sys.stderr)
                sys.exit(1)
            chunk.content = _replace_or_append_field(chunk.content, "Last-Seen", new_last_seen)
            chunk.metadata.timestamp = parsed
            chunk.metadata.time_range = (chunk.metadata.time_range[0], parsed)
        if new_recurrence is not None:
            chunk.content = _replace_or_append_field(chunk.content, "Recurrence-Count", str(new_recurrence))
            score_row = store.get_score(chunk.id)
            if score_row:
                score_row.interaction_weight = max(score_row.interaction_weight, new_recurrence / 10.0)
                score_row.computed_at_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
                store.upsert_scores([score_row])

        store.upsert_chunks([chunk])

    print(f"[edit] Updated {_extract_entry_id(chunk)}")

def _update_heartbeat_state(base_dir: Path, results: Dict[str, List[Dict[str, Any]]], dry_run: bool) -> None:
    """Write/update heartbeat-state.md with timestamp and result summary from maintain."""
    state_file = base_dir / "heartbeat-state.md"
    now = get_now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S %Z")

    action_count = sum(len(v) for k, v in results.items() if k != "entry")
    result = f"dry-run: {action_count} candidates identified" if dry_run else f"apply: {action_count} actions applied"

    lines = [
        "# Self-Improving Heartbeat State",
        "",
        f"last_heartbeat_started_at: {timestamp}",
        f"last_reviewed_change_at: {timestamp}",
        f"last_heartbeat_result: {result}",
        "",
        "## Last actions",
    ]

    actions: List[str] = []
    for category, items in results.items():
        if category == "entry":
            continue
        for item in items:
            aid = item.get("id", "?")
            act = item.get("action", category)
            actions.append(f"- {act}: {aid}")

    if actions:
        prev_actions: List[str] = []
        if state_file.exists():
            for line in state_file.read_text(encoding="utf-8").split("\n"):
                stripped = line.strip()
                if stripped.startswith("- "):
                    prev_actions.append(line)
        all_actions = actions + prev_actions
        lines.extend(all_actions[:20])
    else:
        lines.append("- No actions taken")

    lines.append("")
    state_file.write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Self-Improving Learning Log (Hybrid)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment:
  OPENCLAW_WORKSPACE              Default workspace root if --root is not provided.
  SELF_IMPROVING_LEARNING_ROOT    Shared learning store directory. When set,
                                  SQLite/index/queue files live here instead of
                                  <workspace>/learning.

Examples:
  %(prog)s --root /path/to/workspace init
  %(prog)s --root /path/to/workspace log-correction --summary "Used wrong format" --correct "Use lists" --pattern telegram-format --force
  %(prog)s --root /path/to/workspace log-learning --summary "Search before logging" --details "Avoid duplicates" --pattern dedupe-rule --force
  %(prog)s --root /path/to/workspace search telegram
  %(prog)s --root /path/to/workspace status
  %(prog)s status --root /path/to/workspace --format json
  %(prog)s --root /path/to/workspace maintain
  %(prog)s --root /path/to/workspace maintain --apply
        """,
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Workspace root (default: OPENCLAW_WORKSPACE env, else current directory)",
    )
    parser.add_argument(
        "--learning-root",
        default=None,
        help="Learning store directory (default: SELF_IMPROVING_LEARNING_ROOT env, else <workspace>/learning)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    def _add_root(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--root",
            dest="local_root",
            default=None,
            help="Workspace root (overrides global --root)",
        )
        parser.add_argument(
            "--learning-root",
            dest="local_learning_root",
            default=None,
            help="Learning store directory (overrides global --learning-root)",
        )

    p_init = sub.add_parser("init", help="Initialize learning/ structure")
    _add_root(p_init)
    p_init.set_defaults(func=cmd_init)

    p_status = sub.add_parser("status", help="Show memory status")
    _add_root(p_status)
    p_status.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    p_status.set_defaults(func=cmd_status)

    p_search = sub.add_parser("search", help="Search learning records")
    _add_root(p_search)
    p_search.add_argument("query", nargs="?", help="Search query")
    p_search.add_argument("--limit", "-l", type=int, default=20, help="Result limit")
    p_search.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    p_search.add_argument("--touch", action="store_true", help="Record matching entries as reused")
    p_search.set_defaults(func=cmd_search)

    p_log = sub.add_parser("log", help="Legacy alias for log-correction/log-learning/log-error/log-feature")
    _add_root(p_log)
    p_log.add_argument("content", nargs="?", help="Learning content")
    p_log.add_argument("--type", "-t", default="LRN", help="Entry type (COR/LRN/FTR/ERR)")
    p_log.add_argument("--pattern", "-p", default="", help="Pattern-Key identifier")
    p_log.add_argument("--correct", "-c", default="", help="Correct answer (for COR type)")
    p_log.add_argument("--area", "-a", default="", help="Area (project:name or domain:name)")
    p_log.add_argument("--force", "-f", action="store_true", help="Skip dedup check")
    p_log.set_defaults(func=cmd_log)

    p_logc = sub.add_parser("log-correction", help="Log a correction")
    _add_root(p_logc)
    p_logc.add_argument("--summary", "-s", required=True, help="What went wrong")
    p_logc.add_argument("--correct", "-c", required=True, help="The correct answer")
    p_logc.add_argument("--pattern", "-p", default="", help="Pattern-Key identifier")
    p_logc.add_argument("--area", "-a", default="", help="Area (project:name or domain:name)")
    p_logc.add_argument("--force", "-f", action="store_true", help="Skip dedup check")
    p_logc.set_defaults(func=cmd_log_correction)

    p_logl = sub.add_parser("log-learning", help="Log a learning")
    _add_root(p_logl)
    p_logl.add_argument("--summary", "-s", required=True, help="Learning summary")
    p_logl.add_argument("--details", "-d", default="", help="Learning details")
    p_logl.add_argument("--pattern", "-p", default="", help="Pattern-Key identifier")
    p_logl.add_argument("--area", "-a", default="", help="Area (project:name or domain:name)")
    p_logl.add_argument("--force", "-f", action="store_true", help="Skip dedup check")
    p_logl.set_defaults(func=cmd_log_learning)

    p_loge = sub.add_parser("log-error", help="Log an error")
    _add_root(p_loge)
    p_loge.add_argument("--summary", "-s", required=True, help="Error summary")
    p_loge.add_argument("--details", "-d", default="", help="Error details")
    p_loge.add_argument("--pattern", "-p", default="", help="Pattern-Key identifier")
    p_loge.add_argument("--area", "-a", default="", help="Area (project:name or domain:name)")
    p_loge.add_argument("--force", "-f", action="store_true", help="Skip dedup check")
    p_loge.set_defaults(func=cmd_log_error)

    p_logf = sub.add_parser("log-feature", help="Log a feature request")
    _add_root(p_logf)
    p_logf.add_argument("--summary", "-s", required=True, help="Feature summary")
    p_logf.add_argument("--details", "-d", default="", help="Feature details")
    p_logf.add_argument("--pattern", "-p", default="", help="Pattern-Key identifier")
    p_logf.add_argument("--area", "-a", default="", help="Area (project:name or domain:name)")
    p_logf.add_argument("--force", "-f", action="store_true", help="Skip dedup check")
    p_logf.set_defaults(func=cmd_log_feature)

    p_maintain = sub.add_parser("maintain", help="Maintain memory lifecycle")
    _add_root(p_maintain)
    p_maintain.add_argument("--apply", dest="dry_run", action="store_false", help="Apply moves (default is dry-run)")
    p_maintain.add_argument("--dry-run", dest="dry_run", action="store_true", default=True, help="Show what would be done without applying")
    p_maintain.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    p_maintain.add_argument("--auto-promote", action="store_true",
                            help="With --apply, promote queued candidates into workspace memory files")
    p_maintain.add_argument("--promotion-target", default="",
                            help="Override the suggested promotion target file for maintain --auto-promote")
    p_maintain.set_defaults(func=cmd_maintain)

    p_promote = sub.add_parser("promote", help="Promote an entry to a target memory file")
    _add_root(p_promote)
    p_promote.add_argument("entry_id", help="Entry ID (e.g., LRN-20260512-001)")
    p_promote.add_argument("--to", "-t", required=True, help="Target file path (e.g., CLAUDE.md or projects/foo.md)")
    p_promote.set_defaults(func=cmd_promote)

    p_edit = sub.add_parser("edit", help="Edit entry metadata in-place")
    _add_root(p_edit)
    p_edit.add_argument("entry_id", help="Entry ID (e.g., COR-20260512-001)")
    p_edit.add_argument("--status", choices=["pending", "in_progress", "resolved", "wont_fix", "promoted", "promoted_to_skill"], help="New status")
    p_edit.add_argument("--last-seen", help="New Last-Seen date (YYYY-MM-DD)")
    p_edit.add_argument("--recurrence", type=int, help="New Recurrence-Count")
    p_edit.set_defaults(func=cmd_edit)

    p_export = sub.add_parser("export", help="Export entries as markdown")
    _add_root(p_export)
    p_export.add_argument("--output", "-o", default="", help="Output file path (omit for stdout)")
    p_export.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    p_export.set_defaults(func=cmd_export)

    p_ingest = sub.add_parser("ingest", help="Ingest content through chunker pipeline")
    _add_root(p_ingest)
    p_ingest.add_argument("--kind", "-k", required=True, choices=["chat", "email", "document"],
                          help="Source kind (determines chunking strategy)")
    p_ingest.add_argument("--file", "-f", default="", help="File path (omit for stdin)")
    p_ingest.add_argument("--source-id", default="", help="Stable source id for dedup (default: auto)")
    p_ingest.add_argument("--title", "-t", default="", help="Content title")
    p_ingest.add_argument("--tags", default="", help="Comma-separated tags")
    p_ingest.add_argument("--no-dedup", action="store_true", help="Skip dedup check")
    p_ingest.set_defaults(func=cmd_ingest)

    p_jobs = sub.add_parser("process-jobs", help="Run queued async memory jobs")
    _add_root(p_jobs)
    p_jobs.add_argument("--max-jobs", type=int, default=100, help="Maximum jobs to process (0 = unlimited)")
    p_jobs.add_argument("--daemon", action="store_true", help="Keep polling for due jobs until interrupted")
    p_jobs.add_argument("--idle-sleep", type=float, default=5.0, help="Seconds to sleep when daemon is idle")
    p_jobs.add_argument("--kinds", default="", help="Comma-separated job kinds to process")
    p_jobs.add_argument("--no-maintenance", action="store_true", help="Do not auto-enqueue lifecycle maintenance")
    p_jobs.add_argument("--maintenance-interval-seconds", type=float, default=86400.0,
                        help="Daemon reschedule interval for lifecycle maintenance")
    p_jobs.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    p_jobs.set_defaults(func=cmd_process_jobs)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
        return 0
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
