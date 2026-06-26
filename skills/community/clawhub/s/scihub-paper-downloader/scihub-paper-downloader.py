#!/usr/bin/env python3
"""Resolve a DOI to a direct PDF URL through Sci-Hub.

Zero dependencies. Python standard library only.
"""

from __future__ import annotations

import base64
import hashlib
import http.client
import http.cookiejar
import json
import os
import re
import sys
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlsplit, urlunsplit
from urllib.request import (
    HTTPCookieProcessor,
    HTTPRedirectHandler,
    Request,
    build_opener,
)

TIMEOUT = 20
STATUS_FOUND = "FOUND"
STATUS_NOT_FOUND = "NOT_FOUND"
STATUS_MIRROR_ERROR = "MIRROR_ERROR"
STATUS_INVALID_INPUT = "INVALID_INPUT"
DEFAULT_MIRRORS = (
    "https://sci-hub.st",
    "https://sci-hub.ru",
    "https://sci-hub.se",
)
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/133.0.0.0 Safari/537.36"
)
PDF_PATTERNS = (
    re.compile(r'<(?:iframe|embed|object)[^>]+(?:src|data)=["\']([^"\']+)["\']', re.I),
    re.compile(r'["\']((?:https?:)?//[^"\']+?(?:\.pdf|/pdf)[^"\']*)["\']', re.I),
)
OA_HINT_PATTERN = re.compile(
    r'<block-rounded[^>]+class\s*=\s*["\'][^"\']*\bopenaccess\b[^"\']*["\'][^>]*>(?:(?!</block-rounded>).)*?<a[^>]+href\s*=\s*["\']([^"\']+)["\']',
    re.I | re.S,
)


class Browser:
    def __init__(self) -> None:
        jar = http.cookiejar.CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(jar), HTTPRedirectHandler())

    def open(
        self,
        url: str,
        *,
        data: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> http.client.HTTPResponse:
        req = Request(url, data=data, headers=headers or {})
        return self.opener.open(req, timeout=TIMEOUT)


def _headers(extra: dict[str, str] | None = None) -> dict[str, str]:
    base = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    if extra:
        base.update(extra)
    return base


def _canonicalize(url: str) -> str:
    parts = urlsplit(url.strip().replace("\\/", "/"))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))


def _normalize_doi(raw: str) -> str:
    doi = raw.strip()
    doi = re.sub(r"^(?:doi:\s*)", "", doi, flags=re.I)
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.I)
    return doi.strip()


