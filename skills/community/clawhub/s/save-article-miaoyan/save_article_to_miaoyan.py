#!/usr/bin/env python3
"""
save_article_to_miaoyan.py — 任意网页文章自动保存到 Miaoyan
用法: python3 save_article_to_miaoyan.py <url>

支持:
- 微信公众号文章
- 个人博客/技术博客
- Medium、Substack
- GitHub 文档
- 知乎、掘金等平台
- 任意可访问的网页

流程:
1. 抓取文章内容 (支持多种抓取方式)
2. 提取标题、正文
3. 生成要点总结
4. 写 md 文件到 iCloud Miaoyan/待学习
"""

import subprocess
import re
import os
import sys
import json
from datetime import datetime
from urllib.parse import urlparse, unquote

# 配置
MIAOYAN_DIR = "/Users/andy/Library/Mobile Documents/iCloud~com~tw93~miaoyan/Documents/待学习"

# Tavily API (备用抓取) - 从环境变量读取
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY', '')

def detect_site_type(url: str) -> str:
    """检测网站类型"""
    domain = urlparse(url).netloc.lower()
    
    if 'mp.weixin.qq.com' in domain:
        return 'wechat'
    elif 'medium.com' in domain:
        return 'medium'
    elif 'substack.com' in domain:
        return 'substack'
    elif 'github.com' in domain or 'github.io' in domain:
        return 'github'
    elif 'zhihu.com' in domain:
        return 'zhihu'
    elif 'juejin.cn' in domain:
        return 'juejin'
    elif 'sspai.com' in domain:
        return 'sspai'
    else:
        return 'generic'


def fetch_with_curl(url: str) -> str:
    """使用 curl 直接抓取"""
    cmd = [
        "curl", "-s", "-L", "--max-time", "20",
        "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "-H", "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8",
        url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"curl failed: {result.stderr}")
    
    return result.stdout


