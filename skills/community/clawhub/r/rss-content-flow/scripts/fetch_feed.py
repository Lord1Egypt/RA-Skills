#!/usr/bin/env python3
"""
RSS 抓取脚本：从多个订阅源获取最新文章
用法:
  python3 fetch_feed.py --all --limit 5
  python3 fetch_feed.py --source 36氪 --limit 5
  python3 fetch_feed.py --source 36氪 --url "https://36kr.com/feed"
"""

import json
import os
import sys
import ssl
import socket
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import argparse
import re
import certifi

# 双层 SSL 上下文：macOS Python 需显式加载 certifi 根证书
# 第1层：标准验证（优先）
_SAFE_SSL_CTX = ssl.create_default_context()
_SAFE_SSL_CTX.load_verify_locations(certifi.where())

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

def load_feeds():
    """加载订阅配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def fetch_rss(url, source_name="未知", limit=5, max_age_days=7):
    """
    获取单个 RSS 源的最新文章
    返回: list of dict {title, link, description, pub_date, source}
    """
    articles = []
    xml_content = None

    # 优先使用标准 SSL 证书验证，失败自动降级
    try:
        with urlopen(url, timeout=15, context=_SAFE_SSL_CTX) as response:
            xml_content = response.read().decode("utf-8", errors="replace")
    except URLError as e:
        # SSL错误被包装在URLError.reason里
        reason = getattr(e, 'reason', None)
        if isinstance(reason, ssl.SSLError):
            fallback_ctx = ssl.create_default_context()
            fallback_ctx.load_verify_locations(certifi.where())
            try:
                with urlopen(url, timeout=15, context=fallback_ctx) as response:
                    xml_content = response.read().decode("utf-8", errors="replace")
            except Exception as e2:
                print(f"  ⚠️ 连接失败: {e2}", file=sys.stderr)
                return []
        else:
            print(f"  ⚠️ 连接失败: {e}", file=sys.stderr)
            return []
    except Exception as e:
        print(f"  ⚠️ 连接失败: {e}", file=sys.stderr)
        return []

    if xml_content is None:
        return []
    
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        print(f"  ⚠️ XML 解析错误", file=sys.stderr)
        return []
    
    # 判断 RSS 格式 (RSS 2.0 vs Atom)
    ns = {"dc": "http://purl.org/dc/elements/1.1/"}
    if root.tag == "rss":
        items = root.findall(".//item")
        date_format = "%a, %d %b %Y %H:%M:%S %z"
    elif root.tag.endswith("}feed") or root.tag == "feed":
        # Atom 格式
        items = root.findall(".//entry")
        date_format = "%Y-%m-%dT%H:%M:%S"
    else:
        items = root.findall(".//item") or root.findall(".//entry")
        date_format = "%a, %d %b %Y %H:%M:%S %z"
    
    cutoff_date = datetime.now() - timedelta(days=max_age_days)
    
    for item in items[:limit * 3]:  # 先多取一些，过滤后再截取
        title = ""
        link = ""
        description = ""
        pub_date = ""
        
        # 提取标题（兼容 RSS 和 Atom）
        title = ""
        for t in list(item):
            if t.tag in ("title", "{http://purl.org/dc/elements/1.1/}title"):
                if t.text:
                    title = t.text.strip()
                    break
        
        # 提取链接
        link = ""
        for l in list(item):
            if l.tag == "link":
                if l.text and l.text.strip() and l.text.startswith("http"):
                    link = l.text.strip()
                elif l.attrib.get("href"):
                    link = l.attrib["href"]
                break
        
        # Atom 格式的 link
        if not link:
            atom_links = item.findall("link")
            for al in atom_links:
                href = al.attrib.get("href") or (al.text if al.text else "")
                if href and "http" in str(href):
                    link = href
                    break
        
        # 提取描述
        description = ""
        for d in list(item):
            if d.tag in ("description", "summary", "content"):
                if d.text:
                    desc_text = d.text.strip()
                    # 去除 HTML 标签
                    desc_text = re.sub(r"<[^>]+>", "", desc_text)
                    desc_text = re.sub(r"&[^;]+;", "", desc_text)
                    description = desc_text[:300]
                    break
        
        # 提取日期
        pub_date = ""
        for date_elem in list(item):
            if date_elem.tag in ("pubDate", "published", "updated"):
                if date_elem.text:
                    pub_date = date_elem.text.strip()
                    break
        
        # 过滤：去除广告/太旧的
        ad_keywords = ["广告", "推广", "sponsored", "sponsor", "promoted"]
        is_ad = any(kw in title.lower() for kw in ad_keywords)
        
        # 日期过滤
        try:
            if pub_date:
                if "(" in pub_date:
                    pub_date = pub_date.split("(")[0].strip()
                article_date = datetime.strptime(pub_date[:25].strip(), date_format)
                if article_date < cutoff_date:
                    continue
        except (ValueError, TypeError):
            pass  # 日期解析失败时不过滤
        
        if not is_ad and title:
            articles.append({
                "title": title,
                "link": link,
                "description": description,
                "pub_date": pub_date[:16] if pub_date else "",
                "source": source_name
            })
        
        if len(articles) >= limit:
            break
    
    return articles

def fetch_all_feeds(limit=3, max_age_days=7):
    """获取所有订阅源的最新文章"""
    feeds = load_feeds()
    
    if not feeds:
        print("❌ 暂无订阅源，请先运行 --init 或 --add 添加订阅", file=sys.stderr)
        return []
    
    all_articles = []
    results = {}
    
    for name, url in feeds.items():
        print(f"📡 抓取 {name}...", file=sys.stderr)
        articles = fetch_rss(url, name, limit, max_age_days)
        results[name] = articles
        all_articles.extend(articles)
        if articles:
            print(f"  ✅ 获取 {len(articles)} 篇", file=sys.stderr)
        else:
            print(f"  ⚠️ 无新文章或抓取失败", file=sys.stderr)
    
    # 按日期排序
    return all_articles

def print_summary(all_articles):
    """打印内容摘要"""
    if not all_articles:
        print("\n📭 所有订阅源均无新文章（7天内）")
        return
    
    print(f"\n{'='*50}")
    print(f"📬 今日内容速览（共 {len(all_articles)} 篇）")
    print(f"{'='*50}\n")
    
    # 按来源分组
    from collections import defaultdict
    by_source = defaultdict(list)
    for a in all_articles:
        by_source[a["source"]].append(a)
    
    for source, articles in by_source.items():
        print(f"📰 {source} | {len(articles)} 篇新文章")
        for i, a in enumerate(articles, 1):
            print(f"  {i}. {a['title']}")
            if a["description"]:
                desc = a["description"][:80]
                print(f"     {desc}...")
            if a["pub_date"]:
                print(f"     📅 {a['pub_date']}")
            print()
    
    print("-" * 50)
    print("💡 使用「生成知乎内容」或「改写成小红书」来制作发布内容")

def main():
    parser = argparse.ArgumentParser(description="RSS 内容抓取")
    parser.add_argument("--all", action="store_true", help="抓取所有订阅源")
    parser.add_argument("--source", metavar="名称", help="指定订阅源名称")
    parser.add_argument("--url", metavar="URL", help="直接指定 RSS URL（不依赖配置）")
    parser.add_argument("--limit", type=int, default=3, help="每个源抓取文章数量（默认3）")
    parser.add_argument("--days", type=int, default=7, help="文章有效期天数（默认7）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--init", action="store_true", help="初始化默认订阅源")
    args = parser.parse_args()
    
    if args.init:
        from manage_feeds import init_default
        init_default()
        return
    
    # 加载订阅
    feeds = load_feeds()
    
    if args.url:
        # 直接指定 URL
        print(f"📡 抓取 {args.url}...", file=sys.stderr)
        articles = fetch_rss(args.url, args.source or "自定义", args.limit, args.days)
    elif args.source:
        # 指定源名
        if args.source not in feeds:
            print(f"❌ 未找到订阅源「{args.source}」", file=sys.stderr)
            print(f"   现有订阅：{', '.join(feeds.keys())}", file=sys.stderr)
            sys.exit(1)
        articles = fetch_rss(feeds[args.source], args.source, args.limit, args.days)
    elif args.all:
        articles = fetch_all_feeds(args.limit, args.days)
    else:
        print("❌ 请指定 --all（所有源）或 --source <名称> 或 --url <URL>", file=sys.stderr)
        sys.exit(1)
    
    if args.json:
        print(json.dumps(articles, ensure_ascii=False, indent=2))
    else:
        print_summary(articles)

if __name__ == "__main__":
    main()
