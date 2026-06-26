#!/usr/bin/env python3
"""Shared wallet-authenticated client helpers for ERC-8004 agent flows."""

import os
from typing import Any, Dict, Optional

import requests

from solana_signing import sign_solana_message_base64
from wallet_signing import sign_evm_message

API_BASE = (os.getenv("X402_API_BASE") or "https://api.x402layer.cc").rstrip("/")


def is_solana_network(network: str) -> bool:
    return network in ("solanaMainnet", "solanaDevnet")


def auth_chain_for_network(network: str) -> str:
    return "solana" if is_solana_network(network) else "base"


def post_json(
    url: str,
    body: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 60,
) -> Dict[str, Any]:
    response = requests.post(url, json=body, headers=headers or {}, timeout=timeout)
    try:
        data = response.json()
    except Exception:
        data = {"error": response.text}
    if not response.ok:
        message = data.get("error") or response.text
        details = data.get("details")
        if details:
            raise ValueError(f"{message}: {details}")
        raise ValueError(str(message))
    return data


def get_json(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 60,
) -> Dict[str, Any]:
    response = requests.get(url, params=params or {}, headers=headers or {}, timeout=timeout)
    try:
        data = response.json()
    except Exception:
        data = {"error": response.text}
    if not response.ok:
        message = data.get("error") or response.text
        details = data.get("details")
        if details:
            raise ValueError(f"{message}: {details}")
        raise ValueError(str(message))
    return data


def create_wallet_session(chain: str, wallet_address: str, action: str) -> str:
    challenge = post_json(
        f"{API_BASE}/agent/auth/challenge",
        {
            "chain": chain,
            "walletAddress": wallet_address,
            "action": action,
        },
        timeout=30,
    )
    message = str(challenge["message"])
    nonce = str(challenge["nonce"])

    if chain == "solana":
        signature = sign_solana_message_base64(message)
        signature_encoding = "base64"
    else:
        signature = sign_evm_message(message)
        signature_encoding = "hex"

    verified = post_json(
        f"{API_BASE}/agent/auth/verify",
        {
            "chain": chain,
            "walletAddress": wallet_address,
            "action": action,
            "nonce": nonce,
            "signature": signature,
            "signatureEncoding": signature_encoding,
        },
        timeout=30,
    )
    session_token = verified.get("sessionToken")
    if not session_token:
        raise ValueError("Worker did not return a session token")
    return str(session_token)


def auth_headers(session_token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {session_token}"}
