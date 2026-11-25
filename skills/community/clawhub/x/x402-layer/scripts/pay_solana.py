#!/usr/bin/env python3
"""
x402 Payment - Solana Network

Pay for API access using USDC on Solana.

Signer support:
- private-key mode: SOLANA_SECRET_KEY
"""

import json
import sys

import requests

import x402_wire
from solana_signing import create_solana_payment_header, has_solana_credentials, load_solana_wallet_address


def _find_solana_accept(challenge: dict) -> dict:
    for option in challenge.get("accepts", []):
        if x402_wire.network_name(option.get("network")) == "solana":
            return option
    raise ValueError("No Solana payment option available in challenge")


def pay_for_access(endpoint_url: str) -> dict:
    """Execute paid request to an x402 endpoint using Solana payment option."""
    if not has_solana_credentials():
        return {
            "error": (
                "No Solana signer available. Set SOLANA_SECRET_KEY "
                "(and optionally SOLANA_WALLET_ADDRESS if you need explicit wallet override)."
            )
        }

    print(f"Requesting: {endpoint_url}")

    response = requests.get(endpoint_url, headers={"Accept": "application/json"}, timeout=30)

    if response.status_code == 200:
        print("Access granted (free endpoint)")
        return response.json() if response.headers.get("content-type", "").startswith("application/json") else {"data": response.text}

    if response.status_code != 402:
        return {"error": f"Unexpected status: {response.status_code}", "response": response.text}

    # v2 PAYMENT-REQUIRED header first, v1 JSON body otherwise (x402_wire).
    challenge = x402_wire.read_challenge(response)
    try:
        solana_option = _find_solana_accept(challenge)
    except ValueError as exc:
        return {"error": str(exc)}

    print(f"Solana payment required: {solana_option.get('maxAmountRequired')} atomic units")

    try:
        header_name, x_payment = create_solana_payment_header(challenge, solana_option)
    except Exception as exc:
        return {"error": f"Failed to create Solana payment: {exc}"}

    wallet_address = load_solana_wallet_address()
    if not wallet_address:
        return {"error": "Failed to resolve Solana wallet address"}

    # From here the payment is SENT. A timeout, 202 or 5xx is pending, never a reason to pay again.
    try:
        response = requests.get(
            endpoint_url,
            headers={
                header_name: x_payment,
                "x-wallet-address": wallet_address,
                "Accept": "application/json",
            },
            timeout=45,
        )
    except requests.RequestException as exc:
        return x402_wire.pending_result(None, exc)

    print(f"Response: {response.status_code}")

    if x402_wire.is_ambiguous_status(response.status_code):
        return x402_wire.pending_result(response.status_code, response.text)

    settlement = x402_wire.read_payment_response(response)
    if settlement and settlement.get("transaction"):
        print(f"Settled: {settlement.get('transaction')} on {settlement.get('network')}")

    if response.status_code == 200:
        return response.json() if response.headers.get("content-type", "").startswith("application/json") else {"data": response.text[:500]}

    return {"error": response.text}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pay_solana.py <endpoint_url>")
        sys.exit(1)

    result = pay_for_access(sys.argv[1])
    print(json.dumps(result, indent=2)[:2000])
