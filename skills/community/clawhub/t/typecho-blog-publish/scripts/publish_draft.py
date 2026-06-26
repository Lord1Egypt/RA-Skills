#!/usr/bin/env python3
"""
快速发布草稿文章
"""
import xmlrpc.client
import sys
import os

def load_env():
    config = {}
    env_paths = [
        os.path.expanduser('~/.openclaw/workspace/.env'),
        os.path.join(os.path.dirname(__file__), '..', '.env'),
    ]
    for path in env_paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        k, v = line.split('=', 1)
                        config[k.strip()] = v.strip()
    return config

def publish_draft(post_id):
    """
    将草稿改为发布
    
    方案：先获取文章内容，然后删除草稿，重新发布
    """
    config = load_env()
    XMLRPC_URL = config.get('BLOG_URL', 'http://yuanblog.tk:9980') + config.get('BLOG_XMLRPC', '/index.php/action/xmlrpc')
    username = config.get('BLOG_USERNAME', 'admin')
    password = config.get('BLOG_PASSWORD', '')
    
    client = xmlrpc.client.ServerProxy(XMLRPC_URL)
    
    try:
        # 获取文章
        post = client.metaWeblog.getPost('', username, password, post_id)
        
        if not post:
            print(f"❌ 未找到文章 ID: {post_id}")
            return False
        
        title = post.get('title', '')
        content = post.get('description', '')
        categories = post.get('categories', [])
        
        print(f"📝 准备发布文章：《{title}》")
        print(f"   分类：{', '.join(categories) if categories else '默认'}")
        
        # 获取 blog ID
        users = client.blogger.getUsersBlogs('', username, password)
        blog_id = users[0]['blogid']
        
        # 准备发布数据
        post_data = {
            'title': title,
            'description': content,
            'text': content,
            'mt_text_more': '',
            'mt_allow_comments': 1,
            'mt_allow_pings': 0,
            'categories': categories if categories else [],
        }
        
        # 直接发布（publish_now=True）
        print(f"📡 正在发布...")
        new_post_id = client.metaWeblog.newPost(blog_id, username, password, post_data, True)
        
        # 删除原草稿
        try:
            client.blogger.deletePost('', username, password, post_id, True)
            print(f"🗑️  已删除原草稿 (ID: {post_id})")
        except Exception as e:
            print(f"⚠️  删除原草稿失败：{e}")
        
        print(f"✅ 文章《{title}》已成功发布！")
        blog_url = XMLRPC_URL.replace('/index.php/action/xmlrpc', '')
        print(f"🔗 文章链接：{blog_url}/archives/{new_post_id}.html")
        return True
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 publish_draft.py <文章 ID>")
        print("示例：python3 publish_draft.py 916")
        sys.exit(1)
    
    try:
        post_id = int(sys.argv[1])
        success = publish_draft(post_id)
        sys.exit(0 if success else 1)
    except ValueError:
        print("❌ 文章 ID 必须是数字")
        sys.exit(1)
