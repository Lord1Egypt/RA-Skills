#!/usr/bin/env python3
"""PDF text extraction with chapter slicing and page-limiting support."""

from __future__ import annotations

import io
import re
from typing import Any, Dict, List, Optional, Tuple

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None


# Standard A-share periodic-report chapter headings (证监会模板). Friendly
# aliases map a query to a chapter-title substring; anything not matching a
# chapter falls back to keyword-window extraction over the full text.
# Allow markdown decoration (#, *, spaces) before the heading, since pymupdf4llm
# renders chapter titles as Markdown headings.
PDF_CHAPTER_RE = re.compile(r"(?m)^\s*[#*\s]*第\s*[一二三四五六七八九十百]{1,3}\s*节\s*[*\s]*([^\n]{0,40})")
SECTION_ALIASES = {
    "mda": "管理层讨论与分析",
    "管理层讨论": "管理层讨论与分析",
    "经营": "管理层讨论与分析",
    "经营情况": "管理层讨论与分析",
    "财务报告": "财务报告",
    "附注": "财务报告",
    "notes": "财务报告",
    "治理": "公司治理",
    "公司治理": "公司治理",
    "重要事项": "重要事项",
    "募集": "重要事项",
    "股东": "股份变动及股东情况",
    "股份变动": "股份变动及股东情况",
}


def _read_pdf_pages(
    report_bytes: bytes,
    *,
    to_markdown: bool = False,
    max_pages: int = 0,
) -> Tuple[int, List[str], str]:
    """Return (total_pages, per_page_text, engine).

    Prefers pymupdf4llm (structure-preserving Markdown), then PyMuPDF (fitz),
    then PyPDF2 — so the richer engines are used when installed but the function
    still works on a bare PyPDF2 install.

    When ``max_pages`` > 0, only the first ``max_pages`` pages are extracted
    (saving memory on large PDFs).  A value <= 0 reads the whole document.
    """
    if to_markdown:
        try:
            import fitz  # type: ignore
            import pymupdf4llm  # type: ignore

            doc = fitz.open(stream=report_bytes, filetype="pdf")
            total = doc.page_count
            n = total if max_pages <= 0 else min(total, max_pages)
            chunks = pymupdf4llm.to_markdown(doc, pages=list(range(n)), page_chunks=True)
            pages = [str((c or {}).get("text", "")) for c in chunks]
            return total, pages, "pymupdf4llm"
        except Exception:
            pass
    try:
        import fitz  # type: ignore

        doc = fitz.open(stream=report_bytes, filetype="pdf")
        total = doc.page_count
        n = total if max_pages <= 0 else min(total, max_pages)
        pages = [doc[i].get_text("text") for i in range(n)]
        return total, pages, "pymupdf"
    except Exception:
        pass
    if PdfReader is None:
        raise RuntimeError("Missing dependency: install PyPDF2 (or PyMuPDF) before using PDF text extraction.")
    reader = PdfReader(io.BytesIO(report_bytes))
    total = len(reader.pages)
    n = total if max_pages <= 0 else min(total, max_pages)
    pages = [(reader.pages[i].extract_text() or "") for i in range(n)]
    return total, pages, "pypdf2"


def _locate_chapters(full_text: str) -> List[Dict[str, Any]]:
    """Index standard chapter headings, skipping table-of-contents entries.

    A chapter title appears twice: once in the TOC (with a dot leader + page
    number) and once as the real body heading. We drop the TOC occurrences and,
    when a title still repeats, keep the last (the body) occurrence.
    """
    found: List[Dict[str, Any]] = []
    for match in PDF_CHAPTER_RE.finditer(full_text):
        raw = match.group(1)
        # TOC lines carry dot leaders / trailing page numbers — strip & skip them.
        if re.search(r"\.{4,}|·{4,}|\…", raw):
            continue
        title = re.sub(r"[\s*#.·…]+$", "", raw).strip()
        if not title:
            continue
        found.append({"title": title, "char_start": match.start()})
    # Dedup by title, keeping the later (body) occurrence.
    by_title: Dict[str, Dict[str, Any]] = {}
    for ch in found:
        by_title[ch["title"]] = ch
    return sorted(by_title.values(), key=lambda c: c["char_start"])


