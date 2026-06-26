#!/usr/bin/env python3
import argparse
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
LEDGER = REFERENCES / "feedback-ledger.md"
QUALITY_GATES = REFERENCES / "quality-gates.md"
WORKFLOW = REFERENCES / "workflow.md"


def append_once(path: Path, marker: str, content: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return False
    path.write_text(text.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
    return True


def append_under_heading(path: Path, heading: str, content: str) -> None:
    text = path.read_text(encoding="utf-8")
    if heading not in text:
        path.write_text(text.rstrip() + "\n\n" + heading + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return
    prefix, suffix = text.split(heading, 1)
    path.write_text(prefix + heading + suffix.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def insert_before_heading_once(path: Path, marker: str, heading: str, content: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return False
    if heading not in text:
        path.write_text(text.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")
        return True
    before, after = text.split(heading, 1)
    path.write_text(before.rstrip() + "\n" + content.strip() + "\n\n" + heading + after, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Record user subtitle feedback and optionally update reusable gates.")
    parser.add_argument("--issue", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--fix", required=True)
    parser.add_argument("--video", default="")
    parser.add_argument("--timestamp", default="")
    parser.add_argument("--cause", default="")
    parser.add_argument("--reusable", choices=["yes", "no"], default="yes")
    args = parser.parse_args()

    entry = f"""
### {date.today().isoformat()} - {args.category} - {args.issue}

Date: {date.today().isoformat()}
Video/output: {args.video or "not specified"}
Timestamp: {args.timestamp or "not specified"}
Category: {args.category}
User issue: {args.issue}
Confirmed cause: {args.cause or "to be confirmed during review"}
Fix applied: {args.fix}
Reusable: {args.reusable}
SOP update: {"required" if args.reusable == "yes" else "not required"}
Quality gate update: {"required" if args.reusable == "yes" else "not required"}
"""
    append_under_heading(LEDGER, "## Entries", entry)
    print(f"Recorded feedback in {LEDGER}")

    if args.reusable == "yes":
        marker = f"Feedback gate: {args.category} - {args.issue}"
        gate = f"| <!-- {marker} --> {args.category}: {args.issue} | Same or similar user-visible subtitle problem appears during review | {args.fix} |"
        workflow = f"""
<!-- Feedback workflow: {args.category} - {args.issue} -->
## Feedback Prevention: {args.category}

When this pattern appears: {args.issue}

Prevent it by: {args.fix}
"""
        gate_changed = insert_before_heading_once(QUALITY_GATES, marker, "## Adding New Gates", gate)
        workflow_changed = insert_before_heading_once(WORKFLOW, f"Feedback workflow: {args.category} - {args.issue}", "## 8. Feedback Iteration", workflow)
        print(f"Updated quality gates: {'yes' if gate_changed else 'already present'}")
        print(f"Updated workflow: {'yes' if workflow_changed else 'already present'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
