"""
error_taxonomy.py
=================
Canonical WotoHub error classification and structured error builder.

All script errors are routed through here so error codes, messages,
retry hints, and API error classification are consistent.
"""

from typing import Any, Optional


# ── Internal error codes ────────────────────────────────────────────────────────

INTERNAL_CODES = {
    "SCRIPT_ERROR":            "脚本执行异常，详见 details",
    "PRODUCT_CONTEXT_MISSING": "产品语义信息不足，无法构建有效搜索条件",
    "PAYLOAD_BUILD_FAILED":    "无法从输入构建有效搜索 payload",
    "TOKEN_MISSING":           "未提供有效 Token，无法执行需要鉴权的操作",
    "TOKEN_INVALID":           "Token 无效或已过期",
    "NETWORK_ERROR":           "网络请求失败",
    "API_ERROR":               "WotoHub API 返回异常",
    "NO_SEARCH_RESULTS":       "搜索返回 0 条结果",
    "FALLBACK_EXHAUSTED":      "所有 fallback 策略均失败",
}


# ── API error code classification ─────────────────────────────────────────────

# WotoHub error codes that are retryable (transient)
RETRYABLE_API_CODES = {
    "1001",  # rate limit
    "1002",  # server busy
    "1003",  # timeout
    "1005",  # service unavailable
    "1007",  # gateway timeout
}

# Codes that mean the request itself is bad and won't help to retry with same params
BAD_REQUEST_CODES = {
    "2001",  # invalid parameters
    "2002",  # missing required field
    "2003",  # invalid token
    "2004",  # account suspended
}

# Codes that mean auth / token problems
AUTH_CODES = {
    "1006",  # not logged in
    "1008",  # token expired
    "1009",  # insufficient permissions
}


def classify_api_error(api_response: dict) -> str:
    """
    Classify a WotoHub API error response into a broad category.

    Returns one of: "auth", "bad_request", "retryable", "unknown"
    """
    result = api_response.get("result") or {}
    code = str(result.get("code", ""))

    if code in AUTH_CODES:
        return "auth"
    if code in BAD_REQUEST_CODES:
        return "bad_request"
    if code in RETRYABLE_API_CODES:
        return "retryable"
    if code.startswith("1"):
        return "retryable"
    if code.startswith("2"):
        return "bad_request"
    return "unknown"


def build_error(
    code: str,
    message: str,
    *,
    details: Optional[dict]= None,
    retryable: bool = False,
    next_step: str = "",
) -> dict:
    """
    Build a structured error dict matching the schema consumed by run_campaign.py.

    Returns:
        {
            "code": str,
            "message": str,
            "category": str,
            "details": dict,
            "retryable": bool,
            "next_step": str,
        }
    """
    # Normalize category from internal code table
    category_map = {
        "SCRIPT_ERROR":            "internal_error",
        "PRODUCT_CONTEXT_MISSING": "product_context_missing",
        "PAYLOAD_BUILD_FAILED":    "payload_build_failed",
        "TOKEN_MISSING":           "auth_required",
        "TOKEN_INVALID":           "auth_failed",
        "NETWORK_ERROR":           "network_error",
        "API_ERROR":               "api_error",
        "NO_SEARCH_RESULTS":       "no_results",
        "FALLBACK_EXHAUSTED":      "fallback_exhausted",
    }
    category = category_map.get(code, "internal_error")

    return {
        "code": code,
        "message": message,
        "category": category,
        "details": details or {},
        "retryable": retryable,
        "next_step": next_step,
    }


def api_error_to_structured(
    api_response: dict,
    context: Optional[dict]= None,
) -> dict:
    """
    Convert a raw WotoHub API error response into a structured error dict.

    context: optional extra fields to include in details (e.g. payload, step)
    """
    result = api_response.get("result") or {}
    code = str(result.get("code", ""))
    raw_message = result.get("message", "WotoHub API 返回未知错误")

    classification = classify_api_error(api_response)
    retryable = classification == "retryable"

    code_messages = {
        "1006": "用户未登录，请检查 Token 是否正确",
        "1008": "Token 已过期，请更新 Token",
        "1009": "权限不足",
        "2003": "Token 无效",
        "2004": "账号已被封停",
        "1001": "请求过于频繁，请稍后重试",
        "1002": "服务器繁忙，请稍后重试",
    }

    user_message = code_messages.get(code, raw_message)

    next_steps = {
        "auth":       "检查 Token 是否正确，或重新登录 WotoHub 获取新 Token",
        "bad_request": "适当放宽地区、类目、关键词或邮箱要求后重试",
        "retryable":  "稍等片刻后重试",
        "unknown":    "请检查 WotoHub 服务状态后重试",
    }

    details = {
        "apiCode": code,
        "apiMessage": raw_message,
    }
    if context:
        details.update(context)

    return build_error(
        "API_ERROR",
        user_message,
        details=details,
        retryable=retryable,
        next_step=next_steps.get(classification, "请稍后重试"),
    )
