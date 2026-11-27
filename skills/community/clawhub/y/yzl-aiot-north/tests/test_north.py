#!/usr/bin/env python3
"""北向离线自测：起本地 mock，跑 lib/north_client.py 的所有接口方法。

运行：python tests/test_north.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
sys.path.insert(0, HERE)

import mock_north  # noqa: E402
from north_client import NorthClient, NorthError  # noqa: E402

PASS = 0
FAIL = 0


def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  ✅", name)
    else:
        FAIL += 1
        print("  ❌", name, extra)


def main():
    srv, state = mock_north.start(18081)
    base = "http://127.0.0.1:18081"
    try:
        # 1) 无 token，只有账号密码：首次 401 → 自动登录 → 重试成功
        c = NorthClient(base_url=base, account="tester", password="pw")
        data = c.list_devices(max_results=5)
        check("登录后设备列表", len(data.get("items", [])) == 1)
        check("自动带上 Bearer", any(r["auth"] for r in state.requests if r["path"] == "/open/device/list"))
        check("MaxResultCount 参数", any(r["query"].get("MaxResultCount") == "5" for r in state.requests))
        check("默认脱敏 password", data["items"][0]["password"] == "***")

        check("profile", c.profile().get("id") == "u1")
        check("account", c.account_summary().get("devices") == 1)
        check("device detail", c.get_device("DEV-1")["id"] == "DEV-1")
        check("telemetry", c.telemetry("DEV-1")["values"]["wd"] == "25.3")
        check("history", "items" in c.history("DEV-1", limit=5))
        check("aggregate", "items" in c.aggregate("DEV-1", ["wd"], "2026-01-01 00:00:00",
                                                  "2026-01-02 00:00:00", "1h"))
        check("backfill-logs", "items" in c.backfill_logs("DEV-1"))
        check("device stats", c.device_stats()["online"] == 1)
        check("send command", c.send_command("DEV-1", "set", ["sw", "1"])["tra"] == "tra-1")
        body = [r for r in state.requests if r["path"].endswith("/command")][0]["body"]
        check("命令参数含设备ID前缀", body["args"] == ["DEV-1", "sw", "1"])
        check("commands list", "items" in c.list_commands(device_id="DEV-1"))
        check("command detail", c.get_command("CMD-1")["status"] == "succeeded")
        check("alarms", "items" in c.list_alarms())
        check("products", c.list_products()["items"][0]["id"] == "RSTICQ")
        check("find_product", c.find_product("RSTICQ")["metrics"][0]["key"] == "in1")
        check("gateway ports", c.gateway_ports()["tcp"] == [41032])
        check("update_metric", c.update_metric("RSTICQ", "in1", access="rw")["after"]["access"] == "rw")
        check("metrics-config", c.update_metrics_config("RSTICQ", control={"x": 1}).get("ok") is True)
        check("clean_metrics", c.clean_metrics("RSTICQ")["removed"] == 0)

        # 2) 429 → NorthError(429)
        try:
            c.list_alarms(status="ratelimit")
            check("429 抛出错误", False)
        except NorthError as e:
            check("429 抛出错误", e.code == 429)

        # 3) API Key 头
        c2 = NorthClient(base_url=base, api_key="KEY-1")
        c2.list_alarms()
        check("X-API-Key 头", any(r["api_key"] == "KEY-1" for r in state.requests))
    finally:
        srv.shutdown()

    print("\n结果: %d passed, %d failed" % (PASS, FAIL))
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
