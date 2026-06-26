import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Optional, Tuple

API_BASE = os.environ.get("CHANJING_API_BASE", "https://open-api.chanjing.cc")
CONFIG_DIR = Path(os.environ.get("CHANJING_CONFIG_DIR", Path.home() / ".chanjing"))
CONFIG_FILE = CONFIG_DIR / "credentials.json"
BUFFER_SECONDS = 300
LOGIN_URL = "https://www.chanjing.cc/openapi/login"

_token_cache = {
    "access_token": None,
    "expire_at": 0,
}


def _run_open_login_page() -> None:
    try:
        import webbrowser

        webbrowser.open(LOGIN_URL)
    except Exception:
        pass


def read_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}


def write_config(data: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def clear_cached_token() -> None:
    _token_cache["access_token"] = None
    _token_cache["expire_at"] = 0
    data = read_config()
    data.pop("access_token", None)
    data.pop("expire_in", None)
    write_config(data)


def is_token_invalid(body: dict) -> bool:
    code = body.get("code")
    msg = str(body.get("msg", ""))
    return code == 10400 or "AccessToken已失效" in msg or "AccessToken verification failed" in msg


def _load_credentials() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    data = read_config()
    app_id = (data.get("app_id") or "").strip()
    secret_key = (data.get("secret_key") or "").strip()
    if app_id and secret_key:
        return app_id, secret_key, None

    _run_open_login_page()
    return (
        None,
        None,
        "缺少凭证。请在 ~/.chanjing/credentials.json（或 $CHANJING_CONFIG_DIR/credentials.json）配置 app_id/secret_key。",
    )


def _request_token(
    app_id: str, secret_key: str
) -> Tuple[Optional[str], Optional[int], Optional[str]]:
    url = f"{API_BASE}/open/v1/access_token"
    body = json.dumps(
        {
            "app_id": app_id,
            "secret_key": secret_key,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            res = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return None, None, f"获取 access_token 失败: {e}"

    if res.get("code") != 0:
        _run_open_login_page()
        return None, None, res.get("msg", str(res))

    data = res.get("data") or {}
    token = data.get("access_token")
    expire_in = data.get("expire_in")

    if not token:
        return None, None, "返回中缺少 access_token"

    return str(token), expire_in, None


def get_token(force_refresh: bool = False) -> Tuple[Optional[str], Optional[str]]:
    now = int(time.time())

    cached_token = _token_cache["access_token"]
    expire_at = int(_token_cache["expire_at"] or 0)

    if (not force_refresh) and cached_token and now < expire_at - BUFFER_SECONDS:
        return cached_token, None

    data = read_config()
    file_token = str(data.get("access_token") or "").strip()
    try:
        file_expire = int(data.get("expire_in") or 0)
    except (TypeError, ValueError):
        file_expire = 0
    if (not force_refresh) and file_token and now < file_expire - BUFFER_SECONDS:
        _token_cache["access_token"] = file_token
        _token_cache["expire_at"] = file_expire
        return file_token, None

    app_id, secret_key, err = _load_credentials()
    if err:
        return None, err

    token, new_expire_at, err = _request_token(app_id, secret_key)
    if err:
        return None, err

    _token_cache["access_token"] = token
    _token_cache["expire_at"] = int(new_expire_at or (now + 86400))
    data["app_id"] = app_id
    data["secret_key"] = secret_key
    data["access_token"] = token
    data["expire_in"] = int(new_expire_at or (now + 86400))
    write_config(data)

    return token, None