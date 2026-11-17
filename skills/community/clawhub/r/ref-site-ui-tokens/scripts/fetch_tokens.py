#!/usr/bin/env python3
"""抓取一个网站的设计 token（CSS 自定义属性），标准库、无浏览器。

用法：
    python fetch_tokens.py https://linear.app/
    python fetch_tokens.py https://linear.app/ --grep color
    python fetch_tokens.py https://linear.app/ --json tokens.json
    python fetch_tokens.py https://linear.app/ --top 80

流程：抓首页 HTML -> 提出所有 <link rel=stylesheet> -> 逐个下载合并
      -> 解析 `--var: value` -> 去重、分组、打印。
"""
import argparse
import json
import re
import sys
import urllib.request
from urllib.parse import urljoin

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,text/css,*/*',
        'Accept-Language': 'en-US,en;q=0.9',
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    for enc in ('utf-8', 'latin-1'):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode('utf-8', 'ignore')


LINK_RE = re.compile(r'<link[^>]+rel=["\']?stylesheet["\']?[^>]*>', re.I)
HREF_RE = re.compile(r'href=["\']([^"\']+)["\']')
IMPORT_RE = re.compile(r'@import\s+(?:url\()?["\']?([^"\')]+)["\']?\)?')
VAR_RE = re.compile(r'(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]+)[;}]')


def collect_css(page_url, html, seen, out):
    """顺着 link / @import 把样式表抓回来（含一层 @import 递归）。"""
    urls = []
    for tag in LINK_RE.findall(html):
        m = HREF_RE.search(tag)
        if m:
            urls.append(m.group(1))
    for css_text in list(out):
        urls.extend(IMPORT_RE.findall(css_text))

    for href in urls:
        full = urljoin(page_url, href)
        if full in seen or not full.lower().endswith('.css'):
            continue
        seen.add(full)
        try:
            text = get(full)
        except Exception as exc:
            print('  [skip] %s (%s)' % (full[:90], exc), file=sys.stderr)
            continue
        out.append(text)
        print('  [css ] %5d KB  %s' % (len(text) // 1024, full[:90]))
        # 只递归一层，够用了
        for sub in IMPORT_RE.findall(text):
            f2 = urljoin(full, sub)
            if f2 not in seen and f2.lower().endswith('.css'):
                seen.add(f2)
                try:
                    out.append(get(f2))
                except Exception:
                    pass


def group(name):
    n = name.lower()
    for key in ('color', 'bg', 'border', 'text', 'font', 'radius', 'space',
                'shadow', 'opacity', 'blur', 'z-', 'edge', 'glass', 'size'):
        if key in n:
            return key
    return 'other'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('--grep', help='只看变量名/值里含这个串的')
    ap.add_argument('--json', help='顺手把结果写成 json')
    ap.add_argument('--top', type=int, default=0, help='每个分组最多打印几行')
    args = ap.parse_args()

    if not args.url.startswith('http'):
        args.url = 'https://' + args.url

    print('[*] 抓首页 %s' % args.url)
    html = get(args.url)
    print('    %d KB' % (len(html) // 1024))

    chunks, seen = [], set()
    collect_css(args.url, html, seen, chunks)
    all_css = '\n'.join(chunks)
    print('[*] 合并 CSS %d KB（%d 个文件）' % (len(all_css) // 1024, len(chunks)))

    tokens, order = {}, []
    for name, val in VAR_RE.findall(all_css):
        val = val.strip()
        # 跳过明显是函数体内的局部值
        if val.startswith('(') or len(val) > 90:
            continue
        if name not in tokens:
            order.append(name)
        tokens[name] = val

    print('[*] 解析出 %d 个自定义属性\n' % len(tokens))

    buckets = {}
    for name in order:
        if args.grep and args.grep.lower() not in (name + tokens[name]).lower():
            continue
        buckets.setdefault(group(name), []).append((name, tokens[name]))

    for key in sorted(buckets):
        items = buckets[key]
        print('── %s (%d) %s' % (key, len(items), '─' * 40))
        for name, val in (items[:args.top] if args.top else items):
            print('   %-34s %s' % (name, val))
        if args.top and len(items) > args.top:
            print('   ... 还有 %d 个' % (len(items) - args.top))
        print()

    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(tokens, f, ensure_ascii=False, indent=2)
        print('[*] 已写入 %s' % args.json)


if __name__ == '__main__':
    main()
