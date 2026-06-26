#!/usr/bin/env python3
"""
知乎热搜月度分析工具 v2.0
分析指定月份的热搜数据，生成统计报告
数据来源：https://github.com/SnailDev/zhihu-hot-hub
"""

import json
import re
import sys
import os
import urllib.request
from collections import Counter
from datetime import datetime, timedelta
from typing import List, Dict, Optional

BASE_URL = "https://raw.githubusercontent.com/SnailDev/zhihu-hot-hub/main"
ARCHIVES_BASE = f"{BASE_URL}/archives"
GITHUB_TREE_API = "https://api.github.com/repos/SnailDev/zhihu-hot-hub/git/trees/main?recursive=1"

# 缓存
CACHE_DIR = os.path.expanduser("~/.cache/zhihu-hot")


def fetch_url(url: str, headers: dict = None) -> str:
    """获取 URL 内容"""
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def get_archives_list() -> List[str]:
    """获取所有归档日期列表"""
    cache_file = os.path.join(CACHE_DIR, "archives_list.json")
    
    # 尝试从缓存加载
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            data = json.load(f)
            # 缓存 1 小时
            if datetime.now().timestamp() - data.get("cached_at", 0) < 3600:
                return data.get("dates", [])
    
    # 从 GitHub API 获取
    try:
        content = fetch_url(GITHUB_TREE_API)
        data = json.loads(content)
        dates = []
        for item in data.get("tree", []):
            path = item.get("path", "")
            if path.startswith("archives/") and path.endswith(".md"):
                date = path.replace("archives/", "").replace(".md", "")
                dates.append(date)
        
        # 保存到缓存
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(cache_file, "w") as f:
            json.dump({"cached_at": datetime.now().timestamp(), "dates": dates}, f)
        
        return sorted(dates)
    except Exception as e:
        print(f"⚠️ 无法获取归档列表：{e}", file=sys.stderr)
        return []


def get_month_dates(dates: List[str], year: int, month: int) -> List[str]:
    """筛选指定月份的日期"""
    prefix = f"{year}-{month:02d}"
    return [d for d in dates if d.startswith(prefix)]


def parse_hot_search(content: str) -> Dict:
    """解析热搜内容"""
    result = {
        "update_time": "",
        "hot_search": [],
        "hot_topics": [],
        "hot_videos": []
    }
    
    # 更新时间
    time_match = re.search(r"更新时间 [：:]\s*(.+?)(?:\n|`)", content)
    if time_match:
        result["update_time"] = time_match.group(1).strip().rstrip("`")
    
    # 热门搜索
    hot_section = re.search(r"## 热门搜索\n(.+?)(?=\n## |$)", content, re.DOTALL)
    if hot_section:
        items = re.findall(r"\d+\.\s*\[([^\]]+)\]\(([^)]+)\)", hot_section.group(1))
        result["hot_search"] = [{"title": t, "url": u} for t, u in items]
    
    # 热门话题
    topics_section = re.search(r"## 热门话题\n(.+?)(?=\n## |$)", content, re.DOTALL)
    if topics_section:
        text = topics_section.group(1)
        if "暂无数据" not in text:
            items = re.findall(r"\d+\.\s*\[([^\]]+)\]\(([^)]+)\)", text)
            result["hot_topics"] = [{"title": t, "url": u} for t, u in items]
    
    # 热门视频
    videos_section = re.search(r"## 热门视频\n(.+?)(?=\n## |$)", content, re.DOTALL)
    if videos_section:
        text = videos_section.group(1)
        if "暂无数据" not in text:
            items = re.findall(r"\d+\.\s*\[([^\]]+)\]\(([^)]+)\)", text)
            result["hot_videos"] = [{"title": t, "url": u} for t, u in items]
    
    return result


