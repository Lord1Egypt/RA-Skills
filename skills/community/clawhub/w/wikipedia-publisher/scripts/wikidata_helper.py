#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json


def main():
    ap = argparse.ArgumentParser(description='Generate starter Wikidata statements for a subject')
    ap.add_argument('--name', required=True)
    ap.add_argument('--instance-of', default='organization')
    ap.add_argument('--country', default='')
    ap.add_argument('--inception', default='')
    ap.add_argument('--official-website', default='')
    ap.add_argument('--founders', nargs='*', default=[])
    args = ap.parse_args()

    statements = [
        {'property': 'P31', 'label': 'instance of', 'value': args.instance_of, 'confidence': 'needs-qid-review'},
    ]
    if args.country:
        statements.append({'property': 'P17', 'label': 'country', 'value': args.country, 'confidence': 'needs-qid-review'})
    if args.inception:
        statements.append({'property': 'P571', 'label': 'inception', 'value': args.inception, 'confidence': 'source-required'})
    if args.official_website:
        statements.append({'property': 'P856', 'label': 'official website', 'value': args.official_website, 'confidence': 'source-required'})
    for founder in args.founders:
        statements.append({'property': 'P112', 'label': 'founded by', 'value': founder, 'confidence': 'needs-qid-review'})

    output = {
        'label': args.name,
        'description_guidance': 'Use a short neutral description. Avoid marketing copy or claims of prominence.',
        'starter_statements': statements,
        'checklist': [
            'Confirm an item does not already exist',
            'Attach sources for every factual claim you can',
            'Prefer low-controversy starter statements first',
            'Do not copy website copy into description or aliases',
        ]
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
