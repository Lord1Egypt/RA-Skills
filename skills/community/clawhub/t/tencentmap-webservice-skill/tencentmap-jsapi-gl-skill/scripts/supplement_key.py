#!/usr/bin/env python3
"""
supplement_key.py — 补额 / 新建 Key（supplement 接口）

用法:
    python supplement_key.py <supplement_token> reuse <mkey>
    python supplement_key.py <supplement_token> create

成功输出:
    {"error": 0, "type": "reused",  "key": "xxx", "expire_time": "...", "is_existing": true}   # action=reuse
    {"error": 0, "type": "created", "key": "xxx", "expire_time": "..."}                        # action=create

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
API_URL = f"https://{API_HOST}/nosession/http/skill/v2/tempkey/supplement"


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


def supplement(supplement_token: str, action: str, mkey: str = "") -> dict:
    payload = {"supplement_token": supplement_token, "action": action}
    if action == "reuse":
        if not mkey:
            return {"error": -1, "msg": "action=reuse 时必须提供 mkey"}
        payload["mkey"] = mkey
    payload_bytes = json.dumps(payload).encode("utf-8")
    headers = make_headers()

    req = urllib.request.Request(API_URL, data=payload_bytes, headers=headers, method="POST")
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
        result = {
            "error": 0,
            "type": data.get("type", ""),
            "key": data.get("key", ""),
            "expire_time": data.get("expire_time", ""),
        }
        if "is_existing" in data:
            result["is_existing"] = data["is_existing"]
        return result
    else:
        return {"error": ret, "msg": info.get("msg", "UNKNOWN")}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps(
            {"error": -1, "msg": "用法: supplement_key.py <supplement_token> reuse <mkey>  |  supplement_key.py <supplement_token> create"},
            ensure_ascii=False
        ))
        sys.exit(1)

    token = sys.argv[1]
    action = sys.argv[2]
    mkey = sys.argv[3] if len(sys.argv) > 3 else ""

    if action not in ("reuse", "create"):
        print(json.dumps({"error": -1, "msg": "action 必须为 reuse 或 create"}, ensure_ascii=False))
        sys.exit(1)

    result = supplement(token, action, mkey)
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["error"] == 0 else 1)
