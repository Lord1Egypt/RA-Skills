#!/usr/bin/env python3
"""北向示例（Python）：设备列表 → 最新值 → 历史。

不依赖第三方包：直接用技能自带的 lib/north_client.py。

环境变量：AIOT_TOKEN 或 AIOT_ACCOUNT + AIOT_PASSWORD（也可用 AIOT_API_KEY）
运行：python quickstart.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))

from north_client import NorthClient, NorthError


def main():
    if not (os.environ.get("AIOT_TOKEN") or os.environ.get("AIOT_API_KEY")
            or (os.environ.get("AIOT_ACCOUNT") and os.environ.get("AIOT_PASSWORD"))):
        print("请先设置 AIOT_TOKEN、AIOT_API_KEY 或 AIOT_ACCOUNT/AIOT_PASSWORD")
        return 2

    c = NorthClient.from_env()
    try:
        print("whoami:", c.profile())
        devices = c.list_devices(max_results=10)
        items = devices.get("items", [])
        print("设备数:", len(items))
        if not items:
            return 0
        dev = items[0]
        print("第一个设备:", dev.get("id"), dev.get("name"))
        print("最新值:", json.dumps(c.telemetry(dev["id"]), ensure_ascii=False))
        hist = c.history(dev["id"], limit=20)
        print("历史:", json.dumps(hist, ensure_ascii=False)[:500])
    except NorthError as e:
        print("接口错误:", e, "code=", e.code)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
