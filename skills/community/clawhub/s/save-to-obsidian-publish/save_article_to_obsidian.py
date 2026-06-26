#!/usr/bin/env python3
"""
save_article_to_obsidian.py — 网页文章自动保存到 Obsidian
用法: python3 save_article_to_obsidian.py <url1> [url2] [url3] ... ["用户笔记"]

功能:
1. 批量处理多个文章链接
2. 自动下载图片到本地
3. 自动生成结构化摘要
4. 自动提取标签
5. 去重检测
6. 失败重试

配置说明:
- 修改 OBSIDIAN_DIR 为你的 Obsidian 文章目录
- 修改 ATTACHMENTS_DIR 为你的图片附件目录
"""

import subprocess
import re
import os
import sys
import json
import hashlib
import time
from datetime import datetime
from urllib.parse import urlparse, unquote

# ==================== 用户配置区域 ====================
# 请修改以下路径为你的 Obsidian 实际路径

# 文章保存目录（相对于 vault 根目录或绝对路径）
OBSIDIAN_DIR = os.path.expanduser("~/Documents/Obsidian/articles")

# 图片附件保存目录
ATTACHMENTS_DIR = os.path.expanduser("~/Documents/Obsidian/attachments")

# 去重记录文件路径
DUPLICATE_RECORD_FILE = os.path.join(os.path.dirname(__file__), ".saved_urls.json")

# ==================== 配置结束 ====================


def load_saved_urls() -> dict:
    """加载已保存的 URL 记录"""
    if os.path.exists(DUPLICATE_RECORD_FILE):
        try:
            with open(DUPLICATE_RECORD_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_url_record(url: str, filepath: str):
    """保存 URL 记录"""
    records = load_saved_urls()
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:16]
    records[url_hash] = {
        "url": url,
        "filepath": filepath,
        "saved_at": datetime.now().isoformat()
    }
    try:
        with open(DUPLICATE_RECORD_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except:
        pass


def check_duplicate(url: str) -> tuple:
    """检查是否已保存过"""
    records = load_saved_urls()
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:16]
    
    if url_hash in records:
        existing_path = records[url_hash].get("filepath", "")
        if existing_path and os.path.exists(existing_path):
            return True, existing_path
    
    # 也检查文件名
    article_hash = get_url_hash(url)
    if os.path.exists(OBSIDIAN_DIR):
        for filename in os.listdir(OBSIDIAN_DIR):
            if article_hash in filename:
                return True, os.path.join(OBSIDIAN_DIR, filename)
    
    return False, None


def get_url_hash(url: str) -> str:
    """生成 URL 的短哈希"""
    return hashlib.md5(url.encode('utf-8')).hexdigest()[:8]


def get_file_extension(url: str) -> str:
    """从 URL 获取文件扩展名"""
    decoded = unquote(url)
    path = decoded.split('?')[0]
    ext = os.path.splitext(path)[1].lower()
    valid_exts = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg']
    if ext not in valid_exts:
        if 'wx_fmt=' in url:
            fmt_match = re.search(r'wx_fmt=(\w+)', url)
            if fmt_match:
                fmt = fmt_match.group(1).lower()
                if fmt in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                    return f'.{fmt}'
        return '.png'
    return ext


