"""Markdown -> 微信图文 HTML 转换器（零依赖，仅标准库）。

微信官方编辑器不支持原生 Markdown，业界最佳实践：
1. 用 <section> 包裹整段内容，关键元素加内联样式（移动端友好、各客户端兼容好）；
2. 图片不能引用本地或任意外链，必须先传到微信素材库，用返回的 mmbiz 链接，
   并同时写 data-src 与 src（微信客户端读取 data-src）；
3. 代码块用 <section> 背景 + white-space:pre-wrap，避免 <pre> 被部分客户端截断。

本模块只负责「文本 -> HTML」，图片上传由调用方完成，
这里只维护 {原图引用 -> mmbiz url} 的映射。转换在客户端本地完成，relay 不碰 markdown。
"""
import os
import re

_IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def scan_images(markdown_text: str):
    """返回 markdown 中所有图片引用 src 列表（去重，保留顺序）。"""
    return list(dict.fromkeys(m.group(2).strip() for m in _IMG_RE.finditer(markdown_text)))


def _esc(text: str) -> str:
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))


def _img_tag(alt: str, src: str, img_map: dict) -> str:
    final = img_map.get(src) or img_map.get(os.path.basename(src)) or src
    return (f'<img data-src="{final}" src="{final}" alt="{alt}" '
            'style="max-width:100%;height:auto;display:block;'
            'margin:14px auto;border-radius:6px;"/>')


def _inline(text: str, img_map: dict) -> str:
    """处理行内元素：图片、加粗、斜体、链接、行内代码。"""
    # 先抽出 inline code，避免其中的 * _ 被误当成强调
    codes = []

    def stash(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r'`([^`]+)`', stash, text)
    text = _IMG_RE.sub(lambda m: _img_tag(m.group(1), m.group(2), img_map), text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)',
                  r'<a href="\2" style="color:#07c160;text-decoration:none;">\1</a>', text)

    def restore(m):
        return ('<code style="font-size:13px;background:#f6f8fa;padding:1px 5px;'
                'border-radius:4px;font-family:Menlo,Consolas,monospace;">'
                f'{_esc(codes[int(m.group(1))])}</code>')

    return re.sub(r'\x00(\d+)\x00', restore, text)


_HEAD_STYLE = {
    1: "font-size:22px;font-weight:bold;margin:28px 0 12px;color:#1a1a1a;",
    2: "font-size:19px;font-weight:bold;margin:24px 0 10px;color:#1a1a1a;",
    3: "font-size:17px;font-weight:bold;margin:20px 0 8px;color:#333;",
}


def convert(markdown_text: str, img_map: dict) -> str:
    """把 markdown 转成微信图文 HTML。"""
    lines = markdown_text.split("\n")
    out = []
    para = []
    list_items = []
    list_type = None  # 'ul' / 'ol'

    def flush_para():
        if para:
            joined = " ".join(para).strip()
            if joined:
                out.append(
                    f"<p style='font-size:15px;line-height:1.8;color:#3f3f3f;"
                    f"margin:14px 0;'>{_inline(joined, img_map)}</p>"
                )
            para.clear()

    def flush_list():
        if list_items:
            tag = list_type
            items = "".join(
                f"<li style='margin:6px 0;'>{_inline(it, img_map)}</li>" for it in list_items
            )
            out.append(
                f"<{tag} style='padding-left:22px;margin:14px 0;font-size:15px;"
                f"line-height:1.8;color:#3f3f3f;'>{items}</{tag}>"
            )
            list_items.clear()

    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_para()
            flush_list()
            list_type = None
            i += 1
            continue

        # 代码块 ```
        if stripped.startswith("```"):
            flush_para()
            flush_list()
            list_type = None
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # 跳过结束的 ```
            code = _esc("\n".join(code_lines)).rstrip()
            out.append(
                "<section style='background:#f6f8fa;border:1px solid #eaeef2;"
                "border-radius:6px;padding:12px 14px;overflow-x:auto;margin:14px 0;'>"
                "<code style='font-size:13px;line-height:1.6;white-space:pre-wrap;"
                "word-break:break-all;color:#24292e;"
                "font-family:Menlo,Consolas,monospace;'>"
                f"{code}</code></section>"
            )
            continue

        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if m:
            flush_para()
            flush_list()
            list_type = None
            level = len(m.group(1))
            txt = m.group(2).strip()
            style = _HEAD_STYLE.get(level, "font-size:16px;font-weight:bold;margin:18px 0 8px;color:#333;")
            out.append(f"<h{level} style='{style}'>{_inline(txt, img_map)}</h{level}>")
            i += 1
            continue

        # 分割线
        if re.match(r'^(\-{3,}|\*{3,}|_{3,})$', stripped):
            flush_para()
            flush_list()
            list_type = None
            out.append("<hr style='border:none;border-top:1px solid #eaeaea;margin:20px 0;'/>")
            i += 1
            continue

        # 引用
        if stripped.startswith(">"):
            flush_para()
            flush_list()
            list_type = None
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(
                "<blockquote style='margin:14px 0;padding:10px 14px;"
                "background:#f6f8fa;border-left:4px solid #d0d7de;"
                "color:#57606a;font-size:14px;line-height:1.7;'>"
                f"{_inline(' '.join(quote), img_map)}</blockquote>"
            )
            continue

        # 无序列表
        m = re.match(r'^[-*+]\s+(.*)$', stripped)
        if m:
            flush_para()
            if list_type and list_type != "ul":
                flush_list()
            list_type = "ul"
            list_items.append(m.group(1).strip())
            i += 1
            continue

        # 有序列表
        m = re.match(r'^\d+[.)]\s+(.*)$', stripped)
        if m:
            flush_para()
            if list_type and list_type != "ol":
                flush_list()
            list_type = "ol"
            list_items.append(m.group(1).strip())
            i += 1
            continue

        # 普通段落
        flush_list()
        list_type = None
        para.append(stripped)
        i += 1

    flush_para()
    flush_list()
    body = "\n".join(out)
    return (
        "<section style='font-size:15px;color:#3f3f3f;letter-spacing:.2px;"
        "word-break:break-word;'>"
        f"{body}</section>"
    )
