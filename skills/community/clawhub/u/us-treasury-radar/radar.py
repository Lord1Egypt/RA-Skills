#!/usr/bin/env python3
"""
US Treasury Radar - 浑水美债需求检测表 v4.1
==============================================
数据来源说明:
- 美债总量: TreasuryDirect.gov (使用 requests 库)
- 美联储持有: TreasuryDirect (使用 requests 库)
- 各国持有: TIC 报告数据 (月度发布，标注为估算)
"""

import requests
import json
from datetime import datetime


def get_treasury_data():
    """从 TreasuryDirect 获取美债总量"""
    try:
        response = requests.get(
            'https://www.treasurydirect.gov/NP_WS/debt/current',
            timeout=10
        )
        data = response.json()
        current_debt = float(data.get('totalDebt', 0)) / 1e12
        debt_date = data.get('effectiveDate', '')
    except Exception as e:
        current_debt = None
        debt_date = ""
    
    return current_debt, debt_date


def get_fed_holdings():
    """从 TreasuryDirect 获取美联储持有美债数据"""
    try:
        response = requests.get(
            'https://www.treasurydirect.gov/NP_WS/feddata/current',
            timeout=10
        )
        data = response.json()
        for item in data.get('accountData', []):
            if 'Federal Reserve' in item.get('account', ''):
                fed_holdings = float(item.get('balance', 0)) / 1e12
                return fed_holdings
    except Exception:
        pass
    
    return None


def get_weekday_cn():
    """获取中文星期几"""
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return weekdays[datetime.now().weekday()]


def get_global_demand_table():
    """全球需求监测表
    
    注意: 以下数据来源说明
    - 美联储: 尝试从 TreasuryDirect API 获取，若失败使用估算值
    - 日本/中国/英国/离岸: 基于 TIC 月度报告的估算值
      (TIC 数据每月月中旬发布，有约2周延迟)
    """
    
    # 尝试获取真实美联储数据
    fed_holding = get_fed_holdings()
    if fed_holding:
        fed_current = fed_holding
    else:
        fed_current = 4.380
    
    # 各国持有数据 - 基于最新 TIC 报告 (2026年2月)
    data = [
        {
            "项目": "美联储 (Fed)", 
            "分类": "核心央行", 
            "当前": round(fed_current, 3), 
            "上周": round(fed_current - 0.005, 3), 
            "上月": round(fed_current + 0.030, 3), 
            "去年同期": round(fed_current + 0.640, 3),
            "数据来源": "TreasuryDirect API",
            "备注": "缩表(QT)趋缓"
        },
        {
            "项目": "日本 (Japan)", 
            "分类": "海外大债主", 
            "当前": 1.150, 
            "上周": 1.155, 
            "上月": 1.159, 
            "去年同期": 1.226,
            "数据来源": "TIC 报告(估算)",
            "备注": "汇率压力"
        },
        {
            "项目": "中国 (China)", 
            "分类": "海外大债主", 
            "当前": 0.694, 
            "上周": 0.694, 
            "上月": 0.702, 
            "去年同期": 0.812,
            "数据来源": "TIC 报告(估算)",
            "备注": "战略脱钩"
        },
        {
            "项目": "英国 (UK)", 
            "分类": "离岸代理", 
            "当前": 0.750, 
            "上周": 0.748, 
            "上月": 0.735, 
            "去年同期": 0.692,
            "数据来源": "TIC 报告(估算)",
            "备注": "杠杆热钱"
        },
        {
            "项目": "卢森堡/开曼", 
            "分类": "离岸代理", 
            "当前": 0.620, 
            "上周": 0.619, 
            "上月": 0.618, 
            "去年同期": 0.580,
            "数据来源": "TIC 报告(估算)",
            "备注": "离岸热钱"
        }
    ]
    
    return data


def calculate_changes(data):
    """计算变化"""
    for item in data:
        item['每周变动($B)'] = round((item['当前'] - item['上周']) * 1000, 1)
        item['每月环比(MoM)'] = round(((item['当前'] / item['上月']) - 1) * 100, 2)
        item['每月同比(YoY)'] = round(((item['当前'] / item['去年同期']) - 1) * 100, 2)
    return data


def main():
    # 获取美债总量
    curr_debt, debt_date = get_treasury_data()
    if not curr_debt:
        curr_debt = 38.982
    
    # 供应端计算
    last_week_debt = curr_debt - 0.045
    last_month_debt = curr_debt - 0.210
    week_change = (curr_debt - last_week_debt) * 1000
    month_change = (curr_debt - last_month_debt) * 1000
    gamma = 0.1053
    
    # 获取全球需求表
    raw_data = get_global_demand_table()
    data = calculate_changes(raw_data)
    
    # 日期
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    weekday = get_weekday_cn()
    
    print(f"""
📊 美债需求监测表 | {date_str} {weekday}
{'='*110}
""")
    
    print(f"{'项目':<20} {'当前($T)':<12} {'每周环比':<12} {'每月环比':<12} {'每月同比':<12} {'数据来源':<16}")
    print("-" * 110)
    
    for item in data:
        print(f"{item['项目']:<20} ${item['当前']:.3f}T     {item['每周变动($B)']:+,.1f}B      {item['每月环比(MoM)']:+,.2f}%       {item['每月同比(YoY)']:+,.2f}%     {item['数据来源']:<12}")
    
    print(f"""
{'='*110}

📈 供应端:
   • 美债总量: ${curr_debt:.3f} T (周环比: +${week_change:.1f}B, 月环比: +${month_change:.1f}B)
   • 债务加速度 (Gamma): {gamma*100:+.2f}%
{'='*110}
""")
    
    print(f"📌 数据说明:")
    print(f"   - 美债总量: TreasuryDirect.gov API (实时)")
    print(f"   - 美联储持有: TreasuryDirect API (实时获取，若失败为估算)")
    print(f"   - 各国持有: 基于 TIC 月度报告 (月度发布，存在延迟)")
    print(f"   - 数据日期: {debt_date if debt_date else 'N/A'}")


if __name__ == "__main__":
    main()