def download_image(img_url: str, article_hash: str, img_index: int) -> str:
    """下载图片到本地"""
    try:
        url_hash = get_url_hash(img_url)
        ext = get_file_extension(img_url)
        filename = f"{article_hash}_{img_index:03d}_{url_hash}{ext}"
        
        subfolder = os.path.join(ATTACHMENTS_DIR, article_hash)
        os.makedirs(subfolder, exist_ok=True)
        
        filepath = os.path.join(subfolder, filename)
        
        if os.path.exists(filepath) and os.path.getsize(filepath) > 100:
            return f"../attachments/{article_hash}/{filename}"
        
        cmd = [
            "curl", "-s", "-L", "--max-time", "30",
            "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "-H", "Referer: https://mp.weixin.qq.com/",
            "-o", filepath,
            img_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(filepath) and os.path.getsize(filepath) > 100:
            return f"../attachments/{article_hash}/{filename}"
        return img_url
            
    except Exception as e:
        return img_url


def process_images(content: str, article_url: str) -> tuple:
    """处理图片"""
    article_hash = get_url_hash(article_url)
    img_pattern = r'!\[([^\]]*)\]\((https?://[^)]+)\)'
    images = re.findall(img_pattern, content)
    
    new_content = content
    for i, (alt_text, img_url) in enumerate(images, 1):
        local_path = download_image(img_url, article_hash, i)
        old_pattern = f'![{alt_text}]({img_url})'
        new_pattern = f'![{alt_text}]({local_path})'
        new_content = new_content.replace(old_pattern, new_pattern)
    
    return new_content, article_hash


def generate_summary(content: str, title: str) -> dict:
    """精准生成结构化摘要"""
    lines = content.split('\n')
    
    # 1. 提取核心观点
    core = ""
    for line in lines:
        line = line.strip()
        if (len(line) > 100 and 
            not line.startswith('#') and 
            not line.startswith('![') and
            not line.startswith('http') and
            not line.startswith('[')):
            clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
            clean = re.sub(r'\*\*', '', clean)
            clean = re.sub(r'\*', '', clean)
            core = clean[:280]
            break
    
    if not core:
        core = "文章探讨了相关主题"
    
    # 2. 提取关键要点
    points = []
    seen = set()
    
    for line in lines:
        line = line.strip()
        point = None
        
        # bullet points
        m = re.match(r'^[-•*]\s+(.+)$', line)
        if m:
            point = m.group(1).strip()
        
        # 数字列表
        if not point:
            m = re.match(r'^\d+[.、]\s+(.+)$', line)
            if m:
                point = m.group(1).strip()
        
        if point:
            point = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', point)
            point = re.sub(r'\*\*', '', point)
            if len(point) > 40 and len(point) < 180 and point not in seen:
                points.append(point)
                seen.add(point)
        
        if len(points) >= 5:
            break
    
    # 3. 适用场景
    text = (title + " " + content[:2000]).lower()
    audience_map = [
        ("AI 研究者", ['ai', 'claude', 'gpt', 'llm', '大模型']),
        ("网络安全从业者", ['安全', '漏洞', '攻击', '黑客']),
        ("软件开发者", ['编程', '代码', '开发', 'python']),
    ]
    audience = "对该主题感兴趣的读者"
    for aud, kws in audience_map:
        if any(k in text for k in kws):
            audience = aud
            break
    
    return {"core": core, "points": points[:5], "audience": audience}


def extract_tags(title: str, content: str) -> list:
    """智能标签提取"""
    text = (title + " " + content[:3000]).lower()
    tags = []
    
    # 技术领域
    tech_keywords = {
        'llm': ['llm', '大语言模型', 'gpt-4', 'claude', 'token'],
        'agent': ['agent', '智能体', 'autonomous'],
        'ai': ['ai', '人工智能', '机器学习', '深度学习'],
        'security': ['安全', '漏洞', '攻击', '黑客', '渗透'],
        'coding': ['编程', '代码', '开发', 'python', 'javascript'],
        'architecture': ['架构', '系统设计', '微服务'],
    }
    
    for tag, kws in tech_keywords.items():
        if any(k in text for k in kws):
            tags.append(tag)
    
    # 主题类型
    type_kw = {
        'tutorial': ['教程', '指南', '入门'],
        'news': ['新闻', '发布', '最新'],
        'analysis': ['分析', '深度', '解读'],
    }
    for tag, kws in type_kw.items():
        if any(k in text for k in kws):
            tags.append(tag)
    
    # 去重
    seen = set()
    unique_tags = []
    for t in tags:
        if t not in seen:
            unique_tags.append(t)
            seen.add(t)
    
    return unique_tags[:6] if unique_tags else ['article']


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
    elif 'ithome.com' in domain:
        return 'ithome'
    else:
        return 'generic'


def is_anti_scraping(html: str) -> bool:
    """检测是否被反爬拦截"""
    signals = ['环境异常', '验证', 'captcha', 'CAPTCHA', '请完成验证', 'Access Denied', '403 Forbidden']
    return any(s in html[:3000] for s in signals)


def fetch_with_retry(url: str, max_retries: int = 3) -> str:
    """带重试的抓取，针对不同站点使用不同策略"""
    last_error = None
    site_type = detect_site_type(url)
    
    # 微信文章特殊处理：优先用微信 UA 直接抓取
    wechat_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.43"
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                print(f"    🔄 第 {attempt + 1} 次尝试...")
                time.sleep(1)
            
            # 微信文章：直接用微信 UA
            if site_type == 'wechat':
                cmd = [
                    "curl", "-s", "-L", "--max-time", "30",
                    "-H", f"User-Agent: {wechat_ua}",
                    "-H", "Accept: text/html,application/xhtml+xml",
                    "-H", "Accept-Language: zh-CN",
                    "-H", f"Referer: https://mp.weixin.qq.com/",
                    url
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0 and len(result.stdout) > 500:
                    if not is_anti_scraping(result.stdout):
                        return result.stdout
                    print("    ⚠️ 微信 UA 仍被拦截，尝试其他方式...")
            
            # 通用：尝试 Jina Reader
            try:
                jina_url = f"https://r.jina.ai/{url}"
                cmd = ["curl", "-s", "-L", "--max-time", "30", "-H", "User-Agent: Mozilla/5.0", jina_url]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0 and len(result.stdout) > 100:
                    if not is_anti_scraping(result.stdout):
                        return result.stdout
            except Exception as e:
                last_error = e
            
            # 通用：桌面浏览器 UA curl
            try:
                cmd = [
                    "curl", "-s", "-L", "--max-time", "20",
                    "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                    "-H", "Accept: text/html,application/xhtml+xml",
                    "-H", "Accept-Language: zh-CN",
                    url
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0 and len(result.stdout) > 100:
                    if not is_anti_scraping(result.stdout):
                        return result.stdout
            except Exception as e:
                last_error = e
                
        except Exception as e:
            last_error = e
    
    raise Exception(f"经过 {max_retries} 次尝试后失败: {last_error}")


def parse_jina_markdown(content: str, url: str) -> dict:
    """解析 Jina Reader 返回的 Markdown"""
    lines = content.split('\n')
    title = "未命名文章"
    body_start_idx = 0
    
    for i, line in enumerate(lines):
        if line.startswith('Title:'):
            title = line[6:].strip().strip('"\'')
        elif line.startswith('Markdown Content:'):
            body_start_idx = i + 1
            break
    
    body = '\n'.join(lines[body_start_idx:]).strip()
    
    return {"title": title, "content": body, "url": url, "date": datetime.now().strftime("%Y-%m-%d")}


def parse_html(html: str, url: str, site_type: str) -> dict:
    """解析 HTML 内容"""
    title = extract_title(html)
    content = extract_content(html, site_type)
    content = clean_html(content)
    
    return {"title": title, "content": content, "url": url, "date": datetime.now().strftime("%Y-%m-%d")}


def extract_title(html: str) -> str:
    """提取标题"""
    m = re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']', html)
    if m:
        return m.group(1).strip()
    
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL)
    if m:
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        return re.sub(r'\s*[-|·]\s*.*$', '', title)
    
    return "未命名文章"


def extract_content(html: str, site_type: str) -> str:
    """提取正文内容"""
    content = ""
    
    if site_type == 'wechat':
        m = re.search(r'<div[^>]*class="rich_media_content[^"]*"[^>]*>(.*?)</div>\s*</div>\s*<script', html, re.DOTALL)
        if m:
            content = m.group(1)
        else:
            m = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>', html, re.DOTALL)
            content = m.group(1) if m else ""
    elif site_type == 'zhihu':
        m = re.search(r'<div[^>]*class="Post-RichText[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
        if m:
            content = m.group(1)
        else:
            m = re.search(r'<div[^>]*class="RichText[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
            content = m.group(1) if m else ""
    elif site_type == 'ithome':
        m = re.search(r'<div[^>]*class="post_content[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
        content = m.group(1) if m else ""
    else:
        m = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
        if m:
            content = m.group(1)
        else:
            m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
            if m:
                content = m.group(1)
    
    return content


def clean_html(html: str) -> str:
    """清理 HTML 标签"""
    def replace_img(m):
        img = m.group(0)
        data = re.search(r'data-src="([^"]+)"', img)
        src = re.search(r'src="([^"]+)"', img)
        alt = re.search(r'alt="([^"]*)"', img)
        
        url = data.group(1) if data else (src.group(1) if src else "")
        text = alt.group(1) if alt else "图片"
        
        return f"\n![{text}]({url})\n" if url else ""
    
    text = re.sub(r'<img[^>]+>', replace_img, html)
    text = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'\n```\n\1\n```\n', text, flags=re.DOTALL)
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', text, flags=re.DOTALL)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', text, flags=re.DOTALL)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', text, flags=re.DOTALL)
    text = re.sub(r'</p>', '\n\n', text)
    text = re.sub(r'</div>', '\n', text)
    text = re.sub(r'<br[^>]*>', '\n', text)
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', text, flags=re.DOTALL)
    text = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL)
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    
    text = text.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&amp;', '&')
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&#x27;', "'")
    
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()


def clean_special_chars(text: str) -> str:
    """清理特殊字符"""
    return (text
        .replace('\u200B', '').replace('\u200C', '').replace('\u200D', '').replace('\uFEFF', '')
        .replace('\u00A0', ' ').replace('\u1680', ' ').replace('\u180E', ' ')
        .replace('\u200E', '').replace('\u200F', '')
    )


def generate_block_ref(note: str, url: str) -> str:
    """生成 block reference ID"""
    h = hashlib.md5(f"{url}|{note}".lower().encode()).hexdigest()[:8]
    return f"note-{h}"


def save_to_obsidian(article: dict, article_hash: str, summary: dict, tags: list, user_note: str = "") -> str:
    """保存为 md 文件"""
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', article['title'])[:80]
    safe_title = re.sub(r'\s+', '_', safe_title).strip('_')
    
    date_prefix = datetime.now().strftime("%Y%m%d")
    filename = f"{date_prefix}_{safe_title}.md"
    filepath = os.path.join(OBSIDIAN_DIR, filename)
    
    content = article['content']
    if len(content) > 50000:
        content = content[:50000] + "\n\n... (内容过长，已截断)"
    
    content = clean_special_chars(content)
    title = clean_special_chars(article['title'])
    
    # 标签 YAML
    tags_yaml = "tags:\n"
    for tag in tags:
        tags_yaml += f"  - {tag}\n"
    
    # 摘要
    summary_text = f"""**核心观点**: {summary['core']}

**关键要点**:
"""
    for point in summary['points']:
        summary_text += f"- {point}\n"
    
    summary_text += f"""
**适用场景**: {summary['audience']}

🔗 [阅读原文]({article['url']})
"""
    
    # 用户笔记
    note_section = ""
    if user_note:
        block_id = generate_block_ref(user_note, article['url'])
        note_section = f"""
## 💭 我的笔记

> {user_note}
^{block_id}
"""
    
    # markdown 内容
    md_content = f"""---
title: "{title}"
url: "{article['url']}"
created: {article['date']}
source: {detect_site_type(article['url'])}
{tags_yaml}---

## 📌 摘要

{summary_text}
{note_section}
---

{content}
"""
    
    os.makedirs(OBSIDIAN_DIR, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return filepath


def process_single_article(url: str, user_note: str = "") -> dict:
    """处理单篇文章"""
    # 检查重复
    is_dup, existing = check_duplicate(url)
    if is_dup:
        return {
            "success": True,
            "duplicate": True,
            "title": "已存在",
            "filepath": existing,
            "url": url,
            "message": "文章已保存过"
        }
    
    try:
        # 抓取（带重试）
        html = fetch_with_retry(url)
        
        # 解析
        if 'Title:' in html and 'Markdown Content:' in html:
            article = parse_jina_markdown(html, url)
        else:
            article = parse_html(html, url, detect_site_type(url))
        
        # 生成摘要和标签
        summary = generate_summary(article['content'], article['title'])
        tags = extract_tags(article['title'], article['content'])
        
        # 处理图片
        article['content'], article_hash = process_images(article['content'], article['url'])
        
        # 保存
        filepath = save_to_obsidian(article, article_hash, summary, tags, user_note)
        
        # 记录
        save_url_record(url, filepath)
        
        return {
            "success": True,
            "duplicate": False,
            "title": article['title'],
            "filepath": filepath,
            "url": url,
            "tags": tags,
            "summary": summary
        }
        
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "error": str(e)
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 save_article_to_obsidian.py <url1> [url2] ... [\"笔记\"]")
        sys.exit(1)
    
    # 提取 URL 和笔记
    urls = []
    user_note = ""
    for arg in sys.argv[1:]:
        if arg.startswith('http'):
            urls.append(arg)
        else:
            user_note = arg
    
    if not urls:
        print("❌ 未找到有效的 URL")
        sys.exit(1)
    
    print(f"🔄 共 {len(urls)} 篇文章需要处理\n")
    
    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}")
        result = process_single_article(url, user_note)
        results.append(result)
        
        if result['success']:
            if result.get('duplicate'):
                print(f"  ⚠️ 已存在")
            else:
                print(f"  ✅ {result['title'][:40]}...")
        else:
            print(f"  ❌ {result.get('error', '失败')}")
    
    # 汇总
    print("\n" + "="*60)
    print("📊 处理完成")
    print("="*60)
    
    success = sum(1 for r in results if r['success'])
    new_cnt = sum(1 for r in results if r['success'] and not r.get('duplicate'))
    dup_cnt = sum(1 for r in results if r.get('duplicate'))
    
    print(f"\n✅ 成功: {success}/{len(urls)} (新增: {new_cnt}, 重复: {dup_cnt})")
    
    for r in results:
        if r['success'] and not r.get('duplicate'):
            print(f"\n📄 {r['title']}")
            print(f"   🏷️ {', '.join(r['tags'])}")
            print(f"   📌 {r['summary']['core'][:60]}...")
            for p in r['summary']['points'][:2]:
                print(f"      • {p[:50]}...")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
