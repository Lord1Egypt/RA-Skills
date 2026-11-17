#!/usr/bin/env python3
"""Plan a three-way merge or calculate exact totals; never mutate a workbook."""
import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path

FIELDS = ('date', 'merchant', 'description', 'amount', 'currency', 'category', 'account', 'type', 'notes')
TYPES = ('expense', 'refund', 'income', 'transfer', 'card_payment')


def money(value):
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError('Invalid decimal amount') from exc
    if not result.is_finite() or result < 0:
        raise ValueError('Amount must be finite and nonnegative')
    return result


def index(payload):
    rows = payload.get('transactions')
    if not isinstance(rows, list):
        raise ValueError('transactions must be an array')
    out = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Each transaction must be an object')
        key = row.get('transaction_id')
        if not isinstance(key, str) or not key.strip() or key in out:
            raise ValueError('Missing or duplicate transaction_id')
        if not isinstance(row.get('deleted', False), bool):
            raise ValueError('deleted must be boolean')
        if row.get('type') not in TYPES:
            raise ValueError('Invalid transaction type: ' + key)
        if not isinstance(row.get('currency'), str) or len(row['currency']) != 3 or not row['currency'].isalpha() or row['currency'] != row['currency'].upper():
            raise ValueError('Explicit uppercase currency required: ' + key)
        money(row.get('amount'))
        out[key] = row
    return out


def values(row):
    result = {field: row.get(field, '') for field in FIELDS}
    result['amount'] = format(money(row['amount']).normalize(), 'f')
    return result


def active(row):
    return row is not None and not row.get('deleted', False)


def plan(base, current, incoming):
    b, c, u = index(base), index(current), index(incoming)
    output = {'additions': [], 'updates': [], 'possible_deletions': [], 'conflicts': [], 'preserved_current': []}
    for key in sorted(set(b) | set(c) | set(u)):
        old, now, new = b.get(key), c.get(key), u.get(key)
        if old is None:
            if active(new) and now is None:
                output['additions'].append({'transaction_id': key, 'values': values(new)})
            elif active(new) and not active(now):
                output['conflicts'].append({'transaction_id': key, 'reason': 'current_deleted'})
            elif active(new) and active(now) and values(new) != values(now):
                output['conflicts'].append({'transaction_id': key, 'reason': 'same_id_different_addition', 'current': values(now), 'incoming': values(new)})
            elif active(now) and new is None:
                output['preserved_current'].append(key)
            continue
        if not active(old):
            if active(new):
                output['conflicts'].append({'transaction_id': key, 'reason': 'baseline_deleted_requires_explicit_restore'})
            continue
        if not active(now):
            if active(new) and values(new) != values(old):
                output['conflicts'].append({'transaction_id': key, 'reason': 'edit_after_current_deletion', 'incoming': values(new)})
            continue
        if not active(new):
            output['possible_deletions'].append({'transaction_id': key, 'current_changed': values(now) != values(old), 'reason': 'missing_or_delete_marker_requires_intent'})
            continue
        bv, cv, uv = values(old), values(now), values(new)
        edits, conflicts = {}, {}
        for field in FIELDS:
            if uv[field] == bv[field] or uv[field] == cv[field]:
                continue
            if cv[field] == bv[field]:
                edits[field] = uv[field]
            else:
                conflicts[field] = {'base': bv[field], 'current': cv[field], 'incoming': uv[field]}
        if conflicts:
            output['conflicts'].append({'transaction_id': key, 'fields': conflicts, 'nonconflicting_proposed': edits})
        elif edits:
            output['updates'].append({'transaction_id': key, 'changes': edits})
    return output


def summary(payload):
    totals = {}
    for row in index(payload).values():
        if not active(row):
            continue
        bucket = totals.setdefault(row['currency'], {kind: Decimal(0) for kind in TYPES})
        bucket[row['type']] += money(row['amount'])
    result = {}
    for currency, bucket in sorted(totals.items()):
        bucket['net_spending'] = bucket['expense'] - bucket['refund']
        result[currency] = {kind: format(amount, 'f') for kind, amount in bucket.items()}
    return {'totals_by_currency': result, 'policy': 'expense minus refund; excludes income, transfer and card_payment from net spending; flat postings only'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('plan')
    p.add_argument('base'); p.add_argument('current'); p.add_argument('incoming')
    s = sub.add_parser('summary'); s.add_argument('input')
    args = parser.parse_args()
    def read(path):
        return json.loads(Path(path).read_text(encoding='utf-8'))
    try:
        output = plan(read(args.base), read(args.current), read(args.incoming)) if args.command == 'plan' else summary(read(args.input))
    except (ValueError, TypeError, AttributeError, OSError) as exc:
        parser.exit(2, 'Validation failed: ' + str(exc) + '\n')
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
