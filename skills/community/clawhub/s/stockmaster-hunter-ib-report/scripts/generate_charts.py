#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StockMaster Hunter - Professional Chart Generator
摩根士丹利风格投行报告专业图表生成器

Usage:
    python generate_charts.py --data data.json --output ./charts/

Requirements:
    pip install matplotlib numpy pandas
"""

import argparse
import json
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.patches import FancyBboxPatch

# ============================================================
# Font Configuration - CRITICAL for Chinese character display
# 字体配置 - 中文字体正确显示的关键
# ============================================================
plt.rcParams['font.sans-serif'] = [
    'PingFang SC',           # Apple macOS system font (primary)
    'Heiti SC',               # Apple macOS system font
    'Hiragino Sans GB',       # Apple macOS system font
    'Microsoft YaHei',        # Windows system font
    'SimHei',                 # Windows system font
    'Arial Unicode MS',       # Cross-platform fallback
    'Arial'                   # Last resort
]
plt.rcParams['axes.unicode_minus'] = False  # Fix minus sign display
plt.rcParams['figure.dpi'] = 200
plt.rcParams['savefig.dpi'] = 200
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.1

# ============================================================
# Morgan Stanley Color Palette
# 摩根士丹利配色方案
# ============================================================
COLORS = {
    'ms_blue': '#002B5C',        # Morgan Stanley Deep Blue
    'ms_gold': '#C5A572',         # Morgan Stanley Gold
    'ms_light_blue': '#60A3D9',   # Light Blue
    'ms_red': '#C0392B',           # Red for negative
    'ms_green': '#27AE60',         # Green for positive
    'ms_gray': '#7F8C8D',          # Gray
    'ms_light_gray': '#ECF0F1',    # Light Gray
    'ms_orange': '#E67E22',        # Orange
    'ms_purple': '#8E44AD',        # Purple
}

# Peer company colors for comparison charts
PEER_COLORS = [
    COLORS['ms_light_blue'],
    COLORS['ms_gold'],
    COLORS['ms_gray'],
    COLORS['ms_orange'],
    COLORS['ms_purple'],
    '#16A085',
    '#D35400',
]


def load_data(data_path):
    """Load chart data from JSON file."""
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_chart(fig, output_dir, filename):
    """Save chart to file with proper formatting."""
    output_path = os.path.join(output_dir, filename)
    fig.savefig(output_path, facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  ✓ Saved: {output_path}")
    return output_path


# ============================================================
# Chart 1: Price Trend with Moving Averages
# 图表1：股价走势与均线系统
# ============================================================
def chart_price_volume(data, output_dir):
    """Generate price trend chart with moving averages and volume."""
    print("\n[1/7] Generating Price & Volume Chart...")

    dates = [d['date'] for d in data['kline']]
    closes = [d['close'] for d in data['kline']]
    volumes = [d['volume'] for d in data['kline']]

    # Calculate moving averages
    def ma(data, period):
        result = []
        for i in range(len(data)):
            if i < period - 1:
                result.append(None)
            else:
                result.append(sum(data[i-period+1:i+1]) / period)
        return result

    ma5 = ma(closes, 5)
    ma10 = ma(closes, 10)
    ma30 = ma(closes, 30)
    ma60 = ma(closes, 60)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8),
                                     gridspec_kw={'height_ratios': [3, 1]},
                                     sharex=True)
    fig.patch.set_facecolor('white')

    # Price subplot
    x = range(len(dates))
    ax1.plot(x, closes, color=COLORS['ms_blue'], linewidth=1.5, label='Close / 收盘价', zorder=5)
    ax1.plot(x, ma5, color=COLORS['ms_gold'], linewidth=1, label='MA5 / 攻击线', alpha=0.8)
    ax1.plot(x, ma10, color=COLORS['ms_orange'], linewidth=1, label='MA10 / 操盘线', alpha=0.8)
    ax1.plot(x, ma30, color=COLORS['ms_purple'], linewidth=1, label='MA30 / 生命线', alpha=0.8)
    ax1.plot(x, ma60, color=COLORS['ms_green'], linewidth=1, label='MA60 / 决策线', alpha=0.8)

    # Mark position cost if provided
    if 'position' in data and data['position'].get('cost_price'):
        cost = data['position']['cost_price']
        ax1.axhline(y=cost, color=COLORS['ms_red'], linestyle='--', linewidth=1.5, alpha=0.7)
        ax1.text(len(dates)-1, cost, f' Cost / 成本 ¥{cost}',
                color=COLORS['ms_red'], fontsize=9, va='center')

    ax1.set_title(f"{data['stock_name']} ({data['stock_code']}) - Price Trend & Moving Averages / 股价走势与均线系统",
                  fontsize=14, fontweight='bold', color=COLORS['ms_blue'], pad=15)
    ax1.set_ylabel('Price (¥) / 价格', fontsize=11)
    ax1.legend(loc='upper left', fontsize=9, framealpha=0.9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_facecolor('#FAFAFA')

    # Volume subplot
    colors_vol = [COLORS['ms_red'] if closes[i] < closes[i-1] else COLORS['ms_green']
                  for i in range(1, len(closes))]
    colors_vol.insert(0, COLORS['ms_green'])
    ax2.bar(x, volumes, color=colors_vol, alpha=0.7, width=0.8)
    ax2.set_ylabel('Volume / 成交量', fontsize=11)
    ax2.set_xlabel('Date / 日期', fontsize=11)
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax2.set_facecolor('#FAFAFA')

    # Set x-axis ticks
    tick_positions = list(range(0, len(dates), max(1, len(dates)//10)))
    ax2.set_xticks(tick_positions)
    ax2.set_xticklabels([dates[i] for i in tick_positions], rotation=45, fontsize=8)

    plt.tight_layout()
    return save_chart(fig, output_dir, '01_price_volume.png')


# ============================================================
# Chart 2: Revenue & Net Profit Trends
# 图表2：营收与净利润趋势
# ============================================================
def chart_financial_trends(data, output_dir):
    """Generate revenue and net profit trend chart."""
    print("\n[2/7] Generating Financial Trends Chart...")

    financials = data['financials']
    periods = [f['period'] for f in financials]
    revenues = [f['revenue'] for f in financials]
    net_profits = [f['net_profit'] for f in financials]

    fig, ax1 = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')

    x = np.arange(len(periods))
    width = 0.35

    bars1 = ax1.bar(x - width/2, revenues, width, label='Revenue / 营收 (亿元)',
                     color=COLORS['ms_blue'], alpha=0.85)
    ax1.set_xlabel('Period / 报告期', fontsize=11)
    ax1.set_ylabel('Revenue (100M ¥) / 营收（亿元）', fontsize=11, color=COLORS['ms_blue'])
    ax1.tick_params(axis='y', labelcolor=COLORS['ms_blue'])

    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, net_profits, width, label='Net Profit / 净利润 (亿元)',
                     color=COLORS['ms_gold'], alpha=0.85)
    ax2.set_ylabel('Net Profit (100M ¥) / 净利润（亿元）', fontsize=11, color=COLORS['ms_gold'])
    ax2.tick_params(axis='y', labelcolor=COLORS['ms_gold'])

    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9, color=COLORS['ms_blue'])
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9, color=COLORS['ms_gold'])

    ax1.set_xticks(x)
    ax1.set_xticklabels(periods, fontsize=10)
    ax1.set_title(f"{data['stock_name']} - Revenue & Net Profit Trends / 营收与净利润趋势",
                  fontsize=14, fontweight='bold', color=COLORS['ms_blue'], pad=15)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

    ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax1.set_facecolor('#FAFAFA')

    plt.tight_layout()
    return save_chart(fig, output_dir, '02_financial_trends.png')


# ============================================================
# Chart 3: Peer Valuation Comparison
# 图表3：同业估值对比
# ============================================================
def chart_peer_valuation(data, output_dir):
    """Generate peer valuation comparison chart."""
    print("\n[3/7] Generating Peer Valuation Chart...")

    peers = data['peers']
    names = [p['name'] for p in peers]
    pe_values = [p['pe'] for p in peers]
    pb_values = [p['pb'] for p in peers]
    is_target = [p.get('is_target', False) for p in peers]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('white')

    # PE comparison
    colors_pe = [COLORS['ms_gold'] if t else COLORS['ms_light_blue'] for t in is_target]
    bars1 = ax1.barh(range(len(names)), pe_values, color=colors_pe, alpha=0.85, height=0.6)
    ax1.set_yticks(range(len(names)))
    ax1.set_yticklabels(names, fontsize=10)
    ax1.set_xlabel('PE (TTM) / 市盈率', fontsize=11)
    ax1.set_title('PE Comparison / 市盈率对比', fontsize=12, fontweight='bold', color=COLORS['ms_blue'])
    ax1.invert_yaxis()
    ax1.grid(True, alpha=0.3, linestyle='--', axis='x')
    ax1.set_facecolor('#FAFAFA')

    for i, (bar, val) in enumerate(zip(bars1, pe_values)):
        ax1.text(val + 0.5, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}x', va='center', fontsize=9, fontweight='bold' if is_target[i] else 'normal')

    # PB comparison
    colors_pb = [COLORS['ms_gold'] if t else COLORS['ms_light_blue'] for t in is_target]
    bars2 = ax2.barh(range(len(names)), pb_values, color=colors_pb, alpha=0.85, height=0.6)
    ax2.set_yticks(range(len(names)))
    ax2.set_yticklabels(names, fontsize=10)
    ax2.set_xlabel('PB / 市净率', fontsize=11)
    ax2.set_title('PB Comparison / 市净率对比', fontsize=12, fontweight='bold', color=COLORS['ms_blue'])
    ax2.invert_yaxis()
    ax2.grid(True, alpha=0.3, linestyle='--', axis='x')
    ax2.set_facecolor('#FAFAFA')

    for i, (bar, val) in enumerate(zip(bars2, pb_values)):
        ax2.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}x', va='center', fontsize=9, fontweight='bold' if is_target[i] else 'normal')

    fig.suptitle(f"{data['stock_name']} - Peer Valuation Comparison / 同业估值对比",
                 fontsize=14, fontweight='bold', color=COLORS['ms_blue'], y=1.02)

    plt.tight_layout()
    return save_chart(fig, output_dir, '03_peer_valuation.png')


# ============================================================
# Chart 4: Fibonacci Target Levels
# 图表4：斐波那契目标价位
# ============================================================
def chart_fibonacci_targets(data, output_dir):
    """Generate Fibonacci target levels chart."""
    print("\n[4/7] Generating Fibonacci Targets Chart...")

    fib = data['fibonacci']
    base_price = fib['base_price']

    levels = [
        ('Stop Loss / 止损', fib['stop_loss'], COLORS['ms_red']),
        ('Base / 基准开盘价', base_price, COLORS['ms_gray']),
        ('T1 (0.382) / 保守目标', fib['t1'], COLORS['ms_light_blue']),
        ('T2 (0.500) / 普通目标', fib['t2'], COLORS['ms_blue']),
        ('T3 (0.618) / 强势目标', fib['t3'], COLORS['ms_gold']),
        ('T4 (1.000) / 超强目标', fib['t4'], COLORS['ms_orange']),
        ('T5 (1.382) / 延伸目标', fib['t5'], COLORS['ms_purple']),
        ('T6 (1.618) / 极限目标', fib['t6'], COLORS['ms_red']),
    ]

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor('white')

    y_positions = range(len(levels))
    prices = [l[1] for l in levels]
    colors = [l[2] for l in levels]

    bars = ax.barh(y_positions, prices, color=colors, alpha=0.8, height=0.6)

    # Add price labels
    for i, (bar, price, label) in enumerate(zip(bars, prices, [l[0] for l in levels])):
        ax.text(price + 0.2, bar.get_y() + bar.get_height()/2,
                f'¥{price:.2f}', va='center', fontsize=11, fontweight='bold')

    ax.set_yticks(y_positions)
    ax.set_yticklabels([l[0] for l in levels], fontsize=10)
    ax.set_xlabel('Price (¥) / 价格', fontsize=11)
    ax.set_title(f"{data['stock_name']} - Fibonacci Target Levels / 斐波那契目标价位全景\n"
                 f"Base Price / 基准价: ¥{base_price:.2f} (Breakout Day Open / 起涨日开盘价)",
                 fontsize=13, fontweight='bold', color=COLORS['ms_blue'], pad=15)
    ax.invert_yaxis()
    ax.grid(True, alpha=0.3, linestyle='--', axis='x')
    ax.set_facecolor('#FAFAFA')

    # Add take-profit annotations
    ax.annotate('Take Profit 1/3 / 减仓1/3', xy=(fib['t2'], 3),
               xytext=(fib['t2']+2, 3.5), fontsize=9, color=COLORS['ms_blue'],
               arrowprops=dict(arrowstyle='->', color=COLORS['ms_blue']))
    ax.annotate('Take Profit 1/3 / 减仓1/3', xy=(fib['t3'], 4),
               xytext=(fib['t3']+2, 4.5), fontsize=9, color=COLORS['ms_gold'],
               arrowprops=dict(arrowstyle='->', color=COLORS['ms_gold']))
    ax.annotate('Clear Position / 清仓', xy=(fib['t4'], 5),
               xytext=(fib['t4']+2, 5.5), fontsize=9, color=COLORS['ms_orange'],
               arrowprops=dict(arrowstyle='->', color=COLORS['ms_orange']))

    plt.tight_layout()
    return save_chart(fig, output_dir, '04_fibonacci_targets.png')


# ============================================================
# Chart 5: Position P&L Sensitivity
# 图表5：持仓盈亏敏感性分析
# ============================================================
def chart_position_pnl(data, output_dir):
    """Generate position P&L sensitivity chart."""
    print("\n[5/7] Generating Position P&L Chart...")

    if 'position' not in data:
        print("  ⚠ No position data, skipping chart 5")
        return None

    pos = data['position']
    shares = pos['shares']
    cost = pos['cost_price']

    # Generate price range for sensitivity
    current_price = data.get('current_price', cost)
    price_min = min(cost * 0.7, current_price * 0.9)
    price_max = max(cost * 1.6, current_price * 1.1)
    prices = np.linspace(price_min, price_max, 100)
    pnl = (prices - cost) * shares / 10000  # Convert to 万元

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6),
                                      gridspec_kw={'width_ratios': [2, 1]})
    fig.patch.set_facecolor('white')

    # P&L sensitivity curve
    ax1.plot(prices, pnl, color=COLORS['ms_blue'], linewidth=2.5)
    ax1.axhline(y=0, color=COLORS['ms_gray'], linestyle='--', linewidth=1, alpha=0.7)
    ax1.axvline(x=cost, color=COLORS['ms_red'], linestyle='--', linewidth=1.5, alpha=0.7)
    ax1.axvline(x=current_price, color=COLORS['ms_green'], linestyle='--', linewidth=1.5, alpha=0.7)

    # Mark key points
    current_pnl = (current_price - cost) * shares / 10000
    ax1.scatter([current_price], [current_pnl], color=COLORS['ms_green'], s=100, zorder=5)
    ax1.annotate(f'Current / 当前\n¥{current_price:.2f}\n{current_pnl:+.0f}万',
                xy=(current_price, current_pnl),
                xytext=(current_price+0.5, current_pnl),
                fontsize=9, color=COLORS['ms_green'],
                arrowprops=dict(arrowstyle='->', color=COLORS['ms_green']))

    ax1.scatter([cost], [0], color=COLORS['ms_red'], s=80, zorder=5)
    ax1.annotate(f'Cost / 成本\n¥{cost:.2f}',
                xy=(cost, 0), xytext=(cost-1, max(pnl)*0.3),
                fontsize=9, color=COLORS['ms_red'],
                arrowprops=dict(arrowstyle='->', color=COLORS['ms_red']))

    ax1.set_xlabel('Stock Price (¥) / 股价', fontsize=11)
    ax1.set_ylabel('P&L (10K ¥) / 盈亏（万元）', fontsize=11)
    ax1.set_title('Position P&L Sensitivity / 持仓盈亏敏感性分析',
                  fontsize=12, fontweight='bold', color=COLORS['ms_blue'])
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_facecolor('#FAFAFA')

    # Position summary table
    ax2.axis('off')
    summary_data = [
        ['Stock / 股票', f"{data['stock_name']}"],
        ['Code / 代码', data['stock_code']],
        ['Shares / 持股', f'{shares:,}'],
        ['Cost / 成本价', f'¥{cost:.2f}'],
        ['Current / 当前价', f'¥{current_price:.2f}'],
        ['Position Value / 市值', f'¥{current_price*shares/10000:,.0f}万'],
        ['Cost Value / 成本', f'¥{cost*shares/10000:,.0f}万'],
        ['Floating P&L / 浮盈', f'{current_pnl:+,.0f}万'],
        ['Return / 收益率', f'{(current_price/cost-1)*100:+.2f}%'],
    ]

    table = ax2.table(cellText=summary_data, loc='center', cellLoc='left',
                      colWidths=[0.5, 0.5])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)

    for i, key in enumerate(summary_data):
        table[i, 0].set_facecolor(COLORS['ms_blue'])
        table[i, 0].set_text_props(color='white', fontweight='bold')
        table[i, 1].set_facecolor('#FAFAFA')

    ax2.set_title('Position Summary / 持仓概览', fontsize=12,
                   fontweight='bold', color=COLORS['ms_blue'], pad=20)

    fig.suptitle(f"{data['stock_name']} - Position Analysis / 持仓分析",
                 fontsize=14, fontweight='bold', color=COLORS['ms_blue'], y=1.02)

    plt.tight_layout()
    return save_chart(fig, output_dir, '05_position_pnl.png')


# ============================================================
# Chart 6: Revenue & Profit Breakdown
# 图表6：收入与净利润分部构成
# ============================================================
def chart_revenue_breakdown(data, output_dir):
    """Generate revenue and profit breakdown chart."""
    print("\n[6/7] Generating Revenue Breakdown Chart...")

    segments = data['segments']
    names = [s['name'] for s in segments]
    revenues = [s['revenue'] for s in segments]
    profits = [s['profit'] for s in segments]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('white')

    # Revenue pie chart
    colors = [COLORS['ms_blue'], COLORS['ms_gold'], COLORS['ms_light_blue'],
              COLORS['ms_orange'], COLORS['ms_purple'], COLORS['ms_green']]
    wedges1, texts1, autotexts1 = ax1.pie(revenues, labels=names, autopct='%1.1f%%',
                                             colors=colors[:len(names)], startangle=90,
                                             textprops={'fontsize': 10})
    for autotext in autotexts1:
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
    ax1.set_title('Revenue Breakdown / 收入构成', fontsize=12,
                  fontweight='bold', color=COLORS['ms_blue'])

    # Profit breakdown bar chart
    x = np.arange(len(names))
    bars = ax2.bar(x, profits, color=colors[:len(names)], alpha=0.85, width=0.6)
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, fontsize=9, rotation=15)
    ax2.set_ylabel('Net Profit (100M ¥) / 净利润（亿元）', fontsize=11)
    ax2.set_title('Profit Breakdown / 净利润构成', fontsize=12,
                  fontweight='bold', color=COLORS['ms_blue'])
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax2.set_facecolor('#FAFAFA')

    for bar, val in zip(bars, profits):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    fig.suptitle(f"{data['stock_name']} - Revenue & Profit Breakdown / 收入与净利润分部构成",
                 fontsize=14, fontweight='bold', color=COLORS['ms_blue'], y=1.02)

    plt.tight_layout()
    return save_chart(fig, output_dir, '06_revenue_breakdown.png')


# ============================================================
# Chart 7: Risk Radar Chart
# 图表7：风险画像雷达图
# ============================================================
def chart_risk_radar(data, output_dir):
    """Generate risk profile radar chart."""
    print("\n[7/7] Generating Risk Radar Chart...")

    risks = data['risks']
    categories = [r['category'] for r in risks]
    scores = [r['score'] for r in risks]
    industry_avg = [r['industry_avg'] for r in risks]

    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    scores += scores[:1]
    industry_avg += industry_avg[:1]

    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    fig.patch.set_facecolor('white')

    # Plot company risk profile
    ax.plot(angles, scores, 'o-', linewidth=2.5, color=COLORS['ms_gold'],
            label='Company / 公司', zorder=5)
    ax.fill(angles, scores, alpha=0.25, color=COLORS['ms_gold'])

    # Plot industry average
    ax.plot(angles, industry_avg, 'o--', linewidth=1.5, color=COLORS['ms_blue'],
            label='Industry Avg / 行业平均', alpha=0.7)
    ax.fill(angles, industry_avg, alpha=0.1, color=COLORS['ms_blue'])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=9, color='gray')
    ax.set_title(f"{data['stock_name']} - Risk Profile Radar / 风险画像雷达图\n"
                 f"(Score 1-10, higher = higher risk / 分数越高风险越大)",
                 fontsize=13, fontweight='bold', color=COLORS['ms_blue'], pad=30)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#FAFAFA')

    plt.tight_layout()
    return save_chart(fig, output_dir, '07_risk_radar.png')


# ============================================================
# Main Function
# ============================================================
def main():
    parser = argparse.ArgumentParser(description='StockMaster Hunter Chart Generator')
    parser.add_argument('--data', required=True, help='Path to data JSON file')
    parser.add_argument('--output', default='./charts', help='Output directory for charts')
    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    # Load data
    print(f"Loading data from: {args.data}")
    data = load_data(args.data)
    print(f"Stock: {data['stock_name']} ({data['stock_code']})")

    # Generate all charts
    charts = []
    charts.append(chart_price_volume(data, args.output))
    charts.append(chart_financial_trends(data, args.output))
    charts.append(chart_peer_valuation(data, args.output))
    charts.append(chart_fibonacci_targets(data, args.output))
    charts.append(chart_position_pnl(data, args.output))
    charts.append(chart_revenue_breakdown(data, args.output))
    charts.append(chart_risk_radar(data, args.output))

    print("\n" + "="*60)
    print(f"✓ All charts generated successfully!")
    print(f"  Output directory: {os.path.abspath(args.output)}")
    print(f"  Total charts: {len([c for c in charts if c])}")
    print("="*60)


if __name__ == '__main__':
    main()
