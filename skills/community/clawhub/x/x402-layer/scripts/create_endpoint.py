
#!/usr/bin/env python3
"""
x402 Agentic Endpoint Creation

Create a new monetized API endpoint on the x402 network.
Cost: $1 USDC (includes 4,000 credits)

IMPORTANT: Credits are production credits.
- Each API request to your endpoint consumes 1 credit
- When credits reach 0, your endpoint stops serving traffic
- You must top up credits to keep endpoint active

Usage:
    python create_endpoint.py <slug> <name> <origin_url> <price> [options]

Example:
    python create_endpoint.py my-api "My API Service" https://api.example.com 0.01

With Marketplace Listing:
    python create_endpoint.py my-api "My API" https://api.example.com 0.01 \
        --category ai --description "AI-powered analysis" \
        --logo https://example.com/logo.png --banner https://example.com/banner.jpg

With API Schema (auto-documented routes):
    python create_endpoint.py my-api "My API" https://api.example.com 0.01 \
        --schema-file schema.json

Auth Modes:
- Base: private-key (PRIVATE_KEY) or awal (X402_USE_AWAL=1)
- Solana: SOLANA_SECRET_KEY (private-key mode only)
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional

import requests

from awal_bridge import awal_pay_url
from network_selection import pick_payment_option
from solana_signing import create_solana_xpayment_from_accept, load_solana_wallet_address
from wallet_signing import is_awal_mode, load_wallet_address

API_BASE = "https://api.x402layer.cc"


def _resolve_secondary_wallet(cli_value: Optional[str]) -> Optional[str]:
    if cli_value:
        return cli_value
    return os.getenv("WALLET_ADDRESS_SECONDARY") or os.getenv("SOLANA_WALLET_ADDRESS") or load_solana_wallet_address()


def create_endpoint(
    slug: str,
    name: str,
    origin_url: str,
    price: float,
    chain: str = "base",
    category: Optional[str] = None,
    description: Optional[str] = None,
    logo_url: Optional[str] = None,
    banner_url: Optional[str] = None,
    list_on_marketplace: bool = True,
    wallet_secondary: Optional[str] = None,
    webhook_url: Optional[str] = None,
    audience_mode: str = "all",
    agentkit_benefit_mode: str = "off",
    agentkit_discount_percent: Optional[float] = None,
    agentkit_free_trial_uses: Optional[int] = None,
    api_schema: Optional[Dict[str, Any]] = None,
) -> dict:
    """Create a new agentic endpoint."""
    if chain == "solana":
        sol_wallet = load_solana_wallet_address()
        if not sol_wallet:
            return {
                "error": (
                    "Solana endpoint creation requires a Solana signer: "
                    "SOLANA_SECRET_KEY (private-key mode) or "
                    "CDP_SOLANA_ACCOUNT_ADDRESS with CDP credentials (coinbase-wallet mode)."
                )
            }
        wallet_address = sol_wallet
        header_wallet = sol_wallet
    else:
        header_wallet = load_wallet_address(required=True)
        wallet_address = header_wallet

    data: dict = {
        "name": name,
        "slug": slug,
        "origin_url": origin_url,
        "chain": chain,
        "wallet_address": wallet_address,
        "price": price,
        "currency": "USDC",
        "list_on_marketplace": list_on_marketplace,
        "audience_mode": audience_mode,
        "agentkit_benefit_mode": agentkit_benefit_mode,
    }

    if chain == "both":
        secondary = _resolve_secondary_wallet(wallet_secondary)
        if not secondary:
            return {
                "error": (
                    "chain='both' requires a Solana secondary wallet. "
                    "Set --wallet-secondary or WALLET_ADDRESS_SECONDARY/SOLANA_WALLET_ADDRESS"
                )
            }
        data["wallet_address_secondary"] = secondary

    if category:
        data["category"] = category
    if description:
        data["description"] = description
    if logo_url:
        data["image_url"] = logo_url
    if banner_url:
        data["banner_url"] = banner_url
    if webhook_url:
        data["webhook_url"] = webhook_url
    if agentkit_benefit_mode == "discount":
        data["agentkit_discount_percent"] = agentkit_discount_percent
    if agentkit_benefit_mode == "free_trial":
        data["agentkit_free_trial_uses"] = agentkit_free_trial_uses
    if api_schema:
        data["apiSchema"] = api_schema

    url = f"{API_BASE}/agent/endpoints"

    print(f"Creating endpoint: {slug}")
    print(f"Origin: {origin_url}")
    print(f"Price: ${price} per call")
    print(f"Chain: {chain}")
    print(f"List on Marketplace: {list_on_marketplace}")
    print(f"Best Fit Audience: {audience_mode}")
    if agentkit_benefit_mode != "off":
        print(f"AgentKit Benefit: {agentkit_benefit_mode}")
    if api_schema:
        route_count = len(api_schema.get("routes", []))
        print(f"API Schema: {route_count} route(s) defined")
    print("Cost: $1 USDC (includes 4,000 credits)")

    challenge_resp = requests.post(
        url,
        json=data,
        headers={"x-wallet-address": header_wallet},
        timeout=30,
    )

    if challenge_resp.status_code != 402:
        return {
            "error": f"Unexpected status: {challenge_resp.status_code}",
            "response": challenge_resp.text,
        }

    challenge = challenge_resp.json()

    # AWAL mode: Use Coinbase Agentic Wallet for Base payments
    if is_awal_mode():
        print("Payment mode: AWAL (Base)")
        result = awal_pay_url(
            url,
            method="POST",
            data=data,
            headers={"x-wallet-address": header_wallet},
        )
        if isinstance(result, dict):
            if result.get("error"):
                return result
            # Check for successful endpoint creation
            if "endpoint" in result or result.get("success"):
                print("\nEndpoint created")
                print(f"URL: https://api.x402layer.cc/e/{slug}")
                if "endpoint" in result and "api_key" in result["endpoint"]:
                    print("API Key returned. You must validate x-api-key at your origin.")
        return result

    # Private-key mode: Use local signing for Base or Solana
    try:
        selected_network, selected_option, signer = pick_payment_option(challenge, context="endpoint creation")
    except ValueError as exc:
        return {"error": str(exc)}

    if selected_network == "base":
        if signer is None:
            return {"error": "Internal error: missing Base signer"}
        x_payment = signer.create_x402_payment_header(
            pay_to=selected_option["payTo"],
            amount=int(selected_option["maxAmountRequired"]),
        )
        payer_wallet = signer.wallet
    else:
        x_payment = create_solana_xpayment_from_accept(selected_option)
        payer_wallet = load_solana_wallet_address() or header_wallet

    response = requests.post(
        url,
        json=data,
        headers={
            "X-Payment": x_payment,
            "x-wallet-address": payer_wallet,
        },
        timeout=45,
    )

    print(f"Payment network used: {selected_network}")
    print(f"Response: {response.status_code}")

    if response.status_code in (200, 201):
        result = response.json()
        print("\nEndpoint created")
        print(f"URL: https://api.x402layer.cc/e/{slug}")
        if "endpoint" in result and "api_key" in result["endpoint"]:
            print("API Key returned. You must validate x-api-key at your origin.")
        if "webhook" in result:
            print(f"\n⚠️  SAVE WEBHOOK SECRET — it will not be shown again:")
            print(f"   {result['webhook'].get('signing_secret', 'N/A')}")
        return result

    return {"error": response.text}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a new x402 monetized endpoint",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_endpoint.py my-api "My API" https://api.example.com 0.01 --no-list

  python create_endpoint.py my-api "My AI Service" https://api.example.com 0.01 \\
      --category ai --description "AI-powered data analysis" \\
      --logo https://example.com/logo.png --banner https://example.com/banner.jpg

  python create_endpoint.py my-api "Multi-chain API" https://api.example.com 0.02 \\
      --chain both --wallet-secondary <SOLANA_ADDRESS>
""",
    )

    parser.add_argument("slug", help="URL-friendly identifier (e.g., 'my-api')")
    parser.add_argument("name", help="Human-readable name")
    parser.add_argument("origin_url", help="Your backend API URL")
    parser.add_argument("price", type=float, help="Price per call in USD")
    parser.add_argument("--chain", choices=["base", "solana", "both"], default="base", help="Payment chain")
    parser.add_argument("--wallet-secondary", help="Required when --chain both (Solana wallet)")
    parser.add_argument("--category", choices=["ai", "data", "finance", "utility", "social", "gaming"], help="Marketplace category")
    parser.add_argument("--description", help="Public description for marketplace")
    parser.add_argument("--logo", help="Logo image URL for marketplace listing")
    parser.add_argument("--banner", help="Banner image URL for marketplace listing")
    parser.add_argument("--no-list", action="store_true", help="Create endpoint without listing")
    parser.add_argument("--webhook-url", help="HTTPS URL to receive payment.succeeded webhook events (optional)")
    parser.add_argument("--best-fit", choices=["everyone", "humans", "agents"], default="everyone", help="Best fit audience shown in marketplace")
    parser.add_argument("--agentkit-benefit", choices=["off", "free", "free_trial", "discount"], default="off", help="Benefit for verified human-backed agent wallets (direct endpoints only)")
    parser.add_argument("--agentkit-discount-percent", type=float, help="Discount percent when --agentkit-benefit discount")
    parser.add_argument("--agentkit-free-trial-uses", type=int, help="Free requests when --agentkit-benefit free_trial")
    parser.add_argument("--schema-file", help="Path to JSON file containing API schema (routes, params, body)")
    parser.add_argument("--schema-json", help="Inline JSON string for API schema")

    args = parser.parse_args()

    audience_mode = {
        "everyone": "all",
        "humans": "human_only",
        "agents": "agent_only",
    }[args.best_fit]

    if args.agentkit_benefit != "off" and args.chain == "solana":
        print(json.dumps({"error": "AgentKit benefits currently apply only to Base/direct endpoint flows"}, indent=2))
        sys.exit(1)

    if args.agentkit_benefit != "off" and args.price is None:
        print(json.dumps({"error": "AgentKit benefits require a direct endpoint price"}, indent=2))
        sys.exit(1)

    if args.agentkit_benefit == "discount":
        if args.agentkit_discount_percent is None or args.agentkit_discount_percent <= 0 or args.agentkit_discount_percent >= 100:
            print(json.dumps({"error": "Set --agentkit-discount-percent to a value greater than 0 and less than 100"}, indent=2))
            sys.exit(1)

    if args.agentkit_benefit == "free_trial":
        if args.agentkit_free_trial_uses is None or args.agentkit_free_trial_uses < 1:
            print(json.dumps({"error": "Set --agentkit-free-trial-uses to an integer of at least 1"}, indent=2))
            sys.exit(1)

    api_schema = None
    if args.schema_file:
        with open(args.schema_file, "r") as f:
            api_schema = json.load(f)
    elif args.schema_json:
        api_schema = json.loads(args.schema_json)

    list_on_marketplace = not args.no_list and bool(args.category or args.description or args.logo or args.banner)

    result = create_endpoint(
        slug=args.slug,
        name=args.name,
        origin_url=args.origin_url,
        price=args.price,
        chain=args.chain,
        category=args.category,
        description=args.description,
        logo_url=args.logo,
        banner_url=args.banner,
        list_on_marketplace=list_on_marketplace,
        wallet_secondary=args.wallet_secondary,
        webhook_url=args.webhook_url,
        audience_mode=audience_mode,
        agentkit_benefit_mode=args.agentkit_benefit,
        agentkit_discount_percent=args.agentkit_discount_percent,
        agentkit_free_trial_uses=args.agentkit_free_trial_uses,
        api_schema=api_schema,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        sys.exit(1)
