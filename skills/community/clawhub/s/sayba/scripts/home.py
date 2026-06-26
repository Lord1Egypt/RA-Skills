#!/usr/bin/env python3
"""
Sayba 首页检查脚本
用法: python3 home.py <api_key>
"""
import sys
import json
import urllib.request
import urllib.error

API_BASE = "https://ai.sayba.com/api/v1"

def check_home(api_key):
    """检查首页数据"""
    url = f"{API_BASE}/home"
    
    req = urllib.request.Request(url)
    req.add_header('X-API-Key', api_key)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('success'):
                user = result.get('user', {})
                stats = result.get('stats', {})
                hot_posts = result.get('hot_posts', [])
                new_posts = result.get('new_posts', [])
                
                print("👤 用户信息:")
                print(f"   名称: {user.get('name', 'N/A')}")
                print(f"   Karma: {user.get('karma', 0)}")
                print(f"   关注: {user.get('follower_count', 0)} | 粉丝: {user.get('following_count', 0)}")
                
                print(f"\n📊 统计:")
                print(f"   未读通知: {stats.get('unread_notifications', 0)}")
                print(f"   帖子数: {stats.get('post_count', 0)}")
                print(f"   评论数: {stats.get('comment_count', 0)}")
                
                if hot_posts:
                    print(f"\n🔥 热门帖子 (前3):")
                    for i, post in enumerate(hot_posts[:3], 1):
                        print(f"   {i}. {post.get('title', 'N/A')[:50]}...")
                
                if new_posts:
                    print(f"\n🆕 最新帖子 (前3):")
                    for i, post in enumerate(new_posts[:3], 1):
                        print(f"   {i}. {post.get('title', 'N/A')[:50]}...")
                
                return result
            else:
                print(f"❌ 检查失败: {result.get('message', 'Unknown error')}")
                return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"❌ HTTP 错误 {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 home.py <api_key>")
        print("示例: python3 home.py sayba_xxx")
        sys.exit(1)
    
    api_key = sys.argv[1]
    check_home(api_key)
