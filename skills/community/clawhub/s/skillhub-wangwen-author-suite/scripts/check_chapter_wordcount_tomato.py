#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""番茄专线字数检查：目标 2200–2800 汉字（不计空白与#标题行）。"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LO, HI = 2200, 2800


def count_zh(text: str) -> int:
    # 去掉 markdown 标题行与 HTML 注释后，统计中日韩统一表意文字粗算+所有非空白
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = []
    for line in text.splitlines():
        if line.startswith("#"):
            continue
        lines.append(line)
    body = "\n".join(lines)
    # 汉字为主；同时计入常见标点外的字
    chars = re.findall(r"[\u4e00-\u9fffA-Za-z0-9]", body)
    return len(chars)


def check_file(path: Path) -> int:
    n = count_zh(path.read_text(encoding="utf-8"))
    status = "OK"
    if n < LO:
        status = "短"
    elif n > HI:
        status = "长"
    print(f"{path}: {n} 字 [{status}] (目标 {LO}-{HI})")
    return 0 if LO <= n <= HI else 1


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("path", nargs="?", help="章节文件")
    p.add_argument("--all", metavar="DIR", help="检查目录下所有 md 章")
    args = p.parse_args()
    if args.all:
        root = Path(args.all)
        codes = [
            check_file(f)
            for f in sorted(root.glob("*.md"))
            if not f.name.startswith("00")
            and not f.name.startswith("01")
            and not f.name.startswith("02")
            and not f.name.startswith("03")
            and not f.name.startswith("000")
        ]
        return 1 if any(codes) else 0
    if not args.path:
        p.print_help()
        return 2
    return check_file(Path(args.path))


if __name__ == "__main__":
    sys.exit(main())
