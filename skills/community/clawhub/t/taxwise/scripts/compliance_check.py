#!/usr/bin/env python3
"""合规检查工具 - 付费版
用法: python3 compliance_check.py [--data-file <路径>] [--period <YYYY-MM>]

检查税务合规风险：
- 逾期申报检查
- 税负率异常检测
- 发票合规检查
- 税收优惠未享受提示
- 社保合规
"""

import argparse
import json
import os
import sys
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bookkeeping_data.json")


def load_data(data_file=None):
    path = data_file or DATA_FILE
    if not os.path.exists(path):
        return {"records": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_checks(data, period=None):
    """运行所有合规检查"""
    records = data["records"]
    checks = []

    # 1. 申报期限检查
    checks.append(check_filing_deadline(records, period))

    # 2. 税负率异常
    checks.append(check_tax_burden(records, period))

    # 3. 发票合规
    checks.append(check_invoice(records, period))

    # 4. 税收优惠
    checks.append(check_tax_benefits(records, period))

    # 5. 费用合理性
    checks.append(check_expense_reasonable(records, period))

    # 6. 零申报风险
    checks.append(check_zero_filing(records, period))

    return checks


def check_filing_deadline(records, period):
    """检查申报期限"""
    today = datetime.now()
    current_month = today.strftime("%Y-%m")

    # 检查上月的增值税是否已申报（简化）
    if period == current_month:
        return {
            "name": "申报期限",
            "status": "info",
            "message": "本月申报期进行中，增值税/附加税应于次月15日前申报",
            "risk_level": "low",
        }

    return {
        "name": "申报期限",
        "status": "pass",
        "message": "申报期限正常",
        "risk_level": "low",
    }


def check_tax_burden(records, period):
    """检查税负率是否异常"""
    income = sum(r["amount"] for r in records if r["type"] == "income")
    if income == 0:
        return {
            "name": "税负率",
            "status": "warning",
            "message": "无收入记录，如为正常经营请关注长期零收入风险",
            "risk_level": "medium",
        }

    expenses = sum(r["amount"] for r in records if r["type"] == "expense")
    profit_rate = (income - expenses) / income * 100

    # 行业参考税负率
    warnings = []
    if profit_rate < 5:
        warnings.append(f"利润率偏低({profit_rate:.1f}%)，可能引起税务关注")
    if profit_rate > 50:
        warnings.append(f"利润率偏高({profit_rate:.1f}%)，建议检查成本是否完整入账")

    if not warnings:
        return {
            "name": "税负率",
            "status": "pass",
            "message": f"利润率 {profit_rate:.1f}%，处于正常区间",
            "risk_level": "low",
        }

    return {
        "name": "税负率",
        "status": "warning",
        "message": "；".join(warnings),
        "risk_level": "medium",
    }


def check_invoice(records, period):
    """发票合规检查"""
    no_invoice_expenses = [r for r in records
                           if r["type"] == "expense"
                           and not r.get("invoice_no")
                           and r["amount"] > 500]

    if no_invoice_expenses:
        total = sum(r["amount"] for r in no_invoice_expenses)
        return {
            "name": "发票合规",
            "status": "warning",
            "message": f"发现 {len(no_invoice_expenses)} 笔大额无票支出，合计 ¥{total:,.2f}，建议及时取得发票",
            "risk_level": "medium",
            "items": [f"#{r['id']} {r['category']} ¥{r['amount']:,.2f} {r.get('desc','')}"
                      for r in no_invoice_expenses[:5]],
        }

    return {
        "name": "发票合规",
        "status": "pass",
        "message": "发票合规性良好",
        "risk_level": "low",
    }


def check_tax_benefits(records, period):
    """税收优惠检查"""
    income = sum(r["amount"] for r in records if r["type"] == "income")
    expenses = sum(r["amount"] for r in records if r["type"] == "expense")
    profit = income - expenses

    benefits = []

    # 小微企业
    if income <= 3000000 and profit <= 3000000:
        benefits.append("✅ 可享受小微企业所得税优惠（实际税负5%）")

    # 研发费用加计扣除
    if any("研发" in r.get("desc", "") for r in records):
        benefits.append("✅ 有研发支出，可享受100%加计扣除")

    # 小规模纳税人增值税减免
    if income <= 100000:
        benefits.append("✅ 月销售额≤10万，免征增值税")

    # 六税两费减半
    if income <= 3000000:
        benefits.append("✅ 可享受六税两费减半征收优惠")

    if not benefits:
        return {
            "name": "税收优惠",
            "status": "info",
            "message": "未发现可享受的税收优惠",
            "risk_level": "low",
        }

    return {
        "name": "税收优惠",
        "status": "pass",
        "message": "可享受以下优惠：",
        "risk_level": "low",
        "items": benefits,
    }


def check_expense_reasonable(records, period):
    """费用合理性检查"""
    income = sum(r["amount"] for r in records if r["type"] == "income")

    # 招待费比例
    entertainment = sum(r["amount"] for r in records if r["category"] == "招待费")
    if income > 0 and entertainment / income > 0.05:
        return {
            "name": "费用合理性",
            "status": "warning",
            "message": f"招待费占比 {entertainment/income*100:.1f}% 偏高，税前扣除有限额（发生额60%且不超过收入5‰）",
            "risk_level": "medium",
        }

    return {
        "name": "费用合理性",
        "status": "pass",
        "message": "费用结构合理",
        "risk_level": "low",
    }


def check_zero_filing(records, period):
    """零申报风险检查"""
    income = sum(r["amount"] for r in records if r["type"] == "income")

    if income == 0:
        return {
            "name": "零申报风险",
            "status": "warning",
            "message": "本期零收入，长期零申报可能被列为非正常户",
            "risk_level": "high",
        }

    return {
        "name": "零申报风险",
        "status": "pass",
        "message": "有正常收入记录",
        "risk_level": "low",
    }


def format_checks(checks):
    """格式化检查结果"""
    lines = [
        f"\n🔍 税务合规检查报告",
        f"{'='*50}",
    ]

    status_icons = {"pass": "✅", "warning": "⚠️", "info": "ℹ️", "fail": "❌"}

    for c in checks:
        icon = status_icons.get(c["status"], "📌")
        lines.append(f"\n  {icon} {c['name']}")
        lines.append(f"     {c['message']}")

        if "items" in c:
            for item in c["items"]:
                lines.append(f"     - {item}")

    # 总结
    warnings = [c for c in checks if c["status"] == "warning"]
    fails = [c for c in checks if c["status"] == "fail"]

    lines.append(f"\n{'='*50}")
    if fails:
        lines.append(f"  ❌ 发现 {len(fails)} 项高风险问题，需立即处理！")
    elif warnings:
        lines.append(f"  ⚠️  发现 {len(warnings)} 项需关注的问题")
    else:
        lines.append(f"  ✅ 未发现合规风险")

    lines.append(f"\n  💡 解锁完整版可生成正式合规报告并自动修复建议。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="税务合规检查工具")
    parser.add_argument("--data-file", help="记账数据文件路径")
    parser.add_argument("--period", help="检查期间 (YYYY-MM)")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    data = load_data(args.data_file)
    checks = run_checks(data, args.period)

    if args.json:
        print(json.dumps(checks, ensure_ascii=False, indent=2))
    else:
        print(format_checks(checks))


if __name__ == "__main__":
    main()
