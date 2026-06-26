#!/usr/bin/env python3
"""
Shared Base payment signing utilities for x402 scripts.

Modes:
- private-key: local EVM private key signing (existing behavior)
- awal: use Coinbase Agentic Wallet CLI (AWAL) from wrapper helpers
- ows: use Open Wallet Standard (OWS) for wallet lookup and message signing
"""

import base64
import json
import os
import secrets
import shutil
import subprocess
import time
from typing import Any, Dict, Optional

from eth_account import Account
from eth_account.messages import encode_defunct

USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
USDC_NAME = "USD Coin"
USDC_VERSION = "2"
BASE_CHAIN_ID = 8453


def load_auth_mode() -> str:
    """
    Supported values:
    - auto (default): private-key if creds exist, OWS if OWS_WALLET is set, otherwise error
    - private-key: force local EVM key signing
    - awal: force AWAL mode for Base payments
    - ows: force Open Wallet Standard mode for wallet lookup and message signing
    """
    if (os.getenv("X402_USE_AWAL") or "").strip() == "1":
        return "awal"
    explicit = (os.getenv("X402_AUTH_MODE") or "auto").strip().lower()
    if explicit == "auto" and os.getenv("OWS_WALLET"):
        return "ows"
    return explicit


def is_awal_mode() -> bool:
    return load_auth_mode() == "awal"


def is_ows_mode() -> bool:
    return load_auth_mode() == "ows"




def _build_ows_command(args: list[str]) -> list[str]:
    explicit_bin = (os.getenv("OWS_BIN") or "").strip()
    if explicit_bin:
        return [explicit_bin, *args]

    local_ows = shutil.which("ows")
    if local_ows:
        return [local_ows, *args]

    raise ValueError(
        "OWS binary not found in PATH. Install it with `npm install -g @open-wallet-standard/core` "
        "or set OWS_BIN to the full executable path."
    )


def _run_ows(args: list[str], timeout: int = 180) -> str:
    proc = subprocess.run(_build_ows_command(args), text=True, capture_output=True, timeout=timeout)
    if proc.returncode != 0:
        raise ValueError((proc.stderr or proc.stdout or "OWS command failed").strip())
    return (proc.stdout or "").strip()


def _load_ows_wallet_name() -> str:
    wallet = (os.getenv("OWS_WALLET") or "").strip()
    if not wallet:
        raise ValueError("Set OWS_WALLET for OWS wallet-backed flows")
    return wallet


def _lookup_ows_evm_address() -> str:
    wallet = _load_ows_wallet_name()
    output = _run_ows(["wallet", "list"])
    blocks = [block.strip() for block in output.split("\n\n") if block.strip()]
    for block in blocks:
        if f"Name:    {wallet}" not in block and f"ID:      {wallet}" not in block:
            continue
        for line in block.splitlines():
            if "eip155:" in line and "→" in line:
                return line.split("→", 1)[1].strip().lower()
    raise ValueError(f"Could not resolve an OWS EVM address for wallet '{wallet}'")

def load_wallet_address(required: bool = True, allow_awal_fallback: bool = True) -> Optional[str]:
    wallet = os.getenv("WALLET_ADDRESS")

    if not wallet and allow_awal_fallback and is_awal_mode():
        try:
            from awal_bridge import get_awal_evm_address  # type: ignore

            wallet = get_awal_evm_address(required=False)
        except Exception:
            wallet = None

    if not wallet and is_ows_mode():
        try:
            wallet = _lookup_ows_evm_address()
        except Exception:
            wallet = None

    if required and not wallet:
        if is_awal_mode() and allow_awal_fallback:
            raise ValueError(
                "Set WALLET_ADDRESS or authenticate AWAL so address can be resolved"
            )
        if is_ows_mode():
            raise ValueError("Set OWS_WALLET or ensure the OWS wallet exists so the address can be resolved")
        raise ValueError("Set WALLET_ADDRESS environment variable")
    return wallet


def has_private_key_credentials() -> bool:
    return bool(os.getenv("PRIVATE_KEY") and os.getenv("WALLET_ADDRESS"))


