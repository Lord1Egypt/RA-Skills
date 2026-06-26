from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import fitz

from sds_generator.config_loader import load_defaults, resolve_source_profile
from sds_generator.exceptions import MostlyScannedPdfError, ParsingError
from sds_generator.models.common import BoundingBox, FileType
from sds_generator.models.source import PageBlock, PageWord, ParsedPage, ParsedSourceDocument
from sds_generator.parsing.ocr_backends import OCRPageResult
from sds_generator.parsing.layout_cleanup import (
    assign_column_indexes,
    detect_repeated_noise_lines,
    iter_clean_lines,
    normalize_text,
    order_blocks_for_reading,
    strip_repeated_noise_lines,
)

from .ocr_fallback import run_ocr_for_pages
from .section_detector import detect_sections


_REVISION_PATTERNS = (
    re.compile(r"(?i)\brevision date\s*[:#]?\s*(.+)$"),
    re.compile(r"(?i)\bdate of first issue\s*[:#]?\s*(.+)$"),
    re.compile(r"(?i)\bprint date\s*[:#]?\s*(.+)$"),
    re.compile(r"(?i)\brevision\s*[:#]?\s*(.+)$"),
)


def _extract_revision_date(text: str) -> str | None:
    for line in text.splitlines():
        cleaned = normalize_text(line)
        for pattern in _REVISION_PATTERNS:
            match = pattern.search(cleaned)
            if match:
                return normalize_text(match.group(1))
    return None


def _image_area_ratio(page: fitz.Page) -> float:
    try:
        page_dict = page.get_text("dict")
    except Exception:
        return 0.0

    page_area = max(page.rect.width * page.rect.height, 1.0)
    image_area = 0.0
    for block in page_dict.get("blocks", []):
        if block.get("type") != 1:
            continue
        x0, y0, x1, y1 = block.get("bbox", [0.0, 0.0, 0.0, 0.0])
        image_area += max((x1 - x0) * (y1 - y0), 0.0)
    return min(image_area / page_area, 1.0)


def _build_block(page_number: int, page_width: float, page_height: float, index: int, raw_block: tuple[Any, ...]) -> PageBlock | None:
    x0, y0, x1, y1, text, *_rest = raw_block
    cleaned = normalize_text(text or "")
    if not cleaned:
        return None
    return PageBlock(
        block_id=f"page-{page_number}-block-{index}",
        page_number=page_number,
        text=cleaned,
        bbox=BoundingBox(x0=float(x0), y0=float(y0), x1=float(x1), y1=float(y1)),
        order_index=index,
        metadata={
            "raw_block_index": index,
            "page_width": page_width,
            "page_height": page_height,
            "top_ratio": float(y0) / max(page_height, 1.0),
            "bottom_ratio": float(y1) / max(page_height, 1.0),
        },
    )


def _build_words(page_number: int, raw_words: list[tuple[Any, ...]]) -> list[PageWord]:
    words: list[PageWord] = []
    for raw_word in raw_words:
        x0, y0, x1, y1, text, block_no, line_no, word_no = raw_word
        cleaned = normalize_text(str(text))
        if not cleaned:
            continue
        words.append(
            PageWord(
                text=cleaned,
                page_number=page_number,
                bbox=BoundingBox(x0=float(x0), y0=float(y0), x1=float(x1), y1=float(y1)),
                block_no=int(block_no),
                line_no=int(line_no),
                word_no=int(word_no),
            )
        )
    return words


def _build_ocr_blocks(page_number: int, page_width: float, page_height: float, result: OCRPageResult) -> list[PageBlock]:
    if result.lines and result.image_width and result.image_height:
        x_scale = page_width / max(result.image_width, 1)
        y_scale = page_height / max(result.image_height, 1)
        blocks: list[PageBlock] = []
        for index, line in enumerate(result.lines):
            cleaned = normalize_text(line.text or "")
            if not cleaned:
                continue
            x0 = float(line.left) * x_scale
            y0 = float(line.top) * y_scale
            width = float(line.width) * x_scale
            height = float(line.height) * y_scale
            x1 = min(page_width, x0 + max(width, 0.0))
            y1 = min(page_height, y0 + max(height, 0.0))
            blocks.append(
                PageBlock(
                    block_id=f"page-{page_number}-ocr-line-{index}",
                    page_number=page_number,
                    text=cleaned,
                    bbox=BoundingBox(x0=x0, y0=y0, x1=x1, y1=y1),
                    order_index=index,
                    metadata={
                        "ocr_generated": True,
                        "page_width": page_width,
                        "page_height": page_height,
                        "top_ratio": y0 / max(page_height, 1.0),
                        "bottom_ratio": y1 / max(page_height, 1.0),
                        "ocr_line_confidence": line.confidence,
                    },
                )
            )
        if blocks:
            return blocks

    cleaned = normalize_text(result.text or "")
    if not cleaned:
        return []
    return [
        PageBlock(
            block_id=f"page-{page_number}-ocr-block-0",
            page_number=page_number,
            text=cleaned,
            bbox=BoundingBox(x0=0.0, y0=0.0, x1=float(page_width), y1=float(page_height)),
            order_index=0,
            metadata={
                "ocr_generated": True,
                "page_width": page_width,
                "page_height": page_height,
            },
        )
    ]


