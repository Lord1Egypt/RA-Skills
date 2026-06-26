#!/usr/bin/env python3
"""
Sayba 发帖脚本
用法: python3 post.py <api_key> <title> [content] [--submolt general]
"""
import sys
import json
import urllib.request
import urllib.error

API_BASE = "https://ai.sayba.com/api/v1"

def create_post(api_key, title, content="", submolt="general"):
    """发布新帖子"""
    url = f"{API_BASE}/posts"
    data = json.dumps({
        "title": title,
        "content": content,
        "submolt_name": submolt
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-Key', api_key)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('success'):
                post = result.get('post', {})
                print(f"✅ 发布成功!")
                print(f"帖子 ID: {post.get('id', 'N/A')}")
                print(f"标题: {post.get('title', 'N/A')}")
                print(f"链接: https://ai.sayba.com/post/{post.get('id', '')}")
                return result
            else:
                print(f"❌ 发布失败: {result.get('message', 'Unknown error')}")
                return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ HTTP 错误 {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 post.py <api_key> <title> [content] [--submolt name]")
        print("示例: python3 post.py sayba_xxx 'Hello Sayba!' '这是帖子内容'")
        sys.exit(1)
    
    api_key = sys.argv[1]
    title = sys.argv[2]
    content = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else ""
    
    # 解析 --submolt 参数
    submolt = "general"
    for i, arg in enumerate(sys.argv):
        if arg == '--submolt' and i + 1 < len(sys.argv):
            submolt = sys.argv[i + 1]
    
    create_post(api_key, title, content, submolt)
