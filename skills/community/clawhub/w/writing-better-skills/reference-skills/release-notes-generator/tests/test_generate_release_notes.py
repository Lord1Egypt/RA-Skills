#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "generate_release_notes.py"

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        input_path = tmp_path / "input.json"
        output_dir = tmp_path / "dist"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "release-notes.md"

        input_path.write_text(json.dumps({
            "version": "v1.2.3",
            "highlights": ["Added project-local context support"],
            "changes": ["Improved validator", "Added completion gate"],
            "notes": ["No breaking changes"],
        }), encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(script), str(input_path), str(output_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            return result.returncode

        text = output_path.read_text(encoding="utf-8")
        required = ["# Release Notes - v1.2.3", "## Highlights", "## Changes", "## Notes"]
        missing = [item for item in required if item not in text]
        if missing:
            print(f"FAIL: missing expected sections: {missing}")
            return 1

    print("PASS: release notes generator produced expected output")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
