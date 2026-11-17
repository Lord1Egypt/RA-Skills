#!/usr/bin/env python3
"""闲沐连环画 MCP 直连客户端（纯 Python 标准库，零第三方依赖）。

不经客户端 MCP 配置、直接以 JSON-RPC over Streamable HTTP 调用
https://www.wwzu.com/mcp 的全部工具，鉴权用你自己的 API Key（xm- 前缀）。
与配置 MCP 客户端完全等价：同一端点、同一计费、同一每日额度。

用法：
  python xianmu_mcp.py tools                        # 列出全部工具
  python xianmu_mcp.py call <tool> '<json参数>'      # 调用工具，参数为 JSON 对象
  python xianmu_mcp.py call <tool> -                # 参数 JSON 从 stdin 读入
  python xianmu_mcp.py call get_comic '{"comic_id":"200741113201"}'

环境变量：
  XIANMU_API_KEY   必填，你的 API Key（https://www.wwzu.com/mcp-keys.php 免费创建）
  XIANMU_MCP_URL   选填，默认 https://www.wwzu.com/mcp（本地调试可覆盖）

输出约定：工具结果文本写 stdout；诊断信息写 stderr（密钥永不输出）。
退出码：0 成功；1 传输/协议/配置错误；2 工具返回业务错误（isError=true）。
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_URL = "https://www.wwzu.com/mcp"
CLIENT_NAME = "xianmu-comics-skill"
CLIENT_VERSION = "1.0.0"
PROTOCOL_VERSION = "2025-03-26"
TIMEOUT_SECONDS = 90

EXIT_OK, EXIT_TRANSPORT, EXIT_TOOL = 0, 1, 2


def _err(msg: str) -> None:
    print(msg, file=sys.stderr)


class HttpError(Exception):
    """服务端返回 4xx/5xx；携带状态码与原始响应体。"""

    def __init__(self, status: int, body: str) -> None:
        super().__init__(f"HTTP {status}")
        self.status = status
        self.body = body


def _load_env_file() -> None:
    """可选：从脚本同目录及当前目录的 .env 补充 XIANMU_API_KEY（真实环境变量优先）。"""
    if os.environ.get("XIANMU_API_KEY"):
        return
    here = os.path.dirname(os.path.abspath(__file__))
    for path in (os.path.join(here, ".env"), os.path.join(os.getcwd(), ".env")):
        try:
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line.startswith("XIANMU_API_KEY="):
                        value = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if value:
                            os.environ["XIANMU_API_KEY"] = value
                            return
        except OSError:
            continue


class McpHttpClient:
    """最小 Streamable HTTP 客户端：initialize 握手 → 会话头回传 → tools/* 调用。"""

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session_id: str | None = None
        self._next_id = 0

    def _post(self, payload: dict) -> tuple[dict | None, int, str]:
        """POST 一个 JSON-RPC 消息，返回 (解析后的响应对象, HTTP 状态码, 原始 body)。"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": f"Bearer {self.api_key}",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        req = urllib.request.Request(
            self.base_url, data=json.dumps(payload).encode("utf-8"),
            headers=headers, method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                status = resp.status
                new_session = resp.headers.get("Mcp-Session-Id")
                if new_session:
                    self.session_id = new_session
                body = resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise HttpError(exc.code, body) from exc
        except urllib.error.URLError as exc:
            raise ConnectionError(f"无法连接 {self.base_url}：{exc.reason}") from exc
        return _parse_body(body), status, body

    def _rpc(self, method: str, params: dict | None = None, *, notify: bool = False) -> dict:
        self._next_id += 1
        payload: dict = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        if not notify:
            payload["id"] = self._next_id
        obj, status, _body = self._post(payload)
        if notify:
            return {}
        if obj is not None:
            if "error" in obj:
                err = obj["error"]
                raise RuntimeError(
                    f"{method} 返回 JSON-RPC 错误 {err.get('code')}：{err.get('message')}"
                )
            return obj.get("result") or {}
        if status == 202:
            return {}
        raise RuntimeError(f"{method} 响应无法解析（HTTP {status}）")

    def initialize(self) -> None:
        result = self._rpc("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": CLIENT_NAME, "version": CLIENT_VERSION},
        })
        server = (result.get("serverInfo") or {}).get("name", "?")
        _err(f"已连接：{server}（协议 {result.get('protocolVersion', '?')}）")
        self._rpc("notifications/initialized", notify=True)

    def list_tools(self) -> list[dict]:
        result = self._rpc("tools/list", {})
        return result.get("tools") or []

    def call_tool(self, name: str, arguments: dict) -> dict:
        return self._rpc("tools/call", {"name": name, "arguments": arguments})


def _parse_body(body: str) -> dict | None:
    """响应体可能是普通 JSON，也可能是 SSE 流（data: 行），两者都解析出 JSON-RPC 响应。"""
    text = body.strip()
    if not text:
        return None
    if text.startswith("{") or text.startswith("["):
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return None
        if isinstance(parsed, list):  # 极少数服务端会回批量数组
            for item in parsed:
                if isinstance(item, dict) and "id" in item:
                    return item
            return parsed[0] if parsed else None
        return parsed if isinstance(parsed, dict) else None
    # SSE：取最后一个携带 result/error 的 data 载荷
    candidate: dict | None = None
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("data:"):
            continue
        chunk = line[5:].strip()
        if not chunk or chunk == "[DONE]":
            continue
        try:
            obj = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and ("result" in obj or "error" in obj):
            candidate = obj
    return candidate


def _human_http_error(status: int, body: str) -> str:
    snippet = body.strip()[:300]
    if status == 401:
        return ("API Key 无效或已撤销（HTTP 401）。请到 https://www.wwzu.com/mcp-keys.php "
                "登录后重建/复制 Key，再更新 XIANMU_API_KEY。\n服务端返回：" + snippet)
    if status == 429:
        return ("今日免费查询额度已用尽（HTTP 429）。可让智能体调用 reset_daily_quota 扣积分立即重置，"
                "或次日自动恢复（VIP 每日 300 次）。\n服务端返回：" + snippet)
    if status == 404:
        return ("端点或会话不存在（HTTP 404）。若反复出现，请确认 XIANMU_MCP_URL 指向 "
                "https://www.wwzu.com/mcp。\n服务端返回：" + snippet)
    return f"HTTP {status}：{snippet}"


def _extract_text(result: dict) -> str:
    parts = []
    for item in result.get("content") or []:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(item.get("text") or "")
    return "\n".join(parts)


def main(argv: list[str]) -> int:
    _load_env_file()
    api_key = os.environ.get("XIANMU_API_KEY", "").strip()
    base_url = os.environ.get("XIANMU_MCP_URL", DEFAULT_URL).strip()

    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return EXIT_OK
    command = argv[0]

    if not api_key:
        _err("缺少 XIANMU_API_KEY 环境变量。到 https://www.wwzu.com/mcp-keys.php 免费创建 Key 后：\n"
             "  export XIANMU_API_KEY=xm-你的Key     （macOS/Linux）\n"
             "  setx XIANMU_API_KEY \"xm-你的Key\"    （Windows，重开终端生效）")
        return EXIT_TRANSPORT

    if command == "tools":
        client = McpHttpClient(base_url, api_key)
        try:
            client.initialize()
            tools = client.list_tools()
        except ConnectionError as exc:
            _err(str(exc))
            return EXIT_TRANSPORT
        except HttpError as exc:
            _err(_human_http_error(exc.status, exc.body))
            return EXIT_TRANSPORT
        except RuntimeError as exc:
            _err(str(exc))
            return EXIT_TRANSPORT
        brief = [
            {
                "name": t.get("name"),
                "description": (t.get("description") or "").strip().splitlines()[0]
                if (t.get("description") or "").strip() else "",
                "required": (t.get("inputSchema") or {}).get("required") or [],
            }
            for t in tools
        ]
        print(json.dumps(brief, ensure_ascii=False, indent=2))
        return EXIT_OK

    if command == "call":
        if len(argv) < 2:
            _err("用法：xianmu_mcp.py call <tool> ['<json参数>' | -]")
            return EXIT_TRANSPORT
        tool = argv[1]
        raw_args = argv[2] if len(argv) > 2 else "{}"
        if raw_args == "-":
            raw_args = sys.stdin.read()
        try:
            arguments = json.loads(raw_args) if raw_args.strip() else {}
        except json.JSONDecodeError as exc:
            _err(f"参数不是合法 JSON：{exc}")
            return EXIT_TRANSPORT
        if not isinstance(arguments, dict):
            _err("参数必须是一个 JSON 对象，如 {\"comic_id\":\"200741113201\"}")
            return EXIT_TRANSPORT

        client = McpHttpClient(base_url, api_key)
        try:
            client.initialize()
            try:
                result = client.call_tool(tool, arguments)
            except HttpError as exc:
                if exc.status == 404 and client.session_id:
                    # 会话可能已过期：丢弃会话重新握手一次再试
                    client.session_id = None
                    client.initialize()
                    result = client.call_tool(tool, arguments)
                else:
                    raise
        except ConnectionError as exc:
            _err(str(exc))
            return EXIT_TRANSPORT
        except HttpError as exc:
            _err(_human_http_error(exc.status, exc.body))
            return EXIT_TRANSPORT
        except RuntimeError as exc:
            _err(str(exc))
            return EXIT_TRANSPORT

        text = _extract_text(result)
        if not text and result.get("structuredContent") is not None:
            text = json.dumps(result["structuredContent"], ensure_ascii=False, indent=2)
        print(text or json.dumps(result, ensure_ascii=False, indent=2))
        return EXIT_TOOL if result.get("isError") else EXIT_OK

    _err(f"未知命令 {command!r}；可用命令：tools / call")
    return EXIT_TRANSPORT


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
