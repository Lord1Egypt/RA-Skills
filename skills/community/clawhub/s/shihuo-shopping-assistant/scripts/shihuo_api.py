#!/usr/bin/env python3
"""直接调用识货开放平台 sh.mcpapi 的命令行入口。

用法：
    python3 scripts/shihuo_api.py verify
    python3 scripts/shihuo_api.py call <tool_name> --args '<json>'
    python3 scripts/shihuo_api.py call <tool_name> --args-file <path>
    python3 scripts/shihuo_api.py call <tool_name> --args-file -   # 从标准输入读 JSON

Access Secret 只从 <skill_root>/assets/authorization.txt 读取：不接受命令行参数，
不打印到标准输出或标准错误，避免进入 Shell 历史、进程列表和日志。

输出固定为单个 JSON 对象：
    成功  {"ok": true, "result": { 工具结果壳 }}
    失败  {"ok": false, "code": "<错误码>", "message": "<说明>"}

退出码：0 成功，1 用法错误，2 缺少 Access Secret，3 Access Secret 被拒绝，4 请求失败。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_ENDPOINT = "http://sh-gateway.shihuo.cn/v4/services/sh-mcpapi/mcp"
API_KEY = "ShmcpClawhubCQCJy6Qy5yLw"
SECRET_PATH = Path(__file__).resolve().parent.parent / "assets" / "authorization.txt"
TIMEOUT = 30

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_MISSING_SECRET = 2
EXIT_INVALID_SECRET = 3
EXIT_REQUEST_FAILED = 4

# 常见占位值，视为未配置，避免拿占位串去换一次 401。
PLACEHOLDERS = {
    "xxx",
    "xxxx",
    "xxxxx",
    "<access_secret>",
    "access_secret",
    "your_access_secret",
    "todo",
}


def endpoint() -> str:
    return os.environ.get("SHIHUO_MCP_ENDPOINT", "").strip() or DEFAULT_ENDPOINT


def emit(payload: dict[str, Any], code: int) -> int:
    json.dump(payload, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return code


def fail(code: str, message: str, exit_code: int) -> int:
    return emit({"ok": False, "code": code, "message": message}, exit_code)


def read_secret() -> tuple[str, dict[str, Any] | None]:
    """读取并规范化 Access Secret，不回显内容。"""
    if not SECRET_PATH.is_file():
        return "", {
            "code": "missing_secret",
            "message": "assets/authorization.txt 不存在，尚未配置 Access Secret",
            "exit": EXIT_MISSING_SECRET,
        }
    try:
        raw = SECRET_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        return "", {
            "code": "secret_unreadable",
            "message": f"assets/authorization.txt 无法读取：{exc.strerror or exc}",
            "exit": EXIT_MISSING_SECRET,
        }
    secret = raw.strip().splitlines()[0].strip() if raw.strip() else ""
    if secret.lower().startswith("bearer "):
        secret = secret[len("bearer ") :].strip()
    if not secret or secret.lower() in PLACEHOLDERS:
        return "", {
            "code": "missing_secret",
            "message": "assets/authorization.txt 为空或仍是占位值，尚未配置 Access Secret",
            "exit": EXIT_MISSING_SECRET,
        }
    return secret, None


def _http_error(exc: urllib.error.HTTPError) -> dict[str, Any]:
    detail = ""
    try:
        body = exc.read().decode("utf-8", errors="replace")
        parsed = json.loads(body)
        if isinstance(parsed, dict):
            detail = str(parsed.get("message") or "").strip()
    except (OSError, ValueError):
        detail = ""
    lowered = detail.lower()
    if exc.code == 401:
        if "api key" in lowered:
            return {
                "code": "api_key_rejected",
                "message": "服务端拒绝了脚本内置的 X-API-Key，需要联系识货开放平台确认调用凭证",
                "exit": EXIT_INVALID_SECRET,
            }
        return {
            "code": "invalid_secret",
            "message": "Access Secret 缺失或无效，服务端返回 401",
            "exit": EXIT_INVALID_SECRET,
        }
    if exc.code == 403:
        return {
            "code": "secret_rejected",
            "message": detail or "Access Secret 已被禁用或当前用户无权调用，服务端返回 403",
            "exit": EXIT_INVALID_SECRET,
        }
    return {
        "code": "request_failed",
        "message": f"服务端返回 HTTP {exc.code}" + (f"：{detail}" if detail else ""),
        "exit": EXIT_REQUEST_FAILED,
    }


def rpc(method: str, params: dict[str, Any] | None, secret: str) -> tuple[Any, dict[str, Any] | None]:
    payload = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params is not None:
        payload["params"] = params
    request = urllib.request.Request(
        endpoint(),
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY,
            "Authorization": f"Bearer {secret}",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return None, _http_error(exc)
    except urllib.error.URLError as exc:
        return None, {
            "code": "request_failed",
            "message": f"无法连接识货开放平台：{exc.reason}",
            "exit": EXIT_REQUEST_FAILED,
        }
    except OSError as exc:
        return None, {"code": "request_failed", "message": f"请求失败：{exc}", "exit": EXIT_REQUEST_FAILED}
    try:
        parsed = json.loads(body)
    except ValueError:
        return None, {
            "code": "request_failed",
            "message": "服务端响应不是合法 JSON",
            "exit": EXIT_REQUEST_FAILED,
        }
    if not isinstance(parsed, dict):
        return None, {
            "code": "request_failed",
            "message": "服务端响应不是 JSON-RPC 对象",
            "exit": EXIT_REQUEST_FAILED,
        }
    if parsed.get("error"):
        error = parsed["error"] if isinstance(parsed["error"], dict) else {}
        return None, {
            "code": "rpc_error",
            "message": f"JSON-RPC 错误 {error.get('code')}：{error.get('message')}",
            "exit": EXIT_REQUEST_FAILED,
        }
    return parsed.get("result"), None


def unwrap(result: Any) -> Any:
    """把标准 MCP CallToolResult 还原成工具结果壳。"""
    if not isinstance(result, dict):
        return result
    structured = result.get("structuredContent")
    if isinstance(structured, dict):
        return structured
    content = result.get("content")
    if isinstance(content, list) and content:
        first = content[0]
        if isinstance(first, dict) and isinstance(first.get("text"), str):
            try:
                return json.loads(first["text"])
            except ValueError:
                return first["text"]
    return result


def load_arguments(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    if args.args is not None and args.args_file is not None:
        return {}, "--args 与 --args-file 只能用一个"
    raw = args.args
    if args.args_file is not None:
        try:
            raw = sys.stdin.read() if args.args_file == "-" else Path(args.args_file).read_text(encoding="utf-8")
        except OSError as exc:
            return {}, f"入参文件读取失败：{exc}"
    if raw is None or not raw.strip():
        return {}, ""
    try:
        parsed = json.loads(raw)
    except ValueError as exc:
        return {}, f"入参不是合法 JSON：{exc}"
    if not isinstance(parsed, dict):
        return {}, "入参必须是 JSON 对象"
    return parsed, ""


def cmd_verify() -> int:
    secret, error = read_secret()
    if error:
        return fail(error["code"], error["message"], error["exit"])
    result, error = rpc("tools/list", None, secret)
    if error:
        return fail(error["code"], error["message"], error["exit"])
    tools = result.get("tools") if isinstance(result, dict) else None
    if not isinstance(tools, list) or not tools:
        return fail("no_tools", "鉴权通过但服务端未返回可用工具", EXIT_REQUEST_FAILED)
    names = [str(item.get("name")) for item in tools if isinstance(item, dict) and item.get("name")]
    return emit({"ok": True, "tool_count": len(names), "tools": names}, EXIT_OK)


def cmd_call(args: argparse.Namespace) -> int:
    arguments, usage_error = load_arguments(args)
    if usage_error:
        return fail("invalid_arguments", usage_error, EXIT_USAGE)
    secret, error = read_secret()
    if error:
        return fail(error["code"], error["message"], error["exit"])
    result, error = rpc("tools/call", {"name": args.tool, "arguments": arguments}, secret)
    if error:
        return fail(error["code"], error["message"], error["exit"])
    return emit({"ok": True, "tool": args.tool, "result": unwrap(result)}, EXIT_OK)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="调用识货开放平台 sh.mcpapi 的商品工具组")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("verify", help="校验 assets/authorization.txt 中的 Access Secret 是否可用")
    call = sub.add_parser("call", help="调用一个识货工具")
    call.add_argument("tool", help="工具名，如 search_goods_by_keyword")
    call.add_argument("--args", help="工具入参 JSON 对象字符串")
    call.add_argument("--args-file", help="工具入参 JSON 文件路径，- 表示标准输入")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "verify":
        return cmd_verify()
    return cmd_call(args)


if __name__ == "__main__":
    raise SystemExit(main())
