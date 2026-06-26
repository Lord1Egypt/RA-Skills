#!/usr/bin/env python3
"""
Scaffold a workflow JSON file for the work-style-memory skill.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from workflow_engine import slugify


def build_template(name: str) -> dict:
    workflow_id = slugify(name)
    return {
        "id": workflow_id,
        "name": name,
        "summary": "Describe the repeated task this workflow should handle.",
        "match": {
            "keywords": [],
        },
        "steps": [
            {
                "id": "step-1",
                "title": "First step",
                "instruction": "Describe the first meaningful action.",
            }
        ],
        "tool_preferences": [],
        "version": 1,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a starter workflow JSON file.")
    parser.add_argument("name", help="Human-readable workflow name")
    parser.add_argument(
        "--dir",
        default=".",
        help="Destination directory for the workflow file",
    )
    args = parser.parse_args()

    output_dir = Path(args.dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    template = build_template(args.name)
    output_path = output_dir / f"{template['id']}.json"
    output_path.write_text(json.dumps(template, indent=2) + "\n", encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
