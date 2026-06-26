#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from subtitle_style import STYLE_VERSION, get_style, style_names


STYLE_RE = re.compile(r"^Style:\s*([^,]+),(.*)$")
FIELD_NAMES = [
    "Fontname",
    "Fontsize",
    "PrimaryColour",
    "SecondaryColour",
    "OutlineColour",
    "BackColour",
    "Bold",
    "Italic",
    "Underline",
    "StrikeOut",
    "ScaleX",
    "ScaleY",
    "Spacing",
    "Angle",
    "BorderStyle",
    "Outline",
    "Shadow",
    "Alignment",
    "MarginL",
    "MarginR",
    "MarginV",
    "Encoding",
]


def parse_styles(path: Path) -> dict[str, dict[str, str]]:
    styles: dict[str, dict[str, str]] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = STYLE_RE.match(line)
        if not match:
            continue
        name = match.group(1).strip()
        values = [value.strip() for value in match.group(2).split(",")]
        if len(values) != len(FIELD_NAMES):
            raise SystemExit(f"FAIL: malformed style line for {name}: expected {len(FIELD_NAMES)} fields, got {len(values)}")
        styles[name] = dict(zip(FIELD_NAMES, values))
    return styles


def expected(profile: str, style_name: str) -> dict[str, str]:
    style = get_style(profile)
    english = style_name.lower().startswith("english")
    return {
        "Fontname": style.font,
        "Fontsize": str(style.en_size if english else style.zh_size),
        "Bold": "0" if english else "-1",
        "Outline": str(max(3, style.outline - 1) if english else style.outline),
        "Shadow": str(style.shadow),
        "MarginL": "80" if english else str(style.margin_l),
        "MarginR": "80" if english else str(style.margin_r),
        "MarginV": str(style.en_margin_v if english else style.zh_margin_v),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check ASS subtitle styles against fixed skill profiles.")
    parser.add_argument("ass", type=Path)
    parser.add_argument("--style-profile", choices=style_names(), required=True)
    parser.add_argument("--require-version-comment", action="store_true")
    args = parser.parse_args()

    if not args.ass.exists():
        print(f"FAIL: missing ASS file {args.ass}")
        return 1
    text = args.ass.read_text(encoding="utf-8-sig")
    if args.require_version_comment and f"StyleVersion: {STYLE_VERSION}" not in text:
        print(f"FAIL: missing style version comment {STYLE_VERSION}")
        return 1

    styles = parse_styles(args.ass)
    names = ["Default"] if args.style_profile.startswith("zh-only") else ["Chinese", "English"]
    issues: list[str] = []
    for name in names:
        if name not in styles:
            issues.append(f"missing style {name}")
            continue
        for field, value in expected(args.style_profile, name).items():
            actual = styles[name].get(field)
            if actual != value:
                issues.append(f"{name}.{field}: expected {value}, got {actual}")
    if issues:
        print(f"FAIL: {len(issues)} subtitle style issue(s)")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"PASS: {args.ass} matches {args.style_profile}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
