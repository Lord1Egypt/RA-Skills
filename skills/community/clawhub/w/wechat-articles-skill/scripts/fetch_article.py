#!/usr/bin/env python3
"""
微信公众号文章抓取脚本
使用Playwright抓取文章并转换为Markdown格式
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("需要安装playwright: pip install playwright && playwright install chromium")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("需要安装beautifulsoup4: pip install beautifulsoup4")
    sys.exit(1)


def clean_filename(name: str) -> str:
    """清理文件名，移除非法字符"""
    # 移除Windows/Linux不支持的字段
    name = re.sub(r'[<>:"/\\|?*\n\r\t]', '', name)
    # 移除首尾空格和点
    name = name.strip('. ')
    # 限制长度
    return name[:100] if name else 'untitled'


def html_to_markdown(html_content: str, images_dir: Path = None, download_images: bool = True) -> str:
    """将HTML内容转换为Markdown格式"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 处理图片
    for img in soup.find_all('img'):
        src = img.get('data-src') or img.get('src')
        if src and images_dir and download_images:
            # 图片会在后续下载，这里先创建占位符
            alt = img.get('alt', '图片')
            img.replace_with(f'![{alt}]({src})')
        elif src:
            alt = img.get('alt', '图片')
            img.replace_with(f'![{alt}]({src})')
    
    # 处理链接
    for a in soup.find_all('a'):
        href = a.get('href', '')
        text = a.get_text(strip=True)
        if href and text:
            a.replace_with(f'[{text}]({href})')
        elif text:
            a.replace_with(text)
    
    # 处理标题
    for i, tag in enumerate(['h6', 'h5', 'h4', 'h3', 'h2', 'h1']):
        for h in soup.find_all(tag):
            level = 6 - i
            h.replace_with(f'\n{"#" * level} {h.get_text(strip=True)}\n')
    
    # 处理列表
    for ul in soup.find_all('ul'):
        for li in ul.find_all('li', recursive=False):
            li.insert_before('- ')
        ul.insert_after('\n')
    
    for ol in soup.find_all('ol'):
        for i, li in enumerate(ol.find_all('li', recursive=False), 1):
            li.insert_before(f'{i}. ')
        ol.insert_after('\n')
    
    # 处理段落和换行
    for p in soup.find_all('p'):
        p.insert_after('\n')
    
    for br in soup.find_all('br'):
        br.replace_with('\n')
    
    # 处理加粗和斜体
    for strong in soup.find_all(['strong', 'b']):
        text = strong.get_text()
        strong.replace_with(f'**{text}**')
    
    for em in soup.find_all(['em', 'i']):
        text = em.get_text()
        em.replace_with(f'*{text}*')
    
    # 处理代码块
    for pre in soup.find_all('pre'):
        code = pre.get_text()
        pre.replace_with(f'\n```\n{code}\n```\n')
    
    for code in soup.find_all('code'):
        if code.parent.name != 'pre':
            text = code.get_text()
            code.replace_with(f'`{text}`')
    
    # 处理引用
    for blockquote in soup.find_all('blockquote'):
        lines = blockquote.get_text().strip().split('\n')
        quoted = '\n'.join(f'> {line}' for line in lines)
        blockquote.replace_with(f'\n{quoted}\n')
    
    # 获取纯文本
    text = soup.get_text()
    
    # 清理多余空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def fetch_wechat_article(url: str, output_dir: str = '.', download_images: bool = True) -> dict:
    """
    抓取微信公众号文章
    
    Args:
        url: 微信文章链接
        output_dir: 输出目录
        download_images: 是否下载图片
    
    Returns:
        包含文章信息的字典
    """
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            print(f"正在打开: {url}")
            page.goto(url, timeout=60000, wait_until='networkidle')
            
            # 等待关键元素加载
            page.wait_for_selector('#js_content', timeout=30000)
            
            # 提取信息
            title = page.locator('#activity-name').inner_text(timeout=5000).strip()
            
            # 尝试获取公众号名称
            try:
                author = page.locator('#js_name').inner_text(timeout=3000).strip()
            except:
                author = "未知公众号"
            
            # 获取正文HTML
            content_html = page.locator('#js_content').inner_html()
            
            # 获取完整页面标题作为备选
            page_title = page.title()
            
            print(f"标题: {title}")
            print(f"公众号: {author}")
            
            return {
                'title': title or page_title,
                'author': author,
                'url': url,
                'content_html': content_html,
                'fetch_time': datetime.utcnow().isoformat() + 'Z'
            }
            
        except Exception as e:
            print(f"抓取失败: {e}")
            raise
        finally:
            browser.close()


def save_article(article: dict, output_dir: str, download_images: bool = True):
    """保存文章为Markdown文件"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 创建图片目录
    images_dir = output_path / 'images'
    if download_images:
        images_dir.mkdir(exist_ok=True)
    
    # 转换内容
    markdown_content = html_to_markdown(
        article['content_html'],
        images_dir if download_images else None,
        download_images
    )
    
    # 构建完整Markdown
    filename = clean_filename(article['title'])
    
    frontmatter = f"""---
title: {article['title']}
author: {article['author']}
url: {article['url']}
fetched: {article['fetch_time']}
---

"""
    
    full_content = frontmatter + f"# {article['title']}\n\n> 作者：{article['author']}\n\n{markdown_content}"
    
    # 保存文件
    md_path = output_path / f"{filename}.md"
    
    # 避免覆盖
    counter = 1
    while md_path.exists():
        md_path = output_path / f"{filename}_{counter}.md"
        counter += 1
    
    md_path.write_text(full_content, encoding='utf-8')
    print(f"已保存: {md_path}")
    
    return str(md_path)


def main():
    parser = argparse.ArgumentParser(description='抓取微信公众号文章')
    parser.add_argument('url', help='微信文章链接')
    parser.add_argument('--output', '-o', default='.', help='输出目录 (默认: 当前目录)')
    parser.add_argument('--no-images', action='store_true', help='不下载图片')
    
    args = parser.parse_args()
    
    try:
        article = fetch_wechat_article(
            args.url,
            args.output,
            not args.no_images
        )
        
        saved_path = save_article(
            article,
            args.output,
            not args.no_images
        )
        
        print(f"\n✅ 抓取完成!")
        print(f"📄 文件: {saved_path}")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
