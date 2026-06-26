#!/usr/bin/env python3
"""Update an existing ERC-8004 or Solana-8004 agent using wallet-authenticated APIs."""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from erc8004_wallet_client import API_BASE, auth_chain_for_network, auth_headers, create_wallet_session, post_json
from register_agent import _send_evm_contract_tx
from solana_signing import load_solana_wallet_address, send_prepared_solana_transaction, wait_for_solana_confirmation
from wallet_signing import is_ows_mode, load_wallet_address


def _resolve_wallet(chain: str) -> str:
    if chain == "solana":
        wallet = load_solana_wallet_address()
        if not wallet:
            raise ValueError("Set SOLANA_SECRET_KEY or SOLANA_WALLET_ADDRESS for Solana agent updates")
        return wallet
    wallet = load_wallet_address(required=True)
    if not wallet:
        raise ValueError("Set WALLET_ADDRESS for EVM agent updates")
    return wallet


def _normalize_list(values: Optional[List[str]]) -> List[str]:
    return [value.strip() for value in (values or []) if value and value.strip()]


def _build_update_body(args: argparse.Namespace) -> Dict[str, Any]:
    body: Dict[str, Any] = {"network": args.network}
    chain = auth_chain_for_network(args.network)
    if chain == "solana":
        if not args.asset_address:
            raise ValueError("--asset-address is required for Solana agent updates")
        body["assetAddress"] = args.asset_address
    else:
        if args.agent_id is None:
            raise ValueError("--agent-id is required for EVM agent updates")
        body["agentId"] = args.agent_id

    if args.name is not None:
        body["name"] = args.name
    if args.description is not None:
        body["description"] = args.description
    if args.endpoint is not None:
        body["endpoint"] = args.endpoint
    if args.image is not None:
        body["image"] = args.image
    if args.version is not None:
        body["version"] = args.version

    if args.clear_tags:
        body["tags"] = []
    elif args.tag:
        body["tags"] = _normalize_list(args.tag)

    if args.private and args.public:
        raise ValueError("Use only one of --public or --private")
    if args.public:
        body["is_public"] = True
    if args.private:
        body["is_public"] = False

    if args.clear_endpoints:
        body["endpointIds"] = []
        body["customEndpoints"] = []
    else:
        if args.endpoint_id:
            body["endpointIds"] = _normalize_list(args.endpoint_id)
        if args.custom_endpoint:
            body["customEndpoints"] = _normalize_list(args.custom_endpoint)

    if len(body) <= 2:
        raise ValueError("No updates specified")

    return body


def update_agent(args: argparse.Namespace) -> Dict[str, Any]:
    chain = auth_chain_for_network(args.network)
    wallet = _resolve_wallet(chain)
    session_token = create_wallet_session(chain, wallet, "erc8004_manage")
    headers = auth_headers(session_token)
    body = _build_update_body(args)

    prepare = post_json(
        f"{API_BASE}/agent/erc8004/update/prepare",
        body,
        headers=headers,
        timeout=120,
    )
    if args.prepare_only:
        return {"success": True, "prepare": prepare}

    finalize_body: Dict[str, Any] = dict(body)
    tx_payload: Dict[str, Optional[str]] = {}

    if prepare.get("requiresOnChainUpdate"):
        if is_ows_mode():
            raise ValueError(
                "OWS can handle wallet-auth update flows, but this agent update requires an on-chain transaction. "
                "Use direct signing keys for the actual on-chain update step."
            )
        if chain == "solana":
            prepared_tx = (((prepare.get("tx") or {}).get("prepared") or {}).get("transaction"))
            rpc_url = ((prepare.get("tx") or {}).get("rpcUrl")) or (
                "https://api.devnet.solana.com" if args.network == "solanaDevnet" else "https://api.mainnet-beta.solana.com"
            )
            if not prepared_tx:
                raise ValueError("Prepare response is missing the Solana transaction payload")
            tx_signature = send_prepared_solana_transaction(
                prepared_transaction_base64=str(prepared_tx),
                rpc_url=str(rpc_url),
            )
            wait_for_solana_confirmation(tx_signature, str(rpc_url))
            finalize_body["tokenUri"] = prepare.get("tokenUri")
            finalize_body["txSignature"] = tx_signature
            tx_payload["setUri"] = tx_signature
        else:
            onchain_action = prepare.get("onChainAction") or {}
            tx_hash = _send_evm_contract_tx(
                network=args.network,
                contract_address=str(onchain_action["contractAddress"]),
                abi=list(onchain_action["abi"]),
                function_name=str(onchain_action["functionName"]),
                args=list(onchain_action.get("args") or []),
            )
            finalize_body["tokenUri"] = prepare.get("tokenUri")
            finalize_body["txHash"] = tx_hash
            tx_payload["setUri"] = tx_hash

    finalize = post_json(
        f"{API_BASE}/agent/erc8004/update/finalize",
        finalize_body,
        headers=headers,
        timeout=120,
    )
    return {
        "success": True,
        "prepare": prepare,
        "finalize": finalize,
        "transactions": tx_payload,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Update an ERC-8004/Solana-8004 agent")
    parser.add_argument(
        "--network",
        required=True,
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
        help="Target agent network",
    )
    parser.add_argument("--agent-id", type=int, help="EVM ERC-8004 agent id")
    parser.add_argument("--asset-address", help="Solana asset address")
    parser.add_argument("--name", help="Updated agent name")
    parser.add_argument("--description", help="Updated agent description")
    parser.add_argument("--endpoint", help="Updated primary or fallback endpoint URL")
    parser.add_argument("--image", help="Updated image URL")
    parser.add_argument("--version", help="Updated agent version")
    parser.add_argument("--tag", action="append", default=[], help="Repeatable agent tag")
    parser.add_argument("--clear-tags", action="store_true", help="Replace tags with an empty list")
    parser.add_argument("--endpoint-id", action="append", default=[], help="Repeatable platform endpoint UUID")
    parser.add_argument("--custom-endpoint", action="append", default=[], help="Repeatable custom endpoint URL")
    parser.add_argument("--clear-endpoints", action="store_true", help="Replace endpointIds/customEndpoints with empty lists")
    parser.add_argument("--public", action="store_true", help="Make the agent public in the marketplace")
    parser.add_argument("--private", action="store_true", help="Make the agent private in the marketplace")
    parser.add_argument("--prepare-only", action="store_true", help="Only run update/prepare and print the result")
    args = parser.parse_args()

    result = update_agent(args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        sys.exit(1)
