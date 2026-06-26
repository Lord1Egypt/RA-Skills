#!/usr/bin/env python3
"""
Convert Markdown to WeChat-compatible HTML.

Usage:
  python3 md_to_html.py article.md
  python3 md_to_html.py article.md --image-map images.json

Output: prints WeChat HTML to stdout

WeChat HTML rules:
- All CSS must be inline (no <style> tags, no external CSS)
- No <script> tags
- Images must use WeChat CDN URLs (http://mmbiz.qpic.cn/...)
- Supported tags: p, h1-h4, strong, em, ul, ol, li, blockquote, img, br, a, hr
- image-map: JSON file mapping local filenames to WeChat CDN URLs
  e.g. {"cover.jpg": "http://mmbiz.qpic.cn/...", "fig1.png": "http://..."}

Dependencies: none (stdlib only, basic markdown parsing)
For richer markdown, install: pip3 install markdown
"""

import json, re, sys
from pathlib import Path

# WeChat-safe inline styles
STYLES = {
    "body":       "font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif; font-size: 17px; line-height: 1.8; color: #333; padding: 0 16px;",
    "h1":         "font-size: 24px; font-weight: bold; color: #1a1a1a; margin: 24px 0 12px; line-height: 1.4;",
    "h2":         "font-size: 20px; font-weight: bold; color: #1a1a1a; margin: 20px 0 10px; border-left: 4px solid #07C160; padding-left: 10px;",
    "h3":         "font-size: 18px; font-weight: bold; color: #333; margin: 16px 0 8px;",
    "p":          "margin: 12px 0; line-height: 1.8;",
    "blockquote": "border-left: 4px solid #07C160; margin: 16px 0; padding: 8px 16px; background: #f9f9f9; color: #666;",
    "li":         "margin: 6px 0; line-height: 1.8;",
    "ul":         "margin: 12px 0; padding-left: 24px;",
    "ol":         "margin: 12px 0; padding-left: 24px;",
    "strong":     "font-weight: bold; color: #1a1a1a;",
    "em":         "font-style: italic;",
    "hr":         "border: none; border-top: 1px solid #eee; margin: 24px 0;",
    "img":        "max-width: 100%; height: auto; display: block; margin: 16px auto;",
    "code":       "background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 14px; font-family: monospace;",
}


def try_import_markdown():
    """Try to use the markdown library; fall back to basic regex parser."""
    try:
        import markdown
        return True
    except ImportError:
        return False


