#!/usr/bin/env python3
"""
WeChat Look OCR - 支持OCR的微信文章读取工具

升级版，能够提取图片内容并进行文字识别
"""

import re
import base64
import subprocess, json
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import Dict, Any, Optional, List
import requests


class WeChatLookOCR:
    """支持OCR的微信文章读取器"""

    def __init__(self):
        self.base_url_pattern = r'^https://mp\.weixin\.qq\.com/s/'

    def normalize_url(self, url: str) -> str:
        """规范化微信文章URL"""
        if not re.match(self.base_url_pattern, url):
            return url

        try:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            params['scene'] = ['1']
            new_query = urlencode(params, doseq=True)

            new_url = urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, new_query, parsed.fragment
            ))
            return new_url
        except Exception as e:
            print(f"URL规范化失败: {e}")
            return url

    def extract_images_from_html(self, html_content: str) -> List[str]:
        """从HTML中提取所有图片URL"""
        image_urls = []

        # 提取img标签的src属性
        img_pattern = r'<img[^>]*src=["\']([^"\']+)["\']'
        matches = re.findall(img_pattern, html_content, re.I)

        for url in matches:
            if url.startswith('http'):
                image_urls.append(url)
            elif url.startswith('//'):
                image_urls.append('https:' + url)
            elif url.startswith('/'):
                # 相对路径转换为绝对路径
                from urllib.parse import urljoin
                # 这里需要原始URL来解析相对路径
                pass

        return image_urls

    def ocr_image_via_node(self, image_url: str) -> str:
        """使用 Node.js OCR 脚本处理图片并返回文字（支持中英文）"""
        script_path = Path(__file__).parent / "ocr_node" / "ocr_chinese.js"
        try:
            result = subprocess.run(
                ["node", str(script_path), image_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get("text", "").strip()
            else:
                print(f"OCR 失败: {result.stderr}")
                return ""
        except Exception as e:
            print(f"OCR 执行异常: {e}")
            return ""


    def extract_content(self, html_content: str, original_url: str) -> Dict[str, Any]:
        """
        提取文章内容（支持图文混合）

        Args:
            html_content: HTML页面内容
            original_url: 原始URL，用于解析相对路径

        Returns:
            包含文章信息的字典
        """
        result = {
            'title': '',
            'author': '',
            'text_content': '',
            'images': [],
            'image_count': 0,
            'ocr_text': '',
            'status': 'success'
        }

        try:
            # 提取标题
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.I)
            if title_match:
                result['title'] = title_match.group(1).strip()

            # 提取作者信息
            author_match = re.search(r'author["\']?\s*[:=]\s*["\']([^"\']+)', html_content, re.I)
            if author_match:
                result['author'] = author_match.group(1).strip()

            # 提取文本内容
            content_selectors = [
                r'id=["\']js_content["\'][^>]*>(.*?)</div>',
                r'class=["\']rich_media_content["\'][^>]*>(.*?)</div>',
                r'<body[^>]*>(.*?)</body>'
            ]

            for selector in content_selectors:
                content_match = re.search(selector, html_content, re.DOTALL | re.I)
                if content_match:
                    raw_content = content_match.group(1)
                    clean_content = re.sub(r'<[^>]+>', '', raw_content)
                    result['text_content'] = clean_content.strip()
                    break

            # 如果没有提取到内容，使用整个HTML
            if not result['text_content']:
                result['text_content'] = html_content[:2000] + "..." if len(html_content) > 2000 else html_content

            # 提取图片
            image_urls = self.extract_images_from_html(html_content)
            result['images'] = image_urls
            result['image_count'] = len(image_urls)

            # 实际OCR识别（调用 Node OCR）
            if image_urls:
                ocr_texts = []
                for idx, img_url in enumerate(image_urls, start=1):
                    txt = self.ocr_image_via_node(img_url)
                    if txt:
                        ocr_texts.append(f"[图片{idx}] {txt}")
                result['ocr_text'] = "\n".join(ocr_texts)

        except Exception as e:
            result['status'] = f'extraction_error: {str(e)}'

        return result

    def read_article(self, original_url: str) -> Dict[str, Any]:
        """
        读取微信文章（支持图文混合）

        Args:
            original_url: 原始URL

        Returns:
            包含文章信息的字典
        """
        try:
            # 规范化URL
            normalized_url = self.normalize_url(original_url)

            # 使用 requests 抓取页面并解析内容
            try:
                resp = requests.get(normalized_url, timeout=15, headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; wechat-look/1.0)'
                })
                resp.raise_for_status()
                html = resp.text
                # 解析实际内容，包括 OCR
                result = self.extract_content(html, normalized_url)
                result.update({
                    'original_url': original_url,
                    'normalized_url': normalized_url,
                    'status': 'success'
                })
                return result
            except Exception as e:
                return {
                    'original_url': original_url,
                    'normalized_url': normalized_url,
                    'error': str(e),
                    'status': 'failed'
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
    reader = WeChatLookOCR()

    # 测试用例
    test_url = "https://mp.weixin.qq.com/s/D7vSSNGCQFT4NAdY6loPWA"

    print("WeChat Look OCR 演示:")
    print("=" * 50)

    # URL规范化测试
    normalized = reader.normalize_url(test_url)
    print(f"URL规范化:")
    print(f"  原始: {test_url}")
    print(f"  规范: {normalized}")
    print()

    # 文章读取测试
    article_result = reader.read_article(test_url)
    print(f"文章读取结果:")
    print(f"  标题: {article_result.get('title')}")
    print(f"  作者: {article_result.get('author')}")
    print(f"  文本长度: {len(article_result.get('text_content', ''))} 字符")
    print(f"  图片数量: {article_result.get('image_count', 0)}")
    print(f"  OCR文本长度: {len(article_result.get('ocr_text', ''))} 字符")
    print(f"  状态: {article_result.get('status')}")

    # 显示图片URL示例
    images = article_result.get('images', [])
    if images:
        print(f"  图片URL示例: {images[0]}")


if __name__ == "__main__":
    main()