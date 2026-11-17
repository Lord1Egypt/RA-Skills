"""Build a point-in-time research panel from raw scoring snapshots and daily CSV bars."""
import argparse
import bisect
import calendar
import csv
from datetime import date
from pathlib import Path
from value_model import evaluate
from weight_registry import read_json, write_json, digest, SCORING_RULES


def add_months(day, months):
    d = date.fromisoformat(day)
    n = d.year * 12 + d.month - 1 + months
    year, month = divmod(n, 12)
    return date(year, month + 1, min(d.day, calendar.monthrange(year, month + 1)[1])).isoformat()


def flag(x):
    if x not in ('true', 'false', '1', '0'):
        raise ValueError(f'Boolean CSV field must be true/false/1/0: {x}')
    return x in ('true', '1')


def finite(x):
    import math
    value = float(x)
    if not math.isfinite(value):
        raise ValueError('Non-finite price')
    return value


def load_market(bars_path, benchmark_path):
    bars = {}
    with open(bars_path, encoding='utf-8-sig', newline='') as f:
        for x in csv.DictReader(f):
            date.fromisoformat(x['date'])
            code, day = x['code'], x['date']
            if not code or day in bars.setdefault(code, {}):
                raise ValueError('Empty code or duplicate market row')
            b = {k: finite(x[k]) for k in ('open', 'close', 'split_factor', 'cash_dividend')}
            b.update({k: flag(x[k]) for k in ('buy_allowed', 'sell_allowed', 'delisted')})
            if b['split_factor'] <= 0 or b['cash_dividend'] < 0 or b['open'] < 0 or b['close'] < 0:
                raise ValueError('Invalid corporate action or price')
            if not b['delisted'] and (b['close'] <= 0 or (b['buy_allowed'] or b['sell_allowed']) and b['open'] <= 0):
                raise ValueError('Active tradable prices must be positive')
            bars[code][day] = b
    benchmark = {}
    with open(benchmark_path, encoding='utf-8-sig', newline='') as f:
        for x in csv.DictReader(f):
            date.fromisoformat(x['date'])
            if x['date'] in benchmark:
                raise ValueError('Duplicate benchmark day')
            b = {k: finite(x[k]) for k in ('open_tr', 'close_tr')}
            if min(b.values()) <= 0:
                raise ValueError('Benchmark total-return index must be positive')
            benchmark[x['date']] = b
    sessions = sorted(benchmark)
    if not sessions or any(d not in benchmark for series in bars.values() for d in series):
        raise ValueError('Missing benchmark calendar or stock day outside calendar')
    return bars, benchmark, sessions


def forward_label(series, benchmark, sessions, entry_index, months):
    entry = sessions[entry_index]
    bar = series.get(entry)
    if not bar:
        raise ValueError(f'Missing entry-day market data: {entry}')
    if not bar['buy_allowed'] or bar['delisted']:
        return None  # Cannot enter at the specified next-session open; never pretend a fill.
    end_index = bisect.bisect_left(sessions, add_months(entry, months))
    if end_index == len(sessions):
        return None
    shares, cash = 1.0, 0.0
    for d in sessions[entry_index + 1:end_index + 1]:
        if not shares:
            continue
        b = series.get(d)
        if not b:
            raise ValueError(f'Missing held-stock data on {d}; provide suspension rows or terminal settlement')
        cash += shares * b['cash_dividend']
        shares *= b['split_factor']
        if b['delisted']:
            cash += shares * b['close']
            shares = 0
    end = sessions[end_index]
    wealth = cash + (shares * series[end]['close'] if shares else 0)
    asset_return = wealth / bar['open'] - 1
    benchmark_return = benchmark[end]['close_tr'] / benchmark[entry]['open_tr'] - 1
    return dict(label_end=end, forward_return=asset_return, benchmark_return=benchmark_return,
                excess_return=asset_return - benchmark_return, entry_date=entry)


def build(manifest, base):
    if manifest.get('point_in_time') is not True or manifest.get('includes_delisted') is not True:
        raise ValueError('Manifest must declare point-in-time universe and inclusion of delisted securities')
    if manifest.get('historical_assumptions_verified') is not True or not manifest.get('universe_description') or not manifest.get('source'):
        raise ValueError('Historical assumptions, universe definition and source are required')
    months = manifest.get('label_months', 12)
    if isinstance(months, bool) or not isinstance(months, int) or not 1 <= months <= 36:
        raise ValueError('label_months must be 1..36')
    snapshots = manifest.get('snapshots')
    if not isinstance(snapshots, list) or not snapshots:
        raise ValueError('Explicit snapshot file list required')
    bars, benchmark, sessions = load_market(base / manifest['bars_csv'], base / manifest['benchmark_csv'])
    last_days = {}
    for d in sessions:
        last_days[d[:7]] = d
    rows, seen, synthetic, exclusions = [], set(), manifest.get('synthetic') is True, []
    for filename in snapshots:
        raw = read_json(base / filename)
        d = raw.get('date')
        date.fromisoformat(d)
        if d in seen or last_days.get(d[:7]) != d:
            raise ValueError('Snapshot dates must be unique month-end trading sessions')
        seen.add(d)
        synthetic = synthetic or raw.get('synthetic') is True
        # Recompute dimensions with fixed v2.1 rules; ignore any deployed learned weights.
        result = evaluate(raw, registry={'schema_version': 1, 'releases': []})
        next_index = bisect.bisect_right(sessions, d)
        for s in result['stocks']:
            row = dict(date=d, code=s['code'], profile=s['profile'], industry=s.get('industry'),
                       exposure_group=s.get('exposure_group'), dims={k:s['dims'][k] for k in 'QGV'},
                       eligible=s['total'] is not None and not s['red_flags'], label=None)
            if row['eligible'] and (not row['industry'] or not row['exposure_group']):
                raise ValueError('Eligible historical rows need industry and exposure_group')
            if row['eligible'] and next_index < len(sessions):
                if s['code'] not in bars:
                    raise ValueError('Missing market history for eligible security: ' + s['code'])
                row['label'] = forward_label(bars[s['code']], benchmark, sessions, next_index, months)
                if row['label'] is None:
                    exclusions.append({'date': d, 'code': s['code'], 'reason': 'unmatured horizon or next-open entry unavailable'})
            rows.append(row)
    decisions = sorted(seen)
    expected = sorted(d for d in last_days.values() if decisions[0] <= d <= decisions[-1])
    if decisions != expected:
        raise ValueError('Missing monthly snapshot; cannot silently skip adverse months')
    dataset = dict(schema_version=1, rules_version=SCORING_RULES, synthetic=synthetic,
                   label_months=months, manifest=manifest, rows=rows, decision_dates=decisions, sessions=sessions,
                   bars=bars, benchmark=benchmark, label_exclusions=exclusions,
                   note='Historical manifest declarations require external audit; they are not proof against hindsight bias.')
    dataset['dataset_hash'] = digest(dataset)
    return dataset


def verify_dataset(dataset):
    body = {k:v for k,v in dataset.items() if k != 'dataset_hash'}
    if digest(body) != dataset.get('dataset_hash') or dataset.get('rules_version') != SCORING_RULES:
        raise ValueError('Dataset checksum or scoring-rule version mismatch; rebuild')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    try:
        path = Path(a.manifest)
        dataset = build(read_json(path), path.parent)
        write_json(a.output, dataset)
        print(f"[OK] {len(dataset['rows'])} rows; synthetic={dataset['synthetic']}")
    except (ValueError, KeyError, TypeError, OSError) as exc:
        p.error(str(exc))


if __name__ == '__main__':
    main()
