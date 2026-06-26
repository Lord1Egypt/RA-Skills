"""
Tech News Daily - 科技资讯自动聚合
用法：python tech-news-daily.py [date]
"""

import json
import requests
from datetime import datetime, timedelta
import os
from pathlib import Path

# 配置
DATE = os.getenv("TODAY", datetime.now().strftime("%Y-%m-%d"))
OUTPUT_DIR = Path("data/daily")
OUTPUT_FILE = OUTPUT_DIR / f"{DATE}.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 信源列表
RSS_FEEDS = {
    "机器之心": "https://www.jiqizhixin.com/feed",
    "量子位": "https://qbit.ai/feed",
    "新智元": "https://www.leiphone.com/feed",
}

GITHUB_API = "https://api.github.com/search/repositories"

# 去重键值
seen_urls = set()


def fetch_rss(source, url):
    """抓取 RSS 源"""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        # 这里需要解析 RSS XML
        return []
    except Exception as e:
        print(f"[WARN] {source} 抓取失败: {e}")
        return []


def fetch_github_trending():
    """获取 GitHub 热门 AI 项目"""
    try:
        params = {
            "q": "created:>2026-03-28+stars:>100",
            "sort": "stars",
            "order": "desc",
            "per_page": 10
        }
        resp = requests.get(GITHUB_API, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("items", [])[:10]
    except Exception as e:
        print(f"[WARN] GitHub API 失败: {e}")
        return []


def dedupe(items):
    """去重"""
    result = []
    for item in items:
        url = item.get("url", item.get("html_url", ""))
        if url and url not in seen_urls:
            seen_urls.add(url)
            result.append(item)
    return result


def summarize_with_llm(items):
    """调用 LLM 总结内容"""
    # TODO: 集成 LLM 调用 (GLM-5)
    # 对每篇文章生成: 标题、3 个看点、重要性评级
    pass


def generate_daily_report():
    """生成日报"""
    print(f"\n=== 科技日报生成: {DATE} ===\n")
    
    # 1. 抓取各信源
    all_items = []
    
    print("[1/5] 抓取 RSS 信源...")
    for name, url in RSS_FEEDS.items():
        items = fetch_rss(name, url)
        all_items.extend(items)
        print(f"  - {name}: {len(items)} 条")
    
    print("[2/5] 抓取 GitHub Trending...")
    gh_items = fetch_github_trending()
    all_items.extend(gh_items)
    print(f"  - GitHub: {len(gh_items)} 条")
    
    # 2. 去重
    print("[3/5] 去重...")
    all_items = dedupe(all_items)
    print(f"  - 去重后: {len(all_items)} 条")
    
    # 3. 智能总结
    print("[4/5] LLM 总结...")
    # summary = summarize_with_llm(all_items)
    
    # 4. 生成日报
    print("[5/5] 生成日报...")
    report = {
        "date": DATE,
        "title": f"📅 科技日报 | {DATE}",
        "sections": {
            "重磅": [],
            "技术前沿": [],
            "行业动态": [],
            "AI 应用": []
        },
        "total": len(all_items)
    }
    
    # 保存
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 日报已保存: {OUTPUT_FILE}")
    return report


if __name__ == "__main__":
    report = generate_daily_report()
    print(f"📊 共计 {report['total']} 条资讯")