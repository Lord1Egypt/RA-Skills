#!/usr/bin/env python3
"""跨境电商买家消息回复 — ClawHub 云端薄客户端。"""

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

SKILL_API_ID = "chat-assist"


def main() -> int:
    parser = argparse.ArgumentParser(description="TokenApi 客服回复（云端）")
    parser.add_argument("--message", required=True, help="买家消息")
    parser.add_argument("--platform", choices=["amazon", "shopify", "tiktok"], default="amazon")
    parser.add_argument("--lang", default="zh", help="zh|en|es|de|fr|ja")
    parser.add_argument("--product", help="关联商品名或 SKU")
    parser.add_argument("--order-context", dest="order_context", help="订单号或物流状态")
    args = parser.parse_args()

    payload: dict = {
        "platform": args.platform,
        "lang": args.lang,
        "message": args.message.strip(),
    }
    if args.product:
        payload["product"] = args.product.strip()
    if args.order_context:
        payload["order_context"] = args.order_context.strip()

    try:
        data = run_skill(SKILL_API_ID, payload, timeout=120.0)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    print_skill_output(data, prefer_formatted=False)
    print_run_meta(data, platform=args.platform, lang=args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
