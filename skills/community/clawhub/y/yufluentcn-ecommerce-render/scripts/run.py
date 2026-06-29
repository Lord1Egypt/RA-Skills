#!/usr/bin/env python3
"""模板渲染 — ClawHub 云端薄客户端。"""

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

from cloud_cli import print_run_meta, print_skill_output, read_text_arg
from yufluent_api import YufluentApiError, run_skill

SKILL_API_ID = "commerce-render"
TEMPLATES = ("size_chart", "spec_card", "feature_grid", "compare_table", "promo_banner")


def main() -> int:
    parser = argparse.ArgumentParser(description="TokenApi 模板渲染（Pillow）")
    parser.add_argument("--product", required=True, help="产品名称")
    parser.add_argument("--template", "-t", default="size_chart", choices=TEMPLATES, help="模板类型")
    parser.add_argument("--render-data", help="JSON 数据文件或 JSON 字符串")
    parser.add_argument("--headers", help="表头 JSON 数组（size_chart/compare_table）")
    parser.add_argument("--rows", help="表格行 JSON 数组")
    parser.add_argument("--specs", help="参数 JSON（spec_card）")
    parser.add_argument("--features", help="卖点 JSON（feature_grid）")
    parser.add_argument("--title", help="标题")
    parser.add_argument("--subtitle", help="副标题（promo_banner）")
    parser.add_argument("--brand-color", default="#1a56db", help="品牌色 hex")
    parser.add_argument("--platform-size", help="如 amazon-main / amazon-aplus-banner")
    parser.add_argument("--platform", default="amazon", choices=["amazon", "shopify", "tiktok"])
    parser.add_argument("--lang", default="zh")
    parser.add_argument("--json", action="store_true", help="输出完整 JSON")
    args = parser.parse_args()

    payload: dict = {
        "product": args.product.strip(),
        "template": args.template,
        "platform": args.platform,
        "lang": args.lang,
        "brand_color": args.brand_color.strip(),
    }
    if args.platform_size:
        payload["platform_size"] = args.platform_size.strip()
    if args.render_data:
        payload["render_data"] = read_text_arg(args.render_data)
    if args.title:
        payload["title"] = args.title.strip()
    if args.subtitle:
        payload["subtitle"] = args.subtitle.strip()
    if args.headers:
        payload["headers"] = read_text_arg(args.headers)
    if args.rows:
        payload["rows"] = read_text_arg(args.rows)
    if args.specs:
        payload["specs"] = read_text_arg(args.specs)
    if args.features:
        payload["features"] = read_text_arg(args.features)

    try:
        data = run_skill(SKILL_API_ID, payload, timeout=120.0)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    print_skill_output(data, as_json=args.json, prefer_formatted=not args.json)
    print_run_meta(data, template=args.template, platform=args.platform, lang=args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
