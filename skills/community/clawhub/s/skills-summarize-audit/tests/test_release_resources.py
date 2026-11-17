#!/usr/bin/env python3
"""Ensure Audit's directly loaded resources cannot be omitted from a Git release."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = (
    "scripts/collect_codex_display_candidates.py",
    "references/display-source-map.md",
    "references/codex-ui-zh-glossary.json",
    "references/description-quality.md",
    "references/execution-flow.md",
    "references/report-template.md",
    "references/project-types.yaml",
)


def main() -> None:
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
    print("audit release resources are tracked")


if __name__ == "__main__":
    main()
