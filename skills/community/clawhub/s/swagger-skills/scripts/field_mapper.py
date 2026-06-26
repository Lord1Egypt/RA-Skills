"""Transform HTTP JSON response keys using openapi_field_index.json descriptions."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from openapi_fields import (
    Entry,
    canonical_api_path,
    entries_matching_route,
    entry_from_dict,
    lookup_by_key,
)

_index_cache: list[Entry] | None = None
_route_bundle_cache: dict[tuple[str, str], tuple[dict[str, str], list[Entry]]] = {}
_index_warned = False


def _sanitize_desc(description: str) -> str:
    text = re.sub(r"\s+", " ", str(description or "")).strip()
    return text


def _load_entries(index_path: Path) -> list[Entry]:
    global _index_cache, _index_warned
    if _index_cache is not None:
        return _index_cache
    if not index_path.is_file():
        if not _index_warned:
            print(
                f"警告: 未找到字段索引 {index_path}；响应不做键替换。",
                file=sys.stderr,
            )
            _index_warned = True
        _index_cache = []
        return _index_cache
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        if not _index_warned:
            print(f"警告: 字段索引 JSON 无法解析：{exc}；响应不做键替换。", file=sys.stderr)
            _index_warned = True
        _index_cache = []
        return _index_cache
    raw = data.get("entries")
    if not isinstance(raw, list):
        if not _index_warned:
            print("警告: 字段索引缺少 entries；响应不做键替换。", file=sys.stderr)
            _index_warned = True
        _index_cache = []
        return _index_cache
    entries: list[Entry] = []
    for item in raw:
        if isinstance(item, dict):
            entry = entry_from_dict(item)
            if entry and entry.key and entry.description:
                entries.append(entry)
    _index_cache = entries
    return entries


def _build_key_to_description(route_entries: list[Entry]) -> dict[str, str]:
    best: dict[str, tuple[int, str]] = {}
    for entry in route_entries:
        key = (entry.key or "").strip()
        desc = _sanitize_desc(entry.description)
        if not key or not desc:
            continue
        line = entry.line if entry.line else 0
        if key not in best or line < best[key][0]:
            best[key] = (line, desc)
    return {key: value[1] for key, value in best.items()}


def _join_field_path(prefix: str, segment: str) -> str:
    if not prefix:
        return str(segment)
    return prefix + "." + str(segment)


def _describe_for_field(
    logical_path: str,
    leaf_key: str,
    key_to_desc: dict[str, str],
    route_entries: list[Entry],
) -> str | None:
    if logical_path in key_to_desc:
        return key_to_desc[logical_path]
    matches = lookup_by_key(route_entries, leaf_key)
    if not matches:
        return None
    for entry in matches:
        if entry.key == logical_path:
            return _sanitize_desc(entry.description)
    candidates = [
        entry
        for entry in matches
        if logical_path == entry.key or logical_path.endswith("." + entry.key)
    ]
    if not candidates:
        return None
    candidates.sort(key=lambda entry: (-len(entry.key or ""), entry.line))
    return _sanitize_desc(candidates[0].description)


def _transform_any(
    value: Any,
    prefix: str,
    key_to_desc: dict[str, str],
    route_entries: list[Entry],
) -> Any:
    if isinstance(value, dict):
        return _transform_dict(value, prefix, key_to_desc, route_entries)
    if isinstance(value, list):
        child_prefix = (prefix + "[]") if prefix else "[]"
        return [_transform_any(item, child_prefix, key_to_desc, route_entries) for item in value]
    return value


def _transform_dict(
    data: dict[str, Any],
    prefix: str,
    key_to_desc: dict[str, str],
    route_entries: list[Entry],
) -> dict[str, Any]:
    output: dict[str, Any] = {}
    used_out_keys: set[str] = set()
    for key, value in data.items():
        logical_path = _join_field_path(prefix, key) if prefix else key
        desc = _describe_for_field(logical_path, key, key_to_desc, route_entries)
        new_key = desc if desc else key
        if new_key in used_out_keys and new_key != key:
            base = desc if desc else key
            new_key = f"{base}（{key}）"
        elif new_key in used_out_keys:
            new_key = f"{key}（重复）"
        used_out_keys.add(new_key)
        output[new_key] = _transform_any(value, logical_path, key_to_desc, route_entries)
    return output


def transform_response(
    obj: Any,
    *,
    http_method: str,
    path: str,
    index_path: Path,
) -> Any:
    """Replace JSON object keys with OpenAPI field descriptions for one route."""

    if obj is None or not http_method or not str(path).strip():
        return obj
    entries = _load_entries(index_path)
    if not entries:
        return obj
    method = http_method.strip().upper()
    canon = canonical_api_path(path)
    cache_key = (method, canon)
    bundled = _route_bundle_cache.get(cache_key)
    if bundled is not None:
        key_to_desc, route_cached = bundled
        return _transform_any(obj, "", key_to_desc, route_cached)
    route = entries_matching_route(entries, http_method, path)
    if not route:
        return obj
    key_to_desc = _build_key_to_description(route)
    _route_bundle_cache[cache_key] = (key_to_desc, route)
    return _transform_any(obj, "", key_to_desc, route)
