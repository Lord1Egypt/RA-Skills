#!/usr/bin/env python3
"""
Tavily Search Client for Rumor Buster
使用 Tavily API 进行深度英文搜索，专为事实核查设计
"""

import requests
import sys
import os

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "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")

def tavily_search(query, search_depth="advanced", include_answer=True, max_results=5):
    """
    使用 Tavily API 搜索英文内容
    
    Args:
        query: 英文搜索关键词
        search_depth: "basic" 或 "advanced" (advanced 更深入)
        include_answer: 是否包含 AI 生成的答案总结
        max_results: 返回结果数量 (1-10)
    """
    url = "https://api.tavily.com/search"
    
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": search_depth,
        "include_answer": include_answer,
        "include_images": False,
        "include_raw_content": True,
        "max_results": max_results
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def format_results(data):
    """格式化搜索结果输出"""
    output = []
    
    # AI 生成的答案总结
    if "answer" in data and data["answer"]:
        output.append("=" * 60)
        output.append("🤖 AI 总结")
        output.append("=" * 60)
        output.append(data["answer"])
        output.append("")
    
    # 搜索结果列表
    output.append("=" * 60)
    output.append("📚 搜索结果")
    output.append("=" * 60)
    
    for i, result in enumerate(data.get("results", []), 1):
        title = result.get("title", "N/A")
        url = result.get("url", "N/A")
        score = result.get("score", 0)
        content = result.get("content", "")[:200]
        
        output.append(f"\n{i}. {title}")
        output.append(f"   🔗 {url}")
        output.append(f"   ⭐ 相关度: {score:.2f}")
        output.append(f"   📝 {content}...")
    
    output.append("\n" + "=" * 60)
    output.append(f"总结果数: {len(data.get('results', []))}")
    output.append("=" * 60)
    
    return "\n".join(output)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tavily_search.py 'English search keywords'")
        print("   or: echo 'search keywords' | python3 tavily_search.py")
        sys.exit(1)
    
    # 获取搜索关键词
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = sys.stdin.read().strip()
    
    if not query:
        print("Error: 搜索关键词不能为空", file=sys.stderr)
        sys.exit(1)
    
    print(f"🔍 Tavily English Search: {query}")
    print("-" * 60)
    
    # 执行搜索
    result = tavily_search(query)
    
    if "error" in result:
        print(f"❌ 搜索失败: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    # 输出格式化结果
    print(format_results(result))

if __name__ == "__main__":
    main()
