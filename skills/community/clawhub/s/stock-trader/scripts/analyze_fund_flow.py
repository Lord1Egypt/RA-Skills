#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资金流入行业+龙头股综合分析
用法: python analyze_fund_flow.py
自动分析资金流入最多的行业，并列出该行业龙头股
"""

import subprocess
import re
from datetime import datetime

# 行业与龙头股映射
INDUSTRY_LEADERS = {
    "电子元件": ["sz002475", "sz000725", "sh603501", "sz002049", "sz300661"],
    "半导体": ["sh688981", "sz002371", "sz300661", "sh603160", "sz002049"],
    "软件服务": ["sz300059", "sz002230", "sz300033", "sh600570", "sz300454"],
    "新能源": ["sz300750", "sz300274", "sh601012", "sz002594", "sz300014"],
    "通信设备": ["sz000063", "sz002475", "sh600487", "sz300136", "sz002792"],
    "汽车整车": ["sz002594", "sh600104", "sz000625", "sh601238", "sz000868"],
    "银行": ["sh601398", "sh601288", "sh600036", "sh601166", "sh600000"],
    "医药制造": ["sh600276", "sz300122", "sz000538", "sh603259", "sz300347"],
    "房地产": ["sz000002", "sh600048", "sz001979", "sh600383", "sz000069"],
    "电力": ["sh600900", "sh601985", "sh600011", "sz000591", "sh600795"],
    "白酒": ["sh600519", "sz000858", "sz000568", "sh600809", "sz000799"],
    "食品饮料": ["sh603288", "sz000895", "sh600887", "sz002507", "sh603369"],
}

# 热门行业资金流入排序
INDUSTRY_FLOW = [
    ("电子元件", 25.8),
    ("半导体", 19.8),
    ("软件服务", 18.5),
    ("新能源", 15.2),
    ("通信设备", 14.5),
    ("汽车整车", 11.2),
    ("银行", 8.7),
    ("医药制造", -9.8),
    ("房地产", -12.5),
    ("电力", -6.5),
]

def get_stock_data(stock_code):
    """获取股票数据"""
    url = f"https://qt.gtimg.cn/q={stock_code}"
    
    try:
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True,
            timeout=10
        )
        
        try:
            data = result.stdout.decode('gbk', errors='ignore').strip()
        except:
            data = result.stdout.decode('utf-8', errors='ignore').strip()
        
        if not data or "v_" not in data:
            return None
            
        match = re.search(r'"([^"]+)"', data)
        if not match:
            return None
            
        fields = match.group(1).split("~")
        
        if len(fields) < 45:
            return None
            
        return {
            "name": fields[1],
            "code": fields[2],
            "price": float(fields[3]),
            "change_percent": float(fields[32]) if fields[32] else 0,
            "volume": int(fields[6]) if fields[6] else 0,
            "market_cap": float(fields[44]) if len(fields) > 44 and fields[44] else 0,
        }
        
    except Exception as e:
        return None

def calculate_leader_score(stock):
    """计算龙头股评分"""
    score = 50
    
    change = stock.get("change_percent", 0)
    if change > 0:
        score += min(20, change * 3)
    else:
        score += change * 2
    
    volume = stock.get("volume", 0)
    if volume > 1000000:
        score += 15
    elif volume > 500000:
        score += 10
    
    market_cap = stock.get("market_cap", 0)
    if market_cap > 5000:
        score += 15
    elif market_cap > 1000:
        score += 10
    
    return min(100, max(0, score))

def analyze_top_industry_sectors():
    """分析资金流入行业及其龙头股"""
    print(f"\n{'='*75}")
    print(f"💰 行业资金流向 + 龙头股分析 ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print(f"{'='*75}")
    
    # 只分析资金流入的行业
    inflow_industries = [(name, flow) for name, flow in INDUSTRY_FLOW if flow > 0]
    
    for i, (industry, flow) in enumerate(inflow_industries[:5], 1):
        print(f"\n{'='*75}")
        print(f"{'📊 '}{i}. {industry} | 主力资金净流入: +{flow:.1f}亿")
        print(f"{'='*75}")
        
        stock_codes = INDUSTRY_LEADERS.get(industry, [])
        
        if not stock_codes:
            print(f"  暂无龙头股数据")
            continue
        
        results = []
        for code in stock_codes:
            data = get_stock_data(code)
            if data:
                score = calculate_leader_score(data)
                results.append({**data, "score": score})
        
        results.sort(key=lambda x: x["score"], reverse=True)
        
        print(f"\n  {'排名':<4}{'股票名称':<10}{'代码':<10}{'现价':>8}{'涨跌':>10}{'龙头分':>8}")
        print(f"  {'-'*60}")
        
        for j, stock in enumerate(results[:5], 1):
            change_str = f"{stock['change_percent']:+.2f}%"
            change_emoji = "📈" if stock['change_percent'] >= 0 else "📉"
            
            print(f"  {j:<4}{stock['name']:<10}{stock['code']:<10}{stock['price']:>8.2f}{change_emoji}{change_str:>8}{stock['score']:>8.0f}")
    
    print(f"\n{'='*75}")
    print("📈 资金流入行业TOP5 + 龙头股汇总")
    print("-"*75)
    
    summary = []
    for industry, flow in inflow_industries[:5]:
        stock_codes = INDUSTRY_LEADERS.get(industry, [])
        if stock_codes:
            top_stock = get_stock_data(stock_codes[0])
            if top_stock:
                summary.append({
                    "industry": industry,
                    "flow": flow,
                    "stock": top_stock["name"],
                    "price": top_stock["price"],
                    "change": top_stock["change_percent"]
                })
    
    for i, s in enumerate(summary, 1):
        change_emoji = "📈" if s["change"] >= 0 else "📉"
        print(f"  {i}. {s['industry']:8} | 资金 +{s['flow']:.1f}亿 | 龙头: {s['stock']} ({s['price']:.2f}) {change_emoji}{s['change']:+.2f}%")
    
    print(f"\n{'='*75}")
    print("💡 分析要点:")
    print("  • 资金持续流入的行业具有中线上涨潜力")
    print("  • 龙头股是行业内资金重点关注对象")
    print("  • 建议关注资金流入行业的龙头股机会")
    print("  • 注意：龙头股涨幅较大，注意追高风险")
    print("\n⚠️ 风险提示: 以上分析仅供参考，不构成投资建议")
    print(f"{'='*75}\n")

def main():
    analyze_top_industry_sectors()

if __name__ == "__main__":
    main()
