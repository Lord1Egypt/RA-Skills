#!/usr/bin/env python3
"""YZL-AIoT 北向命令行（yzl-aiot-north）v2.0.0

每个北向接口对应一个命令，底层用同目录 `lib/north_client.py`（标准库实现），
不依赖任何第三方包。

认证（环境变量，三选一）：
  AIOT_TOKEN / AIOT_API_KEY / AIOT_ACCOUNT + AIOT_PASSWORD
可选：
  AIOT_BASE_URL   默认 https://aiot.yzlkj.com
"""

import argparse
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "lib"))

from north_client import NorthClient, NorthError  # noqa: E402

LOCAL_VERSION = "2.0.0"
SKILL_SLUG = "yzl-aiot-north"
CLAWHUB_REGISTRY = "https://clawhub.ai"
VERSION_CACHE_FILE = os.path.join(HERE, ".version_cache.json")
VERSION_CACHE_TTL = 12 * 3600


def dump(data):
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def build_parser():
    p = argparse.ArgumentParser(prog="tool.py", description="YZL-AIoT 北向命令行")
    p.add_argument("--json", action="store_true", help="只输出 JSON（默认就是 JSON）")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami", help="当前用户 GET /auth/profile")
    sub.add_parser("account", help="账号概览 GET /open/account")
    sub.add_parser("ports", help="网关端口 GET /open/gateway/ports")

    d = sub.add_parser("devices", help="设备列表 GET /open/device/list")
    d.add_argument("--filter", default=None)
    d.add_argument("--group", default=None)
    d.add_argument("--online", action="store_true")
    d.add_argument("--limit", type=int, default=50)
    d.add_argument("--offset", type=int, default=0)
    d.add_argument("--secrets", action="store_true")

    g = sub.add_parser("device", help="设备详情 GET /open/device/{id}")
    g.add_argument("id")
    g.add_argument("--secrets", action="store_true")

    s = sub.add_parser("stats", help="设备统计 GET /open/device/stats")
    s.add_argument("--group", default=None)

    t = sub.add_parser("telemetry", help="最新值 GET /open/device/{id}/telemetry")
    t.add_argument("id")

    h = sub.add_parser("history", help="历史 GET /open/device/{id}/history")
    h.add_argument("id")
    h.add_argument("--keys", default=None)
    h.add_argument("--start", default=None)
    h.add_argument("--end", default=None)
    h.add_argument("--limit", type=int, default=None)

    a = sub.add_parser("aggregate", help="聚合 GET /open/device/{id}/aggregate")
    a.add_argument("id")
    a.add_argument("--keys", required=True)
    a.add_argument("--start", required=True)
    a.add_argument("--end", required=True)
    a.add_argument("--bucket", default="1h")

    b = sub.add_parser("backfill-logs", help="补传记录 GET /open/device/{id}/backfill-logs")
    b.add_argument("id")
    b.add_argument("--limit", type=int, default=10)

    c = sub.add_parser("command", help="下发指令 POST /open/device/{id}/command")
    c.add_argument("id")
    c.add_argument("action", choices=("set", "get"))
    c.add_argument("args", nargs="*")
    c.add_argument("--tra", default=None)

    cl = sub.add_parser("commands", help="指令列表 GET /open/command/list")
    cl.add_argument("--device", default=None)
    cl.add_argument("--status", default=None)
    cl.add_argument("--page", type=int, default=1)
    cl.add_argument("--page-size", type=int, default=20)

    cd = sub.add_parser("command-detail", help="指令详情 GET /open/command/{id}")
    cd.add_argument("id")

    al = sub.add_parser("alarms", help="告警列表 GET /open/alarm/list")
    al.add_argument("--status", default=None)
    al.add_argument("--page", type=int, default=1)
    al.add_argument("--page-size", type=int, default=20)

    pr = sub.add_parser("products", help="型号列表 GET /open/product/list")
    pr.add_argument("--id", default=None)

    m = sub.add_parser("metric", help="改单个测点 PATCH /open/product/{id}/metric/{key}")
    m.add_argument("product")
    m.add_argument("key")
    m.add_argument("--data-type", default=None, choices=("int", "decimal", "text", "enum"))
    m.add_argument("--access", default=None, choices=("rw", "r", "none"))
    m.add_argument("--label", default=None)
    m.add_argument("--unit", default=None)
    m.add_argument("--visible", default=None, choices=("true", "false"))

    mc = sub.add_parser("metrics-config", help="设施语义配置 PUT /open/product/{id}/metrics-config")
    mc.add_argument("product")
    mc.add_argument("--control", default=None, help="JSON 字符串")
    mc.add_argument("--compare", default=None, help="JSON 字符串")

    cm = sub.add_parser("clean-metrics", help="清理自动设施 POST /open/product/{id}/clean-metrics")
    cm.add_argument("product")
    cm.add_argument("--keys", default=None, help="逗号分隔")

    sub.add_parser("check-update", help="检查技能版本")
    sub.add_parser("version", help="显示版本")
    return p


