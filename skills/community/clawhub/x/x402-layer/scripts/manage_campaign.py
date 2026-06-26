#!/usr/bin/env python3
"""
x402 Fundraiser Campaign Management

Manage fundraiser campaigns through the owner-scoped worker API.

Authentication:
- Preferred: X_API_KEY / API_KEY when you already have the dashboard-linked management key
- Optional: SINGULARITY_PAT for the PAT-backed control-plane path

Usage:
    python manage_campaign.py list
    python manage_campaign.py info <slug>
    python manage_campaign.py create --title "My Campaign" --wallet <SOLANA_WALLET> --target 1000
    python manage_campaign.py update <slug> --title "Updated Title"
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional

import requests

API_BASE = "https://api.x402layer.cc"


def _load_auth_headers() -> Dict[str, str]:
    pat = (os.getenv("SINGULARITY_PAT") or "").strip()
    if pat:
        return {"Authorization": f"Bearer {pat}", "Accept": "application/json"}

    api_key = (os.getenv("X_API_KEY") or os.getenv("API_KEY") or "").strip()
    if api_key:
        return {"X-API-Key": api_key, "Accept": "application/json"}

    raise ValueError("Set SINGULARITY_PAT or X_API_KEY/API_KEY")


def _request(method: str, params: Optional[Dict[str, str]] = None, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    headers = _load_auth_headers()
    if payload is not None:
        headers["Content-Type"] = "application/json"

    response = requests.request(
        method,
        f"{API_BASE}/agent/campaigns",
        params=params,
        json=payload,
        headers=headers,
        timeout=30,
    )

    try:
        data = response.json()
    except Exception:
        data = {"raw": response.text}

    if response.ok:
        return data

    return {
        "error": f"Status {response.status_code}",
        "response": data,
    }


def list_campaigns(slug: Optional[str] = None) -> Dict[str, Any]:
    params = {"slug": slug} if slug else None
    return _request("GET", params=params)


def create_campaign(
    title: str,
    wallet_address: str,
    target_amount: float,
    description: Optional[str] = None,
    token_ticker: Optional[str] = None,
    x_handle: Optional[str] = None,
    deadline: Optional[str] = None,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    fee_option: Optional[str] = None,
    fee_split_pct: Optional[float] = None,
    bags_config_type: Optional[str] = None,
    idempotency_key: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "title": title,
        "wallet_address": wallet_address,
        "target_amount": target_amount,
    }
    if description is not None:
        payload["description"] = description
    if token_ticker is not None:
        payload["token_ticker"] = token_ticker
    if x_handle is not None:
        payload["x_handle"] = x_handle
    if deadline is not None:
        payload["deadline"] = deadline
    if category is not None:
        payload["category"] = category
    if subcategory is not None:
        payload["subcategory"] = subcategory
    if fee_option is not None:
        payload["fee_option"] = fee_option
    if fee_split_pct is not None:
        payload["fee_split_pct"] = fee_split_pct
    if bags_config_type is not None:
        payload["bags_config_type"] = bags_config_type
    if idempotency_key is not None:
        payload["idempotency_key"] = idempotency_key

    return _request("POST", payload=payload)


def update_campaign(
    slug: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    x_handle: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    if title is not None:
        payload["title"] = title
    if description is not None:
        payload["description"] = description
    if x_handle is not None:
        payload["x_handle"] = x_handle

    if not payload:
        return {"error": "No updates specified"}

    return _request("PATCH", params={"slug": slug}, payload=payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage x402 fundraiser campaigns")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    list_parser = subparsers.add_parser("list", help="List owned campaigns")
    list_parser.add_argument("--slug", help="Optional campaign slug to fetch a single campaign")

    info_parser = subparsers.add_parser("info", help="Get owned campaign details")
    info_parser.add_argument("slug", help="Campaign slug")

    create_parser = subparsers.add_parser("create", help="Create a campaign")
    create_parser.add_argument("--title", required=True, help="Campaign title")
    create_parser.add_argument("--wallet", required=True, help="Creator payout Solana wallet")
    create_parser.add_argument("--target", required=True, type=float, help="Target amount in USDC")
    create_parser.add_argument("--description", help="Campaign description")
    create_parser.add_argument("--ticker", help="Token ticker")
    create_parser.add_argument("--x-handle", help="X handle without @")
    create_parser.add_argument("--deadline", help="ISO 8601 deadline")
    create_parser.add_argument("--category", help="Category")
    create_parser.add_argument("--subcategory", help="Subcategory")
    create_parser.add_argument("--fee-option", choices=["supporters", "creator", "split"], help="Fee share option")
    create_parser.add_argument("--fee-split-pct", type=float, help="Split percentage for creator")
    create_parser.add_argument("--bags-config-type", help="Bags fee tier UUID")
    create_parser.add_argument("--idempotency-key", help="Safe retry key")

    update_parser = subparsers.add_parser("update", help="Update campaign metadata")
    update_parser.add_argument("slug", help="Campaign slug")
    update_parser.add_argument("--title", help="Updated title")
    update_parser.add_argument("--description", help="Updated description")
    update_parser.add_argument("--x-handle", help="Updated X handle without @")

    args = parser.parse_args()

    if args.command == "list":
        result = list_campaigns(args.slug)
    elif args.command == "info":
        result = list_campaigns(args.slug)
    elif args.command == "create":
        result = create_campaign(
            title=args.title,
            wallet_address=args.wallet,
            target_amount=args.target,
            description=args.description,
            token_ticker=args.ticker,
            x_handle=args.x_handle,
            deadline=args.deadline,
            category=args.category,
            subcategory=args.subcategory,
            fee_option=args.fee_option,
            fee_split_pct=args.fee_split_pct,
            bags_config_type=args.bags_config_type,
            idempotency_key=args.idempotency_key,
        )
    elif args.command == "update":
        result = update_campaign(
            slug=args.slug,
            title=args.title,
            description=args.description,
            x_handle=args.x_handle,
        )
    else:
        parser.print_help()
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        sys.exit(1)
