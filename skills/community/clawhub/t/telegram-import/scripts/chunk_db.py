#!/usr/bin/env python3
"""
Telegram messages -> LanceDB vector import.
Resume from checkpoint at D:\\edata.lance\\temp\\telegram.ckpt
Embedding: LM Studio text-embedding-qwen3-embedding-4b @ localhost:1234
"""

import os
import sys
import json
import pickle
import time
import sqlite3
import logging
import tempfile
from datetime import datetime

import requests
import numpy as np
import pyarrow as pa
import lance

# ── Config ──────────────────────────────────────────────────────────────────
DB_PATH        = r"D:\chat\telegram_messages.db"
TABLE_NAME     = "telegram_messages"
LANCE_PATH     = r"D:\edata.lance"
CKPT_PATH      = r"D:\edata.lance\temp\telegram.ckpt"
TEMP_DIR       = r"D:\edata.lance\temp"

LM_URL         = "http://127.0.0.1:1234/v1/embeddings"
LM_MODEL       = "text-embedding-qwen3-embedding-4b"
EMBED_DIM      = 2560
BATCH_SIZE     = 10
CKPT_INTERVAL  = 500
# ────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("telegram_import")


def load_checkpoint():
    if os.path.exists(CKPT_PATH):
        try:
            with open(CKPT_PATH, "rb") as f:
                data = pickle.load(f)
            log.info("Checkpoint loaded: last_idx=%d total_written=%d",
                     data.get("last_idx", -1), data.get("total_written", 0))
            return data
        except Exception as e:
            log.warning("Checkpoint unreadable (%s), starting fresh", e)
    return {"last_idx": -1, "seen_keys": set(), "total_written": 0}


def save_checkpoint(state):
    os.makedirs(TEMP_DIR, exist_ok=True)
    tmp = CKPT_PATH + ".tmp"
    with open(tmp, "wb") as f:
        pickle.dump(state, f)
    os.replace(tmp, CKPT_PATH)


def embed_texts(texts, timeout=120):
    """Call LM Studio embedding API. Returns list of float[EMBED_DIM] vectors."""
    resp = requests.post(
        LM_URL,
        json={"model": LM_MODEL, "input": texts},
        timeout=timeout,
    )
    resp.raise_for_status()
    result = resp.json()
    data = result["data"]
    data.sort(key=lambda x: x["index"])
    return [e["embedding"] for e in data]


def row_timestamp(row):
    d = row["date"]
    if isinstance(d, str):
        try:
            # "2024-01-01 12:00:00" or ISO string
            return datetime.fromisoformat(d.replace("Z", "+00:00")).timestamp()
        except Exception:
            return 0.0
    elif isinstance(d, (int, float)):
        return float(d)
    return 0.0


def row_metadata(row):
    return json.dumps({
        "group_name":         row["group_name"] or "",
        "group_id":           row["group_id"] or "",
        "message_id":         row["message_id"],
        "sender_id":          row["sender_id"],
        "sender_name":        row["sender_name"] or "",
        "matched_keywords":   row["matched_keywords"] or "",
        "is_reply":           row["is_reply"],
        "media_type":         row["media_type"] or "",
        "has_6_digit_number": row["has_6_digit_number"],
    }, ensure_ascii=False)


def main():
    start_time = time.time()
    log.info("=== Telegram Import Started ===")

    state          = load_checkpoint()
    last_idx       = state["last_idx"]
    seen_keys      = state["seen_keys"]
    total_written  = state["total_written"]

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    total_rows = cur.fetchone()[0]
    log.info("DB total rows: %d", total_rows)

    cur.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 1")
    cols = [d[0] for d in cur.description]
    log.info("Columns: %s", cols)

    # Detect existing dataset to choose create vs append mode
    dataset_exists = os.path.exists(LANCE_PATH) and os.listdir(LANCE_PATH)
    write_mode = "append" if dataset_exists else "create"
    log.info("LanceDB write mode: %s", write_mode)

    batch_keys   = []
    batch_texts  = []
    batch_rows   = []
    rows_since_ckpt = 0

    cur.execute(
        f"SELECT {','.join(cols)} FROM {TABLE_NAME} WHERE id > ? ORDER BY id",
        (last_idx,)
    )

    while True:
        block = cur.fetchmany(BATCH_SIZE)
        if not block:
            break

        for row in block:
            key = f"telegram:{row['group_id']}:{row['message_id']}"

            if key in seen_keys:
                continue

            msg = row["message"]
            if not msg or not str(msg).strip():
                seen_keys.add(key)
                continue

            batch_keys.append(key)
            batch_texts.append(str(msg))
            batch_rows.append(row)

            if len(batch_keys) < BATCH_SIZE:
                continue

            _write_batch(batch_keys, batch_texts, batch_rows, write_mode)
            total_written += len(batch_keys)
            seen_keys.update(batch_keys)
            rows_since_ckpt += len(batch_keys)
            write_mode = "append"  # always append after first write

            if rows_since_ckpt >= CKPT_INTERVAL:
                _save_state(state, last_idx=row["id"], seen_keys=seen_keys,
                            total_written=total_written)
                rows_since_ckpt = 0

            last_idx = row["id"]
            _log_progress(last_idx, total_rows, total_written, start_time)

            batch_keys  = []
            batch_texts = []
            batch_rows  = []

    # Flush remainder
    if batch_keys:
        _write_batch(batch_keys, batch_texts, batch_rows, write_mode)
        total_written += len(batch_keys)
        seen_keys.update(batch_keys)
        write_mode = "append"

    # Final checkpoint
    state["last_idx"]      = last_idx
    state["seen_keys"]     = seen_keys
    state["total_written"] = total_written
    state["saved_at"]      = time.time()
    save_checkpoint(state)

    elapsed = time.time() - start_time
    log.info(
        "=== Import Complete === total_written=%d last_idx=%d elapsed=%.0fs",
        total_written, last_idx, elapsed,
    )
    conn.close()


def _write_batch(keys, texts, rows, mode):
    """Embed and write a batch to LanceDB."""
    try:
        vectors = embed_texts(texts)
    except Exception as e:
        log.error("Embedding failed: %s", e)
        return  # skip batch, keys already added to seen_keys by caller

    n = len(keys)
    table = pa.table({
        "id":         pa.array(keys,                           pa.string()),
        "text":       pa.array(texts,                         pa.string()),
        "vector":     pa.array([list(v) for v in vectors],    pa.list_(pa.float32())),
        "category":   pa.array(["telegram"] * n,              pa.string()),
        "scope":      pa.array(["shared"]  * n,              pa.string()),
        "importance": pa.array([0.5]       * n,              pa.float64()),
        "timestamp":  pa.array([row_timestamp(r) for r in rows], pa.float64()),
        "metadata":   pa.array([row_metadata(r) for r in rows],  pa.string()),
    })

    lance.write_dataset(table, LANCE_PATH, mode=mode)


def _save_state(state, last_idx, seen_keys, total_written):
    state["last_idx"]      = last_idx
    state["seen_keys"]     = seen_keys
    state["total_written"] = total_written
    state["saved_at"]      = time.time()
    save_checkpoint(state)


def _log_progress(row_idx, total, written, start):
    elapsed = time.time() - start
    pct = (row_idx / total) * 100 if total > 0 else 0
    log.info(
        "Progress: row %d/%d (%.1f%%) | written: %d | elapsed: %.0fs",
        row_idx, total, pct, written, elapsed,
    )


if __name__ == "__main__":
    main()
