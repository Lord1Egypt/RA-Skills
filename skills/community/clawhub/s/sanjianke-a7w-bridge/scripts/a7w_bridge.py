#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a7w-bridge —— 把算力集市（api.a7w.cn）的**全部**能力，翻译成生态通用的 OpenAI 协议。

## 为什么需要它

算力集市有两条入口，但生态只认 OpenAI 协议：

    模型网关（真 OpenAI 兼容）  POST /api/v1/chat/completions      ← 生态直接可用
    应用任务（自有异步协议）    POST /api/v1/apps/{app}/{code}     ← 生态完全不认

而实测（2026-09-25，真实 Key）以下端点在网关上都 **404**：

    /v1/audio/speech        /v1/audio/transcriptions
    /v1/images/generations  /v1/images/edits        /v1/embeddings

所以任何开源项目只要碰 TTS / ASR / 出图，接上去就是 404——**不是能力没有，是协议缺口**。

本桥在本地补上缺口，让 21 个应用 + 75 个模型 都能被标准 OpenAI 客户端直接调用。

## 用法

    python -X utf8 a7w_bridge.py --port 8788
    # 然后把客户端 base_url 指向 http://127.0.0.1:8788/v1

## 端点

    GET  /v1/models                    75 个模型 + 全部应用能力
    POST /v1/chat/completions          透传（支持 stream）
    POST /v1/audio/speech              文字转语音 → voice_tts/tts
    POST /v1/audio/transcriptions      语音转文字 → voice_tts/stt
    GET  /v1/audio/voices              音色列表   → voice_tts/list_voices
    POST /v1/images/generations        文生图     → nano_banana(action=generate)
    POST /v1/images/edits              图片编辑   → nano_banana(action=edit)
    POST /v1/embeddings                明确返回 501（网关无 embedding 模型）
    ANY  /a7w/{app}/{code}             ★ 全量应用透传（21 个应用都可这样调）
    GET  /a7w/tasks/{id}               任务查询
    GET  /health

零依赖（仅 Python 标准库）。Key 从 ~/.a7w/config.json 或环境变量 A7W_API_KEY 读取，
仅访问 api.a7w.cn。客户端自带 Authorization 时优先用客户端的。"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = "https://api.a7w.cn"
DEFAULT_PORT = 8788
POLL_INTERVAL = 2.0
POLL_TIMEOUT = 300.0

# --------------------------------------------------------------------------- #
# embedding 缺口的外挂方案
#
# 算力集市 75 个模型里没有 embedding / rerank，这是真缺口，桥本身补不了。
# 但 RAG 平台本来就支持把 embedding 指向另一个提供方，所以桥把 /v1/embeddings
# 转发到使用者自备的 OpenAI 兼容 embedding 服务（比如本地 bge-m3）。
# 这样客户端仍然只配一个 base_url —— 这正是"桥"存在的意义。
#
#   A7W_EMBEDDING_BASE_URL  例如 http://127.0.0.1:11434/v1  (Ollama)
#                                 http://127.0.0.1:9997/v1   (Xinference)
#   A7W_EMBEDDING_API_KEY   可选，不填则不带 Authorization
#   A7W_EMBEDDING_MODEL     可选；请求里没带 model 时用这个兜底
# --------------------------------------------------------------------------- #
EMBED_BASE = (os.environ.get("A7W_EMBEDDING_BASE_URL") or "").rstrip("/")
EMBED_KEY = os.environ.get("A7W_EMBEDDING_API_KEY") or ""
EMBED_MODEL = os.environ.get("A7W_EMBEDDING_MODEL") or ""


