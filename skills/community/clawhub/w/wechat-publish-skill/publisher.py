#!/usr/bin/env python3
"""
微信公众号文章发布脚本
支持批量发布 Markdown 文章到公众号草稿箱
"""

import os
import json
import requests
import markdown2
from typing import Dict, List, Optional
from pathlib import Path

# ==================== 配置区域 ====================

# 微信公众号配置（从环境变量读取）
APP_ID = os.getenv("WECHAT_APP_ID", "")
APP_SECRET = os.getenv("WECHAT_APP_SECRET", "")
ACCOUNT_NAME = os.getenv("WECHAT_ACCOUNT_NAME", "公众号名称")

# API 配置
MAX_DIGEST_LENGTH = 120  # 摘要最大长度
API_BASE_URL = "https://api.weixin.qq.com"

# ==================== 工具函数 ====================

def generate_digest(markdown_content: str, max_length: int = 120) -> str:
    """
    从 Markdown 内容生成摘要
    
    Args:
        markdown_content: Markdown 文本
        max_length: 最大长度
        
    Returns:
        摘要文本
    """
    import re
    
    lines = markdown_content.split('\n')
    content_lines = []
    
    for line in lines:
        line = line.strip()
        # 跳过标题、代码块等
        if line.startswith('#') or line.startswith('```') or line.startswith('---'):
            continue
        if line and not re.match(r'^[-*|+]+$', line):
            content_lines.append(line)
    
    content = ' '.join(content_lines)
    # 移除链接
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
    # 移除格式符号
    content = re.sub(r'[*_`#>-]', '', content)
    
    # 按句子截取
    sentences = re.split(r'[。！？\n]', content)
    digest = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 10:
            if len(digest) + len(sentence) + 1 <= max_length:
                digest += sentence + "。"
            else:
                break
    
    return digest or content[:max_length].rstrip()


def markdown_to_wechat_html(markdown_content: str) -> str:
    """
    将 Markdown 转换为微信公众号支持的 HTML 格式
    
    Args:
        markdown_content: Markdown 文本
        
    Returns:
        格式化的 HTML
    """
    # 转换基础 Markdown
    extras = ['fenced-code-blocks', 'tables', 'strike', 'task_list']
    html = markdown2.markdown(markdown_content, extras=extras)
    
    # 微信公众号样式适配
    style_map = {
        '<h1>': '<h1 style="font-size: 22px; font-weight: bold; color: #000; margin: 30px 0 20px 0; text-align: center; line-height: 1.4;">',
        '<h2>': '<h2 style="font-size: 18px; font-weight: bold; color: #333; margin: 25px 0 15px 0; border-left: 4px solid #3b82f6; padding-left: 10px; line-height: 1.4;">',
        '<h3>': '<h3 style="font-size: 16px; font-weight: bold; color: #333; margin: 20px 0 10px 0; line-height: 1.4;">',
        '<p>': '<p style="margin: 15px 0; text-align: justify; line-height: 1.8; color: #333; font-size: 16px;">',
        '<pre>': '<pre style="background-color: #f8f8f8; padding: 15px; border-radius: 5px; overflow-x: auto; margin: 20px 0; border: 1px solid #e1e1e8; font-size: 14px;">',
        '<code>': '<code style="background-color: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: Courier New, monospace; font-size: 14px; color: #c7254e;">',
        '<blockquote>': '<blockquote style="border-left: 4px solid #3b82f6; padding: 10px 20px; margin: 20px 0; color: #666; background-color: #f0f7ff;">',
        '<ul>': '<ul style="padding-left: 25px; margin: 15px 0; color: #333;">',
        '<ol>': '<ol style="padding-left: 25px; margin: 15px 0; color: #333;">',
        '<li>': '<li style="margin: 8px 0; line-height: 1.6;">',
        '<hr>': '<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">',
        '<strong>': '<strong style="font-weight: bold; color: #000;">',
        '<table>': '<table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; border: 1px solid #ddd;">',
        '<th>': '<th style="background-color: #f5f5f5; font-weight: bold; padding: 10px; text-align: center; border: 1px solid #ddd;">',
        '<td>': '<td style="padding: 10px; text-align: left; border: 1px solid #ddd;">',
    }
    
    for old, new in style_map.items():
        html = html.replace(old, new)
    
    return html


# ==================== API 客户端 ====================

