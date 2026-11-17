#!/usr/bin/env python3
"""
双色球智能分析生成器
基于 SQLite 数据库中的累计历史数据，做冷热统计、特征分布分析和规则过滤。
仅生成免费分析报告。付费推荐号码由 service.py 在支付验证后单独生成。
"""
import os
import random
import sqlite3
import sys
from collections import Counter
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ssq_data.db")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "最新分析结果.md")

# ============================================================
# 1. 数据库读取
# ============================================================

def get_recent_draws(conn, n=20):
    """获取最近 n 期开奖数据"""
    c = conn.cursor()
    c.execute("""
        SELECT code, red1, red2, red3, red4, red5, red6, blue, draw_date
        FROM draws ORDER BY code DESC LIMIT ?
    """, (n,))
    rows = c.fetchall()
    draws = []
    for row in rows:
        draws.append({
            "code": row[0],
            "reds": sorted([row[1], row[2], row[3], row[4], row[5], row[6]]),
            "blue": row[7],
            "date": row[8],
        })
    return draws


def get_historical_draws(conn, n=100):
    """获取历史 n 期完整数据"""
    c = conn.cursor()
    c.execute("""
        SELECT code, red1, red2, red3, red4, red5, red6, blue, draw_date
        FROM draws ORDER BY code DESC LIMIT ?
    """, (n,))
    rows = c.fetchall()
    draws = []
    for row in rows:
        draws.append({
            "code": row[0],
            "reds": sorted([row[1], row[2], row[3], row[4], row[5], row[6]]),
            "blue": row[7],
            "date": row[8],
        })
    return draws


# ============================================================
# 2. 红球冷热属性
# ============================================================

HOT_THRESHOLD = 6
WARM_THRESHOLD = 3
COLD_THRESHOLD = 2


def compute_red_stats(draws):
    """统计红球出现频率和热度"""
    freq = Counter()
    for draw in draws:
        for r in draw["reds"]:
            freq[r] += 1

    recent = draws[:20] if len(draws) >= 20 else draws
    recent_freq = Counter()
    for draw in recent:
        for r in draw["reds"]:
            recent_freq[r] += 1

    stats = {}
    for n in range(1, 34):
        total = freq.get(n, 0)
        rec = recent_freq.get(n, 0)
        if rec >= HOT_THRESHOLD:
            attr = "🔥 热号"
        elif rec >= WARM_THRESHOLD:
            attr = "⚡ 温号"
        else:
            attr = "❄️ 冷号"
        # 计算遗漏期数
        missing = 0
        for draw in reversed(recent):
            if n in draw["reds"]:
                break
            missing += 1
        stats[n] = {"frequency": total, "recent": rec, "attribute": attr, "missing": missing}

    return stats


# ============================================================
# 3. 蓝球统计
# ============================================================

def compute_blue_stats(draws):
    """统计蓝球出现频率"""
    freq = Counter()
    for draw in draws:
        freq[draw["blue"]] += 1

    recent = draws[:20] if len(draws) >= 20 else draws
    recent_freq = Counter()
    for draw in recent:
        recent_freq[draw["blue"]] += 1

    stats = {}
    for n in range(1, 17):
        total = freq.get(n, 0)
        rec = recent_freq.get(n, 0)
        if rec >= HOT_THRESHOLD:
            attr = "🔥 热号"
        elif rec >= WARM_THRESHOLD:
            attr = "⚡ 温号"
        else:
            attr = "❄️ 冷号"
        missing = 0
        for draw in reversed(recent):
            if n == draw["blue"]:
                break
            missing += 1
        stats[n] = {"frequency": total, "recent": rec, "attribute": attr, "missing": missing}

    return stats


# ============================================================
# 4. 特征分布
# ============================================================

def odd_even_ratio(reds):
    """计算奇偶比，返回 (odd_count, even_count)"""
    odd = sum(1 for r in reds if r % 2 == 1)
    even = 6 - odd
    return (odd, even)


def ac_value(reds):
    """计算 AC 值（算术复杂度）"""
    diffs = set()
    for i in range(len(reds)):
        for j in range(i + 1, len(reds)):
            diffs.add(abs(reds[i] - reds[j]))
    return len(diffs) - 5


def zone_distribution(reds):
    """三区分布：1-11, 12-22, 23-33"""
    zone1 = sum(1 for r in reds if 1 <= r <= 11)
    zone2 = sum(1 for r in reds if 12 <= r <= 22)
    zone3 = sum(1 for r in reds if 23 <= r <= 33)
    return (zone1, zone2, zone3)


