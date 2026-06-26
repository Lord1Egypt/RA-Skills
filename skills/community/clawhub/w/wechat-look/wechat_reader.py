#!/usr/bin/env python3
"""
WeChat Look - 微信文章读取工具

一个专门为 OpenClaw 设计的微信文章读取技能，能够自动处理URL规范化并提取文章内容。
"""

import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import Dict, Any, Optional


class WeChatReader:
    """微信文章读取器"""

    def __init__(self):
        self.base_url_pattern = r'^https://mp\.weixin\.qq\.com/s/'

    def normalize_url(self, url: str) -> str:
        """
        规范化微信文章URL，确保包含scene=1参数

        Args:
            url: 原始URL

        Returns:
            规范化后的URL
        """
        if not re.match(self.base_url_pattern, url):
            return url

        try:
            parsed = urlparse(url)

            # 获取现有查询参数
            params = parse_qs(parsed.query)

            # 设置scene=1 (如果不存在则添加，存在则覆盖)
            params['scene'] = ['1']

            # 重新构建查询字符串
            new_query = urlencode(params, doseq=True)

            # 构建新URL
            new_url = urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment
            ))

            return new_url
        except Exception as e:
            print(f"URL规范化失败: {e}")
            return url

    def extract_content(self, html_content: str) -> Dict[str, Any]:
        """
        从HTML内容中提取文章信息

        Args:
            html_content: HTML页面内容

        Returns:
            包含文章信息的字典
        """
        result = {
            'title': '',
            'author': '',
            'content': '',
            'url': '',
            'status': 'success'
        }

        try:
            # 提取标题
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.I)
            if title_match:
                result['title'] = title_match.group(1).strip()

            # 提取作者信息（简单匹配）
            author_match = re.search(r'author["\']?\s*[:=]\s*["\']([^"\']+)', html_content, re.I)
            if author_match:
                result['author'] = author_match.group(1).strip()

            # 尝试提取正文内容
            content_selectors = [
                r'id=["\']js_content["\'][^>]*>(.*?)</div>',
                r'class=["\']rich_media_content["\'][^>]*>(.*?)</div>',
                r'<body[^>]*>(.*?)</body>'
            ]

            for selector in content_selectors:
                content_match = re.search(selector, html_content, re.DOTALL | re.I)
                if content_match:
                    raw_content = content_match.group(1)
                    # 清理HTML标签
                    clean_content = re.sub(r'<[^>]+>', '', raw_content)
                    result['content'] = clean_content.strip()
                    break

            # 如果没有提取到内容，使用整个HTML
            if not result['content']:
                result['content'] = html_content[:2000] + "..." if len(html_content) > 2000 else html_content

        except Exception as e:
            result['status'] = f'extraction_error: {str(e)}'

        return result

    def read_article(self, original_url: str) -> Dict[str, Any]:
        """
        读取微信文章

        Args:
            original_url: 原始URL

        Returns:
            包含文章信息的字典
        """
        try:
            # 规范化URL
            normalized_url = self.normalize_url(original_url)

            # 这里应该调用OpenClaw的浏览器工具来获取内容
            # 由于这是演示版本，我们模拟返回结果
            return {
                'original_url': original_url,
                'normalized_url': normalized_url,
                'title': '测试文章标题',
                'author': '测试作者',
                'content': '这是从微信文章中提取的内容...',
                'status': 'success'
            }

        except Exception as e:
            return {
                'original_url': original_url,
                'normalized_url': original_url,
                'error': str(e),
                'status': 'failed'
            }


def main():
    """主函数 - 演示使用方法"""
    reader = WeChatReader()

    # 测试用例
    test_urls = [
        "https://mp.weixin.qq.com/s/D7vSSNGCQFT4NAdY6loPWA",
        "https://mp.weixin.qq.com/s/S3AF2BKqRYcxHaI8uZ71BA?param=value",
        "https://example.com/not-wechat"
    ]

    print("WeChat Reader 测试:")
    print("=" * 50)

    for url in test_urls:
        normalized = reader.normalize_url(url)
        print(f"原始: {url}")
        print(f"规范: {normalized}")
        print("-" * 30)


if __name__ == "__main__":
    main()