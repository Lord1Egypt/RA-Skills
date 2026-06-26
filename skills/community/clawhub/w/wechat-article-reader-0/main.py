#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章读取 Skill
支持提取文章关键信息并生成摘要
"""

import json
import re
import sys
from typing import Dict, Any, Optional
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
except ImportError as e:
    print(json.dumps({
        "status": "error",
        "message": f"缺少必要依赖: {str(e)}。请运行: pip install -r requirements.txt"
    }))
    sys.exit(1)


class WeChatArticleReader:
    """微信公众号文章读取器"""

    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.ua = UserAgent()
        self.session = requests.Session()

    def is_wechat_url(self, url: str) -> bool:
        """检查是否为微信公众号链接"""
        parsed = urlparse(url)
        return 'mp.weixin.qq.com' in parsed.netloc

    def fetch_article(self, url: str) -> Dict[str, Any]:
        """获取文章内容"""
        if not self.is_wechat_url(url):
            return {
                "status": "error",
                "message": "不是有效的微信公众号文章链接"
            }

        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    allow_redirects=True
                )

                if response.status_code == 200:
                    return self.parse_article(response.text, url)
                elif response.status_code == 404:
                    return {
                        "status": "error",
                        "message": "文章不存在或已被删除"
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"请求失败，状态码: {response.status_code}"
                    }

            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    continue
                return {
                    "status": "error",
                    "message": "请求超时，请检查网络连接"
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"获取文章时出错: {str(e)}"
                }

    def parse_article(self, html: str, url: str) -> Dict[str, Any]:
        """解析文章内容"""
        soup = BeautifulSoup(html, 'lxml')

        # 提取文章标题
        title = self.extract_title(soup)

        # 提取公众号名称
        account = self.extract_account(soup)

        # 提取作者
        author = self.extract_author(soup)

        # 提取发布时间
        publish_time = self.extract_publish_time(soup)

        # 提取正文内容
        content = self.extract_content(soup)

        # 生成摘要（提取前几段）
        summary = self.generate_summary(content)

        if not title and not content:
            return {
                "status": "error",
                "message": "无法解析文章内容，可能需要关注公众号才能阅读"
            }

        return {
            "status": "success",
            "data": {
                "title": title,
                "author": author,
                "account": account,
                "publish_time": publish_time,
                "content": content,
                "summary": summary,
                "url": url
            }
        }

    def extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """提取文章标题"""
        # 尝试多种方式获取标题
        selectors = [
            'meta[property="og:title"]',
            'h1.rich_media_title',
            'h1',
            '.rich_media_title',
            '#activity-name'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    title = element.get('content', '').strip()
                else:
                    title = element.get_text().strip()
                if title:
                    return title
        return None

    def extract_account(self, soup: BeautifulSoup) -> Optional[str]:
        """提取公众号名称"""
        selectors = [
            'meta[property="og:site_name"]',
            '.rich_media_meta_link',
            '#js_profile_qrcode_img'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    account = element.get('content', '').strip()
                else:
                    account = element.get_text().strip()
                if account:
                    return account
        return "未知公众号"

    def extract_author(self, soup: BeautifulSoup) -> Optional[str]:
        """提取作者信息"""
        selectors = [
            '.rich_media_meta_text',
            '#meta_content',
            '.author'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                author = element.get_text().strip()
                if author and len(author) < 50:  # 避免误取长文本
                    return author
        return None

    def extract_publish_time(self, soup: BeautifulSoup) -> Optional[str]:
        """提取发布时间"""
        selectors = [
            'meta[property="article:published_time"]',
            '#publish_time',
            '.publish_time'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    time = element.get('content', '').strip()
                else:
                    time = element.get_text().strip()
                if time:
                    return time
        return None

    def extract_content(self, soup: BeautifulSoup) -> str:
        """提取正文内容"""
        # 微信公众号正文通常在 #js_content 中
        content_div = soup.select_one('#js_content')
        if not content_div:
            content_div = soup.select_one('.rich_media_content')

        if content_div:
            # 移除脚本和样式标签
            for script in content_div(['script', 'style']):
                script.decompose()

            # 获取文本内容
            content = content_div.get_text(separator='\n', strip=True)
            # 清理多余的空行
            content = re.sub(r'\n{3,}', '\n\n', content)
            return content.strip()

        return ""

    def generate_summary(self, content: str, max_length: int = 500) -> str:
        """生成文章摘要"""
        if not content:
            return ""

        # 按段落分割
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]

        if not paragraphs:
            return content[:max_length]

        # 取前几段作为摘要
        summary = ""
        for para in paragraphs[:5]:
            if len(summary) + len(para) > max_length:
                break
            summary += para + "\n\n"

        # 如果摘要太短，取第一段的前max_length个字符
        if len(summary.strip()) < 100 and paragraphs:
            summary = paragraphs[0][:max_length] + "..."

        return summary.strip()

    def format_output(self, result: Dict[str, Any]) -> str:
        """格式化输出结果"""
        if result["status"] == "error":
            return f"❌ {result['message']}"

        data = result["data"]
        output = []

        output.append("📄 " + (data.get("title") or "未知标题"))
        output.append("")

        if data.get("author"):
            output.append(f"👤 作者：{data['author']}")
        if data.get("account"):
            output.append(f"🏢 公众号：{data['account']}")
        if data.get("publish_time"):
            output.append(f"📅 发布时间：{data['publish_time']}")

        output.append("")
        output.append("📝 内容摘要：")
        output.append("")
        output.append(data.get("summary") or "无法生成摘要")

        if data.get("content"):
            content_lines = data["content"].split('\n')
            if len(content_lines) > 10:
                output.append("")
                output.append("...")
                output.append("(完整内容已省略，文章较长)")

        return "\n".join(output)


def handle(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    OpenClaw Skill 主入口函数
    :param request: 包含用户消息和上下文的请求
    :return: 技能执行结果
    """
    # 获取用户消息
    message = request.get("message", "")
    url = extract_url(message)

    if not url:
        return {
            "status": "error",
            "message": "未找到有效的微信公众号文章链接。请发送以 mp.weixin.qq.com 开头的链接。"
        }

    # 创建读取器实例
    config = request.get("config", {})
    timeout = config.get("timeout", 30)
    max_retries = config.get("max_retries", 3)

    reader = WeChatArticleReader(timeout=timeout, max_retries=max_retries)

    # 获取文章
    result = reader.fetch_article(url)

    # 格式化输出
    if result["status"] == "success":
        formatted_output = reader.format_output(result)
        return {
            "status": "success",
            "message": formatted_output,
            "data": result["data"]
        }
    else:
        return result


def extract_url(text: str) -> Optional[str]:
    """从文本中提取微信公众号链接"""
    # 匹配微信公众号链接
    pattern = r'https?://mp\.weixin\.qq\.com/s[^\s<>"]+'
    match = re.search(pattern, text)

    if match:
        return match.group(0)
    return None


if __name__ == "__main__":
    # 测试代码
    test_url = "https://mp.weixin.qq.com/s/test"

    test_request = {
        "message": f"请帮我读取这篇文章：{test_url}",
        "config": {
            "timeout": 30,
            "max_retries": 3
        }
    }

    result = handle(test_request)
    print(json.dumps(result, ensure_ascii=False, indent=2))
