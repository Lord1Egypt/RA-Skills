from __future__ import annotations

import re
from typing import Iterable

from sds_generator.parsing.layout_cleanup import normalize_text as _normalize_text


def normalize_text(value: str | None) -> str:
    return _normalize_text(value or "")


def normalize_blank_to_none(value: str | None) -> str | None:
    cleaned = normalize_text(value)
    return cleaned or None


def normalize_no_data(value: str | None) -> str | None:
    cleaned = normalize_blank_to_none(value)
    if cleaned is None:
        return None
    if cleaned.casefold() in {"no data available", "none", "no information available"}:
        return None
    return cleaned


def split_list_text(value: str | Iterable[str] | None, delimiters: str = r"[;\n,]") -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        items = re.split(delimiters, value)
    else:
        items = list(value)
    seen: set[str] = set()
    normalized: list[str] = []
    for item in items:
        cleaned = normalize_text(str(item))
        if not cleaned:
            continue
        key = cleaned.casefold()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(cleaned)
    return normalized
