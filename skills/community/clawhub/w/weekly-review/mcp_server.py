"""轻量 MCP server：接收 Agent 整理的 review_input，返回 Markdown 报告.

不依赖 `mcp` 官方包，使用 stdio JSON-RPC 2.0。
读会话存储由调用方 Agent 完成；本工具只做结构校验与渲染。
"""

from __future__ import annotations

import json
import sys
from typing import Any

from report import ReportBuilder


TOOLS_SCHEMA = {
    "tools": [
        {
            "name": "run_weekly_review",
            "description": (
                "将 Agent 已采集的周度复盘事实（review_input）渲染为 Markdown 报告。"
                "不读取任何本地会话数据库；采集由调用方 Agent 负责。"
            ),
            "inputSchema": {
                "type": "object",
                "required": ["review_input"],
                "properties": {
                    "review_input": {
                        "type": "object",
                        "description": (
                            "标准复盘事实包：period / dashboard / projects / "
                            "problems / actions / open_sessions / automations。"
                            "见 skill 内 schema/review-input.example.json。"
                        ),
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["markdown", "json"],
                        "description": "输出格式，默认 markdown。",
                    },
                },
            },
        }
    ]
}


def _run_review(params: dict[str, Any]) -> dict[str, Any]:
    data = params.get("review_input")
    if not isinstance(data, dict):
        raise ValueError("缺少 review_input 对象")
    if not (data.get("period") or {}).get("start"):
        raise ValueError("review_input.period.start 必填")

    fmt = params.get("output_format", "markdown")
    if fmt == "json":
        content = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        content = ReportBuilder(data).build()

    return {"content": [{"type": "text", "text": content}]}


def _send_response(id_: Any, result: Any) -> None:
    msg = {"jsonrpc": "2.0", "id": id_, "result": result}
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _send_error(id_: Any, code: int, message: str) -> None:
    msg = {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _handle_request(req: dict[str, Any]) -> None:
    method = req.get("method")
    id_ = req.get("id")
    params = req.get("params", {})

    if method == "initialize":
        _send_response(
            id_,
            {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "weekly-review-skill-mcp",
                    "version": "1.2.3",
                },
                "capabilities": {"tools": {}},
            },
        )
    elif method == "notifications/initialized":
        pass
    elif method == "tools/list":
        _send_response(id_, TOOLS_SCHEMA)
    elif method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})
        if name != "run_weekly_review":
            _send_error(id_, -32601, f"未知工具: {name}")
            return
        try:
            result = _run_review(arguments)
            _send_response(id_, result)
        except Exception as e:
            _send_error(id_, -32603, f"运行复盘失败: {e}")
    else:
        _send_error(id_, -32601, f"未知方法: {method}")


def serve() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            _send_error(None, -32700, "非法 JSON")
            continue
        _handle_request(req)


if __name__ == "__main__":
    serve()
