"""Markdown heading tree and stable source-position chunking."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

_HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", re.MULTILINE)


@dataclass(frozen=True)
class ParsedSection:
    key: str
    parent_key: str | None
    title: str
    slug: str
    path: str
    heading_path: tuple[str, ...]
    depth: int
    order_index: int
    start_line: int
    end_line: int
    char_start: int
    char_end: int
    body_start: int
    body_end: int


@dataclass(frozen=True)
class ParsedChunk:
    section_key: str
    heading: str
    heading_path: tuple[str, ...]
    chunk_index: int
    start_line: int
    end_line: int
    char_start: int
    char_end: int
    text: str


def slugify(value: str) -> str:
    normalized = re.sub(r"[^\w]+", "-", value.casefold(), flags=re.UNICODE).strip("-")
    return normalized[:80] or hashlib.sha1(value.encode("utf-8")).hexdigest()[:12]


def _line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def _trim_span(text: str, start: int, end: int) -> tuple[int, int]:
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return start, end


def _paragraph_spans(text: str, start: int, end: int) -> list[tuple[int, int]]:
    body = text[start:end]
    spans: list[tuple[int, int]] = []
    cursor = 0
    for separator in re.finditer(r"\n[ \t]*\n+", body):
        left, right = _trim_span(text, start + cursor, start + separator.start())
        if left < right:
            spans.append((left, right))
        cursor = separator.end()
    left, right = _trim_span(text, start + cursor, end)
    if left < right:
        spans.append((left, right))
    return spans


def _split_large_span(text: str, start: int, end: int, max_chars: int) -> list[tuple[int, int]]:
    if end - start <= max_chars:
        return [(start, end)]
    result: list[tuple[int, int]] = []
    cursor = start
    while cursor < end:
        target = min(cursor + max_chars, end)
        if target < end:
            newline = text.rfind("\n", cursor, target)
            sentence = max(text.rfind(". ", cursor, target), text.rfind("。", cursor, target))
            split_at = max(newline, sentence + 1)
            if split_at > cursor + max_chars // 2:
                target = split_at
        left, right = _trim_span(text, cursor, target)
        if left < right:
            result.append((left, right))
        cursor = max(target, cursor + 1)
    return result


def parse_markdown(text: str, *, max_chunk_chars: int = 2200) -> tuple[list[ParsedSection], list[ParsedChunk]]:
    matches = list(_HEADING_RE.finditer(text))
    sections: list[ParsedSection] = []
    chunks: list[ParsedChunk] = []
    stack: list[tuple[int, str, str, tuple[str, ...]]] = []
    path_counts: dict[str, int] = {}

    if not matches and text.strip():
        matches = []
        section = ParsedSection(
            key="document",
            parent_key=None,
            title="Document",
            slug="document",
            path="document",
            heading_path=("Document",),
            depth=1,
            order_index=0,
            start_line=1,
            end_line=_line_number(text, len(text)),
            char_start=0,
            char_end=len(text),
            body_start=0,
            body_end=len(text),
        )
        sections.append(section)
    else:
        for index, match in enumerate(matches):
            depth = len(match.group(1))
            title = match.group(2).strip()
            while stack and stack[-1][0] >= depth:
                stack.pop()
            parent_key = stack[-1][1] if stack else None
            parent_path = stack[-1][2] if stack else ""
            parent_headings = stack[-1][3] if stack else ()
            base_slug = slugify(title)
            candidate = f"{parent_path}/{base_slug}".strip("/")
            count = path_counts.get(candidate, 0) + 1
            path_counts[candidate] = count
            path = candidate if count == 1 else f"{candidate}-{count}"
            key = f"section-{index}"
            body_start = match.end()
            if body_start < len(text) and text[body_start] == "\n":
                body_start += 1
            body_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            section_end = len(text)
            for later in matches[index + 1 :]:
                if len(later.group(1)) <= depth:
                    section_end = later.start()
                    break
            heading_path = (*parent_headings, title)
            section = ParsedSection(
                key=key,
                parent_key=parent_key,
                title=title,
                slug=base_slug,
                path=path,
                heading_path=heading_path,
                depth=depth,
                order_index=index,
                start_line=_line_number(text, match.start()),
                end_line=_line_number(text, section_end),
                char_start=match.start(),
                char_end=section_end,
                body_start=body_start,
                body_end=body_end,
            )
            sections.append(section)
            stack.append((depth, key, path, heading_path))

    chunk_index = 0
    for section in sections:
        spans: list[tuple[int, int]] = []
        for start, end in _paragraph_spans(text, section.body_start, section.body_end):
            spans.extend(_split_large_span(text, start, end, max_chunk_chars))
        current: list[tuple[int, int]] = []
        current_size = 0
        grouped: list[tuple[int, int]] = []
        for span in spans:
            size = span[1] - span[0]
            if current and current_size + size + 2 > max_chunk_chars:
                grouped.append((current[0][0], current[-1][1]))
                current = []
                current_size = 0
            current.append(span)
            current_size += size + 2
        if current:
            grouped.append((current[0][0], current[-1][1]))
        for start, end in grouped:
            chunks.append(
                ParsedChunk(
                    section_key=section.key,
                    heading=section.title,
                    heading_path=section.heading_path,
                    chunk_index=chunk_index,
                    start_line=_line_number(text, start),
                    end_line=_line_number(text, end),
                    char_start=start,
                    char_end=end,
                    text=text[start:end].strip(),
                )
            )
            chunk_index += 1
    return sections, chunks
