#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

REPLACEMENTS = [
    (r'\bleading\b', 'noted'),
    (r'\bworld-class\b', 'well-known'),
    (r'\bpremier\b', 'established'),
    (r'\binnovative\b', 'described by sources as notable'),
    (r'\btrusted\b', 'used by'),
    (r'\bpremium\b', 'higher-end'),
    (r'\bofficial supplier\b', 'supplier'),
    (r'\bindustry leader\b', 'company'),
]
REMOVE_PATTERNS = [r'\bstate-of-the-art\b', r'\bcutting-edge\b', r'\bworld-renowned\b']


def load_text(path: str | None) -> str:
    if not path or path == '-':
        return sys.stdin.read()
    return Path(path).read_text(encoding='utf-8')


def rewrite(text: str) -> tuple[str, list[str]]:
    notes = []
    out = text
    for pat, repl in REPLACEMENTS:
        if re.search(pat, out, flags=re.I):
            out = re.sub(pat, repl, out, flags=re.I)
            notes.append(f'replaced {pat} -> {repl}')
    for pat in REMOVE_PATTERNS:
        if re.search(pat, out, flags=re.I):
            out = re.sub(pat, '', out, flags=re.I)
            notes.append(f'removed {pat}')
    out = re.sub(r'\s+', ' ', out).strip()
    if not re.search(r'\b(according to|coverage in|reported by|described by)\b', out, flags=re.I):
        attributed = 'According to independent coverage, ' + out if out else out
    else:
        attributed = out
    return attributed, notes


def main():
    ap = argparse.ArgumentParser(description='Rewrite promo-ish text into more neutral, attributed wiki prose')
    ap.add_argument('path', nargs='?', help='Input text file path, or omit/read stdin')
    args = ap.parse_args()
    text = load_text(args.path)
    rewritten, notes = rewrite(text)
    print('neutral_rewrite:')
    print(rewritten)
    print('\nnotes:')
    if notes:
        for n in notes:
            print(f'- {n}')
    else:
        print('- no heuristic replacements applied')
    print('- manual fact-check still required')


if __name__ == '__main__':
    main()
