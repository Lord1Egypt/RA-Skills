#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def render_release_notes(version: str, highlights: list[str], changes: list[str], notes: list[str]) -> str:
    lines = [f"# Release Notes - {version}", "", "## Highlights"]
    lines.extend([f"- {item}" for item in highlights] or ["- No highlights provided"])
    lines.extend(["", "## Changes"])
    lines.extend([f"- {item}" for item in changes] or ["- No changes provided"])
    if notes:
        lines.extend(["", "## Notes"])
        lines.extend([f"- {item}" for item in notes])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: generate_release_notes.py <input.json> <output.md>")
        return 1

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1

    data = json.loads(input_path.read_text(encoding="utf-8"))
    version = data.get("version", "unversioned")
    highlights = data.get("highlights", [])
    changes = data.get("changes", [])
    notes = data.get("notes", [])

    if not output_path.parent.exists():
        print(f"Output directory does not exist: {output_path.parent}")
        return 2

    output_path.write_text(render_release_notes(version, highlights, changes, notes), encoding="utf-8")
    print(f"Wrote release notes to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
