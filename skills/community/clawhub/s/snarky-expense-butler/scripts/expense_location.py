#!/usr/bin/env python3
# 地域消费统计 — 看看你的钱都喂了哪些商圈

import json
import sys
import os
from collections import defaultdict

DATA_FILE = os.environ.get('EXPENSE_DATA_FILE', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expense_records.json'))


def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ 消费记录文件不存在")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ 消费记录文件格式错误")
        sys.exit(1)


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_location_stats(data):
    """聚合所有带 location 的消费"""
    stats = defaultdict(lambda: {
        "total": 0,
        "count": 0,
        "categories": defaultdict(float),
        "dates": set(),
        "items": []
    })

    for record in data['records']:
        date = record['date']
        for item in record['items']:
            loc = item.get('location')
            if not loc:
                continue
            s = stats[loc]
            s['total'] += item['amount']
            s['count'] += 1
            s['categories'][item['category']] += item['amount']
            s['dates'].add(date)
            s['items'].append({
                'date': date,
                'category': item['category'],
                'amount': item['amount'],
                'note': item.get('note', '')
            })

    return stats


def show_summary(data):
    """地域汇总排名"""
    stats = get_location_stats(data)

    if not stats:
        print("📍 地域消费统计")
        print("━━━━━━━━━━━━━━━━━━")
        print("还没有任何消费带 location，快用 add_expense.py --location 记一笔吧！")
        print()
        print("💡 提示: python3 add_expense.py 餐饮 15 午餐 --location 福田cocopark")
        return

    # 按总消费排序
    sorted_locs = sorted(stats.items(), key=lambda x: x[1]['total'], reverse=True)

    # 计算总额用于标注
    grand_total = sum(s['total'] for s in stats.values())
    avg_total = grand_total / len(sorted_locs) if sorted_locs else 0

    print("📍 地域消费统计")
    print("━━━━━━━━━━━━━━━━━━")
    print(f"总覆盖地点: {len(sorted_locs)} | 带地点消费总额: ¥{abs(grand_total):.1f}")
    print()

    for i, (loc, s) in enumerate(sorted_locs):
        pct = abs(s['total']) / abs(grand_total) * 100 if grand_total != 0 else 0
        days = len(s['dates'])
        daily_avg = abs(s['total']) / days if days > 0 else 0

        # 标注
        if abs(s['total']) > avg_total * 2:
            tag = "🐷 吞金兽"
        elif abs(s['total']) < avg_total * 0.3:
            tag = "💰 省钱区"
        else:
            tag = ""

        print(f"{'🥇' if i==0 else '🥈' if i==1 else '🥉' if i==2 else '  '} {loc} {tag}")
        print(f"     总花费: ¥{abs(s['total']):.1f} ({pct:.0f}%) | {s['count']}笔 | {days}天 | 日均: ¥{abs(daily_avg):.1f}")

        # 分类分布
        cats = sorted(s['categories'].items(), key=lambda x: x[1], reverse=True)
        cat_str = " | ".join([f"{c}: ¥{abs(a):.0f}" for c, a in cats[:3]])
        print(f"     分类: {cat_str}")
        print()


def show_top(n):
    """前 N 高消费区域"""
    data = load_data()
    stats = get_location_stats(data)

    if not stats:
        print("还没有带 location 的记录")
        return

    sorted_locs = sorted(stats.items(), key=lambda x: x[1]['total'], reverse=True)[:n]

    print(f"📍 消费 Top {n} 地域")
    print("━━━━━━━━━━━━━━━━━━")

    for i, (loc, s) in enumerate(sorted_locs):
        print(f"  {i+1}. {loc}: ¥{abs(round(s['total'], 1))} ({s['count']}笔)")


def backfill(index, location):
    """给历史记录补地点。index=0 表示最近一条"""
    data = load_data()

    # 收集所有 items（倒序）
    all_items = []
    for record in reversed(data['records']):
        for item in reversed(record['items']):
            all_items.append((record, item))

    if index < 0 or index >= len(all_items):
        print(f"❌ 序号 {index} 超出范围，当前共有 {len(all_items)} 条记录（0 ~ {len(all_items)-1}）")
        return

    record, item = all_items[index]
    old_loc = item.get('location', '(无)')

    # 如果 item 没有 note，加一个提示
    item['location'] = location

    # 保存
    save_data(data)

    note = item.get('note', '')
    print(f"✅ 已更新第 {index} 条记录的地点:")
    print(f"   日期: {record['date']}")
    print(f"   分类: {item['category']} | ¥{abs(item['amount'])}")
    if note:
        print(f"   备注: {note}")
    print(f"   地点: {old_loc} → {location}")


def show_help():
    print("📍 地域消费统计工具")
    print("用法: python3 expense_location.py <命令>")
    print()
    print("命令:")
    print("  summary            - 地域汇总排名（默认）")
    print("  top <n>            - 前 N 高消费区域")
    print("  backfill <n> <地点> - 给第 n 条记录补地点（0=最近一条）")
    print()
    print("示例:")
    print("  python3 expense_location.py summary")
    print("  python3 expense_location.py top 5")
    print("  python3 expense_location.py backfill 0 南山海岸城")


def main():
    if len(sys.argv) < 2:
        # 默认显示 summary
        data = load_data()
        show_summary(data)
        return

    command = sys.argv[1]

    if command == "summary":
        data = load_data()
        show_summary(data)
    elif command == "top":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        show_top(n)
    elif command == "backfill":
        if len(sys.argv) < 4:
            print("❌ 用法: python3 expense_location.py backfill <序号> <地点>")
            print("   序号 0 = 最近一条记录")
            return
        index = int(sys.argv[2])
        location = sys.argv[3]
        backfill(index, location)
    elif command == "help":
        show_help()
    else:
        print(f"❌ 未知命令: {command}")
        show_help()


if __name__ == "__main__":
    main()
