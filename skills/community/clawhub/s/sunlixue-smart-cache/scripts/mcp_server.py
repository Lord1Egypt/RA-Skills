#!/usr/bin/env python3
"""
Smart Cache MCP Server
提供 MCP 协议接口，允许其他 AI 工具通过 MCP 协议访问缓存
支持 stdio 和 HTTP 两种传输模式
"""

import os
import sys
import json
import argparse
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from cache_api import SmartCache, CacheEntry, CacheStats


# MCP 协议常量
MCP_VERSION = "2024-11-05"
PROTOCOL_VERSION = "2025-03-26"


class MCPProtocol:
    """MCP 协议处理器"""

    @staticmethod
    def parse_request(request: Dict) -> Dict[str, Any]:
        """解析 MCP 请求"""
        return request

    @staticmethod
    def build_response(
        result: Any = None,
        error: Optional[str] = None,
        request_id: Optional[str] = None
    ) -> Dict:
        """构建 MCP 响应"""
        response = {
            "jsonrpc": "2.0",
            "protocolVersion": PROTOCOL_VERSION,
        }

        if error is not None:
            response["error"] = {
                "code": -32603,
                "message": str(error)
            }
        else:
            response["result"] = result

        if request_id is not None:
            response["id"] = request_id

        return response


class MCPServer:
    """
    Smart Cache MCP 服务器
    实现 MCP 协议的核心功能
    """

    def __init__(self, cache_dir: Optional[str] = None):
        self.cache = SmartCache(cache_dir=cache_dir)
        self.capabilities = {
            "tools": {
                "cache_query": {
                    "description": "查询缓存，精确匹配优先",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "查询文本"
                            },
                            "threshold": {
                                "type": "number",
                                "description": "L2 语义匹配阈值（0-1）",
                                "default": 0.85
                            }
                        },
                        "required": ["query"]
                    }
                },
                "cache_query_l1": {
                    "description": "L1 精确缓存查询",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "查询文本"
                            }
                        },
                        "required": ["query"]
                    }
                },
                "cache_query_l2": {
                    "description": "L2 语义缓存查询（需要 embedding）",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "查询文本"
                            },
                            "threshold": {
                                "type": "number",
                                "description": "相似度阈值（0-1）",
                                "default": 0.85
                            }
                        },
                        "required": ["query"]
                    }
                },
                "cache_store": {
                    "description": "存储到缓存",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "查询文本"
                            },
                            "response": {
                                "type": "string",
                                "description": "响应文本"
                            },
                            "tokens": {
                                "type": "integer",
                                "description": "节省的 token 数量",
                                "default": 0
                            },
                            "cache_type": {
                                "type": "string",
                                "description": "缓存类型: l1, l2, both",
                                "default": "both"
                            }
                        },
                        "required": ["query", "response"]
                    }
                },
                "cache_stats": {
                    "description": "获取缓存统计信息",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                },
                "cache_clean": {
                    "description": "清理缓存",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "mode": {
                                "type": "string",
                                "description": "清理模式: expired, all",
                                "default": "expired"
                            }
                        }
                    }
                }
            }
        }

    def handle_initialize(self, params: Dict) -> Dict:
        """处理初始化请求"""
        return {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {
                "tools": True
            },
            "serverInfo": {
                "name": "smart-cache",
                "version": "1.0.0"
            }
        }

    def handle_tools_list(self, params: Dict) -> Dict:
        """处理工具列表请求"""
        return {
            "tools": [
                {
                    "name": name,
                    "description": info["description"],
                    "inputSchema": info["inputSchema"]
                }
                for name, info in self.capabilities["tools"].items()
            ]
        }

    def handle_tools_call(self, params: Dict) -> Dict:
        """处理工具调用请求"""
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})

        if tool_name not in self.capabilities["tools"]:
            raise ValueError(f"未知工具: {tool_name}")

        result = self._call_tool(tool_name, tool_args)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, ensure_ascii=False, indent=2)
                }
            ]
        }

    def _call_tool(self, name: str, args: Dict) -> Any:
        """执行工具调用"""
        if name == "cache_query":
            result = self.cache.query(
                args["query"],
                threshold=args.get("threshold")
            )
            return self._format_cache_entry(result)

        elif name == "cache_query_l1":
            result = self.cache.query_l1(args["query"])
            return self._format_cache_entry(result)

        elif name == "cache_query_l2":
            result = self.cache.query_l2(
                args["query"],
                threshold=args.get("threshold")
            )
            return self._format_cache_entry(result)

        elif name == "cache_store":
            success = self.cache.store(
                args["query"],
                args["response"],
                tokens=args.get("tokens", 0),
                cache_type=args.get("cache_type", "both")
            )
            return {"success": success}

        elif name == "cache_stats":
            stats = self.cache.get_stats()
            return self._format_stats(stats)

        elif name == "cache_clean":
            mode = args.get("mode", "expired")
            if mode == "all":
                count = self.cache.clean_all()
            else:
                count = self.cache.clean_expired()
            return {"cleaned": count}

        else:
            raise ValueError(f"未实现的工具: {name}")

    def _format_cache_entry(self, entry: Optional[CacheEntry]) -> Any:
        """格式化缓存条目"""
        if entry is None:
            return {"hit": False}

        return {
            "hit": True,
            "cache_type": entry.cache_type,
            "similarity": entry.similarity,
            "response": entry.response,
            "hit_count": entry.hit_count,
            "tokens_saved": entry.tokens_saved,
            "created_at": entry.created_at
        }

    def _format_stats(self, stats: CacheStats) -> Dict:
        """格式化统计信息"""
        total = stats.total_requests
        hits = stats.l1_hits + stats.l2_hits
        hit_rate = (hits / total * 100) if total > 0 else 0

        return {
            "total_requests": total,
            "l1_hits": stats.l1_hits,
            "l2_hits": stats.l2_hits,
            "misses": stats.misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "l1_entries": stats.l1_entries,
            "l2_entries": stats.l2_entries,
            "tokens_saved": stats.tokens_saved,
            "cost_saved": f"${stats.cost_saved:.4f}"
        }


