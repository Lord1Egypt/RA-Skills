#!/usr/bin/env python3
"""Validate and submit a fixed-shape Solana custodial order transaction."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from solana.rpc.api import Client
from solana.rpc.commitment import Commitment
from solana.rpc.types import TxOpts
from solders.instruction import Instruction
from solders.keypair import Keypair
from solders.message import Message
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from spl.token.instructions import (
    TransferParams as SplTransferParams,
    get_associated_token_address,
    transfer as spl_transfer,
)


TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
MEMO_PROGRAM_ID = Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr")
SOLANA_USDC_MINT = Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
SVIM_SOLANA_RECIPIENT = Pubkey.from_string(
    "CdnwmDJhaokY6r5W9EpFGvxnf4xDcAfe2XPHqCvfR2cf"
)
PUBLIC_SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
DEFAULT_CONFIG = Path.home() / ".config" / "swimmer-stock-trading" / "config.json"


class ValidationError(ValueError):
    pass


@dataclass(frozen=True)
class WalletConfig:
    keypair: Keypair
    rpc_url: str
    trusted_stock_mints: dict[str, str]
    max_offer_raw_by_mint: dict[str, int]


def _decode_object(data: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"Cannot parse {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must contain one JSON object")
    return value


def _secure_config_text() -> str:
    """Read only the fixed config path, atomically and without following symlinks."""
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise ValidationError("This platform cannot enforce no-symlink config access")
    common = os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW
    directory_flags = common | os.O_DIRECTORY
    opened: list[int] = []
    try:
        home_fd = os.open(Path.home(), directory_flags)
        opened.append(home_fd)
        dot_config_fd = os.open(".config", directory_flags, dir_fd=home_fd)
        opened.append(dot_config_fd)
        skill_dir_fd = os.open("swimmer-stock-trading", directory_flags, dir_fd=dot_config_fd)
        opened.append(skill_dir_fd)
        directory = os.fstat(skill_dir_fd)
        if hasattr(os, "getuid") and directory.st_uid != os.getuid():
            for item in reversed(opened):
                os.close(item)
            raise ValidationError("Fixed config directory must be owned by the current user")
        if stat.S_IMODE(directory.st_mode) != 0o700:
            for item in reversed(opened):
                os.close(item)
            raise ValidationError("Config directory permissions are unsafe; require exact mode 0700")
        descriptor = os.open("config.json", common, dir_fd=skill_dir_fd)
        opened.append(descriptor)
    except OSError as exc:
        for item in reversed(opened):
            os.close(item)
        raise ValidationError(f"Cannot open fixed no-symlink config path: {exc}") from exc
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            raise ValidationError("Fixed config must be a regular file")
        if hasattr(os, "getuid") and info.st_uid != os.getuid():
            raise ValidationError("Fixed config must be owned by the current user")
        if stat.S_IMODE(info.st_mode) != 0o600:
            raise ValidationError("Config permissions are unsafe; require exact mode 0600")
        with os.fdopen(descriptor, "r", encoding="utf-8", closefd=False) as handle:
            return handle.read()
    finally:
        for item in reversed(opened):
            os.close(item)


def _canonical_positive_integer(value: Any, field: str) -> int:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a positive integer string")
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValidationError(f"{field} must be a positive integer string") from exc
    if parsed <= 0 or str(parsed) != value:
        raise ValidationError(f"{field} must be a canonical positive integer string")
    return parsed


def _validate_policy_map(value: Any, field: str) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ValidationError(f"Config {field} must be an object")
    result: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not isinstance(item, str):
            raise ValidationError(f"Config {field} keys and values must be strings")
        result[key] = item
    return result


def load_config() -> WalletConfig:
    config = _decode_object(_secure_config_text(), "fixed config")
    private_key = config.get("private_key")
    if not isinstance(private_key, str) or private_key.startswith("REPLACE_"):
        raise ValidationError("Config private_key must be a base58 Solana keypair")
    if config.get("rpc_url") != PUBLIC_SOLANA_RPC_URL:
        raise ValidationError(f"rpc_url must be exactly {PUBLIC_SOLANA_RPC_URL}")
    if config.get("accepted_custodial_recipient") != str(SVIM_SOLANA_RECIPIENT):
        raise ValidationError(
            "Verify the custodial recipient independently, then place its exact "
            "address in accepted_custodial_recipient"
        )

    trusted = _validate_policy_map(config.get("trusted_stock_mints"), "trusted_stock_mints")
    normalized: dict[str, str] = {}
    for ticker, mint_text in trusted.items():
        upper = ticker.upper()
        if ticker != upper or not upper.isascii() or not upper.isalnum():
            raise ValidationError("trusted_stock_mints keys must be uppercase ASCII tickers")
        try:
            mint = Pubkey.from_string(mint_text)
        except Exception as exc:
            raise ValidationError(f"Invalid trusted mint for {ticker}") from exc
        if mint == SOLANA_USDC_MINT:
            raise ValidationError(f"Trusted stock mint for {ticker} cannot be USDC")
        normalized[ticker] = str(mint)

    cap_strings = _validate_policy_map(config.get("max_offer_raw_by_mint"), "max_offer_raw_by_mint")
    caps = {mint: _canonical_positive_integer(cap, f"cap for {mint}") for mint, cap in cap_strings.items()}
    for mint in caps:
        try:
            Pubkey.from_string(mint)
        except Exception as exc:
            raise ValidationError(f"Invalid mint in max_offer_raw_by_mint: {mint}") from exc

    try:
        keypair = Keypair.from_base58_string(private_key)
    except Exception as exc:
        raise ValidationError("Config private_key is not a valid keypair") from exc
    return WalletConfig(keypair, PUBLIC_SOLANA_RPC_URL, normalized, caps)


def _ui_amount(raw_amount: int, decimals: int) -> str:
    return format(Decimal(raw_amount).scaleb(-decimals), "f")


def _token_balance(client: Client, owner: Pubkey, mint: Pubkey, symbol: str) -> dict[str, Any]:
    token_account = get_associated_token_address(owner, mint)
    commitment = Commitment("confirmed")
    account = client.get_account_info(token_account, commitment=commitment)
    if account.value is None:
        supply = client.get_token_supply(mint, commitment=commitment).value
        raw_amount, decimals = 0, supply.decimals
    else:
        balance = client.get_token_account_balance(token_account, commitment=commitment).value
        raw_amount, decimals = int(balance.amount), balance.decimals
    return {
        "symbol": symbol,
        "mint": str(mint),
        "token_account": str(token_account),
        "raw_amount": str(raw_amount),
        "decimals": decimals,
        "ui_amount": _ui_amount(raw_amount, decimals),
    }


def get_balances(config: WalletConfig, stock: str | None) -> dict[str, Any]:
    wallet = config.keypair.pubkey()
    client = Client(config.rpc_url, timeout=20)
    lamports = client.get_balance(wallet, commitment=Commitment("confirmed")).value
    result: dict[str, Any] = {
        "status": "success",
        "wallet_address": str(wallet),
        "network": "solana-mainnet",
        "sol": {"lamports": str(lamports), "decimals": 9, "ui_amount": _ui_amount(lamports, 9)},
        "usdc": _token_balance(client, wallet, SOLANA_USDC_MINT, "USDC"),
        "stock": None,
    }
    if stock is not None:
        ticker = stock.upper()
        if stock != ticker or ticker not in config.trusted_stock_mints:
            raise ValidationError("Stock must be an uppercase ticker in trusted_stock_mints")
        result["stock"] = _token_balance(
            client, wallet, Pubkey.from_string(config.trusted_stock_mints[ticker]), f"{ticker}s"
        )
    return result


def _required_string(plan: dict[str, Any], field: str) -> str:
    value = plan.get(field)
    if not isinstance(value, str) or not value:
        raise ValidationError(f"Plan field {field} must be a non-empty string")
    return value


def _canonical_nonnegative_integer(value: str, field: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValidationError(f"{field} must be a nonnegative integer string") from exc
    if parsed < 0 or str(parsed) != value:
        raise ValidationError(f"{field} must be a canonical nonnegative integer string")
    return parsed


def _intent(plan: dict[str, Any], config: WalletConfig) -> dict[str, Any]:
    allowed_fields = {
        "stock", "side", "order_type", "token_pair_name", "offer_mint",
        "stock_mint", "offer_amount_raw", "request_amount_raw",
    }
    extras = sorted(set(plan) - allowed_fields)
    if extras:
        raise ValidationError(f"Plan contains unsupported fields: {', '.join(extras)}")

    stock = _required_string(plan, "stock").upper()
    side = _required_string(plan, "side").upper()
    order_type = _required_string(plan, "order_type").upper()
    pair = _required_string(plan, "token_pair_name")
    if stock not in config.trusted_stock_mints:
        raise ValidationError("Stock is not present in the independently verified mint allowlist")
    try:
        offer_mint = Pubkey.from_string(_required_string(plan, "offer_mint"))
        stock_mint = Pubkey.from_string(_required_string(plan, "stock_mint"))
    except Exception as exc:
        raise ValidationError("Plan contains an invalid Solana mint") from exc
    if str(stock_mint) != config.trusted_stock_mints[stock]:
        raise ValidationError("Plan stock mint does not match trusted_stock_mints")

    offer_text = _required_string(plan, "offer_amount_raw")
    request_text = _required_string(plan, "request_amount_raw")
    offer = _canonical_positive_integer(offer_text, "offer_amount_raw")
    if order_type == "MARKET":
        request = _canonical_nonnegative_integer(request_text, "request_amount_raw")
    elif order_type == "LIMIT":
        request = _canonical_positive_integer(request_text, "request_amount_raw")
    else:
        raise ValidationError("order_type must be MARKET or LIMIT")
    if side not in {"BUY", "SELL"}:
        raise ValidationError("side must be BUY or SELL")
    stock_symbol = f"{stock}s"
    expected_pair = f"USDC-{stock_symbol}" if side == "BUY" else f"{stock_symbol}-USDC"
    if pair != expected_pair or ".S" in pair.upper():
        raise ValidationError("Plan must use the exact non-legacy canonical pair")
    if side == "BUY" and offer_mint != SOLANA_USDC_MINT:
        raise ValidationError("BUY offer mint must be canonical Solana USDC")
    if side == "SELL" and offer_mint != stock_mint:
        raise ValidationError("SELL offer mint must equal the trusted stock mint")
    cap = config.max_offer_raw_by_mint.get(str(offer_mint))
    if cap is None:
        raise ValidationError("Offered mint has no max_offer_raw_by_mint safety cap")
    if offer > cap:
        raise ValidationError(f"Offer exceeds configured raw safety cap {cap}")

    return {
        "network": "solana-mainnet",
        "wallet_address": str(config.keypair.pubkey()),
        "stock": stock,
        "stock_symbol": stock_symbol,
        "side": side,
        "order_type": order_type,
        "token_pair_name": pair,
        "offer_mint": str(offer_mint),
        "stock_mint": str(stock_mint),
        "recipient": str(SVIM_SOLANA_RECIPIENT),
        "offer_amount_raw": offer_text,
        "request_amount_raw": request_text,
        "request_amount": request,
        "offer_cap_raw": str(cap),
        "settlement_model": "custodial-off-chain-non-atomic",
    }


def _confirmation_id(intent: dict[str, Any]) -> str:
    canonical = json.dumps(intent, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def _order_memo(intent: dict[str, Any]) -> str:
    return json.dumps(
        {
            "did_id": intent["wallet_address"],
            "type": intent["order_type"],
            "offer": intent["offer_amount_raw"],
            "request": intent["request_amount_raw"],
            "token_address": intent["stock_mint"],
            "customer_id": "SVIM",
            "trade_source": "SVIM",
            "currency": "USDC",
        },
        separators=(",", ":"),
    )


def _build_order_transaction(intent: dict[str, Any], keypair: Keypair, recent_blockhash) -> Transaction:
    offer_mint = Pubkey.from_string(intent["offer_mint"])
    transfer_ix = spl_transfer(
        SplTransferParams(
            program_id=TOKEN_PROGRAM_ID,
            source=get_associated_token_address(keypair.pubkey(), offer_mint),
            dest=get_associated_token_address(SVIM_SOLANA_RECIPIENT, offer_mint),
            owner=keypair.pubkey(),
            amount=int(intent["offer_amount_raw"]),
        )
    )
    memo_ix = Instruction(MEMO_PROGRAM_ID, _order_memo(intent).encode("utf-8"), [])
    message = Message.new_with_blockhash([transfer_ix, memo_ix], keypair.pubkey(), recent_blockhash)
    return Transaction.new_unsigned(message)


def inspect_plan(plan: dict[str, Any], config: WalletConfig) -> dict[str, Any]:
    intent = _intent(plan, config)
    unbounded_market = intent["order_type"] == "MARKET" and intent["request_amount"] == 0
    return {
        "status": "validated",
        "confirmation_id": _confirmation_id(intent),
        **intent,
        "irreversible_transfer": True,
        "on_chain_minimum_receive": None if unbounded_market else intent["request_amount_raw"],
        "execution_amount_unknown": unbounded_market,
        "on_chain_settlement_guarantee": "none",
        "authorization_text": (
            f"Authorize irreversible transfer of {intent['offer_amount_raw']} raw units of "
            f"{intent['offer_mint']} to {intent['recipient']} for custodial order processing."
        ),
        "warning": (
            "This is not an atomic swap. The transfer cannot enforce execution, receipt of "
            "stock tokens or USDC, cancellation, or refund."
        ),
    }


def send(plan: dict[str, Any], config: WalletConfig, confirmation: str) -> dict[str, Any]:
    intent = _intent(plan, config)
    if confirmation != _confirmation_id(intent):
        raise ValidationError("Confirmation digest does not match the validated intent")
    client = Client(config.rpc_url, timeout=20)
    blockhash = client.get_latest_blockhash(commitment=Commitment("confirmed")).value.blockhash
    unsigned = _build_order_transaction(intent, config.keypair, blockhash)
    signed = Transaction([config.keypair], unsigned.message, unsigned.message.recent_blockhash)
    simulation = client.simulate_transaction(signed, sig_verify=True, commitment=Commitment("confirmed"))
    if simulation.value.err is not None:
        raise ValidationError(f"Simulation failed: {simulation.value.err}")
    response = client.send_transaction(
        signed,
        opts=TxOpts(skip_confirmation=False, preflight_commitment=Commitment("confirmed"), max_retries=4),
    )
    return {
        "status": "submitted",
        "signature": str(response.value),
        "confirmation_id": confirmation,
        "settlement_status": "not-verified",
        "warning": "Submission and on-chain confirmation do not prove custodial order settlement.",
    }


def _plan_from_stdin() -> dict[str, Any]:
    if sys.stdin.isatty():
        raise ValidationError("Provide the non-secret plan JSON on standard input")
    return _decode_object(sys.stdin.read(), "plan from standard input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("address")
    balance = commands.add_parser("balance")
    balance.add_argument("--stock", help="uppercase ticker from trusted_stock_mints")
    commands.add_parser("inspect")
    send_parser = commands.add_parser("send")
    send_parser.add_argument("--confirm", required=True)
    args = parser.parse_args()
    try:
        config = load_config()
        if args.command == "address":
            result = {"wallet_address": str(config.keypair.pubkey()), "config_path": str(DEFAULT_CONFIG)}
        elif args.command == "balance":
            result = get_balances(config, args.stock)
        else:
            plan = _plan_from_stdin()
            result = inspect_plan(plan, config) if args.command == "inspect" else send(plan, config, args.confirm)
        print(json.dumps(result, sort_keys=True))
        return 0
    except ValidationError as exc:
        print(json.dumps({"status": "rejected", "error": str(exc)}), file=sys.stderr)
        return 2
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
