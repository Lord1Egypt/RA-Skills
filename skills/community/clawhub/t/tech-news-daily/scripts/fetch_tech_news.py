#!/usr/bin/env python3
"""
Fetch top 10 trending tech news, focusing on AI/LLM topics.
Requires BRAVE_API_KEY environment variable or OpenClaw web_search tool.
"""

import json
import sys
from datetime import datetime

# Search queries for tech news
QUERIES = [
    "AI 大模型 最新进展 2026",
    "人工智能 科技新闻 今日热点",
    "LLM GPT 大模型  breakthrough",
    "科技资讯 AI 机器学习 深度学习",
    "OpenAI Anthropic Google AI 最新动态",
]

def format_news_results(results: list) -> str:
    """Format search results into readable news summary."""
    if not results:
        return "暂无相关新闻结果"
    
    output = []
    output.append(f"📰 今日科技资讯 Top 10")
    output.append(f"更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output.append("=" * 50)
    
    for i, item in enumerate(results[:10], 1):
        title = item.get('title', '无标题')
        url = item.get('url', '')
        snippet = item.get('snippet', '')[:150]  # Limit snippet length
        
        output.append(f"\n{i}. {title}")
        output.append(f"   {snippet}...")
        output.append(f"   🔗 {url}")
    
    output.append("\n" + "=" * 50)
    output.append("💡 提示：配置 Brave API 后可获取实时新闻")
    
    return "\n".join(output)

def main():
    """Main entry point."""
    # This script is designed to be called from OpenClaw's web_search tool
    # The actual search is performed by the agent, not this script
    print(json.dumps({
        "queries": QUERIES,
        "count": 10,
        "freshness": "pd",  # Past day
        "instructions": "Use web_search tool with these queries, then format results"
    }))

if __name__ == "__main__":
    main()
