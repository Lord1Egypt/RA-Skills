#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个税计算工具 — 支持月度累计预扣、年终奖优化对比、劳务报酬预扣

使用方式:
  python calculate_tax.py --monthly-salary 15000 --social-insurance 2250 --special-deduction 3000 --bonus 30000
  python calculate_tax.py --config case.json --output-dir ./output

JSON 配置格式:
{
  "monthly_salary": 15000,
  "social_insurance": 2250,
  "housing_fund": 0,
  "special_deduction": 3000,
  "bonus": 30000,
  "other_income": 0,
  "months": 12
}
"""

import argparse
import json
import os
from datetime import datetime

TAX_BRACKETS = [
    (36000, 0.03, 0),
    (144000, 0.10, 2520),
    (300000, 0.20, 16920),
    (420000, 0.25, 31920),
    (660000, 0.30, 52920),
    (960000, 0.35, 85920),
    (float('inf'), 0.45, 181920),
]

BONUS_TAX_BRACKETS = [
    (3000, 0.03, 0),
    (12000, 0.10, 210),
    (25000, 0.20, 1410),
    (35000, 0.25, 2660),
    (55000, 0.30, 4410),
    (80000, 0.35, 7160),
    (float('inf'), 0.45, 15160),
]

MONTHLY_DEDUCTION = 5000


def calc_tax(taxable_income):
    if taxable_income <= 0:
        return 0
    for limit, rate, quick_deduction in TAX_BRACKETS:
        if taxable_income <= limit:
            return taxable_income * rate - quick_deduction
    return 0


def calc_bonus_tax_separate(bonus):
    if bonus <= 0:
        return 0
    monthly_avg = bonus / 12
    for limit, rate, quick_deduction in BONUS_TAX_BRACKETS:
        if monthly_avg <= limit:
            return bonus * rate - quick_deduction
    return 0


def calc_bonus_tax_combined(bonus, annual_salary, annual_deductions):
    combined_income = annual_salary + bonus
    taxable = combined_income - annual_deductions
    if taxable <= 0:
        return 0
    annual_tax = calc_tax(taxable)
    salary_tax = calc_tax(annual_salary - annual_deductions) if annual_salary - annual_deductions > 0 else 0
    return annual_tax - salary_tax


def calculate_monthly_tax(monthly_salary, social_insurance, housing_fund, special_deduction, months=12):
    results = []
    cumulative_income = 0
    cumulative_deduction = 0
    cumulative_tax = 0
    cumulative_taxable = 0

    monthly_total_deduction = (MONTHLY_DEDUCTION + social_insurance + housing_fund + special_deduction)

    for month in range(1, months + 1):
        cumulative_income += monthly_salary
        cumulative_deduction += monthly_total_deduction
        cumulative_taxable = cumulative_income - cumulative_deduction
        if cumulative_taxable < 0:
            cumulative_taxable = 0

        cumulative_tax_should = calc_tax(cumulative_taxable)
        month_tax = cumulative_tax_should - cumulative_tax
        if month_tax < 0:
            month_tax = 0

        cumulative_tax = cumulative_tax_should
        net_income = monthly_salary - social_insurance - housing_fund - month_tax

        results.append({
            "month": month,
            "monthly_salary": monthly_salary,
            "social_insurance": social_insurance + housing_fund,
            "special_deduction": special_deduction,
            "tax": round(month_tax, 2),
            "net_income": round(net_income, 2),
            "cumulative_tax": round(cumulative_tax, 2),
        })

    return results


def generate_report(monthly_salary, social_insurance, housing_fund, special_deduction, bonus, other_income, months, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    monthly_results = calculate_monthly_tax(monthly_salary, social_insurance, housing_fund, special_deduction, months)

    annual_salary = monthly_salary * months
    annual_deductions = (MONTHLY_DEDUCTION + social_insurance + housing_fund + special_deduction) * months
    annual_tax_only_salary = sum(r["tax"] for r in monthly_results)

    bonus_separate_tax = 0
    bonus_combined_tax = 0
    bonus_recommendation = ""

    if bonus > 0:
        bonus_separate_tax = calc_bonus_tax_separate(bonus)
        bonus_combined_tax = calc_bonus_tax_combined(bonus, annual_salary, annual_deductions)

        if bonus_combined_tax < bonus_separate_tax:
            bonus_recommendation = "并入综合所得计税更优"
        else:
            bonus_recommendation = "单独计税更优"

        for limit, _, _ in BONUS_TAX_BRACKETS:
            threshold = limit * 12
            if bonus > threshold and bonus <= threshold + 12:
                bonus_recommendation += f"\n警告：年终奖 {bonus} 元处于临界点附近，多1元可能多缴数千元税！"
                break

    lines = []
    lines.append("# 个人所得税计算报告")
    lines.append("")
    lines.append(f"**生成日期：** {datetime.now().strftime('%Y年%m月%d日')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 基础信息")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("|------|------|")
    lines.append(f"| 月工资 | ¥{monthly_salary:,.2f} |")
    lines.append(f"| 五险一金个人部分 | ¥{social_insurance + housing_fund:,.2f} |")
    lines.append(f"| 专项附加扣除 | ¥{special_deduction:,.2f}/月 |")
    lines.append(f"| 年终奖 | ¥{bonus:,.2f} |")
    if other_income:
        lines.append(f"| 其他收入 | ¥{other_income:,.2f} |")
    lines.append(f"| 计算月数 | {months}个月 |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 月度预扣预缴明细")
    lines.append("")
    lines.append("| 月份 | 月工资 | 五险一金 | 专项附加扣除 | 当月税额 | 税后收入 | 累计已缴税 |")
    lines.append("|------|--------|---------|-------------|---------|---------|-----------|")
    for r in monthly_results:
        lines.append(f"| {r['month']}月 | ¥{r['monthly_salary']:,.2f} | ¥{r['social_insurance']:,.2f} | ¥{r['special_deduction']:,.2f} | ¥{r['tax']:,.2f} | ¥{r['net_income']:,.2f} | ¥{r['cumulative_tax']:,.2f} |")
    lines.append(f"| **合计** | | | | **¥{annual_tax_only_salary:,.2f}** | | |")
    lines.append("")

    if bonus > 0:
        lines.append("---")
        lines.append("")
        lines.append("## 年终奖计税对比")
        lines.append("")
        lines.append("| 计税方式 | 税额 | 说明 |")
        lines.append("|---------|------|------|")
        lines.append(f"| 单独计税 | ¥{bonus_separate_tax:,.2f} | 年终奖÷12确定税率 |")
        lines.append(f"| 并入综合所得 | ¥{bonus_combined_tax:,.2f} | 与工资合并计税 |")
        lines.append(f"| **推荐方式** | | **{bonus_recommendation}** |")
        lines.append("")
        lines.append(f"**两种方式差额：** ¥{abs(bonus_separate_tax - bonus_combined_tax):,.2f}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 年度汇总")
    lines.append("")
    lines.append("| 项目 | 金额 |")
    lines.append("|------|------|")
    lines.append(f"| 年度税前总收入（不含年终奖） | ¥{annual_salary:,.2f} |")
    lines.append(f"| 年度五险一金合计 | ¥{(social_insurance + housing_fund) * months:,.2f} |")
    lines.append(f"| 年度专项附加扣除合计 | ¥{special_deduction * months:,.2f} |")
    lines.append(f"| 年度基本减除费用 | ¥{MONTHLY_DEDUCTION * months:,.2f} |")
    lines.append(f"| 工资部分已预缴税额 | ¥{annual_tax_only_salary:,.2f} |")
    if bonus > 0:
        lines.append(f"| 年终奖推荐计税税额 | ¥{min(bonus_separate_tax, bonus_combined_tax):,.2f} |")
        total_tax = annual_tax_only_salary + min(bonus_separate_tax, bonus_combined_tax)
        lines.append(f"| **年度总税额（最优方案）** | **¥{total_tax:,.2f}** |")
        total_income = annual_salary + bonus
        total_deductions = (social_insurance + housing_fund) * months
        net_annual = total_income - total_deductions - total_tax
        lines.append(f"| **年度税后总收入** | **¥{net_annual:,.2f}** |")
    else:
        lines.append(f"| **年度总税额** | **¥{annual_tax_only_salary:,.2f}** |")
        net_annual = annual_salary - (social_insurance + housing_fund) * months - annual_tax_only_salary
        lines.append(f"| **年度税后总收入** | **¥{net_annual:,.2f}** |")
    lines.append("")
    lines.append("> 注意：以上计算基于输入参数，实际以个税APP汇算清缴结果为准。")
    lines.append("")

    report_path = os.path.join(output_dir, "个税计算报告.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"个税计算报告已生成：{report_path}")
    if bonus > 0:
        print(f"年终奖推荐：{bonus_recommendation}")
        print(f"两种方式差额：¥{abs(bonus_separate_tax - bonus_combined_tax):,.2f}")
    print(f"年度总税额：¥{annual_tax_only_salary + (min(bonus_separate_tax, bonus_combined_tax) if bonus > 0 else 0):,.2f}")
    print(f"输出目录：{output_dir}")


def main():
    parser = argparse.ArgumentParser(description='个税计算工具')
    parser.add_argument('--monthly-salary', type=float, default=0, help='月工资')
    parser.add_argument('--social-insurance', type=float, default=0, help='五险一金个人部分')
    parser.add_argument('--housing-fund', type=float, default=0, help='补充公积金个人部分')
    parser.add_argument('--special-deduction', type=float, default=0, help='专项附加扣除月度合计')
    parser.add_argument('--bonus', type=float, default=0, help='年终奖')
    parser.add_argument('--other-income', type=float, default=0, help='其他收入')
    parser.add_argument('--months', type=int, default=12, help='计算月数')
    parser.add_argument('--config', help='案件信息JSON文件路径')
    parser.add_argument('--output-dir', default='./output', help='输出目录')

    args = parser.parse_args()

    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            data = json.load(f)
        monthly_salary = data.get('monthly_salary', 0)
        social_insurance = data.get('social_insurance', 0)
        housing_fund = data.get('housing_fund', 0)
        special_deduction = data.get('special_deduction', 0)
        bonus = data.get('bonus', 0)
        other_income = data.get('other_income', 0)
        months = data.get('months', 12)
    else:
        monthly_salary = args.monthly_salary
        social_insurance = args.social_insurance
        housing_fund = args.housing_fund
        special_deduction = args.special_deduction
        bonus = args.bonus
        other_income = args.other_income
        months = args.months

    generate_report(monthly_salary, social_insurance, housing_fund, special_deduction, bonus, other_income, months, args.output_dir)


if __name__ == '__main__':
    main()
