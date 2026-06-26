#!/usr/bin/env python3
"""
月度报告生成器（CSV 格式版）

生成月度收支报告。

CSV 格式账本，无需解析借贷或账户层级。

用法:
    python generate_report.py /path/to/ledger.csv --month 2026-05
    python generate_report.py /path/to/ledger.csv --month 2026-05 --output report.txt
"""

import sys
import argparse
from datetime import datetime
from collections import defaultdict
from pathlib import Path

def _safe_write_path(path: Path) -> bool:
    """安全校验：只允许写入 ~/.openclaw/workspace/ 范围内的路径，返回 True/False"""
    try:
        if str(path.resolve()).startswith(str(Path.home() / ".openclaw" / "workspace")):
            return True
    except Exception:
        pass
    return False



def parse_csv_line(line: str) -> dict:
    """解析 CSV 行。"""
    line = line.strip()
    if not line or line.startswith('#') or line.startswith('账户') or line.startswith('余额'):
        return None
    parts = []
    current = ""
    in_quote = False
    for ch in line:
        if ch == '"':
            in_quote = not in_quote
        elif ch == ',' and not in_quote:
            parts.append(current)
            current = ""
        else:
            current += ch
    parts.append(current)
    if len(parts) != 6:
        return None
    try:
        return {
            "date": parts[0],
            "type": parts[1],
            "amount": float(parts[2]),
            "category": parts[3],
            "description": parts[4],
            "account": parts[5],
        }
    except ValueError:
        return None


def read_entries(filepath: str) -> list:
    """读取账本所有条目。文件不存在时返回空列表（不主动退出）。"""
    path = Path(filepath)
    if not path.exists():
        print(f"⚠️  文件不存在: {filepath}", file=sys.stderr)
        return []
    entries = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        e = parse_csv_line(line)
        if e:
            entries.append(e)
    return entries


def get_prev_month(month: str) -> str:
    """返回上一个月。"""
    y, m = int(month[:4]), int(month[5:7])
    return f"{y-1:04d}-12" if m == 1 else f"{y:04d}-{m-1:02d}"


def calc_month(entries: list, month: str) -> dict:
    """计算指定月份的收支汇总。"""
    income = expense = 0.0
    exp_cats = defaultdict(float)
    inc_cats = defaultdict(float)
    count = 0
    max_expense = 0.0

    for e in entries:
        if e["date"][:7] != month:
            continue
        count += 1
        amt = e["amount"]
        cat = e["category"]
        if e["type"] == "收入":
            income += amt
            inc_cats[cat] += amt
        elif e["type"] == "支出":
            expense += amt
            exp_cats[cat] += amt
            if amt > max_expense:
                max_expense = amt

    # 计算日均消费
    days_in_month = _days_in_month(month)
    daily_avg = expense / days_in_month if days_in_month > 0 else 0.0

    return {
        "income": income,
        "expense": expense,
        "net": income - expense,
        "exp_cats": dict(sorted(exp_cats.items(), key=lambda x: x[1], reverse=True)),
        "inc_cats": dict(sorted(inc_cats.items(), key=lambda x: x[1], reverse=True)),
        "count": count,
        "daily_avg": daily_avg,
        "max_expense": max_expense,
    }


def fmt(v: float) -> str:
    return f"¥{v:,.2f}" if abs(v) >= 10000 else f"¥{v:.2f}"


def _days_in_month(month: str) -> int:
    """返回指定月份的天数。"""
    try:
        from calendar import monthrange
        y, m = int(month[:4]), int(month[5:7])
        return monthrange(y, m)[1]
    except Exception:
        return 30


def pct_change(cur: float, prev: float) -> str:
    if prev == 0:
        return "+∞" if cur > 0 else "N/A"
    c = ((cur - prev) / prev) * 100
    return f"+{c:.1f}%" if c > 0 else f"{c:.1f}%"


