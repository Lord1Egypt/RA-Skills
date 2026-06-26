#!/usr/bin/env python3
"""
V2EX MCP 服务
提供 V2EX API 的工具供 AI 助手调用
"""

import argparse
import json
import ssl
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import urllib3
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import AnyUrl

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "v2ex_monitor_config.json"
DATA_DIR = BASE_DIR / "v2ex_monitor_data"
DEFAULT_NODES = ["python", "linux", "programmer", "hardware", "macos"]
DEFAULT_API_KEY = ""
BASE_URL = "https://www.v2ex.com/api/v2"


class V2EXClient:
    """V2EX API 客户端"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "V2EX-MCP/1.0"
        }

    def _request(self, method: str, url: str, **kwargs) -> dict:
        """发送请求"""
        kwargs.setdefault("headers", self.headers)
        with urllib3.PoolManager(ssl_context=self.ctx) as pool:
            resp = pool.request(method, url, timeout=15, **kwargs)
            data = json.loads(resp.data.decode("utf-8"))
            return data

    def get_node_topics(self, node_name: str, page: int = 1) -> list:
        """获取节点主题"""
        url = f"{BASE_URL}/nodes/{node_name}/topics"
        data = self._request("GET", url, fields={"p": page})
        return data.get("result", [])

    def get_topic(self, topic_id: int) -> dict:
        """获取主题详情"""
        url = f"{BASE_URL}/topics/{topic_id}"
        data = self._request("GET", url)
        return data.get("result", {})

    def get_topic_replies(self, topic_id: int, page: int = 1) -> list:
        """获取主题回复"""
        url = f"{BASE_URL}/topics/{topic_id}/replies"
        data = self._request("GET", url, fields={"p": page})
        return data.get("result", [])

    def get_notifications(self, page: int = 1) -> list:
        """获取提醒"""
        url = f"{BASE_URL}/notifications"
        data = self._request("GET", url, fields={"p": page})
        return data.get("result", [])

    def get_me(self) -> dict:
        """获取当前用户信息"""
        url = f"{BASE_URL}/member"
        data = self._request("GET", url)
        return data.get("result", {})

    def get_node(self, node_name: str) -> dict:
        """获取节点信息"""
        url = f"{BASE_URL}/nodes/{node_name}"
        data = self._request("GET", url)
        return data.get("result", {})


def load_config() -> dict:
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"nodes": DEFAULT_NODES, "apikey": DEFAULT_API_KEY}


def get_client() -> V2EXClient:
    """获取 API 客户端"""
    config = load_config()
    api_key = config.get("apikey", DEFAULT_API_KEY)
    if not api_key:
        raise ValueError("未配置 V2EX API Key，请先写入 v2ex_monitor_config.json 或调用 v2ex_config")
    return V2EXClient(api_key)


# 创建 MCP 服务器
app = Server("v2ex-monitor")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用工具"""
    return [
        Tool(
            name="v2ex_get_node_topics",
            description="获取 V2EX 指定节点的主题列表，可以用来监控某个节点的新帖子",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_name": {
                        "type": "string",
                        "description": "节点名称，如 python, linux, programmer, hardware, macos, apple 等"
                    },
                    "page": {
                        "type": "integer",
                        "description": "页码，默认 1",
                        "default": 1
                    }
                },
                "required": ["node_name"]
            }
        ),
        Tool(
            name="v2ex_get_topic",
            description="获取 V2EX 主题的详细内容，包括正文和统计信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic_id": {
                        "type": "integer",
                        "description": "主题 ID"
                    }
                },
                "required": ["topic_id"]
            }
        ),
        Tool(
            name="v2ex_get_topic_replies",
            description="获取 V2EX 主题的所有回复",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic_id": {
                        "type": "integer",
                        "description": "主题 ID"
                    },
                    "page": {
                        "type": "integer",
                        "description": "页码，默认 1",
                        "default": 1
                    }
                },
                "required": ["topic_id"]
            }
        ),
        Tool(
            name="v2ex_get_notifications",
            description="获取当前用户的提醒通知",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "integer",
                        "description": "页码，默认 1",
                        "default": 1
                    }
                }
            }
        ),
        Tool(
            name="v2ex_get_my_info",
            description="获取当前登录用户的个人信息",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="v2ex_get_node_info",
            description="获取 V2EX 节点的信息，如节点名称、描述、帖子数等",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_name": {
                        "type": "string",
                        "description": "节点名称"
                    }
                },
                "required": ["node_name"]
            }
        ),
        Tool(
            name="v2ex_monitor_topics",
            description="运行一次监控，检查各节点的新帖子并生成报告",
            inputSchema={
                "type": "object",
                "properties": {
                    "nodes": {
                        "type": "string",
                        "description": "要监控的节点，用逗号分隔，默认 python,linux,programmer,hardware,macos"
                    }
                }
            }
        ),
        Tool(
            name="v2ex_config",
            description="配置 V2EX 监控的节点和 API Key",
            inputSchema={
                "type": "object",
                "properties": {
                    "nodes": {
                        "type": "string",
                        "description": "监控的节点，用逗号分隔"
                    },
                    "apikey": {
                        "type": "string",
                        "description": "V2EX API Key"
                    }
                }
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """调用工具"""
    client = get_client()

    try:
        if name == "v2ex_get_node_topics":
            topics = client.get_node_topics(
                arguments["node_name"],
                arguments.get("page", 1)
            )
            # 简化返回数据
            simplified = []
            for t in topics[:20]:  # 限制返回数量
                simplified.append({
                    "id": t.get("id"),
                    "title": t.get("title"),
                    "replies": t.get("replies"),
                    "url": t.get("url"),
                })
            return [TextContent(type="text", text=json.dumps(simplified, ensure_ascii=False))]

        elif name == "v2ex_get_topic":
            topic = client.get_topic(arguments["topic_id"])
            return [TextContent(type="text", text=json.dumps(topic, ensure_ascii=False, indent=2))]

        elif name == "v2ex_get_topic_replies":
            replies = client.get_topic_replies(
                arguments["topic_id"],
                arguments.get("page", 1)
            )
            return [TextContent(type="text", text=json.dumps(replies, ensure_ascii=False))]

        elif name == "v2ex_get_notifications":
            notifications = client.get_notifications(arguments.get("page", 1))
            return [TextContent(type="text", text=json.dumps(notifications, ensure_ascii=False))]

        elif name == "v2ex_get_my_info":
            info = client.get_me()
            return [TextContent(type="text", text=json.dumps(info, ensure_ascii=False, indent=2))]

        elif name == "v2ex_get_node_info":
            info = client.get_node(arguments["node_name"])
            return [TextContent(type="text", text=json.dumps(info, ensure_ascii=False, indent=2))]

        elif name == "v2ex_monitor_topics":
            # 运行监控
            nodes = arguments.get("nodes", "").split(",") if arguments.get("nodes") else DEFAULT_NODES
            nodes = [n.strip() for n in nodes if n.strip()]

            all_topics = []
            for node in nodes:
                topics = client.get_node_topics(node)
                for t in topics:
                    t["_source_node"] = node
                all_topics.extend(topics)

            # 按回复数排序
            hot_topics = sorted(all_topics, key=lambda x: x.get("replies", 0), reverse=True)[:15]

            report = {
                "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "监控节点": nodes,
                "帖子总数": len(all_topics),
                "热门帖子": [{
                    "id": t.get("id"),
                    "标题": t.get("title"),
                    "回复数": t.get("replies"),
                    "节点": t.get("_source_node"),
                    "链接": t.get("url"),
                } for t in hot_topics]
            }
            return [TextContent(type="text", text=json.dumps(report, ensure_ascii=False, indent=2))]

        elif name == "v2ex_config":
            config = load_config()
            if arguments.get("nodes"):
                config["nodes"] = [n.strip() for n in arguments["nodes"].split(",")]
            if arguments.get("apikey"):
                config["apikey"] = arguments["apikey"]
            CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return [TextContent(type="text", text=json.dumps({"状态": "配置已保存", "配置": config}, ensure_ascii=False))]

        else:
            return [TextContent(type="text", text=f"未知工具: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"错误: {str(e)}")]


async def main():
    """主函数"""
    # 解析参数
    parser = argparse.ArgumentParser(description="V2EX MCP 服务")
    parser.add_argument("--stdio", action="store_true", help="STDIO 模式（默认）")
    parser.add_argument("--host", default="0.0.0.0", help="HTTP 模式主机")
    parser.add_argument("--port", type=int, default=8080, help="HTTP 模式端口")
    args = parser.parse_args()

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
