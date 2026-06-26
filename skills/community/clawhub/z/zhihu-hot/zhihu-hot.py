#!/usr/bin/env python3
"""
知乎热搜获取工具 v3.0
数据来源：https://github.com/SnailDev/zhihu-hot-hub
数据覆盖：2021-01-08 至今
"""

import argparse
import re
import sys
import os
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Tuple
from pathlib import Path
from collections import Counter

__version__ = "3.0.0"

# 缓存配置
CACHE_DIR = os.path.expanduser("~/.cache/zhihu-hot")
CACHE_EXPIRE = 3600  # 1 小时
ARCHIVES_CACHE_EXPIRE = 7200  # 归档列表 2 小时

# 数据源
BASE_URL = "https://raw.githubusercontent.com/SnailDev/zhihu-hot-hub/main"
GITHUB_TREE_API = "https://api.github.com/repos/SnailDev/zhihu-hot-hub/git/trees/main?recursive=1"

# 终端颜色
USE_COLOR = sys.stdout.isatty()
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "magenta": "\033[95m",
} if USE_COLOR else {}


def colorize(text: str, color: str) -> str:
    """添加颜色"""
    return f"{COLORS.get(color, '')}{text}{COLORS.get('reset', '')}"


# ==================== 缓存管理 ====================

def ensure_cache_dir():
    """确保缓存目录存在"""
    os.makedirs(CACHE_DIR, exist_ok=True)


def get_cache_path(name: str) -> str:
    """获取缓存文件路径"""
    return os.path.join(CACHE_DIR, f"{name}.json")


def load_cache(name: str, expire: int = CACHE_EXPIRE) -> Optional[dict]:
    """加载缓存"""
    cache_path = get_cache_path(name)
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if time.time() - data.get("cached_at", 0) < expire:
                return data.get("data")
    return None


def save_cache(name: str, data):
    """保存缓存"""
    ensure_cache_dir()
    cache_path = get_cache_path(name)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump({"cached_at": time.time(), "data": data}, f, ensure_ascii=False, indent=2)


def clear_cache():
    """清理缓存"""
    if os.path.exists(CACHE_DIR):
        count = 0
        size = 0
        for f in os.listdir(CACHE_DIR):
            fp = os.path.join(CACHE_DIR, f)
            if os.path.isfile(fp):
                size += os.path.getsize(fp)
                os.remove(fp)
                count += 1
        return count, size
    return 0, 0


def get_cache_stats() -> Dict:
    """获取缓存统计"""
    if not os.path.exists(CACHE_DIR):
        return {"count": 0, "size": 0}
    
    files = os.listdir(CACHE_DIR)
    total_size = sum(
        os.path.getsize(os.path.join(CACHE_DIR, f))
        for f in files if os.path.isfile(os.path.join(CACHE_DIR, f))
    )
    return {"count": len(files), "size": total_size}


# ==================== 数据获取 ====================

