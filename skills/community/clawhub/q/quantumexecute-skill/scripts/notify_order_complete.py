#!/usr/bin/env python3
"""Poll master order status and send completion notification.

Usage:
  python3 scripts/notify_order_complete.py <master_order_id> [wait_seconds] [channel] [target] [lang]

Channels:
  - stdout (default): print message
  - webhook: POST JSON payload to target URL
  - command: execute NOTIFY_COMMAND with [target, message]
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import request
from urllib.error import URLError, HTTPError

TERMINAL_STATUSES = {"COMPLETED", "EXPIRED", "CANCELLED", "REJECTED"}
USAGE = "Usage: notify_order_complete.py <master_order_id> [wait_seconds] [channel] [target] [lang]"


def _parse_args(argv: list[str]) -> tuple[str, int, str, str, str]:
    if len(argv) >= 2 and argv[1] in {"-h", "--help"}:
        print(USAGE)
        print("Channels: stdout | webhook | command")
        print("Languages: zh | en")
        raise SystemExit(0)
    if len(argv) < 2:
        raise ValueError(USAGE)
    master_order_id = argv[1]
    wait_seconds = int(argv[2]) if len(argv) > 2 else 300
    channel = argv[3] if len(argv) > 3 else "stdout"
    target = argv[4] if len(argv) > 4 else "-"
    lang = argv[5] if len(argv) > 5 else "zh"
    if lang not in {"zh", "en"}:
        raise ValueError("lang must be zh or en")
    return master_order_id, wait_seconds, channel, target, lang


def _detail_script_path() -> Path:
    env_path = os.environ.get("DETAIL_SCRIPT")
    if env_path:
        return Path(env_path)
    return Path(__file__).resolve().parent / "get_master_order_detail.py"


def _python_bin() -> str:
    return os.environ.get("PYTHON_BIN", sys.executable or "python3")


def _fetch_detail(master_order_id: str) -> tuple[Optional[Dict[str, Any]], str]:
    cmd = [_python_bin(), str(_detail_script_path()), "--master-order-id", master_order_id]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    raw = (proc.stdout or "").strip()
    if proc.returncode != 0:
        err = (proc.stderr or "").strip()
        return None, err or raw or f"command failed: {' '.join(cmd)}"
    try:
        return json.loads(raw), raw
    except json.JSONDecodeError:
        return None, raw


def _format_result(data: Dict[str, Any], lang: str) -> str:
    mo = data.get("masterOrder") or {}
    if not mo:
        return "Query failed: missing masterOrder" if lang == "en" else "查询失败: 返回中缺少 masterOrder"

    maker_rate_raw = mo.get("makerRate", 0)
    try:
        maker_rate_pct = round(float(maker_rate_raw or 0) * 100, 1)
    except (TypeError, ValueError):
        maker_rate_pct = 0.0

    side = mo.get("side", "")
    if lang == "en":
        side_text = "Buy" if side == "buy" else "Sell"
        reason = f"\nReason: {mo.get('reason')}" if mo.get("reason") else ""
        return (
            "Order Completed\n"
            f"Master Order ID: {mo.get('masterOrderId')}\n"
            f"Direction: {side_text} {mo.get('symbol')}\n"
            f"Status: {mo.get('status')}\n"
            f"Filled Quantity: {mo.get('filledQuantity')}\n"
            f"Average Price: {mo.get('averagePrice')} USDT\n"
            f"Total Value: {mo.get('totalValue')} USDT\n"
            f"Maker Rate: {maker_rate_pct}%\n"
            f"Completion: {mo.get('completionProgress')}%{reason}"
        )

    side_text = "买入" if side == "buy" else "卖出"
    reason = f"\n原因: {mo.get('reason')}" if mo.get("reason") else ""
    return (
        "订单执行完成\n"
        f"母单ID: {mo.get('masterOrderId')}\n"
        f"方向: {side_text} {mo.get('symbol')}\n"
        f"状态: {mo.get('status')}\n"
        f"成交数量: {mo.get('filledQuantity')}\n"
        f"均价: {mo.get('averagePrice')} USDT\n"
        f"总成交额: {mo.get('totalValue')} USDT\n"
        f"Maker Rate: {maker_rate_pct}%\n"
        f"完成进度: {mo.get('completionProgress')}%{reason}"
    )


def _send_stdout(message: str) -> None:
    print(message)


def _send_webhook(target: str, master_order_id: str, message: str) -> None:
    if not target or target == "-":
        raise ValueError("webhook channel requires target URL")
    payload = json.dumps({"message": message, "masterOrderId": master_order_id}).encode("utf-8")
    req = request.Request(target, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with request.urlopen(req, timeout=15) as resp:
            if resp.status >= 400:
                raise RuntimeError(f"webhook returned status {resp.status}")
    except (HTTPError, URLError, TimeoutError) as e:
        raise RuntimeError(f"webhook request failed: {e}")


def _send_command(target: str, message: str) -> None:
    notify_cmd = os.environ.get("NOTIFY_COMMAND")
    if not notify_cmd:
        raise ValueError("NOTIFY_COMMAND not set for command channel")
    proc = subprocess.run([notify_cmd, target, message], capture_output=True, text=True)
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"command notify failed: {err}")


def _send(channel: str, target: str, master_order_id: str, message: str) -> None:
    if channel == "stdout":
        _send_stdout(message)
        return
    if channel == "webhook":
        _send_webhook(target, master_order_id, message)
        return
    if channel == "command":
        _send_command(target, message)
        return
    raise ValueError(f"unknown channel: {channel}")


def main(argv: list[str]) -> int:
    try:
        master_order_id, wait_seconds, channel, target, lang = _parse_args(argv)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    poll_interval = int(os.environ.get("POLL_INTERVAL", "15"))
    elapsed = 0

    while elapsed < wait_seconds + 60:
        time.sleep(poll_interval)
        elapsed += poll_interval

        data, raw_or_err = _fetch_detail(master_order_id)
        if not data:
            # keep polling; if still invalid at timeout we'll send final failure
            continue

        status = (data.get("masterOrder") or {}).get("status")
        if status in TERMINAL_STATUSES:
            message = _format_result(data, lang)
            try:
                _send(channel, target, master_order_id, message)
            except Exception as e:
                print(f"notification failed: {e}", file=sys.stderr)
                _send_stdout(message)
            return 0

    data, raw_or_err = _fetch_detail(master_order_id)
    if data:
        message = _format_result(data, lang)
    else:
        message = ("Query failed: " if lang == "en" else "查询失败: ") + raw_or_err

    try:
        _send(channel, target, master_order_id, message)
    except Exception as e:
        print(f"notification failed: {e}", file=sys.stderr)
        _send_stdout(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
