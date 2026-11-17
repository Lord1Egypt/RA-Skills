#!/usr/bin/env python3
"""WPS/金山文档 连接器 — MCP 客户端（Hermes 版）

协议：streamable-http JSON-RPC 2.0，端点 https://mcp-center.wps.cn/skill_hub/mcp
认证：Authorization: Bearer <skill_hub token>（token 由 wps_auth.py 取得，存在 ~/.hermes/.env 的 WPS_KDOCS_TOKEN）

用法：
  python3 wps_mcp.py list                        # 列出全部工具名
  python3 wps_mcp.py list --grep drive           # 按关键字筛工具
  python3 wps_mcp.py schema <tool_name>          # 打印某工具入参 JSON Schema
  python3 wps_mcp.py call <tool_name> '<json>'   # 调用工具，入参为 JSON 对象
  python3 wps_mcp.py call <tool_name> --file p.json
  python3 wps_mcp.py whoami                      # 校验 token 是否有效

退出码：0 成功；1 失败；2 未登录/未配置 token
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
import uuid

MCP_URL = "https://mcp-center.wps.cn/skill_hub/mcp"
SKILL_VERSION = "1.6.14"
ENV_FILE = os.environ.get("WPS_KDOCS_ENV_FILE", "wps_kdocs.env")
TOKEN_KEY = "WPS_KDOCS_TOKEN"
CLIENT_ID_FILE = os.environ.get("WPS_KDOCS_CLIENT_ID_FILE") or os.path.join(
    os.path.expanduser("~"), ".hermes", "wps_kdocs_client_id")


def read_token() -> str:
    tok = os.environ.get(TOKEN_KEY, "").strip()
    if tok:
        return tok
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if line.startswith(f"{TOKEN_KEY}="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def client_id() -> str:
    if os.path.exists(CLIENT_ID_FILE):
        cid = open(CLIENT_ID_FILE, encoding="utf-8").read().strip()
        if len(cid) == 16:
            return cid
    cid = uuid.uuid4().hex[:16]
    os.makedirs(os.path.dirname(CLIENT_ID_FILE), exist_ok=True)
    with open(CLIENT_ID_FILE, "w", encoding="utf-8") as fh:
        fh.write(cid)
    os.chmod(CLIENT_ID_FILE, 0o600)
    return cid


class McpSession:
    def __init__(self, token: str | None = None, timeout: int = 60):
        self.url = MCP_URL
        self.timeout = timeout
        self.sid = None
        self._id = 0
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "X-Request-Source": "workbuddy",
            "X-Skill-Version": SKILL_VERSION,
            "X-Client-Id": client_id(),
        }
        tok = token if token is not None else read_token()
        if tok:
            self.headers["Authorization"] = f"Bearer {tok}"
        self.auth_status = None

    def _post(self, payload: dict):
        h = dict(self.headers)
        if self.sid:
            h["mcp-session-id"] = self.sid
        req = urllib.request.Request(self.url, data=json.dumps(payload).encode(), headers=h)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                status = r.status
                resp_headers = dict(r.headers)
                body = r.read()
        except urllib.error.HTTPError as e:
            body = e.read()
            status = e.code
            resp_headers = dict(e.headers or {})
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"网络失败: {type(exc).__name__}: {exc}") from exc

        self.auth_status = resp_headers.get("x-kso-auth-status") or self.auth_status
        sid = resp_headers.get("mcp-session-id") or resp_headers.get("Mcp-Session-Id")
        if sid:
            self.sid = sid
        return status, body

    @staticmethod
    def _parse(body: bytes):
        text = body.decode("utf-8", "replace").strip()
        if not text:
            return None
        if text.startswith("event:") or "\ndata:" in text or text.startswith("data:"):
            # SSE: 取最后一个 data: 行
            datas = [ln[5:].strip() for ln in text.splitlines() if ln.startswith("data:")]
            for chunk in reversed(datas):
                if chunk and chunk != "[DONE]":
                    try:
                        return json.loads(chunk)
                    except json.JSONDecodeError:
                        continue
            return None
        return json.loads(text)

    def _rpc(self, method: str, params: dict | None = None):
        self._id += 1
        payload = {"jsonrpc": "2.0", "id": self._id, "method": method, "params": params or {}}
        status, body = self._post(payload)
        data = self._parse(body)
        if data is None:
            raise RuntimeError(f"{method} 返回空响应 (HTTP {status})")
        if "error" in data:
            err = data["error"]
            raise RuntimeError(f"{method} 报错: {err.get('code')} {err.get('message')}")
        return data.get("result", {})

    def initialize(self):
        return self._rpc("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "hermes-wps-connector", "version": "1.0.0"},
        })

    def list_tools(self) -> list[dict]:
        tools, cursor = [], None
        while True:
            params = {"cursor": cursor} if cursor else {}
            res = self._rpc("tools/list", params)
            tools.extend(res.get("tools") or [])
            cursor = res.get("nextCursor")
            if not cursor:
                return tools

    def call_tool(self, name: str, arguments: dict):
        return self._rpc("tools/call", {"name": name, "arguments": arguments})


def _load_args(argv: list[str]) -> dict:
    if not argv:
        return {}
    if argv[0] == "--file":
        with open(argv[1], encoding="utf-8") as fh:
            return json.load(fh)
    return json.loads(argv[0])


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in {"-h", "--help"}:
        print(__doc__)
        return 0
    cmd = argv[0]
    tok = read_token()

    if cmd == "whoami":
        if not tok:
            print(f"未配置 token：请在 {ENV_FILE} 写入 {TOKEN_KEY}=<token>，或运行 wps_auth.py")
            return 2
        s = McpSession()
        s.initialize()
        tools = s.list_tools()
        if s.auth_status and s.auth_status.lower() != "login":
            print(f"token 无效或已过期（服务端状态 {s.auth_status}），请重新运行 wps_auth.py")
            return 2
        print(f"登录有效；工具数 {len(tools)}")
        return 0

    s = McpSession()
    s.initialize()

    if cmd == "list":
        grep = None
        if "--grep" in argv:
            grep = argv[argv.index("--grep") + 1]
        tools = s.list_tools()
        for t in tools:
            name = t.get("name", "")
            if grep and grep not in name and grep not in (t.get("description") or ""):
                continue
            print(f"{name}\t{(t.get('description') or '').splitlines()[0][:90]}")
        return 0

    if cmd == "schema":
        if len(argv) < 2:
            print("用法: wps_mcp.py schema <tool_name>")
            return 1
        for t in s.list_tools():
            if t.get("name") == argv[1]:
                print(json.dumps({"name": t["name"], "description": t.get("description"),
                                  "inputSchema": t.get("inputSchema")}, ensure_ascii=False, indent=2))
                return 0
        print(f"工具不存在: {argv[1]}")
        return 1

    if cmd == "call":
        if len(argv) < 2:
            print("用法: wps_mcp.py call <tool_name> '<json>' | --file <path>")
            return 1
        if not tok:
            print(f"未配置 token：请运行 wps_auth.py 取得 token 并写入 {ENV_FILE}")
            return 2
        args = _load_args(argv[2:])
        res = s.call_tool(argv[1], args)
        if s.auth_status and s.auth_status.lower() != "login":
            print(f"[warn] 服务端登录态 {s.auth_status}，结果可能为未授权错误", file=sys.stderr)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    print(f"未知命令: {cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
