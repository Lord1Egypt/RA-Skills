#!/usr/bin/env python3
"""
王聚财面皮铺 MCP Server - 发布加固版
提供店铺信息、菜单、外卖、预约与到店指引查询功能。
"""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

SERVER_NAME = "wangjucai-liangpi"
SERVER_VERSION = "1.3.0"
RUNTIME_PORT = os.getenv("PORT")
DEFAULT_HOST = os.getenv("MCP_HOST", "0.0.0.0" if RUNTIME_PORT else "127.0.0.1")
DEFAULT_PORT = int(os.getenv("MCP_PORT", RUNTIME_PORT or "8080"))
MAX_BODY_BYTES = 64 * 1024

# ============ 店铺数据 ============

RESTAURANT_INFO = {
    "name": "王聚财面皮铺",
    "slogan": "西安首家芥末蒜香酿皮",
    "description": "大众点评4.6-4.7分，西安擀面皮人气榜TOP店铺",
    "address": "西安市凤城6路ee新城南门底商",
    "area": "张家堡商圈，西安北站附近",
    "phone": "19537080416",
    "opening_hours": "9:00 - 21:00",
    "avg_price": "12-13元",
    "highlights": [
        "西安首家芥末蒜香酿皮",
        "擀面皮人气榜TOP",
        "辣椒香而不辣",
        "面筋给得多",
        "性价比高",
    ],
}

MENU_DATA = {
    "categories": [
        {
            "name": "酿皮系列",
            "items": [
                {"name": "经典酿皮", "price": 8, "desc": "传统酿皮，软糯爽滑，配秘制辣椒油"},
                {
                    "name": "芥末蒜香酿皮",
                    "price": 8,
                    "desc": "招牌特色，芥末清新加蒜香，口味轻松不重",
                    "is_signature": True,
                },
                {"name": "麻酱酿皮", "price": 10, "desc": "麻酱浓郁，口感丰富"},
            ],
        },
        {
            "name": "擀面皮系列",
            "items": [
                {"name": "经典擀面皮", "price": 8, "desc": "劲道有嚼劲，辣椒香而不辣，面筋多"},
                {"name": "芥末蒜香擀面皮", "price": 8, "desc": "擀面皮的劲道加芥末蒜香的清爽"},
            ],
        },
        {
            "name": "搭配",
            "items": [
                {"name": "辣肠夹馍", "price": 9, "desc": "经典搭配，一个够饱"},
            ],
        },
    ],
    "spice_levels": ["微辣", "中辣", "特辣"],
    "tips": [
        "芥末蒜香是特色，口味更轻松",
        "擀面皮劲道有嚼劲",
        "辣椒香而不辣，怕辣的朋友可以放心",
        "人均12-13元，性价比高",
    ],
}

DELIVERY_INFO = {
    "available": True,
    "platforms": [
        {"name": "美团外卖", "search": "搜索“王聚财面皮铺”"},
        {"name": "饿了么", "search": "搜索“王聚财面皮铺”"},
    ],
    "range": "约3公里内",
    "tips": "外卖和堂食价格一致，外卖平台可能有优惠",
}

RESERVATION_INFO = {
    "dine_in_available": True,
    "seats_limited": True,
    "reservation_required": "建议预约",
    "phone": "19537080416",
    "tips": [
        "店里位置不多，建议提前电话预约",
        "环境温馨，服务好",
        "高峰期可能需要等位",
    ],
}

WIFI_INFO = {
    "ssid": "王聚财面皮铺",
    "access": "请到店后询问店员或查看店内提示",
    "tips": "为保护店内网络安全，公开 Skill 不直接返回 Wi-Fi 密码",
}

ORDER_ENTRY_INFO = {
    "entry_type": "public_order_url",
    "provider": "美团点餐",
    "order_url": "https://rms.meituan.com/diancan/14/2HpfZPxOFw0",
    "usage": "可直接打开链接进入点单页面",
    "alternative_access": "用户到店后也可以扫描桌面二维码进入同一入口",
    "notes": [
        "该链接来自门店公开二维码对应的下单入口",
        "如需堂食，到店后扫码或直接告知店员也可以点单",
        "如页面要求登录、定位或平台内打开，以美团页面实际提示为准",
    ],
}

COMMON_INPUT_SCHEMA = {
    "type": "object",
    "properties": {},
    "required": [],
}

COMMON_ANNOTATIONS = {
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": False,
}


def build_text_result(payload: Any) -> dict[str, Any]:
    """将业务数据包装成 MCP content 结构。"""
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(payload, ensure_ascii=False, indent=2),
            }
        ]
    }


def get_restaurant_info() -> dict[str, Any]:
    """获取餐厅基本信息。"""
    return build_text_result(RESTAURANT_INFO)


def get_menu() -> dict[str, Any]:
    """获取菜单。"""
    return build_text_result(MENU_DATA)


def get_delivery_info() -> dict[str, Any]:
    """获取外卖信息。"""
    return build_text_result(DELIVERY_INFO)


def get_reservation_info() -> dict[str, Any]:
    """获取预约信息。"""
    return build_text_result(RESERVATION_INFO)


def get_wifi_info() -> dict[str, Any]:
    """获取到店 Wi-Fi 指引。"""
    return build_text_result(WIFI_INFO)


def get_order_entry() -> dict[str, Any]:
    """获取公开下单入口。"""
    return build_text_result(ORDER_ENTRY_INFO)


