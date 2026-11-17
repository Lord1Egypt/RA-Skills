#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用自己的标准库重建 references 索引（标准目录.csv + stdno_index.json）。

用法：
    python scripts/setup.py --root "D:/你的标准库"
    python scripts/setup.py --root "D:/你的标准库" --out references

说明：
    - 遍历 root 下所有文件，用正则识别标准号（GB/AQ/TSG/JGJ/DB/...）
    - 主题(topic) 取文件所在的一级文件夹名
    - 输出到技能内 references/（默认），或 --out 指定目录
    - 不含正文抽取；需要正文检索请另行生成 corpus/index.jsonl
"""
import os
import re
import csv
import json
import argparse

# 标准号前缀（覆盖国标/行标/地标/团标常见前缀）
STD_PREFIX = (
    r"GB|GBZ|AQ|AQT|TSG|JGJ|GA|SY|MT|NB|SH|HG|YY|LD|JT|TB|DL|SL|MH|WB|CB|YB|CJ|"
    r"JTG|YS|QC|JB|GY|DA|BB|WH|EJ|HB|FZ|SN|SD|QX|CH|JR|NY|LS|SC|CECS|XF|GH|CJJ|"
    r"DB|Q/SY|Q/SH|Q/CD|NB/T|HJ|WS|T/CIS|TCEMA"
)
STD_RE = re.compile(
    r"(?<![\w])(" + STD_PREFIX + r")(?:/[TZ])?\s*\d+(?:\.\d+)?(?:[-—]\d+)?",
    re.I,
)


def guess_stdno(name):
    m = STD_RE.search(name)
    return m.group(0).replace(" ", "").upper() if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="你的标准库根目录")
    ap.add_argument("--out", default=None, help="输出目录，默认技能内 references/")
    args = ap.parse_args()

    if not os.path.isdir(args.root):
        raise SystemExit("目录不存在: %s" % args.root)

    out = args.out or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references"
    )
    os.makedirs(out, exist_ok=True)

    rows = []
    stdmap = {}
    for dp, _, fs in os.walk(args.root):
        for fn in fs:
            ext = os.path.splitext(fn)[1].lower()
            full = os.path.join(dp, fn)
            rel = os.path.relpath(full, args.root)
            base = os.path.splitext(fn)[0]
            stdno = guess_stdno(fn)
            topic = os.path.basename(dp)
            rows.append(
                {
                    "标准号": stdno,
                    "标题": base,
                    "主题": topic,
                    "格式": ext,
                    "相对路径": rel,
                }
            )
            if stdno:
                stdmap.setdefault(stdno, []).append(
                    {"rel": rel, "title": base, "ext": ext}
                )

    cat = os.path.join(out, "标准目录.csv")
    with open(cat, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["标准号", "标题", "主题", "格式", "相对路径"]
        )
        w.writeheader()
        w.writerows(rows)

    idx = os.path.join(out, "stdno_index.json")
    json.dump(stdmap, open(idx, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"已写入 {len(rows)} 条索引 -> {cat}")
    print(f"识别标准号 {len(stdmap)} 个 -> {idx}")


if __name__ == "__main__":
    main()
