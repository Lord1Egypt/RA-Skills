#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章内容获取脚本
用于绕过 WebFetch 无法获取的情况
"""

import re
import sys
import html
import json
import requests
from urllib.parse import unquote

# 设置输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def fetch_wechat_article(url: str) -> dict:
    """
    获取微信公众号文章内容

    Args:
        url: 公众号文章链接

    Returns:
        dict: 包含 title, author, content 的字典
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        html_content = response.text

        result = {
            'title': '',
            'author': '',
            'account': '',
            'content': '',
            'success': True,
            'error': None
        }

        # 提取标题
        title_patterns = [
            r'<h1[^>]*class="rich_media_title"[^>]*>(.*?)</h1>',
            r'<meta\s+property="og:title"\s+content="([^"]+)"',
            r'var\s+msg_title\s*=\s*["\'](.+?)["\']',
        ]
        for pattern in title_patterns:
            match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if match:
                result['title'] = clean_text(match.group(1))
                break

        # 提取作者
        author_patterns = [
            r'<span[^>]*class="rich_media_meta_text"[^>]*>(.*?)</span>',
            r'var\s+author\s*=\s*["\'](.+?)["\']',
            r'<meta\s+name="author"\s+content="([^"]+)"',
        ]
        for pattern in author_patterns:
            match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if match:
                result['author'] = clean_text(match.group(1))
                break

        # 提取公众号名称
        account_patterns = [
            r'var\s+nickname\s*=\s*["\'](.+?)["\']',
            r'<a[^>]*id="js_name"[^>]*>(.*?)</a>',
            r'profile_nickname\s*=\s*["\'](.+?)["\']',
        ]
        for pattern in account_patterns:
            match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
            if match:
                result['account'] = clean_text(match.group(1))
                break

        # 提取正文内容
        content_match = re.search(
            r'<div[^>]*id="js_content"[^>]*>(.*?)</div>\s*<div[^>]*class="(?:ct_mpda_wrp|qr_code)',
            html_content,
            re.DOTALL | re.IGNORECASE
        )

        if not content_match:
            # 备用正则 - 更宽松的匹配
            content_match = re.search(
                r'<div[^>]*id="js_content"[^>]*>([\s\S]*?)</div>\s*(?:<script|<div[^>]*class="rich_media_tool")',
                html_content,
                re.IGNORECASE
            )

        if not content_match:
            # 最宽松的匹配
            content_match = re.search(
                r'id="js_content"[^>]*>([\s\S]*?)<div[^>]*class="rich_media_area_extra"',
                html_content,
                re.IGNORECASE
            )

        if content_match:
            raw_content = content_match.group(1)
            result['content'] = extract_text_from_html(raw_content)

        # 检查是否遇到验证页面
        if '环境异常' in html_content or '完成验证' in html_content:
            result['success'] = False
            result['error'] = '遇到微信验证页面，需要人工验证'

        # 检查是否获取到内容
        if not result['content'] and not result['title']:
            result['success'] = False
            result['error'] = '未能提取到文章内容'

        return result

    except requests.exceptions.Timeout:
        return {'success': False, 'error': '请求超时'}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': f'请求失败: {str(e)}'}
    except Exception as e:
        return {'success': False, 'error': f'解析失败: {str(e)}'}


def clean_text(text: str) -> str:
    """清理文本，去除 HTML 标签和多余空白"""
    if not text:
        return ''
    # 解码 HTML 实体
    text = html.unescape(text)
    # 去除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    # 去除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_text_from_html(html_content: str) -> str:
    """从 HTML 中提取纯文本，保留段落结构"""
    if not html_content:
        return ''

    # 解码 HTML 实体
    text = html.unescape(html_content)

    # 将块级元素转换为换行
    block_tags = ['p', 'div', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'section']
    for tag in block_tags:
        text = re.sub(f'<{tag}[^>]*>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(f'</{tag}>', '\n', text, flags=re.IGNORECASE)

    # 去除所有剩余 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)

    # 清理空白
    lines = [line.strip() for line in text.split('\n')]
    lines = [line for line in lines if line]
    text = '\n'.join(lines)

    return text


def main():
    if len(sys.argv) < 2:
        print("用法: python fetch_article.py <公众号文章URL> [--json]")
        sys.exit(1)

    url = sys.argv[1]
    output_json = '--json' in sys.argv

    result = fetch_wechat_article(url)

    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result['success']:
            print(f"【标题】{result['title']}")
            print(f"【公众号】{result['account']}")
            print(f"【作者】{result['author']}")
            print(f"\n【正文】\n{result['content']}")
        else:
            print(f"获取失败: {result['error']}")
            sys.exit(1)


if __name__ == '__main__':
    main()
