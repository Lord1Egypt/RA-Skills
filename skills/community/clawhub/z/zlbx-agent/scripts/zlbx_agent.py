#!/usr/bin/env python3
"""知了商机大师开放平台 CLI（无第三方依赖，仅标准库）。

从环境变量读取凭证：
  ZLBX_AGENT_API_KEY  必填，形如 zlbx_agent_xxx
  ZLBX_AGENT_BASE     可选，默认 https://agent.zhiliaobiaoxun.com/openapi/v1

所有子命令输出 JSON。异步类（opp-trigger/task-run/bid-analyze）支持 --wait 轮询到完成。
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = os.getenv("ZLBX_AGENT_BASE", "https://agent.zhiliaobiaoxun.com/openapi/v1").rstrip("/")
KEY = os.getenv("ZLBX_AGENT_API_KEY", "")


def _die(msg: str, code: int = 1):
    print(json.dumps({"error": msg}, ensure_ascii=False), file=sys.stderr)
    sys.exit(code)


def _request(method: str, path: str, params: dict | None = None, body: dict | None = None):
    if not KEY:
        _die("未设置 ZLBX_AGENT_API_KEY 环境变量")
    url = f"{BASE}{path}"
    if params:
        clean = {k: v for k, v in params.items() if v is not None}
        if clean:
            url += "?" + urllib.parse.urlencode(clean)
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {KEY}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=310) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            err = json.loads(raw).get("error", {})
            _die(f"[{err.get('code', e.code)}] {err.get('message', raw)}", 2)
        except json.JSONDecodeError:
            _die(f"[{e.code}] {raw}", 2)
    except urllib.error.URLError as e:
        _die(f"网络错误：{e.reason}", 3)


def _out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _poll(fn, done, interval=3.0, timeout=600):
    """轮询 fn() 直到 done(result) 为真或超时；返回最后一次结果。"""
    deadline = time.time() + timeout
    result = fn()
    while not done(result) and time.time() < deadline:
        time.sleep(interval)
        result = fn()
    return result


def main():
    p = argparse.ArgumentParser(prog="zlbx_agent")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, **kw):
        return sub.add_parser(name, **kw)

    # 对话
    c = add("chat")
    c.add_argument("--message", required=True)
    c.add_argument("--session")
    add("conversations").add_argument("--page", type=int, default=1)
    add("messages").add_argument("--session", required=True)
    add("last-reply").add_argument("--session", required=True)
    # 商机
    add("opp-trigger").add_argument("--wait", action="store_true")
    add("opp-status").add_argument("--task-id", type=int, required=True)
    add("opp-list").add_argument("--date")
    # 跟进任务
    t = add("task-create")
    t.add_argument("--description", required=True)
    t.add_argument("--schedule")
    t.add_argument("--title")
    t.add_argument("--no-notify", action="store_true")
    add("task-list").add_argument("--status")
    add("task-latest-run").add_argument("--task-id", type=int, required=True)
    tr = add("task-run")
    tr.add_argument("--task-id", type=int, required=True)
    tr.add_argument("--wait", action="store_true")
    # 标讯
    bd = add("bid-detail")
    bd.add_argument("--bid-id", type=int, required=True)
    bd.add_argument("--bid-type", type=int)
    ba = add("bid-analyze")
    ba.add_argument("--bid-id", type=int, required=True)
    ba.add_argument("--bid-type", type=int)
    ba.add_argument("--wait", action="store_true")
    add("bid-analysis").add_argument("--bid-id", type=int, required=True)
    # 账户
    add("balance")

    a = p.parse_args()

    if a.cmd == "chat":
        _out(_request("POST", "/chat", body={"message": a.message, "session_uid": a.session, "stream": False}))
    elif a.cmd == "conversations":
        _out(_request("GET", "/chat/conversations", params={"page": a.page}))
    elif a.cmd == "messages":
        _out(_request("GET", f"/chat/conversations/{a.session}/messages"))
    elif a.cmd == "last-reply":
        _out(_request("GET", f"/chat/conversations/{a.session}/last-reply"))
    elif a.cmd == "opp-trigger":
        started = _request("POST", "/opportunities/runs")
        if not a.wait:
            _out(started)
        else:
            tid = started.get("task_id")
            _poll(lambda: _request("GET", f"/opportunities/runs/{tid}"),
                  lambda r: r and r.get("status") in ("done", "failed"))
            _out(_request("GET", "/opportunities"))
    elif a.cmd == "opp-status":
        _out(_request("GET", f"/opportunities/runs/{a.task_id}"))
    elif a.cmd == "opp-list":
        _out(_request("GET", "/opportunities", params={"task_date": a.date}))
    elif a.cmd == "task-create":
        body = {"description": a.description, "notify_enabled": not a.no_notify}
        if a.title:
            body["title"] = a.title
        if a.schedule:
            try:
                body["schedule"] = json.loads(a.schedule)
            except json.JSONDecodeError:
                _die("--schedule 必须是合法 JSON，例：'{\"kind\":\"daily\",\"hour\":8}'")
        _out(_request("POST", "/tasks", body=body))
    elif a.cmd == "task-list":
        _out(_request("GET", "/tasks", params={"status": a.status}))
    elif a.cmd == "task-latest-run":
        _out(_request("GET", f"/tasks/{a.task_id}/latest-run"))
    elif a.cmd == "task-run":
        started = _request("POST", f"/tasks/{a.task_id}/runs")
        if not a.wait:
            _out(started)
        else:
            rid = started.get("run_id")
            _out(_poll(lambda: _request("GET", f"/tasks/{a.task_id}/runs/{rid}"),
                       lambda r: r and r.get("status") in ("done", "failed")))
    elif a.cmd == "bid-detail":
        params = {"bid_type": a.bid_type} if a.bid_type is not None else None
        _out(_request("GET", f"/bids/{a.bid_id}", params=params))
    elif a.cmd == "bid-analyze":
        params = {"bid_type": a.bid_type} if a.bid_type is not None else None
        started = _request("POST", f"/bids/{a.bid_id}/analysis", params=params)
        if not a.wait:
            _out(started)
        else:
            _poll(lambda: _request("GET", f"/bids/{a.bid_id}/analysis"), lambda r: bool(r))
            _out(_request("GET", f"/bids/{a.bid_id}/analysis"))
    elif a.cmd == "bid-analysis":
        _out(_request("GET", f"/bids/{a.bid_id}/analysis"))
    elif a.cmd == "balance":
        _out(_request("GET", "/account/balance"))


if __name__ == "__main__":
    main()