def fetch_with_jina(url: str) -> str:
    """使用 Jina AI Reader 抓取（返回 Markdown）"""
    jina_url = f"https://r.jina.ai/http://{url}"
    
    cmd = [
        "curl", "-s", "-L", "--max-time", "30",
        "-H", "User-Agent: Mozilla/5.0",
        jina_url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Jina fetch failed: {result.stderr}")
    
    return result.stdout


def fetch_with_tavily(url: str) -> str:
    """使用 Tavily Extract API 抓取"""
    api_url = "https://api.tavily.com/extract"
    
    payload = {
        "api_key": TAVILY_API_KEY,
        "urls": [url]
    }
    
    cmd = [
        "curl", "-s", "-X", "POST", api_url,
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Tavily fetch failed: {result.stderr}")
    
    try:
        data = json.loads(result.stdout)
        if data.get('results') and len(data['results']) > 0:
            return data['results'][0].get('raw_content', '')
        else:
            raise Exception(f"Tavily no results: {data}")
    except json.JSONDecodeError:
        raise Exception(f"Tavily invalid JSON: {result.stdout[:200]}")


def fetch_article(url: str) -> dict:
    """抓取文章内容，尝试多种方式"""
    site_type = detect_site_type(url)
    
    # 尝试顺序：Jina -> curl -> Tavily
    html = None
    method = None
    
    # 1. Jina Reader（最适合博客/技术文章，直接返回 Markdown）
    try:
        html = fetch_with_jina(url)
        if html and len(html) > 100:
            method = 'jina'
            print(f"✅ 使用 Jina Reader 抓取成功")
    except Exception as e:
        print(f"⚠️ Jina 抓取失败: {e}")
    
    # 2. 直接 curl（微信等需要）
    if not html or len(html) < 100:
        try:
            html = fetch_with_curl(url)
            if html and len(html) > 100:
                method = 'curl'
                print(f"✅ 使用 curl 抓取成功")
        except Exception as e:
            print(f"⚠️ curl 抓取失败: {e}")
    
    # 3. Tavily（最后的备选）
    if not html or len(html) < 100:
        try:
            html = fetch_with_tavily(url)
            if html and len(html) > 100:
                method = 'tavily'
                print(f"✅ 使用 Tavily 抓取成功")
        except Exception as e:
            print(f"⚠️ Tavily 抓取失败: {e}")
    
    if not html or len(html) < 100:
        raise Exception("所有抓取方式都失败了")
    
    # 解析内容
    if method == 'jina':
        # Jina 返回的是 Markdown，直接解析
        return parse_jina_markdown(html, url)
    else:
        # HTML 需要提取
        return parse_html(html, url, site_type)


def parse_jina_markdown(content: str, url: str) -> dict:
    """解析 Jina Reader 返回的 Markdown"""
    lines = content.split('\n')
    
    # Jina Reader 格式：
    # Title: 文章标题
    # URL Source: ...
    # Published Time: ...
    # 
    # Markdown Content:
    # #### Categories: ...
    # ## 0. 太长不读
    # 正文...
    
    # 从 Title: 元数据提取标题
    title = "未命名文章"
    title_from_meta = None
    body_start_idx = 0
    
    for i, line in enumerate(lines):
        if line.startswith('Title:'):
            title_from_meta = line[6:].strip()
            # 清理可能的引号
            title_from_meta = title_from_meta.strip('"\'')
        elif line.startswith('Markdown Content:'):
            body_start_idx = i + 1
            break
    
    # 使用元数据中的标题
    if title_from_meta:
        title = title_from_meta
    
    # 提取正文（从 Markdown Content: 之后开始）
    body_lines = lines[body_start_idx:]
    
    # 清理内容
    clean_lines = []
    for line in body_lines:
        # 清理图片链接中的 oss-process 参数
        line = re.sub(r'\?x-oss-process[^\)]+', '', line)
        clean_lines.append(line)
    
    body = '\n'.join(clean_lines).strip()
    
    # 生成摘要
    summary = generate_summary(body, title)
    
    return {
        "title": title,
        "content": body,
        "summary": summary,
        "url": url,
        "date": datetime.now().strftime("%Y-%m-%d")
    }


def parse_html(html: str, url: str, site_type: str) -> dict:
    """解析 HTML 内容"""
    # 提取标题
    title = extract_title(html, site_type)
    
    # 提取正文
    content = extract_content(html, site_type)
    
    # 清理内容
    content = clean_html(content)
    
    # 生成摘要
    summary = generate_summary(content, title)
    
    return {
        "title": title,
        "content": content,
        "summary": summary,
        "url": url,
        "date": datetime.now().strftime("%Y-%m-%d")
    }


def extract_title(html: str, site_type: str) -> str:
    """提取标题"""
    # 通用方法：先找 og:title
    title_match = re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']', html)
    if title_match:
        return title_match.group(1).strip()
    
    # 再找 <title>
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
    if title_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        # 清理常见的后缀
        title = re.sub(r'\s*[-|·]\s*.*$', '', title)
        return title
    
    return "未命名文章"


def extract_content(html: str, site_type: str) -> str:
    """提取正文内容"""
    content = ""
    
    if site_type == 'wechat':
        # 微信公众号
        content_match = re.search(r'<div[^>]*class="rich_media_content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*<script', html, re.DOTALL)
        if content_match:
            content = content_match.group(1)
        else:
            content_match = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>', html, re.DOTALL)
            content = content_match.group(1) if content_match else ""
    
    elif site_type == 'zhihu':
        # 知乎
        content_match = re.search(r'<div[^>]*class="Post-RichText[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
        if content_match:
            content = content_match.group(1)
        else:
            content_match = re.search(r'<div[^>]*class="RichText[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
            content = content_match.group(1) if content_match else ""
    
    elif site_type == 'juejin':
        # 掘金
        content_match = re.search(r'<div[^>]*class="article-content[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
        content = content_match.group(1) if content_match else ""
    
    elif site_type == 'sspai':
        # 少数派
        content_match = re.search(r'<div[^>]*class="content[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
        content = content_match.group(1) if content_match else ""
    
    else:
        # 通用方法：找 article 标签或 main 标签
        content_match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
        if content_match:
            content = content_match.group(1)
        else:
            content_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
            if content_match:
                content = content_match.group(1)
            else:
                # 最后尝试找大的 div
                content_match = re.search(r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
                content = content_match.group(1) if content_match else ""
    
    return content


def clean_html(html: str) -> str:
    """清理 HTML 标签，保留段落结构"""
    # 替换代码块
    text = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'\n```\n\1\n```\n', html, flags=re.DOTALL)
    
    # 替换标题
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', text, flags=re.DOTALL)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', text, flags=re.DOTALL)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', text, flags=re.DOTALL)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n#### \1\n', text, flags=re.DOTALL)
    
    # 替换段落标签为换行
    text = re.sub(r'</p>', '\n\n', text)
    text = re.sub(r'</div>', '\n', text)
    text = re.sub(r'<br[^>]*>', '\n', text)
    
    # 替换列表
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', text, flags=re.DOTALL)
    
    # 替换链接
    text = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL)
    
    # 替换加粗和斜体
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', text, flags=re.DOTALL)
    
    # 移除所有剩余标签
    text = re.sub(r'<[^>]+>', '', text)
    
    # 解码 HTML 实体
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&#x27;', "'")
    text = text.replace('&#x2F;', '/')
    
    # 清理多余空白
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()


def generate_summary(content: str, title: str) -> str:
    """生成要点总结"""
    lines = content.split('\n')
    summary_lines = []
    
    # 找关键句（包含数字、首先、其次、总结等关键词的句子）
    keywords = ['首先', '其次', '第一', '第二', '第三', '总结', '结论', '建议', '要点', '核心', '关键', '重要', '注意', '推荐']
    
    for line in lines[:30]:  # 只看前30行
        line = line.strip()
        # 跳过标题、代码块、空行
        if not line or line.startswith('#') or line.startswith('```') or line.startswith('-'):
            continue
        if len(line) > 15 and len(line) < 150:
            if any(kw in line for kw in keywords) or re.search(r'\d+[\.、]', line):
                summary_lines.append(line)
        if len(summary_lines) >= 5:
            break
    
    # 如果没有找到关键句，取前几段
    if not summary_lines:
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('```'):
                continue
            if len(line) > 30 and len(line) < 300:
                summary_lines.append(line)
            if len(summary_lines) >= 3:
                break
    
    return '\n'.join(summary_lines) if summary_lines else content[:300] + "..."


def save_to_miaoyan(article: dict) -> str:
    """保存为 md 文件到 Miaoyan"""
    # 清理文件名
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', article['title'])[:80]
    # 去掉多余的空格和特殊字符
    safe_title = re.sub(r'\s+', '_', safe_title)
    safe_title = safe_title.strip('_')
    
    date_prefix = datetime.now().strftime("%Y%m%d")
    filename = f"{date_prefix}_{safe_title}.md"
    filepath = os.path.join(MIAOYAN_DIR, filename)
    
    # 截断过长的正文（避免文件过大）
    content = article['content']
    if len(content) > 50000:
        content = content[:50000] + "\n\n... (内容过长，已截断)"
    
    # 生成 markdown 内容
    md_content = f"""# {article['title']}

> 保存时间: {article['date']}
> 源链接: [{article['url']}]({article['url']})

## 📌 要点

{article['summary']}

---

## 正文

{content}
"""
    
    # 写入文件
    os.makedirs(MIAOYAN_DIR, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return filepath


def process_article(url: str) -> dict:
    """主流程"""
    try:
        print(f"🔄 正在处理: {url}")
        
        # 1. 抓取文章
        article = fetch_article(url)
        print(f"✅ 已获取: {article['title']}")
        
        # 2. 保存到 Miaoyan
        filepath = save_to_miaoyan(article)
        print(f"✅ 已保存: {filepath}")
        
        return {
            "success": True,
            "title": article['title'],
            "filepath": filepath,
            "summary": article['summary'][:200] + "..." if len(article['summary']) > 200 else article['summary']
        }
        
    except Exception as e:
        error_msg = f"❌ 处理失败: {str(e)}"
        print(error_msg)
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 save_article_to_miaoyan.py <article_url>")
        print("\n支持的链接类型:")
        print("  - 微信公众号文章")
        print("  - 个人博客/技术博客")
        print("  - Medium、Substack")
        print("  - GitHub 文档")
        print("  - 知乎、掘金等平台")
        print("  - 任意可访问的网页")
        sys.exit(1)
    
    url = sys.argv[1]
    result = process_article(url)
    
    if result['success']:
        print(f"\n🎉 完成: {result['title']}")
        print(f"📄 摘要: {result['summary']}")
    else:
        print(f"\n💥 失败: {result.get('error', 'Unknown error')}")
        sys.exit(1)