def _slice_section(full_text: str, chapters: List[Dict[str, Any]], section: str, max_chars: int) -> Dict[str, Any]:
    """Resolve `section` to a chapter slice, or fall back to keyword windows."""
    target = SECTION_ALIASES.get(section.strip().lower(), section.strip())
    # 1) chapter match (by title substring)
    for idx, chap in enumerate(chapters):
        if target in chap["title"] or chap["title"] in target:
            start = chap["char_start"]
            end = chapters[idx + 1]["char_start"] if idx + 1 < len(chapters) else len(full_text)
            text = full_text[start:end].strip()
            truncated = len(text) > max_chars > 0
            return {
                "section_query": section,
                "section_mode": "chapter",
                "section_matched": chap["title"],
                "section_found": True,
                "text": text[:max_chars] if max_chars > 0 else text,
                "truncated": truncated,
            }
    # 2) keyword windows around each occurrence of the raw query
    windows: List[str] = []
    window = 1500
    used = 0
    low = full_text.lower()
    q = section.strip().lower()
    pos = 0
    while q and used < (max_chars or 10 ** 9):
        hit = low.find(q, pos)
        if hit < 0:
            break
        s = max(0, hit - window // 3)
        e = min(len(full_text), hit + window)
        snippet = full_text[s:e].strip()
        windows.append(snippet)
        used += len(snippet)
        pos = e
        if len(windows) >= 8:
            break
    joined = "\n\n…\n\n".join(windows)
    return {
        "section_query": section,
        "section_mode": "keyword_window",
        "section_matched": None,
        "section_found": bool(windows),
        "text": joined[:max_chars] if max_chars > 0 else joined,
        "truncated": len(joined) > max_chars > 0,
    }


def extract_pdf_text(
    report_bytes: bytes,
    *,
    max_pages: int = 120,
    max_chars: int = 60000,
    to_markdown: bool = False,
    section: Optional[str] = None,
) -> Dict[str, Any]:
    """Extract bounded text from PDF bytes.

    Engine preference: pymupdf4llm → PyMuPDF → PyPDF2. When ``section`` is given,
    the whole document is scanned so the requested chapter (e.g. 管理层讨论与分析,
    财务报告) can be located and returned instead of the blind first-N-pages slice;
    unknown sections fall back to keyword windows. ``to_markdown`` keeps Markdown
    structure when pymupdf4llm is available.
    """
    # When a section is requested we must scan the whole document for chapter
    # headings; otherwise limit the read to max_pages to avoid loading the full
    # PDF into memory.
    read_max = 0 if section else max_pages
    total_pages, page_texts, engine = _read_pdf_pages(
        report_bytes, to_markdown=to_markdown, max_pages=read_max
    )
    chapters_full = _locate_chapters("\n\n".join(p or "" for p in page_texts))

    result: Dict[str, Any] = {
        "page_count": total_pages,
        "engine": engine,
        "chapters": [c["title"] for c in chapters_full],
    }

    if section:
        full_text = "\n\n".join(p or "" for p in page_texts)
        sliced = _slice_section(full_text, chapters_full, section, max_chars)
        result.update(sliced)
        result["extracted_pages"] = total_pages
        result["text_length"] = len(result.get("text") or "")
        return result

    # Default: bounded first-N-pages slice (backward compatible).
    pages_to_read = total_pages if max_pages <= 0 else min(total_pages, max_pages)
    extracted_chunks: List[str] = []
    current_chars = 0
    for page_index in range(pages_to_read):
        page_text = (page_texts[page_index] or "").strip()
        if not page_text:
            continue
        remaining_chars = max_chars - current_chars
        if remaining_chars <= 0:
            break
        if len(page_text) > remaining_chars:
            extracted_chunks.append(page_text[:remaining_chars])
            current_chars += remaining_chars
            break
        extracted_chunks.append(page_text)
        current_chars += len(page_text)

    result["extracted_pages"] = pages_to_read
    result["text_length"] = sum(len(chunk) for chunk in extracted_chunks)
    result["text"] = "\n\n".join(extracted_chunks)
    return result
