#!/usr/bin/env python3
"""
爆款单集追踪脚本 — 追踪特定话题/嘉宾在热门单集中的出现频率和表现

用法:
  python3 scripts/track_episodes.py --topic AI --limit 30
  python3 scripts/track_episodes.py --guest "张雪峰" --limit 20
  python3 scripts/track_episodes.py --topic "注意力" --report
"""

import argparse
import json
import math
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
HISTORY_FILE = SCRIPT_DIR / "episode_history.json"
MAX_HOT_FETCH = 200
MAX_NEW_FETCH = 100


def load_history():
    if HISTORY_FILE.exists():
        return json.load(open(HISTORY_FILE))
    return {"episodes": {}, "last_full_scan": None}


def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_episodes(list_type, limit=100, offset=0):
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


def search_episodes(query, limit=30):
    """用 xyzrank 搜索特定关键词的单集"""
    hot = fetch_episodes("hot-episodes", limit=limit)
    new = fetch_episodes("new-episodes", limit=limit // 2)
    query_lower = query.lower()
    results = []
    for ep in hot + new:
        title = ep.get("title", "") or ""
        podcast = ep.get("podcastName", "") or ""
        if query_lower in title.lower() or query_lower in podcast.lower():
            results.append(ep)
        if len(results) >= limit:
            break
    return results


def search_guest_episodes(guest_name, limit=20):
    """搜索包含特定嘉宾/人物的单集"""
    patterns = [
        re.compile(rf"(?:对话|对谈|访谈)\s*[^\｜:：!！?？]*{re.escape(guest_name)}", re.IGNORECASE),
        re.compile(rf"[/／]\s*{re.escape(guest_name)}"),
    ]
    hot = fetch_episodes("hot-episodes", limit=MAX_HOT_FETCH)
    results = []
    for ep in hot:
        title = ep.get("title", "") or ""
        for pat in patterns:
            if pat.search(title):
                results.append(ep)
                break
        if len(results) >= limit:
            break
    return results


def score_episode(ep):
    """给单集打综合分（播放量 log + 评论加权）"""
    play = ep.get("playCount", 0) or 0
    comment = ep.get("commentCount", 0) or 0
    play_score = math.log1p(play) * 10
    comment_score = math.log1p(comment) * 20 if play > 0 else 0
    return round(play_score + comment_score, 1)


def group_by_podcast(episodes):
    """按播客分组"""
    groups = defaultdict(list)
    for ep in episodes:
        name = ep.get("podcastName", "未知")
        groups[name].append(ep)
    return dict(groups)


def format_duration(minutes):
    if not minutes:
        return "—"
    if minutes >= 60:
        h = int(minutes // 60)
        m = int(minutes % 60)
        return f"{h}h{m}m" if m else f"{h}h"
    return f"{minutes:.0f}min"


def print_episode(ep, index):
    title = ep.get("title", "—")
    podcast = ep.get("podcastName", "—")
    play = ep.get("playCount", 0) or 0
    comment = ep.get("commentCount", 0) or 0
    dur = format_duration(ep.get("durationMinutes") or ep.get("duration"))
    freshness = ep.get("freshnessDays", 0) or 0
    rank = ep.get("rank", "—")
    print(f"  {index:>2}. {title}")
    print(f"      📻 {podcast}  |  🎧 {play:>9,}  💬 {comment:>5}  ⏱ {dur}  🕐 {freshness:.0f}天  #{rank}")


def cmd_topic(args):
    """按话题搜索单集"""
    query = args.topic
    print(f"\n🔍 搜索话题「{query}」的爆款单集\n")
    episodes = search_episodes(query, limit=args.limit)
    if not episodes:
        episodes = search_episodes(query, limit=args.limit * 2)
        if not episodes:
            print("❌ 未找到相关单集")
            return
    episodes.sort(key=score_episode, reverse=True)

    plays = [e.get("playCount", 0) for e in episodes if e.get("playCount")]
    comments = [e.get("commentCount", 0) for e in episodes if e.get("commentCount")]
    durations = [e.get("durationMinutes") or e.get("duration", 0) for e in episodes
                 if e.get("durationMinutes") or e.get("duration")]

    print(f"📊 命中 {len(episodes)} 期\n")
    if plays:
        print(f"  平均播放量: {sum(plays)/len(plays):,.0f}  最高: {max(plays):,}")
    if comments:
        avg_c = sum(comments) / len(comments)
        print(f"  平均评论数: {avg_c:.1f}  最高: {max(comments)}")
    if durations:
        avg_d = sum(durations) / len(durations)
        long_pct = sum(1 for d in durations if d > 60) / len(durations) * 100
        print(f"  平均时长:   {avg_d:.0f}min  长单集占{long_pct:.0f}%")

    groups = group_by_podcast(episodes)
    print(f"\n📻 涉及 {len(groups)} 个播客频道：")
    for name, eps in sorted(groups.items(), key=lambda x: score_episode(x[1][0]), reverse=True):
        eps.sort(key=score_episode, reverse=True)
        print(f"\n  📌 {name} ({len(eps)}期)")
        for i, ep in enumerate(eps[:3], 1):
            print_episode(ep, i)

    if args.track:
        history = load_history()
        today = datetime.now().strftime("%Y-%m-%d")
        for ep in episodes:
            eid = ep.get("podcastExternalId") or ep.get("title", "")
            if eid not in history["episodes"]:
                history["episodes"][eid] = {
                    "title": ep.get("title"),
                    "podcastName": ep.get("podcastName"),
                    "first_seen": today,
                    "appearances": 1,
                    "peak_play": ep.get("playCount", 0) or 0,
                }
            else:
                history["episodes"][eid]["appearances"] += 1
                if ep.get("playCount", 0) > history["episodes"][eid]["peak_play"]:
                    history["episodes"][eid]["peak_play"] = ep.get("playCount", 0)
        history["last_full_scan"] = today
        save_history(history)
        print(f"\n✅ 已记录到 episode_history.json")


def cmd_guest(args):
    """按嘉宾搜索单集"""
    guest = args.guest
    print(f"\n👤 搜索嘉宾「{guest}」出现的单集\n")
    episodes = search_guest_episodes(guest, limit=args.limit)
    if not episodes:
        print("❌ 未找到该嘉宾出现的单集")
        return
    episodes.sort(key=score_episode, reverse=True)

    for i, ep in enumerate(episodes, 1):
        print_episode(ep, i)

    groups = group_by_podcast(episodes)
    print(f"\n📊 共出现于 {len(groups)} 个播客：")
    for name, eps in sorted(groups.items(), key=lambda x: score_episode(x[1][0]), reverse=True):
        print(f"  · {name} ({len(eps)}期)")


def cmd_report(args):
    """生成话题简报"""
    query = args.topic or "注意力"
    episodes = search_episodes(query, limit=30)
    if not episodes:
        print(f"❌ 未找到「{query}」相关单集")
        return
    episodes.sort(key=score_episode, reverse=True)

    print(f"\n{'='*56}")
    print(f"📋 话题简报: {query}")
    print(f"{'='*56}")
    print(f"命中单集数: {len(episodes)}")
    print()
    for i, ep in enumerate(episodes[:15], 1):
        title = ep.get("title", "—")
        podcast = ep.get("podcastName", "—")
        play = ep.get("playCount", 0) or 0
        dur = format_duration(ep.get("durationMinutes") or ep.get("duration"))
        freshness = ep.get("freshnessDays", 0) or 0
        print(f"{i:>2}. [{podcast}] {title}")
        print(f"    🎧 {play:>9,}  ⏱ {dur}  🕐 {freshness:.0f}天前")
    print(f"{'='*56}\n")


def main():
    parser = argparse.ArgumentParser(description="爆款单集追踪工具")
    parser.add_argument("--topic", help="搜索话题关键词")
    parser.add_argument("--guest", help="搜索特定嘉宾出现的单集")
    parser.add_argument("--limit", type=int, default=30, help="最大结果数")
    parser.add_argument("--report", action="store_true", help="输出简报格式")
    parser.add_argument("--track", action="store_true", help="记录到历史")
    args = parser.parse_args()

    if args.topic:
        if args.report:
            cmd_report(args)
        else:
            cmd_topic(args)
    elif args.guest:
        cmd_guest(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
