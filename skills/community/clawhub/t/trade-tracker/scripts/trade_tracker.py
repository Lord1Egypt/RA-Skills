#!/usr/bin/env python3
"""
Trade Tracker — 交易记录追踪与归因分析（v1.1.0）

从交易记录 CSV 追踪每笔交易的盈亏、持仓时间、归因分析、
交易成本、策略标签归类。支持月度/季度归因分解、
多策略对比、ASCII盈亏分布图。

用法:
    python3 scripts/trade_tracker.py --file trades.csv
    python3 scripts/trade_tracker.py --file trades.csv --by month
    python3 scripts/trade_tracker.py --file trades.csv --compare
    python3 scripts/trade_tracker.py --file trades.csv --cost
    python3 scripts/trade_tracker.py --file trades.csv --chart
"""

import argparse
import csv
import json
import math
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def read_trades(filepath):
    with open(filepath, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _pf(row, candidates):
    for c in candidates:
        if c in row and row[c]:
            try:
                return float(str(row[c]).replace(",", "").replace("%", "").replace(" ", ""))
            except ValueError:
                pass
    return 0.0


def parse_date(val):
    """尝试多种日期格式解析，返回 (year, month, quarter)。"""
    val = str(val).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%Y.%m.%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            dt = datetime.strptime(val, fmt)
            return dt.year, dt.month, (dt.month - 1) // 3 + 1, dt.strftime("%Y-%m")
        except ValueError:
            continue
    return None, None, None, None


def parse_trades(rows):
    trades = []
    for row in rows:
        dt_val = row.get("date", row.get("日期", row.get("trade_date", "")))
        yr, mo, qtr, ym = parse_date(dt_val)
        trade = {
            "date": dt_val,
            "year": yr,
            "month": mo,
            "quarter": qtr,
            "year_month": ym,
            "stock": row.get("stock", row.get("代码", row.get("symbol", row.get("name", "")))),
            "direction": row.get("direction", row.get("action", row.get("方向", "buy"))).lower().strip(),
            "price": _pf(row, ["price", "成交价", "avg_price", "close"]),
            "shares": _pf(row, ["shares", "数量", "qty", "volume", "amount"]),
            "pnl": _pf(row, ["pnl", "profit", "盈亏", "net_pnl", "realized_pnl"]),
            "pnl_pct": _pf(row, ["pnl_pct", "盈亏%", "return_pct", "return"]),
            "commission": _pf(row, ["commission", "佣金", "fee", "cost"]),
            "tag": row.get("tag", row.get("strategy", row.get("策略", "default"))),
        }
        # 计算入仓日期（用于持仓时间）
        trade["entry_date"] = row.get("entry_date", row.get("入场日", row.get("open_date", "")))
        trade["exit_date"] = row.get("exit_date", row.get("出场日", row.get("close_date", dt_val)))
        if trade["price"] > 0 or trade["pnl"] != 0:
            trades.append(trade)
    return trades


# ── 基础分析 ──────────────────────────────────────────

def analyze_trades(trades):
    total_pnl = sum(t["pnl"] for t in trades)
    wins = [t for t in trades if t["pnl"] > 0]
    losses = [t for t in trades if t["pnl"] < 0]
    buys = [t for t in trades if "buy" in t["direction"] or "买入" in t["direction"]]
    sells = [t for t in trades if "sell" in t["direction"] or "卖出" in t["direction"]]

    by_stock = defaultdict(lambda: {"count": 0, "pnl": 0.0, "wins": 0, "losses": 0})
    for t in trades:
        s = t["stock"] or "unknown"
        by_stock[s]["count"] += 1
        by_stock[s]["pnl"] += t["pnl"]
        if t["pnl"] > 0:
            by_stock[s]["wins"] += 1
        elif t["pnl"] < 0:
            by_stock[s]["losses"] += 1

    best = max(trades, key=lambda t: t["pnl"]) if trades else None
    worst = min(trades, key=lambda t: t["pnl"]) if trades else None

    return {
        "total_trades": len(trades),
        "buy_trades": len(buys),
        "sell_trades": len(sells),
        "total_pnl": round(total_pnl, 2),
        "win_trades": len(wins),
        "loss_trades": len(losses),
        "win_rate": round(len(wins) / len(trades) * 100, 1) if trades else 0,
        "avg_pnl": round(total_pnl / len(trades), 2) if trades else 0,
        "avg_win": round(sum(t["pnl"] for t in wins) / len(wins), 2) if wins else 0,
        "avg_loss": round(sum(t["pnl"] for t in losses) / len(losses), 2) if losses else 0,
        "largest_win": {"stock": best["stock"], "pnl": round(best["pnl"], 2)} if best else None,
        "largest_loss": {"stock": worst["stock"], "pnl": round(worst["pnl"], 2)} if worst else None,
        "by_stock": {k: {"trades": v["count"], "pnl": round(v["pnl"], 2),
                         "win_rate": round(v["wins"]/v["count"]*100, 1) if v["count"] else 0}
                    for k, v in sorted(by_stock.items(), key=lambda x: -x[1]["pnl"])},
    }


# ── 月度/季度归因 ────────────────────────────────────

def attribution_by_period(trades, period="month"):
    """按月度或季度进行归因分解。"""
    groups = defaultdict(list)
    for t in trades:
        if period == "month":
            key = t["year_month"]
        elif period == "quarter":
            key = f"{t['year']}Q{t['quarter']}" if t["year"] else "unknown"
        else:
            key = str(t["year"]) if t["year"] else "unknown"
        if key and key != "None-None":
            groups[key].append(t)

    result = {}
    for period_key in sorted(groups):
        g = groups[period_key]
        total = sum(t["pnl"] for t in g)
        wins = [t for t in g if t["pnl"] > 0]
        losses = [t for t in g if t["pnl"] < 0]
        best = max(g, key=lambda t: t["pnl"]) if g else None
        worst = min(g, key=lambda t: t["pnl"]) if g else None
        result[period_key] = {
            "trades": len(g),
            "pnl": round(total, 2),
            "win_rate": round(len(wins) / len(g) * 100, 1) if g else 0,
            "best_trade": f"{best['stock']} ({best['pnl']:+,.0f})" if best else "",
            "worst_trade": f"{worst['stock']} ({worst['pnl']:+,.0f})" if worst else "",
        }
    return result


# ── 交易成本分析 ────────────────────────────────────

def cost_analysis(trades):
    """佣金占比、滑点估算、成本对盈亏的影响。"""
    total_commission = sum(t.get("commission", 0) for t in trades)
    total_pnl = sum(t["pnl"] for t in trades)
    total_turnover = sum(abs(t["price"] * t["shares"]) for t in trades if t["price"] and t["shares"])

    # 有佣金数据的交易
    trades_with_commission = [t for t in trades if t.get("commission", 0) > 0]
    avg_commission_rate = (
        sum(t["commission"] / (t["price"] * t["shares"]) * 100 for t in trades_with_commission) / len(trades_with_commission)
        if trades_with_commission and total_turnover > 0
        else 0
    )

    # 滑点估算（假设滑点为成交价的0.05%）
    slippage_est = total_turnover * 0.0005 if total_turnover > 0 else 0
    total_cost = total_commission + slippage_est
    cost_pnl_ratio = round(abs(total_cost / total_pnl) * 100, 1) if total_pnl != 0 else 0

    return {
        "total_commission": round(total_commission, 2),
        "avg_commission_rate_pct": round(avg_commission_rate, 3),
        "est_slippage": round(slippage_est, 2),
        "total_cost": round(total_cost, 2),
        "cost_pnl_ratio_pct": cost_pnl_ratio,
        "trades_with_cost_data": len(trades_with_commission),
    }


# ── 持仓时间分析 ────────────────────────────────────

def holding_period_analysis(trades):
    """持仓时间分析：平均持仓天数、按区间分组。"""
    holds = []
    for t in trades:
        ed = t.get("entry_date", "")
        xd = t.get("exit_date", t.get("date", ""))
        if not ed or not xd:
            continue
        try:
            e = datetime.strptime(str(ed)[:10], "%Y-%m-%d")
            x = datetime.strptime(str(xd)[:10], "%Y-%m-%d")
        except ValueError:
            try:
                e = datetime.strptime(str(ed)[:8], "%Y%m%d")
                x = datetime.strptime(str(xd)[:8], "%Y%m%d")
            except ValueError:
                continue
        days = (x - e).days
        if days >= 0:
            holds.append({"stock": t["stock"], "days": days, "pnl": t["pnl"],
                          "direction": t["direction"]})

    if not holds:
        return None

    avg_days = sum(h["days"] for h in holds) / len(holds)

    # 按持仓区间分组
    bins = {"0-1天": 0, "2-3天": 0, "4-7天": 0, "8-14天": 0, "15-30天": 0, "30天+": 0}
    bin_pnl = {b: 0.0 for b in bins}
    for h in holds:
        d = h["days"]
        if d <= 1:
            bins["0-1天"] += 1
            bin_pnl["0-1天"] += h["pnl"]
        elif d <= 3:
            bins["2-3天"] += 1
            bin_pnl["2-3天"] += h["pnl"]
        elif d <= 7:
            bins["4-7天"] += 1
            bin_pnl["4-7天"] += h["pnl"]
        elif d <= 14:
            bins["8-14天"] += 1
            bin_pnl["8-14天"] += h["pnl"]
        elif d <= 30:
            bins["15-30天"] += 1
            bin_pnl["15-30天"] += h["pnl"]
        else:
            bins["30天+"] += 1
            bin_pnl["30天+"] += h["pnl"]

    return {
        "avg_holding_days": round(avg_days, 1),
        "total_with_hold_data": len(holds),
        "max_hold": max(h["days"] for h in holds),
        "min_hold": min(h["days"] for h in holds),
        "by_hold_period": {
            k: {"trades": v, "pnl": round(bin_pnl[k], 2)} for k, v in bins.items()
        },
    }


# ── 策略标签归类 ────────────────────────────────────

def analyze_by_tag(trades):
    """按策略标签归类分析。"""
    by_tag = defaultdict(list)
    for t in trades:
        by_tag[t.get("tag", "default")].append(t)

    result = {}
    for tag in sorted(by_tag):
        g = by_tag[tag]
        pnl = sum(t["pnl"] for t in g)
        wins = [t for t in g if t["pnl"] > 0]
        result[tag] = {
            "trades": len(g),
            "pnl": round(pnl, 2),
            "win_rate": round(len(wins) / len(g) * 100, 1) if g else 0,
            "avg_pnl": round(pnl / len(g), 2) if g else 0,
        }
    return result


# ── 多策略对比 ──────────────────────────────────────

def compare_strategies(trades):
    """多策略或多时段对比。"""
    # 按标签
    by_tag = analyze_by_tag(trades)
    # 按季度
    by_q = attribution_by_period(trades, "quarter")
    # 按年份
    by_y = attribution_by_period(trades, "year")

    return {
        "by_tag": by_tag,
        "by_quarter": by_q,
        "by_year": by_y,
    }


# ── ASCII盈亏分布图 ────────────────────────────────

def ascii_pnl_chart(trades, width=50):
    """K线图风格的ASCII盈亏分布图。"""
    if not trades:
        return ""

    pnls = [t["pnl"] for t in trades]
    lo, hi = min(pnls), max(pnls)
    if hi - lo < 0.001:
        return "（所有盈亏接近零）"

    # 分桶
    num_bins = 20
    bin_size = (hi - lo) / num_bins
    bins = [0] * num_bins
    labels = []
    for i in range(num_bins):
        b_lo = lo + i * bin_size
        b_hi = b_lo + bin_size
        labels.append(f"{b_lo:+.0f}")
    for p in pnls:
        idx = min(int((p - lo) / bin_size), num_bins - 1)
        bins[idx] += 1

    max_count = max(bins)
    if max_count == 0:
        return ""

    lines = []
    for row in range(10, 0, -1):
        threshold = max_count * row / 10
        line = ""
        for i, count in enumerate(bins):
            if count >= threshold:
                # 根据正负着色指示
                is_positive = (lo + (i + 0.5) * bin_size) > 0
                line += "█" if is_positive else "▓"
            else:
                line += " "
        lines.append(f"   {threshold:>4.0f} {line}")

    # X轴标签
    mid = num_bins // 2
    axis = f"   {' ':<4} {'─' * num_bins}"
    label_line = f"   {' ':<4} {'亏损' + ' ' * (mid-2) + '→' + ' ' * (mid-2) + '盈利'}"

    chart = "\n".join(lines)
    chart += f"\n{axis}"
    chart += f"\n{label_line}"
    chart += f"\n   规模: {len(pnls)}笔  范围: {lo:+.0f} ~ {hi:+.0f}"
    return chart


# ── 打印 ──────────────────────────────────────────────

def print_analysis(analysis):
    print(f"\n📊 交易归因分析")
    print(f"   {'='*55}")
    print(f"   总交易: {analysis['total_trades']} (买入{analysis['buy_trades']} / 卖出{analysis['sell_trades']})")
    print(f"   总盈亏: {analysis['total_pnl']:+,.2f}")
    print(f"   胜率: {analysis['win_rate']:.1f}% ({analysis['win_trades']}/{analysis['total_trades']})")
    print(f"   平均每笔: {analysis['avg_pnl']:+,.2f}")
    print(f"   平均盈利: {analysis['avg_win']:+,.2f}")
    print(f"   平均亏损: {analysis['avg_loss']:+,.2f}")

    if analysis['largest_win']:
        print(f"   最大盈利: {analysis['largest_win']['stock']} ({analysis['largest_win']['pnl']:+,.2f})")
    if analysis['largest_loss']:
        print(f"   最大亏损: {analysis['largest_loss']['stock']} ({analysis['largest_loss']['pnl']:+,.2f})")

    if analysis['by_stock']:
        print(f"\n   按股票归因:")
        print(f"   {'代码':<10} {'交易':>5} {'盈亏':>12} {'胜率':>7}")
        print(f"   {'-'*38}")
        for stock, s in list(analysis['by_stock'].items())[:15]:
            print(f"   {stock:<10} {s['trades']:>5} {s['pnl']:>+12.2f} {s['win_rate']:>6.1f}%")


def print_period_attribution(attr, period_name="月度"):
    if not attr:
        return
    print(f"\n   ── {period_name}归因 ──")
    print(f"   {'期间':<10} {'交易':>5} {'盈亏':>12} {'胜率':>7} {'最佳':<18} {'最差':<18}")
    print(f"   {'-'*75}")
    for period in sorted(attr):
        a = attr[period]
        print(f"   {period:<10} {a['trades']:>5} {a['pnl']:>+12.2f} "
              f"{a['win_rate']:>6.1f}% {a.get('best_trade', ''):<18} {a.get('worst_trade', ''):<18}")


def print_cost(cost):
    if not cost:
        return
    print(f"\n   ── 交易成本 ──")
    print(f"   总佣金: {cost['total_commission']:+,.2f}")
    print(f"   平均佣金率: {cost['avg_commission_rate_pct']:.3f}%")
    print(f"   估算滑点: {cost['est_slippage']:+,.2f}")
    print(f"   总成本: {cost['total_cost']:+,.2f}")
    print(f"   成本/盈亏比: {cost['cost_pnl_ratio_pct']:.1f}%")


def print_holding(hp):
    if not hp:
        return
    print(f"\n   ── 持仓时间 ──")
    print(f"   平均持仓: {hp['avg_holding_days']:.1f}天 (最短{hp['min_hold']}天 / 最长{hp['max_hold']}天)")
    print(f"   数据: {hp['total_with_hold_data']}笔")
    print(f"   {'持仓区间':<10} {'交易':>5} {'盈亏':>12}")
    print(f"   {'-'*30}")
    for period in sorted(hp['by_hold_period']):
        d = hp['by_hold_period'][period]
        print(f"   {period:<10} {d['trades']:>5} {d['pnl']:>+12.2f}")


def print_tag_analysis(tags):
    if not tags:
        return
    print(f"\n   ── 策略标签归因 ──")
    print(f"   {'策略':<12} {'交易':>5} {'盈亏':>12} {'胜率':>7} {'平均每笔':>10}")
    print(f"   {'-'*50}")
    for tag in sorted(tags, key=lambda t: -tags[t]["pnl"]):
        t = tags[tag]
        print(f"   {tag:<12} {t['trades']:>5} {t['pnl']:>+12.2f} {t['win_rate']:>6.1f}% {t['avg_pnl']:>+10.2f}")


def print_compare(comparison):
    if comparison.get("by_tag"):
        print(f"\n📊 策略对比")
        for tag in sorted(comparison["by_tag"], key=lambda t: -comparison["by_tag"][t]["pnl"]):
            t = comparison["by_tag"][tag]
            print(f"   {tag:<15} 交易{t['trades']:>4}  盈亏{t['pnl']:>+12.2f}  胜率{t['win_rate']:>6.1f}%")
    if comparison.get("by_quarter"):
        print(f"\n📊 季度对比")
        for q in sorted(comparison["by_quarter"]):
            c = comparison["by_quarter"][q]
            print(f"   {q:<10} 交易{c['trades']:>4}  盈亏{c['pnl']:>+12.2f}  胜率{c['win_rate']:>6.1f}%")


# ── 主入口 ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Trade Tracker v1.1.0 — 交易记录追踪与归因分析",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
命令说明:
  (默认)       综合交易分析
  --cost       交易成本分析（佣金 + 滑点估算）
  --hold       持仓时间分析
  --tag        按策略标签归类分析（需要CSV有 tag/strategy/策略列）
  --compare    多策略或多时段对比
  --chart      显示ASCII盈亏分布图
  --by         归因周期 (month/quarter/year)

示例:
  python3 %(prog)s --file trades.csv
  python3 %(prog)s --file trades.csv --by month
  python3 %(prog)s --file trades.csv --cost --hold
  python3 %(prog)s --file trades.csv --tag
  python3 %(prog)s --file trades.csv --compare
  python3 %(prog)s --file trades.csv --chart

免责声明: 本工具仅供交易复盘参考，不构成投资建议。
        """
    )
    parser.add_argument("--file", required=True, help="交易CSV文件")
    parser.add_argument("--by", choices=["stock", "month", "quarter", "year"],
                        default="stock", help="归因周期")
    parser.add_argument("--cost", action="store_true", help="交易成本分析")
    parser.add_argument("--hold", action="store_true", help="持仓时间分析")
    parser.add_argument("--tag", action="store_true", help="策略标签归类")
    parser.add_argument("--compare", action="store_true", help="多策略对比")
    parser.add_argument("--chart", action="store_true", help="ASCII盈亏分布图")
    parser.add_argument("--output", help="JSON输出路径")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)

    rows = read_trades(args.file)
    if not rows:
        print("❌ 空文件")
        sys.exit(1)

    trades = parse_trades(rows)

    if args.chart:
        print(f"\n📊 盈亏分布图 — {Path(args.file).name}")
        print(ascii_pnl_chart(trades))
        return

    # 综合输出
    output = {}

    # 默认分析
    analysis = analyze_trades(trades)

    if not args.cost and not args.hold and not args.tag and not args.compare:
        print_analysis(analysis)

    # 归因周期
    if args.by in ("month", "quarter", "year"):
        period_name = {"month": "月度", "quarter": "季度", "year": "年度"}
        attr = attribution_by_period(trades, args.by)
        output[f"by_{args.by}"] = attr
        print_period_attribution(attr, period_name.get(args.by, ""))

    # 交易成本
    if args.cost:
        cost = cost_analysis(trades)
        output["cost"] = cost
        print_cost(cost)

    # 持仓时间
    if args.hold:
        hp = holding_period_analysis(trades)
        output["holding"] = hp
        print_holding(hp)

    # 策略标签
    if args.tag:
        tags = analyze_by_tag(trades)
        output["by_tag"] = tags
        print_tag_analysis(tags)

    # 对比
    if args.compare:
        comp = compare_strategies(trades)
        output["comparison"] = comp
        print_compare(comp)

    if args.json or args.output:
        if not output:
            output = analysis
        print(json.dumps(output, indent=2, ensure_ascii=False))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output if output else analysis, f, indent=2, ensure_ascii=False)
        print(f"\n💾 已保存: {args.output}")


if __name__ == "__main__":
    main()
