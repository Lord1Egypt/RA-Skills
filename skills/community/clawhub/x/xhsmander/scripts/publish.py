"""
发布图文到小红书

用法: python publish.py "<标题>" "<正文>" "<图片路径(容器内)>" "<标签(逗号分隔)>"

示例:
  python publish.py "测试标题" "测试内容" "/app/images/test.png" "标签1,标签2"
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(__file__))

from mcp_dispatcher import call_tool, check_running

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: publish.py <title> <content> <image_path> <tags_csv>")
        sys.exit(1)
    
    title = sys.argv[1]
    content = sys.argv[2]
    image_path = sys.argv[3]  # 容器内路径，如 /app/images/xxx.png
    tags = [t.strip() for t in sys.argv[4].split(",") if t.strip()]
    
    if not check_running():
        print("MCP service not running")
        sys.exit(1)
    
    result = call_tool("publish_content", {
        "title": title,
        "content": content,
        "images": [image_path],
        "tags": tags
    })
    
    for item in result:
        if item.get("type") == "text":
            print(item["text"])
        elif item.get("type") == "image":
            # 图片响应通常是上传后的预览
            print(f"[Image] mimeType: {item.get('mimeType', 'image/png')}")
