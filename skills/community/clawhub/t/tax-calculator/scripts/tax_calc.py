#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国税务计算工具
支持：增值税、企业所得税、个人所得税、土地增值税、印花税
"""

def calc_vat_general(sales_excl_tax, input_tax, rate=0.13, city_type='city'):
    """一般纳税人增值税计算"""
    output_tax = sales_excl_tax * rate
    vat = output_tax - input_tax
    city_rates = {'city': 0.07, 'town': 0.05, 'rural': 0.01}
    city_rate = city_rates.get(city_type, 0.07)
    urban_tax = vat * city_rate
    edu_levy = vat * 0.03
    local_edu = vat * 0.02
    total = vat + urban_tax + edu_levy + local_edu
    return {
        '销项税额': round(output_tax, 2),
        '进项税额': round(input_tax, 2),
        '应纳增值税': round(vat, 2),
        '城建税': round(urban_tax, 2),
        '教育费附加': round(edu_levy, 2),
        '地方教育附加': round(local_edu, 2),
        '合计流转税': round(total, 2)
    }

def calc_vat_small(sales_excl_tax, rate=0.01):
    """小规模纳税人增值税计算（默认优惠税率1%）"""
    vat = sales_excl_tax * rate
    urban_tax = vat * 0.07
    edu_levy = vat * 0.03
    local_edu = vat * 0.02
    total = vat + urban_tax + edu_levy + local_edu
    return {
        '不含税销售额': round(sales_excl_tax, 2),
        '应纳增值税': round(vat, 2),
        '城建税': round(urban_tax, 2),
        '教育费附加': round(edu_levy, 2),
        '地方教育附加': round(local_edu, 2),
        '合计': round(total, 2)
    }

def calc_cit(taxable_income, rate=0.25, rd_extra_deduction=0, is_small=False):
    """企业所得税计算"""
    if is_small and taxable_income <= 3000000:
        rate = 0.05
    actual_taxable = taxable_income - rd_extra_deduction
    tax = actual_taxable * rate
    saving = rd_extra_deduction * rate
    return {
        '应纳税所得额': round(taxable_income, 2),
        '研发加计扣除': round(rd_extra_deduction, 2),
        '实际计税所得': round(actual_taxable, 2),
        '适用税率': f'{rate*100}%',
        '应纳所得税': round(tax, 2),
        '研发扣除节税': round(saving, 2)
    }

def calc_iit_salary(annual_income, special_deduction=0, additional_deduction=0):
    """个人所得税-综合所得（年度）"""
    basic_deduction = 60000
    taxable = annual_income - basic_deduction - special_deduction - additional_deduction
    taxable = max(taxable, 0)

    brackets = [
        (36000,    0.03, 0),
        (144000,   0.10, 2520),
        (300000,   0.20, 16920),
        (420000,   0.25, 31920),
        (660000,   0.30, 52920),
        (960000,   0.35, 85920),
        (float('inf'), 0.45, 181920),
    ]

    tax = 0
    rate_used = 0
    deduction_used = 0
    for limit, rate, quick_deduct in brackets:
        if taxable <= limit:
            tax = taxable * rate - quick_deduct
            rate_used = rate
            deduction_used = quick_deduct
            break

    return {
        '年度综合所得': round(annual_income, 2),
        '基本减除费用': basic_deduction,
        '专项扣除': round(special_deduction, 2),
        '专项附加扣除': round(additional_deduction, 2),
        '应纳税所得额': round(taxable, 2),
        '适用税率': f'{rate_used*100}%',
        '速算扣除数': deduction_used,
        '应纳个人所得税': round(max(tax, 0), 2)
    }

def calc_iit_equity_transfer(transfer_price, original_cost, expenses=0):
    """个人所得税-股权转让"""
    taxable = transfer_price - original_cost - expenses
    tax = max(taxable, 0) * 0.20
    return {
        '股权转让收入': round(transfer_price, 2),
        '股权原值': round(original_cost, 2),
        '合理费用': round(expenses, 2),
        '应纳税所得额': round(taxable, 2),
        '适用税率': '20%',
        '应纳个人所得税': round(tax, 2)
    }

def calc_land_vat(revenue, land_cost, dev_cost, dev_expense_rate=0.10, is_residential=True):
    """土地增值税计算"""
    dev_expense = (land_cost + dev_cost) * dev_expense_rate
    extra_deduction = (land_cost + dev_cost) * 0.20 if is_residential else 0

    # 扣除项目金额
    deductions = land_cost + dev_cost + dev_expense + extra_deduction
    # 增值额
    appreciation = revenue - deductions
    # 增值率
    appreciation_rate = appreciation / deductions if deductions > 0 else 0

    brackets = [
        (0.5,  0.30, 0),
        (1.0,  0.40, 0.05),
        (2.0,  0.50, 0.15),
        (float('inf'), 0.60, 0.35),
    ]

    tax = 0
    rate_used = 0
    for limit, rate, quick_rate in brackets:
        if appreciation_rate <= limit:
            tax = appreciation * rate - deductions * quick_rate
            rate_used = rate
            break

    return {
        '收入额': round(revenue, 2),
        '扣除项目合计': round(deductions, 2),
        '  其中-取得土地成本': round(land_cost, 2),
        '  其中-开发成本': round(dev_cost, 2),
        '  其中-开发费用': round(dev_expense, 2),
        '  其中-加计扣除(20%)': round(extra_deduction, 2),
        '增值额': round(appreciation, 2),
        '增值率': f'{appreciation_rate*100:.1f}%',
        '适用税率': f'{rate_used*100}%',
        '应纳土地增值税': round(max(tax, 0), 2)
    }

def calc_stamp_duty(contract_amount, duty_type='sales'):
    """印花税计算"""
    rates = {
        'loan': 0.00005,        # 借款合同 0.005%
        'sales': 0.0003,        # 买卖合同 0.03%
        'construction': 0.0003, # 建筑工程 0.03%
        'tech': 0.0003,         # 技术合同 0.03%
        'property': 0.0005,     # 产权转移 0.05%
        'account_book': 0.00025,# 营业账簿 0.025%
    }
    rate = rates.get(duty_type, 0.0003)
    tax = contract_amount * rate
    return {
        '合同/凭证金额': round(contract_amount, 2),
        '税率': f'{rate*100}%',
        '应纳印花税': round(tax, 2)
    }

def compare_scenarios(scenarios):
    """多方案税负对比"""
    print("\n" + "="*60)
    print("税负对比分析")
    print("="*60)
    for i, (name, result) in enumerate(scenarios, 1):
        print(f"\n方案{i}：{name}")
        print("-"*40)
        for k, v in result.items():
            print(f"  {k}: {v}")
    print("="*60)

# ==================== 示例使用 ====================
if __name__ == '__main__':
    print("=" * 50)
    print("中国税务计算工具")
    print("=" * 50)

    # 示例1：一般纳税人增值税
    print("\n【示例1】一般纳税人增值税计算")
    r = calc_vat_general(sales_excl_tax=1000000, input_tax=80000, rate=0.13)
    for k, v in r.items():
        print(f"  {k}: {v:,.2f} 元")

    # 示例2：企业所得税（高新技术企业）
    print("\n【示例2】高新技术企业所得税（含研发加计扣除）")
    r = calc_cit(taxable_income=5000000, rate=0.15, rd_extra_deduction=200000)
    for k, v in r.items():
        print(f"  {k}: {v}")

    # 示例3：个人所得税（年薪）
    print("\n【示例3】个人所得税（年薪80万，专项附加扣除3.6万）")
    r = calc_iit_salary(annual_income=800000, special_deduction=30000, additional_deduction=36000)
    for k, v in r.items():
        print(f"  {k}: {v}")

    # 示例4：股权转让
    print("\n【示例4】股权转让个人所得税")
    r = calc_iit_equity_transfer(transfer_price=5000000, original_cost=1000000, expenses=50000)
    for k, v in r.items():
        print(f"  {k}: {v}")

    # 示例5：土地增值税
    print("\n【示例5】土地增值税计算")
    r = calc_land_vat(revenue=10000000, land_cost=3000000, dev_cost=2000000)
    for k, v in r.items():
        print(f"  {k}: {v}")
