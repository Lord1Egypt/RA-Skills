"""Layout-aware PDF to structured Markdown conversion for D&D modules."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from pypdf import PdfReader


@dataclass(frozen=True)
class PdfBookmark:
    title: str
    page: int
    depth: int


@dataclass(frozen=True)
class PdfMarkdownResult:
    content: str
    page_count: int
    bookmark_count: int
    matched_bookmarks: int
    heading_count: int
    room_heading_count: int
    warnings: tuple[str, ...]


_CHAPTER_RE = re.compile(
    r"^(?:第[一二三四五六七八九十0-9]+章(?:\s|：|:)|附录\s*[A-ZＡ-Ｚ](?:\s|：|:))"
)
_ROOM_RE = re.compile(r"^[A-Z]{1,3}\d+[A-Za-z]?\s*[.．]\s*\S+")
_LIST_RE = re.compile(r"^(?:[-*•●▪◼]|\d+[.)、]|[A-Za-z][.)])\s*")
_PAGE_NUMBER_RE = re.compile(r"^\d{1,3}$")
_TERMINAL_RE = re.compile(r"[。！？!?；;：:…][”’』」）》】]*$")
_PAGE_MARKER_RE = re.compile(r"^<!-- page: \d+ -->$")


def _normalize(value: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", value.casefold())


def _clean_line(value: str) -> str:
    value = value.replace("\uf06c", "•").replace("\uf0b7", "•")
    value = "".join(" " if 0xE000 <= ord(char) <= 0xF8FF else char for char in value)
    return re.sub(r"[ \t]+", " ", value).strip()


def _flatten_outline(reader: PdfReader) -> list[PdfBookmark]:
    bookmarks: list[PdfBookmark] = []

    def walk(items: list[Any], depth: int = 0) -> None:
        for item in items:
            if isinstance(item, list):
                walk(item, depth + 1)
                continue
            try:
                page = reader.get_destination_page_number(item) + 1
            except Exception:
                continue
            title = str(getattr(item, "title", item)).strip()
            if title:
                bookmarks.append(PdfBookmark(title=title, page=page, depth=depth))

    outline = reader.outline
    if isinstance(outline, list):
        walk(outline)
    return bookmarks


def _repeated_margin_lines(pages: list[list[str]]) -> set[str]:
    candidates: Counter[str] = Counter()
    for lines in pages:
        nonempty = [line for line in lines if line]
        for line in [*nonempty[:3], *nonempty[-3:]]:
            if _CHAPTER_RE.match(line) or re.match(
                r"^(?:Chapter|Appendix)\s+[0-9A-Z]", line, re.IGNORECASE
            ):
                continue
            normalized = _normalize(line)
            if normalized and not _PAGE_NUMBER_RE.fullmatch(line):
                candidates[normalized] += 1
    threshold = max(2, len(pages) // 8)
    return {line for line, count in candidates.items() if count >= threshold}


def _match_bookmarks(
    pages: list[list[str]], bookmarks: list[PdfBookmark]
) -> tuple[dict[tuple[int, int], int], int]:
    heading_levels: dict[tuple[int, int], int] = {}
    matched = 0
    for bookmark in bookmarks:
        if bookmark.page < 1 or bookmark.page > len(pages):
            continue
        target = _normalize(bookmark.title)
        if not target:
            continue
        best_index = -1
        best_score = 0.0
        for index, line in enumerate(pages[bookmark.page - 1]):
            candidate = _normalize(line)
            if not candidate:
                continue
            if target in candidate or candidate in target:
                score = min(len(target), len(candidate)) / max(len(target), len(candidate))
                score = max(score, 0.9)
            else:
                score = SequenceMatcher(None, target, candidate).ratio()
            if score > best_score:
                best_score = score
                best_index = index
        if best_index >= 0 and best_score >= 0.68:
            key = (bookmark.page, best_index)
            level = min(4, 2 + bookmark.depth)
            heading_levels[key] = min(level, heading_levels.get(key, level))
            matched += 1
    return heading_levels, matched


def _joiner(left: str, right: str) -> str:
    if not left or not right:
        return ""
    if left.endswith("-") and right[:1].isascii() and right[:1].isalpha():
        return ""
    if "\u4e00" <= left[-1] <= "\u9fff" and "\u4e00" <= right[0] <= "\u9fff":
        return ""
    return " "


def _split_inline_chapter_heading(line: str) -> tuple[str, str]:
    match = _CHAPTER_RE.match(line)
    if match is None:
        return line, ""
    ascii_seen = False
    for index in range(match.end(), len(line)):
        char = line[index]
        if char.isascii() and char.isalpha():
            ascii_seen = True
            continue
        if (
            ascii_seen
            and "\u4e00" <= char <= "\u9fff"
            and index > 0
            and line[index - 1].isspace()
        ):
            return line[:index].rstrip(), line[index:].lstrip()
    return line, ""


def _reflow_page(
    page_number: int,
    lines: list[str],
    heading_levels: dict[tuple[int, int], int],
    repeated_margins: set[str],
) -> tuple[list[str], int, int]:
    output = [f"<!-- page: {page_number} -->", ""]
    paragraph: list[str] = []
    heading_count = 0
    room_count = 0

    def flush() -> None:
        if not paragraph:
            return
        merged = paragraph[0]
        for line in paragraph[1:]:
            if merged.endswith("-") and line[:1].isascii() and line[:1].isalpha():
                merged = merged[:-1] + line
            else:
                merged += _joiner(merged, line) + line
        output.extend((merged, ""))
        paragraph.clear()

    nonempty_indexes = [index for index, line in enumerate(lines) if line]
    margin_indexes = set(nonempty_indexes[:3] + nonempty_indexes[-3:])
    for index, line in enumerate(lines):
        if not line:
            flush()
            continue
        if index in margin_indexes and _normalize(line) in repeated_margins:
            continue
        if index in margin_indexes and _PAGE_NUMBER_RE.fullmatch(line):
            continue

        level = heading_levels.get((page_number, index))
        next_nonempty = next((value for value in lines[index + 1 :] if value), "")
        chapter_confirmation = bool(
            re.match(r"^(?:Chapter|Appendix)\s+[0-9A-Z]", next_nonempty, re.IGNORECASE)
        )
        if _CHAPTER_RE.match(line) and (
            level is not None or chapter_confirmation or page_number > 3
        ):
            level = 1
        elif _ROOM_RE.match(line):
            level = level or 4
            room_count += 1
        if level is not None:
            flush()
            heading_line, remainder = (
                _split_inline_chapter_heading(line) if level == 1 else (line, "")
            )
            output.extend((f"{'#' * level} {heading_line}", ""))
            heading_count += 1
            if remainder:
                paragraph.append(remainder)
                if _TERMINAL_RE.search(remainder):
                    flush()
            continue
        if _LIST_RE.match(line):
            flush()
            normalized = re.sub(r"^[•●▪◼]\s*", "- ", line)
            output.append(normalized)
            continue

        paragraph.append(line)
        if _TERMINAL_RE.search(line):
            flush()
    flush()
    return output, heading_count, room_count


def build_structured_markdown(
    page_texts: list[str], bookmarks: list[PdfBookmark]
) -> PdfMarkdownResult:
    pages = [[_clean_line(line) for line in text.splitlines()] for text in page_texts]
    repeated_margins = _repeated_margin_lines(pages)
    heading_levels, matched = _match_bookmarks(pages, bookmarks)
    output: list[str] = []
    heading_count = room_count = 0
    for page_number, lines in enumerate(pages, start=1):
        rendered, page_headings, page_rooms = _reflow_page(
            page_number, lines, heading_levels, repeated_margins
        )
        output.extend(rendered)
        heading_count += page_headings
        room_count += page_rooms
    warnings: list[str] = []
    if bookmarks and matched / len(bookmarks) < 0.95:
        warnings.append(
            f"bookmark match rate is {matched}/{len(bookmarks)}; expected at least 95%"
        )
    if heading_count == 0:
        warnings.append("no structural headings were recovered")
    content = "\n".join(output).strip() + "\n"
    return PdfMarkdownResult(
        content=content,
        page_count=len(page_texts),
        bookmark_count=len(bookmarks),
        matched_bookmarks=matched,
        heading_count=heading_count,
        room_heading_count=room_count,
        warnings=tuple(warnings),
    )


def convert_pdf_to_markdown(path: str | Path) -> PdfMarkdownResult:
    source = Path(path).expanduser().resolve()
    reader = PdfReader(str(source))
    pages = [page.extract_text() or "" for page in reader.pages]
    bookmarks = _flatten_outline(reader)
    return build_structured_markdown(pages, bookmarks)


def page_for_offset(content: str, offset: int) -> int | None:
    current: int | None = None
    cursor = 0
    for line in content.splitlines(keepends=True):
        if cursor > offset:
            break
        marker = re.match(r"<!-- page: (\d+) -->", line.strip())
        if marker:
            current = int(marker.group(1))
        cursor += len(line)
    return current


def strip_page_markers(value: str) -> str:
    return "\n".join(
        line for line in value.splitlines() if not _PAGE_MARKER_RE.match(line.strip())
    ).strip()
