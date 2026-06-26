"""Zopia Skill 共享模块 — 封装 HTTP 请求、认证、错误处理。

仅依赖 Python 标准库。

环境变量:
    ZOPIA_ACCESS_KEY  (必需) Bearer token，格式 zopia-xxxxxxxxxxxx
    ZOPIA_BASE_URL    (可选) API 基础地址，默认 https://zopia.ai
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

def _get_access_key() -> str:
    key = os.environ.get("ZOPIA_ACCESS_KEY", "").strip()
    if not key:
        print("错误: 环境变量 ZOPIA_ACCESS_KEY 未设置", file=sys.stderr)
        sys.exit(1)
    return key


def _get_base_url() -> str:
    return os.environ.get("ZOPIA_BASE_URL", "https://zopia.ai").rstrip("/")


# ---------------------------------------------------------------------------
# 底层 HTTP 工具
# ---------------------------------------------------------------------------

def _build_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_get_access_key()}",
        "Content-Type": "application/json",
    }


def api_get(path: str, params: dict[str, str] | None = None) -> Any:
    """发送 GET 请求，返回解析后的 JSON。"""
    url = f"{_get_base_url()}{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    req = urllib.request.Request(url, headers=_build_headers(), method="GET")
    return _do_request(req)


def api_post(path: str, body: dict[str, Any] | None = None) -> Any:
    """发送 POST 请求，返回解析后的 JSON。"""
    url = f"{_get_base_url()}{path}"
    data = json.dumps(body or {}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=_build_headers(), method="POST")
    return _do_request(req)


def api_delete(path: str) -> Any:
    """发送 DELETE 请求，返回解析后的 JSON。"""
    url = f"{_get_base_url()}{path}"
    req = urllib.request.Request(url, headers=_build_headers(), method="DELETE")
    return _do_request(req)


def _do_request(req: urllib.request.Request) -> Any:
    """执行请求，统一处理错误。"""
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            if not raw:
                return {}
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        print(f"HTTP {exc.code} 错误: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"网络错误: {exc.reason}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# 业务级封装
# ---------------------------------------------------------------------------

def create_project(base_name: str | None = None) -> dict[str, Any]:
    """创建项目，返回 {baseId, baseName, episodeId}。"""
    body: dict[str, Any] = {}
    if base_name:
        body["baseName"] = base_name
    resp = api_post("/api/base/create", body)
    return resp.get("data", resp)


def save_settings(base_id: str, settings: dict[str, Any]) -> dict[str, Any]:
    """保存项目设置，返回合并后的设置。"""
    resp = api_post("/api/base/settings", {"base_id": base_id, "settings": settings})
    return resp


def get_settings(base_id: str) -> dict[str, Any]:
    """获取项目设置。"""
    resp = api_get("/api/base/settings", {"base_id": base_id})
    return resp


def send_message(base_id: str, episode_id: str, message: str,
                 session_id: str | None = None) -> dict[str, Any]:
    """异步发送消息，返回 {session_id, ...}。"""
    body: dict[str, Any] = {
        "base_id": base_id,
        "episode_id": episode_id,
        "message": message,
    }
    if session_id:
        body["session_id"] = session_id
    return api_post("/api/v1/agent/chat/async", body)


def query_session(session_id: str, after_seq: int = 0) -> dict[str, Any]:
    """增量查询会话消息，返回结构化结果。"""
    params: dict[str, str] = {}
    if after_seq > 0:
        params["afterSeq"] = str(after_seq)
    return api_get(f"/api/v1/agent/session/{session_id}/messages", params)


def list_projects(page: int = 1, page_size: int = 12) -> dict[str, Any]:
    """获取项目列表。"""
    return api_get("/api/base/list", {"page": str(page), "pageSize": str(page_size)})


def get_project_detail(base_id: str, episode_id: str) -> dict[str, Any]:
    """获取项目详情。"""
    return api_get(f"/api/base/{base_id}", {"episode_id": episode_id})


def create_episode(base_id: str) -> dict[str, Any]:
    """创建新剧集。"""
    return api_post(f"/api/episode/create?base_id={base_id}")


def list_episodes(base_id: str) -> dict[str, Any]:
    """列出项目的所有剧集。"""
    return api_get("/api/episode/list", {"base_id": base_id})


def delete_episode(episode_id: str) -> dict[str, Any]:
    """删除剧集。"""
    return api_delete(f"/api/episode/{episode_id}")


def get_balance() -> dict[str, Any]:
    """查询余额。"""
    return api_get("/api/billing/getBalance")


def trigger_render(base_id: str, episode_id: str, show_watermark: bool = False) -> dict[str, Any]:
    """触发 episode 视频合成渲染（异步），返回 {render_id, status}。"""
    return api_post(
        f"/api/v1/base/{base_id}/episode/{episode_id}/render",
        {"show_watermark": show_watermark},
    )


def get_render_status(base_id: str, episode_id: str, render_id: str | None = None) -> dict[str, Any]:
    """查询渲染状态，返回 {status, render_id?, progress?, video_url?, error?}。"""
    params: dict[str, str] = {}
    if render_id:
        params["render_id"] = render_id
    return api_get(f"/api/v1/base/{base_id}/episode/{episode_id}/render", params or None)


def build_project_url(base_id: str, session_id: str | None = None) -> str:
    """构造项目的 Web 访问 URL。"""
    url = f"{_get_base_url()}/base/{base_id}"
    if session_id:
        url = f"{url}?session_id={session_id}"
    return url


# ---------------------------------------------------------------------------
# 输出工具
# ---------------------------------------------------------------------------

def print_json(data: Any) -> None:
    """以格式化的 JSON 输出到 stdout。"""
    print(json.dumps(data, ensure_ascii=False, indent=2))
