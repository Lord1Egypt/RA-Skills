#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qryma Search for ClawHub
A single-file search skill with multiple output formats
"""
import json
import os
import re
import sys
import urllib.request
from typing import Optional

# Backward compatibility
QRYMA_URL = "https://search.qryma.com/api/web"


def load_key() -> Optional[str]:
    """Load Qryma API key"""
    # Load from environment variable
    key = os.environ.get("QRYMA_API_KEY")
    if key:
        return key.strip()

    # Load from config file
    env_path = os.path.expanduser("~/.qryma/.env")
    if not os.path.exists(env_path):
        env_path = ".env"
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            m = re.search(r"^\s*QRYMA_API_KEY\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    return v
        except Exception:
            pass

    return None


def load_endpoint() -> str:
    """Load Qryma API endpoint"""
    # Load from environment variable
    endpoint = os.environ.get("QRYMA_ENDPOINT")
    if endpoint:
        return endpoint.strip()

    # Load from config file
    env_path = os.path.expanduser("~/.qryma/.env")
    if not os.path.exists(env_path):
        env_path = ".env"
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            m = re.search(r"^\s*QRYMA_ENDPOINT\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    return v
        except Exception:
            pass

    # Default to the old endpoint for backward compatibility
    return "https://search.qryma.com/api/web"


class QrymaSearchCore:
    """Qryma search core class"""

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        self.api_key = api_key or load_key()
        self.endpoint = endpoint or load_endpoint()

    def search(
        self,
        query: str,
        max_results: int = 5,
        lang: Optional[str] = None,
        safe: bool = False,
        mode: str = "fulltext",
    ) -> dict:
        """Execute search"""
        if not self.api_key:
            raise ValueError("QRYMA_API_KEY not found")

        # 如果没有指定语言，则自动检测
        if lang is None:
            lang = ""

        # 处理向后兼容性：如果传入布尔值，转换为对应的字符串
        if isinstance(mode, bool):
            mode = "fulltext" if mode else "snippet"

        # Backend API parameters: query, lang, safe, mode, max_results
        payload = {
            "query": query,
            "lang": lang,
            "safe": safe,
            "mode": mode,
            "max_results": max_results,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "X-Api-Key": self.api_key,
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")

        try:
            obj = json.loads(body)
        except json.JSONDecodeError as e:
            raise ValueError(f"Response parsing failed: {e}") from e

        # Format response
        out = {
            "query": query,
            "results": [],
        }
        # Process result format returned by backend
        organic_results = obj.get("organic") or []
        for r in organic_results:
            out["results"].append(
                {
                    "title": r.get("title"),
                    "url": r.get("link"),  # API returns link field
                    "content": r.get("text") or r.get("snippet"),
                }
            )

        return out


def search(
    query: str,
    max_results: int = 5,
    lang: Optional[str] = None,
    safe: bool = False,
    mode: str = "fulltext",
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> dict:
    """Execute search against Qryma API (convenience function)"""
    core = QrymaSearchCore(api_key, endpoint)
    return core.search(query, max_results, lang, safe, mode)


def to_brave_like(obj: dict) -> dict:
    """Format result like Brave search (title/url/snippet)"""
    results = []
    for r in obj.get("results", []) or []:
        results.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "content": r.get("content"),
        })
    out = {"query": obj.get("query"), "results": results}
    return out


def to_markdown(obj: dict) -> str:
    """Format result as human-readable Markdown"""
    lines = []
    for i, r in enumerate(obj.get("results", []) or [], 1):
        title = (r.get("title") or "").strip() or r.get("url") or "(no title)"
        url = r.get("url") or ""
        content = (r.get("content") or "").strip()
        lines.append(f"{i}. {title}")
        if url:
            lines.append(f"   {url}")
        if content:
            lines.append(f"   - {content}")
    return "\n".join(lines).strip() + "\n"


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Qryma Web Search")
    ap.add_argument("--api-key", help="Qryma API key")
    ap.add_argument("--query", required=True, help="Search query")
    ap.add_argument("--max-results", type=int, default=5, help="Max results (default: 5)")
    ap.add_argument("--lang", nargs="?", const="", help="Language code (auto-detect if not specified or empty) - [See available languages](https://developers.google.com/custom-search/docs/xml_results_appendices#interfaceLanguages)")
    ap.add_argument("--safe", action="store_true", help="Enable safe search (default: False)")
    ap.add_argument("--mode", default="fulltext", help="Search mode: fulltext | snippet (default: fulltext)")
    ap.add_argument(
        "--format",
        choices=["raw", "brave", "md"],
        default="md",
        help="Output format: raw | brave (title/url/snippet) | md (human-readable, default)"
    )

    args = ap.parse_args()

    res = search(
        query=args.query,
        max_results=max(1, min(args.max_results, 10)),
        lang=args.lang,
        safe=args.safe,
        mode=args.mode,
        api_key=args.api_key,
    )
    if args.format == "md":
        output = to_markdown(res)
        sys.stdout.buffer.write(output.encode('utf-8'))
        return

    if args.format == "brave":
        res = to_brave_like(res)

    json_str = json.dumps(res, ensure_ascii=False, default=str)
    sys.stdout.buffer.write(json_str.encode('utf-8'))
    sys.stdout.buffer.write(b'\n')


if __name__ == "__main__":
    main()
