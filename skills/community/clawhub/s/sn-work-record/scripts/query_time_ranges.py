#!/usr/bin/env python3
"""Read-only inclusive multi-range OA snapshot; no OA write endpoints.

Repeat --range START END. Stdout is always plain JSON (pretty by default,
compact with --json); descriptions are preserved, internal IDs omitted. Hours
are decimal strings. Empty days are successful; failed days contribute no
records/totals. Any invalid record invalidates its whole day. Conflicting IDs
invalidate every implicated day, including earlier results. Overlapping ranges
retain their own totals while dates are fetched once globally.

--raw-output creates a new, atomic 0600 JSON evidence file, never overwriting.
Evidence contains the snapshot and allowlisted source fields (including IDs)
from validated query responses, without authentication data or error bodies.
It is deliberately not a full HTTP dump; failed/malformed queries have only
safe errors in the snapshot. Keep this sensitive work-data file private.

Exit codes: 0 complete; 1 incomplete query/setup/evidence failure; 2 bad CLI.
Partial means incomplete, even if all days failed. Range completeness concerns
queries; a file-publication failure can make overall completeness false despite
complete ranges. Date suffixes support OA's observed midnight ' 00:00:00'
and optional '(周X)' / '（周X）'; other formats fail closed. Numeric hours are bounded to 100 characters and
100 exponent places. Atomic publication requires same-directory hard links.
Imports are side-effect free; runtime discovery occurs only in the CLI entry.
"""
import argparse
from collections import Counter
from contextlib import redirect_stdout, redirect_stderr
from decimal import Decimal, localcontext
from datetime import date, timedelta
import json
import os
import re
import tempfile

# Evidence is a source-field projection, not an unfiltered server/error dump.
RAW_FIELDS = ('id', 'fillDate', 'projectName', 'manHour', 'jobDesc', 'state',
              'createdTime', 'updatedTime')

DEFAULT_CREDS = os.path.expanduser('~/.openclaw/workspace/memory/sn-work-record-credentials.md')


def _api():
    import oa_utils
    return oa_utils


def parse_ranges(values):
    ranges = []
    for start, end in values:
        if not all(re.fullmatch(r'\d{4}-\d{2}-\d{2}', x) for x in (start, end)):
            raise ValueError('Dates must be YYYY-MM-DD')
        first, last = date.fromisoformat(start), date.fromisoformat(end)
        if first > last:
            raise ValueError('Range start must not follow end')
        ranges.append([ (first + timedelta(days=i)).isoformat()
                        for i in range((last - first).days + 1)])
    return ranges


def stats(records):
    values = [Decimal(r['hours']) for r in records]
    with localcontext() as ctx:
        # Exact even beyond Decimal's default 28 significant digits.
        ctx.prec = max(28, max((v.adjusted() for v in values), default=0)
                       - min((int(v.as_tuple().exponent) for v in values), default=0)
                       + len(str(len(values))) + 2)
        total = sum(values, Decimal(0))
    return {'records': len(records), 'dates': len({r['date'] for r in records}),
            'hours': str(total),
            'states': dict(sorted(Counter(r['state'] for r in records).items()))}


def normalize(row, day, api):
    if not isinstance(row, dict):
        raise ValueError('Invalid record')
    identity = row.get('id')
    if type(identity) not in (str, int) or not str(identity).strip():
        raise ValueError('Missing/invalid identity')
    if 'fillDate' in row:
        returned = row['fillDate']
        # OA also emits a localized weekday suffix. Do not strip arbitrary text.
        if (not isinstance(returned, str) or not re.fullmatch(
                r'\d{4}-\d{2}-\d{2}(?: 00:00:00|\(周[一二三四五六日天]\)|（周[一二三四五六日天]）)?', returned)
                or returned[:10] != day):
            raise ValueError('Returned date mismatch')
    value = row.get('manHour')
    if type(value) not in (str, int, float) or len(str(value)) > 100:
        raise ValueError('Invalid hours')
    hours = Decimal(str(value))
    if not hours.is_finite() or hours < 0 or abs(int(hours.as_tuple().exponent)) > 100:
        raise ValueError('Invalid hours')
    if not isinstance(row.get('jobDesc'), str):
        raise ValueError('Missing description')
    if type(row.get('state')) not in (str, int) or not str(row['state']).strip():
        raise ValueError('Missing state')
    for field in ('projectName', 'createdTime', 'updatedTime'):
        if row.get(field) is not None and not isinstance(row[field], str):
            raise ValueError('Invalid display field')
    return str(identity), {'date': day, 'project': row.get('projectName'),
                           'hours': str(hours), 'description': row['jobDesc'],
                           'state': api.state_to_text(str(row['state'])),
                           'created_time': row.get('createdTime'),
                           'updated_time': row.get('updatedTime')}


def snapshot(ranges, days):
    complete = all(d['status'] != 'failed' for d in days)
    result = {'complete': complete, 'partial': not complete, 'days': days, 'ranges': []}
    for group in ranges:
        selected = [d for d in days if d['date'] in group]
        records = [r for d in selected for r in d['records']]
        result['ranges'].append({'start': group[0], 'end': group[-1],
                                 'complete': all(d['status'] != 'failed' for d in selected),
                                 'stats': stats(records)})
    result['stats'] = stats([r for d in days for r in d['records']])
    return result