class WeChatPublisher:
    """微信公众号发布客户端"""
    
    def __init__(self, app_id: str, app_secret: str, account_name: str = ""):
        self.app_id = app_id
        self.app_secret = app_secret
        self.account_name = account_name
        self.access_token = None
    
    def get_access_token(self) -> str:
        """获取 access_token"""
        url = f"{API_BASE_URL}/cgi-bin/token"
        params = {
            'grant_type': 'client_credential',
            'appid': self.app_id,
            'secret': self.app_secret
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'access_token' in data:
            self.access_token = data['access_token']
            return self.access_token
        else:
            raise Exception(f"获取 access_token 失败: {data}")
    
    def upload_cover(self, image_path: str) -> str:
        """
        上传封面图
        
        Args:
            image_path: 图片路径
            
        Returns:
            media_id
        """
        if not self.access_token:
            self.get_access_token()
        
        url = f"{API_BASE_URL}/cgi-bin/material/add_material"
        params = {
            'access_token': self.access_token,
            'type': 'thumb'
        }
        
        with open(image_path, 'rb') as f:
            files = {
                'media': (os.path.basename(image_path), f, 'image/png')
            }
            data = {
                'description': json.dumps({
                    'title': 'Cover',
                    'introduction': ''
                }, ensure_ascii=False)
            }
            response = requests.post(url, params=params, files=files, data=data)
        
        result = response.json()
        if 'media_id' in result:
            return result['media_id']
        else:
            raise Exception(f"上传封面失败: {result}")
    
    def create_draft(self, title: str, content: str, thumb_media_id: str, 
                     digest: str = "", author: str = "") -> str:
        """
        创建草稿
        
        Args:
            title: 文章标题
            content: 文章内容（HTML）
            thumb_media_id: 封面图 media_id
            digest: 摘要
            author: 作者
            
        Returns:
            草稿 media_id
        """
        if not self.access_token:
            self.get_access_token()
        
        url = f"{API_BASE_URL}/cgi-bin/draft/add"
        params = {'access_token': self.access_token}
        
        article = {
            "title": title,
            "author": author or self.account_name,
            "digest": digest,
            "content": content,
            "content_source_url": "",
            "thumb_media_id": thumb_media_id,
            "need_open_comment": 1,
            "only_fans_can_comment": 0,
            "show_cover_pic": 1
        }
        
        payload = {"articles": [article]}
        
        response = requests.post(
            url, 
            params=params,
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json; charset=utf-8'}
        )
        
        result = response.json()
        if 'media_id' in result:
            return result['media_id']
        else:
            raise Exception(f"创建草稿失败: {result}")
    
    def publish_article(self, article_path: str, cover_path: str = None) -> str:
        """
        发布单篇文章
        
        Args:
            article_path: Markdown 文章路径
            cover_path: 封面图路径（可选）
            
        Returns:
            草稿 ID
        """
        # 读取文章
        with open(article_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # 提取标题（第一个 # 标题）
        title = ""
        for line in markdown_content.split('\n'):
            line = line.strip()
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        if not title:
            title = Path(article_path).stem
        
        # 转换内容
        html_content = markdown_to_wechat_html(markdown_content)
        digest = generate_digest(markdown_content, MAX_DIGEST_LENGTH)
        
        # 上传封面
        if cover_path and os.path.exists(cover_path):
            thumb_media_id = self.upload_cover(cover_path)
        else:
            raise Exception("需要提供封面图")
        
        # 创建草稿
        draft_id = self.create_draft(
            title=title,
            content=html_content,
            thumb_media_id=thumb_media_id,
            digest=digest
        )
        
        return draft_id


def batch_publish(tutorial_dir: str, publisher: WeChatPublisher, 
                  episodes: List[tuple]) -> Dict[int, str]:
    """
    批量发布文章
    
    Args:
        tutorial_dir: 教程根目录
        publisher: 发布客户端
        episodes: [(期数, 目录名, 标题简称), ...]
        
    Returns:
        {期数: 草稿ID}
    """
    results = {}
    
    for ep_num, dir_name, title_short in episodes:
        print(f"\n处理第 {ep_num} 期...")
        
        article_path = os.path.join(tutorial_dir, dir_name, "README.md")
        cover_path = os.path.join(tutorial_dir, dir_name, "cover.png")
        
        if not os.path.exists(article_path):
            print(f"  ⚠️ 文章不存在: {article_path}")
            continue
        
        try:
            draft_id = publisher.publish_article(article_path, cover_path)
            results[ep_num] = draft_id
            print(f"  ✅ 发布成功: {draft_id}")
        except Exception as e:
            print(f"  ❌ 发布失败: {e}")
    
    return results


# ==================== 主程序 ====================

if __name__ == "__main__":
    # 检查配置
    if not APP_ID or not APP_SECRET:
        print("❌ 请先配置环境变量 WECHAT_APP_ID 和 WECHAT_APP_SECRET")
        print("\n使用方法:")
        print("  export WECHAT_APP_ID='your_app_id'")
        print("  export WECHAT_APP_SECRET='your_app_secret'")
        print("  python publisher.py")
        exit(1)
    
    # 示例：发布单篇文章
    # publisher = WeChatPublisher(APP_ID, APP_SECRET, ACCOUNT_NAME)
    # draft_id = publisher.publish_article("path/to/README.md", "path/to/cover.png")
    # print(f"草稿 ID: {draft_id}")
    
    # 示例：批量发布
    # publisher = WeChatPublisher(APP_ID, APP_SECRET, ACCOUNT_NAME)
    # episodes = [
    #     (1, "01-intro", "入门介绍"),
    #     (2, "02-advanced", "进阶内容"),
    # ]
    # results = batch_publish("/path/to/tutorial", publisher, episodes)
    
    print("微信公众号文章发布脚本")
    print("请配置环境变量后使用")
