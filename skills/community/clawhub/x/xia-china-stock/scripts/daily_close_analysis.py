#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股收盘分析 + 技术指标
用于每日15:05 cron任务
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# 导入技术指标分析器
sys.path.insert(0, str(Path(__file__).parent))
from technical_indicators import TechnicalAnalyzer

# 监控标的
WATCH_LIST = [
    ('002475.SZ', '立讯精密'),
    ('002594.SZ', '比亚迪'),
    ('688180.SH', '君实生物'),
    ('603893.SH', '瑞芯微'),
    ('600938.SH', '中国海油'),
    ('688981.SH', '中芯国际'),
    ('600276.SH', '恒瑞医药'),
]


def analyze_stock(symbol: str, name: str) -> dict:
    """分析单只股票"""
    analyzer = TechnicalAnalyzer(symbol, period="3mo")
    result = analyzer.run_analysis()
    
    if not result:
        return {
            'symbol': symbol,
            'name': name,
            'error': '获取数据失败'
        }
    
    return {
        'symbol': symbol,
        'name': name,
        'price': result['price'],
        'source': result['source'],
        'trend': result['trend'],
        'indicators': {
            'MA': result['indicators']['MA']['status'],
            'MACD': result['indicators']['MACD'],
            'RSI': result['indicators']['RSI'],
            'KDJ': result['indicators']['KDJ'],
            'BOLL': result['indicators']['BOLL'],
        },
        'signals': result['signals']
    }


def generate_report(results: list, format: str = 'markdown') -> str:
    """生成收盘分析报告"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    if format == 'json':
        return json.dumps({
            'date': date_str,
            'type': '收盘分析',
            'stocks': results
        }, ensure_ascii=False, indent=2)
    
    # Markdown报告
    md = f"""# 📈 A股收盘技术分析

**日期**: {date_str}  
**分析内容**: 技术指标综合评估

---

## 📊 监控标的概览

| 股票 | 代码 | 现价 | 趋势 | 信号 |
|------|------|------|------|------|
"""
    
    for r in results:
        if 'error' in r:
            md += f"| {r['name']} | {r['symbol']} | - | ❌ | {r['error']} |\n"
        else:
            trend = r['trend']
            signals = r['signals']
            bullish = sum(1 for s in signals if '买入' in s[1] or '看涨' in s[1])
            bearish = sum(1 for s in signals if '卖出' in s[1] or '看跌' in s[1])
            signal_str = f"🟢{bullish}/🔴{bearish}"
            md += f"| {r['name']} | {r['symbol']} | {r['price']} | {trend['emoji']} {trend['trend']} | {signal_str} |\n"
    
    # 每只股票详细分析
    for r in results:
        if 'error' in r:
            continue
            
        md += f"""
---

## 📋 {r['name']} ({r['symbol']})

**当前价格**: {r['price']}  
**数据来源**: {r['source']}  
**综合趋势**: {r['trend']['emoji']} {r['trend']['trend']} (分数: {r['trend']['score']})

### 技术指标

| 指标 | 关键数据 |
|------|----------|
"""
        ind = r['indicators']
        
        # MA
        ma_status = []
        for ma, data in ind['MA'].items():
            ma_status.append(f"{ma}: {data['value']} ({data['position']})")
        md += f"| **均线** | {'; '.join(ma_status[:3])} |\n"
        
        # MACD
        macd = ind['MACD']
        macd_trend = '多头' if macd['MACD'] > 0 else '空头'
        md += f"| **MACD** | DIF: {macd['DIF']}, DEA: {macd['DEA']} ({macd_trend}) |\n"
        
        # RSI
        rsi = ind['RSI']
        rsi_status = '超买' if rsi['RSI14'] > 70 else '超卖' if rsi['RSI14'] < 30 else '正常'
        md += f"| **RSI** | RSI14: {rsi['RSI14']} ({rsi_status}) |\n"
        
        # KDJ
        kdj = ind['KDJ']
        kdj_status = '金叉' if kdj['K'] > kdj['D'] else '死叉'
        md += f"| **KDJ** | K: {kdj['K']}, D: {kdj['D']} ({kdj_status}) |\n"
        
        # BOLL
        boll = ind['BOLL']
        md += f"| **布林带** | 上: {boll['upper']}, 中: {boll['mid']}, 下: {boll['lower']} |\n"
        
        # 信号
        md += "\n### 🚨 信号汇总\n\n"
        for sig in r['signals']:
            md += f"- {sig[2]} **{sig[0]}**: {sig[1]}\n"
    
    md += """
---

## 💡 操作建议

"""
    
    # 根据分析结果给出建议
    for r in results:
        if 'error' in r:
            continue
        trend_score = r['trend']['score']
        name = r['name']
        
        if trend_score >= 30:
            md += f"- **{name}**: 技术面偏多，可关注回调买入机会\n"
        elif trend_score <= -30:
            md += f"- **{name}**: 技术面偏空，建议观望或减仓\n"
        else:
            md += f"- **{name}**: 震荡整理，建议等待方向明确\n"
    
    md += """
---

*⚠️ 以上分析基于技术指标，仅供参考，不构成投资建议*  
*🦞 由地铁龙虾自动生成*
"""
    
    return md


def main():
    parser = argparse.ArgumentParser(description='A股收盘技术分析')
    parser.add_argument('--stocks', nargs='+', help='自定义股票列表 (格式: 代码.名称)')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown')
    parser.add_argument('--output', help='输出文件路径')
    
    args = parser.parse_args()
    
    # 解析股票列表
    if args.stocks:
        stocks = []
        for s in args.stocks:
            if '.' in s:
                code, name = s.split('.', 1)
                stocks.append((code, name))
            else:
                stocks.append((s, s))
    else:
        stocks = WATCH_LIST
    
    print(f"正在分析 {len(stocks)} 只股票...")
    
    # 分析每只股票
    results = []
    for symbol, name in stocks:
        print(f"  分析 {name} ({symbol})...")
        result = analyze_stock(symbol, name)
        results.append(result)
    
    # 生成报告
    report = generate_report(results, args.format)
    
    if args.output:
        Path(args.output).write_text(report, encoding='utf-8')
        print(f"\n报告已保存到: {args.output}")
    else:
        print("\n" + "="*50)
        print(report)


if __name__ == '__main__':
    main()
