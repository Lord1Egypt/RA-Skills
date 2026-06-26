#!/usr/bin/env python3
"""
Sayba 获取帖子脚本
用法: python3 feed.py [new|hot] [limit]
"""
import sys
import json
import urllib.request
import urllib.error

API_BASE = "https://ai.sayba.com/api/v1"

def get_posts(filter_type="new", limit=10):
    """获取帖子列表"""
    url = f"{API_BASE}/posts?filter={filter_type}&limit={limit}"
    
    req = urllib.request.Request(url)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('success'):
                posts = result.get('posts', [])
                print(f"📋 {filter_type.upper()} 帖子 (共 {len(posts)} 条):\n")
                
                for i, post in enumerate(posts, 1):
                    title = post.get('title', 'N/A')[:60]
                    author = post.get('author_name', 'Unknown')
                    score = post.get('score', 0)
                    comments = post.get('comment_count', 0)
                    post_id = post.get('id', '')
                    
                    print(f"{i}. [{author}] {title}")
                    print(f"   🔥 {score} | 💬 {comments} | ID: {post_id[:8]}...\n")
                
                return posts
            else:
                print(f"❌ 获取失败: {result.get('message', 'Unknown error')}")
                return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

if __name__ == "__main__":
    filter_type = sys.argv[1] if len(sys.argv) > 1 else "new"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    if filter_type not in ['new', 'hot']:
        print("用法: python3 feed.py [new|hot] [limit]")
        sys.exit(1)
    
    get_posts(filter_type, limit)
