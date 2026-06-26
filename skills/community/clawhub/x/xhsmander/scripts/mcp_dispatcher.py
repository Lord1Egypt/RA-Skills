"""
xiaohongshu-mcp HTTP+JSON-RPC 调度器
每次调用自动处理 initialize + session 管理
"""
import urllib.request
import json
import os

MCP_URL = "http://localhost:18060/mcp"

def _init():
    """初始化并返回 session_id"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "xhsmander", "version": "1.0"}
        },
        "id": 1
    }
    req = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        json.loads(resp.read().decode())
        return resp.headers.get("Mcp-Session-Id")

def call_tool(tool_name, arguments=None):
    """
    调用 MCP 工具，返回解析后的 content 列表
    """
    if arguments is None:
        arguments = {}
    
    session_id = _init()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Mcp-Session-Id": session_id
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": 2
    }
    req = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode())
        if "result" in result and "content" in result["result"]:
            return result["result"]["content"]
        return result

def check_running():
    """检查 MCP 服务是否运行"""
    try:
        req = urllib.request.Request(MCP_URL, method="HEAD")
        with urllib.request.urlopen(req, timeout=3):
            return True
    except:
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: mcp_dispatcher.py <tool_name> [arg_json]")
        sys.exit(1)
    
    tool = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    
    result = call_tool(tool, args)
    print(json.dumps(result, ensure_ascii=False))
