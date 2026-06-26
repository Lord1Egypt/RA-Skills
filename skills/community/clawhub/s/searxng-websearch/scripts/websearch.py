from __future__ import annotations
import argparse, json, os, sys, requests
try:
    from dotenv import load_dotenv; load_dotenv()
except ImportError:
    pass

def _get_url(override=None):
    return (override or os.environ.get("SEARXNG_URL", "http://localhost:8080")).rstrip("/")

def _search(query, url, **kw):
    params = {"q": query, "format": "json",
              "language": os.environ.get("SEARXNG_LANGUAGE", "en"), **kw}
    r = requests.get(f"{url}/search", params=params,
                     timeout=int(os.environ.get("SEARXNG_TIMEOUT", "20")),
                     headers={"User-Agent": "wsearch/1.0"})
    r.raise_for_status()
    return r.json()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--searxng-url", default=None)
    p.add_argument("--category", default="general")
    p.add_argument("--max-results", type=int, default=5)
    p.add_argument("--language", default=None)
    p.add_argument("--safe-search", type=int, default=None)
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--time-range", default=None)
    p.add_argument("--format", default="markdown",
                   choices=["markdown", "text", "json", "agent"])
    args = p.parse_args()

    url = _get_url(args.searxng_url)
    kw = {"categories": args.category, "pageno": args.page}
    if args.language:    kw["language"]    = args.language
    if args.safe_search is not None: kw["safesearch"] = args.safe_search
    if args.time_range:  kw["time_range"]  = args.time_range

    data = _search(args.query, url, **kw)
    results = data.get("results", [])[:args.max_results]

    if args.format == "json":
        print(json.dumps({"query": args.query, "results": results}, indent=2, ensure_ascii=False))
    elif args.format in ("text", "agent"):
        for i, r in enumerate(results, 1):
            print(f"[{i}] {r.get('title','')}\n    {r.get('url','')}")
            if r.get("content"): print(f"    {r['content'][:200]}")
            print()
    else:  # markdown
        print(f"## Results for: {args.query}\n")
        for i, r in enumerate(results, 1):
            print(f"### {i}. [{r.get('title','')}]({r.get('url','')})")
            if r.get("content"): print(f"> {r['content'][:300]}")
            print()

if __name__ == "__main__":
    main()
