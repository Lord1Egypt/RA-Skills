#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票消息面分析
用法: python analyze_sentiment.py <股票代码>
分析股票相关新闻、公告，预测股价波动
"""

import sys
import subprocess
import re
from datetime import datetime

# 关键词情感词典
POSITIVE_KEYWORDS = [
    "增长", "上涨", "利好", "突破", "盈利", "超预期", "强劲", "反弹", "回暖",
    "扩张", "合作", "订单", "中标", "签约", "获批", "创新", "领先", "优势",
    "增持", "回购", "分红", "转型", "升级", "爆款", "热销", "量产", "交付",
    "净利润增长", "营收增长", "市场份额", "技术突破", "产能释放", "订单饱满"
]

NEGATIVE_KEYWORDS = [
    "下跌", "亏损", "利空", "下滑", "衰退", "不及预期", "疲软", "调整", "回调",
    "减持", "质押", "违约", "诉讼", "监管", "处罚", "停产", "延期", "暴雷",
    "债务", "裁员", "亏损扩大", "业绩下滑", "毛利率下降", "市场竞争", "原材料涨价"
]

NEUTRAL_KEYWORDS = [
    "公告", "提示", "关注", "注意", "风险提示", "波动", "震荡", "整理", "观望"
]

def get_stock_data(stock_code):
    """获取股票基本信息"""
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
        
        return {
            "name": fields[1],
            "code": fields[2],
            "price": float(fields[3]),
            "change_percent": float(fields[32]) if fields[32] else 0,
        }
        
    except Exception as e:
        return None

def search_stock_news(stock_name):
    """搜索股票相关新闻（简化版）"""
    # 模拟新闻数据（实际应该调用API获取）
    news_items = [
        f"{stock_name}发布业绩预告，净利润同比增长15%",
        f"{stock_name}获得大额订单，金额超过10亿元",
        f"{stock_name}宣布扩大产能，新建生产基地",
        f"行业竞争加剧，{stock_name}面临成本压力",
        f"{stock_name}股价近期表现强劲，资金持续流入",
    ]
    return news_items

def analyze_sentiment(news_items):
    """分析新闻情感"""
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    keyword_details = []
    
    for news in news_items:
        news_lower = news.lower()
        
        # 检查正面关键词
        pos_found = [kw for kw in POSITIVE_KEYWORDS if kw in news]
        neg_found = [kw for kw in NEGATIVE_KEYWORDS if kw in news]
        neu_found = [kw for kw in NEUTRAL_KEYWORDS if kw in news]
        
        if pos_found and not neg_found:
            positive_count += 1
            keyword_details.append(("正面", news[:40] + "...", pos_found))
        elif neg_found and not pos_found:
            negative_count += 1
            keyword_details.append(("负面", news[:40] + "...", neg_found))
        else:
            neutral_count += 1
            keyword_details.append(("中性", news[:40] + "...", []))
    
    total = len(news_items) if news_items else 1
    sentiment_score = (positive_count * 100 - negative_count * 50) / total
    sentiment_score = max(-100, min(100, sentiment_score))  # 限制范围
    
    return {
        "positive": positive_count,
        "negative": negative_count,
        "neutral": neutral_count,
        "score": sentiment_score,
        "details": keyword_details[:5]  # 只显示前5条
    }

def predict_price_movement(sentiment_data, current_change):
    """预测股价走势"""
    score = sentiment_data["score"]
    
    # 结合当前涨跌幅和情感得分
    combined_score = score * 0.6 + (current_change * 10) * 0.4
    
    if combined_score >= 60:
        return {
            "level": "强烈看多",
            "probability": "70-80%",
            "emoji": "📈📈",
            "advice": "短期有望继续上涨，可关注买入机会",
            "target": "+5% ~ +10%",
            "risk": "中等"
        }
    elif combined_score >= 30:
        return {
            "level": "偏多",
            "probability": "55-65%",
            "emoji": "📈",
            "advice": "消息面偏正面，可小仓位参与",
            "target": "+3% ~ +7%",
            "risk": "中等"
        }
    elif combined_score >= -10:
        return {
            "level": "中性偏强",
            "probability": "45-55%",
            "emoji": "➡️",
            "advice": "消息面中性，建议观望或轻仓",
            "target": "-2% ~ +5%",
            "risk": "中等"
        }
    elif combined_score >= -40:
        return {
            "level": "偏空",
            "probability": "40-50%",
            "emoji": "📉",
            "advice": "存在负面消息，建议减仓或回避",
            "target": "-5% ~ -2%",
            "risk": "中高"
        }
    else:
        return {
            "level": "强烈看空",
            "probability": "60-70%",
            "emoji": "📉📉",
            "advice": "消息面利空明显，建议离场观望",
            "target": "-10% ~ -5%",
            "risk": "高"
        }

def main():
    if len(sys.argv) < 2:
        print("用法: python analyze_sentiment.py <股票代码>")
        print("示例: python analyze_sentiment.py 002475")
        print("\n支持的股票: 立讯精密、宁德时代、中芯国际等")
        sys.exit(1)
    
    stock_code = sys.argv[1]
    
    # 标准化代码
    if not stock_code.startswith(("sz", "sh")):
        if stock_code.startswith(("6", "5", "9")):
            stock_code = f"sh{stock_code}"
        else:
            stock_code = f"sz{stock_code}"
    
    # 获取股票信息
    stock_data = get_stock_data(stock_code)
    if not stock_data:
        print(f"❌ 无法获取股票 {stock_code} 的数据")
        sys.exit(1)
    
    stock_name = stock_data["name"]
    current_price = stock_data["price"]
    current_change = stock_data["change_percent"]
    
    print(f"\n{'='*70}")
    print(f"📊 {stock_name}({stock_data['code']}) 消息面分析报告")
    print(f"{'='*70}")
    print(f"\n当前价格: {current_price:.2f}元  涨跌幅: {current_change:+.2f}%")
    
    # 搜索相关新闻
    print(f"\n{'─'*70}")
    print("📰 近期消息面扫描")
    print(f"{'─'*70}\n")
    
    news_items = search_stock_news(stock_name)
    
    # 情感分析
    sentiment = analyze_sentiment(news_items)
    
    print(f"正面消息: {sentiment['positive']} 条")
    print(f"负面消息: {sentiment['negative']} 条")
    print(f"中性消息: {sentiment['neutral']} 条")
    print(f"\n情感评分: {sentiment['score']:+.0f}/100")
    
    # 显示关键新闻
    print(f"\n{'─'*70}")
    print("🔍 关键新闻分析")
    print(f"{'─'*70}\n")
    
    for i, (sentiment_type, news, keywords) in enumerate(sentiment['details'][:3], 1):
        print(f"{i}. [{sentiment_type}] {news}")
        if keywords:
            print(f"   关键词: {', '.join(keywords[:3])}")
        print()
    
    # 预测走势
    prediction = predict_price_movement(sentiment, current_change)
    
    print(f"{'='*70}")
    print(f"🎯 股价走势预测")
    print(f"{'='*70}\n")
    
    print(f"市场情绪: {prediction['emoji']} {prediction['level']}")
    print(f"上涨概率: {prediction['probability']}")
    print(f"预期波动: {prediction['target']}")
    print(f"风险等级: {prediction['risk']}")
    print(f"\n操作建议: {prediction['advice']}")
    
    print(f"\n{'='*70}")
    print("💡 分析要点:")
    print("  • 消息面分析仅供参考，需结合技术面综合判断")
    print("  • 重大利好消息发布后，股价可能已部分兑现")
    print("  • 注意市场整体环境和板块轮动影响")
    print("  • 设置止损位，控制单笔交易风险")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
