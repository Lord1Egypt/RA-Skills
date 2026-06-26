#!/usr/bin/env python3
"""
sync_to_qdrant.py — SysClaw RAG sync pipeline

Reads from:
  - PostgreSQL (memory_entries, daily_logs, tools, skill_docs)
  - ~/.openclaw/memory/*.md files (MEMORY.md, YYYY-MM-DD.md, TOOLS.md)
  - ~/.openclaw/skills/**/*.md files

Embeds via any OpenAI-compatible endpoint (e.g. LiteLLM, Ollama) and upserts to Qdrant.

Usage:
  python sync_to_qdrant.py              # incremental sync (unsynced rows only)
  python sync_to_qdrant.py --full       # full resync, rebuilds all vectors
  python sync_to_qdrant.py --file PATH  # sync a single .md file immediately
"""

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator

import httpx
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

load_dotenv(Path(__file__).parent / "config.env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("sysclaw-rag")

# ── Config ────────────────────────────────────────────────────────────────────
QDRANT_HOST       = os.environ["QDRANT_HOST"]
QDRANT_API_KEY    = os.environ["QDRANT_API_KEY"]
POSTGRES_DSN      = os.environ["POSTGRES_DSN"]
EMBED_BASE_URL    = os.environ["EMBED_BASE_URL"].rstrip("/")
EMBED_API_KEY     = os.getenv("EMBED_API_KEY", "")
EMBED_MODEL       = os.getenv("EMBED_MODEL", "nomic-embed-text")
MEMORY_DIR        = Path(os.environ["MEMORY_DIR"]).expanduser()
SKILL_DIRS        = [Path(p).expanduser() for p in os.getenv("SKILL_DIRS", "").split(";") if p]
CHUNK_SIZE        = int(os.getenv("CHUNK_SIZE", 400))     # chars * ~4 ≈ tokens
CHUNK_CHARS       = CHUNK_SIZE * 4
CHUNK_OVERLAP_CH  = int(os.getenv("CHUNK_OVERLAP", 50)) * 4
BATCH_SIZE        = int(os.getenv("SYNC_BATCH_SIZE", 50))
BATCH_DELAY_S     = int(os.getenv("EMBED_BATCH_DELAY_MS", 250)) / 1000

# Qdrant collection names — namespaced by QDRANT_COLLECTION_PREFIX so multiple agents
# can share the same Qdrant instance without collision.
# Copy config.env to a new machine to keep the same collections.
_PREFIX = os.environ.get("QDRANT_COLLECTION_PREFIX", "").strip()
if not _PREFIX:
    raise SystemExit("ERROR: QDRANT_COLLECTION_PREFIX is not set in config.env")
COL_MEMORY = f"{_PREFIX}_memory"  # long-term facts + daily logs
COL_DOCS   = f"{_PREFIX}_docs"    # tools + skill docs

# ── Boilerplate filter ────────────────────────────────────────────────────────

_BOILERPLATE_RE = re.compile(
    r"^(##\s*Session:.*|Session\s+Key:.*|Session\s+ID:.*)$",
    re.MULTILINE | re.IGNORECASE,
)

def strip_boilerplate(text: str) -> str:
    return _BOILERPLATE_RE.sub("", text).strip()
VECTOR_DIM = 768                # nomic-embed-text output dimension


# ── Qdrant helpers ────────────────────────────────────────────────────────────

def get_qdrant() -> QdrantClient:
    from urllib.parse import urlparse
    parsed = urlparse(QDRANT_HOST)
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return QdrantClient(
        url=f"{parsed.scheme}://{parsed.hostname}:{port}",
        api_key=QDRANT_API_KEY or None,
        timeout=30,
        prefer_grpc=False,
    )


def ensure_collections(client: QdrantClient) -> None:
    existing = {c.name for c in client.get_collections().collections}
    for name in (COL_MEMORY, COL_DOCS):
        if name not in existing:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
            )
            log.info("Created Qdrant collection: %s", name)


