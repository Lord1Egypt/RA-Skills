#!/usr/bin/env python3
"""
Shared Base payment signing utilities for x402 scripts.
Uses local EVM private key signing for USDC TransferWithAuthorization.
"""

import base64
import hashlib
import json
import os
import re
import secrets
import shutil
import stat
import subprocess
import time
import uuid
from typing import Any, Dict, Optional

from eth_account import Account
from eth_account.messages import encode_defunct

# Pinned so a wallet operation never runs whatever version the registry happens to serve.
# Kept in step with scripts/ows_cli.py.
OWS_PINNED_PACKAGE = "@open-wallet-standard/core@0.5.0"

USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
USDC_NAME = "USD Coin"
USDC_VERSION = "2"
BASE_CHAIN_ID = 8453
BASE_CAIP2 = "eip155:8453"

# Robinhood Chain (Arbitrum L2) — USDG stablecoin, EIP-3009 transferWithAuthorization.
# Same "exact" scheme as Base USDC; only the EIP-712 domain differs. The domain
# name/version below are verified against the USDG contract's on-chain
# DOMAIN_SEPARATOR (name="Global Dollar", version="1", chainId=4663).
USDG_ADDRESS = "0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168"
USDG_NAME = "Global Dollar"
USDG_VERSION = "1"
ROBINHOOD_CHAIN_ID = 4663
ROBINHOOD_CAIP2 = "eip155:4663"

# Arc (Circle's L1) — native USDC, EIP-3009 transferWithAuthorization. Gas is
# denominated in USDC on this chain, which is why the platform floors credit
# top-ups at $5 there. The domain name/version below are verified against the
# token's on-chain DOMAIN_SEPARATOR (name="USDC", version="2", chainId=5042).
ARC_USDC_ADDRESS = "0x3600000000000000000000000000000000000000"
ARC_USDC_NAME = "USDC"
ARC_USDC_VERSION = "2"
ARC_CHAIN_ID = 5042
ARC_CAIP2 = "eip155:5042"

# network label -> EIP-712 domain + settlement network for the x402 payload.
EVM_ASSETS = {
    "base": {
        "address": USDC_ADDRESS, "name": USDC_NAME, "version": USDC_VERSION,
        "chain_id": BASE_CHAIN_ID, "network": "base",
    },
    "robinhood": {
        "address": USDG_ADDRESS, "name": USDG_NAME, "version": USDG_VERSION,
        "chain_id": ROBINHOOD_CHAIN_ID, "network": "robinhood",
    },
    "arc": {
        "address": ARC_USDC_ADDRESS, "name": ARC_USDC_NAME, "version": ARC_USDC_VERSION,
        "chain_id": ARC_CHAIN_ID, "network": "arc",
    },
}


# NO .env AUTO-LOADING. Credentials come only from the process environment the caller
# explicitly exported.
#
# This used to call a third-party env-file loader, which walks UP from THIS FILE's directory
# looking for a .env. The default install path is ./x402-compute inside the user's project, so
# that walk reached the project's own .env and every parent's. A signing module has no business
# picking up secrets based on where it happens to be unpacked.
#
# The sharp edge was not the key material — it was OWS_BIN. A .env anywhere above the install
# dir could set OWS_WALLET (which flips load_compute_auth_mode() to "ows") plus OWS_BIN, and
# _run_ows would then subprocess.run whatever that pointed at. Two lines in a file we never
# asked the user to create, and we execute an arbitrary binary.
#
# Every documented setup path already says `export`. See the same removal in x402-layer v1.3.1.


def _load_solders_keypair() -> Any:
    try:
        from solders.keypair import Keypair  # type: ignore
    except ImportError as exc:
        raise ValueError("Solana signing requires solders. Install solders>=0.20.0") from exc

    secret_key = (os.getenv("SOLANA_SECRET_KEY") or "").strip()
    if not secret_key:
        raise ValueError("Set SOLANA_SECRET_KEY for Solana signing")

    # Support either JSON array format or base58 keypair string.
    if secret_key.startswith("["):
        try:
            secret_bytes = bytes(json.loads(secret_key))
            return Keypair.from_bytes(secret_bytes)
        except Exception as exc:
            raise ValueError("Invalid SOLANA_SECRET_KEY JSON array format") from exc

    try:
        return Keypair.from_base58_string(secret_key)
    except Exception as exc:
        raise ValueError("Invalid SOLANA_SECRET_KEY base58 format") from exc


