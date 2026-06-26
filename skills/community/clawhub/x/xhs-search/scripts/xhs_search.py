#!/usr/bin/env python3
"""
小红书 MCP 搜索封装
用法: python3 xhs_search.py <关键词> [排序方式: 最新/最热]
"""
import urllib.request, json, sys

MCP_URL = "http://localhost:18060/mcp"

def mcp_init():
    data = json.dumps({"jsonrpc":"2.0","id":1,"method":"initialize",
        "params":{"protocolVersion":"2024-11-05","capabilities":{},
                  "clientInfo":{"name":"openclaw","version":"1.0"}}}).encode()
    req = urllib.request.Request(MCP_URL, data=data,
        headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream"})
    resp = urllib.request.urlopen(req, timeout=30)
    return resp.headers.get("Mcp-Session-Id","")

def mcp_call(tool, args, sid):
    data = json.dumps({"jsonrpc":"2.0","id":2,"method":"tools/call",
        "params":{"name":tool,"arguments":args}}).encode()
    req = urllib.request.Request(MCP_URL, data=data,
        headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream",
                 "Mcp-Session-Id":sid})
    resp = urllib.request.urlopen(req, timeout=60)
    return json.loads(resp.read().decode())

def search(keyword, sort_by="最新", count=10):
    sid = mcp_init()
    # initialized notification
    data = json.dumps({"jsonrpc":"2.0","method":"notifications/initialized","params":{}}).encode()
    req = urllib.request.Request(MCP_URL, data=data,
        headers={"Content-Type":"application/json","Accept":"application/json, text/event-stream","Mcp-Session-Id":sid})
    urllib.request.urlopen(req, timeout=10)
    
    r = mcp_call("search_feeds", {"keyword": keyword, "filters": {"sort_by": sort_by}}, sid)
    raw = r["result"]["content"][0]["text"]
    feeds = json.loads(raw).get("feeds", [])
    return feeds[:count]

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else "AP微积分"
    sort_by = sys.argv[2] if len(sys.argv) > 2 else "最新"
    feeds = search(keyword, sort_by)
    print(f"=== 小红书搜索: {keyword} (排序:{sort_by}) 共{len(feeds)}条 ===\n")
    for i, f in enumerate(feeds, 1):
        nc = f["noteCard"]
        u = nc["user"]
        ii = nc["interactInfo"]
        print(f"{i}. {nc.get('displayTitle','无标题')}")
        print(f"   @{u.get('nickName','?')} | 👍{ii.get('likedCount',0)} | ⭐{ii.get('collectedCount',0)} | 💬{ii.get('commentCount',0)}")
        print(f"   ID: {f.get('id','')}")
        print()
