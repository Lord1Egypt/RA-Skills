#!/usr/bin/env python3
"""
Property Valuation Calculator
Usage: python calc-valuation.py <input-json> <output-path>

Input format:
{
  "property": {
    "address": "台北市大安區...",
    "total_area": 45,
    "building_area": 25,
    "common_area": 15,
    "accessory_area": 5,
    "parking_area": 0,
    "parking_type": "none",
    "building_age": 15,
    "floor": 8,
    "total_floors": 14,
    "type": "大樓"
  },
  "comps": [
    { "address": "同棟8樓", "price": 25000000, "area": 45, "days_ago": 60 }
  ],
  "adjustments": {
    "floor_premium": 0,
    "view_premium": 0,
    "condition_premium": -5,
    "location_premium": 0,
    "special_risk": 0
  }
}
"""

import json, sys, os
from datetime import datetime

REGIONAL_BASE = {
    "台北市": {"大安區": 100, "信義區": 105, "中正區": 85, "中山區": 80, "松山區": 85, "內湖區": 65, "南港區": 70, "士林區": 65, "文山區": 50, "萬華區": 50, "大同區": 60, "北投區": 45, "default": 55},
    "新北市": {"板橋區": 55, "永和區": 55, "中和區": 45, "新店區": 50, "三重區": 42, "新莊區": 40, "蘆洲區": 38, "汐止區": 32, "林口區": 35, "淡水區": 24, "三峽區": 32, "default": 30},
    "桃園市": {"桃園區": 35, "中壢區": 32, "龜山區": 28, "default": 22},
    "台中市": {"西屯區": 55, "南屯區": 42, "北屯區": 35, "default": 25},
    "高雄市": {"鼓山區": 40, "左營區": 32, "前鎮區": 27, "default": 20}
}

def estimate_base_price(address):
    """Estimate base price per ping from address string"""
    for city, districts in REGIONAL_BASE.items():
        if city in address:
            for dist, price in districts.items():
                if dist in address:
                    return price * 10000
            return districts.get('default', 25) * 10000
    return 250000  # default

def calc_age_adjustment(age):
    if age <= 5: return 0.98
    elif age <= 10: return 0.92
    elif age <= 15: return 0.85
    elif age <= 20: return 0.78
    elif age <= 25: return 0.72
    elif age <= 30: return 0.65
    elif age <= 35: return 0.58
    elif age <= 40: return 0.52
    else: return 0.45

def calc_valuation(data):
    prop = data.get('property', {})
    adj = data.get('adjustments', {})
    
    total_area = prop.get('total_area', 0)
    parking_area = prop.get('parking_area', 0)
    building_age = prop.get('building_age', 0)
    floor = prop.get('floor', 0)
    total_floors = prop.get('total_floors', 1)
    floor_ratio = floor / total_floors if total_floors > 0 else 0.5
    ptype = prop.get('type', '大樓')
    
    # Main area (ex. parking)
    main_area = max(0.1, total_area - parking_area)
    
    # Base unit price
    base_price = estimate_base_price(prop.get('address', ''))
    
    # Age adjustment
    age_factor = calc_age_adjustment(building_age)
    
    # Type adjustment
    type_factors = {"大樓": 1.0, "華廈": 0.93, "公寓": 0.78, "透天厝": 1.15, "套房": 0.85}
    type_factor = type_factors.get(ptype, 1.0)
    
    # Floor adjustment
    if floor_ratio > 0.7:
        floor_factor = 1.05
    elif floor_ratio > 0.5:
        floor_factor = 1.02
    elif floor_ratio > 0.2:
        floor_factor = 1.0
    else:
        floor_factor = 0.98
    
    # Side adjustments
    side_adjustments = 1.0
    for key in ['floor_premium', 'view_premium', 'condition_premium', 'location_premium', 'special_risk']:
        val = adj.get(key, 0)
        side_adjustments *= (1 + val/100)
    
    # Estimated unit price
    unit_price = base_price * age_factor * type_factor * floor_factor * side_adjustments
    
    # Total estimate
    estimated_total = round(unit_price * main_area)
    estimated_unit = round(unit_price)
    
    # Compare with comps if available
    comps = data.get('comps', [])
    comp_analysis = []
    for c in comps:
        c_unit = c['price'] / c['area'] if c['area'] > 0 else 0
        comp_analysis.append({
            'address': c.get('address', ''),
            'unit_price': round(c_unit),
            'total_price': c.get('price', 0),
        })
    
    return {
        'estimated_total': estimated_total,
        'estimated_unit': estimated_unit,
        'main_area': main_area,
        'base_price': round(base_price),
        'factors': {
            'age_factor': round(age_factor, 2),
            'type_factor': round(type_factor, 2),
            'floor_factor': round(floor_factor, 2),
            'side_adjustments': round(side_adjustments, 2),
        },
        'comp_analysis': comp_analysis,
        'unit_comparison': f"{'高於行情' if estimated_unit > (comp_analysis[0]['unit_price'] if comp_analysis else estimated_unit) else '低於行情'}" if comp_analysis else "無比較對象"
    }

