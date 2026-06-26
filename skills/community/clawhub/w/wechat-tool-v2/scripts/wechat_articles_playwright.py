
"""
微信公众号文章搜索与读取模块 - Playwright版本
提供更稳定的文章读取功能，使用真实浏览器
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def read_article_playwright(url, screenshot_path=None, headless=True):
    """
    使用Playwright读取微信公众号文章内容
    
    Args:
        url (str): 微信文章URL
        screenshot_path (str, optional): 截图保存路径
        headless (bool): 是否无头模式，默认True
    
    Returns:
        dict: 包含 title, author, paragraphs 的字典
    """
    # 简化URL
    simple_url = url.split("&new=1")[0] if "&new=1" in url else url
    
    iphone_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page(user_agent=iphone_ua)
        
        try:
            # 访问页面
            await page.goto(simple_url, wait_until="networkidle", timeout=60000)
            
            # 保存截图（如果需要）
            if screenshot_path:
                await page.screenshot(path=screenshot_path, full_page=True)
            
            # 获取页面内容
            content = await page.content()
            
            # 解析
            soup = BeautifulSoup(content, 'html.parser')
            
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
                "mode": "playwright"
            }
            
        finally:
            await browser.close()


def read_article_playwright_sync(url, screenshot_path=None, headless=True):
    """
    同步版本的Playwright读取函数
    """
    return asyncio.run(read_article_playwright(url, screenshot_path, headless))


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
