#!/usr/bin/env python3
"""Collect public publication metadata and open PDFs for mentor distillation.

The collector is intentionally dependency-free. It combines an academic
homepage crawl with arXiv, OpenAlex, Semantic Scholar, and Crossref enrichment,
then writes a publication index plus an agent fallback queue for anything the
script could not retrieve reliably.
"""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import hashlib
import html
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable


DEFAULT_UA = (
    "Mozilla/5.0 (compatible; research-mentor-distiller/0.2; "
    "+https://github.com/openai/codex)"
)

SSL_CONTEXT: ssl.SSLContext | None = None


@dataclass
class FetchLog:
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    fetched_urls: list[str] = field(default_factory=list)
    homepage_pages: list[str] = field(default_factory=list)
    source_counts: Counter = field(default_factory=Counter)
    author_candidates: list[dict[str, Any]] = field(default_factory=list)
    pdf_attempts: list[dict[str, Any]] = field(default_factory=list)

    def warn(self, message: str) -> None:
        self.warnings.append(message)
        print(f"[warn] {message}", file=sys.stderr)

    def error(self, message: str) -> None:
        self.errors.append(message)
        print(f"[error] {message}", file=sys.stderr)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def strip_tags(value: str) -> str:
    value = re.sub(r"(?is)<script.*?</script>", " ", value)
    value = re.sub(r"(?is)<style.*?</style>", " ", value)
    value = re.sub(r"(?is)<[^>]+>", " ", value)
    return normalize_whitespace(html.unescape(value))


def normalize_title(value: str) -> str:
    value = html.unescape(value or "").lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return normalize_whitespace(value)


def normalize_name(value: str) -> str:
    value = html.unescape(value or "").lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return normalize_whitespace(value)


def title_similarity(a: str, b: str) -> float:
    na = normalize_title(a)
    nb = normalize_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    return SequenceMatcher(None, na, nb).ratio()


def slugify(value: str, max_len: int = 96) -> str:
    value = normalize_title(value)
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    if not value:
        value = "untitled"
    return value[:max_len].strip("-") or "untitled"


def stable_id(title: str) -> str:
    norm = normalize_title(title)
    digest = hashlib.sha1(norm.encode("utf-8")).hexdigest()[:12]
    return f"paper-{digest}"


def request_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
    retries: int = 3,
    log: FetchLog | None = None,
) -> dict[str, Any] | None:
    body = request_bytes(url, headers=headers, timeout=timeout, retries=retries, log=log)
    if not body:
        return None
    try:
        return json.loads(body.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        if log:
            log.warn(f"Could not parse JSON from {url}: {exc}")
        return None


def request_text(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
    retries: int = 3,
    log: FetchLog | None = None,
) -> str | None:
    body = request_bytes(url, headers=headers, timeout=timeout, retries=retries, log=log)
    if not body:
        return None
    # Academic pages are often utf-8 but sometimes omit headers.
    for encoding in ("utf-8", "latin-1"):
        try:
            return body.decode(encoding)
        except UnicodeDecodeError:
            continue
    return body.decode("utf-8", errors="replace")


def request_bytes(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
    retries: int = 3,
    log: FetchLog | None = None,
) -> bytes | None:
    request_headers = {"User-Agent": DEFAULT_UA}
    if headers:
        request_headers.update(headers)
    last_error = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=request_headers)
            with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as response:
                if log:
                    final_url = response.geturl()
                    if final_url not in log.fetched_urls:
                        log.fetched_urls.append(final_url)
                return response.read()
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                retry_after = exc.headers.get("Retry-After")
                delay = parse_retry_after(retry_after) or (2 ** attempt + 1)
                time.sleep(delay)
                continue
            break
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt < retries - 1:
                time.sleep(2 ** attempt + 1)
                continue
            break
    if log:
        log.warn(f"Fetch failed: {url} ({last_error})")
    return None


def parse_retry_after(value: str | None) -> float | None:
    if not value:
        return None
    value = value.strip()
    if value.isdigit():
        return float(value)
    try:
        parsed = email.utils.parsedate_to_datetime(value)
        return max(0.0, (parsed - dt.datetime.now(dt.timezone.utc)).total_seconds())
    except Exception:
        return None


def absolutize_url(base_url: str, href: str) -> str:
    href = html.unescape((href or "").strip())
    if not href or href.startswith(("mailto:", "javascript:", "#")):
        return ""
    return urllib.parse.urljoin(base_url, href)


def extract_links(html_text: str, base_url: str) -> list[dict[str, str]]:
    pattern = re.compile(
        r"(?is)<a\s+[^>]*href\s*=\s*(?:\"([^\"]+)\"|'([^']+)'|([^\s>]+))[^>]*>(.*?)</a>"
    )
    links: list[dict[str, str]] = []
    for match in pattern.finditer(html_text):
        href = match.group(1) or match.group(2) or match.group(3) or ""
        text = strip_tags(match.group(4))
        url = absolutize_url(base_url, href)
        if url:
            links.append({"url": url, "text": text})
    return links


def same_site(url_a: str, url_b: str) -> bool:
    a = urllib.parse.urlparse(url_a)
    b = urllib.parse.urlparse(url_b)
    return a.netloc.lower() == b.netloc.lower()


