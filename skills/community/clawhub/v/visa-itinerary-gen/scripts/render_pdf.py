#!/usr/bin/env python3
"""将 Markdown 行程表渲染为 A4 PDF。内部处理 md→HTML→PDF 全链路。"""
import argparse
import os
import re
import sys
import tempfile


# ── Markdown 解析 ──────────────────────────────────────────────

def parse_md_table(text):
    """从 Markdown 文本中提取标题和第一个 pipe table。

    返回 (title, headers, rows)
    - title: str, 如 "Travel Plan"
    - headers: list[str], 如 ["Country", "Day", ...]
    - rows: list[list[str]]
    """
    lines = text.strip().splitlines()

    # 提取标题：第一个 # 开头的行
    title = "Travel Plan"
    for line in lines:
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            break

    # 提取表格：找所有 | 开头的行
    table_lines = [l for l in lines if l.strip().startswith("|")]
    if len(table_lines) < 3:
        print("Error: Markdown 中未找到有效的表格（至少需要表头、分隔行、一行数据）", file=sys.stderr)
        sys.exit(1)

    def split_row(line):
        """按 | 分割一行，去掉首尾空单元格。"""
        cells = line.split("|")
        # 首尾是空字符串（因为行以 | 开头和结尾）
        return [c.strip() for c in cells[1:-1]]

    headers = split_row(table_lines[0])

    # 跳过分隔行（第二行，全是 -、:、|、空格）
    rows = []
    for line in table_lines[2:]:
        row = split_row(line)
        if row:
            rows.append(row)

    return title, headers, rows


# ── HTML 生成 ──────────────────────────────────────────────────

# 列宽百分比，针对 7 列签证行程表优化
COLUMN_WIDTHS = [8, 4, 10, 10, 28, 22, 18]

CSS = """
body {
    font-family: 'Times New Roman', 'Noto Serif CJK SC', serif;
    margin: 0;
    padding: 20px;
    color: #000;
}
h1 {
    text-align: center;
    font-size: 18px;
    margin: 0 0 16px 0;
    font-weight: bold;
}
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 10px;
    table-layout: fixed;
}
th, td {
    border: 1px solid #000;
    padding: 4px 6px;
    text-align: left;
    word-wrap: break-word;
    overflow-wrap: break-word;
    vertical-align: top;
}
th {
    background: #f0f0f0;
    font-weight: bold;
    font-size: 10px;
}
"""


def build_html(title, headers, rows):
    """生成带内嵌 CSS 的完整 HTML 文档。"""
    # colgroup
    col_tags = ""
    for w in COLUMN_WIDTHS[:len(headers)]:
        col_tags += f'<col style="width:{w}%">'

    # thead
    th_cells = "".join(f"<th>{h}</th>" for h in headers)

    # tbody
    tr_rows = ""
    for row in rows:
        td_cells = ""
        for i, cell in enumerate(row):
            # 转义 HTML 特殊字符
            safe = cell.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            td_cells += f"<td>{safe}</td>"
        # 补齐列数（如果某行单元格少于表头）
        for _ in range(len(headers) - len(row)):
            td_cells += "<td></td>"
        tr_rows += f"<tr>{td_cells}</tr>\n"

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>{CSS}</style>
</head>
<body>
<h1>{title}</h1>
<table>
<colgroup>{col_tags}</colgroup>
<thead><tr>{th_cells}</tr></thead>
<tbody>
{tr_rows}</tbody>
</table>
</body>
</html>"""


# ── PDF 渲染 ──────────────────────────────────────────────────

def render_pdf(html_path, output_path):
    """用 playwright chromium 将 HTML 渲染为 A4 PDF。"""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{os.path.abspath(html_path)}")
        page.pdf(
            path=output_path,
            format="A4",
            margin={
                "top": "16mm",
                "right": "14mm",
                "bottom": "16mm",
                "left": "14mm",
            },
            print_background=True,
        )
        browser.close()


# ── 主流程 ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="将 Markdown 行程表渲染为 A4 PDF（md→HTML→PDF）"
    )
    parser.add_argument("--md", required=True, help="输入的 Markdown 文件路径")
    parser.add_argument("--output", required=True, help="输出的 PDF 文件路径")
    args = parser.parse_args()

    # 1. 读取 Markdown
    if not os.path.exists(args.md):
        print(f"Error: {args.md} not found", file=sys.stderr)
        sys.exit(1)

    with open(args.md, "r", encoding="utf-8") as f:
        md_text = f.read()

    # 2. 解析表格
    title, headers, rows = parse_md_table(md_text)

    # 3. 生成 HTML
    html_content = build_html(title, headers, rows)

    # 4. 写入临时 HTML 文件
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", encoding="utf-8", delete=False
    )
    tmp.write(html_content)
    tmp.close()

    try:
        # 5. 渲染 PDF
        render_pdf(tmp.name, args.output)
        print(f"PDF saved to {args.output}")
    finally:
        # 6. 清理临时 HTML（Markdown 原文件不动）
        if os.path.exists(tmp.name):
            os.remove(tmp.name)


if __name__ == "__main__":
    main()
