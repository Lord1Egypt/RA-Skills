#!/usr/bin/env python3
"""
计算租房预算
用法: python calculate_budget.py --rent 5000 --deposit "押一付三" [--agency 2500] [--other 500]
"""

import argparse

def calculate_budget(args):
    """计算租房预算"""
    rent = args.rent
    deposit_months = 1
    
    # 解析押金方式
    if args.deposit:
        if "押一" in args.deposit:
            deposit_months = 1
        elif "押二" in args.deposit:
            deposit_months = 2
        elif "押三" in args.deposit:
            deposit_months = 3
    
    # 计算各项费用
    deposit = rent * deposit_months
    first_month_rent = rent
    agency_fee = args.agency or 0
    other_fees = args.other or 0
    
    # 首月总支出
    first_month_total = deposit + first_month_rent + agency_fee + other_fees
    
    # 月均成本（假设租期一年）
    monthly_other = args.monthly_other or 0
    monthly_cost = rent + monthly_other
    
    # 年总成本
    annual_cost = rent * 12 + monthly_other * 12 + agency_fee + other_fees
    
    # 输出结果
    print("\n" + "="*50)
    print("💰 租房预算分析")
    print("="*50)
    
    print(f"\n📋 基础信息:")
    print(f"   月租金: {rent}元")
    print(f"   押金方式: {args.deposit or '押一付三'}")
    print(f"   押金金额: {deposit}元")
    
    print(f"\n💸 首月支出:")
    print(f"   押金: {deposit}元")
    print(f"   首月租金: {first_month_rent}元")
    if agency_fee:
        print(f"   中介费: {agency_fee}元")
    if other_fees:
        print(f"   其他费用: {other_fees}元")
    print(f"   ────────────────")
    print(f"   合计: {first_month_total}元")
    
    print(f"\n📊 月均成本:")
    print(f"   租金: {rent}元")
    if monthly_other:
        print(f"   其他费用: {monthly_other}元")
    print(f"   ────────────────")
    print(f"   月均: {monthly_cost}元")
    
    print(f"\n📈 年总成本: {annual_cost}元")
    
    # 预算建议
    if args.income:
        ratio = (monthly_cost / args.income) * 100
        print(f"\n💡 预算建议:")
        print(f"   月收入: {args.income}元")
        print(f"   租房占比: {ratio:.1f}%")
        if ratio <= 30:
            print(f"   ✅ 占比合理（≤30%）")
        elif ratio <= 40:
            print(f"   ⚠️ 占比偏高（30%-40%），建议控制其他开支")
        else:
            print(f"   ❌ 占比过高（>40%），可能影响生活质量")
    
    print("="*50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="计算租房预算")
    parser.add_argument("--rent", type=int, required=True, help="月租金")
    parser.add_argument("--deposit", help="押金方式（如：押一付三）")
    parser.add_argument("--agency", type=int, help="中介费")
    parser.add_argument("--other", type=int, help="其他一次性费用")
    parser.add_argument("--monthly-other", type=int, help="月均其他费用（物业+网费等）")
    parser.add_argument("--income", type=int, help="月收入（用于计算占比）")
    
    args = parser.parse_args()
    calculate_budget(args)
