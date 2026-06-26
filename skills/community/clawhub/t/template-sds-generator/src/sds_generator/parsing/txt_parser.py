from __future__ import annotations

import re
from pathlib import Path

from sds_generator.config_loader import resolve_source_profile
from sds_generator.models.common import BoundingBox, FileType
from sds_generator.models.source import PageBlock, ParsedPage, ParsedSourceDocument
from sds_generator.parsing.layout_cleanup import iter_clean_lines, normalize_text
from sds_generator.parsing.section_detector import detect_sections


_REVISION_PATTERNS = (
    re.compile(r"(?i)\brevision date\s*[:#]?\s*(.+)$"),
    re.compile(r"(?i)\bdate of first issue\s*[:#]?\s*(.+)$"),
    re.compile(r"(?i)\bprint date\s*[:#]?\s*(.+)$"),
)


def _extract_revision_date(text: str) -> str | None:
    for line in text.splitlines():
        cleaned = normalize_text(line)
        for pattern in _REVISION_PATTERNS:
            match = pattern.search(cleaned)
            if match:
                return normalize_text(match.group(1))
    return None


def parse_txt(path: str | Path) -> ParsedSourceDocument:
    txt_path = Path(path)
    raw_text = txt_path.read_text(encoding="utf-8")
    blocks: list[PageBlock] = []
    for line_index, line in enumerate(raw_text.splitlines()):
        cleaned = normalize_text(line)
        if not cleaned:
            continue
        blocks.append(
            PageBlock(
                block_id=f"txt-line-{line_index}",
                page_number=1,
                text=cleaned,
                bbox=BoundingBox(x0=0.0, y0=float(line_index), x1=0.0, y1=float(line_index) + 1.0),
                order_index=line_index,
                metadata={"line_number": line_index + 1},
            )
        )

    joined_text = "\n".join(block.text for block in blocks)
    sections = detect_sections(iter_clean_lines(blocks))
    source_profile = resolve_source_profile(txt_path, hint_text=joined_text[:500])
    parsed_page = ParsedPage(page_number=1, width=0.0, height=0.0, raw_text=joined_text, normalized_text=joined_text, blocks=blocks)

    return ParsedSourceDocument(
        file_path=str(txt_path),
        file_name=txt_path.name,
        file_type=FileType.TXT,
        source_profile=source_profile.name,
        source_authority=source_profile.authority,
        parser_name="text",
        revision_date=_extract_revision_date(joined_text),
        pages=[parsed_page],
        blocks=blocks,
        sections=sections,
        raw_text=joined_text,
        normalized_text=joined_text,
    )
