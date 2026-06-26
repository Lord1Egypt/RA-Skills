#!/usr/bin/env python3
"""
format_article.py — 将 Markdown 文章转换为微信公众号 IT科技风格 HTML

微信公众号 HTML 特殊要求：
1. 所有样式必须内联（inline style），不支持 <style> 标签中的 class
2. 不支持外部字体、外部 CSS
3. 图片必须先上传到微信CDN，不能用外链（此脚本保留占位符，由 publisher 替换）
4. 建议最大宽度 677px

用法：
    python format_article.py --input article.md --output article.html

或在代码中调用：
    from format_article import markdown_to_wechat_html
    html = markdown_to_wechat_html(markdown_text, cover_url, images)
"""

import re
import argparse
from pathlib import Path


# ── 颜色主题（IT科技风，蓝紫渐变系）──────────────────────────────────
COLOR_PRIMARY   = "#1a6ff4"   # 主色：科技蓝
COLOR_SECONDARY = "#6c3be8"   # 辅色：科技紫
COLOR_BG_CODE   = "#1e1e2e"   # 代码块背景（深色）
COLOR_BG_QUOTE  = "#f0f4ff"   # 引用块背景
COLOR_TEXT      = "#333333"   # 正文颜色
COLOR_LIGHT     = "#666666"   # 次要文字
COLOR_BORDER    = "#e8edf5"   # 边框颜色


def s(style_dict: dict) -> str:
    """将样式字典转换为内联 style 字符串"""
    return "; ".join(f"{k}: {v}" for k, v in style_dict.items())


# ── 各元素内联样式定义 ───────────────────────────────────────────────

STYLE_BODY = s({
    "font-family": "-apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif",
    "font-size": "16px",
    "line-height": "1.75",
    "color": COLOR_TEXT,
    "max-width": "677px",
    "margin": "0 auto",
    "padding": "0 16px",
    "word-break": "break-word",
})

STYLE_COVER = s({
    "width": "100%",
    "border-radius": "8px",
    "margin": "0 0 24px 0",
    "display": "block",
})

STYLE_H1 = s({
    "font-size": "22px",
    "font-weight": "bold",
    "color": COLOR_PRIMARY,
    "text-align": "center",
    "padding": "16px 0 8px 0",
    "margin": "0 0 24px 0",
    "border-bottom": f"2px solid {COLOR_PRIMARY}",
    "letter-spacing": "1px",
})

STYLE_H2 = s({
    "font-size": "18px",
    "font-weight": "bold",
    "color": COLOR_PRIMARY,
    "margin": "28px 0 12px 0",
    "padding": "0 0 0 12px",
    "border-left": f"4px solid {COLOR_PRIMARY}",
    "background": f"linear-gradient(90deg, {COLOR_BG_QUOTE}, transparent)",
})

STYLE_H3 = s({
    "font-size": "16px",
    "font-weight": "bold",
    "color": COLOR_SECONDARY,
    "margin": "20px 0 8px 0",
})

STYLE_P = s({
    "font-size": "16px",
    "line-height": "1.8",
    "color": COLOR_TEXT,
    "margin": "0 0 16px 0",
    "text-align": "justify",
})

STYLE_STRONG = s({
    "color": COLOR_PRIMARY,
    "font-weight": "bold",
})

STYLE_CODE_INLINE = s({
    "font-family": "Menlo, Monaco, Consolas, monospace",
    "font-size": "14px",
    "background": "#f0f4ff",
    "color": COLOR_SECONDARY,
    "padding": "2px 6px",
    "border-radius": "3px",
})

STYLE_CODE_BLOCK = s({
    "font-family": "Menlo, Monaco, Consolas, monospace",
    "font-size": "13px",
    "background": COLOR_BG_CODE,
    "color": "#cdd6f4",
    "padding": "16px",
    "border-radius": "8px",
    "overflow-x": "auto",
    "margin": "16px 0",
    "line-height": "1.6",
    "white-space": "pre",
})

