#!/usr/bin/env python3
"""
SSQ 推荐号码生成器
由 service.py 在支付验证成功后调用。基于 SQLite 数据库中的历史数据，
通过多维规则过滤生成 5 组推荐号码。
"""
import os
import random
import sqlite3
from collections import Counter

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ssq_data.db")


def get_draws(conn, n=50):
    c = conn.cursor()
    c.execute("""SELECT red1,red2,red3,red4,red5,red6,blue FROM draws ORDER BY code DESC LIMIT ?""", (n,))
    rows = c.fetchall()
    draws = []
    for row in rows:
        draws.append({"reds": sorted(row[:6]), "blue": row[6]})
    return draws


def odd_even_ratio(reds):
    odd = sum(1 for r in reds if r % 2 == 1)
    return (odd, 6 - odd)


def ac_value(reds):
    diffs = set()
    for i in range(6):
        for j in range(i + 1, 6):
            diffs.add(abs(reds[i] - reds[j]))
    return len(diffs) - 5


def zone_dist(reds):
    z1 = sum(1 for r in reds if 1 <= r <= 11)
    z2 = sum(1 for r in reds if 12 <= r <= 22)
    z3 = sum(1 for r in reds if 23 <= r <= 33)
    return (z1, z2, z3)


def count_consecutive(reds):
    cnt = 0
    for i in range(5):
        if reds[i + 1] - reds[i] == 1:
            cnt += 1
    return cnt


def hot_cold_ratio(reds, recent_freq):
    hot = sum(1 for r in reds if recent_freq.get(r, 0) >= 6)
    cold = sum(1 for r in reds if recent_freq.get(r, 0) < 3)
    warm = 6 - hot - cold
    return (hot, warm, cold)


def is_valid_set(reds, recent_freq):
    oe = odd_even_ratio(reds)
    if oe not in [(3, 3), (4, 2), (2, 4)]:
        return False
    ac = ac_value(reds)
    if ac < 7 or ac > 10:
        return False
    zd = zone_dist(reds)
    if not (1 <= zd[0] <= 4 and 1 <= zd[1] <= 4 and 1 <= zd[2] <= 4):
        return False
    s = sum(reds)
    if s < 80 or s > 150:
        return False
    cc = count_consecutive(reds)
    if cc >= 3:
        return False
    hc = hot_cold_ratio(reds, recent_freq)
    if hc[0] > 3 or hc[2] > 3 or hc[1] < 2:
        return False
    return True


def generate_recommendations():
    if not os.path.exists(DB_PATH):
        print("⚠️ 数据库不存在。请先运行 fetch_ssq.py 抓取数据。")
        return

    conn = sqlite3.connect(DB_PATH)
    draws = get_draws(conn, 50)
    conn.close()

    if len(draws) < 20:
        print("⚠️ 历史数据不足 20 期，无法生成可靠推荐。")
        return

    # 计算近 20 期频率
    recent_draws = draws[:20]
    recent_freq = Counter()
    for d in recent_draws:
        for r in d["reds"]:
            recent_freq[r] += 1

    # 备选蓝球推荐
    blue_freq = Counter(d["blue"] for d in recent_draws)
    blue_candidates = sorted(
        [(n, blue_freq.get(n, 0)) for n in range(1, 17)],
        key=lambda x: (x[1], -x[0])
    )[:4]

    # 生成候选红球池：热号 + 温号 + 少量冷号
    hot_pool = [n for n in range(1, 34) if recent_freq.get(n, 0) >= 6]
    warm_pool = [n for n in range(1, 34) if 3 <= recent_freq.get(n, 0) <= 5]
    cold_pool = [n for n in range(1, 34) if recent_freq.get(n, 0) < 3]

    # 生成 5 组推荐
    sets = []
    for attempt in range(2000):
        if len(sets) >= 5:
            break
        # 选择红球：2-3 热号 + 2-3 温号 + 0-1 冷号
        n_hot = random.randint(2, 3)
        n_warm = random.randint(2, 3)
        n_cold = 6 - n_hot - n_warm
        if n_cold < 0:
            continue
        if len(hot_pool) < n_hot or len(warm_pool) < n_warm or len(cold_pool) < n_cold:
            continue
        selected = (random.sample(hot_pool, n_hot) +
                    random.sample(warm_pool, n_warm) +
                    random.sample(cold_pool, n_cold))
        selected_reds = sorted(selected)

        if not is_valid_set(selected_reds, recent_freq):
            continue

        # 组间交叉验证：任意两组重复红球不超过 2 个
        duplicate = False
        for existing in sets:
            overlap = len(set(selected_reds) & set(existing["reds"]))
            if overlap > 2:
                duplicate = True
                break
        if duplicate:
            continue

        # 随机选一个蓝球
        blue = random.choice([b[0] for b in blue_candidates])

        sets.append({
            "reds": selected_reds,
            "blue": blue,
            "oe": odd_even_ratio(selected_reds),
            "ac": ac_value(selected_reds),
            "zone": zone_dist(selected_reds),
            "sum": sum(selected_reds),
            "consecutive": count_consecutive(selected_reds),
            "hc": hot_cold_ratio(selected_reds, recent_freq),
        })
    else:
        if len(sets) < 5:
            print("⚠️ 仅生成了 {} 组满足条件的推荐号码（目标 5 组）。".format(len(sets)))

    # 输出报告
    print("\n" + "=" * 60)
    print("  推荐号码（付费内容）")
    print("=" * 60)

    print("\n### 备选蓝球推荐\n")
    print("| 蓝球 | 近 20 期出现次数 |")
    print("|------|-----------------|")
    for cn, cf in blue_candidates:
        print(f"| {cn:02d} | {cf} |")

    print("\n### 最终推荐号码（{}组）\n".format(len(sets)))
    print("| 组 | 红球 | 蓝球 | 奇偶比 | AC值 | 三区分布 | 和值 | 连号 | 热/温/冷 |")
    print("|---|------|------|--------|------|----------|------|------|----------|")
    for i, s in enumerate(sets, 1):
        reds_str = " ".join(f"{r:02d}" for r in s["reds"])
        hc_str = "{}/{}/{}".format(s["hc"][0], s["hc"][1], s["hc"][2])
        print(f"| {i} | {reds_str} | {s['blue']:02d} | {s['oe'][0]}:{s['oe'][1]} | {s['ac']} | {s['zone'][0]}-{s['zone'][1]}-{s['zone'][2]} | {s['sum']} | {s['consecutive']} | {hc_str} |")

    print("\n---")
    print("> ⚠️ 本推荐基于历史数据统计分析生成。彩票开奖为随机独立事件，")
    print("> 任何分析方法均不能保证中奖。请理性购彩，量力而行。")


if __name__ == "__main__":
    generate_recommendations()
