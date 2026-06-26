#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日股票推荐脚本
基于技术指标 + 基本面筛选，每日推荐 5 只股票
"""

import sys
import io

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 导入数据源管理器
from data_sources import fetch_stock_price, DataSourceManager, get_manager

# 热门股票池（A 股为主）
STOCK_POOL = [
    # 白酒/消费
    ('600519', '贵州茅台'),
    ('000858', '五粮液'),
    ('000568', '泸州老窖'),

    # 银行/金融
    ('601398', '工商银行'),
    ('600036', '招商银行'),
    ('601318', '中国平安'),

    # 科技/新能源
    ('002415', '海康威视'),
    ('300750', '宁德时代'),
    ('002594', '比亚迪'),

    # 医药
    ('600276', '恒瑞医药'),
    ('300015', '爱尔眼科'),
]


def fetch_stock_basic(symbol_name_pair, timeout=3):
    """
    获取股票基本行情（使用数据源管理器）
    """
    symbol, name = symbol_name_pair

    data = fetch_stock_price(symbol)

    if not data or 'error' in data:
        return None

    # 计算振幅
    high = data.get('high', 0)
    low = data.get('low', 0)
    prev_close = data.get('prev_close', 0)
    amplitude = ((high - low) / prev_close * 100) if prev_close else 0

    return {
        'symbol': symbol,
        'name': name,
        'current': data.get('current', 0),
        'prev_close': prev_close,
        'open': data.get('open', 0),
        'high': high,
        'low': low,
        'change': data.get('change', 0),
        'change_pct': data.get('change_pct', 0),
        'volume': data.get('volume', 0),
        'amplitude': amplitude,
        'source': data.get('source', 'unknown'),
    }


def calculate_score(stock_data):
    """
    计算股票综合得分
    """
    if not stock_data or stock_data['current'] <= 0:
        return 0

    score = 50  # 基础分

    # 涨跌幅得分（温和上涨最佳）
    change = stock_data['change_pct']
    if 0 < change <= 3:
        score += 25  # 温和上涨
    elif 3 < change <= 5:
        score += 20  # 中等上涨
    elif -2 <= change <= 0:
        score += 10  # 小幅回调可关注
    elif change > 5:
        score += 5   # 大涨可能回调
    elif change < -5:
        score -= 20  # 大跌回避

    # 振幅得分（适度活跃）
    amp = stock_data['amplitude']
    if 2 <= amp <= 6:
        score += 15  # 适度活跃
    elif 6 < amp <= 10:
        score += 10  # 比较活跃
    elif amp < 2:
        score -= 5   # 成交不活跃

    # 成交量得分
    if stock_data['volume'] > 5000000:  # 500 万股以上
        score += 10

    return score


def get_daily_picks(count=5, date=None):
    """
    获取每日推荐股票
    使用多线程获取行情数据
    """
    if date is None:
        date = datetime.now().date()

    # 使用日期作为随机种子
    random.seed(date.toordinal())

    # 多线程获取股票数据
    stocks_data = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_stock_basic, stock): stock
                   for stock in STOCK_POOL}

        for future in as_completed(futures):
            data = future.result()
            if data and data['current'] > 0:
                data['score'] = calculate_score(data)
                stocks_data.append(data)

    # 按得分排序
    stocks_data.sort(key=lambda x: x['score'], reverse=True)

    # 取前 count 只
    top_n = min(count * 2, len(stocks_data))
    top_stocks = stocks_data[:top_n]

    # 随机选择增加多样性
    if len(top_stocks) > count:
        picks = random.sample(top_stocks, count)
    else:
        picks = top_stocks

    picks.sort(key=lambda x: x['score'], reverse=True)

    return picks


def format_recommendation(picks, date=None):
    """格式化推荐输出"""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    if not picks:
        return "❌ 无法获取股票数据，请稍后重试"

    lines = [
        f"## 💡 每日股票推荐 ({date})",
        "",
        "_免责声明：以下推荐仅供参考，不构成投资建议。股市有风险，投资需谨慎。_",
        "",
    ]

    for i, stock in enumerate(picks, 1):
        change_emoji = "📈" if stock['change_pct'] > 0 else "📉" if stock['change_pct'] < 0 else "➖"
        source_tag = f"[{stock.get('source', 'unknown')}]"

        lines.append(f"**{i}. {stock['name']}** ({stock['symbol']}) {source_tag}")
        lines.append(f"   - 当前价：¥{stock['current']:.2f}")
        lines.append(f"   - 涨跌幅：{change_emoji} {stock['change_pct']:+.2f}%")
        lines.append(f"   - 振幅：{stock['amplitude']:.2f}%")
        lines.append(f"   - 成交量：{stock['volume']:,} 股")
        lines.append(f"   - 推荐得分：{stock['score']}")
        lines.append("")

    lines.append("---")
    lines.append("📊 **选股逻辑**：")
    lines.append("   - 技术面：涨跌幅、振幅、成交量")
    lines.append("   - 基本面：行业龙头、业绩稳定")
    lines.append("⏰ **更新时间**：每个交易日盘中实时更新")

    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='每日股票推荐')
    parser.add_argument('--count', type=int, default=5, help='推荐数量 (默认 5)')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')

    args = parser.parse_args()

    picks = get_daily_picks(args.count)

    if args.json:
        import json
        print(json.dumps(picks, ensure_ascii=False, indent=2))
    else:
        print(format_recommendation(picks))


if __name__ == '__main__':
    main()