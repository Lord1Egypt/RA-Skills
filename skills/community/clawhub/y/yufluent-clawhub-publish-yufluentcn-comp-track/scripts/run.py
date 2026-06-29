#!/usr/bin/env python3
"""竞品 Listing 快照对比 — ClawHub 云端薄客户端。"""

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

SKILL_API_ID = "comp-track"


def main() -> int:
    parser = argparse.ArgumentParser(description="TokenApi Comp Track（云端）")
    parser.add_argument("--our-product", required=True, help="我方产品名")
    parser.add_argument(
        "--competitor",
        required=True,
        help="竞品 Listing 文案或 .txt 文件路径",
    )
    parser.add_argument("--our-listing", help="我方 Listing 文案或文件路径")
    parser.add_argument("--platform", choices=["amazon", "shopify", "tiktok"], default="amazon")
    parser.add_argument("--lang", default="zh")
    parser.add_argument("-o", "--output", help="写入 JSON 文件")
    args = parser.parse_args()

    payload: dict = {
        "platform": args.platform,
        "lang": args.lang,
        "our_product": args.our_product.strip(),
        "competitor": read_text_arg(args.competitor),
    }
    if args.our_listing:
        payload["our_listing"] = read_text_arg(args.our_listing)

    try:
        data = run_skill(SKILL_API_ID, payload, timeout=180.0)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    if args.output:
        out = data.get("formatted_text") or ""
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print_skill_output(data, prefer_formatted=True)
    print_run_meta(data, platform=args.platform)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
