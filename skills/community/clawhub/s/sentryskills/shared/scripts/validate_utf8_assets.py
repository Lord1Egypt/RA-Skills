#!/usr/bin/env python3
"""Validate UTF-8 readability and basic text quality for skill assets."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable, List

TEXT_EXTS = {".md", ".json", ".py", ".txt"}
SKIP_DIRS = {"__pycache__", ".verify_project", ".git", "out", "tmp"}
POLICY_FIELDS = [
    "single_source_disclosure_title",
    "single_source_missing_hint",
    "force_uncertainty_prefix",
]

# Common mojibake signatures from mis-decoded UTF-8 bytes.
MOJIBAKE_PATTERNS = [
    re.compile(r"[\u00C2-\u00C3\u00E0-\u00EF][\u0080-\u00BF]"),
    re.compile("".join(chr(x) for x in (0x951F, 0x65A4, 0x62F7))),
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validate UTF-8 and policy text quality")
    p.add_argument("skill_dir", help="Path to skills/trinityguard-self-guard")
    p.add_argument("--strict", action="store_true", help="Fail when suspicious mojibake fragments are found")
    return p.parse_args()


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_EXTS:
            continue
        rel_parts = set(path.relative_to(root).parts)
        if rel_parts & SKIP_DIRS:
            continue
        yield path


def load_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def validate_policy_fields(path: Path, content: str) -> List[str]:
    issues: List[str] = []
    if not path.name.startswith("runtime_policy") or path.suffix.lower() != ".json":
        return issues
    data = json.loads(content)
    for key in POLICY_FIELDS:
        value = str(data.get(key, "")).strip()
        if not value:
            issues.append(f"{path}: policy field `{key}` is empty")
            continue
        if re.fullmatch(r"\?+", value):
            issues.append(f"{path}: policy field `{key}` contains placeholder question marks only")
    return issues


def has_mojibake(text: str) -> bool:
    return any(p.search(text) for p in MOJIBAKE_PATTERNS)


def main() -> None:
    args = parse_args()
    root = Path(args.skill_dir).resolve()
    if not root.exists():
        raise FileNotFoundError(f"skill dir not found: {root}")

    errors: List[str] = []
    warnings: List[str] = []

    for path in iter_text_files(root):
        try:
            text = load_utf8(path)
        except UnicodeDecodeError as exc:
            errors.append(f"{path}: utf-8 decode failed ({exc})")
            continue

        if "\ufffd" in text:
            errors.append(f"{path}: contains replacement character U+FFFD")

        if has_mojibake(text):
            msg = f"{path}: suspicious mojibake fragment detected"
            if args.strict:
                errors.append(msg)
            else:
                warnings.append(msg)

        try:
            errors.extend(validate_policy_fields(path, text))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid json ({exc})")

    for w in warnings:
        print(f"[WARN] {w}")
    for err in errors:
        print(f"[ERROR] {err}")

    if errors:
        raise SystemExit(1)
    print(f"[OK] UTF-8 gate passed: {root}")


if __name__ == "__main__":
    main()
