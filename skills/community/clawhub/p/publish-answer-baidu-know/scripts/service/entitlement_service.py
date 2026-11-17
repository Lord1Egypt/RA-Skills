"""在线鉴权（可选模板）。"""

from __future__ import annotations

import os
from typing import Tuple

import requests


def check_entitlement(skill_slug: str) -> Tuple[bool, str]:
    auth_base = (os.getenv("JIANGCHANG_AUTH_BASE_URL") or "").strip().rstrip("/")
    if not auth_base:
        return True, ""
    user_id = (os.getenv("JIANGCHANG_USER_ID") or "").strip()
    if not user_id:
        return False, "鉴权失败：缺少用户身份（JIANGCHANG_USER_ID）"

    auth_api_key = (os.getenv("JIANGCHANG_AUTH_API_KEY") or "").strip()
    timeout = int((os.getenv("JIANGCHANG_AUTH_TIMEOUT_SECONDS") or "5").strip())
    headers = {"Content-Type": "application/json"}
    if auth_api_key:
        headers["Authorization"] = f"Bearer {auth_api_key}"
    payload = {
        "user_id": user_id,
        "skill_slug": skill_slug,
        "trace_id": (os.getenv("JIANGCHANG_TRACE_ID") or "").strip(),
        "context": {"entry": "main.py"},
    }
    try:
        res = requests.post(f"{auth_base}/api/entitlements/check", json=payload, headers=headers, timeout=timeout)
    except requests.RequestException as exc:
        return False, f"鉴权请求失败：{exc}"
    if res.status_code != 200:
        return False, f"鉴权服务异常：HTTP {res.status_code}"
    try:
        body = res.json()
    except ValueError:
        return False, "鉴权服务异常：返回非 JSON"
    code = body.get("code")
    data = body.get("data") or {}
    if code != 200:
        return False, str(body.get("msg") or "鉴权失败")
    if not data.get("allow", False):
        return False, str(data.get("reason") or "未购买或已过期")
    return True, ""
