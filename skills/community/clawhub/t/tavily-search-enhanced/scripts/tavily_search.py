#!/usr/bin/env python3
"""
Tavily Search - Enhanced Edition
Supports: search, news, qna, images, and context modes
"""
import argparse
import json
import os
import pathlib
import re
import sys
import urllib.request

TAVILY_SEARCH_URL = "https://api.tavily.com/search"
TAVILY_NEWS_URL = "https://api.tavily.com/news"
TAVILY_QNA_URL = "https://api.tavily.com/qna"
TAVILY_IMAGES_URL = "https://api.tavily.com/images"
TAVILY_CONTEXT_URL = "https://api.tavily.com/context"

MAX_RESULTS = 10

# ─── API Key Loader ───────────────────────────────────────────────

def load_key():
    key = os.environ.get("TAVILY_API_KEY")
    if key:
        return key.strip()

    env_path = pathlib.Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        try:
            txt = env_path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^\s*TAVILY_API_KEY\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    return v
        except Exception:
            pass
    return None


def load_search_depth():
    """Check if ADVANCED mode is preferred (better results but slower)."""
    val = os.environ.get("TAVILY_SEARCH_DEPTH", "").strip().lower()
    if val == "advanced":
        return "advanced"
    return "basic"


# ─── API Callers ────────────────────────────────────────────────

def api_post(url, payload, timeout=30):
    key = load_key()
    if not key:
        raise SystemExit(
            "Missing TAVILY_API_KEY. Set env var TAVILY_API_KEY "
            "or add it to ~/.openclaw/.env"
        )
    payload["api_key"] = key
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error: {e}")
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        raise SystemExit(f"Tavily returned non-JSON (first 300 chars):\n{body[:300]}")


def search(query, max_results=5, include_answer=False, search_depth=None, domains=None):
    depth = search_depth or load_search_depth()
    payload = {
        "query": query,
        "max_results": min(max_results, MAX_RESULTS),
        "search_depth": depth,
        "include_answer": include_answer,
        "include_images": False,
        "include_raw_content": False,
    }
    if domains:
        payload["include_domains"] = domains if isinstance(domains, list) else [domains]
    return api_post(TAVILY_SEARCH_URL, payload)


def news(query, max_results=5, days=3, include_answer=False):
    payload = {
        "query": query,
        "max_results": min(max_results, MAX_RESULTS),
        "days": days,
        "include_answer": include_answer,
    }
    return api_post(TAVILY_NEWS_URL, payload)


def qna(query, max_results=3):
    payload = {
        "query": query,
        "max_results": min(max_results, 5),
    }
    return api_post(TAVILY_QNA_URL, payload)


def images(query, max_results=5):
    payload = {
        "query": query,
        "max_results": min(max_results, 20),
    }
    return api_post(TAVILY_IMAGES_URL, payload)


def context(query, max_results=5, search_depth=None):
    depth = search_depth or load_search_depth()
    payload = {
        "query": query,
        "max_results": min(max_results, MAX_RESULTS),
        "search_depth": depth,
    }
    return api_post(TAVILY_CONTEXT_URL, payload)


# ─── Normalizers ────────────────────────────────────────────────

def _strip_results(raw, max_results):
    out = []
    for r in (raw.get("results") or [])[:max_results]:
        out.append({
            "title": r.get("title") or "",
            "url":    r.get("url")    or "",
            "content": r.get("content") or "",
            "score":  r.get("score")  or None,
        })
    return out


def normalize_search(obj, include_answer, max_results):
    out = {
        "query": obj.get("query", ""),
        "results": _strip_results(obj, max_results),
    }
    if include_answer and obj.get("answer"):
        out["answer"] = obj["answer"]
    if obj.get("response_time"):
        out["response_time_ms"] = obj["response_time"]
    return out


def normalize_news(obj, include_answer, max_results):
    out = {
        "query": obj.get("query", ""),
        "results": _strip_results(obj, max_results),
    }
    if include_answer and obj.get("answer"):
        out["answer"] = obj["answer"]
    return out


def normalize_qna(obj, max_results):
    results = []
    for r in (obj.get("results") or [])[:max_results]:
        results.append({
            "question": r.get("question") or "",
            "answer":   r.get("answer")   or "",
            "url":      r.get("url")      or "",
        })
    return {"query": obj.get("query", ""), "results": results}


def normalize_images(obj, max_results):
    results = []
    for r in (obj.get("images") or [])[:max_results]:
        results.append({
            "url":     r.get("url")      or "",
            "alt":     r.get("description") or r.get("alt") or "",
            "source":  r.get("source")   or "",
        })
    return {"query": obj.get("query", ""), "results": results}


def normalize_context(obj, max_results):
    out = {
        "query": obj.get("query", ""),
        "results": _strip_results(obj, max_results),
    }
    if obj.get("related_topics"):
        out["related_topics"] = obj["related_topics"]
    return out


# ─── Brave-compatible output ─────────────────────────────────────

