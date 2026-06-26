#!/usr/bin/env python3
"""Shared helpers for the zotero-vectorize skill.

This module is intentionally dependency-light except for the optional embedding/PDF
libraries used by specific commands.
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
DEFAULT_METADATA_BATCH_SIZE = 50
DEFAULT_FULLTEXT_BATCH_SIZE = 32
DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 100

METADATA_VECTORS_FILENAME = "metadata_vectors.json"
FULLTEXT_VECTORS_FILENAME = "fulltext_vectors.json"
STORE_METADATA_FILENAME = "vector_store_metadata.json"
README_FILENAME = "README.md"


@dataclass
class ZoteroPaths:
    data_dir: Path
    db_path: Path
    storage_dir: Path
    output_dir: Path


def default_zotero_data_dir() -> Path:
    return Path.home() / "Zotero"


def resolve_paths(
    *,
    data_dir: str | None = None,
    db_path: str | None = None,
    storage_dir: str | None = None,
    output_dir: str | None = None,
) -> ZoteroPaths:
    data_dir_path = Path(
        data_dir or os.environ.get("ZOTERO_DATA_DIR") or default_zotero_data_dir()
    ).expanduser()
    db_path_path = Path(
        db_path or os.environ.get("ZOTERO_DB") or data_dir_path / "zotero.sqlite"
    ).expanduser()
    storage_dir_path = Path(
        storage_dir or os.environ.get("ZOTERO_STORAGE") or data_dir_path / "storage"
    ).expanduser()
    output_dir_path = Path(
        output_dir or os.environ.get("ZOTERO_VECTORS_DIR") or Path.cwd() / "zotero-vectors"
    ).expanduser()

    return ZoteroPaths(
        data_dir=data_dir_path,
        db_path=db_path_path,
        storage_dir=storage_dir_path,
        output_dir=output_dir_path,
    )


def ensure_output_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def metadata_vectors_path(output_dir: Path) -> Path:
    return output_dir / METADATA_VECTORS_FILENAME


def fulltext_vectors_path(output_dir: Path) -> Path:
    return output_dir / FULLTEXT_VECTORS_FILENAME


def store_metadata_path(output_dir: Path) -> Path:
    return output_dir / STORE_METADATA_FILENAME


def readme_path(output_dir: Path) -> Path:
    return output_dir / README_FILENAME


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


def file_size_bytes(path: Path) -> int:
    return path.stat().st_size if path.exists() else 0


def human_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(num_bytes)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{num_bytes} B"


def backup_with_retention(file_path: Path, keep: int = 2, timestamp: str | None = None) -> Path | None:
    if not file_path.exists():
        return None

    timestamp = timestamp or time.strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.parent / f"{file_path.name}.bak_{timestamp}"
    shutil.copy2(file_path, backup_path)

    backups = sorted(
        file_path.parent.glob(f"{file_path.name}.bak_*"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for old in backups[keep:]:
        old.unlink(missing_ok=True)

    return backup_path


def backup_store_files(output_dir: Path, keep: int = 2) -> list[Path]:
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    created = []
    for path in [
        metadata_vectors_path(output_dir),
        fulltext_vectors_path(output_dir),
        store_metadata_path(output_dir),
        readme_path(output_dir),
    ]:
        backup = backup_with_retention(path, keep=keep, timestamp=timestamp)
        if backup:
            created.append(backup)
    return created


def snapshot_database(source_db: Path, destination_dir: Path) -> Path:
    """Create a local snapshot of the Zotero SQLite database.

    Prefer filesystem copying over sqlite backup() because some live Zotero
    setups can block or hang on backup attempts while a fast copy of the main
    DB and sidecar files remains practical for read-only downstream work.
    """
    destination_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = destination_dir / f"zotero-snapshot-{time.strftime('%Y%m%d_%H%M%S')}.sqlite"

    shutil.copy2(source_db, snapshot_path)
    for suffix in ("-journal", "-wal", "-shm"):
        sidecar = Path(f"{source_db}{suffix}")
        if sidecar.exists():
            shutil.copy2(sidecar, Path(f"{snapshot_path}{suffix}"))

    return snapshot_path


def connect_db(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,))
    return cur.fetchone() is not None


def get_fields_table_name(conn: sqlite3.Connection) -> str:
    return "fieldsCombined" if table_exists(conn, "fieldsCombined") else "fields"


def get_item_types_table_name(conn: sqlite3.Connection) -> str:
    return "itemTypesCombined" if table_exists(conn, "itemTypesCombined") else "itemTypes"


def get_fields_map(conn: sqlite3.Connection) -> dict[int, str]:
    table = get_fields_table_name(conn)
    cur = conn.cursor()
    cur.execute(f"SELECT fieldID, fieldName FROM {table}")
    return {int(row["fieldID"]): row["fieldName"] for row in cur.fetchall()}


def get_item_types_map(conn: sqlite3.Connection) -> dict[int, str]:
    table = get_item_types_table_name(conn)
    cur = conn.cursor()
    cur.execute(f"SELECT itemTypeID, typeName FROM {table}")
    return {int(row["itemTypeID"]): row["typeName"] for row in cur.fetchall()}


def get_excluded_item_type_ids(conn: sqlite3.Connection) -> set[int]:
    table = get_item_types_table_name(conn)
    cur = conn.cursor()
    cur.execute(
        f"SELECT itemTypeID FROM {table} WHERE typeName IN ('annotation', 'attachment', 'note')"
    )
    return {int(row["itemTypeID"]) for row in cur.fetchall()}


def get_top_level_items(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    excluded_ids = sorted(get_excluded_item_type_ids(conn))
    placeholders = ",".join("?" for _ in excluded_ids) or "NULL"
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT itemID, key, itemTypeID, dateAdded, dateModified
        FROM items
        WHERE itemTypeID NOT IN ({placeholders})
        ORDER BY itemID
        """,
        excluded_ids,
    )
    return cur.fetchall()


