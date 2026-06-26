#!/usr/bin/env python3
"""List ERC-8004 agents owned by the configured wallet or linked dashboard user."""

import argparse
import json
import sys
from typing import Optional

from erc8004_wallet_client import API_BASE, auth_chain_for_network, auth_headers, create_wallet_session, get_json
from solana_signing import load_solana_wallet_address
from wallet_signing import load_wallet_address


def _resolve_chain(args: argparse.Namespace) -> str:
    if args.chain:
        return args.chain
    if args.network:
        return auth_chain_for_network(args.network)
    return "base"


def _resolve_wallet(chain: str) -> str:
    if chain == "solana":
        wallet = load_solana_wallet_address()
        if not wallet:
            raise ValueError("Set SOLANA_SECRET_KEY or SOLANA_WALLET_ADDRESS for Solana agent listing")
        return wallet
    wallet = load_wallet_address(required=True)
    if not wallet:
        raise ValueError("Set WALLET_ADDRESS for EVM agent listing")
    return wallet


def list_agents(chain: str, network: Optional[str] = None) -> dict:
    wallet = _resolve_wallet(chain)
    session_token = create_wallet_session(chain, wallet, "erc8004_manage")
    params = {"network": network} if network else None
    return get_json(
        f"{API_BASE}/agent/erc8004/mine",
        params=params,
        headers=auth_headers(session_token),
        timeout=60,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="List ERC-8004 agents owned by the configured wallet")
    parser.add_argument(
        "--chain",
        choices=["base", "solana"],
        help="Wallet auth chain. Defaults to base unless a Solana network is provided.",
    )
    parser.add_argument(
        "--network",
        choices=[
            "base",
            "baseSepolia",
            "ethereum",
            "ethereumSepolia",
            "polygon",
            "polygonAmoy",
            "bsc",
            "bscTestnet",
            "monad",
            "monadTestnet",
            "solanaMainnet",
            "solanaDevnet",
        ],
        help="Optional network filter",
    )
    args = parser.parse_args()

    result = list_agents(chain=_resolve_chain(args), network=args.network)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        sys.exit(1)
