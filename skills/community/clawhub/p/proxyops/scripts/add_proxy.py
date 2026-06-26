#!/usr/bin/env python3
import argparse
import os
import sys
import uuid
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_proxies, save_proxies, load_stats, save_stats
from lib.scoring import calculate_quality_score

VALID_PROTOCOLS = ["http", "https", "socks5"]
VALID_ROTATION = ["sticky", "rotating"]
VALID_STATUS = ["active", "inactive"]

def parse_csv(value):
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]

def recount_stats(proxies):
    total = len(proxies)
    active = 0
    inactive = 0
    expired = 0
    now = datetime.now().date()

    for proxy in proxies.values():
        if proxy.get("status") == "active":
            active += 1
        else:
            inactive += 1

        expires_on = proxy.get("expires_on")
        if expires_on:
            try:
                if datetime.fromisoformat(expires_on).date() < now:
                    expired += 1
            except ValueError:
                pass

    return total, active, inactive, expired

def main():
    parser = argparse.ArgumentParser(description="Add a proxy asset")
    parser.add_argument("--label", required=True)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--protocol", choices=VALID_PROTOCOLS, required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--auth_type", default="userpass")
    parser.add_argument("--region", help="Country/region code, e.g. JP")
    parser.add_argument("--city")
    parser.add_argument("--type", default="datacenter", help="datacenter / residential / mobile / isp")
    parser.add_argument("--rotation", choices=VALID_ROTATION, default="sticky")
    parser.add_argument("--session_label")
    parser.add_argument("--status", choices=VALID_STATUS, default="active")
    parser.add_argument("--success_rate", type=float)
    parser.add_argument("--avg_latency_ms", type=int)
    parser.add_argument("--expires_on", help="YYYY-MM-DD")
    parser.add_argument("--cost_monthly", type=float)
    parser.add_argument("--tags")
    parser.add_argument("--notes", default="")

    args = parser.parse_args()

    proxy_id = f"PRX-{str(uuid.uuid4())[:4].upper()}"
    now = datetime.now().isoformat()

    proxy = {
        "id": proxy_id,
        "label": args.label,
        "provider": args.provider,
        "protocol": args.protocol,
        "host": args.host,
        "port": args.port,
        "auth_type": args.auth_type,
        "region": args.region,
        "city": args.city,
        "type": args.type,
        "rotation": args.rotation,
        "session_label": args.session_label,
        "status": args.status,
        "quality_score": 0,
        "success_rate": args.success_rate,
        "avg_latency_ms": args.avg_latency_ms,
        "expires_on": args.expires_on,
        "cost_monthly": args.cost_monthly,
        "tags": parse_csv(args.tags),
        "notes": args.notes,
        "created_at": now,
        "updated_at": now
    }

    proxy["quality_score"] = calculate_quality_score(proxy)

    data = load_proxies()
    data["proxies"][proxy_id] = proxy
    save_proxies(data)

    stats = load_stats()
    total, active, inactive, expired = recount_stats(data["proxies"])
    stats["total_proxies"] = total
    stats["active_proxies"] = active
    stats["inactive_proxies"] = inactive
    stats["expired_proxies"] = expired
    save_stats(stats)

    print(f"✓ Proxy added: {proxy_id}")
    print(f"  {args.label}")
    print(f"  Provider: {args.provider}")
    print(f"  Quality score: {proxy['quality_score']}")

if __name__ == "__main__":
    main()