def load_solana_wallet_address(required: bool = True) -> Optional[str]:
    explicit = (os.getenv("SOLANA_WALLET_ADDRESS") or os.getenv("WALLET_ADDRESS_SECONDARY") or "").strip()
    if explicit:
        return explicit

    try:
        keypair = _load_solders_keypair()
        return str(keypair.pubkey())
    except Exception:
        if required:
            raise ValueError("Set SOLANA_WALLET_ADDRESS or SOLANA_SECRET_KEY")
        return None


def load_wallet_address(required: bool = True) -> Optional[str]:
    wallet = os.getenv("WALLET_ADDRESS")

    if required and not wallet:
        raise ValueError("Set WALLET_ADDRESS environment variable")
    return wallet


def load_compute_chain() -> str:
    """
    Resolve compute auth chain from env/wallet context.
    Priority:
    1) COMPUTE_AUTH_CHAIN (base|solana)
    2) WALLET_ADDRESS shape (0x... => base)
    3) SOLANA credentials present => solana
    4) default base
    """
    explicit = (os.getenv("COMPUTE_AUTH_CHAIN") or "").strip().lower()
    if explicit in ("base", "solana"):
        return explicit

    wallet = (os.getenv("WALLET_ADDRESS") or "").strip()
    if wallet:
        return "base" if wallet.lower().startswith("0x") else "solana"

    if os.getenv("SOLANA_SECRET_KEY") or os.getenv("SOLANA_WALLET_ADDRESS"):
        return "solana"
    return "base"


def load_compute_auth_mode() -> str:
    """
    Supported values:
    - auto (default): OWS if OWS_WALLET is set, otherwise local key mode
    - private-key: force local signing
    - ows: force Open Wallet Standard message signing
    """
    explicit = (os.getenv("COMPUTE_AUTH_MODE") or "auto").strip().lower()
    if explicit in {"private-key", "ows"}:
        return explicit
    if os.getenv("OWS_WALLET"):
        return "ows"
    return "private-key"


def is_ows_mode() -> bool:
    return load_compute_auth_mode() == "ows"


def _resolve_ows_bin(explicit_bin: str) -> str:
    """
    OWS_BIN names a program we are about to execute, so it gets checked rather than trusted.

    An absolute path is required: a bare name like "ows" would resolve through PATH, and a
    relative one like "./ows" through the current directory, either of which can be steered by
    whatever the caller happened to cd into. Requiring an absolute path to a file that already
    exists means the value has to name a real, deliberately-chosen program.
    """
    expanded = os.path.expanduser(explicit_bin)
    if not os.path.isabs(expanded):
        raise ValueError(
            f"OWS_BIN must be an absolute path to the ows executable (got {explicit_bin!r}). "
            "A bare or relative name would be resolved against PATH or the current directory."
        )

    # Resolve symlinks and hand the RESOLVED path to subprocess. Checking one path and
    # executing another is the gap a symlink swap walks through; there is still a TOCTOU
    # window between these checks and exec, but resolving first keeps the thing we validated
    # and the thing we run the same file.
    resolved = os.path.realpath(expanded)
    if not os.path.isfile(resolved):
        raise ValueError(f"OWS_BIN points at {expanded!r}, which is not an existing file")
    if not os.access(resolved, os.X_OK):
        raise ValueError(f"OWS_BIN points at {resolved!r}, which is not executable")

    # A world-writable binary, or one in a world-writable directory, can be replaced by any
    # local user between now and the next signing call.
    for path, label in ((resolved, "file"), (os.path.dirname(resolved), "parent directory")):
        try:
            if os.stat(path).st_mode & stat.S_IWOTH:
                raise ValueError(
                    f"OWS_BIN refuses {resolved!r}: its {label} is world-writable, so another "
                    "local user could swap the binary that signs your transactions."
                )
        except OSError:
            raise ValueError(f"OWS_BIN could not stat {path!r}")
    return resolved


