#!/usr/bin/env python3
from __future__ import annotations
import argparse
from wiki_ref_utils import load_text, extract_refs, count_weak


def main():
    ap = argparse.ArgumentParser(description='Classify citation/source hygiene for a wiki draft')
    ap.add_argument('path', nargs='?', help='Draft file path, or omit/read stdin')
    args = ap.parse_args()
    text = load_text(args.path)
    refs = extract_refs(text)

    counts = {}
    rows = []
    for ref in refs:
        cls = ref['classification']
        counts[cls] = counts.get(cls, 0) + 1
        label = ref['title'] or (ref['urls'][0] if ref['urls'] else ref['preview'])
        rows.append((ref['index'], cls, ref['detail'], label))

    print(f'refs_total: {len(refs)}')
    for key in sorted(counts):
        print(f'{key}: {counts[key]}')

    print('\nDetailed review:')
    for i, cls, detail, label in rows:
        print(f'[{i}] {cls} | {detail} | {label}')

    weak = count_weak(refs)
    if weak == 0:
        print('\nhygiene: strong')
    elif weak <= max(2, len(refs) // 4):
        print('\nhygiene: mixed')
    else:
        print('\nhygiene: weak')


if __name__ == '__main__':
    main()
