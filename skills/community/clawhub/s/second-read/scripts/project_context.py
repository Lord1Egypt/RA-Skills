#!/usr/bin/env python3
"""Validate a supplied project/house-rules context, without inferring identity or truth.

Usage: python3 scripts/project_context.py assets/project-context.example.json
This program validates provenance LINKS and shape. It does NOT verify the truth
of statements, legal compliance, authority of a cited author, or live URLs.
"""
import argparse
import json
import sys
from pathlib import Path

RULE_KINDS = frozenset({'must', 'must_not', 'prefer', 'example', 'context'})
SOURCE_KINDS = frozenset({'author_brief', 'house_style', 'campaign_brief',
                          'product_source', 'publication_style', 'other'})
SCOPES = frozenset({'all', 'essay', 'policy', 'fiction', 'brand', 'email', 'blog',
                    'landing_page', 'ad', 'journalism', 'docs'})
PROJECT_KINDS = frozenset({'company', 'product', 'campaign', 'publication',
                           'documentation', 'personal', 'other'})


class ContextError(ValueError):
    pass


def nonempty(obj, key, path):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ContextError(f'{path}.{key} must be a nonempty string')
    return value.strip()


def validate_context(data):
    if not isinstance(data, dict) or data.get('schema_version') != 1 or isinstance(data.get('schema_version'), bool):
        raise ContextError('Expected schema_version: 1')
    project = data.get('project')
    if not isinstance(project, dict):
        raise ContextError('project must be an object')
    nonempty(project, 'name', 'project')
    if nonempty(project, 'kind', 'project') not in PROJECT_KINDS:
        raise ContextError('project.kind is unrecognized')
    project_source = nonempty(project, 'source_id', 'project')
    campaign = data.get('campaign')
    if campaign is not None:
        if not isinstance(campaign, dict):
            raise ContextError('campaign must be an object')
        for field in ('name', 'goal', 'audience'):
            nonempty(campaign, field, 'campaign')
        if 'approved_offer' in campaign:
            nonempty(campaign, 'approved_offer', 'campaign')
    sources = data.get('sources')
    if not isinstance(sources, list) or not sources:
        raise ContextError('sources must be a nonempty list')
    ids = set()
    for i, item in enumerate(sources):
        if not isinstance(item, dict):
            raise ContextError(f'sources[{i}] must be an object')
        sid = nonempty(item, 'id', f'sources[{i}]')
        if sid in ids:
            raise ContextError(f'duplicate source ID: {sid}')
        ids.add(sid)
        if nonempty(item, 'kind', f'sources[{i}]') not in SOURCE_KINDS:
            raise ContextError(f'unknown source kind: {sid}')
        nonempty(item, 'location', f'sources[{i}]')
    if project_source not in ids:
        raise ContextError(f'project refers to missing source: {project_source}')
    rules = data.get('rules')
    if not isinstance(rules, list):
        raise ContextError('rules must be a list (possibly empty)')
    rids = set()
    for i, rule in enumerate(rules):
        if not isinstance(rule, dict):
            raise ContextError(f'rules[{i}] must be an object')
        rid = nonempty(rule, 'id', f'rules[{i}]')
        if rid in rids:
            raise ContextError(f'duplicate rule ID: {rid}')
        rids.add(rid)
        if nonempty(rule, 'kind', f'rules[{i}]') not in RULE_KINDS:
            raise ContextError(f'unknown rule kind: {rid}')
        nonempty(rule, 'text', f'rules[{i}]')
        sid = nonempty(rule, 'source_id', f'rules[{i}]')
        if sid not in ids:
            raise ContextError(f'rule {rid} refers to missing source: {sid}')
        scopes = rule.get('scope')
        if not isinstance(scopes, list) or not scopes or any(not isinstance(s, str) or s not in SCOPES for s in scopes):
            raise ContextError(f'rule {rid} must have valid nonempty scope list')
        if 'all' in scopes and len(scopes) != 1:
            raise ContextError(f'rule {rid}: scope all cannot be mixed with other scopes')
        if len(scopes) != len(set(scopes)):
            raise ContextError(f'rule {rid}: duplicate scopes')
    return {'valid': True, 'project': project['name'],
            'source_count': len(sources), 'rule_count': len(rules),
            'limits': 'Provenance pointers checked; factual authority and applicability not verified.'}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('path', type=Path)
    ap.add_argument('--json', type=Path, help='Save the validation report')
    args = ap.parse_args(argv)
    try:
        data = json.loads(args.path.read_text(encoding='utf-8'))
        report = validate_context(data)
    except (ContextError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        report = {'valid': False, 'error': str(exc)}
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.json:
        args.json.write_text(payload + '\n', encoding='utf-8')
    return 0 if report['valid'] else 1


if __name__ == '__main__':
    sys.exit(main())
