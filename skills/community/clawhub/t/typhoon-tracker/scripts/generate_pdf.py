#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 Markdown 文档转换为排版精美的 PDF。
功能：自定义封面页、图片嵌入（含 Obsidian ![[...]] 语法）、代码语法高亮、表格交替行底色、页脚页码。

用法：
    python generate_pdf.py <输入.md> [-o <输出.pdf>] [--title ...] [--subtitle ...] [--author ...] [--date ...]

依赖：
    pip install markdown pygments playwright pypdf
    playwright install chromium
"""

import argparse
import html as html_mod
import os
import sys
import tempfile
from datetime import datetime

import markdown
from pygments.formatters import HtmlFormatter

import re
import xml.etree.ElementTree as etree
from urllib.parse import quote

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.treeprocessors import Treeprocessor


# ============================================================
# 图片路径解析 & Wiki 风格图片扩展（![[filename]] → <img>）
# ============================================================

_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".ico", ".tiff", ".tif"}

# 搜索图片时的常见子目录名
_IMAGE_SUBDIRS = ("attachments", "assets", "images", "media", "imgs", "pics")


def _resolve_image_path(filename, base_dirs):
    """在多个搜索目录中查找图片文件，返回绝对路径（未找到返回 None）。

    搜索顺序：
    1. filename 已是绝对路径且存在 → 直接返回
    2. 在每个 base_dir 下直接拼接 filename
    3. 在每个 base_dir 下的常见子目录中查找
    """
    if os.path.isabs(filename) and os.path.isfile(filename):
        return filename

    for base in base_dirs:
        # 直接拼接
        candidate = os.path.join(base, filename)
        if os.path.isfile(candidate):
            return os.path.abspath(candidate)

        # 常见子目录
        for sub in _IMAGE_SUBDIRS:
            candidate = os.path.join(base, sub, filename)
            if os.path.isfile(candidate):
                return os.path.abspath(candidate)

    return None


class WikiImageInlineProcessor(InlineProcessor):
    """匹配 ![[filename]] 模式的 inline processor。"""

    def __init__(self, pattern, md, base_dirs):
        super().__init__(pattern, md)
        self.base_dirs = base_dirs

    def handleMatch(self, m, data):                 # noqa: N802
        filename = m.group(1).strip()
        if not filename:
            return None, None, None

        # 仅处理图片文件
        _, ext = os.path.splitext(filename)
        if ext.lower() not in _IMAGE_EXTS:
            return None, None, None

        image_path = _resolve_image_path(filename, self.base_dirs)
        if not image_path:
            return None, None, None

        # 构建 <img> 标签
        src = "file:///" + quote(image_path.replace(os.sep, "/"), safe="/:@")
        el = etree.Element("img")
        el.set("src", src)
        el.set("alt", filename)
        el.set("style", "max-width:100%;height:auto;display:block;margin:12px 0;")
        return el, m.start(0), m.end(0)


class ImageSrcTreeprocessor(Treeprocessor):
    """修正 <img> 的 src：将相对路径解析为 file:// 绝对 URL。

    标准 Markdown 图片语法 ![alt](path) 生成的 src 是原始路径字符串，
    当 HTML 写入临时目录时相对路径会失效；中文/空格等字符未编码也会导致加载失败。
    本处理器将所有非 URL 的 src 统一解析为绝对路径的 file:// URL，
    与 ![[...]] 语法走相同的 _resolve_image_path 逻辑。
    """

    _SKIP_PREFIXES = ("file://", "http://", "https://", "data:", "#", "mailto:")

    def __init__(self, md, base_dirs):
        super().__init__(md)
        self.base_dirs = base_dirs

    def run(self, root):
        for img in root.iter("img"):
            src = img.get("src", "")
            if not src or src.startswith(self._SKIP_PREFIXES):
                continue
            image_path = _resolve_image_path(src, self.base_dirs)
            if image_path:
                new_src = "file:///" + quote(image_path.replace(os.sep, "/"), safe="/:@")
                img.set("src", new_src)
        return root


class WikiImageExtension(Extension):
    """Python-Markdown 扩展：将 ![[filename]] 转为 <img> 标签。

    来源不限于 Obsidian ——任何使用 wiki-link 风格的 ![[嵌入]] 均适用。
    非图片后缀的文件保持原文不变，不会误转换。
    """

    def __init__(self, base_dirs, **kwargs):
        self.base_dirs = base_dirs
        super().__init__(**kwargs)

    def extendMarkdown(self, md):                   # noqa: N802
        pattern = WikiImageInlineProcessor(
            r"!\[\[([^\[\]]+)\]\]", md, self.base_dirs
        )
        md.inlinePatterns.register(pattern, "wiki_image", 175)

        # 修正标准 Markdown 图片 ![](path) 的 src 为绝对 file:// URL
        md.treeprocessors.register(
            ImageSrcTreeprocessor(md, self.base_dirs),
            "image_src_fix",
            5,
        )
# 页面边距常量 — 封面页 margin=0，内容页使用以下值
# ============================================================

_PAGE_MARGIN_TOP = "2.5cm"
_PAGE_MARGIN_BOTTOM = "2.5cm"
_PAGE_MARGIN_LEFT = "2cm"
_PAGE_MARGIN_RIGHT = "2cm"


# ============================================================
# CSS — 封面页专用（margin: 0，填满整页）
# ============================================================

COVER_CSS = """\
@page {
    size: A4;
    margin: 0;
}

