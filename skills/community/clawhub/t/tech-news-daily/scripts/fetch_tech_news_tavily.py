#!/usr/bin/env python3
"""
Fetch top 10 trending tech news using Tavily Search API.
Focus on AI/LLM topics.

Requires TAVILY_API_KEY environment variable.
"""

import os
import sys
import json
import urllib.request
import urllib.error
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
        "search_depth": "advanced",  # or "basic"
        "include_answer": False,
        "include_raw_content": False,
        "max_results": max_results,
        "include_domains": [],  # No domain restrictions
        "exclude_domains": [],  # No domain exclusions
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
        print(f"Tavily API Error: {e.code} - {e.reason}", file=sys.stderr)
        return []
    except urllib.error.URLError as e:
        print(f"Network Error: {e.reason}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        return []

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

def format_news_results(results: list) -> str:
    """Format search results into readable news summary."""
    if not results:
        return "📰 今日科技资讯\n\n暂无相关新闻结果\n\n💡 请确保已配置 TAVILY_API_KEY 环境变量"
    
    output = []
    output.append("📰 今日科技资讯 Top 10")
    output.append(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output.append("=" * 50)
    
    for i, item in enumerate(results[:10], 1):
        title = item.get("title", "无标题")
        url = item.get("url", "")
        snippet = item.get("content", item.get("snippet", ""))[:150]
        
        output.append(f"\n{i}. {title}")
        if snippet:
            output.append(f"   {snippet}...")
        output.append(f"   🔗 {url}")
    
    output.append("\n" + "=" * 50)
    output.append("💡 如需深入了解某条新闻，可以让我详细搜索")
    
    return "\n".join(output)

def main():
    """Main entry point."""
    if not TAVILY_API_KEY:
        print(json.dumps({
            "error": "TAVILY_API_KEY not set",
            "instructions": "Please set TAVILY_API_KEY environment variable"
        }))
        return
    
    all_results = []
    
    # Search with multiple queries to get comprehensive results
    for query in SEARCH_QUERIES:
        results = tavily_search(query, max_results=5)
        all_results.extend(results)
    
    # Deduplicate
    unique_results = deduplicate_results(all_results)
    
    # Sort by relevance (Tavily already returns sorted results, but we can boost AI-related)
    ai_keywords = ["AI", "大模型", "LLM", "GPT", "Claude", "Gemini", "OpenAI", "Anthropic"]
    
    def ai_score(result):
        title = result.get("title", "").lower()
        content = result.get("content", "").lower()
        score = sum(1 for kw in ai_keywords if kw.lower() in title or kw.lower() in content)
        return score
    
    # Boost AI-related results
    unique_results.sort(key=ai_score, reverse=True)
    
    # Output formatted results
    formatted = format_news_results(unique_results)
    print(formatted)
    
    # Also output JSON for programmatic use
    print("\n---JSON_START---")
    print(json.dumps({
        "total_results": len(unique_results),
        "top_10": unique_results[:10],
        "timestamp": datetime.now().isoformat()
    }, ensure_ascii=False))
    print("---JSON_END---")

if __name__ == "__main__":
    main()
