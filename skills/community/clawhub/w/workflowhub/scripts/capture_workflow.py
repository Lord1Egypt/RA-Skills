#!/usr/bin/env python3
"""
Generate a workflow draft from a real task description.
"""

from __future__ import annotations

import argparse
import json

from workflow_engine import capture_workflow, normalize_tools


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture a workflow draft from a task description.")
    parser.add_argument("task", help="Task description")
    parser.add_argument("--steps", default="", help="Multi-line step text")
    parser.add_argument("--tools", default="", help="Comma-separated tools")
    args = parser.parse_args()

    workflow = capture_workflow(
        args.task,
        raw_steps=args.steps,
        tools=normalize_tools(args.tools.split(",") if args.tools else []),
    )
    print(json.dumps(workflow, indent=2))


if __name__ == "__main__":
    main()
