#!/usr/bin/env python3
"""电商 AI 生图 — ClawHub 云端薄客户端（平台 Replicate 代理）。"""

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
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from cloud_cli import encode_image_source, print_run_meta, print_skill_output
from yufluent_api import YufluentApiError, run_skill

SKILL_API_ID = "ecommerce-imaging"
# CLI 场景白名单（与 imaging_prompts.py / scripts/prompt_library.py 保持同步；云端 run 不导入后者）
BASE_SCENES = (
    "white_bg",
    "minimal_white",
    "modern_kitchen",
    "living_room",
    "lifestyle",
    "scene",
    "desk_setup",
    "creative",
    "multi_angle_pack",
)
DEFAULT_ANGLE_PACK = (
    "front_view",
    "side_view",
    "top_view",
    "three_quarter_view",
    "other_angles",
)
EXTENDED_SCENES = (
    "back_view",
    "detail_closeup",
    "christmas",
    "black_friday",
    "prime_day",
    "valentine",
    "lunar_new_year",
    "summer_sale",
    "luxury_minimal",
    "youthful_pop",
    "eco_natural",
    "pro_tech",
    "unboxing",
    "gift_set",
    "influencer_flatlay",
    "flash_sale",
) + DEFAULT_ANGLE_PACK
SCENES = BASE_SCENES + tuple(sorted(set(EXTENDED_SCENES) - set(BASE_SCENES)))
BRAND_STYLES = ("luxury_minimal", "youthful_pop", "eco_natural", "pro_tech")
CATEGORIES = ("kitchenware", "furniture", "electronics", "fashion", "jewelry", "sports_outdoor", "general")
MODELS = ("flux-schnell", "flux-dev", "sd3", "sdxl")
PLATFORMS = ("amazon", "shopify", "tiktok")


def main() -> int:
    parser = argparse.ArgumentParser(description="TokenApi 电商 AI 生图（云端）")
    parser.add_argument("--product", required=True, help="产品名称")
    parser.add_argument("--scene", "-s", default="white_bg", choices=SCENES, help="场景 key")
    parser.add_argument("--category", "-c", default="general", choices=CATEGORIES, help="类目 key")
    parser.add_argument("--brand-style", choices=BRAND_STYLES, help="品牌调性叠加（可选）")
    parser.add_argument("--image-model", "-m", default="flux-schnell", choices=MODELS, help="生图模型")
    parser.add_argument("--platform", default="amazon", choices=PLATFORMS, help="目标平台")
    parser.add_argument("--platform-size", help="平台尺寸 key，如 amazon-main")
    parser.add_argument("--source-image", help="产品实拍 URL 或本地路径（多角度必填）")
    parser.add_argument(
        "--angles",
        help="多角度批量：逗号分隔 front_view,side_view,top_view,... 或 multi_angle_pack",
    )
    parser.add_argument("--prompt", "-p", help="完整 Prompt（覆盖自动构造）")
    parser.add_argument("--extra-description", help="追加到 Prompt 的描述")
    parser.add_argument("--remove-bg", action="store_true", help="生成后去背景")
    parser.add_argument("--upscale", type=int, default=0, help="放大倍数 2/4")
    parser.add_argument("--lang", default="zh", help="zh|en")
    parser.add_argument("--json", action="store_true", help="输出完整 JSON")
    args = parser.parse_args()

    payload: dict = {
        "product": args.product.strip(),
        "scene": args.scene,
        "category": args.category,
        "image_model": args.image_model,
        "platform": args.platform,
        "lang": args.lang,
    }
    if args.platform_size:
        payload["platform_size"] = args.platform_size.strip()
    if args.source_image:
        try:
            payload["source_image"] = encode_image_source(args.source_image)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
    if args.angles:
        payload["angles"] = args.angles.strip()
    elif args.scene == "multi_angle_pack":
        payload["angles"] = ",".join(DEFAULT_ANGLE_PACK)
    if args.prompt:
        payload["prompt"] = args.prompt.strip()
    if args.extra_description:
        payload["extra_description"] = args.extra_description.strip()
    if args.brand_style:
        payload["brand_style"] = args.brand_style
    if args.remove_bg:
        payload["remove_bg"] = True
    if args.upscale and args.upscale > 0:
        payload["upscale"] = args.upscale

    try:
        data = run_skill(SKILL_API_ID, payload, timeout=300.0)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    print_skill_output(data, as_json=args.json, prefer_formatted=not args.json)
    print_run_meta(
        data,
        scene=args.scene,
        platform=args.platform,
        lang=args.lang,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
