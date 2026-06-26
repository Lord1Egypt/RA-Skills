#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""OCR text recognition driver module.

Performs text recognition on window screenshots using WeChat OCR engine,
supporting both full-window OCR snapshots and text finding modes.
Depends on optional wx_ocr library and Pillow library.
"""

import logging
import os
import tempfile
import unicodedata

from PIL import Image

from constants import check_wx_ocr_available, wx_ocr
from models import Bounds, ElementFormatter, ElementInfo
from win32_utils import Win32API

_logger = logging.getLogger(__name__)


def _normalize_text(text: str) -> str:
    """Normalize text for comparison, handling encoding variations.

    Applies Unicode normalization (NFKC) and case folding to handle
    different Unicode representations of the same text.

    Args:
        text: Input text to normalize

    Returns:
        Normalized text suitable for comparison
    """
    return unicodedata.normalize("NFKC", text).casefold()


def _text_matches(query: str, candidate: str, exact: bool) -> bool:
    """Check if text matches with robust encoding handling.

    Tries multiple comparison strategies to handle potential encoding
    issues from OCR engines:
    1. Normalized Unicode comparison (handles different normal forms)
    2. Direct comparison (fallback for edge cases)

    Args:
        query: Text to search for
        candidate: OCR recognized text
        exact: Whether to require exact match

    Returns:
        True if match found, False otherwise
    """
    query_stripped = query.strip()
    candidate_stripped = candidate.strip()

    if not query_stripped or not candidate_stripped:
        return False

    query_normalized = _normalize_text(query_stripped)
    candidate_normalized = _normalize_text(candidate_stripped)

    if exact:
        return query_normalized == candidate_normalized
    return query_normalized in candidate_normalized


class OCRDriver:
    """Driver class for OCR text recognition operations."""

    @staticmethod
    def _capture_and_ocr(window_id: int) -> list[dict]:
        """Capture window screenshot and perform OCR recognition.

        Saves window screenshot to a temporary PNG file, calls wx_ocr for text recognition,
        and automatically deletes the temporary file after recognition.

        Note: OCR coordinates are already window-relative because we pass a cropped
        window image to wx_ocr, not a full screenshot.

        Args:
            window_id: Window handle

        Returns:
            OCR result list, each item contains "text" and "location" fields.
            Coordinates are relative to the window (not screen absolute).

        Raises:
            RuntimeError: OCR recognition failed or wx_ocr not installed
        """
        check_wx_ocr_available()

        _, _, width, height, data = Win32API.capture_window_bgra(window_id)
        image = Image.frombytes("RGBA", (width, height), bytes(data)).convert("RGB")
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp_path = tmp.name
            image.save(tmp_path)
            result = wx_ocr.ocr(tmp_path)
            return result if isinstance(result, list) else []
        except Exception as e:
            raise RuntimeError(f"WeChat OCR failed: {e}") from e
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    @staticmethod
    def snapshot_ocr(window_id: int) -> str:
        """Generate an OCR text snapshot for the window.

        Performs OCR recognition on the window screenshot, formatting each
        recognized text segment with its position and size information.

        Returns coordinates relative to the window (not screen absolute).
        """
        results = OCRDriver._capture_and_ocr(window_id)
        lines: list[str] = []
        for r in results:
            text = r.get("text", "")
            loc = r.get("location", {})
            left = int(loc.get("left") or 0)
            top = int(loc.get("top") or 0)
            right = int(loc.get("right") or 0)
            bottom = int(loc.get("bottom") or 0)
            lines.append(ElementFormatter.format_ocr(text, left, top, right - left, bottom - top))
        return "\n".join(lines)

    @staticmethod
    def find_ocr_text(
        window_id: int,
        text: str,
        exact: bool = False,
        confidence_threshold: float = 0.0,
    ) -> list[ElementInfo]:
        """Find specified text in the window via OCR.

        Args:
            window_id: Window handle
            text: Text to find
            exact: Whether to match exactly (default is fuzzy match)
            confidence_threshold: Minimum confidence threshold (0.0-1.0).
                Note: wx_ocr does not provide confidence scores, so this parameter
                is currently ignored. All matches are assigned a fixed confidence of 0.9.
                Included for API consistency with other find methods.

        Returns:
            List of matching ElementInfo with window-relative coordinates.
        """
        if confidence_threshold > 0.0:
            _logger.warning("confidence_threshold is not supported by wx_ocr; parameter ignored")
        results = OCRDriver._capture_and_ocr(window_id)
        matches: list[ElementInfo] = []
        for r in results:
            candidate = (r.get("text", "") or "").strip()
            if not candidate:
                continue
            if not _text_matches(text, candidate, exact):
                continue
            loc = r.get("location", {})
            left = int(loc.get("left") or 0)
            top = int(loc.get("top") or 0)
            right = int(loc.get("right") or 0)
            bottom = int(loc.get("bottom") or 0)
            matches.append(
                ElementInfo(
                    element_id=f"ocr-{left}-{top}",
                    window_id=str(window_id),
                    text=candidate,
                    bounds=Bounds.from_ltrb(left, top, right, bottom),
                    source="ocr",
                    confidence=0.9,
                )
            )
        return matches
