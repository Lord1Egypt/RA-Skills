#!/usr/bin/env python3
"""
播客订阅跟踪脚本 - 记录指定播客的订阅量变化

用法:
  python3 track_subscription.py add <播客名>     # 添加追踪
  python3 track_subscription.py list             # 查看追踪列表
  python3 track_subscription.py update           # 更新订阅量
  python3 track_subscription.py trends <播客名>   # 查看趋势
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from urllib.request import urlopen, Request
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "subscription_data.json")

# 加载数据
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"podcasts": {}, "last_update": None}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def search_podcast(podcast_name):
    """从 xyzrank 搜索播客获取小宇宙 PID"""
    import subprocess
    result = subprocess.run(
        [sys.executable, "fetch_xyz_rank.py", "--list", "hot-podcasts", "--query", podcast_name, "--limit", "5"],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    
    try:
        result_data = json.loads(result.stdout)
        if result_data.get("returnedCount", 0) == 0:
            return None, None
        
        # 找最匹配的播客
        for p in result_data["items"]:
            if podcast_name.lower() in p["title"].lower() or podcast_name.lower() in p["podcastName"].lower():
                # 从 xyzrank 的 links.xyz 获取真实 PID
                xyz_url = p.get("links", {}).get("xyz", "")
                pid = xyz_url.split("/")[-1] if xyz_url else None
                return pid, p.get("title")
        
        # 返回第一个
        p = result_data["items"][0]
        xyz_url = p.get("links", {}).get("xyz", "")
        pid = xyz_url.split("/")[-1] if xyz_url else None
        return pid, p.get("title")
    except:
        return None, None

def fetch_subscription_from_xiaoyuzhou(pid):
    """从小宇宙页面获取真实订阅量"""
    try:
        url = f"https://www.xiaoyuzhoufm.com/podcast/{pid}"
        headers = {"User-Agent": "Mozilla/5.0"}
        req = Request(url, headers=headers)
        response = urlopen(req, timeout=10)
        html = response.read().decode("utf-8")
        
        # 从 JSON 数据中提取 subscriptionCount
        match = re.search(r'"subscriptionCount":(\d+)', html)
        if match:
            return int(match.group(1))
        
        return None
    except Exception as e:
        print(f"  获取订阅失败: {e}")
        return None

# 添加播客追踪
def add_podcast(podcast_name):
    data = load_data()
    if podcast_name in data["podcasts"]:
        print(f"⚠️ '{podcast_name}' 已在追踪列表中")
        return
    
    pid, title = search_podcast(podcast_name)
    if not pid:
        print(f"❌ 未找到播客: {podcast_name}")
        return
    
    data["podcasts"][podcast_name] = {
        "pid": pid,
        "title": title,
        "history": []
    }
    save_data(data)
    print(f"✅ 已添加追踪: {title} (PID: {pid})")

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
            last_sub = history[-1].get("subscribers", 0)
            print(f"  • {name} (当前: {last_sub:,} 订阅)")
        else:
            print(f"  • {name} (未记录)")

# 更新订阅量
def update_subscriptions():
    data = load_data()
    if not data["podcasts"]:
        print("📭 暂无追踪的播客")
        return
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    updated = 0
    
    for podcast_name, info in data["podcasts"].items():
        pid = info.get("pid")
        if not pid:
            print(f"  ✗ {podcast_name}: 缺少PID")
            continue
        
        subs = fetch_subscription_from_xiaoyuzhou(pid)
        if subs:
            info["history"].append({
                "date": today,
                "subscribers": subs
            })
            print(f"  ✓ {podcast_name}: {subs:,} 订阅")
            updated += 1
        else:
            print(f"  ✗ {podcast_name}: 获取失败")
    
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
    
    print(f"\n📈 {podcast_name} 订阅趋势\n")
    print(f"{'日期':<12} {'订阅量':<12} {'周变化':<12}")
    print("-" * 40)
    
    prev_subs = None
    for record in history:
        date = record["date"][:10]
        subs = record.get("subscribers", 0)
        
        if prev_subs:
            change = subs - prev_subs
            if change > 0:
                change_str = f"+{change:,}"
            else:
                change_str = f"{change:,}"
        else:
            change_str = "-"
        
        print(f"{date:<12} {subs:<12,} {change_str:<12}")
        prev_subs = subs
    
    # 计算总趋势
    if len(history) >= 2:
        first = history[0].get("subscribers", 0)
        last = history[-1].get("subscribers", 0)
        total_change = last - first
        if total_change > 0:
            trend = f"📈 总增长 +{total_change:,}"
        elif total_change < 0:
            trend = f"📉 总下降 {total_change:,}"
        else:
            trend = "➡️ 持平"
        print(f"\n{trend}")

# 主入口
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="播客订阅跟踪工具")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("list", help="列出追踪的播客")
    subparsers.add_parser("update", help="更新所有播客的订阅量")
    
    add_parser = subparsers.add_parser("add", help="添加播客追踪")
    add_parser.add_argument("podcast_name", help="播客名称")
    
    trends_parser = subparsers.add_parser("trends", help="查看订阅趋势")
    trends_parser.add_argument("podcast_name", help="播客名称")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_podcast(args.podcast_name)
    elif args.command == "list":
        list_podcasts()
    elif args.command == "update":
        update_subscriptions()
    elif args.command == "trends":
        show_trends(args.podcast_name)
    else:
        parser.print_help()