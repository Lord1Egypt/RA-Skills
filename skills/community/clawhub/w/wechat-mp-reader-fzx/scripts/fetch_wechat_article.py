#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章抓取工具
支持提取标题、作者、发布时间、正文内容，并转换为 Markdown 格式
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from html import unescape
from urllib.parse import unquote, urlparse

import requests


def clean_html(text):
    """清理 HTML 实体和多余空白"""
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_title(html_text):
    """提取文章标题"""
    # 尝试多种标题匹配模式
    patterns = [
        r'<h1[^>]*class=["\']rich_media_title[^>]*>(.*?)</h1>',
        r'<h2[^>]*class=["\']rich_media_title[^>]*>(.*?)</h2>',
        r'var msg_title = ["\'](.+?)["\']\.html\(false\)',
        r'activity_name = ["\'](.+?)["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text, re.DOTALL)
        if match:
            title = clean_html(match.group(1))
            # 移除 HTML 标签
            title = re.sub(r'<[^>]+>', '', title)
            return title
    return None


def extract_author(html_text):
    """提取公众号名称/作者"""
    patterns = [
        r'<a[^>]*id=["\']js_name[^>]*>(.*?)</a>',
        r'var nickname = ["\'](.+?)["\']',
        r'"nick_name":"([^"]+)"',
        r'<span[^>]*class=["\']profile_nickname[^>]*>(.*?)</span>',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text, re.DOTALL)
        if match:
            return clean_html(match.group(1))
    return None


def extract_publish_time(html_text):
    """提取发布时间"""
    patterns = [
        r'<em[^>]*id=["\']publish_time[^>]*>(.*?)</em>',
        r'var publish_time = ["\'](.+?)["\']',
        r's="(\d{4}-\d{2}-\d{2})"',
        r'"svr_time":(\d+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text, re.DOTALL)
        if match:
            time_str = match.group(1)
            # 尝试解析时间戳
            if time_str.isdigit():
                return datetime.fromtimestamp(int(time_str)).strftime('%Y-%m-%d %H:%M:%S')
            return clean_html(time_str)
    return None


def extract_cover_image(html_text):
    """提取封面图 URL"""
    patterns = [
        r'var msg_cdn_url = ["\'](.+?)["\']',
        r'<img[^>]*data-src=["\'](https://mmbiz\.qpic\.cn[^"\']+)["\'][^>]*>',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text, re.DOTALL)
        if match:
            return match.group(1)
    return None


def html_to_markdown(html_text, base_url=None):
    """将 HTML 内容转换为 Markdown"""
    md = html_text

    # 1. 处理图片
    def replace_img(match):
        attrs = match.group(1)
        # 提取 data-src 或 src
        src_match = re.search(r'data-src=["\']([^"\']+)["\']', attrs)
        if not src_match:
            src_match = re.search(r'src=["\']([^"\']+)["\']', attrs)
        src = src_match.group(1) if src_match else ''

        # 提取 alt
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', attrs)
        alt = alt_match.group(1) if alt_match else 'image'

        if src:
            return f'\n\n![{alt}]({src})\n\n'
        return ''

    md = re.sub(r'<img([^>]*)>', replace_img, md)

    # 2. 处理视频
    def replace_video(match):
        attrs = match.group(1)
        src_match = re.search(r'data-src=["\']([^"\']+)["\']', attrs)
        src = src_match.group(1) if src_match else ''
        if src:
            return f'\n\n[视频]({src})\n\n'
        return ''

    md = re.sub(r'<iframe([^>]*)>', replace_video, md)
    md = re.sub(r'<mpvideo([^>]*)>', replace_video, md)

    # 3. 处理标题
    md = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', md, flags=re.DOTALL)
    md = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', md, flags=re.DOTALL)
    md = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', md, flags=re.DOTALL)
    md = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n#### \1\n', md, flags=re.DOTALL)
    md = re.sub(r'<h5[^>]*>(.*?)</h5>', r'\n##### \1\n', md, flags=re.DOTALL)
    md = re.sub(r'<h6[^>]*>(.*?)</h6>', r'\n###### \1\n', md, flags=re.DOTALL)

    # 4. 处理段落和换行
    md = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\1\n', md, flags=re.DOTALL)
    md = re.sub(r'<br\s*/?>', '\n', md)
    md = re.sub(r'<section[^>]*>(.*?)</section>', r'\n\1\n', md, flags=re.DOTALL)

    # 5. 处理文本样式
    md = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', md, flags=re.DOTALL)
    md = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', md, flags=re.DOTALL)
    md = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', md, flags=re.DOTALL)
    md = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', md, flags=re.DOTALL)

    # 6. 处理链接
    def replace_link(match):
        attrs = match.group(1)
        text = match.group(2)
        href_match = re.search(r'href=["\']([^"\']+)["\']', attrs)
        href = href_match.group(1) if href_match else ''
        if href and text.strip():
            return f'[{text.strip()}]({href})'
        return text

    md = re.sub(r'<a([^>]*)>(.*?)</a>', replace_link, md, flags=re.DOTALL)
    # 处理没有 href 的 a 标签
    md = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', md, flags=re.DOTALL)

    # 7. 处理列表
    md = re.sub(r'<ul[^>]*>(.*?)</ul>', r'\n\1\n', md, flags=re.DOTALL)
    md = re.sub(r'<ol[^>]*>(.*?)</ol>', r'\n\1\n', md, flags=re.DOTALL)
    md = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', md, flags=re.DOTALL)

    # 8. 处理引用
    md = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1\n', md, flags=re.DOTALL)

    # 9. 处理代码
    md = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', md, flags=re.DOTALL)
    md = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```', md, flags=re.DOTALL)

    # 10. 清理剩余 HTML 标签
    md = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', md, flags=re.DOTALL)
    md = re.sub(r'<div[^>]*>(.*?)</div>', r'\1', md, flags=re.DOTALL)
    md = re.sub(r'<[^>]+>', '', md)

    # 11. 清理多余空白
    md = re.sub(r'\n{3,}', '\n\n', md)
    md = re.sub(r'[ \t]+\n', '\n', md)

    return md.strip()


def extract_content(html_text):
    """提取文章正文内容"""
    # 尝试多种内容匹配模式
    patterns = [
        # 标准模式
        r'<div[^>]*id=["\']js_content[^>]*>(.*?)</div>\s*</div>\s*<script',
        # 备用模式
        r'<div[^>]*id=["\']js_content[^>]*>(.*?)</div>\s*<script',
        # 更宽松的模式
        r'<div[^>]*id=["\']js_content[^>]*>(.*?)<script[^>]*>',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text, re.DOTALL)
        if match:
            return match.group(1)
    return None


def fetch_article(url, output_dir=None, save_images=False):
    """
    抓取微信公众号文章

    Args:
        url: 文章链接
        output_dir: 输出目录，默认为当前目录
        save_images: 是否下载图片到本地

    Returns:
        dict: 包含文章信息的字典
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    print(f'正在抓取: {url}')
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    html_text = resp.text

    # 提取信息
    title = extract_title(html_text)
    author = extract_author(html_text)
    publish_time = extract_publish_time(html_text)
    cover = extract_cover_image(html_text)
    content_html = extract_content(html_text)

    if not content_html:
        raise ValueError('无法提取文章正文，可能是页面结构变化或文章已被删除')

    # 转换为 Markdown
    content_md = html_to_markdown(content_html)

    # 构建 Markdown 文档
    md_lines = []
    if title:
        md_lines.append(f'# {title}')
        md_lines.append('')
    if author:
        md_lines.append(f'**公众号**: {author}')
    if publish_time:
        md_lines.append(f'**发布时间**: {publish_time}')
    if cover:
        md_lines.append(f'**封面**: ![封面]({cover})')
    md_lines.append(f'**原文链接**: {url}')
    md_lines.append('')
    md_lines.append('---')
    md_lines.append('')
    md_lines.append(content_md)

    markdown = '\n'.join(md_lines)

    # 保存文件
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = os.getcwd()

    # 生成文件名
    safe_title = re.sub(r'[^\w\u4e00-\u9fff-]', '_', title or 'untitled')[:50]
    filename = f"{safe_title}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f'已保存: {filepath}')

    return {
        'title': title,
        'author': author,
        'publish_time': publish_time,
        'cover': cover,
        'url': url,
        'content': content_md,
        'markdown': markdown,
        'filepath': filepath,
    }


def main():
    parser = argparse.ArgumentParser(description='抓取微信公众号文章并转换为 Markdown')
    parser.add_argument('url', help='微信公众号文章链接')
    parser.add_argument('-o', '--output', help='输出目录', default=None)
    parser.add_argument('--images', action='store_true', help='下载图片到本地')
    parser.add_argument('--json', action='store_true', help='以 JSON 格式输出')

    args = parser.parse_args()

    try:
        result = fetch_article(args.url, output_dir=args.output, save_images=args.images)

        if args.json:
            # 移除 content 和 markdown 避免输出过大
            output = {k: v for k, v in result.items() if k not in ('content', 'markdown')}
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(f"\n标题: {result['title']}")
            print(f"作者: {result['author']}")
            print(f"时间: {result['publish_time']}")
            print(f"文件: {result['filepath']}")

    except requests.RequestException as e:
        print(f'网络请求失败: {e}', file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f'解析失败: {e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'错误: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
