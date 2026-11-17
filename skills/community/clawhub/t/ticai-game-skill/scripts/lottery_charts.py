#!/usr/bin/env python3
"""
体彩走势图生成器 — 文本/ASCII 走势图
"""

import csv, argparse, math
from collections import Counter


# ── 数据加载 ──────────────────────────────────────────────

def load_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_dlt(data):
    """解析大乐透 CSV → [(期号, 前区, 后区), ...]"""
    rows = []
    for r in data:
        f = sorted(int(r[f"号码{i}"]) for i in range(1, 6))
        b = sorted(int(r[f"号码{i}"]) for i in range(6, 8))
        rows.append((r["期号"], f, b))
    return rows


def parse_digital(data):
    """解析数字彩 CSV → [(期号, [digits]), ...]"""
    rows = []
    for r in data:
        nums = [int(r[f"号码{i}"]) for i in range(1, 20) if r.get(f"号码{i}")]
        rows.append((r["期号"], nums))
    return rows


# ── 统计工具 ──────────────────────────────────────────────

def odd_even_ratio(nums):
    o = sum(1 for n in nums if n % 2 == 1)
    return f"{o}:{len(nums)-o}"

def big_small_ratio(nums, mid=18):
    b = sum(1 for n in nums if n > mid)
    return f"{b}:{len(nums)-b}"


# ── 走势图生成 ────────────────────────────────────────────

def chart_comprehensive(data, lottery="大乐透"):
    """号码综合走势"""
    lines = ["📊 号码综合走势"]
    if lottery == "大乐透":
        header = f"{'期号':<8} {'号码':<30} {'和值':<6} {'跨度':<6} {'奇偶':<6} {'大小':<6}"
        sep = "─" * len(header)
        lines.extend(["", header, sep])
        for qihao, f, b in data[:20]:
            ns = " ".join(f"{n:02d}" for n in f)
            sv = sum(f)
            sp = f[-1] - f[0]
            oe = odd_even_ratio(f)
            bs = big_small_ratio(f)
            lines.append(f"{qihao:<8} {ns:<30} {sv:<6} {sp:<6} {oe:<6} {bs:<6}")
    else:
        n = len(data[0][1]) if data else 0
        pos_names = ["百", "十", "个"] if n == 3 else ["万", "千", "百", "十", "个"] if n == 5 \
                    else [f"第{i+1}" for i in range(n)]
        pos_h = " ".join(f"{p:<4}" for p in pos_names)
        header = f"{'期号':<8} {pos_h} {'和值':<6} {'跨度':<6} {'形态':<8}"
        lines.extend(["", header, "─" * len(header)])
        for qihao, d in data[:20]:
            ds = " ".join(str(x) for x in d)
            sv = sum(d)
            sp = max(d) - min(d)
            shape = "".join("奇" if x % 2 else "偶" for x in d)
            lines.append(f"{qihao:<8} {ds:<{n*2+n-1 if n<7 else 15}} {sv:<6} {sp:<6} {shape:<8}")
    return "\n".join(lines)