body {
    margin: 0;
    padding: 0;
}

.cover-page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 21cm;
    height: 29.7cm;
    background: linear-gradient(135deg, #0a1628 0%, #1a3a5c 50%, #0d2137 100%);
    color: #ffffff;
    text-align: center;
    padding: 3cm;
    box-sizing: border-box;
}

.cover-page .cover-badge {
    font-size: 11pt;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.6);
    margin-bottom: 40px;
    border: 1px solid rgba(255,255,255,0.3);
    padding: 6px 20px;
    display: inline-block;
    max-width: 90%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.cover-page h1 {
    font-size: 32pt;
    font-weight: 700;
    margin: 20px 0 10px 0;
    letter-spacing: 4px;
    color: #ffffff;
    line-height: 1.3;
}

.cover-page .cover-subtitle {
    font-size: 14pt;
    color: rgba(255,255,255,0.8);
    margin: 15px 0 50px 0;
    line-height: 1.6;
}

.cover-page .cover-meta {
    font-size: 11pt;
    color: rgba(255,255,255,0.7);
    line-height: 2;
}

.cover-page .cover-meta span {
    display: block;
}

.cover-page .cover-datetime {
    margin-top: 30px;
    font-size: 10pt;
    color: rgba(255,255,255,0.5);
}
"""


# ============================================================
# CSS — 内容页专用（标准边距 + 排版样式）
# ============================================================

CONTENT_CSS = """\
@page {{
    size: A4;
    margin: {top} {right} {bottom} {left};
}}

body {{
    font-family: "Microsoft YaHei", "PingFang SC", "SimSun", sans-serif;
    font-size: 11pt;
    line-height: 1.8;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
}}

.content-wrapper {{
    padding: 0;
}}

h1 {{
    font-size: 20pt;
    color: #1a3a5c;
    margin-top: 30px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #1a3a5c;
}}

h2 {{
    font-size: 16pt;
    color: #2c5f8a;
    margin-top: 24px;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid #b0cfe0;
}}

h3 {{
    font-size: 13pt;
    color: #3a7bb5;
    margin-top: 18px;
    margin-bottom: 10px;
}}

p {{
    margin: 8px 0;
    text-align: justify;
}}

strong {{
    color: #c0392b;
}}

em {{
    color: #555;
}}

blockquote {{
    border-left: 4px solid #4a9eff;
    margin: 16px 0;
    padding: 10px 16px;
    background: #f0f6ff;
    color: #2c3e50;
    font-size: 10.5pt;
    border-radius: 0 4px 4px 0;
}}

blockquote p {{
    margin: 4px 0;
}}

hr {{
    border: none;
    border-top: 1px solid #ddd;
    margin: 30px 0;
}}

ul, ol {{
    margin: 8px 0;
    padding-left: 24px;
}}

li {{
    margin: 4px 0;
}}

img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 12px 0;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 10pt;
}}

th {{
    background: #1a3a5c;
    color: #ffffff;
    padding: 10px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 10pt;
}}

