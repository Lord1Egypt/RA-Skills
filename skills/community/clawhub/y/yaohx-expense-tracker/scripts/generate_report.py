#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
月度消费报告生成脚本
读取指定月份的消费记录，生成分类汇总报告

用法:
    python3 generate_report.py [YYYYMM]

    不带参数：生成当前月份的消费报告
    带参数：生成指定月份的消费报告，如 python3 generate_report.py 202606
"""

import json
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict


def get_workspace():
    """获取 skill 根目录（expense-tracker 目录）"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_categories(workspace):
    """加载消费分类"""
    categories_path = os.path.join(workspace, "categories.json")
    if not os.path.exists(categories_path):
        return {}
    with open(categories_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {c["name"]: c for c in data.get("categories", [])}


def load_expenses(workspace, year_month):
    """加载指定月份的消费记录"""
    filepath = os.path.join(workspace, "expenses", f"expenses-{year_month}.json")
    if not os.path.exists(filepath):
        return None, []
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return filepath, data.get("expenses", [])


def load_previous_month_expenses(workspace, year_month):
    """加载上个月的消费记录"""
    year = int(year_month[:4])
    month = int(year_month[4:6])
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1
    prev_ym = f"{prev_year}{prev_month:02d}"
    _, expenses = load_expenses(workspace, prev_ym)
    return prev_ym, expenses


def generate_report(year_month, expenses, categories, prev_expenses):
    """生成月度消费报告"""
    if not expenses:
        return {
            "year_month": year_month,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_amount": 0,
            "total_count": 0,
            "avg_daily": 0,
            "max_single": None,
            "category_breakdown": {},
            "payment_breakdown": {},
            "comparison_with_prev": None,
            "message": "本月暂无消费记录。"
        }

    # 总支出
    total_amount = sum(e["amount"] for e in expenses)
    total_count = len(expenses)

    # 计算天数（从当月第一天到最后一天或到今天）
    dates = set(e["date"] for e in expenses)
    if dates:
        min_date = min(dates)
        max_date = max(dates)
        days = (datetime.strptime(max_date, "%Y-%m-%d") -
                datetime.strptime(min_date, "%Y-%m-%d")).days + 1
    else:
        days = 1
    avg_daily = round(total_amount / max(days, 1), 2)

    # 单笔最高
    max_expense = max(expenses, key=lambda e: e["amount"])
    max_single = {
        "amount": max_expense["amount"],
        "merchant": max_expense["merchant"],
        "date": max_expense["date"],
        "category": max_expense.get("category", "")
    }

    # 分类汇总
    category_breakdown = defaultdict(lambda: {"amount": 0, "count": 0})
    for e in expenses:
        cat = e.get("category", "其他")
        category_breakdown[cat]["amount"] += e["amount"]
        category_breakdown[cat]["count"] += 1

    # 计算百分比
    for cat, data in category_breakdown.items():
        data["amount"] = round(data["amount"], 2)
        data["percentage"] = round(data["amount"] / total_amount * 100, 1) if total_amount > 0 else 0

    # 按金额降序排列
    category_breakdown = dict(
        sorted(category_breakdown.items(), key=lambda x: x[1]["amount"], reverse=True)
    )

    # 支付方式分布
    payment_breakdown = defaultdict(lambda: {"amount": 0, "count": 0})
    for e in expenses:
        pm = e.get("payment_method", "未知")
        payment_breakdown[pm]["amount"] += e["amount"]
        payment_breakdown[pm]["count"] += 1

    for pm, data in payment_breakdown.items():
        data["amount"] = round(data["amount"], 2)

    payment_breakdown = dict(
        sorted(payment_breakdown.items(), key=lambda x: x[1]["amount"], reverse=True)
    )

    # 与上月对比
    comparison = None
    if prev_expenses:
        prev_total = sum(e["amount"] for e in prev_expenses)
        prev_count = len(prev_expenses)
        if prev_total > 0:
            change_pct = round((total_amount - prev_total) / prev_total * 100, 1)
            comparison = {
                "prev_total": round(prev_total, 2),
                "prev_count": prev_count,
                "change_amount": round(total_amount - prev_total, 2),
                "change_percentage": change_pct,
                "trend": "⬆️ 增加" if change_pct > 0 else ("⬇️ 减少" if change_pct < 0 else "➡️ 持平")
            }

    # 添加分类图标
    category_breakdown_with_icon = {}
    for cat, data in category_breakdown.items():
        icon = categories.get(cat, {}).get("icon", "")
        category_breakdown_with_icon[cat] = {
            **data,
            "icon": icon
        }

    report = {
        "year_month": year_month,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_amount": round(total_amount, 2),
        "total_count": total_count,
        "avg_daily": avg_daily,
        "max_single": max_single,
        "category_breakdown": category_breakdown_with_icon,
        "payment_breakdown": payment_breakdown,
        "comparison_with_prev": comparison
    }

    return report


def format_report(report):
    """格式化报告为人类可读文本"""
    if "message" in report:
        return report["message"]

    ym = report["year_month"]
    year = ym[:4]
    month = int(ym[4:6])

    lines = []
    lines.append(f"📊 {year}年{month}月消费报告")
    lines.append("=" * 35)
    lines.append(f"📅 生成时间: {report['generated_at']}")
    lines.append(f"")
    lines.append(f"💰 总支出: ¥{report['total_amount']:,.2f}")
    lines.append(f"📝 消费笔数: {report['total_count']} 笔")
    lines.append(f"📊 日均消费: ¥{report['avg_daily']:,.2f}")
    lines.append(f"")

    if report["max_single"]:
        ms = report["max_single"]
        lines.append(f"🔝 单笔最高: ¥{ms['amount']:,.2f} ({ms['merchant']}, {ms['date']})")
        lines.append(f"")

    # 分类明细
    lines.append("📂 分类明细:")
    lines.append("-" * 35)
    for cat, data in report["category_breakdown"].items():
        icon = data.get("icon", "")
        bar = "█" * int(data["percentage"] / 2)
        lines.append(f"  {icon} {cat}: ¥{data['amount']:,.2f} ({data['percentage']}%) {bar}")
    lines.append(f"")

    # 支付方式
    lines.append("💳 支付方式:")
    lines.append("-" * 35)
    for pm, data in report["payment_breakdown"].items():
        lines.append(f"  {pm}: ¥{data['amount']:,.2f} ({data['count']}笔)")

    # 与上月对比
    if report.get("comparison_with_prev"):
        cmp = report["comparison_with_prev"]
        lines.append(f"")
        lines.append(f"📈 与上月对比:")
        lines.append(f"  上月支出: ¥{cmp['prev_total']:,.2f}")
        lines.append(f"  变化: {cmp['trend']} ¥{abs(cmp['change_amount']):,.2f} ({cmp['change_percentage']}%)")

    lines.append(f"")
    lines.append("=" * 35)

    return "\n".join(lines)


def save_report(filepath, report):
    """将报告保存到消费记录文件的 monthly_summaries 字段"""
    if not filepath or not os.path.exists(filepath):
        return

    with open(filepath, "r", encoding="utf-8") as f:
        monthly_data = json.load(f)

    if "monthly_summaries" not in monthly_data:
        monthly_data["monthly_summaries"] = {}

    monthly_data["monthly_summaries"][report["year_month"]] = report
    monthly_data["last_updated"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(monthly_data, f, ensure_ascii=False, indent=2)


def main():
    # 确定要报告的年月
    if len(sys.argv) > 1:
        year_month = sys.argv[1]
        # 验证格式
        if not re.match(r'^\d{6}$', year_month):
            print(f"[错误] 日期格式不正确，应为 YYYYMM，如 202606", file=sys.stderr)
            sys.exit(1)
    else:
        year_month = datetime.now().strftime("%Y%m")

    workspace = get_workspace()

    # 加载数据
    categories = load_categories(workspace)
    filepath, expenses = load_expenses(workspace, year_month)
    prev_ym, prev_expenses = load_previous_month_expenses(workspace, year_month)

    if expenses is None:
        print(f"[错误] 未找到 {year_month} 月的消费记录文件")
        sys.exit(1)

    # 生成报告
    report = generate_report(year_month, expenses, categories, prev_expenses)

    # 保存报告到文件
    save_report(filepath, report)

    # 输出报告
    print(format_report(report))

    # 同时输出 JSON 格式（供程序读取）
    print("\n--- JSON ---")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    import re
    main()
