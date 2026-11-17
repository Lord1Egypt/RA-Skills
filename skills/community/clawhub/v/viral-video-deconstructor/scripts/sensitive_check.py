#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sensitive_check.py — 纯标准库敏感词/限流风险词扫描器

用法：
  python sensitive_check.py <文本文件> [--dict sensitive_words.txt]
  echo "文案" | python sensitive_check.py -            # 从 stdin 读
  python sensitive_check.py "单条文案字符串"            # 直接传字符串

输出：命中词、所在行号、列号区间、建议替换；结尾给出命中计数。
返回码：0 = 无命中；1 = 有命中（便于在合规闸门里做条件判断）。
"""
import sys
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DICT = os.path.join(HERE, "..", "references", "sensitive_words.txt")


def load_dict(path):
    """读取词库：每行 '原词 => 建议' 或 '原词'。# 开头为注释。
    'SAFE:原词=后续串' 定义安全上下文：命中后紧接该串则视为误报豁免。"""
    rules = []
    safe_cont = {}
    if not os.path.exists(path):
        return rules, safe_cont
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if s.startswith("SAFE:"):
                # 格式 SAFE:原词=后续串
                body = s[len("SAFE:"):]
                if "=" in body:
                    w, follow = body.split("=", 1)
                    w = w.strip()
                    if w:
                        safe_cont.setdefault(w, []).append(follow)
                continue
            if "=>" in s:
                word, sugg = s.split("=>", 1)
                rules.append((word.strip(), sugg.strip()))
            else:
                rules.append((s, ""))
    return rules, safe_cont


def scan(text, rules, safe_cont=None):
    """逐行扫描，返回命中列表 [{line, col_start, col_end, word, sugg}]。
    safe_cont: {原词: [后续串...]}，命中后紧接该串则跳过（误报豁免）。"""
    safe_cont = safe_cont or {}
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for word, sugg in rules:
            if not word:
                continue
            for m in re.finditer(re.escape(word), line):
                end = m.end()
                follows = line[end:end + 8]  # 取后续若干字符判断安全上下文
                if any(follows.startswith(f) for f in safe_cont.get(word, [])):
                    continue
                hits.append({
                    "line": i,
                    "col_start": m.start() + 1,
                    "col_end": end + 1,
                    "word": word,
                    "sugg": sugg,
                })
    return hits


def main(argv):
    args = list(argv)
    dict_path = DEFAULT_DICT
    text = None

    # 解析 --dict
    if "--dict" in args:
        idx = args.index("--dict")
        dict_path = args[idx + 1]
        del args[idx:idx + 2]

    if not args:
        print("用法: python sensitive_check.py <文件|字符串|-|文本> [--dict 词库]", file=sys.stderr)
        return 2

    arg = args[0]
    if arg == "-":
        text = sys.stdin.read()
    elif os.path.exists(arg) and os.path.isfile(arg):
        with open(arg, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = arg  # 当作直接传入的字符串

    rules, safe_cont = load_dict(dict_path)
    if not rules:
        print(f"[警告] 词库未找到或为空：{dict_path}", file=sys.stderr)
    hits = scan(text, rules, safe_cont)

    if not hits:
        print("✅ 敏感词扫描：0 命中")
        return 0

    print(f"⚠️ 敏感词扫描：{len(hits)} 处命中\n")
    # 去重展示（同词只列一次建议）
    seen = {}
    for h in hits:
        print(f"  L{h['line']}:{h['col_start']}-{h['col_end']}  命中「{h['word']}」"
              + (f"  → 建议：{h['sugg']}" if h['sugg'] else "  → 删除/彻底改写"))
        if h["word"] not in seen:
            seen[h["word"]] = h["sugg"]
    print(f"\n命中词汇总（{len(seen)} 类）：")
    for w, s in seen.items():
        print(f"  - {w}" + (f" => {s}" if s else " => 删除/彻底改写"))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
