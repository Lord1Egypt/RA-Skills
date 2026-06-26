#!/usr/bin/env python3
"""
微信公众号文章读取工具
用法: python weixin_reader.py <url>
"""

import sys
import httpx
from bs4 import BeautifulSoup


def read_wechat_article(url: str) -> dict:
    """
    读取微信公众号文章内容

    Args:
        url: 微信公众号文章链接

    Returns:
        dict: 包含 title, account, content 的字典
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x18002629) NetType/WIFI Language/zh_CN",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    result = {"title": "", "account": "", "content": "", "error": None}

    try:
        with httpx.Client(follow_redirects=True, timeout=30) as client:
            resp = client.get(url, headers=headers)
            soup = BeautifulSoup(resp.text, 'html.parser')

            # 获取标题
            title_elem = soup.find('h1', class_='rich_media_title') or soup.find('h2', class_='rich_media_title')
            if title_elem:
                result["title"] = title_elem.get_text(strip=True)

            # 获取公众号名称
            account_elem = soup.find('a', id='js_name') or soup.find('span', class_='rich_media_meta_nickname')
            if account_elem:
                result["account"] = account_elem.get_text(strip=True)

            # 获取正文内容
            content_elem = soup.find('div', id='js_content') or soup.find('div', class_='rich_media_content')
            if content_elem:
                result["content"] = content_elem.get_text(separator='\n', strip=True)
            else:
                # 检查是否需要验证
                if soup.find(text=lambda t: t and '验证' in t):
                    result["error"] = "文章需要验证码，无法直接访问"
                else:
                    result["error"] = "无法解析文章内容"

    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python weixin_reader.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    result = read_wechat_article(url)

    if result["error"]:
        print(f"错误: {result['error']}")
        sys.exit(1)

    if result["title"]:
        print(f"标题: {result['title']}")
    if result["account"]:
        print(f"公众号: {result['account']}")
    if result["content"]:
        print(f"\n--- 正文内容 ---\n")
        print(result["content"])


if __name__ == "__main__":
    main()