def run_stdio_server(cache_dir: Optional[str] = None):
    """
    以 stdio 模式运行 MCP 服务器
    用于通过标准输入/输出与父进程通信
    """
    server = MCPServer(cache_dir=cache_dir)
    protocol = MCPProtocol()

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line.strip())
            request_id = request.get("id")

            try:
                method = request.get("method")
                params = request.get("params", {})

                if method == "initialize":
                    result = server.handle_initialize(params)
                elif method == "tools/list":
                    result = server.handle_tools_list(params)
                elif method == "tools/call":
                    result = server.handle_tools_call(params)
                else:
                    raise ValueError(f"未知方法: {method}")

                response = protocol.build_response(result, request_id=request_id)

            except Exception as e:
                response = protocol.build_response(
                    error=str(e),
                    request_id=request_id
                )

            print(json.dumps(response, ensure_ascii=False), flush=True)

        except json.JSONDecodeError:
            continue
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32700, "message": str(e)}
            }), flush=True)


def run_http_server(cache_dir: Optional[str] = None, host: str = "localhost", port: int = 8080):
    """
    以 HTTP 模式运行 MCP 服务器
    """
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import urllib.parse

    server = MCPServer(cache_dir=cache_dir)
    protocol = MCPProtocol()

    class MCPHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            request = json.loads(body)

            try:
                method = self.path.strip('/')
                params = json.loads(request.get('params', '{}'))

                if method == "initialize":
                    result = server.handle_initialize(params)
                elif method == "tools/list":
                    result = server.handle_tools_list(params)
                elif method == "tools/call":
                    result = server.handle_tools_call(params)
                else:
                    raise ValueError(f"未知方法: {method}")

                response = protocol.build_response(result)

            except Exception as e:
                response = protocol.build_response(error=str(e))

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode())

        def do_GET(self):
            if self.path == "/health":
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode())
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, format, *args):
            pass  # 静默日志

    httpd = HTTPServer((host, port), MCPHandler)
    print(f"MCP Server 运行于 http://{host}:{port}")
    print("按 Ctrl+C 停止服务器")
    httpd.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Smart Cache MCP Server")
    parser.add_argument(
        "--mode",
        choices=["stdio", "http"],
        default="stdio",
        help="服务器模式（默认 stdio）"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="HTTP 服务器监听地址（默认 localhost）"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="HTTP 服务器端口（默认 8080）"
    )
    parser.add_argument(
        "--cache-dir",
        help="缓存目录路径"
    )

    args = parser.parse_args()

    if args.mode == "http":
        run_http_server(
            cache_dir=args.cache_dir,
            host=args.host,
            port=args.port
        )
    else:
        run_stdio_server(cache_dir=args.cache_dir)


if __name__ == '__main__':
    main()
