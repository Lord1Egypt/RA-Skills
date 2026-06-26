#!/usr/bin/env python3
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_proxies
from lib.scoring import fit_score

def reason_for(proxy, region=None, protocol=None, rotation=None):
    reasons = []

    if region and (proxy.get("region") or "").lower() == region.lower():
        reasons.append("region matches")
    if protocol and (proxy.get("protocol") or "").lower() == protocol.lower():
        reasons.append("protocol matches")
    if rotation and (proxy.get("rotation") or "").lower() == rotation.lower():
        reasons.append("rotation matches")

    score = proxy.get("quality_score")
    if score is not None:
        reasons.append(f"quality score {score}")

    latency = proxy.get("avg_latency_ms")
    if latency is not None:
        reasons.append(f"latency {latency}ms")

    return ", ".join(reasons) if reasons else "best available fit"

def main():
    parser = argparse.ArgumentParser(description="Pick the best-fit proxy")
    parser.add_argument("--region")
    parser.add_argument("--protocol", choices=["http", "https", "socks5"])
    parser.add_argument("--rotation", choices=["sticky", "rotating"])
    parser.add_argument("--max_latency_ms", type=int)
    args = parser.parse_args()

    data = load_proxies()
    proxies = list(data.get("proxies", {}).values())

    ranked = []
    for proxy in proxies:
        ranked.append((
            fit_score(
                proxy,
                region=args.region,
                protocol=args.protocol,
                rotation=args.rotation,
                max_latency_ms=args.max_latency_ms
            ),
            proxy
        ))

    ranked.sort(key=lambda x: x[0], reverse=True)
    picks = [proxy for score, proxy in ranked if score > 0][:3]

    if not picks:
        print("No strong proxy match found.")
        return

    labels = ["Top Pick", "Backup", "Backup"]
    for idx, proxy in enumerate(picks):
        print(f"{labels[idx]} — {proxy['id']} | {proxy['label']}")
        print(f"  {reason_for(proxy, region=args.region, protocol=args.protocol, rotation=args.rotation)}")

if __name__ == "__main__":
    main()
