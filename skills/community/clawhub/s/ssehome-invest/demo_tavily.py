#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tavily News Search Demo - 演示如何使用 Tavily 搜索公司相关新闻

API Key 配置: ~/.openclaw/.env 中的 TAVILY_API_KEY
"""

import os
from dotenv import load_dotenv
from tavily import TavilyClient

def get_tavily_api_key():
    """从环境变量或 .env 文件获取 API Key"""
    # 尝试加载 ~/.openclaw/.env
    env_path = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    
    api_key = os.getenv("TAVILY_API_KEY", "")
    if not api_key:
        raise ValueError(
            "⚠️ Tavily API Key 未配置！\n"
            "请在 ~/.openclaw/.env 文件中添加：\n"
            "TAVILY_API_KEY=tvly-你的 API_Key\n"
            "获取地址：https://app.tavily.com/"
        )
    return api_key

def search_company_news(stock_name, stock_symbol):
    """演示搜索公司相关新闻"""
    
    try:
        api_key = get_tavily_api_key()
        client = TavilyClient(api_key=api_key)
    except ValueError as e:
        print(e)
        return
    
    # 搜索 1: 公司动态
    print(f"\n🔍 搜索 {stock_name} ({stock_symbol}) 最新动态...")
    query1 = f"{stock_name} {stock_symbol} 股价 最新"
    result1 = client.search(query1, search_depth="advanced", max_results=3)
    
    if "results" in result1:
        print(f"\n✅ 找到 {len(result1['results'])} 条相关动态:")
        for i, item in enumerate(result1["results"], 1):
            print(f"\n{i}. {item.get('title', '无标题')}")
            print(f"   链接：{item.get('url', '')}")
            print(f"   摘要：{item.get('content', '')[:200]}...")
    
    # 搜索 2: 产品技术
    print(f"\n🔍 搜索 {stock_name} 产品和业务...")
    query2 = f"{stock_name} 主营业务 核心技术"
    result2 = client.search(query2, search_depth="basic", max_results=3)
    
    if "results" in result2:
        print(f"\n✅ 找到 {len(result2['results'])} 条相关信息:")
        for i, item in enumerate(result2["results"], 1):
            print(f"\n{i}. {item.get('title', '无标题')}")
            print(f"   链接：{item.get('url', '')}")

if __name__ == "__main__":
    print("=" * 60)
    print("Tavily 新闻搜索演示")
    print("=" * 60)
    print("\n💡 API Key 配置: ~/.openclaw/.env 中的 TAVILY_API_KEY\n")
    
    search_company_news("中铁物流", "000927")
    search_company_news("两面针", "600249")
    search_company_news("新朋股份", "002328")