class PaymentSigner:
    def __init__(self, wallet: str, private_key: str) -> None:
        self.mode = "private-key"
        self.wallet = wallet
        self.private_key = private_key

    def sign_typed_data(self, typed_data: Dict[str, Any]) -> str:
        signed = Account.from_key(self.private_key).sign_typed_data(
            typed_data["domain"],
            {"TransferWithAuthorization": typed_data["types"]["TransferWithAuthorization"]},
            typed_data["message"],
        )
        sig = signed.signature.hex()
        # Ensure 0x prefix for EVM compatibility
        if not sig.startswith("0x"):
            sig = "0x" + sig
        return sig

    def create_x402_payment_payload(
        self,
        pay_to: str,
        amount: int,
        valid_after: int = 0,
        valid_before: Optional[int] = None,
        nonce: Optional[str] = None,
    ) -> Dict[str, Any]:
        if valid_before is None:
            valid_before = int(time.time()) + 3600
        if nonce is None:
            nonce = "0x" + secrets.token_hex(32)

        typed_data = {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
                "TransferWithAuthorization": [
                    {"name": "from", "type": "address"},
                    {"name": "to", "type": "address"},
                    {"name": "value", "type": "uint256"},
                    {"name": "validAfter", "type": "uint256"},
                    {"name": "validBefore", "type": "uint256"},
                    {"name": "nonce", "type": "bytes32"},
                ],
            },
            "primaryType": "TransferWithAuthorization",
            "domain": {
                "name": USDC_NAME,
                "version": USDC_VERSION,
                "chainId": BASE_CHAIN_ID,
                "verifyingContract": USDC_ADDRESS,
            },
            "message": {
                "from": self.wallet,
                "to": pay_to,
                "value": amount,
                "validAfter": valid_after,
                "validBefore": valid_before,
                "nonce": nonce,
            },
        }

        signature = self.sign_typed_data(typed_data)

        return {
            "x402Version": 1,
            "scheme": "exact",
            "network": "base",
            "payload": {
                "signature": signature,
                "authorization": {
                    "from": self.wallet,
                    "to": pay_to,
                    "value": str(amount),
                    "validAfter": str(valid_after),
                    "validBefore": str(valid_before),
                    "nonce": nonce,
                },
            },
        }

    def create_x402_payment_header(self, pay_to: str, amount: int) -> str:
        payload = self.create_x402_payment_payload(pay_to=pay_to, amount=amount)
        return base64.b64encode(json.dumps(payload).encode()).decode()


def load_payment_signer() -> PaymentSigner:
    mode = load_auth_mode()
    if mode == "awal":
        raise ValueError("AWAL mode does not use local Base signer")
    if mode == "ows":
        raise ValueError("OWS mode currently supports wallet lookup and message-signing flows. Direct Base payment signing still requires PRIVATE_KEY and WALLET_ADDRESS.")

    if mode not in ("auto", "private-key"):
        raise ValueError("X402_AUTH_MODE must be one of: auto, private-key, awal, ows")

    wallet = load_wallet_address(required=True, allow_awal_fallback=False)
    private_key = os.getenv("PRIVATE_KEY")

    if not private_key or not wallet:
        raise ValueError("Set PRIVATE_KEY and WALLET_ADDRESS for private-key mode")

    return PaymentSigner(wallet=wallet, private_key=private_key)


def sign_evm_message(message: str) -> str:
    if is_ows_mode():
        wallet = _load_ows_wallet_name()
        output = _run_ows(["sign", "message", "--chain", "eip155:8453", "--wallet", wallet, "--message", message, "--json"])
        try:
            payload = json.loads(output)
        except Exception as exc:
            raise ValueError("Could not parse OWS sign-message output") from exc
        signature = str(payload.get("signature") or "").strip()
        if not signature:
            raise ValueError("OWS sign-message did not return a signature")
        if not signature.startswith("0x"):
            signature = "0x" + signature
        return signature

    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        raise ValueError("Set PRIVATE_KEY for EVM wallet challenge signing")
    signed = Account.from_key(private_key).sign_message(encode_defunct(text=message))
    signature = signed.signature.hex()
    if not signature.startswith("0x"):
        signature = "0x" + signature
    return signature
