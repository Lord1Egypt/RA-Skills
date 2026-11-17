#!/usr/bin/env python3
"""Score model decision/routing agreement on paired editorial fixtures.

This is a reproducible *triage* metric, NOT a semantic or human quality judge.
Reviewers still need to inspect meaning preservation, voice and factual truth.

Input: one JSON object per line: {"case_id":"...", "decision":"edit|leave|ask|visual",
"source_quote":"<verbatim span>"}. Each output must quote source for edit/ask/visual.
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

DECISIONS = frozenset({'edit', 'leave', 'ask', 'visual'})


class EvaluationError(ValueError):
    pass


def read_jsonl(path):
    records = []
    for num, line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise EvaluationError(f'{path}:{num}: invalid JSON: {exc}') from exc
        if not isinstance(record, dict):
            raise EvaluationError(f'{path}:{num}: expected object')
        records.append(record)
    return records


def validate_cases(cases):
    ids = set()
    for case in cases:
        cid = case.get('id')
        if not isinstance(cid, str) or not cid.strip() or cid in ids:
            raise EvaluationError(f'missing or duplicate case ID: {cid}')
        ids.add(cid)
        if case.get('decision') not in DECISIONS:
            raise EvaluationError(f'{cid}: invalid expected decision')
        for key in ('draft', 'reason', 'pathway', 'source_quote'):
            if not isinstance(case.get(key), str) or not case[key].strip():
                raise EvaluationError(f'{cid}: {key} must be nonempty')
        if case['source_quote'] not in case['draft']:
            raise EvaluationError(f'{cid}: source_quote not found in draft')
        if case['decision'] == 'edit' and not isinstance(case.get('safe_edit'), str):
            raise EvaluationError(f'{cid}: edit fixture needs safe_edit')
        if case['decision'] == 'ask' and not isinstance(case.get('question'), str):
            raise EvaluationError(f'{cid}: ask fixture needs question')
        if case['decision'] == 'visual' and not isinstance(case.get('visual_reason'), str):
            raise EvaluationError(f'{cid}: visual fixture needs visual_reason')
    return ids


def evaluate(cases, predictions):
    case_ids = validate_cases(cases)
    lookup = {c['id']: c for c in cases}
    seen, rows = set(), []
    for result in predictions:
        cid = result.get('case_id')
        if cid not in case_ids or cid in seen:
            raise EvaluationError(f'unknown or duplicate prediction: {cid}')
        seen.add(cid)
        dec = result.get('decision')
        if dec not in DECISIONS:
            raise EvaluationError(f'{cid}: invalid prediction decision')
        source_quote = result.get('source_quote')
        grounded = (dec == 'leave' and not source_quote) or (
            isinstance(source_quote, str) and bool(source_quote.strip()) and
            source_quote in lookup[cid]['draft'])
        rows.append({'id': cid, 'expected': lookup[cid]['decision'],
                     'predicted': dec, 'matched_decision': dec == lookup[cid]['decision'],
                     'source_grounded': grounded, 'pathway': lookup[cid]['pathway']})
    missing = sorted(case_ids - seen)
    by_path = defaultdict(Counter)
    for row in rows:
        counts = by_path[row['pathway']]
        counts['n'] += 1
        counts['match'] += int(row['matched_decision'])
        counts['grounded'] += int(row['source_grounded'])
    return {
        'label': 'Triage decision agreement only; not editing quality, human evaluation or factual verification',
        'evaluated': len(rows),
        'total_cases': len(cases),
        'missing_cases': missing,
        'decision_matches': sum(r['matched_decision'] for r in rows),
        'source_grounded': sum(r['source_grounded'] for r in rows),
        'false_edits_on_leave_cases': sum(r['expected'] == 'leave' and r['predicted'] == 'edit' for r in rows),
        'by_pathway': dict(by_path),
        'rows': rows
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', required=True)
    parser.add_argument('--predictions', required=True)
    parser.add_argument('--json', type=Path)
    args = parser.parse_args(argv)
    try:
        report = evaluate(read_jsonl(args.cases), read_jsonl(args.predictions))
    except (OSError, ValueError) as exc:
        print(f'evaluation error: {exc}', file=sys.stderr)
        return 2
    result = json.dumps(report, ensure_ascii=False, indent=2)
    print(result)
    if args.json:
        args.json.write_text(result + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
