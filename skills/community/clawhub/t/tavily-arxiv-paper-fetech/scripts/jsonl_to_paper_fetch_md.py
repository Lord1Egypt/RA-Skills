#!/usr/bin/env python3
"""Render a markdown report from Tavily/arXiv paper-fetch JSONL."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def render_entry(obj: dict) -> str:
    index = obj.get("index", "")
    title = obj.get("input_title", "").strip()
    status = obj.get("tavily_status", "")
    error = obj.get("tavily_error") or ""
    arxiv_url = (obj.get("arxiv_url") or "").strip()
    fetch = obj.get("fetch") or {}

    arxiv_id = ""
    resolved_title = ""
    authors = ""
    abstract = ""
    if isinstance(fetch, dict):
        arxiv_id = (fetch.get("arxiv_id") or "").strip()
        resolved_title = (fetch.get("title") or "").strip()
        author_list = fetch.get("authors") or []
        if isinstance(author_list, list):
            authors = ", ".join(author_list)
        abstract = (fetch.get("abstract") or "").strip()

    lines = [
        f"### {index}. {title}",
        f"- Status: {status}",
        f"- arXiv URL: {arxiv_url}",
        f"- arXiv ID: {arxiv_id}",
        f"- Resolved Title: {resolved_title}",
        f"- Authors: {authors}",
        f"- Abstract: {abstract}",
    ]
    if error:
        lines.append(f"- Tavily Error: {error}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "Usage: python3 jsonl_to_paper_fetch_md.py <input.jsonl> <output.md>",
            file=sys.stderr,
        )
        return 1

    src = Path(argv[0])
    dst = Path(argv[1])

    parts = ["# Tavily arXiv Paper Fetech Report", "", "## Results", ""]
    for raw in src.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        parts.append(render_entry(json.loads(raw)))

    dst.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
