#!/usr/bin/env python3
"""Recherche un ticker/nom sur ZoneBourse et retourne les slugs."""

import subprocess, json, re, sys

def search_slug(query: str) -> list[str]:
    result = subprocess.run([
        "curl", "-s", "-X", "POST",
        "https://www.zonebourse.com/async/search/quick",
        "-H", "Content-Type: application/x-www-form-urlencoded; charset=UTF-8",
        "-H", "X-Requested-With: XMLHttpRequest",
        "--data-raw", f"search={query}"
    ], capture_output=True, text=True, timeout=15)

    raw = result.stdout

    # Le HTML dans le JSON est échappé en Unicode (\u003C -> < etc.)
    resp = json.loads(raw)
    html = resp.get("data", "")
    html = html.replace('\\u003C', '<').replace('\\u003E', '>').replace('\\u0022', '"').replace('\\n', '\n').replace('\\/', '/')

    slugs = re.findall(r'data-href="/cours/action/([^"]+)/"', html)
    return slugs[:5]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search_slug.py <ticker|nom>")
        sys.exit(1)
    query = sys.argv[1]
    slugs = search_slug(query)
    for s in slugs:
        print(s)