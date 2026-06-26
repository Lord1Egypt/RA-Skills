#!/usr/bin/env python3
"""
账本查询工具（CSV 格式版）

支持按月份、分类、账户余额查询。
仅依赖 Python 标准库。

CSV 格式：日期,类型,金额,分类,描述,账户
- 类型：支出 / 收入
- 无层级账户，无双行条目

用法:
    python query_ledger.py /path/to/ledger.csv
    python query_ledger.py /path/to/ledger.csv --month 2026-05
    python query_ledger.py /path/to/ledger.csv --category
    python query_ledger.py /path/to/ledger.csv --balance
    python query_ledger.py /path/to/ledger.csv --month 2026-05 --category
"""

import csv
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict


# ==================== CSV 读取（原创实现） ====================

def parse_csv_line(line: str) -> dict:
    """
    解析 CSV 行，返回字典或 None。
    支持：
    - 标准 CSV（6个字段，无引号）
    - 描述字段含逗号（引号包裹）—— csv.reader 自动处理
    - 描述字段含逗号但未引号（取前6段，容忍冗余逗号）
    - 余额行：余额,账户,金额
    """
    line = line.strip()
    if not line or line.startswith('#'):
        return None

    # 余额行: 余额,账户,金额
    if line.startswith('余额,'):
        parts = line.split(',', 2)
        if len(parts) >= 3:
            try:
                return {
                    'balance_entry': True,
                    'account': parts[1].strip(),
                    'balance': float(parts[2].strip()),
                }
            except ValueError:
                return None
        return None

    # 交易行：使用 csv 模块解析（正确处理引号包裹的逗号）
    parts = next(csv.reader([line]))
    # 容忍描述中有冗余逗号（取前6列）
    if len(parts) < 6:
        return None
    parts = parts[:6]

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


def read_entries(ledger_path: str) -> list:
    """读取账本所有交易条目（不含余额行）。"""
    path = Path(ledger_path)
    if not path.exists():
        print(f"❌ 文件不存在: {ledger_path}")
        sys.exit(1)

    entries = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        e = parse_csv_line(line)
        # 只收集交易条目，排除余额行、注释行等
        if e and 'balance_entry' not in e:
            entries.append(e)
    return entries


def read_balances(ledger_path: str) -> dict:
    """
    读取初始余额配置。
    支持两种格式：
    1. CSV 余额行（优先）：余额,账户,金额
    2. 注释余额行（旧兼容）：# 余额 账户 金额
    """
    path = Path(ledger_path)
    if not path.exists():
        return {}
    balances = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            # 注释行：# 余额 账户 金额
            if stripped.startswith('# 余额 '):
                parts = stripped[2:].strip().split()
                if len(parts) >= 3:
                    balances[parts[1]] = float(parts[2])
        else:
            # CSV 余额行：余额,账户,金额
            if stripped.startswith('余额,'):
                parts = stripped.split(',', 2)
                if len(parts) >= 3:
                    try:
                        balances[parts[1].strip()] = float(parts[2].strip())
                    except ValueError:
                        pass
    return balances


# ==================== 查询函数 ====================

def query_by_month(entries: list, month: str = None) -> dict:
    """按月份统计收支。

    与传统双行记账的根本区别：
    - 不需要解析借贷 posting，直接按 type（支出/收入）判断
    - 无需账户层级匹配，直接用 category 字段
    """
    data = defaultdict(lambda: {"收入": 0.0, "支出": 0.0})

    for e in entries:
        e_month = e["date"][:7]
        t = e["type"]
        amt = e["amount"]
        data[e_month][t] += amt

    if month:
        d = data.get(month, {"收入": 0.0, "支出": 0.0})
        return {
            "month": month,
            "income": d["收入"],
            "expense": d["支出"],
            "net": d["收入"] - d["支出"],
        }
    else:
        result = {}
        for m in sorted(data.keys()):
            d = data[m]
            result[m] = {
                "income": d["收入"],
                "expense": d["支出"],
                "net": d["收入"] - d["支出"],
            }
        return result


def query_by_category(entries: list, month: str = None) -> dict:
    """按分类统计收支。"""
    expense_cats = defaultdict(float)
    income_cats = defaultdict(float)

    for e in entries:
        if month and e["date"][:7] != month:
            continue
        amt = e["amount"]
        cat = e["category"]
        if e["type"] == "支出":
            expense_cats[cat] += amt
        elif e["type"] == "收入":
            income_cats[cat] += amt

    return {
        "支出": dict(sorted(expense_cats.items(), key=lambda x: x[1], reverse=True)),
        "收入": dict(sorted(income_cats.items(), key=lambda x: x[1], reverse=True)),
    }


def calc_balance(account: str, entries: list, initial_balances: dict) -> float:
    """计算账户余额。

    余额 = 初始余额 + SUM(收入) - SUM(支出)
    无需借贷平衡计算（单边记账）。
    """
    balance = initial_balances.get(account, 0.0)
    for e in entries:
        if e["account"] == account:
            if e["type"] == "收入":
                balance += e["amount"]
            elif e["type"] == "支出":
                balance -= e["amount"]
    return balance


