#!/usr/bin/env python3
"""
Wallet-signed auth for Studio support APIs.

Usage:
  python support_auth.py login
  python support_auth.py whoami --token <token>
"""

import argparse
import json
import os
import sys
from typing import Any, Dict

import requests

from wallet_signing import load_wallet_address, sign_evm_message

STUDIO_BASE = os.getenv("X402_STUDIO_BASE_URL", "https://studio.x402layer.cc").rstrip("/")


def _request_json(method: str, path: str, payload: Dict[str, Any] | None = None, token: str | None = None) -> Dict[str, Any]:
    headers = {"Accept": "application/json"}
    if payload is not None:
      headers["Content-Type"] = "application/json"
    if token:
      headers["Authorization"] = f"Bearer {token}"

    response = requests.request(
        method,
        f"{STUDIO_BASE}{path}",
        headers=headers,
        json=payload,
        timeout=30,
    )

    try:
        data = response.json()
    except Exception:
        data = {"error": response.text}

    if response.status_code >= 400:
        raise ValueError(data.get("error") or f"Request failed with status {response.status_code}")
    return data


def login() -> Dict[str, Any]:
    wallet_address = load_wallet_address(required=True)
    challenge = _request_json(
        "POST",
        "/api/support/agent/auth/nonce",
        {"wallet_address": wallet_address},
    )

    signature = sign_evm_message(challenge["message"])
    verified = _request_json(
        "POST",
        "/api/support/agent/auth/verify",
        {
            "wallet_address": wallet_address,
            "nonce": challenge["nonce"],
            "signature": signature,
        },
    )

    return verified


def whoami(token: str) -> Dict[str, Any]:
    return _request_json("GET", "/api/support/agent/threads", token=token)


def main() -> int:
    parser = argparse.ArgumentParser(description="Authenticate a wallet for Studio support APIs")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("login", help="Create a support API bearer token with wallet signature")

    whoami_parser = subparsers.add_parser("whoami", help="Check that a support token works")
    whoami_parser.add_argument("--token", default=os.getenv("SUPPORT_AGENT_TOKEN"), help="Support bearer token")

    args = parser.parse_args()

    try:
        if args.command == "login":
            result = login()
        elif args.command == "whoami":
            if not args.token:
                raise ValueError("Pass --token or set SUPPORT_AGENT_TOKEN")
            result = whoami(args.token)
        else:
            parser.print_help()
            return 0
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
