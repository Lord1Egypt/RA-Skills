#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
from wiki_ref_utils import load_text, extract_refs, count_independent, count_weak

SECTION_PATTERNS = ['History', 'Operations', 'Reception', 'Projects']


def main():
    ap = argparse.ArgumentParser(description='Estimate rough deletion/rejection risk for a wiki draft')
    ap.add_argument('path', nargs='?', help='Draft file path, or omit/read stdin')
    args = ap.parse_args()
    text = load_text(args.path)
    refs = extract_refs(text)
    independent = count_independent(refs)
    weak = count_weak(refs)

    score = 0
    findings = []
    if independent < 3:
        score += 3
        findings.append('too few independent sources')
    if weak > max(2, len(refs) // 4):
        score += 2
        findings.append('too much primary/weak sourcing')
    if re.search(r'\b(leading|premier|world-class|innovative|trusted|official supplier)\b', text, flags=re.I):
        score += 2
        findings.append('promotional wording detected')
    if len(re.findall(r'^\*', text, flags=re.M)) >= 8:
        score += 1
        findings.append('laundry-list style section may be too long')
    if not re.search(r'==\s*History\s*==', text):
        score += 1
        findings.append('thin article structure / missing history section')
    if len(text) < 1800:
        score += 1
        findings.append('very short draft may look underdeveloped')

    if score <= 1:
        risk = 'low'
    elif score <= 4:
        risk = 'medium'
    else:
        risk = 'high'

    print(f'deletion_risk: {risk}')
    print(f'risk_points: {score}')
    print(f'independent_refs: {independent}')
    print(f'weak_refs: {weak}')
    print('findings:')
    if findings:
        for f in findings:
            print(f'- {f}')
    else:
        print('- no major heuristic flags')


if __name__ == '__main__':
    main()