def discover_homepage_pages(homepage: str, html_text: str, max_pages: int) -> list[str]:
    pages = [homepage]
    for link in extract_links(html_text, homepage):
        url = link["url"]
        text = link["text"].lower()
        path = urllib.parse.urlparse(url).path.lower()
        if not same_site(homepage, url):
            continue
        if any(key in f"{text} {path}" for key in ("research", "publication", "paper", "project", "about")):
            if re.search(r"\.(pdf|jpg|jpeg|png|gif|zip|bib)$", path):
                continue
            if url not in pages:
                pages.append(url)
        if len(pages) >= max_pages:
            break
    return pages[:max_pages]


def heading_context(html_text: str, position: int) -> dict[str, str]:
    before = html_text[:position]
    h2s = list(re.finditer(r"(?is)<h2[^>]*>(.*?)</h2>", before))
    h3s = list(re.finditer(r"(?is)<h3[^>]*>(.*?)</h3>", before))
    year_group = strip_tags(h2s[-1].group(1)) if h2s else ""
    direction = strip_tags(h3s[-1].group(1)) if h3s else ""
    return {"year_group": year_group, "direction": direction}


def extract_block(html_text: str, pos: int) -> str:
    start_candidates = [
        html_text.rfind("<li", 0, pos),
        html_text.rfind("<tr", 0, pos),
        html_text.rfind("<p", 0, pos),
    ]
    start = max(start_candidates)
    if start < 0:
        start = max(0, pos - 1500)
    end_candidates = []
    for marker in ("</li>", "</tr>", "</p>"):
        end = html_text.find(marker, pos)
        if end >= 0:
            end_candidates.append(end + len(marker))
    end = min(end_candidates) if end_candidates else min(len(html_text), pos + 2500)
    return html_text[start:end]


def infer_year(text: str, year_group: str = "") -> int | None:
    candidates = re.findall(r"\b(19[8-9]\d|20[0-5]\d)\b", f"{year_group} {text}")
    if not candidates:
        return None
    years = [int(x) for x in candidates]
    # Prefer explicit group year from publication pages.
    if re.fullmatch(r"(19[8-9]\d|20[0-5]\d)", year_group.strip()):
        return int(year_group.strip())
    return max(years)


