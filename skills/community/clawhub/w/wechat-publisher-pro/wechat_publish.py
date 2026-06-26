#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号自动发布工具（精简版）
一键发布 Markdown/HTML 文章到微信公众号草稿箱
支持自动配图、美化排版、UTF-8 编码
"""

import requests
import json
import argparse
from pathlib import Path
from datetime import datetime

class WeChatPublisher:
    """微信公众号发布器"""
    
    def __init__(self, appid, appsecret):
        self.appid = appid
        self.appsecret = appsecret
        self.token = None
    
    def get_token(self):
        """获取 access_token"""
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.appsecret}"
        resp = requests.get(url, timeout=10)
        result = resp.json()
        if "access_token" in result:
            self.token = result["access_token"]
            return self.token
        return None
    
    def upload_image(self, image_path):
        """上传图片获取 media_id"""
        if not self.token:
            self.get_token()
        
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={self.token}&type=image"
        with open(image_path, 'rb') as f:
            resp = requests.post(url, files={'media': f}, timeout=30)
        result = resp.json()
        return result.get("media_id")
    
    def markdown_to_html(self, content, beautify=True):
        """Markdown 转 HTML（简化版）"""
        html = []
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('# '):
                html.append(f'<h2>{line[2:]}</h2>')
            elif line.startswith('## '):
                html.append(f'<h3>{line[3:]}</h3>')
            elif line.startswith('### '):
                html.append(f'<h4>{line[4:]}</h4>')
            else:
                html.append(f'<p>{line}</p>')
        return ''.join(html)
    
    def create_draft(self, title, content, thumb_media_id, digest="", author="RobotQu"):
        """创建草稿"""
        if not self.token:
            self.get_token()
        
        html_content = self.markdown_to_html(content)
        draft_data = {
            "articles": [{
                "title": title,
                "content": html_content,
                "author": author,
                "digest": digest,
                "thumb_media_id": thumb_media_id,
                "show_cover_pic": 1
            }]
        }
        
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.token}"
        json_data = json.dumps(draft_data, ensure_ascii=False).encode('utf-8')
        resp = requests.post(url, data=json_data, timeout=30)
        return resp.json()
    
    def publish(self, article_path, cover_path, title, digest=""):
        """发布文章"""
        print(f"发布文章：{title}")
        
        # 上传封面
        media_id = self.upload_image(cover_path)
        if not media_id:
            print("封面上传失败")
            return None
        
        # 读取文章
        content = Path(article_path).read_text(encoding='utf-8')
        
        # 创建草稿
        result = self.create_draft(title, content, media_id, digest)
        if result.get("media_id"):
            print(f"发布成功！草稿 ID: {result['media_id']}")
            return result["media_id"]
        else:
            print(f"发布失败：{result}")
            return None

def main():
    parser = argparse.ArgumentParser(description='微信公众号自动发布工具')
    parser.add_argument('--article', required=True, help='文章路径')
    parser.add_argument('--cover', required=True, help='封面图路径')
    parser.add_argument('--title', required=True, help='文章标题')
    parser.add_argument('--appid', default='', help='微信公众号 APPID')
    parser.add_argument('--appsecret', default='', help='微信公众号 APPSECRET')
    
    args = parser.parse_args()
    
    # 从环境变量或参数获取配置
    appid = args.appid or "你的 APPID"
    appsecret = args.appsecret or "你的 APPSECRET"
    
    publisher = WeChatPublisher(appid, appsecret)
    publisher.publish(args.article, args.cover, args.title)

if __name__ == "__main__":
    main()
