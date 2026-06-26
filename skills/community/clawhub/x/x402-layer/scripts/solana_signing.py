#!/usr/bin/env python3
"""
Shared Solana signing helpers for x402 scripts.

Builds x402-compatible X-Payment headers for Solana accepts options.
Direct signing still uses SOLANA_SECRET_KEY. OWS support is optional-first for
wallet lookup and message-signing flows only.
"""

import base64
import json
import os
import shutil
import struct
import subprocess
from typing import Any, Dict, Optional

import requests

RPC_URL = "https://api.mainnet-beta.solana.com"


def _load_auth_mode() -> str:
    if (os.getenv("X402_USE_AWAL") or "").strip() == "1":
        return "awal"
    explicit = (os.getenv("X402_AUTH_MODE") or "auto").strip().lower()
    if explicit == "auto" and os.getenv("OWS_WALLET"):
        return "ows"
    return explicit


def _import_solders() -> Dict[str, Any]:
    try:
        from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price  # type: ignore
        from solders.hash import Hash  # type: ignore
        from solders.instruction import AccountMeta, Instruction  # type: ignore
        from solders.keypair import Keypair  # type: ignore
        from solders.message import MessageV0  # type: ignore
        from solders.null_signer import NullSigner  # type: ignore
        from solders.pubkey import Pubkey  # type: ignore
        from solders.transaction import VersionedTransaction  # type: ignore
    except ImportError as exc:
        raise ValueError("Solana signing requires solders. Install solders>=0.20.0") from exc

    return {
        "Keypair": Keypair,
        "Pubkey": Pubkey,
        "VersionedTransaction": VersionedTransaction,
        "MessageV0": MessageV0,
        "Instruction": Instruction,
        "AccountMeta": AccountMeta,
        "Hash": Hash,
        "NullSigner": NullSigner,
        "set_compute_unit_limit": set_compute_unit_limit,
        "set_compute_unit_price": set_compute_unit_price,
    }


def load_solders() -> Dict[str, Any]:
    return _import_solders()


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
        raise ValueError("Set OWS_WALLET for OWS-backed wallet lookup/signing")
    return wallet


def _lookup_ows_solana_address() -> Optional[str]:
    wallet = _load_ows_wallet_name()
    output = _run_ows(["wallet", "list"])
    blocks = [block.strip() for block in output.split("\n\n") if block.strip()]
    for block in blocks:
        if f"Name:    {wallet}" not in block and f"ID:      {wallet}" not in block:
            continue
        for line in block.splitlines():
            if line.strip().startswith("solana:") and "→" in line:
                return line.split("→", 1)[1].strip()
    return None


def has_solana_credentials() -> bool:
    mode = _load_auth_mode()
    if mode == "awal":
        return False
    if mode == "ows":
        return False
    return bool(os.getenv("SOLANA_SECRET_KEY"))


def _decode_secret_key_bytes(raw_secret: str) -> bytes:
    value = raw_secret.strip()
    if not value:
        raise ValueError("Empty Solana private key")

    if value.startswith("[") and value.endswith("]"):
        parsed = json.loads(value)
        if not isinstance(parsed, list):
            raise ValueError("Invalid Solana private key JSON format")
        return bytes(parsed)

    if "," in value:
        parsed = [int(part.strip()) for part in value.split(",")]
        return bytes(parsed)

    if all(ch in "0123456789abcdefABCDEF" for ch in value) and len(value) % 2 == 0:
        return bytes.fromhex(value)

    return b""


def _load_keypair(keypair_cls: Any) -> Any:
    raw_secret = os.getenv("SOLANA_SECRET_KEY")
    if not raw_secret:
        raise ValueError("Set SOLANA_SECRET_KEY for Solana private-key signing")

    try:
        secret_bytes = _decode_secret_key_bytes(raw_secret)
        if secret_bytes:
            return keypair_cls.from_bytes(secret_bytes)
    except Exception as exc:
        raise ValueError(f"Invalid SOLANA_SECRET_KEY: {exc}") from exc

    try:
        return keypair_cls.from_base58_string(raw_secret.strip())
    except Exception:
        pass

    try:
        return keypair_cls.from_bytes(base64.b64decode(raw_secret.strip()))
    except Exception as exc:
        raise ValueError(
            "Unsupported SOLANA_SECRET_KEY format. Use a base58 secret string or JSON byte array."
        ) from exc