def get_pdf_parent_rows(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT DISTINCT ia.parentItemID AS itemID
        FROM itemAttachments ia
        WHERE ia.parentItemID IS NOT NULL
          AND ia.contentType LIKE '%pdf%'
        ORDER BY ia.parentItemID
        """
    )
    return cur.fetchall()


def get_item_fields(conn: sqlite3.Connection, item_id: int, fields_map: dict[int, str]) -> dict[str, str]:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT fieldID, value
        FROM itemData id
        JOIN itemDataValues idv ON id.valueID = idv.valueID
        WHERE id.itemID = ?
        """,
        (item_id,),
    )
    data: dict[str, str] = {}
    for row in cur.fetchall():
        field_name = fields_map.get(int(row["fieldID"]), f"field_{row['fieldID']}")
        data[field_name] = row["value"]
    return data


def get_item_authors(conn: sqlite3.Connection, item_id: int) -> list[dict[str, str]]:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT c.firstName, c.lastName, ct.creatorType
        FROM itemCreators ic
        JOIN creators c ON ic.creatorID = c.creatorID
        JOIN creatorTypes ct ON ic.creatorTypeID = ct.creatorTypeID
        WHERE ic.itemID = ?
        ORDER BY ic.orderIndex
        """,
        (item_id,),
    )
    authors = []
    for row in cur.fetchall():
        first_name = row["firstName"] or ""
        last_name = row["lastName"] or ""
        name = f"{first_name} {last_name}".strip()
        if name:
            authors.append({"name": name, "type": row["creatorType"]})
    return authors


def get_item_tags(conn: sqlite3.Connection, item_id: int) -> list[str]:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT t.name
        FROM itemTags it
        JOIN tags t ON it.tagID = t.tagID
        WHERE it.itemID = ?
        ORDER BY t.name COLLATE NOCASE
        """,
        (item_id,),
    )
    return [row["name"] for row in cur.fetchall()]


def get_item_row(conn: sqlite3.Connection, item_id: int) -> sqlite3.Row | None:
    cur = conn.cursor()
    cur.execute(
        "SELECT itemID, key, itemTypeID, dateAdded, dateModified FROM items WHERE itemID = ?",
        (item_id,),
    )
    return cur.fetchone()


def build_item_metadata(
    conn: sqlite3.Connection,
    item_id: int,
    *,
    fields_map: dict[int, str],
    item_types_map: dict[int, str],
) -> tuple[dict, str]:
    row = get_item_row(conn, item_id)
    if row is None:
        raise ValueError(f"Item {item_id} not found")

    field_data = get_item_fields(conn, item_id, fields_map)
    item_type = item_types_map.get(int(row["itemTypeID"]), "unknown")
    authors = get_item_authors(conn, item_id)
    tags = get_item_tags(conn, item_id)

    metadata = {
        "title": field_data.get("title", ""),
        "abstractNote": field_data.get("abstractNote", ""),
        "date": field_data.get("date", ""),
        "dateAdded": row["dateAdded"],
        "dateModified": row["dateModified"],
        "DOI": field_data.get("DOI", ""),
        "url": field_data.get("url", ""),
        "authors": authors,
        "tags": tags,
    }

    if item_type == "journalArticle":
        metadata.update(
            {
                "publicationTitle": field_data.get("publicationTitle", ""),
                "volume": field_data.get("volume", ""),
                "issue": field_data.get("issue", ""),
                "pages": field_data.get("pages", ""),
            }
        )
    elif item_type == "book":
        metadata.update(
            {
                "publisher": field_data.get("publisher", ""),
                "ISBN": field_data.get("ISBN", ""),
            }
        )
    elif item_type == "thesis":
        metadata["university"] = field_data.get("university", "")
    elif item_type == "preprint":
        metadata["archive"] = field_data.get("archive", "")
    elif item_type == "webpage":
        metadata["websiteTitle"] = field_data.get("websiteTitle", "")

    embedding_text = create_embedding_text(metadata, item_type)
    return metadata, embedding_text


