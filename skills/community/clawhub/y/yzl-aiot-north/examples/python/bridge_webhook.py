#!/usr/bin/env python3
"""北向示例（Python）：轮询设备最新值，变化时推 Webhook（带 HMAC 签名）。

不依赖第三方包（技能自带 lib/north_client.py）。

运行：
    set AIOT_ACCOUNT=wx_xxx
    set AIOT_PASSWORD=******
    set AIOT_DEVICE=DEV-1
    set AIOT_WEBHOOK_URL=https://app.example.com/aiot/events
    python bridge_webhook.py
"""
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))

from north_client import NorthClient

WEBHOOK_URL = os.environ.get("AIOT_WEBHOOK_URL", "")
SECRET = os.environ.get("AIOT_WEBHOOK_SECRET", "")
DEVICE = os.environ.get("AIOT_DEVICE", "")
INTERVAL = float(os.environ.get("AIOT_POLL_INTERVAL", "5"))


def post_webhook(payload):
    if not WEBHOOK_URL:
        return
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json", "X-AIoT-Event": "telemetry"}
    if SECRET:
        headers["X-AIoT-Signature"] = "sha256=" + hmac.new(
            SECRET.encode("utf-8"), raw, hashlib.sha256).hexdigest()
    req = urllib.request.Request(WEBHOOK_URL, data=raw, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status


def main():
    if not DEVICE:
        print("请设置 AIOT_DEVICE")
        return 2
    c = NorthClient.from_env()
    last = None
    seq = 0
    print("轮询 %s，每 %.0fs 一次；Ctrl+C 退出" % (DEVICE, INTERVAL))
    while True:
        data = c.telemetry(DEVICE)
        values = data.get("values") or data.get("data") or data
        if values != last:
            seq += 1
            payload = {"seq": seq, "ts": int(time.time()), "deviceId": DEVICE,
                       "values": values, "online": data.get("online")}
            print("变化:", json.dumps(payload, ensure_ascii=False))
            post_webhook(payload)
            last = values
        time.sleep(INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n退出")