def _derive_local_solana_wallet_address() -> Optional[str]:
    if not has_solana_credentials():
        return None
    solders = _import_solders()
    keypair = _load_keypair(solders["Keypair"])
    return str(keypair.pubkey())


def load_solana_wallet_address() -> Optional[str]:
    explicit = os.getenv("SOLANA_WALLET_ADDRESS") or os.getenv("WALLET_ADDRESS_SECONDARY")
    local_derived = _derive_local_solana_wallet_address()
    if explicit or local_derived:
        return explicit or local_derived
    if _load_auth_mode() == "ows":
        return _lookup_ows_solana_address()
    return None


def load_solana_keypair() -> Any:
    solders = _import_solders()
    return _load_keypair(solders["Keypair"])


def sign_solana_message_base64(message: str) -> str:
    if _load_auth_mode() == "ows":
        wallet = _load_ows_wallet_name()
        output = _run_ows(["sign", "message", "--chain", "solana", "--wallet", wallet, "--message", message, "--json"])
        try:
            payload = json.loads(output)
        except Exception as exc:
            raise ValueError("Could not parse OWS sign-message output") from exc
        signature_hex = str(payload.get("signature") or "").strip()
        if not signature_hex:
            raise ValueError("OWS sign-message did not return a signature")
        try:
            return base64.b64encode(bytes.fromhex(signature_hex)).decode()
        except Exception as exc:
            raise ValueError("OWS Solana signature was not valid hex") from exc

    keypair = load_solana_keypair()
    signature = keypair.sign_message(message.encode("utf-8"))
    return base64.b64encode(bytes(signature)).decode()


def generate_solana_asset_keypair() -> Dict[str, Any]:
    solders = _import_solders()
    keypair = solders["Keypair"]()
    return {
        "keypair": keypair,
        "address": str(keypair.pubkey()),
    }


