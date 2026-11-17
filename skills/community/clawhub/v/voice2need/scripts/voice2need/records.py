"""Portable records; raw observations and distinct people are not interchangeable."""
from __future__ import annotations

import json
import copy
from datetime import datetime, timezone
from typing import Any


def iso_time(value: Any) -> str | None:
    if value is None or value == "" or isinstance(value, bool):
        return None
    try:
        if isinstance(value, (int, float)):
            dt = datetime.fromtimestamp(value, timezone.utc)
        else:
            dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    except (ValueError, TypeError, OverflowError, OSError):
        return None


def in_window(value, start=None, end=None) -> bool:
    if not start and not end:
        return True
    for bound in (start, end):
        if bound and iso_time(bound) is None:
            raise ValueError("Invalid date boundary")
    parse = lambda x: datetime.fromisoformat(iso_time(x).replace("Z", "+00:00"))
    if start and end and parse(start) >= parse(end):
        raise ValueError("Window start must be before end")
    v = iso_time(value)
    if v is None:
        return False
    return (not start or parse(v) >= parse(start)) and (not end or parse(v) < parse(end))


def make_record(platform, native_id, kind, text, author_id, published_at, url,
                conversation_id, *, parent_id=None, title="", raw=None, metadata=None):
    if not platform or not native_id or not conversation_id:
        raise ValueError("Record requires platform, native_id and conversation_id")
    refs = raw if isinstance(raw, list) else ([raw] if raw else [])
    return {
        "evidence_id": f"{platform}:{native_id}", "platform": str(platform),
        "native_id": str(native_id), "kind": str(kind), "text": str(text or ""),
        "author_id": str(author_id) if author_id is not None else None,
        "published_at": iso_time(published_at), "url": str(url or ""),
        "conversation_id": str(conversation_id),
        "parent_id": str(parent_id) if parent_id else None, "title": str(title or ""),
        "raw": refs, "metadata": metadata or {},
        "content_status": "complete" if str(text or "").strip() else "empty",
        "review_status": "unreviewed",
    }


def deduplicate(records):
    """Latest content per native object, with every raw occurrence preserved."""
    unique = {}
    for record in records:
        key = record["evidence_id"]
        old = unique.get(key, {})
        refs = old.get("raw", []) + record.get("raw", [])
        seen = set()
        merged = []
        for ref in refs:
            signature = json.dumps(ref, sort_keys=True)
            if signature not in seen:
                seen.add(signature)
                merged.append(ref)
        metadata = copy.deepcopy(record.get("metadata", {}))
        before = old.get("metadata", {})
        if "context_only" in before or "context_only" in metadata:
            metadata["context_only"] = before.get("context_only", True) and metadata.get("context_only", True)
        if "in_window" in before or "in_window" in metadata:
            metadata["in_window"] = before.get("in_window", False) or metadata.get("in_window", False)
        scopes = copy.deepcopy(before.get("occurrence_scopes", []))
        for source in (before, record.get("metadata", {})):
            scope = {k: source[k] for k in ("job_id", "in_window", "context_only", "window") if k in source}
            if scope and scope not in scopes:
                scopes.append(scope)
        if scopes:
            metadata["occurrence_scopes"] = scopes
        unique[key] = {**record, "raw": merged, "metadata": metadata}
    return list(unique.values())
