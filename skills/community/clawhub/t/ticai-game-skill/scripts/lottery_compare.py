#!/usr/bin/env python3
"""
号码对比器 — 核对自选号码是否中奖，精确到奖级
"""

import csv, argparse, sys
from itertools import combinations


def parse_dlt_csv(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            front = sorted(int(r[f"号码{i}"]) for i in range(1, 6))
            back = sorted(int(r[f"号码{i}"]) for i in range(6, 8))
            rows.append((r["期号"], front, back))
    return rows


def parse_digital_csv(path, n):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            nums = [int(r[f"号码{i}"]) for i in range(1, n + 1)]
            rows.append((r["期号"], nums))
    return rows


def match_dlt(my_front, my_back, draw_front, draw_back):
    f_match = len(set(my_front) & set(draw_front))
    b_match = len(set(my_back) & set(draw_back))
    return f_match, b_match


def dlt_prize_level(fm, bm):
    if fm == 5 and bm == 2: return "一等奖 🏆"
    if fm == 5 and bm == 1: return "二等奖"
    if fm == 5 or (fm == 4 and bm == 2): return "三等奖"
    if fm == 4 and bm == 1: return "四等奖"
    if fm == 4 or (fm == 3 and bm == 2): return "五等奖"
    if (fm == 3 and bm == 1) or (fm == 2 and bm == 2): return "六等奖"
    if fm == 3 or (fm == 2 and bm == 1) or (fm == 1 and bm == 2) or bm == 2: return "七等奖"
    return "未中奖"


def match_pl3(my_digits, draw_digits):
    direct = sum(1 for i in range(3) if my_digits[i] == draw_digits[i])
    my_set, draw_set = set(my_digits), set(draw_digits)
    group = len(my_set & draw_set)
    return direct, group


def main():
    ap = argparse.ArgumentParser(description="号码对比 — 核对自己的号码是否中奖")
    ap.add_argument("nums", help="自选号码 如 '05 12 19 26 33 + 03 10'")
    ap.add_argument("--draw", "-d", help="开奖CSV文件")
    ap.add_argument("--lottery", default="大乐透", choices=["大乐透", "排列3", "排列5", "七星彩"])
    ap.add_argument("--qihao", help="指定期号, 默认对比全部")
    args = ap.parse_args()

    parts = args.nums.strip().split()
    if args.lottery == "大乐透":
        try:
            sep = parts.index("+")
            my_front = list(map(int, parts[:sep]))
            my_back = list(map(int, parts[sep + 1:]))
        except ValueError:
            my_front = list(map(int, parts[:5]))
            my_back = list(map(int, parts[5:]))
    else:
        my_digits = list(map(int, parts))

    draws = None
    if args.draw:
        try:
            if args.lottery == "大乐透":
                draws = parse_dlt_csv(args.draw)
            elif args.lottery == "排列3":
                draws = parse_digital_csv(args.draw, 3)
            elif args.lottery == "排列5":
                draws = parse_digital_csv(args.draw, 5)
            elif args.lottery == "七星彩":
                draws = parse_digital_csv(args.draw, 7)
        except Exception as e:
            print(f"❌ 读取开奖文件失败: {e}")
            sys.exit(1)

    if not draws:
        print("❌ 未找到开奖数据")
        return

    print(f"📋 自选号码: {' '.join(f'{n:02d}' for n in my_front)} + {' '.join(f'{n:02d}' for n in my_back)}" if args.lottery == "大乐透"
          else f"📋 自选号码: {' '.join(map(str, my_digits))}")
    print("═" * 50)

    matched = False
    for qihao, *rest in draws:
        if args.qihao and qihao != args.qihao:
            continue
        if args.lottery == "大乐透":
            draw_front, draw_back = rest
            fm, bm = match_dlt(my_front, my_back, draw_front, draw_back)
            level = dlt_prize_level(fm, bm)
            if level != "未中奖":
                matched = True
                print(f"✅ {qihao}: 前区中{fm}个 后区中{bm}个 → {level}")
            elif args.qihao:
                print(f"❌ {qihao}: 前区中{fm}个 后区中{bm}个 → 未中奖")
        else:
            draw_digits = rest[0]
            if args.lottery == "排列3":
                direct, group = match_pl3(my_digits, draw_digits)
                if direct == 3:
                    matched = True
                    print(f"✅ {qihao}: 直选中奖！")
                elif group == 3 and len(set(my_digits)) in (2, 3):
                    level = "组选3" if len(set(my_digits)) == 2 else "组选6"
                    matched = True
                    print(f"✅ {qihao}: {level}中奖！(直位{3 - direct}位)")
                elif args.qihao:
                    print(f"❌ {qihao}: 直位{3 - direct}位 未中奖")
            elif args.lottery in ("排列5", "七星彩"):
                n = len(my_digits)
                direct = sum(1 for i in range(n) if my_digits[i] == draw_digits[i])
                all_match = direct == n
                if all_match:
                    matched = True
                    print(f"✅ {qihao}: 全部中奖！")
                elif args.qihao:
                    print(f"❌ {qihao}: 中{direct}/{n}位")

    if not matched and not args.qihao:
        print("😅 未查找到中奖记录")

    print("\n⚠️ 以上核对结果仅供个人验证使用，不构成投注依据。彩票具有随机性，请理性对待。")


if __name__ == "__main__":
    main()
