#!/usr/bin/env python3
import argparse
import json
import pathlib
import shlex

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "requests.json"


def shell_quote(value):
    return shlex.quote(value)


def main():
    parser = argparse.ArgumentParser(description="Print safe curl examples for this ClawMart package.")
    parser.add_argument("--name", help="Only print one example by name.")
    parser.add_argument("--paid", action="store_true", help="Also show where to place a payment header. Do not paste private keys here.")
    args = parser.parse_args()
    data = json.loads(EXAMPLES.read_text())
    requests = data.get("requests", [])
    if args.name:
        requests = [item for item in requests if item.get("name") == args.name]
        if not requests:
            raise SystemExit(f"No example named {args.name!r}. Available: {', '.join(item.get('name','') for item in data.get('requests', []))}")
    for item in requests:
        backend = item.get("backend") or data.get("backend")
        if isinstance(backend, list):
            backend = backend[0]
        url = str(backend).rstrip("/") + item["path"]
        body = json.dumps(item.get("body", {}), separators=(",", ":"))
        headers = ["-H 'content-type: application/json'"]
        if args.paid:
            headers.append("-H 'payment-signature: <x402 payment signature>'")
            headers.append("-H 'X-PAYMENT: <legacy x402 payment header if your client uses it>'")
        print(f"# {item['name']} ({item.get('price','paid x402 endpoint')})")
        print("curl -i -sS \\")
        for header in headers:
            print(f"  {header} \\")
        print(f"  --data {shell_quote(body)} \\")
        print(f"  {shell_quote(url)}")
        print()
    print("Note: without a valid x402 payment header, paid endpoints should return HTTP 402 payment requirements. Never paste wallet private keys into curl commands.")


if __name__ == "__main__":
    main()
