#!/usr/bin/env python3
"""
x402 Payment - Base (EVM) Network

Pay for API access on Base.

Modes:
- private-key (default): PRIVATE_KEY + WALLET_ADDRESS
- awal: Coinbase Agentic Wallet CLI (AWAL)

AgentKit:
- optional for human-backed agent wallet benefits
- private-key mode only in this script
"""

import argparse
import json
import os
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse

import requests

from agentkit_support import (
    build_agentkit_header,
    extract_agentkit_extension,
    registration_guidance,
    summarize_agentkit_extension,
)
from awal_bridge import awal_pay_url
from wallet_signing import is_awal_mode, load_payment_signer, load_wallet_address


def _find_base_accept_option(challenge: Dict[str, Any]) -> Dict[str, Any]:
    for option in challenge.get("accepts", []):
        network = str(option.get("network", "")).lower()
        if network == "base" or "8453" in network:
            return option
    raise ValueError("No Base payment option found in challenge")


def _challenge_amount(challenge: Dict[str, Any]) -> Optional[int]:
    try:
        return int(_find_base_accept_option(challenge)["maxAmountRequired"])
    except Exception:
        return None


def _request(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> requests.Response:
    merged_headers = {"Accept": "application/json"}
    if headers:
        merged_headers.update(headers)
    return requests.get(url, headers=merged_headers, timeout=timeout)


def _normalize_address(value: str) -> str:
    return value.strip().lower()


def _purchase_url(endpoint_url: str) -> str:
    parsed = urlparse(endpoint_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.setdefault("action", "purchase")
    return urlunparse(parsed._replace(query=urlencode(query)))


def _agentkit_mode_default() -> str:
    raw = (os.getenv("X402_AGENTKIT_MODE") or "auto").strip().lower()
    return raw if raw in {"off", "auto", "required"} else "auto"


def _preflight_agentkit(
    endpoint_url: str,
    challenge: Dict[str, Any],
    agentkit_mode: str,
    wallet_address: str,
) -> Tuple[Optional[str], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    extension = extract_agentkit_extension(challenge)

    if not extension:
        if agentkit_mode == "required":
            raise ValueError("This endpoint does not advertise an AgentKit benefit")
        return None, challenge, None

    print(f"AgentKit detected: {summarize_agentkit_extension(extension)}")

    if is_awal_mode():
        note = "AgentKit signing in this script currently requires private-key mode. AWAL mode will continue without the benefit."
        if agentkit_mode == "required":
            raise ValueError(note)
        print(note)
        return None, challenge, None

    agentkit_header = build_agentkit_header(extension, wallet_address)
    agentkit_headers = {
        "agentkit": agentkit_header,
        "x-wallet-address": wallet_address,
    }

    response = _request(endpoint_url, headers=agentkit_headers)

    if response.status_code == 200:
        print("AgentKit benefit qualified this wallet. Access granted without payment.")
        if response.headers.get("content-type", "").startswith("application/json"):
            return agentkit_header, None, response.json()
        return agentkit_header, None, {"data": response.text[:500]}

    if response.status_code != 402:
        raise ValueError(f"Unexpected AgentKit preflight status {response.status_code}: {response.text}")

    next_challenge = response.json()
    original_amount = _challenge_amount(challenge)
    next_amount = _challenge_amount(next_challenge)

    if original_amount is not None and next_amount is not None and next_amount < original_amount:
        print(f"AgentKit discount qualified this wallet: {original_amount} -> {next_amount} atomic USDC units")
        return agentkit_header, next_challenge, None

    if agentkit_mode == "required":
        raise ValueError(
            "This wallet did not qualify for the AgentKit benefit.\n"
            + registration_guidance(wallet_address)
        )

    print("This wallet did not qualify for the AgentKit benefit. Continuing with the normal price.")
    print(registration_guidance(wallet_address))
    return agentkit_header, next_challenge, None


def pay_for_access(endpoint_url: str, agentkit_mode: str = "auto") -> Dict[str, Any]:
    """Execute paid request to an x402 endpoint."""
    endpoint_url = _purchase_url(endpoint_url)

    if is_awal_mode():
        wallet = load_wallet_address(required=False)
        headers = {"x-wallet-address": wallet} if wallet else None
        print(f"Requesting with AWAL: {endpoint_url}")
        return awal_pay_url(endpoint_url, method="GET", headers=headers)

    signer = load_payment_signer()

    print(f"Requesting: {endpoint_url}")

    response = _request(endpoint_url)

    if response.status_code == 200:
        print("Access granted (free endpoint or already authorized)")
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return {"data": response.text[:500]}

    if response.status_code != 402:
        return {"error": f"Unexpected status {response.status_code}", "response": response.text}

    challenge = response.json()
    agentkit_header: Optional[str] = None

    if agentkit_mode != "off":
        agentkit_header, updated_challenge, preflight_result = _preflight_agentkit(
            endpoint_url=endpoint_url,
            challenge=challenge,
            agentkit_mode=agentkit_mode,
            wallet_address=signer.wallet,
        )
        if preflight_result is not None:
            return preflight_result
        if updated_challenge is not None:
            challenge = updated_challenge

    base_option = _find_base_accept_option(challenge)
    pay_to = base_option["payTo"]
    amount = int(base_option["maxAmountRequired"])

    if _normalize_address(pay_to) == _normalize_address(signer.wallet):
        return {
            "error": (
                "Self-payment is not allowed for this endpoint. "
                "The connected wallet matches the endpoint payout wallet. "
                "Use a different buyer wallet to test purchases."
            )
        }

    print(f"Payment required: {amount} atomic USDC units")

    x_payment = signer.create_x402_payment_header(pay_to=pay_to, amount=amount)

    request_headers = {
        "X-Payment": x_payment,
        "x-wallet-address": signer.wallet,
        "Accept": "application/json",
    }
    if agentkit_header:
        request_headers["agentkit"] = agentkit_header

    response = requests.get(endpoint_url, headers=request_headers, timeout=45)

    print(f"Response: {response.status_code}")

    if response.status_code == 200:
        if response.headers.get("content-type", "").startswith("application/json"):
            return response.json()
        return {"data": response.text[:500]}

    return {"error": response.text}


def main() -> int:
    parser = argparse.ArgumentParser(description="Pay a Base x402 endpoint, optionally with World AgentKit")
    parser.add_argument("endpoint_url", help="Full x402 endpoint URL")
    parser.add_argument(
        "--agentkit",
        choices=["off", "auto", "required"],
        default=_agentkit_mode_default(),
        help="AgentKit mode: off, auto, or required (default from X402_AGENTKIT_MODE or auto)",
    )
    args = parser.parse_args()

    result = pay_for_access(args.endpoint_url, agentkit_mode=args.agentkit)
    print(json.dumps(result, indent=2)[:2000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
