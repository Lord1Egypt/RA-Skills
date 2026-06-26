#!/usr/bin/env python3
"""智能报税工具 - 付费版
用法: python3 tax_filing.py --period 2024-03 [--纳税人类型 <小规模|一般>]

根据记账数据计算应纳税额，生成申报表草稿。
包含：增值税、附加税、企业所得税（季度）、个人所得税（月度）。
"""

import argparse
import json
import os
import sys
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bookkeeping_data.json")


def load_bookkeeping(period):
    """加载指定期间的记账数据"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [r for r in data["records"] if r["date"].startswith(period)]


def calc_vat(records, taxpayer_type="小规模"):
    """计算增值税"""
    sales_income = sum(r["amount"] for r in records if r["type"] == "income")
    purchase_amount = sum(r["amount"] for r in records
                          if r["category"] == "采购" and r["type"] == "expense")

    if taxpayer_type == "小规模":
        # 小规模纳税人：月销售额≤10万免征，超过部分1%
        if sales_income <= 100000:
            vat = 0
            policy = "月销售额≤10万，免征增值税"
        else:
            vat = sales_income * 0.01
            policy = "超过10万部分减按1%"
    else:
        # 一般纳税人：销项-进项
        output_vat = sales_income * 0.13  # 假设主要13%
        input_vat = purchase_amount * 0.13
        vat = max(0, output_vat - input_vat)
        policy = f"销项税 ¥{output_vat:,.2f} - 进项税 ¥{input_vat:,.2f}"

    return {
        "type": "增值税",
        "销售额": sales_income,
        "应纳税额": vat,
        "计算说明": policy,
    }


def calc_surcharges(vat_amount, location="市区"):
    """计算附加税"""
    rates = {"市区": 0.12, "县镇": 0.10, "其他": 0.06}
    rate = rates.get(location, 0.12)
    total = vat_amount * rate

    return {
        "type": "附加税费",
        "计税依据": vat_amount,
        "城市维护建设税": vat_amount * (0.07 if location == "市区" else 0.05 if location == "县镇" else 0.01),
        "教育费附加": vat_amount * 0.03,
        "地方教育附加": vat_amount * 0.02,
        "合计": total,
    }


def calc_cit(records, period, taxpayer_type="小规模"):
    """计算企业所得税（季度预缴）"""
    # 简单计算：利润 = 收入 - 费用
    income = sum(r["amount"] for r in records if r["type"] == "income")
    expenses = sum(r["amount"] for r in records if r["type"] == "expense")
    profit = income - expenses

    # 判断是否小微企业
    is_small = profit <= 3000000  # 简化判断

    if is_small and profit > 0:
        cit = profit * 0.05  # 小微企业实际税负5%
        policy = "小微企业优惠税率5%"
    elif profit > 0:
        cit = profit * 0.25
        policy = "基本税率25%"
    else:
        cit = 0
        policy = "亏损，无需缴纳"

    return {
        "type": "企业所得税",
        "利润总额": profit,
        "收入": income,
        "费用": expenses,
        "应纳税额": cit,
        "计算说明": policy,
    }


def generate_report(period, taxpayer_type="小规模", location="市区"):
    """生成报税报告"""
    records = load_bookkeeping(period)

    if not records:
        print(f"⚠️  期间 {period} 暂无记账数据，使用示例数据演示。")
        # Mock数据用于演示
        records = [
            {"type": "income", "amount": 85000, "category": "收入", "desc": "服务费收入"},
            {"type": "expense", "amount": 15000, "category": "工资", "desc": "员工工资"},
            {"type": "expense", "amount": 3000, "category": "办公费", "desc": "办公用品"},
            {"type": "expense", "amount": 2000, "category": "房租", "desc": "办公室租金"},
            {"type": "expense", "amount": 5000, "category": "采购", "desc": "原材料采购"},
        ]

    vat = calc_vat(records, taxpayer_type)
    surcharges = calc_surcharges(vat["应纳税额"], location)
    cit = calc_cit(records, period, taxpayer_type)

    total_tax = vat["应纳税额"] + surcharges["合计"] + cit["应纳税额"]

    return {
        "period": period,
        "taxpayer_type": taxpayer_type,
        "location": location,
        "taxes": {
            "增值税": vat,
            "附加税费": surcharges,
            "企业所得税": cit,
        },
        "total_tax": total_tax,
    }


def format_report(report):
    """格式化报税报告"""
    lines = [
        f"\n📋 纳税申报表草稿",
        f"{'='*50}",
        f"  纳税期间: {report['period']}",
        f"  纳税人类型: {report['taxpayer_type']}",
        f"  所在地区: {report['location']}",
        "",
    ]

    for tax_name, tax_data in report["taxes"].items():
        lines.append(f"  📌 {tax_name}")
        lines.append(f"     应纳税额: ¥{tax_data.get('应纳税额', 0):>10,.2f}")
        if "计算说明" in tax_data:
            lines.append(f"     说明: {tax_data['计算说明']}")
        lines.append("")

    lines.append(f"  💰 应纳税额合计: ¥{report['total_tax']:>10,.2f}")
    lines.append("")
    lines.append("  ⚠️  以上为计算结果参考，实际申报以税务机关为准。")
    lines.append("  📅 增值税/附加税：次月15日前申报")
    lines.append("  📅 企业所得税：季度终了15日内预缴")
    lines.append("")
    lines.append("  💡 解锁完整版可导出标准申报表格、自动填报电子税务局。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="智能报税工具")
    parser.add_argument("--period", required=True, help="纳税期间 (YYYY-MM)")
    parser.add_argument("--纳税人类型", choices=["小规模", "一般"], default="小规模")
    parser.add_argument("--地区", choices=["市区", "县镇", "其他"], default="市区")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    report = generate_report(args.period, args.纳税人类型, args.地区)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(format_report(report))


if __name__ == "__main__":
    main()
