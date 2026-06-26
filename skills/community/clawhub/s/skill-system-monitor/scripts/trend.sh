#!/bin/bash
# 7日趋势图（QuickChart）

HISTORY_DIR="/home/app/.openclaw/skills/skill-system-monitor/history"
DAYS=7

python3 << 'PYEOF'
import os
import json
import urllib.parse
from datetime import datetime, timedelta
from collections import defaultdict

HISTORY_DIR = "/home/app/.openclaw/skills/skill-system-monitor/history"
DAYS = 7

day_disk = defaultdict(list)
day_mem = defaultdict(list)

cutoff = datetime.now() - timedelta(days=DAYS)

for filename in os.listdir(HISTORY_DIR):
    if not filename.endswith('.json'):
        continue
    
    filepath = os.path.join(HISTORY_DIR, filename)
    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
    
    if mtime < cutoff:
        continue
    
    day = mtime.strftime('%Y-%m-%d')
    
    try:
        with open(filepath) as f:
            content = f.read()
            import re
            percents = re.findall(r'"percent":\s*(\d+)', content)
            if len(percents) >= 2:
                day_disk[day].append(int(percents[0]))
                day_mem[day].append(int(percents[-1]))
    except:
        continue

if not day_disk:
    print("⚠️ 无历史数据")
    exit(0)

sorted_days = sorted(day_disk.keys())

# 今天和昨天对比
today = datetime.now().strftime('%Y-%m-%d')
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

print("📈 7日系统监控趋势")
print("================================")

if today in day_disk and yesterday in day_disk:
    today_disk = sum(day_disk[today]) // len(day_disk[today])
    yesterday_disk = sum(day_disk[yesterday]) // len(day_disk[yesterday])
    today_mem = sum(day_mem[today]) // len(day_mem[today])
    yesterday_mem = sum(day_mem[yesterday]) // len(day_mem[yesterday])
    
    disk_diff = today_disk - yesterday_disk
    mem_diff = today_mem - yesterday_mem
    
    disk_sign = "+" if disk_diff > 0 else ""
    mem_sign = "+" if mem_diff > 0 else ""
    
    print(f"💾 硬盘: {yesterday_disk}% → {today_disk}% ({disk_sign}{disk_diff}%)")
    print(f"🧠 内存: {yesterday_mem}% → {today_mem}% ({mem_sign}{mem_diff}%)")
    
    if disk_diff > 5:
        print("⚠️ 硬盘使用增长较快！")
    if mem_diff > 10:
        print("⚠️ 内存使用增长较快！")
else:
    print("⚠️ 缺少昨日数据，无法对比")

# QuickChart 链接
labels = [d[5:] for d in sorted_days]
disk_data = [sum(day_disk[d]) // len(day_disk[d]) for d in sorted_days]
mem_data = [sum(day_mem[d]) // len(day_mem[d]) for d in sorted_days]

config = {
    "type": "line",
    "data": {
        "labels": labels,
        "datasets": [
            {
                "label": "Disk (%)",
                "data": disk_data,
                "borderColor": "#3498db",
                "fill": False
            },
            {
                "label": "Memory (%)",
                "data": mem_data,
                "borderColor": "#e74c3c",
                "fill": False
            }
        ]
    },
    "options": {
        "title": {
            "display": True,
            "text": "7-Day System Monitor"
        }
    }
}

encoded = urllib.parse.quote(json.dumps(config))
print()
print("📊 图表:")
print(f"https://quickchart.io/chart?w=500&h=300&c={encoded}")
PYEOF