def create_embedding_text(metadata: dict, item_type: str) -> str:
    parts = []
    if metadata.get("title"):
        parts.append(f"Title: {metadata['title']}")
    parts.append(f"Type: {item_type}")
    if metadata.get("abstractNote"):
        parts.append(f"Abstract: {metadata['abstractNote']}")
    if metadata.get("publicationTitle"):
        parts.append(f"Publication: {metadata['publicationTitle']}")
    elif metadata.get("publisher"):
        parts.append(f"Publisher: {metadata['publisher']}")
    if metadata.get("tags"):
        parts.append(f"Tags: {', '.join(metadata['tags'])}")
    if metadata.get("authors"):
        parts.append("Authors: " + ", ".join(a["name"] for a in metadata["authors"]))
    if metadata.get("date"):
        parts.append(f"Date: {metadata['date']}")
    if metadata.get("DOI"):
        parts.append(f"DOI: {metadata['DOI']}")
    elif metadata.get("url"):
        parts.append(f"URL: {metadata['url']}")
    return "\n".join(parts)


def build_metadata_record(
    conn: sqlite3.Connection,
    item_id: int,
    *,
    fields_map: dict[int, str],
    item_types_map: dict[int, str],
    vector: list[float],
    model_name: str,
) -> dict:
    row = get_item_row(conn, item_id)
    metadata, embedding_text = build_item_metadata(
        conn,
        item_id,
        fields_map=fields_map,
        item_types_map=item_types_map,
    )
    item_type = item_types_map.get(int(row["itemTypeID"]), "unknown")
    return {
        "itemID": item_id,
        "key": row["key"],
        "metadata": metadata,
        "embedding_text": embedding_text,
        "itemType": item_type,
        "vector": vector,
        "vector_dimension": len(vector),
        "model": model_name,
    }