def to_brave(obj):
    """Convert results to web_search-compatible format: title/url/snippet."""
    results = []
    for r in obj.get("results") or []:
        title = r.get("title") or ""
        snippet = r.get("content") or r.get("answer") or ""
        # Truncate snippet to ~300 chars for readability
        if len(snippet) > 300:
            snippet = snippet[:297] + "..."
        results.append({
            "title": title,
            "url": r.get("url") or "",
            "snippet": snippet,
        })
    out = {"query": obj.get("query", ""), "results": results}
    if "answer" in obj:
        out["answer"] = obj["answer"]
    if "related_topics" in obj:
        out["related_topics"] = obj["related_topics"]
    return out


# ─── Markdown output ─────────────────────────────────────────────

def to_markdown(obj, mode="search"):
    lines = []

    # Answer / Q&A
    if mode == "qna":
        for r in obj.get("results") or []:
            q = r.get("question", "").strip()
            a = r.get("answer", "").strip()
            url = r.get("url", "")
            if q:
                lines.append(f"**Q: {q}**")
            if a:
                lines.append(f"A: {a}")
            if url:
                lines.append(f"   🔗 {url}")
            lines.append("")
        return "\n".join(lines).strip() + "\n"

    # Answer block for search/news
    if obj.get("answer"):
        lines.append(f"> {obj['answer'].strip()}")
        lines.append("")

    # Related topics
    if obj.get("related_topics"):
        topics = ", ".join(obj["related_topics"])
        lines.append(f"**相关话题**: {topics}")
        lines.append("")

    # Image results
    if mode == "images":
        for i, r in enumerate(obj.get("results") or [], 1):
            alt = r.get("alt") or r.get("source") or ""
            lines.append(f"{i}. ![{alt}]({r['url']}) {alt}")
        return "\n".join(lines).strip() + "\n"

    # Standard results
    for i, r in enumerate(obj.get("results") or [], 1):
        title = (r.get("title") or "").strip() or r.get("url") or "(no title)"
        url = r.get("url") or ""
        snippet = (r.get("content") or "").strip()

        if "score" in r:
            score = f"[{r['score']:.3f}] "
        else:
            score = ""

        lines.append(f"**{i}. {score}{title}**")
        if url:
            lines.append(f"   {url}")
        if snippet:
            # Bold first sentence, rest as snippet
            sentences = snippet.split(". ")
            first = sentences[0]
            rest = ". ".join(sentences[1:]) if len(sentences) > 1 else ""
            lines.append(f"   *{first}.*" + (f" {rest}" if rest else ""))
        lines.append("")
    return "\n".join(lines).strip() + "\n"


# ─── Main ───────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        prog="tavily_search.py",
        description="Tavily Search - Enhanced (search/news/qna/images/context)"
    )
    ap.add_argument("--query", required=True, help="Search query (required)")
    ap.add_argument("--mode", default="search",
                    choices=["search", "news", "qna", "images", "context"],
                    help="Tavily endpoint: search | news | qna | images | context")
    ap.add_argument("--max-results", type=int, default=5,
                    help=f"Max results (1-{MAX_RESULTS}, default 5)")
    ap.add_argument("--include-answer", action="store_true",
                    help="Include AI-generated short answer (search/news only)")
    ap.add_argument("--search-depth", default=None,
                    choices=["basic", "advanced"],
                    help="Search quality: basic (faster) | advanced (better)")
    ap.add_argument("--days", type=int, default=3,
                    help="News freshness in days (mode=news, default 3)")
    ap.add_argument("--domains", nargs="+",
                    help="Restrict to domain(s), e.g. --domains reuters.com bbc.com")
    ap.add_argument("--format", default="brave",
                    choices=["raw", "brave", "md"],
                    help="Output: raw (json) | brave (title/url/snippet, default) | md (readable)")
    args = ap.parse_args()

    max_r = max(1, min(args.max_results, MAX_RESULTS))

    # Dispatch
    try:
        if args.mode == "news":
            raw = news(args.query, max_r, days=args.days,
                       include_answer=args.include_answer)
            normalized = normalize_news(raw, args.include_answer, max_r)
        elif args.mode == "qna":
            raw = qna(args.query, max_r)
            normalized = normalize_qna(raw, max_r)
        elif args.mode == "images":
            raw = images(args.query, max_r)
            normalized = normalize_images(raw, max_r)
        elif args.mode == "context":
            raw = context(args.query, max_r,
                          search_depth=args.search_depth)
            normalized = normalize_context(raw, max_r)
        else:  # search
            raw = search(args.query, max_r,
                         include_answer=args.include_answer,
                         search_depth=args.search_depth,
                         domains=args.domains)
            normalized = normalize_search(raw, args.include_answer, max_r)

    except SystemExit:
        raise
    except Exception as e:
        raise SystemExit(f"Tavily error: {e}")

    # Output
    if args.format == "md":
        sys.stdout.write(to_markdown(normalized, mode=args.mode))
    elif args.format == "brave":
        sys.stdout.write(json.dumps(to_brave(normalized), ensure_ascii=False))
        sys.stdout.write("\n")
    else:  # raw
        sys.stdout.write(json.dumps(normalized, ensure_ascii=False, indent=2))
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
