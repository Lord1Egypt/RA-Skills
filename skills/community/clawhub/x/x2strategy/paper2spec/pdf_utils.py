"""PDF text extraction with hybrid strategy.

Uses pymupdf4llm (Markdown output) for normal pages, falls back to
PyMuPDF plain-text for pages with excessive vector drawings.
"""

import logging
import os
import time

import fitz  # PyMuPDF
import pymupdf4llm

logger = logging.getLogger(__name__)

# Pages with more drawing commands than this use fitz plain-text fallback.
DRAWING_THRESHOLD = 10_000

# Engineering decision #9: truncate oversized PDFs (first N + last M pages).
MAX_FRONT_PAGES = 50
MAX_BACK_PAGES = 10


class PDFExtractor:
    """Extract text from PDF, handling heavy-drawing pages gracefully."""

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """Return full paper text from *pdf_path*."""
        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        return PDFExtractor._extract_hybrid(pdf_path)

    @staticmethod
    def _extract_hybrid(pdf_path: str) -> str:
        start = time.time()
        doc = fitz.open(pdf_path)
        total = len(doc)

        # Determine which pages to process (truncation for oversized PDFs)
        if total > MAX_FRONT_PAGES + MAX_BACK_PAGES:
            front = list(range(MAX_FRONT_PAGES))
            back = list(range(total - MAX_BACK_PAGES, total))
            pages_to_process = front + back
            logger.info(
                "Truncating %d-page PDF → first %d + last %d pages",
                total, MAX_FRONT_PAGES, MAX_BACK_PAGES,
            )
        else:
            pages_to_process = list(range(total))

        # Classify pages: heavy-drawing vs normal
        heavy_pages: list[int] = []
        normal_pages: list[int] = []
        for i in pages_to_process:
            drawings = doc[i].get_drawings()
            if len(drawings) > DRAWING_THRESHOLD:
                heavy_pages.append(i)
            else:
                normal_pages.append(i)
        doc.close()

        page_texts: dict[int, str] = {}

        # Heavy-drawing pages → fitz plain text
        if heavy_pages:
            logger.info("Heavy-drawing pages (%d): using fitz fallback", len(heavy_pages))
            doc = fitz.open(pdf_path)
            for i in heavy_pages:
                page_texts[i] = doc[i].get_text()
            doc.close()

        # Normal pages → pymupdf4llm markdown (batch)
        if normal_pages:
            md_pages = pymupdf4llm.to_markdown(pdf_path, pages=normal_pages, page_chunks=True)
            for chunk in md_pages:
                # pymupdf4llm uses 1-indexed page_number
                page_num = chunk["metadata"]["page_number"] - 1
                page_texts[page_num] = chunk["text"]

        # Combine in page order
        combined = "\n\n".join(page_texts[i] for i in sorted(page_texts))
        elapsed = time.time() - start
        logger.info("PDF extracted: %d pages, %d chars, %.1fs", len(page_texts), len(combined), elapsed)
        return combined
