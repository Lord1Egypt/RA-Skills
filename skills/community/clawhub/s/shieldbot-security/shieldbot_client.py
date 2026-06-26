#!/usr/bin/env python3
"""ShieldBot OpenClaw Skill — HTTP client for ShieldBot Security API."""

import argparse
import json
import os
import re
import sys

import requests

DEFAULT_BASE = "https://api.shieldbotsecurity.online"
TIMEOUT = 30
VALID_CHAINS = {56, 1, 8453, 42161, 137, 10, 204}


def get_api_base():
    return os.environ.get("SHIELDBOT_API_BASE", DEFAULT_BASE).rstrip("/")


def validate_address(addr):
    if not addr or not re.match(r"^0x[0-9a-fA-F]{40}$", addr):
        print(f"error: invalid address format: {addr}", file=sys.stderr)
        print("Expected: 0x followed by 40 hex characters", file=sys.stderr)
        sys.exit(1)
    return addr


def validate_chain(chain_id):
    if chain_id not in VALID_CHAINS:
        print(f"error: unsupported chain ID: {chain_id}", file=sys.stderr)
        print(f"Supported: {sorted(VALID_CHAINS)}", file=sys.stderr)
        sys.exit(1)
    return chain_id


def call_api(method, path, params=None, json_body=None):
    url = f"{get_api_base()}{path}"
    try:
        resp = requests.request(
            method, url, params=params, json=json_body, timeout=TIMEOUT
        )
        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After", "unknown")
            print(f"error: rate limited. Retry after {retry_after}s", file=sys.stderr)
            sys.exit(1)
        if resp.status_code >= 400:
            detail = resp.text[:200]
            print(
                f"error: ShieldBot API returned {resp.status_code}: {detail}",
                file=sys.stderr,
            )
            sys.exit(1)
        return resp.json()
    except requests.exceptions.Timeout:
        print(f"error: ShieldBot API timeout ({TIMEOUT}s)", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("error: cannot reach ShieldBot API", file=sys.stderr)
        sys.exit(1)


def action_scan(args):
    validate_address(args.address)
    validate_chain(args.chain)
    return call_api("POST", "/api/scan", json_body={
        "address": args.address,
        "chainId": args.chain,
    })


def action_simulate(args):
    validate_address(args.to)
    validate_address(args.from_addr)
    validate_chain(args.chain)
    body = {
        "to": args.to,
        "from": args.from_addr,
        "value": args.value or "0x0",
        "data": args.data or "0x",
        "chainId": args.chain,
    }
    return call_api("POST", "/api/firewall", json_body=body)


def action_deployer(args):
    validate_address(args.address)
    params = {}
    if args.chain != 56:
        params["chain_id"] = args.chain
    return call_api("GET", f"/api/campaign/{args.address}", params=params or None)


def action_threats(args):
    params = {"limit": args.limit}
    if args.chain != 56:
        params["chain_id"] = args.chain
    return call_api("GET", "/api/threats/feed", params=params)


def action_phishing(args):
    if not args.url:
        print("error: --url is required for phishing check", file=sys.stderr)
        sys.exit(1)
    return call_api("GET", "/api/phishing", params={"url": args.url})


def action_campaigns(args):
    return call_api("GET", "/api/campaigns/top", params={"limit": args.limit})


def action_approvals(args):
    validate_address(args.address)
    validate_chain(args.chain)
    return call_api(
        "GET",
        f"/api/rescue/{args.address}",
        params={"chain_id": args.chain},
    )


def action_ask(args):
    if not args.message:
        print("error: --message is required for ask", file=sys.stderr)
        sys.exit(1)
    return call_api("POST", "/api/agent/chat", json_body={
        "message": args.message,
        "user_id": "openclaw-agent",
        "chain_id": args.chain,
    })


ACTIONS = {
    "scan": action_scan,
    "simulate": action_simulate,
    "deployer": action_deployer,
    "threats": action_threats,
    "phishing": action_phishing,
    "campaigns": action_campaigns,
    "approvals": action_approvals,
    "ask": action_ask,
}


def parse_args():
    p = argparse.ArgumentParser(description="ShieldBot Security API client")
    p.add_argument(
        "--action",
        required=True,
        choices=sorted(ACTIONS.keys()),
        help="Action to perform",
    )
    p.add_argument("--address", help="Contract or wallet address (0x...)")
    p.add_argument("--to", help="Transaction destination address (simulate)")
    p.add_argument("--from-addr", help="Transaction sender address (simulate)")
    p.add_argument("--value", help="Transaction value in hex (simulate, default 0x0)")
    p.add_argument("--data", help="Transaction calldata in hex (simulate, default 0x)")
    p.add_argument("--url", help="URL to check (phishing)")
    p.add_argument("--message", help="Question for AI advisor (ask)")
    p.add_argument("--chain", type=int, default=56, help="Chain ID (default: 56)")
    p.add_argument("--limit", type=int, default=10, help="Result limit (default: 10)")
    p.add_argument(
        "--raw", action="store_true", help="Output raw JSON instead of formatted text"
    )
    return p.parse_args()


def main():
    args = parse_args()
    handler = ACTIONS[args.action]
    result = handler(args)

    if args.raw:
        print(json.dumps(result, indent=2))
    else:
        try:
            from format_output import format_result
            print(format_result(args.action, result))
        except ImportError:
            print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
