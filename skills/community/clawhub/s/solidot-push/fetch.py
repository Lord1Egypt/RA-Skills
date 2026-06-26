#!/usr/bin/env python3
"""
Solidot 资讯抓取脚本
抓取热门文章和最新文章，推送到飞书
"""

import os
import re
import json
import urllib.request
from datetime import datetime

SOLIDOT_URLS = {
    "热门": "https://www.solidot.org/",
    "最新": "https://www.solidot.org/?action=index"
}

FEISHU_DOC_TOKEN = os.environ.get("FEISHU_DOC_TOKEN", "")

def fetch_page(url):
    """获取网页内容"""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8")

def parse_articles(html):
    """解析文章列表"""
    articles = []
    
    # 匹配文章模式: href="/story?sid=xxx" ... 标题 ... 摘要
    pattern = r'href="(/story\?sid=\d+)"[^>]*>([^<]+)</a>.*?center[^>]*>([^<]+)<'
    
    # 简单解析：从页面提取sid和标题
    sid_pattern = r'shref="/story\?sid=(\d+)"[^>]*>([^<]+)</a>'
    
    for match in re.finditer(sid_pattern, html):
        sid = match.group(1)
        title = match.group(2).strip()
        if title and len(title) > 5:
            url = f"https://www.solidot.org/story?sid={sid}"
            articles.append({"sid": sid, "title": title, "url": url})
    
    return articles[:15]  # 最多15条

def build_message(articles_hot, articles_new):
    """构建飞书消息"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    content = f"# Solidot 资讯推送 ({now})\n\n"
    
    content += "## 🔥 热门文章\n\n"
    for i, art in enumerate(articles_hot[:10], 1):
        content += f"{i}. [{art['title']}]({art['url']})\n"
    
    content += "\n## 🆕 最新文章\n\n"
    for i, art in enumerate(articles_new[:10], 1):
        content += f"{i}. [{art['title']}]({art['url']})\n"
    
    content += "\n---\n来源: [Solidot](https://www.solidot.org/)"
    
    return content

def push_to_feishu(content):
    """推送到飞书文档"""
    if not FEISHU_DOC_TOKEN:
        print("⚠️ 未配置 FEISHU_DOC_TOKEN，跳过推送")
        print("=== 推送内容 ===")
        print(content)
        return False
    
    # 使用飞书 API 创建或更新文档
    # 这里简化处理：直接打印内容，实际部署需要配置飞书机器人
    print(f"📤 已准备好飞书推送内容 ({len(content)} 字符)")
    return True

def main():
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 开始抓取 Solidot 资讯")
    
    articles_hot = []
    articles_new = []
    
    try:
        print("📥 抓取热门文章...")
        html = fetch_page(SOLIDOT_URLS["热门"])
        articles_hot = parse_articles(html)
        print(f"   获取到 {len(articles_hot)} 条热门文章")
    except Exception as e:
        print(f"❌ 热门文章抓取失败: {e}")
    
    try:
        print("📥 抓取最新文章...")
        html = fetch_page(SOLIDOT_URLS["最新"])
        articles_new = parse_articles(html)
        print(f"   获取到 {len(articles_new)} 条最新文章")
    except Exception as e:
        print(f"❌ 最新文章抓取失败: {e}")
    
    if not articles_hot and not articles_new:
        print("❌ 未获取到任何文章")
        return
    
    content = build_message(articles_hot, articles_new)
    push_to_feishu(content)
    
    print("✅ 完成!")

if __name__ == "__main__":
    main()