# --------------------------------------------------------------------------- #
# Key
# --------------------------------------------------------------------------- #
def load_key():
    if os.environ.get("A7W_API_KEY"):
        return os.environ["A7W_API_KEY"]
    p = os.path.join(os.path.expanduser("~"), ".a7w", "config.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
        for k in ("key", "api_key", "token", "apikey", "apiKey"):
            if d.get(k):
                return d[k]
    return None


LOCAL_KEY = load_key()


# --------------------------------------------------------------------------- #
# 上游调用
# --------------------------------------------------------------------------- #
def upstream(method, path, body=None, raw=None, ctype=None, key=None, timeout=120):
    """调用算力集市，返回 (status, headers, bytes)。"""
    url = path if path.startswith("http") else UPSTREAM + path
    data = raw if raw is not None else (json.dumps(body).encode("utf-8") if body is not None else None)
    req = urllib.request.Request(url, data=data, method=method)
    k = key or LOCAL_KEY
    if k:
        req.add_header("Authorization", "Bearer " + k)
    if ctype:
        req.add_header("Content-Type", ctype)
    elif data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()
    except Exception as e:
        return 502, {}, json.dumps({"error": {"message": "上游调用失败: %r" % (e,),
                                              "type": "upstream_error"}}).encode()


def a7w_json(method, path, body=None, key=None, timeout=120):
    st, _, raw = upstream(method, path, body=body, key=key, timeout=timeout)
    try:
        return st, json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        return st, {"_raw": raw.decode("utf-8", "replace")[:400]}


def ok_of(payload):
    """网关用 code 表示业务成败：1 或 200 为成功。"""
    return payload.get("code") in (1, 200, "1", "200")


def key_hint(upstream_msg):
    """未配置 Key 时，把上游的英文鉴权错误换成人能照着做的中文指引。

    上游原文是 "Missing or invalid relay API key."——新用户看到这句
    不知道要做什么。这一步直接决定"装完能不能自己跑起来"。
    """
    if LOCAL_KEY:
        return upstream_msg
    low = (upstream_msg or "").lower()
    if any(k in low for k in ("unauthorized", "api key", "401", "invalid relay")):
        return ("尚未配置 API Key —— 这是本桥唯一的必填项。三选一：\n"
                "  1) 环境变量：set A7W_API_KEY=sk-...           （Windows）\n"
                "                export A7W_API_KEY=sk-...      （macOS/Linux）\n"
                "  2) 写配置文件：%s\n"
                "                内容 {'key': 'sk-...'}\n"
                "  3) 用配套技能：python client.py login --key sk-...\n"
                "Key 在 https://api.a7w.cn/ 用户中心 → API 密钥 创建（需实名认证）。\n"
                "上游原始信息：" % os.path.join(os.path.expanduser("~"), ".a7w", "config.json")
                ) + upstream_msg
    return upstream_msg


def err_msg(payload):
    raw = payload.get("msg") or payload.get("message") or json.dumps(payload, ensure_ascii=False)[:200]
    return key_hint(raw)


def unwrap(payload):
    """网关信封 {code,msg,data} 的 data 有时是 dict、有时是 list，统一取出来。"""
    if isinstance(payload, dict) and "data" in payload:
        return payload["data"]
    return payload


def app_list(payload):
    """/api/v1/apps 的 data 是 list；兼容 {'apps': [...]} 形态。"""
    d = unwrap(payload)
    if isinstance(d, dict):
        return d.get("apps") or []
    return d if isinstance(d, list) else []


# --------------------------------------------------------------------------- #
# 任务轮询
# --------------------------------------------------------------------------- #
def poll_task(task_id, app=None, key=None, timeout=POLL_TIMEOUT):
    """轮询任务到终态，返回 (ok, result_dict_or_error)。

    ★ 实测结论（2026-09-25）：**通用端点 /api/v1/tasks/{id} 对 nano_banana 不可靠**。
      同一个任务：
        GET /api/v1/tasks/task_xxx           → {"status":"UNKNOWN","url":""}   ← 假的失败
        GET /api/v1/apps/nano_banana/query   → result.success=true + image_url ← 真实结果
      图片确实生成了（1.9MB PNG 可下载），只是通用端点没映射状态。
      因此**优先用应用专用 query 端点**，通用端点只作兜底。
    """
    deadline = time.time() + timeout
    seen_unknown = 0
    last = None
    while time.time() < deadline:
        # ── 1) 应用专用查询（可靠）
        if app:
            st, d = a7w_json("GET", "/api/v1/apps/%s/query?task_id=%s"
                             % (app, urllib.parse.quote(task_id)), key=key)
            if ok_of(d):
                r = unwrap_result(d)
                if isinstance(r, dict) and r:
                    last = r
                    if r.get("success") is True:
                        return True, r
                    if find_urls(r):
                        return True, r
                    if r.get("success") is False or r.get("error"):
                        return False, r
                    # 还没产物 → 继续等
        # ── 2) 通用端点（兜底）
        st, d = a7w_json("GET", "/api/v1/tasks/" + urllib.parse.quote(task_id), key=key)
        data = d.get("data") if isinstance(d.get("data"), dict) else None
        status = (data or {}).get("status")
        if status in ("completed", "success", "succeeded"):
            return True, data
        if status in ("failed", "cancelled", "error"):
            return False, data or d
        if status == "UNKNOWN":
            # 只有「应用端点也没给出结果」时才真正判失败
            if not app:
                seen_unknown += 1
                if seen_unknown >= 2:
                    return False, {"status": "UNKNOWN", "task_id": task_id, "app": app,
                                   "error": "网关未返回有效任务状态；该应用可能没有专用 query 端点。"}
        time.sleep(POLL_INTERVAL)
    if last:
        return False, dict(last, error="任务超时但已有部分结果")
    return False, {"error": "任务超时（%ss）：%s" % (int(timeout), task_id)}


def find_urls(obj, found=None):
    """从任务结果里递归捞出所有 URL（不同应用的产物字段名不统一）。"""
    if found is None:
        found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and v.startswith("http") and k.lower().endswith(
                    ("url", "urls", "image", "images", "video", "audio", "output", "result", "file")):
                found.append(v)
            else:
                find_urls(v, found)
    elif isinstance(obj, list):
        for v in obj:
            find_urls(v, found)
    return found


# --------------------------------------------------------------------------- #
# 注意：官方 api_doc 与真实响应不一致 —— 真实结构是 data.result.{...}
# 实测 voice_tts/tts   → data.result.audio_url / data.result.format
# 实测 voice_tts/stt   → data.result.{text,duration,language_code,segments}
# --------------------------------------------------------------------------- #
def unwrap_result(payload):
    """取出 data.result（真实结构）；兼容把字段直接放 data 下的旧文档写法。"""
    d = unwrap(payload)
    if isinstance(d, dict) and isinstance(d.get("result"), dict):
        return d["result"]
    return d if isinstance(d, dict) else {}


PUNCT = "，。！？；：、,.!?;:…—"


def group_segments(segments, max_chars=14):
    """把词级 segments 合并成适合做字幕的句子级 cue。

    网关在 ignore_timestamps=false 时返回的是**逐字**片段（每字 ~0.16s），
    直接塞进 SRT 会一行一个字。这里按标点或长度上限合并。"""
    cues, cur = [], None
    for s in segments or []:
        t = (s.get("text") or "").strip()
        if not t:
            continue
        if cur is None:
            cur = {"start": s.get("start", 0), "end": s.get("end", 0), "text": t}
        else:
            cur["text"] += t
            cur["end"] = s.get("end", cur["end"])
        if cur["text"][-1] in PUNCT or len(cur["text"]) >= max_chars:
            cues.append(cur)
            cur = None
    if cur:
        cues.append(cur)
    return cues


def _ts(sec, comma=","):
    sec = max(0.0, float(sec or 0))
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    # 注意括号：% 的优先级低于方法调用，不加括号会对元组调 .replace
    return ("%02d:%02d:%06.3f" % (h, m, s)).replace(".", comma)


def to_srt(cues):
    out = []
    for i, c in enumerate(cues, 1):
        out.append("%d\n%s --> %s\n%s\n" % (i, _ts(c["start"]), _ts(c["end"]), c["text"]))
    return "\n".join(out)


def to_vtt(cues):
    out = ["WEBVTT", ""]
    for c in cues:
        out.append("%s --> %s\n%s\n" % (_ts(c["start"], "."), _ts(c["end"], "."), c["text"]))
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# multipart：把 OpenAI 的 file 字段改写成网关要的 audio 字段
# --------------------------------------------------------------------------- #
def parse_multipart(raw, content_type):
    """极简 multipart 解析，返回 [(name, filename, ctype, bytes)]。"""
    m = re.search(r"boundary=([^;]+)", content_type or "")
    if not m:
        return []
    b = m.group(1).strip('"').encode()
    parts = []
    for seg in raw.split(b"--" + b):
        seg = seg.strip(b"\r\n")
        if not seg or seg == b"--":
            continue
        head, _, body = seg.partition(b"\r\n\r\n")
        if not _:
            continue
        hs = head.decode("utf-8", "replace")
        nm = re.search(r'name="([^"]*)"', hs)
        fn = re.search(r'filename="([^"]*)"', hs)
        ct = re.search(r"Content-Type:\s*([^\r\n]+)", hs)
        parts.append((nm.group(1) if nm else "",
                      fn.group(1) if fn else None,
                      ct.group(1).strip() if ct else "application/octet-stream",
                      body.rstrip(b"\r\n")))
    return parts


def build_multipart(parts, boundary="----a7wbridge"):
    out = b""
    for name, filename, ctype, content in parts:
        out += ("--%s\r\n" % boundary).encode()
        if filename:
            out += ('Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
                    % (name, filename)).encode()
        else:
            out += ('Content-Disposition: form-data; name="%s"\r\n' % name).encode()
        out += ("Content-Type: %s\r\n\r\n" % ctype).encode()
        out += content + b"\r\n"
    out += ("--%s--\r\n" % boundary).encode()
    return out, "multipart/form-data; boundary=" + boundary


# --------------------------------------------------------------------------- #
# 参数映射
# --------------------------------------------------------------------------- #
def map_speech(body):
    """OpenAI /v1/audio/speech → voice_tts/tts 参数。"""
    p = {"text": body.get("input") or body.get("text") or ""}
    fmt = body.get("response_format") or body.get("format")
    if fmt:
        p["format"] = "mp3" if fmt == "mp3" else fmt
    if body.get("model"):
        p["model"] = body["model"]
    v = body.get("voice")
    if v and v not in ("alloy", "echo", "fable", "onyx", "nova", "shimmer"):
        p["reference_id"] = v          # 非内置音色名 → 当成网关音色 ID
    if body.get("speed"):
        p["prosody"] = {"speed": body["speed"]}
    if body.get("mp3_bitrate"):
        p["mp3_bitrate"] = body["mp3_bitrate"]
    return p


def map_image(body, action="generate"):
    p = {"action": action, "prompt": body.get("prompt") or ""}
    if body.get("model"):
        p["model"] = body["model"]
    if body.get("resolution"):
        p["resolution"] = body["resolution"]
    elif body.get("size"):
        p["resolution"] = {"256x256": "1K", "512x512": "1K", "1024x1024": "1K",
                           "1792x1024": "2K", "1024x1792": "2K"}.get(body["size"], "1K")
    if body.get("aspect_ratio"):
        p["aspect_ratio"] = body["aspect_ratio"]
    if action == "edit":
        urls = body.get("image_urls") or ([body["image"]] if isinstance(body.get("image"), str) else [])
        p["image_urls"] = urls
    return p


# --------------------------------------------------------------------------- #
# HTTP 服务
# --------------------------------------------------------------------------- #
class Handler(BaseHTTPRequestHandler):
    server_version = "a7w-bridge/1.0"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *a):
        sys.stderr.write("[bridge] %s %s\n" % (self.address_string(), fmt % a))

    # ---- 基础工具 ----
    def _key(self):
        h = self.headers.get("Authorization") or ""
        if h.lower().startswith("bearer "):
            return h[7:].strip()
        return LOCAL_KEY

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(n) if n else b""

    def _json_body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            return {}

    def _send(self, code, payload, ctype="application/json; charset=utf-8", extra=None):
        raw = payload if isinstance(payload, bytes) else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(raw)

    def _err(self, code, msg, etype="bridge_error"):
        self._send(code, {"error": {"message": msg, "type": etype}})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Content-Length", "0")
        self.end_headers()

    # ---- 路由 ----
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if path in ("/", "/health"):
            return self._send(200, {"ok": True, "service": "a7w-bridge",
                                    "upstream": UPSTREAM, "hasKey": bool(self._key()),
                                    "embeddingProxy": EMBED_BASE or None,
                                    "endpoints": ["/v1/models", "/v1/chat/completions",
                                                  "/v1/audio/speech", "/v1/audio/transcriptions",
                                                  "/v1/audio/voices", "/v1/images/generations",
                                                  "/v1/images/edits", "/a7w/{app}/{code}",
                                                  "/a7w/tasks/{id}"]})
        if path == "/v1/models":
            return self._models()
        if path == "/v1/audio/voices":
            st, d = a7w_json("GET", "/api/v1/apps/voice_tts/list_voices?" +
                             urllib.parse.urlencode({k: v[0] for k, v in q.items()}), key=self._key())
            return self._send(200 if ok_of(d) else st, d)
        if path.startswith("/a7w/tasks/"):
            tid = path.rsplit("/", 1)[-1]
            st, d = a7w_json("GET", "/api/v1/tasks/" + urllib.parse.quote(tid), key=self._key())
            return self._send(200, d)
        return self._err(404, "未知路径: %s" % path)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/v1/chat/completions":
            return self._chat()
        if path == "/v1/audio/speech":
            return self._speech()
        if path == "/v1/audio/transcriptions":
            return self._transcribe()
        if path == "/v1/images/generations":
            return self._image("generate")
        if path == "/v1/images/edits":
            return self._image("edit")
        if path == "/v1/embeddings":
            return self._embeddings()
        if path.startswith("/a7w/"):
            return self._passthrough(path[5:])
        return self._err(404, "未知路径: %s" % path)

    # ---- 各端点实现 ----
    def _models(self):
        st, d = a7w_json("GET", "/api/v1/models", key=self._key())
        native = d.get("data") or d.get("models") or []
        out = []
        for m in native:
            code = m.get("model_code") or m.get("id")
            out.append({"id": code, "object": "model", "owned_by": m.get("vendor_name") or "a7w",
                        "created": m.get("created") or 0,
                        "a7w": {"type": m.get("type_code"), "call_type": m.get("call_type"),
                                "vision": bool(m.get("supports_vision")),
                                "reasoning": bool(m.get("supports_reasoning"))}})
        # 应用型伪模型：让客户端也能发现异步能力
        st2, apps = a7w_json("GET", "/api/v1/apps", key=self._key())
        for a in app_list(apps):
            for api in (a.get("apis") or []):
                out.append({"id": "a7w/%s:%s" % (a.get("code"), api.get("code")),
                            "object": "model", "owned_by": "a7w-app",
                            "created": 0,
                            "a7w": {"app": a.get("code"), "api": api.get("code"),
                                    "category": a.get("category_name"),
                                    "call_type": api.get("call_type")}})
        return self._send(200, {"object": "list", "data": out})

    def _chat(self):
        body = self._json_body()
        stream = bool(body.get("stream"))
        if not stream:
            st, _, raw = upstream("POST", "/api/v1/chat/completions", body=body, key=self._key())
            if st in (401, 403) and not (self.headers.get("Authorization") or "").strip():
                return self._err(st, key_hint(raw.decode("utf-8", "replace")[:200]), "auth_failed")
            return self._send(st, raw, "application/json; charset=utf-8")
        # 流式：原样透传 SSE
        data = json.dumps(body).encode()
        req = urllib.request.Request(UPSTREAM + "/api/v1/chat/completions", data=data, method="POST")
        req.add_header("Authorization", "Bearer " + (self._key() or ""))
        req.add_header("Content-Type", "application/json")
        try:
            r = urllib.request.urlopen(req, timeout=300)
        except urllib.error.HTTPError as e:
            return self._send(e.code, e.read(), "application/json; charset=utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Connection", "close")
        self.end_headers()
        try:
            while True:
                chunk = r.read(1024)
                if not chunk:
                    break
                self.wfile.write(chunk)
                self.wfile.flush()
        except Exception:
            pass
        return

    def _speech(self):
        body = self._json_body()
        text = body.get("input") or body.get("text") or ""
        if not text:
            return self._err(400, "缺少 input 字段")
        params = map_speech(body)
        # 长文本走异步
        if len(text) > 500:
            st, d = a7w_json("POST", "/api/v1/apps/voice_tts/tts_async",
                             body=params, key=self._key())
            if not ok_of(d):
                return self._err(502, "TTS 提交失败: %s" % err_msg(d))
            tid = (d.get("data") or {}).get("task_id")
            ok, res = poll_task(tid, app="voice_tts", key=self._key())
            if not ok:
                return self._err(502, "TTS 任务失败: %s" % json.dumps(res, ensure_ascii=False)[:200])
            urls = find_urls(res)
            if not urls:
                return self._err(502, "TTS 任务完成但未找到产物 URL")
            audio_url, fmt = urls[0], params.get("format", "mp3")
        else:
            st, d = a7w_json("POST", "/api/v1/apps/voice_tts/tts", body=params, key=self._key())
            if not ok_of(d):
                return self._err(502, "TTS 失败: %s" % err_msg(d))
            data = unwrap_result(d)
            audio_url = data.get("audio_url")
            fmt = data.get("format") or params.get("format", "mp3")
            if not audio_url:
                return self._err(502, "TTS 未返回 audio_url（响应结构：%s）"
                                      % json.dumps(d, ensure_ascii=False)[:200])
        # 取回音频字节，按 OpenAI 行为直接返回音频流
        st2, hdr, raw = upstream("GET", audio_url, key=None, timeout=180)
        if st2 != 200 or not raw:
            return self._err(502, "音频下载失败 HTTP %s" % st2)
        ctype = {"mp3": "audio/mpeg", "wav": "audio/wav", "opus": "audio/ogg",
                 "pcm": "audio/pcm"}.get(fmt, "application/octet-stream")
        return self._send(200, raw, ctype)

    def _transcribe(self):
        """OpenAI /v1/audio/transcriptions → voice_tts/stt。

        支持 response_format = json | text | srt | vtt | verbose_json。
        srt / vtt / verbose_json 会打开网关的 ignore_timestamps=false，
        拿到**词级**时间戳后再合并成字幕 cue（网关真实返回见 unwrap_result 注释）。
        """
        ctype = self.headers.get("Content-Type") or ""
        key = self._key()
        rfmt = "json"
        if ctype.startswith("multipart/form-data"):
            raw = self._body()
            parts = parse_multipart(raw, ctype)
            if not parts:
                return self._err(400, "multipart 解析失败")
            # 网关字段名是 audio，OpenAI 是 file → 改写
            want_ts = False
            new = []
            for name, fn, ct, content in parts:
                val = content.decode("utf-8", "replace").strip()
                if name in ("file", "audio"):
                    new.append(("audio", fn or "audio.mp3", ct, content))
                elif name == "language":
                    new.append(("language", None, "text/plain", content))
                elif name == "response_format":
                    rfmt = val or "json"
                elif name in ("timestamp_granularities[]", "timestamp_granularities"):
                    want_ts = True
                elif name == "ignore_timestamps":
                    new.append(("ignore_timestamps", None, "text/plain", content))
            if rfmt in ("srt", "vtt", "verbose_json") or want_ts:
                new = [p for p in new if p[0] != "ignore_timestamps"]
                new.append(("ignore_timestamps", None, "text/plain", b"false"))
            body, ct2 = build_multipart(new)
            st, _, raw2 = upstream("POST", "/api/v1/apps/voice_tts/stt", raw=body, ctype=ct2, key=key)
            try:
                d = json.loads(raw2.decode("utf-8", "replace"))
            except Exception:
                d = {"code": 0, "msg": raw2.decode("utf-8", "replace")[:200]}
        else:
            d = self._json_body()
            rfmt = d.pop("response_format", "json") or "json"
            segs = d.pop("timestamp_granularities", None) or d.pop("timestamp_granularities[]", None)
            if rfmt in ("srt", "vtt", "verbose_json") or segs:
                d["ignore_timestamps"] = False
            st, d = a7w_json("POST", "/api/v1/apps/voice_tts/stt", body=d, key=key)

        if not ok_of(d):
            return self._err(502, "ASR 失败: %s" % err_msg(d))

        r = unwrap_result(d)
        text = r.get("text", "")
        lang = r.get("language_code") or r.get("language") or "zh"
        dur = r.get("duration")
        cues = group_segments(r.get("segments") or [])

        if rfmt == "text":
            return self._send(200, text, "text/plain; charset=utf-8")
        if rfmt == "srt":
            if not cues:
                return self._err(502, "网关未返回时间戳片段（segments 为空），无法生成 SRT")
            return self._send(200, to_srt(cues), "application/x-subrip; charset=utf-8")
        if rfmt == "vtt":
            if not cues:
                return self._err(502, "网关未返回时间戳片段（segments 为空），无法生成 VTT")
            return self._send(200, to_vtt(cues), "text/vtt; charset=utf-8")
        if rfmt == "verbose_json":
            return self._send(200, {"task": "transcribe", "language": lang,
                                    "duration": dur, "text": text,
                                    "segments": [{"id": i, "seek": 0, "start": c["start"],
                                                  "end": c["end"], "text": c["text"],
                                                  "temperature": 0, "avg_logprob": 0,
                                                  "compression_ratio": 0, "no_speech_prob": 0}
                                                 for i, c in enumerate(cues)],
                                    "words": r.get("segments") or []})
        return self._send(200, {"text": text, "duration": dur, "language": lang})

    def _embeddings(self):
        """embedding 缺口的外挂转发。

        算力集市没有 embedding 模型，这是真缺口。但 RAG 平台本来就允许把
        embedding 指向别处，所以桥把 /v1/embeddings 转到使用者自备的
        OpenAI 兼容服务——客户端依然只配一个 base_url。
        """
        if not EMBED_BASE:
            return self._err(
                501,
                "算力集市不提供 embedding 模型（75 个模型里没有 embedding/rerank）。"
                "桥支持外挂：设置环境变量 A7W_EMBEDDING_BASE_URL 指向你自己的 "
                "OpenAI 兼容 embedding 服务即可，例如：\n"
                "  Ollama      A7W_EMBEDDING_BASE_URL=http://127.0.0.1:11434/v1\n"
                "  Xinference  A7W_EMBEDDING_BASE_URL=http://127.0.0.1:9997/v1\n"
                "（可选）A7W_EMBEDDING_API_KEY / A7W_EMBEDDING_MODEL。"
                "重跑桥后，/v1/embeddings 转发过去，其余端点仍走算力集市。",
                "not_implemented")
        body = self._json_body()
        if not body.get("model") and EMBED_MODEL:
            body["model"] = EMBED_MODEL
        url = EMBED_BASE + ("/embeddings" if EMBED_BASE.endswith("/v1") else "/v1/embeddings")
        data = json.dumps(body).encode()
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        if EMBED_KEY:
            req.add_header("Authorization", "Bearer " + EMBED_KEY)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return self._send(r.status, r.read(), "application/json; charset=utf-8")
        except urllib.error.HTTPError as e:
            return self._send(e.code, e.read(), "application/json; charset=utf-8")
        except Exception as e:
            return self._err(502, "外挂 embedding 服务不可达（%s）：%r" % (url, e), "upstream_error")

    def _image(self, action):
        body = self._json_body()
        params = map_image(body, action)
        if not params.get("prompt"):
            return self._err(400, "缺少 prompt 字段")
        if action == "edit" and not params.get("image_urls"):
            return self._err(400, "action=edit 需要 image_urls（网关要求参考图 URL，"
                                  "本地文件请先上传到可访问地址）")
        st, d = a7w_json("POST", "/api/v1/apps/nano_banana/submit", body=params, key=self._key())
        if not ok_of(d):
            return self._err(502, "出图提交失败: %s" % err_msg(d))
        tid = (d.get("data") or {}).get("task_id")
        ok, res = poll_task(tid, app="nano_banana", key=self._key())
        if not ok:
            return self._err(502, "出图任务失败: %s" % json.dumps(res, ensure_ascii=False)[:200])
        urls = find_urls(res)
        if not urls:
            return self._err(502, "出图完成但未找到图片 URL: %s" % json.dumps(res, ensure_ascii=False)[:200])
        return self._send(200, {"created": int(time.time()),
                                "data": [{"url": u} for u in urls]})

    def _passthrough(self, rest):
        """★ 全量应用透传：/a7w/{app}/{code} → /api/v1/apps/{app}/{code}"""
        body = self._json_body()
        st, d = a7w_json("POST", "/api/v1/apps/" + rest, body=body, key=self._key(), timeout=300)
        # 若是异步且调用方要求等待，则轮询到底
        if ok_of(d) and body.get("_wait"):
            tid = (d.get("data") or {}).get("task_id")
            if tid:
                ok, res = poll_task(tid, app=rest.split("/")[0], key=self._key())
                return self._send(200, {"ok": ok, "task": res})
        return self._send(st if st < 400 else 200, d)


