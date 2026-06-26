#!/usr/bin/env python3
"""
话题热度趋势监控 — 定期查询多个话题在热门/新锐榜的出现频率，观察冷热变化

用法:
  python3 scripts/topic_trends.py --topics "AI创业,副业,MBTI,注意力" --weeks 4
  python3 scripts/topic_trends.py --topics "AI,科技,商业" --weeks 8
"""

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
HISTORY_FILE = SCRIPT_DIR / "topic_trends_history.json"


def load_history():
    if HISTORY_FILE.exists():
        return json.load(open(HISTORY_FILE))
    return {"scans": []}


def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_episodes(list_type, limit=150, offset=0):
    args = [
        sys.executable, str(SCRIPT_DIR / "fetch_xyz_rank.py"),
        "--list", list_type,
        "--limit", str(limit),
        "--offset", str(offset),
    ]
    result = subprocess.run(args, capture_output=True, text=True)
    try:
        return json.loads(result.stdout).get("items", [])
    except Exception:
        return []


def count_topic_mentions(topics, list_type, limit=150):
    """统计各话题在榜单中的出现次数"""
    episodes = fetch_episodes(list_type, limit=limit)
    counts = {t: {"count": 0, "episodes": []} for t in topics}

    for ep in episodes:
        title = (ep.get("title", "") or "").lower()
        podcast = (ep.get("podcastName", "") or "").lower()
        text = title + " " + podcast

        for topic in topics:
            if topic.lower() in text:
                counts[topic]["count"] += 1
                counts[topic]["episodes"].append({
                    "title": ep.get("title"),
                    "podcast": ep.get("podcastName"),
                    "playCount": ep.get("playCount", 0) or 0,
                })

    return counts


def run_scan(topics, weeks):
    """执行一次完整扫描"""
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n🔍 扫描时间: {today}  话题: {', '.join(topics)}\n")

    # 热门榜 vs 新锐榜
    hot_counts = count_topic_mentions(topics, "hot-episodes", 150)
    new_counts = count_topic_mentions(topics, "new-episodes", 100)

    scan_result = {
        "date": today,
        "hot": {},
        "new": {},
    }

    print(f"{'话题':<10} {'热门榜':>8} {'新锐榜':>8} {'总计数':>8} {'热度指数':>10}")
    print("─" * 50)

    hot_total = sum(v["count"] for v in hot_counts.values())
    new_total = sum(v["count"] for v in new_counts.values())

    for topic in topics:
        h = hot_counts[topic]["count"]
        n = new_counts[topic]["count"]
        total = h + n
        # 热度指数 = 热门*2 + 新锐*3（越新越热）
        heat = h * 2 + n * 3
        bar = "█" * min(total, 20)
        print(f"{topic:<10} {h:>8} {n:>8} {total:>8} {heat:>10,}  {bar}")
        scan_result["hot"][topic] = h
        scan_result["new"][topic] = n

    print(f"\n📈 热门榜总话题命中: {hot_total}")
    print(f"🆕 新锐榜总话题命中: {new_total}")

    # 保存历史
    history = load_history()
    history["scans"].append(scan_result)
    # 只保留最近 weeks 次扫描
    if len(history["scans"]) > weeks * 7:
        history["scans"] = history["scans"][-weeks * 7:]
    save_history(history)

    # 趋势对比
    if len(history["scans"]) >= 2:
        print(f"\n📊 趋势变化 (对比最近2次扫描)")
        print("─" * 56)
        scans = history["scans"]
        prev = scans[-2]
        curr = scans[-1]

        for topic in topics:
            ph = prev["hot"].get(topic, 0)
            pn = prev["new"].get(topic, 0)
            ch = curr["hot"].get(topic, 0)
            cn = curr["new"].get(topic, 0)
            h_change = ch - ph
            n_change = cn - pn
            h_arrow = "📈" if h_change > 0 else "📉" if h_change < 0 else "➡️"
            n_arrow = "📈" if n_change > 0 else "📉" if n_change < 0 else "➡️"
            print(f"  {topic:<10} 热门榜:{h_arrow}{h_change:+d}  新锐榜:{n_arrow}{n_change:+d}")

    return scan_result


def print_full_trend(topics, weeks):
    """打印完整趋势历史"""
    history = load_history()
    if not history["scans"]:
        print("📭 暂无历史数据，先运行一次 --scan")
        return

    scans = history["scans"][-weeks:] if weeks else history["scans"]

    print(f"\n📈 话题热度趋势 (最近{len(scans)}次扫描)\n")
    dates = [s["date"][5:] for s in scans]

    print(f"{'话题':<10} " + "  ".join(f"{d:>8}" for d in dates))
    print("─" * (10 + 10 * len(dates)))

    for topic in topics:
        row = []
        for s in scans:
            total = s["hot"].get(topic, 0) + s["new"].get(topic, 0)
            row.append(f"{total:>8}")
        print(f"{topic:<10} " + "  ".join(row))

    if len(scans) >= 3:
        print(f"\n💡 趋势解读:")
        recent = scans[-1]
        older = scans[-3] if len(scans) >= 3 else scans[0]
        for topic in topics:
            r_total = recent["hot"].get(topic, 0) + recent["new"].get(topic, 0)
            o_total = older["hot"].get(topic, 0) + older["new"].get(topic, 0)
            if r_total > o_total * 1.5:
                print(f"  📈 {topic}: 热度上升 ({o_total}→{r_total})")
            elif r_total < o_total * 0.7:
                print(f"  📉 {topic}: 热度下降 ({o_total}→{r_total})")


def main():
    parser = argparse.ArgumentParser(description="话题热度趋势监控")
    parser.add_argument("--topics", required=True, help="话题列表，逗号分隔")
    parser.add_argument("--weeks", type=int, default=4, help="保留历史周数")
    parser.add_argument("--trend", action="store_true", help="打印完整趋势历史")
    args = parser.parse_args()

    topics = [t.strip() for t in args.topics.split(",") if t.strip()]

    if args.trend:
        print_full_trend(topics, args.weeks)
    else:
        run_scan(topics, args.weeks)


if __name__ == "__main__":
    main()
