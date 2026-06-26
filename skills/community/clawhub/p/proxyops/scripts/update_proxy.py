#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_proxies, save_proxies
from lib.scoring import calculate_quality_score

def parse_csv(value):
    if not value:
        return None
    return [v.strip() for v in value.split(",") if v.strip()]

def main():
    parser = argparse.ArgumentParser(description="Update proxy metadata")
    parser.add_argument("--id", required=True)
    parser.add_argument("--status", choices=["active", "inactive"])
    parser.add_argument("--expires_on")
    parser.add_argument("--notes")
    parser.add_argument("--tags")
    parser.add_argument("--session_label")
    args = parser.parse_args()

    data = load_proxies()
    proxies = data.get("proxies", {})

    if args.id not in proxies:
        print(f"Proxy not found: {args.id}")
        sys.exit(1)

    proxy = proxies[args.id]

    if args.status is not None:
        proxy["status"] = args.status
    if args.expires_on is not None:
        proxy["expires_on"] = args.expires_on
    if args.notes is not None:
        proxy["notes"] = args.notes
    if args.tags is not None:
        proxy["tags"] = parse_csv(args.tags) or []
    if args.session_label is not None:
        proxy["session_label"] = args.session_label

    proxy["quality_score"] = calculate_quality_score(proxy)
    proxy["updated_at"] = datetime.now().isoformat()
    save_proxies(data)

    print(f"✓ Updated {args.id}")
    print(f"  Quality score: {proxy['quality_score']}")

if __name__ == "__main__":
    main()
