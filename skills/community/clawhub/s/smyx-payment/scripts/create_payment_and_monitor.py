#!/usr/bin/env python3
"""Create a SMYX payment order, print the H5 payment URL, then monitor it.

Designed for OpenClaw WebChat: run this script as a top-level OpenClaw exec
background process. The process prints an initial JSON line containing the
non-sensitive payment card data, then keeps running until payment succeeds or
timeout. When the top-level exec exits, OpenClaw can notify/wake the current
session via exec lifecycle events.

Security:
- privateKey is read only from create_order response.
- privateKey remains in this process memory only.
- privateKey is never printed, saved, passed via argv/env, or written to files.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
import time
from datetime import datetime
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace"
if WORKSPACE not in sys.path:
    sys.path.insert(0, WORKSPACE)

from skills.smyx_payment.scripts.open_id import require_open_id
from skills.smyx_payment.scripts.pay_with_cloud_order import (
    create_payment_with_cloud_order,
    extract_private_key_from_order,
    query_alipay_trade_status,
)
from skills.smyx_payment.scripts.query import query_account
from skills.smyx_payment.scripts.recharge import create_recharge_order

DEFAULT_RESULT_FILE = "/tmp/payment_success.json"


def get_order_no(obj: dict) -> str | None:
    data = obj.get("data") if isinstance(obj.get("data"), dict) else {}
    return obj.get("orderNo") or obj.get("order_no") or data.get("orderNo") or data.get("order_no")


def emit(event: dict) -> None:
    print(json.dumps(event, ensure_ascii=False), flush=True)


def write_success_result(result_file: str, status_result: dict, order_no: str, balance: dict | None = None) -> None:
    result_data = {
        "order_no": order_no,
        "total_amount": status_result.get("total_amount", "0.00"),
        "send_pay_date": status_result.get("send_pay_date", ""),
        "trade_no": status_result.get("trade_no", ""),
        "status": "success",
        "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "balance": balance or {},
    }
    tmp_file = f"{result_file}.tmp.{Path(__file__).name}.{int(time.time())}"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False)
    Path(tmp_file).replace(result_file)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create payment and monitor order status")
    parser.add_argument("--amount", type=float, default=0.01)
    parser.add_argument("--package-name", default="测试套餐")
    parser.add_argument("--uses", type=int, default=10)
    parser.add_argument("--subject", default="小龙虾主厨 - 测试套餐充值")
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--interval-seconds", type=int, default=5)
    parser.add_argument("--result-file", default=DEFAULT_RESULT_FILE)
    args = parser.parse_args()

    open_id = require_open_id(None)

    # Hide noisy create_order prints and avoid accidental sensitive stdout.
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        result = create_recharge_order(
            phone=open_id,
            amount=args.amount,
            package_type=args.package_name,
            detail=f"增值账户续费 - {args.package_name}",
        )

    if not isinstance(result, dict):
        emit({"event": "create_order_failed", "success": False, "message": str(result)})
        return 2

    order_no = get_order_no(result)
    if not order_no:
        emit({"event": "create_order_failed", "success": False, "message": "missing orderNo", "keys": sorted(map(str, result.keys()))})
        return 2

    private_key = extract_private_key_from_order(result)
    pay_result = create_payment_with_cloud_order(
        cloud_order_no=order_no,
        phone=open_id,
        amount=args.amount,
        subject=args.subject,
        package_name=args.package_name,
        uses=args.uses,
        private_key_string=private_key,
    )

    # Initial event: safe for UI display. Do not include internal identity/privateKey.
    emit({
        "event": "payment_ready",
        "success": True,
        "order_no": order_no,
        "payment_url": pay_result.get("pay_url"),
        "amount": args.amount,
        "package_name": args.package_name,
        "uses": args.uses,
        "monitor_mode": "openclaw_exec_background",
    })

    start = time.time()
    last_status = ""
    while time.time() - start <= args.timeout_seconds:
        status_result = query_alipay_trade_status(order_no, private_key_string=private_key)
        trade_status = status_result.get("trade_status", "")
        if trade_status and trade_status != last_status:
            last_status = trade_status
            emit({"event": "payment_status", "order_no": order_no, "trade_status": trade_status})

        if trade_status in ["TRADE_SUCCESS", "TRADE_FINISHED"]:
            try:
                balance = query_account(open_id) or {}
            except Exception as e:
                balance = {"_error": str(e)}
            write_success_result(args.result_file, status_result, order_no, balance=balance)
            emit({
                "event": "payment_success",
                "success": True,
                "order_no": order_no,
                "total_amount": status_result.get("total_amount", "0.00"),
                "send_pay_date": status_result.get("send_pay_date", ""),
                "trade_no": status_result.get("trade_no", ""),
                "balance": balance,
            })
            return 0

        if trade_status == "TRADE_CLOSED":
            emit({"event": "payment_closed", "success": False, "order_no": order_no})
            return 3

        time.sleep(args.interval_seconds)

    emit({"event": "payment_timeout", "success": False, "order_no": order_no, "timeout_seconds": args.timeout_seconds})
    return 4


if __name__ == "__main__":
    raise SystemExit(main())
