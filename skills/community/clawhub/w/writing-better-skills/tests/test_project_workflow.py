#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    return result.returncode, result.stdout, result.stderr


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    project = root / "examples" / "release-notes-project"
    generate = root / "reference-skills" / "release-notes-generator" / "scripts" / "generate_release_notes.py"
    heal = root / "reference-skills" / "release-notes-generator" / "self-healing" / "heal_output_dir.py"

    out_dir = project / "dist"
    out_file = out_dir / "release-notes.md"
    if out_dir.exists():
        shutil.rmtree(out_dir)

    code, out, err = run([sys.executable, str(generate), "data/release-input.json", "dist/release-notes.md"], project)
    if code != 2:
        print(out, end="")
        print(err, end="")
        print(f"Expected initial failure code 2 for missing output directory, got {code}")
        return 1

    code, out, err = run([sys.executable, str(heal), "dist"], project)
    if code != 0:
        print(out, end="")
        print(err, end="")
        return code

    code, out, err = run([sys.executable, str(generate), "data/release-input.json", "dist/release-notes.md"], project)
    print(out, end="")
    if code != 0:
        print(err, end="")
        return code
    if not out_file.exists():
        print("Expected generated release notes file is missing")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
