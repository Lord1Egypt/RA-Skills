#!/usr/bin/env python3
"""
播客排名跟踪脚本 - 记录指定播客的排名变化

用法:
  python3 track_podcast.py add <播客名>     # 添加追踪
  python3 track_podcast.py list             # 查看追踪列表
  python3 track_podcast.py update           # 更新排名
  python3 track_podcast.py trends <播客名>   # 查看趋势
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "tracking_data.json")

# 加载数据
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"podcasts": {}, "last_update": None}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 添加播客追踪
def add_podcast(podcast_name):
    data = load_data()
    if podcast_name in data["podcasts"]:
        print(f"⚠️ '{podcast_name}' 已在追踪列表中")
        return
    
    # 查询播客信息
    import subprocess
    result = subprocess.run(
        [sys.executable, "fetch_xyz_rank.py", "--list", "hot-podcasts", "--query", podcast_name, "--limit", "5"],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    
    try:
        result_data = json.loads(result.stdout)
        if result_data.get("returnedCount", 0) == 0:
            print(f"❌ 未找到播客: {podcast_name}")
            return
        
        # 找到最匹配的播客
        podcast = None
        for p in result_data["items"]:
            if podcast_name.lower() in p["title"].lower() or podcast_name.lower() in p["podcastName"].lower():
                podcast = p
                break
        
        if not podcast:
            podcast = result_data["items"][0]
        
        data["podcasts"][podcast_name] = {
            "externalId": podcast.get("externalId"),
            "title": podcast.get("title"),
            "genre": podcast.get("genre"),
            "history": []
        }
        save_data(data)
        print(f"✅ 已添加追踪: {podcast['title']}")
    except Exception as e:
        print(f"❌ 添加失败: {e}")

# 列出追踪的播客
def list_podcasts():
    data = load_data()
    if not data["podcasts"]:
        print("📭 暂无追踪的播客")
        return
    
    print(f"📡 追踪中的播客 ({len(data['podcasts'])}个):\n")
    for name, info in data["podcasts"].items():
        history = info.get("history", [])
        if history:
            last_rank = history[-1]["rank"]
            print(f"  • {name} (最近排名: #{last_rank})")
        else:
            print(f"  • {name} (未记录排名)")

# 更新排名
def update_rankings():
    data = load_data()
    if not data["podcasts"]:
        print("📭 暂无追踪的播客")
        return
    
    import subprocess
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    updated = 0
    
    for podcast_name, info in data["podcasts"].items():
        try:
            result = subprocess.run(
                [sys.executable, "fetch_xyz_rank.py", "--list", "hot-podcasts", "--query", podcast_name, "--limit", "50"],
                capture_output=True, text=True, cwd=SCRIPT_DIR
            )
            
            result_data = json.loads(result.stdout)
            
            # 找到对应播客
            for p in result_data["items"]:
                if p.get("externalId") == info.get("externalId"):
                    rank = p.get("rank", "N/A")
                    avg_play = p.get("avgPlayCount", 0)
                    
                    info["history"].append({
                        "date": today,
                        "rank": rank,
                        "avgPlayCount": avg_play
                    })
                    print(f"  ✓ {podcast_name}: 排名 #{rank}")
                    updated += 1
                    break
        except Exception as e:
            print(f"  ✗ {podcast_name}: 更新失败 ({e})")
    
    data["last_update"] = today
    save_data(data)
    print(f"\n✅ 更新完成: {updated}个播客")

# 查看趋势
def show_trends(podcast_name):
    data = load_data()
    
    if podcast_name not in data["podcasts"]:
        print(f"❌ 未追踪此播客: {podcast_name}")
        return
    
    info = data["podcasts"][podcast_name]
    history = info.get("history", [])
    
    if not history:
        print(f"📭 {podcast_name} 暂无历史数据")
        return
    
    print(f"\n📈 {podcast_name} 排名趋势\n")
    print(f"{'日期':<12} {'排名':<8} {'平均播放':<12}")
    print("-" * 35)
    
    for record in history:
        date = record["date"][:10]
        rank = f"#{record['rank']}" if record["rank"] else "N/A"
        plays = f"{record.get('avgPlayCount', 0):,}" if record.get("avgPlayCount") else "N/A"
        print(f"{date:<12} {rank:<8} {plays:<12}")
    
    # 计算趋势
    if len(history) >= 2:
        first = history[0]["rank"]
        last = history[-1]["rank"]
        change = first - last
        if change > 0:
            trend = f"⬆️ 上升 {change} 名"
        elif change < 0:
            trend = f"⬇️ 下降 {abs(change)} 名"
        else:
            trend = "➡️ 持平"
        print(f"\n趋势: {trend}")

# 主入口
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="播客排名跟踪工具")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("list", help="列出追踪的播客")
    subparsers.add_parser("update", help="更新所有播客的排名")
    
    add_parser = subparsers.add_parser("add", help="添加播客追踪")
    add_parser.add_argument("podcast_name", help="播客名称")
    
    trends_parser = subparsers.add_parser("trends", help="查看排名趋势")
    trends_parser.add_argument("podcast_name", help="播客名称")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_podcast(args.podcast_name)
    elif args.command == "list":
        list_podcasts()
    elif args.command == "update":
        update_rankings()
    elif args.command == "trends":
        show_trends(args.podcast_name)
    else:
        parser.print_help()