def send_prepared_solana_transaction(
    prepared_transaction_base64: str,
    rpc_url: str,
    extra_signers: Optional[list[Any]] = None,
) -> str:
    solders = _import_solders()
    VersionedTransaction = solders["VersionedTransaction"]
    keypair = _load_keypair(solders["Keypair"])
    raw_tx = VersionedTransaction.from_bytes(base64.b64decode(prepared_transaction_base64))
    signed_tx = VersionedTransaction(raw_tx.message, [keypair, *(extra_signers or [])])
    signed_tx_base64 = base64.b64encode(bytes(signed_tx)).decode()

    response = requests.post(
        rpc_url,
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "sendTransaction",
            "params": [
                signed_tx_base64,
                {
                    "encoding": "base64",
                    "preflightCommitment": "confirmed",
                    "maxRetries": 3,
                },
            ],
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("error"):
        raise ValueError(payload["error"])
    signature = payload.get("result")
    if not signature:
        raise ValueError("Failed to send Solana transaction")
    return str(signature)


def wait_for_solana_confirmation(signature: str, rpc_url: str, timeout_seconds: int = 120) -> None:
    import time

    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        response = requests.post(
            rpc_url,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getSignatureStatuses",
                "params": [[signature], {"searchTransactionHistory": True}],
            },
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        value = ((payload.get("result") or {}).get("value") or [None])[0]
        if value:
            if value.get("err"):
                raise ValueError(f"Solana transaction failed: {value['err']}")
            confirmation_status = value.get("confirmationStatus")
            if confirmation_status in ("confirmed", "finalized"):
                return
        time.sleep(2)
    raise TimeoutError("Timed out waiting for Solana transaction confirmation")


def _get_recent_blockhash(hash_cls: Any) -> Any:
    response = requests.post(
        RPC_URL,
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getLatestBlockhash",
            "params": [{"commitment": "finalized"}],
        },
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    return hash_cls.from_string(result["result"]["value"]["blockhash"])


def _build_transaction_base64(accept_option: Dict[str, Any], payer_wallet_address: str) -> str:
    solders = _import_solders()
    Keypair = solders["Keypair"]
    Pubkey = solders["Pubkey"]
    VersionedTransaction = solders["VersionedTransaction"]
    MessageV0 = solders["MessageV0"]
    Instruction = solders["Instruction"]
    AccountMeta = solders["AccountMeta"]
    Hash = solders["Hash"]
    NullSigner = solders["NullSigner"]
    set_compute_unit_limit = solders["set_compute_unit_limit"]
    set_compute_unit_price = solders["set_compute_unit_price"]

    token_program_id = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
    ata_program_id = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
    usdc_mint_default = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

    payer_pubkey = Pubkey.from_string(payer_wallet_address)

    def get_ata(owner: Any, mint: Any) -> Any:
        seeds = [bytes(owner), bytes(token_program_id), bytes(mint)]
        ata, _ = Pubkey.find_program_address(seeds, ata_program_id)
        return ata

    def create_transfer_checked_ix(source: Any, mint: Any, dest: Any, owner: Any, amount: int, decimals: int) -> Any:
        data = bytes([12]) + struct.pack("<Q", amount) + bytes([decimals])
        keys = [
            AccountMeta(source, False, True),
            AccountMeta(mint, False, False),
            AccountMeta(dest, False, True),
            AccountMeta(owner, True, False),
        ]
        return Instruction(token_program_id, data, keys)

    blockhash = _get_recent_blockhash(Hash)

    extra = accept_option.get("extra") or {}
    fee_payer_str = extra.get("feePayer")
    fee_payer = Pubkey.from_string(fee_payer_str) if fee_payer_str else payer_pubkey
    pay_to = Pubkey.from_string(accept_option["payTo"])
    mint = Pubkey.from_string(accept_option.get("asset") or usdc_mint_default)
    amount = int(accept_option["maxAmountRequired"])

    source_ata = get_ata(payer_pubkey, mint)
    dest_ata = get_ata(pay_to, mint)

    # PayAI-backed exact payments reject oversized compute limits.
    instructions = [
        set_compute_unit_limit(40000),
        set_compute_unit_price(1000),
        create_transfer_checked_ix(source_ata, mint, dest_ata, payer_pubkey, amount, 6),
    ]

    message = MessageV0.try_compile(
        fee_payer,
        instructions,
        [],
        blockhash,
    )

    keypair = _load_keypair(Keypair)
    if str(keypair.pubkey()) != str(payer_pubkey):
        raise ValueError(
            "SOLANA_SECRET_KEY does not match payer wallet address. "
            "Set SOLANA_WALLET_ADDRESS to match keypair or use the correct key."
        )

    signers = [keypair]
    if str(fee_payer) != str(payer_pubkey):
        signers.append(NullSigner(fee_payer))

    tx = VersionedTransaction(message, signers)
    return base64.b64encode(bytes(tx)).decode()


def create_solana_xpayment_from_accept(accept_option: Dict[str, Any]) -> str:
    network = str(accept_option.get("network", "")).lower()
    if network != "solana":
        raise ValueError(f"Expected Solana accept option, got network={accept_option.get('network')}")

    if _load_auth_mode() == "awal":
        raise ValueError("AWAL mode currently supports Base payments only")

    if not has_solana_credentials():
        raise ValueError("No Solana signer available. Set SOLANA_SECRET_KEY.")

    payer = load_solana_wallet_address()
    if not payer:
        raise ValueError("Failed to resolve local Solana wallet address")

    signed_tx = _build_transaction_base64(accept_option, payer_wallet_address=payer)

    payload = {
        "x402Version": 1,
        "scheme": "exact",
        "network": "solana",
        "payload": {"transaction": signed_tx},
    }
    return base64.b64encode(json.dumps(payload).encode()).decode()
