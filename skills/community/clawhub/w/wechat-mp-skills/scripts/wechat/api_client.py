# -*- coding: utf-8 -*-

#!/usr/bin/env python3
"""
微信公众号 API 客户端
获取 AccessToken、上传图片、保存到草稿箱
"""

import argparse
import io
import json
import os
import sys
import time
import requests
from pathlib import Path
from typing import Optional

# API 基础地址
API_BASE = "https://api.weixin.qq.com"


class WeChatMPClient:
    """微信公众号 API 客户端"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self._access_token = None
        self._token_expires_at = 0
    
    def get_access_token(self, force_refresh: bool = False) -> dict:
        """
        获取AccessToken
        文档：https://developers.weixin.qq.com/doc/subscription/api/base/api_getaccesstoken.html
        """
        # 如果有缓存的 token 且未过期，直接返回
        if not force_refresh and self._access_token and time.time() < self._token_expires_at:
            return {
                "errcode": 0,
                "errmsg": "ok",
                "access_token": self._access_token,
                "expires_in": int(self._token_expires_at - time.time())
            }
        
        url = f"{API_BASE}/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get("errcode") == 0:
                self._access_token = data["access_token"]
                self._token_expires_at = time.time() + data["expires_in"] - 300  # 提前5分钟过期
            
            return data
        except Exception as e:
            return {"errcode": -1, "errmsg": f"请求失败: {str(e)}"}
    
    def upload_article_image(self, image_path: str = None, image_url: str = None) -> dict:
        """
        上传文章内图片（返回 URL 用于文章内容中）
        文档：https://developers.weixin.qq.com/doc/subscription/api/material/permanent/api_uploadimage.html
        注意：返回的 url 仅可用于公众号文章中
        """
        token_result = self.get_access_token()
        print(f"Token result: {token_result}")
        
        # 检查错误 - 有 errcode 且不为 0
        if token_result.get("errcode") is not None and token_result.get("errcode") != 0:
            return token_result
        
        if not token_result.get("access_token"):
            return token_result
        
        access_token = token_result["access_token"]
        
        # 获取图片内容
        if image_url:
            # 从网络下载
            response = requests.get(image_url, timeout=30)
            if response.status_code != 200:
                return {"errcode": -3, "errmsg": f"下载图片失败: {response.status_code}"}
            image_data = response.content
            filename = "article_image.jpg"
        elif image_path:
            # 读取本地文件
            if not os.path.exists(image_path):
                return {"errcode": -2, "errmsg": f"文件不存在: {image_path}"}
            with open(image_path, "rb") as f:
                image_data = f.read()
            filename = os.path.basename(image_path)
        else:
            return {"errcode": -1, "errmsg": "请提供 image_path 或 image_url"}
        
        # 上传图片（使用 uploadimg 接口，返回 url 用于文章内容）
        url = f"{API_BASE}/cgi-bin/media/uploadimg"
        params = {"access_token": access_token}
        files = {"media": (filename, io.BytesIO(image_data), "image/jpeg")}
        
        response = requests.post(url, params=params, files=files, timeout=30)
        return response.json()
    
    def upload_permanent_image_from_url(self, image_url: str, access_token: str = None) -> dict:
        """
        从网络URL下载并上传为永久图片素材
        """
        try:
            # 使用传入的token或获取新token
            if not access_token:
                token_result = self.get_access_token()
                if token_result.get("errcode") != 0:
                    return token_result
                access_token = token_result["access_token"]
            
            # 下载图片
            print(f"upload_permanent_image_from_url: downloading {image_url}")
            response = requests.get(image_url, timeout=30)
            if response.status_code != 200:
                return {"errcode": -3, "errmsg": f"下载图片失败: {response.status_code}"}
            
            # 上传到永久素材库
            url = f"{API_BASE}/cgi-bin/material/add_material"
            params = {"access_token": access_token, "type": "image"}
            
            files = {"media": ("cover.jpg", io.BytesIO(response.content), "image/jpeg")}
            upload_resp = requests.post(url, params=params, files=files, timeout=30)
            result = upload_resp.json()
            print(f"upload_permanent_image_from_url: result = {result}")
            return result
            
        except Exception as e:
            return {"errcode": -1, "errmsg": f"上传失败: {str(e)}"}
    
    def save_draft(self, title: str, content: str, author: str = None,
                   content_source_url: str = None, digest: str = None,
                   cover_image_path: str = None) -> dict:
        """
        保存文章到草稿箱
        文档：https://developers.weixin.qq.com/doc/subscription/api/draftbox/draftmanage/api_draft_add.html
        
        参数:
            - title: 文章标题
            - content: 文章正文（HTML格式，支持图片）
            - author: 作者
            - content_source_url: 原文链接
            - digest: 摘要
            - cover_image_path: 封面图片本地路径
        """
        token_result = self.get_access_token()
        
        # 检查是否有错误：有errcode且不为0，或者没有access_token
        if token_result.get("errcode") and token_result.get("errcode") != 0:
            return token_result
        
        if not token_result.get("access_token"):
            return token_result
        
        access_token = token_result["access_token"]
        
        url = f"{API_BASE}/cgi-bin/draft/add"
        params = {"access_token": access_token}
        
        # 构建文章内容
        articles = [{
            "title": title,
            "author": author or "",
            "content": content,
            "content_source_url": content_source_url or "",
            "digest": digest or "",
        }]
        
        # 必须有封面图片（公众号API要求）
        # 自动从网络获取默认封面
        if not cover_image_path:
            cover_image_path = "https://picsum.photos/800/600"
        
        # 上传到永久素材库获取 media_id（传入同一个access_token避免重新获取）
        if cover_image_path.startswith("http"):
            cover_result = self.upload_permanent_image_from_url(cover_image_path, access_token)
        else:
            cover_result = self.upload_permanent_image(cover_image_path)
        
        # 检查是否成功（有 media_id 或者 errcode == 0）
        if cover_result.get("media_id") or cover_result.get("errcode") == 0:
            articles[0]["thumb_media_id"] = cover_result.get("media_id")
        
        try:
            # 手动序列化 JSON，确保中文不转义（关键修复）
            draft_json = json.dumps({"articles": articles}, ensure_ascii=False)
            headers = {"Content-Type": "application/json; charset=utf-8"}
            response = requests.post(
                url, 
                params=params, 
                data=draft_json.encode("utf-8"),
                headers=headers,
                timeout=30
            )
            return response.json()
        except Exception as e:
            return {"errcode": -1, "errmsg": f"保存失败: {str(e)}"}


def format_markdown_to_html(title: str, content: str, image_urls: list = None) -> str:
    """
    将 Markdown 内容转换为公众号可用的 HTML 格式
    支持模板编排：标题样式、段落、图片居中等
    """
    import re
    
    # 基础模板（包含 CSS 样式）
    html = f'''<h1 style="font-size: 24px; font-weight: bold; color: #333; text-align: center; margin: 20px 0;">{title}</h1>

<p style="color: #666; font-size: 14px; text-align: center; margin-bottom: 20px;">— · —</p>

<div style="font-size: 16px; line-height: 1.8; color: #333; padding: 0 10px;">
'''
    
    # 处理段落（简单处理：双换行分割）
    paragraphs = content.split("\n\n")
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        # 检测标题
        if para.startswith("## "):
            h2_text = para[3:]
            html += f'<h2 style="font-size: 20px; font-weight: bold; color: #333; margin: 20px 0 10px 0;">{h2_text}</h2>\n'
        elif para.startswith("# "):
            h1_text = para[2:]
            html += f'<h1 style="font-size: 22px; font-weight: bold; color: #333; margin: 20px 0 10px 0;">{h1_text}</h1>\n'
        else:
            # 处理列表
            if para.startswith("- ") or para.startswith("* "):
                lines = para.split("\n")
                html += '<ul style="margin: 10px 0; padding-left: 20px;">\n'
                for line in lines:
                    if line.startswith("- ") or line.startswith("* "):
                        html += f'<li style="margin: 5px 0;">{line[2:]}</li>\n'
                html += '</ul>\n'
            else:
                # 处理行内换行
                para = para.replace("\n", "<br>")
                html += f'<p style="margin: 10px 0; text-indent: 0;">{para}</p>\n'
    
    # 添加图片（居中显示）
    if image_urls:
        for img_url in image_urls:
            html += f'<p style="text-align: center; margin: 15px 0;"><img src="{img_url}" style="max-width: 100%; height: auto; display: block; margin: 0 auto;"/></p>\n'
    
    html += '</div>'
    
    return html


def main():
    parser = argparse.ArgumentParser(description="微信公众号自动发布工具")
    parser.add_argument("--app-id", help="公众号AppID，环境变量 WECHAT_APP_ID")
    parser.add_argument("--app-secret", help="公众号AppSecret，环境变量 WECHAT_APP_SECRET")
    parser.add_argument("--access-token", help="已获取的AccessToken（可选，会自动刷新）")
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # get-token
    subparsers.add_parser("get-token", help="获取AccessToken")
    
    # upload-image
    img_parser = subparsers.add_parser("upload-image", help="上传文章图片")
    img_parser.add_argument("--image-path", required=True, help="图片本地路径")
    
    # save-draft
    draft_parser = subparsers.add_parser("save-draft", help="保存文章到草稿箱")
    draft_parser.add_argument("--title", required=True, help="文章标题")
    draft_parser.add_argument("--content", required=True, help="文章正文（支持 Markdown）")
    draft_parser.add_argument("--content-file", help="从文件读取文章内容")
    draft_parser.add_argument("--author", help="作者")
    draft_parser.add_argument("--cover-image", help="封面图片路径")
    draft_parser.add_argument("--images", nargs="*", help="文章中的图片URL列表")
    draft_parser.add_argument("--markdown", action="store_true", help="内容为 Markdown 格式，转换为 HTML")
    
    args = parser.parse_args()
    
    # 获取配置
    app_id = args.app_id or os.environ.get("WECHAT_APP_ID")
    app_secret = args.app_secret or os.environ.get("WECHAT_APP_SECRET")
    access_token = args.access_token or os.environ.get("WECHAT_ACCESS_TOKEN")
    
    if not app_id or not app_secret:
        print("错误：请通过 --app-id 和 --app-secret 提供凭证，或设置环境变量")
        print("  环境变量: WECHAT_APP_ID, WECHAT_APP_SECRET")
        sys.exit(1)
    
    client = WeChatMPClient(app_id, app_secret)
    
    if args.command == "get-token":
        result = client.get_access_token()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.command == "upload-image":
        result = client.upload_image(args.image_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.command == "save-draft":
        # 获取内容
        if args.content_file:
            with open(args.content_file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = args.content
        
        # 如果是 Markdown，转换为 HTML
        if args.markdown:
            content = format_markdown_to_html(args.title, content, args.images)
        
        result = client.save_draft(
            title=args.title,
            content=content,
            author=args.author,
            cover_image_path=args.cover_image
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()