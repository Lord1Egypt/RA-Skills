#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""api.a7w.cn（算力集市）· 统一网关零依赖客户端。

一个 Key 走通两条入口：
    模型网关  POST /api/v1/chat/completions          —— OpenAI 兼容，换 model 就是换模型
    应用任务  POST /api/v1/apps/{app}/{api}          —— 生成类应用，返回 task_id

设计要点
    · 只依赖 Python 标准库（urllib），无第三方包
    · **不内嵌任何密钥**——Key 由使用者自己提供，存本机或走环境变量
    · 只把请求发往 api.a7w.cn，不发往其他任何地址
    · 输出 JSON 到 stdout，便于 Agent 解析；人类可读信息走 stderr
    · 端点「文档有、实测不一定通」时按候选顺序探测，并如实报告哪个通了

配置
    client.py login --key sk-xxxx     # 写入 ~/.a7w/config.json（权限 600）
    export A7W_API_KEY=sk-xxxx        # 或用环境变量（优先级更高）

用法
    client.py whoami                  # 验证 Key
    client.py models [--filter 关键词]  # 列出可调用模型（自动试候选端点）
    client.py chat --model <名> --prompt "你好"
    client.py apps                    # 列出全部应用
    client.py schema <app>            # 看某应用有哪些接口、参数是什么、真实价多少
    client.py call <app> <api> --json-file body.json
    client.py task <task_id>          # 查异步任务
    client.py tasks                   # 列出最近任务
    client.py balance                 # 查点数余额（候选端点探测 + 任务用量回退）
    client.py pricing [--query k=v]   # 实时查询价格规则
    client.py openai-env              # 打印 OpenAI SDK 的 base_url / key 接法

异步任务
    生成类接口是任务制：提交后返回 task_id，需要轮询到 completed。
    `call` 默认等到终态再返回；加 --no-wait 则立刻返回 task_id。
    提交时会**预冻结点数**，完成后按实际用量多退少补——不要重复提交同一个任务。