# ── Embedding ──────────────────────────────────────────────────────────────────

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Call OpenAI-compatible /v1/embeddings endpoint for a batch of texts."""
    headers = {"Content-Type": "application/json"}
    if EMBED_API_KEY:
        headers["Authorization"] = f"Bearer {EMBED_API_KEY}"
    with httpx.Client(timeout=60) as client:
        r = client.post(
            f"{EMBED_BASE_URL}/v1/embeddings",
            json={"model": EMBED_MODEL, "input": texts},
            headers=headers,
        )
        r.raise_for_status()
        data = r.json()["data"]
        return [item["embedding"] for item in sorted(data, key=lambda x: x["index"])]


# ── Text chunking ─────────────────────────────────────────────────────────────

def chunk_text(text: str, source_hint: str = "") -> list[str]:
    """
    Split text into chunks, respecting markdown structure.
    Tries to split on section headers first, then paragraphs, then raw size.
    """
    if not text or not text.strip():
        return []

    # Try splitting on markdown h2/h3 headers first
    sections = re.split(r"\n(?=#{1,3} )", text)
    chunks: list[str] = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        if len(section) <= CHUNK_CHARS:
            if len(section) >= 80:  # skip tiny fragments
                chunks.append(section)
        else:
            # Section too large — split on paragraph breaks
            paragraphs = re.split(r"\n{2,}", section)
            current = ""
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                if len(current) + len(para) + 2 <= CHUNK_CHARS:
                    current = (current + "\n\n" + para).strip()
                else:
                    if current and len(current) >= 80:
                        chunks.append(current)
                    # If paragraph itself is huge, hard-split with overlap
                    if len(para) > CHUNK_CHARS:
                        for i in range(0, len(para), CHUNK_CHARS - CHUNK_OVERLAP_CH):
                            piece = para[i : i + CHUNK_CHARS]
                            if len(piece) >= 80:
                                chunks.append(piece)
                        current = ""
                    else:
                        current = para
            if current and len(current) >= 80:
                chunks.append(current)

    return chunks


def stable_id(source: str, chunk_index: int, content: str) -> str:
    """Generate a deterministic point ID from source + position + content hash."""
    raw = f"{source}::{chunk_index}::{hashlib.md5(content.encode()).hexdigest()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


# ── Upsert pipeline ───────────────────────────────────────────────────────────

def upsert_chunks(
    client: QdrantClient,
    collection: str,
    chunks: list[str],
    metadata: dict,
) -> int:
    """Embed chunks and upsert to Qdrant. Returns count of upserted points."""
    if not chunks:
        return 0

    source_id = metadata.get("source_id", metadata.get("source", "unknown"))
    points: list[PointStruct] = []

    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        try:
            vectors = embed_batch(batch)
            if BATCH_DELAY_S > 0:
                time.sleep(BATCH_DELAY_S)
        except Exception as e:
            log.error("Embedding failed for %s chunk %d-%d: %s", source_id, i, i + len(batch), e)
            continue

        for j, (text, vec) in enumerate(zip(batch, vectors)):
            point_id = stable_id(source_id, i + j, text)
            points.append(
                PointStruct(
                    id=point_id,
                    vector=vec,
                    payload={
                        "text": text,
                        "chunk_index": i + j,
                        **metadata,
                    },
                )
            )

    if points:
        client.upsert(collection_name=collection, points=points, wait=True)

    return len(points)


# ── Source readers ────────────────────────────────────────────────────────────

def sync_markdown_file(
    client: QdrantClient,
    path: Path,
    collection: str,
    source_type: str,
    extra_meta: dict | None = None,
) -> int:
    content = strip_boilerplate(path.read_text(encoding="utf-8", errors="replace"))
    chunks = chunk_text(content, source_hint=str(path))
    meta = {
        "source": source_type,
        "source_id": str(path),
        "file_path": str(path),
        "file_name": path.name,
        "indexed_at": datetime.now(timezone.utc).isoformat(),
        **(extra_meta or {}),
    }
    count = upsert_chunks(client, collection, chunks, meta)
    log.info("  %s → %d chunks upserted", path.name, count)
    return count


def sync_memory_files(client: QdrantClient) -> int:
    total = 0
    if not MEMORY_DIR.exists():
        log.warning("Memory dir not found: %s", MEMORY_DIR)
        return 0

    for md_file in sorted(MEMORY_DIR.glob("*.md")):
        name = md_file.stem.upper()

        # Classify file type
        if name == "MEMORY":
            src_type = "memory_longterm"
        elif re.match(r"\d{4}-\d{2}-\d{2}", md_file.stem):
            src_type = "memory_daily"
        elif name == "TOOLS":
            src_type = "tools"
        else:
            src_type = "memory_other"

        collection = COL_DOCS if src_type == "tools" else COL_MEMORY
        total += sync_markdown_file(client, md_file, collection, src_type)

    return total


def sync_skill_docs(client: QdrantClient) -> int:
    total = 0
    for skill_dir in SKILL_DIRS:
        if not skill_dir.exists():
            continue
        for md_file in skill_dir.rglob("*.md"):
            skill_name = md_file.parent.name
            total += sync_markdown_file(
                client,
                md_file,
                COL_DOCS,
                "skill_doc",
                {"skill_name": skill_name},
            )
    return total


def sync_postgres_incremental(client: QdrantClient, full: bool = False) -> int:
    total = 0
    try:
        conn = psycopg2.connect(POSTGRES_DSN)
    except Exception as e:
        log.error("Postgres connection failed: %s", e)
        return 0

    sync_filter = "" if full else "WHERE qdrant_synced_at IS NULL"

    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:

            # memory_entries
            cur.execute(f"SELECT * FROM memory_entries {sync_filter} ORDER BY created_at")
            for row in cur.fetchall():
                chunks = chunk_text(strip_boilerplate(row["content"]))
                meta = {
                    "source": "memory_entry",
                    "source_id": f"memory:{row['id']}",
                    "tags": row["tags"] or [],
                    "importance": row["importance"],
                    "created_at": row["created_at"].isoformat() if row["created_at"] else None,
                }
                n = upsert_chunks(client, COL_MEMORY, chunks, meta)
                total += n
                if n:
                    cur.execute(
                        "UPDATE memory_entries SET qdrant_synced_at=NOW() WHERE id=%s",
                        (row["id"],),
                    )

            # daily_logs
            cur.execute(f"SELECT * FROM daily_logs {sync_filter} ORDER BY log_date DESC")
            for row in cur.fetchall():
                chunks = chunk_text(strip_boilerplate(row["content"]))
                meta = {
                    "source": "daily_log",
                    "source_id": f"log:{row['id']}",
                    "log_date": str(row["log_date"]),
                    "section": row["section"],
                    "tags": row["tags"] or [],
                }
                n = upsert_chunks(client, COL_MEMORY, chunks, meta)
                total += n
                if n:
                    cur.execute(
                        "UPDATE daily_logs SET qdrant_synced_at=NOW() WHERE id=%s",
                        (row["id"],),
                    )

            # tools
            cur.execute(f"SELECT * FROM tools {sync_filter}")
            for row in cur.fetchall():
                text = f"# {row['name']}\n{row['description']}"
                if row["usage"]:
                    text += f"\n\nUsage:\n{row['usage']}"
                chunks = chunk_text(text)
                meta = {
                    "source": "tool",
                    "source_id": f"tool:{row['id']}",
                    "tool_name": row["name"],
                    "category": row["category"],
                    "tags": row["tags"] or [],
                }
                n = upsert_chunks(client, COL_DOCS, chunks, meta)
                total += n
                if n:
                    cur.execute(
                        "UPDATE tools SET qdrant_synced_at=NOW() WHERE id=%s",
                        (row["id"],),
                    )

    conn.close()
    return total


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SysClaw Qdrant sync")
    parser.add_argument("--full", action="store_true", help="Full resync, rebuilds all vectors")
    parser.add_argument("--file", type=Path, help="Sync a single .md file immediately")
    args = parser.parse_args()

    start = time.monotonic()
    client = get_qdrant()
    ensure_collections(client)
    total = 0

    if args.file:
        path = args.file.expanduser().resolve()
        log.info("Single-file sync: %s", path)
        total = sync_markdown_file(client, path, COL_MEMORY, "manual_import")
    else:
        mode = "FULL" if args.full else "INCREMENTAL"
        log.info("Starting %s sync", mode)
        total += sync_memory_files(client)
        total += sync_skill_docs(client)
        total += sync_postgres_incremental(client, full=args.full)

    elapsed = int((time.monotonic() - start) * 1000)
    log.info("Done — %d chunks synced in %dms", total, elapsed)

    # Record in Postgres
    try:
        conn = psycopg2.connect(POSTGRES_DSN)
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO qdrant_sync_log (records_synced, duration_ms) VALUES (%s, %s)",
                    (total, elapsed),
                )
        conn.close()
    except Exception:
        pass


if __name__ == "__main__":
    main()
