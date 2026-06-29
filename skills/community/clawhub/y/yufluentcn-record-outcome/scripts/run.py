#!/usr/bin/env python3
"""Harness 效果回传 — OpenClaw 薄客户端（POST /v1/agent/outcomes）。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SHARED_DIR = _SCRIPT_DIR.parent.parent / "_shared"
if str(_SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(_SHARED_DIR))
from bootstrap import ensure_cloud_client_path

ensure_cloud_client_path(__file__)

from yufluent_api import YufluentApiError, record_outcome


def main() -> int:
    parser = argparse.ArgumentParser(
        description="登记 Listing/SEO 等 Harness run 的后续效果（销量、点击等）"
    )
    parser.add_argument("--run-id", required=True, help="技能返回的 run_id")
    parser.add_argument("--event", default="published", help="事件类型，如 published / sale")
    parser.add_argument("--external-id", default="", help="平台 ASIN/SKU 等")
    parser.add_argument("--impressions", type=int, default=0)
    parser.add_argument("--clicks", type=int, default=0)
    parser.add_argument("--orders", type=int, default=0)
    parser.add_argument("--revenue-cny", type=float, default=0.0)
    parser.add_argument("--notes", default="", help="备注")
    parser.add_argument("--json", action="store_true", help="输出完整 JSON")
    args = parser.parse_args()

    payload = {
        "run_id": args.run_id.strip(),
        "event": args.event.strip() or "published",
        "external_id": args.external_id.strip(),
        "impressions": max(0, args.impressions),
        "clicks": max(0, args.clicks),
        "orders": max(0, args.orders),
        "revenue_cny": max(0.0, args.revenue_cny),
        "notes": args.notes.strip(),
    }

    try:
        data = record_outcome(payload)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"OK run_id={data.get('run_id')} event={data.get('event')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
