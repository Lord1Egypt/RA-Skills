import base64
import os
from pathlib import Path
from typing import Any, Dict, Tuple

import requests


TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
BASE_API_URL = "https://aip.baidubce.com/rest/2.0/image-classify/v1"


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
        raise RuntimeError(f"Failed to get access_token: {data}")
    return token


def read_image_base64(image_path: str) -> str:
    p = Path(image_path)
    if not p.exists() or not p.is_file():
        raise FileNotFoundError(f"image_path not found: {image_path}")
    return base64.b64encode(p.read_bytes()).decode("utf-8")


def build_image_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    data: Dict[str, Any] = {}

    image_base64 = payload.get("image_base64")
    image_path = payload.get("image_path")
    image_url = payload.get("url")

    if image_base64:
        if image_base64.startswith("data:") and "," in image_base64:
            image_base64 = image_base64.split(",", 1)[1]
        data["image"] = image_base64
    elif image_path:
        data["image"] = read_image_base64(image_path)
    elif image_url:
        data["url"] = image_url
    else:
        raise ValueError("One of image_base64/image_path/url must be provided")

    return data


def clamp_int(value: Any, default: int, min_v: int, max_v: int) -> int:
    if value is None:
        return default
    iv = int(value)
    return max(min_v, min(max_v, iv))


def to_bool_str(value: Any, default: bool = False) -> str:
    if value is None:
        return "true" if default else "false"
    if isinstance(value, bool):
        return "true" if value else "false"
    sval = str(value).strip().lower()
    return "true" if sval in {"1", "true", "yes", "on"} else "false"


def call_image_classify(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    api_url = f"{BASE_API_URL}/{endpoint}"
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
        raise RuntimeError(f"Baidu API error: {result}")
    return result
