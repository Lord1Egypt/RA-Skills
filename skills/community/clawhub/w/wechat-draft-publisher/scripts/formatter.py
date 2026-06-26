"""
文章排版和 HTML 格式化模块
将 Markdown 文章转换为微信公众号适配的精美 HTML
"""

import re


# ============================================================
# 微信公众号内联样式（微信不支持外部 CSS，必须内联）
# ============================================================

STYLES = {
    "body": (
        "font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', "
        "'PingFang SC', 'Microsoft YaHei', sans-serif; "
        "font-size: 16px; line-height: 1.8; color: #333; "
        "padding: 0; margin: 0; word-wrap: break-word;"
    ),
    "title": (
        "font-size: 24px; font-weight: bold; color: #1a1a1a; "
        "text-align: center; margin-bottom: 8px; line-height: 1.4;"
    ),
    "digest": (
        "font-size: 14px; color: #888; text-align: center; "
        "margin-bottom: 24px; padding: 0 20px; line-height: 1.6;"
    ),
    "h2": (
        "font-size: 20px; font-weight: bold; color: #1a1a1a; "
        "margin-top: 32px; margin-bottom: 16px; padding-left: 12px; "
        "border-left: 4px solid #07c160; line-height: 1.4;"
    ),
    "h3": (
        "font-size: 17px; font-weight: bold; color: #333; "
        "margin-top: 24px; margin-bottom: 12px; line-height: 1.4;"
    ),
    "p": (
        "font-size: 16px; color: #333; margin: 0 0 16px 0; "
        "line-height: 1.8; letter-spacing: 0.5px;"
    ),
    "img_wrapper": (
        "text-align: center; margin: 20px 0;"
    ),
    "img": (
        "max-width: 100%; border-radius: 8px; "
        "box-shadow: 0 2px 8px rgba(0,0,0,0.1);"
    ),
    "img_caption": (
        "font-size: 13px; color: #999; text-align: center; "
        "margin-top: 8px;"
    ),
    "blockquote": (
        "margin: 16px 0; padding: 12px 16px; "
        "background-color: #f7f7f7; border-left: 4px solid #07c160; "
        "border-radius: 0 4px 4px 0; color: #666; "
        "font-size: 15px; line-height: 1.7;"
    ),
    "code_inline": (
        "background-color: #f0f0f0; color: #e74c3c; "
        "padding: 2px 6px; border-radius: 3px; font-size: 14px; "
        "font-family: 'SFMono-Regular', Consolas, monospace;"
    ),
    "code_block": (
        "background-color: #1e1e1e; color: #dcdcdc; "
        "padding: 16px; border-radius: 8px; font-size: 13px; "
        "line-height: 1.6; overflow-x: auto; margin: 16px 0; "
        "font-family: 'SFMono-Regular', Consolas, monospace;"
    ),
    "ul": (
        "margin: 8px 0 16px 0; padding-left: 24px; "
        "line-height: 1.8; color: #333;"
    ),
    "ol": (
        "margin: 8px 0 16px 0; padding-left: 24px; "
        "line-height: 1.8; color: #333;"
    ),
    "li": (
        "margin-bottom: 6px; font-size: 16px;"
    ),
    "strong": (
        "font-weight: bold; color: #07c160;"
    ),
    "hr": (
        "border: none; border-top: 1px dashed #ddd; "
        "margin: 24px 0;"
    ),
    "footer": (
        "text-align: center; font-size: 13px; color: #bbb; "
        "margin-top: 32px; padding-top: 16px; "
        "border-top: 1px solid #eee;"
    ),
}


