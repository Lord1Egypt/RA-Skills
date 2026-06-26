#!/usr/bin/env python3
"""
x402 Marketplace Discovery

Browse and search the x402 marketplace for available listings.

Usage:
    python discover_marketplace.py                      # List all
    python discover_marketplace.py search <query>       # Search listings
    python discover_marketplace.py category <type>      # Filter by category
    python discover_marketplace.py featured             # Show featured
    python discover_marketplace.py details <slug>       # Find a listing by slug

Categories: ai, data, finance, utility, social, gaming
"""

import json
import sys
from typing import Any, Dict, Optional

import requests

API_BASE = "https://api.x402layer.cc"
STUDIO_BASE = "https://studio.x402layer.cc"


def _query_marketplace(**params) -> Dict[str, Any]:
    try:
        response = requests.get(f"{API_BASE}/api/marketplace", params=params, timeout=30)
    except requests.RequestException as exc:
        return {"error": str(exc)}

    if response.status_code == 200:
        return response.json()
    return {"error": response.text, "status": response.status_code}


def _fetch_public_endpoint_details(slug: str) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"{STUDIO_BASE}/api/public/endpoints/{slug}", timeout=30)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None
    try:
        return response.json()
    except Exception:
        return None


def _agentkit_summary(endpoint: Optional[Dict[str, Any]]) -> Optional[str]:
    if not endpoint:
        return None

    mode = endpoint.get("agentkit_benefit_mode")
    if mode == "free":
        return "free for verified human-backed agent wallets"
    if mode == "free_trial":
        uses = endpoint.get("agentkit_free_trial_uses") or 1
        return f"{uses} free request{'s' if uses != 1 else ''} for verified human-backed agent wallets"
    if mode == "discount":
        percent = endpoint.get("agentkit_discount_percent") or 0
        return f"{percent}% off for verified human-backed agent wallets"
    return None


def list_all_endpoints() -> Dict[str, Any]:
    return _query_marketplace(limit=50)


def search_endpoints(query: str) -> Dict[str, Any]:
    return _query_marketplace(search=query, limit=50)


def get_by_category(category: str) -> Dict[str, Any]:
    return _query_marketplace(category=category, limit=50)


def get_featured() -> Dict[str, Any]:
    return _query_marketplace(featured="true", limit=50)


def get_endpoint_details(slug: str) -> Dict[str, Any]:
    data = _query_marketplace(search=slug, limit=50)
    if "listings" not in data:
        return data

    listings = data.get("listings", [])
    exact = [item for item in listings if item.get("slug") == slug]
    if exact:
        listing = exact[0]
        if listing.get("type") == "endpoint":
            endpoint = _fetch_public_endpoint_details(slug)
            benefit = _agentkit_summary(endpoint)
            if endpoint:
                listing = {
                    **listing,
                    "pricing_mode": endpoint.get("mode"),
                    "payment_chain": endpoint.get("chain"),
                }
            if benefit:
                listing["agentkit_benefit"] = benefit
        return {"listing": listing}

    if listings:
        return {"note": "No exact slug match; returning closest matches", "listings": listings[:5]}

    return {"error": f"No listing found for slug '{slug}'"}


def _print_listing(item: Dict[str, Any]) -> None:
    slug = item.get("slug", "?")
    price = item.get("price", 0)
    name = item.get("name", "Unnamed")
    item_type = item.get("type", "unknown")
    line = f"  - {slug} | ${price} | {name} [{item_type}]"

    if item_type == "endpoint":
        benefit = _agentkit_summary(_fetch_public_endpoint_details(slug))
        if benefit:
            line += f" | AgentKit: {benefit}"

    print(line)


def main() -> None:
    if len(sys.argv) < 2:
        result = list_all_endpoints()
    elif sys.argv[1] == "search" and len(sys.argv) >= 3:
        result = search_endpoints(sys.argv[2])
    elif sys.argv[1] == "category" and len(sys.argv) >= 3:
        result = get_by_category(sys.argv[2])
    elif sys.argv[1] == "featured":
        result = get_featured()
    elif sys.argv[1] == "details" and len(sys.argv) >= 3:
        result = get_endpoint_details(sys.argv[2])
    else:
        print("Usage:")
        print("  python discover_marketplace.py                      # List all")
        print("  python discover_marketplace.py search <query>       # Search")
        print("  python discover_marketplace.py category <type>      # By category")
        print("  python discover_marketplace.py featured             # Featured")
        print("  python discover_marketplace.py details <slug>       # Listing info")
        return

    if "listings" in result:
        listings = result["listings"]
        print(f"Found {len(listings)} listings:")
        for item in listings[:10]:
            _print_listing(item)
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
