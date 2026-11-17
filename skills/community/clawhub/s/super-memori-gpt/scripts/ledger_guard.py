#!/usr/bin/env python3
"""Read-only structural checks for Super Memori schema-v2 JSON. No network I/O."""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

COLLECTIONS = ('constraints', 'decisions', 'memories', 'lessons', 'artifacts', 'checks')
ACTIVE = {'active', 'completed', 'verified', 'validated'}
STALE = {'superseded', 'contradicted', 'expired', 'uncertain', 'needs_recheck', 'rejected'}
STATUSES = ACTIVE | STALE | {'proposed', 'candidate', 'retired', 'source', 'draft', 'passed', 'failed', 'pending'}
RELATIONS = {'depends_on', 'derived_from', 'verified_by', 'affects', 'supersedes', 'contradicts'}
def status(row):
    value = row.get('status', row.get('state'))
    return value if isinstance(value, str) else '<invalid>'
PATTERNS = [
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(r'\bsk-[A-Za-z0-9_-]{20,}'),
    re.compile(r'https?://[^\s/]+:[^\s/@]+@', re.I),
    re.compile(r'[?&](?:token|access_token|api_key|signature|sig|x-amz-signature)=[^\s&#]+', re.I),
    re.compile(r'\b(?:password|api[_-]?key|access[_-]?token)\s*[:=]\s*["\x27]?[A-Za-z0-9_./+~-]{12,}', re.I),
]


