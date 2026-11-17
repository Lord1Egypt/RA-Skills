#!/usr/bin/env python3
"""Package the skill folder as a zip archive."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path


EXCLUDE_PARTS = {
    ".git",
    ".codex",
    ".env",
    "config.toml",
    "config.json",
    "credentials.json",
    "__pycache__",
    ".pytest_cache",
    ".qianlima-skill-state",
    ".qianlima_skill_state.json",
    "dist",
}
EXCLUDE_SUFFIXES = {".pyc", ".tmp", ".DS_Store"}
EXCLUDE_PREFIXES = {
    ("docs", "superpowers"),
    ("tests", "evidence"),
    ("scripts", "evaluate_complex_query_runs.py"),
    ("tests", "complex_query_cases.json"),
    ("tests", "complex_query_prompts.json"),
    ("tests", "test_complex_query_plan.py"),
    ("tests", "test_complex_query_evaluator.py"),
    ("tests", "test_complex_query_release_gates.py"),
}


def has_excluded_prefix(path: Path) -> bool:
    return any(
        tuple(path.parts[index : index + len(prefix)]) == prefix
        for prefix in EXCLUDE_PREFIXES
        for index in range(len(path.parts) - len(prefix) + 1)
    )


def should_include(path: Path) -> bool:
    if path.is_symlink() or path.name.startswith('.env.') or path.name.endswith('.env'):
        return False
    if any(part in EXCLUDE_PARTS for part in path.parts):
        return False
    if has_excluded_prefix(path):
        return False
    return not any(path.name.endswith(suffix) for suffix in EXCLUDE_SUFFIXES)


def package(skill_dir: Path, output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(skill_dir.rglob("*")):
            if path.is_file() and should_include(path):
                zf.write(path, path.relative_to(skill_dir.parent))
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Package Qianlima bidding search skill")
    parser.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]))
    version = json.loads((Path(__file__).resolve().parents[1] / "manifest.json").read_text())["version"]
    parser.add_argument("--output", default=f"dist/qianlima-bidding-search-v{version}.zip")
    args = parser.parse_args()
    archive = package(Path(args.skill_dir).resolve(), Path(args.output).resolve())
    print(archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
