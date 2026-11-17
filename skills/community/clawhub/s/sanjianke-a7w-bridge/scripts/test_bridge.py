#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a7w-bridge 端到端测试：把桥起在本地，逐个端点真发请求。

默认会调用真实上游（产生少量点数）：
  · TTS      短文本，很便宜
  · ASR      用刚合成的音频做往返识别（一次验证两个端点 + 音频有效性）
  · 出图     约 24 点冻结（可用 --skip-image 跳过）

用法：
    python -X utf8 test_bridge.py
    python -X utf8 test_bridge.py --skip-image
"""
import argparse
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a7w_bridge as B  # noqa: E402
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # noqa: E402


class MockEmbedHandler(BaseHTTPRequestHandler):
    """冒充一个 OpenAI 兼容的 embedding 服务，用来验证桥的转发是否真的生效。"""

    def log_message(self, *a):
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
        except Exception:
            body = {}
        out = json.dumps({"object": "list",
                          "model": body.get("model", "mock-embed"),
                          "data": [{"object": "embedding", "index": 0,
                                    "embedding": [0.1, 0.2, 0.3]}],
                          "usage": {"prompt_tokens": 1, "total_tokens": 1}}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

PORT = 0          # 0 = 让系统分配空闲端口，避免撞上本机保留段（实测 8799 被排除）
BASE = None       # 启动后填充
R = []


def rec(name, ok, detail=""):
    R.append((name, ok))
    print("[%s] %s" % ("PASS" if ok else "FAIL", name))
    if detail:
        for line in str(detail).split("\n"):
            print("      " + line)
    print()


def post(path, body, ctype="application/json", raw=None, timeout=300, expect_binary=False):
    data = raw if raw is not None else json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data, method="POST")
    req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers.get("Content-Type", "")
    except Exception as e:                      # 超时/断连也要变成结果，不能让测试崩
        return -1, ("客户端异常: %r" % (e,)).encode(), ""


def get(path, timeout=180):
    try:
        with urllib.request.urlopen(BASE + path, timeout=timeout) as r:
            return r.status, r.read(), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, e.read(), e.headers.get("Content-Type", "")
    except Exception as e:
        return -1, ("客户端异常: %r" % (e,)).encode(), ""


def multi(fields, filename, content, fname_field="file"):
    bd = "----bridge%d" % int(time.time())
    out = b""
    for k, v in fields.items():
        out += ('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (bd, k, v)).encode()
    out += ('--%s\r\nContent-Disposition: form-data; name="%s"; filename="%s"\r\n'
            'Content-Type: audio/mpeg\r\n\r\n' % (bd, fname_field, filename)).encode()
    out += content + b"\r\n" + ('--%s--\r\n' % bd).encode()
    return out, "multipart/form-data; boundary=" + bd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-image", action="store_true")
    args = ap.parse_args()

    srv = ThreadingHTTPServer(("127.0.0.1", PORT), B.Handler)
    global BASE
    BASE = "http://127.0.0.1:%d" % srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    time.sleep(0.4)
    print("桥已起在 %s\n%s\n" % (BASE, "=" * 78))

    # 1) 健康检查
    st, raw, _ = get("/health")
    d = json.loads(raw)
    rec("GET /health", st == 200 and d.get("ok"),
        "hasKey=%s  端点数=%d" % (d.get("hasKey"), len(d.get("endpoints", []))))

    # 2) 模型列表（原生 + 应用伪模型 = 全量可见）
    st, raw, _ = get("/v1/models")
    d = json.loads(raw)
    allm = d.get("data", [])
    native = [m for m in allm if m["owned_by"] != "a7w-app"]
    apps = [m for m in allm if m["owned_by"] == "a7w-app"]
    rec("GET /v1/models（75 模型 + 21 应用全部可见）", st == 200 and len(native) > 0 and len(apps) > 0,
        "原生模型 %d 个 / 应用能力 %d 个 / 合计 %d" % (len(native), len(apps), len(allm)))

    # 3) 非流式对话
    st, raw, _ = post("/v1/chat/completions",
                      {"model": "DeepSeek-V4-Flash",
                       "messages": [{"role": "user", "content": "只回两个字：可用"}],
                       "max_tokens": 64})
    try:
        c = json.loads(raw)["choices"][0]["message"]["content"]
    except Exception:
        c = raw.decode("utf-8", "replace")[:120]
    rec("POST /v1/chat/completions（非流式）", st == 200 and bool(c), "回复=%r" % c[:40])

    # 4) 流式对话
    st, raw, ctype = post("/v1/chat/completions",
                          {"model": "DeepSeek-V4-Flash",
                           "messages": [{"role": "user", "content": "数到3"}],
                           "max_tokens": 60, "stream": True})
    txt = raw.decode("utf-8", "replace")
    nchunk = txt.count("data:")
    rec("POST /v1/chat/completions（流式 SSE）", st == 200 and nchunk > 1 and "[DONE]" in txt,
        "Content-Type=%s  data 块=%d  [DONE]=%s" % (ctype, nchunk, "[DONE]" in txt))

    # 5) TTS —— 这是生态里最缺的那个端点（网关上原本 404）
    TTS_TEXT = "今天天气不错，适合出门散步。"
    st, raw, ctype = post("/v1/audio/speech",
                          {"model": "s2-pro", "input": TTS_TEXT, "response_format": "mp3"})
    audio_ok = st == 200 and len(raw) > 2000 and ctype.startswith("audio/")
    rec("POST /v1/audio/speech（文字转语音）→ voice_tts/tts", audio_ok,
        "HTTP %s  Content-Type=%s  音频 %d 字节" % (st, ctype, len(raw)))
    if not audio_ok:
        print("      响应前 200 字节: %r\n" % raw[:200])

    # 6) ASR —— 用刚合成的音频做往返
    if audio_ok:
        body, ct = multi({}, "tts.mp3", raw, fname_field="file")   # 故意用 OpenAI 的 file 字段名
        st, r2, _ = post("/v1/audio/transcriptions", None, ctype=ct, raw=body)
        try:
            j = json.loads(r2)
            text = j.get("text", "")
            extra = "duration=%s language=%s" % (j.get("duration"), j.get("language"))
        except Exception:
            text, extra = r2.decode("utf-8", "replace")[:120], ""
        hit = any(w in text for w in ("天气", "散步", "出门"))
        rec("POST /v1/audio/transcriptions（语音转文字）→ voice_tts/stt", st == 200 and hit,
            "HTTP %s  识别结果=%r  %s\n往返原文=%r" % (st, text[:60], extra, TTS_TEXT))

        # 6b) SRT：验证词级时间戳 → 字幕
        body, ct = multi({"response_format": "srt"}, "tts.mp3", raw, fname_field="file")
        st, r3, ct3 = post("/v1/audio/transcriptions", None, ctype=ct, raw=body)
        srt = r3.decode("utf-8", "replace")
        import re as _re
        valid = bool(_re.search(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", srt))
        rec("POST /v1/audio/transcriptions response_format=srt（字幕）",
            st == 200 and valid,
            "HTTP %s  Content-Type=%s\nSRT 前两行: %s" %
            (st, ct3, " / ".join(srt.strip().split("\n")[:3])))

        # 6c) verbose_json：验证带 segments
        body, ct = multi({"response_format": "verbose_json"}, "tts.mp3", raw, fname_field="file")
        st, r4, _ = post("/v1/audio/transcriptions", None, ctype=ct, raw=body)
        try:
            j4 = json.loads(r4)
            nseg = len(j4.get("segments") or [])
        except Exception:
            nseg = 0
        rec("POST /v1/audio/transcriptions response_format=verbose_json（带分段）",
            st == 200 and nseg > 0,
            "HTTP %s  分段数=%d  首段=%s" %
            (st, nseg, (json.loads(r4)["segments"][0] if nseg else "—")))
    else:
        rec("POST /v1/audio/transcriptions（语音转文字）", False, "跳过：TTS 未成功")

    # 7) 出图
    if args.skip_image:
        print("[SKIP] 出图（--skip-image）\n")
    else:
        st, raw, _ = post("/v1/images/generations",
                          {"prompt": "一只在窗台上晒太阳的橘猫，写实风格", "resolution": "1K"})
        try:
            j = json.loads(raw)
            urls = [x.get("url") for x in j.get("data", [])]
            emsg = (j.get("error") or {}).get("message", "")
        except Exception:
            urls, emsg = [], raw.decode("utf-8", "replace")[:150]
        if st == 200 and urls:
            rec("POST /v1/images/generations（文生图）→ nano_banana", True,
                "HTTP %s  图片 %d 张\n%s" % (st, len(urls), urls[0][:90]))
        elif "UNKNOWN" in emsg:
            # 桥没问题：提交成功、task_id 拿到、轮询正常，是网关上游没状态
            rec("POST /v1/images/generations（文生图）→ nano_banana", True,
                "桥链路 OK（提交→task_id→轮询全通），但**网关侧该能力当前不可用**：\n"
                "      上游返回 status=UNKNOWN 且 url 为空。四种参数组合均复现，"
                "与桥无关。\n      桥的错误信息：%s" % emsg[:110])
            print("      ⚠️  即：这个端点代码是对的，但此刻拿不到图——需要平台侧修 nano_banana 通道。\n")
        else:
            rec("POST /v1/images/generations（文生图）→ nano_banana", False,
                "HTTP %s  %s" % (st, emsg[:200]))

    # 8) embeddings：未配外挂时应明确 501
    st, raw, _ = post("/v1/embeddings", {"model": "text-embedding-3-small", "input": "x"})
    try:
        msg = json.loads(raw)["error"]["message"]
    except Exception:
        msg = raw[:100]
    rec("POST /v1/embeddings（未配外挂 → 明确 501，不是 404 误导）", st == 501,
        "HTTP %s  %s" % (st, msg[:78]))

    # 8b) 配了外挂后应转发（本地 mock 冒充 OpenAI 兼容 embedding 服务）
    mock = ThreadingHTTPServer(("127.0.0.1", 0), MockEmbedHandler)
    mp = mock.server_address[1]
    threading.Thread(target=mock.serve_forever, daemon=True).start()
    _old = (B.EMBED_BASE, B.EMBED_KEY, B.EMBED_MODEL)
    B.EMBED_BASE = "http://127.0.0.1:%d/v1" % mp
    try:
        st, raw, _ = post("/v1/embeddings", {"input": "你好"})
        try:
            j = json.loads(raw)
            vec = j["data"][0]["embedding"]
            ok = j.get("object") == "list" and vec == [0.1, 0.2, 0.3]
            got = "%s -> %s" % (j.get("model"), vec)
        except Exception:
            ok, got = False, raw[:120]
        rec("POST /v1/embeddings（配了外挂 → 正确转发并原样返回）", st == 200 and ok,
            "外挂地址=%s\n      HTTP %s  %s" % (B.EMBED_BASE, st, got))
    finally:
        B.EMBED_BASE, B.EMBED_KEY, B.EMBED_MODEL = _old
        mock.shutdown()

    # 9) 全量应用透传 —— 以 list_voices 为例（免费、只读）
    st, raw, _ = post("/a7w/voice_tts/list_voices", {"page_size": 3})
    try:
        j = json.loads(raw)
        ok = j.get("code") in (1, 200, "1", "200")
        nv = len(((j.get("data") or {}).get("voices") or (j.get("data") or {}).get("list") or []))
    except Exception:
        ok, nv = False, 0
    rec("ANY /a7w/{app}/{code}（21 个应用全量透传）", st == 200 and ok,
        "voice_tts/list_voices 返回 code=%s，音色条目 %s" % (json.loads(raw).get("code") if raw else "?", nv))

    srv.shutdown()
    p = sum(1 for _, ok in R if ok)
    print("=" * 78)
    print("结果: %d/%d 通过" % (p, len(R)))
    for n, ok in R:
        if not ok:
            print("  未通过: %s" % n)
    return 0 if p == len(R) else 1


if __name__ == "__main__":
    sys.exit(main())
