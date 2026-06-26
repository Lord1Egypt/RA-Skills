#!/usr/bin/env python3
"""
WeChat Article Reader - Read articles from mp.weixin.qq.com
Usage: python3 read_weixin_article.py <url>
"""

import sys
import os
import re

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 not installed. Run: pip3 install beautifulsoup4")
    sys.exit(1)

def read_weixin_article(url):
    """Read a WeChat article and return clean text content."""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    
    # Use curl to fetch the page
    cmd = f'curl -s -L --max-time 20'
    for key, value in headers.items():
        cmd += f' -H "{key}: {value}"'
    cmd += f' "{url}"'
    
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        return f"Error fetching URL: {result.stderr}"
    
    html = result.stdout
    
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script and style elements
    for tag in soup(['script', 'style']):
        tag.decompose()
    
    # Try to find the article content
    # Method 1: Look for id="js_content" (new WeChat format)
    article = soup.find('div', id='js_content')
    
    if not article:
        # Method 2: Look for class="rich_media_content"
        article = soup.find('div', class_='rich_media_content')
    
    if not article:
        # Method 3: Look for any common article content areas
        article = soup.find('div', class_=re.compile(r'.*article.*', re.I))
    
    if not article:
        # Method 4: Try to get the title and meta description
        title = soup.find('meta', property='og:title')
        desc = soup.find('meta', property='og:description')
        if title and desc:
            return f"标题: {title.get('content', 'N/A')}\n\n摘要: {desc.get('content', 'N/A')}\n\n(无法提取完整内容)"
    
    # Get text content
    text = article.get_text(separator='\n', strip=True)
    
    # Clean up excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Also try to get the title
    title_tag = soup.find('meta', property='og:title')
    title = title_tag.get('content', '') if title_tag else ''
    
    return f"# {title}\n\n{text}" if title else text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 read_weixin_article.py <wechat-article-url>")
        sys.exit(1)
    
    url = sys.argv[1]
    content = read_weixin_article(url)
    print(content)