#!/usr/bin/env python3
"""MRR & Subscription Metrics — pull active subscription data from Stripe.

Usage:
    python3 mrr.py
    python3 mrr.py --breakdown
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

CONFIG_PATH = os.path.expanduser("~/.config/revenue-dashboard/config.json")
STRIPE_KEY_PATH = os.path.expanduser("~/.config/stripe/api_key")


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {"accounts": {}, "currency": "usd"}


def load_stripe_key():
    if not os.path.exists(STRIPE_KEY_PATH):
        print(json.dumps({"error": f"Stripe key not found at {STRIPE_KEY_PATH}"}))
        sys.exit(1)
    return open(STRIPE_KEY_PATH).read().strip()


def stripe_api(endpoint, stripe_key, acct_id=None):
    headers = ["-u", f"{stripe_key}:", "-H", "Stripe-Version: 2025-01-27.acacia"]
    if acct_id:
        headers.extend(["-H", f"Stripe-Account: {acct_id}"])

    all_data = []
    url = f"https://api.stripe.com/v1/{endpoint}"

    while url:
        result = subprocess.run(
            ["curl", "-s", "-g", url] + headers,
            capture_output=True, text=True
        )
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            break

        if "error" in data:
            return {"error": data["error"].get("message", "Unknown error")}

        items = data.get("data", [])
        all_data.extend(items)

        if data.get("has_more") and items:
            separator = "&" if "?" in endpoint else "?"
            url = f"https://api.stripe.com/v1/{endpoint}{separator}starting_after={items[-1]['id']}"
        else:
            url = None

    return all_data


def fetch_subscriptions(stripe_key, acct_id):
    """Fetch all active subscriptions."""
    data = stripe_api("subscriptions?limit=100&status=active", stripe_key, acct_id)
    if isinstance(data, dict) and "error" in data:
        return [], data["error"]
    return data, None


def normalize_to_monthly(amount, interval, interval_count):
    """Convert any subscription interval to monthly amount."""
    if interval == "month":
        return amount / interval_count
    elif interval == "year":
        return amount / (12 * interval_count)
    elif interval == "week":
        return amount * (52 / 12) / interval_count
    elif interval == "day":
        return amount * (365 / 12) / interval_count
    return amount


def main():
    config = load_config()
    stripe_key = load_stripe_key()
    breakdown = "--breakdown" in sys.argv

    accounts = config.get("accounts", {})
    if not accounts:
        print(json.dumps({"error": "No Stripe accounts configured. Edit ~/.config/revenue-dashboard/config.json"}))
        sys.exit(1)

    results = {"accounts": {}, "total": {}}
    total_mrr = 0
    total_subs = 0
    all_plans = {}

    for name, acct_id in accounts.items():
        subs, err = fetch_subscriptions(stripe_key, acct_id)
        if err:
            results["accounts"][name] = {"error": err}
            continue

        account_mrr = 0
        account_plans = {}

        for sub in subs:
            for item in sub.get("items", {}).get("data", []):
                price = item.get("price", {})
                amount = price.get("unit_amount", 0)
                interval = price.get("recurring", {}).get("interval", "month")
                interval_count = price.get("recurring", {}).get("interval_count", 1)
                quantity = item.get("quantity", 1)

                monthly = normalize_to_monthly(amount * quantity, interval, interval_count)
                account_mrr += monthly

                if breakdown:
                    plan_name = price.get("nickname") or price.get("product", "unknown")
                    price_str = f"${amount/100:.2f}/{interval}"
                    key = f"{plan_name} ({price_str})"
                    if key not in account_plans:
                        account_plans[key] = {"count": 0, "mrr": 0}
                    account_plans[key]["count"] += quantity
                    account_plans[key]["mrr"] += monthly / 100

        entry = {
            "mrr": round(account_mrr / 100, 2),
            "arr": round(account_mrr * 12 / 100, 2),
            "active_subscriptions": len(subs),
        }

        if breakdown and account_plans:
            entry["plans"] = {k: {"subscribers": v["count"], "mrr": round(v["mrr"], 2)} for k, v in sorted(account_plans.items(), key=lambda x: -x[1]["mrr"])}

        results["accounts"][name] = entry
        total_mrr += account_mrr
        total_subs += len(subs)

        for k, v in account_plans.items():
            if k not in all_plans:
                all_plans[k] = {"count": 0, "mrr": 0}
            all_plans[k]["count"] += v["count"]
            all_plans[k]["mrr"] += v["mrr"]

    results["total"] = {
        "mrr": round(total_mrr / 100, 2),
        "arr": round(total_mrr * 12 / 100, 2),
        "active_subscriptions": total_subs,
    }

    if breakdown and all_plans:
        results["total"]["plans"] = {k: {"subscribers": v["count"], "mrr": round(v["mrr"], 2)} for k, v in sorted(all_plans.items(), key=lambda x: -x[1]["mrr"])}

    results["timestamp"] = datetime.now(timezone.utc).isoformat()
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
