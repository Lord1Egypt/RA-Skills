"""Social Hot Search proxy client.

Stdlib-only client for calling the Social Skill proxy.
Handles: user_id persistence, machine fingerprint, MCP tool calls,
quota-exhausted detection.
"""
from __future__ import annotations

import getpass
import hashlib
import json
import os
import socket
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


PROXY_BASE = os.environ.get("SOCIAL_PROXY_BASE", "https://47-103-200-210.nip.io")
SKILL_ID = "social-hotsearch"
USER_FILE = Path(os.environ.get(
    "SOCIAL_USER_FILE",
    str(Path.home() / ".config" / "social-hotsearch" / "user.json"),
))


class QuotaExhausted(RuntimeError):
    def __init__(self, info: dict[str, Any]):
        self.info = info
        super().__init__(info.get("message") or "quota exhausted")


class ProxyError(RuntimeError):
    pass


def machine_fingerprint() -> str:
    raw = f"{getpass.getuser()}@{socket.gethostname()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


# 平台名归一化:analyze_topic / sample_posts 用的 datasource 名,与口语/热搜榜不一致
# 用户/AI 习惯说"抖音""快手"等具体站点名,这里映射到 social-base 接受的 platform 大类
ANALYSIS_DATASOURCE_ALIASES = {
    "抖音": "短视频",
    "快手": "短视频",
    "微信公众号": "微信",
    "公众号": "微信",
    "B站": "视频",
    "哔哩哔哩": "视频",
    "bilibili": "视频",
}

ANALYSIS_DATASOURCE_VALID = {
    "小红书", "微博", "短视频", "视频", "微信", "电商", "博客", "问答", "新闻", "论坛",
}


def normalize_analysis_datasource(items: list[str]) -> list[str]:
    """把口语/具体站点名归一化到 social_statistic_* / query_raw_posts 接受的 platform 名。

    - 已是合法 platform → 原样保留
    - 命中别名表 → 转换(如 抖音→短视频)
    - 既不合法也不在别名表 → 原样保留(让上游报错给用户更清晰的提示)
    """
    out: list[str] = []
    for it in items:
        # 支持"platform__sub1,sub2"形式,只对 platform 部分做映射
        if "__" in it:
            head, sep, tail = it.partition("__")
            head = ANALYSIS_DATASOURCE_ALIASES.get(head, head)
            out.append(f"{head}{sep}{tail}")
        else:
            out.append(ANALYSIS_DATASOURCE_ALIASES.get(it, it))
    return out


def _post_json(path: str, payload: dict[str, Any], headers: dict[str, str] | None = None,
               timeout: int = 30) -> dict[str, Any]:
    url = PROXY_BASE.rstrip("/") + path
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(body_text)
        except Exception:
            data = {"raw": body_text}
        if e.code == 402:
            raise QuotaExhausted(data) from e
        raise ProxyError(f"HTTP {e.code}: {data}") from e
    except urllib.error.URLError as e:
        raise ProxyError(f"network error: {e.reason}") from e


def _get(path: str, headers: dict[str, str] | None = None, timeout: int = 30) -> dict[str, Any]:
    url = PROXY_BASE.rstrip("/") + path
    req = urllib.request.Request(url, method="GET")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(body_text)
        except Exception:
            data = {"raw": body_text}
        raise ProxyError(f"HTTP {e.code}: {data}") from e
    except urllib.error.URLError as e:
        raise ProxyError(f"network error: {e.reason}") from e


def load_user() -> dict[str, Any] | None:
    if not USER_FILE.exists():
        return None
    try:
        return json.loads(USER_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_user(data: dict[str, Any]) -> None:
    USER_FILE.parent.mkdir(parents=True, exist_ok=True)
    USER_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_user() -> dict[str, Any]:
    """Load or create user_id. Returns full user record from server."""
    cached = load_user()
    fp = machine_fingerprint()
    resp = _post_json("/v1/register", {"machine_fingerprint": fp})
    user_id = resp["user_id"]
    record = {
        "user_id": user_id,
        "machine_fingerprint": fp,
        "is_new": resp.get("is_new", False),
    }
    save_user(record)
    return {**record, **resp}


def get_usage(user_id: str) -> dict[str, Any]:
    return _get("/v1/usage", headers={"Authorization": f"Bearer {user_id}"})


def get_upgrade_info() -> dict[str, Any]:
    return _get("/v1/upgrade-info")


def call_tool(tool_name: str, arguments: dict[str, Any], user_id: str | None = None,
              timeout: int = 180) -> dict[str, Any]:
    """Call an MCP tool through the proxy. Returns the parsed JSON-RPC result.

    Raises QuotaExhausted on 402, ProxyError otherwise.
    """
    if user_id is None:
        u = ensure_user()
        user_id = u["user_id"]

    url = PROXY_BASE.rstrip("/") + "/mcp"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    req.add_header("Authorization", f"Bearer {user_id}")
    req.add_header("X-Skill-Id", SKILL_ID)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(body_text)
        except Exception:
            data = {"raw": body_text}
        if e.code == 402:
            raise QuotaExhausted(data) from e
        raise ProxyError(f"HTTP {e.code}: {data}") from e
    except urllib.error.URLError as e:
        raise ProxyError(f"network error: {e.reason}") from e

    msg = _parse_mcp_response(raw)
    if "error" in msg:
        err = msg["error"] or {}
        raise ProxyError(f"MCP error {err.get('code')}: {err.get('message')}")
    result = msg.get("result", {})
    if result.get("isError"):
        raise ProxyError(f"MCP tool {tool_name} returned an error")
    return result


def extract_text_content(result: dict[str, Any]) -> str:
    """Pull the text content from an MCP tool result (commonly returned as
    JSON-Lines or plain text in result.content[0].text).
    """
    content = result.get("content", [])
    if not isinstance(content, list):
        return ""
    parts = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(item.get("text", ""))
    return "\n".join(parts)


def _parse_mcp_response(body: str) -> dict[str, Any]:
    """Parse either a JSON body or an SSE event stream containing JSON-RPC."""
    body = body.strip()
    if not body:
        raise ProxyError("empty response from proxy")
    # Plain JSON
    if body.startswith("{") or body.startswith("["):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            pass
    # SSE: look for `data: {...}` lines
    for line in body.splitlines():
        if line.startswith("data: "):
            chunk = line[6:].strip()
            if not chunk:
                continue
            try:
                obj = json.loads(chunk)
                if isinstance(obj, dict):
                    return obj
            except json.JSONDecodeError:
                continue
    raise ProxyError(f"unable to parse MCP response: {body[:200]}")


def print_quota_help(info: dict[str, Any]) -> None:
    """Print user-friendly quota-exhausted message and upgrade form URL."""
    sys.stderr.write("\n" + "=" * 60 + "\n")
    sys.stderr.write("免费额度已用完\n")
    sys.stderr.write("=" * 60 + "\n")
    sys.stderr.write(f"已使用: {info.get('used')} / {info.get('limit')}\n")
    sys.stderr.write(f"\n{info.get('message') or '请联系商务获取更多用量'}\n")
    if info.get("form_url"):
        sys.stderr.write(f"\n填写此表单联系商务:\n{info['form_url']}\n")
    sys.stderr.write("=" * 60 + "\n\n")
