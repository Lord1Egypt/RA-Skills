#!/usr/bin/env python3
"""
通用网页文章提取器
支持：微信公众号、知乎专栏、简书、CSDN 等
"""

import sys
import json
import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def clean_text(text):
    """清理文本内容"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_zhihu(soup):
    """提取知乎文章"""
    # 知乎专栏文章选择器
    title = ""
    title_elem = soup.select_one('h1, .Post-Title, [data-zop-title]')
    if title_elem:
        title = clean_text(title_elem.get_text())
    
    author = ""
    author_elem = soup.select_one('.AuthorInfo-name, .UserLink-link')
    if author_elem:
        author = clean_text(author_elem.get_text())
    
    content = ""
    content_elem = soup.select_one('.Post-RichTextContainer, .RichContent-inner')
    if content_elem:
        for script in content_elem(['script', 'style', 'iframe']):
            script.decompose()
        paragraphs = []
        for p in content_elem.find_all(['p', 'h2', 'h3', 'li']):
            text = clean_text(p.get_text())
            if text and len(text) > 5:
                paragraphs.append(text)
        content = '\n\n'.join(paragraphs)
    
    return {'title': title, 'author': author, 'content': content}


def extract_weixin(soup):
    """提取微信公众号文章"""
    title = ""
    title_elem = soup.select_one('#activity_name, .rich_media_title, h1')
    if title_elem:
        title = clean_text(title_elem.get_text())
    
    account = ""
    account_elem = soup.select_one('#js_name, .profile_nickname')
    if account_elem:
        account = clean_text(account_elem.get_text())
    
    author = ""
    author_elem = soup.select_one('#js_author_name')
    if author_elem:
        author = clean_text(author_elem.get_text())
    
    content = ""
    content_elem = soup.select_one('#js_content, .rich_media_content')
    if content_elem:
        for script in content_elem(['script', 'style', 'iframe']):
            script.decompose()
        paragraphs = []
        for p in content_elem.find_all(['p', 'section']):
            text = clean_text(p.get_text())
            if text and len(text) > 5:
                paragraphs.append(text)
        content = '\n\n'.join(paragraphs)
    
    return {'title': title, 'account': account, 'author': author, 'content': content}


def extract_generic(soup):
    """通用提取策略"""
    title = ""
    # 尝试多种标题选择器
    for selector in ['h1', 'article h1', '.article-title', '.post-title', '[class*="title"]']:
        elem = soup.select_one(selector)
        if elem:
            title = clean_text(elem.get_text())
            if len(title) > 5:
                break
    
    # 找正文内容
    content = ""
    for selector in ['article', 'main', '[class*="content"]', '[class*="article"]', '.post']:
        elem = soup.select_one(selector)
        if elem:
            for script in elem(['script', 'style', 'iframe', 'nav', 'header', 'footer']):
                script.decompose()
            paragraphs = []
            for p in elem.find_all(['p', 'h2', 'h3', 'li']):
                text = clean_text(p.get_text())
                if text and len(text) > 10:
                    paragraphs.append(text)
            if len(paragraphs) > 3:
                content = '\n\n'.join(paragraphs)
                break
    
    return {'title': title, 'content': content}


def extract_article(url):
    """提取文章内容"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = context.new_page()
        
        try:
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(3000)  # 等待 JS 渲染
            
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # 根据域名选择提取策略
            if 'zhuanlan.zhihu.com' in url or 'zhihu.com' in url:
                data = extract_zhihu(soup)
                platform = '知乎'
            elif 'mp.weixin.qq.com' in url:
                data = extract_weixin(soup)
                platform = '微信公众号'
            else:
                data = extract_generic(soup)
                platform = '通用'
            
            browser.close()
            
            return {
                'success': True,
                'url': url,
                'platform': platform,
                **data,
                'content_length': len(data.get('content', ''))
            }
            
        except Exception as e:
            browser.close()
            return {
                'success': False,
                'error': str(e),
                'url': url
            }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': '请提供文章链接'}, ensure_ascii=False))
        sys.exit(1)
    
    url = sys.argv[1]
    result = extract_article(url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
