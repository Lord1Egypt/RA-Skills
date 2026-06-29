#!/usr/bin/env python3
"""B2B 询盘回复 / RFQ 报价 — ClawHub 云端薄客户端。"""

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

SKILL_API_ID = "b2b-assist"


def main() -> int:
    parser = argparse.ArgumentParser(description="TokenApi B2B Assist（云端）")
    parser.add_argument("--message", required=True, help="买家询盘原文或 .txt 文件路径")
    parser.add_argument("--product", help="产品名称")
    parser.add_argument("--moq", help="MOQ")
    parser.add_argument("--fob-price", dest="fob_price", help="FOB 报价")
    parser.add_argument("--cif-price", dest="cif_price", help="CIF 报价")
    parser.add_argument("--lead-time", dest="lead_time", help="交期")
    parser.add_argument("--payment-terms", dest="payment_terms", help="付款方式")
    parser.add_argument("--company-profile", dest="company_profile", help="公司简介")
    parser.add_argument(
        "--inquiry-type",
        dest="inquiry_type",
        default="rfq",
        help="询盘类型，如 rfq / general",
    )
    parser.add_argument("--lang", default="en")
    parser.add_argument("-o", "--output", help="写入 JSON 文件")
    args = parser.parse_args()

    payload: dict = {
        "platform": "multi",
        "lang": args.lang,
        "message": read_text_arg(args.message),
        "inquiry_type": args.inquiry_type,
    }
    for key in (
        "product",
        "moq",
        "fob_price",
        "cif_price",
        "lead_time",
        "payment_terms",
        "company_profile",
    ):
        val = getattr(args, key)
        if val and str(val).strip():
            payload[key] = str(val).strip()

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
    print_run_meta(data, lang=args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