def markdown_to_wechat_html(
    markdown_text: str,
    image_urls: dict = None,
    title: str = "",
    digest: str = "",
) -> str:
    """
    将 Markdown 文本转换为微信公众号适配的 HTML

    参数：
        markdown_text: Markdown 格式的文章内容
        image_urls: 图片标记到微信图片 URL 的映射 {index: url}
        title: 文章标题（如果需要在正文中显示）
        digest: 文章摘要
    """
    if image_urls is None:
        image_urls = {}

    lines = markdown_text.strip().split("\n")
    html_parts = []
    in_code_block = False
    code_block_content = []
    in_list = False
    list_type = None
    list_items = []
    image_index = 0

    for line in lines:
        stripped = line.strip()

        # 代码块处理
        if stripped.startswith("```"):
            if in_code_block:
                code_text = _escape_html("\n".join(code_block_content))
                html_parts.append(
                    f'<pre style="{STYLES["code_block"]}">'
                    f"<code>{code_text}</code></pre>"
                )
                code_block_content = []
                in_code_block = False
            else:
                _flush_list(html_parts, list_items, list_type)
                list_items = []
                in_list = False
                in_code_block = True
            continue

        if in_code_block:
            code_block_content.append(line)
            continue

        # 空行
        if not stripped:
            _flush_list(html_parts, list_items, list_type)
            list_items = []
            in_list = False
            continue

        # 图片占位符 <!-- [IMAGE: prompt] -->
        img_match = re.match(r"<!--\s*\[IMAGE:.*?\]\s*-->", stripped)
        if img_match:
            if image_index in image_urls:
                url = image_urls[image_index]
                html_parts.append(
                    f'<div style="{STYLES["img_wrapper"]}">'
                    f'<img src="{url}" style="{STYLES["img"]}" />'
                    f"</div>"
                )
            image_index += 1
            continue

        # 标题（跳过 H1，因为微信文章标题在外部设置）
        h1_match = re.match(r"^#\s+(.+)$", stripped)
        if h1_match:
            continue

        h2_match = re.match(r"^##\s+(.+)$", stripped)
        if h2_match:
            _flush_list(html_parts, list_items, list_type)
            list_items = []
            in_list = False
            text = _inline_format(h2_match.group(1))
            html_parts.append(f'<h2 style="{STYLES["h2"]}">{text}</h2>')
            continue

        h3_match = re.match(r"^###\s+(.+)$", stripped)
        if h3_match:
            _flush_list(html_parts, list_items, list_type)
            list_items = []
            in_list = False
            text = _inline_format(h3_match.group(1))
            html_parts.append(f'<h3 style="{STYLES["h3"]}">{text}</h3>')
            continue

        # 引用
        if stripped.startswith("> "):
            _flush_list(html_parts, list_items, list_type)
            list_items = []
            in_list = False
            text = _inline_format(stripped[2:])
            html_parts.append(
                f'<blockquote style="{STYLES["blockquote"]}">{text}</blockquote>'
            )
            continue

        # 分割线
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            _flush_list(html_parts, list_items, list_type)
            list_items = []
            in_list = False
            html_parts.append(f'<hr style="{STYLES["hr"]}" />')
            continue

        # 无序列表
        ul_match = re.match(r"^[-*+]\s+(.+)$", stripped)
        if ul_match:
            if not in_list or list_type != "ul":
                _flush_list(html_parts, list_items, list_type)
                list_items = []
                in_list = True
                list_type = "ul"
            list_items.append(_inline_format(ul_match.group(1)))
            continue

        # 有序列表
        ol_match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ol_match:
            if not in_list or list_type != "ol":
                _flush_list(html_parts, list_items, list_type)
                list_items = []
                in_list = True
                list_type = "ol"
            list_items.append(_inline_format(ol_match.group(1)))
            continue

        # 普通段落
        _flush_list(html_parts, list_items, list_type)
        list_items = []
        in_list = False
        text = _inline_format(stripped)
        html_parts.append(f'<p style="{STYLES["p"]}">{text}</p>')

    # 清理残余列表
    _flush_list(html_parts, list_items, list_type)

    body = "\n".join(html_parts)
    return f'<div style="{STYLES["body"]}">\n{body}\n</div>'


def _flush_list(html_parts: list, items: list, list_type: str):
    """将收集的列表项输出为 HTML"""
    if not items:
        return
    tag = list_type or "ul"
    style = STYLES.get(tag, STYLES["ul"])
    inner = "\n".join(
        f'<li style="{STYLES["li"]}">{item}</li>' for item in items
    )
    html_parts.append(f'<{tag} style="{style}">\n{inner}\n</{tag}>')


def _inline_format(text: str) -> str:
    """处理行内 Markdown 格式：粗体、斜体、行内代码、链接"""
    # 行内代码
    text = re.sub(
        r"`([^`]+)`",
        rf'<code style="{STYLES["code_inline"]}">\1</code>',
        text,
    )
    # 粗体
    text = re.sub(
        r"\*\*(.+?)\*\*",
        rf'<strong style="{STYLES["strong"]}">\1</strong>',
        text,
    )
    # 斜体
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # 链接
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2" style="color: #07c160; text-decoration: none;">\1</a>',
        text,
    )
    return text


def _escape_html(text: str) -> str:
    """转义 HTML 特殊字符"""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def extract_title(markdown_text: str) -> str:
    """从 Markdown 中提取 H1 标题"""
    match = re.search(r"^#\s+(.+)$", markdown_text, re.MULTILINE)
    return match.group(1).strip() if match else "未命名文章"


def extract_digest(markdown_text: str) -> str:
    """从 Markdown 中提取摘要（第一个引用块的内容）"""
    match = re.search(r"^>\s+(.+)$", markdown_text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_image_prompts(markdown_text: str) -> list:
    """提取所有图片占位符中的提示词"""
    return re.findall(r"<!--\s*\[IMAGE:\s*(.+?)\]\s*-->", markdown_text)
