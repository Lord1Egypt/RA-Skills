from __future__ import annotations

import math
import re
import unicodedata
from collections import defaultdict
from typing import Any, Iterable, Sequence


_WHITESPACE_RE = re.compile(r"\s+")
_HEADING_HINT_RE = re.compile(
    r"(?i)^(?:section\s*)?(?:1[0-6]|[1-9])(?:\s*[:.-]\s*|\s+).+$"
)


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text or "")
    normalized = normalized.replace("\u00a0", " ")
    normalized = normalized.replace("\u200b", "")
    return _WHITESPACE_RE.sub(" ", normalized).strip()


def normalize_for_repeat_detection(text: str) -> str:
    normalized = normalize_text(text).lower()
    normalized = re.sub(r"\bpage\s+\d+\s+(?:of|/)\s+\d+\b", "page # of #", normalized)
    normalized = re.sub(r"\b\d+\s+of\s+\d+\b", "# of #", normalized)
    normalized = re.sub(r"\bchemical book\s+\d+\b", "chemical book #", normalized)
    normalized = re.sub(r"\bsafety data sheet\s+\d+\s+of\s+\d+\b", "safety data sheet # of #", normalized)
    normalized = re.sub(r"\d{4}[/-]\d{2}[/-]\d{2}", "#date#", normalized)
    return normalized.strip(" :-|")


def split_block_lines(text: str) -> list[str]:
    lines = []
    for raw_line in (text or "").splitlines():
        cleaned = normalize_text(raw_line)
        if cleaned:
            lines.append(cleaned)
    return lines


def looks_like_major_section_heading(text: str) -> bool:
    cleaned = normalize_text(text)
    if not cleaned:
        return False
    if re.match(r"(?i)^(?:section\s*)?(?:1[0-6]|[1-9])\.\d", cleaned):
        return False
    return bool(_HEADING_HINT_RE.match(cleaned))


def _get_attr(item: Any, name: str, default: Any = None) -> Any:
    return getattr(item, name, default)


def _get_coord(item: Any, coord: str, default: float = 0.0) -> float:
    direct = getattr(item, coord, None)
    if direct is not None:
        return float(direct)
    bbox = getattr(item, "bbox", None)
    if bbox is not None and hasattr(bbox, coord):
        return float(getattr(bbox, coord))
    return float(default)


def _get_page_height(item: Any) -> float | None:
    metadata = getattr(item, "metadata", None)
    if isinstance(metadata, dict) and metadata.get("page_height"):
        return float(metadata["page_height"])
    return None


def _top_ratio(item: Any) -> float:
    direct = getattr(item, "top_ratio", None)
    if direct is not None:
        return float(direct)
    page_height = _get_page_height(item)
    if page_height:
        return _get_coord(item, "y0") / max(page_height, 1.0)
    return 0.0


def _bottom_ratio(item: Any) -> float:
    direct = getattr(item, "bottom_ratio", None)
    if direct is not None:
        return float(direct)
    page_height = _get_page_height(item)
    if page_height:
        return _get_coord(item, "y1") / max(page_height, 1.0)
    return 1.0


def detect_repeated_noise_lines(
    pages: Sequence[Sequence[Any]],
    *,
    min_page_ratio: float,
    header_region_ratio: float,
    footer_region_ratio: float,
) -> set[str]:
    if len(pages) < 2:
        return set()

    page_hits: dict[str, set[int]] = defaultdict(set)
    threshold = max(1, math.ceil(len(pages) * min_page_ratio))

    for page_index, blocks in enumerate(pages, start=1):
        seen_this_page: set[str] = set()
        for block in blocks:
            top_ratio = _top_ratio(block)
            bottom_ratio = _bottom_ratio(block)
            in_noise_band = top_ratio <= header_region_ratio or bottom_ratio >= (1.0 - footer_region_ratio)
            if not in_noise_band:
                continue

            for line in split_block_lines(_get_attr(block, "text", "") or ""):
                if looks_like_major_section_heading(line):
                    continue
                normalized = normalize_for_repeat_detection(line)
                if normalized:
                    seen_this_page.add(normalized)

        for line in seen_this_page:
            page_hits[line].add(page_index)

    return {line for line, hits in page_hits.items() if len(hits) >= threshold}


def strip_repeated_noise_lines(text: str, repeated_noise_lines: set[str]) -> str:
    if not repeated_noise_lines:
        return normalize_text(text)

    kept_lines = []
    for line in split_block_lines(text):
        if normalize_for_repeat_detection(line) not in repeated_noise_lines:
            kept_lines.append(line)
    return "\n".join(kept_lines)


def _cluster_x_positions(x_positions: Sequence[float], tolerance: float) -> list[float]:
    centers: list[float] = []
    for value in sorted(x_positions):
        if not centers or abs(value - centers[-1]) > tolerance:
            centers.append(value)
            continue
        centers[-1] = (centers[-1] + value) / 2
    return centers


def assign_column_indexes(blocks: Sequence[Any], page_width: float) -> dict[str, int]:
    if len(blocks) < 3:
        return {str(_get_attr(block, "block_id", index)): 0 for index, block in enumerate(blocks)}

    tolerance = max(40.0, page_width * 0.08)
    x_positions = [_get_coord(block, "x0", 0.0) for block in blocks]
    centers = _cluster_x_positions(x_positions, tolerance=tolerance)
    if len(centers) <= 1:
        return {str(_get_attr(block, "block_id", index)): 0 for index, block in enumerate(blocks)}

    def nearest_center_index(x0: float) -> int:
        return min(range(len(centers)), key=lambda idx: abs(x0 - centers[idx]))

    assignments = {}
    for index, block in enumerate(blocks):
        block_key = str(_get_attr(block, "block_id", index))
        assignments[block_key] = nearest_center_index(_get_coord(block, "x0", 0.0))
    return assignments


def order_blocks_for_reading(blocks: Sequence[Any], page_width: float) -> list[Any]:
    column_map = assign_column_indexes(blocks, page_width)
    return sorted(
        blocks,
        key=lambda block: (
            column_map.get(str(_get_attr(block, "block_id", "")), 0),
            _get_coord(block, "y0", 0.0),
            _get_coord(block, "x0", 0.0),
        ),
    )


def iter_clean_lines(blocks: Iterable[Any]) -> list[dict[str, Any]]:
    lines: list[dict[str, Any]] = []
    order_index = 0
    for block in blocks:
        for line_index, line_text in enumerate(split_block_lines(_get_attr(block, "text", "") or "")):
            lines.append(
                {
                    "text": line_text,
                    "page_number": int(_get_attr(block, "page_number", 1) or 1),
                    "block_id": str(_get_attr(block, "block_id", order_index)),
                    "line_index": line_index,
                    "order_index": order_index,
                }
            )
            order_index += 1
    return lines
