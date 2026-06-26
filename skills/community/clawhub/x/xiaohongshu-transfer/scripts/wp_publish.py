#!/usr/bin/env python3
"""小红书笔记发布到 WordPress"""

import os
import sys
import requests
import json

# WordPress 配置
WP_BLOG_ID = "252834205"
WP_TOKEN = os.environ.get("WP_TOKEN", "")

def publish_to_wordpress(title, content, status="publish"):
    """发布文章到 WordPress"""
    
    # 换行符转换为 HTML
    content_html = content.replace('\n', '<br/>')
    
    url = f"https://public-api.wordpress.com/wp/v2/sites/{WP_BLOG_ID}/posts"
    headers = {
        "Authorization": f"Bearer {WP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "title": title,
        "content": content_html,
        "status": status
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200 or response.status_code == 201:
        result = response.json()
        return result.get("ID")
    else:
        print(f"发布失败: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python wp_publish.py <标题> <内容文件>")
        sys.exit(1)
    
    title = sys.argv[1]
    content_file = sys.argv[2]
    
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    post_id = publish_to_wordpress(title, content)
    if post_id:
        print(f"✅ WordPress 文章ID: {post_id}")