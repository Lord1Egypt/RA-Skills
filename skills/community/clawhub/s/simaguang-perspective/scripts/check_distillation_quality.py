#!/usr/bin/env python3
"""Check distilled skill packs against the distillation methodology checklist."""


try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import argparse
import re
import sys
from pathlib import Path

import project_paths


def main():
    parser = argparse.ArgumentParser(description="按蒸馏方法论清单检查蒸馏技能包。")
    parser.add_argument("--strict", action="store_true", help="fail on structural issues")
    args = parser.parse_args()

    root = project_paths.find_project_dir()
    if root is None:
        print(project_paths.project_dir_help(), file=sys.stderr)
        return 2
    files = sorted((root / "书籍蒸馏").rglob("SKILL.md"))
    issues = []
    counts = {}
    missing_boundary = []
    a2_files = []
    over_limit = []

    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        heads = re.findall(r"^##\s+[0-9一二三四五六七八九十]+[\.、]", text, re.M)
        counts[len(heads)] = counts.get(len(heads), 0) + 1
        if "A2：" in text or "A2:" in text:
            a2_files.append(str(path))
        if not re.search(r"^##\s*边界", text, re.M):
            missing_boundary.append(str(path))
        blocks = re.split(r"^##\s+(?:[0-9一二三四五六七八九十]+)[\.、]", text, flags=re.M)[1:]
        for i, block in enumerate(blocks, 1):
            for key in ("R", "I", "A1", "E", "B"):
                if not re.search(rf"\n- {key}[:：]", block):
                    issues.append(f"{path}: scale {i} missing {key}")
        if len(heads) > 14:
            over_limit.append(f"{path}: {len(heads)} scales, over default 14")

    print(f"skill files: {len(files)}")
    print(f"scale distribution: {dict(sorted(counts.items()))}")
    print(f"missing global boundary section: {len(missing_boundary)}")
    print(f"skills using legacy A2 field: {len(a2_files)}")
    print(f"structural issues: {len(issues)}")
    print(f"over default 14 scales (kept, not retroactively edited): {len(over_limit)}")
    for line in issues[:50]:
        print(line)
    for line in over_limit:
        print(line)

    if args.strict and (issues or over_limit):
        raise SystemExit(1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
