from __future__ import annotations

import re

from .text import normalize_no_data, normalize_text


TEMPERATURE_RANGE_RE = re.compile(r"(?i)(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*°?\s*C")
TEMPERATURE_SINGLE_RE = re.compile(r"(?i)(\d+(?:\.\d+)?)\s*°?\s*C")


def normalize_temperature(value: str | None) -> str | None:
    cleaned = normalize_text(value or "")
    if not cleaned:
        return None
    if normalize_no_data(cleaned) is None:
        return None
    range_match = TEMPERATURE_RANGE_RE.search(cleaned)
    if range_match:
        return f"{range_match.group(1)} - {range_match.group(2)} °C"
    single_match = TEMPERATURE_SINGLE_RE.search(cleaned)
    if single_match:
        return f"{single_match.group(1)} °C"
    return cleaned


def normalize_measurement(value: str | None) -> str | None:
    cleaned = normalize_text(value or "")
    if not cleaned:
        return None
    if normalize_no_data(cleaned) is None:
        return None
    cleaned = cleaned.replace("g/mole", "g/mol")
    cleaned = cleaned.replace("mmHg", "mmHg")
    return cleaned
