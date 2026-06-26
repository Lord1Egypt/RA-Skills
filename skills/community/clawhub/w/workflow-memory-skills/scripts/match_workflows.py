#!/usr/bin/env python3
"""
Find the best matching workflows for a task description.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from workflow_engine import find_matches, load_workflows, normalize_tools


def main() -> None:
    parser = argparse.ArgumentParser(description="Match a task against saved workflows.")
    parser.add_argument("task", help="Task description to match")
    parser.add_argument("--dir", default=".", help="Workflow directory")
    parser.add_argument("--tools", default="", help="Comma-separated tools used in the task")
    parser.add_argument("--limit", type=int, default=3, help="Maximum matches to return")
    args = parser.parse_args()

    workflows = load_workflows(Path(args.dir).expanduser().resolve())
    tools = normalize_tools(args.tools.split(",") if args.tools else [])
    matches = find_matches(args.task, workflows, tools=tools, limit=args.limit)
    suggestion = None
    if matches and matches[0]["score"] >= 0.55:
        top = matches[0]
        suggestion = {
            "workflow_id": top["workflow_id"],
            "name": top["name"],
            "message": f'This looks similar to your "{top["name"]}" workflow. Want to reuse that SOP?',
            "score": top["score"],
        }
    print(
        json.dumps(
            {
                "task": args.task,
                "tools": tools,
                "matches": matches,
                "suggestion": suggestion,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
