#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用文章入库脚本：md -> HTML 卡片，按日期倒序插入全文库（最新在顶）。

用法:
    python add_to_library.py <文章.md路径> [--lib <全文库.html路径>]

- 全文库默认位于文章目录的上级目录，名为「文章全文库.html」，不存在自动创建。
- 文章须带 YAML frontmatter（title / date），title 为编号（如 a262）。
- 卡片插入位置：第一个 <details class="article-card"> 之前（倒序库）；若库内无卡片则追加到 </body> 前。
"""
import html
import re
import sys
from pathlib import Path


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta, text[m.end():] if m else text


def md_to_html(md):
    """极简转换：标题/加粗/段落。不支持列表项（并列要点请写成行内加粗+分号）。"""
    out = []
    for block in re.split(r"\n\s*\n", md.strip()):
        block = block.strip()
        if not block:
            continue
        if block.startswith("### "):
            out.append("<h3>%s</h3>" % html.escape(block[4:]))
        elif block.startswith("## "):
            out.append("<h2>%s</h2>" % html.escape(block[3:]))
        elif block.startswith("# "):
            out.append("<h1>%s</h1>" % html.escape(block[2:]))
        else:
            block = html.escape(block).replace("\n", "<br>")
            block = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", block)
            out.append("<p>%s</p>" % block)
    return "\n".join(out)


def build_card(num, title, date, body_html):
    return (
        '<details class="article-card" open>\n'
        "<summary><span class=\"num\">%s</span> %s "
        "<span class=\"date-tag\">%s</span></summary>\n"
        '<div class="card-body">\n%s\n'
        "</div>\n</details>\n" % (html.escape(num), html.escape(title), html.escape(date), body_html)
    )


def main():
    if len(sys.argv) < 2:
        print("用法: python add_to_library.py <文章.md路径> [--lib <全文库.html>]")
        sys.exit(2)
    src = Path(sys.argv[1]).resolve()
    if not src.exists():
        print("找不到文章: %s" % src)
        sys.exit(1)
    lib = None
    if "--lib" in sys.argv:
        lib = Path(sys.argv[sys.argv.index("--lib") + 1]).resolve()
    else:
        lib = src.parent.parent / "文章全文库.html"

    # utf-8-sig：自动吃掉 BOM，否则 frontmatter 匹配失败
    text = src.read_text(encoding="utf-8-sig")
    meta, body = parse_frontmatter(text)
    num = meta.get("title", src.stem)
    date = meta.get("date", "")
    h1 = re.search(r"^# (.+)$", body, re.M)
    title = h1.group(1).strip() if h1 else num

    card = build_card(num, title, date, md_to_html(body))

    if lib.exists():
        libtext = lib.read_text(encoding="utf-8")
    else:
        libtext = (
            "<!DOCTYPE html>\n<html lang=\"zh\">\n<head><meta charset=\"utf-8\">"
            "<title>文章全文库</title></head>\n<body>\n<h1>文章全文库（共 0 篇）</h1>\n</body>\n</html>\n"
        )

    # 倒序插入：第一个卡片之前；无卡片则 </body> 前
    if '<details class="article-card"' in libtext:
        libtext = libtext.replace('<details class="article-card"', card + '<details class="article-card"', 1)
    else:
        libtext = libtext.replace("</body>", card + "</body>")

    # 更新计数
    count = libtext.count('<details class="article-card"')
    libtext = re.sub(r"共 \d+ 篇", "共 %d 篇" % count, libtext)

    lib.write_text(libtext, encoding="utf-8")
    print("已入库: %s -> %s（共 %d 篇，倒序=最新在顶）" % (src.name, lib.name, count))


if __name__ == "__main__":
    main()
