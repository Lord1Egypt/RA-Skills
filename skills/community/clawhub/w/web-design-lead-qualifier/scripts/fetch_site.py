#!/usr/bin/env python3
"""
Site fetcher for WebClient Studio Free Edition.
Tries Playwright (headless Chromium) first, falls back to requests+bs4.

Security: Resolves hostnames via DNS before fetching. Blocks private networks,
localhost, link-local addresses, and non-HTTP schemes. Re-validates after
redirects.

Usage:
    python3 fetch_site.py <url> [--no-playwright] [--timeout 15]
"""

import sys
import json
import argparse
import ipaddress
import socket
from urllib.parse import urlparse

TIMEOUT = 15
MAX_RESPONSE_SIZE = 5_000_000  # 5MB hard cap

# Private and reserved IP ranges
BLOCKED_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
    ipaddress.ip_network("0.0.0.0/8"),       # current network
    ipaddress.ip_network("100.64.0.0/10"),   # shared address space
    ipaddress.ip_network("198.18.0.0/15"),   # benchmarking
    ipaddress.ip_network("::1/128"),          # localhost IPv6
    ipaddress.ip_network("fc00::/7"),         # IPv6 unique local
    ipaddress.ip_network("fe80::/10"),        # IPv6 link-local
    ipaddress.ip_network("::ffff:0:0/96"),    # IPv4-mapped IPv6
]

BLOCKED_HOSTNAMES = {"localhost", "localhost.localdomain"}


def is_blocked_ip(addr_str):
    """Check if an IP address string falls in any blocked network."""
    try:
        addr = ipaddress.ip_address(addr_str)
        for network in BLOCKED_NETWORKS:
            if addr in network:
                return True
    except ValueError:
        pass
    return False


def resolve_and_check(hostname):
    """Resolve hostname via DNS and check all resolved IPs against blocked ranges.

    Returns (ok, error_message).
    """
    if hostname.lower() in BLOCKED_HOSTNAMES:
        return False, f"Blocked: '{hostname}' is a local address."

    # Check if hostname is already a literal IP
    try:
        addr = ipaddress.ip_address(hostname)
        if is_blocked_ip(str(addr)):
            return False, f"Blocked: '{hostname}' is a private/reserved address."
        return True, None
    except ValueError:
        pass

    # DNS resolution — check ALL resolved addresses
    try:
        results = socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror:
        # DNS resolution failed — let it fail naturally at fetch time
        # Don't block here; the fetch will produce a clear error
        return True, None

    if not results:
        return True, None

    for family, _, _, _, sockaddr in results:
        ip_str = sockaddr[0]
        if is_blocked_ip(ip_str):
            return False, f"Blocked: '{hostname}' resolves to private address {ip_str}."

    return True, None


def validate_url(url):
    """Validate that a URL is a public HTTP(S) address.

    Performs scheme check, hostname blocklist check, and DNS resolution
    to verify the target is a public address.

    Returns (parsed_url, error_message). If valid, error_message is None.
    """
    parsed = urlparse(url)

    # Only http and https schemes
    if parsed.scheme not in ("http", "https"):
        return None, f"Blocked: scheme '{parsed.scheme}' is not allowed. Only http:// and https:// are accepted."

    hostname = parsed.hostname
    if not hostname:
        return None, "Blocked: URL has no hostname."

    ok, error = resolve_and_check(hostname)
    if not ok:
        return None, error

    return parsed, None


def validate_final_url(url):
    """Re-validate a URL after redirects (e.g., final response URL)."""
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        return False
    ok, _ = resolve_and_check(hostname)
    return ok


def truncate_text(text, max_size):
    """Truncate text to max_size bytes, appending a marker if truncated."""
    encoded = text.encode("utf-8")
    if len(encoded) <= max_size:
        return text
    # Truncate at a character boundary
    truncated = encoded[:max_size].decode("utf-8", errors="ignore")
    return truncated + "\n\n[Response truncated: exceeded size limit]"


