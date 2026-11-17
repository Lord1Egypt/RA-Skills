#!/usr/bin/env python3
"""
Stock Planner v1.1.0 — 智能交易计划生成器

基于当前持仓、市场状态和策略规则生成交易日操作计划。
新增：多计划对比、组合再平衡、持仓相关性分析、
多日规划回顾、保证金/杠杆风险评估。

用法:
    python3 scripts/stock_planner.py --positions pos.csv
    python3 scripts/stock_planner.py compare --plan1 plan1.json --plan2 plan2.json
    python3 scripts/stock_planner.py rebalance --positions pos.csv --target "tech:30,food:20,health:25,cash:25"
    python3 scripts/stock_planner.py correlation --price-data prices.csv
    python3 scripts/stock_planner.py history --dir plans/
    python3 scripts/stock_planner.py leverage --positions pos.csv --margin 0.5
"""

import argparse
import csv
import json
import math
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional


# 市场状态定义
MARKET_STATES = {
    "strong":    {"label": "强势上涨", "max_positions": 8, "position_pct": 0.85, "risk": "低"},
    "moderate":  {"label": "震荡偏强", "max_positions": 6, "position_pct": 0.65, "risk": "中低"},
    "oscillate": {"label": "震荡",     "max_positions": 5, "position_pct": 0.50, "risk": "中"},
    "weak":      {"label": "震荡偏弱", "max_positions": 4, "position_pct": 0.35, "risk": "中高"},
    "bear":      {"label": "下跌趋势", "max_positions": 3, "position_pct": 0.20, "risk": "高"},
}

DEFAULT_MARKET = "oscillate"


# ── 工具函数 ─────────────────────────────────────────────────────────

