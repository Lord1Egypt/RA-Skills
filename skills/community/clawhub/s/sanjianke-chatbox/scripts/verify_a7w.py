#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 Chatbox 接入算力集市（api.a7w.cn）所依赖的 HTTP 契约。

Chatbox 这类 OpenAI 兼容客户端的实际依赖只有 4 条：
  1. GET  {apiHost}/v1/models              模型列表（导入配置 / 自动发现用）
  2. POST {apiHost}/v1/chat/completions    非流式对话
  3. POST {apiHost}/v1/chat/completions    流式对话（SSE，Chatbox 默认开流式）
  4. 无 Key 时应被拒（验证鉴权确实生效）

只读 + 极小额度调用（max_tokens 很小），不写入任何文件。
Key 从 ~/.a7w/config.json 或环境变量 A7W_API_KEY 读取，不内嵌。"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

DEFAULT_APIHOST = "https://api.a7w.cn/api"
DEFAULT_MODEL = "DeepSeek-V4-Flash"


def load_key():
    k = os.environ.get("A7W_API_KEY")
    if k:
        return k
    p = os.path.join(os.path.expanduser("~"), ".a7w", "config.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
        for name in ("key", "api_key", "token", "apikey", "apiKey"):
            if d.get(name):
                return d[name]
    return None


def call(url, key=None, body=None, method="POST", stream=False, timeout=90):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if key:
        req.add_header("Authorization", "Bearer " + key)
    if stream:
        req.add_header("Accept", "text/event-stream")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), r.headers.get("Content-Type", ""), time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers.get("Content-Type", ""), time.time() - t0
    except Exception as e:
        return -1, ("EXC %r" % (e,)).encode(), "", time.time() - t0


def run(api_host, api_key, model):
    base = api_host.rstrip("/")
    res = []

    def add(name, ok, detail):
        res.append({"name": name, "ok": bool(ok), "detail": detail})

    # 1) 模型列表
    code, raw, ctype, dt = call(base + "/v1/models", api_key, method="GET")
    n = "?"
    try:
        j = json.loads(raw.decode("utf-8", "replace"))
        arr = j.get("data") or j.get("models") or []
        n = len(arr) if isinstance(arr, list) else j.get("raw_count", "?")
    except Exception:
        pass
    add("模型列表 GET /v1/models", code == 200,
        "HTTP %s (%.2fs) 解析到 %s 个模型" % (code, dt, n))

    # 2) 非流式
    body = {"model": model, "messages": [{"role": "user", "content": "只回复两个字：可用"}],
            "max_tokens": 64, "stream": False}
    code, raw, ctype, dt = call(base + "/v1/chat/completions", api_key, body)
    txt = raw.decode("utf-8", "replace")
    content, usage = "", None
    try:
        j = json.loads(txt)
        ch = (j.get("choices") or [{}])[0]
        content = (ch.get("message") or {}).get("content") or ""
        usage = j.get("usage")
    except Exception as e:
        content = "(解析失败 %s)" % e
    add("非流式 POST /v1/chat/completions", code == 200 and bool(content),
        "HTTP %s (%.2fs) 回复=%r usage=%s" % (code, dt, content[:40],
                                             json.dumps(usage, ensure_ascii=False) if usage else "无"))

    # 3) 流式 SSE
    body = {"model": model, "messages": [{"role": "user", "content": "从 1 数到 5"}],
            "max_tokens": 80, "stream": True}
    code, raw, ctype, dt = call(base + "/v1/chat/completions", api_key, body, stream=True)
    txt = raw.decode("utf-8", "replace")
    chunks = [l for l in txt.split("\n") if l.startswith("data:")]
    done = any("[DONE]" in l for l in chunks)
    add("流式 POST stream=true (SSE)", code == 200 and len(chunks) > 1 and done,
        "HTTP %s (%.2fs) %d 个 data 块，以 [DONE] 结束=%s" % (code, dt, len(chunks), done))

    # 4) 鉴权
    code, _, _, _ = call(base + "/v1/chat/completions", None,
                         {"model": model, "messages": [{"role": "user", "content": "hi"}]})
    add("无 Key 应被拒（鉴权生效）", code in (401, 403), "HTTP %s（期望 401/403）" % code)

    return res


def main():
    ap = argparse.ArgumentParser(description="验证 Chatbox ↔ api.a7w.cn 契约")
    ap.add_argument("--api-host", default=DEFAULT_APIHOST,
                    help="Chatbox 里填的 API Host，默认 %s" % DEFAULT_APIHOST)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    key = load_key()
    if not key:
        msg = "未找到 API Key：请设置环境变量 A7W_API_KEY，或先运行 one-key-ai-gateway 的 login"
        if args.json:
            print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
        else:
            print("[FAIL] " + msg)
        return 2

    res = run(args.api_host, key, args.model)
    passed = sum(1 for r in res if r["ok"])
    if args.json:
        print(json.dumps({"apiHost": args.api_host, "model": args.model,
                          "passed": passed, "total": len(res),
                          "ok": passed == len(res), "checks": res}, ensure_ascii=False, indent=2))
    else:
        print("目标 API Host: %s" % args.api_host)
        print("测试模型     : %s\n" % args.model)
        for r in res:
            print("[%s] %s\n      %s" % ("PASS" if r["ok"] else "FAIL", r["name"], r["detail"]))
        print("\n结果: %d/%d 通过" % (passed, len(res)))
        if passed == len(res):
            print("=> Chatbox 可以正常使用该网关。API Host 就这么填：%s" % args.api_host)
    return 0 if passed == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
