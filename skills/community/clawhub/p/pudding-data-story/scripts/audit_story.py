#!/usr/bin/env python3
"""Audit a visual-story project for common editorial and interaction omissions."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".jsx",
    ".md",
    ".mjs",
    ".svelte",
    ".ts",
    ".tsx",
    ".vue",
}

META_COPY = {
    "this visualization shows": "Replace production commentary with the finding.",
    "this chart shows": "State the finding, not the chart's existence.",
    "push the data": "Use a concrete action label.",
    "choose a lens": "Name the dimension or comparison.",
    "same group of particles": "Do not expose implementation metaphors to readers.",
    "这里展示": "直接陈述发现，不要复述设计要求。",
    "本图展示": "直接陈述发现，不要复述图表。",
    "推动数据": "把控件改成读者能理解的具体动作。",
    "观察镜头": "说清楚读者正在比较什么。",
    "同一组粒子": "不要向读者暴露实现隐喻。",
}

CHECKS = {
    "reduced motion": re.compile(r"prefers-reduced-motion", re.I),
    "accessible labels": re.compile(r"\baria-(?:label|labelledby|describedby)\b", re.I),
    "sticky scrolly": re.compile(r"position\s*:\s*sticky", re.I),
    "source or methods": re.compile(r"\b(source|sources|method|methodology)\b|来源|方法", re.I),
}


def collect_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() in TEXT_SUFFIXES else []
    return sorted(
        path
        for path in target.rglob("*")
        if path.is_file()
        and path.suffix.lower() in TEXT_SUFFIXES
        and not any(part in {"node_modules", ".git", "dist", "build", ".next"} for part in path.parts)
    )


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit a data-story source tree for meta-copy and basic experience requirements."
    )
    parser.add_argument("target", type=Path, help="Story file or project directory")
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    if not target.exists():
        print(f"ERROR: target does not exist: {target}", file=sys.stderr)
        return 2

    files = collect_files(target)
    if not files:
        print("ERROR: no supported text story files found", file=sys.stderr)
        return 2

    combined_parts: list[str] = []
    issues: list[str] = []

    for path in files:
        content = read_text(path)
        combined_parts.append(content)
        lowered = content.casefold()
        for phrase, advice in META_COPY.items():
            if phrase.casefold() in lowered:
                rel = path.relative_to(target) if target.is_dir() else path.name
                issues.append(f"META COPY [{rel}]: {phrase!r}. {advice}")

    combined = "\n".join(combined_parts)
    missing = [label for label, pattern in CHECKS.items() if not pattern.search(combined)]

    print(f"Audited {len(files)} text file(s).")
    if issues:
        print("\nReader-copy issues:")
        for issue in issues:
            print(f"- {issue}")
    if missing:
        print("\nProject signals not found (review manually):")
        for label in missing:
            print(f"- {label}")

    if not issues and not missing:
        print("PASS: no flagged meta-copy and all baseline project signals were found.")
        return 0

    print("\nREVIEW: automated signals are prompts for human QA, not proof of story quality.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
