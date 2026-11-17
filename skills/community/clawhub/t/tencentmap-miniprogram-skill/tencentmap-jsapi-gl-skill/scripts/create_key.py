#!/usr/bin/env python3
"""
create_key.py — 校验短信验证码并创建/获取 Key

用法:
    python create_key.py <phone> <verify_code> <session_token>

成功输出（三种 type）:
    {"error": 0, "type": "created", "key": "xxx", "expire_time": "2027-07-17 19:59:59"}
    {"error": 0, "type": "created", "key": "xxx", "expire_time": "...", "is_existing": true}
    {"error": 0, "type": "reused",  "key": "xxx", "expire_time": "...", "is_existing": true}
    {"error": 0, "type": "select",  "key_list": [...], "supplement_token": "...", "supplement_token_expire": 300}

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
API_URL = f"https://{API_HOST}/nosession/http/skill/v2/tempkey/create"
SCENE = 1  # 固定 Skill 场景


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


def create_key(phone: str, verify_code: str, session_token: str) -> dict:
    payload = json.dumps({
        "customer_phone": phone,
        "verify_code": verify_code,
        "session_token": session_token,
        "scene": SCENE,
    }).encode("utf-8")
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
        # 响应结构：{"info":{"error":0,"msg":"成功"},"detail":{...业务字段...}}
        data = body.get("detail") or {}
        resp_type = data.get("type", "")
        result = {"error": 0, "type": resp_type}
        if resp_type in ("created", "reused"):
            result["key"] = data.get("key", "")
            result["expire_time"] = data.get("expire_time", "")
            if "is_existing" in data:
                result["is_existing"] = data["is_existing"]
        elif resp_type == "select":
            result["key_list"] = data.get("key_list", [])
            result["supplement_token"] = data.get("supplement_token", "")
            result["supplement_token_expire"] = data.get("supplement_token_expire", 300)
        return result
    else:
        return {"error": ret, "msg": info.get("msg", "UNKNOWN")}


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(json.dumps(
            {"error": -1, "msg": "用法: create_key.py <phone> <verify_code> <session_token>"},
            ensure_ascii=False
        ))
        sys.exit(1)

    result = create_key(sys.argv[1], sys.argv[2], sys.argv[3])
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["error"] == 0 else 1)
