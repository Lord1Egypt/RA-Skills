# -*- coding: utf-8 -*-
"""
ClawHub device-flow 登录助手（沙箱内可读验证码的版本）。

为什么需要它：
  `clawhub login` 是交互式 CLI，在沙箱后台运行时 stdout 被管道缓冲，
  取不到 user_code。此脚本直接调 ClawHub 的 device flow API，把 user_code
  写进文件，然后轮询换取 token 并落盘到 %APPDATA%\\clawhub\\config.json。

用法：
  python clawhub_device_login.py request   # 申请设备码，写入 device_code.json
  python clawhub_device_login.py poll      # 轮询直到授权成功，写入 token 到 config.json
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
import ssl

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "clawhub_device_code.json")
GRANT = "urn:ietf:params:oauth:grant-type:device_code"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def post(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            return r.status, json.loads(r.read().decode("utf-8", "ignore"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"raw": body}


def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            return r.status, json.loads(r.read().decode("utf-8", "ignore"))
    except Exception as e:
        return "ERR", {"error": str(e)[:200]}


def discover(site):
    for path in ("/.well-known/clawhub.json", "/.well-known/clawdhub.json"):
        st, body = get(site.rstrip("/") + path)
        if st == 200:
            api = body.get("apiBase") or body.get("registry")
            return api, body.get("authBase") or site
    return None, None


def config_path():
    base = os.environ.get("APPDATA") or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, "clawhub", "config.json")


def cmd_request():
    site = os.environ.get("CLAWHUB_SITE", "https://clawhub.ai")
    api_base, auth_base = discover(site)
    registry = api_base or site
    payload = {"scope": "read write", "site_url": auth_base, "label": "WorkBuddy CLI (agent)"}
    st, body = post(registry.rstrip("/") + "/api/cli/device/code", payload)
    out = {
        "status": st,
        "registry": registry,
        "auth_base": auth_base,
        "request": payload,
        "response": body,
    }
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2)[:1200])


def cmd_poll():
    with open(STATE, encoding="utf-8") as f:
        saved = json.load(f)
    resp = saved.get("response") or {}
    device_code = resp.get("device_code")
    if not device_code:
        print("NO_DEVICE_CODE: 先跑 request")
        return 1
    registry = saved["registry"].rstrip("/")
    interval = float(resp.get("interval") or 5)
    expires_in = float(resp.get("expires_in") or 900)
    deadline = time.time() + expires_in
    url = registry + "/api/cli/device/token"
    last = None
    while time.time() < deadline:
        time.sleep(interval)
        st, body = post(url, {"device_code": device_code, "grant_type": GRANT})
        if st == 200 and body.get("access_token"):
            token = body["access_token"]
            cfg_path = config_path()
            os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
            existing = {}
            if os.path.exists(cfg_path):
                try:
                    with open(cfg_path, encoding="utf-8") as f:
                        existing = json.load(f)
                except Exception:
                    existing = {}
            existing["registry"] = saved.get("registry")
            existing["token"] = token
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(existing, f, ensure_ascii=False, indent=2)
            print("LOGGED_IN")
            print("config:", cfg_path)
            print("token_prefix:", token[:8] + "..." + " (len %d)" % len(token))
            return 0
        err = (body or {}).get("error")
        if err == "slow_down":
            interval += 5
        elif err in ("expired_token",):
            print("EXPIRED")
            return 2
        elif err == "access_denied":
            print("DENIED")
            return 3
        if err != last:
            print("pending:", err or st, flush=True)
            last = err
    print("TIMEOUT")
    return 4


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "request"
    sys.exit(cmd_request() if mode == "request" else cmd_poll())
