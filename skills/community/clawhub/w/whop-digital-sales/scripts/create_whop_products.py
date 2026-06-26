#!/usr/bin/env python3
"""
Whop Digital Sales — create products and checkout links.
API docs: https://docs.whop.com/api-reference/
"""

import os, json, requests

WHOP_API_KEY = os.environ.get("WHOP_API_KEY", "")
BASE_URL = "https://api.whop.com/api/v1"
HEADERS = {"Authorization": f"Bearer {WHOP_API_KEY}", "Content-Type": "application/json"}

PRODUCTS = [
    {
        "name": "AI Trading Tools — Free Entry",
        "description": "Get free access to our whale scanner, options signal generator, and daily market reports. No credit card needed.",
        "price": 0,
        "price_type": "free",
    },
    {
        "name": "AI Trading Tools — Pro",
        "description": "Full access to options trading brain, Elliott Wave analyzer, liquidity map, and all paid strategies. $19/month.",
        "price": 1900,
        "price_type": "recurring",
        "billing_cycle": "month",
    },
    {
        "name": "AI Trading Tools — Lifetime",
        "description": "One-time payment, lifetime access to all current and future AI trading tools, skills, and strategies. All features included.",
        "price": 19900,
        "price_type": "one_time",
    },
]

def create_product(p):
    """Create a product on Whop."""
    if not WHOP_API_KEY:
        print("❌ No WHOP_API_KEY set. Add it in Settings > Advanced.")
        return None
    
    payload = {
        "name": p["name"],
        "description": p["description"],
        "visibility": "public",
    }
    
    resp = requests.post(f"{BASE_URL}/products", headers=HEADERS, json=payload, timeout=15)
    if resp.status_code not in (200, 201):
        print(f"  ❌ {p['name']}: {resp.text[:200]}")
        return None
    
    product = resp.json().get("data", {}) or resp.json()
    pid = product.get("id", product.get("product_id", ""))
    print(f"  ✅ Created: {p['name']} (ID: {pid})")
    
    # Create plan
    if p["price_type"] != "free":
        plan_payload = {
            "product_id": pid,
            "plan_type": "renewal" if p["price_type"] == "recurring" else "one_time",
            "base_currency": "usd",
            "price": p["price"],
            "visibility": "public",
        }
        plan_resp = requests.post(f"{BASE_URL}/v2/plans", headers=HEADERS, json=plan_payload, timeout=15)
        if plan_resp.status_code in (200, 201):
            plan = plan_resp.json().get("data", {}) or plan_resp.json()
            plan_id = plan.get("id", "")
            print(f"     📋 Plan created: ${p['price']/100:.0f} (ID: {plan_id})")
            
            # Generate checkout link
            checkout_payload = {
                "plan_id": plan_id,
                "allow_multiple_quantity": False,
            }
            checkout_resp = requests.post(f"{BASE_URL}/checkouts", headers=HEADERS, json=checkout_payload, timeout=15)
            if checkout_resp.status_code in (200, 201):
                checkout = checkout_resp.json().get("data", {}) or checkout_resp.json()
                checkout_url = checkout.get("url", checkout.get("checkout_url", ""))
                print(f"     🔗 Checkout: {checkout_url}")
    else:
        # Free product - create membership checkout
        checkout_payload = {
            "product_id": pid,
            "allow_multiple_quantity": False,
        }
        checkout_resp = requests.post(f"{BASE_URL}/checkouts", headers=HEADERS, json=checkout_payload, timeout=15)
        if checkout_resp.status_code in (200, 201):
            checkout = checkout_resp.json().get("data", {}) or checkout_resp.json()
            print(f"     🔗 Free access: {checkout.get('url', 'N/A')}")
    
    return pid

def main():
    print("🚀 Whop Digital Sales — Creating Products\n")
    created = 0
    for p in PRODUCTS:
        pid = create_product(p)
        if pid:
            created += 1
    print(f"\n✅ Created {created}/{len(PRODUCTS)} products")

if __name__ == "__main__":
    main()