#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search Workflow - 标准化搜索工作流
"""

import os
import sys
import json
import requests
from datetime import datetime

TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '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')

def tavily_search(query, max_results=10):
    """Tavily 搜索"""
    url = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}
    data = {
        "query": query,
        "search_depth": "advanced",
        "include_answer": True,
        "max_results": max_results
    }
    response = requests.post(url, json=data, headers=headers, timeout=30)
    return response.json()

def process_results(results):
    """结果处理：去重、排序"""
    unique_urls = set()
    unique_results = []
    for r in results.get('results', []):
        if r['url'] not in unique_urls:
            unique_urls.add(r['url'])
            unique_results.append(r)
    return unique_results[:10]

def generate_report(query, results):
    """生成搜索报告"""
    report = []
    report.append(f"# 搜索结果报告\n")
    report.append(f"**查询**: {query}")
    report.append(f"**搜索时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**结果数量**: {len(results)}\n")
    
    if results and results[0].get('answer'):
        report.append(f"## 📝 搜索摘要\n")
        report.append(f"{results[0]['answer']}\n")
    
    report.append(f"## 🔍 搜索结果\n")
    for i, r in enumerate(results, 1):
        report.append(f"### {i}. {r.get('title', '无标题')}")
        report.append(f"**URL**: {r.get('url', '')}")
        if r.get('published_date'):
            report.append(f"**日期**: {r.get('published_date')}")
        report.append(f"\n{r.get('content', '')[:200]}...\n")
        report.append("---\n")
    
    return "\n".join(report)

def search_workflow(query, search_type="academic"):
    """标准化搜索工作流"""
    print(f"🔍 开始搜索：{query}")
    print(f"搜索类型：{search_type}")
    
    # 阶段 1: 查询分析
    print("\n阶段 1: 查询分析...")
    
    # 阶段 2: 搜索执行
    print("阶段 2: 搜索执行...")
    results = tavily_search(query)
    
    # 阶段 3: 结果处理
    print("阶段 3: 结果处理...")
    processed = process_results(results)
    
    # 阶段 4: 内容提取 (可选)
    if search_type == "deep":
        print("阶段 4: 内容提取...")
        # 可以调用 web_fetch
    
    # 阶段 5: 整理输出
    print("阶段 5: 整理输出...")
    report = generate_report(query, processed)
    
    # 保存结果
    filename = f"search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 搜索完成！")
    print(f"📁 结果已保存：{filename}")
    
    return report

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "测试查询"
    search_type = sys.argv[2] if len(sys.argv) > 2 else "academic"
    search_workflow(query, search_type)
