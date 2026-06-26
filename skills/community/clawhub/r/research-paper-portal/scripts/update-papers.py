#!/usr/bin/env python3
"""
从 OpenAlex 和 arXiv 收集最新论文

配置要求:
- OPENALEX_EMAIL: 用于 API 认证（可选，提高限额）
- 关键词列表: 在脚本中配置

输出:
- pending-papers.json: 待发布论文队列
"""

import json
import requests
import time
import os
from datetime import datetime, timedelta

# ============ 配置区域 ============
KEYWORDS = ["thermoelectric", "heat pipe", "geothermal"]  # 修改为你的研究关键词
OUTPUT_FILE = "pending-papers.json"
MAX_PAPERS = 20  # 每次收集的最大论文数
# ==================================

OPENALEX_BASE = "https://api.openalex.org"
ARXIV_BASE = "http://export.arxiv.org/api/query"

def search_openalex(keywords, max_results=10):
    """从 OpenAlex 搜索论文"""
    papers = []
    email = os.environ.get("OPENALEX_EMAIL", "")
    headers = {"User-Agent": f"mailto:{email}"} if email else {}
    
    for kw in keywords:
        try:
            # 搜索最近 30 天的论文
            from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            url = f"{OPENALEX_BASE}/works?search={kw}&filter=from_publication_date:{from_date}&sort=cited_by_count:desc&per_page={max_results}"
            
            resp = requests.get(url, headers=headers, timeout=30)
            data = resp.json()
            
            for work in data.get("results", []):
                paper = {
                    "id": work.get("id", "").split("/")[-1],
                    "title": work.get("title", ""),
                    "doi": work.get("doi", ""),
                    "url": work.get("id", "") if not work.get("doi") else f"https://doi.org/{work.get('doi', '')}",
                    "source": work.get("primary_location", {}).get("source", {}).get("display_name", "Unknown"),
                    "authors": ", ".join([a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])[:3]]),
                    "pubDate": work.get("publication_date", ""),
                    "citedBy": work.get("cited_by_count", 0),
                    "excerpt": work.get("abstract", "") or "暂无摘要",
                    "tags": keywords,
                    "bgImage": "",
                    "chineseTitle": "",
                    "overview": ""
                }
                papers.append(paper)
            
            time.sleep(1)  # 避免请求过快
            
        except Exception as e:
            print(f"OpenAlex 搜索 '{kw}' 失败: {e}")
    
    return papers

def search_arxiv(keywords, max_results=10):
    """从 arXiv 搜索论文"""
    papers = []
    
    for kw in keywords:
        try:
            query = f"all:{kw}"
            url = f"{ARXIV_BASE}?search_query={query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
            
            resp = requests.get(url, timeout=30)
            # 简单解析 arXiv XML 响应
            # 实际使用建议用 feedparser 库
            
            time.sleep(3)  # arXiv 要求每 3 秒一次请求
            
        except Exception as e:
            print(f"arXiv 搜索 '{kw}' 失败: {e}")
    
    return papers

def translate_with_llm(paper, llm_command="gemini -p"):
    """使用 LLM 翻译标题和生成概述"""
    import subprocess
    
    prompt = f"""请为以下论文生成中文标题和研究概述：

英文标题：{paper['title']}
摘要：{paper['excerpt'][:500]}

请输出：
1. 中文标题（简洁，不超过30字）
2. 研究概述（一句话说明研究内容和意义，不超过50字）

格式：
标题：xxx
概述：xxx"""

    try:
        result = subprocess.run(
            f'{llm_command} "{prompt}"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout
        # 解析输出
        lines = output.strip().split("\n")
        for line in lines:
            if line.startswith("标题："):
                paper["chineseTitle"] = line.replace("标题：", "").strip()
            elif line.startswith("概述："):
                paper["overview"] = line.replace("概述：", "").strip()
                
    except Exception as e:
        print(f"翻译失败: {e}")
        paper["chineseTitle"] = paper["title"][:50]
        paper["overview"] = paper["excerpt"][:50]

def main():
    print("=" * 50)
    print(" 论文收集脚本")
    print("=" * 50)
    print(f"关键词: {KEYWORDS}")
    print()
    
    # 收集论文
    print("正在从 OpenAlex 收集论文...")
    papers = search_openalex(KEYWORDS, MAX_PAPERS // 2)
    
    print(f"收集到 {len(papers)} 篇论文")
    
    # 翻译标题和生成概述
    print("\n正在翻译论文标题...")
    for i, paper in enumerate(papers[:10]):  # 只翻译前 10 篇
        print(f"  [{i+1}/{min(10, len(papers))}] {paper['title'][:40]}...")
        translate_with_llm(paper)
        time.sleep(2)
    
    # 去重
    seen = set()
    unique_papers = []
    for p in papers:
        if p["title"] not in seen:
            seen.add(p["title"])
            unique_papers.append(p)
    
    # 保存到队列
    output = {
        "updateTime": datetime.now().isoformat(),
        "papers": unique_papers[:MAX_PAPERS]
    }
    
    # 如果已有队列，合并
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
            existing_ids = {p["id"] for p in existing.get("papers", [])}
            new_papers = [p for p in unique_papers if p["id"] not in existing_ids]
            output["papers"] = existing.get("papers", []) + new_papers
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n保存 {len(output['papers'])} 篇论文到 {OUTPUT_FILE}")
    print("=" * 50)

if __name__ == "__main__":
    main()
