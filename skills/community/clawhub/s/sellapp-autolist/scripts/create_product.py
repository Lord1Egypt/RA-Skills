#!/usr/bin/env python3
"""
SellApp Auto-List v1.0 — creates digital products auto on SellApp.

API base: https://sell.app/api/v2
Docs: https://sell.app/docs/api
"""
import os, json, time, requests

SELLAPP_KEY = os.environ.get("SELLAPP_API_KEY", "")
BASE_URL = "https://sell.app/api/v2"
HEADERS = {"Authorization": f"Bearer {SELLAPP_KEY}", "Content-Type": "application/json"}

DIGITAL_PRODUCTS = [
    {
        "name": "Options Trading Brain — Notion Template",
        "description": "The ultimate options trading dashboard. Track whale flow signals, Elliott Wave counts, max pain zones, and position Greeks in one place. Built by a quant-trained trader.",
        "price": 27,
        "file_url": "https://example.com/options-brain-template.zip",
        "description_short": "Professional options trading dashboard for Notion",
    },
    {
        "name": "Whale Alert Scanner — Trading Journal",
        "description": "Auto-log unusual options activity, track whale trades, and analyze institutional flow. CSV import + live scanning. The edge serious traders use.",
        "price": 37,
        "file_url": "https://example.com/whale-journal.zip",
        "description_short": "Track whale trades and institutional flow automatically",
    },
    {
        "name": "Elliott Wave Cheat Sheet — PDF",
        "description": "The complete Elliott Wave rules, patterns, and Fibonacci ratios on one page. Wave identification, invalidation levels, and trade entry templates included.",
        "price": 17,
        "file_url": "https://example.com/elliott-wave-sheet.pdf",
        "description_short": "Complete Elliott Wave rules and patterns reference",
    },
    {
        "name": "Iron Condor Starter Pack — Calculator",
        "description": "Pre-built Iron Condor calculator for SPY, QQQ, and major tickers. Adjust wing widths, set probability targets, see max profit/loss instantly.",
        "price": 22,
        "file_url": "https://example.com/iron-condor-calc.zip",
        "description_short": "Iron Condor calculator with probability targeting",
    },
    {
        "name": "DeFi Sniper Bot — Setup Guide",
        "description": "Complete walkthrough for building a pump.fun sniper bot. Includes bot code, RPC setup, slippage configuration, and exit strategies. Used by 200+ traders.",
        "price": 47,
        "file_url": "https://example.com/defi-sniper-guide.zip",
        "description_short": "Build a pump.fun sniper bot in 30 minutes",
    },
    {
        "name": "Freelance Code — Win Crypto Gigs",
        "description": "The exact proposal templates, profile optimization steps, and skill listing strategy used to land 6-figure crypto freelance contracts. Works on FreeLanceDAO, CryptoGig, and more.",
        "price": 32,
        "file_url": "https://example.com/freelance-code.zip",
        "description_short": "Land high-paying crypto freelance gigs on autopilot",
    },
]


def create_product(product: dict) -> dict:
    """Create a product on SellApp."""
    payload = {
        "title": product["name"],
        "description": product["description"],
        "price": product["price"],
        "visibility": "public",
    }
    r = requests.post(f"{BASE_URL}/products", headers=HEADERS, json=payload)
    return r.json()


def list_products() -> dict:
    r = requests.get(f"{BASE_URL}/products", headers=HEADERS)
    return r.json()


def main():
    if not SELLAPP_KEY:
        print("❌ SELLAPP_API_KEY not set")
        return

    # Check existing products
    existing = list_products()
    existing_names = {p["title"] for p in existing.get("data", [])}
    print(f"📦 {len(existing.get('data', []))} products already on SellApp")

    created = 0
    for product in DIGITAL_PRODUCTS:
        if product["name"] in existing_names:
            print(f"  ⏭ Already exists: {product['name']}")
            continue

        print(f"  ➕ Creating: {product['name']} — ${product['price']}")
        result = create_product(product)
        if result.get("data", {}).get("id"):
            pid = result["data"]["id"]
            print(f"    ✅ Created (ID: {pid})")
            created += 1
        elif "id" in result:
            print(f"    ✅ Created (ID: {result['id']})")
            created += 1
        else:
            err = result.get("message") or str(result.get("errors", result))[:100]
            print(f"    ❌ Error: {err}")
        time.sleep(1)

    print(f"\n✅ Done. Created {created} new products.")


if __name__ == "__main__":
    main()
