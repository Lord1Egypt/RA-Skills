#!/usr/bin/env python3
import argparse
import json
from decimal import Decimal
from pathlib import Path

import requests

BASE_URL = 'https://spawnxchange.com'


def _load_api_key(path: str) -> str:
    """Read api_key field from a JSON file (e.g. saved by register_agent.py)."""
    data = json.loads(Path(path).read_text())
    key = data.get('api_key')
    if not key:
        raise RuntimeError(f'api_key field not found in {path}')
    return key


def format_amount(amount_text):
    amount = Decimal(str(amount_text or '0'))
    return format(amount.normalize(), 'f') if amount else '0'


def get_pending_payouts(api_key):
    resp = requests.get(
        f'{BASE_URL}/api/v1/seller/payouts',
        headers={'X-API-KEY': api_key},
        timeout=30,
    )
    if resp.status_code != 200:
        raise RuntimeError(
            f'payout lookup failed: {resp.status_code} {resp.text[:500]}'
        )

    body = resp.json()
    chain_amounts = {}
    errors = {}

    for payout in body.get('payouts', []):
        if payout.get('currency') != 'USDC':
            continue
        chain = payout.get('chain')
        if not chain:
            continue
        if payout.get('status') == 'ok':
            chain_amounts[chain] = format_amount(payout.get('amount'))
        else:
            chain_amounts[chain] = None
            errors[chain] = payout.get('status', 'unknown_error')

    known_amounts = [Decimal(value) for value in chain_amounts.values() if value is not None]
    data = {
        'source': 'spawnxchange_api',
        'currency': 'USDC',
        'pending': chain_amounts,
        'total_pending': format(sum(known_amounts, Decimal('0')).normalize(), 'f') if known_amounts else '0',
    }
    if errors:
        data['errors'] = errors
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check pending USDC payouts via SpawnXchange API.')
    parser.add_argument('--api-key-file', required=True, metavar='FILE',
                        help='Path to api-key.json written by register_agent.py')
    args = parser.parse_args()

    try:
        api_key = _load_api_key(args.api_key_file)
        data = get_pending_payouts(api_key)
    except Exception as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(data, indent=2))