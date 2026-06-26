#!/usr/bin/env python3
from __future__ import annotations
import argparse
from urllib.parse import urlparse
from wiki_ref_utils import load_text, extract_refs


def fallback_work(url: str) -> str:
    host = urlparse(url).netloc.replace('www.', '')
    return host or 'UNKNOWN'


def template_for(ref: dict) -> str:
    url = ref['urls'][0] if ref['urls'] else ''
    work = ref['work'] or fallback_work(url)
    title = ref['title'] or 'MISSING TITLE'
    pieces = [
        '{{cite web',
        f' |title={title}',
        f' |url={url or "MISSING URL"}',
        f' |work={work}',
    ]
    if ref['author']:
        pieces.append(f' |author={ref["author"]}')
    else:
        pieces.append(' |author=')
    if ref['date']:
        pieces.append(f' |date={ref["date"]}')
    else:
        pieces.append(' |date=')
    if ref['archive_url']:
        pieces.append(f' |archive-url={ref["archive_url"]}')
    pieces.append('}}')
    return ''.join(pieces)


def missing_fields(ref: dict) -> list[str]:
    misses = []
    if not ref['title']:
        misses.append('title')
    if not ref['urls']:
        misses.append('url')
    if not ref['work']:
        misses.append('work/publisher')
    if not ref['date']:
        misses.append('date')
    if not ref['author']:
        misses.append('author')
    if not ref['archive_url']:
        misses.append('archive-url')
    return misses


def main():
    ap = argparse.ArgumentParser(description='Suggest cleaner citation templates and flag missing fields')
    ap.add_argument('path', nargs='?', help='Draft file path, or omit/read stdin')
    args = ap.parse_args()
    text = load_text(args.path)
    refs = extract_refs(text)

    print(f'refs_total: {len(refs)}')
    for ref in refs:
        print(f'\n[{ref["index"]}] class={ref["classification"]} detail={ref["detail"]}')
        print(f'current: {ref["title"] or ref["preview"]}')
        misses = missing_fields(ref)
        print('missing_fields: ' + (', '.join(misses) if misses else 'none'))
        print('suggested_template:')
        print(template_for(ref))


if __name__ == '__main__':
    main()