def validate(data):
    errors, warnings = [], []
    def error(path, message):
        errors.append({'path': path, 'message': message})
    def scan(value, path='$'):
        if isinstance(value, dict):
            for key, item in value.items():
                scan(key, path + '.<key>')
                scan(item, path + '.<value>')
        elif isinstance(value, list):
            for index, item in enumerate(value):
                scan(item, path + '[' + str(index) + ']')
        elif isinstance(value, str) and any(p.search(value) for p in PATTERNS):
            error(path, 'possible credential: remove before persistence; value omitted')
    scan(data)
    if not isinstance(data, dict):
        error('$', 'expected an object')
        return {'ok': False, 'errors': errors, 'warnings': warnings}
    if data.get('schema_version') != 2:
        error('schema_version', 'requires schema 2; migrate old ledgers without inventing missing evidence')
    for key in ('project_id', 'objective', 'updated_at'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            error(key, 'required non-empty text')
    if status(data) not in {'active', 'paused', 'completed', 'blocked'}:
        error('status', 'invalid project status')
    work = data.get('work_state')
    if not isinstance(work, dict):
        error('work_state', 'required object')
    elif status(data) != 'completed' and not (isinstance(work.get('next_action'), str) and work['next_action'].strip()):
        error('work_state.next_action', 'required for an unfinished project')
    rows, origins = {}, {}
    for collection in COLLECTIONS:
        values = data.get(collection, [])
        if not isinstance(values, list):
            error(collection, 'expected a list')
            continue
        for index, row in enumerate(values):
            path = collection + '[' + str(index) + ']'
            if not isinstance(row, dict):
                error(path, 'expected an object')
                continue
            rid = row.get('id')
            if not isinstance(rid, str) or not rid.strip():
                error(path, 'required stable string id')
                continue
            if rid in rows:
                error(path, 'duplicate record id')
                continue
            rows[rid], origins[rid] = row, (collection, path)
            if row.get('project_id', data.get('project_id')) != data.get('project_id'):
                error(path, 'record belongs to a different project')
            state = status(row)
            if 'status' in row and 'state' in row:
                error(path, 'use status or state, not both')
            if state not in STATUSES:
                error(path, 'missing or invalid record status')
            source = row.get('evidence_ref') if collection == 'checks' else row.get('source_ref')
            if state not in {'proposed', 'candidate', 'pending', 'uncertain'} and not (isinstance(source, str) and source.strip()):
                error(path, 'required source/evidence reference')
            if collection == 'artifacts' and not (isinstance(row.get('version_or_fingerprint'), str) and row['version_or_fingerprint'].strip()):
                error(path, 'artifact must bind an exact version/fingerprint')
            dates = {}
            for field in ('recorded_at', 'valid_from', 'valid_to'):
                value = row.get(field)
                if value is None:
                    continue
                try:
                    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    if dt.tzinfo is None:
                        raise ValueError('timezone required')
                    dates[field] = dt
                except (ValueError, TypeError, AttributeError):
                    error(path + '.' + field, 'use ISO-8601 with timezone or null for unknown')
            if 'valid_from' in dates and 'valid_to' in dates and dates['valid_to'] < dates['valid_from']:
                error(path, 'validity interval is reversed')
    deps = {rid: [] for rid in rows}
    for rid, row in rows.items():
        path = origins[rid][1]
        values = row.get('depends_on', [])
        if not isinstance(values, list):
            error(path + '.depends_on', 'expected a list')
            continue
        for dep in values:
            if not isinstance(dep, dict) or not isinstance(dep.get('id'), str) or dep['id'] not in rows:
                error(path + '.depends_on', 'unresolved dependency id')
                continue
            deps[rid].append(dep)
            if origins[dep['id']][0] == 'artifacts' and not isinstance(dep.get('version'), str):
                error(path + '.depends_on', 'artifact dependency needs an exact version')
    rels = data.get('relations', [])
    if not isinstance(rels, list):
        error('relations', 'expected a list')
        rels = []
    for index, rel in enumerate(rels):
        path = 'relations[' + str(index) + ']'
        if not isinstance(rel, dict) or not isinstance(rel.get('type'), str) or rel['type'] not in RELATIONS:
            error(path, 'invalid relation')
            continue
        left, right = rel.get('from'), rel.get('to')
        if not isinstance(left, str) or not isinstance(right, str) or left not in rows or right not in rows:
            error(path, 'unresolved relation endpoint')
        elif rel['type'] in {'depends_on', 'derived_from'}:
            deps[left].append({'id': right})
        elif rel['type'] == 'supersedes' and status(rows[right]) != 'superseded':
            error(path, 'superseded record must be marked superseded')
    invalid = {rid for rid, row in rows.items() if status(row) in STALE}
    for rid, values in deps.items():
        for dep in values:
            actual = rows[dep['id']].get('version_or_fingerprint')
            if 'version' in dep and dep['version'] != actual:
                invalid.add(rid)
    changed = True
    while changed:
        changed = False
        for rid, values in deps.items():
            if rid not in invalid and any(dep['id'] in invalid for dep in values):
                invalid.add(rid)
                changed = True
    for rid in invalid:
        if status(rows[rid]) in ACTIVE:
            error(origins[rid][1], 'current claim has a stale dependency; needs_recheck')
    valid_checks = []
    for rid, row in rows.items():
        if origins[rid][0] != 'checks':
            continue
        path = origins[rid][1]
        if status(row) not in {'passed', 'failed', 'pending'}:
            error(path, 'check status must be passed, failed or pending')
        if not isinstance(row.get('applicability'), str) or row['applicability'] not in {'current', 'historical'}:
            error(path, 'check applicability must be current or historical')
        targets = row.get('targets')
        if not isinstance(targets, list) or not targets or not row.get('scope'):
            error(path, 'check requires targets and explicit scope')
            continue
        match = True
        for target in targets:
            if not isinstance(target, dict) or not isinstance(target.get('id'), str) or target['id'] not in rows or origins[target['id']][0] != 'artifacts' or not target.get('version'):
                error(path, 'invalid version-bound artifact target')
                match = False
            elif target['version'] != rows[target['id']].get('version_or_fingerprint'):
                match = False
                if row.get('applicability') == 'current':
                    error(path, 'current check targets another artifact version')
        if row.get('status') == 'passed' and row.get('applicability') == 'current' and match:
            valid_checks.append(row)
    for rid, row in rows.items():
        if origins[rid][0] == 'artifacts' and row.get('state') == 'verified':
            scope = row.get('verification_scope')
            if not scope or not any(check['scope'] == scope and any(t['id'] == rid for t in check['targets']) for check in valid_checks):
                error(origins[rid][1], 'verified artifact needs a current passing check for its version and stated scope')
    warnings.append('Structural checks only; verify source truth, missing dependencies and privacy manually.')
    return {'ok': not errors, 'errors': errors, 'warnings': warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', help='JSON ledger path, or - for stdin')
    args = parser.parse_args()
    try:
        raw = sys.stdin.read() if args.file == '-' else Path(args.file).read_text(encoding='utf-8')
        result = validate(json.loads(raw))
    except (OSError, UnicodeError, json.JSONDecodeError):
        result = {'ok': False, 'errors': [{'path': '$', 'message': 'cannot read valid UTF-8 JSON; contents omitted'}], 'warnings': []}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
