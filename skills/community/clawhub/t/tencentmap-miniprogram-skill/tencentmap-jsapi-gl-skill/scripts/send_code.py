#!/usr/bin/env python3
"""
send_code.py — 发送短信验证码

用法:
    python send_code.py <phone>

成功输出:
    {"error": 0, "session_token": "sk_xxx"}

失败输出:
    {"error": <code>, "msg": "<错误码字符串>"}
"""

import sys
import json
import time
import random
import ssl
import urllib.request
import urllib.error

# 修复 macOS Python SSL 证书问题：优先使用 certifi 的 CA bundle
try:
    import certifi
    _SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CONTEXT = ssl.create_default_context()

API_HOST = "lbsconsole.map.qq.com"
API_URL = f"https://{API_HOST}/nosession/http/skill/auth/send-code"


def make_headers():
    ts = str(int(time.time()))
    nonce = ts + format(random.getrandbits(32), "08x")
    return {
        "Content-Type": "application/json",
        "X-Skill-Timestamp": ts,
        "X-Skill-Nonce": nonce,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://lbs.qq.com/",
    }


def send_code(phone: str) -> dict:
    payload = json.dumps({"customer_phone": phone}).encode("utf-8")
    headers = make_headers()

    req = urllib.request.Request(API_URL, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10, context=_SSL_CONTEXT) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            return {"error": -1, "msg": f"HTTP {e.code}"}
    except Exception as e:
        return {"error": -1, "msg": f"网络异常: {e}"}

    info = body.get("info") or {}
    ret = info.get("error", -1)
    if ret == 0:
        # 响应结构：{"info":{"error":0,"msg":"成功"},"detail":{"session_token":"sk_xxx"}}
        detail = body.get("detail") or {}
        return {"error": 0, "session_token": detail.get("session_token", "")}
    else:
        return {"error": ret, "msg": info.get("msg", "UNKNOWN")}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": -1, "msg": "用法: send_code.py <phone>"}, ensure_ascii=False))
        sys.exit(1)

    result = send_code(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["error"] == 0 else 1)