def _build_ows_command(args: list[str]) -> list[str]:
    explicit_bin = (os.getenv("OWS_BIN") or "").strip()
    if explicit_bin:
        return [_resolve_ows_bin(explicit_bin), *args]

    local_ows = shutil.which("ows")
    if local_ows:
        return [local_ows, *args]

    # NO npx FALLBACK. This used to run `npx -y @open-wallet-standard/core`, which downloads
    # and executes whatever the registry currently serves for an UNPINNED package — and then
    # hands it a wallet operation. A signing path must never fetch its own signer at runtime.
    # ows_cli.py already took this stance; the two now agree.
    raise ValueError(
        "OWS binary not found. Install it explicitly:\n"
        f"  npm install -g {OWS_PINNED_PACKAGE}\n"
        "Then ensure `ows` is on PATH, or set OWS_BIN to its absolute path.\n"
        "Runtime npx downloads are deliberately not used for wallet operations."
    )


def _run_ows(args: list[str], timeout: int = 180) -> str:
    proc = subprocess.run(
        _build_ows_command(args),
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise ValueError((proc.stderr or proc.stdout or "OWS command failed").strip())
    return (proc.stdout or "").strip()


def _load_ows_wallet_name(cli_wallet: Optional[str] = None) -> str:
    wallet = (cli_wallet or os.getenv("OWS_WALLET") or "").strip()
    if not wallet:
        raise ValueError("Set OWS_WALLET or pass an explicit OWS wallet name/ID")
    return wallet


def _lookup_ows_wallet_address(chain: str, wallet_name: Optional[str] = None) -> str:
    wallet = _load_ows_wallet_name(wallet_name)
    output = _run_ows(["wallet", "list"])

    blocks = [block.strip() for block in output.split("\n\n") if block.strip()]
    for block in blocks:
        if f"Name:    {wallet}" not in block and f"ID:      {wallet}" not in block:
            continue

        if chain == "solana":
            match = re.search(r"solana:[^\n]*→\s*([1-9A-HJ-NP-Za-km-z]{32,64})", block)
            if match:
                return match.group(1).strip()
        else:
            match = re.search(r"eip155:[^\n]*→\s*(0x[a-fA-F0-9]{40})", block)
            if match:
                return match.group(1).strip().lower()

    raise ValueError(f"Could not resolve an OWS {chain} address for wallet '{wallet}'")


def _sign_message_with_ows(chain: str, message: str, wallet_name: Optional[str] = None) -> str:
    wallet = _load_ows_wallet_name(wallet_name)
    ows_chain = "solana" if chain == "solana" else BASE_CAIP2
    output = _run_ows(
        [
            "sign",
            "message",
            "--chain",
            ows_chain,
            "--wallet",
            wallet,
            "--message",
            message,
            "--json",
        ]
    )

    try:
        payload = json.loads(output)
    except Exception as exc:
        raise ValueError("Could not parse OWS sign-message output") from exc

    signature = str(payload.get("signature") or "").strip()
    if not signature:
        raise ValueError("OWS sign-message did not return a signature")
    return signature


class PaymentSigner:
    def __init__(self, wallet: str, private_key: str) -> None:
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
        network: str = "base",
    ) -> Dict[str, Any]:
        asset = EVM_ASSETS.get(network.lower())
        if asset is None:
            raise ValueError(f"Unsupported EVM payment network '{network}' (expected: {', '.join(EVM_ASSETS)})")
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
                "name": asset["name"],
                "version": asset["version"],
                "chainId": asset["chain_id"],
                "verifyingContract": asset["address"],
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
            "network": asset["network"],
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

    def create_x402_payment_header(self, pay_to: str, amount: int, network: str = "base") -> str:
        payload = self.create_x402_payment_payload(pay_to=pay_to, amount=amount, network=network)
        return base64.b64encode(json.dumps(payload).encode()).decode()


def load_payment_signer() -> PaymentSigner:

    if is_ows_mode():
        raise ValueError(
            "OWS mode currently supports compute auth and API-key creation flows. "
            "Provision and extend still require direct Base or Solana signing keys."
        )

    wallet = load_wallet_address(required=True)
    private_key = os.getenv("PRIVATE_KEY")

    if not private_key or not wallet:
        raise ValueError("Set PRIVATE_KEY and WALLET_ADDRESS for Base payments")

    return PaymentSigner(wallet=wallet, private_key=private_key)


