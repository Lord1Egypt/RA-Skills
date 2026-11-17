#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 Chatbox 生成「算力集市 a7w」的一键导入配置（JSON + chatbox:// 深链）。

安全约定：生成的配置与深链**一律不含 API Key**——它们可能被分享或转发，
携带可复用凭证会造成泄露。Key 由用户在 Chatbox 界面里手动填写一次。

Chatbox ≥ 1.15.1 支持导入第三方提供方配置，格式见官方文档：
  https://docs.chatboxai.app/en/guides/providers/import-config

关键点（已实测）：Chatbox 的 apiPath 默认 `/v1/chat/completions`，
所以 apiHost 必须填到 `https://api.a7w.cn/api`。
填成 `https://api.a7w.cn/api/v1` 会双拼成 /api/v1/v1/chat/completions → 404。

只读调用 /v1/models 拉真实模型清单，不产生对话费用。"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_APIHOST = "https://api.a7w.cn/api"
API_PATH = "/v1/chat/completions"

# 推荐默认模型（按用途挑，避免把 58 个文本模型全塞进去）
CURATED = [
    ("DeepSeek-V4-Flash", "日常对话 · 快 · 便宜"),
    ("DeepSeek-V4-Pro", "复杂推理 · 长文"),
    ("Qwen3.6-Plus", "综合能力强 · 支持视觉"),
    ("Qwen3-Coder-Next", "写代码"),
    ("GLM-5.2", "中文场景"),
    ("Kimi-K2.6", "长上下文"),
    ("ERNIE-5.0-Thinking", "深度推理"),
    ("gpt-5.6-sol", "国际模型对照"),
]


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


def fetch_models(api_host, key, timeout=45):
    """拉取真实模型清单。api_host 需为 .../api 形式。"""
    url = api_host.rstrip("/") + "/v1/models"
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", "Bearer " + key)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read().decode("utf-8"))
    return d.get("data") or d.get("models") or []


def to_model_info(m, note=""):
    """把网关的模型对象映射成 Chatbox 的 ModelInfo。"""
    caps = []
    if m.get("supports_vision"):
        caps.append("vision")
    if m.get("supports_reasoning"):
        caps.append("reasoning")
    nickname = m.get("model_name") or m.get("model_code") or m.get("id")
    if note:
        nickname = "%s ｜ %s" % (nickname, note)
    info = {
        "modelId": m.get("model_code") or m.get("id"),
        "nickname": nickname,
        "type": "chat",
    }
    if caps:
        info["capabilities"] = caps
    mt = m.get("max_tokens")
    if isinstance(mt, int) and mt > 1:
        info["maxOutput"] = mt
    return info


def pick_models(api_models, use_all=False, limit=None):
    """默认走精选清单；use_all=True 时纳入全部「同步文本」模型。"""
    by_code = {m.get("model_code") or m.get("id"): m for m in api_models}
    out, missing = [], []

    if use_all:
        for m in api_models:
            if m.get("type_code") != "text" or m.get("call_type") == 2:
                continue
            out.append(to_model_info(m))
    else:
        for code, note in CURATED:
            m = by_code.get(code)
            if m:
                out.append(to_model_info(m, note))
            else:
                missing.append(code)
        # 精选清单一个都没命中时，退回全部文本模型，避免生成空配置
        if not out:
            for m in api_models:
                if m.get("type_code") == "text" and m.get("call_type") != 2:
                    out.append(to_model_info(m))
    if limit:
        out = out[:limit]
    return out, missing


def build_provider_config(models, api_host=DEFAULT_APIHOST, api_path=API_PATH):
    cfg = {
        "id": "a7w",
        "name": "算力集市 a7w",
        "type": "openai",
        "iconUrl": "https://api.a7w.cn/favicon.ico",
        "urls": {
            "website": "https://api.a7w.cn/",
            "getApiKey": "https://api.a7w.cn/user-center.html",
            "docs": "https://api.a7w.cn/docs.html",
        },
        "settings": {
            "apiHost": api_host,
            "apiPath": api_path,
        },
    }
    # 注意：**绝不把 API Key 写进配置**。生成的配置与深链可能被分享/转发，
    # 一旦含可复用 Key 就会造成凭证泄露（安全扫描已就此告警）。
    # Key 由用户在 Chatbox 界面里手动填写一次即可。
    cfg["settings"]["models"] = models
    return cfg


def to_deep_link(config):
    """生成 chatbox:// 导入深链。

    深链会被打开、转发、留在浏览器历史里，因此**必须不含任何密钥**。
    这里做一次硬校验：一旦发现配置里带 Key，直接拒绝生成。
    """
    settings = (config or {}).get("settings") or {}
    if settings.get("apiKey") or settings.get("api_key"):
        raise ValueError("拒绝生成含 API Key 的深链：深链可能被转发/留存，会泄露可复用凭证。"
                         "请先移除 apiKey，让用户在 Chatbox 界面内手动填写。")
    raw = json.dumps(config, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return "chatbox://provider/import?config=" + base64.b64encode(raw).decode("ascii")


def main():
    ap = argparse.ArgumentParser(description="生成 Chatbox 一键导入配置")
    ap.add_argument("--api-host", default=DEFAULT_APIHOST)
    ap.add_argument("--all", action="store_true", help="纳入全部同步文本模型（默认只给精选）")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--out", default=None, help="把 JSON 写到文件")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    key = load_key()
    if not key:
        print("未找到 API Key：请设置 A7W_API_KEY 或先跑 one-key-ai-gateway 的 login", file=sys.stderr)
        return 2

    try:
        api_models = fetch_models(args.api_host, key)
    except urllib.error.HTTPError as e:
        print("拉取模型失败 HTTP %s —— 确认 apiHost 是 %s（不是 .../api/v1）" % (e.code, DEFAULT_APIHOST),
              file=sys.stderr)
        return 1

    models, missing = pick_models(api_models, use_all=args.all, limit=args.limit)
    cfg = build_provider_config(models, args.api_host)
    link = to_deep_link(cfg)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    if args.json:
        print(json.dumps({"config": cfg, "deepLink": link,
                          "modelCount": len(models), "missingCurated": missing},
                         ensure_ascii=False, indent=2))
    else:
        print("apiHost : %s" % args.api_host)
        print("apiPath : %s" % API_PATH)
        print("模型数  : %d（网关共 %d 个模型）" % (len(models), len(api_models)))
        if missing:
            print("精选未命中（已跳过）: %s" % ", ".join(missing))
        if args.out:
            print("已写入  : %s" % args.out)
        print("\n[!] 导入后请用你自己的 API Key（在 api.a7w.cn 申请）；")
        print("    本工具生成的配置与深链不含任何 Key。")
        print("\n--- 深链（浏览器/聊天里点开即可导入）---")
        print(link[:300] + ("…（已截断，完整内容见 --json 或 --out）" if len(link) > 300 else ""))
        print("\n--- 配置 JSON ---")
        print(json.dumps(cfg, ensure_ascii=False, indent=2)[:1500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
