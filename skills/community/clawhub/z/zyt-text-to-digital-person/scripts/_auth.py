#!/usr/bin/env python3
import json
import os
import time
import urllib.request
from pathlib import Path

CONFIG_DIR = Path(os.environ.get("CHANJING_CONFIG_DIR", Path.home() / ".chanjing"))
CONFIG_FILE = CONFIG_DIR / "credentials.json"
API_BASE = "https://open-api.chanjing.cc"
BUFFER_SECONDS = 300
LOGIN_URL = "https://www.chanjing.cc/openapi/login"
AUTO_OPEN_LOGIN = os.environ.get("CHANJING_AUTO_OPEN_LOGIN", "").strip().lower() in {"1", "true", "yes", "on"}

NO_CREDENTIALS_MSG = """缺少 AK/SK 本地凭证。
请先在 ~/.chanjing/credentials.json（或 $CHANJING_CONFIG_DIR/credentials.json）中配置：
  {
    "app_id": "<你的app_id>",
    "secret_key": "<你的secret_key>"
  }
登录页：https://www.chanjing.cc/openapi/login
配置完成后请重新执行您之前的操作。"""

INVALID_CREDENTIALS_MSG = """AK/SK 无效或已过期。
请重新获取 app_id 和 secret_key，并更新 ~/.chanjing/credentials.json
（或 $CHANJING_CONFIG_DIR/credentials.json）后重试。
登录页：https://www.chanjing.cc/openapi/login"""


def _run_open_login_page():
    if not AUTO_OPEN_LOGIN:
        return
    try:
        import webbrowser

        webbrowser.open(LOGIN_URL)
    except Exception:
        pass


def read_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def write_config(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(CONFIG_DIR, 0o700)
    except Exception:
        pass
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    try:
        os.chmod(CONFIG_FILE, 0o600)
    except Exception:
        pass


def clear_cached_token():
    data = read_config()
    data.pop("access_token", None)
    data.pop("expire_in", None)
    write_config(data)


def _request_new_token(app_id, secret_key):
    url = API_BASE + "/open/v1/access_token"
    req = urllib.request.Request(
        url,
        data=json.dumps({"app_id": app_id, "secret_key": secret_key}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_token(force_refresh=False):
    data = read_config()
    app_id = (data.get("app_id") or "").strip()
    secret_key = (data.get("secret_key") or "").strip()
    if not app_id or not secret_key:
        _run_open_login_page()
        return None, NO_CREDENTIALS_MSG

    now = int(time.time())
    token = (data.get("access_token") or "").strip()
    expire_in = data.get("expire_in")
    try:
        expire_in = int(expire_in) if expire_in is not None else 0
    except (ValueError, TypeError):
        expire_in = 0

    if (not force_refresh) and token and expire_in > now + BUFFER_SECONDS:
        return token, None

    try:
        body = _request_new_token(app_id, secret_key)
    except Exception as e:
        return None, str(e)

    if body.get("code") != 0:
        _run_open_login_page()
        return None, INVALID_CREDENTIALS_MSG

    payload = body.get("data", {})
    new_token = payload.get("access_token")
    if not new_token:
        _run_open_login_page()
        return None, INVALID_CREDENTIALS_MSG

    data["access_token"] = new_token
    data["expire_in"] = payload.get("expire_in")
    write_config(data)
    return new_token, None
