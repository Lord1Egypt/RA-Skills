from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator

from docx import Document
from docx.document import Document as DocumentObject
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

from sds_generator.config_loader import resolve_source_profile
from sds_generator.exceptions import ParsingError
from sds_generator.models.common import BoundingBox, FileType
from sds_generator.models.source import PageBlock, ParsedPage, ParsedSourceDocument
from sds_generator.parsing.layout_cleanup import iter_clean_lines, normalize_text
from sds_generator.parsing.section_detector import detect_sections


_REVISION_PATTERNS = (
    re.compile(r"(?i)\brevision date\s*[:#]?\s*(.+)$"),
    re.compile(r"(?i)\bdate of first issue\s*[:#]?\s*(.+)$"),
    re.compile(r"(?i)\bprint date\s*[:#]?\s*(.+)$"),
)


def _iter_block_items(document: DocumentObject) -> Iterator[Paragraph | Table]:
    for child in document.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, document)
        elif isinstance(child, CT_Tbl):
            yield Table(child, document)


def _extract_revision_date(text: str) -> str | None:
    for line in text.splitlines():
        cleaned = normalize_text(line)
        for pattern in _REVISION_PATTERNS:
            match = pattern.search(cleaned)
            if match:
                return normalize_text(match.group(1))
    return None


def parse_docx(path: str | Path) -> ParsedSourceDocument:
    docx_path = Path(path)
    try:
        document = Document(docx_path)
    except Exception as exc:  # pragma: no cover - backend-specific failure
        raise ParsingError(f"Failed to parse DOCX {docx_path.name}: {exc}") from exc

    blocks: list[PageBlock] = []
    block_index = 0
    full_text_parts: list[str] = []

    for item in _iter_block_items(document):
        if isinstance(item, Paragraph):
            text = normalize_text(item.text)
            metadata = {"paragraph_index": block_index}
        else:
            rows = []
            for row in item.rows:
                cells = [normalize_text(cell.text) for cell in row.cells if normalize_text(cell.text)]
                if cells:
                    rows.append(" | ".join(cells))
            text = "\n".join(rows)
            metadata = {"table_index": block_index}

        if not text:
            continue
        blocks.append(
            PageBlock(
                block_id=f"docx-block-{block_index}",
                page_number=1,
                text=text,
                bbox=BoundingBox(x0=0.0, y0=float(block_index), x1=0.0, y1=float(block_index) + 1.0),
                order_index=block_index,
                metadata=metadata,
            )
        )
        full_text_parts.append(text)
        block_index += 1

    joined_text = "\n".join(full_text_parts).strip()
    sections = detect_sections(iter_clean_lines(blocks))
    source_profile = resolve_source_profile(docx_path, hint_text=joined_text[:500])
    parsed_page = ParsedPage(page_number=1, width=0.0, height=0.0, raw_text=joined_text, normalized_text=joined_text, blocks=blocks)

    return ParsedSourceDocument(
        file_path=str(docx_path),
        file_name=docx_path.name,
        file_type=FileType.DOCX,
        source_profile=source_profile.name,
        source_authority=source_profile.authority,
        parser_name="python-docx",
        revision_date=_extract_revision_date(joined_text),
        pages=[parsed_page],
        blocks=blocks,
        sections=sections,
        raw_text=joined_text,
        normalized_text=joined_text,
    )
