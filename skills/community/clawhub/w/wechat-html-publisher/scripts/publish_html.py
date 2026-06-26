#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号HTML文章发布工具
直接上传HTML富文本到草稿箱
"""

import os
import sys
import argparse
import requests
import re
from pathlib import Path
from urllib.parse import urlparse

class WeChatHTMLPublisher:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.base_url = "https://api.weixin.qq.com/cgi-bin"
    
    def get_access_token(self):
        """获取access_token"""
        url = f"{self.base_url}/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }
        
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if "access_token" in data:
                self.access_token = data["access_token"]
                print("[OK] 获取access_token成功")
                return True
            else:
                print(f"[ERROR] 获取access_token失败: {data.get('errmsg', '未知错误')}")
                return False
        except Exception as e:
            print(f"[ERROR] 请求失败: {e}")
            return False
    
    def upload_image(self, image_path):
        """上传图片到微信图床,返回(media_id, url)"""
        if not self.access_token:
            print("[ERROR] 请先获取access_token")
            return None, None
        
        # 判断是本地文件还是网络URL
        if image_path.startswith(('http://', 'https://')):
            # 网络图片,先下载
            try:
                resp = requests.get(image_path, timeout=10)
                resp.raise_for_status()
                image_data = resp.content
                filename = os.path.basename(urlparse(image_path).path) or "image.jpg"
            except Exception as e:
                print(f"[ERROR] 下载图片失败 {image_path}: {e}")
                return None, None
        else:
            # 本地文件
            image_file = Path(image_path)
            if not image_file.exists():
                print(f"[ERROR] 图片不存在: {image_path}")
                return None, None
            
            with open(image_file, 'rb') as f:
                image_data = f.read()
            filename = image_file.name
        
        # 上传到微信
        url = f"{self.base_url}/material/add_material"
        params = {"access_token": self.access_token, "type": "image"}
        files = {"media": (filename, image_data, "image/jpeg")}
        
        try:
            resp = requests.post(url, params=params, files=files, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
            if "url" in data and "media_id" in data:
                print(f"[OK] 图片上传成功: {filename}")
                return data["media_id"], data["url"]
            else:
                print(f"[ERROR] 图片上传失败: {data.get('errmsg', '未知错误')}")
                return None, None
        except Exception as e:
            print(f"[ERROR] 上传失败: {e}")
            return None, None
    
    def process_html_images(self, html_content, html_dir):
        """处理HTML中的图片,上传并替换URL"""
        # 匹配所有img标签的src属性
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        
        def replace_image(match):
            src = match.group(1)
            
            # 跳过已经是微信图床的URL
            if 'mmbiz.qpic.cn' in src or 'wx.qlogo.cn' in src:
                return match.group(0)
            
            # 处理相对路径
            if not src.startswith(('http://', 'https://', '/')):
                src = os.path.join(html_dir, src)
            
            # 上传图片
            print(f"[UPLOAD] 上传图片: {src}")
            media_id, new_url = self.upload_image(src)
            
            if new_url:
                return match.group(0).replace(match.group(1), new_url)
            else:
                print(f"[WARN] 图片上传失败,保持原URL: {src}")
                return match.group(0)
        
        return re.sub(img_pattern, replace_image, html_content)
    
    def publish_draft(self, title, content, thumb_media_id, author="", digest="", source_url=""):
        """发布草稿到微信公众号"""
        if not self.access_token:
            print("[ERROR] 请先获取access_token")
            return None
        
        url = f"{self.base_url}/draft/add"
        params = {"access_token": self.access_token}
        
        data = {
            "articles": [{
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "content_source_url": source_url,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }]
        }
        
        try:
            # 使用json.dumps确保中文不被转义
            import json
            json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            
            resp = requests.post(url, params=params, data=json_data, headers=headers, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            
            if "media_id" in result:
                print("[SUCCESS] 发布成功!")
                print(f"[INFO] Media ID: {result['media_id']}")
                return result['media_id']
            else:
                print(f"[ERROR] 发布失败: {result.get('errmsg', '未知错误')}")
                return None
        except Exception as e:
            print(f"[ERROR] 请求失败: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='发布HTML文章到微信公众号草稿箱')
    parser.add_argument('--file', required=True, help='HTML文件路径')
    parser.add_argument('--title', required=True, help='文章标题')
    parser.add_argument('--cover', required=True, help='封面图路径')
    parser.add_argument('--author', default='', help='作者名称')
    parser.add_argument('--digest', default='', help='文章摘要')
    parser.add_argument('--source-url', default='', help='原文链接')
    
    args = parser.parse_args()
    
    # 获取环境变量
    app_id = os.environ.get('WECHAT_APP_ID')
    app_secret = os.environ.get('WECHAT_APP_SECRET')
    
    if not app_id or not app_secret:
        print("[ERROR] 请设置环境变量: WECHAT_APP_ID 和 WECHAT_APP_SECRET")
        sys.exit(1)
    
    # 读取HTML文件
    html_file = Path(args.file)
    if not html_file.exists():
        print(f"[ERROR] HTML文件不存在: {args.file}")
        sys.exit(1)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"[FILE] 读取HTML文件: {args.file}")
    
    # 初始化发布器
    publisher = WeChatHTMLPublisher(app_id, app_secret)
    
    # 获取access_token
    if not publisher.get_access_token():
        sys.exit(1)
    
    # 上传封面图
    print(f"[UPLOAD] 上传封面图: {args.cover}")
    thumb_media_id, cover_url = publisher.upload_image(args.cover)
    if not thumb_media_id:
        print("[ERROR] 封面图上传失败")
        sys.exit(1)
    
    # 处理HTML中的图片
    print("[PROCESS] 处理HTML中的图片...")
    html_dir = html_file.parent
    processed_html = publisher.process_html_images(html_content, str(html_dir))
    
    # 发布草稿
    print("[UPLOAD] 发布到草稿箱...")
    media_id = publisher.publish_draft(
        title=args.title,
        content=processed_html,
        thumb_media_id=thumb_media_id,
        author=args.author,
        digest=args.digest,
        source_url=args.source_url
    )
    
    if media_id:
        print("\n[SUCCESS] 发布完成!")
        print("请到微信公众号后台草稿箱查看")
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
