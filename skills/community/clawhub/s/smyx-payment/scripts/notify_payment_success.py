#!/usr/bin/env python3
"""Print a non-sensitive payment success notification for OpenClaw command cron.

Reads /tmp/payment_success.json (or --result-file), queries account balance, and
prints final markdown to stdout. stdout is announced by OpenClaw cron.
Never reads or prints privateKey/api-key.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-file", default="/tmp/payment_success.json")
    args = parser.parse_args()

    result_path = Path(args.result_file)
    if not result_path.exists():
        print("🦞 支付检测任务已触发，但暂未找到支付结果文件，请稍后回复「再查」。")
        return 0

    try:
        payment = json.loads(result_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"🦞 支付检测任务已触发，但结果文件读取失败：{e}")
        return 0

    sys.path.insert(0, "/root/.openclaw/workspace")
    try:
        from skills.smyx_payment.scripts.query import query_account
        from skills.smyx_payment.scripts.open_id import require_open_id
        balance = query_account(require_open_id(None)) or {}
    except Exception as e:
        balance = {"_error": str(e)}

    order_no = payment.get("order_no", "")
    amount = payment.get("total_amount", "0.00")
    pay_time = payment.get("send_pay_date", "")
    trade_no = payment.get("trade_no", "")

    print("🦞 支付自动检测成功，充值已入账！")
    print()
    print("## ✅ 支付结果")
    print()
    print("| 项目 | 内容 |")
    print("|---|---|")
    print(f"| 订单号 | `{order_no}` |")
    print(f"| 支付金额 | ¥{amount} |")
    print(f"| 支付时间 | {pay_time} |")
    print(f"| 支付宝交易号 | `{trade_no}` |")
    print("| 状态 | ✅ 支付成功 |")
    print()

    if balance.get("_error"):
        print(f"余额查询暂时失败：{balance['_error']}。你可以稍后回复「查余额」。")
        return 0

    print("## 📊 当前账户余额")
    print()
    print("| 项目 | 内容 |")
    print("|---|---:|")
    print(f"| 账户 | {balance.get('phoneNumber', '')} |")
    print(f"| 总可用次数 | {balance.get('totalRecharged', 0)} 次 |")
    print(f"| 已使用次数 | {balance.get('usedCount', 0)} 次 |")
    print(f"| 剩余次数/余额 | ✅ {balance.get('remainingUses', 0)} 次 |")
    print(f"| 是否余额不足 | {'是' if balance.get('isInsufficient', False) else '否'} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