def infer_venue(text: str) -> str:
    patterns = [
        r"\bIn:\s*(.*?)(?:\s*,?\s*(?:19[8-9]\d|20[0-5]\d)\b|$)",
        r"\bTo appear at\s*(.*?)(?:\s*,?\s*(?:19[8-9]\d|20[0-5]\d)\b|$)",
        r"\bUnder Review\b",
        r"\bUnder Revision\b",
        r"\bIn submission\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        if match.groups():
            venue = normalize_whitespace(match.group(1))
            venue = re.sub(r"\s*\(.*?(Impact Factor|IF).*?\)", "", venue, flags=re.IGNORECASE)
            return venue.strip(" .,:;")
        return match.group(0)
    return ""


def classify_link(url: str, text: str = "") -> str:
    lower = f"{url} {text}".lower()
    if "arxiv.org/abs/" in lower or "arxiv.org/pdf/" in lower:
        return "arxiv"
    if ".pdf" in urllib.parse.urlparse(url).path.lower() or "pdf" == text.strip().lower():
        return "pdf"
    if "github.com" in lower or "gitlab" in lower or "code" in text.lower():
        return "code"
    if "project" in text.lower() or "demo" in text.lower() or "web app" in text.lower():
        return "project"
    if "doi.org" in lower:
        return "doi"
    return "landing"


def extract_homepage_publications(
    page_url: str,
    html_text: str,
    scholar_name: str | None,
    log: FetchLog,
) -> list[dict[str, Any]]:
    pubs: list[dict[str, Any]] = []
    seen_positions: set[int] = set()
    title_pattern = re.compile(r"(?is)<papertitle[^>]*>(.*?)</papertitle>")
    for match in title_pattern.finditer(html_text):
        seen_positions.add(match.start())
        title = strip_tags(match.group(1)).rstrip(".")
        if len(normalize_title(title)) < 8:
            continue
        block = extract_block(html_text, match.start())
        context = heading_context(html_text, match.start())
        pubs.append(publication_from_homepage_block(title, block, page_url, context))

    # Generic fallback for pages without <papertitle>.
    if not pubs:
        for match in re.finditer(r"(?is)<li[^>]*>(.*?)</li>", html_text):
            block = match.group(0)
            text = strip_tags(block)
            if scholar_name and normalize_name(scholar_name) not in normalize_name(text):
                continue
            if not re.search(r"\b(19[8-9]\d|20[0-5]\d)\b", text):
                continue
            links = extract_links(block, page_url)
            title = ""
            for link in links:
                candidate = link["text"].rstrip(".")
                if len(normalize_title(candidate)) >= 8 and classify_link(link["url"], link["text"]) != "code":
                    title = candidate
                    break
            if title:
                context = heading_context(html_text, match.start())
                pubs.append(publication_from_homepage_block(title, block, page_url, context))

    log.source_counts["homepage"] += len(pubs)
    return pubs


def publication_from_homepage_block(
    title: str,
    block: str,
    page_url: str,
    context: dict[str, str],
) -> dict[str, Any]:
    links = extract_links(block, page_url)
    text = strip_tags(block)
    source_urls = []
    pdf_url = ""
    project_url = ""
    code_url = ""
    doi = ""
    url = ""
    arxiv_id = ""
    for link in links:
        link_url = link["url"]
        kind = classify_link(link_url, link["text"])
        source_urls.append(link_url)
        if not url and kind not in ("code",):
            url = link_url
        if kind == "pdf" and not pdf_url:
            pdf_url = link_url
        elif kind == "arxiv":
            arxiv_id = extract_arxiv_id(link_url) or arxiv_id
            if not pdf_url:
                pdf_url = arxiv_pdf_url(link_url)
            if not url:
                url = arxiv_abs_url(link_url)
        elif kind == "project" and not project_url:
            project_url = link_url
        elif kind == "code" and not code_url:
            code_url = link_url
        elif kind == "doi" and not doi:
            doi = link_url.rstrip("/").split("/")[-1]

    return {
        "id": stable_id(title),
        "title": title,
        "year": infer_year(text, context.get("year_group", "")),
        "year_group": context.get("year_group", ""),
        "direction": context.get("direction", ""),
        "venue": infer_venue(text),
        "authors": infer_authors_from_homepage_text(text, title),
        "abstract": "",
        "doi": doi,
        "url": url,
        "pdf_url": pdf_url,
        "project_url": project_url,
        "code_url": code_url,
        "arxiv_id": arxiv_id,
        "citation_count": None,
        "source_urls": dedupe(source_urls),
        "sources": ["homepage"],
        "collection_notes": [],
    }


def infer_authors_from_homepage_text(text: str, title: str) -> list[str]:
    text = text.replace(title, "")
    text = re.split(r"\b(In:|To appear at|Under Review|Under Revision|In submission)\b", text, maxsplit=1)[0]
    text = re.sub(r"\b(Arxiv|Paper|PDF|Project Page|Code|Bibtex|Web App)\b.*", "", text, flags=re.IGNORECASE)
    text = normalize_whitespace(text)
    if not text or len(text) > 600:
        return []
    raw = [x.strip(" .;*^\u2020") for x in re.split(r",|\band\b", text) if x.strip()]
    authors = []
    for item in raw:
        item = normalize_whitespace(item)
        if not item:
            continue
        if re.search(r"\d{4}|conference|journal|under review|impact factor", item, re.IGNORECASE):
            continue
        authors.append(item)
    return authors[:30]


def dedupe(values: Iterable[str]) -> list[str]:
    seen = set()
    out = []
    for value in values:
        if not value:
            continue
        key = value.strip()
        if key and key not in seen:
            seen.add(key)
            out.append(key)
    return out


def extract_arxiv_id(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    match = re.search(r"/(?:abs|pdf)/([^/?#]+)", path)
    if not match:
        return ""
    arxiv_id = match.group(1)
    arxiv_id = re.sub(r"\.pdf$", "", arxiv_id)
    return arxiv_id


def arxiv_pdf_url(url_or_id: str) -> str:
    arxiv_id = extract_arxiv_id(url_or_id) or url_or_id
    return f"https://arxiv.org/pdf/{arxiv_id}.pdf"


def arxiv_abs_url(url_or_id: str) -> str:
    arxiv_id = extract_arxiv_id(url_or_id) or url_or_id
    return f"https://arxiv.org/abs/{arxiv_id}"


def collect_from_homepage(args: argparse.Namespace, log: FetchLog) -> list[dict[str, Any]]:
    if not args.homepage:
        return []
    homepage = args.homepage
    first_html = request_text(homepage, timeout=args.timeout, log=log)
    if not first_html:
        return []
    pages = discover_homepage_pages(homepage, first_html, args.max_homepage_pages)
    page_html = {homepage: first_html}
    pubs: list[dict[str, Any]] = []
    for page in pages:
        html_text = page_html.get(page)
        if html_text is None:
            html_text = request_text(page, timeout=args.timeout, log=log)
        if not html_text:
            continue
        log.homepage_pages.append(page)
        pubs.extend(extract_homepage_publications(page, html_text, args.scholar_name, log))
    return pubs


def collect_from_arxiv(args: argparse.Namespace, log: FetchLog) -> list[dict[str, Any]]:
    if args.skip_arxiv or not args.scholar_name:
        return []
    query = f'au:"{args.scholar_name}"'
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "start": 0,
            "max_results": args.max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    url = f"https://export.arxiv.org/api/query?{params}"
    text = request_text(url, timeout=args.timeout, retries=3, log=log)
    if not text:
        return []
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        log.warn(f"Could not parse arXiv Atom feed: {exc}")
        return []
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    pubs = []
    scholar_norm = normalize_name(args.scholar_name)
    for entry in root.findall("atom:entry", ns):
        title = normalize_whitespace("".join(entry.findtext("atom:title", default="", namespaces=ns).split()))
        summary = normalize_whitespace(entry.findtext("atom:summary", default="", namespaces=ns))
        published = entry.findtext("atom:published", default="", namespaces=ns)
        year = int(published[:4]) if re.match(r"\d{4}", published) else None
        entry_id = entry.findtext("atom:id", default="", namespaces=ns)
        authors = [normalize_whitespace(node.text or "") for node in entry.findall("atom:author/atom:name", ns)]
        if scholar_norm and not any(normalize_name(name) == scholar_norm for name in authors):
            # arXiv author search can be fuzzy; keep exact-name entries only.
            continue
        pdf_url = ""
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("title") == "pdf" or link.attrib.get("type") == "application/pdf":
                pdf_url = link.attrib.get("href", "")
                break
        arxiv_id = extract_arxiv_id(entry_id)
        pubs.append(
            {
                "id": stable_id(title),
                "title": title,
                "year": year,
                "year_group": str(year or ""),
                "direction": "",
                "venue": "arXiv",
                "authors": authors,
                "abstract": summary,
                "doi": "",
                "url": arxiv_abs_url(arxiv_id) if arxiv_id else entry_id,
                "pdf_url": pdf_url or (arxiv_pdf_url(arxiv_id) if arxiv_id else ""),
                "project_url": "",
                "code_url": "",
                "arxiv_id": arxiv_id,
                "citation_count": None,
                "source_urls": dedupe([entry_id, pdf_url]),
                "sources": ["arxiv"],
                "collection_notes": [],
            }
        )
    log.source_counts["arxiv"] += len(pubs)
    return pubs


def collect_from_openalex(args: argparse.Namespace, log: FetchLog) -> list[dict[str, Any]]:
    if args.skip_openalex or not args.scholar_name:
        return []
    mailto = args.email or os.environ.get("OPENALEX_MAILTO") or ""
    api_key = os.environ.get("OPENALEX_API_KEY") or ""
    params = {"search": args.scholar_name, "per-page": 10}
    if mailto:
        params["mailto"] = mailto
    if api_key:
        params["api_key"] = api_key
    search_url = "https://api.openalex.org/authors?" + urllib.parse.urlencode(params)
    data = request_json(search_url, timeout=args.timeout, log=log)
    if not data:
        return []
    results = data.get("results") or []
    if not results:
        log.warn(f"OpenAlex found no author for {args.scholar_name}")
        return []
    candidates = []
    scholar_norm = normalize_name(args.scholar_name)
    for item in results:
        display = item.get("display_name") or ""
        candidates.append(
            {
                "id": item.get("id"),
                "display_name": display,
                "works_count": item.get("works_count"),
                "cited_by_count": item.get("cited_by_count"),
                "last_known_institution": (item.get("last_known_institutions") or [{}])[0].get("display_name")
                if item.get("last_known_institutions")
                else "",
            }
        )
    log.author_candidates.extend({"source": "openalex", **candidate} for candidate in candidates)
    exact = [item for item in results if normalize_name(item.get("display_name") or "") == scholar_norm]
    chosen = sorted(exact or results, key=lambda x: (x.get("works_count") or 0, x.get("cited_by_count") or 0), reverse=True)[0]
    author_id = chosen.get("id", "")
    if not author_id:
        return []
    pubs = []
    cursor = "*"
    pages = 0
    while cursor and pages < 10 and len(pubs) < args.max_results:
        work_params = {
            "filter": f"authorships.author.id:{author_id}",
            "per-page": min(100, args.max_results),
            "cursor": cursor,
            "sort": "publication_year:desc",
        }
        if mailto:
            work_params["mailto"] = mailto
        if api_key:
            work_params["api_key"] = api_key
        works_url = "https://api.openalex.org/works?" + urllib.parse.urlencode(work_params)
        works_data = request_json(works_url, timeout=args.timeout, log=log)
        if not works_data:
            break
        for work in works_data.get("results") or []:
            title = normalize_whitespace(work.get("title") or "")
            if not title:
                continue
            authors = [
                (((auth.get("author") or {}).get("display_name")) or "")
                for auth in (work.get("authorships") or [])
            ]
            authors = [a for a in authors if a]
            primary = work.get("primary_location") or {}
            source = primary.get("source") or {}
            open_access = work.get("open_access") or {}
            locations = work.get("locations") or []
            pdf_url = primary.get("pdf_url") or open_access.get("oa_url") or ""
            landing = primary.get("landing_page_url") or work.get("doi") or work.get("id") or ""
            for location in locations:
                if pdf_url:
                    break
                pdf_url = location.get("pdf_url") or ""
            pubs.append(
                {
                    "id": stable_id(title),
                    "title": title,
                    "year": work.get("publication_year"),
                    "year_group": str(work.get("publication_year") or ""),
                    "direction": "",
                    "venue": source.get("display_name") or "",
                    "authors": authors,
                    "abstract": reconstruct_openalex_abstract(work.get("abstract_inverted_index") or {}),
                    "doi": strip_doi(work.get("doi") or ""),
                    "url": landing,
                    "pdf_url": pdf_url if looks_like_pdf_url(pdf_url) else "",
                    "project_url": "",
                    "code_url": "",
                    "arxiv_id": extract_arxiv_id(landing),
                    "citation_count": work.get("cited_by_count"),
                    "source_urls": dedupe([landing, pdf_url, work.get("id") or ""]),
                    "sources": ["openalex"],
                    "collection_notes": [],
                    "openalex_id": work.get("id"),
                }
            )
            if len(pubs) >= args.max_results:
                break
        cursor = (works_data.get("meta") or {}).get("next_cursor")
        pages += 1
    log.source_counts["openalex"] += len(pubs)
    return pubs


def reconstruct_openalex_abstract(index: dict[str, list[int]]) -> str:
    if not index:
        return ""
    words: list[tuple[int, str]] = []
    for word, positions in index.items():
        for pos in positions:
            words.append((pos, word))
    return normalize_whitespace(" ".join(word for _, word in sorted(words)))


def strip_doi(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value, flags=re.IGNORECASE)
    return value


def collect_from_semantic_scholar(args: argparse.Namespace, log: FetchLog) -> list[dict[str, Any]]:
    if args.skip_semantic_scholar or not (args.scholar_name or args.semantic_scholar_author_id):
        return []
    headers = {}
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    if api_key:
        headers["x-api-key"] = api_key
    author_fields = "authorId,name,aliases,affiliations,paperCount,citationCount,hIndex"
    detail_fields = (
        "name,aliases,affiliations,paperCount,citationCount,hIndex,"
        "papers.paperId,papers.title,papers.abstract,papers.year,papers.venue,"
        "papers.citationCount,papers.authors,papers.url,papers.openAccessPdf,"
        "papers.externalIds"
    )
    if args.semantic_scholar_author_id:
        authors = [{"authorId": args.semantic_scholar_author_id, "name": args.scholar_name or ""}]
    else:
        params = {
            "query": args.scholar_name,
            "fields": author_fields,
            "limit": 10,
        }
        url = "https://api.semanticscholar.org/graph/v1/author/search?" + urllib.parse.urlencode(params)
        data = request_json(url, headers=headers, timeout=args.timeout, retries=2, log=log)
        authors = (data or {}).get("data") or []
    if not authors:
        return []
    scholar_norm = normalize_name(args.scholar_name or "")
    log.author_candidates.extend(
        {
            "source": "semantic-scholar",
            "id": author.get("authorId"),
            "display_name": author.get("name"),
            "works_count": author.get("paperCount"),
            "cited_by_count": author.get("citationCount"),
            "affiliations": ", ".join(author.get("affiliations") or []),
        }
        for author in authors
    )
    exact = [author for author in authors if scholar_norm and normalize_name(author.get("name") or "") == scholar_norm]
    chosen = sorted(
        exact or authors,
        key=lambda a: (a.get("paperCount") or len(a.get("papers") or []), a.get("citationCount") or 0),
        reverse=True,
    )[0]
    author_id = chosen.get("authorId")
    if not author_id:
        return []
    detail_url = (
        "https://api.semanticscholar.org/graph/v1/author/"
        f"{urllib.parse.quote(str(author_id))}?fields={urllib.parse.quote(detail_fields)}"
    )
    detail = request_json(detail_url, headers=headers, timeout=args.timeout, retries=3, log=log)
    if not detail:
        return []
    chosen.update(detail)
    papers = chosen.get("papers") or []
    pubs = []
    for paper in papers[: args.max_results]:
        title = normalize_whitespace(paper.get("title") or "")
        if not title:
            continue
        external = paper.get("externalIds") or {}
        oa = paper.get("openAccessPdf") or {}
        authors_list = [a.get("name") for a in paper.get("authors") or [] if a.get("name")]
        arxiv_id = external.get("ArXiv") or extract_arxiv_id(paper.get("url") or "")
        pdf_url = (oa.get("url") or "").strip()
        if not pdf_url and arxiv_id:
            pdf_url = arxiv_pdf_url(arxiv_id)
        doi = external.get("DOI") or ""
        pubs.append(
            {
                "id": stable_id(title),
                "title": title,
                "year": paper.get("year"),
                "year_group": str(paper.get("year") or ""),
                "direction": "",
                "venue": paper.get("venue") or "",
                "authors": authors_list,
                "abstract": paper.get("abstract") or "",
                "doi": doi,
                "url": paper.get("url") or (f"https://doi.org/{doi}" if doi else ""),
                "pdf_url": pdf_url if looks_like_pdf_url(pdf_url) else "",
                "project_url": "",
                "code_url": "",
                "arxiv_id": arxiv_id,
                "citation_count": paper.get("citationCount"),
                "source_urls": dedupe([paper.get("url") or "", pdf_url, f"https://doi.org/{doi}" if doi else ""]),
                "sources": ["semantic-scholar"],
                "collection_notes": [],
                "semantic_scholar_paper_id": paper.get("paperId"),
            }
        )
    log.source_counts["semantic-scholar"] += len(pubs)
    return pubs


def looks_like_pdf_url(url: str) -> bool:
    if not url:
        return False
    lower = url.lower()
    return lower.endswith(".pdf") or "arxiv.org/pdf/" in lower or "pdf" in urllib.parse.urlparse(url).path.lower()


def enrich_with_crossref(publications: list[dict[str, Any]], args: argparse.Namespace, log: FetchLog) -> None:
    if args.skip_crossref:
        return
    mailto = args.email or os.environ.get("CROSSREF_MAILTO") or ""
    enriched = 0
    for pub in publications:
        if enriched >= args.crossref_limit:
            break
        if pub.get("doi") and pub.get("year") and pub.get("venue"):
            continue
        title = pub.get("title") or ""
        if not title:
            continue
        params = {"query.bibliographic": title, "rows": 1}
        if mailto:
            params["mailto"] = mailto
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
        data = request_json(url, timeout=args.timeout, retries=2, log=log)
        items = ((data or {}).get("message") or {}).get("items") or []
        if not items:
            continue
        item = items[0]
        cr_title = normalize_whitespace((item.get("title") or [""])[0])
        if title_similarity(title, cr_title) < 0.82:
            continue
        pub.setdefault("sources", []).append("crossref")
        pub["sources"] = dedupe(pub["sources"])
        pub["doi"] = pub.get("doi") or item.get("DOI") or ""
        pub["url"] = pub.get("url") or item.get("URL") or (f"https://doi.org/{pub['doi']}" if pub.get("doi") else "")
        pub["venue"] = pub.get("venue") or normalize_whitespace((item.get("container-title") or [""])[0])
        pub["year"] = pub.get("year") or crossref_year(item)
        if not pub.get("authors"):
            pub["authors"] = crossref_authors(item)
        if item.get("URL"):
            pub["source_urls"] = dedupe([*(pub.get("source_urls") or []), item.get("URL")])
        enriched += 1
        time.sleep(args.crossref_delay)
    log.source_counts["crossref-enriched"] += enriched


def crossref_year(item: dict[str, Any]) -> int | None:
    for key in ("published-print", "published-online", "published", "issued"):
        parts = ((item.get(key) or {}).get("date-parts") or [])
        if parts and parts[0]:
            try:
                return int(parts[0][0])
            except Exception:
                pass
    return None


def crossref_authors(item: dict[str, Any]) -> list[str]:
    authors = []
    for author in item.get("author") or []:
        name = normalize_whitespace(f"{author.get('given', '')} {author.get('family', '')}")
        if name:
            authors.append(name)
    return authors


def merge_publications(publication_lists: Iterable[list[dict[str, Any]]], log: FetchLog) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for pub_list in publication_lists:
        for pub in pub_list:
            title = normalize_whitespace(pub.get("title") or "")
            if not title:
                continue
            key = normalize_title(title)
            if not key:
                continue
            existing_key = None
            if key in merged:
                existing_key = key
            else:
                # Catch minor punctuation/version differences.
                for candidate_key, candidate in merged.items():
                    if title_similarity(title, candidate.get("title") or "") >= 0.96:
                        existing_key = candidate_key
                        break
            if existing_key is None:
                pub = normalize_publication(pub)
                merged[key] = pub
            else:
                merge_into(merged[existing_key], pub)
    publications = list(merged.values())
    publications.sort(key=lambda p: (p.get("year") or 0, p.get("citation_count") or 0, p.get("title") or ""), reverse=True)
    for pub in publications:
        log.source_counts["merged"] += 1
    return publications


def normalize_publication(pub: dict[str, Any]) -> dict[str, Any]:
    pub = dict(pub)
    title = normalize_whitespace(pub.get("title") or "")
    pub["id"] = pub.get("id") or stable_id(title)
    pub["title"] = title
    pub["authors"] = dedupe([normalize_whitespace(x) for x in (pub.get("authors") or [])])
    pub["source_urls"] = dedupe(pub.get("source_urls") or [])
    pub["sources"] = dedupe(pub.get("sources") or [])
    pub["collection_notes"] = pub.get("collection_notes") or []
    return pub


def merge_into(base: dict[str, Any], incoming: dict[str, Any]) -> None:
    for key in ("abstract", "doi", "url", "pdf_url", "project_url", "code_url", "arxiv_id", "venue", "direction", "year_group"):
        if not base.get(key) and incoming.get(key):
            base[key] = incoming[key]
    for key in ("openalex_id", "semantic_scholar_paper_id"):
        if incoming.get(key):
            base[key] = incoming[key]
    if not base.get("year") and incoming.get("year"):
        base["year"] = incoming["year"]
    if base.get("citation_count") is None and incoming.get("citation_count") is not None:
        base["citation_count"] = incoming["citation_count"]
    elif incoming.get("citation_count") is not None:
        base["citation_count"] = max(base.get("citation_count") or 0, incoming.get("citation_count") or 0)
    base["authors"] = dedupe([*(base.get("authors") or []), *(incoming.get("authors") or [])])
    base["source_urls"] = dedupe([*(base.get("source_urls") or []), *(incoming.get("source_urls") or [])])
    base["sources"] = dedupe([*(base.get("sources") or []), *(incoming.get("sources") or [])])
    base["collection_notes"] = dedupe([*(base.get("collection_notes") or []), *(incoming.get("collection_notes") or [])])


def candidate_pdf_urls(pub: dict[str, Any]) -> list[str]:
    candidates = []
    for value in [pub.get("pdf_url"), pub.get("url"), *(pub.get("source_urls") or [])]:
        if not value:
            continue
        value = str(value)
        if "arxiv.org/abs/" in value or "arxiv.org/pdf/" in value:
            candidates.append(arxiv_pdf_url(value))
        elif "biorxiv.org/content/" in value or "medrxiv.org/content/" in value:
            clean = value.split("?")[0].rstrip("/")
            if not clean.endswith(".full.pdf"):
                candidates.append(clean + ".full.pdf")
            candidates.append(value)
        elif looks_like_pdf_url(value):
            candidates.append(value)
    if pub.get("arxiv_id"):
        candidates.append(arxiv_pdf_url(pub["arxiv_id"]))
    return dedupe(candidates)


def download_pdfs(publications: list[dict[str, Any]], args: argparse.Namespace, log: FetchLog) -> None:
    if not args.download_pdfs:
        return
    papers_dir = args.output_dir / "papers"
    papers_dir.mkdir(parents=True, exist_ok=True)
    successes = 0
    attempts = 0
    for pub in publications:
        if successes >= args.max_pdfs or attempts >= args.max_pdf_attempts:
            break
        if pub.get("local_pdf"):
            continue
        for url in candidate_pdf_urls(pub):
            if successes >= args.max_pdfs or attempts >= args.max_pdf_attempts:
                break
            attempts += 1
            filename = f"{pub.get('year') or 'unknown'}-{slugify(pub.get('title') or pub['id'], 80)}.pdf"
            target = papers_dir / filename
            result = try_download_pdf(url, target, args, log)
            log.pdf_attempts.append(
                {
                    "title": pub.get("title"),
                    "url": url,
                    "status": "success" if result else "failed",
                    "path": str(target) if result else "",
                }
            )
            if result:
                pub["local_pdf"] = str(target)
                pub["pdf_url"] = pub.get("pdf_url") or url
                successes += 1
                break
    log.source_counts["pdf-downloaded"] += successes


def try_download_pdf(url: str, target: Path, args: argparse.Namespace, log: FetchLog) -> bool:
    if target.exists() and not args.overwrite_pdfs and target.stat().st_size > 0:
        return True
    request_headers = {"User-Agent": DEFAULT_UA, "Accept": "application/pdf,*/*;q=0.8"}
    try:
        req = urllib.request.Request(url, headers=request_headers)
        with urllib.request.urlopen(req, timeout=args.pdf_timeout, context=SSL_CONTEXT) as response:
            content_type = response.headers.get("Content-Type", "").lower()
            first = response.read(5)
            if first != b"%PDF-" and "pdf" not in content_type:
                return False
            max_bytes = args.max_pdf_mb * 1024 * 1024
            total = len(first)
            with target.open("wb") as f:
                f.write(first)
                while True:
                    chunk = response.read(1024 * 256)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > max_bytes:
                        f.close()
                        target.unlink(missing_ok=True)
                        log.warn(f"PDF exceeded --max-pdf-mb: {url}")
                        return False
                    f.write(chunk)
        return target.exists() and target.stat().st_size > 1024
    except Exception as exc:  # noqa: BLE001
        log.warn(f"PDF download failed: {url} ({exc})")
        target.unlink(missing_ok=True)
        return False


def write_outputs(publications: list[dict[str, Any]], args: argparse.Namespace, log: FetchLog) -> None:
    args.output_dir.mkdir(parents=True, exist_ok=True)
    metadata = {
        "generated_at": now_iso(),
        "scholar_name": args.scholar_name,
        "homepage": args.homepage,
        "publication_count": len(publications),
        "sources": dict(log.source_counts),
    }
    index_json = {"metadata": metadata, "publications": publications}
    (args.output_dir / "publication-index.json").write_text(
        json.dumps(index_json, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (args.output_dir / "publication-index.md").write_text(
        render_publication_index(publications, metadata),
        encoding="utf-8",
    )
    (args.output_dir / "crawl-report.md").write_text(
        render_crawl_report(publications, metadata, log),
        encoding="utf-8",
    )
    (args.output_dir / "agent-fallback-queue.md").write_text(
        render_fallback_queue(publications, args, log),
        encoding="utf-8",
    )


def md_escape(value: Any) -> str:
    text = normalize_whitespace(str(value or ""))
    return text.replace("|", "\\|")


def render_publication_index(publications: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    lines = [
        f"# {metadata.get('scholar_name') or 'Scholar'} Publication Index",
        "",
        f"- Generated: {metadata['generated_at']}",
        f"- Homepage: {metadata.get('homepage') or 'not provided'}",
        f"- Publications: {len(publications)}",
        "",
        "| Year | Direction | Title | Venue | Links | Sources | Local PDF |",
        "|---:|---|---|---|---|---|---|",
    ]
    for pub in publications:
        links = []
        for label, key in (("paper", "url"), ("pdf", "pdf_url"), ("project", "project_url"), ("code", "code_url")):
            if pub.get(key):
                links.append(f"[{label}]({pub[key]})")
        lines.append(
            "| {year} | {direction} | {title} | {venue} | {links} | {sources} | {local_pdf} |".format(
                year=md_escape(pub.get("year") or ""),
                direction=md_escape(pub.get("direction") or ""),
                title=md_escape(pub.get("title") or ""),
                venue=md_escape(pub.get("venue") or ""),
                links="<br>".join(links),
                sources=md_escape(", ".join(pub.get("sources") or [])),
                local_pdf=md_escape(pub.get("local_pdf") or ""),
            )
        )
    lines.append("")
    return "\n".join(lines)


def render_crawl_report(publications: list[dict[str, Any]], metadata: dict[str, Any], log: FetchLog) -> str:
    with_pdf = sum(1 for pub in publications if pub.get("pdf_url") or pub.get("local_pdf"))
    downloaded = sum(1 for pub in publications if pub.get("local_pdf"))
    with_abstract = sum(1 for pub in publications if pub.get("abstract"))
    lines = [
        f"# Crawl Report: {metadata.get('scholar_name') or 'Scholar'}",
        "",
        f"- Generated: {metadata['generated_at']}",
        f"- Publication records: {len(publications)}",
        f"- Records with PDF URL: {with_pdf}",
        f"- Downloaded PDFs: {downloaded}",
        f"- Records with abstracts: {with_abstract}",
        "",
        "## Source Counts",
        "",
    ]
    for key, value in sorted(log.source_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Homepage Pages", ""])
    if log.homepage_pages:
        lines.extend(f"- {url}" for url in log.homepage_pages)
    else:
        lines.append("- none")
    lines.extend(["", "## Author Candidates", ""])
    if log.author_candidates:
        for candidate in log.author_candidates[:20]:
            label = candidate.get("display_name") or candidate.get("id") or "unknown"
            details = ", ".join(
                f"{k}={v}"
                for k, v in candidate.items()
                if k not in {"display_name"} and v not in (None, "")
            )
            lines.append(f"- {label}: {details}")
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {warning}" for warning in log.warnings) if log.warnings else lines.append("- none")
    lines.extend(["", "## PDF Attempts", ""])
    if log.pdf_attempts:
        for item in log.pdf_attempts[:100]:
            lines.append(f"- {item['status']}: {item.get('title')} -> {item.get('url')}")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Coverage Guidance",
            "",
            "- If publication count is much lower than the scholar's public profile, rerun with fewer skipped sources and an API key if available.",
            "- If PDF coverage is weak, use `agent-fallback-queue.md` and the agent's own browser/search capability to recover open PDFs, project pages, or abstracts.",
            "- Treat non-open or paywalled full text as unavailable unless the user provides lawful access.",
            "",
        ]
    )
    return "\n".join(lines)


def render_fallback_queue(publications: list[dict[str, Any]], args: argparse.Namespace, log: FetchLog) -> str:
    lines = [
        f"# Agent Fallback Queue: {args.scholar_name or 'Scholar'}",
        "",
        "Use this file after running the script. The agent should manually browse/search only for records whose metadata, abstract, or open PDF coverage remains weak.",
        "",
    ]
    if not publications:
        scholar = args.scholar_name or "the scholar"
        lines.extend(
            [
                "No publication records were collected by the script.",
                "",
                "## Manual Recovery Searches",
                "",
                f"- \"{scholar}\" publications",
                f"- \"{scholar}\" Google Scholar",
                f"- \"{scholar}\" Semantic Scholar",
                f"- \"{scholar}\" arXiv",
                f"- \"{scholar}\" research homepage",
                "",
                "If a homepage or profile is found, rerun the collector with `--homepage`. If an author id is found, rerun with `--semantic-scholar-author-id` or use the source manually and record the confidence.",
                "",
            ]
        )
        return "\n".join(lines)
    weak = []
    for pub in publications:
        issues = []
        if not pub.get("pdf_url") and not pub.get("local_pdf"):
            issues.append("missing open PDF")
        if not pub.get("abstract"):
            issues.append("missing abstract")
        if not pub.get("year"):
            issues.append("missing year")
        if not pub.get("venue"):
            issues.append("missing venue")
        if issues:
            weak.append((pub, issues))
    if not weak:
        lines.append("No weak records detected by the script.")
        lines.append("")
        return "\n".join(lines)
    for idx, (pub, issues) in enumerate(weak, 1):
        title = pub.get("title") or "Untitled"
        lines.extend(
            [
                f"## {idx}. {title}",
                "",
                f"- Issues: {', '.join(issues)}",
                f"- Known URL: {pub.get('url') or 'none'}",
                f"- Known PDF URL: {pub.get('pdf_url') or 'none'}",
                "- Suggested searches:",
                f"  - \"{title}\" PDF",
                f"  - \"{title}\" arXiv",
                f"  - \"{title}\" \"{args.scholar_name or ''}\"",
                "- If found manually, record the source URL and confidence in the evidence snapshot before using it for distillation.",
                "",
            ]
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scholar-name", help="Scholar name, e.g. 'Weidi Xie'")
    parser.add_argument("--homepage", help="Academic homepage or publication page")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for index, reports, and downloaded PDFs")
    parser.add_argument("--semantic-scholar-author-id", help="Semantic Scholar author id to avoid ambiguous author search")
    parser.add_argument("--skip-semantic-scholar", action="store_true", help="Skip Semantic Scholar")
    parser.add_argument("--skip-openalex", action="store_true", help="Skip OpenAlex")
    parser.add_argument("--skip-arxiv", action="store_true", help="Skip arXiv")
    parser.add_argument("--skip-crossref", action="store_true", help="Skip Crossref title enrichment")
    parser.add_argument("--download-pdfs", action="store_true", help="Download public/open-access PDFs when direct URLs are available")
    parser.add_argument("--max-pdfs", type=int, default=30, help="Maximum successful PDF downloads")
    parser.add_argument("--max-pdf-attempts", type=int, default=150, help="Maximum candidate PDF URLs to try")
    parser.add_argument("--max-pdf-mb", type=int, default=80, help="Maximum size for a downloaded PDF")
    parser.add_argument("--overwrite-pdfs", action="store_true", help="Overwrite existing local PDF files")
    parser.add_argument("--max-results", type=int, default=200, help="Maximum records to request from each external source")
    parser.add_argument("--max-homepage-pages", type=int, default=10, help="Maximum same-site homepage pages to crawl")
    parser.add_argument("--crossref-limit", type=int, default=60, help="Maximum records to enrich through Crossref")
    parser.add_argument("--crossref-delay", type=float, default=0.15, help="Delay between Crossref requests")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds")
    parser.add_argument("--pdf-timeout", type=int, default=45, help="PDF download timeout in seconds")
    parser.add_argument("--email", help="Email for polite API usage when supported")
    parser.add_argument(
        "--allow-insecure-ssl",
        action="store_true",
        help="Disable HTTPS certificate verification only when local certificate stores are broken",
    )
    args = parser.parse_args()
    if not args.scholar_name and not args.homepage and not args.semantic_scholar_author_id:
        parser.error("provide --scholar-name, --homepage, or --semantic-scholar-author-id")
    args.output_dir = args.output_dir.resolve()
    return args


def configure_ssl(args: argparse.Namespace, log: FetchLog) -> None:
    global SSL_CONTEXT
    if args.allow_insecure_ssl:
        SSL_CONTEXT = ssl._create_unverified_context()  # noqa: SLF001
        log.warn("HTTPS certificate verification is disabled for this run.")
        return
    try:
        import certifi  # type: ignore

        SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        SSL_CONTEXT = None


def main() -> int:
    args = parse_args()
    log = FetchLog()
    configure_ssl(args, log)
    publication_lists = []
    publication_lists.append(collect_from_homepage(args, log))
    publication_lists.append(collect_from_arxiv(args, log))
    publication_lists.append(collect_from_openalex(args, log))
    publication_lists.append(collect_from_semantic_scholar(args, log))
    publications = merge_publications(publication_lists, log)
    if publications:
        enrich_with_crossref(publications, args, log)
        download_pdfs(publications, args, log)
    else:
        log.warn("No publications found. Use the agent fallback path with manual search/browsing.")
    write_outputs(publications, args, log)
    print(f"Wrote {len(publications)} records to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
