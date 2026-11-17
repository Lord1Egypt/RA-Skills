#!/usr/bin/env python3
"""
定胆参考 — 基于多策略计算胆码
"""

import argparse, csv, sys
from collections import Counter


def load_history(path, lottery):
    data = []
    n = {"大乐透": 5, "排列3": 3, "排列5": 5, "七星彩": 7}[lottery]
    if lottery == "大乐透":
        n = 5
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            nums = [int(r[f"号码{i}"]) for i in range(1, n + 1)]
            data.append(nums)
    return data


def hot_strategy(data, top=3):
    """热号定胆"""
    counter = Counter()
    for nums in data:
        counter.update(nums)
    return [n for n, _ in counter.most_common(top)]


def missing_strategy(data, total_range):
    """冷号回补定胆（遗漏最大）"""
    counter = Counter()
    for nums in data:
        counter.update(nums)
    scored = []
    for n in total_range:
        miss = len(data) - counter.get(n, 0)
        scored.append((miss, n))
    return [n for _, n in sorted(scored, reverse=True)[:3]]


def last_freq_strategy(data):
    """近N期热号"""
    recent = data[-min(10, len(data)):]
    counter = Counter()
    for nums in recent:
        counter.update(nums)
    return [n for n, _ in counter.most_common(3)]


def adjacent_strategy(data, total_range):
    """邻号定胆(keyword: 上期号码±1)"""
    if not data:
        return []
    last = set(data[-1])
    adj = set()
    for n in last:
        if n - 1 in total_range:
            adj.add(n - 1)
        if n + 1 in total_range:
            adj.add(n + 1)
    return sorted(adj)[:5]


def interval_strategy(data, total_range):
    """等间隔定胆：上期间隔差值参考"""
    if len(data) < 3:
        return []
    last = data[-1]
    second = data[-2]
    intervals = {}
    for i in range(min(len(last), len(second))):
        diff = abs(last[i] - second[i])
        intervals.setdefault(diff, 0)
        intervals[diff] += 1
    if intervals:
        max_diff = max(intervals, key=intervals.get)
        candidates = sorted(total_range)
        return candidates[:3]
    return []


def main():
    ap = argparse.ArgumentParser(description="定胆参考 — 多策略胆码")
    ap.add_argument("file", help="历史开奖CSV")
    ap.add_argument("--lottery", default="大乐透", choices=["大乐透","排列3","排列5","七星彩"])
    ap.add_argument("--count", type=int, default=3, help="每策略胆码数量")
    args = ap.parse_args()

    if args.lottery == "大乐透":
        total_range = list(range(1, 36))
    else:
        total_range = list(range(10))

    try:
        data = load_history(args.file, args.lottery)
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        sys.exit(1)

    if len(data) < 2:
        print("❌ 至少需要2期数据")
        return

    print(f"📊 定胆参考 — {args.lottery} ({len(data)}期)")
    print("═" * 50)

    def show(name, nums):
        print(f"\n  {name}: {' '.join(f'{n:02d}' for n in nums)}")

    c = min(args.count, 5)

    hot = hot_strategy(data, c)
    show("🔥 热号定胆", hot)

    miss = missing_strategy(data, total_range)
    show("❄️ 冷号回补", miss[:c])

    recent = last_freq_strategy(data)
    show("📈 近期高频", recent[:c])

    adj = adjacent_strategy(data, set(total_range))
    if adj:
        show("↔️ 邻号定胆", adj[:c])

    # 综合参考
    combined = []
    seen = set()
    for n in hot + miss + recent:
        if n not in seen:
            combined.append(n)
            seen.add(n)
    combined = combined[:args.count]

    print(f"\n  {'─'*35}")
    print(f"  ⭐ 综合胆码: {' '.join(f'{n:02d}' for n in combined)}")
    print(f"  💡 提示: 胆码至少应含1-2个")

    # 大乐透后区定胆
    if args.lottery == "大乐透":
        back_data = []
        with open(args.file, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                b = [int(r[f"号码{i}"]) for i in range(6, 8)]
                back_data.append(b)
        bc = Counter()
        for b in back_data:
            bc.update(b)
        back_hot = [n for n, _ in bc.most_common(3)]
        print(f"\n  🔵 后区胆码: {' '.join(f'{n:02d}' for n in back_hot[:2])}")

    print("\n⚠️ 以上数据仅供统计参考，不构成投注建议。彩票具有随机性，请理性对待。")

if __name__ == "__main__":
    main()
