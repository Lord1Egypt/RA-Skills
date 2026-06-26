#!/usr/bin/env python3
"""财务分析工具 - 付费版
用法: python3 financial_analysis.py [--data-file <路径>] [--period <YYYY-MM>]

基于记账数据生成财务分析报告：
- 利润表摘要
- 税负率分析
- 同比环比对比
- 关键财务指标
"""

import argparse
import json
import os
import sys
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bookkeeping_data.json")


def load_data(data_file=None):
    """加载记账数据"""
    path = data_file or DATA_FILE
    if not os.path.exists(path):
        return {"records": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _analyze_records(records, period):
    """分析单个期间的记录列表"""
    period_records = [r for r in records if r["date"].startswith(period)]
    return _analyze_from_records(period_records, period)


def _analyze_from_records(period_records, period):
    """从记录列表分析"""
    income = sum(r["amount"] for r in period_records if r["type"] == "income")
    expenses = sum(r["amount"] for r in period_records if r["type"] == "expense")
    by_category = {}
    for r in period_records:
        cat = r["category"]
        by_category[cat] = by_category.get(cat, 0) + r["amount"]
    return {
        "period": period,
        "income": income,
        "expenses": expenses,
        "profit": income - expenses,
        "by_category": by_category,
        "record_count": len(period_records),
        "margin": (income - expenses) / income * 100 if income > 0 else 0,
    }


def analyze_period(data, period):
    """分析单个期间（兼容旧接口）"""
    records = [r for r in data["records"] if r["date"].startswith(period)]
    return _analyze_from_records(records, period)


def calc_tax_burden(records, income):
    """计算税负率"""
    tax_items = [
        ("增值税", "income"),
        ("附加税", "income"),
        ("企业所得税", "profit"),
    ]

    # 简化计算
    if income > 0:
        vat = income * 0.01 if income <= 100000 else income * 0.01
        surcharge = vat * 0.12
        profit = income * 0.3  # 假设利润率30%
        cit = profit * 0.05 if profit <= 3000000 else profit * 0.25
        total_tax = vat + surcharge + cit
        burden_rate = total_tax / income * 100
    else:
        total_tax = 0
        burden_rate = 0

    return {
        "total_tax": total_tax,
        "vat": vat if income > 0 else 0,
        "surcharge": surcharge if income > 0 else 0,
        "cit": cit if income > 0 else 0,
        "burden_rate": burden_rate,
    }


def generate_report(data, period=None):
    """生成财务分析报告"""
    records = data["records"]
    use_mock = False
    if not records:
        # Mock data
        records = [
            {"date": "2024-01-10", "type": "income", "amount": 120000, "category": "收入", "desc": "1月服务费"},
            {"date": "2024-01-15", "type": "expense", "amount": 30000, "category": "工资", "desc": "工资"},
            {"date": "2024-01-20", "type": "expense", "amount": 5000, "category": "房租", "desc": "房租"},
            {"date": "2024-02-10", "type": "income", "amount": 95000, "category": "收入", "desc": "2月服务费"},
            {"date": "2024-02-15", "type": "expense", "amount": 30000, "category": "工资", "desc": "工资"},
            {"date": "2024-02-20", "type": "expense", "amount": 5000, "category": "房租", "desc": "房租"},
            {"date": "2024-03-10", "type": "income", "amount": 150000, "category": "收入", "desc": "3月项目款"},
            {"date": "2024-03-15", "type": "expense", "amount": 35000, "category": "工资", "desc": "工资+奖金"},
            {"date": "2024-03-20", "type": "expense", "amount": 5000, "category": "房租", "desc": "房租"},
            {"date": "2024-03-25", "type": "expense", "amount": 8000, "category": "办公费", "desc": "设备采购"},
        ]
        use_mock = True

    # 按月份分组
    months = {}
    for r in records:
        m = r["date"][:7]
        if m not in months:
            months[m] = []
        months[m].append(r)

    analyses = []
    for m in sorted(months.keys()):
        analyses.append(_analyze_records(records, m))

    # 总体
    total_income = sum(a["income"] for a in analyses)
    total_expenses = sum(a["expenses"] for a in analyses)
    total_profit = total_income - total_expenses
    avg_margin = total_profit / total_income * 100 if total_income > 0 else 0

    # 税负率
    tax_burden = calc_tax_burden(records if not use_mock else [], total_income)

    # 环比分析
    mom = []
    for i in range(1, len(analyses)):
        prev = analyses[i - 1]
        curr = analyses[i]
        income_change = ((curr["income"] - prev["income"]) / prev["income"] * 100
                         if prev["income"] > 0 else 0)
        profit_change = ((curr["profit"] - prev["profit"]) / abs(prev["profit"]) * 100
                         if prev["profit"] != 0 else 0)
        mom.append({
            "from": prev["period"],
            "to": curr["period"],
            "income_change": income_change,
            "profit_change": profit_change,
        })

    return {
        "period_range": f"{analyses[0]['period']} ~ {analyses[-1]['period']}" if analyses else "N/A",
        "summary": {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "total_profit": total_profit,
            "avg_margin": avg_margin,
            "months_analyzed": len(analyses),
        },
        "monthly": analyses,
        "tax_burden": tax_burden,
        "mom_analysis": mom,
    }


def format_report(report):
    """格式化财务报告"""
    s = report["summary"]
    lines = [
        f"\n📊 财务分析报告",
        f"{'='*50}",
        f"  分析期间: {report['period_range']}",
        f"  分析月数: {s['months_analyzed']} 个月",
        "",
        "  📈 利润表摘要",
        f"    总收入:   ¥{s['total_income']:>12,.2f}",
        f"    总支出:   ¥{s['total_expenses']:>12,.2f}",
        f"    净利润:   ¥{s['total_profit']:>12,.2f} {'🟢' if s['total_profit'] >= 0 else '🔴'}",
        f"    利润率:   {s['avg_margin']:.1f}%",
        "",
        "  📂 费用构成",
    ]

    # 汇总类别（仅支出）
    all_cats = {}
    for m in report["monthly"]:
        for cat, amt in m["by_category"].items():
            if cat != "收入":  # 收入不列入费用
                all_cats[cat] = all_cats.get(cat, 0) + amt

    total_exp = s["total_expenses"]
    for cat in sorted(all_cats.keys(), key=lambda x: all_cats[x], reverse=True):
        amt = all_cats[cat]
        pct = amt / total_exp * 100 if total_exp > 0 else 0
        bar = "█" * int(pct / 5)
        lines.append(f"    {cat:<8s} ¥{amt:>10,.2f} ({pct:5.1f}%) {bar}")

    tb = report["tax_burden"]
    lines.extend([
        "",
        "  💰 税负分析",
        f"    综合税负率: {tb['burden_rate']:.2f}%",
        f"    增值税: ¥{tb['vat']:,.2f}",
        f"    附加税: ¥{tb['surcharge']:,.2f}",
        f"    企业所得税: ¥{tb['cit']:,.2f}",
    ])

    if report["mom_analysis"]:
        lines.append("")
        lines.append("  📊 环比分析")
        for m in report["mom_analysis"]:
            inc = f"+{m['income_change']:.1f}%" if m["income_change"] >= 0 else f"{m['income_change']:.1f}%"
            prf = f"+{m['profit_change']:.1f}%" if m["profit_change"] >= 0 else f"{m['profit_change']:.1f}%"
            lines.append(f"    {m['from']}→{m['to']}: 收入 {inc}  利润 {prf}")

    lines.extend([
        "",
        "  💡 解锁完整版可生成标准财务报表(利润表/资产负债表/现金流量表)。",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="财务分析工具")
    parser.add_argument("--data-file", help="记账数据文件路径")
    parser.add_argument("--period", help="指定分析期间 (YYYY-MM)")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    data = load_data(args.data_file)
    report = generate_report(data, args.period)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(format_report(report))


if __name__ == "__main__":
    main()
