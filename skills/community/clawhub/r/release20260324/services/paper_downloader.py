"""Download academic paper PDFs for reference extraction.

Download priority:
  1. arXiv PDF (free, stable, no auth needed)
  2. Unpaywall (free OA link discovery via DOI)
  3. Direct URL (if paper has a known PDF URL)

Caches downloaded PDFs to avoid redundant downloads.
"""
import os
import re
import sys
import hashlib
import logging
from typing import Optional

import httpx

from schemas import Paper

logger = logging.getLogger(__name__)

DEFAULT_CACHE_DIR = os.path.join(os.environ.get("TMPDIR", "/tmp"), "opg_pdf_cache")
UNPAYWALL_EMAIL = "openpapergraph@users.noreply.github.com"


def _ensure_cache_dir(cache_dir: str) -> str:
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def _cache_path(paper_id: str, cache_dir: str) -> str:
    """Generate a cache file path for a paper ID."""
    safe_id = hashlib.md5(paper_id.encode()).hexdigest()
    return os.path.join(cache_dir, f"{safe_id}.pdf")


def _extract_arxiv_id(paper: Paper) -> Optional[str]:
    """Extract arXiv ID from a Paper object."""
    # From paper.arxiv_id field
    if paper.arxiv_id:
        return paper.arxiv_id

    # From paper.id (ARXIV:xxxx format)
    if paper.id and paper.id.upper().startswith("ARXIV:"):
        return paper.id.split(":", 1)[1]

    # From paper.url (arxiv.org/abs/xxxx or arxiv.org/pdf/xxxx)
    if paper.url:
        match = re.search(r'arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5}(?:v\d+)?)', paper.url)
        if match:
            return match.group(1)

    return None


def _download_from_arxiv(arxiv_id: str, dest: str) -> bool:
    """Download PDF from arXiv. Returns True on success."""
    # Clean the ID (remove version suffix for consistency, but keep if present)
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    try:
        print(f"[download] arXiv PDF: {url}", file=sys.stderr)
        with httpx.Client(timeout=60, follow_redirects=True) as client:
            resp = client.get(url)
            if resp.status_code == 200 and len(resp.content) > 1000:
                # Verify it's actually a PDF
                if resp.content[:4] == b'%PDF':
                    with open(dest, "wb") as f:
                        f.write(resp.content)
                    print(f"[download] Saved: {dest} ({len(resp.content)} bytes)", file=sys.stderr)
                    return True
                else:
                    print(f"[download] arXiv response is not PDF", file=sys.stderr)
            else:
                print(f"[download] arXiv returned {resp.status_code}", file=sys.stderr)
    except Exception as e:
        print(f"[download] arXiv download failed: {e}", file=sys.stderr)
    return False


def _download_from_unpaywall(doi: str, dest: str) -> bool:
    """Try to find and download an open-access PDF via Unpaywall."""
    if not doi:
        return False

    url = f"https://api.unpaywall.org/v2/{doi}?email={UNPAYWALL_EMAIL}"
    try:
        print(f"[download] Checking Unpaywall for DOI:{doi}", file=sys.stderr)
        with httpx.Client(timeout=30, follow_redirects=True) as client:
            resp = client.get(url)
            if resp.status_code != 200:
                return False

            data = resp.json()
            # Find best OA location with a PDF URL
            pdf_url = None
            best_oa = data.get("best_oa_location") or {}
            pdf_url = best_oa.get("url_for_pdf")

            if not pdf_url:
                # Try other OA locations
                for loc in (data.get("oa_locations") or []):
                    if loc.get("url_for_pdf"):
                        pdf_url = loc["url_for_pdf"]
                        break

            if not pdf_url:
                print(f"[download] No OA PDF found for DOI:{doi}", file=sys.stderr)
                return False

            # Download the PDF
            print(f"[download] Unpaywall PDF: {pdf_url[:80]}...", file=sys.stderr)
            pdf_resp = client.get(pdf_url, timeout=60)
            if pdf_resp.status_code == 200 and len(pdf_resp.content) > 1000:
                if pdf_resp.content[:4] == b'%PDF':
                    with open(dest, "wb") as f:
                        f.write(pdf_resp.content)
                    print(f"[download] Saved: {dest} ({len(pdf_resp.content)} bytes)", file=sys.stderr)
                    return True

    except Exception as e:
        print(f"[download] Unpaywall failed: {e}", file=sys.stderr)
    return False


def _download_from_url(url: str, dest: str) -> bool:
    """Try to download PDF from a direct URL."""
    if not url:
        return False

    # Only try URLs that look like they could be PDFs
    if not any(hint in url.lower() for hint in ['.pdf', '/pdf/', 'pdf?', 'fulltext']):
        return False

    try:
        print(f"[download] Direct URL: {url[:80]}...", file=sys.stderr)
        with httpx.Client(timeout=60, follow_redirects=True) as client:
            resp = client.get(url)
            if resp.status_code == 200 and len(resp.content) > 1000:
                if resp.content[:4] == b'%PDF':
                    with open(dest, "wb") as f:
                        f.write(resp.content)
                    print(f"[download] Saved: {dest} ({len(resp.content)} bytes)", file=sys.stderr)
                    return True
    except Exception as e:
        logger.debug(f"Direct URL download failed: {e}")
    return False


def download_pdf(paper: Paper, cache_dir: str = DEFAULT_CACHE_DIR) -> Optional[str]:
    """Download a paper's PDF. Returns local file path or None.

    Priority:
      1. Check cache
      2. arXiv (if paper has arXiv ID)
      3. Unpaywall (if paper has DOI)
      4. Direct URL (if paper has a PDF-like URL)
    """
    _ensure_cache_dir(cache_dir)
    dest = _cache_path(paper.id, cache_dir)

    # Check cache
    if os.path.isfile(dest) and os.path.getsize(dest) > 1000:
        print(f"[download] Cache hit: {dest}", file=sys.stderr)
        return dest

    # 1. arXiv
    arxiv_id = _extract_arxiv_id(paper)
    if arxiv_id:
        if _download_from_arxiv(arxiv_id, dest):
            return dest

    # 2. Unpaywall (via DOI)
    if paper.doi:
        if _download_from_unpaywall(paper.doi, dest):
            return dest

    # 3. Direct URL
    if paper.url:
        if _download_from_url(paper.url, dest):
            return dest

    # Also try pdf_url if available
    pdf_url = getattr(paper, 'pdf_url', None)
    if pdf_url:
        if _download_from_url(pdf_url, dest):
            return dest

    print(f"[download] Could not download PDF for: {paper.title[:50]}", file=sys.stderr)
    return None
