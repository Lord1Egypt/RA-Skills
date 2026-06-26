#!/usr/bin/env python3
"""
Typecho 博客管理工具集
- 查看最近文章
- 删除指定文章
- 批量操作
"""
import xmlrpc.client
import sys
import os
from datetime import datetime

def load_env():
    """加载 .env 文件（支持多级查找）"""
    config = {}
    
    # 可能的位置
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', '.env'),
        os.path.join(os.path.dirname(__file__), '..', '..', '.env'),
        os.path.expanduser('~/.openclaw/workspace/.env'),
    ]
    
    for env_path in possible_paths:
        env_path = os.path.abspath(env_path)
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        if key not in config:
                            config[key.strip()] = value.strip()
    
    return config

def get_client(config):
    """获取 XML-RPC 客户端"""
    XMLRPC_URL = config.get('BLOG_URL', 'http://yuanblog.tk:9980') + config.get('BLOG_XMLRPC', '/index.php/action/xmlrpc')
    return xmlrpc.client.ServerProxy(XMLRPC_URL), config.get('BLOG_USERNAME', 'admin'), config.get('BLOG_PASSWORD', '')

def list_recent_posts(limit=10):
    """列出最近的文章"""
    config = load_env()
    client, username, password = get_client(config)
    
    try:
        # 获取所有文章
        posts = client.metaWeblog.getRecentPosts('', username, password, limit)
        
        print(f"📋 最近 {len(posts)} 篇文章：\n")
        print(f"{'ID':<8} {'标题':<40} {'状态':<8} {'日期'}")
        print("-" * 80)
        
        for post in posts:
            post_id = post.get('postid', 'N/A')
            title = post.get('title', '无标题')[:40]
            status = '发布' if post.get('status') == 'publish' else '草稿'
            date = post.get('dateCreated', '')
            if date:
                try:
                    if hasattr(date, 'value'):
                        date = date.value.strftime('%Y-%m-%d')
                    else:
                        date = str(date)[:10]
                except:
                    date = str(date)[:10]
            
            print(f"{str(post_id):<8} {title:<40} {status:<8} {date}")
        
        print(f"\n总计：{len(posts)} 篇")
        return posts
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return []

def delete_post(post_id):
    """删除指定文章"""
    config = load_env()
    client, username, password = get_client(config)
    
    try:
        result = client.blogger.deletePost('', username, password, post_id, True)
        print(f"✅ 文章 {post_id} 已删除")
        return True
    except Exception as e:
        print(f"❌ 删除失败：{e}")
        return False

def get_post_stats():
    """获取文章统计信息"""
    config = load_env()
    client, username, password = get_client(config)
    
    try:
        # 获取所有文章
        posts = client.metaWeblog.getRecentPosts('', username, password, 1000)
        
        published = sum(1 for p in posts if p.get('status') == 'publish')
        drafts = len(posts) - published
        
        print("📊 博客统计：")
        print(f"  总文章数：{len(posts)}")
        print(f"  已发布：{published}")
        print(f"  草稿：{drafts}")
        
        return {'total': len(posts), 'published': published, 'drafts': drafts}
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return {}

def print_help():
    """打印帮助信息"""
    print("""
📝 Typecho 博客管理工具

用法:
  python3 manage.py list [数量]      # 列出最近文章
  python3 manage.py delete [ID]      # 删除指定文章
  python3 manage.py stats            # 查看统计
  python3 manage.py help             # 显示帮助

示例:
  python3 manage.py list 20          # 列出最近 20 篇
  python3 manage.py delete 123       # 删除 ID 为 123 的文章
  python3 manage.py stats            # 查看统计信息
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        list_recent_posts(limit)
    
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("❌ 错误：需要指定文章 ID")
            sys.exit(1)
        delete_post(int(sys.argv[2]))
    
    elif command == 'stats':
        get_post_stats()
    
    elif command == 'help' or command == '--help':
        print_help()
    
    else:
        print(f"❌ 未知命令：{command}")
        print_help()
        sys.exit(1)
