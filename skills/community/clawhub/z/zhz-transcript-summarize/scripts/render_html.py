#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把摘要 Markdown 渲染成可独立打开的 HTML 文件。

纯 Python 标准库实现（无 markdown 依赖），内联 CSS、无外部资源，
双击 .html 即可用浏览器打开。

用法:
    python render_html.py <summary.md|运行目录> [--title 标题] [--out summary.html] [--lang zh]

参数可传摘要 Markdown 文件，或直接传运行目录（自动找目录下的 summary.md）。
标题默认取 Markdown 中第一个一级标题，否则取文件名。
"""

import argparse
import html
import logging
import re
import sys
import time
from pathlib import Path

LOG = logging.getLogger("zhz-render-html")


def _setup_logging():
    if LOG.handlers:
        return
    LOG.setLevel(logging.INFO)
    h_out = logging.StreamHandler(sys.stdout)
    h_out.setLevel(logging.INFO)
    h_out.addFilter(lambda r: r.levelno < logging.ERROR)
    h_err = logging.StreamHandler(sys.stderr)
    h_err.setLevel(logging.ERROR)
    h_err.setFormatter(logging.Formatter("[错误] %(message)s"))
    LOG.addHandler(h_out)
    LOG.addHandler(h_err)


def _reconfigure_stdout():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def fatal(msg):
    LOG.error(msg)
    sys.exit(1)


def escape(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------------------
# 行内元素
# ---------------------------------------------------------------------------

def inline(text):
    codes = []

    def protect(m):
        codes.append(escape(m.group(1)))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`\n]+)`", protect, text)
    text = escape(text)
    # 链接
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                  lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', text)
    # 加粗
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # 斜体
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)

    def restore(m):
        return f"<code>{codes[int(m.group(1))]}</code>"

    text = re.sub(r"\x00(\d+)\x00", restore, text)
    return text


def strip_md(text):
    t = re.sub(r"`([^`]*)`", r"\1", text)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"\*([^*]+)\*", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    return t.strip()


# ---------------------------------------------------------------------------
# 块级解析
# ---------------------------------------------------------------------------

def is_table_separator(line):
    s = line.strip()
    if "|" not in s or "-" not in s:
        return False
    return all(c in "|-: " for c in s)


def parse_cells(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def parse_blocks(lines):
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # 代码围栏
        if stripped.startswith("```"):
            j = i + 1
            buf = []
            while j < n and not lines[j].strip().startswith("```"):
                buf.append(lines[j])
                j += 1
            blocks.append(("code", escape("\n".join(buf))))
            i = j + 1
            continue

        # 空行
        if not stripped:
            i += 1
            continue

        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            blocks.append(("heading", len(m.group(1)), m.group(2)))
            i += 1
            continue

        # 分隔线
        if re.match(r"^\s*([-*_])(\s*\1){2,}\s*$", line):
            blocks.append(("hr",))
            i += 1
            continue

        # 引用
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append(("quote", parse_blocks(buf)))
            continue

        # 表格（当前行含 |，下一行是分隔线）
        if "|" in line and i + 1 < n and is_table_separator(lines[i + 1]):
            header = parse_cells(line)
            rows = []
            j = i + 2
            while j < n and "|" in lines[j] and lines[j].strip():
                rows.append(parse_cells(lines[j]))
                j += 1
            blocks.append(("table", header, rows))
            i = j
            continue

        # 列表
        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
        if m:
            items = []
            j = i
            while j < n:
                lm = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", lines[j])
                if not lm:
                    if lines[j].strip() == "":
                        j += 1
                        continue
                    break
                items.append((len(lm.group(1)), lm.group(2), lm.group(3)))
                j += 1
            ordered = bool(re.match(r"^\d+[.)]", items[0][1]))
            blocks.append(("list", ordered, items))
            i = j
            continue

        # 段落（连续非空、非块起始行）
        buf = [stripped]
        j = i + 1
        while j < n and lines[j].strip() and not is_block_start(lines[j]):
            buf.append(lines[j].strip())
            j += 1
        blocks.append(("para", " ".join(buf)))
        i = j
        continue
    return blocks


def is_block_start(line):
    s = line.strip()
    if not s:
        return False
    if s.startswith("```"):
        return True
    if re.match(r"^#{1,6}\s+", s):
        return True
    if re.match(r"^\s*([-*_])(\s*\1){2,}\s*$", s):
        return True
    if s.startswith(">"):
        return True
    if re.match(r"^(\s*)([-*+]|\d+[.)])\s+", s):
        return True
    return False


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------

def render_items(items, ordered):
    tag = "ol" if ordered else "ul"
    out = []
    i = 0
    while i < len(items):
        indent, marker, text = items[i]
        children = []
        j = i + 1
        while j < len(items) and items[j][0] > indent:
            children.append(items[j])
            j += 1
        out.append(f"<li>{inline(text)}")
        if children:
            child_ordered = bool(re.match(r"^\d+[.)]", children[0][1]))
            out.append(render_items(children, child_ordered))
        out.append("</li>")
        i = j
    return f"<{tag}>" + "".join(out) + f"</{tag}>"


def render_table(header, rows):
    th = "".join(f"<th>{inline(c)}</th>" for c in header)
    body = ""
    for row in rows:
        # 补齐/截断到表头列数
        cells = (row + [""] * len(header))[:len(header)]
        body += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>"
    return f"<table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>"


def render_blocks(blocks):
    out = []
    for b in blocks:
        kind = b[0]
        if kind == "heading":
            out.append(f"<h{b[1]}>{inline(b[2])}</h{b[1]}>")
        elif kind == "para":
            out.append(f"<p>{inline(b[1])}</p>")
        elif kind == "code":
            out.append(f"<pre><code>{b[1]}</code></pre>")
        elif kind == "quote":
            out.append("<blockquote>" + render_blocks(b[1]) + "</blockquote>")
        elif kind == "list":
            out.append(render_items(b[2], b[1]))
        elif kind == "table":
            out.append(render_table(b[1], b[2]))
        elif kind == "hr":
            out.append("<hr>")
    return "\n".join(out)


CSS = """
:root {
  --bg: #f6f7f9;
  --card: #ffffff;
  --text: #1f2328;
  --muted: #59636e;
  --accent: #2563eb;
  --border: #e1e4e8;
  --code-bg: #f6f8fa;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei",
    "Hiragino Sans GB", sans-serif;
  line-height: 1.7;
}
.page {
  max-width: 860px;
  margin: 0 auto;
  padding: 40px 24px 64px;
}
header.top {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px 28px;
  margin-bottom: 20px;
}
header.top h1 {
  margin: 0 0 8px;
  font-size: 1.6em;
  line-height: 1.35;
}
header.top .meta {
  color: var(--muted);
  font-size: 0.88em;
}
.content {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 32px 36px;
}
.content > *:first-child { margin-top: 0; }
.content > *:last-child { margin-bottom: 0; }
h1, h2, h3, h4, h5, h6 { line-height: 1.4; }
h1 { font-size: 1.5em; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
h2 { font-size: 1.3em; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
h3 { font-size: 1.12em; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
code {
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: Consolas, "SF Mono", Menlo, monospace;
  font-size: 0.9em;
}
pre {
  background: var(--code-bg);
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
}
pre code { background: none; padding: 0; }
blockquote {
  margin: 1em 0;
  padding: 8px 18px;
  border-left: 4px solid var(--accent);
  background: #eef3ff;
  color: #33415c;
  border-radius: 0 6px 6px 0;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
}
th, td {
  border: 1px solid var(--border);
  padding: 8px 12px;
  text-align: left;
  vertical-align: top;
}
th { background: var(--code-bg); font-weight: 600; }
hr { border: none; border-top: 1px solid var(--border); margin: 1.5em 0; }
ul, ol { padding-left: 1.6em; }
li { margin: 0.25em 0; }
@media (max-width: 640px) {
  .page { padding: 16px 10px 40px; }
  .content { padding: 20px 18px; }
  header.top { padding: 18px 20px; }
}
"""

PAGE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="page">
  <header class="top">
    <h1>{title}</h1>
    <div class="meta">{meta_line}</div>
  </header>
  <div class="content">
{content}
  </div>
</div>
</body>
</html>
"""


def main():
    _reconfigure_stdout()
    _setup_logging()
    ap = argparse.ArgumentParser(description="渲染摘要 Markdown 为可独立打开的 HTML")
    ap.add_argument("path", help="Markdown 文件路径（如 summary.md）")
    ap.add_argument("--title", default=None, help="页面标题（默认取第一个一级标题或文件名）")
    ap.add_argument("--out", default=None, help="输出 HTML 路径（默认同目录同名 .html）")
    ap.add_argument("--lang", default="zh", help="HTML lang 属性（默认 zh）")
    ap.add_argument("--meta", default=None, help="额外元信息文本（显示在标题下方）")
    args = ap.parse_args()

    src = Path(args.path).expanduser().resolve()
    if src.is_dir():
        summary_md = src / "summary.md"
        if not summary_md.is_file():
            fatal(f"目录中未找到 summary.md: {src}")
        src = summary_md
    if not src.is_file():
        fatal(f"文件不存在: {src}")

    md = src.read_text(encoding="utf-8")
    blocks = parse_blocks(md.split("\n"))

    title = args.title
    if blocks and blocks[0][0] == "heading" and blocks[0][1] == 1:
        if not title:
            title = strip_md(blocks[0][2])
        blocks = blocks[1:]
    if not title:
        title = src.stem

    content = render_blocks(blocks)

    meta_line = args.meta or f"由 zhz-transcript-summarize 生成 · {time.strftime('%Y-%m-%d %H:%M')}"

    out_path = Path(args.out).expanduser().resolve() if args.out else src.with_suffix(".html")
    page = PAGE.format(
        lang=args.lang,
        title=escape(title),
        css=CSS,
        meta_line=escape(meta_line),
        content=content,
    )
    out_path.write_text(page, encoding="utf-8")
    LOG.info("✅ 已生成 HTML: %s", out_path)


if __name__ == "__main__":
    main()
