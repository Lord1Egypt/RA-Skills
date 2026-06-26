#!/usr/bin/env python3
"""
微信公众号文章解析器
解析 mp.weixin.qq.com 文章，提取标题、作者、正文、图片。
核心：iPhone UA 绕过微信验证 + BeautifulSoup 解析。
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import sys
from datetime import datetime


def parse_article(url):
    """解析微信公众号文章"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) '
                      'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 '
                      'Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')

        # 标题
        title_tag = soup.find('h1', class_='rich_media_title')
        title = title_tag.get_text(strip=True) if title_tag else None
        if not title:
            m = re.search(r'var\s+msg_title\s*=\s*["\']([^"\']+)["\']', resp.text)
            title = m.group(1) if m else "未知标题"

        # 作者/公众号
        author_tag = soup.find('a', class_='rich_media_meta_link')
        if not author_tag:
            author_tag = soup.find('span', class_='rich_media_meta_nickname')
        author = author_tag.get_text(strip=True) if author_tag else "未知"

        # 发布时间
        time_tag = soup.find('span', id='publish_time')
        if time_tag:
            publish_time = time_tag.get_text(strip=True)
        else:
            m = re.search(r'var\s+publish_time\s*=\s*"([^"]+)"', resp.text)
            publish_time = m.group(1) if m else None

        # 正文
        content_div = soup.find('div', class_='rich_media_content')
        content = ""
        images = []

        if content_div:
            for tag in content_div(['script', 'style']):
                tag.decompose()

            # 提取图片
            for img in content_div.find_all('img'):
                img_url = img.get('data-src') or img.get('src')
                if img_url and not img_url.startswith('data:'):
                    images.append(img_url)

            # 提取段落（去重，保留结构）
            seen = set()
            paragraphs = []
            for p in content_div.find_all(['p', 'section']):
                text = p.get_text(strip=True)
                if text and len(text) > 10 and text not in seen:
                    seen.add(text)
                    paragraphs.append(text)
            content = '\n\n'.join(paragraphs)

        return {
            'title': title,
            'author': author,
            'publish_time': publish_time,
            'content': content,
            'word_count': len(content),
            'images_count': len(images),
            'images': images[:20],
            'url': url,
            'parsed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'ok'
        }

    except Exception as e:
        return {
            'error': str(e),
            'url': url,
            'status': 'error'
        }


def print_result(article):
    if article.get('status') == 'error':
        print(f"❌ 解析失败: {article['error']}")
        return
    print(f"📰 标题: {article['title']}")
    print(f"✍️  作者: {article['author']}")
    print(f"🕐 时间: {article.get('publish_time', '未知')}")
    print(f"📊 字数: {article['word_count']}")
    print(f"🖼️  图片: {article['images_count']}")
    print("─" * 60)
    text = article['content']
    print(text[:2000] + ("..." if len(text) > 2000 else ""))


def main():
    if len(sys.argv) < 2:
        print("用法: python3 parse_article.py <URL> [--save] [--output file.json]")
        sys.exit(1)

    url = sys.argv[1]
    article = parse_article(url)
    print_result(article)

    if '--save' in sys.argv:
        out = 'output.json'
        if '--output' in sys.argv:
            idx = sys.argv.index('--output')
            if idx + 1 < len(sys.argv):
                out = sys.argv[idx + 1]
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(article, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 已保存到 {out}")


if __name__ == '__main__':
    main()