td {{
    padding: 8px 12px;
    border: 1px solid #d0d7de;
}}

tr:nth-child(even) td {{
    background: #f6f8fa;
}}

tr:nth-child(odd) td {{
    background: #ffffff;
}}

pre {{
    background: #272822;
    color: #f8f8f2;
    padding: 14px 18px;
    border-radius: 6px;
    overflow-x: auto;
    white-space: pre-wrap;
    overflow-wrap: break-word;
    word-break: break-all;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 9.5pt;
    line-height: 1.5;
    margin: 16px 0;
}}

code {{
    font-family: "Consolas", "Courier New", monospace;
    font-size: 9.5pt;
    background: #f0f0f0;
    padding: 2px 5px;
    border-radius: 3px;
    color: #c0392b;
}}

pre code {{
    background: none;
    padding: 0;
    color: inherit;
    font-size: 9.5pt;
}}

.codehilite {{
    background: #272822;
    padding: 14px 18px;
    border-radius: 6px;
    margin: 16px 0;
}}

.codehilite pre {{
    background: none;
    padding: 0;
    margin: 0;
}}
""".format(
    top=_PAGE_MARGIN_TOP,
    right=_PAGE_MARGIN_RIGHT,
    bottom=_PAGE_MARGIN_BOTTOM,
    left=_PAGE_MARGIN_LEFT,
)


# ============================================================
# HTML 模板
# ============================================================

COVER_HTML = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>
{cover_css}
</style>
</head>
<body>
<div class="cover-page">
    <div class="cover-badge">{badge_text}</div>
    <h1>{display_title}</h1>
{subtitle_block}
    <div class="cover-meta">
        <span>作者：{cover_author}</span>
    </div>
    <div class="cover-datetime">报告日期：{cover_date}</div>
</div>
</body>
</html>"""


CONTENT_HTML = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<style>
{content_css}
{code_style}
</style>
</head>
<body>
<div class="content-wrapper">
{html_body}
</div>
</body>
</html>"""


# ============================================================
# 辅助函数
# ============================================================

def _build_subtitle_block(subtitle):
    """构建副标题 HTML 片段。副标题为空时返回空字符串。"""
    if not subtitle or not subtitle.strip():
        return ""
    safe = html_mod.escape(subtitle)
    return f'    <p class="cover-subtitle">{safe}</p>\n'


def _badge_text(cover_title):
    """根据封面标题返回徽章文字。"""
    return cover_title if cover_title else "REPORT"


# ============================================================
# 构建 HTML
# ============================================================

_MD_EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.codehilite",
    "markdown.extensions.tables",
    "markdown.extensions.toc",
    "markdown.extensions.fenced_code",
    "markdown.extensions.smarty",
]

_CODE_STYLE = HtmlFormatter(style="monokai").get_style_defs(".codehilite")


def build_cover_html(cover_title, cover_subtitle, cover_author, cover_date):
    """构建封面页 HTML（独立文档，margin: 0）。"""
    display_title = html_mod.escape(cover_title) if cover_title else "COVER_TITLE"
    return COVER_HTML.format(
        cover_css=COVER_CSS,
        badge_text=html_mod.escape(_badge_text(cover_title)),
        display_title=display_title,
        subtitle_block=_build_subtitle_block(cover_subtitle),
        cover_author=html_mod.escape(cover_author) if cover_author else "user",
        cover_date=html_mod.escape(cover_date),
    )


def build_content_html(md_content, base_dirs=None):
    """构建内容页 HTML（独立文档，标准边距）。

    Parameters
    ----------
    md_content : str
        Markdown 原文。
    base_dirs : list[str] | None
        图片搜索目录列表；为 None 时不启用 ![[...]] 语法转换。
    """
    extensions = list(_MD_EXTENSIONS)
    if base_dirs:
        extensions.append(WikiImageExtension(base_dirs))

    html_body = markdown.markdown(md_content, extensions=extensions)
    return CONTENT_HTML.format(
        content_css=CONTENT_CSS,
        code_style=_CODE_STYLE,
        html_body=html_body,
    )


# ============================================================
# 参数解析
# ============================================================

def parse_args():
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="将 Markdown 文档转换为排版精美的 PDF（带封面页）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python generate_pdf.py report.md
    python generate_pdf.py report.md -o output.pdf
    python generate_pdf.py report.md --title "月度分析报告" --subtitle "2026年7月" --author "张三"
    python generate_pdf.py report.md --title "" --subtitle "" --date "2026年7月8日"
        """,
    )

    parser.add_argument("input", help="输入的 Markdown 文件路径")

    parser.add_argument("-o", "--output", default=None,
                        help="输出的 PDF 文件路径（默认：与输入文件同名，后缀改为 .pdf）")

    parser.add_argument("--title", default=None,
                        help="""封面标题。
未指定时：从 Markdown 中提取第一个一级标题。
指定空字符串 ""：封面显示 "COVER_TITLE" 占位。""")

    parser.add_argument("--subtitle", default=None,
                        help="""封面副标题。
未指定时：从 Markdown 中提取第二个一级标题（若存在）。
指定空字符串 ""：封面不显示副标题。""")

    parser.add_argument("--author", default=None,
                        help='封面作者（默认："user"）。指定空字符串 "" 则使用默认值。')

    parser.add_argument("--date", default=None,
                        help='封面日期（默认：系统当前日期，格式 "XX年XX月XX日"）。')

    parser.add_argument("--image-dir", default=None,
                        help="图片搜索目录。未指定时自动在 Markdown 文件所在目录及常见子目录中查找。")

    parser.add_argument("--keep-html", action="store_true", default=False,
                        help="保留生成的中间 HTML 文件（默认保存在临时目录，脚本结束后自动删除）。")

    return parser.parse_args()


