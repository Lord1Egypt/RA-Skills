#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会话回调（Session Callback）— 向 WorkBuddy 指定会话注入消息并唤醒其 agent

用法:
  python callback.py <session_id> "要注入的消息" [--workdir <path>] [--endpoint <url>]

流程（全部 loopback 免认证）:
  1. 发现目标会话 endpoint（按 lastHeartbeat 取最新，或 --endpoint 指定）
  2. POST /api/v1/acp/connect      → {connectionId, sessionToken}
  3. POST /api/v1/acp initialize   → capabilities（loadSession: true）
  4. POST /api/v1/acp session/load → 加载目标会话（绑定后收实时事件）
  5. POST /api/v1/acp session/prompt → 注入消息（转 user 消息，agent 自动处理）

验证:
  注入后转录落盘 projects/<workdir>/<sessionId>*.jsonl
  role=user = 注入消息, role=assistant = 目标 agent 响应
"""

import argparse
import glob
import json
import os
import sys
import time
import urllib.error
import urllib.request


def read_endpoint(session_id):
    """从 ~/.workbuddy/sessions/*.json 发现 endpoint：按 lastHeartbeat 排序后逐个探测连通性，取第一个活的"""
    sessions_dir = os.path.expanduser("~/.workbuddy/sessions")
    candidates = []
    for f in glob.glob(os.path.join(sessions_dir, "*.json")):
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if data.get("sessionId") == session_id and data.get("endpoint"):
                ep = data["endpoint"]
                if not ep.startswith("http"):
                    ep = f"http://{ep}"
                candidates.append((data.get("lastHeartbeat", 0), ep))
        except Exception:
            continue
    if not candidates:
        return None
    # 按心跳降序，逐个探测连通性（注册表可能有死进程残留）
    candidates.sort(key=lambda x: x[0], reverse=True)
    for hb, ep in candidates:
        try:
            req = urllib.request.Request(ep + "/api/v1/auth/status",
                                         headers={"X-CodeBuddy-Request": "1"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                if resp.status == 200:
                    return ep
        except Exception:
            continue  # 端口拒连/超时 = 死进程，试下一个
    return None


def post_json(endpoint, path, payload, headers=None):
    url = f"{endpoint}{path}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return -1, str(e)


def sse_send(endpoint, method, params, headers=None):
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000),
        "method": method,
        "params": params,
    }
    status, body = post_json(endpoint, "/api/v1/acp", payload, headers)
    events = []
    if body:
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                try:
                    events.append(json.loads(line[5:].strip()))
                except Exception:
                    pass
    return status, events


def main():
    ap = argparse.ArgumentParser(description="会话回调（Session Callback）")
    ap.add_argument("session_id", help="目标会话 ID（UUID，从 app/sessions.json 获取）")
    ap.add_argument("message", help="要注入的消息文本")
    ap.add_argument("--workdir", default=os.getcwd(), help="目标会话工作目录")
    ap.add_argument("--endpoint", default=None, help="手动指定 endpoint（默认按心跳自动发现）")
    args = ap.parse_args()

    endpoint = args.endpoint or read_endpoint(args.session_id)
    if not endpoint:
        print(f"[ERR] 会话 {args.session_id} 无可用 endpoint（进程可能未激活），请先打开该会话窗口")
        sys.exit(1)
    print(f"[OK] endpoint: {endpoint}")

    # 1. connect
    status, body = post_json(endpoint, "/api/v1/acp/connect", {})
    if status != 200:
        print(f"[ERR] connect 失败: {body[:200]}")
        sys.exit(1)
    try:
        conn = json.loads(body)
        cid, tok = conn["connectionId"], conn["sessionToken"]
    except Exception as e:
        print(f"[ERR] connect 响应解析失败: {body[:200]}")
        sys.exit(1)
    print(f"[1/4] connect OK: {cid[:12]}")

    hdrs = {
        "Accept": "application/json, text/event-stream",
        "acp-connection-id": cid,
        "acp-session-token": tok,
    }

    # 2. initialize
    status, events = sse_send(endpoint, "initialize", {"protocolVersion": 1, "clientCapabilities": {}}, hdrs)
    caps = events[0].get("result", {}).get("agentCapabilities", {}) if events else {}
    print(f"[2/4] initialize: loadSession={caps.get('loadSession')}")

    # 3. session/load
    status, events = sse_send(endpoint, "session/load",
                              {"sessionId": args.session_id, "cwd": args.workdir, "mcpServers": []}, hdrs)
    print(f"[3/4] session/load: {status}")

    # 4. session/prompt（注入）
    status, events = sse_send(endpoint, "session/prompt", {
        "sessionId": args.session_id,
        "cwd": args.workdir,
        "prompt": [{"type": "text", "text": args.message}],
        "_meta": {"codebuddy.ai/mode": "ask"},
    }, hdrs)
    print(f"[4/4] session/prompt: {status}")
    for ev in events:
        upd = ev.get("params", {}).get("update", {})
        if upd.get("sessionUpdate") == "usage_update":
            meta = upd.get("_meta", {})
            usage = meta.get("usage", {})
            print(f"      usage_update: prompt_tokens={usage.get('prompt_tokens')} (=目标会话完整上下文)")
    print("[DONE] 回调注入完成，验证: projects/<workdir>/<sessionId>*.jsonl 落盘")


if __name__ == "__main__":
    main()
