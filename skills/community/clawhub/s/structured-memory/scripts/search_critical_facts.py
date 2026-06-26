#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CARDS_DIR = ROOT / 'critical-facts' / 'cards'
FACTS_DIR = ROOT / 'critical-facts'


def search_cards(query: str):
    q = query.lower()
    hits = []
    for path in sorted(CARDS_DIR.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        if q in text.lower() or q in path.stem.lower():
            hits.append(str(path.relative_to(ROOT)))
    return hits


def search_fact_files(query: str):
    q = query.lower()
    hits = []
    for path in sorted(FACTS_DIR.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        if q in text.lower() or q in path.stem.lower():
            hits.append(str(path.relative_to(ROOT)))
    return hits


def main():
    parser = argparse.ArgumentParser(description='Search critical-fact cards first, then raw critical-facts files.')
    parser.add_argument('query', help='Keyword, host, path fragment, service name, project, or entity')
    args = parser.parse_args()

    cards = search_cards(args.query)
    facts = search_fact_files(args.query)

    print('cards:')
    for item in cards:
        print(f'- {item}')
    print('facts:')
    for item in facts:
        print(f'- {item}')


if __name__ == '__main__':
    main()