STYLE_BLOCKQUOTE = s({
    "background": COLOR_BG_QUOTE,
    "border-left": f"4px solid {COLOR_PRIMARY}",
    "margin": "16px 0",
    "padding": "12px 16px",
    "border-radius": "0 8px 8px 0",
    "color": COLOR_LIGHT,
    "font-style": "italic",
})

STYLE_IMG = s({
    "width": "100%",
    "border-radius": "8px",
    "margin": "16px 0",
    "display": "block",
})

STYLE_IMG_CAPTION = s({
    "text-align": "center",
    "font-size": "13px",
    "color": "#999",
    "margin": "-8px 0 16px 0",
})

STYLE_DIVIDER = s({
    "border": "none",
    "border-top": f"1px solid {COLOR_BORDER}",
    "margin": "24px 0",
})

STYLE_FOOTER = s({
    "text-align": "center",
    "font-size": "13px",
    "color": "#aaa",
    "margin": "32px 0 16px 0",
    "padding-top": "16px",
    "border-top": f"1px solid {COLOR_BORDER}",
})

STYLE_TAG = s({
    "display": "inline-block",
    "background": f"linear-gradient(135deg, {COLOR_PRIMARY}, {COLOR_SECONDARY})",
    "color": "white",
    "font-size": "12px",
    "padding": "2px 10px",
    "border-radius": "12px",
    "margin": "0 4px 8px 0",
})

STYLE_CTA = s({
    "background": f"linear-gradient(135deg, {COLOR_PRIMARY}, {COLOR_SECONDARY})",
    "color": "white",
    "text-align": "center",
    "padding": "16px",
    "border-radius": "12px",
    "margin": "24px 0",
    "font-size": "15px",
    "font-weight": "bold",
})


def convert_markdown_to_html(md: str) -> str:
    """基础 Markdown → HTML 转换（内联样式版）"""
    lines = md.split("\n")
    html_lines = []
    in_code_block = False
    code_buffer = []
    code_lang = ""

    for line in lines:
        # 代码块
        if line.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lang = line[3:].strip()
                code_buffer = []
            else:
                in_code_block = False
                code_content = "\n".join(code_buffer)
                # 转义 HTML
                code_content = code_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                lang_label = f'<span style="color:#89b4fa;font-size:11px">{code_lang}</span>\n' if code_lang else ""
                html_lines.append(
                    f'<pre style="{STYLE_CODE_BLOCK}">{lang_label}{code_content}</pre>'
                )
            continue

        if in_code_block:
            code_buffer.append(line)
            continue

        # 图片占位符 [配图N占位：描述]
        img_match = re.match(r"^\[配图(\d+)占位：(.+?)\]$", line)
        if img_match:
            n = img_match.group(1)
            desc = img_match.group(2)
            html_lines.append(
                f'<img src="{{{{IMAGE_{n}}}}}" alt="{desc}" style="{STYLE_IMG}" />'
                f'<p style="{STYLE_IMG_CAPTION}">▲ {desc}</p>'
            )
            continue

        # 封面图占位
        if line.strip() == "[封面图占位]":
            html_lines.append(f'<img src="{{{{COVER_IMAGE}}}}" alt="封面图" style="{STYLE_COVER}" />')
            continue

        # 标题
        if line.startswith("# "):
            text = line[2:].strip()
            html_lines.append(f'<h1 style="{STYLE_H1}">{text}</h1>')
        elif line.startswith("## "):
            text = line[3:].strip()
            html_lines.append(f'<h2 style="{STYLE_H2}">{text}</h2>')
        elif line.startswith("### "):
            text = line[4:].strip()
            html_lines.append(f'<h3 style="{STYLE_H3}">{text}</h3>')

        # 分割线
        elif line.strip() in ("---", "***", "==="):
            html_lines.append(f'<hr style="{STYLE_DIVIDER}" />')

        # 引用
        elif line.startswith("> "):
            text = line[2:].strip()
            text = apply_inline_styles(text)
            html_lines.append(f'<blockquote style="{STYLE_BLOCKQUOTE}">{text}</blockquote>')

        # 空行
        elif not line.strip():
            html_lines.append("")

        # 普通段落
        else:
            text = apply_inline_styles(line)
            if text.strip():
                html_lines.append(f'<p style="{STYLE_P}">{text}</p>')

    return "\n".join(html_lines)


