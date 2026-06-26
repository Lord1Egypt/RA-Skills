#!/usr/bin/env python3
"""
Typecho 博客发布工具 - 原生 Markdown 模式
直接发送 Markdown 内容，让 Typecho 自己处理
"""
import xmlrpc.client
import sys
import os
from datetime import datetime

# 导入主发布脚本的函数
sys.path.insert(0, os.path.dirname(__file__))
from publish_post import load_env, parse_markdown_header, log_message

def publish_raw_markdown(title, content, categories=None, tags=None, publish_now=True, config=None):
    """
    直接发送 Markdown 内容（不转换 HTML）
    适用于支持原生 Markdown 的 Typecho
    """
    if config is None:
        config = load_env()
    
    if categories is None:
        categories = ["技术"]
    
    XMLRPC_URL = config.get('BLOG_URL', 'http://yuanblog.tk:9980') + config.get('BLOG_XMLRPC', '/index.php/action/xmlrpc')
    USERNAME = config.get('BLOG_USERNAME', 'admin')
    PASSWORD = config.get('BLOG_PASSWORD', '')
    
    if not PASSWORD:
        log_message("❌ 错误：未找到密码！")
        return False
    
    log_message(f"📝 [原生 Markdown] 准备发布：《{title}》")
    log_message(f"   分类：{', '.join(categories)}")
    if tags:
        log_message(f"   标签：{', '.join(tags)}")
    log_message(f"   模式：{'立即发布' if publish_now else '草稿'}")
    
    client = xmlrpc.client.ServerProxy(XMLRPC_URL)
    
    try:
        users = client.blogger.getUsersBlogs('', USERNAME, PASSWORD)
        if not users:
            log_message("❌ 登录失败")
            return False
        
        blog_id = users[0]['blogid']
        log_message(f"✅ 登录成功！Blog ID: {blog_id}")
        
        # 关键：直接发送原始 Markdown，不转换
        post_data = {
            'title': title,
            'description': content,  # 直接发送 Markdown
            'text': content,  # 同时设置 text 字段
            'mt_text_more': '',
            'mt_allow_comments': 1,
            'mt_allow_pings': 0,
            'categories': categories,
        }
        
        if tags:
            post_data['mt_keywords'] = ', '.join(tags)
        
        log_message(f"📡 发布到：{XMLRPC_URL}")
        post_id = client.metaWeblog.newPost(blog_id, USERNAME, PASSWORD, post_data, publish_now)
        
        blog_url = XMLRPC_URL.replace('/index.php/action/xmlrpc', '')
        log_message(f"✅ 成功！文章 ID: {post_id}")
        log_message(f"🔗 链接：{blog_url}/archives/{post_id}.html")
        return True
        
    except Exception as e:
        log_message(f"❌ 失败：{e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 publish_raw.py --file article.md [--draft]")
        sys.exit(1)
    
    # 解析参数
    filepath = None
    publish_now = True
    
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == '--file' and i < len(sys.argv) - 1:
            filepath = sys.argv[i + 1]
        elif arg == '--draft':
            publish_now = False
    
    if not filepath:
        print("❌ 需要指定文件路径")
        sys.exit(1)
    
    # 读取文件
    if not os.path.exists(filepath):
        log_message(f"❌ 文件不存在：{filepath}")
        sys.exit(1)
    
    content = open(filepath, 'r', encoding='utf-8').read()
    title, body, categories, tags = parse_markdown_header(content)
    
    if not title:
        title = os.path.splitext(os.path.basename(filepath))[0]
        body = content
    
    config = load_env()
    success = publish_raw_markdown(title, body, categories, tags, publish_now, config)
    sys.exit(0 if success else 1)
