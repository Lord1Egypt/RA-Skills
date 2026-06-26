#!/usr/bin/env python3
"""
研报生成器
生成股票分析报告（盘前/盘后/个股深度报告）
"""

import argparse
import json
import sys
import os
from datetime import datetime

_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
_trading_src = os.path.join(_base, 'toc-trading', 'src')
if _trading_src not in sys.path:
    sys.path.insert(0, _trading_src)

from stock_data_adapter import StockDataAdapter


def generate_daily_report(date: str = None) -> dict:
    """生成每日市场报告"""
    adapter = StockDataAdapter()
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    # 获取指数
    indices = adapter.get_index_quote()
    
    # 获取板块
    sectors = adapter.get_sector_data()
    
    # 获取市场广度
    breadth = adapter.get_market_breadth()
    
    # 获取北向资金
    north = adapter.get_north_bound()
    
    # 构建报告
    report = []
    report.append(f"# 📊 每日市场报告 | {date}")
    report.append("")
    
    # 指数表现
    report.append("## 主要指数")
    report.append("| 指数 | 最新价 | 涨跌幅 |")
    report.append("|------|--------|-------|")
    for idx in indices[:5]:
        change = idx.get('change', 0)
        emoji = "🟢" if change >= 0 else "🔴"
        report.append(f"| {emoji} {idx.get('name', '')} | {idx.get('price', 0):.2f} | {change:+.2f}% |")
    
    report.append("")
    
    # 市场广度
    if breadth:
        report.append("## 市场广度")
        report.append(f"- 上涨家数: **{breadth.get('up_count', 0)}**")
        report.append(f"- 下跌家数: **{breadth.get('down_count', 0)}**")
        report.append(f"- 上涨比例: **{breadth.get('up_ratio', 0)}%**")
        report.append(f"- 涨停家数: **{breadth.get('limit_up', 0)}**")
        report.append(f"- 跌停家数: **{breadth.get('limit_down', 0)}**")
        report.append("")
    
    # 北向资金
    if north:
        flow = north.get('north_flow', 0)
        emoji = "🟢" if flow >= 0 else "🔴"
        report.append("## 北向资金")
        report.append(f"{emoji} 今日净流入: **{flow:+.2f}亿** ({north.get('trend', '')})")
        report.append("")
    
    # 板块表现
    if sectors:
        report.append("## 板块涨跌排行")
        report.append("")
        report.append("**涨幅前五：**")
        for s in sectors[:5]:
            change = s.get('change', 0)
            emoji = "🟢" if change >= 0 else "🔴"
            report.append(f"{emoji} {s.get('name', '')} {change:+.2f}%")
        report.append("")
        report.append("**跌幅前五：**")
        for s in sectors[-5:]:
            change = s.get('change', 0)
            emoji = "🔴" if change >= 0 else "🟢"
            report.append(f"{emoji} {s.get('name', '')} {change:+.2f}%")
        report.append("")
    
    # 风险提示
    report.append("---")
    report.append("⚠️ **免责声明**：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。")
    report.append("")
    report.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    return {
        'success': True,
        'date': date,
        'report': '\n'.join(report),
        'summary': {
            'indices_count': len(indices),
            'sectors_count': len(sectors),
            'market_breadth': breadth,
            'north_bound': north,
        }
    }


def generate_stock_report(symbol: str, name: str = None, 
                          technical_result: dict = None,
                          fundamental_result: dict = None) -> dict:
    """生成个股分析报告"""
    adapter = StockDataAdapter()
    
    # 获取实时行情
    quote = adapter.get_realtime_quote(symbol)
    
    if not name:
        name = quote.get('name', symbol)
    
    report = []
    report.append(f"# 📈 {name} ({symbol}) 个股分析报告")
    report.append("")
    report.append(f"**日期**: {datetime.now().strftime('%Y-%m-%d')}")
    report.append("")
    
    # 基本信息
    report.append("## 基本信息")
    price = quote.get('price', 0)
    change = quote.get('change', 0)
    emoji = "🟢" if change >= 0 else "🔴"
    report.append(f"- **当前价**: {emoji} {price} ({change:+.2f}%)")
    report.append(f"- **PE(动)**: {quote.get('pe', 'N/A')}")
    report.append(f"- **PB**: {quote.get('pb', 'N/A')}")
    mkt_cap = quote.get('mkt_cap', 0)
    if mkt_cap:
        report.append(f"- **总市值**: {mkt_cap/1e8:.2f}亿" if mkt_cap > 1e8 else f"- **总市值**: {mkt_cap/1e4:.2f}万")
    report.append("")
    
    # 技术面（如果提供）
    if technical_result:
        report.append("## 技术面分析")
        score = technical_result.get('composite', {}).get('score', 'N/A')
        conclusion = technical_result.get('composite', {}).get('conclusion', '')
        report.append(f"- **综合评分**: {score}/100 ({conclusion})")
        
        signals = technical_result.get('composite', {}).get('signals', [])
        if signals:
            report.append("- **关键信号**:")
            for sig in signals[:5]:
                report.append(f"  - {sig}")
        report.append("")
    
    # 基本面（如果提供）
    if fundamental_result:
        report.append("## 基本面分析")
        pe = fundamental_result.get('pe', 'N/A')
        pb = fundamental_result.get('pb', 'N/A')
        report.append(f"- **PE**: {pe}")
        report.append(f"- **PB**: {pb}")
        report.append("")
    
    # 操作建议
    report.append("## 操作建议")
    report.append("*（待综合技术面和基本面后生成）*")
    report.append("")
    
    # 风险提示
    report.append("---")
    report.append("⚠️ **免责声明**：本报告仅供参考，不构成投资建议。股市有风险，投资需谨慎。")
    report.append("")
    report.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    return {
        'success': True,
        'symbol': symbol,
        'name': name,
        'report': '\n'.join(report)
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='研报生成器')
    parser.add_argument('--type', required=True, 
                       choices=['daily', 'stock'],
                       help='报告类型: daily=每日市场, stock=个股分析')
    parser.add_argument('--symbol', default='', help='股票代码（stock类型需要）')
    parser.add_argument('--name', default='', help='股票名称')
    parser.add_argument('--date', default='', help='日期（daily类型使用）')
    parser.add_argument('--output', default='/tmp/report.md', help='输出文件')
    
    args = parser.parse_args()
    
    if args.type == 'daily':
        result = generate_daily_report(args.date)
    else:
        result = generate_stock_report(args.symbol, args.name)
    
    if result.get('success'):
        report_text = result.get('report', '')
        with open(args.output, 'w') as f:
            f.write(report_text)
        print(f"✅ 报告生成成功: {args.output}")
        print(f"--- 预览 ---")
        print(report_text[:500] + "..." if len(report_text) > 500 else report_text)
    else:
        print(f"❌ 生成失败: {result.get('error')}")
