#!/usr/bin/env python3
"""
小红书笔记发布脚本

自动检查登录状态并发布笔记到小红书。

Usage:
    python publish.py --title "标题" --content "正文" --images "/path/img.png" --tags "标签1,标签2"
"""

import argparse
import json
import requests
import sys

BASE_URL = "http://localhost:18060"
TIMEOUT = 180  # 发布需要较长时间


def check_login():
    """检查登录状态"""
    try:
        resp = requests.get(f"{BASE_URL}/api/v1/login/status", timeout=10)
        data = resp.json()
        if data.get("success") and data.get("data", {}).get("is_logged_in"):
            print(f"✅ 已登录: {data['data'].get('username', 'Unknown')}")
            return True
        else:
            print("❌ 未登录，请运行登录工具:")
            print("   /Users/mac/.openclaw/extensions/xiaohongshu-mcp/xiaohongshu-login-darwin-amd64")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ MCP 服务未启动，请先运行:")
        print("   /Users/mac/.openclaw/extensions/xiaohongshu-mcp/xiaohongshu-mcp-darwin-amd64 -headless=true &")
        sys.exit(1)


def publish(title, content, images, tags=None):
    """发布笔记"""
    if not check_login():
        sys.exit(1)
    
    payload = {
        "title": title,
        "content": content,
        "images": images if isinstance(images, list) else [images]
    }
    
    if tags:
        payload["tags"] = tags if isinstance(tags, list) else tags.split(",")
    
    print(f"📝 正在发布: {title}")
    print(f"   图片: {len(payload['images'])} 张")
    
    try:
        resp = requests.post(
            f"{BASE_URL}/api/v1/publish",
            json=payload,
            timeout=TIMEOUT
        )
        data = resp.json()
        
        if data.get("success"):
            print("🎉 发布成功!")
            return data
        else:
            print(f"❌ 发布失败: {data.get('error', 'Unknown')}")
            return data
    except requests.exceptions.Timeout:
        print("❌ 发布超时，请检查浏览器状态")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="小红书笔记发布")
    parser.add_argument("--title", required=True, help="笔记标题")
    parser.add_argument("--content", required=True, help="正文内容")
    parser.add_argument("--images", required=True, help="图片路径（多个用逗号分隔）")
    parser.add_argument("--tags", default="", help="标签（逗号分隔）")
    
    args = parser.parse_args()
    
    images = [img.strip() for img in args.images.split(",")]
    tags = [tag.strip() for tag in args.tags.split(",")] if args.tags else None
    
    result = publish(args.title, args.content, images, tags)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()