#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Tuple

DEFAULT_TTL_DAYS = 7
DEFAULT_MAX_ENTRIES = 500
DEFAULT_VERSION = 1


def now_ts() -> int:
    return int(time.time())


def stable_item_id(item: dict) -> str:
    for key in ("item_id", "id", "url"):
        value = item.get(key)
        if value:
            return str(value)
    raw = "|".join(
        str(item.get(k, ""))
        for k in ("circle_name", "author", "published_at", "title_or_hook", "title")
    )
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]
    return f"hash:{digest}"


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_items(path: Path) -> List[dict]:
    data = load_json(path, [])
    if isinstance(data, dict) and "items" in data:
        data = data["items"]
    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list or an object with an 'items' array")
    return data


def normalize_cursor(cursor: dict, ttl_days: int, max_entries: int) -> dict:
    seen = cursor.get("seen") if isinstance(cursor, dict) else {}
    if not isinstance(seen, dict):
        seen = {}
    normalized_seen = {}
    for key, value in seen.items():
        try:
            normalized_seen[str(key)] = int(value)
        except Exception:
            continue
    return {
        "version": int(cursor.get("version", DEFAULT_VERSION)) if isinstance(cursor, dict) else DEFAULT_VERSION,
        "updated_at": cursor.get("updated_at") if isinstance(cursor, dict) else None,
        "access_mode": cursor.get("access_mode") if isinstance(cursor, dict) else None,
        "ttl_days": int(cursor.get("ttl_days", ttl_days)) if isinstance(cursor, dict) else ttl_days,
        "max_entries": int(cursor.get("max_entries", max_entries)) if isinstance(cursor, dict) else max_entries,
        "seen": normalized_seen,
    }


def prune_seen(seen: Dict[str, int], ttl_days: int, max_entries: int, now: int) -> Dict[str, int]:
    min_ts = now - ttl_days * 86400
    kept = {k: v for k, v in seen.items() if v >= min_ts}
    if len(kept) <= max_entries:
        return kept
    ordered = sorted(kept.items(), key=lambda kv: kv[1], reverse=True)
    return dict(ordered[:max_entries])


def split_new_items(items: List[dict], cursor: dict, now: int) -> Tuple[List[dict], dict]:
    seen = dict(cursor["seen"])
    new_items = []
    for item in items:
        item_id = stable_item_id(item)
        if item_id not in seen:
            enriched = dict(item)
            enriched["item_id"] = item_id
            new_items.append(enriched)
        seen[item_id] = now
    next_seen = prune_seen(seen, cursor["ttl_days"], cursor["max_entries"], now)
    return new_items, next_seen


def atomic_write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def main():
    parser = argparse.ArgumentParser(description="Deduplicate ZSXQ items against a bounded cursor state")
    parser.add_argument("input", help="Path to JSON input")
    parser.add_argument("--cursor", required=True, help="Path to cursor.json")
    parser.add_argument("--ttl-days", type=int, default=DEFAULT_TTL_DAYS)
    parser.add_argument("--max-entries", type=int, default=DEFAULT_MAX_ENTRIES)
    parser.add_argument("--access-mode", default=None)
    parser.add_argument("--write-new-items", default=None, help="Optional output path for new items JSON")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input)
    cursor_path = Path(args.cursor)
    items = load_items(input_path)
    current = normalize_cursor(load_json(cursor_path, {}), args.ttl_days, args.max_entries)
    current["ttl_days"] = args.ttl_days
    current["max_entries"] = args.max_entries
    if args.access_mode:
        current["access_mode"] = args.access_mode

    ts = now_ts()
    new_items, next_seen = split_new_items(items, current, ts)
    next_cursor = {
        "version": DEFAULT_VERSION,
        "updated_at": ts,
        "access_mode": current.get("access_mode"),
        "ttl_days": current["ttl_days"],
        "max_entries": current["max_entries"],
        "seen": next_seen,
    }

    result = {
        "status": "ok",
        "input_count": len(items),
        "new_count": len(new_items),
        "seen_count": len(next_seen),
        "cursor": str(cursor_path),
    }

    if args.write_new_items:
        out_path = Path(args.write_new_items)
        if not args.dry_run:
            atomic_write_json(out_path, {"items": new_items})
        result["new_items_path"] = str(out_path)

    if not args.dry_run:
        atomic_write_json(cursor_path, next_cursor)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