def fetch_url(url: str, headers: dict = None) -> str:
    """获取 URL 内容"""
    req = urllib.request.Request(
        url,
        headers=headers or {"User-Agent": "Mozilla/5.0 (compatible; ZhihuHotBot/3.0)"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def get_archives_list() -> List[str]:
    """获取所有归档日期列表"""
    # 尝试从缓存加载
    cached = load_cache("archives_list", ARCHIVES_CACHE_EXPIRE)
    if cached:
        return cached
    
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
        
        dates = sorted(dates)
        save_cache("archives_list", dates)
        return dates
    except Exception as e:
        print(colorize(f"⚠️ 无法获取归档列表：{e}", "yellow"), file=sys.stderr)
        return []


def fetch_day_data(date: str) -> Optional[Dict]:
    """获取指定日期的热搜数据"""
    # 尝试缓存
    cached = load_cache(date)
    if cached:
        return cached
    
    url = f"{BASE_URL}/archives/{date}.md"
    if date == datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d"):
        url = f"{BASE_URL}/README.md"
    
    try:
        content = fetch_url(url)
        data = parse_markdown(content)
        save_cache(date, data)
        return data
    except Exception as e:
        print(colorize(f"⚠️ 获取 {date} 失败：{e}", "yellow"), file=sys.stderr)
        return None


# ==================== 数据解析 ====================

def decode_url(url: str) -> str:
    """解码 URL 中的中文"""
    try:
        return urllib.parse.unquote(url)
    except:
        return url


def get_display_width(s: str) -> int:
    """计算字符串显示宽度（中文 2，英文 1）"""
    width = 0
    for c in s:
        if '\u4e00' <= c <= '\u9fff' or '\u3000' <= c <= '\u303f':
            width += 2
        elif c in '，。！？、；：""''（）【】《》':
            width += 2
        else:
            width += 1
    return width


def pad_string(s: str, width: int) -> str:
    """填充字符串到指定显示宽度"""
    current = get_display_width(s)
    if current >= width:
        return s
    return s + ' ' * (width - current)


def parse_markdown(content: str) -> Dict:
    """解析 Markdown 内容"""
    result = {
        "update_time": "",
        "hot_search": [],
        "hot_topics": [],
        "hot_videos": []
    }
    
    # 提取更新时间
    time_match = re.search(r"更新时间 [：:]\s*(.+?)(?:\n|$)", content)
    if time_match:
        result["update_time"] = time_match.group(1).strip().rstrip("`")
    
    # 提取热门搜索
    hot_section = re.search(r"## 热门搜索\n(.+?)(?=\n## |$)", content, re.DOTALL)
    if hot_section:
        items = re.findall(r"\d+\.\s*\[([^\]]+)\]\(([^)]+)\)", hot_section.group(1))
        for title, url in items:
            result["hot_search"].append({
                "title": title,
                "url": url,
                "decoded_url": decode_url(url)
            })
    
    # 提取热门话题
    topics_section = re.search(r"## 热门话题\n(.+?)(?=\n## |$)", content, re.DOTALL)
    if topics_section:
        text = topics_section.group(1)
        if "暂无数据" not in text:
            items = re.findall(r"\d+\.\s*\[([^\]]+)\]\(([^)]+)\)", text)
            for title, url in items:
                result["hot_topics"].append({
                    "title": title,
                    "url": url,
                    "decoded_url": decode_url(url)
                })
    
    # 提取热门视频
    videos_section = re.search(r"## 热门视频\n(.+?)(?=\n## |$)", content, re.DOTALL)
    if videos_section:
        text = videos_section.group(1)
        if "暂无数据" not in text:
            items = re.findall(r"\d+\.\s*\[([^\]]+)\]\(([^)]+)\)", text)
            for title, url in items:
                result["hot_videos"].append({
                    "title": title,
                    "url": url,
                    "decoded_url": decode_url(url)
                })
    
    return result


# ==================== 格式化输出 ====================

def format_table(data: Dict, date: str, limit: int = 0, show_url: bool = False) -> str:
    """表格格式输出"""
    lines = []
    lines.append(colorize(f"📊 知乎热搜 - {date}", "bold"))
    lines.append("")
    
    if data["update_time"]:
        lines.append(colorize(f"⏰ 更新：{data['update_time']}", "cyan"))
        lines.append("")
    
    if data["hot_search"]:
        lines.append(colorize("🔥 热门搜索", "bold"))
        lines.append("┌────┬──────────────────────────────────────────┐")
        items = data["hot_search"][:limit] if limit > 0 else data["hot_search"]
        for i, item in enumerate(items, 1):
            title = item["title"]
            if get_display_width(title) > 38:
                title = title[:18] + ".."
            lines.append(f"│ {i:2d} │ {pad_string(title, 40)} │")
        lines.append("└────┴──────────────────────────────────────────┘")
        
        if show_url:
            lines.append("")
            for i, item in enumerate(items, 1):
                lines.append(f"{colorize(str(i)+'.', 'yellow')} {item['decoded_url']}")
    
    if data["hot_topics"]:
        lines.append("")
        lines.append(colorize("💬 热门话题", "bold"))
        items = data["hot_topics"][:limit] if limit > 0 else data["hot_topics"]
        for i, item in enumerate(items, 1):
            lines.append(f"  {colorize(str(i)+'.', 'yellow')} {item['title']}")
    
    if data["hot_videos"]:
        lines.append("")
        lines.append(colorize("🎬 热门视频", "bold"))
        items = data["hot_videos"][:limit] if limit > 0 else data["hot_videos"]
        for i, item in enumerate(items, 1):
            lines.append(f"  {colorize(str(i)+'.', 'yellow')} {item['title']}")
    
    return "\n".join(lines)


def format_compact(data: Dict, date: str, limit: int = 0) -> str:
    """紧凑格式输出"""
    lines = []
    header = f"📊 知乎热搜 {date}"
    if data["update_time"]:
        header += colorize(f" | ⏰ {data['update_time']}", "cyan")
    lines.append(colorize(header, "bold"))
    lines.append("")
    
    if data["hot_search"]:
        items = data["hot_search"][:limit] if limit > 0 else data["hot_search"]
        for i, item in enumerate(items, 1):
            lines.append(f"{colorize(str(i).rjust(2), 'yellow')}. {item['title']}")
    
    return "\n".join(lines)


def format_oneline(data: Dict, date: str, limit: int = 5) -> str:
    """单行格式输出（适合推送）"""
    items = data["hot_search"][:limit]
    titles = [item["title"] for item in items]
    return f"📊 知乎热搜 {date}: " + " | ".join(titles)


def format_json(data: Dict, date: str, limit: int = 0) -> str:
    """JSON 格式输出"""
    output = {
        "date": date,
        "update_time": data.get("update_time", ""),
        "hot_search": data["hot_search"][:limit] if limit > 0 else data["hot_search"],
        "hot_topics": data["hot_topics"][:limit] if limit > 0 else data["hot_topics"],
        "hot_videos": data["hot_videos"][:limit] if limit > 0 else data["hot_videos"]
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def format_output(data: Dict, date: str, format_type: str = "table",
                  limit: int = 0, show_url: bool = False) -> str:
    """格式化输出"""
    if format_type == "json":
        return format_json(data, date, limit)
    if format_type == "oneline":
        return format_oneline(data, date, limit if limit > 0 else 5)
    if format_type == "compact":
        return format_compact(data, date, limit)
    return format_table(data, date, limit, show_url)


# ==================== 搜索功能 ====================

def search_items(data: Dict, keyword: str) -> List[Dict]:
    """搜索热搜"""
    results = []
    keyword_lower = keyword.lower()
    for item in data["hot_search"]:
        if keyword_lower in item["title"].lower():
            results.append(item)
    return results


def search_in_range(start_date: str, end_date: str, keyword: str) -> List[Tuple[str, Dict]]:
    """在日期范围内搜索"""
    results = []
    archives = get_archives_list()
    
    for date in archives:
        if start_date <= date <= end_date:
            data = fetch_day_data(date)
            if data:
                matches = search_items(data, keyword)
                if matches:
                    results.append((date, matches))
    
    return results


# ==================== 统计功能 ====================

def analyze_range(start_date: str, end_date: str) -> Dict:
    """分析日期范围内的热搜"""
    archives = get_archives_list()
    date_range = [d for d in archives if start_date <= d <= end_date]
    
    if not date_range:
        return {"error": "未找到指定范围内的数据"}
    
    all_titles = []
    daily_data = {}
    
    for date in date_range:
        data = fetch_day_data(date)
        if data:
            titles = [item["title"] for item in data["hot_search"]]
            daily_data[date] = len(titles)
            all_titles.extend(titles)
    
    title_counts = Counter(all_titles)
    keywords = Counter()
    for title in all_titles:
        words = re.findall(r'[\u4e00-\u9fff]{2,}', title)
        keywords.update(words)
    
    daily_counts = list(daily_data.values())
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_days": len(date_range),
        "total_items": len(all_titles),
        "unique_titles": len(set(all_titles)),
        "avg_daily": sum(daily_counts) / len(daily_counts) if daily_counts else 0,
        "top_titles": title_counts.most_common(20),
        "top_keywords": keywords.most_common(30),
    }


def format_analysis(analysis: Dict) -> str:
    """格式化分析报告"""
    if "error" in analysis:
        return colorize(f"❌ {analysis['error']}", "red")
    
    lines = []
    lines.append(colorize(f"📊 热搜分析报告", "bold"))
    lines.append(f"时间范围：{analysis['start_date']} 至 {analysis['end_date']}")
    lines.append(f"数据天数：{analysis['total_days']} 天")
    lines.append(f"总热搜数：{analysis['total_items']} 条")
    lines.append(f"不重复热搜：{analysis['unique_titles']} 条")
    lines.append(f"日均热搜：{analysis['avg_daily']:.1f} 条/天")
    lines.append("")
    
    lines.append(colorize("🔥 高频热搜 TOP 20", "bold"))
    for i, (title, count) in enumerate(analysis["top_titles"], 1):
        lines.append(f"  {i:2d}. {title} ({count}天)")
    lines.append("")
    
    lines.append(colorize("📊 高频关键词 TOP 20", "bold"))
    for i, (word, count) in enumerate(analysis["top_keywords"], 1):
        if count < 3:
            break
        lines.append(f"  {i:2d}. {word} ({count}次)")
    
    return "\n".join(lines)


# ==================== 导出功能 ====================

def export_to_file(content: str, filename: str):
    """导出到文件"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


# ==================== 主函数 ====================

def main():
    parser = argparse.ArgumentParser(
        description="获取知乎热搜",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                    # 今日热搜
  %(prog)s -n 10              # 前 10 条
  %(prog)s -c                 # 紧凑格式
  %(prog)s -o                 # 单行格式 (适合推送)
  %(prog)s -j                 # JSON 格式
  %(prog)s -u                 # 显示完整 URL
  %(prog)s 2026-03-20         # 历史热搜
  %(prog)s -s AI              # 搜索热搜
  %(prog)s -r 2026-03-01 2026-03-25  # 日期范围分析
  %(prog)s --export out.md    # 导出文件
  %(prog)s --clear-cache      # 清理缓存
  %(prog)s --stats            # 缓存统计
  %(prog)s --archives         # 显示归档信息
        """
    )
    
    parser.add_argument("date", nargs="?", help="日期 (YYYY-MM-DD)，默认今天")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 格式输出")
    parser.add_argument("-n", "--limit", type=int, default=0, help="限制显示条数")
    parser.add_argument("-c", "--compact", action="store_true", help="紧凑格式")
    parser.add_argument("-o", "--oneline", action="store_true", help="单行格式")
    parser.add_argument("-u", "--url", action="store_true", help="显示完整 URL")
    parser.add_argument("-s", "--search", type=str, help="搜索关键词")
    parser.add_argument("-r", "--range", nargs=2, metavar=("START", "END"), help="日期范围分析")
    parser.add_argument("--no-cache", action="store_true", help="不使用缓存")
    parser.add_argument("--clear-cache", action="store_true", help="清理缓存")
    parser.add_argument("--stats", action="store_true", help="缓存统计")
    parser.add_argument("--archives", action="store_true", help="显示归档信息")
    parser.add_argument("--export", "-e", type=str, help="导出到文件")
    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {__version__}")
    
    args = parser.parse_args()
    
    # 清理缓存
    if args.clear_cache:
        count, size = clear_cache()
        print(colorize(f"✅ 已清理 {count} 个文件 ({size/1024:.1f} KB)", "green"))
        return
    
    # 缓存统计
    if args.stats:
        stats = get_cache_stats()
        print(colorize("📦 缓存统计", "bold"))
        print(f"   目录：{CACHE_DIR}")
        print(f"   文件数：{stats['count']}")
        print(f"   大小：{stats['size'] / 1024:.1f} KB")
        return
    
    # 归档信息
    if args.archives:
        print(colorize("📚 归档信息", "bold"))
        archives = get_archives_list()
        if archives:
            print(f"   最早：{archives[0]}")
            print(f"   最新：{archives[-1]}")
            print(f"   总计：{len(archives)} 天")
        return
    
    # 日期范围分析
    if args.range:
        start, end = args.range
        print(colorize(f"📊 分析 {start} 至 {end} 数据...", "cyan"), file=sys.stderr)
        analysis = analyze_range(start, end)
        output = format_analysis(analysis)
        if args.export:
            export_to_file(output, args.export)
            print(colorize(f"✅ 已导出到 {args.export}", "green"))
        else:
            print(output)
        return
    
    # 计算日期
    beijing_tz = timezone(timedelta(hours=8))
    today = datetime.now(beijing_tz).strftime("%Y-%m-%d")
    
    if args.date:
        date = args.date
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print(colorize(f"❌ 日期格式无效，应为 YYYY-MM-DD", "red"), file=sys.stderr)
            sys.exit(1)
    else:
        date = today
    
    # 清除缓存选项
    if args.no_cache and date != today:
        cache_path = get_cache_path(date)
        if os.path.exists(cache_path):
            os.remove(cache_path)
    
    # 获取数据
    data = fetch_day_data(date)
    if not data:
        print(colorize(f"❌ 无法获取 {date} 的数据", "red"), file=sys.stderr)
        sys.exit(1)
    
    # 搜索模式
    if args.search:
        results = search_items(data, args.search)
        if results:
            print(colorize(f"🔍 搜索结果：{args.search}", "bold"))
            for i, item in enumerate(results, 1):
                print(f"{colorize(str(i)+'.', 'yellow')} {item['title']}")
                if args.url:
                    print(f"   {item['decoded_url']}")
        else:
            print(colorize(f"❌ 未找到包含 '{args.search}' 的热搜", "yellow"))
        return
    
    # 确定输出格式
    format_type = "table"
    if args.json:
        format_type = "json"
    elif args.oneline:
        format_type = "oneline"
    elif args.compact:
        format_type = "compact"
    
    # 输出
    output = format_output(
        data, date,
        format_type=format_type,
        limit=args.limit,
        show_url=args.url
    )
    
    # 导出文件
    if args.export:
        export_to_file(output, args.export)
        print(colorize(f"✅ 已导出到 {args.export}", "green"))
    else:
        print(output)


if __name__ == "__main__":
    main()