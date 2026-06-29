# -*- coding: utf-8 -*-
"""
获取并缓存微信公众号 access_token
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), "config.json")
CACHE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), ".cache")
TOKEN_CACHE_PATH = os.path.join(CACHE_DIR, "access_token.json")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_access_token(force_refresh=False):
    os.makedirs(CACHE_DIR, exist_ok=True)

    if not force_refresh and os.path.exists(TOKEN_CACHE_PATH):
        with open(TOKEN_CACHE_PATH, "r", encoding="utf-8") as f:
            cache = json.load(f)
        if cache.get("expires_at", 0) > time.time() + 300:
            return cache["access_token"]

    cfg = load_config()
    appid = cfg["appid"]
    appsecret = cfg["appsecret"]

    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8") if e.fp else str(e)
        print(f"HTTP错误: {e.code} - {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"网络错误: {e}", file=sys.stderr)
        sys.exit(1)

    if "access_token" not in data:
        err_msg = data.get("errmsg", str(data))
        print(f"获取token失败: {err_msg}", file=sys.stderr)
        sys.exit(1)

    token = data["access_token"]
    expires_in = data.get("expires_in", 7200)

    cache_data = {"access_token": token, "expires_at": time.time() + expires_in}
    with open(TOKEN_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)

    return token


if __name__ == "__main__":
    force = "--force" in sys.argv
    token = get_access_token(force_refresh=force)
    print(token)
