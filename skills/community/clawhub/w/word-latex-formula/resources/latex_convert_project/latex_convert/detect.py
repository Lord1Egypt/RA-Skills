from __future__ import annotations

import re


FORMULA_CHARS = (
    r"A-Za-z0-9_{}\^\\/\+\-\*=<>\(\)\[\],.;: "
    r"α-ωΑ-Ωϑϖ℘ℓ∑∏∞∂≤≥≈∈·×−±𝓡ℛḡ"
)

FORMULA_RE = re.compile(rf"[{FORMULA_CHARS}]+")

STRONG_MARKERS = set("_^\\=∑∏∞∂≤≥≈∈{}")
GREEK_RE = re.compile(r"[α-ωΑ-Ωϑϖ℘]")
MATH_LETTER_CHARS = r"A-Za-z0-9α-ωΑ-Ωϑϖ℘ℓ𝓡ℛḡ"
RELATION_RE = re.compile(rf"[{MATH_LETTER_CHARS}]\s*[<>=≤≥≈]\s*[{MATH_LETTER_CHARS}]")
SCRIPT_RE = re.compile(rf"[{MATH_LETTER_CHARS}]_\{{?[{MATH_LETTER_CHARS},]+\}}?")


def split_formula_segments(text: str) -> list[tuple[str, bool]]:
    return [(value, is_formula) for value, is_formula, _, _ in split_formula_spans(text)]


def split_formula_spans(text: str) -> list[tuple[str, bool, int, int]]:
    """Split a Word text node and keep offsets for likely formula substrings."""
    parts: list[tuple[str, bool, int, int]] = []
    pos = 0
    for match in FORMULA_RE.finditer(text):
        if match.start() > pos:
            parts.append((text[pos : match.start()], False, pos, match.start()))
        candidate = match.group(0)
        leading = candidate[: len(candidate) - len(candidate.lstrip())]
        trailing = candidate[len(candidate.rstrip()) :]
        core = candidate.strip()
        if leading:
            parts.append((leading, False, match.start(), match.start() + len(leading)))
        if core:
            start = match.start() + len(leading)
            parts.append((core, is_formula_like(core), start, start + len(core)))
        if trailing:
            start = match.end() - len(trailing)
            parts.append((trailing, False, start, match.end()))
        pos = match.end()
    if pos < len(text):
        parts.append((text[pos:], False, pos, len(text)))
    return _merge_adjacent(parts)


def is_formula_like(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 2:
        return False
    if stripped.startswith(("_", "^")):
        return False
    if not any(ch.isalpha() or ch.isdigit() or GREEK_RE.match(ch) for ch in stripped):
        return False
    if _looks_like_english_prose(stripped):
        return False
    if SCRIPT_RE.search(stripped):
        return True
    if any(marker in stripped for marker in STRONG_MARKERS):
        return True
    if GREEK_RE.search(stripped) and RELATION_RE.search(stripped):
        return True
    if re.search(r"\([^)]*[+*/=<>≤≥≈][^)]*\)", stripped):
        return True
    return False


def _looks_like_english_prose(text: str) -> bool:
    math_marks = len(re.findall(r"[_^=<>≤≥≈∑∏∂∞{}α-ωΑ-Ωϑϖ℘ℓ]", text))
    if math_marks >= 4 and re.search(r"[=<>≤≥≈∑∏∂∞]", text):
        return False
    words = re.findall(r"[A-Za-z]{2,}", text)
    if len(words) < 3:
        return False
    lower_words = [word for word in words if any(ch.islower() for ch in word)]
    if len(lower_words) < 2:
        return False
    mathish = re.search(r"[_^=<>≤≥≈∑∏∂∞α-ωΑ-Ωϑϖ℘ℓ]", text)
    if not mathish:
        return True
    if re.search(r"\b(with|without|after|before|include|includes|including|feature|features|metric|metrics|split|train|testing|validation|overlaps|dropped|where)\b", text, re.I):
        return True
    return False


def _merge_adjacent(
    parts: list[tuple[str, bool, int, int]]
) -> list[tuple[str, bool, int, int]]:
    merged: list[tuple[str, bool, int, int]] = []
    for text, is_formula, start, end in parts:
        if not text:
            continue
        if merged and merged[-1][1] == is_formula:
            prev_text, _, prev_start, _ = merged[-1]
            merged[-1] = (prev_text + text, is_formula, prev_start, end)
        else:
            merged.append((text, is_formula, start, end))
    return merged
