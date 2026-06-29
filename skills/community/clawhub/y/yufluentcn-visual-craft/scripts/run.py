#!/usr/bin/env python3
"""视觉内容工坊 — ClawHub 云端薄客户端。"""

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

from cloud_cli import print_run_meta, print_skill_output, read_text_arg
from yufluent_api import YufluentApiError, run_skill

SKILL_API_ID = "visual-craft"
MODES = ("a_plus", "video_script", "main_image", "image_compliance")
PLATFORMS = ("amazon", "shopify", "tiktok")


def main() -> int:
    parser = argparse.ArgumentParser(description="TokenApi 视觉工坊（云端）")
    parser.add_argument("--message", "-m", required=True, help="本轮视觉内容需求")
    parser.add_argument("--product", required=True, help="产品名称")
    parser.add_argument(
        "--mode",
        default="a_plus",
        choices=MODES,
        help="视觉模式",
    )
    parser.add_argument(
        "--platform",
        default="amazon",
        choices=PLATFORMS,
        help="目标平台",
    )
    parser.add_argument("--duration", default="30s", help="视频时长 15s/30s/60s")
    parser.add_argument("--listing-context", help="Listing 文案或文件路径")
    parser.add_argument("--competitor-ref", help="竞品参考描述")
    parser.add_argument("--image-description", help="待检查图片描述")
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
    if args.duration:
        payload["duration"] = args.duration.strip()
    if args.listing_context:
        payload["listing_context"] = read_text_arg(args.listing_context)
    if args.competitor_ref:
        payload["competitor_ref"] = args.competitor_ref.strip()
    if args.image_description:
        payload["image_description"] = args.image_description.strip()
    if args.context:
        payload["context"] = args.context.strip()

    try:
        data = run_skill(SKILL_API_ID, payload, timeout=180.0)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    print_skill_output(data, prefer_formatted=False)
    print_run_meta(data, mode=args.mode, platform=args.platform, lang=args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
