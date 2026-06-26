#!/usr/bin/env python3
"""税务筹划工具 - 付费版
用法: python3 tax_planning.py [--data-file <路径>] [--纳税人类型 <小规模|一般>]

提供节税建议：
- 纳税人身份最优选择
- 税收优惠政策利用
- 费用扣除优化
- 业务架构建议
"""

import argparse
import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bookkeeping_data.json")


def load_data(data_file=None):
    path = data_file or DATA_FILE
    if not os.path.exists(path):
        return {"records": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_planning(data, taxpayer_type="小规模"):
    """分析并生成筹划建议"""
    records = data["records"]
    if not records:
        # Mock data
        records = [
            {"type": "income", "amount": 95000, "category": "收入", "desc": "月服务费"},
            {"type": "expense", "amount": 30000, "category": "工资", "desc": "工资"},
            {"type": "expense", "amount": 5000, "category": "房租", "desc": "房租"},
            {"type": "expense", "amount": 3000, "category": "办公费", "desc": "办公用品"},
        ]

    income = sum(r["amount"] for r in records if r["type"] == "income")
    expenses = sum(r["amount"] for r in records if r["type"] == "expense")
    profit = income - expenses

    suggestions = []

    # 1. 纳税人身份选择
    suggestions.append(analyze_taxpayer_type(income))

    # 2. 小微企业优惠
    suggestions.append(analyze_small_micro(profit))

    # 3. 研发费用加计扣除
    suggestions.append(analyze_rd(records))

    # 4. 费用扣除优化
    suggestions.append(analyze_expense_optimization(records, income))

    # 5. 增值税优惠
    suggestions.append(analyze_vat_benefits(income))

    # 6. 其他优惠
    suggestions.append(analyze_other_benefits(records))

    return {
        "income": income,
        "expenses": expenses,
        "profit": profit,
        "suggestions": suggestions,
    }


def analyze_taxpayer_type(income):
    """纳税人身份选择分析"""
    # 年销售额500万为分界线
    annual = income * 12

    if annual < 5000000:
        small_vat = income * 0.01 if income <= 100000 else income * 0.01
        general_vat = income * 0.13  # 假设无进项
        saving = general_vat - small_vat

        return {
            "category": "纳税人身份",
            "title": "建议维持小规模纳税人",
            "details": f"年销售额约 ¥{annual:,.0f}，低于500万强制登记线。小规模纳税人税负更低，预计比一般纳税人节省 ¥{saving:,.2f}/月。",
            "saving": saving,
            "priority": "high",
        }
    else:
        return {
            "category": "纳税人身份",
            "title": "需登记为一般纳税人",
            "details": "年销售额超过500万，应登记为一般纳税人。建议加强进项税管理，确保取得专用发票抵扣。",
            "saving": 0,
            "priority": "high",
        }


def analyze_small_micro(profit):
    """小微企业优惠分析"""
    if profit > 0 and profit <= 3000000:
        normal_cit = profit * 0.25
        small_cit = profit * 0.05
        saving = normal_cit - small_cit
        return {
            "category": "企业所得税",
            "title": "确认享受小微企业优惠",
            "details": f"年利润 ¥{profit:,.0f}，符合小微企业条件。享受5%实际税负（vs 25%），预计节省 ¥{saving:,.0f}/年。",
            "saving": saving,
            "priority": "high",
        }
    elif profit > 3000000:
        return {
            "category": "企业所得税",
            "title": "接近小微企业标准临界点",
            "details": f"年利润 ¥{profit:,.0f} 接近300万标准。超过部分按25%纳税，建议在年底前合理规划利润（如增加费用支出、提前确认费用）。",
            "saving": 0,
            "priority": "medium",
        }
    return {
        "category": "企业所得税",
        "title": "当前亏损，无需缴纳企业所得税",
        "details": "亏损可结转弥补，最长5年。",
        "saving": 0,
        "priority": "low",
    }


def analyze_rd(records):
    """研发费用加计扣除分析"""
    rd_expense = sum(r["amount"] for r in records
                     if "研发" in r.get("desc", "") or "研发" in r.get("category", ""))

    if rd_expense > 0:
        saving = rd_expense * 1.0 * 0.25  # 100%加计扣除，省25%企税
        return {
            "category": "研发费用",
            "title": "享受研发费用加计扣除",
            "details": f"研发费用 ¥{rd_expense:,.0f}，可按100%加计扣除。额外扣除 ¥{rd_expense:,.0f}，预计节省 ¥{saving:,.0f} 企业所得税。",
            "saving": saving,
            "priority": "high",
        }
    else:
        return {
            "category": "研发费用",
            "title": "无研发费用记录",
            "details": "如有研发活动，建议单独建账，享受100%加计扣除优惠。",
            "saving": 0,
            "priority": "info",
        }


def analyze_expense_optimization(records, income):
    """费用扣除优化"""
    tips = []

    # 招待费
    entertainment = sum(r["amount"] for r in records if r["category"] == "招待费")
    if entertainment > 0:
        limit1 = entertainment * 0.6
        limit2 = income * 0.005
        actual_deduct = min(limit1, limit2)
        non_deduct = entertainment - actual_deduct
        tips.append(f"业务招待费 ¥{entertainment:,.0f}，税前扣除限额 ¥{actual_deduct:,.0f}，超限额 ¥{non_deduct:,.0f} 需纳税调增。")

    # 工资
    salary = sum(r["amount"] for r in records if r["category"] == "工资")
    if salary > 0:
        tips.append(f"工资薪金 ¥{salary:,.0f}/月可全额税前扣除，确保已代扣代缴个税。")

    # 房租
    rent = sum(r["amount"] for r in records if r["category"] == "房租")
    if rent > 0:
        tips.append(f"房租 ¥{rent:,.0f}/月可扣除，确保取得合规发票/租赁合同。")

    return {
        "category": "费用扣除",
        "title": "费用扣除优化建议",
        "details": "；".join(tips) if tips else "费用结构合理，暂无优化建议。",
        "saving": 0,
        "priority": "medium",
    }


def analyze_vat_benefits(income):
    """增值税优惠分析"""
    if income <= 100000:
        return {
            "category": "增值税",
            "title": "月销售额≤10万，免征增值税",
            "details": f"当前月销售额 ¥{income:,.0f}，享受小规模纳税人免征增值税优惠。注意：开具专票的部分不免税。",
            "saving": income * 0.01,
            "priority": "high",
        }
    elif income <= 120000:
        return {
            "category": "增值税",
            "title": "接近免税额度临界点",
            "details": f"月销售额 ¥{income:,.0f}，超过10万需缴纳增值税。建议在合规前提下合理控制开票节奏。",
            "saving": 0,
            "priority": "medium",
        }
    else:
        return {
            "category": "增值税",
            "title": "月销售额超过10万",
            "details": f"月销售额 ¥{income:,.0f}，减按1%征收率。建议取得更多进项抵扣（如升级一般纳税人）。",
            "saving": 0,
            "priority": "medium",
        }


def analyze_other_benefits(records):
    """其他税收优惠"""
    benefits = []

    # 残保金
    salary_count = sum(1 for r in records if r["category"] == "工资")
    if salary_count > 0:
        benefits.append("残疾人就业保障金：如安置残疾人，可按规定减免")

    # 六税两费减半
    benefits.append("六税两费减半：小微企业可享受城建税、教育费附加等减半")

    # 印花税优惠
    benefits.append("印花税：小微企业营业账簿免征")

    return {
        "category": "其他优惠",
        "title": "其他可享优惠",
        "details": "；".join(benefits),
        "saving": 0,
        "priority": "low",
    }


def format_plan(plan):
    """格式化筹划方案"""
    lines = [
        f"\n💡 税务筹划方案",
        f"{'='*50}",
        f"  月收入: ¥{plan['income']:>12,.2f}",
        f"  月支出: ¥{plan['expenses']:>12,.2f}",
        f"  月利润: ¥{plan['profit']:>12,.2f}",
        "",
    ]

    priority_order = {"high": 1, "medium": 2, "low": 3, "info": 4}
    sorted_suggestions = sorted(plan["suggestions"],
                                 key=lambda x: priority_order.get(x["priority"], 5))

    total_saving = 0
    for i, s in enumerate(sorted_suggestions, 1):
        priority_icons = {"high": "🔴 高优先", "medium": "🟡 中优先", "low": "🟢 低优先", "info": "ℹ️ 参考"}
        icon = priority_icons.get(s["priority"], "📌")

        lines.append(f"  {icon} 【{s['category']}】{s['title']}")
        lines.append(f"     {s['details']}")
        if s["saving"] > 0:
            total_saving += s["saving"]
            lines.append(f"     💰 预计节税: ¥{s['saving']:,.2f}/月")
        lines.append("")

    if total_saving > 0:
        lines.append(f"{'='*50}")
        lines.append(f"  💰 预计合计节税: ¥{total_saving:,.2f}/月 (¥{total_saving*12:,.2f}/年)")

    lines.append(f"\n  💡 解锁完整版可获取个性化筹划方案和风险预警。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="税务筹划工具")
    parser.add_argument("--data-file", help="记账数据文件路径")
    parser.add_argument("--纳税人类型", choices=["小规模", "一般"], default="小规模")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    data = load_data(args.data_file)
    plan = analyze_planning(data, args.纳税人类型)

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(format_plan(plan))


if __name__ == "__main__":
    main()