"""

import argparse
import json
import os
import stat
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_HOST = "https://api.a7w.cn"
API_PREFIX = "/api/v1"
CONFIG_PATH = Path.home() / ".a7w" / "config.json"
ENV_KEY = "A7W_API_KEY"
ENV_HOST = "A7W_HOST"

TERMINAL_STATES = ("completed", "failed", "error", "cancelled")
POLL_INTERVAL = 6          # 秒
POLL_TIMEOUT = 1800        # 秒（30 分钟）

# 同一语义可能有多个端点，文档口径与实测口径未必一致 → 按序探测
MODELS_CANDIDATES = ["/api/v1/models", "/api/user_center/modelList?page_no=1"]
BALANCE_CANDIDATES = ["/api/v1/user/balance", "/api/v1/user/points", "/api/v1/me"]
APPS_CANDIDATES = ["/api/v1/apps", "/api/plugins"]


# ---------------------------------------------------------------- 基础工具

def die(msg, code=2):
    print(msg, file=sys.stderr)
    sys.exit(code)


def info(msg):
    print(msg, file=sys.stderr)


def emit(obj):
    json.dump(obj, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


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
    """返回 (key, host)。Key 优先级：--key > 环境变量 > 本机配置。"""
    cfg = load_config()
    key = (getattr(args, "key", None) or os.environ.get(ENV_KEY) or cfg.get("key") or "").strip()
    host = (getattr(args, "host", None) or os.environ.get(ENV_HOST)
            or cfg.get("host") or DEFAULT_HOST).rstrip("/")
    if not key:
        die("未配置 API Key。\n"
            "  · 先执行：client.py login --key sk-xxxx\n"
            "  · 或设置环境变量 {}=sk-xxxx".format(ENV_KEY))
    return key, host


# ---------------------------------------------------------------- 请求层

def raw_request(key, method, url, body=None, timeout=120):
    """发一次请求，返回 (status, payload_dict)。不退出，便于候选端点探测。"""
    data = None
    headers = {"Authorization": "Bearer " + key, "Accept": "application/json"}
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw, status = resp.read().decode("utf-8", "replace"), resp.status
    except urllib.error.HTTPError as exc:
        raw, status = exc.read().decode("utf-8", "replace"), exc.code
    except urllib.error.URLError as exc:
        return 0, {"_error": "网络错误：{}".format(exc.reason),
                   "_hint": "确认能访问 {}".format(url)}
    except Exception as exc:                                   # noqa: BLE001
        return 0, {"_error": "{}: {}".format(type(exc).__name__, exc)}
    try:
        return status, json.loads(raw)
    except ValueError:
        return status, {"_raw": raw[:2000]}


def unwrap(payload):
    """把网关的 {code,msg,data} 拆成 (ok, data, msg)。

    注意：**code 为 0 表示业务失败**（实测 POST 不存在的接口会返回
    HTTP 200 + {"code":0,"msg":"应用或 API 不可用或未配置价格"}）。
    所以 0 不能当作成功——HTTP 状态码在这里不足以判断成败。
    """
    if not isinstance(payload, dict):
        return False, None, "响应不是 JSON 对象"
    code = payload.get("code")
    ok = code in (1, 200, "1", "200") or code is None
    return ok, payload.get("data"), payload.get("msg", "")


def endpoint_usable(payload):
    """判断候选端点是否真的可用。

    有些端点（/api/v1/user/balance、/api/v1/pricing）直接返回**裸对象**，
    没有 code/msg/data 外壳——不能因为取不到 data 就当成不可用。
    """
    if not isinstance(payload, dict) or "_error" in payload or "_raw" in payload:
        return False
    code = payload.get("code")
    if code is None:
        return True
    return code in (1, 200, "1", "200")


def explain(status, payload):
    """把失败翻译成「人话 + 下一步」。"""
    code = payload.get("code") if isinstance(payload, dict) else None
    raw = ""
    if isinstance(payload, dict):
        r = payload.get("_raw")
        if isinstance(r, str):
            # 404 可能返回 HTML，压成一行再截断
            raw = " ".join(r.split())[:160]
    msg = ((payload.get("msg") or payload.get("message")
            or (payload.get("error") if isinstance(payload.get("error"), str) else None)
            or payload.get("_error") or raw or "") if isinstance(payload, dict) else "")
    table = {
        "invalid_request": "参数缺失或格式错误 → 用 `schema <app>` 核对参数名与必填项",
        "auth_failed": "API Key 缺失或无效 → 重新 login",
        "insufficient_points": "点数余额不足 → 去算力中心充值（错误里会写本次所需点数）",
        "key_quota_exceeded": "该 Key 的点数额度打满 → 去用户中心调高/重置 Key quota",
        "permission_denied": "该 Key 无权调用此模型/应用 → 检查是否已开通、Key 是否被限权",
        "not_found": "模型/应用/任务不存在 → 用 `apps` / `models` 拿真名（应用代码用下划线）",
        "queue_limit_exceeded": "排队任务已达上限 → 降并发，等队列消化后重试",
        "server_error": "服务异常 → 退避重试；仍失败换模型/线路",
    }
    hint = table.get(str(code), "")
    if status == 402 or code == 402:
        return "点数不足：{}　{}".format(msg or "余额不够", hint), 5
    if status == 401:
        return "鉴权失败（401）：Key 无效或已过期。\n  重新执行：client.py login --key sk-xxxx", 4
    if status >= 400:
        return "请求失败（HTTP {}）：{}　{}".format(status, msg, hint), 4
    return msg, 4


def request(key, method, url, body=None, timeout=120):
    """严格版：失败即退出。"""
    status, payload = raw_request(key, method, url, body, timeout)
    if status == 0:
        die(payload.get("_error", "网络错误") + "\n" + payload.get("_hint", ""), 3)
    if status >= 400:
        text, code = explain(status, payload)
        die(text, code)
    return payload


def probe(key, paths, host, timeout=30):
    """按候选顺序探测，返回第一个可用的 (path, status, payload, attempts)。"""
    attempts = []
    for p in paths:
        status, payload = raw_request(key, "GET", host + p, timeout=timeout)
        attempts.append({"path": p, "status": status})
        if status and status < 400 and endpoint_usable(payload):
            return p, status, payload, attempts
        info("  · {} -> HTTP {}（不可用，试下一个）".format(p, status or "无响应"))
    return None, None, None, attempts


# ---------------------------------------------------------------- 解析助手

def pick_list(data):
    """从各种包装里找出真正的列表。"""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in ("lists", "items", "list", "data", "rows", "records", "apps", "models"):
            v = data.get(k)
            if isinstance(v, list):
                return v
    return []


def name_of(item, keys=("code", "app", "app_code", "model", "model_name", "name", "id")):
    if not isinstance(item, dict):
        return str(item)
    for k in keys:
        if item.get(k):
            return str(item[k])
    return ""


def schema_props(schema):
    """params_schema 有两种形态：带 properties 包装，或扁平字典。返回 (props, required)。"""
    if not isinstance(schema, dict):
        return {}, []
    if isinstance(schema.get("properties"), dict):
        return schema["properties"], list(schema.get("required") or [])
    meta = {"type", "required", "description", "title", "properties"}
    flat = {k: v for k, v in schema.items() if k not in meta}
    return flat, list(schema.get("required") or [])


# ---------------------------------------------------------------- 配置类命令

def cmd_login(args):
    host = (args.host or DEFAULT_HOST).rstrip("/")
    key = args.key.strip()
    info("验证 Key …")
    path, status, payload, attempts = probe(key, APPS_CANDIDATES, host)
    if not path:
        die("Key 验证失败：应用列表端点都不通。\n" + json.dumps(attempts, ensure_ascii=False, indent=2), 4)
    _, data, _ = unwrap(payload)
    apps = pick_list(data)
    saved = save_config(key, host)
    info("Key 有效，可用应用 {} 个（端点 {}）".format(len(apps) or "?", path))
    info("已保存到 {}".format(saved))
    emit({"ok": True, "saved": str(saved), "host": host, "app_endpoint": path,
          "app_count": len(apps) or None})


def cmd_whoami(args):
    key, host = resolve(args)
    path, status, payload, attempts = probe(key, APPS_CANDIDATES, host)
    if not path:
        emit({"ok": False, "host": host, "key_prefix": key[:10] + "…",
              "attempts": attempts,
              "message": "Key 可能无效，或当前网络到不了 {}".format(host)})
        return 4
    _, data, msg = unwrap(payload)
    apps = pick_list(data)
    emit({
        "ok": True,
        "host": host,
        "key_prefix": key[:10] + "…",
        "app_endpoint": path,
        "app_count": len(apps) or None,
        "apps": [{"code": name_of(a), "name": (a or {}).get("name") if isinstance(a, dict) else ""}
                 for a in apps if isinstance(a, dict)],
        "message": msg,
        "note": "余额请用 balance 子命令；402 报错里也会附带本次所需点数。",
    })


def cmd_models(args):
    key, host = resolve(args)
    info("探测模型列表端点 …")
    path, status, payload, attempts = probe(key, MODELS_CANDIDATES, host)
    if not path:
        emit({"ok": False, "attempts": attempts,
              "message": "候选端点都不可用；可到 api.a7w.cn 站内「模型市场」查看，或询问技术微信。",
              "candidates": MODELS_CANDIDATES})
        return 4
    _, data, msg = unwrap(payload)
    items = pick_list(data)
    # 真实字段是 model_code / model_name（不是 model）
    names = [name_of(m, ("model_code", "model", "model_name", "name", "code", "id"))
             for m in items]
    names = [n for n in names if n]
    if args.filter:
        needle = args.filter.lower()
        names = [n for n in names if needle in n.lower()]
    emit({"ok": True, "endpoint": path, "count": len(names), "models": names,
          "raw_count": len(items), "message": msg})


def cmd_pricing(args):
    """查询**计费规则表**（价格页给出的端点）。

    实测响应是**裸对象**，且只有 6 条规则——是一条全局 markup 加少量特例，
    **不是**逐接口价格表（例如 voice_tts 就不在表里）：

        {"currency":"points","markupPercent":20,"note":"...",
         "pricing":{"*":{"mode":"flat","cost":0,"markupPercent":20},
                    "/api/v1/apps/full_video/submit":{"mode":"per_second",
                        "resolutionRates":{"480P":10,"768P":20,"1080P":40},...}}}

    要**逐接口**的真实价，请用 `schema <app>` 读 tenant_* 字段，那才是完整口径。
    """
    key, host = resolve(args)
    qs = ""
    if args.query:
        pairs = []
        for item in args.query:
            if "=" not in item:
                die("--query 需要 k=v 形式，收到：{}".format(item))
            k, _, v = item.partition("=")
            pairs.append((k.strip(), v.strip()))
        qs = "?" + urllib.parse.urlencode(pairs)
    payload = request(key, "GET", "{}{}/pricing{}".format(host, API_PREFIX, qs))
    ok, data, msg = unwrap(payload)
    obj = data if isinstance(data, dict) else (payload if isinstance(payload, dict) else {})
    pricing = obj.get("pricing")
    total = len(pricing) if isinstance(pricing, dict) else None
    if args.filter and isinstance(pricing, dict):
        needle = args.filter.lower()
        pricing = {k: v for k, v in pricing.items() if needle in k.lower()}
    emit({"ok": ok, "endpoint": API_PREFIX + "/pricing" + qs,
          "currency": obj.get("currency"),
          "markupPercent": obj.get("markupPercent"),
          "note": obj.get("note"),
          "count": len(pricing) if isinstance(pricing, dict) else None,
          "total_before_filter": total,
          "pricing": pricing, "message": msg,
          "hint": "这是**规则表**（键为路径或通配，值为 {mode, cost/perSecond, markupPercent}），"
                  "不含全部接口。逐接口真实价请用 `schema <app>` 看 tenant_* 字段。"})


def cmd_openai_env(args):
    _, host = resolve(args)
    emit({
        "ok": True,
        "base_url": host + API_PREFIX,
        "chat_completions": host + API_PREFIX + "/chat/completions",
        "auth_header": "Authorization: Bearer $A7W_API_KEY",
        "python": (
            "from openai import OpenAI\n"
            "client = OpenAI(base_url=\"{}\", api_key=\"sk-你的key\")\n"
            "r = client.chat.completions.create(model=\"DeepSeek-V4-Flash\",\n"
            "                                   messages=[{{\"role\":\"user\",\"content\":\"你好\"}}])"
        ).format(host + API_PREFIX),
        "node": (
            "import OpenAI from \"openai\";\n"
            "const client = new OpenAI({{ baseURL: \"{}\", apiKey: \"sk-你的key\" }});"
        ).format(host + API_PREFIX),
        "note": "model 名以 `models` 子命令的结果为准；换模型不用换 base_url 与 Key。",
    })


def _task_points(t):
    """从一条任务里取结算点数。真实字段是 actual_points。"""
    if not isinstance(t, dict):
        return 0.0
    for k in ("actual_points", "points_cost", "points", "cost", "amount"):
        try:
            if t.get(k) is not None:
                return float(t[k])
        except (TypeError, ValueError):
            pass
    usage = t.get("usage") or {}
    if isinstance(usage, dict):
        for k in ("points_cost", "points", "cost", "actual_points"):
            try:
                if usage.get(k) is not None:
                    return float(usage[k])
            except (TypeError, ValueError):
                pass
    return 0.0


def cmd_balance(args):
    key, host = resolve(args)
    info("探测余额端点 …")
    path, status, payload, attempts = probe(key, BALANCE_CANDIDATES, host)
    if path:
        # /api/v1/user/balance 返回的是**裸对象** {"available_points":…, "currency":"points"}
        _, data, msg = unwrap(payload)
        obj = data if isinstance(data, dict) else (payload if isinstance(payload, dict) else {})
        points = None
        for k in ("available_points", "points", "balance", "available", "remain_points"):
            if obj.get(k) is not None:
                points = obj[k]
                break
        emit({"ok": True, "endpoint": path, "points": points,
              "currency": obj.get("currency"), "data": obj,
              "message": msg, "attempts": attempts})
        return 0

    # 回退：用最近任务的结算点数汇总做参考
    info("余额端点不可用，回退为最近任务用量汇总 …")
    payload = request(key, "GET", host + API_PREFIX + "/tasks?page_no=1&page_size=50")
    ok, data, msg = unwrap(payload)
    tasks = pick_list(data)
    total = sum(_task_points(t) for t in tasks)
    emit({"ok": True, "endpoint": None, "points": None,
          "recent_task_count": len(tasks), "recent_points_cost": round(total, 2),
          "tasks": tasks[:20], "attempts": attempts, "message": msg,
          "note": "余额端点不可用。这里按最近任务的 actual_points 汇总估算；"
                  "点数不足时调用会返回 402 并附带余额。"})
    return 0


# ---------------------------------------------------------------- 模型网关

def sse_stream(key, url, body, timeout=300):
    """流式读取 SSE，把增量文本打到 stdout。返回累积文本。"""
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST", headers={
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    })
    chunks = []
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            for raw in resp:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if payload == "[DONE]":
                    break
                try:
                    obj = json.loads(payload)
                except ValueError:
                    continue
                for ch in (obj.get("choices") or []):
                    piece = ((ch.get("delta") or {}).get("content")) or ""
                    if piece:
                        chunks.append(piece)
                        sys.stdout.write(piece)
                        sys.stdout.flush()
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", "replace")
        try:
            parsed = json.loads(text)
        except ValueError:
            parsed = {"_raw": text[:500]}
        msg, code = explain(exc.code, parsed)
        die(msg, code)
    except urllib.error.URLError as exc:
        die("网络错误：{}\n（请确认能访问 {}）".format(exc.reason, url), 3)
    sys.stdout.write("\n")
    return "".join(chunks)


def cmd_chat(args):
    key, host = resolve(args)
    if not args.model:
        die("缺少 --model。先用 `client.py models` 拿可用模型名。")
    if args.prompt is not None and not args.system:
        messages = [{"role": "user", "content": args.prompt}]
    else:
        messages = []
        if args.system:
            messages.append({"role": "system", "content": args.system})
        if args.prompt is not None:
            messages.append({"role": "user", "content": args.prompt})
    if not messages:
        die("需要 --prompt \"...\"（或 --system 搭配 --prompt）。复杂消息体请用 --json-file。")

    body = {"model": args.model, "messages": messages}
    if args.max_tokens:
        body["max_tokens"] = args.max_tokens
    if args.temperature is not None:
        body["temperature"] = args.temperature
    if args.stream:
        body["stream"] = True

    url = host + API_PREFIX + "/chat/completions"
    info("POST {}/chat/completions  model={}".format(API_PREFIX, args.model))

    if args.stream:
        text = sse_stream(key, url, body, timeout=args.timeout or 300)
        info("（流式输出完毕，共 {} 字符）".format(len(text)))
        return 0

    payload = request(key, "POST", url, body=body, timeout=args.timeout or 300)
    # OpenAI 兼容响应直接就有 choices；若被网关包了一层，先拆
    ok, data, msg = unwrap(payload)
    core = data if (ok and isinstance(data, dict) and "choices" in data) else payload
    if not isinstance(core, dict) or "choices" not in core:
        emit({"ok": True, "raw": payload})
        return 0
    choice = (core.get("choices") or [{}])[0] or {}
    message = choice.get("message") or {}
    # 推理模型在 max_tokens 过小时会把 token 全用在 reasoning 上，content 会是 null。
    # 实测网关在不同模型/线路上分别用过 reasoning 与 reasoning_content，两个都取。
    content = message.get("content") or ""
    reasoning = message.get("reasoning") or message.get("reasoning_content")
    finish = choice.get("finish_reason")
    result = {"ok": True, "model": core.get("model", args.model),
              "content": content,
              "finish_reason": finish,
              "usage": core.get("usage"),
              "raw": core}
    if reasoning:
        result["reasoning"] = reasoning
    if not content and finish == "length":
        result["hint"] = ("content 为空且 finish_reason=length：该模型是推理模型，"
                          "token 可能全被 reasoning 消耗了。把 --max-tokens 调大再试。")
    emit(result)


# ---------------------------------------------------------------- 应用任务

def cmd_apps(args):
    key, host = resolve(args)
    path, status, payload, attempts = probe(key, APPS_CANDIDATES, host)
    if not path:
        emit({"ok": False, "attempts": attempts, "message": "应用列表端点都不可用"})
        return 4
    _, data, msg = unwrap(payload)
    apps = pick_list(data)
    if args.brief:
        emit({"ok": True, "endpoint": path, "count": len(apps),
              "apps": [{"code": name_of(a), "name": (a or {}).get("name") if isinstance(a, dict) else ""}
                       for a in apps]})
        return 0
    emit({"ok": True, "endpoint": path, "count": len(apps), "apps": apps, "message": msg})


def cmd_schema(args):
    key, host = resolve(args)
    payload = request(key, "GET", "{}{}/apps/{}".format(host, API_PREFIX, args.app))
    ok, data, msg = unwrap(payload)
    apis = []
    if isinstance(data, dict):
        apis = data.get("apis") or data.get("api_list") or []
    summary = []
    for a in (apis if isinstance(apis, list) else []):
        if not isinstance(a, dict):
            continue
        # 真实字段名是 params_schema（老样本里也有写成 schema 的），两种都认
        props, required = schema_props(a.get("params_schema") or a.get("schema"))
        summary.append({
            # 真实字段名是 code；api / name 是历史或展示用的回退
            "api": a.get("code") or a.get("api") or a.get("name"),
            "name": a.get("name"),
            "method": a.get("method") or "POST",
            "call_type": a.get("call_type"),          # 1=同步 2=异步
            "endpoint_path": a.get("endpoint_path"),
            "params": sorted(props.keys()),
            "required": required,
            "tenant_fixed_points": a.get("tenant_fixed_points"),
            "tenant_points_per_1k_input": a.get("tenant_points_per_1k_input"),
            "tenant_points_per_1k_output": a.get("tenant_points_per_1k_output"),
            "fixed_price": a.get("fixed_price"),
        })
    emit({"ok": ok, "app": args.app, "api_count": len(summary), "apis": summary,
          "note": "调用用 `api` 字段（真实接口代码），不要用 name（那是中文展示名）。",
          "schema": data, "message": msg})


def _parse_scalar(value):
    v = value.strip()
    if v == "":
        return ""
    try:
        return json.loads(v)
    except ValueError:
        return value


def build_body(args):
    """支持 --json / --json-file / --param 三种方式，避开 shell 引号问题。"""
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
            k, _, v = item.partition("=")
            body[k.strip()] = _parse_scalar(v)
        return body
    return {}


def cmd_call(args):
    key, host = resolve(args)
    body = build_body(args)
    url = "{}{}/apps/{}/{}".format(host, API_PREFIX, args.app, args.api)
    info("提交任务：POST {}/apps/{}/{}".format(API_PREFIX, args.app, args.api))
    payload = request(key, "POST", url, body=body)
    ok, data, msg = unwrap(payload)
    if not ok:
        emit({"ok": False, "stage": "submit", "message": msg, "raw": payload})
        return 4
    if not isinstance(data, dict):
        emit({"ok": True, "mode": "sync", "result": data})
        return 0

    task_id = data.get("task_id") or data.get("taskId") or data.get("id")
    if not task_id:
        emit({"ok": True, "mode": "sync", "result": data})
        return 0

    info("task_id = {}（预冻结 {} 点）".format(task_id, data.get("frozen_points", "?")))
    if args.no_wait:
        emit({"ok": True, "mode": "async", "task_id": task_id, "submit": data})
        return 0

    deadline = time.time() + (args.timeout or POLL_TIMEOUT)
    interval = args.interval or POLL_INTERVAL
    last = None
    while time.time() < deadline:
        time.sleep(interval)
        poll = request(key, "GET", "{}{}/tasks/{}".format(host, API_PREFIX, task_id))
        pok, pdata, pmsg = unwrap(poll)
        pdata = pdata if isinstance(pdata, dict) else {}
        status = pdata.get("status")
        if status != last:
            info("  状态：{}".format(status))
            last = status
        if status in TERMINAL_STATES:
            emit({"ok": status == "completed", "mode": "async", "task_id": task_id,
                  "status": status, "result": pdata.get("result"),
                  "usage": pdata.get("usage"),
                  "points_cost": _task_points(pdata),
                  "error": pdata.get("error"), "task": pdata})
            return 0 if status == "completed" else 6

    emit({"ok": False, "mode": "async", "task_id": task_id, "message": "轮询超时",
          "hint": "任务可能仍在跑，用 client.py task {} 继续查".format(task_id)})
    return 7


def cmd_task(args):
    key, host = resolve(args)
    payload = request(key, "GET", "{}{}/tasks/{}".format(host, API_PREFIX, args.task_id))
    ok, data, msg = unwrap(payload)
    emit({"ok": ok, "task": data, "message": msg})


def cmd_tasks(args):
    key, host = resolve(args)
    qs = urllib.parse.urlencode({"page_no": args.page_no, "page_size": args.page_size})
    payload = request(key, "GET", "{}{}/tasks?{}".format(host, API_PREFIX, qs))
    ok, data, msg = unwrap(payload)
    tasks = pick_list(data)
    out = {"ok": ok, "count": len(tasks), "tasks": tasks, "message": msg}
    if isinstance(data, dict):
        out["page"] = data.get("page")
        out["per_page"] = data.get("per_page")
        out["total"] = data.get("total")
        if data.get("per_page") and args.page_size and int(data["per_page"]) != args.page_size:
            out["note"] = ("上游忽略了 page_size（请求 %s，实际每页 %s）。"
                           "翻页请用 --page-no。" % (args.page_size, data["per_page"]))
    emit(out)


def cmd_dump(args):
    """把所有应用的 schema 一次性导出，便于离线检索参数。"""
    key, host = resolve(args)
    path, status, payload, _ = probe(key, APPS_CANDIDATES, host)
    if not path:
        die("应用列表端点不可用", 4)
    _, data, _ = unwrap(payload)
    apps = pick_list(data)
    out = {"host": host, "count": 0, "apps": {}}
    for i, app in enumerate(apps, 1):
        code = name_of(app)
        if not code:
            continue
        detail = request(key, "GET", "{}{}/apps/{}".format(host, API_PREFIX, code))
        _, d, m = unwrap(detail)
        out["apps"][code] = {"summary": app, "schema": d, "message": m}
        info("  [{}/{}] {} ✓".format(i, len(apps), code))
    out["count"] = len(out["apps"])
    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    emit({"ok": True, "apps": out["count"], "out": str(Path(args.out).resolve())})


# ---------------------------------------------------------------- 入口

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="client.py",
        description="api.a7w.cn 统一网关客户端（零依赖，不内嵌密钥）")
    parser.add_argument("--key", help="覆盖 API Key（默认读环境变量或本机配置）")
    parser.add_argument("--host", help="覆盖服务地址（默认 {}）".format(DEFAULT_HOST))

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--key", default=argparse.SUPPRESS, help="覆盖 API Key")
    common.add_argument("--host", default=argparse.SUPPRESS, help="覆盖服务地址")

    sub = parser.add_subparsers(dest="cmd", required=True, metavar="<命令>")

    p = sub.add_parser("login", parents=[common], help="验证并保存 API Key 到本机")
    p.set_defaults(func=cmd_login)

    p = sub.add_parser("whoami", parents=[common], help="验证当前 Key")
    p.set_defaults(func=cmd_whoami)

    p = sub.add_parser("models", parents=[common], help="列出可调用模型")
    p.add_argument("--filter", help="按关键词过滤模型名")
    p.set_defaults(func=cmd_models)

    p = sub.add_parser("openai-env", parents=[common], help="打印 OpenAI SDK 接入参数")
    p.set_defaults(func=cmd_openai_env)

    p = sub.add_parser("balance", parents=[common], help="查点数余额（含回退方案）")
    p.set_defaults(func=cmd_balance)

    p = sub.add_parser("pricing", parents=[common],
                       help="查询计费规则表（全局 markup + 少量特例）")
    p.add_argument("--query", action="append",
                   help="附加查询参数 k=v，可重复")
    p.add_argument("--filter", help="按接口路径片段过滤，如 voice_tts")
    p.set_defaults(func=cmd_pricing)

    p = sub.add_parser("chat", parents=[common], help="调用模型网关（OpenAI 兼容）")
    p.add_argument("--model", required=True, help="模型名，用 `models` 查")
    p.add_argument("--prompt", help="用户消息")
    p.add_argument("--system", help="system 消息")
    p.add_argument("--max-tokens", type=int, dest="max_tokens", help="最大生成 tokens")
    p.add_argument("--temperature", type=float, help="采样温度")
    p.add_argument("--stream", action="store_true", help="流式输出（直接打印文本）")
    p.add_argument("--timeout", type=int, help="请求超时秒数")
    p.set_defaults(func=cmd_chat)

    p = sub.add_parser("apps", parents=[common], help="列出全部应用")
    p.add_argument("--brief", action="store_true", help="只输出代码与名称")
    p.set_defaults(func=cmd_apps)

    p = sub.add_parser("schema", parents=[common], help="查看某应用的接口、参数与真实价")
    p.add_argument("app", help="应用代码，如 voice_tts（用下划线，不是连字符）")
    p.set_defaults(func=cmd_schema)

    p = sub.add_parser("call", parents=[common], help="调用应用的某个接口")
    p.add_argument("app", help="应用代码")
    p.add_argument("api", help="接口代码，如 tts")
    p.add_argument("--json", help="请求体 JSON 字符串（'-' 表示从标准输入读）")
    p.add_argument("--json-file", help="从 JSON 文件读请求体（最稳，推荐）")
    p.add_argument("--param", action="append", help="键值对 k=v，可重复；值按 JSON 解析")
    p.add_argument("--no-wait", action="store_true", help="异步任务不等待，直接返回 task_id")
    p.add_argument("--interval", type=int, help="轮询间隔秒数（默认 {}）".format(POLL_INTERVAL))
    p.add_argument("--timeout", type=int, help="轮询超时秒数（默认 {}）".format(POLL_TIMEOUT))
    p.set_defaults(func=cmd_call)

    p = sub.add_parser("task", parents=[common], help="查询异步任务状态")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_task)

    p = sub.add_parser("tasks", parents=[common], help="列出最近任务")
    p.add_argument("--page-no", type=int, dest="page_no", default=1)
    p.add_argument("--page-size", type=int, dest="page_size", default=20)
    p.set_defaults(func=cmd_tasks)

    p = sub.add_parser("dump", parents=[common], help="导出全部应用 schema 到一个 JSON")
    p.add_argument("--out", default="a7w-apps-schema.json", help="输出文件路径")
    p.set_defaults(func=cmd_dump)

    args = parser.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
