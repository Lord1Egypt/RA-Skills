#!/usr/bin/env python3
# Reference example for agent authors.
# This script demonstrates the public SpawnXchange acquire flow.
# It is not a full supported SDK or production-ready client library.
import argparse
import base64
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

import requests
from eth_account import Account
from x402 import x402ClientSync
from x402.http.x402_http_client import x402HTTPClientSync
from x402.mechanisms.evm.exact import register_exact_evm_client
from x402.mechanisms.evm.signers import EthAccountSigner

BASE_URL = 'https://spawnxchange.com'
TERMS_URL = 'https://spawnxchange.com/terms/v1'
LICENSE_URL = 'https://spawnxchange.com/license/v1'

PUBLIC_CHAIN_TO_TRANSPORT_NETWORKS = {
    'base': {'base', 'eip155:8453'},
    'polygon': {'polygon', 'eip155:137'},
}

TRANSPORT_NETWORK_TO_PUBLIC_CHAIN = {
    'base': 'base',
    'eip155:8453': 'base',
    'polygon': 'polygon',
    'eip155:137': 'polygon',
}


def _matches_requested_chain(requirement_network: str | None, chain: str | None) -> bool:
    if not chain:
        return True
    if requirement_network is None:
        return True
    return requirement_network in PUBLIC_CHAIN_TO_TRANSPORT_NETWORKS.get(chain, {chain})


def _normalize_public_chain(network: str | None) -> str | None:
    if network is None:
        return None
    return TRANSPORT_NETWORK_TO_PUBLIC_CHAIN.get(network, network)


def _load_wallet_key(path: str) -> str:
    """Read a plain-text hex private key file, stripping whitespace."""
    return Path(path).read_text().strip()


def acquire_item(item_id: str, private_key: str | None = None, chain: str | None = None,
                 dry_run: bool = True) -> dict:
    """Quote or execute the public SpawnXchange acquire flow and return plain data.

    When dry_run is true, this only retrieves and summarizes the x402 quote.
    When dry_run is false, private_key must control an EOA that holds sufficient
    USDC and can sign the canonical x402 exact EIP-3009 payment. If a wallet
    runtime cannot produce that standard exact payment header, it is outside
    the scope of this script.
    """
    url = f'{BASE_URL}/api/v1/items/{item_id}/acquire'

    prompt_payload = {'chain': chain} if chain else {}
    prompt_resp = requests.post(url, json=prompt_payload, timeout=60)
    if prompt_resp.status_code == 200:
        purchase = prompt_resp.json()
        return {'mode': 'completed_without_payment_prompt', 'purchase': purchase}
    if prompt_resp.status_code != 402:
        raise RuntimeError(f'acquire failed: {prompt_resp.status_code}')

    encoded = prompt_resp.headers.get('PAYMENT-REQUIRED')
    if not encoded:
        raise RuntimeError('acquire failed: missing PAYMENT-REQUIRED header')

    prompt_meta = json.loads(base64.b64decode(encoded).decode('utf-8'))
    completion_payload = {
        **prompt_meta['extensions']['bazaar']['info']['input']['completion_request']['example'],
        'policy_accepted': True,
        'license_accepted': True,
        **({'chain': chain} if chain else {}),
    }
    exact_requirement = next((
        requirement for requirement in prompt_meta.get('accepts', [])
        if requirement.get('scheme') == 'exact'
        and _matches_requested_chain(requirement.get('network'), chain)
    ), None)

    amount_raw = exact_requirement and (exact_requirement.get('maxAmountRequired') or exact_requirement.get('amount'))
    amount_usdc = None
    if amount_raw is not None and completion_payload.get('currency', 'USDC') == 'USDC':
        try:
            amount_usdc = format((Decimal(str(amount_raw)) / Decimal('1000000')).normalize(), 'f')
        except InvalidOperation:
            amount_usdc = None

    quote = {key: value for key, value in {
        'requires_payment': True,
        'payment_scheme': exact_requirement and exact_requirement.get('scheme'),
        'chain': chain or _normalize_public_chain(exact_requirement and exact_requirement.get('network')) or completion_payload.get('chain'),
        'currency': completion_payload.get('currency', 'USDC'),
        'amount_smallest_unit': amount_raw,
        'amount_usdc': amount_usdc,
        'terms_url': TERMS_URL,
        'license_url': LICENSE_URL,
        'execute_instruction': (
            'Run again with --execute to authorize this payment and accept the current '
            'SpawnXchange Terms and buyer license for this purchase.'
        ),
    }.items() if value is not None}
    if dry_run:
        return {'mode': 'quote', 'quote': quote}

    if not private_key:
        raise RuntimeError('private_key is required when dry_run is false')
    if exact_requirement is None:
        raise RuntimeError("acquire failed: no supported x402 'exact' EOA requirement found")

    account = Account.from_key(private_key)
    signer = EthAccountSigner(account)
    xclient = x402ClientSync()
    register_exact_evm_client(xclient, signer)
    http_client = x402HTTPClientSync(xclient)
    payment_headers, _ = http_client.handle_402_response(dict(prompt_resp.headers), prompt_resp.content)

    retry = requests.post(url, json=completion_payload, headers=payment_headers, timeout=60)
    if retry.status_code != 200:
        raise RuntimeError(f'acquire completion failed: {retry.status_code}')
    purchase = retry.json()
    download_url = purchase.get('download_url', '')
    try:
        download_resp = requests.head(download_url, allow_redirects=True, timeout=30)
        delivery = {'verified': 200 <= download_resp.status_code < 400, 'status_code': download_resp.status_code}
    except requests.RequestException as exc:
        delivery = {'verified': False, 'reason': str(exc)}
    return {
        'mode': 'executed',
        'quote': quote,
        'purchase': purchase,
        'download_verification': delivery,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Acquire a SpawnXchange item (public flow).')
    parser.add_argument('--item-id', required=True, help='Item UUID to acquire')
    parser.add_argument('--chain', default=None, help='Preferred chain (e.g. base, polygon)')
    parser.add_argument('--execute', action='store_true',
                        help='Authorize payment and accept current SpawnXchange terms/license')
    parser.add_argument('--private-key-file', metavar='FILE',
                        help='Path to plain-text file containing the hex private key; required with --execute')
    args = parser.parse_args()

    try:
        private_key = None
        if args.execute and not args.private_key_file:
            raise RuntimeError('--private-key-file is required with --execute')
        if args.execute:
            private_key = _load_wallet_key(args.private_key_file)
        data = acquire_item(
            args.item_id,
            private_key=private_key,
            chain=args.chain,
            dry_run=not args.execute,
        )
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(data, indent=2))