def chart_sum(data, lottery="大乐透"):
    """和值走势图"""
    if lottery == "大乐透":
        vals = [sum(f) for _, f, _ in data]
        lo, hi = 15, 165
    else:
        vals = [sum(d) for _, d in data]
        lo, hi = 0, 45 if len(vals) and max(vals) > 27 else 27

    rng = hi - lo
    tick = max(1, rng // 30)
    lines = [f"📈 和值走势（近{len(data)}期）"]
    lines.append("")

    # 柱状图
    max_v = max(vals) if vals else 0
    scale = 40
    for i, (row, v) in enumerate(zip(data, vals)):
        qihao = row[0]
        bar_len = max(1, int(v * scale / max_v))
        bar = "█" * bar_len
        lines.append(f"{qihao:<8} {v:<4} {bar}")

    # 统计
    avg = sum(vals) / len(vals) if vals else 0
    lines.extend([
        "",
        f"📊 统计：均值为 {avg:.1f}，最高 {max(vals)}，最低 {min(vals)}",
        f"区间分布：≤{lo + rng//3} {sum(1 for v in vals if v <= lo + rng//3)}次  "
        f"≤{lo + rng*2//3} {sum(1 for v in vals if lo + rng//3 < v <= lo + rng*2//3)}次  "
        f"≤{hi} {sum(1 for v in vals if v > lo + rng*2//3)}次",
    ])
    return "\n".join(lines)


def chart_span(data, lottery="大乐透"):
    """跨度走势图"""
    if lottery == "大乐透":
        vals = [row[1][-1] - row[1][0] for row in data]
    else:
        vals = [max(d) - min(d) for _, d in data]

    max_v = max(vals) if vals else 10
    scale = 30
    lines = [f"📈 跨度走势（近{len(data)}期）", ""]
    for row, v in zip(data, vals):
        bar = "█" * max(1, int(v * scale / max_v))
        lines.append(f"{row[0]:<8} {v:<4} {bar}")

    avg = sum(vals) / len(vals) if vals else 0
    mid = max_v / 2
    lines.extend([
        "",
        f"📊 均值 {avg:.1f}，最高 {max(vals)}，最低 {min(vals)}",
        f"大跨度(≥{mid:.0f}) {sum(1 for v in vals if v >= mid)}次  "
        f"小跨度(<{mid:.0f}) {sum(1 for v in vals if v < mid)}次",
    ])
    return "\n".join(lines)


def chart_position(data, pos=0, name="百位"):
    """定位走势（数字彩）"""
    vals = [d[pos] for _, d in data]
    freq = Counter(vals)
    scale = 20
    lines = [f"📈 {name}走势（近{len(data)}期）", ""]
    for row, v in zip(data, vals):
        bar = "█" * max(1, int(freq[v] * scale / max(freq.values()))) if freq else ""
        mark = "●" if v == max(set(vals), key=vals.count) else "○"
        lines.append(f"{row[0]:<8} 号码 {v}  {mark} {bar}")

    top3 = freq.most_common(3)
    missing = [n for n in range(10) if n not in freq]
    lines.extend([
        "",
        f"高频: {' | '.join(f'{n}({c}次)' for n, c in top3)}",
        f"遗漏: {', '.join(str(n) for n in missing[:5]) if missing else '无'}",
    ])
    return "\n".join(lines)


def chart_hot_cold(data, lottery="大乐透"):
    """冷热走势图"""
    if lottery == "大乐透":
        all_nums = [n for _, f, _ in data for n in f]
        total_range = list(range(1, 36))
    else:
        all_nums = [n for _, d in data for n in d]
        total_range = list(range(10))

    freq = Counter(all_nums)
    last_qihao = data[-1][0] if data else "最近"

    hot = sorted([n for n in total_range if freq.get(n, 0) >= len(data) * 0.2],
                 key=lambda n: -freq.get(n, 0))
    warm = sorted([n for n in total_range if 0 < freq.get(n, 0) < len(data) * 0.2],
                  key=lambda n: -freq.get(n, 0))
    cold = sorted([n for n in total_range if freq.get(n, 0) == 0])

    lines = [f"🔥 冷热图（近{len(data)}期，截至{last_qihao}期）", ""]
    for n in total_range[:20] if lottery == "大乐透" else total_range:
        c = freq.get(n, 0)
        bar = "█" * min(c, 10)
        status = "🔥热" if c >= len(data) * 0.2 else "🌡温" if c > 0 else "❄️冷"
        lines.append(f"{n:02d} | {bar:<10} {c:<3} | {status}")
    if lottery == "大乐透":
        for n in total_range[20:]:
            c = freq.get(n, 0)
            bar = "█" * min(c, 10)
            status = "🔥热" if c >= len(data) * 0.2 else "🌡温" if c > 0 else "❄️冷"
            lines.append(f"{n:02d} | {bar:<10} {c:<3} | {status}")

    lines.extend([
        "",
        f"🔥热号({len(hot)}): {' '.join(f'{n:02d}' for n in hot[:8])}",
        f"🌡温号({len(warm)}): {' '.join(f'{n:02d}' for n in warm[:10])}",
        f"❄️冷号({len(cold)}): {' '.join(f'{n:02d}' for n in cold[:10])}",
        f"\n配比建议: 热{min(3, len(hot))}+温{min(2, len(warm))}{'+冷'+str(min(1, len(cold))) if cold else ''}",
    ])
    return "\n".join(lines)


def chart_oe_trend(data, lottery="大乐透"):
    """奇偶形态走势"""
    if lottery == "大乐透":
        ratios = [odd_even_ratio(f) for _, f, _ in data]
        labels = ["5:0", "4:1", "3:2", "2:3", "1:4", "0:5"]
    else:
        ratios = ["".join("奇" if x % 2 else "偶" for x in d) for _, d in data]
        labels = sorted(set(ratios))

    r_freq = Counter(ratios)
    lines = [f"📈 奇偶形态走势（近{len(data)}期）", ""]
    for row, r in zip(data, ratios):
        lines.append(f"{row[0]:<8} {r:<10} {'◆':>3}")
    lines.append("")
    lines.append("📊 统计:")
    for lb in labels:
        c = r_freq.get(lb, 0)
        bar = "█" * c
        lines.append(f"  {lb:<10} {c:<3}次 {bar}")
    return "\n".join(lines)


CHARTS = {
    "comprehensive": chart_comprehensive,
    "sum": chart_sum,
    "span": chart_span,
    "position": chart_position,
    "hotcold": chart_hot_cold,
    "oe": chart_oe_trend,
}

CHART_DESC = {
    "comprehensive": "号码综合走势（号码+和值+跨度+奇偶+大小）",
    "sum": "和值走势（柱状图+统计）",
    "span": "跨度走势（柱状图+统计）",
    "position": "定位走势（数字彩每位分布）",
    "hotcold": "冷热走势图（频率+状态分类）",
    "oe": "奇偶形态走势（比例分布）",
}


# ── CLI ───────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="体彩走势图生成器")
    parser.add_argument("file", help="CSV 数据文件")
    parser.add_argument("--lottery", default="大乐透", choices=["大乐透", "排列3", "排列5", "七星彩"])
    parser.add_argument("--periods", type=int, default=15, help="显示期数")
    parser.add_argument("--type", default="comprehensive", choices=list(CHARTS.keys()),
                        help=f"走势图类型: {CHART_DESC}")
    parser.add_argument("--pos", type=int, default=0, help="定位走势的位置索引(0=百位/万位)")
    parser.add_argument("--pos-name", default="百位", help="定位名称")
    args = parser.parse_args()

    try:
        data = load_csv(args.file)
    except Exception as e:
        print(f"❌ 文件加载失败: {e}")
        return

    if args.lottery == "大乐透":
        parsed = parse_dlt(data)
    else:
        parsed = parse_digital(data)

    # 截取最近 N 期
    show = parsed[-args.periods:] if len(parsed) > args.periods else parsed

    if args.type == "position":
        print(chart_position(show, args.pos, args.pos_name))
    else:
        fn = CHARTS[args.type]
        print(fn(show, args.lottery))


if __name__ == "__main__":
    main()
