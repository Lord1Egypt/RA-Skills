#!/usr/bin/env python3
"""Build batch markdown from a JSONL of per-title Tavily/fetch results."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def line_to_block(obj: dict) -> str:
    dedup_id = obj.get("dedup_id", "")
    title = obj.get("input_title", "").strip()
    arxiv_url = (obj.get("arxiv_url") or "").strip()
    fetch = obj.get("fetch") or {}
    abstract = ""
    if isinstance(fetch, dict):
        abstract = (fetch.get("abstract") or "").strip()

    return "\n".join(
        [
            f"### {dedup_id}. {title}",
            f"- arXiv URL: {arxiv_url}",
            f"- Abstract: {abstract}",
            "",
        ]
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            "Usage: python3 jsonl_to_abstract_batch_md.py <input.jsonl> <output.md>",
            file=sys.stderr,
        )
        return 1

    src = Path(argv[0])
    dst = Path(argv[1])

    parts = ["# Paper Abstract Retrieval", "", "## Results", ""]
    for raw in src.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        parts.append(line_to_block(json.loads(raw)))

    dst.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
