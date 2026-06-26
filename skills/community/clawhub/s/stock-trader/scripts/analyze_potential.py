#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股潜力股分析
用法: python analyze_potential.py
分析标准：近期涨幅、成交量、市盈率、行业热度
"""

import subprocess
import re
import json

# 潜力股候选池（可以根据策略调整）
CANDIDATE_STOCKS = [
    "sz300750",  # 宁德时代
    "sz002475",  # 立讯精密
    "sz000858",  # 五粮液
    "sh600519",  # 贵州茅台
    "sh603288",  # 海天味业
    "sz000725",  # 京东方A
    "sz002594",  # 比亚迪
    "sh688981",  # 中芯国际
    "sz300059",  # 东方财富
    "sh600036",  # 招商银行
    "sz300274",  # 阳光电源
    "sh601012",  # 隆基绿能
    "sz300124",  # 汇川技术
    "sh600276",  # 恒瑞医药
    "sz300122",  # 智飞生物
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
            "yesterday_close": float(fields[4]),
            "today_open": float(fields[5]),
            "volume": int(fields[6]) if fields[6] else 0,
            "change_percent": float(fields[32]) if fields[32] else 0,
            "high": float(fields[33]) if fields[33] else 0,
            "low": float(fields[34]) if fields[34] else 0,
            "pe": float(fields[52]) if len(fields) > 52 and fields[52] else 0,  # 市盈率
            "market_cap": float(fields[44]) if len(fields) > 44 and fields[44] else 0,  # 总市值
        }
        
    except Exception as e:
        return None

def calculate_potential_score(stock):
    """计算潜力分（0-100）"""
    score = 50  # 基础分
    
    # 涨幅因素 (0-20分)
    change = stock.get("change_percent", 0)
    if 2 <= change <= 5:
        score += 15  # 适度上涨
    elif 5 < change <= 8:
        score += 20  # 强势上涨
    elif -5 <= change < -2:
        score -= 10  # 回调可能有机会
    
    # 成交量因素 (0-15分)
    volume = stock.get("volume", 0)
    if volume > 1000000:  # 100万手以上
        score += 15
    elif volume > 500000:
        score += 10
    
    # 市盈率因素 (0-15分)
    pe = stock.get("pe", 0)
    if 10 <= pe <= 30:
        score += 15  # 合理估值
    elif 30 < pe <= 50:
        score += 10
    elif pe > 100 or pe <= 0:
        score -= 10  # 估值过高或亏损
    
    # 市值因素 (0-10分)
    market_cap = stock.get("market_cap", 0)
    if 100 <= market_cap <= 5000:  # 100亿-5000亿
        score += 10
    elif market_cap > 5000:
        score += 5
    
    return min(100, max(0, score))

def get_industry_tag(name):
    """根据名称返回行业标签"""
    if any(k in name for k in ["酒", "食品", "饮料", "医药", "医疗"]):
        return "消费/医药"
    elif any(k in name for k in ["科技", "精密", "技术", "电子", "芯"]):
        return "科技制造"
    elif any(k in name for k in ["银行", "证券", "保险", "财富", "金融"]):
        return "金融"
    elif any(k in name for k in ["能源", "光伏", "电", "电池", "锂"]):
        return "新能源"
    elif any(k in name for k in ["车", "汽", "比亚"]):
        return "汽车"
    return "综合"

def main():
    print("\n" + "="*70)
    print("🔥 A股潜力股分析报告")
    print("="*70)
    print("\n正在分析候选股票...\n")
    
    results = []
    
    for code in CANDIDATE_STOCKS:
        data = get_stock_data(code)
        if data:
            score = calculate_potential_score(data)
            industry = get_industry_tag(data["name"])
            results.append({
                **data,
                "score": score,
                "industry": industry
            })
    
    # 按潜力分排序
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # 输出TOP10
    print(f"{'排名':<4}{'股票名称':<10}{'代码':<10}{'现价':>8}{'涨跌':>10}{'行业':<12}{'潜力分':>8}")
    print("-"*70)
    
    for i, stock in enumerate(results[:10], 1):
        change_str = f"{stock['change_percent']:+.2f}%"
        change_emoji = "📈" if stock['change_percent'] >= 0 else "📉"
        
        print(f"{i:<4}{stock['name']:<10}{stock['code']:<10}{stock['price']:>8.2f}{change_emoji}{change_str:>8}{stock['industry']:<10}{stock['score']:>8.0f}")
    
    print("\n" + "="*70)
    print("📊 分析维度:")
    print("  • 近期涨幅 (适度上涨为佳)")
    print("  • 成交量 (活跃度)")
    print("  • 市盈率 (合理估值)")
    print("  • 市值规模 (流动性)")
    print("\n⚠️ 风险提示: 以上分析仅供参考，不构成投资建议")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
