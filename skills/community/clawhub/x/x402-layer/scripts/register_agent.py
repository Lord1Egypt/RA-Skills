#!/usr/bin/env python3
"""
x402 ERC-8004 Agent Registration.

Registration mode:
- wallet-first registration through worker challenge/session APIs
- the same wallet signs the challenge and sends the on-chain transaction
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

from erc8004_wallet_client import API_BASE, create_wallet_session, is_solana_network, post_json
from solana_signing import (
    generate_solana_asset_keypair,
    load_solana_wallet_address,
    send_prepared_solana_transaction,
    wait_for_solana_confirmation,
)
from wallet_signing import (
    is_awal_mode,
    is_ows_mode,
    load_wallet_address,
)

EVM_RPC_URLS = {
    "base": os.getenv("BASE_RPC_URL") or "https://mainnet.base.org",
    "baseSepolia": os.getenv("BASE_SEPOLIA_RPC_URL") or "https://sepolia.base.org",
    "ethereum": os.getenv("ETHEREUM_RPC_URL") or "https://cloudflare-eth.com",
    "ethereumSepolia": os.getenv("ETHEREUM_SEPOLIA_RPC_URL") or "https://ethereum-sepolia-rpc.publicnode.com",
    "polygon": os.getenv("POLYGON_RPC_URL") or "https://polygon-rpc.com",
    "polygonAmoy": os.getenv("POLYGON_AMOY_RPC_URL") or "https://rpc-amoy.polygon.technology",
    "bsc": os.getenv("BSC_RPC_URL") or "https://bsc-dataseed.binance.org",
    "bscTestnet": os.getenv("BSC_TESTNET_RPC_URL") or "https://data-seed-prebsc-1-s1.binance.org:8545",
    "monad": os.getenv("MONAD_RPC_URL") or "https://rpc.monad.xyz",
    "monadTestnet": os.getenv("MONAD_TESTNET_RPC_URL") or "https://testnet-rpc.monad.xyz",
}


def _resolve_owner_address(network: str, owner_address: Optional[str]) -> str:
    if owner_address:
        return owner_address
    if is_solana_network(network):
        sol_wallet = load_solana_wallet_address()
        if not sol_wallet:
            raise ValueError(
                "Solana registration requires ownerAddress. Set --owner-address or configure SOLANA_SECRET_KEY/SOLANA_WALLET_ADDRESS."
            )
        return sol_wallet
    wallet = load_wallet_address(required=True)
    if not wallet:
        raise ValueError("Failed to resolve WALLET_ADDRESS")
    return wallet


def _assert_local_signer_matches_owner(network: str, owner: str) -> None:
    if is_solana_network(network):
        local_wallet = load_solana_wallet_address()
        if local_wallet and local_wallet != owner:
            raise ValueError("ownerAddress must match the configured Solana signing wallet")
        return

    local_wallet = load_wallet_address(required=True)
    if local_wallet.lower() != owner.lower():
        raise ValueError("ownerAddress must match WALLET_ADDRESS for wallet-first EVM registration")


def _normalize_string_list(values: Optional[List[str]]) -> List[str]:
    return [value.strip() for value in (values or []) if value and value.strip()]


def _build_registration_body(
    name: str,
    description: str,
    endpoint: Optional[str],
    network: str,
    owner_address: str,
    image: Optional[str] = None,
    version: Optional[str] = None,
    tags: Optional[List[str]] = None,
    endpoint_ids: Optional[List[str]] = None,
    custom_endpoints: Optional[List[str]] = None,
    asset_address: Optional[str] = None,
) -> Dict[str, Any]:
    body: Dict[str, Any] = {
        "name": name,
        "description": description,
        "network": network,
        "ownerAddress": owner_address,
    }
    if endpoint and endpoint.strip():
        body["endpoint"] = endpoint.strip()
    if image:
        body["image"] = image
    if version and version.strip():
        body["version"] = version.strip()

    normalized_tags = _normalize_string_list(tags)
    if normalized_tags:
        body["tags"] = normalized_tags

    normalized_endpoint_ids = _normalize_string_list(endpoint_ids)
    if normalized_endpoint_ids:
        body["endpointIds"] = normalized_endpoint_ids

    normalized_custom_endpoints = _normalize_string_list(custom_endpoints)
    if normalized_custom_endpoints:
        body["customEndpoints"] = normalized_custom_endpoints

    if asset_address:
        body["assetAddress"] = asset_address

    return body


def _send_evm_contract_tx(
    network: str,
    contract_address: str,
    abi: list[Dict[str, Any]],
    function_name: str,
    args: list[Any],
) -> str:
    from web3 import Web3

    private_key = os.getenv("PRIVATE_KEY")
    wallet_address = load_wallet_address(required=True, allow_awal_fallback=False)
    if not private_key or not wallet_address:
        raise ValueError("Set PRIVATE_KEY and WALLET_ADDRESS for wallet-first EVM registration")

    rpc_url = EVM_RPC_URLS.get(network)
    if not rpc_url:
        raise ValueError(f"Unsupported EVM network for wallet-first registration: {network}")

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise ValueError(f"Failed to connect to EVM RPC for {network}")

    checksum_wallet = Web3.to_checksum_address(wallet_address)
    checksum_contract = Web3.to_checksum_address(contract_address)
    contract = w3.eth.contract(address=checksum_contract, abi=abi)
    # Harden dynamic dispatch: only allow real, simple-named ABI functions
    # (never dunder/arbitrary attributes), even though function_name comes from
    # the trusted platform API. Constrains attribute access to known methods.
    abi_functions = {f.get("name") for f in abi if isinstance(f, dict) and f.get("type") == "function"}
    if not function_name.isidentifier() or function_name.startswith("_") or function_name not in abi_functions:
        raise ValueError(f"Refusing dynamic call to non-ABI contract function: {function_name!r}")
    contract_fn = getattr(contract.functions, function_name)(*args)

    nonce = w3.eth.get_transaction_count(checksum_wallet)
    tx: Dict[str, Any] = {
        "from": checksum_wallet,
        "nonce": nonce,
        "chainId": int(w3.eth.chain_id),
    }

    latest_block = w3.eth.get_block("latest")
    base_fee = latest_block.get("baseFeePerGas")
    if base_fee is not None:
        priority_fee = w3.to_wei(1, "gwei")
        tx["maxPriorityFeePerGas"] = priority_fee
        tx["maxFeePerGas"] = int(base_fee * 2 + priority_fee)
    else:
        tx["gasPrice"] = int(w3.eth.gas_price)

    try:
        gas_estimate = contract_fn.estimate_gas({"from": checksum_wallet})
        tx["gas"] = int(gas_estimate * 1.2)
    except Exception:
        tx["gas"] = 500000

    built_tx = contract_fn.build_transaction(tx)
    signed = w3.eth.account.sign_transaction(built_tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
    if receipt.status != 1:
        raise ValueError(f"{function_name} transaction failed on-chain")
    tx_hash_hex = tx_hash.hex()
    return tx_hash_hex if tx_hash_hex.startswith("0x") else f"0x{tx_hash_hex}"


def _wallet_first_register_evm(
    name: str,
    description: str,
    endpoint: Optional[str],
    network: str,
    owner_address: str,
    image: Optional[str] = None,
    version: Optional[str] = None,
    tags: Optional[List[str]] = None,
    endpoint_ids: Optional[List[str]] = None,
    custom_endpoints: Optional[List[str]] = None,
) -> Dict[str, Any]:
    session_token = create_wallet_session("base", owner_address, "erc8004_register")
    headers = {"Authorization": f"Bearer {session_token}"}
    prepare_body = _build_registration_body(
        name=name,
        description=description,
        endpoint=endpoint,
        network=network,
        owner_address=owner_address,
        image=image,
        version=version,
        tags=tags,
        endpoint_ids=endpoint_ids,
        custom_endpoints=custom_endpoints,
    )

    prepare = post_json(f"{API_BASE}/agent/erc8004/prepare", prepare_body, headers=headers)
    register_tx_hash = _send_evm_contract_tx(
        network=network,
        contract_address=str(prepare["contractAddress"]),
        abi=prepare["abi"],
        function_name=str(prepare["functionName"]),
        args=list(prepare.get("args") or []),
    )

    finalize_register = post_json(
        f"{API_BASE}/agent/erc8004/finalize",
        {
            **prepare_body,
            "stage": "register",
            "registerTxHash": register_tx_hash,
        },
        headers=headers,
    )

    onchain_action = finalize_register.get("onChainAction") or {}
    set_uri_tx_hash = _send_evm_contract_tx(
        network=network,
        contract_address=str(onchain_action["contractAddress"]),
        abi=onchain_action["abi"],
        function_name=str(onchain_action["functionName"]),
        args=list(onchain_action.get("args") or []),
    )

    finalize_set_uri = post_json(
        f"{API_BASE}/agent/erc8004/finalize",
        {
            "network": network,
            "agentId": finalize_register["agentId"],
            "stage": "set-uri",
            "setUriTxHash": set_uri_tx_hash,
        },
        headers=headers,
    )

    return {
        "success": True,
        "mode": "wallet-first",
        "chainType": "evm",
        "network": network,
        "agentId": finalize_register.get("agentId"),
        "tokenUri": finalize_set_uri.get("tokenUri") or finalize_register.get("tokenUri"),
        "ownerAddress": owner_address,
        "transactions": {
            "register": register_tx_hash,
            "setUri": set_uri_tx_hash,
        },
        "finalize": finalize_set_uri,
    }


def _wallet_first_register_solana(
    name: str,
    description: str,
    endpoint: Optional[str],
    network: str,
    owner_address: str,
    image: Optional[str] = None,
    version: Optional[str] = None,
    tags: Optional[List[str]] = None,
    endpoint_ids: Optional[List[str]] = None,
    custom_endpoints: Optional[List[str]] = None,
) -> Dict[str, Any]:
    session_token = create_wallet_session("solana", owner_address, "erc8004_register")
    headers = {"Authorization": f"Bearer {session_token}"}

    asset = generate_solana_asset_keypair()
    prepare_body = _build_registration_body(
        name=name,
        description=description,
        endpoint=endpoint,
        network=network,
        owner_address=owner_address,
        image=image,
        version=version,
        tags=tags,
        endpoint_ids=endpoint_ids,
        custom_endpoints=custom_endpoints,
        asset_address=asset["address"],
    )

    prepare = post_json(f"{API_BASE}/agent/erc8004/prepare", prepare_body, headers=headers)
    prepared_tx = (((prepare.get("tx") or {}).get("prepared") or {}).get("transaction"))
    rpc_url = ((prepare.get("tx") or {}).get("rpcUrl")) or (
        "https://api.devnet.solana.com" if network == "solanaDevnet" else "https://api.mainnet-beta.solana.com"
    )
    if not prepared_tx:
        raise ValueError("Prepare response is missing the Solana transaction payload")

    signature = send_prepared_solana_transaction(
        prepared_transaction_base64=str(prepared_tx),
        rpc_url=str(rpc_url),
        extra_signers=[asset["keypair"]],
    )
    wait_for_solana_confirmation(signature, str(rpc_url))

    finalize = post_json(
        f"{API_BASE}/agent/erc8004/finalize",
        {
            **prepare_body,
            "metadataUri": prepare["metadataUri"],
            "registerTxSignature": signature,
        },
        headers=headers,
    )

    return {
        "success": True,
        "mode": "wallet-first",
        "chainType": "solana",
        "network": network,
        "assetAddress": prepare.get("assetAddress") or asset["address"],
        "tokenUri": finalize.get("tokenUri") or prepare.get("metadataUri"),
        "ownerAddress": owner_address,
        "transactions": {
            "register": signature,
        },
        "finalize": finalize,
    }
def register_agent(
    name: str,
    description: str,
    endpoint: Optional[str],
    network: str,
    owner_address: Optional[str] = None,
    image: Optional[str] = None,
    version: Optional[str] = None,
    tags: Optional[List[str]] = None,
    endpoint_ids: Optional[List[str]] = None,
    custom_endpoints: Optional[List[str]] = None,
) -> Dict[str, Any]:
    owner = _resolve_owner_address(network, owner_address)
    normalized_custom_endpoints = _normalize_string_list(custom_endpoints)
    normalized_endpoint_ids = _normalize_string_list(endpoint_ids)
    normalized_tags = _normalize_string_list(tags)
    normalized_endpoint = endpoint.strip() if endpoint else ""

    if not normalized_endpoint and not normalized_endpoint_ids and not normalized_custom_endpoints:
        raise ValueError("Provide a primary endpoint, one or more --endpoint-id values, or one or more --custom-endpoint URLs")

    if is_awal_mode():
        raise ValueError("Wallet-first registration requires direct wallet signing keys. Disable AWAL mode and set PRIVATE_KEY/WALLET_ADDRESS or SOLANA_SECRET_KEY.")
    if is_ows_mode():
        raise ValueError(
            "OWS now supports wallet lookup and challenge-signing flows in x402-layer, but deep ERC-8004 registration transactions still require direct signing keys. "
            "Set PRIVATE_KEY/WALLET_ADDRESS for EVM registration or SOLANA_SECRET_KEY for Solana registration."
        )

    _assert_local_signer_matches_owner(network, owner)

    if is_solana_network(network):
        return _wallet_first_register_solana(
            name,
            description,
            normalized_endpoint or None,
            network,
            owner,
            image,
            version,
            normalized_tags,
            normalized_endpoint_ids,
            normalized_custom_endpoints,
        )
    return _wallet_first_register_evm(
        name,
        description,
        normalized_endpoint or None,
        network,
        owner,
        image,
        version,
        normalized_tags,
        normalized_endpoint_ids,
        normalized_custom_endpoints,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Register an ERC-8004/Solana-8004 agent",
    )
    parser.add_argument("name", help="Agent display name")
    parser.add_argument("description", help="Agent description")
    parser.add_argument("endpoint", nargs="?", help="Primary service endpoint URL or fallback URL")
    parser.add_argument(
        "--network",
        default="baseSepolia",
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
        help="Target registration network",
    )
    parser.add_argument("--owner-address", help="Owner wallet address (auto-resolved if omitted)")
    parser.add_argument("--image", help="Optional image URL")
    parser.add_argument("--version", help="Optional agent version string")
    parser.add_argument("--tag", action="append", default=[], help="Repeatable agent tag")
    parser.add_argument("--endpoint-id", action="append", default=[], help="Repeatable platform endpoint UUID to bind")
    parser.add_argument("--custom-endpoint", action="append", default=[], help="Repeatable custom endpoint URL to bind")
    args = parser.parse_args()

    result = register_agent(
        name=args.name,
        description=args.description,
        endpoint=args.endpoint,
        network=args.network,
        owner_address=args.owner_address,
        image=args.image,
        version=args.version,
        tags=args.tag,
        endpoint_ids=args.endpoint_id,
        custom_endpoints=args.custom_endpoint,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        sys.exit(1)
