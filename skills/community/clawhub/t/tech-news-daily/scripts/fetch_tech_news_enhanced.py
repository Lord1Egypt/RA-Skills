#!/usr/bin/env python3
"""
获取今日最热门的科技资讯（增强版 - 多数据源）
优先使用 Tavily API，失败时自动切换到备用方案

数据源优先级:
1. Tavily Search API (主要)
2. OpenClaw web_search 工具 (备用 1)
3. 直接抓取科技新闻网站 (备用 2)

Requires: TAVILY_API_KEY environment variable (optional, will fallback if not set)
"""

import os
import sys
import json
import urllib.request
import urllib.error
import re
from html import unescape
from datetime import datetime

# Tavily API configuration
TAVILY_API_URL = "https://api.tavily.com/search"
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")

# Search queries for tech news (优先级从高到低)
SEARCH_QUERIES = [
    "AI 大模型 最新进展 2026",
    "人工智能 科技新闻 今日热点",
    "LLM GPT Claude Gemini 最新动态",
    "OpenAI Anthropic Google DeepMind AI 新闻",
    "科技资讯 AI 机器学习 深度学习",
]

# Tech news websites for direct scraping (备用数据源)
TECH_NEWS_SITES = [
    {
        'name': '36 氪 - AI',
        'url': 'https://36kr.com/motifs/806919956817',
        'timeout': 10,
    },
    {
        'name': '机器之心',
        'url': 'https://www.jiqizhixin.com/',
        'timeout': 10,
    },
    {
        'name': '量子位',
        'url': 'https://www.qbitai.com/',
        'timeout': 10,
    },
    {
        'name': 'AI 科技大本营',
        'url': 'https://aitechtalk.com/',
        'timeout': 10,
    },
]

# HTTP 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


