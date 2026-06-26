#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


QUERY_SUFFIXES = [
    ("papers", "paper arxiv benchmark"),
    ("benchmarks", "benchmark dataset leaderboard"),
    ("repos", "github repo implementation"),
    ("docs", "official documentation evaluation metrics"),
    ("case-studies", "case study production deployment"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a first-pass search plan from a research topic."
    )
    parser.add_argument("topic", help="Research topic or paper theme.")
    parser.add_argument("-o", "--output", help="Write markdown output to file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    topic = args.topic.strip()
    output = render_plan(topic)
    if args.output:
        path = Path(args.output).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


def render_plan(topic: str) -> str:
    lines = [
        "# Search Plan Draft",
        "",
        f"Topic: {topic}",
        "",
        "## Query buckets",
        "",
    ]

    for label, suffix in QUERY_SUFFIXES:
        lines.extend(
            [
                f"### {label}",
                "",
                f"- Query: {topic} {suffix}",
                "",
            ]
        )

    lines.extend(
        [
            "## Review notes",
            "",
            "- Prefer primary papers, benchmark pages, official documentation, and original project repositories.",
            "- Treat blog posts and summaries as discovery aids, not evidence anchors.",
            "- Narrow claims if the search plan returns only partial benchmark or baseline coverage.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
