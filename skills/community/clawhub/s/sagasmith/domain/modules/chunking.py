"""Structure-aware chunking for imported D&D module Markdown."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .pdf_parser import page_for_offset, strip_page_markers
from ..rules.parser import parse_markdown


@dataclass(frozen=True)
class ModuleParsedChunk:
    section_key: str
    heading: str
    heading_path: tuple[str, ...]
    chunk_index: int
    start_line: int
    end_line: int
    char_start: int
    char_end: int
    page_start: int | None
    page_end: int | None
    chunk_type: str
    overlap_chars: int
    text: str


_ROOM_RE = re.compile(r"^[A-Z]{1,3}\d+[A-Za-z]?\s*[.．]")
_TOC_HEADING_RE = re.compile(
    r"^(?:第[一二三四五六七八九十0-9]+章|附录\s*[A-ZＡ-Ｚ])"
)
_STAT_SIGNALS = (
    "护甲等级",
    "Armor Class",
    "生命值",
    "Hit Points",
    "速度：",
    "Speed:",
    "伤害免疫",
    "Damage Immunities",
    "状态免疫",
    "Condition Immunities",
    "动作 Actions",
)


def _chunk_type(heading: str, text: str) -> str:
    if _ROOM_RE.match(heading):
        return "room"
    if sum(signal.casefold() in text.casefold() for signal in _STAT_SIGNALS) >= 2:
        return "statblock"
    lines = [line for line in text.splitlines() if line.strip()]
    if lines and all(line.lstrip().startswith("|") for line in lines):
        return "table"
    if text.lstrip().startswith(">"):
        return "read_aloud"
    if lines and sum(line.lstrip().startswith(('-', '*')) for line in lines) >= len(lines) / 2:
        return "list"
    return "narrative"


def _tail(value: str, size: int) -> str:
    if len(value) <= size:
        return value
    candidate = value[-size:]
    boundary = max(candidate.find("。"), candidate.find("\n"))
    return candidate[boundary + 1 :] if 0 <= boundary < len(candidate) - 1 else candidate


def parse_module_markdown(
    content: str,
    *,
    max_chunk_chars: int = 1200,
    overlap_chars: int = 100,
) -> list[ModuleParsedChunk]:
    """Chunk within heading sections and retain source page provenance."""
    _, parsed = parse_markdown(content, max_chunk_chars=max_chunk_chars)
    result: list[ModuleParsedChunk] = []
    previous_by_section: dict[str, str] = {}
    for raw in parsed:
        clean = strip_page_markers(raw.text)
        if not clean:
            continue
        overlap = ""
        previous = previous_by_section.get(raw.section_key)
        if previous and overlap_chars:
            overlap = _tail(previous, overlap_chars)
        text = f"{overlap}\n\n{clean}" if overlap else clean
        kind = _chunk_type(raw.heading, clean)
        page_start = page_for_offset(content, raw.char_start)
        page_end = page_for_offset(content, raw.char_end)
        if page_start is not None and page_start <= 3 and _TOC_HEADING_RE.match(raw.heading):
            kind = "toc"
        result.append(
            ModuleParsedChunk(
                section_key=raw.section_key,
                heading=raw.heading,
                heading_path=raw.heading_path,
                chunk_index=len(result),
                start_line=raw.start_line,
                end_line=raw.end_line,
                char_start=raw.char_start,
                char_end=raw.char_end,
                page_start=page_start,
                page_end=page_end,
                chunk_type=kind,
                overlap_chars=len(overlap),
                text=text,
            )
        )
        previous_by_section[raw.section_key] = clean
    return result
