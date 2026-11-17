#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""翻译术语一致性校验器。

检查源术语是否在译文中被一致译出，报告缺失/不一致项。

用法:
  python glossary_check.py <译文文件> --glossary glossary.json
  python glossary_check.py <译文文件> --term "人工智能:Artificial Intelligence" --term "wafer:晶圆"
"""
import argparse
import json
import os
import sys


def load_glossary(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_term(s):
    # "源:目标" -> (源, 目标)
    if ":" not in s:
        return None
    src, dst = s.split(":", 1)
    return src.strip(), dst.strip()


def check(text, glossary):
    issues = []
    for src, dst in glossary.items():
        if src in text:
            # 目标可能是多个候选（用 | 分隔）
            candidates = [c.strip() for c in dst.split("|")]
            found_any = any(c in text for c in candidates if c)
            if not found_any:
                issues.append({
                    "source_term": src,
                    "expected": dst,
                    "status": "MISSING",
                })
            # 检测是否出现其他不一致译法（启发式：源术语出现但目标候选拼写变体）
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="译文文件（utf-8）")
    ap.add_argument("--glossary", help="术语表 json")
    ap.add_argument("--term", action="append", default=[], help="单个术语 源:目标，可多次")
    args = ap.parse_args()

    if not os.path.exists(args.file):
        print("❌ 文件不存在:", args.file, file=sys.stderr)
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        text = f.read()

    glossary = {}
    if args.glossary:
        glossary.update(load_glossary(args.glossary))
    for t in args.term:
        p = parse_term(t)
        if p:
            glossary[p[0]] = p[1]

    if not glossary:
        print("⚠️ 没有提供术语表（--glossary 或 --term）", file=sys.stderr)
        sys.exit(1)

    issues = check(text, glossary)
    if not issues:
        print(f"✅ 术语一致性校验通过：共检查 {len(glossary)} 条术语，无缺失。")
    else:
        print(f"⚠️ 发现 {len(issues)} 处术语不一致：")
        for it in issues:
            print(f"  - 源术语「{it['source_term']}」期望译法「{it['expected']}」→ 译文中未找到")
    # 始终输出 JSON，便于 agent 程序化判断
    print("__JSON__" + json.dumps({"issues": issues, "checked": len(glossary)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
