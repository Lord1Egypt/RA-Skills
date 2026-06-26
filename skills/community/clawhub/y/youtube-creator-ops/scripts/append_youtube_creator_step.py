#!/usr/bin/env python3
"""Append one publish step to a YouTube publish manifest."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

VALID_STATUSES = {"passed", "failed", "blocked"}


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_manifest(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        normalized = value.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def recompute_summary(payload: dict) -> None:
    steps = payload.get("steps", [])
    passed_steps = sum(1 for step in steps if step.get("status") == "passed")
    failed_steps = sum(1 for step in steps if step.get("status") == "failed")
    blocked_steps = sum(1 for step in steps if step.get("status") == "blocked")
    issue_keys: list[str] = []
    published_url = ""
    for step in steps:
        issue_keys.extend(step.get("issue_keys", []))
        url = str(step.get("published_url", "") or "").strip()
        if url:
            published_url = url

    payload["summary"] = {
        "status": "failed" if failed_steps else "blocked" if blocked_steps else "passed",
        "passed_steps": passed_steps,
        "failed_steps": failed_steps,
        "blocked_steps": blocked_steps,
        "published_url": published_url,
        "issue_keys": dedupe(issue_keys),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Run manifest JSON to update.")
    parser.add_argument("--step-id", required=True, help="Stable step identifier.")
    parser.add_argument("--surface", default="", help="Surface such as upload or publish.")
    parser.add_argument("--action", required=True, help="What was attempted.")
    parser.add_argument("--expected", required=True, help="Expected Studio behavior.")
    parser.add_argument("--actual", required=True, help="Observed Studio behavior.")
    parser.add_argument("--status", required=True, choices=sorted(VALID_STATUSES), help="Step status.")
    parser.add_argument("--note", default="", help="Optional extra note.")
    parser.add_argument("--issue-key", action="append", default=[], help="Repeatable issue key.")
    parser.add_argument("--screenshot", default="", help="Relative path to screenshot artifact.")
    parser.add_argument("--snapshot-json", default="", help="Relative path to snapshot artifact.")
    parser.add_argument("--console-log", default="", help="Relative path to console log.")
    parser.add_argument("--video-proof", default="", help="Relative path to video proof.")
    parser.add_argument("--published-url", default="", help="Public YouTube URL when known.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    payload = load_manifest(manifest_path)

    step_id = args.step_id.strip()
    existing_ids = {step.get("step_id") for step in payload.get("steps", [])}
    if step_id in existing_ids:
        raise SystemExit(f"Step '{step_id}' already exists in {manifest_path}")

    step = {
        "step_id": step_id,
        "captured_utc": datetime.now(timezone.utc).isoformat(),
        "surface": args.surface.strip(),
        "action": args.action.strip(),
        "expected": args.expected.strip(),
        "actual": args.actual.strip(),
        "status": args.status,
        "note": args.note.strip(),
        "issue_keys": dedupe(args.issue_key),
        "published_url": args.published_url.strip(),
        "artifacts": {
            "screenshot": args.screenshot.strip(),
            "snapshot_json": args.snapshot_json.strip(),
            "console_log": args.console_log.strip(),
            "video_proof": args.video_proof.strip(),
        },
    }

    payload.setdefault("steps", []).append(step)
    recompute_summary(payload)
    save_manifest(manifest_path, payload)
    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
