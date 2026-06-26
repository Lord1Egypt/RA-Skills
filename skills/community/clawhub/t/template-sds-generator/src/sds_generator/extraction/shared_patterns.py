from __future__ import annotations

import re


CAS_RE = re.compile(r"\b\d{2,7}-\d{2}-\d\b")
EC_RE = re.compile(r"\b\d{3}-\d{3}-\d\b")
UN_RE = re.compile(r"\bUN\s*-?\s*(\d{4})\b", re.IGNORECASE)
H_CODE_RE = re.compile(r"\bH\d{3}\b")
P_CODE_RE = re.compile(r"\bP\d{3}\b")
PRODUCT_NUMBER_RE = re.compile(
    r"(?i)\b(product\s*(number|no\.?|code)|catalog(?:ue)?\s*no\.?|cbnumber)\s*[:#]?\s*([A-Za-z0-9-]+)"
)
FORMULA_RE = re.compile(r"\bC\d+H\d+[A-Za-z0-9]+\b")
MOLECULAR_WEIGHT_RE = re.compile(r"(?i)\b(?:molecular\s*weight|mw)\s*[:#]?\s*([0-9]+(?:\.[0-9]+)?\s*(?:g/mol|g/mole)?)")
TEMPERATURE_RE = re.compile(r"\b\d+\s*-\s*\d+\s*°?\s*C\b|\b\d+(?:\.\d+)?\s*°?\s*C\b", re.IGNORECASE)


def find_all(pattern: re.Pattern[str], text: str) -> list[str]:
    values: list[str] = []
    for match in pattern.finditer(text):
        value = match.group(1) if match.lastindex else match.group(0)
        values.append(value.strip())
    return values
