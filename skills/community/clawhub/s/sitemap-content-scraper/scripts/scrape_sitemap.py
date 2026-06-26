#!/usr/bin/env python3
"""
Scrape public pages listed in a sitemap and save them as Markdown plus a manifest.

This script supports the sitemap-content-scraper skill by taking a chosen sitemap,
optionally filtering its URLs, and writing a traceable local corpus for later use.
"""

from __future__ import annotations

import argparse
import functools
import ipaddress
import json
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


IGNORE_TAGS = {
    "script",
    "style",
    "noscript",
    "svg",
    "canvas",
    "iframe",
    "form",
    "nav",
    "button",
}
BLOCK_TAGS = {
    "p",
    "div",
    "section",
    "article",
    "main",
    "aside",
    "header",
    "footer",
    "li",
    "ul",
    "ol",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "pre",
    "blockquote",
}


@functools.lru_cache(maxsize=1024)
def hostname_public_status(hostname: str) -> tuple[bool, str | None]:
    normalized = hostname.strip().strip(".").lower()
    if not normalized:
        return False, "empty hostname"
    if normalized in {"localhost"}:
        return False, "localhost is not allowed"
    if normalized.endswith((".local", ".localhost", ".internal", ".home.arpa")):
        return False, "internal-only hostname suffix is not allowed"

    try:
        ip = ipaddress.ip_address(normalized)
    except ValueError:
        pass
    else:
        if not ip.is_global:
            return False, f"non-public IP {ip} is not allowed"
        return True, None

    try:
        addrinfo = socket.getaddrinfo(normalized, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        return False, f"hostname resolution failed: {exc}"

    resolved_ips: set[ipaddress.IPv4Address | ipaddress.IPv6Address] = set()
    for info in addrinfo:
        addr = info[4][0]
        try:
            resolved_ips.add(ipaddress.ip_address(addr))
        except ValueError:
            continue

    if not resolved_ips:
        return False, "hostname did not resolve to usable IP addresses"
    for ip in resolved_ips:
        if not ip.is_global:
            return False, f"hostname resolves to non-public address {ip}"
    return True, None


def assert_public_url(url: str, field_name: str) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"{field_name} must use http or https")
    if not parsed.netloc or not parsed.hostname:
        raise ValueError(f"invalid {field_name}: {url}")
    is_public, reason = hostname_public_status(parsed.hostname)
    if not is_public:
        raise ValueError(f"{field_name} host is not public: {reason}")
    return parsed


def is_public_hostname(hostname: str | None) -> bool:
    if not hostname:
        return False
    is_public, _ = hostname_public_status(hostname)
    return is_public


def normalize_http_url(raw_url: str, field_name: str) -> str:
    value = raw_url.strip()
    if not value:
        raise ValueError(f"{field_name} is required")
    if "://" not in value:
        value = f"https://{value}"

    parsed = assert_public_url(value, field_name=field_name)
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", parsed.query, ""))


def fetch_text(url: str, timeout: float, user_agent: str) -> tuple[str | None, str | None]:
    class PublicOnlyRedirectHandler(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
            assert_public_url(newurl, field_name="redirect target")
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    try:
        assert_public_url(url, field_name="request URL")
    except ValueError as exc:
        return None, str(exc)

    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    opener = urllib.request.build_opener(PublicOnlyRedirectHandler())
    try:
        with opener.open(request, timeout=timeout) as response:
            try:
                assert_public_url(response.geturl(), field_name="final URL")
            except ValueError as exc:
                return None, str(exc)
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace"), None
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return None, str(exc.reason)
    except Exception as exc:  # pragma: no cover - defensive path
        return None, str(exc)


def parse_sitemap_urls(xml_text: str) -> tuple[str, list[str]]:
    root = ET.fromstring(xml_text)
    tag = root.tag.rsplit("}", 1)[-1].lower()
    locs: list[str] = []
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1].lower() == "loc" and element.text:
            locs.append(element.text.strip())
    return tag, locs


