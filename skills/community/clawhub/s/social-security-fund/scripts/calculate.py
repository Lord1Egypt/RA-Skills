#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
五险一金计算器
根据工资和城市，计算个人和企业缴纳部分
"""

import argparse
import json
from city_rates import CITY_RATES

def calculate(salary: float, city: str = "北京", fund_ratio: float = None) -> dict:
    """
    计算五险一金
    
    Args:
        salary: 月薪（税前）
        city: 城市名称
        fund_ratio: 公积金比例（None 则使用默认值）
    
    Returns:
        计算结果字典
    """
    if city not in CITY_RATES:
        # 默认使用北京费率
        city = "北京"
    
    rates = CITY_RATES[city]
    ss_rates = rates["social_security"]
    fund_rates = rates["fund"]
    base = rates["base"]
    
    # 确定缴费基数（在上下限范围内）
    if salary < base["min"]:
        contribution_base = base["min"]
    elif salary > base["max"]:
        contribution_base = base["max"]
    else:
        contribution_base = salary
    
    # 公积金比例
    if fund_ratio is None:
        fund_ratio = fund_rates["default"]
    
    # 个人缴纳部分
    personal = {
        "pension": contribution_base * ss_rates["pension"]["personal"],
        "medical": contribution_base * ss_rates["medical"]["personal"],
        "unemployment": contribution_base * ss_rates["unemployment"]["personal"],
        "work_injury": 0,  # 个人不缴纳
        "maternity": 0,    # 个人不缴纳
        "fund": contribution_base * fund_ratio,
    }
    personal_total = sum(personal.values())
    
    # 企业缴纳部分
    company = {
        "pension": contribution_base * ss_rates["pension"]["company"],
        "medical": contribution_base * ss_rates["medical"]["company"],
        "unemployment": contribution_base * ss_rates["unemployment"]["company"],
        "work_injury": contribution_base * ss_rates["work_injury"]["company"],
        "maternity": contribution_base * ss_rates["maternity"]["company"],
        "fund": contribution_base * fund_ratio,
    }
    company_total = sum(company.values())
    
    # 实发工资估算（税前 - 个人缴纳 - 个税起征点 5000）
    taxable_income = salary - personal_total - 5000
    if taxable_income <= 0:
        tax = 0
    elif taxable_income <= 3000:
        tax = taxable_income * 0.03
    elif taxable_income <= 12000:
        tax = taxable_income * 0.1 - 210
    elif taxable_income <= 25000:
        tax = taxable_income * 0.2 - 1410
    elif taxable_income <= 35000:
        tax = taxable_income * 0.25 - 2660
    elif taxable_income <= 55000:
        tax = taxable_income * 0.3 - 4410
    elif taxable_income <= 80000:
        tax = taxable_income * 0.35 - 7160
    else:
        tax = taxable_income * 0.45 - 15160
    
    net_salary = salary - personal_total - tax
    
    return {
        "city": city,
        "salary": salary,
        "contribution_base": contribution_base,
        "fund_ratio": fund_ratio,
        "personal": {
            "details": personal,
            "total": personal_total,
            "rate": personal_total / salary if salary > 0 else 0,
        },
        "company": {
            "details": company,
            "total": company_total,
            "rate": company_total / salary if salary > 0 else 0,
        },
        "tax": tax,
        "net_salary": net_salary,
        "total_cost": salary + company_total,  # 企业用人总成本
    }

def format_result(result: dict) -> str:
    """格式化输出结果"""
    lines = [
        f"💰 五险一金计算结果",
        f"━━━━━━━━━━━━━━━━",
        f"📍 城市：{result['city']}",
        f"💵 税前工资：¥{result['salary']:,.2f}",
        f"📊 缴费基数：¥{result['contribution_base']:,.2f}",
        f"🏦 公积金比例：{result['fund_ratio']*100:.0f}%",
        f"",
        f"👤 个人缴纳部分：",
        f"   • 养老保险：¥{result['personal']['details']['pension']:,.2f}",
        f"   • 医疗保险：¥{result['personal']['details']['medical']:,.2f}",
        f"   • 失业保险：¥{result['personal']['details']['unemployment']:,.2f}",
        f"   • 住房公积金：¥{result['personal']['details']['fund']:,.2f}",
        f"   ─────────────",
        f"   • 个人合计：¥{result['personal']['total']:,.2f} ({result['personal']['rate']*100:.1f}%)",
        f"",
        f"🏢 企业缴纳部分：",
        f"   • 养老保险：¥{result['company']['details']['pension']:,.2f}",
        f"   • 医疗保险：¥{result['company']['details']['medical']:,.2f}",
        f"   • 失业保险：¥{result['company']['details']['unemployment']:,.2f}",
        f"   • 工伤保险：¥{result['company']['details']['work_injury']:,.2f}",
        f"   • 生育保险：¥{result['company']['details']['maternity']:,.2f}",
        f"   • 住房公积金：¥{result['company']['details']['fund']:,.2f}",
        f"   ─────────────",
        f"   • 企业合计：¥{result['company']['total']:,.2f} ({result['company']['rate']*100:.1f}%)",
        f"",
        f"📋 最终结果：",
        f"   • 个人所得税：¥{result['tax']:,.2f}",
        f"   • 实发工资：¥{result['net_salary']:,.2f}",
        f"   • 企业用人成本：¥{result['total_cost']:,.2f}",
    ]
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="五险一金计算器")
    parser.add_argument("--salary", type=float, required=True, help="月薪（税前）")
    parser.add_argument("--city", type=str, default="北京", help="城市名称")
    parser.add_argument("--fund-ratio", type=float, default=None, help="公积金比例 (0.05-0.12)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    result = calculate(args.salary, args.city, args.fund_ratio)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_result(result))

if __name__ == "__main__":
    main()
