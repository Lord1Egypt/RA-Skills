#!/usr/bin/env python3
"""Check generated image siblings for *.image.genai prompt files."""

from __future__ import annotations

import argparse
from pathlib import Path


EXPECTED_SUFFIXES = (".svg", ".png", ".webp")
SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
}


def iter_prompt_files(root: Path) -> list[Path]:
    prompts: list[Path] = []
    for path in root.rglob("*.image.genai"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        prompts.append(path)
    return sorted(prompts)


def sibling_paths(prompt: Path) -> list[Path]:
    if not prompt.name.endswith(".image.genai"):
        return []
    stem = prompt.name.removesuffix(".image.genai")
    return [prompt.with_name(f"{stem}{suffix}") for suffix in EXPECTED_SUFFIXES]


def check(root: Path) -> int:
    missing: list[tuple[Path, Path]] = []
    stale: list[tuple[Path, Path]] = []
    prompts = iter_prompt_files(root)

    for prompt in prompts:
        prompt_mtime = prompt.stat().st_mtime
        for sibling in sibling_paths(prompt):
            if not sibling.exists():
                missing.append((prompt, sibling))
            elif sibling.stat().st_mtime < prompt_mtime:
                stale.append((prompt, sibling))

    if not prompts:
        print("No *.image.genai prompt files found.")
        return 0

    if not missing and not stale:
        print(f"All Images generated for {len(prompts)} prompt file(s).")
        return 0

    if missing:
        print("Missing generated image siblings:")
        for prompt, sibling in missing:
            print(f"- {prompt.relative_to(root)} -> {sibling.relative_to(root)}")

    if stale:
        print("Generated image siblings older than their prompt:")
        for prompt, sibling in stale:
            print(f"- {prompt.relative_to(root)} -> {sibling.relative_to(root)}")

    return 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check that every *.image.genai prompt has fresh .svg, .png, and .webp siblings.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Workspace or repository root to scan. Defaults to the current directory.",
    )
    args = parser.parse_args()
    raise SystemExit(check(Path(args.root).resolve()))


if __name__ == "__main__":
    main()
