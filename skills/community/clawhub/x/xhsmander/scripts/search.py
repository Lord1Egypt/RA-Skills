"""
搜索小红书内容

用法: python search.py "<关键词>" [数量]
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(__file__))

from mcp_dispatcher import call_tool, check_running

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else ""
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    if not keyword:
        print("Usage: search.py <keyword> [limit]")
        sys.exit(1)
    
    if not check_running():
        print("MCP service not running")
        sys.exit(1)
    
    result = call_tool("search_feeds", {
        "keyword": keyword,
        "limit": limit
    })
    
    for item in result:
        if item.get("type") == "text":
            print(item["text"])
