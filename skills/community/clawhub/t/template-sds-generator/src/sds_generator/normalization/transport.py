from __future__ import annotations

import re

from .text import normalize_text


def normalize_un_number(value: str | None) -> str | None:
    cleaned = normalize_text(value or "")
    if not cleaned or cleaned == "-":
        return None
    digits = re.search(r"(\d{4})", cleaned)
    return f"UN{digits.group(1)}" if digits else cleaned


def normalize_transport_class(value: str | None) -> str | None:
    cleaned = normalize_text(value or "")
    if not cleaned or cleaned == "-":
        return None
    match = re.search(r"(?i)(?:class\s*:?\s*)?([0-9A-Za-z.]+)$", cleaned)
    return match.group(1) if match else cleaned


def normalize_packing_group(value: str | None) -> str | None:
    cleaned = normalize_text(value or "")
    if not cleaned or cleaned == "-":
        return None
    match = re.search(r"\b(I|II|III|IV|V)\b", cleaned)
    return match.group(1) if match else cleaned


def normalize_transport_status(value: str | None) -> str | None:
    cleaned = normalize_text(value or "")
    if not cleaned:
        return None
    if cleaned.casefold() in {"not dangerous goods", "not classified as dangerous in the meaning of transport regulations."}:
        return "Not dangerous goods"
    return cleaned
