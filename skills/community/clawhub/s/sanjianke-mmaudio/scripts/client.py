#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a7w 插件市场 · 通用客户端。

一个零依赖的命令行工具，让 Skill 能调用 a7w 插件市场里的任何插件。

设计要点
    · 只依赖 Python 标准库（urllib），无第三方包
    · **不内嵌任何密钥**——key 由使用者自己提供，存在本机
    · 凭据读取顺序：--key 参数 → 环境变量 → 本机配置文件
    · 输出 JSON 到 stdout，便于 Agent 解析；人类可读信息走 stderr

配置
    client.py login --key sk-xxxx        # 写入 ~/.a7w/config.json（权限 600）
    export A7W_API_KEY=sk-xxxx        # 或用环境变量（优先级更高）

用法
    client.py whoami                     # 验证 key，看账号与余额
    client.py apps                       # 列出所有可用插件
    client.py schema <app>               # 看某个插件有哪些 API、参数是什么
    client.py call <app> <api> --json '{...}'
    client.py task <task_id>             # 查任务状态
    client.py points                     # 查余额

异步任务
    大部分插件是异步的：提交后返回 task_id，需要轮询到 completed。
    `call` 默认等到完成再返回；加 --no-wait 则立即返回 task_id。
"""

import argparse
import json
import os
import stat
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_HOST = "https://api.a7w.cn"
CONFIG_PATH = Path.home() / ".a7w" / "config.json"
ENV_KEY = "A7W_API_KEY"
ENV_HOST = "A7W_HOST"

TERMINAL_STATES = ("completed", "failed", "error", "cancelled")
POLL_INTERVAL = 6          # 秒
POLL_TIMEOUT = 1800        # 秒（30 分钟）


# ---------------------------------------------------------------- 配置

def load_config():
    if not CONFIG_PATH.is_file():
        return {}
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_config(key, host):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = load_config()
    data["key"] = key
    data["host"] = host
    CONFIG_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        CONFIG_PATH.chmod(stat.S_IRUSR | stat.S_IWUSR)   # 600
    except OSError:
        pass
    return CONFIG_PATH


def resolve(args):
    """返回 (key, host)；key 为空则报错退出。"""
    cfg = load_config()
    key = getattr(args, "key", None) or os.environ.get(ENV_KEY) or cfg.get("key")
    host = (getattr(args, "host", None) or os.environ.get(ENV_HOST)
            or cfg.get("host") or DEFAULT_HOST)
    if not key:
        die("未配置 API Key。\n"
            "  · 先执行：client.py login --key sk-xxxx\n"
            "  · 或设置环境变量 {}={}".format(ENV_KEY, "sk-xxxx"))
    return key.rstrip("/") and key.strip(), host.rstrip("/")


def die(msg, code=2):
    print(msg, file=sys.stderr)
    sys.exit(code)


def info(msg):
    print(msg, file=sys.stderr)


def emit(obj):
    json.dump(obj, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


# ---------------------------------------------------------------- 请求

def request(key, method, url, body=None, timeout=120):
    data = None
    headers = {"Authorization": "Bearer " + key, "Accept": "application/json"}
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            status = resp.status
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        status = exc.code
    except urllib.error.URLError as exc:
        die("网络错误：{}\n（请确认能访问 {}）".format(exc.reason, url), 3)

    try:
        payload = json.loads(raw)
    except ValueError:
        payload = {"raw": raw}

    if status == 401:
        die("鉴权失败（401）：API Key 无效或已过期。\n"
            "  重新执行：client.py login --key sk-xxxx", 4)
    if status >= 400:
        # 402 = 点数不足，是最常见的业务失败，单独提示
        msg = payload.get("msg") or payload.get("error") or raw[:200]
        if status == 402 or payload.get("code") == 402:
            die("点数不足：{}\n  请到 api.a7w.cn 对应账号充值后重试。".format(msg), 5)
        die("请求失败（HTTP {}）：{}".format(status, msg), 4)
    return payload


def unwrap(payload):
    """把 gate{code,msg,data} 拆成 (ok, data, msg)。"""
    code = payload.get("code")
    ok = code in (1, 200, "1", "200") or code is None
    return ok, payload.get("data"), payload.get("msg", "")


def request_soft(key, method, url, body=None, timeout=120):
    """同 request，但失败时返回 (payload, status) 而不退出——用于批量遍历。"""
    data = None
    headers = {"Authorization": "Bearer " + key, "Accept": "application/json"}
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", "replace")), resp.status
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        try:
            return json.loads(raw), exc.code
        except ValueError:
            return {"raw": raw}, exc.code
    except Exception as exc:                      # noqa: BLE001 - 批量场景要吞掉单个失败
        return {"error": str(exc)}, 0


def cmd_dump(args):
    """把所有插件的 schema 一次性导出到一个 JSON 文件。"""
    key, host = resolve(args)
    payload = request(key, "GET", host + "/api/v1/apps")
    ok, data, msg = unwrap(payload)
    apps = data if isinstance(data, list) else (data or {}).get("apps", data)
    if not isinstance(apps, list):
        emit({"ok": False, "message": "应用列表格式异常", "raw": data})
        return 4

    out = {"host": host, "count": len(apps), "apps": {}}
    for i, app in enumerate(apps, 1):
        code = (app.get("code") or app.get("app_code") or app.get("name")
                or app.get("id")) if isinstance(app, dict) else str(app)
        if not code:
            continue
        code = str(code)
        detail, status = request_soft(key, "GET", "{}/api/v1/apps/{}".format(host, code))
        _, d, m = unwrap(detail)
        out["apps"][code] = {
            "summary": app,
            "http_status": status,
            "schema": d if d is not None else detail,
            "message": m,
        }
        info("  [{}/{}] {} {}".format(i, len(apps), code, "✓" if status == 200 else "HTTP {}".format(status)))

    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    emit({"ok": True, "apps": len(out["apps"]), "out": str(Path(args.out).resolve())})
    return 0


# ---------------------------------------------------------------- 命令

def cmd_login(args):
    host = (args.host or DEFAULT_HOST).rstrip("/")
    info("验证 Key …")
    payload = request(args.key.strip(), "GET", host + "/api/v1/apps")
    ok, data, msg = unwrap(payload)
    if not ok:
        die("Key 验证失败：{}".format(msg or "未知错误"), 4)
    path = save_config(args.key.strip(), host)
    count = len(data) if isinstance(data, list) else "?"
    info("Key 有效，可用插件 {} 个".format(count))
    info("已保存到 {}".format(path))
    emit({"ok": True, "saved": str(path), "host": host, "app_count": count})


def cmd_whoami(args):
    """用 /api/v1/apps 验证 Key 是否有效（该网关未提供账号信息接口）。"""
    key, host = resolve(args)
    payload = request(key, "GET", host + "/api/v1/apps")
    ok, data, msg = unwrap(payload)
    apps = data if isinstance(data, list) else []
    emit({
        "ok": ok,
        "host": host,
        "key_prefix": key[:10] + "…",
        "app_count": len(apps),
        "apps": [{"code": a.get("code"), "name": a.get("name")} for a in apps if isinstance(a, dict)],
        "message": msg,
        "note": "该网关未公开账号/余额接口；点数不足时调用会返回 402 并附带当前余额。",
    })


def cmd_apps(args):
    key, host = resolve(args)
    payload = request(key, "GET", host + "/api/v1/apps")
    ok, data, msg = unwrap(payload)
    apps = data if isinstance(data, list) else (data or {}).get("apps", data)
    emit({"ok": ok, "count": len(apps) if isinstance(apps, list) else None,
          "apps": apps, "message": msg})


def cmd_schema(args):
    key, host = resolve(args)
    payload = request(key, "GET", "{}/api/v1/apps/{}".format(host, args.app))
    ok, data, msg = unwrap(payload)
    emit({"ok": ok, "app": args.app, "schema": data, "message": msg})


def cmd_task(args):
    key, host = resolve(args)
    payload = request(key, "GET", "{}/api/v1/tasks/{}".format(host, args.task_id))
    ok, data, msg = unwrap(payload)
    emit({"ok": ok, "task": data, "message": msg})


def cmd_points(args):
    """该网关未公开余额接口 → 用最近任务的用量汇总作为参考。"""
    key, host = resolve(args)
    payload = request(key, "GET", host + "/api/v1/tasks")
    ok, data, msg = unwrap(payload)
    tasks = []
    if isinstance(data, dict):
        tasks = data.get("lists") or data.get("items") or []
    elif isinstance(data, list):
        tasks = data
    total = 0.0
    for t in tasks:
        if isinstance(t, dict):
            try:
                total += float((t.get("usage") or {}).get("points_cost") or 0)
            except (TypeError, ValueError):
                pass
    emit({"ok": ok, "recent_task_count": len(tasks), "recent_points_cost": round(total, 2),
          "tasks": tasks[:20], "message": msg,
          "note": "网关未提供余额查询接口；点数不足时调用会返回 402 并附带当前余额。"})


def _parse_scalar(value):
    """把字符串按 JSON 解析；解析不出来就当普通字符串。"""
    v = value.strip()
    if v == "":
        return ""
    try:
        return json.loads(v)
    except ValueError:
        return value


def build_body(args):
    """构造请求体。支持三种方式，避免 shell 引号问题：

        --json '{...}'        直接传 JSON（注意 PowerShell 会吃掉内部双引号）
        --json-file body.json 从文件读（最稳，推荐复杂参数用这个）
        --param k=v           键值对，可重复；值会按 JSON 解析（--param n=3 → 数字）
        --json -              从标准输入读
    """
    sources = [bool(args.json), bool(args.json_file), bool(args.param)]
    if sum(sources) > 1:
        die("--json / --json-file / --param 三者只能用一种")

    if args.json_file:
        path = Path(args.json_file)
        if not path.is_file():
            die("找不到 JSON 文件：{}".format(path))
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            die("{} 不是合法 JSON：{}".format(path, exc))

    if args.json:
        raw = sys.stdin.read() if args.json.strip() == "-" else args.json
        try:
            return json.loads(raw)
        except ValueError as exc:
            die("JSON 解析失败：{}\n"
                "  提示：PowerShell / CMD 会吃掉 JSON 里的双引号。\n"
                "  改用 --json-file body.json，或用 --param k=v 逐个传。".format(exc))

    if args.param:
        body = {}
        for item in args.param:
            if "=" not in item:
                die("--param 需要 k=v 形式，收到：{}".format(item))
            key, _, value = item.partition("=")
            body[key.strip()] = _parse_scalar(value)
        return body

    return {}


def cmd_call(args):
    key, host = resolve(args)
    body = build_body(args)

    url = "{}/api/v1/apps/{}/{}".format(host, args.app, args.api)
    info("提交任务：POST {}/{}".format(args.app, args.api))
    payload = request(key, "POST", url, body=body)
    ok, data, msg = unwrap(payload)
    if not ok:
        emit({"ok": False, "stage": "submit", "message": msg, "raw": payload})
        return 4

    task_id = (data or {}).get("task_id")
    if not task_id:
        # 同步接口：直接返回结果
        emit({"ok": True, "mode": "sync", "result": data})
        return 0

    info("task_id = {}（预计消耗 {} 点）".format(task_id, (data or {}).get("frozen_points", "?")))
    if args.no_wait:
        emit({"ok": True, "mode": "async", "task_id": task_id, "submit": data})
        return 0

    # 轮询
    deadline = time.time() + (args.timeout or POLL_TIMEOUT)
    interval = args.interval or POLL_INTERVAL
    last = None
    while time.time() < deadline:
        time.sleep(interval)
        poll = request(key, "GET", "{}/api/v1/tasks/{}".format(host, task_id))
        pok, pdata, pmsg = unwrap(poll)
        status = (pdata or {}).get("status")
        if status != last:
            info("  状态：{}".format(status))
            last = status
        if status in TERMINAL_STATES:
            result = (pdata or {}).get("result") or {}
            inner = result.get("data") or {}
            emit({
                "ok": status == "completed",
                "mode": "async",
                "task_id": task_id,
                "status": status,
                "video_url": inner.get("videoUrl") or result.get("video_url") or "",
                "duration": inner.get("duration") or result.get("duration"),
                "width": inner.get("width"),
                "height": inner.get("height"),
                "points_cost": ((pdata or {}).get("usage") or {}).get("points_cost"),
                "error": (pdata or {}).get("error"),
                "task": pdata,
            })
            return 0 if status == "completed" else 6

    emit({"ok": False, "mode": "async", "task_id": task_id, "message": "轮询超时",
          "hint": "任务可能仍在跑，用 client.py task {} 继续查".format(task_id)})
    return 7


# ---------------------------------------------------------------- 入口

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="client.py",
        description="a7w 插件市场通用客户端（零依赖，不内嵌密钥）")
    parser.add_argument("--key", help="覆盖 API Key（默认读环境变量或本机配置）")
    parser.add_argument("--host", help="覆盖服务地址（默认 {}）".format(DEFAULT_HOST))

    # 让 --key / --host 在子命令前后都能写。用 SUPPRESS 做默认值，
    # 这样「没传」时不会把主解析器已设的值覆盖成 None。
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--key", default=argparse.SUPPRESS,
                        help="覆盖 API Key（同全局参数）")
    common.add_argument("--host", default=argparse.SUPPRESS,
                        help="覆盖服务地址（同全局参数）")

    sub = parser.add_subparsers(dest="cmd", required=True, metavar="<命令>")

    p = sub.add_parser("login", parents=[common], help="验证并保存 API Key 到本机")
    p.set_defaults(func=cmd_login)

    p = sub.add_parser("whoami", parents=[common], help="查看当前账号")
    p.set_defaults(func=cmd_whoami)

    p = sub.add_parser("points", parents=[common], help="查看余额")
    p.set_defaults(func=cmd_points)

    p = sub.add_parser("apps", parents=[common], help="列出所有可用插件")
    p.set_defaults(func=cmd_apps)

    p = sub.add_parser("dump", parents=[common], help="把所有插件的 schema 导出到一个 JSON 文件")
    p.add_argument("--out", default="a7w-apps-schema.json", help="输出文件路径")
    p.set_defaults(func=cmd_dump)

    p = sub.add_parser("schema", parents=[common], help="查看某插件的 API 列表与参数")
    p.add_argument("app", help="插件代码，如 smart_clip")
    p.set_defaults(func=cmd_schema)

    p = sub.add_parser("task", parents=[common], help="查询异步任务状态")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_task)

    p = sub.add_parser("call", parents=[common], help="调用插件的某个 API")
    p.add_argument("app", help="插件代码")
    p.add_argument("api", help="接口代码，如 realman_broadcast")
    p.add_argument("--json", help="请求体 JSON 字符串（'-' 表示从标准输入读）")
    p.add_argument("--json-file", help="从 JSON 文件读请求体（最稳，推荐）")
    p.add_argument("--param", action="append", help="键值对 k=v，可重复；值按 JSON 解析")
    p.add_argument("--no-wait", action="store_true", help="异步任务不等待，直接返回 task_id")
    p.add_argument("--interval", type=int, help="轮询间隔秒数（默认 {}）".format(POLL_INTERVAL))
    p.add_argument("--timeout", type=int, help="轮询超时秒数（默认 {}）".format(POLL_TIMEOUT))
    p.set_defaults(func=cmd_call)

    args = parser.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
