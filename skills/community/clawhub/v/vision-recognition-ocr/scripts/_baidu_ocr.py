import json
import os
from typing import Any, Dict, Tuple

import requests


TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
BASE_OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1"


def pick_oauth_credentials() -> Tuple[str, str]:
    api_key = os.getenv("BAIDU_VISION_API_KEY") or os.getenv("BAIDU_API_KEY")
    secret_key = os.getenv("BAIDU_VISION_SECRET_KEY") or os.getenv("BAIDU_SECRET_KEY")
    if not api_key or not secret_key:
        raise RuntimeError(
            "Missing OAuth credentials: set BAIDU_VISION_API_KEY/BAIDU_VISION_SECRET_KEY or BAIDU_API_KEY/BAIDU_SECRET_KEY"
        )
    return api_key, secret_key


def pick_bearer_token() -> str:
    return (
        os.getenv("BAIDU_BCE_BEARER_TOKEN")
        or os.getenv("BAIDU_BCE_BEARER")
        or os.getenv("BAIDU_API_KEY", "")
    )


def get_access_token(api_key: str, secret_key: str) -> str:
    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key,
    }
    resp = requests.post(TOKEN_URL, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError(f"Failed to get access_token: {json.dumps(data, ensure_ascii=False)}")
    return token


def to_bool_str(value: Any, default: bool = False) -> str:
    if value is None:
        return "true" if default else "false"
    if isinstance(value, bool):
        return "true" if value else "false"
    sval = str(value).strip().lower()
    return "true" if sval in {"1", "true", "yes", "on"} else "false"


def call_ocr(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    api_url = f"{BASE_OCR_URL}/{endpoint}"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}

    bearer = pick_bearer_token()
    if bearer.startswith("bce-v3/"):
        headers["Authorization"] = f"Bearer {bearer}"
        resp = requests.post(api_url, headers=headers, data=data, timeout=30)
    else:
        api_key, secret_key = pick_oauth_credentials()
        token = get_access_token(api_key, secret_key)
        resp = requests.post(f"{api_url}?access_token={token}", headers=headers, data=data, timeout=30)

    resp.raise_for_status()
    result = resp.json()
    if "error_code" in result:
        raise RuntimeError(f"Baidu OCR API error: {json.dumps(result, ensure_ascii=False)}")
    return result