# ============================================================
# Markdown 标题提取
# ============================================================

def extract_titles_from_md(md_content):
    """从 Markdown 内容中提取所有一级标题（# 开头），返回列表。"""
    titles = []
    for line in md_content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            title_text = stripped[2:].strip()
            if title_text:
                titles.append(title_text)
    return titles


# ============================================================
# PDF 生成 — 双 PDF 合并方案
# ============================================================

def _generate_pdf(cover_html_path, content_html_path, output_pdf_path):
    """生成 PDF：封面 PDF（无页码）+ 内容 PDF（有页码）→ pypdf 合并。

    封面 PDF：margin=0，display_header_footer=False → 填满整页，无页码
    内容 PDF：margin=2.5cm/2cm，display_header_footer=True → 标准边距，有页码
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[错误] 未安装 playwright。请运行：pip install playwright && playwright install chromium",
              file=sys.stderr)
        sys.exit(1)

    try:
        from pypdf import PdfWriter
    except ImportError:
        print("[错误] 未安装 pypdf。请运行：pip install pypdf", file=sys.stderr)
        sys.exit(1)

    cover_abs = os.path.abspath(cover_html_path).replace(os.sep, "/")
    content_abs = os.path.abspath(content_html_path).replace(os.sep, "/")

    # 临时 PDF 文件
    fd1, cover_pdf = tempfile.mkstemp(suffix=".pdf", prefix="md2pdf_cover_")
    os.close(fd1)
    fd2, content_pdf = tempfile.mkstemp(suffix=".pdf", prefix="md2pdf_content_")
    os.close(fd2)

    footer_template = (
        '<div style="width:100%;text-align:center;font-size:9pt;'
        'color:#888;font-family:Microsoft YaHei,sans-serif;padding:0 2cm;">'
        '<span class="pageNumber"></span> / <span class="totalPages"></span></div>'
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            # ---- 1. 封面 PDF：margin=0，无页眉页脚 ----
            page = browser.new_page()
            page.goto(f"file:///{cover_abs}")
            page.wait_for_load_state("networkidle")
            page.pdf(
                path=cover_pdf,
                format="A4",
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                display_header_footer=False,
                print_background=True,
            )
            page.close()

            # ---- 2. 内容 PDF：标准边距，有页眉页脚 ----
            page = browser.new_page()
            page.goto(f"file:///{content_abs}")
            page.wait_for_load_state("networkidle")
            page.pdf(
                path=content_pdf,
                format="A4",
                margin={
                    "top": _PAGE_MARGIN_TOP,
                    "bottom": _PAGE_MARGIN_BOTTOM,
                    "left": _PAGE_MARGIN_LEFT,
                    "right": _PAGE_MARGIN_RIGHT,
                },
                display_header_footer=True,
                header_template="<span></span>",
                footer_template=footer_template,
                print_background=True,
            )
            page.close()
        finally:
            browser.close()

    # ---- 3. 合并 PDF ----
    writer = PdfWriter()
    writer.append(cover_pdf)
    writer.append(content_pdf)
    writer.write(output_pdf_path)
    writer.close()

    # ---- 4. 清理临时 PDF ----
    for tmp in (cover_pdf, content_pdf):
        try:
            os.remove(tmp)
        except OSError:
            pass


# ============================================================
# 主流程
# ============================================================

def main():
    args = parse_args()

    # ---- 1. 检查输入文件 ----
    if not os.path.isfile(args.input):
        print(f"[错误] 输入文件不存在：{args.input}", file=sys.stderr)
        sys.exit(1)

    # ---- 2. 推导输出路径 & 确保目录存在 ----
    if args.output:
        output_pdf = os.path.abspath(args.output)
    else:
        base, _ = os.path.splitext(os.path.abspath(args.input))
        output_pdf = base + ".pdf"

    output_dir = os.path.dirname(output_pdf)
    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    print(f"[1/5] 读取 Markdown 文件：{args.input}")

    # ---- 3. 读取 Markdown ----
    with open(args.input, "r", encoding="utf-8") as f:
        md_content = f.read()

    # ---- 4. 从 Markdown 中提取标题用于智能回退 ----
    h1_titles = extract_titles_from_md(md_content)

    # ---- 5. 处理封面参数 ----
    if args.title is not None:
        cover_title = args.title
    else:
        cover_title = h1_titles[0] if h1_titles else ""

    if args.subtitle is not None:
        cover_subtitle = args.subtitle
    else:
        cover_subtitle = h1_titles[1] if len(h1_titles) >= 2 else ""

    cover_author = args.author if args.author else "user"

    if args.date:
        cover_date = args.date
    else:
        now = datetime.now()
        cover_date = f"{now.year}年{now.month}月{now.day}日"

    print(f"     封面标题：{cover_title if cover_title else '(COVER_TITLE 占位)'}")
    print(f"     封面副标题：{cover_subtitle if cover_subtitle else '(无)'}")
    print(f"     封面作者：{cover_author}")
    print(f"     封面日期：{cover_date}")

    # ---- 6. 构建封面 HTML 和内容 HTML ----
    # 图片搜索目录：默认 = 输入文件所在目录；可额外指定 --image-dir
    base_dirs = [os.path.dirname(os.path.abspath(args.input))]
    if args.image_dir:
        base_dirs.append(os.path.abspath(args.image_dir))

    cover_html = build_cover_html(cover_title, cover_subtitle, cover_author, cover_date)
    content_html = build_content_html(md_content, base_dirs)
    print(f"[2/5] HTML 构建完成（封面 + 内容）")

    # ---- 7. 保存中间 HTML ----
    keep = args.keep_html
    if keep:
        base, _ = os.path.splitext(args.input)
        cover_html_path = base + "_cover.html"
        content_html_path = base + "_content.html"
    else:
        fd1, cover_html_path = tempfile.mkstemp(suffix=".html", prefix="md2pdf_cover_")
        os.close(fd1)
        fd2, content_html_path = tempfile.mkstemp(suffix=".html", prefix="md2pdf_content_")
        os.close(fd2)

    with open(cover_html_path, "w", encoding="utf-8") as f:
        f.write(cover_html)
    with open(content_html_path, "w", encoding="utf-8") as f:
        f.write(content_html)

    # ---- 8. 生成 PDF（双 PDF 合并） ----
    print(f"[3/5] 生成封面 PDF（无页码）...")
    print(f"[4/5] 生成内容 PDF（有页码）并合并...")
    _generate_pdf(cover_html_path, content_html_path, output_pdf)

    # ---- 9. 清理临时 HTML ----
    if not keep:
        for p in (cover_html_path, content_html_path):
            try:
                os.remove(p)
            except OSError:
                pass

    print(f"[5/5] PDF 生成成功！")
    print(f"     输出：{os.path.abspath(output_pdf)}")
    print(f"     大小：{os.path.getsize(output_pdf) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
