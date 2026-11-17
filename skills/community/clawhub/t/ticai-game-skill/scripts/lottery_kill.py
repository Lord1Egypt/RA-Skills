#!/usr/bin/env python3
"""
杀号工具 — 多种杀号策略，过滤缩减号码池
"""

import argparse, sys
from itertools import combinations


def digit_sum(n):
    return sum(int(d) for d in str(n))


def last_digit_sum(nums):
    return sum(n % 10 for n in nums)


def parity_pattern(nums):
    return "".join("奇" if n % 2 else "偶" for n in nums)


def delta_kill(history, pos):
    """杀相邻两期差值重复号"""
    if len(history) < 2:
        return set()
    last = set(history[-1])
    second_last = set(history[-2])
    return last & second_last


def sum_tail_kill(total_range, sum_val):
    """和值尾杀号"""
    tail = sum_val % 10
    return {n for n in total_range if n % 10 == tail}


def mod_kill(total_range, base=3):
    """杀同路号: 返回当前最热路以外的号码"""
    return set()


def kill_by_last_digit(nums, digit_pool):
    """杀指定尾数号码"""
    killed = set()
    for n in nums:
        for d in digit_pool:
            if n % 10 == d:
                killed.add(n)
    return killed


def main():
    ap = argparse.ArgumentParser(description="杀号工具 — 多策略过滤")
    ap.add_argument("--pool", required=True, help="当前号码池 如 01-35 或 1,2,3,4,5")
    ap.add_argument("--lottery", default="大乐透", choices=["大乐透", "排列3", "排列5", "七星彩"])
    ap.add_argument("--position", help="杀位置 如 '前区' '后区' '百位' '十位' '个位'")
    ap.add_argument("--kill-tail", help="杀尾数 如 0,1,5")
    ap.add_argument("--kill-eoo", choices=["全奇","全偶","奇奇","奇偶","偶奇","偶偶"], help="杀排列3形态")
    ap.add_argument("--kill-sum-tail", type=int, help="杀和值尾 如 0")
    ap.add_argument("--kill-range", help="杀区间 如 1-10")
    ap.add_argument("--kill-ac", type=int, help="杀AC值" if False else "杀AC值（预留）")
    ap.add_argument("--kill-span", nargs=2, type=int, metavar=("MIN","MAX"), help="杀跨度不在范围")
    ap.add_argument("--history", help="历史开奖CSV（用于差值杀号）")
    ap.add_argument("--sections", type=int, default=0, help="分区个数(杀空区)")
    args = ap.parse_args()

    if "-" in args.pool and args.pool.count("-") == 1 and not any(c.isalpha() for c in args.pool):
        raw = args.pool.strip()
        if raw.startswith("0") and not raw.startswith("0-") and not raw.startswith("00-"):
            raw = raw.lstrip("0")
        parts = raw.split("-")
        try:
            lo, hi = int(parts[0]), int(parts[1])
            if 0 <= lo < hi:
                pool = set(range(lo, hi + 1))
            else:
                pool = set(map(int, args.pool.replace(",", " ").replace("-", " ").split()))
        except (ValueError, IndexError):
            pool = set(map(int, args.pool.replace(",", " ").replace("-", " ").split()))
    else:
        pool = set(map(int, args.pool.replace(",", " ").split()))

    original = len(pool)
    kills = {}

    # 1. 杀尾数
    if args.kill_tail:
        tails = set(map(int, args.kill_tail.split(",")))
        killed = {n for n in pool if n % 10 in tails}
        if killed:
            kills["尾数"] = killed
            pool -= killed

    # 2. 杀区间
    if args.kill_range:
        parts = args.kill_range.split("-")
        r = set(range(int(parts[0]), int(parts[1]) + 1))
        killed = pool & r
        if killed:
            kills["区间"] = killed
            pool -= killed

    # 3. 杀和值尾
    if args.kill_sum_tail is not None:
        killed = sum_tail_kill(pool, args.kill_sum_tail)
        if killed:
            kills["和值尾"] = killed
            pool -= killed

    # 4. 杀跨度过小/过大
    if args.kill_span:
        lo, hi = args.kill_span
        killed = {n for n in pool if n < lo or n > hi}
        if killed:
            kills["跨度"] = killed
            pool -= killed

    # 5. 分区杀号
    if args.sections:
        section_size = max(pool) // args.sections
        counts = {}
        for n in pool:
            sec = (n - 1) // section_size
            counts[sec] = counts.get(sec, 0) + 1
        if counts:
            min_sec = min(counts, key=counts.get)
            killed = {n for n in pool if (n - 1) // section_size == min_sec}
            if killed:
                kills[f"空区(第{min_sec+1}区)"] = killed
                pool -= killed

    # 6. 历史差值杀号
    if args.history:
        try:
            import csv
            with open(args.history, encoding="utf-8") as f:
                draw_data = []
                for r in csv.DictReader(f):
                    nums = [int(v) for k, v in r.items() if k.startswith("号码")]
                    draw_data.append(nums)
            if len(draw_data) >= 2:
                last = set(draw_data[-1])
                second = set(draw_data[-2])
                killed = last & second
                if killed:
                    kills["重复差值"] = killed
                    pool -= killed
        except Exception as e:
            print(f"⚠️ 历史文件处理异常: {e}")

    # 结果
    removed = original - len(pool)
    print(f"📊 杀号结果:")
    print(f"   原始池: {original} 个号码")
    if kills:
        for method, nums in kills.items():
            nums_str = " ".join(f"{n:02d}" for n in sorted(nums))
            print(f"   🗑️ {method}: 杀{len(nums)}个 → {nums_str}")
    print(f"   ✅ 剩余: {len(pool)} 个号码")
    if pool:
        print(f"   📋 剩余号码: {' '.join(f'{n:02d}' for n in sorted(pool))}")
    print(f"   📈 缩减率: {(1 - len(pool)/original)*100:.1f}%")


if __name__ == "__main__":
    main()