def query_balance(entries: list, initial_balances: dict) -> dict:
    """查询所有有交易的账户余额。"""
    accounts = set(e["account"] for e in entries)
    result = {}
    for acc in sorted(accounts):
        result[acc] = calc_balance(acc, entries, initial_balances)
    return result


# ==================== 格式化输出 ====================

def fmt(amount: float) -> str:
    """格式化金额。"""
    return f"¥{amount:,.2f}" if abs(amount) >= 10000 else f"¥{amount:.2f}"


def print_monthly(data: dict):
    """打印月度收支概览。"""
    if isinstance(data, dict) and "month" in data:
        d = data
        print(f"\n{'='*50}")
        print(f"  📊 {d['month']} 收支概览")
        print(f"{'='*50}")
        print(f"  收入：{fmt(d['income']):>15}")
        print(f"  支出：{fmt(d['expense']):>15}")
        print(f"  净额：{fmt(d['net']):>15}")
        print(f"{'='*50}\n")
    else:
        print(f"\n{'='*60}")
        print(f"  📊 月度收支总览")
        print(f"{'='*60}")
        print(f"  {'月份':<12} {'收入':>12} {'支出':>12} {'净额':>12}")
        print(f"  {'-'*48}")
        total_income = total_expense = 0
        for m in sorted(data.keys()):
            d = data[m]
            total_income += d["income"]
            total_expense += d["expense"]
            net_color = "🟢" if d["net"] >= 0 else "🔴"
            print(f"  {m:<12} {fmt(d['income']):>12} {fmt(d['expense']):>12} {net_color}{fmt(d['net']):>12}")
        print(f"  {'-'*48}")
        print(f"  {'合计':<12} {fmt(total_income):>12} {fmt(total_expense):>12} {fmt(total_income - total_expense):>12}")
        print(f"{'='*60}\n")


def print_category(data: dict):
    """打印分类统计。"""
    expense = data.get("支出", {})
    income = data.get("收入", {})

    if expense:
        total = sum(expense.values())
        print(f"\n{'='*50}")
        print(f"  📋 支出分类统计")
        print(f"{'='*50}")
        for cat, amount in expense.items():
            pct = (amount / total * 100) if total > 0 else 0
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"  {cat:<10} {fmt(amount):>12}  {pct:5.1f}%  {bar}")
        print(f"  {'─'*40}")
        print(f"  {'合计':<10} {fmt(total):>12}")
        print(f"{'='*50}\n")

    if income:
        total = sum(income.values())
        print(f"{'='*50}")
        print(f"  💰 收入分类统计")
        print(f"{'='*50}")
        for cat, amount in income.items():
            pct = (amount / total * 100) if total > 0 else 0
            print(f"  {cat:<10} {fmt(amount):>12}  {pct:5.1f}%")
        print(f"  {'─'*40}")
        print(f"  {'合计':<10} {fmt(total):>12}")
        print(f"{'='*50}\n")


def print_balance(data: dict):
    """打印账户余额。"""
    if not data:
        print("\n  没有找到账户数据。\n")
        return

    print(f"\n{'='*50}")
    print(f"  💳 账户余额")
    print(f"{'='*50}")
    for acc, bal in sorted(data.items()):
        sign = "+" if bal >= 0 else ""
        print(f"  {acc:<20} {sign}{fmt(bal):>15}")
    print(f"\n{'='*50}\n")


# ==================== CLI ====================

def main():
    parser = argparse.ArgumentParser(
        description="账本查询工具（CSV 格式）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python query_ledger.py ./my.csv
  python query_ledger.py ./my.csv --month 2026-05
  python query_ledger.py ./my.csv --category
  python query_ledger.py ./my.csv --balance
  python query_ledger.py ./my.csv --month 2026-05 --category
        """,
    )

    parser.add_argument("ledger", help="账本文件路径（CSV 格式）")
    parser.add_argument("--month", metavar="YYYY-MM", help="按月份查询")
    parser.add_argument("--category", action="store_true", help="按分类统计")
    parser.add_argument("--balance", action="store_true", help="查询账户余额")

    args = parser.parse_args()

    show_all = not (args.month or args.category or args.balance)

    entries = read_entries(args.ledger)
    balances = read_balances(args.ledger)

    if not entries:
        print("⚠️  账本中没有交易记录。")
        sys.exit(0)

    print(f"📂 已加载 {len(entries)} 条交易记录\n")

    if args.month or show_all:
        data = query_by_month(entries, args.month)
        print_monthly(data)

    if args.category or (show_all and args.month):
        data = query_by_category(entries, args.month)
        print_category(data)

    if args.balance or show_all:
        data = query_balance(entries, balances)
        print_balance(data)


if __name__ == "__main__":
    main()