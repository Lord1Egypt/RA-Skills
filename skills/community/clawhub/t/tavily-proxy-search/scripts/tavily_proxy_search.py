#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import re
import sys
import urllib.request
import urllib.error

DEFAULT_TAVILY_PROXY_URL = "http://127.0.0.1:8080/search"


def load_env_value(name: str):
    value = os.environ.get(name)
    if value:
        return value.strip()

    env_path = pathlib.Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        try:
            txt = env_path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(rf"^\s*{re.escape(name)}\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    return v
        except Exception:
            pass

    return None


def load_proxy_url():
    return load_env_value("TAVILY_PROXY_URL") or DEFAULT_TAVILY_PROXY_URL


def load_master_key():
    return load_env_value("TAVILY_PROXY_MASTER_KEY")


def tavily_proxy_search(query: str, max_results: int, include_answer: bool, search_depth: str):
    proxy_url = load_proxy_url()
    master_key = load_master_key()
    if not master_key:
        raise SystemExit(
            "Missing TAVILY_PROXY_MASTER_KEY. Set env var TAVILY_PROXY_MASTER_KEY or add it to ~/.openclaw/.env"
        )

    payload = {
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
        "include_answer": bool(include_answer),
        "include_images": False,
        "include_raw_content": False,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        proxy_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {master_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Tavily proxy returned HTTP {e.code}: {detail[:500]}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Tavily proxy request failed: {e}")

    try:
        obj = json.loads(body)
    except json.JSONDecodeError:
        raise SystemExit(f"Tavily proxy returned non-JSON: {body[:300]}")

    out = {
        "query": query,
        "answer": obj.get("answer"),
        "results": [],
    }

    for r in (obj.get("results") or [])[:max_results]:
        out["results"].append(
            {
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content"),
            }
        )

    if not include_answer:
        out.pop("answer", None)

    return out


def to_brave_like(obj: dict) -> dict:
    results = []
    for r in obj.get("results", []) or []:
        results.append(
            {
                "title": r.get("title"),
                "url": r.get("url"),
                "snippet": r.get("content"),
            }
        )
    out = {"query": obj.get("query"), "results": results}
    if "answer" in obj:
        out["answer"] = obj.get("answer")
    return out


def to_markdown(obj: dict) -> str:
    lines = []
    if obj.get("answer"):
        lines.append(obj["answer"].strip())
        lines.append("")
    for i, r in enumerate(obj.get("results", []) or [], 1):
        title = (r.get("title") or "").strip() or r.get("url") or "(no title)"
        url = r.get("url") or ""
        snippet = (r.get("content") or "").strip()
        lines.append(f"{i}. {title}")
        if url:
            lines.append(f"   {url}")
        if snippet:
            lines.append(f"   - {snippet}")
    return "\n".join(lines).strip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--max-results", type=int, default=5)
    ap.add_argument("--include-answer", action="store_true")
    ap.add_argument(
        "--search-depth",
        default="basic",
        choices=["basic", "advanced"],
        help="Tavily search depth",
    )
    ap.add_argument(
        "--format",
        default="raw",
        choices=["raw", "brave", "md"],
        help="Output format: raw (default) | brave (title/url/snippet) | md (human-readable)",
    )
    args = ap.parse_args()

    res = tavily_proxy_search(
        query=args.query,
        max_results=max(1, min(args.max_results, 10)),
        include_answer=args.include_answer,
        search_depth=args.search_depth,
    )

    if args.format == "md":
        sys.stdout.write(to_markdown(res))
        return

    if args.format == "brave":
        res = to_brave_like(res)

    json.dump(res, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