def _clean_blocks(
    raw_pages: list[list[PageBlock]],
    page_widths: list[float],
    page_heights: list[float],
    page_words: list[list[PageWord]],
) -> tuple[list[ParsedPage], list[PageBlock]]:
    defaults = load_defaults()
    parsing_defaults = defaults.get("parsing", {})
    repeated_noise = detect_repeated_noise_lines(
        raw_pages,
        min_page_ratio=float(parsing_defaults.get("repeated_noise_min_page_ratio", 0.5)),
        header_region_ratio=float(parsing_defaults.get("header_region_ratio", 0.10)),
        footer_region_ratio=float(parsing_defaults.get("footer_region_ratio", 0.10)),
    )

    parsed_pages: list[ParsedPage] = []
    all_blocks: list[PageBlock] = []
    for page_index, blocks in enumerate(raw_pages, start=1):
        ordered = order_blocks_for_reading(blocks, page_width=page_widths[page_index - 1])
        column_map = assign_column_indexes(ordered, page_width=page_widths[page_index - 1])
        cleaned_blocks: list[PageBlock] = []
        removed_noise_block_ids: list[str] = []
        for block in ordered:
            cleaned_text = strip_repeated_noise_lines(block.text, repeated_noise)
            if not cleaned_text:
                removed_noise_block_ids.append(block.block_id)
                continue
            cleaned_blocks.append(
                PageBlock(
                    block_id=block.block_id,
                    page_number=block.page_number,
                    text=cleaned_text,
                    bbox=block.bbox,
                    order_index=block.order_index,
                    column_index=column_map.get(block.block_id, 0),
                    metadata=block.metadata,
                )
            )
        page_text = "\n".join(block.text for block in cleaned_blocks).strip()
        page_columns = {block.column_index for block in cleaned_blocks if block.column_index is not None} or {0}
        parsed_page = ParsedPage(
            page_number=page_index,
            width=page_widths[page_index - 1],
            height=page_heights[page_index - 1],
            raw_text=page_text,
            normalized_text=page_text,
            blocks=cleaned_blocks,
            words=page_words[page_index - 1],
            column_count=max(1, len(page_columns)),
            removed_noise_block_ids=removed_noise_block_ids,
        )
        parsed_pages.append(parsed_page)
        all_blocks.extend(cleaned_blocks)
    return parsed_pages, all_blocks


