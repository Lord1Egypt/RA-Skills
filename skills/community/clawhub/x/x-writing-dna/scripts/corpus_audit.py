"""Audit explicit corpus observations; no networking or inferred identity."""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from statistics import median
from urllib.parse import urlsplit, urlunsplit


def canonical_url(url):
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc.lower(), parts.path.rstrip('/'), '', ''))


def body_hash(body):
    return hashlib.sha256(re.sub(r'\s+', ' ', body).strip().encode()).hexdigest()


def audit(records, author):
    seen_urls, seen_bodies, seen_groups = set(), set(), set()
    rows, accepted, eligible = [], [], []
    # Prefer verified native captures so an unconfirmed mirror cannot shadow them.
    def priority(r):
        verified = (r.get('author_verified') is True
                    and r.get('identity_status') == 'confirmed'
                    and bool(r.get('identity_evidence'))
                    and r.get('source_kind') in {'x_native', 'author_archive', 'mirror'})
        return (verified, r.get('source_kind') == 'x_native')

    for source in sorted(records, key=priority, reverse=True):
        r = dict(source)
        body = r.get('body', '')
        url = canonical_url(r.get('url', ''))
        medium = r.get('medium', '')
        digest = body_hash(body)
        group = (medium, r.get('group_id') or url)
        reasons = []
        if r.get('author', '').casefold() != author.casefold():
            reasons.append('wrong_author')
        if medium not in {'post', 'article', 'thread'}:
            reasons.append('unknown_medium')
        formats = {'post': {'short_post', 'long_post'},
                   'article': {'x_article', 'external_article'}, 'thread': {'thread'}}
        if r.get('format') not in formats.get(medium, set()):
            reasons.append('genre_format_mismatch')
        if r.get('format') == 'x_article' and r.get('source_kind') != 'x_native':
            reasons.append('native_article_source_mismatch')
        if r.get('format') == 'external_article' and r.get('source_kind') == 'x_native':
            reasons.append('external_article_source_mismatch')
        if not url.startswith(('https://', 'http://')):
            reasons.append('missing_url')
        if not body.strip():
            reasons.append('empty_body')
        if r.get('complete') is not True or not r.get('completeness_evidence'):
            reasons.append('incomplete_or_unproven')
        if r.get('coauthors'):
            reasons.append('coauthored')
        if r.get('exclude_reason'):
            reasons.append(r['exclude_reason'])
        if not re.sub(r'https?://\S+', '', body).strip():
            reasons.append('link_only')
        if url in seen_urls:
            reasons.append('duplicate_url')
        if (medium, digest) in seen_bodies:
            reasons.append('duplicate_body')
        if group in seen_groups:
            reasons.append('duplicate_work_group')
        # Rejected previews must not suppress a later complete capture.
        body_eligible = not reasons
        if body_eligible:
            seen_urls.add(url)
            seen_bodies.add((medium, digest))
            seen_groups.add(group)
            eligible.append(r)
        if (r.get('author_verified') is not True
                or r.get('identity_status') != 'confirmed'
                or not r.get('identity_evidence')):
            reasons.append('identity_unconfirmed')
        if r.get('source_kind') not in {'x_native', 'author_archive', 'mirror'}:
            reasons.append('unknown_source')
        if not reasons:
            accepted.append(r)
        rows.append({'url': url, 'medium': medium, 'format': r.get('format', ''),
                     'source_kind': r.get('source_kind', ''), 'date': r.get('date'),
                     'body_sha256': digest, 'characters': len(body),
                     'body_eligible': body_eligible, 'accepted': not reasons,
                     'reasons': ';'.join(reasons)})
    branches = {}
    for medium, target in [('post', 50), ('article', 20), ('thread', None)]:
        rs = [r for r in accepted if r['medium'] == medium]
        native = [r for r in rs if r['source_kind'] == 'x_native']
        branches[medium] = {
            'target': target,
            'raw': sum(r.get('medium') == medium for r in records),
            'eligible_body': sum(r.get('medium') == medium for r in eligible),
            'confirmed': len(rs), 'x_native_confirmed': len(native),
            'target_met': target is not None and len(rs) >= target,
            'x_native_target_met': target is not None and len(native) >= target,
            'sources': dict(Counter(r['source_kind'] for r in rs)),
            'formats': dict(Counter(r.get('format', '') for r in rs)),
            'campaigns': dict(Counter(r.get('campaign') or 'untagged' for r in rs)),
            'dates': sorted(set(r['date'] for r in rs if r.get('date'))),
        }
    stats = {}
    for key in sorted({(r['medium'], r.get('format', '')) for r in accepted}):
        rs = [r for r in accepted if (r['medium'], r.get('format', '')) == key]
        stats['/'.join(key)] = {
            'n': len(rs), 'raw_body_characters_median': median(len(r['body']) for r in rs),
            'raw_nonempty_lines_median': median(len([p for p in r['body'].splitlines() if p.strip()]) for r in rs),
            'raw_blankline_blocks_median': median(len([p for p in re.split(r'\n\s*\n', r['body']) if p.strip()]) for r in rs),
            'warning': 'Raw body includes quotes/prompts/code. Not narration-only statistics.'}
    return {'author': author, 'raw_records': len(records), 'branches': branches,
            'raw_body_stats': stats, 'samples': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('corpus', type=Path)
    parser.add_argument('--author', required=True)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    records = []
    for number, line in enumerate(args.corpus.read_text().splitlines(), 1):
        if line.strip():
            item = json.loads(line)
            if not isinstance(item, dict) or not isinstance(item.get('body', ''), str):
                raise ValueError(f'Invalid record at line {number}')
            records.append(item)
    result = audit(records, args.author)
    args.out.mkdir(parents=True, exist_ok=True)
    json_path = args.out / 'audit.json'
    csv_path = args.out / 'sample-index.csv'
    if json_path.exists() or csv_path.exists():
        raise FileExistsError('Use a fresh output directory to preserve earlier audits.')
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    with csv_path.open('w', newline='') as stream:
        fields = ['url', 'medium', 'format', 'source_kind', 'date', 'body_sha256',
                  'characters', 'body_eligible', 'accepted', 'reasons']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result['samples'])
    print(json.dumps({'author': args.author, 'raw': len(records),
                      'branches': result['branches']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
