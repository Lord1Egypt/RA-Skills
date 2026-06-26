#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys

import requests
import trafilatura
from bs4 import BeautifulSoup


def fallback_markdown(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'noscript']):
        tag.decompose()
    title = (soup.title.string or '').strip() if soup.title and soup.title.string else ''
    parts = []
    if title:
        parts.append(f'# {title}')
    texts = []
    for node in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
        text = node.get_text(' ', strip=True)
        text = re.sub(r'\s+', ' ', text).strip()
        if not text:
            continue
        if node.name in ('h1', 'h2', 'h3'):
            level = {'h1': '#', 'h2': '##', 'h3': '###'}[node.name]
            texts.append(f'{level} {text}')
        elif node.name == 'li':
            texts.append(f'- {text}')
        else:
            texts.append(text)
    if texts:
        parts.append('\n\n'.join(texts[:400]))
    return '\n\n'.join([p for p in parts if p]).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', required=True)
    ap.add_argument('--timeout', type=int, default=30)
    ap.add_argument('--max-chars', type=int, default=20000)
    args = ap.parse_args()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        resp = requests.get(args.url, headers=headers, timeout=args.timeout)
        resp.raise_for_status()
    except Exception as e:
        out = {
            'ok': False,
            'source_url': args.url,
            'engine': 'trafilatura',
            'markdown': None,
            'artifacts': {},
            'sources': [args.url],
            'notes': [f'fetch failed: {e}'],
        }
        print(json.dumps(out, ensure_ascii=False))
        return 2

    html = resp.text
    markdown = trafilatura.extract(
        html,
        url=args.url,
        output_format='markdown',
        include_links=True,
        include_formatting=True,
        favor_precision=True,
        deduplicate=True,
    )
    engine = 'trafilatura'
    notes = []
    if not markdown:
        markdown = fallback_markdown(html)
        engine = 'beautifulsoup'
        notes.append('trafilatura returned empty; fell back to BeautifulSoup extraction')

    markdown = (markdown or '').strip()
    if args.max_chars > 0 and len(markdown) > args.max_chars:
        markdown = markdown[:args.max_chars].rstrip() + '\n\n...[truncated]'
        notes.append(f'truncated to {args.max_chars} chars')

    out = {
        'ok': bool(markdown),
        'source_url': args.url,
        'engine': engine,
        'markdown': markdown or None,
        'artifacts': {
            'status_code': resp.status_code,
            'content_type': resp.headers.get('content-type', ''),
            'final_url': resp.url,
        },
        'sources': [args.url, resp.url] if resp.url != args.url else [args.url],
        'notes': notes,
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0 if markdown else 1


if __name__ == '__main__':
    raise SystemExit(main())
