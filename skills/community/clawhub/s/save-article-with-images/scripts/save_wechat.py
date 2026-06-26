#!/usr/bin/env python3
"""
Save WeChat article with images - using save-article-with-images skill workflow
"""

import os
import re
import json
import base64
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

def download_image(url, save_path):
    """Download image with proper headers"""
    headers = {
        'Referer': 'https://mp.weixin.qq.com/',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        print(f"❌ HTTP {response.status_code}: {url}")
        return False
    except Exception as e:
        print(f"❌ {e}: {url}")
        return False

def main():
    url = 'https://mp.weixin.qq.com/s/M8_oqIdYQGjsl2sF38c_wQ?scene=334'
    
    # Step 1: Fetch article
    print("📥 获取文章内容...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.0',
        'Referer': 'https://mp.weixin.qq.com/'
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = 'utf-8'
    
    if response.status_code != 200:
        print(f"❌ 请求失败：{response.status_code}")
        return
    
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract metadata
    title_elem = soup.find('h1', class_='rich_media_title') or soup.find('title')
    title = title_elem.get_text(strip=True) if title_elem else '无标题'
    title = re.sub(r'[\\/:*?"<>|]', '_', title)[:50]
    
    author_elem = soup.find('span', class_='rich_media_meta_nickname')
    author = author_elem.get_text(strip=True) if author_elem else '未知'
    
    time_elem = soup.find('em', class_='rich_media_meta_text')
    publish_time = time_elem.get_text(strip=True) if time_elem else datetime.now().strftime('%Y-%m-%d')
    
    content_div = soup.find('div', id='js_content')
    if not content_div:
        print("❌ 无法找到文章内容")
        return
    
    print(f"✅ 标题：{title}")
    print(f"✅ 作者：{author}")
    
    # Step 2: Create directory
    date_str = datetime.now().strftime('%Y%m%d')
    article_dir = Path(f'/home/admin/.openclaw/workspace/reports/{date_str}-{title}')
    images_dir = article_dir / 'images'
    article_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(exist_ok=True)
    
    print(f"📁 目录：{article_dir}")
    
    # Step 3: Extract and download images
    print("\n🖼️  下载图片...")
    img_tags = content_div.find_all('img', class_='rich_pages')
    
    image_map = {}
    for i, img in enumerate(img_tags, 1):
        img_url = img.get('data-src') or img.get('src')
        if img_url and img_url.startswith('http'):
            img_url = img_url.replace('&amp;', '&')
            
            # Get extension
            ext = Path(img_url.split('?')[0]).suffix or '.jpg'
            if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                ext = '.jpg'
            
            img_name = f'image_{i:03d}{ext}'
            img_path = images_dir / img_name
            
            if download_image(img_url, img_path):
                image_map[img_url] = f'images/{img_name}'
                print(f"  ✅ {img_name}")
            else:
                print(f"  ❌ {img_name}")
    
    # Step 4: Generate Markdown
    print("\n📝 生成 Markdown...")
    
    # Get text content
    text_content = content_div.get_text('\n', strip=True)
    
    # Build markdown
    md_content = f"""# {title}

> 来源：{url}
> 作者：{author}
> 发布时间：{publish_time}

---

"""
    
    # Add images references
    for i, (orig_url, local_path) in enumerate(image_map.items(), 1):
        md_content += f"![图片 {i}]({local_path})\n\n"
    
    md_content += f"---\n\n{text_content}\n\n"
    md_content += f"---\n\n*保存时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    md_path = article_dir / f'{title}.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✅ Markdown: {md_path}")
    
    # Step 5: Generate HTML with CSS for PDF
    print("\n📄 生成 HTML...")
    
    # Replace image URLs with local paths in HTML
    content_html = str(content_div)
    for orig_url, local_path in image_map.items():
        content_html = content_html.replace(f'data-src="{orig_url}"', f'src="{local_path}"')
        content_html = content_html.replace(f'data-src="{orig_url.replace("&", "&amp;")}"', f'src="{local_path}"')
        content_html = content_html.replace(f'src="{orig_url}"', f'src="{local_path}"')
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 100%;
            padding: 1cm;
        }}
        .header {{
            text-align: center;
            padding: 30px 0;
            border-bottom: 2px solid #eaeaea;
            margin-bottom: 30px;
        }}
        .title {{
            font-size: 24px;
            font-weight: bold;
            color: #1a1a1a;
            margin-bottom: 15px;
        }}
        .meta {{
            font-size: 14px;
            color: #888;
        }}
        .content {{
            font-size: 16pt;
            line-height: 1.8;
        }}
        .content p {{
            margin-bottom: 24px;
            text-align: justify;
        }}
        .content h1 {{
            font-size: 20px;
            font-weight: 600;
            color: #cf5148;
            margin: 30px 0 15px 0;
            text-align: center;
        }}
        /* Prevent image overflow - CRITICAL */
        img {{
            max-width: 90%;
            height: auto;
            display: block;
            margin: 1em auto;
        }}
        img[src^="images/"] {{
            max-width: 90%;
        }}
        .footer {{
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #eaeaea;
            text-align: center;
            font-size: 14px;
            color: #888;
        }}
        @media print {{
            body {{ padding: 1cm; }}
            img {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1 class="title">{title}</h1>
        <div class="meta">
            <span>{author}</span> · {publish_time}
        </div>
    </div>
    <div class="content">
        {content_html}
    </div>
    <div class="footer">
        <p>原文：{url}</p>
        <p>保存时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>'''
    
    html_path = article_dir / f'{title}.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML: {html_path}")
    
    # Save metadata
    meta = {
        'title': title,
        'author': author,
        'publish_time': publish_time,
        'url': url,
        'images_downloaded': len(image_map),
        'directory': str(article_dir)
    }
    meta_path = article_dir / 'meta.json'
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 完成!")
    print(f"   图片数：{len(image_map)}")
    print(f"   目录：{article_dir}")
    print(f"\n下一步：用 browser 打开 HTML 生成 PDF")

if __name__ == '__main__':
    main()
