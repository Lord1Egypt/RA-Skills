#!/usr/bin/env python3
"""
Yufluent Listing — ClawHub 云端薄客户端（模式 A）。

Harness 在服务端执行；本机仅需 TOKENAPI_KEY + requests。
"""

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
from yufluent_api import YufluentApiError, run_skill

SKILL_API_ID = "listing"


def main() -> int:
    parser = argparse.ArgumentParser(description="Yufluent Listing（云端 Harness）")
    parser.add_argument("--product", required=True, help="产品名称")
    parser.add_argument("--keywords", required=True, help="核心关键词，逗号分隔")
    parser.add_argument("--platform", choices=["amazon", "shopify", "tiktok"], default="amazon")
    parser.add_argument("--lang", default="zh", help="zh|en|es|de|fr|ja")
    parser.add_argument("--features", default=None, help="卖点，逗号分隔")
    parser.add_argument("--target-audience", default=None)
    parser.add_argument("--brand-tone", default=None)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument(
        "--format",
        dest="fmt",
        choices=["amazon", "shopify", "tiktok", "json", "auto"],
        default="auto",
        help="输出格式；auto 跟随 --platform",
    )
    parser.add_argument("-o", "--output", default=None, help="写入文件路径")
    args = parser.parse_args()

    payload: dict = {
        "product": args.product.strip(),
        "keywords": args.keywords.strip(),
        "platform": args.platform,
        "lang": args.lang,
        "temperature": args.temperature,
    }
    if args.features and args.features.strip():
        payload["features"] = args.features.strip()
    if args.target_audience:
        payload["target_audience"] = args.target_audience.strip()
    if args.brand_tone:
        payload["brand_tone"] = args.brand_tone.strip()

    try:
        data = run_skill(SKILL_API_ID, payload, timeout=180.0)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    fmt = args.fmt if args.fmt != "auto" else args.platform
    if fmt == "json":
        text = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        text = str(data.get("formatted_text") or "").strip()
        if not text:
            text = json.dumps(data, ensure_ascii=False, indent=2)

    meta = f"# run_id={data.get('run_id')} model={data.get('model_used')} tokens={data.get('total_tokens')}\n"
    out = meta + text

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"Saved to {args.output}")
    else:
        print(out)

    validation = data.get("validation")
    if isinstance(validation, dict) and validation.get("issues"):
        print("\n[validation]", json.dumps(validation, ensure_ascii=False), file=sys.stderr)

    print_run_meta(data, platform=args.platform, lang=args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
