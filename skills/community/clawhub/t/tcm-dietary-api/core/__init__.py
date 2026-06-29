"""
core/__init__.py — 中医食疗辨证 API 客户端 (v1.0.0)

tcm-dietary-api: 远程 API 客户端，不是本地知识库。
所有查询通过 HTTPS 发送到 api.tcmplate.com 处理。

Usage:
    import core
    from core.diagnose import diagnose
    result = diagnose(["头晕", "乏力", "失眠"])  # 免费, 无需 API Key

    core.set_api_key("tcm_xxxx")  # 付费 $5/月, 不限次数

API Base: https://api.tcmplate.com
Subscribe: https://api.tcmplate.com/subscribe
Privacy: https://tcmplate.com/privacy
"""

__version__ = "1.0.0"

import urllib.request
import json as _json

API_BASE = "https://api.tcmplate.com"
api_key = None

# 字段白名单 — 只发送必要数据, 不在代码层面泄露用户信息
_ALLOWED_FIELDS = {
    "symptoms", "language", "gender",
    "category", "keywords",
    "constitution", "dietary_preference",
    "dish_name", "meal_type", "dishes",
}


def _sanitize_payload(data: dict) -> dict:
    """白名单过滤: 仅允许 API 需要的字段通过, 拦截意外传入的个人信息."""
    if not isinstance(data, dict):
        return data
    return {k: v for k, v in data.items() if k in _ALLOWED_FIELDS}


def set_api_key(key: str):
    """设置付费 API Key. 免费层不需要."""
    global api_key
    api_key = key


def _api_request(method: str, path: str, body: dict = None, timeout: int = 30) -> dict:
    """
    发送 API 请求.
    免费层: 不发送 Authorization header.
    付费层: 发送 Bearer token.
    所有请求: HTTPS 加密, 字段白名单过滤.
    """
    url = f"{API_BASE}{path}"
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    data = None
    if body is not None:
        sanitized = _sanitize_payload(body)
        data = _json.dumps(sanitized).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    resp = urllib.request.urlopen(req, timeout=timeout)
    return _json.loads(resp.read().decode("utf-8"))
