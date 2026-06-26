#!/usr/bin/env python3
"""
快速发布文章（直接发布模式）
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

def quick_publish(title, content, categories=None, tags=None):
    """快速发布文章"""
    config = load_env()
    XMLRPC_URL = config.get('BLOG_URL', 'http://yuanblog.tk:9980') + config.get('BLOG_XMLRPC', '/index.php/action/xmlrpc')
    username = config.get('BLOG_USERNAME', 'admin')
    password = config.get('BLOG_PASSWORD', '')
    
    if categories is None:
        categories = ['默认分类']
    
    client = xmlrpc.client.ServerProxy(XMLRPC_URL)
    
    try:
        # 登录
        users = client.blogger.getUsersBlogs('', username, password)
        blog_id = users[0]['blogid']
        
        # 准备数据
        post_data = {
            'title': title,
            'description': content,
            'text': content,
            'mt_text_more': '',
            'mt_allow_comments': 1,
            'mt_allow_pings': 0,
            'categories': categories,
        }
        
        if tags:
            post_data['mt_keywords'] = ', '.join(tags)
        
        # 发布
        post_id = client.metaWeblog.newPost(blog_id, username, password, post_data, True)
        
        print(f"✅ 文章《{title}》已成功发布！")
        print(f"🔗 链接：http://yuanblog.tk:9980/archives/{post_id}.html")
        return True
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

if __name__ == "__main__":
    # 测试发布
    title = "测试：" + str(int(os.urandom(4).hex(), 16))
    content = "这是自动发布的测试内容。"
    
    quick_publish(title, content, ['测试'], ['自动化'])
