#!/usr/bin/env python3
"""Phase 1 helper: build audit state from workspace files.

Scans watched files, computes hashes, detects changes since last run,
and outputs a structured audit-state.json.

Usage:
  python3 scripts/build_audit_state.py [--workspace PATH] [--state PATH] [--output PATH]
"""

from __future__ import annotations

import hashlib
import json
import argparse
from datetime import UTC, date, datetime
from pathlib import Path


DEFAULT_WORKSPACE = Path.home() / ".openclaw" / "workspace"
DEFAULT_STATE = Path("memory/audits/state.json")
DEFAULT_OUTPUT = Path("memory/audits/audit-state.json")

WATCHED_PATTERNS = {
    "skills": "skills/*/SKILL.md",
    "learnings": ".learnings/*.md",
    "core_config": ["SOUL.md", "AGENTS.md", "USER.md", "TOOLS.md", "MEMORY.md", "HEARTBEAT.md"],
    "recent_memory": "memory/*.md",
}


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def collect_watched_files(workspace: Path) -> dict[str, list[Path]]:
    result: dict[str, list[Path]] = {}

    # Skills
    result["skills"] = sorted(workspace.glob("skills/*/SKILL.md"))

    # Learnings
    learnings_dir = workspace / ".learnings"
    result["learnings"] = sorted(learnings_dir.glob("*.md")) if learnings_dir.exists() else []

    # Core config
    result["core_config"] = [
        workspace / name
        for name in ["SOUL.md", "AGENTS.md", "USER.md", "TOOLS.md", "MEMORY.md", "HEARTBEAT.md"]
        if (workspace / name).exists()
    ]

    # Recent memory (last 14 days)
    memory_dir = workspace / "memory"
    if memory_dir.exists():
        cutoff = date.today().isoformat().replace("-", "")[:8]
        result["recent_memory"] = sorted([
            f for f in memory_dir.glob("*.md")
            if f.stem.replace("-", "") >= cutoff[:6]  # rough filter: same month or newer
        ])
    else:
        result["recent_memory"] = []

    return result


def build_state(
    workspace: Path,
    previous_state_path: Path | None = None,
) -> dict:
    files = collect_watched_files(workspace)
    previous: dict[str, str] = {}
    if previous_state_path and previous_state_path.exists():
        previous = json.loads(previous_state_path.read_text()).get("hashes", {})

    hashes: dict[str, str] = {}
    changed: list[str] = []
    unchanged: list[str] = []

    for category, paths in files.items():
        for path in paths:
            rel = str(path.relative_to(workspace))
            h = hash_file(path)
            hashes[rel] = h
            if previous.get(rel) != h:
                changed.append(rel)
            else:
                unchanged.append(rel)

    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "workspace": str(workspace),
        "total_files": len(hashes),
        "changed_files": changed,
        "unchanged_files": unchanged,
        "hashes": hashes,
        "categories": {cat: [str(p.relative_to(workspace)) for p in paths] for cat, paths in files.items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build audit state from workspace")
    parser.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    parser.add_argument("--state", type=Path, default=None, help="Previous state.json for change detection")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    state = build_state(args.workspace, args.state)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(state, indent=2))

    print(f"Scanned {state['total_files']} files: {len(state['changed_files'])} changed, {len(state['unchanged_files'])} unchanged")


if __name__ == "__main__":
    main()
