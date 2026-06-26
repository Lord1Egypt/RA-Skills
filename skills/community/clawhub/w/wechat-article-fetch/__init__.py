"""
WeChat Article Fetch - 提取微信公众号文章内容

依赖安装：
    pip install beautifulsoup4 requests
"""
import os
import re
from datetime import datetime
from typing import Dict, Optional, List


def fetch_article(
    url: str,
    include_raw_html: bool = False
) -> Dict[str, any]:
    """
    获取微信公众号文章的完整信息
    
    Args:
        url: 微信公众号文章链接 (https://mp.weixin.qq.com/s/xxx)
        include_raw_html: 是否包含原始 HTML
        
    Returns:
        包含文章信息的字典
        
    Example:
        article = fetch_article("https://mp.weixin.qq.com/s/xxx")
        print(article['title'])
        print(article['content'][:200])
    """
    from bs4 import BeautifulSoup
    import requests
    
    # 下载网页
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://mp.weixin.qq.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = 'utf-8'
    html = response.text
    
    # 解析 HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # 提取元数据
    title = _extract_title(soup)
    author = _extract_author(soup)
    publish_time = _extract_publish_time(soup)
    account = _extract_account(soup)
    
    # 提取正文内容
    content = _extract_content(soup)
    
    # 构建返回数据
    result = {
        'title': title,
        'author': author,
        'publish_time': publish_time,
        'account': account,
        'content': content,
        'url': url,
        'content_length': len(content),
        'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if include_raw_html:
        result['raw_html'] = html
    
    return result


def get_article_text(url: str) -> str:
    """
    快速获取文章纯文本内容
    
    Args:
        url: 微信公众号文章链接
        
    Returns:
        文章纯文本内容
    """
    article = fetch_article(url)
    return article['content']


def get_article_metadata(url: str) -> Dict[str, str]:
    """
    获取文章元数据（不包含正文）
    
    Args:
        url: 微信公众号文章链接
        
    Returns:
        包含标题、作者、发布时间等信息的字典
    """
    from bs4 import BeautifulSoup
    import requests
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://mp.weixin.qq.com/',
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    return {
        'title': _extract_title(soup),
        'author': _extract_author(soup),
        'publish_time': _extract_publish_time(soup),
        'account': _extract_account(soup),
        'url': url
    }


def summarize_article(content: str, max_length: int = 500) -> str:
    """
    生成文章摘要（简单版本：取开头部分）
    
    Args:
        content: 文章正文内容
        max_length: 摘要最大长度
        
    Returns:
        文章摘要
    """
    # 移除多余空白
    content = re.sub(r'\n+', '\n', content).strip()
    
    if len(content) <= max_length:
        return content
    
    # 找到合适的截断点（在句号处）
    truncated = content[:max_length]
    last_period = truncated.rfind('。')
    last_question = truncated.rfind('？')
    last_exclaim = truncated.rfind('！')
    
    # 选择最远的标点符号
    break_point = max(last_period, last_question, last_exclaim)
    
    if break_point > max_length * 0.5:  # 确保不是太短
        return truncated[:break_point + 1] + "..."
    else:
        return truncated + "..."


def _extract_title(soup: 'BeautifulSoup') -> str:
    """提取文章标题"""
    # 多种方式尝试
    title = soup.find('h1')
    if title:
        return title.get_text(strip=True)
    
    title = soup.find('title')
    if title:
        text = title.get_text(strip=True)
        # 去除" - 自媒"等后缀
        text = re.sub(r'\s*-.*$', '', text)
        return text
    
    return "未找到标题"


def _extract_author(soup: 'BeautifulSoup') -> str:
    """提取作者信息"""
    # 尝试从不同位置提取
    author_div = soup.find('strong', class_='rich_media_meta_name')
    if author_div:
        return author_div.get_text(strip=True)
    
    author_div = soup.find('div', class_='rich_media_meta')
    if author_div:
        text = author_div.get_text(strip=True)
        # 提取作者名（通常在第一个"·"之前）
        if '·' in text:
            return text.split('·')[0].strip()
        return text
    
    return "未知作者"


def _extract_publish_time(soup: 'BeautifulSoup') -> str:
    """提取发布时间"""
    # 查找时间相关的元素
    time_pattern = r'(\d{4}-\d{2}-\d{2}|\d{4}年\d{2}月\d{2}日)[\s\S]{0,20}(\d{2}:\d{2})?'
    
    for tag in soup.find_all(class_=re.compile('meta|time')):
        text = tag.get_text(strip=True)
        match = re.search(time_pattern, text)
        if match:
            return match.group(0).strip()
    
    # 尝试从页脚提取
    footer = soup.find('div', class_='rich_media_meta_list')
    if footer:
        text = footer.get_text()
        match = re.search(time_pattern, text)
        if match:
            return match.group(0).strip()
    
    return "未知时间"


def _extract_account(soup: 'BeautifulSoup') -> str:
    """提取公众号名称"""
    # 公众号名称通常在分享区域
    share_div = soup.find('div', id='js_share')
    if share_div:
        # 查找公众号名称
        account_span = share_div.find('strong', class_='rich_media_meta_name')
        if account_span:
            return account_span.get_text(strip=True)
    
    # 尝试从 meta 标签提取
    meta = soup.find('meta', property='og/site_name')
    if meta and meta.get('content'):
        return meta['content']
    
    return "未知公众号"


def _extract_content(soup: 'BeautifulSoup') -> str:
    """提取文章正文内容"""
    # 微信公众号文章内容通常在以下区域
    content_div = (
        soup.find('div', id='js_content') or
        soup.find('div', class_='rich_media_content') or
        soup.find('div', class_='rich_media')
    )
    
    if not content_div:
        return "未找到文章内容"
    
    # 移除不需要的元素
    for tag in content_div.find_all(['script', 'style', 'noscript']):
        tag.decompose()
    
    # 移除广告和推广
    for tag in content_div.find_all(class_=re.compile('ad|promo|推广 | 广告', re.I)):
        tag.decompose()
    
    # 提取文本（保留段落结构）
    text = content_div.get_text('\n', strip=True)
    
    # 清理多余空白
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()


def batch_fetch_articles(urls: List[str]) -> List[Dict[str, any]]:
    """
    批量获取多篇文章
    
    Args:
        urls: 文章链接列表
        
    Returns:
        文章信息列表
    """
    results = []
    for url in urls:
        try:
            article = fetch_article(url)
            results.append(article)
        except Exception as e:
            results.append({
                'url': url,
                'error': str(e)
            })
    return results


# 导出公共 API
__all__ = [
    'fetch_article',
    'get_article_text',
    'get_article_metadata',
    'summarize_article',
    'batch_fetch_articles'
]
