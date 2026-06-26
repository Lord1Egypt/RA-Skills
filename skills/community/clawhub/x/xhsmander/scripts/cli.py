"""
xhsmander CLI - 统一的 MCP 操作入口

用法:
  python cli.py check-login
  python cli.py get-qrcode
  python cli.py publish "<标题>" "<正文>" "<容器图片路径>" "<标签1,标签2>"
  python cli.py search "<关键词>" [数量]
  python cli.py list-feeds [数量]
  python cli.py like <feed_id> <xsec_token>
  python cli.py favorite <feed_id> <xsec_token>
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from mcp_dispatcher import call_tool, check_running

COMMANDS = {
    "check-login":    ("check_login_status", {}),
    "get-qrcode":     ("get_login_qrcode", {}),
}

def cmd_check_login():
    result = call_tool("check_login_status")
    for item in result:
        if item.get("type") == "text":
            print(item["text"])

def cmd_get_qrcode():
    import base64
    result = call_tool("get_login_qrcode")
    for item in result:
        if item.get("type") == "text":
            print(item["text"])
        elif item.get("type") == "image":
            data = item.get("data")
            if data:
                img_bytes = base64.b64decode(data)
                out_path = os.path.join(os.path.dirname(__file__), "login_qrcode.png")
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                print(f"QR saved: {out_path}")

def cmd_publish(title, content, image_path, tags_csv):
    tags = [t.strip() for t in tags_csv.split(",") if t.strip()]
    result = call_tool("publish_content", {
        "title": title,
        "content": content,
        "images": [image_path],
        "tags": tags
    })
    for item in result:
        if item.get("type") == "text":
            print(item["text"])

def cmd_search(keyword, limit=10):
    result = call_tool("search_feeds", {"keyword": keyword, "limit": limit})
    for item in result:
        if item.get("type") == "text":
            print(item["text"])

def cmd_list_feeds(limit=10):
    result = call_tool("list_feeds", {"limit": limit})
    for item in result:
        if item.get("type") == "text":
            print(item["text"])

def cmd_like(feed_id, xsec_token):
    result = call_tool("like_feed", {"feed_id": feed_id, "xsec_token": xsec_token})
    for item in result:
        if item.get("type") == "text":
            print(item["text"])

def cmd_favorite(feed_id, xsec_token):
    result = call_tool("favorite_feed", {"feed_id": feed_id, "xsec_token": xsec_token})
    for item in result:
        if item.get("type") == "text":
            print(item["text"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    if not check_running():
        print("ERROR: MCP service not running. Start Docker first.")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "check-login":
        cmd_check_login()
    elif cmd == "get-qrcode":
        cmd_get_qrcode()
    elif cmd == "publish":
        if len(sys.argv) < 6:
            print("Usage: cli.py publish <title> <content> <image_path> <tags_csv>")
            sys.exit(1)
        cmd_publish(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: cli.py search <keyword> [limit]")
            sys.exit(1)
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        cmd_search(sys.argv[2], limit)
    elif cmd == "list-feeds":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        cmd_list_feeds(limit)
    elif cmd == "like":
        if len(sys.argv) < 4:
            print("Usage: cli.py like <feed_id> <xsec_token>")
            sys.exit(1)
        cmd_like(sys.argv[2], sys.argv[3])
    elif cmd == "favorite":
        if len(sys.argv) < 4:
            print("Usage: cli.py favorite <feed_id> <xsec_token>")
            sys.exit(1)
        cmd_favorite(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
