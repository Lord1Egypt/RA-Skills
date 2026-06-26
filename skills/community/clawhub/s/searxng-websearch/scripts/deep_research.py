from __future__ import annotations
import argparse, os, re, sys, requests
from collections import Counter
from html import unescape
try:
    from dotenv import load_dotenv; load_dotenv()
except ImportError:
    pass
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

def _get_url(override=None):
    return (override or os.environ.get("SEARXNG_URL", "http://localhost:8080")).rstrip("/")

def _search(query, url, max_results=4):
    params = {"q": query, "format": "json",
              "language": os.environ.get("SEARXNG_LANGUAGE", "en")}
    try:
        r = requests.get(f"{url}/search", params=params,
                         timeout=int(os.environ.get("SEARXNG_TIMEOUT", "20")),
                         headers={"User-Agent": "wsearch/1.0"})
        r.raise_for_status()
        return r.json().get("results", [])[:max_results]
    except Exception as e:
        print(f"[warn] search failed for {query!r}: {e}", file=sys.stderr)
        return []

def _fetch(url, max_chars=2500):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "wsearch-fetch/1.0"})
        r.raise_for_status()
        ct = (r.headers.get("content-type") or "").lower()
        if HAS_BS4 and ("text/html" in ct or "<html" in r.text[:200].lower()):
            text = BeautifulSoup(r.text, "lxml").get_text("\n")
            text = re.sub(r"\s+", " ", unescape(text)).strip()
        else:
            text = r.text.strip()
        return text[:max_chars]
    except Exception as e:
        return f"[fetch error: {e}]"

def _domain(url):
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc
    except Exception:
        return url

def _rank(results):
    scored = []
    for r in results:
        d = _domain(r.get("url","")).lower()
        s = 0
        if "github.com" in d or "gitlab.com" in d: s += 5
        if "arxiv.org"  in d or "openreview" in d:  s += 5
        if "docs"       in d or "readthedocs" in d:  s += 4
        if "research"   in d or "paper"       in d:  s += 3
        if r.get("publishedDate"): s += 1
        if r.get("content"):       s += 1
        scored.append((s, r))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in scored]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("topic")
    p.add_argument("--searxng-url",     default=None)
    p.add_argument("--max-results",     type=int, default=4)
    p.add_argument("--fetch-top-pages", type=int, default=3)
    p.add_argument("--max-chars",       type=int, default=2500)
    p.add_argument("--output", choices=["markdown","text"], default="markdown")
    args = p.parse_args()

    url = _get_url(args.searxng_url)

    # health check
    try:
        requests.get(url, timeout=5)
    except Exception as e:
        print(f"Cannot reach SearXNG at {url!r}: {e}\n"
              "Set SEARXNG_URL in .env or pass --searxng-url <url>.")
        return 1

    subqueries = [
        args.topic,
        f"{args.topic} overview",
        f"{args.topic} technical details",
        f"{args.topic} benchmarks",
        f"{args.topic} github OR docs OR paper",
    ]

    seen, all_results = set(), []
    for q in subqueries:
        for r in _search(q, url, args.max_results):
            u = r.get("url","")
            if u not in seen:
                seen.add(u); all_results.append(r)

    ranked = _rank(all_results)
    fetched = [(r, _fetch(r["url"], args.max_chars)) for r in ranked[:args.fetch_top_pages]]

    if args.output == "text":
        print(f"Research topic: {args.topic}\n")
        for i, r in enumerate(ranked[:10], 1):
            print(f"{i}. {r.get('title','')}\n   {r.get('url','')}")
            if r.get("content"): print(f"   {r['content'][:200]}")
            print()
        for r, page in fetched:
            print("="*60)
            print(r.get("title","")); print(r.get("url",""))
            print("="*60); print(page); print()
        return 0

    # markdown
    print(f"# Deep Research: {args.topic}\n")
    print("## Queries")
    for q in subqueries: print(f"- {q}")
    print()
    print("## Top sources")
    for i, r in enumerate(ranked[:10], 1):
        print(f"### {i}. {r.get('title','')}")
        print(f"- URL: {r.get('url','')}")
        print(f"- Domain: {_domain(r.get('url',''))}")
        if r.get("content"): print(f"- Snippet: {r['content'][:200]}")
        print()
    print("## Fetched excerpts")
    for r, page in fetched:
        print(f"### {r.get('title','')}\n- {r.get('url','')}\n\n{page}\n")
    print("## Domain frequency")
    for d, c in Counter(_domain(r.get("url","")) for r in ranked[:20]).most_common():
        print(f"- {d}: {c}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
