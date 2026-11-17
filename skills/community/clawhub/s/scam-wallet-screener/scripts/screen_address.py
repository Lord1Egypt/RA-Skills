#!/usr/bin/env python3
"""
Scam / Drainer Wallet Screener
--------------------------------
Checks EVM addresses (Ethereum, Base, Polygon, BSC, etc.) against the
ScamSniffer community-maintained blocklist of known phishing, drainer,
and scam addresses. Data source is a public, actively-updated GitHub
JSON feed maintained by the ScamSniffer project (no API key required).

Usage:
    python3 screen_address.py 0xabc123...
    python3 screen_address.py 0xabc123... 0xdef456...
    python3 screen_address.py --json 0xabc123...
    python3 screen_address.py --refresh 0xabc123...   # force re-download of blocklist

Cache:
    The blocklist (~2,500+ addresses, ~120KB) is cached locally at
    ~/.cache/scam-wallet-screener/address.json for 6 hours to avoid
    hitting GitHub on every call. Use --refresh to force an update.
"""
import argparse
import json
import os
import sys
import time
import urllib.request

BLOCKLIST_URL = "https://raw.githubusercontent.com/scamsniffer/scam-database/main/blacklist/address.json"
CACHE_DIR = os.path.expanduser("~/.cache/scam-wallet-screener")
CACHE_FILE = os.path.join(CACHE_DIR, "address.json")
CACHE_TTL_SECONDS = 6 * 60 * 60
TIMEOUT = 15
HEADERS = {"User-Agent": "scam-wallet-screener/1.0"}


def _download_blocklist():
    req = urllib.request.Request(BLOCKLIST_URL, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = json.loads(resp.read().decode())
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump({"fetched_at": time.time(), "addresses": data}, f)
    return data


def load_blocklist(force_refresh: bool = False):
    if not force_refresh and os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE) as f:
                cached = json.load(f)
            if time.time() - cached.get("fetched_at", 0) < CACHE_TTL_SECONDS:
                return cached["addresses"]
        except Exception:
            pass
    try:
        return _download_blocklist()
    except Exception as e:
        # fall back to stale cache if the network fetch fails
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE) as f:
                cached = json.load(f)
            return cached["addresses"]
        raise RuntimeError(f"Could not fetch or load blocklist: {e}")


def screen(address: str, blocklist_set) -> dict:
    normalized = address.strip().lower()
    is_flagged = normalized in blocklist_set
    return {
        "address": address,
        "flagged": is_flagged,
        "source": "scamsniffer/scam-database (community-maintained)" if is_flagged else None,
    }


def main():
    parser = argparse.ArgumentParser(description="Screen EVM addresses against the ScamSniffer community blocklist.")
    parser.add_argument("addresses", nargs="+", help="One or more 0x... addresses to check")
    parser.add_argument("--refresh", action="store_true", help="Force re-download of the blocklist instead of using cache")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of a formatted report")
    args = parser.parse_args()

    try:
        blocklist = load_blocklist(force_refresh=args.refresh)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    blocklist_set = {a.lower() for a in blocklist}
    results = [screen(a, blocklist_set) for a in args.addresses]

    if args.json:
        print(json.dumps({"blocklist_size": len(blocklist_set), "results": results}, indent=2))
        return

    print(f"Checked against {len(blocklist_set)} known scam/drainer addresses.\n")
    for r in results:
        status = "FLAGGED — known scam/drainer address" if r["flagged"] else "not found in blocklist"
        print(f"  {r['address']}  ->  {status}")
    print(
        "\nNote: absence from this list is NOT proof of safety — it only means "
        "the address hasn't been reported to this particular community feed. "
        "Always independently verify contracts before signing transactions."
    )


if __name__ == "__main__":
    sys.exit(main())