TOOLS = {
    "get_restaurant_info": {
        "handler": get_restaurant_info,
        "description": "查询王聚财面皮铺的基本信息",
        "inputSchema": COMMON_INPUT_SCHEMA,
        "annotations": COMMON_ANNOTATIONS,
    },
    "get_menu": {
        "handler": get_menu,
        "description": "获取王聚财面皮铺的完整菜单",
        "inputSchema": COMMON_INPUT_SCHEMA,
        "annotations": COMMON_ANNOTATIONS,
    },
    "get_delivery_info": {
        "handler": get_delivery_info,
        "description": "获取外卖配送信息",
        "inputSchema": COMMON_INPUT_SCHEMA,
        "annotations": COMMON_ANNOTATIONS,
    },
    "get_reservation_info": {
        "handler": get_reservation_info,
        "description": "获取堂食预约信息",
        "inputSchema": COMMON_INPUT_SCHEMA,
        "annotations": COMMON_ANNOTATIONS,
    },
    "get_wifi_info": {
        "handler": get_wifi_info,
        "description": "获取到店 Wi-Fi 指引，不直接返回密码",
        "inputSchema": COMMON_INPUT_SCHEMA,
        "annotations": COMMON_ANNOTATIONS,
    },
    "get_order_entry": {
        "handler": get_order_entry,
        "description": "获取公开下单入口，支持直接打开链接或到店扫码进入",
        "inputSchema": COMMON_INPUT_SCHEMA,
        "annotations": COMMON_ANNOTATIONS,
    },
}


def build_success_response(result: dict[str, Any], request_id: Any, jsonrpc: str | None) -> dict[str, Any]:
    """兼容 JSON-RPC MCP 与简单调试请求两种返回格式。"""
    if jsonrpc or request_id is not None:
        return {
            "jsonrpc": jsonrpc or "2.0",
            "id": request_id,
            "result": result,
        }
    return result


def build_error_response(
    code: int,
    message: str,
    request_id: Any = None,
    jsonrpc: str | None = None,
) -> dict[str, Any]:
    """统一输出 MCP 与 JSON-RPC 错误结构。"""
    if jsonrpc or request_id is not None:
        return {
            "jsonrpc": jsonrpc or "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message,
            },
        }
    return {
        "error": message,
        "code": code,
    }


def handle_mcp_request(request: dict[str, Any]) -> dict[str, Any]:
    """处理 MCP 请求。"""
    method = request.get("method")
    jsonrpc = request.get("jsonrpc")
    request_id = request.get("id")

    if not method:
        return build_error_response(-32600, "Missing method", request_id, jsonrpc)

    if method == "initialize":
        return build_success_response(
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": False,
                    }
                },
                "serverInfo": {
                    "name": SERVER_NAME,
                    "version": SERVER_VERSION,
                },
            },
            request_id,
            jsonrpc,
        )

    if method == "tools/list":
        return build_success_response(
            {
                "tools": [
                    {
                        "name": name,
                        "description": tool["description"],
                        "inputSchema": tool["inputSchema"],
                        "annotations": tool["annotations"],
                    }
                    for name, tool in TOOLS.items()
                ]
            },
            request_id,
            jsonrpc,
        )

    if method == "tools/call":
        params = request.get("params") or {}
        tool_name = params.get("name")
        if not tool_name:
            return build_error_response(-32602, "Missing tool name", request_id, jsonrpc)

        tool = TOOLS.get(tool_name)
        if tool is None:
            return build_error_response(-32601, f"Unknown tool: {tool_name}", request_id, jsonrpc)

        return build_success_response(tool["handler"](), request_id, jsonrpc)

    return build_error_response(-32601, f"Unknown method: {method}", request_id, jsonrpc)


class MCPHandler(BaseHTTPRequestHandler):
    """最小可运行的 MCP over HTTP 处理器。"""

    def _send_common_headers(self, content_length: int) -> None:
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(content_length))
        self.end_headers()

    def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self._send_common_headers(len(body))
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        """处理跨域预检请求。"""
        self.send_response(204)
        self._send_common_headers(0)

    def do_GET(self) -> None:
        """GET 仅返回健康检查，避免暴露全部业务数据。"""
        response = {
            "name": SERVER_NAME,
            "version": SERVER_VERSION,
            "status": "ok",
            "transport": "streamable-http",
            "tools": list(TOOLS.keys()),
        }
        self._send_json(response)

    def do_POST(self) -> None:
        """POST 请求走 MCP 协议。"""
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(build_error_response(-32600, "Invalid Content-Length", jsonrpc="2.0"), status=400)
            return

        if content_length > MAX_BODY_BYTES:
            self._send_json(build_error_response(-32000, "Request body too large", jsonrpc="2.0"), status=413)
            return

        raw_body = self.rfile.read(content_length).decode("utf-8")
        try:
            request = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            self._send_json(build_error_response(-32700, "Parse error", jsonrpc="2.0"), status=400)
            return

        self._send_json(handle_mcp_request(request))

    def log_message(self, format: str, *args: Any) -> None:
        print(f"[MCP] {self.client_address[0]} - {format % args}")


def main() -> None:
    """启动本地调试服务。"""
    server = HTTPServer((DEFAULT_HOST, DEFAULT_PORT), MCPHandler)
    print(f"王聚财面皮铺 MCP Server {SERVER_VERSION} 运行中...")
    print(f"监听地址: http://{DEFAULT_HOST}:{DEFAULT_PORT}/")
    print("GET  /  健康检查")
    print("POST /  MCP 协议调用")
    print("如需对外监听，请显式设置 MCP_HOST=0.0.0.0")
    server.serve_forever()


if __name__ == "__main__":
    main()
