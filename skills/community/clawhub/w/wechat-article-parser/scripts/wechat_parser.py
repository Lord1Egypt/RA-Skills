#!/usr/bin/env python3
"""
微信公众号文章解析器
解析 mp.weixin.qq.com 文章内容并提取主要信息
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime


def parse_wechat_article(url):
    """
    解析微信公众号文章
    
    Args:
        url: 公众号文章链接
        
    Returns:
        dict: 包含标题、作者、发布时间、内容等信息
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取标题
        title_tag = soup.find('h1', class_='rich_media_title')
        title = title_tag.get_text(strip=True) if title_tag else "未找到标题"
        
        # 提取作者
        author_tag = soup.find('a', class_='rich_media_meta rich_media_meta_link rich_media_meta_nickname')
        if not author_tag:
            author_tag = soup.find('span', class_='rich_media_meta rich_media_meta_text')
        author = author_tag.get_text(strip=True) if author_tag else "未知作者"
        
        # 提取发布时间
        time_tag = soup.find('span', class_='rich_media_meta rich_media_meta_text')
        if time_tag and time_tag.get('id') == 'publish_time':
            publish_time = time_tag.get_text(strip=True)
        else:
            # 尝试从脚本中提取
            time_match = re.search(r'var\s+publish_time\s*=\s*"([^"]+)"', response.text)
            publish_time = time_match.group(1) if time_match else "未知时间"
        
        # 提取正文内容
        content_div = soup.find('div', class_='rich_media_content')
        if content_div:
            # 移除所有脚本和样式
            for script in content_div(['script', 'style']):
                script.decompose()
            
            # 提取文本，保留段落结构
            paragraphs = []
            for p in content_div.find_all(['p', 'section']):
                text = p.get_text(strip=True)
                if text and len(text) > 10:  # 过滤掉太短的段落
                    paragraphs.append(text)
            
            content = '\n\n'.join(paragraphs)
        else:
            content = "未找到正文内容"
        
        # 提取图片
        images = []
        if content_div:
            for img in content_div.find_all('img'):
                img_url = img.get('data-src') or img.get('src')
                if img_url:
                    images.append(img_url)
        
        result = {
            'title': title,
            'author': author,
            'publish_time': publish_time,
            'content': content,
            'word_count': len(content),
            'images_count': len(images),
            'images': images[:5],  # 只保留前5张图片URL
            'url': url,
            'parsed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'url': url
        }


def print_article(article):
    """格式化打印文章信息"""
    if 'error' in article:
        print(f"❌ 解析失败: {article['error']}")
        return
    
    print("=" * 80)
    print(f"📰 标题: {article['title']}")
    print(f"✍️  作者: {article['author']}")
    print(f"🕐 发布时间: {article['publish_time']}")
    print(f"📊 字数: {article['word_count']}")
    print(f"🖼️  图片数: {article['images_count']}")
    print("=" * 80)
    print("\n📝 正文内容:\n")
    print(article['content'][:1000] + "..." if len(article['content']) > 1000 else article['content'])
    print("\n" + "=" * 80)


def save_to_file(article, filename=None):
    """保存文章到文件"""
    if 'error' in article:
        print(f"❌ 无法保存，解析失败: {article['error']}")
        return
    
    if not filename:
        # 使用标题作为文件名
        safe_title = re.sub(r'[^\w\s-]', '', article['title']).strip()[:50]
        filename = f"{safe_title}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已保存到: {filename}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 wechat_parser.py <公众号文章URL> [--save] [--output 文件名]")
        print("示例: python3 wechat_parser.py 'https://mp.weixin.qq.com/s/xxx' --save")
        sys.exit(1)
    
    url = sys.argv[1]
    save_flag = '--save' in sys.argv
    
    output_file = None
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]
    
    print("🔄 正在解析文章...")
    article = parse_wechat_article(url)
    print_article(article)
    
    if save_flag:
        save_to_file(article, output_file)
