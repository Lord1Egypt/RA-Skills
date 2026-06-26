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
        "User-Agent": "openclaw-stripe-api-actions-skill/1.0",
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


def parse_metadata(items):
    result = {}
    for item in items or []:
        if "=" not in item:
            raise SystemExit(f"Invalid metadata item: {item}. Expected key=value")
        key, value = item.split("=", 1)
        result[key] = value
    return result


def require_confirm(args):
    if not getattr(args, "confirm", False):
        raise SystemExit("Refusing write action without --confirm")


def main():
    p = argparse.ArgumentParser(description="Stripe write-capable helper for OpenClaw skill use")
    sub = p.add_subparsers(dest="cmd", required=True)

    cust = sub.add_parser("create_customer", help="Create customer")
    cust.add_argument("--name")
    cust.add_argument("--email")
    cust.add_argument("--phone")
    cust.add_argument("--description")
    cust.add_argument("--metadata", action="append", default=[])
    cust.add_argument("--confirm", action="store_true")

    upd_cust = sub.add_parser("update_customer", help="Update customer")
    upd_cust.add_argument("customer_id")
    upd_cust.add_argument("--name")
    upd_cust.add_argument("--email")
    upd_cust.add_argument("--phone")
    upd_cust.add_argument("--description")
    upd_cust.add_argument("--metadata", action="append", default=[])
    upd_cust.add_argument("--confirm", action="store_true")

    prod = sub.add_parser("create_product", help="Create product")
    prod.add_argument("--name", required=True)
    prod.add_argument("--description")
    prod.add_argument("--metadata", action="append", default=[])
    prod.add_argument("--confirm", action="store_true")

    price = sub.add_parser("create_price", help="Create price")
    price.add_argument("--product", required=True)
    price.add_argument("--unit-amount", required=True, type=int)
    price.add_argument("--currency", required=True)
    price.add_argument("--interval", choices=["day", "week", "month", "year"])
    price.add_argument("--confirm", action="store_true")

    link = sub.add_parser("create_payment_link", help="Create payment link")
    link.add_argument("--price", required=True)
    link.add_argument("--quantity", type=int, default=1)
    link.add_argument("--confirm", action="store_true")

    refund = sub.add_parser("create_refund", help="Create refund")
    refund.add_argument("--payment-intent")
    refund.add_argument("--charge")
    refund.add_argument("--amount", type=int)
    refund.add_argument("--reason", choices=["duplicate", "fraudulent", "requested_by_customer"])
    refund.add_argument("--confirm", action="store_true")

    cancel = sub.add_parser("cancel_subscription", help="Cancel subscription")
    cancel.add_argument("subscription_id")
    cancel.add_argument("--invoice-now", action="store_true")
    cancel.add_argument("--prorate", action="store_true")
    cancel.add_argument("--confirm", action="store_true")

    meta = sub.add_parser("update_metadata", help="Update metadata on a supported object path")
    meta.add_argument("path", help="API path like /customers/cus_123 or /products/prod_123")
    meta.add_argument("--metadata", action="append", default=[], required=True)
    meta.add_argument("--confirm", action="store_true")

    args = p.parse_args()

    if args.cmd == "create_customer":
        require_confirm(args)
        params = {k: v for k, v in {
            "name": args.name,
            "email": args.email,
            "phone": args.phone,
            "description": args.description,
        }.items() if v is not None}
        for k, v in parse_metadata(args.metadata).items():
            params[f"metadata[{k}]"] = v
        print_json(request("POST", "/customers", params))
        return

    if args.cmd == "update_customer":
        require_confirm(args)
        params = {k: v for k, v in {
            "name": args.name,
            "email": args.email,
            "phone": args.phone,
            "description": args.description,
        }.items() if v is not None}
        for k, v in parse_metadata(args.metadata).items():
            params[f"metadata[{k}]"] = v
        print_json(request("POST", f"/customers/{args.customer_id}", params))
        return

    if args.cmd == "create_product":
        require_confirm(args)
        params = {"name": args.name}
        if args.description is not None:
            params["description"] = args.description
        for k, v in parse_metadata(args.metadata).items():
            params[f"metadata[{k}]"] = v
        print_json(request("POST", "/products", params))
        return

    if args.cmd == "create_price":
        require_confirm(args)
        params = {
            "product": args.product,
            "unit_amount": args.unit_amount,
            "currency": args.currency,
        }
        if args.interval:
            params["recurring[interval]"] = args.interval
        print_json(request("POST", "/prices", params))
        return

    if args.cmd == "create_payment_link":
        require_confirm(args)
        params = {
            "line_items[0][price]": args.price,
            "line_items[0][quantity]": args.quantity,
        }
        print_json(request("POST", "/payment_links", params))
        return

    if args.cmd == "create_refund":
        require_confirm(args)
        if not args.payment_intent and not args.charge:
            raise SystemExit("Provide --payment-intent or --charge")
        params = {}
        if args.payment_intent:
            params["payment_intent"] = args.payment_intent
        if args.charge:
            params["charge"] = args.charge
        if args.amount is not None:
            params["amount"] = args.amount
        if args.reason:
            params["reason"] = args.reason
        print_json(request("POST", "/refunds", params))
        return

    if args.cmd == "cancel_subscription":
        require_confirm(args)
        params = {
            "invoice_now": "true" if args.invoice_now else "false",
            "prorate": "true" if args.prorate else "false",
        }
        print_json(request("DELETE", f"/subscriptions/{args.subscription_id}", params))
        return

    if args.cmd == "update_metadata":
        require_confirm(args)
        path = args.path if args.path.startswith("/") else f"/{args.path}"
        params = {}
        for k, v in parse_metadata(args.metadata).items():
            params[f"metadata[{k}]"] = v
        print_json(request("POST", path, params))
        return


if __name__ == "__main__":
    main()
