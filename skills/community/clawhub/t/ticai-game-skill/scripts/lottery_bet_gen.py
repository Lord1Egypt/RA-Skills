#!/usr/bin/env python3
"""
复式胆拖全组合生成器 — 生成所有号码组合，输出到 CSV
"""

import csv, argparse, math, sys
from itertools import combinations


def comb_count(n, k):
    return math.comb(n, k) if k <= n else 0


def gen_dlt(front_pool, back_pool, front_dan=None, back_dan=None):
    front_dan = front_dan or []
    back_dan = back_dan or []
    f_need = 5 - len(front_dan)
    b_need = 2 - len(back_dan)
    f_pool = [n for n in front_pool if n not in front_dan]
    b_pool = [n for n in back_pool if n not in back_dan]

    total = comb_count(len(f_pool), f_need) * comb_count(len(b_pool), b_need)
    return total


def gen_dlt_full(front_pool, back_pool, front_dan=None, back_dan=None):
    front_dan = front_dan or []
    back_dan = back_dan or []
    f_need = 5 - len(front_dan)
    b_need = 2 - len(back_dan)
    f_pool = [n for n in front_pool if n not in front_dan]
    b_pool = [n for n in back_pool if n not in back_dan]

    rows = []
    for f_comb in combinations(f_pool, f_need):
        front = sorted(front_dan + list(f_comb))
        for b_comb in combinations(b_pool, b_need):
            back = sorted(back_dan + list(b_comb))
            rows.append(front + back)
    return rows


def gen_pl3_full(picks):
    """picks = [百选号, 十选号, 个选号]"""
    rows = []
    for b in picks[0]:
        for s in picks[1]:
            for g in picks[2]:
                rows.append([b, s, g])
    return rows


def gen_pl5_full(picks):
    rows = [[]]
    for pos in picks:
        rows = [r + [p] for r in rows for p in pos]
    return rows


def main():
    ap = argparse.ArgumentParser(description="复式胆拖全组合生成器")
    ap.add_argument("--lottery", default="大乐透", choices=["大乐透", "排列3", "排列5"])
    ap.add_argument("--front", help="前区选号(逗号分隔) 如 01,02,03,04,05,06,07")
    ap.add_argument("--back", help="后区选号(逗号分隔) 如 01,02,03")
    ap.add_argument("--front-dan", help="前区胆码(逗号分隔)")
    ap.add_argument("--back-dan", help="后区胆码(逗号分隔)")
    ap.add_argument("--output", "-o", help="输出CSV路径（默认仅打印注数）")
    ap.add_argument("--max", type=int, default=5000, help="最大输出注数(默认5000)")
    args = ap.parse_args()

    if args.lottery == "大乐透":
        front = [int(n) for n in args.front.split(",")] if args.front else list(range(1, 36))
        back = [int(n) for n in args.back.split(",")] if args.back else list(range(1, 13))
        f_dan = [int(n) for n in args.front_dan.split(",")] if args.front_dan else None
        b_dan = [int(n) for n in args.back_dan.split(",")] if args.back_dan else None

        total = gen_dlt(front, back, f_dan, b_dan)
        print(f"📊 组合注数: {total:,} 注")
        print(f"💰 金额: {total * 2:,} 元 (追加: {total * 3:,} 元)")

        if total > args.max:
            print(f"⚠️  注数超过限制({args.max})，不生成明细")
            return

        if args.output:
            rows = gen_dlt_full(front, back, f_dan, b_dan)
            with open(args.output, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["号码1","号码2","号码3","号码4","号码5","号码6","号码7"])
                w.writerows(rows)
            print(f"✅ 已输出 {len(rows)} 注 → {args.output}")

    elif args.lottery in ("排列3", "排列5"):
        if not args.front:
            print("❌ 请指定选号，如 --front 1,2,3")
            return
        picks_str = args.front.split("/")
        n = 3 if args.lottery == "排列3" else 5
        if len(picks_str) == 1:
            picks = [list(map(int, picks_str[0].split(",")))] * n
        else:
            picks = [list(map(int, p.split(","))) for p in picks_str]

        total = 1
        for p in picks:
            total *= len(p)
        print(f"📊 直选定位复式: {'×'.join(str(len(p)) for p in picks)} = {total:,} 注")
        print(f"💰 金额: {total * 2:,} 元")

        if total > args.max:
            print(f"⚠️  注数超过限制({args.max})，不生成明细")
            return

        if args.output:
            if args.lottery == "排列3":
                rows = gen_pl3_full(picks)
            else:
                rows = gen_pl5_full(picks)
            with open(args.output, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow([f"位置{i+1}" for i in range(n)])
                w.writerows(rows)
            print(f"✅ 已输出 {len(rows)} 注 → {args.output}")


if __name__ == "__main__":
    main()
