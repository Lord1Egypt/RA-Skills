"""Academic paper search — arXiv + SSRN + Google Scholar.

Provides a unified search interface for quantitative finance papers.
Results include title, authors, abstract, URL, and source.
"""

import logging
import os
import random
import re
import threading
import urllib.parse
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from typing import Optional
import time

from paper2spec.config import load_project_env

load_project_env()

logger = logging.getLogger(__name__)

ARXIV_API = "https://export.arxiv.org/api/query"
SSRN_SEARCH = "https://papers.ssrn.com/sol3/results.cfm"
ARXIV_MIN_INTERVAL = float(os.getenv("PAPER2SPEC_ARXIV_MIN_INTERVAL", "3.0"))
SEARCH_MAX_RETRIES = int(os.getenv("PAPER2SPEC_SEARCH_MAX_RETRIES", "3"))
SEARCH_TIMEOUT_SECONDS = int(os.getenv("PAPER2SPEC_SEARCH_TIMEOUT_SECONDS", "30"))

_arxiv_lock = threading.Lock()
_last_arxiv_request_ts = 0.0


@dataclass
class SearchResult:
    title: str = ""
    authors: list[str] = field(default_factory=list)
    abstract: str = ""
    url: str = ""
    source: str = ""  # arxiv | ssrn | scholar
    published: str = ""
    pdf_url: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def search(query: str, *, max_results: int = 10, sources: Optional[list[str]] = None) -> list[SearchResult]:
    """Search for papers across configured sources.

    Args:
        query: Search query string.
        max_results: Max results per source.
        sources: Which sources to query. Default: ["arxiv"].
                 Options: "arxiv", "ssrn" (scraping, best-effort).

    Returns:
        Combined list of SearchResult.
    """
    if sources is None:
        sources = ["arxiv"]

    results: list[SearchResult] = []
    for src in sources:
        if src == "arxiv":
            results.extend(_search_arxiv(query, max_results=max_results))
        elif src == "ssrn":
            logger.warning("SSRN search is best-effort (HTML scraping); may break.")
            results.extend(_search_ssrn(query, max_results=max_results))
        else:
            logger.warning("Unknown source: %s (skipped)", src)

    return results


def _polite_wait_for_arxiv() -> None:
    """Respect arXiv API usage guidance (~1 request per 3 seconds)."""
    global _last_arxiv_request_ts
    with _arxiv_lock:
        now = time.time()
        wait_seconds = ARXIV_MIN_INTERVAL - (now - _last_arxiv_request_ts)
        if wait_seconds > 0:
            logger.info("arXiv rate-limit wait: %.2fs", wait_seconds)
            time.sleep(wait_seconds)
        _last_arxiv_request_ts = time.time()


def _request_text_with_retry(
    url: str,
    *,
    headers: dict[str, str],
    source: str,
    timeout: int = SEARCH_TIMEOUT_SECONDS,
    max_retries: int = SEARCH_MAX_RETRIES,
    use_arxiv_pacing: bool = False,
) -> Optional[str]:
    """HTTP GET with 429/5xx retry, exponential backoff, and Retry-After support."""
    for attempt in range(max_retries):
        if use_arxiv_pacing:
            _polite_wait_for_arxiv()

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            is_retryable = e.code in {429, 500, 502, 503, 504}
            if not is_retryable or attempt == max_retries - 1:
                logger.error("%s request failed with HTTP %s: %s", source, e.code, e)
                return None

            retry_after_header = e.headers.get("Retry-After") if e.headers else None
            if retry_after_header and retry_after_header.isdigit():
                delay = float(retry_after_header)
            else:
                delay = min(20.0, (2 ** attempt) + random.uniform(0.2, 0.8))
            logger.warning(
                "%s HTTP %s (attempt %d/%d), retrying in %.1fs",
                source,
                e.code,
                attempt + 1,
                max_retries,
                delay,
            )
            time.sleep(delay)
        except Exception as e:
            logger.error("%s request failed: %s", source, e)
            return None

    return None


# ── arXiv ────────────────────────────────────────────────────


def _search_arxiv(query: str, *, max_results: int = 10) -> list[SearchResult]:
    """Search arXiv using their Atom API."""
    params = urllib.parse.urlencode({
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    })
    url = f"{ARXIV_API}?{params}"
    logger.info("arXiv query: %s", url)

    data = _request_text_with_retry(
        url,
        headers={
            "User-Agent": "paper2spec/0.3 (research tool; contact: support@alagent.ai)",
            "Accept": "application/atom+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        source="arXiv",
        use_arxiv_pacing=True,
    )
    if data is None:
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        logger.error("arXiv parse failed (non-XML response): %s", e)
        return []
    results = []
    for entry in root.findall("atom:entry", ns):
        title = (entry.findtext("atom:title", "", ns) or "").strip().replace("\n", " ")
        abstract = (entry.findtext("atom:summary", "", ns) or "").strip().replace("\n", " ")
        published = entry.findtext("atom:published", "", ns) or ""
        authors = [
            a.findtext("atom:name", "", ns)
            for a in entry.findall("atom:author", ns)
        ]

        # Links
        entry_url = ""
        pdf_url = ""
        for link in entry.findall("atom:link", ns):
            rel = link.get("rel", "")
            href = link.get("href", "")
            if rel == "alternate":
                entry_url = href
            elif link.get("title") == "pdf":
                pdf_url = href

        results.append(SearchResult(
            title=title,
            authors=authors,
            abstract=abstract[:500],
            url=entry_url,
            source="arxiv",
            published=published[:10],
            pdf_url=pdf_url,
        ))

    logger.info("arXiv returned %d results", len(results))
    return results


# ── SSRN (best-effort HTML scraping) ─────────────────────────


def _search_ssrn(query: str, *, max_results: int = 10) -> list[SearchResult]:
    """Best-effort search of SSRN via HTML scraping. May break if SSRN changes layout."""
    params = urllib.parse.urlencode({"txtKey_Words": query, "npage": 1})
    url = f"{SSRN_SEARCH}?{params}"
    logger.info("SSRN query: %s", url)

    html = _request_text_with_retry(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://papers.ssrn.com/",
            "Connection": "keep-alive",
        },
        source="SSRN",
    )
    if html is None:
        return []

    # Very basic extraction — SSRN HTML is complex, this is best-effort
    results = []
    # Look for title links: <a class="title" href="...">Title</a>
    for m in re.finditer(
        r'href="(https://papers\.ssrn\.com/sol3/papers\.cfm\?abstract_id=\d+)"[^>]*>\s*<[^>]*font[^>]*>([^<]+)',
        html,
    ):
        if len(results) >= max_results:
            break
        results.append(SearchResult(
            title=m.group(2).strip(),
            url=m.group(1),
            source="ssrn",
        ))

    logger.info("SSRN returned %d results", len(results))
    return results
