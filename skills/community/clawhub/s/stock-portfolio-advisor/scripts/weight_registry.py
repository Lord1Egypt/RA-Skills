"""Versioned, date-aware Q/G/V releases. No external dependencies."""
import hashlib
import json
import math
import os
from datetime import date, timedelta
from pathlib import Path

SCORING_RULES = 'value-v2.1'
DEFAULT_PATH = Path(__file__).resolve().parent.parent / 'config' / 'weights.json'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def read_json(path):
    def reject(x):
        raise ValueError(f'Non-finite JSON value: {x}')
    value = json.loads(Path(path).read_text(encoding='utf-8-sig'), parse_constant=reject)
    # JSON allows 1e999 syntactically; reject its overflowing float as well.
    def check(x):
        if isinstance(x, float) and not math.isfinite(x):
            raise ValueError('Non-finite number')
        if isinstance(x, dict):
            for v in x.values(): check(v)
        if isinstance(x, list):
            for v in x: check(v)
    check(value)
    return value


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    owned = False
    try:
        with temporary.open('x', encoding='utf-8') as f:
            owned = True
            json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporary, path)
    finally:
        if owned and temporary.exists():
            temporary.unlink()


def valid_weights(w):
    return (isinstance(w, dict) and set(w) == set('QGV')
            and all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and 0 <= x <= 100 for x in w.values())
            and abs(sum(w.values()) - 100) < .0001)


def normalize(values):
    w = {k: round(x / sum(values) * 100, 6) for k, x in zip('QGV', values)}
    w['V'] = round(100 - w['Q'] - w['G'], 6)
    return w


def read_registry(path=DEFAULT_PATH):
    if not Path(path).exists():
        return {'schema_version': 1, 'releases': []}
    r = read_json(path)
    if not isinstance(r, dict) or r.get('schema_version') != 1 or not isinstance(r.get('releases'), list):
        raise ValueError('Invalid weight registry')
    return r


def release_valid(r):
    try:
        start, cutoff = date.fromisoformat(r['effective_from']), date.fromisoformat(r['training_cutoff'])
        mature = date.fromisoformat(r['max_label_end'])
        expires = date.fromisoformat(r['expires_on'])
        return (r.get('rules_version') == SCORING_RULES and r.get('synthetic') is False
                and r.get('validation_passed') is True and bool(r.get('version'))
                and isinstance(r.get('weights'), dict) and bool(r['weights'])
                and all(valid_weights(w) for w in r['weights'].values())
                and mature <= cutoff < start <= expires and r.get('calibration_id'))
    except (ValueError, TypeError, KeyError):
        return False


def resolve(registry, profile, as_of, default):
    fallback = (normalize(default), 'builtin-v2.1', [])
    try:
        date.fromisoformat(as_of)
    except (TypeError, ValueError):
        return fallback
    valid = [r for r in registry.get('releases', []) if release_valid(r) and profile in r['weights']
             and r['effective_from'] <= as_of <= r['expires_on']]
    if not valid:
        return fallback
    r = max(valid, key=lambda x: (x['effective_from'], x['version']))
    return dict(r['weights'][profile]), r['version'], []


def activate(report, registry_path=DEFAULT_PATH):
    """Only validated, real-data proposals. Lock + archive + atomic replacement."""
    if report.get('synthetic') is not False:
        raise ValueError('Synthetic results cannot activate production weights')
    if digest({k:v for k,v in report.items() if k != 'calibration_id'}) != report.get('calibration_id'):
        raise ValueError('Calibration report checksum mismatch')
    accepted = {k: v['proposed_weights'] for k, v in report['profiles'].items() if v.get('accepted') is True}
    if not accepted:
        return {'status': 'unchanged', 'reason': 'No profile passed the gates'}
    path = Path(registry_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + '.lock')
    with lock.open('x') as handle:
        handle.write('weight calibration\n')
    try:
        registry = read_registry(path)
        if any(r.get('calibration_id') == report['calibration_id'] for r in registry['releases']):
            return {'status': 'unchanged', 'reason': 'Calibration already applied'}
        if digest(registry) != report['registry_hash']:
            raise ValueError('Registry changed during calibration; rerun before activation')
        cutoff = date.fromisoformat(report['as_of'])
        release = dict(version='cal-' + report['calibration_id'][:16], calibration_id=report['calibration_id'],
                       rules_version=SCORING_RULES, weights=accepted, synthetic=False, validation_passed=True,
                       training_cutoff=report['as_of'], max_label_end=report['max_label_end'],
                       effective_from=(cutoff + timedelta(days=1)).isoformat(),
                       expires_on=(cutoff + timedelta(days=370)).isoformat(), dataset_hash=report['dataset_hash'])
        if not release_valid(release):
            raise ValueError('Invalid proposed release')
        registry['releases'].append(release)
        archive = path.parent / 'weight_history' / (release['version'] + '.json')
        write_json(archive, {'release': release, 'validation': report})
        write_json(path, registry)
        return {'status': 'activated', 'version': release['version'], 'effective_from': release['effective_from']}
    finally:
        lock.unlink()