def _extract_title(html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if not match:
        return ""
    return " ".join(match.group(1).split())


def _iter_pdf_candidates(html: str, page_url: str) -> Iterable[str]:
    seen: set[str] = set()
    for pattern in PDF_PATTERNS:
        for raw in pattern.findall(html):
            candidate = raw.strip()
            if not candidate:
                continue
            if candidate.startswith("//"):
                candidate = f"https:{candidate}"
            else:
                candidate = urljoin(page_url, candidate)
            candidate = _canonicalize(candidate)
            if candidate in seen:
                continue
            seen.add(candidate)
            yield candidate


def _has_altcha(html: str) -> bool:
    return bool(re.search(r"/captcha/challenge/\d+", html))


def _hexdigest(data: str, algorithm: str) -> str:
    digest = hashlib.new(algorithm.strip().lower().replace("-", ""))
    digest.update(data.encode("utf-8"))
    return digest.hexdigest()


def _solve_altcha(browser: Browser, page_url: str, html: str) -> bool:
    challenge_id = re.search(r"/captcha/challenge/(\d+)", html)
    if not challenge_id:
        return False
    parts = urlsplit(page_url)
    base_url = f"{parts.scheme}://{parts.netloc}"
    challenge_url = urljoin(base_url, f"/captcha/challenge/{challenge_id.group(1)}")
    solution_url = urljoin(base_url, f"/captcha/solution/{challenge_id.group(1)}")
    try:
        with browser.open(challenge_url, headers=_headers({"Accept": "application/json"})) as resp:
            challenge = json.loads(resp.read().decode("utf-8", errors="replace"))
        algorithm = str(challenge["algorithm"])
        salt = str(challenge["salt"])
        target = str(challenge["challenge"])
        max_number = int(challenge["maxNumber"])
    except (HTTPError, URLError, OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return False
    number = None
    try:
        for value in range(max_number + 1):
            if _hexdigest(f"{salt}{value}", algorithm) == target:
                number = value
                break
    except ValueError:
        return False
    if number is None:
        return False
    payload = base64.b64encode(
        json.dumps(
            {
                "algorithm": algorithm,
                "challenge": target,
                "number": number,
                "salt": salt,
                "signature": challenge.get("signature", ""),
                "took": 0,
            },
            separators=(",", ":"),
        ).encode("utf-8")
    ).decode("ascii")
    body = json.dumps({"captcha": payload}).encode("utf-8")
    try:
        with browser.open(
            solution_url,
            data=body,
            headers=_headers(
                {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Origin": base_url,
                    "Referer": page_url,
                }
            ),
        ) as resp:
            response = json.loads(resp.read().decode("utf-8", errors="replace"))
    except (HTTPError, URLError, OSError, TypeError, ValueError, json.JSONDecodeError):
        return False
    return bool(response.get("success"))


def _fetch_page(browser: Browser, doi_url: str) -> tuple[str, str]:
    current_url = doi_url
    for _ in range(3):
        with browser.open(current_url, headers=_headers()) as resp:
            final_url = resp.geturl()
            html = resp.read().decode("utf-8", errors="replace")
        if not _has_altcha(html):
            return final_url, html
        if not _solve_altcha(browser, final_url, html):
            break
        current_url = doi_url
    return "", ""


def _is_pdf(browser: Browser, url: str) -> bool:
    headers = _headers(
        {
            "Accept": "application/pdf,*/*;q=0.8",
            "Range": "bytes=0-7",
        }
    )
    try:
        with browser.open(url, headers=headers) as resp:
            content_type = (resp.headers.get("Content-Type") or "").lower()
            if "application/pdf" in content_type:
                return True
            prefix = resp.read(8)
            return prefix.startswith(b"%PDF-")
    except (HTTPError, URLError, OSError):
        return False


def _extract_oa_link(html: str, page_url: str) -> str:
    match = OA_HINT_PATTERN.search(html)
    if not match:
        return ""
    candidate = match.group(1).strip()
    if not candidate:
        return ""
    if candidate.startswith("//"):
        candidate = f"https:{candidate}"
    else:
        candidate = urljoin(page_url, candidate)
    return _canonicalize(candidate)


def _mirror_list() -> tuple[str, ...]:
    raw = os.environ.get("SCIHUB_MIRRORS", "")
    if raw.strip():
        return tuple(item.strip().rstrip("/") for item in raw.split(",") if item.strip())
    return DEFAULT_MIRRORS


def resolve_pdf(doi: str) -> tuple[str, str]:
    normalized = _normalize_doi(doi)
    if not normalized:
        return STATUS_INVALID_INPUT, ""
    safe_doi = quote(normalized, safe="/:().-_")
    saw_not_found = False
    saw_mirror_error = False
    oa_link = ""
    for mirror in _mirror_list():
        browser = Browser()
        try:
            page_url, html = _fetch_page(browser, f"{mirror}/{safe_doi}")
        except (HTTPError, URLError, OSError):
            saw_mirror_error = True
            continue
        if not html:
            saw_mirror_error = True
            continue
        title = _extract_title(html).lower()
        if "not available through sci-hub" in title or "no articles found" in title:
            saw_not_found = True
            if not oa_link:
                oa_link = _extract_oa_link(html, page_url)
            continue
        for candidate in _iter_pdf_candidates(html, page_url):
            if _is_pdf(browser, candidate):
                return STATUS_FOUND, candidate
        saw_mirror_error = True
    if saw_not_found:
        return STATUS_NOT_FOUND, oa_link
    if saw_mirror_error:
        return STATUS_MIRROR_ERROR, ""
    return STATUS_NOT_FOUND, ""


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: scihub-paper-downloader.py <DOI>", file=sys.stderr)
        sys.exit(1)
    status, url = resolve_pdf(sys.argv[1])
    if status == STATUS_FOUND:
        print(url)
        sys.exit(0)
    print(status)
    if status == STATUS_NOT_FOUND and url:
        print(f"OA_LINK {url}")
    if status == STATUS_NOT_FOUND:
        sys.exit(1)
    if status == STATUS_MIRROR_ERROR:
        sys.exit(2)
    sys.exit(3)
