#!/usr/bin/env python3
"""
图表生成器
生成K线图、技术指标图等可视化图表
"""

import argparse
import json
import sys
import os
import tempfile

_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
_trading_src = os.path.join(_base, 'toc-trading', 'src')
if _trading_src not in sys.path:
    sys.path.insert(0, _trading_src)

# 尝试导入图表库
HAS_MPF = False
try:
    import mplfinance as mpf
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    HAS_MPF = True
except ImportError:
    pass


def generate_chart(kline_data: dict, chart_type: str = 'kline', 
                   indicators: list = None, output: str = None,
                   theme: str = 'dark') -> dict:
    """生成股票图表"""
    
    if not HAS_MPF:
        return {
            'success': False,
            'error': 'mplfinance未安装，使用文字描述替代',
            'output': None
        }
    
    if not kline_data.get('data'):
        return {
            'success': False,
            'error': '无K线数据',
            'output': None
        }
    
    if output is None:
        output = tempfile.mktemp(suffix='.png')
    
    df = pd.DataFrame(kline_data['data'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    
    # 主题配置
    if theme == 'dark':
        style = 'charcoal'
        colors = ['#89b4fa', '#f38ba8', '#a6e3a1', '#f9e2af']
    else:
        style = 'default'
        colors = ['#007bff', '#dc3545', '#28a745', '#fd7e14']
    
    # K线类型
    chart_types = {
        'kline': 'candle',
        'line': 'line',
        'renko': 'renko',
        'pnf': 'pnf'
    }
    
    mpf_type = chart_types.get(chart_type, 'candle')
    
    # 添加均线
    add_plots = []
    if indicators and 'MA' in indicators:
        for period, color in [(5, colors[0]), (10, colors[1]), (20, colors[2])]:
            ma = df['close'].rolling(period).mean()
            add_plots.append(mpf.make_addplot(ma, color=color, width=0.8))
    
    try:
        mpf.plot(
            df,
            type=mpf_type,
            style=style,
            volume=True,
            addplot=add_plots if add_plots else None,
            figsize=(14, 8),
            title=f"\n{kline_data.get('symbol', '')} {chart_type.upper()}",
            savefig=output
        )
        
        return {
            'success': True,
            'output': output,
            'type': chart_type
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'output': None
        }


def generate_text_chart(kline_data: dict) -> str:
    """生成文字版K线图（当mplfinance不可用时）"""
    if not kline_data.get('data'):
        return "无数据"
    
    data = kline_data['data'][-20:]  # 最近20根K线
    symbol = kline_data.get('symbol', '')
    
    lines = [f"📈 {symbol} 近20日K线", ""]
    
    for bar in data:
        date = bar.get('date', '')[:10] if bar.get('date') else ''
        open_p = bar.get('open', 0)
        close_p = bar.get('close', 0)
        high = bar.get('high', 0)
        low = bar.get('low', 0)
        pct = bar.get('pct_change', 0)
        
        # 涨跌符号
        if pct > 0:
            bar_char = '▲'
            color = '🔴'
        elif pct < 0:
            bar_char = '▼'
            color = '🟢'
        else:
            bar_char = '●'
            color = '⚪'
        
        lines.append(f"{color} {date} {bar_char} 开{open_p:.2f} 高{high:.2f} 低{low:.2f} 收{close_p:.2f} ({pct:+.2f}%)")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='图表生成器')
    parser.add_argument('--input', required=True, help='K线数据JSON文件')
    parser.add_argument('--symbol', default='', help='股票代码')
    parser.add_argument('--type', default='kline', 
                       choices=['kline', 'line', 'renko', 'pnf'])
    parser.add_argument('--indicators', default='MA', help='指标列表，逗号分隔')
    parser.add_argument('--output', default='/tmp/chart.png', help='输出图片路径')
    parser.add_argument('--theme', default='dark', choices=['dark', 'light'])
    parser.add_argument('--text-only', action='store_true', help='仅输出文字图表')
    
    args = parser.parse_args()
    
    with open(args.input) as f:
        kline_data = json.load(f)
    
    if args.text_only or not HAS_MPF:
        result = generate_text_chart(kline_data)
        print(result)
    else:
        indicators = args.indicators.split(',') if args.indicators else None
        result = generate_chart(kline_data, args.type, indicators, args.output, args.theme)
        
        if result['success']:
            print(f"✅ 图表生成成功: {result['output']}")
        else:
            print(f"❌ 生成失败: {result.get('error')}")
            print("--- 文字版 ---")
            print(generate_text_chart(kline_data))
