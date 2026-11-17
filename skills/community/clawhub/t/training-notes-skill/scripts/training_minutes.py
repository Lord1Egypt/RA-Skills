#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""培训纪要结构化 - 离线生成脚本。

输入培训转写/纪要素材，按标题/段落切分章节，抽取要点，并基于要点生成
自测题，输出带目录的培训手册 Markdown。

纯标准库实现，零第三方依赖。支撑 training-notes-skill 的"可独立运行"。
"""

import argparse
import os
import re
import sys
from datetime import date


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def split_chapters(text):
    """按 '#' 标题或空行分段切分章节，返回 [(标题, 要点行列表)]。"""
    chapters = []
    title = "第一章（未命名）"
    buf = []
    for line in text.splitlines():
        m = re.match(r"^#{1,3}\s+(.*)$", line)
        if m:
            if buf:
                chapters.append((title, buf))
            title = m.group(1).strip()
            buf = []
        else:
            s = line.strip()
            if s:
                buf.append(s)
    if buf:
        chapters.append((title, buf))
    return chapters


def extract_key_points(lines):
    """提取要点：列表项、加粗句、含冒号的短句。"""
    points = []
    for s in lines:
        if re.match(r"^[-*]\s+", s) or re.match(r"^\d+[.、]\s+", s):
            points.append(re.sub(r"^([-*]|\d+[.、])\s*", "", s))
        elif s.startswith("**") and s.endswith("**"):
            points.append(s.strip("*"))
        elif "：" in s and len(s) < 60:
            points.append(s)
    # 去重保序
    seen, out = set(), []
    for p in points:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out[:6]


def make_quiz(points):
    """基于要点生成 2 道自测题（启发式）。"""
    qs = []
    if points:
        p0 = points[0]
        kw = re.split(r"[，。：:、]", p0)[0]
        qs.append(f"（简答）本章提到的「{kw}」具体指什么？请用自己的话说明。")
    if len(points) > 1:
        p1 = points[1]
        short = re.split(r"[，。、：:]", p1)[0][:18]
        qs.append(f"（简答）为什么要关注「{short}」？它解决了什么问题？")
    if not qs:
        qs.append("（简答）请简述本章的核心内容。")
    return qs


def render(title, chapters):
    lines = [f"# {title}", ""]
    lines.append("## 目录")
    for i, (t, _) in enumerate(chapters, 1):
        lines.append(f"{i}. {t}")
    lines.append("")
    for i, (t, body) in enumerate(chapters, 1):
        lines.append(f"## 第{i}章 {t}")
        lines.append("### 要点")
        pts = extract_key_points(body)
        for p in pts:
            lines.append(f"- {p}")
        lines.append("### 自测题")
        for q in make_quiz(pts):
            lines.append(f"{q}")
        lines.append("")
    lines.append("> 本手册由 training-notes-skill 离线生成，自测题为复习引导，正式考核请人工审校。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="培训纪要结构化")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default="培训手册.md")
    ap.add_argument("--title", default=f"培训手册 · {date.today()}")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"错误：文件不存在 {args.input}", file=sys.stderr)
        sys.exit(1)

    text = read_text(args.input)
    chapters = split_chapters(text)
    if not chapters:
        print("错误：未能切分出章节，请检查输入格式", file=sys.stderr)
        sys.exit(1)
    out = render(args.title, chapters)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"已生成培训手册：{args.output}（{len(chapters)} 章）")


if __name__ == "__main__":
    main()
