#!/usr/bin/env python3
"""Verify file:line citations in a markdown artifact resolve against the repo.

Usage: verify-citations.py <artifact.md> [repo-root]
Exit: 0 = all cites resolve, 1 = one or more unresolved, 2 = usage/IO error.
"""
import re
import sys
from pathlib import Path

# A repo-relative path of word/dot/dash segments ending in .ext, then :line.
# Lookbehind drops cites mid-word, after a scheme colon or slash (URLs), or in
# `{{...}}` template placeholders; the segment shape forbids a leading slash.
CITATION = re.compile(r"(?<![\w:/{])((?:[\w.\-]+/)*[\w.\-]+\.[A-Za-z][\w]*):(\d+)")


def main(argv):
    if not (2 <= len(argv) <= 3):
        print("usage: verify-citations.py <artifact.md> [repo-root]", file=sys.stderr)
        return 2
    artifact = Path(argv[1])
    repo_root = Path(argv[2]) if len(argv) == 3 else Path.cwd()
    try:
        text = artifact.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"cannot read artifact: {exc}", file=sys.stderr)
        return 2

    seen, failures, checked = set(), [], 0
    for match in CITATION.finditer(text):
        path, line_s = match.group(1), match.group(2)
        if (path, line_s) in seen:
            continue
        seen.add((path, line_s))
        checked += 1
        target = repo_root / path
        if not target.is_file():
            failures.append(f"{path}:{line_s} -- file not found")
            continue
        try:
            with target.open("r", encoding="utf-8", errors="replace") as fh:
                total = sum(1 for _ in fh)
        except OSError as exc:
            failures.append(f"{path}:{line_s} -- cannot read ({exc})")
            continue
        if not (1 <= int(line_s) <= total):
            failures.append(f"{path}:{line_s} -- line out of range (file has {total})")

    print(f"citations checked: {checked} | unresolved: {len(failures)}")
    for line in failures:
        print(f"  {line}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