def apply_inline_styles(text: str) -> str:
    """处理行内 Markdown 格式"""
    # 粗体
    text = re.sub(r"\*\*(.+?)\*\*", f'<strong style="{STYLE_STRONG}">\\1</strong>', text)
    text = re.sub(r"__(.+?)__", f'<strong style="{STYLE_STRONG}">\\1</strong>', text)
    # 行内代码
    text = re.sub(r"`(.+?)`", f'<code style="{STYLE_CODE_INLINE}">\\1</code>', text)
    # 斜体
    text = re.sub(r"\*(.+?)\*", r'<em>\1</em>', text)
    # 链接
    text = re.sub(r"\[(.+?)\]\((.+?)\)", f'<a href="\\2" style="color:{COLOR_PRIMARY}">\\1</a>', text)
    return text


def build_footer(author: str = "IT科技号") -> str:
    """生成文章底部（版权+关注引导）"""
    return f"""
<hr style="{STYLE_DIVIDER}" />
<div style="{STYLE_CTA}">
    👋 觉得有用？点个「在看」支持一下<br/>
    💬 欢迎在留言区分享你的看法
</div>
<div style="{STYLE_FOOTER}">
    <p>— {author} —</p>
    <p style="font-size:12px">本文内容综合整理自知乎、公开报道及技术文档<br/>
    图片来自 Unsplash，如有侵权请联系删除</p>
</div>
"""


def markdown_to_wechat_html(
    markdown_text: str,
    cover_url: str = "",
    inline_images: list = None,
    author: str = "IT科技号",
    tags: list = None,
) -> str:
    """
    主函数：将 Markdown 转换为完整的微信公众号 HTML

    Args:
        markdown_text: Markdown 格式文章
        cover_url: 封面图 URL（已上传到微信CDN的 URL 或外链）
        inline_images: 正文配图列表，[{"url": ..., "alt": ...}, ...]
        author: 作者署名
        tags: 文章标签列表

    Returns:
        完整 HTML 字符串
    """
    if inline_images is None:
        inline_images = []
    if tags is None:
        tags = ["科技", "IT", "互联网"]

    # 转换 Markdown
    body_html = convert_markdown_to_html(markdown_text)

    # 替换封面图占位符
    body_html = body_html.replace("{{COVER_IMAGE}}", cover_url or "")

    # 替换正文配图占位符
    for i, img in enumerate(inline_images, 1):
        body_html = body_html.replace(
            f"{{{{IMAGE_{i}}}}}",
            img.get("url", "")
        )

    # 标签区
    tags_html = "".join(f'<span style="{STYLE_TAG}">#{tag}</span>' for tag in tags)

    # 完整 HTML
    html = f"""<section style="{STYLE_BODY}">
{body_html}
<p>{tags_html}</p>
{build_footer(author)}
</section>"""

    return html


def main():
    parser = argparse.ArgumentParser(description="将 Markdown 转换为微信公众号 HTML")
    parser.add_argument("--input", required=True, help="输入 Markdown 文件路径")
    parser.add_argument("--output", default="article.html", help="输出 HTML 文件路径")
    parser.add_argument("--author", default="IT科技号", help="作者名称")
    args = parser.parse_args()

    md_text = Path(args.input).read_text(encoding="utf-8")
    html = markdown_to_wechat_html(md_text, author=args.author)

    Path(args.output).write_text(html, encoding="utf-8")
    print(f"✅ HTML 已生成：{args.output}")
    print(f"   字符数：{len(html)}")


if __name__ == "__main__":
    main()
