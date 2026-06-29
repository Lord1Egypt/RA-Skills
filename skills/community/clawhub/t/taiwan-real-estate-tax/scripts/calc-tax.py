#!/usr/bin/env python3
"""
Real Estate Tax Calculator
Usage: python calc-tax.py <input-json> <output-path>

Input format:
{
  "scenario": "sell" | "buy" | "gift" | "inherit",
  "acquisition": { "date": "2020-01", "price": 12000000, "costs": 150000 },
  "sale": { "date": "2026-06", "price": 18000000, "fee_rate": 0.03 },
  "property": { "self_use": true, "years_held": 6, "land_appreciation": 500000 },
  "tax_payer": { "spouse": false, "children": 2, "parent": false }
}
"""

import json, sys, os
from datetime import datetime, date

def calc_house_land_tax(scenario):
    """房地合一稅"""
    price_buy = scenario.get('acquisition', {}).get('price', 0)
    cost_buy = scenario.get('acquisition', {}).get('costs', 0)
    price_sell = scenario.get('sale', {}).get('price', 0)
    fee_rate = scenario.get('sale', {}).get('fee_rate', 0.03)
    land_appr = scenario.get('property', {}).get('land_appreciation', 0)
    years_held = scenario.get('property', {}).get('years_held', 0)
    self_use = scenario.get('property', {}).get('self_use', False)

    # 相關費用
    fee_sell = price_sell * fee_rate
    max_doc_fee = price_sell * 0.05
    actual_fees = cost_buy + fee_sell
    doc_fee = min(actual_fees, max_doc_fee)

    tax_base = price_sell - price_buy - doc_fee - land_appr
    if tax_base < 0:
        return 0, "虧損出售，無房地合一稅"

    # 稅率
    if self_use and years_held >= 6:
        # 自住滿6年
        tax_base_after_exemption = max(0, tax_base - 4000000)
        rate = 0.10
        tax = round(tax_base_after_exemption * rate)
        note = f"自住滿6年，免稅額400萬，稅率10%"
        return tax, note

    if years_held < 2:
        rate = 0.45
    elif years_held < 5:
        rate = 0.35
    elif years_held < 10:
        rate = 0.20
    else:
        rate = 0.15

    tax = round(tax_base * rate)
    note = f"持有{years_held}年，稅率{rate*100:.0f}%，稅基{round(tax_base)}"
    return tax, note

def calc_land_value_tax(price_buy, price_sell, self_use):
    """土地增值稅（簡化版）"""
    rise = price_sell - price_buy
    if rise <= 0:
        return 0, "無漲價"
    multiple = rise / price_buy if price_buy > 0 else 0
    
    if self_use:
        tax = round(rise * 0.10)
        return tax, f"自用住宅稅率10%"
    
    if multiple < 1.0:
        tax = round(rise * 0.20)
        return tax, f"漲價倍數{multiple:.1%}，第1級稅率20%"
    elif multiple < 2.0:
        tax = round(rise * 0.30)
        return tax, f"漲價倍數{multiple:.1%}，第2級稅率30%"
    else:
        tax = round(rise * 0.40)
        return tax, f"漲價倍數{multiple:.1%}，第3級稅率40%"

def calc_deed_tax(assessed_value, reason="買賣"):
    """契稅"""
    rates = {"買賣": 0.06, "贈與": 0.06, "典權": 0.04, "交換": 0.02, "分割": 0.02, "占有": 0.06}
    rate = rates.get(reason, 0.06)
    return round(assessed_value * rate)

def calc_gift_tax(net_value):
    """贈與稅"""
    exemption = 2440000
    net = max(0, net_value - exemption)
    if net <= 0:
        return 0, "低於免稅額244萬，免稅"
    
    if net <= 25000000:
        tax = round(net * 0.10)
    elif net <= 50000000:
        tax = round(net * 0.15 - 1250000)
    else:
        tax = round(net * 0.20 - 3750000)
    
    return tax, f"贈與淨額{round(net)}"

def calc_estate_tax(net_value, children=0, spouse=False, parent=False):
    """遺產稅"""
    exemption = 13330000
    deductions = 0
    if spouse: deductions += 5530000
    if children: deductions += children * 560000
    if parent: deductions += 1380000
    deductions += 1380000  # 喪葬費
    
    net = max(0, net_value - exemption - deductions)
    if net <= 0:
        return 0, "低於免稅額+扣除額，免稅"
    
    if net <= 50000000:
        tax = round(net * 0.10)
    elif net <= 100000000:
        tax = round(net * 0.15 - 2500000)
    else:
        tax = round(net * 0.20 - 7500000)
    
    return tax, f"遺產淨額{round(net)}"