def generate_report(entries: list, month: str) -> str:
    """生成月度报告文字。entries 为空时生成「空月报告」。"""
    cur = calc_month(entries, month)
    prev_m = get_prev_month(month)
    prev = calc_month(entries, prev_m)
    sr = (cur["net"] / cur["income"] * 100) if cur["income"] > 0 else 0.0

    L = []
    L.append("=" * 60)
    L.append(f"  📊 月度财务报告 — {month}")
    L.append("=" * 60)
    L.append("")

    # 空账本提示
    if cur["count"] == 0 and prev["count"] == 0:
        L.append("  ⚠️  本月及上月均无交易记录，无法生成有效报告。")
        L.append("  请先记账后再生成月度报告。")
        L.append("")
        L.append("=" * 60)
        return "\n".join(L)

    # 收支概览
    ns = "🟢" if cur["net"] >= 0 else "🔴"
    L.append("  ┌─────────────────────────────────────────┐")
    L.append("  │           收 支 概 览                    │")
    L.append("  ├─────────────────────────────────────────┤")
    L.append(f"  │  交易笔数：    {cur['count']:>5} 笔                  │")
    L.append(f"  │  总收入：  {fmt(cur['income']):>12}                  │")
    L.append(f"  │  总支出：  {fmt(cur['expense']):>12}                  │")
    L.append(f"  │  净收入：  {ns}{fmt(cur['net']):>12}                  │")
    L.append(f"  │  储蓄率：      {sr:>5.1f}%                  │")
    L.append(f"  │  日均消费：{fmt(cur['daily_avg']):>12}                  │")
    if cur['max_expense'] > 0:
        L.append(f"  │  最大单笔：{fmt(cur['max_expense']):>12}                  │")
    L.append("  └─────────────────────────────────────────┘")

    # 环比
    ic = pct_change(cur["income"], prev["income"])
    ec = pct_change(cur["expense"], prev["expense"])
    nc = pct_change(cur["net"], prev["net"])
    ia = "📈" if cur["income"] >= prev["income"] else "📉"
    ea = "📉" if cur["expense"] <= prev["expense"] else "📈"
    na = "📈" if cur["net"] >= prev["net"] else "📉"

    L.append("")
    L.append(f"  ┌─────────────────────────────────────────┐")
    L.append(f"  │       与上月 ({prev_m}) 环比               │")
    L.append("  ├─────────────────────────────────────────┤")
    L.append(f"  │  收入：  {fmt(cur['income']):>10}  {ia} {ic:>8}        │")
    L.append(f"  │  支出：  {fmt(cur['expense']):>10}  {ea} {ec:>8}        │")
    L.append(f"  │  净额：  {fmt(cur['net']):>10}  {na} {nc:>8}        │")
    L.append("  └─────────────────────────────────────────┘")

    # 支出分类
    if cur["exp_cats"]:
        te = cur["expense"]
        L.append("")
        L.append("  ┌─────────────────────────────────────────┐")
        L.append("  │         支出分类占比                     │")
        L.append("  ├─────────────────────────────────────────┤")

        for cat, amt in cur["exp_cats"].items():
            p = (amt / te * 100) if te > 0 else 0
            bl = int(p / 4)
            bar = "█" * bl + "░" * (25 - bl)
            pa = prev["exp_cats"].get(cat, 0)
            cs = f"{pct_change(amt, pa):>7}" if pa > 0 else "  新增  "
            L.append(f"  │  {cat:<8} {fmt(amt):>10}  {p:5.1f}% {cs}  │")
            L.append(f"  │           {bar}                │")

        L.append("  ├─────────────────────────────────────────┤")
        L.append(f"  │  合计：   {fmt(te):>10}                   │")
        L.append("  └─────────────────────────────────────────┘")

    # 收入分类
    if cur["inc_cats"]:
        ti = cur["income"]
        L.append("")
        L.append("  ┌─────────────────────────────────────────┐")
        L.append("  │         收入来源                         │")
        L.append("  ├─────────────────────────────────────────┤")
        for cat, amt in cur["inc_cats"].items():
            p = (amt / ti * 100) if ti > 0 else 0
            L.append(f"  │  {cat:<8} {fmt(amt):>10}  {p:5.1f}%          │")
        L.append("  └─────────────────────────────────────────┘")

    # 洞察
    L.append("")
    L.append("  💡 洞察与建议")
    tips = []

    if sr >= 30:
        tips.append("  ✅ 储蓄率优秀，继续保持！")
    elif sr >= 15:
        tips.append("  👍 储蓄率良好，有进一步提升空间。")
    elif sr >= 5:
        tips.append("  ⚠️ 储蓄率偏低，建议审视非必要支出。")
    elif cur["income"] > 0:
        tips.append("  🔴 储蓄率较低，需要重点关注支出控制。")

    if cur["exp_cats"]:
        top_cat = list(cur["exp_cats"].keys())[0]
        top_amt = list(cur["exp_cats"].values())[0]
        tp = (top_amt / cur["expense"] * 100) if cur["expense"] > 0 else 0
        if tp > 50:
            tips.append(f"  📌 「{top_cat}」占比 {tp:.0f}%，集中度过高，建议优化。")

    if prev["expense"] > 0:
        eg = ((cur["expense"] - prev["expense"]) / prev["expense"]) * 100
        if eg > 20:
            tips.append(f"  📈 本月支出环比增长 {eg:.0f}%，注意控制消费节奏。")
        elif eg < -10:
            tips.append(f"  📉 本月支出环比下降 {-eg:.0f}%，节省有方！")

    if not tips:
        tips.append("  📝 数据正常，保持记账习惯即可。")

    for t in tips:
        L.append(t)

    L.append("")
    L.append("=" * 60)
    L.append(f"  报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    L.append("=" * 60)
    return "\n".join(L)


def main():
    parser = argparse.ArgumentParser(description="月度报告生成器（CSV 格式）")
    parser.add_argument("ledger", help="账本文件路径（CSV 格式）")
    parser.add_argument("--month", required=True, metavar="YYYY-MM", help="报告月份")
    parser.add_argument("--output", "-o", metavar="FILE", help="输出到文件")
    args = parser.parse_args()

    entries = read_entries(args.ledger)

    report = generate_report(entries, args.month)


    if args.output:
        out_path = Path(args.output)
        if not _safe_write_path(out_path):
            print(f"❌ 不允许写入该路径：{args.output}（必须在 ~/.openclaw/workspace/ 范围内）")
            sys.exit(1)
        out_path.write_text(report, encoding="utf-8")
        print(f"\n💾 报告已保存到 {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()