def gather_urls_from_sitemap(
    sitemap_url: str,
    timeout: float,
    user_agent: str,
    seen_sitemaps: set[str] | None = None,
) -> list[str]:
    sitemap_url = normalize_http_url(sitemap_url, field_name="sitemap-url")
    seen_sitemaps = seen_sitemaps or set()
    if sitemap_url in seen_sitemaps:
        return []
    seen_sitemaps.add(sitemap_url)

    xml_text, error = fetch_text(sitemap_url, timeout=timeout, user_agent=user_agent)
    if xml_text is None:
        raise RuntimeError(f"could not fetch sitemap {sitemap_url}: {error}")

    tag, locs = parse_sitemap_urls(xml_text)
    if tag == "sitemapindex":
        urls: list[str] = []
        for child_url in locs:
            resolved_child_url = urllib.parse.urljoin(sitemap_url, child_url)
            urls.extend(
                gather_urls_from_sitemap(
                    resolved_child_url,
                    timeout=timeout,
                    user_agent=user_agent,
                    seen_sitemaps=seen_sitemaps,
                )
            )
        return urls

    if tag == "urlset":
        return [urllib.parse.urljoin(sitemap_url, url) for url in locs]

    raise RuntimeError(f"unsupported sitemap type: {tag}")


class ReadableHTMLExtractor(HTMLParser):
    """Extract page title, description, and readable body text from HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ignore_depth = 0
        self.main_depth = 0
        self.article_depth = 0
        self.in_title = False
        self.title_parts: list[str] = []
        self.article_chunks: list[str] = []
        self.main_chunks: list[str] = []
        self.all_chunks: list[str] = []
        self.description: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key.lower(): (value or "") for key, value in attrs}
        tag = tag.lower()
        if tag in IGNORE_TAGS:
            self.ignore_depth += 1
            return
        if tag == "title":
            self.in_title = True
        if tag == "article":
            self.article_depth += 1
        if tag == "main" or attrs_dict.get("role", "").lower() == "main":
            self.main_depth += 1
        if tag == "meta":
            meta_name = attrs_dict.get("name", "").lower()
            meta_property = attrs_dict.get("property", "").lower()
            if meta_name == "description" or meta_property == "og:description":
                description = attrs_dict.get("content", "").strip()
                if description and not self.description:
                    self.description = description
        if tag in BLOCK_TAGS:
            self._append_text("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in IGNORE_TAGS and self.ignore_depth:
            self.ignore_depth -= 1
            return
        if tag == "title":
            self.in_title = False
        if tag == "article" and self.article_depth:
            self.article_depth -= 1
        if tag == "main" and self.main_depth:
            self.main_depth -= 1
        if tag in BLOCK_TAGS:
            self._append_text("\n")

    def handle_data(self, data: str) -> None:
        if self.ignore_depth:
            return
        text = normalize_whitespace(data)
        if not text:
            return
        if self.in_title:
            self.title_parts.append(text)
        self._append_text(text)

    def _append_text(self, text: str) -> None:
        if self.article_depth:
            self.article_chunks.append(text)
        elif self.main_depth:
            self.main_chunks.append(text)
        self.all_chunks.append(text)

    def result(self) -> tuple[str, str | None, str]:
        title = normalize_whitespace(" ".join(self.title_parts)) or "Untitled"
        article_text = cleanup_text("".join(self.article_chunks))
        main_text = cleanup_text("".join(self.main_chunks))
        full_text = cleanup_text("".join(self.all_chunks))
        body = article_text if len(article_text) >= 180 else main_text if len(main_text) >= 280 else full_text
        return title, self.description, body


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def cleanup_text(text: str) -> str:
    lines = [normalize_whitespace(line) for line in text.splitlines()]
    compact = [line for line in lines if line]
    return "\n\n".join(compact)


def slugify_segment(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower()).strip("-")
    return cleaned or "index"


def output_path_for_url(output_dir: Path, page_url: str) -> Path:
    parsed = urllib.parse.urlparse(page_url)
    parts = [slugify_segment(parsed.netloc)]
    path_segments = [segment for segment in parsed.path.split("/") if segment]
    if not path_segments:
        path_segments = ["index"]

    stem_segments = path_segments[:-1]
    leaf = path_segments[-1]
    if leaf.lower().endswith((".html", ".htm", ".md", ".txt")):
        leaf = leaf.rsplit(".", 1)[0]

    for segment in stem_segments:
        parts.append(slugify_segment(segment))

    filename = f"{slugify_segment(leaf)}.md"
    return output_dir.joinpath("pages", *parts, filename)


def should_keep_url(url: str, include_substrings: list[str], exclude_substrings: list[str]) -> bool:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False
    if not is_public_hostname(parsed.hostname):
        return False
    if include_substrings and not any(token in url for token in include_substrings):
        return False
    if exclude_substrings and any(token in url for token in exclude_substrings):
        return False
    return True


def unique_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


@dataclass
class ScrapeResult:
    url: str
    status: str
    output_file: str | None = None
    title: str | None = None
    error: str | None = None


def scrape_page(page_url: str, timeout: float, user_agent: str) -> tuple[str, str | None, str]:
    html_text, error = fetch_text(page_url, timeout=timeout, user_agent=user_agent)
    if html_text is None:
        raise RuntimeError(error or "unknown fetch error")

    parser = ReadableHTMLExtractor()
    parser.feed(html_text)
    title, description, body = parser.result()
    if len(body) < 80:
        raise RuntimeError("extracted content is too small; page may be client-rendered or non-article")
    return title, description, body


def write_markdown(output_path: Path, page_url: str, title: str, description: str | None, body: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {title}",
        "",
        f"- Source: {page_url}",
        f"- Scraped At: {datetime.now(timezone.utc).isoformat()}",
    ]
    if description:
        lines.extend(["", f"Description: {description}"])
    lines.extend(["", body, ""])
    output_path.write_text("\n".join(lines), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sitemap-url", required=True, help="The sitemap XML URL to scrape")
    parser.add_argument("--output-dir", required=True, help="Directory where scraped files will be written")
    parser.add_argument("--timeout", type=float, default=20.0, help="Per-request timeout in seconds")
    parser.add_argument("--delay-seconds", type=float, default=0.0, help="Sleep between page requests")
    parser.add_argument("--limit", type=int, default=0, help="Maximum number of pages to scrape, 0 means no limit")
    parser.add_argument(
        "--include-substring",
        action="append",
        default=[],
        help="Keep only URLs containing this substring; may be repeated",
    )
    parser.add_argument(
        "--exclude-substring",
        action="append",
        default=[],
        help="Skip URLs containing this substring; may be repeated",
    )
    parser.add_argument(
        "--user-agent",
        default="CodexSitemapScraper/1.0",
        help="User-Agent header to send with requests",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        sitemap_url = normalize_http_url(args.sitemap_url, field_name="sitemap-url")
    except ValueError as exc:
        parser.error(str(exc))
        return 2

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        discovered_urls = gather_urls_from_sitemap(
            sitemap_url=sitemap_url,
            timeout=args.timeout,
            user_agent=args.user_agent,
        )
    except Exception as exc:
        parser.error(str(exc))
        return 2
    discovered_urls = unique_preserving_order(discovered_urls)

    filtered_urls = [
        url
        for url in discovered_urls
        if should_keep_url(
            url,
            include_substrings=args.include_substring,
            exclude_substrings=args.exclude_substring,
        )
    ]
    if args.limit > 0:
        filtered_urls = filtered_urls[: args.limit]

    results: list[ScrapeResult] = []
    for index, page_url in enumerate(filtered_urls):
        if index and args.delay_seconds > 0:
            time.sleep(args.delay_seconds)
        try:
            title, description, body = scrape_page(
                page_url=page_url,
                timeout=args.timeout,
                user_agent=args.user_agent,
            )
            output_path = output_path_for_url(output_dir, page_url)
            write_markdown(output_path, page_url, title, description, body)
            results.append(
                ScrapeResult(
                    url=page_url,
                    status="saved",
                    output_file=str(output_path),
                    title=title,
                )
            )
        except Exception as exc:
            results.append(ScrapeResult(url=page_url, status="failed", error=str(exc)))

    manifest = {
        "sitemap_url": sitemap_url,
        "requested_at": datetime.now(timezone.utc).isoformat(),
        "output_dir": str(output_dir),
        "total_urls": len(discovered_urls),
        "selected_urls": len(filtered_urls),
        "saved_pages": sum(1 for result in results if result.status == "saved"),
        "failed_pages": sum(1 for result in results if result.status == "failed"),
        "results": [result.__dict__ for result in results],
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    json.dump(manifest, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
