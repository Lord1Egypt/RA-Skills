#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
estimate_pages.py — 技术标页数估算与篇幅接近度校验

用法:
  python estimate_pages.py <merged.md> [--target-pages N] [--chars-per-page 1050]

功能:
  1. 统计正文字符数（CJK 计 1，ASCII 按 0.5 计，忽略空白）
  2. 估算页数 = 字符数 / 每页字数
  3. 若给定 --target-pages，校验估算页数是否落在 目标±15% 区间
  4. 按 "第X章" / "技术要求偏离表" 拆分各章分别估算
依赖: 标准库（无第三方包）
"""
import sys
import os
import re
import argparse

CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")


def count_chars(text):
    cjk = len(CJK.findall(text))
    non_ws = re.sub(r"\s", "", text)
    non_cjk = sum(1 for ch in non_ws if not CJK.match(ch))
    return cjk + non_cjk * 0.5


def split_chapters(text):
    pat = re.compile(r"^#{1,2}\s*(第[一二三四五六七八九十]+章|技术要求偏离表).*$", re.M)
    matches = list(pat.finditer(text))
    chunks = []
    for idx, m in enumerate(matches):
        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        title = m.group(1)
        body = text[start:end]
        chunks.append((title, count_chars(body)))
    if not chunks:
        chunks = [("全文", count_chars(text))]
    return chunks


def main(argv=None):
    ap = argparse.ArgumentParser(description="技术标页数估算与篇幅档位校验")
    ap.add_argument("md", help="合并后的技术标 Markdown")
    ap.add_argument("--target-pages", type=float, default=None, help="目标页数（用户指定或 AI 推荐）")
    ap.add_argument("--chars-per-page", type=float, default=1050.0, help="每页字数基准（仿宋小四公文版式默认1050）")
    args = ap.parse_args(argv)

    if not os.path.exists(args.md):
        print("ERR -> 文件不存在: %s" % args.md)
        return 1
    with open(args.md, "r", encoding="utf-8") as f:
        text = f.read()

    total = count_chars(text)
    est = total / args.chars_per_page

    print("=" * 60)
    print("estimate_pages — 技术标页数估算")
    print("=" * 60)
    print("输入           : %s" % args.md)
    print("每页字数基准   : %.0f" % args.chars_per_page)
    print("正文字符数     : %d" % int(total))
    print("估算页数       : %.1f" % est)
    print("-" * 60)
    print("分章估算:")
    for title, c in split_chapters(text):
        print("  %-12s %8d 字  ≈ %.1f 页" % (title, int(c), c / args.chars_per_page))
    print("-" * 60)

    if args.target_pages:
        lo = args.target_pages * 0.85
        hi = args.target_pages * 1.15
        ok = lo <= est <= hi
        print("目标页数       : %.0f  (容差 ±15%% → %.0f~%.0f)" % (args.target_pages, lo, hi))
        status = "PASS ✅" if ok else ("UNDER ⚠️ 需补写" if est < lo else "OVER ⚠️ 偏多")
        print("篇幅校验       : %s" % status)
        print("=" * 60)
        return 0 if ok else 2
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
