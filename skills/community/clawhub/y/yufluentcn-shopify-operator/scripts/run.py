#!/usr/bin/env python3
"""Shopify 全店运营教练 — ClawHub 云端薄客户端。"""

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

SKILL_API_ID = "shopify-operator"
STAGES = ("sourcing", "supplier", "listing", "decoration", "social", "monitoring")


def main() -> int:
    parser = argparse.ArgumentParser(description="TokenApi Shopify 全店运营教练（云端）")
    parser.add_argument("--message", "-m", required=True, help="本轮用户消息")
    parser.add_argument("--stage", default="sourcing", choices=STAGES, help="工作流阶段")
    parser.add_argument("--niche", help="细分品类")
    parser.add_argument("--store-url", dest="store_url", help="Shopify 店铺 URL")
    parser.add_argument("--context", help="补充背景")
    parser.add_argument("--lang", default="zh", help="zh|en|...")
    args = parser.parse_args()

    payload: dict = {
        "message": args.message.strip(),
        "stage": args.stage,
        "platform": "shopify",
        "lang": args.lang,
    }
    if args.niche:
        payload["niche"] = args.niche.strip()
    if args.store_url:
        payload["store_url"] = args.store_url.strip()
    if args.context:
        payload["context"] = args.context.strip()

    try:
        data = run_skill(SKILL_API_ID, payload, timeout=180.0)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    print_skill_output(data, prefer_formatted=False)
    print_run_meta(data, stage=args.stage, lang=args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
