#!/usr/bin/env python3
from __future__ import annotations
import argparse
from wiki_ref_utils import load_text, extract_refs, count_independent, count_weak

SUBSTANTIAL_HINTS = ['profile', 'feature', 'interview', 'explainer', 'case study']
ROUTINE_HINTS = ['announced', 'launches', 'opens', 'appoints', 'wins contract', 'expands']


def score_ref(ref: dict) -> tuple[int, str]:
    cls = ref['classification']
    label = (ref['title'] or ref['preview']).lower()
    if cls == 'independent-secondary':
        if any(h in label for h in SUBSTANTIAL_HINTS):
            return 4, 'substantial-independent'
        if any(h in label for h in ROUTINE_HINTS):
            return 2, 'routine-independent'
        return 3, 'independent-secondary'
    if cls == 'needs-review':
        return 1, 'review-needed'
    if cls == 'institutional-primary':
        return 1, 'institutional-primary'
    if cls == 'directory/database':
        return 0, 'directory'
    if cls == 'press-release-wire':
        return 0, 'press-wire'
    if cls == 'primary-or-affiliated':
        return 0, 'primary'
    return 0, 'unknown'


def verdict(total: int, strong: int, weak: int) -> str:
    if strong >= 5 and weak <= max(2, strong // 2) and total >= 12:
        return 'strong'
    if strong >= 3 and total >= 8:
        return 'plausible'
    if strong >= 2:
        return 'borderline'
    return 'weak'


def main():
    ap = argparse.ArgumentParser(description='Estimate rough Wikipedia article viability from citation mix')
    ap.add_argument('path', nargs='?', help='Draft/source file path, or omit/read stdin')
    args = ap.parse_args()
    text = load_text(args.path)
    refs = extract_refs(text)

    points = 0
    strong = 0
    buckets = []
    for ref in refs:
        pts, bucket = score_ref(ref)
        points += pts
        if pts >= 3:
            strong += 1
        buckets.append((ref['index'], bucket, ref['title'] or ref['detail']))

    weak = count_weak(refs)
    independent = count_independent(refs)
    v = verdict(len(refs), strong, weak)

    print(f'refs_total: {len(refs)}')
    print(f'independent_refs: {independent}')
    print(f'strong_refs: {strong}')
    print(f'weak_refs: {weak}')
    print(f'notability_points: {points}')
    print(f'viability: {v}')
    print('\nBreakdown:')
    for idx, bucket, label in buckets:
        print(f'[{idx}] {bucket} | {label}')

    if v == 'strong':
        print('\nRecommendation: article likely viable if prose stays neutral and claims match sources.')
    elif v == 'plausible':
        print('\nRecommendation: viable in sandbox/draft; tighten lead and reduce primary-source dependence.')
    elif v == 'borderline':
        print('\nRecommendation: draft carefully and look for more independent coverage before mainspace.')
    else:
        print('\nRecommendation: do not push toward mainspace yet; sourcing is too weak.')


if __name__ == '__main__':
    main()
