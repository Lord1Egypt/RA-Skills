#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional


ROOT = Path(__file__).resolve().parents[1]
REGION_JSON = ROOT / "references" / "region-source.json"
LANGUAGE_JSON = ROOT / "references" / "language-source.json"


def _normalize_token(value: Any) -> str:
    text = str(value or "").strip().lower()
    return re.sub(r"[\s（）()\-_/]+", "", text)


def _load_alias_map(path: Path, code_keys: tuple[str, ...], alias_keys: tuple[str, ...]) -> dict[str, str]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    items = data if isinstance(data, list) else (data.get("items") if isinstance(data, dict) else [])
    alias_map: dict[str, str] = {}
    for item in items or []:
        if not isinstance(item, dict):
            continue
        code = ""
        for key in code_keys:
            value = str(item.get(key) or "").strip().lower()
            if value:
                code = value
                break
        if not code:
            continue
        for key in alias_keys:
            raw = item.get(key)
            values = raw if isinstance(raw, list) else [raw]
            for value in values:
                token = _normalize_token(value)
                if token:
                    alias_map[token] = code
        alias_map.setdefault(code, code)
    return alias_map


@lru_cache(maxsize=1)
def load_region_keywords() -> dict[str, str]:
    return _load_alias_map(
        REGION_JSON,
        code_keys=("code", "regionCode", "countryCode"),
        alias_keys=("aliases", "name", "country", "regionName"),
    )


@lru_cache(maxsize=1)
def load_lang_keywords() -> dict[str, str]:
    return _load_alias_map(
        LANGUAGE_JSON,
        code_keys=("code", "lang", "languageCode"),
        alias_keys=("aliases", "name", "language"),
    )


def _infer_codes(text: str, mapping: dict[str, str]) -> list[str]:
    lowered = str(text or "").lower()
    compact = _normalize_token(text)
    out: list[str] = []
    for alias, code in mapping.items():
        if not alias:
            continue
        if alias in compact or alias in lowered:
            if code not in out:
                out.append(code)
    return out


def infer_regions(text: str, mapping: Optional[dict[str, str]]= None) -> list[str]:
    mapping = mapping or load_region_keywords()
    regions = _infer_codes(text, mapping)
    return regions or ["us"]


def infer_languages(text: str, mapping: Optional[dict[str, str]]= None) -> list[str]:
    mapping = mapping or load_lang_keywords()
    languages = _infer_codes(text, mapping)
    return languages or []


def infer_values(text: str) -> dict[str, Any]:
    lowered = str(text or "").lower()
    min_fans = 10000 if any(x in lowered for x in ("1万", "10k", "10000")) else None
    max_fans = 500000 if any(x in lowered for x in ("50万", "500k", "500000")) else None
    return {"minFansNum": min_fans, "maxFansNum": max_fans}


def infer_sort(text: str) -> dict[str, Any]:
    lowered = str(text or "").lower()
    if any(x in lowered for x in ("互动", "engagement", "interactive")):
        return {"searchSort": "interactiveRateAvg", "sortOrder": "desc"}
    if any(x in lowered for x in ("销量", "gmv", "sales")):
        return {"searchSort": "gmv30d", "sortOrder": "desc"}
    return {}


def build_region_list(regions: Optional[list[str]]) -> list[dict[str, str]]:
    if not REGION_JSON.exists():
        return []

    data = json.loads(REGION_JSON.read_text())
    items = data if isinstance(data, list) else (data.get("items") if isinstance(data, dict) else [])

    requested = []
    seen_codes = set()
    for region in regions or []:
        code = str(region or "").strip().lower()
        if not code or code in seen_codes:
            continue
        seen_codes.add(code)
        requested.append(code)

    groups: dict[int, dict[str, Any]] = {}
    for item in items or []:
        if not isinstance(item, dict):
            continue
        code = str(item.get("dictCode") or "").strip().lower()
        if code not in requested:
            continue
        group_id = item.get("orderNum")
        if group_id is None:
            continue
        existing = groups.setdefault(int(group_id), {"id": item.get("id"), "country": []})
        existing["country"].append(code)

    ordered = []
    for group_id in sorted(groups.keys()):
        entry = groups[group_id]
        if entry.get("id") and entry.get("country"):
            ordered.append({"id": entry["id"], "country": entry["country"]})
    return ordered
