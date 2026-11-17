#!/usr/bin/env python3
"""
x402 Credit-Based Consumption

Consume API endpoints using pre-purchased credits instead of per-request payments.
Credits provide instant access without blockchain latency.

Every credit spend is signed by the wallet that owns the credits (the gateway rejects a
bare x-wallet-address header, because anyone can read a wallet's balance and type its
address). One signature per request; no gas, no transaction.

Usage:
    python consume_credits.py <endpoint_url> [--chain base|solana]

Example:
    python consume_credits.py https://api.x402layer.cc/e/weather-data

Environment Variables:
    Base:   WALLET_ADDRESS + PRIVATE_KEY (or X402_AUTH_MODE=ows)
    Solana: SOLANA_SECRET_KEY (or SOLANA_WALLET_ADDRESS + OWS)
    CREDITS_CHAIN - optional default chain (base | solana)
"""

import hashlib
import json
import os
import sys
import time
import uuid
from typing import Dict, Tuple
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

import requests

SOLANA_ALPHABET = set("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")


def _print_usage() -> None:
    print("Usage: python consume_credits.py <endpoint_url> [--chain base|solana]")
    print("Example: python consume_credits.py https://api.x402layer.cc/e/weather-data")


def _looks_solana(address: str) -> bool:
    return 32 <= len(address) <= 44 and set(address) <= SOLANA_ALPHABET


def resolve_wallet(chain_hint: str = "") -> Tuple[str, str]:
    """Return (chain, address). Solana addresses are kept exactly as-is (never lowercased)."""
    chain = (chain_hint or os.getenv("CREDITS_CHAIN") or "").strip().lower()
    if not chain:
        explicit = (os.getenv("WALLET_ADDRESS") or "").strip()
        if explicit.startswith("0x"):
            chain = "base"
        elif explicit and _looks_solana(explicit):
            chain = "solana"
        elif os.getenv("SOLANA_SECRET_KEY") and not os.getenv("PRIVATE_KEY"):
            chain = "solana"
        else:
            chain = "base"

    if chain == "solana":
        from solana_signing import load_solana_wallet_address

        address = load_solana_wallet_address()
        if not address:
            explicit = (os.getenv("WALLET_ADDRESS") or "").strip()
            address = explicit if _looks_solana(explicit) else None
        if not address:
            raise ValueError("Set SOLANA_SECRET_KEY (or SOLANA_WALLET_ADDRESS with OWS) to spend Solana credits")
        return "solana", address

    if chain != "base":
        raise ValueError("chain must be 'base' or 'solana'")
    from wallet_signing import load_wallet_address

    address = load_wallet_address(required=True)
    return "base", address.lower()


def build_credits_auth_headers(chain: str, address: str, method: str, path_url: str, body: bytes = b"") -> Dict[str, str]:
    """Sign X402-CREDITS-AUTH v1 for one request. path_url is the exact path+query sent."""
    timestamp_ms = int(time.time() * 1000)
    nonce = uuid.uuid4().hex
    message = "\n".join(
        [
            "X402-CREDITS-AUTH",
            "v1",
            chain,
            address,
            method.upper(),
            path_url,
            hashlib.sha256(body or b"").hexdigest(),
            str(timestamp_ms),
            nonce,
        ]
    )

    if chain == "base":
        from wallet_signing import sign_evm_message

        signature, encoding = sign_evm_message(message), "hex"
    else:
        from solana_signing import sign_solana_message_base64

        signature, encoding = sign_solana_message_base64(message), "base64"

    return {
        "x-wallet-address": address,
        "X-Auth-Address": address,
        "X-Auth-Chain": chain,
        "X-Auth-Signature": signature,
        "X-Auth-Timestamp": str(timestamp_ms),
        "X-Auth-Nonce": nonce,
        "X-Auth-Sig-Encoding": encoding,
    }


def consume_with_credits(endpoint_url: str, chain_hint: str = "") -> dict:
    """Consume an endpoint using credits."""
    try:
        chain, wallet = resolve_wallet(chain_hint)
    except ValueError as exc:
        return {"error": str(exc)}

    parsed = urlparse(endpoint_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["useCredits"] = "1"
    credits_url = urlunparse(parsed._replace(query=urlencode(query)))

    print(f"Wallet: {wallet} ({chain})")
    print(f"Consuming: {credits_url}")

    # Sign exactly the path+query that will go on the wire.
    prepared = requests.Request("GET", credits_url, headers={"Accept": "application/json"}).prepare()
    try:
        prepared.headers.update(build_credits_auth_headers(chain, wallet, "GET", prepared.path_url))
    except Exception as exc:
        return {"error": f"Could not sign credit request: {exc}"}

    try:
        with requests.Session() as session:
            response = session.send(prepared, timeout=30)
    except requests.RequestException as exc:
        return {"error": str(exc)}

    print(f"Response: {response.status_code}")

    if response.status_code == 200:
        return response.json() if response.headers.get("content-type", "").startswith("application/json") else {"data": response.text[:500]}
    elif response.status_code == 402:
        return {"error": "Insufficient credits", "challenge": response.json()}
    else:
        return {"error": response.text}


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] in {"-h", "--help"}:
        _print_usage()
        sys.exit(0)

    chain_arg = ""
    if "--chain" in args:
        i = args.index("--chain")
        if i + 1 >= len(args):
            _print_usage()
            sys.exit(1)
        chain_arg = args[i + 1]
        args = args[:i] + args[i + 2:]

    if len(args) < 1:
        _print_usage()
        sys.exit(1)

    result = consume_with_credits(args[0], chain_arg)
    print(json.dumps(result, indent=2)[:500])
