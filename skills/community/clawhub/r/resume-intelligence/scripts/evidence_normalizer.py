#!/usr/bin/env python3
"""Render structured evidence JSON as Markdown evidence tables."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


FIELD_NAMES = [
    "claim",
    "evidence_reference",
    "confidence",
    "disclosure_level",
    "resume_use",
]


def load_records(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        return data["records"]
    if isinstance(data, dict) and isinstance(data.get("evidence"), list):
        return data["evidence"]
    raise ValueError("Expected a JSON list or an object with a records/evidence list.")


def escape_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()


def render_markdown(records: list[dict[str, Any]]) -> str:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[str(record.get("source_context_id") or "unknown-source")].append(record)

    lines = [
        "# Evidence",
        "",
        "Generated from structured evidence records. Review confidence, disclosure, and resume-use fields before final resume wording.",
    ]

    for source_context_id in sorted(grouped):
        lines.extend(
            [
                "",
                f"## {source_context_id}",
                "",
                "| Claim | Evidence Reference | Confidence | Disclosure Level | Resume Use |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for record in grouped[source_context_id]:
            cells = [escape_cell(record.get(field_name, "")) for field_name in FIELD_NAMES]
            lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", help="Structured evidence JSON file.")
    parser.add_argument("--output", help="Markdown output path. Defaults to stdout.")
    args = parser.parse_args()

    markdown = render_markdown(load_records(Path(args.input_json)))
    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