def _compute_auth_message(
    chain: str,
    address: str,
    method: str,
    path: str,
    body_hash: str,
    timestamp_ms: int,
    nonce: str,
) -> str:
    return "\n".join(
        [
            "X402-COMPUTE-AUTH",
            "v1",
            chain,
            address,
            method.upper(),
            path,
            body_hash,
            str(timestamp_ms),
            nonce,
        ]
    )


def create_compute_auth_headers(
    method: str,
    path: str,
    body_str: str = "",
    chain: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, str]:
    """
    Create auth headers for x402 Compute management endpoints.
    Supports:
    - API key auth via COMPUTE_API_KEY
    - Base wallet message signature (EIP-191)
    - Solana wallet message signature
    """
    api_key = api_key or os.getenv("COMPUTE_API_KEY")
    if api_key:
        return {"X-API-Key": api_key}

    resolved_chain = (chain or load_compute_chain()).strip().lower()
    if resolved_chain not in ("base", "solana"):
        raise ValueError("Compute auth chain must be 'base' or 'solana'")

    body_hash = hashlib.sha256((body_str or "").encode()).hexdigest()
    timestamp_ms = int(time.time() * 1000)
    nonce = uuid.uuid4().hex

    if is_ows_mode():
        address = _lookup_ows_wallet_address(resolved_chain)
        message = _compute_auth_message(
            chain=resolved_chain,
            address=address,
            method=method,
            path=path,
            body_hash=body_hash,
            timestamp_ms=timestamp_ms,
            nonce=nonce,
        )
        signature_hex = _sign_message_with_ows(resolved_chain, message)

        if resolved_chain == "base":
            if not signature_hex.startswith("0x"):
                signature_hex = f"0x{signature_hex}"
            return {
                "X-Auth-Address": address,
                "X-Auth-Chain": "base",
                "X-Auth-Signature": signature_hex,
                "X-Auth-Timestamp": str(timestamp_ms),
                "X-Auth-Nonce": nonce,
                "X-Auth-Sig-Encoding": "hex",
            }

        try:
            signature_base64 = base64.b64encode(bytes.fromhex(signature_hex)).decode()
        except Exception as exc:
            raise ValueError("OWS Solana signature was not valid hex") from exc

        return {
            "X-Auth-Address": address,
            "X-Auth-Chain": "solana",
            "X-Auth-Signature": signature_base64,
            "X-Auth-Timestamp": str(timestamp_ms),
            "X-Auth-Nonce": nonce,
            "X-Auth-Sig-Encoding": "base64",
        }

    if resolved_chain == "base":
        wallet = load_wallet_address(required=True)
        private_key = os.getenv("PRIVATE_KEY")
        if not private_key:
            raise ValueError("Set PRIVATE_KEY for Base auth signing")

        address = wallet.lower()
        message = _compute_auth_message(
            chain="base",
            address=address,
            method=method,
            path=path,
            body_hash=body_hash,
            timestamp_ms=timestamp_ms,
            nonce=nonce,
        )
        signed = Account.from_key(private_key).sign_message(encode_defunct(text=message))
        signature = signed.signature.hex()
        if not signature.startswith("0x"):
            signature = "0x" + signature

        return {
            "X-Auth-Address": address,
            "X-Auth-Chain": "base",
            "X-Auth-Signature": signature,
            "X-Auth-Timestamp": str(timestamp_ms),
            "X-Auth-Nonce": nonce,
            "X-Auth-Sig-Encoding": "hex",
        }

    # Solana auth signing
    address = load_solana_wallet_address(required=True)
    keypair = _load_solders_keypair()
    message = _compute_auth_message(
        chain="solana",
        address=address,
        method=method,
        path=path,
        body_hash=body_hash,
        timestamp_ms=timestamp_ms,
        nonce=nonce,
    )
    sig = keypair.sign_message(message.encode())
    signature = base64.b64encode(bytes(sig)).decode()

    return {
        "X-Auth-Address": address,
        "X-Auth-Chain": "solana",
        "X-Auth-Signature": signature,
        "X-Auth-Timestamp": str(timestamp_ms),
        "X-Auth-Nonce": nonce,
        "X-Auth-Sig-Encoding": "base64",
    }
