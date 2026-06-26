#!/usr/bin/env python3
"""
微信公众号文章发布工具
支持：创建草稿、发布文章、管理文章、数据统计
"""

import os
import json
import time
import requests
from datetime import datetime


class WechatPublisher:
    """微信公众号发布工具"""

    def __init__(self, app_id=None, app_secret=None, config_path=None):
        """
        初始化发布工具

        Args:
            app_id: 微信公众号AppID
            app_secret: 微信公众号AppSecret
            config_path: 配置文件路径（可选）
        """
        if config_path and os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.app_id = config.get("wechat", {}).get("app_id")
            self.app_secret = config.get("wechat", {}).get("app_secret")
            self.author = config.get("wechat", {}).get("author", "")
        else:
            self.app_id = app_id or os.environ.get("WECHAT_APP_ID")
            self.app_secret = app_secret or os.environ.get("WECHAT_APP_SECRET")
            self.author = os.environ.get("WECHAT_AUTHOR", "")

        self.access_token = None
        self.token_expires = 0

    def get_access_token(self):
        """获取access_token（自动缓存）"""
        if self.access_token and time.time() < self.token_expires:
            return self.access_token

        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret,
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if "access_token" in data:
            self.access_token = data["access_token"]
            self.token_expires = time.time() + data["expires_in"] - 300
            return self.access_token
        else:
            raise Exception(f"获取token失败: {data}")

    def create_draft(self, title, content, author="", thumb_media_id="", source_url=""):
        """
        创建草稿

        Args:
            title: 文章标题
            content: 文章内容（HTML格式）
            author: 作者名称
            thumb_media_id: 封面图片media_id
            source_url: 原文链接

        Returns:
            media_id: 草稿ID
        """
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"

        article = {
            "title": title,
            "author": author or self.author,
            "content": content,
            "need_open_comment": 1,
        }

        if thumb_media_id:
            article["thumb_media_id"] = thumb_media_id
        if source_url:
            article["content_source_url"] = source_url

        payload = {"articles": [article]}

        response = requests.post(url, json=payload, timeout=30)
        data = response.json()

        if "media_id" in data:
            return data["media_id"]
        else:
            raise Exception(f"创建草稿失败: {data}")

    def publish(self, media_id):
        """
        发布文章

        Args:
            media_id: 草稿ID

        Returns:
            publish_id: 发布ID
        """
        token = self.get_access_token()
        url = (
            f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={token}"
        )

        payload = {"media_id": media_id}

        response = requests.post(url, json=payload, timeout=30)
        data = response.json()

        if "publish_id" in data:
            return data["publish_id"]
        else:
            raise Exception(f"发布失败: {data}")

    def get_publish_status(self, publish_id):
        """获取发布状态"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/get?access_token={token}"

        payload = {"publish_id": publish_id}

        response = requests.post(url, json=payload, timeout=10)
        return response.json()

    def list_drafts(self, offset=0, count=20):
        """获取草稿列表"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={token}"

        payload = {"offset": offset, "count": count, "no_content": 1}

        response = requests.post(url, json=payload, timeout=10)
        return response.json()

    def delete_draft(self, media_id):
        """删除草稿"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={token}"

        payload = {"media_id": media_id}

        response = requests.post(url, json=payload, timeout=10)
        return response.json()

    def list_published(self, offset=0, count=20):
        """获取已发布文章列表"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/batchget?access_token={token}"

        payload = {"offset": offset, "count": count}

        response = requests.post(url, json=payload, timeout=10)
        return response.json()

    def delete_published(self, article_id):
        """删除已发布文章"""
        token = self.get_access_token()
        url = (
            f"https://api.weixin.qq.com/cgi-bin/freepublish/delete?access_token={token}"
        )

        payload = {"article_id": article_id}

        response = requests.post(url, json=payload, timeout=10)
        return response.json()

    def get_article_data(self, article_id, begin_date, end_date):
        """获取文章数据统计"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/datacube/getarticleanalysis?access_token={token}"

        payload = {"begin_date": begin_date, "end_date": end_date, "msgid": article_id}

        response = requests.post(url, json=payload, timeout=10)
        return response.json()

    def get_account_info(self):
        """获取公众号账号信息"""
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/account/getaccountinfo?access_token={token}"

        response = requests.post(url, timeout=10)
        return response.json()


class ContentProcessor:
    """内容处理器：从网页/文件提取内容"""

    @staticmethod
    def from_url(url):
        """从URL提取内容"""
        try:
            from bs4 import BeautifulSoup

            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                },
            )
            soup = BeautifulSoup(response.text, "html.parser")

            # 提取标题
            title = soup.find("h1")
            title = title.text.strip() if title else "Untitled"

            # 提取正文
            paragraphs = []
            for p in soup.find_all("p"):
                text = p.text.strip()
                if len(text) > 20:
                    paragraphs.append(text)

            content = "\n\n".join(paragraphs[:20])

            return {"title": title, "content": content}
        except Exception as e:
            raise Exception(f"URL提取失败: {e}")

    @staticmethod
    def from_markdown(file_path):
        """从Markdown文件提取内容"""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 提取标题
        lines = content.split("\n")
        title = "Untitled"
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break

        return {"title": title, "content": content}

    @staticmethod
    def from_docx(file_path):
        """从Word文件提取内容"""
        try:
            from docx import Document

            doc = Document(file_path)

            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            title = paragraphs[0] if paragraphs else "Untitled"
            content = "\n\n".join(paragraphs)

            return {"title": title, "content": content}
        except ImportError:
            raise Exception("需要安装python-docx: pip install python-docx")

    @staticmethod
    def from_pdf(file_path):
        """从PDF文件提取内容"""
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(file_path)

            text = ""
            for page in doc:
                text += page.get_text()

            doc.close()

            lines = text.split("\n")
            title = lines[0] if lines else "Untitled"

            return {"title": title, "content": text}
        except ImportError:
            raise Exception("需要安装PyMuPDF: pip install pymupdf")


class HtmlRenderer:
    """HTML渲染器：生成精美的公众号文章HTML"""

    @staticmethod
    def render(title, content, style="standard", author="", date=""):
        """渲染HTML"""

        styles = {
            "standard": HtmlRenderer._standard_style,
            "business": HtmlRenderer._business_style,
            "minimal": HtmlRenderer._minimal_style,
        }

        renderer = styles.get(style, styles["standard"])
        return renderer(title, content, author, date)

    @staticmethod
    def _standard_style(title, content, author, date):
        """标准样式"""
        return f"""
        <div style="font-family: 'Microsoft YaHei', sans-serif; max-width: 677px; margin: 0 auto; padding: 20px;">
            <h1 style="font-size: 22px; font-weight: bold; color: #333; margin-bottom: 10px;">{title}</h1>
            <p style="color: #888; font-size: 14px; margin-bottom: 20px;">
                {author + " | " if author else ""}{date}
            </p>
            <div style="font-size: 15px; line-height: 1.8; color: #333;">
                {content}
            </div>
        </div>
        """

    @staticmethod
    def _business_style(title, content, author, date):
        """商务样式"""
        return f"""
        <div style="font-family: 'Microsoft YaHei', sans-serif; max-width: 677px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #1a365d, #3182ce); padding: 30px; text-align: center;">
                <h1 style="color: white; font-size: 24px; margin: 0;">{title}</h1>
                <p style="color: rgba(255,255,255,0.8); font-size: 14px; margin-top: 10px;">
                    {author + " | " if author else ""}{date}
                </p>
            </div>
            <div style="padding: 20px; font-size: 15px; line-height: 1.8; color: #333;">
                {content}
            </div>
        </div>
        """

    @staticmethod
    def _minimal_style(title, content, author, date):
        """极简样式"""
        return f"""
        <div style="font-family: Georgia, serif; max-width: 677px; margin: 0 auto; padding: 20px;">
            <h1 style="font-size: 28px; font-weight: bold; color: #333; text-align: center;">{title}</h1>
            <p style="text-align: center; color: #888; font-size: 14px;">
                {author + " | " if author else ""}{date}
            </p>
            <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
            <div style="font-size: 15px; line-height: 1.8; color: #333;">
                {content}
            </div>
        </div>
        """


if __name__ == "__main__":
    # 测试用例
    print("微信公众号发布工具 - 测试模式")
    print("=" * 50)

    # 检查配置
    app_id = os.environ.get("WECHAT_APP_ID")
    app_secret = os.environ.get("WECHAT_APP_SECRET")

    if app_id and app_secret:
        print(f"✅ 配置已找到: {app_id[:8]}...")

        # 测试获取token
        try:
            publisher = WechatPublisher(app_id, app_secret)
            token = publisher.get_access_token()
            print(f"✅ Token获取成功: {token[:20]}...")
        except Exception as e:
            print(f"❌ Token获取失败: {e}")
    else:
        print("⚠️ 未找到配置，请设置环境变量:")
        print("   export WECHAT_APP_ID='your_app_id'")
        print("   export WECHAT_APP_SECRET='your_app_secret'")
