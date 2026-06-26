from __future__ import annotations

from functools import lru_cache
import re
from typing import Any, Sequence

from rapidfuzz import fuzz

from sds_generator.config_loader import load_section_aliases
from sds_generator.constants import SECTION_TITLES
from sds_generator.models.source import SectionBlock
from sds_generator.parsing.layout_cleanup import normalize_text


_SECTION_PATTERNS = (
    re.compile(r"(?i)^section\s*(?P<number>1[0-6]|[1-9])\s*[:.-]\s*(?P<title>.+)$"),
    re.compile(r"(?i)^(?P<number>1[0-6]|[1-9])\.\s*(?P<title>.+)$"),
    re.compile(r"(?i)^(?P<number>1[0-6]|[1-9])\s+(?P<title>.+)$"),
)


def _normalize_alias(text: str) -> str:
    normalized = normalize_text(text).lower()
    normalized = normalized.replace("&", "and")
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _matches_alias(section_number: int, title: str) -> bool:
    aliases = load_section_aliases().get(section_number, [])
    normalized_title = _normalize_alias(title)
    normalized_aliases = [_normalize_alias(alias) for alias in aliases]
    if normalized_title in normalized_aliases:
        return True
    return any(fuzz.ratio(normalized_title, alias) >= 88 for alias in normalized_aliases)


def _alias_to_regex(alias: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9]+", alias)
    return r"\W+".join(re.escape(token) for token in tokens)


@lru_cache(maxsize=1)
def _embedded_heading_patterns() -> list[re.Pattern[str]]:
    patterns: list[re.Pattern[str]] = []
    for section_number, aliases in load_section_aliases().items():
        for alias in aliases:
            alias_pattern = _alias_to_regex(alias)
            patterns.extend(
                [
                    re.compile(fr"(?i)(?<![A-Za-z0-9])section\s*{section_number}\s*[:.-]\s*{alias_pattern}"),
                    re.compile(fr"(?i)(?<![A-Za-z0-9]){section_number}\.\s*{alias_pattern}"),
                    re.compile(fr"(?i)(?<![A-Za-z0-9.]){section_number}\s+{alias_pattern}"),
                ]
            )
    return patterns


def _find_embedded_heading_spans(text: str) -> list[tuple[int, int]]:
    matches: list[tuple[int, int]] = []
    for pattern in _embedded_heading_patterns():
        for match in pattern.finditer(text):
            matches.append((match.start(), match.end()))

    if not matches:
        return []

    matches.sort(key=lambda item: (item[0], -(item[1] - item[0])))
    collapsed: list[tuple[int, int]] = []
    for start, end in matches:
        if collapsed and start < collapsed[-1][1]:
            continue
        if collapsed and start == collapsed[-1][0]:
            continue
        collapsed.append((start, end))
    return collapsed


def _expand_lines(lines: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    expanded: list[dict[str, Any]] = []
    for line in lines:
        text = normalize_text(line["text"])
        spans = _find_embedded_heading_spans(text)
        if not spans:
            expanded.append({**line, "text": text})
            continue

        cursor = 0
        fragment_index = 0
        for start, end in spans:
            prefix = normalize_text(text[cursor:start])
            if prefix:
                expanded.append({**line, "text": prefix, "fragment_index": fragment_index})
                fragment_index += 1

            heading = normalize_text(text[start:end])
            if heading:
                expanded.append({**line, "text": heading, "fragment_index": fragment_index})
                fragment_index += 1
            cursor = end

        suffix = normalize_text(text[cursor:])
        if suffix:
            expanded.append({**line, "text": suffix, "fragment_index": fragment_index})
    return expanded


def parse_major_section_heading(text: str) -> tuple[int, str] | None:
    cleaned = normalize_text(text)
    if not cleaned or re.match(r"(?i)^(?:section\s*)?(?:1[0-6]|[1-9])\.\d", cleaned):
        return None

    for pattern in _SECTION_PATTERNS:
        match = pattern.match(cleaned)
        if not match:
            continue
        section_number = int(match.group("number"))
        title = normalize_text(match.group("title"))
        if title and _matches_alias(section_number, title):
            return section_number, title
    return None


def _consume_heading(lines: Sequence[dict[str, Any]], start_index: int) -> tuple[int, str, int] | None:
    for consumed in (1, 2):
        candidate = " ".join(
            normalize_text(lines[start_index + offset]["text"])
            for offset in range(consumed)
            if start_index + offset < len(lines)
        ).strip()
        parsed = parse_major_section_heading(candidate)
        if parsed:
            return parsed[0], parsed[1], consumed
    return None


def detect_sections(lines: Sequence[dict[str, Any]]) -> dict[int, SectionBlock]:
    expanded_lines = _expand_lines(lines)
    if not expanded_lines:
        return {}

    headings: list[tuple[int, int, str, int]] = []
    index = 0
    while index < len(expanded_lines):
        parsed = _consume_heading(expanded_lines, index)
        if parsed is None:
            index += 1
            continue
        section_number, title, consumed = parsed
        headings.append((index, section_number, title, consumed))
        index += consumed

    if not headings:
        return {}

    sections: dict[int, SectionBlock] = {}
    for heading_index, (start_index, section_number, title, consumed) in enumerate(headings):
        end_index = headings[heading_index + 1][0] if heading_index + 1 < len(headings) else len(expanded_lines)
        body_lines = expanded_lines[start_index + consumed : end_index]
        if not body_lines:
            continue
        page_numbers = list(dict.fromkeys(int(line["page_number"]) for line in body_lines))
        canonical_name = SECTION_TITLES.get(section_number, f"Section {section_number}: {title}")
        sections[section_number] = SectionBlock(
            section_number=section_number,
            canonical_name=canonical_name,
            heading_text=canonical_name,
            text="\n".join(line["text"] for line in body_lines).strip(),
            start_page=min(page_numbers),
            end_page=max(page_numbers),
            pages=page_numbers,
            block_ids=list(dict.fromkeys(str(line["block_id"]) for line in body_lines)),
            detection_pattern="section_heading_regex",
            detection_confidence=1.0,
        )

    return sections
