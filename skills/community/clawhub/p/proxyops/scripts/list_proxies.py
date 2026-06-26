#!/usr/bin/env python3
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_proxies

def main():
    parser = argparse.ArgumentParser(description="List proxies")
    parser.add_argument("--region")
    parser.add_argument("--protocol")
    parser.add_argument("--status")
    parser.add_argument("--provider")
    args = parser.parse_args()

    data = load_proxies()
    proxies = list(data.get("proxies", {}).values())

    filtered = []
    for proxy in proxies:
        if args.region and (proxy.get("region") or "").lower() != args.region.lower():
            continue
        if args.protocol and (proxy.get("protocol") or "").lower() != args.protocol.lower():
            continue
        if args.status and (proxy.get("status") or "").lower() != args.status.lower():
            continue
        if args.provider and (proxy.get("provider") or "").lower() != args.provider.lower():
            continue
        filtered.append(proxy)

    if not filtered:
        print("No proxies found.")
        return

    filtered.sort(key=lambda x: x.get("quality_score", 0), reverse=True)

    for proxy in filtered:
        print(f"{proxy['id']} | {proxy['label']}")
        print(
            f"  provider={proxy.get('provider')} "
            f"protocol={proxy.get('protocol')} "
            f"region={proxy.get('region')} "
            f"rotation={proxy.get('rotation')} "
            f"status={proxy.get('status')} "
            f"score={proxy.get('quality_score')}"
        )

if __name__ == "__main__":
    main()
