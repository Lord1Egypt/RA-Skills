#!/usr/bin/env python3
"""跨境合规卫士 — ClawHub 云端薄客户端。"""

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

SKILL_API_ID = "compliance-guard"
MODES = ("certification", "tariff", "labeling", "platform_rules")
PLATFORMS = ("multi", "amazon", "shopify", "tiktok")


def main() -> int:
    parser = argparse.ArgumentParser(description="TokenApi 合规卫士（云端）")
    parser.add_argument("--message", "-m", required=True, help="本轮合规问题")
    parser.add_argument("--product", required=True, help="产品名称或描述")
    parser.add_argument(
        "--mode",
        default="certification",
        choices=MODES,
        help="合规模式",
    )
    parser.add_argument(
        "--platform",
        default="multi",
        choices=PLATFORMS,
        help="平台（platform_rules 模式用 amazon/shopify/tiktok）",
    )
    parser.add_argument("--target-market", "--market", dest="target_market", help="目标市场")
    parser.add_argument("--category", help="产品类目")
    parser.add_argument("--material", help="材质或成分")
    parser.add_argument("--declared-value", help="申报货值")
    parser.add_argument("--hs-code", help="已知 HS 编码")
    parser.add_argument("--origin-country", help="原产国")
    parser.add_argument("--context", help="补充背景")
    parser.add_argument("--lang", default="zh", help="zh|en|...")
    args = parser.parse_args()

    payload: dict = {
        "message": args.message.strip(),
        "product": args.product.strip(),
        "mode": args.mode,
        "platform": args.platform,
        "lang": args.lang,
    }
    if args.target_market:
        payload["target_market"] = args.target_market.strip()
    if args.category:
        payload["category"] = args.category.strip()
    if args.material:
        payload["material"] = args.material.strip()
    if args.declared_value:
        payload["declared_value"] = args.declared_value.strip()
    if args.hs_code:
        payload["hs_code"] = args.hs_code.strip()
    if args.origin_country:
        payload["origin_country"] = args.origin_country.strip()
    if args.context:
        payload["context"] = args.context.strip()

    try:
        data = run_skill(SKILL_API_ID, payload, timeout=180.0)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    print_skill_output(data, prefer_formatted=True)
    print_run_meta(data, mode=args.mode, platform=args.platform, lang=args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
