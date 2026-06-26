#!/usr/bin/env python3
"""
Capture or update a workflow file from a real task description.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from workflow_engine import capture_workflow, normalize_tools, slugify


def load_existing(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def merge_workflow(existing: dict, draft: dict) -> dict:
    merged = dict(existing)
    merged["name"] = draft.get("name", existing.get("name", "New Workflow"))
    merged["summary"] = draft.get("summary", existing.get("summary", ""))
    merged["match"] = {
        "keywords": draft.get("match", {}).get("keywords", existing.get("match", {}).get("keywords", []))
    }
    merged["steps"] = draft.get("steps", existing.get("steps", []))
    merged["tool_preferences"] = draft.get(
        "tool_preferences", existing.get("tool_preferences", [])
    )
    merged["version"] = int(existing.get("version", 1)) + 1
    return merged


def main() -> None:
    parser = argparse.ArgumentParser(description="Save a workflow draft to disk.")
    parser.add_argument("task", help="Task description")
    parser.add_argument("--dir", required=True, help="Workflow directory")
    parser.add_argument("--steps", default="", help="Observed steps as multi-line text")
    parser.add_argument("--tools", default="", help="Comma-separated tools")
    parser.add_argument("--name", default="", help="Optional workflow name override")
    parser.add_argument("--summary", default="", help="Optional summary override")
    parser.add_argument("--keywords", default="", help="Optional comma-separated keywords override")
    parser.add_argument("--id", default="", help="Optional workflow id override")
    parser.add_argument("--update", default="", help="Existing workflow id to update")
    args = parser.parse_args()

    output_dir = Path(args.dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    draft = capture_workflow(
        args.task,
        raw_steps=args.steps,
        tools=normalize_tools(args.tools.split(",") if args.tools else []),
    )

    if args.name.strip():
        draft["name"] = args.name.strip()
        draft["id"] = slugify(draft["name"])
    if args.summary.strip():
        draft["summary"] = args.summary.strip()
    if args.keywords.strip():
        draft["match"]["keywords"] = normalize_tools(args.keywords.split(","))
    if args.id.strip():
        draft["id"] = slugify(args.id.strip())

    if args.update.strip():
        target = output_dir / f"{slugify(args.update.strip())}.json"
        if not target.exists():
            raise SystemExit(f"Workflow not found: {target.stem}")
        existing = load_existing(target)
        workflow = merge_workflow(existing, draft)
        workflow["id"] = existing.get("id", target.stem)
        target.write_text(json.dumps(workflow, indent=2) + "\n", encoding="utf-8")
        print(target)
        return

    target = output_dir / f"{draft['id']}.json"
    target.write_text(json.dumps(draft, indent=2) + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
