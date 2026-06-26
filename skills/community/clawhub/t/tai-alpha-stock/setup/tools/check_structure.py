#!/usr/bin/env python3
"""
Enforce documentation layout: Markdown and SQL under /setup only.

Root exceptions (thin stubs / marketplace): SKILL.md, AGENTS.md, CLAUDE.md.
Skips common build/venv/cache directories.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

SKIP_DIR_NAMES = frozenset(
    {
        ".git",
        ".venv",
        ".cursor",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "tai_alpha_output",
        "dist",
        "build",
        "tai_alpha_stock.egg-info",
        "__pycache__",
    }
)

ALLOWED_ROOT_MD = frozenset({"SKILL.md", "AGENTS.md", "CLAUDE.md"})


def _skip_path(rel: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in rel.parts)


def check_markdown() -> list[str]:
    errors: list[str] = []
    for p in REPO_ROOT.rglob("*.md"):
        rel = p.relative_to(REPO_ROOT)
        if _skip_path(rel):
            continue
        if rel.parts[0] == "setup":
            continue
        if len(rel.parts) == 1 and rel.name in ALLOWED_ROOT_MD:
            continue
        errors.append(f"Disallowed Markdown (move to /setup): {rel.as_posix()}")
    return errors


def check_sql() -> list[str]:
    errors: list[str] = []
    for p in REPO_ROOT.rglob("*.sql"):
        rel = p.relative_to(REPO_ROOT)
        if _skip_path(rel):
            continue
        parts = rel.parts
        if parts[0] == "setup" and "sql" in parts:
            continue
        errors.append(f"Disallowed SQL (move to /setup/sql): {rel.as_posix()}")
    return errors


def main() -> int:
    md_err = check_markdown()
    sql_err = check_sql()
    all_err = md_err + sql_err
    if all_err:
        print("Structure check failed:\n", file=sys.stderr)
        for e in all_err:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("Structure check OK (Markdown + SQL layout).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
