#!/usr/bin/env python3
"""广告投放优化 — ClawHub 云端薄客户端。"""

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

from cloud_cli import print_run_meta, print_skill_output
from metrics_input import build_metrics_payload, load_metrics_file, load_metrics_json_arg
from yufluent_api import YufluentApiError, run_skill

SKILL_API_ID = "ad-optimize"
DIMENSIONS = ("targeting", "creatives", "bidding", "landing", "analytics")
CHANNELS = ("meta", "tiktok", "google", "multi")
# browser_extract 产出的 platform 值 → ad-optimize 渠道别名
_ADS_PLATFORM_ALIASES = {
    "meta_ads": "meta",
    "google_ads": "google",
    "tiktok_ads": "tiktok",
    "amazon_ads": "multi",
}


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
        default=None,
        choices=CHANNELS,
        help="广告渠道 meta|tiktok|google|multi（省略时从 --metrics-json 推断）",
    )
    parser.add_argument("--product", help="产品或品类")
    parser.add_argument("--market", help="目标市场，如 Vietnam、美国")
    parser.add_argument("--metrics", help="指标快照文本（ROAS、CTR、CPA 等）")
    parser.add_argument(
        "--metrics-json",
        help='结构化指标 JSON，如 browser_extract 输出或 {"summary":{"roas":"1.4"},"campaigns":[...]}',
    )
    parser.add_argument("--metrics-file", help="结构化指标 JSON 文件路径")
    parser.add_argument("--context", help="补充背景")
    parser.add_argument("--lang", default="zh", help="zh|en|...")
    args = parser.parse_args()

    try:
        metrics_data = load_metrics_json_arg(args.metrics_json)
        if args.metrics_file:
            file_data = load_metrics_file(args.metrics_file)
            metrics_data = {**(metrics_data or {}), **(file_data or {})}
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: 指标 JSON 无效 — {exc}", file=sys.stderr)
        return 1

    payload: dict = {
        "message": args.message.strip(),
        "dimension": args.dimension,
        "lang": args.lang,
    }
    if args.platform:
        payload["platform"] = args.platform
    if args.product:
        payload["product"] = args.product.strip()
    if args.market:
        payload["market"] = args.market.strip()
    if args.context:
        payload["context"] = args.context.strip()

    payload.update(
        build_metrics_payload(
            metrics_text=args.metrics,
            metrics_data=metrics_data,
        )
    )
    # 用户未显式指定 platform 时，从结构化指标推断（兼容 browser_extract 的 *_ads 值）
    if not str(payload.get("platform") or "").strip() and metrics_data:
        raw_platform = str(metrics_data.get("platform") or "").strip().lower()
        platform = _ADS_PLATFORM_ALIASES.get(raw_platform, raw_platform)
        if platform in CHANNELS:
            payload["platform"] = platform
    # 仍未确定时回退 meta（保持原默认行为）
    if not str(payload.get("platform") or "").strip():
        payload["platform"] = "meta"

    try:
        data = run_skill(SKILL_API_ID, payload, timeout=180.0)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    print_skill_output(data, prefer_formatted=False)
    print_run_meta(data, dimension=args.dimension, platform=payload.get("platform"), lang=args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