def compute_distributions(draws):
    """统计特征分布"""
    oe_counter = Counter()
    ac_counter = Counter()
    zone_counter = Counter()
    sums = []

    for draw in draws:
        reds = draw["reds"]
        oe = odd_even_ratio(reds)
        ac = ac_value(reds)
        zone = zone_distribution(reds)
        oe_counter[f"{oe[0]}:{oe[1]}"] += 1
        ac_counter[ac] += 1
        zone_counter[f"{zone[0]}-{zone[1]}-{zone[2]}"] += 1
        sums.append(sum(reds))

    avg_sum = sum(sums) / len(sums) if sums else 0
    return {
        "odd_even": dict(sorted(oe_counter.items())),
        "ac": dict(sorted(ac_counter.items())),
        "zone": dict(sorted(zone_counter.items())),
        "sum_min": min(sums) if sums else 0,
        "sum_max": max(sums) if sums else 0,
        "sum_avg": avg_sum,
    }


# ============================================================
# 5. 报告生成（仅限免费统计部分）
# ============================================================

def generate_free_report(conn):
    """生成纯免费的分析报告，不包含推荐号码"""
    draws = get_recent_draws(conn, 20)
    historical = get_historical_draws(conn, 100)

    if not draws:
        return "⚠️ 没有足够的历史数据。请先运行 fetch_ssq.py 抓取数据。"

    red_stats = compute_red_stats(historical)
    blue_stats = compute_blue_stats(historical)
    distributions = compute_distributions(historical)

    lines = []
    lines.append("# 双色球智能分析报告")
    lines.append(f"\n> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> 数据来源：cwl.gov.cn（最近 {len(historical)} 期）")

    # --- 免费报告内容 ---
    lines.append("\n---\n")
    lines.append("## 一、红球冷热属性统计（近 20 期）\n")
    lines.append("| 号码 | 出现次数 | 热度 | 遗漏期数 |")
    lines.append("|------|----------|------|----------|")
    for n in range(1, 34):
        s = red_stats[n]
        lines.append(f"| {n:02d} | {s['recent']} | {s['attribute']} | {s['missing']} |")

    lines.append("\n---\n")
    lines.append("## 二、蓝球统计（近 20 期）\n")
    lines.append("| 号码 | 出现次数 | 热度 | 遗漏期数 |")
    lines.append("|------|----------|------|----------|")
    for n in range(1, 17):
        s = blue_stats[n]
        lines.append(f"| {n:02d} | {s['recent']} | {s['attribute']} | {s['missing']} |")

    lines.append("\n---\n")
    lines.append("## 三、特征分布统计\n")

    lines.append("\n### 奇偶比分布\n")
    lines.append("| 奇偶比 | 出现次数 |")
    lines.append("|--------|----------|")
    for oe, cnt in sorted(distributions["odd_even"].items()):
        bar = "#" * cnt
        lines.append(f"| {oe} | {cnt} {bar} |")

    lines.append("\n### AC 值分布\n")
    lines.append("| AC 值 | 出现次数 |")
    lines.append("|-------|----------|")
    for ac, cnt in sorted(distributions["ac"].items()):
        bar = "#" * cnt
        lines.append(f"| {ac} | {cnt} {bar} |")

    lines.append("\n### 三区分布\n")
    lines.append("| 分布 | 出现次数 |")
    lines.append("|------|----------|")
    for zone, cnt in sorted(distributions["zone"].items()):
        bar = "#" * cnt
        lines.append(f"| {zone} | {cnt} {bar} |")

    lines.append(f"\n### 和值统计\n")
    lines.append(f"- 平均值：{distributions['sum_avg']:.1f}")
    lines.append(f"- 最小值：{distributions['sum_min']}")
    lines.append(f"- 最大值：{distributions['sum_max']}")

    lines.append("\n---\n")
    lines.append("## 四、近 20 期开奖数据\n")
    lines.append("| 期号 | 红球 | 蓝球 | 日期 |")
    lines.append("|------|------|------|------|")
    for draw in draws:
        reds_str = " ".join(f"{r:02d}" for r in draw["reds"])
        lines.append(f"| {draw['code']} | {reds_str} | {draw['blue']:02d} | {draw['date']} |")

    # 付费提醒
    lines.append("\n---\n")
    lines.append("## 💡 推荐号码（需支付验证）\n")
    lines.append("> 如需 5 组推荐号码（含备选蓝球），请通过 clawtip 完成支付验证（3.9 元/次）后，")
    lines.append("> 运行 `python3 scripts/service.py \"<订单号>\"` 获取完整推荐。")

    report = "\n".join(lines)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    return report


# ============================================================
# 6. 主入口
# ============================================================

def main():
    if not os.path.exists(DB_PATH):
        print("⚠️ 数据库不存在。请先运行 fetch_ssq.py 抓取数据。")
        return 1

    conn = sqlite3.connect(DB_PATH)
    try:
        report = generate_free_report(conn)
        print(report)
        print(f"\n✅ 免费分析报告已生成：{OUTPUT_PATH}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
