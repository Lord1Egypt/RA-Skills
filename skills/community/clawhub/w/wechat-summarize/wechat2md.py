#!/usr/bin/env python3
"""
微信公众号文章转 Markdown 工具

Usage:
    python wechat2md.py <url>
    python wechat2md.py <url> --save-images
"""

import argparse
import os
import re
import sys
from urllib.parse import urlparse

import html2text
import requests
from bs4 import BeautifulSoup


def fetch_article(url: str) -> str:
    """抓取微信公众号文章 HTML"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    response.encoding = 'utf-8'
    return response.text


def parse_article(html: str) -> tuple[str, str]:
    """解析文章，返回 (标题, 正文HTML)"""
    soup = BeautifulSoup(html, 'html.parser')

    # 提取标题
    title_elem = soup.find(id='activity-name')
    if not title_elem:
        title_elem = soup.find(class_='rich_media_title')
    title = title_elem.get_text().strip() if title_elem else '未知标题'

    # 提取正文
    content_elem = soup.find(id='js_content')
    if not content_elem:
        raise ValueError('无法找到文章正文 (id="js_content")')

    # 微信图片使用 data-src 懒加载，需要转换为 src
    for img in content_elem.find_all('img'):
        data_src = img.get('data-src')
        if data_src:
            img['src'] = data_src

    return title, str(content_elem)


def html_to_markdown(html: str) -> str:
    """将 HTML 转换为 Markdown"""
    h = html2text.HTML2Text()
    h.body_width = 0  # 禁用自动换行
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.skip_internal_links = True
    return h.handle(html)


def sanitize_filename(name: str) -> str:
    """清理文件名，移除非法字符"""
    # 移除/替换非法字符
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    # 限制长度
    if len(name) > 100:
        name = name[:100]
    return name


def download_images(markdown: str, output_dir: str, article_url: str) -> str:
    """下载图片到本地并替换链接"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36',
        'Referer': article_url
    }

    # 查找所有图片链接
    img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    images = re.findall(img_pattern, markdown)

    if not images:
        return markdown

    # 创建 images 目录
    img_dir = os.path.join(output_dir, 'images')
    os.makedirs(img_dir, exist_ok=True)

    for idx, (alt, url) in enumerate(images, 1):
        if not url.startswith('http'):
            continue

        try:
            # 下载图片
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()

            # 确定扩展名
            content_type = resp.headers.get('Content-Type', '')
            if 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            elif 'webp' in content_type:
                ext = '.webp'
            else:
                ext = '.jpg'

            # 保存图片
            img_filename = f'image_{idx:02d}{ext}'
            img_path = os.path.join(img_dir, img_filename)
            with open(img_path, 'wb') as f:
                f.write(resp.content)

            # 替换 Markdown 中的链接
            new_img_ref = f'![{alt}](images/{img_filename})'
            markdown = markdown.replace(f'![{alt}]({url})', new_img_ref)
            print(f'  下载图片: {img_filename}')

        except Exception as e:
            print(f'  图片下载失败: {url[:50]}... ({e})')

    return markdown


def main():
    parser = argparse.ArgumentParser(description='微信公众号文章转 Markdown')
    parser.add_argument('url', help='微信公众号文章链接')
    parser.add_argument('--save-images', action='store_true',
                        help='下载图片到本地')
    parser.add_argument('-o', '--output', help='输出目录 (默认当前目录)')
    args = parser.parse_args()

    # 验证 URL
    if 'mp.weixin.qq.com' not in args.url:
        print('警告: 这可能不是微信公众号文章链接')

    print(f'正在抓取文章...')

    try:
        # 抓取文章
        html = fetch_article(args.url)

        # 解析文章
        title, content_html = parse_article(html)
        print(f'标题: {title}')

        # 转换为 Markdown
        markdown = html_to_markdown(content_html)

        # 添加标题
        markdown = f'# {title}\n\n{markdown}'

        # 确定输出路径
        safe_title = sanitize_filename(title)
        output_dir = args.output or '.'

        if args.save_images:
            # 创建文章目录
            article_dir = os.path.join(output_dir, safe_title)
            os.makedirs(article_dir, exist_ok=True)

            # 下载图片
            print('正在下载图片...')
            markdown = download_images(markdown, article_dir, args.url)

            # 保存 Markdown
            output_path = os.path.join(article_dir, f'{safe_title}.md')
        else:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f'{safe_title}.md')

        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f'已保存: {output_path}')

    except requests.RequestException as e:
        print(f'网络错误: {e}', file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f'解析错误: {e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'错误: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