def scan_storage_for_pdfs(storage_dir: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for file_path in storage_dir.rglob("*.pdf"):
        index.setdefault(file_path.name, file_path)
    return index


def resolve_attachment_path(raw_path: str, storage_dir: Path, pdf_index: dict[str, Path]) -> Path | None:
    raw_path = raw_path or ""
    candidate = Path(raw_path)
    if candidate.is_absolute() and candidate.exists():
        return candidate

    if raw_path.startswith("storage:"):
        filename = Path(raw_path[len("storage:") :]).name
        return pdf_index.get(filename)

    if candidate.exists():
        return candidate

    joined = storage_dir / candidate.name
    if joined.exists():
        return joined

    return pdf_index.get(candidate.name)


def get_item_pdf_attachment(conn: sqlite3.Connection, item_id: int) -> sqlite3.Row | None:
    item_types_table = get_item_types_table_name(conn)
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT ia.itemID AS attachmentID, ia.path, ia.contentType,
               i.itemTypeID, it.typeName
        FROM itemAttachments ia
        JOIN items i ON ia.parentItemID = i.itemID
        LEFT JOIN {item_types_table} it ON i.itemTypeID = it.itemTypeID
        WHERE ia.parentItemID = ? AND ia.contentType LIKE '%pdf%'
        ORDER BY ia.itemID
        LIMIT 1
        """,
        (item_id,),
    )
    return cur.fetchone()


def extract_pdf_text(pdf_path: Path):
    import fitz

    doc = fitz.open(pdf_path)
    pages = []
    for page_num in range(len(doc)):
        text = doc[page_num].get_text("text")
        pages.append({"page": page_num + 1, "text": text})
    total_pages = len(doc)
    doc.close()
    full_text = "\n\n".join(page["text"] for page in pages)
    return {
        "pages": pages,
        "total_pages": total_pages,
        "full_text": full_text,
    }


def chunk_text(text: str, chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_CHUNK_OVERLAP) -> list[dict]:
    words = text.split()
    if not words:
        return []
    if len(words) <= chunk_size:
        return [{"text": text, "word_count": len(words), "start_word": 0, "end_word": len(words)}]

    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunks.append(
            {
                "text": " ".join(chunk_words),
                "word_count": len(chunk_words),
                "start_word": start,
                "end_word": end,
            }
        )
        start = end - overlap
        if start >= len(words) - overlap:
            if start < len(words):
                remainder = words[start:]
                chunks.append(
                    {
                        "text": " ".join(remainder),
                        "word_count": len(remainder),
                        "start_word": start,
                        "end_word": len(words),
                    }
                )
            break
    return chunks


def get_embedding_model(model_name: str = DEFAULT_MODEL):
    try:
        from sentence_transformers import SentenceTransformer
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "sentence-transformers is required. Install: pip install sentence-transformers"
        ) from exc
    return SentenceTransformer(model_name)


def encode_texts(model, texts: list[str], batch_size: int) -> list[list[float]]:
    if not texts:
        return []
    vectors: list[list[float]] = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        encoded = model.encode(batch, show_progress_bar=False)
        vectors.extend(encoded.tolist())
    return vectors


def default_store_metadata() -> dict:
    return {
        "generated_at": None,
        "embedding_model": DEFAULT_MODEL,
        "embedding_dimension": None,
        "chunk_size": DEFAULT_CHUNK_SIZE,
        "chunk_overlap": DEFAULT_CHUNK_OVERLAP,
        "paths": {},
        "statistics": {
            "metadata_items": 0,
            "fulltext_items": 0,
            "fulltext_chunks": 0,
        },
        "history": [],
    }


def update_store_metadata(
    store_meta: dict,
    *,
    paths: ZoteroPaths,
    model_name: str,
    embedding_dimension: int,
    metadata_count: int,
    fulltext_count: int,
    fulltext_chunks: int,
    operation: str,
    item_ids: Iterable[int] | None = None,
) -> dict:
    now = time.strftime("%Y-%m-%dT%H:%M:%S")
    store_meta = store_meta or default_store_metadata()
    store_meta["generated_at"] = now
    store_meta["embedding_model"] = model_name
    store_meta["embedding_dimension"] = embedding_dimension
    store_meta.setdefault("paths", {})
    store_meta["paths"].update(
        {
            "zotero_data_dir": str(paths.data_dir),
            "zotero_db": str(paths.db_path),
            "zotero_storage": str(paths.storage_dir),
            "output_dir": str(paths.output_dir),
            "metadata_vectors": str(metadata_vectors_path(paths.output_dir)),
            "fulltext_vectors": str(fulltext_vectors_path(paths.output_dir)),
        }
    )
    store_meta.setdefault("statistics", {})
    store_meta["statistics"].update(
        {
            "metadata_items": metadata_count,
            "fulltext_items": fulltext_count,
            "fulltext_chunks": fulltext_chunks,
        }
    )
    history_entry = {
        "timestamp": now,
        "operation": operation,
        "metadata_items": metadata_count,
        "fulltext_items": fulltext_count,
        "fulltext_chunks": fulltext_chunks,
    }
    if item_ids is not None:
        history_entry["itemIDs"] = list(item_ids)
    store_meta.setdefault("history", []).append(history_entry)
    return store_meta


def write_store_readme(output_dir: Path, store_meta: dict) -> None:
    stats = store_meta.get("statistics", {})
    content = f"""# Zotero Vector Store

This directory contains the outputs generated by the zotero-vectorize skill.

## Files
- `{METADATA_VECTORS_FILENAME}` — metadata embeddings for Zotero items
- `{FULLTEXT_VECTORS_FILENAME}` — chunked full-text embeddings from PDF attachments
- `{STORE_METADATA_FILENAME}` — build metadata, paths, and history

## Statistics
- Metadata items: {stats.get('metadata_items', 0)}
- Full-text items: {stats.get('fulltext_items', 0)}
- Full-text chunks: {stats.get('fulltext_chunks', 0)}
- Metadata vectors size: {human_size(file_size_bytes(metadata_vectors_path(output_dir)))}
- Full-text vectors size: {human_size(file_size_bytes(fulltext_vectors_path(output_dir)))}

## Embedding Model
- Model: {store_meta.get('embedding_model')}
- Dimension: {store_meta.get('embedding_dimension')}
- Chunk size: {store_meta.get('chunk_size')}
- Chunk overlap: {store_meta.get('chunk_overlap')}

## Safety Rules
- Treat Zotero as read-only input.
- Snapshot or back up before writing store updates.
- Keep only the latest and previous backup for each output file.
"""
    readme_path(output_dir).write_text(content, encoding="utf-8")


def print_json(payload) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
