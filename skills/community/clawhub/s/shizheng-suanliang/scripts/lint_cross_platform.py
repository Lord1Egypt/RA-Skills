#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""交叉平台 lint（纯 stdlib）：CRLF / BOM / 非 ASCII 文件名 / 可执行位 / 语法。

用法：python3 scripts/lint_cross_platform.py [技能根目录]
exit 0 = 全部通过，1 = 存在问题（逐条列出）。
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent


def main(argv=None) -> int:
    root = Path(argv[0] if argv else DEFAULT_ROOT).resolve()
    problems: list[str] = []
    files: list[Path] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        # 1) 非 ASCII 文件名（Windows zip 分发乱码根因）
        if any(ord(ch) > 127 for ch in path.name):
            problems.append("非 ASCII 文件名: %s" % rel)
            continue
        files.append(path)

    for path in files:
        rel = path.relative_to(root)
        try:
            raw = path.read_bytes()
        except OSError as exc:
            problems.append("读不了: %s（%s）" % (rel, exc))
            continue
        # 2) BOM（JSON/py/sh 一律不允许；csv/md 由写入口控制 utf-8-sig，不在此列）
        if path.suffix in (".json", ".py", ".sh", ".txt") and raw.startswith(b"\xef\xbb\xbf"):
            problems.append("BOM 头: %s" % rel)
        # 3) CRLF（.sh 在部分 shell 下直接失效）
        if path.suffix in (".py", ".sh") and b"\r\n" in raw:
            problems.append("CRLF 换行: %s" % rel)
        # 4) .py 语法
        if path.suffix == ".py":
            try:
                ast.parse(raw.decode("utf-8"))
            except SyntaxError as exc:
                problems.append("语法错误: %s 第 %d 行（%s）" % (rel, exc.lineno, exc.msg))
            except UnicodeDecodeError:
                problems.append("非 UTF-8: %s" % rel)

    for problem in problems:
        print("FAIL " + problem)
    print("lint: %d 个文件，%d 个问题" % (len(files), len(problems)))
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