def fetch_with_playwright(url, timeout):
    """Fetch a page using Playwright headless Chromium."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.set_default_timeout(timeout * 1000)
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)  # let JS settle

            # Re-validate after any redirects
            final_url = page.url
            if not validate_final_url(final_url):
                return {"source": "none", "error": f"Blocked: redirect target resolves to a private address."}

            title = page.title()
            content = page.content()

            # Enforce size limit
            content = truncate_text(content, MAX_RESPONSE_SIZE)

            # Extract text content
            text = page.evaluate("""() => {
                const body = document.body;
                const remove = ['SCRIPT', 'STYLE', 'NAV', 'FOOTER', 'HEADER', 'NOSCRIPT'];
                const clone = body.cloneNode(true);
                remove.forEach(tag => {
                    clone.querySelectorAll(tag).forEach(el => el.remove());
                });
                return clone.innerText || '';
            }""")
            # Extract links
            links = page.evaluate("""() => {
                const anchors = Array.from(document.querySelectorAll('a[href]'));
                return anchors
                    .map(a => ({ text: a.innerText.trim().substring(0, 100), href: a.href }))
                    .filter(a => a.text && a.href && !a.href.startsWith('javascript:'));
            }""")
            return {
                "source": "playwright",
                "title": title,
                "text": truncate_text(text, MAX_RESPONSE_SIZE),
                "html": content,
                "links": links,
                "url": final_url,
            }
        finally:
            browser.close()


def fetch_with_requests(url, timeout):
    """Fallback: fetch with requests + beautifulsoup4."""
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        return {"source": "none", "error": "Neither Playwright nor requests/bs4 available. Install: pip3 install requests beautifulsoup4"}

    try:
        resp = requests.get(url, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0 (compatible; WebClientStudio/1.0)"
        }, stream=True, allow_redirects=True)
        resp.raise_for_status()
    except Exception as e:
        return {"source": "requests", "error": str(e), "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None}

    # Re-validate final URL after redirects
    if not validate_final_url(resp.url):
        return {"source": "none", "error": "Blocked: redirect target resolves to a private address."}

    # Enforce size limit on response body
    content_length = int(resp.headers.get("Content-Length", 0))
    if content_length > MAX_RESPONSE_SIZE:
        return {"source": "none", "error": f"Blocked: response too large ({content_length} bytes). Maximum is {MAX_RESPONSE_SIZE}."}

    raw = resp.content[:MAX_RESPONSE_SIZE]
    resp.close()

    soup = BeautifulSoup(raw, "html.parser")

    # Remove noise
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title else ""
    text = soup.get_text(separator="\n", strip=True)

    links = []
    for a in soup.find_all("a", href=True):
        a_text = a.get_text(strip=True)[:100]
        href = a["href"]
        if a_text and href and not href.startswith("javascript:"):
            links.append({"text": a_text, "href": href})

    return {
        "source": "requests",
        "title": title,
        "text": truncate_text(text, MAX_RESPONSE_SIZE),
        "links": links,
        "url": str(resp.url),
        "status_code": resp.status_code,
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch a public website page")
    parser.add_argument("url", help="Public HTTP(S) URL to fetch")
    parser.add_argument("--no-playwright", action="store_true", help="Skip Playwright, use requests only")
    parser.add_argument("--timeout", type=int, default=TIMEOUT, help="Request timeout in seconds")
    args = parser.parse_args()

    # Validate URL — includes DNS resolution check
    parsed, error = validate_url(args.url)
    if error:
        print(json.dumps({"source": "none", "error": error}))
        sys.exit(1)

    url = parsed.geturl()

    if not args.no_playwright:
        result = fetch_with_playwright(url, args.timeout)
        if result is not None:
            print(json.dumps(result, ensure_ascii=False))
            return

    # Fallback to requests
    result = fetch_with_requests(url, args.timeout)
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
