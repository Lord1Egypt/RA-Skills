#!/usr/bin/env python3
"""Verify traceability HTML panels contain only existing local source paths."""

import argparse
import html
import re
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--panels",
        nargs="*",
        default=["学习记录/可查技能原文"],
        help="HTML panel file(s) or a directory containing HTML panels.",
    )
    return parser.parse_args()


def iter_panels(paths):
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            yield from sorted(path.glob("*.html"))
        elif path.is_file():
            yield path


def extract_links(text):
    return re.findall(r'href="([^"]+)"', text)


def check_panel(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    links = extract_links(text)
    issues = []
    for link in links:
        target = Path(link)
        if not target.exists():
            issues.append(f"MISSING {link}")
        elif target.stat().st_size == 0:
            issues.append(f"EMPTY {link}")
    return issues


def main():
    args = parse_args()
    panels = list(iter_panels(args.panels))
    if not panels:
        print("NO_PANELS_FOUND")
        return 1

    total_issues = 0
    for panel in panels:
        issues = check_panel(panel)
        if issues:
            total_issues += len(issues)
            print(f"PANEL {panel}")
            for issue in issues:
                print(f"  {issue}")
        else:
            print(f"OK {panel}")

    if total_issues:
        print(f"VERIFY_FAILED issues={total_issues}")
        return 1
    print(f"VERIFY_OK panels={len(panels)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