def read_positions(filepath: str) -> list[dict]:
    """读取持仓 CSV。"""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def read_json(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_pct(val, default=0.0) -> float:
    """解析百分比或数值。"""
    if not val:
        return default
    s = str(val).replace("%", "").replace(" ", "").replace(",", "")
    try:
        return float(s)
    except ValueError:
        return default


def _parse_date(dt_str: str) -> Optional[datetime]:
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(dt_str, fmt)
        except (ValueError, TypeError):
            continue
    return None


def _validate_file(path: str) -> bool:
    if not os.path.exists(path):
        print(f"❌ 文件不存在: {path}")
        return False
    return True


# ── 核心功能：生成计划 ─────────────────────────────────────────────────

def generate_plan(positions: list[dict], market: str = DEFAULT_MARKET,
                  cash: float = 0, total_capital: float = 0) -> dict:
    """生成交易计划。"""
    ms = MARKET_STATES.get(market, MARKET_STATES[DEFAULT_MARKET])

    if not positions:
        return {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "market": market,
            "market_label": ms["label"],
            "market_risk": ms["risk"],
            "total_positions": 0,
            "max_positions": ms["max_positions"],
            "positions": [],
            "summary": "当前无持仓。建议根据市场状态选择标的建仓。",
            "actions": [],
        }

    total_value = 0.0
    total_cost = 0.0
    items = []

    for row in positions:
        name = row.get("name", row.get("stock", row.get("代码", "?")))
        shares = float(row.get("shares", row.get("数量", row.get("qty", 0))))
        avg_price = parse_pct(row.get("avg_price", row.get("成本", row.get("cost", 0))))
        current = parse_pct(row.get("price", row.get("现价", row.get("current", 0))))
        pnl_pct = parse_pct(row.get("pnl_pct", row.get("盈亏%", "")))

        if current == 0 and avg_price > 0:
            current = avg_price

        cost_value = shares * avg_price
        current_value = shares * current
        pnl = current_value - cost_value
        if pnl_pct == 0 and cost_value > 0:
            pnl_pct = (current_value - cost_value) / cost_value * 100

        total_value += current_value
        total_cost += cost_value

        stop_loss, take_profit, action, reason = False, False, "持有", ""
        if pnl_pct <= -8:
            stop_loss, action, reason = True, "止损", f"亏损{pnl_pct:.1f}%，触发止损"
        elif pnl_pct >= 20:
            take_profit, action, reason = True, "止盈", f"盈利{pnl_pct:.1f}%，建议分批止盈"
        elif pnl_pct <= -5:
            action, reason = "关注", f"亏损{pnl_pct:.1f}%，接近止损线"
        elif pnl_pct >= 12:
            action, reason = "观察", f"盈利{pnl_pct:.1f}%，考虑减持"

        items.append({
            "name": name,
            "shares": int(shares),
            "avg_price": round(avg_price, 3),
            "current_price": round(current, 3),
            "cost_value": round(cost_value, 2),
            "current_value": round(current_value, 2),
            "pnl": round(pnl, 2),
            "pnl_pct": round(pnl_pct, 1),
            "action": action,
            "reason": reason,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
        })

    if total_capital == 0:
        total_capital = max(total_value + cash, total_cost + cash)
    if total_capital <= 0:
        total_capital = 1

    position_ratio = total_value / total_capital * 100
    cash_ratio = cash / total_capital * 100

    actions = []
    for item in items:
        if item["stop_loss"]:
            actions.append(f"🔴 止损: {item['name']} — {item['reason']}")
        elif item["take_profit"]:
            actions.append(f"🟢 止盈: {item['name']} — {item['reason']}")
        elif item["action"] == "关注":
            actions.append(f"👀 关注: {item['name']} — {item['reason']}")

    max_pos = ms["max_positions"]
    target_ratio = ms["position_pct"] * 100

    if position_ratio > target_ratio + 10:
        actions.append(f"⚠️ 仓位{position_ratio:.0f}% > 目标{target_ratio:.0f}%，建议减仓")
    elif position_ratio < target_ratio - 10 and cash > 0:
        actions.append(f"💡 仓位{position_ratio:.0f}% < 目标{target_ratio:.0f}%，可适当加仓")

    if len(items) > max_pos:
        actions.append(f"📋 持仓{len(items)}只 > 建议{max_pos}只，考虑集中")
    if not actions:
        actions.append(f"✅ 仓位{position_ratio:.0f}%符合{ms['label']}建议({target_ratio:.0f}%)，继续持有")

    return {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "market": market,
        "market_label": ms["label"],
        "market_risk": ms["risk"],
        "total_positions": len(items),
        "max_positions": max_pos,
        "total_value": round(total_value, 2),
        "total_cost": round(total_cost, 2),
        "total_pnl": round(total_value - total_cost, 2),
        "total_pnl_pct": round((total_value - total_cost) / total_cost * 100, 1) if total_cost > 0 else 0,
        "position_ratio": round(position_ratio, 1),
        "cash": cash,
        "cash_ratio": round(cash_ratio, 1),
        "positions": items,
        "actions": actions,
    }


def print_plan(plan: dict):
    """打印交易计划。"""
    print(f"\n📋 交易计划 — {plan['market_label']}市场")
    print(f"   {'='*50}")
    print(f"   生成时间:   {plan['generated_at']}")
    print(f"   市场判定:   {plan['market_label']} (风险:{plan['market_risk']})")
    print(f"   {'='*50}")
    print(f"   持仓总数:   {plan['total_positions']}/{plan['max_positions']}")
    print(f"   持仓市值:   {plan['total_value']:,.2f}")
    print(f"   总盈亏:     {plan['total_pnl']:+,.2f} ({plan['total_pnl_pct']:+.1f}%)")
    print(f"   仓位比例:   {plan['position_ratio']:.1f}%")
    if plan['cash'] > 0:
        print(f"   可用资金:   {plan['cash']:,.2f} ({plan['cash_ratio']:.1f}%)")
    print()

    if plan['positions']:
        print(f"   {'代码':<12} {'盈亏%':>8} {'操作':<6}  说明")
        print(f"   {'-'*55}")
        for p in plan['positions']:
            emoji = {"止损": "🔴", "止盈": "🟢", "关注": "👀", "观察": "📌", "持有": "  "}.get(p['action'], "  ")
            print(f"   {p['name']:<12} {p['pnl_pct']:>+7.1f}% {emoji}{p['action']:<4}  {p['reason']}")
    print()
    for action in plan['actions']:
        print(f"   {action}")


# ── compare 命令 ──────────────────────────────────────────────────────

def cmd_compare(args):
    """多计划对比。"""
    plan1 = read_json(args.plan1)
    plan2 = read_json(args.plan2)

    print(f"\n🔄 多计划对比")
    print(f"   {'='*55}")
    print(f"   {'指标':<20} {'计划1':<16} {'计划2':<16}")
    print(f"   {'-'*55}")

    rows = [
        ("市场状态", plan1.get("market_label", "?"), plan2.get("market_label", "?")),
        ("市场风险", plan1.get("market_risk", "?"), plan2.get("market_risk", "?")),
        ("持仓数", str(plan1.get("total_positions", 0)), str(plan2.get("total_positions", 0))),
        ("持仓市值", f"{plan1.get('total_value', 0):,.0f}", f"{plan2.get('total_value', 0):,.0f}"),
        ("总盈亏", f"{plan1.get('total_pnl', 0):+,.0f}", f"{plan2.get('total_pnl', 0):+,.0f}"),
        ("总收益率", f"{plan1.get('total_pnl_pct', 0):+.1f}%", f"{plan2.get('total_pnl_pct', 0):+.1f}%"),
        ("仓位比例", f"{plan1.get('position_ratio', 0):.0f}%", f"{plan2.get('position_ratio', 0):.0f}%"),
    ]

    for label, v1, v2 in rows:
        print(f"   {label:<20} {v1:<16} {v2:<16}")

    # 操作建议对比
    a1 = plan1.get("actions", [])
    a2 = plan2.get("actions", [])
    print(f"\n   操作建议对比:")
    print(f"   {'='*55}")
    common = set(a1) & set(a2)
    only1 = set(a1) - set(a2)
    only2 = set(a2) - set(a1)

    if common:
        print(f"\n   共同建议:")
        for a in common:
            print(f"      · {a}")
    if only1:
        print(f"\n   计划1特有:")
        for a in only1:
            print(f"      · {a}")
    if only2:
        print(f"\n   计划2特有:")
        for a in only2:
            print(f"      · {a}")

    # 分歧分析
    p1_actions = {p["name"]: p["action"] for p in plan1.get("positions", [])}
    p2_actions = {p["name"]: p["action"] for p in plan2.get("positions", [])}
    conflicts = []
    for name in set(p1_actions) | set(p2_actions):
        act1 = p1_actions.get(name, "-")
        act2 = p2_actions.get(name, "-")
        if act1 != act2:
            conflicts.append(f"{name}: {act1} vs {act2}")
    if conflicts:
        print(f"\n   操作分歧:")
        for c in conflicts:
            print(f"      ⚡ {c}")

    print()


# ── rebalance 命令 ────────────────────────────────────────────────────

def cmd_rebalance(args):
    """组合再平衡建议。"""
    positions = read_positions(args.positions)
    if not positions:
        print("❌ 无持仓数据")
        return

    # 解析目标配置: "tech:30,food:20,health:25,cash:25"
    target_allocation: dict[str, float] = {}
    for part in args.target.split(","):
        part = part.strip()
        if ":" in part:
            key, val = part.rsplit(":", 1)
            target_allocation[key.strip()] = float(val.strip())

    if not target_allocation:
        print("❌ 目标配置格式错误，示例: --target \"tech:30,food:20,health:25,cash:25\"")
        return

    total_target = sum(target_allocation.values())
    if abs(total_target - 100) > 0.01:
        print(f"⚠️ 目标配置之和为{total_target:.0f}%，已归一化至100%")

    # 读取总市值和现金
    # 从持仓计算当前各分类市值
    total_value = 0.0
    sector_values: dict[str, float] = defaultdict(float)
    for row in positions:
        shares = float(row.get("shares", row.get("数量", row.get("qty", 0))))
        current = parse_pct(row.get("price", row.get("现价", row.get("current", 0))))
        name = row.get("name", row.get("stock", row.get("代码", "?")))
        sector = row.get("sector", row.get("行业", row.get("industry", "未分类")))

        value = shares * current
        total_value += value
        sector_values[sector] += value

    total_portfolio = total_value + args.cash
    if total_portfolio <= 0:
        print("❌ 总资产为0")
        return

    print(f"\n🔄 组合再平衡建议")
    print(f"   {'='*55}")
    print(f"   当前总资产: {total_portfolio:,.2f}")
    print(f"   当前持仓:   {total_value:,.2f} ({total_value/total_portfolio*100:.0f}%)")
    print(f"   当前现金:   {args.cash:,.2f} ({args.cash/total_portfolio*100:.0f}%)")
    print()

    # 计算再平衡
    print(f"   {'分类':<15} {'当前%':>8} {'目标%':>8} {'偏差%':>8} {'建议调整':>12}")
    print(f"   {'-'*55}")

    total_adjust = 0.0
    for sector, target_pct in target_allocation.items():
        target_pct = target_pct / total_target * 100  # normalize
        current_pct = sector_values.get(sector, 0) / total_portfolio * 100
        diff = target_pct - current_pct
        adj_amount = abs(diff / 100 * total_portfolio)

        if diff > 1:
            action = f"+{adj_amount:,.0f}"
            total_adjust += adj_amount
        elif diff < -1:
            action = f"-{adj_amount:,.0f}"
            total_adjust += adj_amount
        else:
            action = "✓"

        print(f"   {sector:<15} {current_pct:>7.1f}% {target_pct:>7.1f}% {diff:>+7.1f}% {action:>12}")

    # 现金列
    cash_current = args.cash / total_portfolio * 100
    cash_target = target_allocation.get("cash", target_allocation.get("现金", 0)) / total_target * 100 if "cash" in target_allocation or "现金" in target_allocation else 0
    cash_diff = cash_target - cash_current
    print(f"   {'现金':<15} {cash_current:>7.1f}% {cash_target:>7.1f}% {cash_diff:>+7.1f}% {'':>12}")

    print(f"   {'-'*55}")
    print(f"   总调整规模: {total_adjust:,.2f} ({total_adjust/total_portfolio*100:.1f}%)")
    if total_adjust / total_portfolio > 0.3:
        print(f"   ⚠️ 调整幅度较大，建议分步执行")


# ── correlation 命令 ──────────────────────────────────────────────────

def cmd_correlation(args):
    """持仓相关性检查。"""
    if not _validate_file(args.price_data):
        return

    with open(args.price_data, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("❌ 价格数据为空")
        return

    # Format: columns = stocks, rows = dates with prices
    sample = rows[0]
    date_col = next((c for c in ["date", "日期", "time", "时间"] if c in sample), None)
    stock_cols = [c for c in sample.keys() if c != date_col]

    if len(stock_cols) < 2:
        print("❌ 至少需要2只股票的价格数据")
        return

    # Build price matrix
    prices: dict[str, list[float]] = {s: [] for s in stock_cols}
    for row in rows:
        for s in stock_cols:
            try:
                p = float(row[s].replace(",", ""))
            except (ValueError, AttributeError):
                p = 0.0
            prices[s].append(p)

    # Compute returns
    returns: dict[str, list[float]] = {}
    for s in stock_cols:
        rets = []
        for i in range(1, len(prices[s])):
            if prices[s][i-1] != 0:
                rets.append((prices[s][i] - prices[s][i-1]) / prices[s][i-1] * 100)
            else:
                rets.append(0.0)
        returns[s] = rets

    # Correlation matrix using Pearson
    print(f"\n📊 持仓相关性矩阵")
    print(f"   数据来源: {Path(args.price_data).name}")
    print(f"   周期: {len(returns[stock_cols[0]])} 个区间")
    print(f"   {'='*55}")

    # Header
    print(f"   {'':<12}", end="")
    for s in stock_cols:
        print(f" {s:<10}", end="")
    print()
    print(f"   {'-'*55}")

    for s1 in stock_cols:
        print(f"   {s1:<12}", end="")
        for s2 in stock_cols:
            if s1 == s2:
                print(f" {'1.000':<10}", end="")
            else:
                r1, r2 = returns[s1], returns[s2]
                n = min(len(r1), len(r2))
                if n < 2:
                    print(f" {'N/A':<10}", end="")
                    continue
                r1, r2 = r1[:n], r2[:n]
                mean1 = sum(r1) / n
                mean2 = sum(r2) / n
                num = sum((r1[i] - mean1) * (r2[i] - mean2) for i in range(n))
                den1 = math.sqrt(sum((r1[i] - mean1)**2 for i in range(n)))
                den2 = math.sqrt(sum((r2[i] - mean2)**2 for i in range(n)))
                corr = num / (den1 * den2) if den1 * den2 != 0 else 0
                color = "🟢" if abs(corr) < 0.3 else "🟡" if abs(corr) < 0.7 else "🔴"
                print(f" {color}{corr:.3f}", end=" ")
        print()

    # Interpretation
    print(f"\n   解读:")
    print(f"   🟢 |r|<0.3 弱相关 → 分散好")
    print(f"   🟡 0.3≤|r|<0.7 中度相关")
    print(f"   🔴 |r|≥0.7 强相关 → 集中风险")
    print()


# ── history 命令 ──────────────────────────────────────────────────────

def cmd_history(args):
    """多日规划历史回顾。"""
    if not _validate_file(args.dir):
        return

    path = Path(args.dir)
    plan_files = sorted(path.glob("*.json"))

    if not plan_files:
        print(f"❌ 在 {args.dir} 中未找到计划JSON文件")
        return

    print(f"\n📅 多日规划历史回顾 ({len(plan_files)} 个计划)")
    print(f"   {'='*60}")

    records = []
    for pf in plan_files:
        try:
            plan = json.loads(pf.read_text(encoding="utf-8"))
            records.append({
                "date": plan.get("generated_at", pf.stem),
                "market": plan.get("market_label", "?"),
                "positions": plan.get("total_positions", 0),
                "value": plan.get("total_value", 0),
                "pnl": plan.get("total_pnl", 0),
                "pnl_pct": plan.get("total_pnl_pct", 0),
                "ratio": plan.get("position_ratio", 0),
                "actions": plan.get("actions", []),
                "file": pf.name,
            })
        except (json.JSONDecodeError, KeyError):
            continue

    if not records:
        print("   未解析到有效计划")
        return

    print(f"   {'日期':<20} {'市场':<10} {'持仓':<6} {'市值':<12} {'盈亏%':<8} {'仓位%':<6}")
    print(f"   {'-'*60}")
    for r in records:
        sign = "+" if r["pnl_pct"] >= 0 else ""
        print(f"   {r['date']:<20} {r['market']:<10} {r['positions']:<6} "
              f"{r['value']:<12,.0f} {sign}{r['pnl_pct']:<+6.1f}% {r['ratio']:<5.0f}%")

    # 趋势分析
    if len(records) >= 2:
        first, last = records[0], records[-1]
        print(f"\n   趋势概览:")
        print(f"   初始: 仓位{first['ratio']:.0f}% | 收益{first['pnl_pct']:+.1f}%")
        print(f"   最新: 仓位{last['ratio']:.0f}% | 收益{last['pnl_pct']:+.1f}%")
        pnl_change = last["pnl_pct"] - first["pnl_pct"]
        print(f"   收益变化: {'+' if pnl_change>=0 else ''}{pnl_change:.1f}%")

        # Action consistency
        recent = records[-1].get("actions", [])
        if recent:
            print(f"\n   最新操作建议:")
            for a in recent[:5]:
                print(f"      {a}")

    print()


# ── leverage 命令 ─────────────────────────────────────────────────────

def cmd_leverage(args):
    """保证金/杠杆风险评估。"""
    positions = read_positions(args.positions) if args.positions else []

    if not positions and not args.margin:
        print("❌ 需要持仓数据或保证金比例")
        return

    # 计算总资产情况
    total_value = 0.0
    total_cost = 0.0
    for row in positions:
        shares = float(row.get("shares", row.get("数量", row.get("qty", 0))))
        avg_price = parse_pct(row.get("avg_price", row.get("成本", row.get("cost", 0))))
        current = parse_pct(row.get("price", row.get("现价", row.get("current", 0))))
        if current == 0 and avg_price > 0:
            current = avg_price
        total_value += shares * current
        total_cost += shares * avg_price

    equity = args.capital if args.capital > 0 else total_value
    margin_pct = args.margin

    if margin_pct <= 0:
        margin_pct = 0.5  # default 50% margin

    # 如果总价值=0，用资本金
    if total_value <= 0 and equity > 0:
        total_value = equity

    # 杠杆倍数 = 总资产 / 自有资金
    leverage = total_value / equity if equity > 0 else 1.0

    # 融资部分
    loan = total_value - equity
    if loan < 0:
        loan = 0
        leverage = 1.0

    # 维持担保比例
    maintenance = 1.3  # 130%
    liquidation_price_ratio = maintenance * equity / total_value if total_value > 0 else 1.0

    # 最大可承受下跌
    max_drawdown_before_liquidation = (1 - 1 / leverage) if leverage > 1 else 1.0
    max_dd_pct = max_drawdown_before_liquidation * 100

    # 保证金利用率
    margin_used = loan / total_value * 100 if total_value > 0 else 0
    margin_available = margin_pct * total_value if margin_pct > 0 else 0
    margin_remaining = max(margin_available - loan, 0) if margin_available > 0 else 0

    print(f"\n⚠️ 保证金/杠杆风险评估")
    print(f"   {'='*45}")
    print(f"   自有资金:      {equity:,.2f}")
    print(f"   总持仓市值:    {total_value:,.2f}")
    print(f"   融资负债:      {loan:,.2f}")
    print(f"   {'='*45}")

    if leverage > 1:
        print(f"   杠杆倍数:      {leverage:.2f}x")
        print(f"   保证金比例:    {margin_pct*100:.0f}%")
        print(f"   保证金利用率:  {margin_used:.1f}%")
        print(f"   剩余保证金:    {margin_remaining:,.2f}")
        print(f"   {'='*45}")
        print(f"   维持担保比例:  {maintenance:.0f}%")
        print(f"   强平前最大下跌:{max_dd_pct:.1f}%")
        print(f"   {'='*45}")

        # 风险评级
        if leverage >= 4:
            risk = "🔴 极高"
            advice = "强烈建议立即降杠杆，爆仓风险极大"
        elif leverage >= 2.5:
            risk = "🟡 高"
            advice = "建议逐步降低杠杆，预留更多安全垫"
        elif leverage >= 1.5:
            risk = "🟢 中等"
            advice = "杠杆适中，但需关注市场波动"
        else:
            risk = "✅ 低"
            advice = "杠杆水平安全"

        print(f"   风险等级:      {risk}")
        print(f"   建议:          {advice}")

        # 跌幅压力测试
        print(f"\n   跌幅压力测试:")
        print(f"   {'跌幅':<10} {'净资产':<12} {'担保比例':<10} {'状态':<10}")
        print(f"   {'-'*45}")
        for drop in [5, 10, 15, 20, 25]:
            new_value = total_value * (1 - drop / 100)
            new_equity = new_value - loan
            if new_equity <= 0:
                status = "💀 穿仓"
            elif new_value / max(loan, 1) < maintenance:
                status = "🔴 追保"
            else:
                status = "✅ 安全"
            guarantee_ratio = new_value / max(loan, 1)
            print(f"   -{drop:<5}%  {new_equity:<10,.0f}  {guarantee_ratio:<8.1f}x  {status}")
    else:
        print(f"   杠杆倍数:      1.00x (无融资)")
        print(f"   风险等级:      ✅ 无杠杆风险")


# ── 主入口 ───────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="Stock Planner v1.1 — 智能交易计划生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python3 scripts/stock_planner.py --positions pos.csv\n"
            "  python3 scripts/stock_planner.py compare --plan1 a.json --plan2 b.json\n"
            "  python3 scripts/stock_planner.py rebalance --positions pos.csv --target \"tech:30,food:20\"\n"
            "  python3 scripts/stock_planner.py correlation --price-data prices.csv\n"
            "  python3 scripts/stock_planner.py history --dir plans/\n"
            "  python3 scripts/stock_planner.py leverage --margin 0.5 --capital 500000\n"
        ),
    )

    sp = p.add_subparsers(dest="command", required=True)

    # plan (default)
    plan_p = sp.add_parser("plan", help="生成交易计划（默认）")
    plan_p.add_argument("--positions", required=True, help="持仓CSV文件")
    plan_p.add_argument("--market", default=DEFAULT_MARKET, choices=list(MARKET_STATES.keys()), help="市场状态")
    plan_p.add_argument("--cash", type=float, default=0, help="可用资金")
    plan_p.add_argument("--capital", type=float, default=0, help="总资产")
    plan_p.add_argument("--output", help="保存计划为JSON")
    plan_p.add_argument("--json", action="store_true", help="JSON格式输出")

    # compare
    cmp_p = sp.add_parser("compare", help="多计划对比")
    cmp_p.add_argument("--plan1", required=True, help="计划1 JSON")
    cmp_p.add_argument("--plan2", required=True, help="计划2 JSON")

    # rebalance
    reb_p = sp.add_parser("rebalance", help="组合再平衡")
    reb_p.add_argument("--positions", required=True, help="持仓CSV")
    reb_p.add_argument("--target", required=True, help='目标配置，如 "tech:30,food:20,health:25,cash:25"')
    reb_p.add_argument("--cash", type=float, default=0, help="可用现金")

    # correlation
    corr_p = sp.add_parser("correlation", help="持仓相关性分析")
    corr_p.add_argument("--price-data", required=True, help="价格CSV（列为股票代码，行为时间点）")

    # history
    hist_p = sp.add_parser("history", help="多日规划回顾")
    hist_p.add_argument("--dir", required=True, help="计划JSON目录")

    # leverage
    lev_p = sp.add_parser("leverage", help="杠杆风险评估")
    lev_p.add_argument("--positions", help="持仓CSV")
    lev_p.add_argument("--margin", type=float, default=0.5, help="保证金比例（默认0.5）")
    lev_p.add_argument("--capital", type=float, default=0, help="自有资金")

    args = p.parse_args()

    if args.command == "plan":
        if not _validate_file(args.positions):
            return
        positions = read_positions(args.positions)
        plan = generate_plan(positions, args.market, args.cash, args.capital)
        if args.json or args.output:
            print(json.dumps(plan, indent=2, ensure_ascii=False))
        else:
            print_plan(plan)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(plan, f, indent=2, ensure_ascii=False)
            print(f"📄 已保存: {args.output}")

    elif args.command == "compare":
        cmd_compare(args)
    elif args.command == "rebalance":
        cmd_rebalance(args)
    elif args.command == "correlation":
        cmd_correlation(args)
    elif args.command == "history":
        cmd_history(args)
    elif args.command == "leverage":
        cmd_leverage(args)


if __name__ == "__main__":
    main()
