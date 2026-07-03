#!/usr/bin/env python3
"""广告投放优化 — ClawHub 云端薄客户端。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_SHARED_DIR = _SCRIPT_DIR.parent.parent / "_shared"
if str(_SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(_SHARED_DIR))
from bootstrap import ensure_cloud_client_path

ensure_cloud_client_path(__file__)
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from cloud_cli import print_run_meta, print_skill_output
from yufluent_api import YufluentApiError, run_skill

SKILL_API_ID = "ad-optimize"
DIMENSIONS = ("targeting", "creatives", "bidding", "landing", "analytics")
CHANNELS = ("meta", "tiktok", "google", "multi")


def main() -> int:
    parser = argparse.ArgumentParser(description="TokenApi 广告投放优化（云端）")
    parser.add_argument("--message", "-m", required=True, help="本轮问题或优化目标")
    parser.add_argument(
        "--dimension",
        default="targeting",
        choices=DIMENSIONS,
        help="优化维度",
    )
    parser.add_argument(
        "--platform",
        "--channel",
        dest="platform",
        default="meta",
        choices=CHANNELS,
        help="广告渠道 meta|tiktok|google|multi",
    )
    parser.add_argument("--product", help="产品或品类")
    parser.add_argument("--market", help="目标市场，如 Vietnam、美国")
    parser.add_argument("--metrics", help="现有指标快照（ROAS、CTR、CPA 等）")
    parser.add_argument("--context", help="补充背景")
    parser.add_argument("--lang", default="zh", help="zh|en|...")
    args = parser.parse_args()

    payload: dict = {
        "message": args.message.strip(),
        "dimension": args.dimension,
        "platform": args.platform,
        "lang": args.lang,
    }
    if args.product:
        payload["product"] = args.product.strip()
    if args.market:
        payload["market"] = args.market.strip()
    if args.metrics:
        payload["metrics"] = args.metrics.strip()
    if args.context:
        payload["context"] = args.context.strip()

    try:
        data = run_skill(SKILL_API_ID, payload, timeout=180.0)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    print_skill_output(data, prefer_formatted=False)
    print_run_meta(data, dimension=args.dimension, platform=args.platform, lang=args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
