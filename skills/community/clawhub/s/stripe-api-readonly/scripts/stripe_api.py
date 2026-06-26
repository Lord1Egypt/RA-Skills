#!/usr/bin/env python3
import argparse
import json
import os
import urllib.parse
import urllib.request

BASE = "https://api.stripe.com/v1"


def get_key() -> str:
    key = os.environ.get("STRIPE_SECRET_KEY", "").strip()
    if not key:
        raise SystemExit("Missing STRIPE_SECRET_KEY environment variable.")
    return key


def request(method: str, path: str, params=None):
    key = get_key()
    url = BASE + path
    data = None
    headers = {
        "Authorization": f"Bearer {key}",
        "User-Agent": "openclaw-stripe-api-skill/1.0",
    }
    if params:
        encoded = urllib.parse.urlencode(params, doseq=True)
        if method.upper() == "GET":
            url += ("?" if "?" not in url else "&") + encoded
        else:
            data = encoded.encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"error": {"message": body, "type": "http_error", "status": e.code}}
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
        raise SystemExit(1)


def print_json(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def main():
    p = argparse.ArgumentParser(description="Minimal Stripe API helper for OpenClaw skill use")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("account", help="Retrieve account details")

    for name, help_text in [
        ("customers", "List customers"),
        ("products", "List products"),
        ("prices", "List prices"),
        ("charges", "List charges"),
        ("payment_intents", "List payment intents"),
        ("subscriptions", "List subscriptions"),
        ("invoices", "List invoices"),
        ("refunds", "List refunds"),
        ("disputes", "List disputes"),
        ("payouts", "List payouts"),
        ("balance_transactions", "List balance transactions"),
        ("webhook_endpoints", "List webhook endpoints"),
    ]:
        sp = sub.add_parser(name, help=help_text)
        sp.add_argument("--limit", type=int, default=10)

    search = sub.add_parser("search_customers", help="Search customers")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)

    get_obj = sub.add_parser("get", help="Retrieve an object by API path, e.g. /customers/cus_123")
    get_obj.add_argument("path")

    args = p.parse_args()

    if args.cmd == "account":
        print_json(request("GET", "/account"))
        return

    listing = {
        "customers": "/customers",
        "products": "/products",
        "prices": "/prices",
        "charges": "/charges",
        "payment_intents": "/payment_intents",
        "subscriptions": "/subscriptions",
        "invoices": "/invoices",
        "refunds": "/refunds",
        "disputes": "/disputes",
        "payouts": "/payouts",
        "balance_transactions": "/balance_transactions",
        "webhook_endpoints": "/webhook_endpoints",
    }
    if args.cmd in listing:
        print_json(request("GET", listing[args.cmd], {"limit": args.limit}))
        return

    if args.cmd == "search_customers":
        print_json(request("GET", "/customers/search", {"query": args.query, "limit": args.limit}))
        return

    if args.cmd == "get":
        path = args.path if args.path.startswith("/") else f"/{args.path}"
        print_json(request("GET", path))
        return


if __name__ == "__main__":
    main()
