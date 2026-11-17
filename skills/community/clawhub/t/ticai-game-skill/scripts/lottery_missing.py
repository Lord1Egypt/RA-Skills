#!/usr/bin/env python3
"""
遗漏深度分析 — 号码遗漏值统计、排序与回补信号检测
"""

import csv, argparse
from collections import Counter

def load_dlt(path):
    data = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            f_nums = [int(r[f"号码{i}"]) for i in range(1, 6)]
            b_nums = [int(r[f"号码{i}"]) for i in range(6, 8)]
            data.append((r["期号"], f_nums, b_nums))
    return data

def load_digital(path, n):
    data = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            nums = [int(r[f"号码{i}"]) for i in range(1, n + 1)]
            data.append((r["期号"], nums))
    return data

def compute_missing(data, total_range, front_col=True):
    """计算遗漏: 从最近一期往前推算"""
    missing = {n: 0 for n in total_range}
    appeared = set()
    for qihao, *rest in reversed(data):
        nums = rest[0] if len(rest) == 1 else rest[0]
        for n in total_range:
            if n in nums:
                missing[n] = 0
                appeared.add(n)
            else:
                missing[n] += 1
    # 从未出现的号码设为极大值
    for n in total_range:
        if n not in appeared:
            missing[n] = len(data)
    return missing

def main():
    ap = argparse.ArgumentParser(description="遗漏深度分析")
    ap.add_argument("file", help="CSV 文件")
    ap.add_argument("--lottery", default="大乐透", choices=["大乐透", "排列3", "排列5", "七星彩"])
    ap.add_argument("--top", type=int, default=15, help="显示TOP N")
    args = ap.parse_args()

    if args.lottery == "大乐透":
        data = load_dlt(args.file)
        f_range = list(range(1, 36))
        b_range = list(range(1, 13))
        front_miss = compute_missing(data, f_range)
        back_miss = compute_missing(data, b_range)
    elif args.lottery == "排列3":
        data = load_digital(args.file, 3)
        f_range = list(range(10))
        front_miss = compute_missing(data, f_range)
    elif args.lottery == "排列5":
        data = load_digital(args.file, 5)
        f_range = list(range(10))
        front_miss = compute_missing(data, f_range)
    elif args.lottery == "七星彩":
        data = load_digital(args.file, 7)
        f_range = list(range(10))
        front_miss = compute_missing(data, f_range)

    if not data:
        print("❌ 无数据")
        return

    total = len(data)
    sorted_miss = sorted(front_miss.items(), key=lambda x: -x[1])

    print(f"📊 遗漏分析 — {args.lottery} (共{total}期)")
    print("═" * 50)

    # 冷号 TOP
    print(f"\n❄️  冷号 TOP{min(args.top, len(sorted_miss))} (遗漏最大):")
    print(f"   {'号码':<6} {'遗漏':<8} {'状态':<10}")
    print(f"   {'─'*22}")
    for n, miss in sorted_miss[:args.top]:
        status = "❄️冷" if miss >= 16 else "🌡温" if miss >= 6 else "🔥热"
        print(f"   {n:02d}     {miss}期     {status}")

    # 热号 TOP
    sorted_hot = sorted(front_miss.items(), key=lambda x: x[1])
    print(f"\n🔥 热号 TOP{min(args.top, len(sorted_hot))} (遗漏最小):")
    for n, miss in sorted_hot[:args.top]:
        print(f"   {n:02d}     {miss}期")

    # 回补信号
    max_miss = max(front_miss.values())
    print(f"\n⚠️  回补信号 (遗漏 > 均值 + 标准差):")
    avg = sum(front_miss.values()) / len(front_miss)
    std = (sum((v - avg)**2 for v in front_miss.values()) / len(front_miss)) ** 0.5
    threshold = avg + std
    rebound = [(n, m) for n, m in sorted_miss if m > threshold]
    for n, m in rebound[:10]:
        bar = "█" * min(m, 30)
        print(f"   {n:02d}  遗漏{m}期 {'>' if m > threshold else '<'} {avg:.0f}+{std:.0f}  {bar} ⬆️关注反弹")

    if args.lottery == "大乐透":
        print(f"\n🔵 后区遗漏:")
        for n, m in sorted(back_miss.items(), key=lambda x: -x[1])[:6]:
            print(f"   {n:02d}  遗漏{m}期")

    # 遗漏分布
    cold = sum(1 for m in front_miss.values() if m >= 16)
    warm = sum(1 for m in front_miss.values() if 6 <= m < 16)
    hot = sum(1 for m in front_miss.values() if 0 < m < 6)
    never = sum(1 for m in front_miss.values() if m >= total)
    print(f"\n📊 遗漏分布: 冷{cold}个 / 温{warm}个 / 热{hot}个{' / 从未出现'+str(never) if never else ''}")


if __name__ == "__main__":
    main()
