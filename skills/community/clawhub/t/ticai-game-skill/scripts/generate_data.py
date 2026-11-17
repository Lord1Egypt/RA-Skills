#!/usr/bin/env python3
"""
体彩示例数据生成器 — 支持全部数字彩种 CSV 生成
"""

import csv, argparse, random, os
from datetime import datetime, timedelta

LOTTERY_META = {
    "大乐透": {
        "cols": "彩种,期号,开奖日期,号码1,号码2,号码3,号码4,号码5,号码6,号码7,奖池(亿),销量(亿)",
        "f_range": (1, 35),
        "b_range": (1, 12),
        "days": [0, 2, 5],  # 一/三/六
    },
    "排列3": {
        "cols": "彩种,期号,开奖日期,号码1,号码2,号码3",
        "d_range": (0, 9),
        "days": list(range(7)),
    },
    "排列5": {
        "cols": "彩种,期号,开奖日期,号码1,号码2,号码3,号码4,号码5",
        "d_range": (0, 9),
        "days": list(range(7)),
    },
    "七星彩": {
        "cols": "彩种,期号,开奖日期,号码1,号码2,号码3,号码4,号码5,号码6,号码7",
        "d_range": (0, 9),
        "days": [1, 4, 6],
    },
}

WEEKDAY_NAMES = ["一", "二", "三", "四", "五", "六", "日"]


def generate(lottery, count=20, start_date=None):
    """生成指定彩种的示例数据"""
    meta = LOTTERY_META[lottery]
    rows = []

    start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else datetime(2026, 6, 1)

    # 找到最近的符合开奖日的日期
    cur = start
    while cur.weekday() not in meta["days"]:
        cur += timedelta(days=1)

    for i in range(count):
        year = cur.year % 100
        seq = (cur - datetime(cur.year, 1, 1)).days + 1
        qihao = f"{year}{seq:03d}"

        if lottery == "大乐透":
            front = sorted(random.sample(range(meta["f_range"][0], meta["f_range"][1] + 1), 5))
            back = sorted(random.sample(range(meta["b_range"][0], meta["b_range"][1] + 1), 2))
            pool = round(random.uniform(8.0, 12.0), 2)
            sales = round(random.uniform(2.5, 3.5), 2)
            row = [lottery, qihao, cur.strftime("%Y-%m-%d")] + front + back + [pool, sales]
        else:
            digits = [random.randint(meta["d_range"][0], meta["d_range"][1])
                      for _ in range(3 if lottery == "排列3" else 5 if lottery == "排列5" else 7)]
            row = [lottery, qihao, cur.strftime("%Y-%m-%d")] + digits

        rows.append(row)

        # 下一期
        next_d = cur + timedelta(days=1)
        while next_d.weekday() not in meta["days"]:
            next_d += timedelta(days=1)
        cur = next_d

    return rows, meta["cols"]


def main():
    parser = argparse.ArgumentParser(description="体彩示例数据生成器")
    parser.add_argument("--lottery", default="大乐透", choices=list(LOTTERY_META.keys()),
                        help="彩种")
    parser.add_argument("--count", type=int, default=20, help="期数")
    parser.add_argument("--start", default="2026-06-01", help="起始日期 YYYY-MM-DD")
    parser.add_argument("--output", "-o", help="输出路径（默认打印到终端）")
    args = parser.parse_args()

    rows, cols = generate(args.lottery, args.count, args.start)
    headers = cols.split(",")

    if args.output:
        with open(args.output, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(headers)
            w.writerows(rows)
        print(f"✅ 已生成 {args.count} 期 {args.lottery} 数据 → {args.output}")
    else:
        print(",".join(headers))
        for r in rows:
            print(",".join(str(v) for v in r))


if __name__ == "__main__":
    main()
