#!/usr/bin/env python3
"""Bounded, robots-aware website inventory for the Rankizz local audit skill."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from collections import Counter, deque
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


USER_AGENT = "Rankizz-Skill-LocalAudit/1.0"
MAX_BYTES = 5_000_000
MAX_SITEMAPS = 5


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta: dict[str, str] = {}
        self.canonical: str | None = None
        self.headings: list[dict[str, str]] = []
        self.links: list[str] = []
        self.images = 0
        self.images_missing_alt = 0
        self.json_ld_types: list[str] = []
        self._capture: str | None = None
        self._buffer: list[str] = []
        self._ignored_depth = 0
        self._json_ld_depth = 0
        self._json_ld_buffer: list[str] = []
        self.visible_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        lower = tag.lower()
        if lower in {"style", "noscript"}:
            self._ignored_depth += 1
        if lower == "script":
            if values.get("type", "").lower() == "application/ld+json":
                self._json_ld_depth = 1
                self._json_ld_buffer = []
            else:
                self._ignored_depth += 1
        if lower == "title" or re.fullmatch(r"h[1-6]", lower):
            self._capture = lower
            self._buffer = []
        if lower == "meta":
            key = (values.get("name") or values.get("property") or "").lower()
            if key:
                self.meta[key] = values.get("content", "").strip()
        if lower == "link" and "canonical" in values.get("rel", "").lower().split():
            self.canonical = values.get("href", "").strip() or None
        if lower == "a" and values.get("href"):
            self.links.append(values["href"].strip())
        if lower == "img":
            self.images += 1
            if "alt" not in values:
                self.images_missing_alt += 1

    def handle_endtag(self, tag: str) -> None:
        lower = tag.lower()
        if self._capture == lower:
            text = normalize_text(" ".join(self._buffer))
            if lower == "title":
                self.title = text
            elif text:
                self.headings.append({"level": lower, "text": text})
            self._capture = None
            self._buffer = []
        if lower == "script" and self._json_ld_depth:
            self._record_json_ld("".join(self._json_ld_buffer))
            self._json_ld_depth = 0
            self._json_ld_buffer = []
        elif lower in {"script", "style", "noscript"} and self._ignored_depth:
            self._ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buffer.append(data)
        if self._json_ld_depth:
            self._json_ld_buffer.append(data)
        elif not self._ignored_depth:
            text = normalize_text(data)
            if text:
                self.visible_text.append(text)

    def _record_json_ld(self, source: str) -> None:
        try:
            value = json.loads(source)
        except (json.JSONDecodeError, TypeError):
            return

        def visit(item: Any) -> None:
            if isinstance(item, list):
                for child in item:
                    visit(child)
            elif isinstance(item, dict):
                schema_type = item.get("@type")
                if isinstance(schema_type, str):
                    self.json_ld_types.append(schema_type)
                elif isinstance(schema_type, list):
                    self.json_ld_types.extend(
                        entry for entry in schema_type if isinstance(entry, str)
                    )
                for key in ("@graph",):
                    visit(item.get(key))

        visit(value)


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def validate_target(url: str, allow_private: bool) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Target must be an absolute HTTP or HTTPS URL")
    if parsed.username or parsed.password:
        raise ValueError("Credential-bearing URLs are not allowed")
    if allow_private:
        return parsed
    addresses = {
        item[4][0]
        for item in socket.getaddrinfo(parsed.hostname, parsed.port or 443)
    }
    for address in addresses:
        ip = ipaddress.ip_address(address)
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
        ):
            raise ValueError(
                "Private-network targets are blocked by default; use "
                "--allow-private-network only for a site you control"
            )
    return parsed


def normalized_url(base: str, candidate: str, hostname: str) -> str | None:
    absolute = urllib.parse.urljoin(base, candidate)
    parsed = urllib.parse.urlparse(absolute)
    if parsed.scheme not in {"http", "https"} or parsed.hostname != hostname:
        return None
    if parsed.username or parsed.password:
        return None
    clean = parsed._replace(fragment="", query=parsed.query).geturl()
    return clean


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, allow_private: bool) -> None:
        super().__init__()
        self.allow_private = allow_private

    def redirect_request(
        self,
        request: urllib.request.Request,
        file_pointer: Any,
        code: int,
        message: str,
        headers: Any,
        new_url: str,
    ) -> urllib.request.Request | None:
        validate_target(new_url, self.allow_private)
        return super().redirect_request(
            request, file_pointer, code, message, headers, new_url
        )


def fetch(
    url: str, timeout: float, allow_private: bool
) -> tuple[int, str, bytes, str]:
    validate_target(url, allow_private)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xml;q=0.9,*/*;q=0.5"},
    )
    opener = urllib.request.build_opener(SafeRedirectHandler(allow_private))
    try:
        with opener.open(request, timeout=timeout) as response:
            length = response.headers.get("Content-Length")
            if length and int(length) > MAX_BYTES:
                raise ValueError(f"Response exceeds {MAX_BYTES} bytes")
            body = response.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                raise ValueError(f"Response exceeds {MAX_BYTES} bytes")
            return (
                response.status,
                response.headers.get("Content-Type", ""),
                body,
                response.geturl(),
            )
    except urllib.error.HTTPError as error:
        body = error.read(MAX_BYTES + 1)
        return error.code, error.headers.get("Content-Type", ""), body[:MAX_BYTES], error.geturl()


def sitemap_urls(body: bytes) -> tuple[list[str], list[str]]:
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return [], []
    tag = root.tag.rsplit("}", 1)[-1]
    locations = [
        normalize_text(element.text or "")
        for element in root.iter()
        if element.tag.rsplit("}", 1)[-1] == "loc" and element.text
    ]
    return (locations, []) if tag == "urlset" else ([], locations)


def load_sitemaps(
    candidates: list[str],
    hostname: str,
    timeout: float,
    delay: float,
    allow_private: bool,
) -> list[str]:
    pages: list[str] = []
    queue = deque(candidates)
    seen: set[str] = set()
    while queue and len(seen) < MAX_SITEMAPS:
        sitemap = queue.popleft()
        if sitemap in seen:
            continue
        seen.add(sitemap)
        try:
            status, _, body, final_url = fetch(sitemap, timeout, allow_private)
            if status >= 400:
                continue
            urls, nested = sitemap_urls(body)
            for url in urls:
                normalized = normalized_url(final_url, url, hostname)
                if normalized:
                    pages.append(normalized)
            for url in nested:
                normalized = normalized_url(final_url, url, hostname)
                if normalized:
                    queue.append(normalized)
        except (OSError, ValueError, urllib.error.URLError):
            continue
        time.sleep(delay)
    return pages


def inspect_page(url: str, status: int, content_type: str, body: bytes) -> dict[str, Any]:
    row: dict[str, Any] = {"url": url, "status": status, "contentType": content_type}
    if "html" not in content_type.lower() and b"<html" not in body[:500].lower():
        return row
    parser = PageParser()
    parser.feed(body.decode("utf-8", errors="replace"))
    words = re.findall(r"\b[\w'-]+\b", " ".join(parser.visible_text), re.UNICODE)
    row.update(
        {
            "title": parser.title or None,
            "metaDescription": parser.meta.get("description") or None,
            "metaRobots": parser.meta.get("robots") or None,
            "canonical": parser.canonical,
            "headings": parser.headings,
            "wordCount": len(words),
            "images": parser.images,
            "imagesMissingAlt": parser.images_missing_alt,
            "jsonLdTypes": sorted(set(parser.json_ld_types)),
            "openGraph": {
                key: value for key, value in parser.meta.items() if key.startswith("og:")
            },
            "links": parser.links,
        }
    )
    return row


def page_count(value: str) -> int:
    count = int(value)
    if not 1 <= count <= 500:
        raise argparse.ArgumentTypeError("must be between 1 and 500")
    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Absolute HTTP or HTTPS start URL")
    parser.add_argument("--max-pages", type=page_count, default=10)
    parser.add_argument("--path-prefix", default="/", help="Only crawl paths under this prefix")
    parser.add_argument("--output", default="site-audit.json")
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--delay", type=float, default=0.25)
    parser.add_argument("--allow-private-network", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    parsed = validate_target(args.url, args.allow_private_network)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    start_url = parsed._replace(fragment="").geturl()
    robots_url = urllib.parse.urljoin(origin, "/robots.txt")
    robot_parser = urllib.robotparser.RobotFileParser()
    robot_parser.set_url(robots_url)
    sitemap_candidates = [urllib.parse.urljoin(origin, "/sitemap.xml")]
    robots_status: int | None = None
    robots_error: str | None = None

    try:
        robots_status, _, robots_body, _ = fetch(
            robots_url, args.timeout, args.allow_private_network
        )
        robots_text = robots_body.decode("utf-8", errors="replace")
        robot_parser.parse(robots_text.splitlines())
        sitemap_candidates = [
            normalize_text(line.split(":", 1)[1])
            for line in robots_text.splitlines()
            if line.lower().startswith("sitemap:") and ":" in line
        ] or sitemap_candidates
    except (OSError, ValueError, urllib.error.URLError) as error:
        robots_error = str(error)
        robot_parser.parse([])

    discovered = load_sitemaps(
        sitemap_candidates,
        parsed.hostname or "",
        args.timeout,
        args.delay,
        args.allow_private_network,
    )
    queue = deque([start_url, *discovered])
    queued = set(queue)
    visited: set[str] = set()
    pages: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []

    while queue and len(pages) < args.max_pages:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        if not urllib.parse.urlparse(url).path.startswith(args.path_prefix):
            continue
        if robots_status and robots_status < 400 and not robot_parser.can_fetch(USER_AGENT, url):
            skipped.append({"url": url, "reason": "robots.txt disallow"})
            continue
        try:
            status, content_type, body, final_url = fetch(
                url, args.timeout, args.allow_private_network
            )
            final_parsed = validate_target(final_url, args.allow_private_network)
            if final_parsed.hostname != parsed.hostname:
                skipped.append({"url": url, "reason": "redirected off origin"})
                continue
            row = inspect_page(final_url, status, content_type, body)
            pages.append(row)
            for href in row.pop("links", []):
                candidate = normalized_url(final_url, href, parsed.hostname or "")
                if candidate and candidate not in queued and candidate not in visited:
                    queued.add(candidate)
                    queue.append(candidate)
        except (OSError, ValueError, urllib.error.URLError) as error:
            pages.append({"url": url, "status": None, "error": str(error)})
        time.sleep(max(0.0, args.delay))

    titles = [row.get("title") for row in pages if row.get("title")]
    duplicate_titles = {
        title: count for title, count in Counter(titles).items() if count > 1
    }
    result = {
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "startUrl": start_url,
        "scope": {"maxPages": args.max_pages, "pathPrefix": args.path_prefix},
        "robots": {"url": robots_url, "status": robots_status, "error": robots_error},
        "sitemaps": sitemap_candidates,
        "summary": {
            "pagesFetched": len(pages),
            "pagesSkipped": len(skipped),
            "errorPages": sum(1 for row in pages if row.get("error") or (row.get("status") or 0) >= 400),
            "missingTitles": sum(1 for row in pages if row.get("status") == 200 and not row.get("title")),
            "missingDescriptions": sum(1 for row in pages if row.get("status") == 200 and not row.get("metaDescription")),
            "duplicateTitles": duplicate_titles,
        },
        "pages": pages,
        "skipped": skipped,
    }
    output = Path(args.output)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {output} with {len(pages)} fetched pages")


if __name__ == "__main__":
    main()
