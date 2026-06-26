#!/usr/bin/env python3
"""Release verification for Study Buddy."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(cmd):
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout


def main():
    skill_json = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
    clawhub_json = json.loads((ROOT / "clawhub.json").read_text(encoding="utf-8"))
    skill_md = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if skill_json["version"] != clawhub_json["version"]:
        raise SystemExit("skill.json and clawhub.json versions must match")
    if f"version: {skill_json['version']}" not in skill_md:
        raise SystemExit("SKILL.md frontmatter version must match skill.json")

    print("[verify] compiling scripts")
    run([sys.executable, "-m", "py_compile", "scripts/study-buddy.py", "scripts/visualization.py"])

    print("[verify] running command tests")
    run([sys.executable, "test/test_commands.py"])

    print("[verify] ok")


if __name__ == "__main__":
    main()
