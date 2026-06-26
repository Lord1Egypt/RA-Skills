#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_SELECTORS = [
    'article',
    'main',
    '.post-content',
    '[class*="body"]',
    'body',
]

WECHAT_NOISE_PATTERNS = [
    r'预览时标签不可点.*',
    r'Scan to Follow.*',
    r'继续滑动看下一个.*',
    r'轻触阅读原文.*',
    r'微信扫一扫可打开此内容.*',
    r'使用完整服务.*',
    r'Scan with Weixin to.*',
    r'use this Mini Program.*',
    r'Video Mini Program Like.*',
    r'轻点两下取消赞.*',
    r'轻点两下取消在看.*',
    r'Share Comment Favorite.*',
    r'哎咆科技.*向上滑动看下一个.*',
    r'\[Got It\].*',
    r'\[Cancel\].*\[Allow\].*',
    r'× 分析.*',
    r'!\[跳转二维码\]\(\)',
    r'!\[作者头像\]\([^\)]*\)',
]

WECHAT_TRUNCATE_MARKERS = [
    '预览时标签不可点',
    'Scan to Follow',
    '继续滑动看下一个',
    '轻触阅读原文',
    '微信扫一扫可打开此内容',
    'Scan with Weixin to',
    'use this Mini Program',
    '× 分析',
]


def fail(msg, code=1, as_json=False):
    if as_json:
        print(json.dumps({'ok': False, 'error': msg}, ensure_ascii=False))
    else:
        print(f'[error] {msg}', file=sys.stderr)
    sys.exit(code)


def parse_args(argv):
    if len(argv) < 2:
        return None
    urls = []
    max_chars = 30000
    as_json = False
    batch_file = None
    selector_overrides_path = None
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == '--json':
            as_json = True
        elif arg == '--batch' and i + 1 < len(argv):
            batch_file = argv[i + 1]
            i += 1
        elif arg == '--selectors' and i + 1 < len(argv):
            selector_overrides_path = argv[i + 1]
            i += 1
        elif arg.isdigit():
            max_chars = int(arg)
        else:
            urls.append(arg)
        i += 1
    if batch_file:
        urls.extend([line.strip() for line in Path(batch_file).read_text(encoding='utf-8').splitlines() if line.strip()])
    return urls, max_chars, as_json, selector_overrides_path


def ensure_deps(as_json=False):
    try:
        from scrapling import Fetcher
    except Exception as e:
        fail(f'scrapling import failed: {e}. install with: python3 -m pip install scrapling html2text', 2, as_json)
    try:
        from html2text import HTML2Text
    except Exception as e:
        fail(f'html2text import failed: {e}. install with: python3 -m pip install scrapling html2text', 2, as_json)
    return Fetcher, HTML2Text


def load_overrides(path_str):
    if not path_str:
        return {}
    path = Path(path_str)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def build_selectors(url, overrides):
    host = urlparse(url).hostname or ''
    custom = overrides.get(host, [])
    merged = []
    for item in custom + DEFAULT_SELECTORS:
        if item not in merged:
            merged.append(item)
    return merged


def score_markdown(md):
    text = md.strip()
    if not text:
        return 0
    score = 0
    score += min(len(text) // 500, 10)
    if '\n' in text:
        score += 2
    if '#' in text or '-' in text:
        score += 1
    if len(text.split()) > 80:
        score += 2
    return score


def clean_wechat_noise(markdown, url):
    host = urlparse(url).hostname or ''
    if 'mp.weixin.qq.com' not in host:
        return markdown, False

    original = markdown
    for marker in WECHAT_TRUNCATE_MARKERS:
        idx = markdown.find(marker)
        if idx != -1:
            markdown = markdown[:idx].rstrip()
            break

    lines = []
    for line in markdown.splitlines():
        stripped = line.strip()
        noisy = False
        for pattern in WECHAT_NOISE_PATTERNS:
            if re.search(pattern, stripped, re.IGNORECASE):
                noisy = True
                break
        if not noisy:
            lines.append(line)

    markdown = '\n'.join(lines)
    markdown = re.sub(r'\n{3,}', '\n\n', markdown).strip()
    return markdown, markdown != original


def fetch_one(url, max_chars, as_json, overrides, Fetcher, HTML2Text):
    parts = urlparse(url)
    if parts.scheme not in ('http', 'https'):
        return {'ok': False, 'url': url, 'error': 'url must start with http:// or https://'}

    Fetcher.configure(auto_match=True)
    fetcher = Fetcher()
    page = fetcher.get(url)
    html = getattr(page, 'html', '') or ''
    used_selector = None
    selected_html = ''

    for selector in build_selectors(url, overrides):
        try:
            nodes = page.css(selector)
        except Exception:
            nodes = []
        if nodes:
            node = nodes[0]
            selected_html = getattr(node, 'html', '') or str(node)
            used_selector = selector
            break

    if not selected_html:
        selected_html = html
        used_selector = 'raw_html'

    h = HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    markdown = h.handle(selected_html).strip()
    markdown, wechat_noise_cleaned = clean_wechat_noise(markdown, url)
    markdown = markdown[:max_chars]

    title = getattr(page, 'title', None) or ''
    final_url = getattr(page, 'url', None) or url
    quality = score_markdown(markdown)

    return {
        'ok': True,
        'url': url,
        'final_url': final_url,
        'title': title,
        'selector': used_selector,
        'content_length': len(markdown),
        'quality_score': quality,
        'wechat_noise_cleaned': wechat_noise_cleaned,
        'content': markdown,
    }


def main():
    parsed = parse_args(sys.argv)
    if not parsed:
        print('Usage: python3 scrapling_fetch.py <url> [max_chars] [--json] [--batch urls.txt] [--selectors overrides.json]', file=sys.stderr)
        sys.exit(1)

    urls, max_chars, as_json, selector_overrides_path = parsed
    if not urls:
        fail('no url provided', 1, as_json)

    Fetcher, HTML2Text = ensure_deps(as_json)
    overrides = load_overrides(selector_overrides_path)

    results = []
    for url in urls:
        try:
            results.append(fetch_one(url, max_chars, as_json, overrides, Fetcher, HTML2Text))
        except Exception as e:
            results.append({'ok': False, 'url': url, 'error': f'fetch failed: {e}'})

    if as_json or len(results) > 1:
        print(json.dumps(results if len(results) > 1 else results[0], ensure_ascii=False))
    else:
        result = results[0]
        if not result.get('ok'):
            fail(result.get('error', 'unknown error'), 3, False)
        print(f"[selector] {result['selector']}", file=sys.stderr)
        if result.get('title'):
            print(f"[title] {result['title']}", file=sys.stderr)
        print(f"[quality] {result['quality_score']}", file=sys.stderr)
        if result.get('wechat_noise_cleaned'):
            print('[wechat_noise_cleaned] true', file=sys.stderr)
        print(result['content'])


if __name__ == '__main__':
    main()
