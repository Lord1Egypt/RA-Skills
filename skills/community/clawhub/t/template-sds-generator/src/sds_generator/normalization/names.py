from __future__ import annotations

import re

from .text import normalize_text, split_list_text


def normalize_name(value: str | None) -> str | None:
    cleaned = normalize_text(value or "")
    return cleaned or None


def normalize_synonyms(values: str | list[str] | None) -> list[str]:
    synonyms = split_list_text(values)
    synonyms.sort(key=lambda item: (-len(re.findall(r"[A-Za-z0-9]+", item)), item.casefold()))
    return synonyms
