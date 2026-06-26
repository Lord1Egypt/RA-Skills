#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球号码预测分析脚本（离线版）
从标准输入读取JSON格式的历史数据，输出三套预测方案及频次分析。

用法：
  echo '<json_data>' | python predict.py
  python predict.py --data '<json_string>'

输入JSON格式：
  [
    {"red": "06,09,14,16,25,32", "blue": "16", "date": "2026-04-19(日)"},
    ...
  ]
"""
import argparse
import json
import random
import sys


def build_freq(records):
    red_freq = {str(n).zfill(2): 0 for n in range(1, 34)}
    blue_freq = {str(n).zfill(2): 0 for n in range(1, 17)}
    for r in records:
        reds = [s.strip().zfill(2) for s in r["red"].split(",")]
        blue = r["blue"].strip().zfill(2)
        for n in reds:
            if n in red_freq:
                red_freq[n] += 1
        if blue in blue_freq:
            blue_freq[blue] += 1
    return red_freq, blue_freq


def weighted_sample(freq_dict, k, exclude=None):
    exclude = exclude or set()
    items = [(num, cnt) for num, cnt in freq_dict.items() if num not in exclude]
    weights = [cnt + 1 for _, cnt in items]
    chosen = []
    remaining = list(range(len(items)))
    while len(chosen) < k and remaining:
        total = sum(weights[i] for i in remaining)
        r = random.uniform(0, total)
        acc = 0.0
        for i in remaining:
            acc += weights[i]
            if acc >= r:
                chosen.append(items[i][0])
                remaining.remove(i)
                break
    return chosen


def analyze(records):
    red_freq, blue_freq = build_freq(records)
    red_sorted = sorted(red_freq.items(), key=lambda x: -x[1])
    blue_sorted = sorted(blue_freq.items(), key=lambda x: -x[1])

    hot_reds = [n for n, _ in red_sorted[:10]]
    cold_reds = [n for n, _ in red_sorted[-10:]]
    hot_blues = [n for n, _ in blue_sorted[:5]]

    plan1_red = sorted(hot_reds[:6])
    plan1_blue = hot_blues[0]

    plan2_red = sorted(hot_reds[:4] + cold_reds[:2])
    plan2_blue = hot_blues[1] if len(hot_blues) > 1 else hot_blues[0]

    # 方案三：均衡分区（低区1-11，中区12-22，高区23-33各取2个）
    def zone_pick(zone_start, zone_end, n):
        zone = {k: v for k, v in red_freq.items()
                if zone_start <= int(k) <= zone_end}
        z_sorted = sorted(zone.items(), key=lambda x: -x[1])
        return [z_sorted[i][0] for i in range(min(n, len(z_sorted)))]

    plan3_red = sorted(zone_pick(1, 11, 2) + zone_pick(12, 22, 2) + zone_pick(23, 33, 2))
    # 蓝球取中等频次
    mid_idx = len(blue_sorted) // 2
    plan3_blue = blue_sorted[mid_idx][0]

    return {
        "plans": [
            {
                "name": "方案一：高频热号",
                "desc": "选取近期出现频率最高的6个红球，搭配最热蓝球",
                "red_balls": plan1_red,
                "blue_ball": plan1_blue,
            },
            {
                "name": "方案二：冷热结合",
                "desc": "4个高频红球 + 2个低频冷球，次热蓝球",
                "red_balls": plan2_red,
                "blue_ball": plan2_blue,
            },
            {
                "name": "方案三：均衡分区",
                "desc": "低/中/高区各取2个，覆盖全号码段",
                "red_balls": plan3_red,
                "blue_ball": plan3_blue,
            },
        ],
        "red_freq_top10": [{"num": n, "count": c} for n, c in red_sorted[:10]],
        "red_freq_cold5": [{"num": n, "count": c} for n, c in red_sorted[-5:]],
        "blue_freq_all": [{"num": n, "count": c} for n, c in blue_sorted],
        "periods_analyzed": len(records),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="JSON格式的历史数据字符串")
    args = parser.parse_args()

    if args.data:
        raw = args.data
    else:
        raw = sys.stdin.read().strip()

    try:
        records = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    result = analyze(records)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