def check_update():
    now = time.time()
    cache = None
    try:
        with open(VERSION_CACHE_FILE, encoding="utf-8") as f:
            cache = json.load(f)
    except Exception:
        pass
    if isinstance(cache, dict) and now - cache.get("cached_at", 0) < VERSION_CACHE_TTL:
        info = cache.get("result", {})
    else:
        info = {"local_version": LOCAL_VERSION, "latest_version": None, "error": None}
        try:
            req = urllib.request.Request("%s/api/v1/skills/%s" % (CLAWHUB_REGISTRY, SKILL_SLUG),
                                         headers={"User-Agent": "yzl-aiot-north/%s" % LOCAL_VERSION})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            info["latest_version"] = (data.get("latestVersion") or {}).get("version")
        except Exception as e:
            info["error"] = str(e)
        try:
            with open(VERSION_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump({"result": info, "cached_at": now}, f, ensure_ascii=False)
        except Exception:
            pass
    print("📡 %s：本地 v%s，远程 %s" % (SKILL_SLUG, LOCAL_VERSION,
                                   ("v" + info["latest_version"]) if info.get("latest_version") else "未发布/查询失败"))


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.cmd == "version":
        print("yzl-aiot-north v%s" % LOCAL_VERSION)
        return 0
    if args.cmd == "check-update":
        check_update()
        return 0

    client = NorthClient.from_env()
    if not (client.token or client.api_key or (client.account and client.password)):
        print("请设置 AIOT_TOKEN、AIOT_API_KEY 或 AIOT_ACCOUNT/AIOT_PASSWORD", file=sys.stderr)
        return 2

    try:
        if args.cmd == "whoami":
            dump(client.profile())
        elif args.cmd == "account":
            dump(client.account_summary())
        elif args.cmd == "ports":
            dump(client.gateway_ports())
        elif args.cmd == "devices":
            dump(client.list_devices(filter=args.filter, group_id=args.group,
                                     online=True if args.online else None,
                                     max_results=args.limit, offset=args.offset,
                                     include_secrets=args.secrets))
        elif args.cmd == "device":
            dump(client.get_device(args.id, include_secrets=args.secrets))
        elif args.cmd == "stats":
            dump(client.device_stats(args.group))
        elif args.cmd == "telemetry":
            dump(client.telemetry(args.id))
        elif args.cmd == "history":
            dump(client.history(args.id, keys=args.keys, start=args.start, end=args.end, limit=args.limit))
        elif args.cmd == "aggregate":
            dump(client.aggregate(args.id, args.keys, args.start, args.end, args.bucket))
        elif args.cmd == "backfill-logs":
            dump(client.backfill_logs(args.id, args.limit))
        elif args.cmd == "command":
            dump(client.send_command(args.id, args.action, args.args, tra=args.tra))
        elif args.cmd == "commands":
            dump(client.list_commands(device_id=args.device, status=args.status,
                                      page=args.page, page_size=args.page_size))
        elif args.cmd == "command-detail":
            dump(client.get_command(args.id))
        elif args.cmd == "alarms":
            dump(client.list_alarms(status=args.status, page=args.page, page_size=args.page_size))
        elif args.cmd == "products":
            data = client.find_product(args.id) if args.id else client.list_products()
            dump(data)
        elif args.cmd == "metric":
            dump(client.update_metric(args.product, args.key, data_type=args.data_type,
                                      access=args.access, label=args.label, unit=args.unit,
                                      visible=None if args.visible is None else args.visible == "true"))
        elif args.cmd == "metrics-config":
            dump(client.update_metrics_config(
                args.product,
                control=json.loads(args.control) if args.control else None,
                compare=json.loads(args.compare) if args.compare else None))
        elif args.cmd == "clean-metrics":
            dump(client.clean_metrics(args.product, args.keys.split(",") if args.keys else None))
        else:
            print("未知命令")
            return 2
    except NorthError as e:
        print("❌ %s (code=%s, HTTP=%s)" % (e, e.code, e.status), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
