"""
检查登录状态
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(__file__))

from mcp_dispatcher import call_tool, check_running

if __name__ == "__main__":
    if not check_running():
        print(json.dumps({"error": "MCP service not running"}))
        sys.exit(1)
    result = call_tool("check_login_status")
    for item in result:
        if item.get("type") == "text":
            print(item["text"])
