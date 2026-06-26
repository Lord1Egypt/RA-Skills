#!/usr/bin/env python3
"""UUMuse MCP stdio → HTTP 桥接脚本

纯 Python（零第三方依赖），将 stdin 上的 newline-delimited JSON-RPC 消息
转发到 UUMuse 嵌入式 MCP HTTP 端点，将响应写回 stdout。

LobsterAI / OpenClaw 等只支持 stdio transport 的客户端通过此脚本
连接局域网或远程 HTTP MCP Server。

环境变量：
    UUMUSE_MCP_URL  — MCP HTTP 端点 URL（必填，如 http://192.168.4.58:8082/mcp/）
    UUMUSE_API_KEY  — API Key（必填，如 sk-uu-xxx）
"""

import json
import os
import sys
import urllib.error
import urllib.request

MCP_URL = os.environ.get("UUMUSE_MCP_URL", "").rstrip("/")
API_KEY = os.environ.get("UUMUSE_API_KEY", "")

# MCP Streamable HTTP 需要 session ID 跟踪会话
_session_id: str | None = None


def _fatal(msg: str) -> None:
    print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": msg}}),
          flush=True)
    sys.exit(1)


def _post(payload: str) -> str:
    """发送 JSON-RPC 到 MCP HTTP 端点，返回响应体"""
    global _session_id

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Authorization": f"Bearer {API_KEY}",
    }
    if _session_id:
        headers["Mcp-Session-Id"] = _session_id

    url = MCP_URL if MCP_URL.endswith("/") else MCP_URL + "/"
    req = urllib.request.Request(url, data=payload.encode("utf-8"), headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            # 记录服务端返回的 session ID
            sid = resp.headers.get("Mcp-Session-Id")
            if sid:
                _session_id = sid

            content_type = resp.headers.get("Content-Type", "")
            body = resp.read().decode("utf-8")

            # Streamable HTTP 可能返回 SSE 格式
            if "text/event-stream" in content_type:
                return _parse_sse(body)
            return body
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace") if e.fp else str(e)
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": f"HTTP {e.code}: {error_body[:500]}"},
        })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": f"Connection error: {e}"},
        })


def _parse_sse(body: str) -> str:
    """从 SSE 流中提取最后一个 data: 行的 JSON"""
    last_data = ""
    for line in body.splitlines():
        if line.startswith("data: "):
            last_data = line[6:]
    return last_data or body


def main() -> None:
    if not MCP_URL:
        _fatal("UUMUSE_MCP_URL environment variable is not set")
    if not API_KEY:
        _fatal("UUMUSE_API_KEY environment variable is not set")

    # 逐行从 stdin 读取 JSON-RPC 消息
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = msg.get("method", "")

        # notification 类消息（无 id）：转发但不期待有意义的响应
        if "id" not in msg:
            _post(line)
            continue

        # 带 id 的请求：转发并将响应写回 stdout
        response = _post(line)
        if response:
            # 确保响应是合法 JSON，且 id 与请求匹配
            try:
                resp_obj = json.loads(response)
                if resp_obj.get("id") is None and msg.get("id") is not None:
                    resp_obj["id"] = msg["id"]
                    response = json.dumps(resp_obj)
            except json.JSONDecodeError:
                response = json.dumps({
                    "jsonrpc": "2.0",
                    "id": msg.get("id"),
                    "error": {"code": -32603, "message": f"Invalid server response: {response[:200]}"},
                })

            print(response, flush=True)


if __name__ == "__main__":
    main()
