#!/usr/bin/env python3
"""
factcheck.py — read-only web lookup to verify a claim before stating it.

Usage:
    python3 factcheck.py "<short neutral query>"

This script NEVER posts data, logs in, or modifies anything. It only
performs a GET request against a public search endpoint and returns
plain-text snippets + source URLs for the agent (or human) to evaluate.
"""
import sys
import re
import json
import urllib.request
import urllib.parse

BLOCKED_PATTERNS = [
    r"login", r"signin", r"account", r"password", r"private",
    r"internal\.", r"\.local\b", r"localhost", r"127\.0\.0\.1",
]

USER_AGENT = "Mozilla/5.0 (compatible; TriskillFactCheck/1.0; +https://example.invalid/bot)"


def looks_like_credential_fetch(query: str) -> bool:
    q = query.lower()
    return any(re.search(p, q) for p in BLOCKED_PATTERNS)


def search_duckduckgo_html(query: str, max_results: int = 5):
    """
    Uses DuckDuckGo's HTML-only endpoint (no JS, no API key required).
    This is a best-effort, dependency-free fallback search. It is meant
    for casual fact verification, not high-volume scraping.
    """
    url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return {"error": f"network/search error: {e}"}

    # Very small, dependency-free extraction: pull result blocks.
    # We deliberately keep this simple/fragile-but-honest rather than
    # pulling in a heavy HTML parser dependency.
    results = []
    for m in re.finditer(
        r'<a rel="nofollow" class="result__a" href="([^"]+)">(.*?)</a>.*?'
        r'<a class="result__snippet"[^>]*>(.*?)</a>',
        html,
        re.S,
    ):
        href, title_html, snippet_html = m.groups()
        title = re.sub("<[^<]+?>", "", title_html).strip()
        snippet = re.sub("<[^<]+?>", "", snippet_html).strip()
        # DuckDuckGo HTML wraps outbound links in a redirect; unwrap if present.
        real_url = href
        parsed = urllib.parse.urlparse(href)
        if parsed.path == "/l/" or "uddg=" in parsed.query:
            qs = urllib.parse.parse_qs(parsed.query)
            if "uddg" in qs:
                real_url = urllib.parse.unquote(qs["uddg"][0])
        results.append({"title": title, "url": real_url, "snippet": snippet})
        if len(results) >= max_results:
            break

    return {"query": query, "results": results}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "usage: factcheck.py \"<query>\""}))
        sys.exit(1)

    query = " ".join(sys.argv[1:]).strip()

    if not query:
        print(json.dumps({"error": "empty query"}))
        sys.exit(1)

    if looks_like_credential_fetch(query):
        print(json.dumps({
            "error": "refused: query looks like it targets private/auth-gated "
                     "content, which this read-only fact-check tool will not fetch."
        }))
        sys.exit(2)

    data = search_duckduckgo_html(query)
    print(json.dumps(data, indent=2, ensure_ascii=False))

    if "error" in data:
        sys.exit(1)


if __name__ == "__main__":
    main()
