#!/usr/bin/env python3
"""
Rental Property Return Calculator
Usage: python calc-return.py <input-json> <output-path>

Input format:
{
  "property": { "price": 10000000, "area": 30 },
  "rental": { "monthly_rent": 25000, "vacancy_rate": 0.05 },
  "costs": {
    "loan_interest_monthly": 8000,
    "property_tax_yearly": 5000,
    "land_tax_yearly": 2000,
    "insurance_yearly": 3000,
    "management_fee_monthly": 2000,
    "maintenance_yearly": 15000,
    "agency_fee": 0.10
  }
}
"""

import json, sys, os
from datetime import datetime

def calc_return(data):
    p = data.get('property', {})
    r = data.get('rental', {})
    c = data.get('costs', {})

    price = p.get('price', 0)
    monthly_rent = r.get('monthly_rent', 0)
    vacancy_rate = r.get('vacancy_rate', 0.05)
    
    loan_interest = c.get('loan_interest_monthly', 0) * 12
    property_tax = c.get('property_tax_yearly', 0)
    land_tax = c.get('land_tax_yearly', 0)
    insurance = c.get('insurance_yearly', 0)
    management_fee = c.get('management_fee_monthly', 0) * 12
    maintenance = c.get('maintenance_yearly', 0)
    agency_fee = c.get('agency_fee', 0)

    # 年租金收入
    gross_yearly = monthly_rent * 12
    vacancy_loss = gross_yearly * vacancy_rate
    agency_cost = gross_yearly * agency_fee if agency_fee > 0 else 0
    net_yearly = gross_yearly - vacancy_loss - agency_cost

    # 年支出
    yearly_costs = loan_interest + property_tax + land_tax + insurance + management_fee + maintenance
    
    # 年淨現金流
    yearly_cashflow = net_yearly - yearly_costs

    # 投報率計算
    if price > 0:
        gross_roi = (gross_yearly / price) * 100
        net_roi = (yearly_cashflow / price) * 100
    else:
        gross_roi = 0
        net_roi = 0

    # 自備款投報率（假設貸款8成）
    down_payment = price * 0.2
    if down_payment > 0:
        cash_on_cash = (yearly_cashflow / down_payment) * 100
    else:
        cash_on_cash = 0

    # 租金回本年限
    payback_years = price / net_yearly if net_yearly > 0 else float('inf')
    
    # 資金活用判斷
    if yearly_cashflow > 0:
        verdict = "✅ 正現金流，此物件可考慮持有。"
    else:
        verdict = "⚠️ 負現金流，需補貼！考慮降低貸款或提高租金。"

    return {
        "gross_yearly": round(gross_yearly),
        "vacancy_loss": round(vacancy_loss),
        "agency_cost": round(agency_cost),
        "net_yearly": round(net_yearly),
        "loan_interest": round(loan_interest),
        "property_tax": round(property_tax),
        "land_tax": round(land_tax),
        "insurance": round(insurance),
        "management_fee": round(management_fee),
        "maintenance": round(maintenance),
        "total_costs": round(yearly_costs),
        "yearly_cashflow": round(yearly_cashflow),
        "monthly_cashflow": round(yearly_cashflow / 12),
        "gross_roi": round(gross_roi, 2),
        "net_roi": round(net_roi, 2),
        "cash_on_cash": round(cash_on_cash, 2),
        "payback_years": round(payback_years, 1) if payback_years != float('inf') else "N/A",
        "verdict": verdict,
        "price": price,
        "monthly_rent": monthly_rent,
        "down_payment": round(down_payment)
    }

def generate_report(data, output_path):
    result = calc_return(data)

    report = f"""# 📊 包租代管投報率分析報告

## 基本條件

| 項目 | 金額 |
|------|------|
| 房屋總價 | {result['price']:,} 元 |
| 自備款（20%） | {result['down_payment']:,} 元 |
| 月租金 | {result['monthly_rent']:,} 元 |

## 年收支明細

### 年收入
| 項目 | 金額 |
|------|------|
| 年租金收入（{result['monthly_rent']:,}×12） | {result['gross_yearly']:,} 元 |
| 空置損失（約{data['rental']['vacancy_rate']*100:.0f}%） | -{result['vacancy_loss']:,} 元 |
| 代管費 | -{result['agency_cost']:,} 元 |
| **實際年收入** | **{result['net_yearly']:,} 元** |

### 年支出
| 項目 | 金額 |
|------|------|
| 房貸利息 | {result['loan_interest']:,} 元 |
| 房屋稅 | {result['property_tax']:,} 元 |
| 地價稅 | {result['land_tax']:,} 元 |
| 保險 | {result['insurance']:,} 元 |
| 管理費 | {result['management_fee']:,} 元 |
| 修繕預備金 | {result['maintenance']:,} 元 |
| **年支出合計** | **{result['total_costs']:,} 元** |

## 投報率分析

| 指標 | 數值 |
|------|:----:|
| 年淨現金流 | {result['yearly_cashflow']:,} 元 |
| 月淨現金流 | {result['monthly_cashflow']:,} 元 |
| **總價報酬率（毛報酬）** | **{result['gross_roi']}%** |
| **總價報酬率（淨報酬）** | **{result['net_roi']}%** |
| **自備款報酬率（Cash-on-Cash）** | **{result['cash_on_cash']}%** |
| 租金回本年限 | {result['payback_years']} 年 |

## 結論

{result['verdict']}

---
*試算日期：{datetime.now().strftime('%Y-%m-%d')}
*本分析為概估，實際狀況依市場變動*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f'✅ 投報率分析報告已產出：{output_path}')
    print(f'   毛報酬率：{result["gross_roi"]}% | 淨報酬率：{result["net_roi"]}% | 現金流：{result["monthly_cashflow"]:,}/月')

def main():
    if len(sys.argv) < 3:
        print('Usage: python calc-return.py <input-json> <output-path>')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f'❌ 找不到輸入檔案：{input_path}')
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    generate_report(data, output_path)

if __name__ == '__main__':
    main()
