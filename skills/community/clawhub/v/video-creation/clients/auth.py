import json
import time
import urllib.request
from typing import Optional, Tuple

API_BASE = "https://open-api.chanjing.cc"

_token_cache = {
    "access_token": None,
    "expire_at": 0,
}


def _load_credentials_from_env() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    import os

    app_id = (os.environ.get("CHANJING_APP_ID") or "").strip()
    secret_key = (os.environ.get("CHANJING_SECRET_KEY") or "").strip()

    if not app_id or not secret_key:
        return None, None, "缺少环境变量 CHANJING_APP_ID 或 CHANJING_SECRET_KEY"

    return app_id, secret_key, None


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
        return None, None, res.get("msg", str(res))

    data = res.get("data") or {}
    token = data.get("access_token")
    expire_in = data.get("expire_in")

    if not token:
        return None, None, "返回中缺少 access_token"

    return str(token), expire_in, None


def get_token() -> Tuple[Optional[str], Optional[str]]:
    now = int(time.time())

    cached_token = _token_cache["access_token"]
    expire_at = int(_token_cache["expire_at"] or 0)

    if cached_token and now < expire_at - 60:
        return cached_token, None

    app_id, secret_key, err = _load_credentials_from_env()
    if err:
        return None, err

    token, new_expire_at, err = _request_token(app_id, secret_key)
    if err:
        return None, err

    _token_cache["access_token"] = token
    _token_cache["expire_at"] = int(new_expire_at or (now + 86400))

    return token, None