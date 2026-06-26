#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业龙头股分析
用法: python analyze_leaders.py [行业名称]
根据行业资金流入情况，分析该行业龙头股
"""

import sys
import subprocess
import re
from datetime import datetime

# 行业龙头股数据库
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
            "yesterday_close": float(fields[4]),
            "volume": int(fields[6]) if fields[6] else 0,
            "change_percent": float(fields[32]) if fields[32] else 0,
            "high": float(fields[33]) if fields[33] else 0,
            "low": float(fields[34]) if fields[34] else 0,
            "market_cap": float(fields[44]) if len(fields) > 44 and fields[44] else 0,
        }
        
    except Exception as e:
        return None

def calculate_leader_score(stock):
    """计算龙头股评分"""
    score = 50  # 基础分
    
    # 涨幅因素
    change = stock.get("change_percent", 0)
    if change > 0:
        score += min(20, change * 3)  # 涨幅加分
    else:
        score += change * 2  # 跌幅减分
    
    # 成交量因素
    volume = stock.get("volume", 0)
    if volume > 1000000:
        score += 15
    elif volume > 500000:
        score += 10
    
    # 市值因素
    market_cap = stock.get("market_cap", 0)
    if market_cap > 5000:  # 5000亿以上
        score += 15
    elif market_cap > 1000:  # 1000亿以上
        score += 10
    
    return min(100, max(0, score))

def analyze_industry_leaders(industry_name):
    """分析指定行业的龙头股"""
    print(f"\n{'='*70}")
    print(f"🏆 {industry_name}行业龙头股分析 ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print(f"{'='*70}")
    
    # 获取行业股票代码
    stock_codes = INDUSTRY_LEADERS.get(industry_name, [])
    
    if not stock_codes:
        # 模糊匹配
        for key in INDUSTRY_LEADERS:
            if industry_name in key or key in industry_name:
                stock_codes = INDUSTRY_LEADERS[key]
                print(f"已匹配到行业: {key}")
                break
    
    if not stock_codes:
        print(f"\n❌ 未找到行业 '{industry_name}' 的数据")
        print(f"\n支持的行业:")
        for i, name in enumerate(INDUSTRY_LEADERS.keys(), 1):
            print(f"  {i}. {name}")
        return
    
    print(f"\n正在分析 {len(stock_codes)} 只龙头股候选...\n")
    
    results = []
    for code in stock_codes:
        data = get_stock_data(code)
        if data:
            score = calculate_leader_score(data)
            results.append({**data, "score": score})
    
    # 按评分排序
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # 输出结果
    print(f"{'排名':<4}{'股票名称':<10}{'代码':<10}{'现价':>10}{'涨跌':>10}{'市值(亿)':>12}{'龙头分':>8}")
    print("-"*70)
    
    for i, stock in enumerate(results[:10], 1):
        change_str = f"{stock['change_percent']:+.2f}%"
        change_emoji = "📈" if stock['change_percent'] >= 0 else "📉"
        market_cap_str = f"{stock['market_cap']:.0f}" if stock['market_cap'] else "--"
        
        print(f"{i:<4}{stock['name']:<10}{stock['code']:<10}{stock['price']:>10.2f}{change_emoji}{change_str:>8}{market_cap_str:>12}{stock['score']:>8.0f}")
    
    print("\n" + "="*70)
    print("📊 龙头股特征:")
    print("  • 市值大、成交活跃")
    print("  • 行业内影响力强")
    print("  • 资金关注度高")
    print("  • 走势相对稳健")
    print("\n💡 投资建议:")
    print("  • 龙头股适合中长期配置")
    print("  • 分批建仓，逢低加仓")
    print("  • 设置止损位保护本金")
    print("="*70 + "\n")

def list_all_industries():
    """列出所有行业"""
    print(f"\n{'='*70}")
    print(f"📊 支持分析的行业列表")
    print(f"{'='*70}\n")
    
    for i, (industry, stocks) in enumerate(INDUSTRY_LEADERS.items(), 1):
        print(f"{i:2}. {industry} ({len(stocks)}只龙头股)")
    
    print(f"\n{'='*70}")
    print("用法: python analyze_leaders.py <行业名称>")
    print("示例: python analyze_leaders.py 半导体")
    print("="*70 + "\n")

def main():
    if len(sys.argv) < 2:
        list_all_industries()
        return
    
    industry_name = sys.argv[1]
    analyze_industry_leaders(industry_name)

if __name__ == "__main__":
    main()
