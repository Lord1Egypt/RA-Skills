#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
福利彩票（双色球）开奖数据查询与预测脚本
用法：
  python lottery.py --mode latest
  python lottery.py --mode history [--count 10]
  python lottery.py --mode predict
"""

import argparse
import json
import math
import random
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

# ============================================================
# 配置
# ============================================================
API_URL = "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=30&pageNo=1&pageSize=30&systemType=PC"

PRIZE_NAMES = {
    1: "一等奖", 2: "二等奖", 3: "三等奖",
    4: "四等奖", 5: "五等奖", 6: "六等奖",
}

# ============================================================
# 工具函数
# ============================================================

def fetch_json(url: str) -> dict:
    """HTTP GET，返回 JSON dict"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            if isinstance(data, dict) and data.get("state") == 0:
                return data
            raise RuntimeError(f"接口返回异常：{data.get('message', '未知错误')}")
    except Exception as e:
        raise RuntimeError(f"请求失败：{e}")


def format_money(value: str) -> str:
    """将元数字格式化为亿/万单位"""
    try:
        n = float(value)
    except (ValueError, TypeError):
        return str(value)
    if n >= 1e8:
        return f"{n / 1e8:.2f} 亿元"
    if n >= 1e4:
        return f"{n / 1e4:.2f} 万元"
    return f"{n:,.0f} 元"


def parse_balls(record: dict):
    """从 record 解析红球列表和蓝球字符串"""
    reds = [s.strip().zfill(2) for s in record["red"].split(",")]
    blue = record["blue"].strip().zfill(2)
    return reds, blue


def next_draw_info() -> str:
    """计算距下次开奖的倒计时字符串（北京时间）"""
    tz_cst = timezone(timedelta(hours=8))
    now = datetime.now(tz_cst)
    draw_days = {1, 3, 5}  # 周一=0 … 周日=6，周二=1,周四=3,周六=5
    draw_hour, draw_min = 21, 15

    for delta in range(8):
        candidate = now + timedelta(days=delta)
        if candidate.weekday() in draw_days:
            target = candidate.replace(hour=draw_hour, minute=draw_min, second=0, microsecond=0)
            if target > now:
                diff = target - now
                total_sec = int(diff.total_seconds())
                h = total_sec // 3600
                m = (total_sec % 3600) // 60
                s = total_sec % 60
                weekday_map = ["一", "二", "三", "四", "五", "六", "日"]
                date_str = f"{target.month}月{target.day}日（周{weekday_map[target.weekday()]}）"
                return f"{h:02d}:{m:02d}:{s:02d}（{date_str} 21:15）"
    return "即将开奖"


def load_data() -> list:
    """拉取接口数据，返回列表（最新在前）"""
    result = fetch_json(API_URL)
    data = result.get("result", [])
    if not data:
        raise ValueError("接口返回数据为空")
    return data


# ============================================================
# 模式：最新开奖
# ============================================================

