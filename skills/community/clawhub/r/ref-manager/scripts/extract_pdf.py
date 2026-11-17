"""Extract bibliographic metadata from a PDF file.

Strategy: extract text (front pages), look for a DOI. If a DOI is found it is
handed to Crossref later for authoritative metadata. Otherwise use light
heuristics on the first page.
"""
import os
import re

from pypdf import PdfReader

from common import clean_text, find_doi


def _first_pages_text(path, max_pages=3, max_chars=6000):
    reader = PdfReader(path)
    chunks = []
    total = 0
    for i, page in enumerate(reader.pages):
        if i >= max_pages or total >= max_chars:
            break
        try:
            t = page.extract_text() or ""
        except Exception:
            t = ""
        chunks.append(t)
        total += len(t)
    return "\n".join(chunks)


def extract_pdf_metadata(path):
    filename = os.path.basename(path)
    text = _first_pages_text(path)
    doi = find_doi(text)

    rec = {
        "source_type": "pdf",
        "original_url": None,
        "original_filename": filename,
        "original_apa": None,
        "title": "", "authors": [], "year": "", "month": "", "day": "",
        "journal": "", "publisher": "", "volume": "", "issue": "", "pages": "",
        "doi": doi, "url": None,
    }

    if doi:
        return rec, text

    # Heuristic: first non-empty line is often the title.
    lines = [clean_text(l) for l in text.splitlines() if clean_text(l)]
    if lines:
        rec["title"] = lines[0][:300]
    m = re.search(r'\b(19|20)\d{2}\b', text)
    if m:
        rec["year"] = m.group(0)
    return rec, text
