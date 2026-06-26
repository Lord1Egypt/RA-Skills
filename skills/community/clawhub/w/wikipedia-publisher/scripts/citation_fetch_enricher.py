#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import re
from html import unescape
from urllib.parse import urlparse

import requests

from wiki_ref_utils import load_text, extract_refs, classify_url

TITLE_PAT = re.compile(r'<title[^>]*>(.*?)</title>', re.I | re.S)
META_PAT = re.compile(r'<meta\s+[^>]*(?:name|property)=["\']([^"\']+)["\'][^>]*content=["\']([^"\']+)["\'][^>]*>|<meta\s+[^>]*content=["\']([^"\']+)["\'][^>]*(?:name|property)=["\']([^"\']+)["\'][^>]*>', re.I | re.S)
WS_PAT = re.compile(r'\s+')
UA = 'wikipedia-publisher/0.3 citation enricher'

TITLE_KEYS = ['og:title', 'twitter:title', 'headline', 'title']
AUTHOR_KEYS = ['author', 'article:author', 'parsely-author']
DATE_KEYS = ['article:published_time', 'publication_date', 'pubdate', 'date', 'parsely-pub-date', 'dc.date']
WORK_KEYS = ['og:site_name', 'application-name', 'twitter:site']
DESC_KEYS = ['description', 'og:description', 'twitter:description']


def clean(value: str) -> str:
    value = unescape(value or '')
    value = re.sub(r'<[^>]+>', ' ', value)
    value = WS_PAT.sub(' ', value).strip()
    return value


def parse_meta(html: str) -> dict[str, str]:
    meta = {}
    for m in META_PAT.finditer(html):
        k1, v1, v2, k2 = m.groups()
        key = (k1 or k2 or '').strip().lower()
        value = clean(v1 or v2 or '')
        if key and value and key not in meta:
            meta[key] = value
    return meta


def first(meta: dict[str, str], keys: list[str]) -> str:
    for key in keys:
        if key in meta and meta[key]:
            return meta[key]
    return ''


def fallback_title(html: str) -> str:
    m = TITLE_PAT.search(html)
    return clean(m.group(1)) if m else ''


def fetch_one(url: str, timeout: int = 20) -> dict:
    result = {'url': url}
    try:
        r = requests.get(url, headers={'User-Agent': UA}, timeout=timeout, allow_redirects=True)
        result['status_code'] = r.status_code
        result['final_url'] = r.url
        result['classification'], result['host'] = classify_url(r.url)
        html = r.text[:400000]
        meta = parse_meta(html)
        title = first(meta, TITLE_KEYS) or fallback_title(html)
        work = first(meta, WORK_KEYS) or urlparse(r.url).netloc.replace('www.', '')
        author = first(meta, AUTHOR_KEYS)
        date = first(meta, DATE_KEYS)
        desc = first(meta, DESC_KEYS)
        result.update({
            'title': title,
            'work': work,
            'author': author,
            'date': date,
            'description': desc,
        })
        result['suggested_cite'] = '{{cite web |title=%s |url=%s |work=%s%s%s}}' % (
            title or 'MISSING TITLE',
            r.url,
            work or 'MISSING WORK',
            f' |author={author}' if author else ' |author=',
            f' |date={date}' if date else ' |date=',
        )
    except Exception as e:
        result['error'] = f'{type(e).__name__}: {e}'
        result['classification'], result['host'] = classify_url(url)
    return result


def urls_from_args(args) -> list[str]:
    urls: list[str] = []
    if args.urls:
        urls.extend(args.urls)
    if args.draft:
        refs = extract_refs(load_text(args.draft))
        for ref in refs[: args.limit]:
            if ref['urls']:
                urls.append(ref['urls'][0])
    return list(dict.fromkeys(urls))


def main():
    ap = argparse.ArgumentParser(description='Fetch live citation metadata from URLs or a wiki draft')
    ap.add_argument('urls', nargs='*', help='URLs to enrich')
    ap.add_argument('--draft', help='Path to a wiki draft; extracts citation URLs')
    ap.add_argument('--limit', type=int, default=5, help='Max refs to extract from --draft')
    ap.add_argument('--json', action='store_true', help='Emit JSON')
    ap.add_argument('--timeout', type=int, default=20)
    args = ap.parse_args()

    urls = urls_from_args(args)
    if not urls:
        raise SystemExit('Provide URLs or --draft')

    results = [fetch_one(url, timeout=args.timeout) for url in urls]
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    for i, item in enumerate(results, start=1):
        print(f'[{i}] {item.get("final_url", item["url"])}')
        if 'error' in item:
            print(f'  error: {item["error"]}')
            print(f'  class: {item["classification"]} ({item["host"]})')
            continue
        print(f'  status: {item.get("status_code")}')
        print(f'  class: {item["classification"]} ({item["host"]})')
        print(f'  title: {item.get("title", "")}')
        print(f'  work: {item.get("work", "")}')
        print(f'  author: {item.get("author", "")}')
        print(f'  date: {item.get("date", "")}')
        if item.get('description'):
            print(f'  description: {item["description"][:160]}')
        print(f'  suggested_cite: {item["suggested_cite"]}')


if __name__ == '__main__':
    main()
