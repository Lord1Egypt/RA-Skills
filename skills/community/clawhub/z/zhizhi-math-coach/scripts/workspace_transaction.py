"""Recoverable local recording transactions (macOS/Linux)."""

from __future__ import annotations

import base64
import fcntl
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Callable


def inside(root: Path, relative: str | Path) -> Path:
    path = root / relative
    path.resolve().relative_to(root.resolve())
    if path.resolve() == root.resolve():
        raise ValueError("output path cannot be the workspace root")
    return path


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".record-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def record_once(workspace: Path, payload: dict, prepare: Callable) -> dict:
    """Prepare off-workspace, journal final bytes, then roll forward on retry.

    The lock serializes bundled recorders. External editors must not edit these
    files while a pending transaction is being recovered.
    """
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()
    fingerprint = hashlib.sha256(canonical).hexdigest()
    key = hashlib.sha256(str(payload.get("record_id") or fingerprint).encode()).hexdigest()
    receipt_rel = f"records/.receipts/{key}.json"
    state = inside(workspace, ".zhizhi-math-coach")
    state.mkdir(parents=True, exist_ok=True)
    journal_path = inside(workspace, ".zhizhi-math-coach/recording-pending.json")

    def apply(journal: dict) -> None:
        paths = {rel: inside(workspace, rel) for rel in journal["files"]}
        for rel, encoded in journal["files"].items():
            atomic_write(paths[rel], base64.b64decode(encoded))
        journal_path.unlink()

    with inside(workspace, ".zhizhi-math-coach/recording.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if journal_path.exists():
            apply(json.loads(journal_path.read_text(encoding="utf-8")))
        receipt_path = inside(workspace, receipt_rel)
        if receipt_path.exists():
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            if receipt["fingerprint"] != fingerprint:
                raise ValueError("record_id already exists with different content; use a new record_id for a correction")
            return {**receipt["result"], "duplicate": True}
        files, result = prepare()
        result = {**result, "duplicate": False}
        files[receipt_rel] = json.dumps({"fingerprint": fingerprint, "result": result}, ensure_ascii=False).encode()
        for rel in files:
            inside(workspace, rel)
        journal = {"files": {rel: base64.b64encode(data).decode() for rel, data in files.items()}}
        atomic_write(journal_path, json.dumps(journal).encode())
        apply(journal)
        return result
