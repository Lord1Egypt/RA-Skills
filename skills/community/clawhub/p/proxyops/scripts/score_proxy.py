#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_proxies, save_proxies, load_stats, save_stats
from lib.scoring import calculate_quality_score

def main():
    parser = argparse.ArgumentParser(description="Update scoring fields for a proxy")
    parser.add_argument("--id", required=True)
    parser.add_argument("--success_rate", type=float)
    parser.add_argument("--avg_latency_ms", type=int)
    parser.add_argument("--status", choices=["active", "inactive"])
    args = parser.parse_args()

    data = load_proxies()
    proxies = data.get("proxies", {})

    if args.id not in proxies:
        print(f"Proxy not found: {args.id}")
        sys.exit(1)

    proxy = proxies[args.id]

    if args.success_rate is not None:
        proxy["success_rate"] = args.success_rate
    if args.avg_latency_ms is not None:
        proxy["avg_latency_ms"] = args.avg_latency_ms
    if args.status is not None:
        proxy["status"] = args.status

    proxy["quality_score"] = calculate_quality_score(proxy)
    proxy["updated_at"] = datetime.now().isoformat()
    save_proxies(data)

    stats = load_stats()
    stats["last_scored_at"] = datetime.now().isoformat()
    save_stats(stats)

    print(f"✓ Scored {args.id}")
    print(f"  Quality score: {proxy['quality_score']}")

if __name__ == "__main__":
    main()
