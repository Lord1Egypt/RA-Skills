
"""
微信公众号文章搜索与读取模块
提供搜索和读取微信公众号文章的功能，支持简单模式和Playwright模式
"""

import asyncio
import miku_ai.spider
import requests
from bs4 import BeautifulSoup


def search_articles(query, top_num=5):
    """
    搜索微信公众号文章
    
    Args:
        query (str): 搜索关键词
        top_num (int): 返回结果数量，默认5篇
    
    Returns:
        list: 文章列表，每篇包含 title, snippet, url, source, date
    """
    articles = asyncio.run(miku_ai.spider.get_wexin_article(query, top_num))
    return articles


def read_article_simple(url):
    """
    使用简单模式读取微信公众号文章内容（requests + BeautifulSoup）
    
    Args:
        url (str): 微信文章URL
    
    Returns:
        dict: 包含 title, author, paragraphs 的字典
    """
    # 简化URL
    simple_url = url.split("&new=1")[0] if "&new=1" in url else url
    
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    
    response = requests.get(simple_url, headers=headers, timeout=30, allow_redirects=True)
    
    if response.status_code != 200:
        raise Exception(f"请求失败，状态码: {response.status_code}")
    
    # 解析HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 提取标题
    title_elem = soup.find('h1', {'class': 'rich_media_title'})
    title = title_elem.get_text().strip() if title_elem else "N/A"
    
    # 提取公众号
    author_elem = soup.find('a', {'id': 'js_name'})
    author = author_elem.get_text().strip() if author_elem else "N/A"
    
    # 提取正文
    content_div = soup.find('div', {'id': 'js_content'})
    if not content_div:
        raise Exception("未找到正文内容")
    
    # 移除脚本和样式
    for script in content_div.find_all(['script', 'style']):
        script.decompose()
    
    # 提取段落
    paragraphs = content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li'])
    valid_paragraphs = []
    
    for p in paragraphs:
        text = p.get_text().strip()
        if len(text) > 5:
            valid_paragraphs.append(text)
    
    return {
        "title": title,
        "author": author,
        "paragraphs": valid_paragraphs,
        "mode": "simple"
    }


def read_article(url, mode="auto", screenshot_path=None):
    """
    读取微信公众号文章内容（支持多种模式）
    
    Args:
        url (str): 微信文章URL
        mode (str): 读取模式 - "simple"| "playwright"| "auto"
        screenshot_path (str, optional): Playwright模式下的截图保存路径
    
    Returns:
        dict: 包含 title, author, paragraphs 的字典
    """
    if mode == "simple":
        return read_article_simple(url)
    
    elif mode == "playwright":
        from wechat_articles_playwright import read_article_playwright_sync
        return read_article_playwright_sync(url, screenshot_path)
    
    elif mode == "auto":
        # 自动模式：先试简单模式，失败再试Playwright
        try:
            return read_article_simple(url)
        except Exception as e:
            print(f"简单模式失败: {e}，尝试Playwright模式...")
            from wechat_articles_playwright import read_article_playwright_sync
            return read_article_playwright_sync(url, screenshot_path)
    
    else:
        raise ValueError(f"未知模式: {mode}，可选值: simple, playwright, auto")


def print_article_summary(article):
    """
    打印文章摘要（搜索结果）
    """
    print(f"标题: {article['title']}")
    print(f"来源: {article['source']}")
    print(f"日期: {article['date']}")
    print(f"链接: {article['url']}")
    if article.get('snippet'):
        print(f"摘要: {article['snippet'][:100]}...")
    print("-" * 60)


def print_article_content(content, max_paragraphs=50):
    """
    打印文章内容
    """
    print("=" * 80)
    print(f"标题: {content['title']}")
    print(f"公众号: {content['author']}")
    print(f"模式: {content.get('mode', 'unknown')}")
    print("=" * 80)
    print()
    
    for i, p in enumerate(content['paragraphs'][:max_paragraphs]):
        print(p)
        print()
    
    if len(content['paragraphs']) > max_paragraphs:
        print(f"... (还有 {len(content['paragraphs']) - max_paragraphs} 段)")
