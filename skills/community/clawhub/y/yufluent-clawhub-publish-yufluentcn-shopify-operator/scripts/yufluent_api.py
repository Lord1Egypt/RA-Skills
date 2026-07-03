"""
Yufluent 技能云端薄客户端（ClawHub 分发用，仅依赖 requests）。
"""

from __future__ import annotations

import json
import os
from typing import Any

import requests


class YufluentApiError(Exception):
    def __init__(self, message: str, *, status: int | None = None, body: Any = None):
        super().__init__(message)
        self.status = status
        self.body = body


def normalize_api_root(base_url: str) -> str:
    base = (base_url or "").strip().rstrip("/")
    if not base:
        base = "http://localhost:8080/v1"
    if base.endswith("/v1"):
        return base
    return f"{base}/v1"


def skill_run_url(base_url: str, skill_id: str) -> str:
    return f"{normalize_api_root(base_url)}/skills/{skill_id}/run"


def agent_turn_url(base_url: str) -> str:
    return f"{normalize_api_root(base_url)}/agent/turn"


def agent_outcomes_url(base_url: str) -> str:
    return f"{normalize_api_root(base_url)}/agent/outcomes"


def _parse_error_body(raw: str) -> str:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw[:500]
    err = data.get("error") if isinstance(data, dict) else None
    if isinstance(err, dict) and err.get("message"):
        return str(err["message"])
    if isinstance(data, dict) and data.get("detail"):
        return str(data["detail"])
    return raw[:500]


def _auth_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }


def _json_headers(api_key: str) -> dict[str, str]:
    return {**_auth_headers(api_key), "Content-Type": "application/json"}