def collect(ranges, api, auth, base_url, queries):
    days = []
    seen = {}
    conflict_days = set()
    for day in sorted({d for group in ranges for d in group}):
        entry = {'date': day, 'status': 'failed', 'records': []}
        days.append(entry)
        try:
            response = auth.call(lambda s: api.query_time_entries(s, base_url, day))
        except Exception:
            entry['error_type'] = 'query_failed'
            continue
        try:
            rows, raw = response
            if (not isinstance(raw, dict) or str(raw.get('code')) != '200'
                    or not isinstance(raw.get('data'), list) or not isinstance(rows, list)
                    or rows != raw['data']):
                raise ValueError('Invalid response envelope')
            # Track identity conflicts before other validation: a malformed
            # later row must not leave its earlier conflicting copy in totals.
            for row in rows:
                if (not isinstance(row, dict) or type(row.get('id')) not in (str, int)
                        or not str(row['id']).strip()):
                    continue
                identity = str(row['id'])
                if identity in seen:
                    prior_day, prior_row = seen[identity]
                    if prior_day != day or prior_row != row:
                        conflict_days.update((prior_day, day))
                else:
                    seen[identity] = (day, row)
            records = list(dict(normalize(row, day, api) for row in rows).values())
            queries.append({'date': day, 'response': {'code': raw['code'], 'data': [
                {key: row[key] for key in RAW_FIELDS if key in row} for row in rows]}})
            entry.update(status='ok' if records else 'empty', records=records)
        except Exception:
            entry['error_type'] = 'malformed_response'
    for entry in days:
        if entry['date'] in conflict_days:
            entry.update(status='failed', records=[], error_type='conflicting_id')
    return snapshot(ranges, days)


def write_evidence(path, evidence):
    """Publish complete 0600 JSON atomically; link refuses even racing targets.

    Requires a filesystem supporting same-directory hard links (POSIX). Never
    falls back to replace/truncate. Parents must already exist.
    """
    target = os.path.abspath(os.path.expanduser(os.fspath(path)))
    fd, temporary = tempfile.mkstemp(prefix='.oa-query-', suffix='.json',
                                     dir=os.path.dirname(target))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as output:
            os.fchmod(output.fileno(), 0o600)
            json.dump(evidence, output, ensure_ascii=False, allow_nan=False,
                      separators=(',', ':'))
            output.write('\n')
            output.flush()
            os.fsync(output.fileno())
        os.link(temporary, target)
    finally:
        os.unlink(temporary)


def main(argv=None, *, bootstrap=False):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--range', nargs=2, action='append', required=True,
                        metavar=('START', 'END'))
    parser.add_argument('--credentials', default=DEFAULT_CREDS)
    parser.add_argument('--base-url', default=None)
    parser.add_argument('--json', action='store_true', help='Compact normalized JSON snapshot')
    parser.add_argument('--raw-output', metavar='PATH')
    args = parser.parse_args(argv)
    try:
        ranges = parse_ranges(args.range)
    except ValueError as exc:
        parser.error(str(exc))
    queries = []
    stage = 'evidence_failed'
    try:
        if args.raw_output:
            args.raw_output = os.path.abspath(os.path.expanduser(args.raw_output))
            if os.path.lexists(args.raw_output) or not os.path.isdir(os.path.dirname(args.raw_output)):
                raise FileExistsError('Evidence target unavailable')
        stage = 'runtime_failed'
        # Existing login helpers can print server bodies. Never forward their logs.
        with open(os.devnull, 'w') as sink, redirect_stdout(sink), redirect_stderr(sink):
            if bootstrap:
                from runtime_bootstrap import ensure_runtime
                ensure_runtime(['requests', 'ddddocr', 'PIL'])
            api = _api()
            stage = 'credentials_failed'
            username, password, base_url = api.load_credentials(args.credentials)
            base_url = api.resolve_base_url(base_url, args.base_url)
            stage = 'authentication_failed'
            auth = api.OAAuth(base_url, username, password)
            stage = 'query_failed'
            result = collect(ranges, api, auth, base_url, queries)
    except Exception:
        result = snapshot(ranges, [{'date': day, 'status': 'failed', 'records': [],
                                    'error_type': stage}
                                   for day in sorted({d for group in ranges for d in group})])
        result['error_type'] = stage
    if args.raw_output and stage != 'evidence_failed':
        try:
            write_evidence(args.raw_output, {'snapshot': result, 'queries': queries,
                'evidence_format': 'allowlisted-source-fields-v1'})
        except Exception:
            result.update(complete=False, partial=True, error_type='evidence_failed')
    print(json.dumps(result, ensure_ascii=False, separators=(',', ':') if args.json else None,
                     indent=None if args.json else 2))
    return 0 if result['complete'] else 1


if __name__ == '__main__':
    raise SystemExit(main(bootstrap=True))
