#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
format_helpers.py — 生成符合语雀渲染习惯的Markdown片段。

语雀完整支持CommonMark+GFM,并扩展了:
  * 字号/颜色:  <font color="#FF0000" size="5">文字</font>
                 也接受  <span style="color:#xxx;font-size:20px">文字</span>
  * 警示框:     :::info / :::warning / :::danger / :::success / :::tips
  * 折叠块:     :::details 标题 ... :::
  * 数学公式:   $...$ 行内, $$...$$ 行间
  * 思维导图:   ```mind  代码块
  * 流程图:     ```mermaid 代码块
  * 标签:       #标签#

本模块只做生成与转义,不发起网络请求。可被其他脚本 import 使用,
也可作为CLI生成片段并写入文件。
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from typing import Iterable, List, Sequence

# ---------- 基础原语 ----------

CALLOUT_KINDS = {"info", "warning", "danger", "success", "tips", "note"}


def heading(text: str, level: int = 1) -> str:
    level = max(1, min(6, int(level)))
    return f"{'#' * level} {text.strip()}"


def colored(text: str, color: str = "#FF0000") -> str:
    """给文字染色。color 接受 #RRGGBB 或 CSS 颜色名。"""
    if not re.match(r"^(#[0-9A-Fa-f]{3,8}|[a-zA-Z]+)$", color):
        raise ValueError(f"非法颜色: {color}")
    return f'<font color="{color}">{html.escape(text, quote=False)}</font>'


def sized(text: str, size: str = "18px") -> str:
    """字号。语雀 <font size> 只接受1-7的等级,所以这里改用 <span style>。"""
    if not re.match(r"^\d+(px|pt|em|%)$", size):
        raise ValueError(f"非法字号: {size}, 例如 '18px' '1.2em'")
    return f'<span style="font-size:{size}">{html.escape(text, quote=False)}</span>'


def styled(text: str, *, color: str | None = None, size: str | None = None,
           bold: bool = False, italic: bool = False, underline: bool = False) -> str:
    """组合样式。生成的是 <span style="...">,语雀完整渲染。"""
    css: list[str] = []
    if color:
        css.append(f"color:{color}")
    if size:
        css.append(f"font-size:{size}")
    if bold:
        css.append("font-weight:bold")
    if italic:
        css.append("font-style:italic")
    if underline:
        css.append("text-decoration:underline")
    style = ";".join(css)
    return f'<span style="{style}">{html.escape(text, quote=False)}</span>'


def callout(content: str, kind: str = "info", title: str | None = None) -> str:
    """语雀提示框。kind ∈ info/warning/danger/success/tips/note"""
    if kind not in CALLOUT_KINDS:
        raise ValueError(f"kind 必须是 {sorted(CALLOUT_KINDS)} 之一")
    head = f":::{kind}" + (f" {title}" if title else "")
    return f"{head}\n{content.strip()}\n:::"


def collapsible(content: str, title: str = "展开查看") -> str:
    return f":::details {title}\n{content.strip()}\n:::"


def code_block(src: str, lang: str = "") -> str:
    fence = "```"
    # 若src里出现```就升到4个反引号
    while fence in src:
        fence += "`"
    return f"{fence}{lang}\n{src.rstrip()}\n{fence}"


def math_inline(expr: str) -> str:
    return f"${expr}$"


def math_block(expr: str) -> str:
    return f"$$\n{expr.strip()}\n$$"


def table(headers: Sequence[str], rows: Iterable[Sequence[str]],
          aligns: Sequence[str] | None = None) -> str:
    """生成GFM表格。aligns 元素可以是 'l' 'c' 'r'。"""
    headers = list(headers)
    rows = [list(r) for r in rows]
    if aligns is None:
        aligns = ["l"] * len(headers)
    if len(aligns) != len(headers):
        raise ValueError("aligns长度必须与headers相同")

    def _esc(c: str) -> str:
        return str(c).replace("|", "\\|").replace("\n", "<br>")

    sep_map = {"l": ":---", "c": ":---:", "r": "---:"}
    sep_line = "| " + " | ".join(sep_map[a] for a in aligns) + " |"
    out = ["| " + " | ".join(_esc(h) for h in headers) + " |", sep_line]
    for r in rows:
        if len(r) < len(headers):
            r = list(r) + [""] * (len(headers) - len(r))
        out.append("| " + " | ".join(_esc(c) for c in r) + " |")
    return "\n".join(out)


def toc_anchor(label: str, slug: str | None = None) -> str:
    """生成可在语雀目录里跳转的锚点。"""
    s = slug or re.sub(r"\s+", "-", label.strip().lower())
    return f'<a name="{s}"></a>{label}'


def mermaid(graph: str) -> str:
    return code_block(graph, "mermaid")


def mindmap(text: str) -> str:
    """语雀思维导图,代码块 lang=mind。text为缩进的层级文本。"""
    return code_block(text, "mind")


def tag(*names: str) -> str:
    return " ".join(f"#{n.strip()}#" for n in names)


# ---------- 清洗 ----------

_BAD_TAG = re.compile(r"<\s*(script|iframe|object|embed)[^>]*>.*?<\s*/\s*\1\s*>",
                      re.IGNORECASE | re.DOTALL)


def sanitize(body: str) -> str:
    """剔除语雀通常会拒绝(422)的危险HTML标签。"""
    return _BAD_TAG.sub("", body or "")


# ---------- CLI ----------

def _cli(argv=None) -> int:
    p = argparse.ArgumentParser(prog="format_helpers.py",
                                description="生成语雀Markdown格式片段")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("colored")
    s.add_argument("text"); s.add_argument("--color", default="#FF0000")

    s = sub.add_parser("sized")
    s.add_argument("text"); s.add_argument("--size", default="18px")

    s = sub.add_parser("callout")
    s.add_argument("content"); s.add_argument("--kind", default="info")
    s.add_argument("--title")

    s = sub.add_parser("table")
    s.add_argument("--headers", required=True, help="逗号分隔")
    s.add_argument("--rows", required=True,
                   help="行用|分隔,列用,分隔,例如 'a,b|c,d'")
    s.add_argument("--aligns", help="逗号分隔的 l/c/r")

    s = sub.add_parser("heading")
    s.add_argument("text"); s.add_argument("--level", type=int, default=1)

    args = p.parse_args(argv)
    if args.cmd == "colored":
        out = colored(args.text, args.color)
    elif args.cmd == "sized":
        out = sized(args.text, args.size)
    elif args.cmd == "callout":
        out = callout(args.content, args.kind, args.title)
    elif args.cmd == "heading":
        out = heading(args.text, args.level)
    elif args.cmd == "table":
        headers = [h.strip() for h in args.headers.split(",")]
        rows = [[c.strip() for c in row.split(",")] for row in args.rows.split("|")]
        aligns = [a.strip() for a in args.aligns.split(",")] if args.aligns else None
        out = table(headers, rows, aligns)
    else:
        raise SystemExit(2)
    sys.stdout.write(out + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