def banner(host, port):
    """启动横幅 —— 中文提示放这里，而不是 .cmd 里（cmd 按 ANSI 代码页解析，UTF-8 中文会冲坏脚本）。"""
    line = "=" * 64
    print(line)
    print("  a7w-bridge —— 算力集市全量协议桥")
    print(line)
    print("  上游       : %s" % UPSTREAM)
    print("  Python     : %s" % sys.version.split()[0])
    if LOCAL_KEY:
        print("  API Key    : 已配置（%s***）" % LOCAL_KEY[:3])
    else:
        print("  API Key    : [!] 未配置 —— 这是唯一的必填项")
        print()
        print("      1) 去 https://api.a7w.cn/ 注册并实名")
        print("         ⚠️ 必须用你自己的 Key，不要使用他人分享的 Key")
        print("      2) 用户中心 - API 密钥 创建 Key")
        print("      3) 二选一：")
        print("         a) set A7W_API_KEY=sk-你的key        (Windows)")
        print("            export A7W_API_KEY=sk-你的key     (macOS/Linux)")
        print("         b) 写文件 %s" % os.path.join(os.path.expanduser("~"), ".a7w", "config.json"))
        print('            内容 {"key": "sk-你的key"}')
        print()
        print("      桥仍会启动，但所有调用都会返回 401。")
    if EMBED_BASE:
        print("  embedding  : 外挂转发 -> %s" % EMBED_BASE)
    else:
        print("  embedding  : 未配外挂（/v1/embeddings 返回 501 + 配置指引）")
    print(line)
    print("  客户端 base_url   : http://%s:%d/v1" % (host, port))
    print("  健康检查          : http://%s:%d/health" % (host, port))
    print("  21 个应用全量透传 : http://%s:%d/a7w/{app}/{code}" % (host, port))
    print(line)
    print("  Ctrl+C 停止")
    print()

def main():
    ap = argparse.ArgumentParser(description="a7w-bridge：把算力集市全量能力转成 OpenAI 协议")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()


    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    banner(args.host, args.port)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。", file=sys.stderr)


if __name__ == "__main__":
    main()