def analyze_month(year: int, month: int, dates: List[str]) -> Dict:
    """分析月份数据"""
    month_dates = get_month_dates(dates, year, month)
    
    if not month_dates:
        return {"error": f"未找到 {year}年{month}月 的数据"}
    
    all_titles = []
    daily_data = {}
    progress = 0
    
    for date in month_dates:
        url = f"{ARCHIVES_BASE}/{date}.md"
        try:
            content = fetch_url(url)
            data = parse_hot_search(content)
            titles = [item["title"] for item in data["hot_search"]]
            daily_data[date] = {
                "count": len(titles),
                "titles": titles,
                "topics": [t["title"] for t in data["hot_topics"]],
                "videos": [t["title"] for t in data["hot_videos"]]
            }
            all_titles.extend(titles)
            progress += 1
            print(f"\r✓ {date}: {len(titles)}条 ({progress}/{len(month_dates)})", end="", file=sys.stderr)
        except Exception as e:
            print(f"\r✗ {date}: 失败 - {e}", file=sys.stderr)
    
    print("", file=sys.stderr)
    
    # 统计
    title_counts = Counter(all_titles)
    
    # 关键词提取
    keywords = Counter()
    for title in all_titles:
        words = re.findall(r'[\u4e00-\u9fff]{2,}', title)
        keywords.update(words)
    
    # 每日热搜数统计
    daily_counts = [daily_data[d]["count"] for d in daily_data]
    
    return {
        "year": year,
        "month": month,
        "total_days": len(month_dates),
        "available_days": len(daily_data),
        "total_items": len(all_titles),
        "unique_titles": len(set(all_titles)),
        "top_titles": title_counts.most_common(30),
        "top_keywords": keywords.most_common(50),
        "daily_counts": daily_counts,
        "avg_daily": sum(daily_counts) / len(daily_counts) if daily_counts else 0,
        "max_day": month_dates[daily_counts.index(max(daily_counts))] if daily_counts else "",
        "min_day": month_dates[daily_counts.index(min(daily_counts))] if daily_counts else "",
    }


def format_report(data: Dict) -> str:
    """生成报告"""
    if "error" in data:
        return f"❌ {data['error']}"
    
    lines = []
    lines.append(f"# 📊 知乎热搜月度分析报告")
    lines.append("")
    lines.append(f"**时间**: {data['year']}年{data['month']}月")
    lines.append(f"**数据天数**: {data['available_days']}/{data['total_days']} 天")
    lines.append(f"**总热搜数**: {data['total_items']} 条")
    lines.append(f"**不重复热搜**: {data['unique_titles']} 条")
    lines.append(f"**日均热搜**: {data['avg_daily']:.1f} 条/天")
    lines.append(f"**最多热搜**: {data['max_day']} ({max(data['daily_counts']) if data['daily_counts'] else 0}条)")
    lines.append(f"**最少热搜**: {data['min_day']} ({min(data['daily_counts']) if data['daily_counts'] else 0}条)")
    lines.append("")
    
    lines.append("## 🔥 高频热搜 TOP 30")
    lines.append("")
    lines.append("| 排名 | 热搜话题 | 出现天数 |")
    lines.append("|------|----------|----------|")
    for i, (title, count) in enumerate(data["top_titles"], 1):
        lines.append(f"| {i} | {title} | {count} |")
    lines.append("")
    
    lines.append("## 📊 高频关键词 TOP 50")
    lines.append("")
    lines.append("| 排名 | 关键词 | 出现次数 |")
    lines.append("|------|--------|----------|")
    for i, (word, count) in enumerate(data["top_keywords"], 1):
        if count < 3:
            break
        lines.append(f"| {i} | {word} | {count} |")
    lines.append("")
    
    lines.append("## 📈 趋势分析")
    lines.append("")
    
    # 按周统计
    if data['daily_counts']:
        weeks = []
        for i in range(0, len(data['daily_counts']), 7):
            week = data['daily_counts'][i:i+7]
            weeks.append(sum(week) / len(week))
        
        lines.append("### 周均热搜趋势")
        lines.append("")
        for i, avg in enumerate(weeks, 1):
            bar = "█" * int(avg / 5)
            lines.append(f"第{i}周: {bar} ({avg:.1f}条/天)")
        lines.append("")
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print("用法：analyze-month.py <year> <month>")
        print("示例：analyze-month.py 2026 3")
        print("      analyze-month.py 2023 9")
        sys.exit(1)
    
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    
    print(f"📡 正在获取归档列表...", file=sys.stderr)
    dates = get_archives_list()
    
    if not dates:
        print("❌ 无法获取归档列表", file=sys.stderr)
        sys.exit(1)
    
    print(f"📚 共 {len(dates)} 天的归档数据 ({dates[0]} 至 {dates[-1]})", file=sys.stderr)
    print(f"📅 正在分析 {year}年{month}月 数据...", file=sys.stderr)
    
    # 分析
    report = analyze_month(year, month, dates)
    
    # 输出
    print(format_report(report))


if __name__ == "__main__":
    main()