def generate_report(data, output_path):
    result = calc_valuation(data)
    prop = data.get('property', {})

    # Comp table
    comp_lines = []
    for c in result.get('comp_analysis', []):
        comp_lines.append(f"- {c['address']} → {c['total_price']:,} 元（{c['unit_price']:,} 元/坪）")
    comp_text = '\n'.join(comp_lines) if comp_lines else '無參考對象'

    report = f"""# 📊 不動產估值分析報告

## 物件基本資料

| 項目 | 內容 |
|------|------|
| 地址 | {prop.get('address', '—')} |
| 總坪數 | {prop.get('total_area', '—')} 坪 |
| 屋齡 | {prop.get('building_age', '—')} 年 |
| 樓層 | {prop.get('floor', '—')}F / {prop.get('total_floors', '—')}F |
| 類型 | {prop.get('type', '—')} |

## 估值結果

| 項目 | 金額 |
|------|------|
| **總價估值** | **{result['estimated_total']:,} 元** |
| **單價估值** | **{result['estimated_unit']:,} 元／坪** |
| 主建物坪數（不含車位） | {result['main_area']:.1f} 坪 |

## 調整因子

| 因子 | 數值 | 說明 |
|------|:----:|------|
| 屋齡調整 | ×{result['factors']['age_factor']} | {prop.get('building_age', 0)}年 |
| 類型調整 | ×{result['factors']['type_factor']} | {prop.get('type', '大樓')} |
| 樓層調整 | ×{result['factors']['floor_factor']} | {prop.get('floor', 0)}F/{prop.get('total_floors', 1)}F |
| 其他調整 | ×{result['factors']['side_adjustments']} | 含景觀/座向/狀態/風險 |
| **綜合調整** | **×{round(result['estimated_unit'] / result['base_price'], 2) if result.get('base_price') else 1}** | 對區域基準之比例 |

## 實價登錄比較

{comp_text}

**比較結論：** {result.get('unit_comparison', '—')}

## 估值區間建議

- 保守估值（-5%）：{round(result['estimated_total'] * 0.95):,} 元
- 合理估值：{result['estimated_total']:,} 元
- 樂觀估值（+5%）：{round(result['estimated_total'] * 1.05):,} 元

## 注意事項

1. 本估值為市場比較法概估，實際成交價視情況而異
2. 建議參考 3 筆以上同社區/同區域近期實價登錄
3. 特殊因素（凶宅、海砂屋等）需另行評估
4. 如需精確估價，建議委託不動產估價師

---
*估值日期：{datetime.now().strftime('%Y-%m-%d')}
*報告由 Property Valuation Skill 自動產生*
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f'✅ 估值報告已產出：{output_path}')
    print(f'   總價估值：{result["estimated_total"]:,} 元 | 單價：{result["estimated_unit"]:,} 元/坪')

def main():
    if len(sys.argv) < 3:
        print('Usage: python calc-valuation.py <input-json> <output-path>')
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