def basic_md_to_html(md_text: str) -> str:
    """Basic markdown converter using regex (no external deps).

    Supports a minimal subset of Markdown plus fenced code blocks (``` ... ```).
    WeChat has limited HTML support, so code blocks are rendered as a <p><code>...
    with <br/> line breaks.
    """
    lines = md_text.split("\n")
    html_lines = []
    in_ul = False
    in_ol = False
    in_blockquote = False
    in_codeblock = False
    code_lines = []

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            html_lines.append("</ul>")
            in_ul = False
        if in_ol:
            html_lines.append("</ol>")
            in_ol = False

    def inline(text):
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', f'<strong style="{STYLES["strong"]}">\\1</strong>', text)
        text = re.sub(r'__(.+?)__', f'<strong style="{STYLES["strong"]}">\\1</strong>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', f'<em style="{STYLES["em"]}">\\1</em>', text)
        # Inline code
        text = re.sub(r'`(.+?)`', f'<code style="{STYLES["code"]}">\\1</code>', text)
        # Links
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
        return text

    def escape_html(s: str) -> str:
        return (s.replace('&', '&amp;')
                 .replace('<', '&lt;')
                 .replace('>', '&gt;'))

    def render_codeblock(lines_: list[str]) -> str:
        rendered = []
        for ln in lines_:
            # preserve leading spaces (YAML etc.)
            m = re.match(r'^(\s+)(.*)$', ln)
            if m:
                lead = '&nbsp;' * len(m.group(1))
                rendered.append(lead + escape_html(m.group(2)))
            else:
                rendered.append(escape_html(ln))
        inner = '<br/>'.join(rendered)
        return f'<p style="{STYLES["p"]}"><code style="{STYLES["code"]}">{inner}</code></p>'

    for line in lines:
        stripped = line.strip()

        # Fenced code blocks
        if stripped.startswith("```"):
            # toggle
            if not in_codeblock:
                close_lists()
                if in_blockquote:
                    html_lines.append("</blockquote>")
                    in_blockquote = False
                in_codeblock = True
                code_lines = []
            else:
                # close and render
                html_lines.append(render_codeblock(code_lines))
                in_codeblock = False
                code_lines = []
            continue

        if in_codeblock:
            code_lines.append(line.rstrip("\n"))
            continue

        # Blank line
        if not stripped:
            close_lists()
            if in_blockquote:
                html_lines.append("</blockquote>")
                in_blockquote = False
            continue

        # HR
        if re.match(r'^[-*_]{3,}$', stripped):
            close_lists()
            html_lines.append(f'<hr style="{STYLES["hr"]}">')
            continue

        # Headings
        m = re.match(r'^(#{1,4})\s+(.+)', stripped)
        if m:
            close_lists()
            level = len(m.group(1))
            tag = f"h{level}"
            style = STYLES.get(tag, STYLES["h3"])
            html_lines.append(f'<{tag} style="{style}">{inline(m.group(2))}</{tag}>')
            continue

        # Blockquote
        if stripped.startswith("> "):
            if not in_blockquote:
                html_lines.append(f'<blockquote style="{STYLES["blockquote"]}">')
                in_blockquote = True
            html_lines.append(f'<p style="{STYLES["p"]}">{inline(stripped[2:])}</p>')
            continue
        elif in_blockquote:
            html_lines.append("</blockquote>")
            in_blockquote = False

        # Unordered list
        m = re.match(r'^[-*+]\s+(.+)', stripped)
        if m:
            if not in_ul:
                close_lists()
                html_lines.append(f'<ul style="{STYLES["ul"]}">')
                in_ul = True
            html_lines.append(f'<li style="{STYLES["li"]}">{inline(m.group(1))}</li>')
            continue

        # Ordered list
        m = re.match(r'^\d+\.\s+(.+)', stripped)
        if m:
            if not in_ol:
                close_lists()
                html_lines.append(f'<ol style="{STYLES["ol"]}">')
                in_ol = True
            html_lines.append(f'<li style="{STYLES["li"]}">{inline(m.group(1))}</li>')
            continue

        close_lists()

        # Image
        m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)', stripped)
        if m:
            alt, src = m.group(1), m.group(2)
            html_lines.append(f'<img src="{src}" alt="{alt}" style="{STYLES["img"]}">')
            continue

        # Paragraph
        html_lines.append(f'<p style="{STYLES["p"]}">{inline(stripped)}</p>')

    close_lists()
    if in_blockquote:
        html_lines.append("</blockquote>")

    return "\n".join(html_lines)


def strip_empty_list_items(html: str) -> str:
    """Remove empty list items that can render as blank bullets in WeChat."""
    # Remove <li ...>   </li>
    html = re.sub(r'<li\b[^>]*>\s*</li>', '', html)
    # Remove <li ...><p ...>\s*</p></li>
    html = re.sub(r'<li\b[^>]*>\s*<p\b[^>]*>\s*</p>\s*</li>', '', html)
    return html


def apply_image_map(html: str, image_map: dict) -> str:
    """Replace local image filenames with WeChat CDN URLs."""
    for local_name, wx_url in image_map.items():
        html = html.replace(f'src="{local_name}"', f'src="{wx_url}"')
        # Also handle paths
        html = re.sub(
            rf'src="[^"]*{re.escape(local_name)}"',
            f'src="{wx_url}"',
            html
        )
    return html


def convert(md_path: str, image_map_path: str = None) -> str:
    md_text = Path(md_path).read_text(encoding="utf-8")

    # Remove markdown frontmatter (---...---) if present
    md_text = re.sub(r'^---\n.*?\n---\n', '', md_text, flags=re.DOTALL)

    if try_import_markdown():
        import markdown
        html = markdown.markdown(md_text, extensions=["extra"])
        # Apply inline styles (basic pass)
        for tag, style in STYLES.items():
            html = re.sub(rf'<{tag}>', f'<{tag} style="{style}">', html)
    else:
        html = basic_md_to_html(md_text)

    # Apply image map
    if image_map_path:
        image_map = json.loads(Path(image_map_path).read_text())
        html = apply_image_map(html, image_map)

    # Strip empty list items (prevents blank bullets in WeChat)
    html = strip_empty_list_items(html)

    return html


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 md_to_html.py article.md [--image-map images.json]", file=sys.stderr)
        sys.exit(1)

    md_path = sys.argv[1]
    image_map_path = None
    if "--image-map" in sys.argv:
        idx = sys.argv.index("--image-map")
        if idx + 1 < len(sys.argv):
            image_map_path = sys.argv[idx + 1]

    print(convert(md_path, image_map_path))