def generate_report(data, output_path):
    scenario = data.get('scenario', 'sell')
    
    if scenario == 'sell':
        hl_tax, hl_note = calc_house_land_tax(data)
        land_tax, land_note = calc_land_value_tax(
            data.get('acquisition', {}).get('price', 0),
            data.get('sale', {}).get('price', 0) * 0.3,  # 假設土地佔30%
            data.get('property', {}).get('self_use', False)
        )
        
        report = f"""# 💰 不動產稅務試算報告

## 基本條件
| 項目 | 金額 |
|------|------|
| 取得價格 | {data['acquisition']['price']:,.0f} 元 |
| 出售價格 | {data['sale']['price']:,.0f} 元 |
| 持有期間 | {data['property']['years_held']} 年 |
| 自住使用 | {'是' if data['property']['self_use'] else '否'} |

## 稅額試算

### 房地合一稅
- **{hl_tax:,} 元**
- 說明：{hl_note}

### 土地增值稅（概估）
- **{land_tax:,} 元**
- 說明：{land_note}

### 合計應繳稅款
- **{hl_tax + land_tax:,} 元**

---
*試算日期：{datetime.now().strftime('%Y-%m-%d')}
*本試算為概估，實際稅額以稅務局核定為準*
"""
    
    elif scenario == 'gift':
        assessed = data.get('property', {}).get('assessed_value', 0)
        deed = calc_deed_tax(assessed, "贈與")
        land_tax, land_note = calc_land_value_tax(0, assessed, False)
        gift_tax, gift_note = calc_gift_tax(assessed)
        total = deed + land_tax + gift_tax

        report = f"""# 💰 不動產贈與稅務試算報告

## 基本條件
| 項目 | 金額 |
|------|------|
| 公告現值+評定現值 | {assessed:,} 元 |
| 贈與年度免稅額 | 2,440,000 元 |

## 稅額試算

### 贈與稅
- **{gift_tax:,} 元**
- 說明：{gift_note}

### 土地增值稅（一般稅率）
- **{land_tax:,} 元**
- 說明：{land_note}

### 契稅
- **{deed:,} 元**
- 稅率：6%

### 稅賦合計
- **{total:,} 元**

## 建議
贈與不動產稅負極重（三重課稅），建議考慮：
1. 低價買賣取代贈與
2. 先售後贈現金
3. 繼承規劃

---
*試算日期：{datetime.now().strftime('%Y-%m-%d')}*
"""
    
    elif scenario == 'inherit':
        assessed = data.get('property', {}).get('assessed_value', 0)
        children = data.get('tax_payer', {}).get('children', 0)
        spouse = data.get('tax_payer', {}).get('spouse', False)
        parent = data.get('tax_payer', {}).get('parent', False)
        estate_tax, estate_note = calc_estate_tax(assessed, children, spouse, parent)

        report = f"""# 💰 不動產繼承稅務試算報告

## 基本條件
| 項目 | 金額 |
|------|------|
| 不動產公告現值+評定現值 | {assessed:,} 元 |
| 有配偶 | {'是' if spouse else '否'} |
| 子女數 | {children} 人 |

## 稅額試算

### 遺產稅
- **{estate_tax:,} 元**
- 說明：{estate_note}

### 土地增值稅
- **0 元**（繼承免徵土增稅）
- 但：繼承後再出售時，前次移轉現值以繼承時為準

### 契稅
- **0 元**（繼承免徵契稅）

## 繼承 vs 贈與比較
| 項目 | 繼承 | 贈與 |
|------|:----:|:----:|
| 土增稅 | 免徵 | 需繳 |
| 契稅 | 免徵 | 需繳 |
| 主要稅種 | 遺產稅 | 贈與稅+土增+契稅 |
| 建議 | ✅ 優先 | ❌ 儘量避免 |

---
*試算日期：{datetime.now().strftime('%Y-%m-%d')}*
"""
    
    else:
        report = f"# 不支援的情境：{scenario}"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f'✅ 稅務試算報告已產出：{output_path}')

def main():
    if len(sys.argv) < 3:
        print('Usage: python calc-tax.py <input-json> <output-path>')
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
