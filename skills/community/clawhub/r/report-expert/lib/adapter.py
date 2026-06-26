"""输入适配模块 — 将不同类型的输入内容转为符合报告产出规范的 HTML

支持的输入类型：
- HTML（直接使用）
- Markdown（转为 HTML）
- URL（抓取网页内容提取正文）
- 纯文本（转为带标题的 HTML 段落）

职责边界：
- 只做格式转换，不做内容修改（lint/修复交给 html_lint）
- 输出为纯净 HTML（无框架 wrapper、无 script、无 chrome）
"""

import re
from pathlib import Path


def detect_type(source):
    """检测输入内容类型

    Args:
        source: 文件路径字符串或 URL 字符串

    Returns:
        类型标识: 'html' | 'markdown' | 'url' | 'text'
    """
    # URL pattern
    if re.match(r'^https?://', source):
        return 'url'

    path = Path(source)
    ext = path.suffix.lower()

    if ext in ('.html', '.htm'):
        return 'html'
    elif ext in ('.md', '.markdown'):
        return 'markdown'
    else:
        # Try content-based detection
        try:
            content = path.read_text('utf-8', errors='ignore')[:2000]
            # If content looks like HTML (has common HTML tags)
            if re.search(r'<(html|body|div|table|h[1-6]|p|img|script|style|head)\b', content, re.IGNORECASE):
                return 'html'
            # If content looks like Markdown (has headers, lists, code blocks)
            if re.search(r'^#{1,6}\s|^>\s|^\*\s|^-\s|^```|^\|.*\|', content, re.MULTILINE):
                return 'markdown'
        except (OSError, UnicodeDecodeError):
            pass

        return 'text'


def adapt(source, title=None):
    """将输入内容适配为 HTML

    Args:
        source: 文件路径或 URL
        title: 报告标题（不填则自动提取）

    Returns:
        (html_content, title, source_type) — HTML内容, 标题, 输入类型
    """
    input_type = detect_type(source)

    if input_type == 'html':
        html = Path(source).read_text('utf-8')
        if not title:
            title_match = re.search(r'<title>(.*?)</title>', html)
            title = title_match.group(1).strip() if title_match else Path(source).stem
        return html, title, 'html'

    elif input_type == 'markdown':
        html = _markdown_to_html(source, title)
        return html, title or Path(source).stem, 'markdown'

    elif input_type == 'url':
        html = _url_to_html(source, title)
        return html, title or '网页报告', 'url'

    else:  # text
        html = _text_to_html(source, title)
        return html, title or Path(source).stem, 'text'


def _markdown_to_html(filepath, title=None):
    """Markdown 转 HTML，使用 markdown 库渲染"""
    md_content = Path(filepath).read_text('utf-8')

    # Extract title from first # header if not provided
    if not title:
        first_h1 = re.search(r'^#\s+(.+)', md_content, re.MULTILINE)
        if first_h1:
            title = first_h1.group(1).strip()
        else:
            title = Path(filepath).stem

    # Remove the first H1 line to avoid duplication with template header
    md_content = re.sub(r'^#\s+.*\n', '', md_content, count=1)

    try:
        import markdown
        html_body = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'codehilite', 'toc'],
            extension_configs={'codehilite': {'linenums': False}}
        )
    except ImportError:
        # Fallback: basic regex conversion
        html_body = _markdown_basic(md_content)

    # Wrap in minimal HTML structure
    html = f"""<!DOCTYPE html>
<html><head><title>{title}</title></head>
<body>
{html_body}
</body></html>"""
    return html


def _markdown_basic(md):
    """简单 Markdown → HTML（markdown 库不可用时的兜底）"""
    # Headers
    md = re.sub(r'^###\s+(.+)', r'<h3>\1</h3>', md, flags=re.MULTILINE)
    md = re.sub(r'^##\s+(.+)', r'<h2>\1</h2>', md, flags=re.MULTILINE)
    md = re.sub(r'^#\s+(.+)', r'<h1>\1</h1>', md, flags=re.MULTILINE)
    # Bold/italic
    md = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', md)
    md = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md)
    md = re.sub(r'\*(.+?)\*', r'<em>\1</em>', md)
    # Code
    md = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="\1">\2</code></pre>', md, flags=re.DOTALL)
    md = re.sub(r'`(.+?)`', r'<code>\1</code>', md)
    # Links
    md = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', md)
    # Images
    md = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', md)
    # Paragraphs (lines not starting with HTML tags)
    lines = md.split('\n')
    html_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('<'):
            html_lines.append(f'<p>{stripped}</p>')
        elif stripped:
            html_lines.append(stripped)
    return '\n'.join(html_lines)


def _url_to_html(url, title=None):
    """从 URL 抓取网页内容，提取正文转为 HTML

    使用 fetch_web 或 curl 抓取，然后提取 body 内容。
    """
    # Try curl first
    import subprocess
    try:
        result = subprocess.run(
            ['curl', '-sL', '--max-time', '30', url],
            capture_output=True, text=True
        )
        if result.returncode != 0 or not result.stdout.strip():
            raise RuntimeError(f"curl 失败: {url}")
        html = result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # Fallback to urllib
        from urllib.request import urlopen
        from urllib.error import URLError
        try:
            with urlopen(url, timeout=30) as resp:
                html = resp.read().decode('utf-8', errors='replace')
        except (URLError, OSError) as e:
            raise RuntimeError(f"无法抓取 URL: {url} — {e}")

    # Extract title
    if not title:
        title_match = re.search(r'<title>(.*?)</title>', html)
        title = title_match.group(1).strip() if title_match else url

    # Extract body content
    body_match = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL)
    if body_match:
        body = body_match.group(1).strip()
    else:
        body = html

    # Clean up: remove scripts, nav, sidebar, etc.
    for tag in ['script', 'nav', 'aside', 'iframe', 'noscript']:
        body = re.sub(rf'<{tag}[^>]*>.*?</{tag}>', '', body, flags=re.DOTALL)

    # Remove inline scripts
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)

    return f"""<!DOCTYPE html>
<html><head><title>{title}</title></head>
<body>
{body}
</body></html>"""


def _text_to_html(filepath, title=None):
    """纯文本转 HTML：段落包裹，保留换行结构"""
    content = Path(filepath).read_text('utf-8')
    if not title:
        title = Path(filepath).stem

    # Split into paragraphs by double newline
    paragraphs = content.split('\n\n')
    html_parts = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # Single newlines within paragraph → line breaks
        lines = para.split('\n')
        formatted = '<br>\n'.join(lines)
        html_parts.append(f'<p>{formatted}</p>')

    body = '\n'.join(html_parts)

    return f"""<!DOCTYPE html>
<html><head><title>{title}</title></head>
<body>
{body}
</body></html>"""