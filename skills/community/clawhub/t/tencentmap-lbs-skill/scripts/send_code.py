#!/usr/bin/env python3
"""
send_code.py — 发送短信验证码

用法:
    python send_code.py <phone>

成功输出:
    {"error": 0, "session_token": "sk_xxx"}

失败输出:
    {"error": <code>, "msg": "<描述>"}
"""

import sys
import json
import time
import random
import urllib.request
import urllib.error

API_URL = "https://lbsconsole.map.qq.com/nosession/http/skill/auth/send-code"


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
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = json.loads(e.read().decode("utf-8"))
    except Exception as e:
        return {"error": -1, "msg": f"网络异常: {e}"}

    error = body.get("info", {}).get("error", -1)
    if error == 0:
        return {"error": 0, "session_token": body["detail"]["session_token"]}
    else:
        return {"error": error, "msg": body.get("info", {}).get("msg", "未知错误")}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": -1, "msg": "用法: send_code.py <phone>"}, ensure_ascii=False))
        sys.exit(1)

    result = send_code(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["error"] == 0 else 1)
