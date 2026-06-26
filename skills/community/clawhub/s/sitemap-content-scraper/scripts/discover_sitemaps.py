#!/usr/bin/env python3
"""
Discover sitemap files for a website from robots.txt and common sitemap paths.

This script is intended to support the sitemap-content-scraper skill by
returning a compact JSON inventory of candidate sitemaps, their type, and
sample URLs that help a human choose which content family to scrape.
"""

from __future__ import annotations

import argparse
import functools
import ipaddress
import json
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Iterable


COMMON_SITEMAP_PATHS = (
    "/sitemap.xml",
    "/sitemap_index.xml",
    "/sitemap-index.xml",
    "/sitemaps.xml",
    "/sitemap/sitemap.xml",
)


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


def normalize_site_input(raw_url: str) -> tuple[str, str, str | None]:
    raw_url = raw_url.strip()
    if not raw_url:
        raise ValueError("site_url is required")
    if "://" not in raw_url:
        raw_url = f"https://{raw_url}"

    parsed = assert_public_url(raw_url, field_name="site_url")

    site_root = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))
    path_segments = [segment for segment in parsed.path.split("/") if segment]
    requested_path = f"/{'/'.join(path_segments)}" if path_segments else "/"
    scope_hint_substring = f"/{path_segments[0]}/" if path_segments else None
    return site_root, requested_path, scope_hint_substring


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
            body = response.read().decode(charset, errors="replace")
            return body, None
    except urllib.error.HTTPError as exc:
        return None, f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return None, str(exc.reason)
    except Exception as exc:  # pragma: no cover - defensive path
        return None, str(exc)


def parse_loc_entries(xml_text: str) -> tuple[str, list[str]]:
    root = ET.fromstring(xml_text)
    tag = root.tag.rsplit("}", 1)[-1].lower()
    locs = []
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1].lower() == "loc" and element.text:
            locs.append(element.text.strip())

    if tag == "sitemapindex":
        return "index", locs
    if tag == "urlset":
        return "urlset", locs
    return "unknown", locs


def extract_robot_sitemaps(robots_text: str, site_root: str) -> list[str]:
    urls: list[str] = []
    for line in robots_text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip().lower() == "sitemap":
            candidate = value.strip()
            if candidate:
                urls.append(urllib.parse.urljoin(f"{site_root}/", candidate))
    return urls


def candidate_sitemap_urls(site_root: str) -> Iterable[str]:
    for path in COMMON_SITEMAP_PATHS:
        yield urllib.parse.urljoin(f"{site_root}/", path.lstrip("/"))


def unique_preserving_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            output.append(item)
    return output


def inspect_sitemap(url: str, timeout: float, user_agent: str, sample_size: int) -> dict:
    xml_text, error = fetch_text(url, timeout=timeout, user_agent=user_agent)
    if xml_text is None:
        return {
            "url": url,
            "kind": "unreachable",
            "entry_count": 0,
            "sample_urls": [],
            "error": error,
        }

    try:
        kind, locs = parse_loc_entries(xml_text)
    except ET.ParseError as exc:
        return {
            "url": url,
            "kind": "invalid-xml",
            "entry_count": 0,
            "sample_urls": [],
            "error": str(exc),
        }

    return {
        "url": url,
        "kind": kind,
        "entry_count": len(locs),
        "sample_urls": locs[:sample_size],
    }


def discover_sitemaps(site_url: str, timeout: float, user_agent: str, sample_size: int) -> dict:
    site_root, requested_path, scope_hint_substring = normalize_site_input(site_url)
    robots_url = urllib.parse.urljoin(f"{site_root}/", "robots.txt")
    robots_text, robots_error = fetch_text(robots_url, timeout=timeout, user_agent=user_agent)

    discovered = []
    if robots_text:
        discovered.extend(extract_robot_sitemaps(robots_text, site_root=site_root))
    discovered.extend(candidate_sitemap_urls(site_root))
    discovered = [
        url
        for url in unique_preserving_order(discovered)
        if is_public_target_url(url)
    ]

    return {
        "requested_site": site_url,
        "site_root": site_root,
        "requested_path": requested_path,
        "scope_hint_substring": scope_hint_substring,
        "robots_txt": {
            "url": robots_url,
            "status": "found" if robots_text is not None else "missing",
            "error": robots_error,
        },
        "discovered_sitemaps": [
            inspect_sitemap(url, timeout=timeout, user_agent=user_agent, sample_size=sample_size)
            for url in discovered
        ],
    }


def is_public_target_url(url: str) -> bool:
    try:
        assert_public_url(url, field_name="candidate URL")
    except ValueError:
        return False
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_url", help="Website root or any URL on the target site")
    parser.add_argument("--timeout", type=float, default=15.0, help="Per-request timeout in seconds")
    parser.add_argument(
        "--sample-size",
        type=int,
        default=5,
        help="Maximum sample URLs to include per sitemap",
    )
    parser.add_argument(
        "--user-agent",
        default="CodexSitemapDiscovery/1.0",
        help="User-Agent header to send with requests",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = discover_sitemaps(
            site_url=args.site_url,
            timeout=args.timeout,
            user_agent=args.user_agent,
            sample_size=max(1, args.sample_size),
        )
    except ValueError as exc:
        parser.error(str(exc))
        return 2

    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