def tavily_search(query: str, max_results: int = 10) -> list:
    """
    Search using Tavily API.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        List of search results with title, url, snippet
    """
    if not TAVILY_API_KEY:
        return []
    
    payload = {
        "query": query,
        "search_depth": "advanced",
        "include_answer": False,
        "include_raw_content": False,
        "max_results": max_results,
        "include_domains": [],
        "exclude_domains": [],
    }
    
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        TAVILY_API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TAVILY_API_KEY}",
        },
    )
    
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("results", [])
    except urllib.error.HTTPError as e:
        print(f"[Tavily] API Error: {e.code} - {e.reason}", file=sys.stderr)
        return []
    except urllib.error.URLError as e:
        print(f"[Tavily] Network Error: {e.reason}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"[Tavily] Unexpected Error: {e}", file=sys.stderr)
        return []


def fetch_webpage(url: str, timeout: int = 10) -> str:
    """Fetch webpage content."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw_html = response.read()
            # Try to decode
            for encoding in ['utf-8', 'gb2312', 'gbk']:
                try:
                    return raw_html.decode(encoding)
                except:
                    continue
            return raw_html.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"[Fetch] Error fetching {url}: {e}", file=sys.stderr)
        return ""


def parse_36kr(html: str) -> list:
    """Parse 36 氪 AI 频道."""
    results = []
    html = unescape(html)
    
    # Match article titles and links
    pattern = r'<a[^>]*href="(https?://36kr\.com/p/\d+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html)
    
    for url, title in matches[:10]:
        if title.strip() and len(title) > 5:
            results.append({
                'title': title.strip(),
                'url': url,
                'snippet': '',
                'source': '36 氪 AI'
            })
    
    return results


def parse_jiqizhixin(html: str) -> list:
    """Parse 机器之心."""
    results = []
    html = unescape(html)
    
    # Match article titles
    pattern = r'<a[^>]*href="(/article/\d+|https?://www\.jiqizhixin\.com/article/[^"]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html)
    
    for url_path, title in matches[:10]:
        if title.strip() and len(title) > 5:
            url = url_path if url_path.startswith('http') else f'https://www.jiqizhixin.com{url_path}'
            results.append({
                'title': title.strip(),
                'url': url,
                'snippet': '',
                'source': '机器之心'
            })
    
    return results


def parse_qbitai(html: str) -> list:
    """Parse 量子位."""
    results = []
    html = unescape(html)
    
    # Match article titles
    pattern = r'<a[^>]*href="(https?://www\.qbitai\.com/[^"]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html)
    
    for url, title in matches[:10]:
        if title.strip() and len(title) > 5 and 'category' not in url:
            results.append({
                'title': title.strip(),
                'url': url,
                'snippet': '',
                'source': '量子位'
            })
    
    return results


def scrape_tech_sites() -> list:
    """Scrape tech news from multiple websites."""
    all_results = []
    
    for site in TECH_NEWS_SITES:
        print(f"[Scrape] Trying {site['name']}...", file=sys.stderr)
        html = fetch_webpage(site['url'], site['timeout'])
        
        if not html:
            print(f"[Scrape] {site['name']} failed", file=sys.stderr)
            continue
        
        # Parse based on site
        if '36kr' in site['url']:
            results = parse_36kr(html)
        elif 'jiqizhixin' in site['url']:
            results = parse_jiqizhixin(html)
        elif 'qbitai' in site['url']:
            results = parse_qbitai(html)
        else:
            results = []
        
        if results:
            print(f"[Scrape] {site['name']} got {len(results)} articles", file=sys.stderr)
            all_results.extend(results)
        else:
            print(f"[Scrape] {site['name']} no results", file=sys.stderr)
    
    return all_results


def deduplicate_results(all_results: list) -> list:
    """Remove duplicate results based on URL."""
    seen_urls = set()
    unique_results = []
    
    for result in all_results:
        url = result.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)
    
    return unique_results


def format_news_results(results: list, source_name: str = "混合数据源") -> str:
    """Format search results into readable news summary."""
    if not results:
        return "📰 今日科技资讯\n\n暂无相关新闻结果\n\n💡 请确保网络连接正常"
    
    output = []
    output.append("📰 今日科技资讯 Top 10")
    output.append(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output.append(f"数据来源：{source_name}")
    output.append("=" * 50)
    
    for i, item in enumerate(results[:10], 1):
        title = item.get("title", "无标题")
        url = item.get("url", "")
        snippet = item.get("content", item.get("snippet", item.get("summary", "")))[:150]
        source = item.get("source", "")
        
        output.append(f"\n{i}. {title}")
        if snippet:
            output.append(f"   {snippet}...")
        if source:
            output.append(f"   📍 {source}")
        output.append(f"   🔗 {url}")
    
    output.append("\n" + "=" * 50)
    output.append("💡 如需深入了解某条新闻，可以让我详细搜索")
    
    return "\n".join(output)


def fetch_news_with_tavily() -> tuple:
    """Fetch news using Tavily API."""
    print("[Tavily] Starting search...", file=sys.stderr)
    all_results = []
    
    for query in SEARCH_QUERIES:
        results = tavily_search(query, max_results=5)
        all_results.extend(results)
        print(f"[Tavily] Query '{query[:20]}...' got {len(results)} results", file=sys.stderr)
    
    unique_results = deduplicate_results(all_results)
    
    # Boost AI-related results
    ai_keywords = ["AI", "大模型", "LLM", "GPT", "Claude", "Gemini", "OpenAI", "Anthropic"]
    
    def ai_score(result):
        title = result.get("title", "").lower()
        content = result.get("content", "").lower()
        score = sum(1 for kw in ai_keywords if kw.lower() in title or kw.lower() in content)
        return score
    
    unique_results.sort(key=ai_score, reverse=True)
    
    return unique_results, "Tavily API"


def fetch_news_with_scraping() -> tuple:
    """Fetch news by scraping tech websites."""
    print("[Scrape] Starting to scrape tech sites...", file=sys.stderr)
    all_results = scrape_tech_sites()
    unique_results = deduplicate_results(all_results)
    return unique_results, "科技网站直连"


def main():
    """Main entry point - try multiple sources."""
    print("=" * 50, file=sys.stderr)
    print("科技资讯获取 (增强版 - 多数据源)", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    results = []
    source_name = ""
    
    # Try Tavily API first
    if TAVILY_API_KEY:
        results, source_name = fetch_news_with_tavily()
        if results:
            print(f"[Success] Got {len(results)} results from Tavily", file=sys.stderr)
        else:
            print("[Warn] Tavily returned no results, trying fallback...", file=sys.stderr)
    else:
        print("[Info] TAVILY_API_KEY not set, skipping Tavily...", file=sys.stderr)
    
    # Fallback to scraping if Tavily failed
    if not results:
        results, source_name = fetch_news_with_scraping()
        if results:
            print(f"[Success] Got {len(results)} results from scraping", file=sys.stderr)
        else:
            print("[Error] All sources failed", file=sys.stderr)
    
    print(file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    print(file=sys.stderr)
    
    # Output formatted results
    if results:
        formatted = format_news_results(results, source_name)
        print(formatted)
    else:
        print("❌ 暂时无法获取科技资讯")
        print()
        print("可能原因：")
        print("  1. 网络连接问题")
        print("  2. Tavily API 不可用且无法访问科技网站")
        print("  3. 所有数据源暂时不可用")
        print()
        print("建议：")
        print("  - 检查 TAVILY_API_KEY 环境变量是否设置")
        print("  - 检查网络连接")
        print("  - 稍后重试")
        sys.exit(1)
    
    # Output JSON for programmatic use
    print("\n---JSON_START---")
    print(json.dumps({
        "total_results": len(results),
        "top_10": results[:10],
        "source": source_name,
        "timestamp": datetime.now().isoformat()
    }, ensure_ascii=False))
    print("---JSON_END---")


if __name__ == "__main__":
    main()