def _build_agent_turn_body(skill_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """将 CLI payload 转成 agent/turn 请求（与桌面助手同编排入口）。"""
    slots = {
        k: str(v)
        for k, v in payload.items()
        if v is not None and str(v).strip()
    }
    lines = [f"请直接执行技能 {skill_id}（参数已齐全，勿追问）："]
    for key, val in slots.items():
        lines.append(f"- {key}: {val}")
    return {
        "user_message": "\n".join(lines),
        "react": False,
        "history": [],
        "session": {
            "pending_skill_id": skill_id,
            "slots": slots,
            "strategy_state": {
                "preferred_skill_locked": True,
                "skill_id": skill_id,
            },
        },
        "web_fast": True,
    }


def _normalize_agent_turn_response(data: dict[str, Any], skill_id: str) -> dict[str, Any]:
    """agent/turn → run.py 期望的 skill run 形状。"""
    typ = str(data.get("type") or "")
    if typ == "skill_result":
        inner = data.get("result")
        if isinstance(inner, dict) and inner:
            return dict(inner)
        text = str(data.get("text") or "").strip()
        return {
            "skill_id": data.get("skill_id") or skill_id,
            "formatted_text": text,
            "text": text,
            "output_mode": "text",
        }
    if typ == "workflow_result":
        inner = data.get("result")
        if isinstance(inner, dict) and inner:
            return dict(inner)
        text = str(data.get("text") or "").strip()
        return {
            "formatted_text": text,
            "text": text,
            "output_mode": "text",
        }
    if typ == "message":
        text = str(data.get("text") or "").strip()
        if not text:
            raise YufluentApiError(
                "Agent 未执行技能（返回空 message）",
                body=data,
            )
        return {
            "skill_id": skill_id,
            "formatted_text": text,
            "text": text,
            "output_mode": "text",
            "_agent_turn_fallback": True,
            "_agent_turn_type": "message",
        }
    raise YufluentApiError(
        f"Unexpected agent turn response type: {typ or '(empty)'}",
        body=data,
    )


def _post_json(
    url: str,
    *,
    api_key: str,
    body: dict[str, Any] | None = None,
    timeout: float,
) -> requests.Response:
    kwargs: dict[str, Any] = {
        "headers": _json_headers(api_key) if body is not None else _auth_headers(api_key),
        "timeout": timeout,
    }
    if body is not None:
        kwargs["json"] = body
    return requests.post(url, **kwargs)


def _raise_for_status(resp: requests.Response) -> None:
    msg = _parse_error_body(resp.text)
    if resp.status_code == 402:
        msg = (
            f"积分余额不足。\n前往 https://claw.changzhiai.com/dashboard 充值 "
            f"（100 积分 = ¥1）。\n详情：{msg}"
        )
    elif resp.status_code == 401:
        msg = (
            f"API 密钥无效或未注册。\n"
            f"新用户请前往 https://claw.changzhiai.com/login 注册获取免费密钥。\n"
            f"详情：{msg}"
        )
    raise YufluentApiError(msg, status=resp.status_code, body=resp.text)


# 直连 Harness HTTP 路由故障时 fallback 到 /agent/turn（与桌面助手同编排入口）
_SKILL_RUN_FALLBACK_STATUSES = frozenset({500, 502})


def _should_fallback_skill_run(status_code: int) -> bool:
    return status_code in _SKILL_RUN_FALLBACK_STATUSES


def _parse_success_json(resp: requests.Response) -> dict[str, Any]:
    try:
        data = resp.json()
    except json.JSONDecodeError as exc:
        raise YufluentApiError(f"Invalid JSON response: {resp.text[:200]}") from exc
    if not isinstance(data, dict):
        raise YufluentApiError("Unexpected response shape")
    return data


def _run_skill_via_agent_turn(
    skill_id: str,
    payload: dict[str, Any],
    *,
    api_key: str,
    base_url: str,
    timeout: float,
) -> dict[str, Any]:
    """Fallback：/skills/*/run 不可用时走 /agent/turn（进程内 run_skill，与桌面一致）。"""
    url = agent_turn_url(base_url)
    agent_timeout = max(timeout, 600.0)
    try:
        resp = _post_json(
            url,
            api_key=api_key,
            body=_build_agent_turn_body(skill_id, payload),
            timeout=agent_timeout,
        )
    except requests.RequestException as exc:
        raise YufluentApiError(f"Agent turn request failed: {exc}") from exc

    if resp.status_code >= 400:
        _raise_for_status(resp)

    data = _parse_success_json(resp)
    return _normalize_agent_turn_response(data, skill_id)


def run_skill(
    skill_id: str,
    payload: dict[str, Any],
    *,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: float = 120.0,
) -> dict[str, Any]:
    key = (api_key or os.getenv("TOKENAPI_KEY", "")).strip()
    if not key:
        msg = (
            "未配置 TOKENAPI_KEY。\n"
            "新用户请前往 https://claw.changzhiai.com/login 注册，即送体验积分。\n"
            "获取密钥后设置环境变量：export TOKENAPI_KEY=tk-..."
        )
        raise YufluentApiError(msg)

    root = base_url or os.getenv("TOKENAPI_BASE_URL", "")
    url = skill_run_url(root, skill_id)
    try:
        resp = _post_json(url, api_key=key, body=payload, timeout=timeout)
    except requests.RequestException as exc:
        raise YufluentApiError(f"Request failed: {exc}") from exc

    if _should_fallback_skill_run(resp.status_code):
        return _run_skill_via_agent_turn(
            skill_id,
            payload,
            api_key=key,
            base_url=root,
            timeout=timeout,
        )

    if resp.status_code >= 400:
        _raise_for_status(resp)

    return _parse_success_json(resp)


def record_outcome(
    payload: dict[str, Any],
    *,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """登记 Harness 效果（POST /v1/agent/outcomes）。"""
    key = (api_key or os.getenv("TOKENAPI_KEY", "")).strip()
    if not key:
        msg = (
            "未配置 TOKENAPI_KEY。\n"
            "新用户请前往 https://claw.changzhiai.com/login 注册，即送体验积分。\n"
            "获取密钥后设置环境变量：export TOKENAPI_KEY=tk-..."
        )
        raise YufluentApiError(msg)

    url = agent_outcomes_url(base_url or os.getenv("TOKENAPI_BASE_URL", ""))
    try:
        resp = _post_json(url, api_key=key, body=payload, timeout=timeout)
    except requests.RequestException as exc:
        raise YufluentApiError(f"Request failed: {exc}") from exc

    if resp.status_code >= 400:
        msg = _parse_error_body(resp.text)
        if resp.status_code == 401:
            msg = f"API 密钥无效：{msg}"
        raise YufluentApiError(msg, status=resp.status_code, body=resp.text)

    return _parse_success_json(resp)


# ClawHub / OpenClaw SKILL.md frontmatter（单行 JSON）
OPENCLAW_METADATA_JSON = (
    '{"requires":{"env":["TOKENAPI_KEY"]},"primaryEnv":"TOKENAPI_KEY",'
    '"install":[{"id":"deps","kind":"pip","label":"Install requests","packages":["requests>=2.31.0"]}]}'
)
