#!/usr/bin/env python3
"""
Fetch a WeChat public account article and return structured blocks for Notion.
Usage: python3 fetch_wechat.py <url>
Output: JSON to stdout with keys: title, blocks
Block types: image (url), paragraph (rich_text), heading_2 (rich_text), 
             bulleted_list_item (rich_text), code (text)
rich_text: list of {type, text: {content}, annotations?: {bold, italic}}
"""

import sys
import re
import json
import subprocess
from urllib.parse import urlparse

ALLOWED_HOSTS = {"mp.weixin.qq.com"}

def validate_url(url):
    """Enforce URL whitelist to prevent SSRF via internal/arbitrary endpoints."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        print(f"ERROR: URL scheme must be http or https, got: {parsed.scheme}", file=sys.stderr)
        sys.exit(1)
    if parsed.hostname not in ALLOWED_HOSTS:
        print(f"ERROR: URL host must be one of {ALLOWED_HOSTS}, got: {parsed.hostname}", file=sys.stderr)
        sys.exit(1)

def fetch_html(url):
    result = subprocess.run([
        'curl', '-s', url,
        '-H', 'User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        '-H', 'Accept-Language: zh-CN,zh;q=0.9',
        '--max-time', '15'
    ], capture_output=True, text=True)
    return result.stdout

def parse_rich_text(html_frag):
    runs = []
    pattern = re.compile(r'(<strong[^>]*>.*?</strong>|<b[^>]*>.*?</b>|<em[^>]*>.*?</em>|<i[^>]*>.*?</i>)', re.DOTALL)
    parts = pattern.split(html_frag)
    for part in parts:
        bold = bool(re.match(r'<(strong|b)[^>]*>', part))
        italic = bool(re.match(r'<(em|i)[^>]*>', part))
        text = re.sub(r'<[^>]+>', '', part)
        text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').strip()
        if not text:
            continue
        run = {'type': 'text', 'text': {'content': text}}
        if bold or italic:
            run['annotations'] = {}
            if bold: run['annotations']['bold'] = True
            if italic: run['annotations']['italic'] = True
        runs.append(run)
    return runs

def parse(url):
    html = fetch_html(url)

    # Title
    title_match = re.search(r'id="activity-name"[^>]*>\s*(.*?)\s*</span>', html, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else ''

    # Cover image (og:image)
    og_match = re.search(r'property="og:image"\s+content="([^"]+)"', html)
    if not og_match:
        og_match = re.search(r'content="([^"]+)"\s+property="og:image"', html)
    cover_url = og_match.group(1) if og_match else None

    # Body
    content_match = re.search(r'id="js_content"[^>]*>(.*?)<div[^>]+id="js_pc_qr_code"', html, re.DOTALL)

    blocks = []
    if content_match:
        raw = content_match.group(1)
        tokens = re.split(
            r'(<img[^>]+>|<pre[^>]*>.*?</pre>|<ul[^>]*>.*?</ul>|<ol[^>]*>.*?</ol>|<p[^>]*>.*?</p>|<h[1-6][^>]*>.*?</h[1-6]>)',
            raw, flags=re.DOTALL
        )
        first_block = True
        for tok in tokens:
            tok = tok.strip()
            if not tok:
                continue
            # Image
            img_match = re.search(r'data-src="([^"]+)"', tok)
            if not img_match:
                img_match = re.search(r'src="(https://mmbiz[^"]+)"', tok)
            if img_match and not re.search(r'<(p|h[1-6])[^>]*>', tok):
                url_img = img_match.group(1)
                if 'mmbiz' in url_img:
                    blocks.append({'type': 'image', 'url': url_img})
                    first_block = False
                continue
            # Code block
            if re.match(r'<pre', tok, re.IGNORECASE):
                code = re.sub(r'<[^>]+>', '', tok)
                code = code.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').strip()
                if code:
                    blocks.append({'type': 'code', 'text': code})
                continue
            # List
            if re.match(r'<[uo]l', tok, re.IGNORECASE):
                for item in re.findall(r'<li[^>]*>(.*?)</li>', tok, re.DOTALL):
                    plain = re.sub(r'<[^>]+>', '', item).replace('&nbsp;', ' ').strip()
                    if plain:
                        rt = parse_rich_text(item)
                        blocks.append({'type': 'bulleted_list_item', 'rich_text': rt or [{'type': 'text', 'text': {'content': plain}}]})
                continue
            # Text
            plain = re.sub(r'<[^>]+>', '', tok).replace('&nbsp;', ' ').strip()
            if not plain or plain.startswith('var ') or plain.startswith('window.'):
                continue
            if first_block and plain.strip() == title.strip():
                first_block = False
                continue
            first_block = False
            h_match = re.match(r'<h([1-3])', tok)
            if h_match:
                blocks.append({'type': 'heading_2', 'rich_text': parse_rich_text(tok) or [{'type': 'text', 'text': {'content': plain}}]})
            else:
                rt = parse_rich_text(tok)
                if rt:
                    blocks.append({'type': 'paragraph', 'rich_text': rt})

    # Prepend cover image
    if cover_url:
        blocks.insert(0, {'type': 'image', 'url': cover_url})

    return {'title': title, 'blocks': blocks}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: fetch_wechat.py <url>', file=sys.stderr)
        sys.exit(1)
    validate_url(sys.argv[1])
    result = parse(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