def mode_latest(data: list):
    r = data[0]
    reds, blue = parse_balls(r)

    output = {
        "mode": "latest",
        "date": r.get("date", ""),
        "red_balls": reds,
        "blue_ball": blue,
        "pool_money": format_money(r.get("poolmoney", "0")),
        "sales": format_money(r.get("sales", "0")),
        "prize_info": r.get("content", ""),
        "prize_grades": [],
        "next_draw_countdown": next_draw_info(),
    }

    for g in r.get("prizegrades", []):
        t = int(g.get("type", 0))
        output["prize_grades"].append({
            "name": PRIZE_NAMES.get(t, f"{t}等奖"),
            "count": g.get("typenum", "0"),
            "money": format_money(g.get("typemoney", "0")),
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============================================================
# 模式：往期历史
# ============================================================

def mode_history(data: list, count: int):
    count = min(count, len(data))
    records = []
    for r in data[:count]:
        reds, blue = parse_balls(r)
        records.append({
            "date": r.get("date", ""),
            "red_balls": reds,
            "blue_ball": blue,
            "pool_money": format_money(r.get("poolmoney", "0")),
        })

    output = {
        "mode": "history",
        "count": count,
        "records": records,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============================================================
# 模式：预测
# ============================================================

def build_freq(data: list):
    """统计红球/蓝球历史频次"""
    red_freq = {str(n).zfill(2): 0 for n in range(1, 34)}
    blue_freq = {str(n).zfill(2): 0 for n in range(1, 17)}

    for r in data:
        reds, blue = parse_balls(r)
        for n in reds:
            if n in red_freq:
                red_freq[n] += 1
        if blue in blue_freq:
            blue_freq[blue] += 1

    return red_freq, blue_freq


def weighted_sample_red(freq: dict, k: int) -> list:
    """按频次加权随机抽取 k 个红球"""
    items = list(freq.items())
    weights = [v + 1 for _, v in items]  # +1 避免零权重
    chosen = set()
    attempts = 0
    while len(chosen) < k and attempts < 300:
        attempts += 1
        total = sum(w for i, (_, _) in enumerate(items) if items[i][0] not in chosen for w in [weights[i]])
        if total <= 0:
            break
        r = random.uniform(0, total)
        acc = 0.0
        for i, (num, _) in enumerate(items):
            if num in chosen:
                continue
            acc += weights[i]
            if acc >= r:
                chosen.add(num)
                break
    # 补足
    for num, _ in sorted(items, key=lambda x: -x[1]):
        if len(chosen) >= k:
            break
        chosen.add(num)
    return sorted(chosen)


def weighted_sample_blue(freq: dict) -> str:
    """按频次加权随机抽取1个蓝球"""
    items = list(freq.items())
    weights = [v + 1 for _, v in items]
    total = sum(weights)
    r = random.uniform(0, total)
    acc = 0.0
    for i, (num, _) in enumerate(items):
        acc += weights[i]
        if acc >= r:
            return num
    return items[0][0]


def mode_predict(data: list):
    if len(data) < 3:
        print(json.dumps({"error": "历史数据不足，无法分析"}, ensure_ascii=False))
        return

    red_freq, blue_freq = build_freq(data)
    n_periods = len(data)

    red_sorted = sorted(red_freq.items(), key=lambda x: -x[1])
    blue_sorted = sorted(blue_freq.items(), key=lambda x: -x[1])

    hot_reds = [num for num, _ in red_sorted[:10]]
    cold_reds = [num for num, _ in red_sorted[-10:]]
    hot_blues = [num for num, _ in blue_sorted[:5]]

    # 方案一：高频热号
    plan1_red = sorted(hot_reds[:6])
    plan1_blue = hot_blues[0]

    # 方案二：冷热结合
    plan2_red = sorted(hot_reds[:4] + cold_reds[:2])
    plan2_blue = hot_blues[1] if len(hot_blues) > 1 else hot_blues[0]

    # 方案三：加权随机
    plan3_red = weighted_sample_red(red_freq, 6)
    plan3_blue = weighted_sample_blue(blue_freq)

    output = {
        "mode": "predict",
        "periods_analyzed": n_periods,
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
                "name": "方案三：加权随机",
                "desc": "按历史频次加权随机抽取，每次不同",
                "red_balls": plan3_red,
                "blue_ball": plan3_blue,
            },
        ],
        "red_freq_top10": [{"num": num, "count": cnt} for num, cnt in red_sorted[:10]],
        "red_freq_cold10": [{"num": num, "count": cnt} for num, cnt in red_sorted[-10:]],
        "blue_freq_all": [{"num": num, "count": cnt} for num, cnt in blue_sorted],
        "next_draw_countdown": next_draw_info(),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="福利彩票双色球查询工具")
    parser.add_argument("--mode", choices=["latest", "history", "predict"],
                        default="latest", help="查询模式")
    parser.add_argument("--count", type=int, default=10,
                        help="history 模式查询期数（最多15）")
    args = parser.parse_args()

    try:
        data = load_data()
    except Exception as e:
        print(json.dumps({"error": f"数据加载失败：{e}"}, ensure_ascii=False))
        sys.exit(1)

    if args.mode == "latest":
        mode_latest(data)
    elif args.mode == "history":
        mode_history(data, args.count)
    elif args.mode == "predict":
        mode_predict(data)


if __name__ == "__main__":
    main()
