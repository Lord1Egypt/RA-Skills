#!/usr/bin/env python3
"""Render a compact execution brief from a workflow JSON file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from workflow_engine import render_execution_brief


def load_json(path: str) -> dict:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a workflow execution brief.")
    parser.add_argument("workflow", help="Path to the workflow JSON file")
    parser.add_argument("--task", default="", help="Optional current task description")
    args = parser.parse_args()

    workflow = load_json(args.workflow)
    print(render_execution_brief(workflow, task=args.task), end="")


if __name__ == "__main__":
    main()