def parse_pdf(path: str | Path, *, enable_ocr: bool = False) -> ParsedSourceDocument:
    pdf_path = Path(path)
    try:
        with fitz.open(pdf_path) as document:
            defaults = load_defaults()
            parsing_defaults = defaults.get("parsing", {})
            page_payloads: list[dict[str, Any]] = []
            scanned_pages: list[int] = []
            first_page_text = ""
            revision_date: str | None = None

            for page_number, page in enumerate(document, start=1):
                page_width = float(page.rect.width)
                page_height = float(page.rect.height)
                text = page.get_text("text") or ""
                if page_number == 1:
                    first_page_text = text
                if revision_date is None:
                    revision_date = _extract_revision_date(text)
                raw_words = page.get_text("words") or []
                blocks: list[PageBlock] = []
                for index, raw_block in enumerate(page.get_text("blocks") or []):
                    built = _build_block(page_number, page_width, page_height, index, raw_block)
                    if built is not None:
                        blocks.append(built)
                image_area_ratio = _image_area_ratio(page)

                likely_scanned = (
                    len(normalize_text(text)) < int(parsing_defaults.get("scanned_text_min_length", 80))
                    or len(raw_words) < int(parsing_defaults.get("scanned_words_min_count", 15))
                    or (not blocks and image_area_ratio >= float(parsing_defaults.get("image_page_coverage_threshold", 0.7)))
                )
                if likely_scanned:
                    scanned_pages.append(page_number)
                page_payloads.append(
                    {
                        "page_number": page_number,
                        "page_width": page_width,
                        "page_height": page_height,
                        "text": text,
                        "raw_words": raw_words,
                        "blocks": blocks,
                        "likely_scanned": likely_scanned,
                        "image_area_ratio": image_area_ratio,
                    }
                )
    except Exception as exc:  # pragma: no cover - backend-specific failure
        raise ParsingError(f"Failed to parse PDF {pdf_path.name}: {exc}") from exc

    if scanned_pages and not enable_ocr:
        raise MostlyScannedPdfError(
            f"{pdf_path.name} appears to be mostly scanned on pages {scanned_pages}; OCR is disabled."
        )
    ocr_results = {}
    if scanned_pages and enable_ocr:
        ocr_results = run_ocr_for_pages(pdf_path, scanned_pages)
        if not normalize_text(first_page_text) and 1 in ocr_results:
            first_page_text = ocr_results[1].text
            if revision_date is None:
                revision_date = _extract_revision_date(first_page_text)

    raw_pages: list[list[PageBlock]] = []
    page_widths: list[float] = []
    page_heights: list[float] = []
    page_words: list[list[PageWord]] = []
    payload_by_page: dict[int, dict[str, Any]] = {}
    for payload in page_payloads:
        page_number = int(payload["page_number"])
        page_width = float(payload["page_width"])
        page_height = float(payload["page_height"])
        if page_number in ocr_results:
            result = ocr_results[page_number]
            payload["text"] = result.text
            payload["raw_words"] = []
            payload["blocks"] = _build_ocr_blocks(page_number, page_width, page_height, result)
        raw_pages.append(list(payload["blocks"]))
        page_widths.append(page_width)
        page_heights.append(page_height)
        page_words.append(_build_words(page_number, list(payload["raw_words"])))
        payload_by_page[page_number] = payload

    parsed_pages, all_blocks = _clean_blocks(raw_pages, page_widths, page_heights, page_words)
    low_confidence_threshold = float(parsing_defaults.get("ocr_low_confidence_threshold", 70.0))
    ocr_backend = next((result.backend_name for result in ocr_results.values()), None)
    ocr_cache_hits: list[int] = []
    ocr_low_confidence_pages: list[int] = []
    for parsed_page in parsed_pages:
        payload = payload_by_page.get(parsed_page.page_number, {})
        parsed_page.likely_scanned = bool(payload.get("likely_scanned", False))
        parsed_page.metadata["image_area_ratio"] = payload.get("image_area_ratio")
        result = ocr_results.get(parsed_page.page_number)
        if result is None:
            continue
        parsed_page.ocr_used = True
        parsed_page.ocr_backend = result.backend_name
        parsed_page.ocr_confidence = result.confidence
        parsed_page.ocr_cache_hit = result.cache_hit
        if result.cache_hit:
            ocr_cache_hits.append(parsed_page.page_number)
        if result.confidence is not None and result.confidence < low_confidence_threshold:
            ocr_low_confidence_pages.append(parsed_page.page_number)
        if result.engine_version:
            parsed_page.metadata["ocr_engine_version"] = result.engine_version
        parsed_page.metadata["ocr_text_length"] = len(result.text)

    sections = detect_sections(iter_clean_lines(all_blocks))
    source_profile = resolve_source_profile(pdf_path, hint_text=first_page_text)
    raw_text = "\n\n".join(page.raw_text for page in parsed_pages).strip()
    parser_warnings = [f"Likely scanned pages: {scanned_pages}"] if scanned_pages else []
    if ocr_results:
        parser_warnings.append(
            f"OCR used backend {ocr_backend} on pages {sorted(ocr_results)}; cache hits: {sorted(ocr_cache_hits)}"
        )
    if ocr_low_confidence_pages:
        parser_warnings.append(f"OCR low confidence pages: {sorted(set(ocr_low_confidence_pages))}")

    return ParsedSourceDocument(
        file_path=str(pdf_path),
        file_name=pdf_path.name,
        file_type=FileType.PDF,
        source_profile=source_profile.name,
        source_authority=source_profile.authority,
        parser_name="pymupdf",
        revision_date=revision_date,
        pages=parsed_pages,
        blocks=all_blocks,
        sections=sections,
        raw_text=raw_text,
        normalized_text=raw_text,
        source_metadata={
            "first_page_text": normalize_text(first_page_text),
            "ocr": {
                "backend": ocr_backend,
                "pages_requested": sorted(scanned_pages),
                "pages_used": sorted(ocr_results),
                "cache_hits": sorted(ocr_cache_hits),
            },
        },
        likely_scanned=bool(scanned_pages),
        ocr_backend=ocr_backend,
        ocr_pages_used=sorted(ocr_results),
        ocr_cache_hits=sorted(ocr_cache_hits),
        ocr_low_confidence_pages=sorted(set(ocr_low_confidence_pages)),
        parser_warnings=parser_warnings,
    )
