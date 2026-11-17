#!/usr/bin/env python3
"""Ensure summarize's mandatory save and recommendation resources are releasable."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = (
    "SKILL.md",
    "manifest.json",
    "sutras.yaml",
    "agents/openai.yaml",
    "references/operations.md",
    "references/recommendations.md",
    "references/history-diagnostics.md",
    "references/layered-handoff.md",
    "scripts/save_handoff.py",
    "scripts/inspect_handoff.py",
)


def test_release_resources_are_tracked() -> None:
    if not (ROOT / ".git").exists():
        print("release resource test skipped: no Git metadata")
        return
    for relative in REQUIRED:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "--error-unmatch", relative],
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, f"发布缺少受跟踪依赖: {relative}"
    print("summarize release resources are tracked")


def main() -> None:
    test_release_resources_are_tracked()


if __name__ == "__main__":
    main()
