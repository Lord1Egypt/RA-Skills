from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from research_mode_task import ResearchTask
from research_mode_utils import atomic_json_write, read_json, utc_now


def _basic_entry(path: Path, task: ResearchTask) -> dict[str, Any]:
    rel = path.relative_to(task.task_dir)
    return {
        "id": f"corpus-{uuid.uuid4().hex[:10]}",
        "path": str(rel),
        "name": path.name,
        "size_bytes": path.stat().st_size,
        "attached_at": utc_now(),
        "source_path": None,
        "label": None,
        "note": None,
    }


def read_corpus_manifest(task: ResearchTask) -> list[dict[str, Any]]:
    if not task.corpus_manifest_path.exists():
        return []
    payload = read_json(task.corpus_manifest_path)
    if isinstance(payload, dict):
        entries = payload.get("entries") or []
    elif isinstance(payload, list):
        entries = payload
    else:
        entries = []
    result: list[dict[str, Any]] = []
    for item in entries:
        if not isinstance(item, dict):
            continue
        result.append(dict(item))
    return result


def write_corpus_manifest(task: ResearchTask, entries: list[dict[str, Any]]) -> None:
    atomic_json_write(
        task.corpus_manifest_path,
        {
            "task_id": task.task_dir.name,
            "entries": entries,
            "updated_at": utc_now(),
        },
    )


def list_corpus_entries(task: ResearchTask) -> list[dict[str, Any]]:
    manifest_entries = read_corpus_manifest(task)
    if manifest_entries:
        normalized: list[dict[str, Any]] = []
        changed = False
        for item in manifest_entries:
            rel_path = item.get("path")
            if not rel_path:
                continue
            abs_path = task.task_dir / str(rel_path)
            if not abs_path.exists() or not abs_path.is_file():
                continue
            entry = dict(item)
            size_bytes = abs_path.stat().st_size
            if entry.get("size_bytes") != size_bytes:
                entry["size_bytes"] = size_bytes
                changed = True
            entry.setdefault("id", f"corpus-{uuid.uuid4().hex[:10]}")
            entry.setdefault("name", abs_path.name)
            entry.setdefault("attached_at", utc_now())
            entry.setdefault("source_path", None)
            entry.setdefault("label", None)
            entry.setdefault("note", None)
            normalized.append(entry)
        if changed or len(normalized) != len(manifest_entries):
            write_corpus_manifest(task, normalized)
        return normalized

    if not task.corpus_dir.exists():
        return []
    entries: list[dict[str, Any]] = []
    for path in sorted(task.corpus_dir.rglob("*")):
        if not path.is_file():
            continue
        entries.append(_basic_entry(path, task))
    if entries:
        write_corpus_manifest(task, entries)
    return entries


def unique_copy_destination(dest_dir: Path, name: str) -> Path:
    candidate = dest_dir / Path(name).name
    if not candidate.exists():
        return candidate
    stem = candidate.stem
    suffix = candidate.suffix
    counter = 2
    while True:
        alt = dest_dir / f"{stem}-{counter}{suffix}"
        if not alt.exists():
            return alt
        counter += 1


def build_corpus_entry(
    task: ResearchTask,
    dest: Path,
    *,
    source_path: str | None,
    label: str | None,
    note: str | None,
) -> dict[str, Any]:
    rel = dest.relative_to(task.task_dir)
    entry = {
        "id": f"corpus-{uuid.uuid4().hex[:10]}",
        "path": str(rel),
        "name": dest.name,
        "size_bytes": dest.stat().st_size,
        "attached_at": utc_now(),
        "source_path": source_path,
        "label": label,
        "note": note,
    }
    if dest.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}:
        entry["content_hint"] = "image"
    return entry
