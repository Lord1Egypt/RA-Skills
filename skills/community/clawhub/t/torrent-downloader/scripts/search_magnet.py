#!/usr/bin/env python3
"""Search magnet links - multi-source, prefers Chinese built-in subtitles, 1080P/4K"""

import sys
import json
import os
import urllib.request
import urllib.parse
import re


SOURCES = [
    {"name": "SolidTorrents", "url": "https://solidtorrents.to/api/v1/search?q={query}&sort=seeders"},
]

SUBTITLE_KEYWORDS_BUILTIN = ["中字", "内嵌", "内封", "中文字幕", "国语", "国英双语", "双语双字", "CHI", "chinese.sub"]
SUBTITLE_KEYWORDS_EXTERNAL = ["外挂", "字幕组", "SRT", "ASS", "SUB"]
RES_4K = ["2160p", "4K", "UHD", "4k"]
RES_1080 = ["1080p", "1080P", "BluRay", "BLURAY", "Blu-ray", "BDRip"]
RES_720 = ["720p", "720P"]


def score_result(title: str, prefer_4k: bool = False) -> int:
    """Score a torrent result: higher = better match."""
    s = 0
    t = title.lower()

    # Subtitle priority
    if any(kw.lower() in t for kw in SUBTITLE_KEYWORDS_BUILTIN):
        s += 100
    elif any(kw.lower() in t for kw in SUBTITLE_KEYWORDS_EXTERNAL):
        s += 50

    # Resolution priority
    if any(kw.lower() in t for kw in RES_4K):
        s += 80 if prefer_4k else 40
    elif any(kw.lower() in t for kw in RES_1080):
        s += 60 if not prefer_4k else 30
    elif any(kw.lower() in t for kw in RES_720):
        s += 10

    # Chinese title bonus
    if re.search(r'[\u4e00-\u9fff]', title):
        s += 20

    return s


def search_solidtorrents(query: str) -> list:
    encoded = urllib.parse.quote(query)
    url = f"https://solidtorrents.to/api/v1/search?q={encoded}&sort=seeders"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            results = []
            for r in data.get("results", []):
                infohash = r.get("infohash", "")
                if not infohash:
                    continue
                magnet = f"magnet:?xt=urn:btih:{infohash}&dn={urllib.parse.quote(r.get('title', ''))}"
                results.append({
                    "title": r.get("title", ""),
                    "magnet": magnet,
                    "size": r.get("size", 0),
                    "seeders": r.get("seeders", 0),
                    "leechers": r.get("leechers", 0),
                    "source": "SolidTorrents",
                })
            return results
    except Exception as e:
        print(f"SolidTorrents error: {e}", file=sys.stderr)
        return []


def format_size(size_bytes: int) -> str:
    if size_bytes >= 1024**3:
        return f"{size_bytes / 1024**3:.1f}GB"
    elif size_bytes >= 1024**2:
        return f"{size_bytes / 1024**2:.0f}MB"
    return f"{size_bytes}B"


def main():
    if len(sys.argv) < 2:
        print("Usage: search_magnet.py <query> [--prefer-4k] [--limit N]")
        sys.exit(1)

    query = sys.argv[1]
    prefer_4k = "--prefer-4k" in sys.argv
    limit = 10
    for i, arg in enumerate(sys.argv):
        if arg == "--limit" and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])

    results = search_solidtorrents(query)

    if not results:
        print(json.dumps({"results": [], "query": query, "error": "No results found"}))
        sys.exit(0)

    # Filter: minimum seeders
    results = [r for r in results if r["seeders"] >= 1]

    # Score and sort
    for r in results:
        r["score"] = score_result(r["title"], prefer_4k)
    results.sort(key=lambda x: (-x["score"], -x["seeders"]))

    results = results[:limit]

    output = {
        "query": query,
        "total": len(results),
        "results": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
