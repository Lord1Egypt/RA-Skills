#!/usr/bin/env python3
"""查询技能调用统计"""
import json, sys, os
from datetime import datetime, timezone, timedelta
from collections import defaultdict

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'usage.json')

def get_date_range(dim: str):
    now = datetime.now(timezone.utc)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    if dim == '日':
        start = today
        label = f"{now.strftime('%Y年%m月%d日')}"
    elif dim == '周':
        start = today - timedelta(days=now.weekday())
        label = f"本周（{start.strftime('%m月%d日')} 至 {today.strftime('%m月%d日')}）"
    elif dim == '月':
        start = today.replace(day=1)
        label = f"{now.strftime('%Y年%m月')}"
    elif dim == '季':
        quarter = (now.month - 1) // 3 + 1
        month_start = (quarter - 1) * 3 + 1
        start = now.replace(month=month_start, day=1)
        label = f"{now.year}年第{quarter}季度"
    elif dim == '年':
        start = today.replace(month=1, day=1)
        label = f"{now.year}年"
    else:
        start = today
        label = dim

    return start, label

def load_records():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f).get('records', [])

def query(dim: str = '周'):
    records = load_records()
    start, label = get_date_range(dim)

    filtered = []
    for r in records:
        try:
            called = datetime.fromisoformat(r['called_at'])
            if called >= start:
                filtered.append(r)
        except:
            pass

    stats = defaultdict(int)
    for r in filtered:
        stats[r['skill']] += 1

    total = len(filtered)

    if total == 0:
        return f"技能使用报告 - {label}\n\n暂无记录。"

    sorted_skills = sorted(stats.items(), key=lambda x: -x[1])

    lines = [f"技能使用报告 - {label}\n"]
    lines.append(f"\n总调用次数：{total}次\n")

    for skill, count in sorted_skills:
        pct = count / total * 100
        if pct >= 80:
            emoji = '🟢'
        elif pct >= 30:
            emoji = '🟡'
        else:
            emoji = '🔵'
        lines.append(f"{emoji} {skill}")
        lines.append(f"   {count}次 · {pct:.1f}%")

    return '\n'.join(lines)

if __name__ == '__main__':
    dim = sys.argv[1] if len(sys.argv) > 1 else '周'
    print(query(dim))
