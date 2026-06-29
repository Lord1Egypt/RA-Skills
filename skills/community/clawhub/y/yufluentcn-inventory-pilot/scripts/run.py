#!/usr/bin/env python3
"""库存驾驭助手 — ClawHub 云端薄客户端。"""

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

SKILL_API_ID = "inventory-pilot"
MODES = ("forecast", "replenish", "clearance", "capital")


def main() -> int:
    parser = argparse.ArgumentParser(description="TokenApi 库存驾驭（云端）")
    parser.add_argument("--message", "-m", required=True, help="本轮库存问题")
    parser.add_argument(
        "--mode",
        default="forecast",
        choices=MODES,
        help="库存模式",
    )
    parser.add_argument("--sales-data", help="历史销量 CSV 或文件路径")
    parser.add_argument("--current-stock", help="当前库存")
    parser.add_argument("--inventory-data", help="库存明细（含库龄）或文件路径")
    parser.add_argument("--lead-time", help="供应商交期（天）")
    parser.add_argument("--transit-days", help="头程时效（天）")
    parser.add_argument("--target-days", default="30", help="目标库存天数")
    parser.add_argument("--age-threshold", default="60/90", help="库龄预警阈值")
    parser.add_argument("--unit-cost", help="单位成本说明")
    parser.add_argument("--context", help="补充背景")
    parser.add_argument("--lang", default="zh", help="zh|en|...")
    args = parser.parse_args()

    payload: dict = {
        "message": args.message.strip(),
        "mode": args.mode,
        "platform": "multi",
        "lang": args.lang,
    }
    if args.sales_data:
        payload["sales_data"] = read_text_arg(args.sales_data)
    if args.current_stock:
        payload["current_stock"] = read_text_arg(args.current_stock)
    if args.inventory_data:
        payload["inventory_data"] = read_text_arg(args.inventory_data)
    if args.lead_time:
        payload["lead_time"] = args.lead_time.strip()
    if args.transit_days:
        payload["transit_days"] = args.transit_days.strip()
    if args.target_days:
        payload["target_days"] = args.target_days.strip()
    if args.age_threshold:
        payload["age_threshold"] = args.age_threshold.strip()
    if args.unit_cost:
        payload["unit_cost"] = args.unit_cost.strip()
    if args.context:
        payload["context"] = args.context.strip()

    try:
        data = run_skill(SKILL_API_ID, payload, timeout=180.0)
    except YufluentApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1 if exc.status != 402 else 2

    print_skill_output(data, prefer_formatted=True)
    print_run_meta(data, mode=args.mode, lang=args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
