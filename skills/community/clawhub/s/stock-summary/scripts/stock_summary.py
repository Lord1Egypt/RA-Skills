#!/usr/bin/env python3
"""
stock_summary.py - 获取股票行情、技术分析、并生成走势图
支持：A股（东方财富）、港股、美股（Yahoo Finance）
"""

import sys
import json
import re
import subprocess
import os

# 判断市场类型
def get_market(code: str):
    code = code.strip().upper()
    if re.fullmatch(r'\d{5,6}', code):
        return 'CN'  # A股
    elif re.fullmatch(r'\d{4,5}', code):
        return 'HK'
    elif re.fullmatch(r'[A-Z]{1,5}', code):
        return 'US'
    return 'UNKNOWN'

# ============ A股（东方财富）============
def get_cn_stock(code: str):
    """东方财富 A股行情"""
    import requests
    url = f'http://push2.eastmoney.com/api/qt/stock/get?secid=1.{code}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f107,f169,f170'
    try:
        r = requests.get(url, timeout=5)
        d = r.json()['data']
        return {
            'code': code,
            'name': d.get('f58', code),
            'price': d.get('f43', 0) / 100,
            'change': d.get('f169', 0) / 100,
            'pct': d.get('f170', 0) / 100,
            'open': d.get('f60', 0) / 100,
            'high': d.get('f44', 0) / 100,
            'low': d.get('f45', 0) / 100,
            'volume': d.get('f48', 0),
            'prev_close': d.get('f60', 0) / 100,
        }
    except Exception as e:
        return None

def get_cn_history(code: str):
    """东方财富 A股历史K线（用于画图）"""
    import requests
    url = f'http://push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.{code}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57&klt=101&fqt=1&end=20500101&lmt=30'
    try:
        r = requests.get(url, timeout=5)
        data = r.json()['data']['klines']
        records = []
        for item in data:
            parts = item.split(',')
            records.append({
                'date': parts[0],
                'open': float(parts[1]),
                'close': float(parts[2]),
                'high': float(parts[3]),
                'low': float(parts[4]),
                'volume': float(parts[5]),
            })
        return records
    except:
        return None

# ============ 港股/美股（Yahoo Finance）============
def get_us_stock(code: str):
    """Yahoo Finance 港股/美股"""
    import yfinance as yf
    try:
        df = yf.download(code, period='2d', interval='1d', auto_adjust=True, progress=False)
        if df.empty:
            return None
        # MultiIndex 列，访问方式：df['Close'].iloc[-1].item()
        close = df['Close'].iloc[-1].item()
        prev_close = df['Close'].iloc[-2].item() if len(df) > 1 else close
        change = close - prev_close
        pct = (change / prev_close) * 100
        return {
            'code': code,
            'name': code,
            'price': close,
            'change': change,
            'pct': pct,
            'open': df['Open'].iloc[-1].item(),
            'high': df['High'].iloc[-1].item(),
            'low': df['Low'].iloc[-1].item(),
            'volume': df['Volume'].iloc[-1].item(),
        }
    except Exception as e:
        return None

def get_us_history(code: str):
    """Yahoo Finance 历史K线"""
    import yfinance as yf
    try:
        df = yf.download(code, period='1mo', interval='1d', auto_adjust=True, progress=False)
        if df.empty:
            return None
        records = []
        for _, row in df.iterrows():
            records.append({
                'date': str(row.name.date()),
                'open': row['Open'].item(),
                'close': row['Close'].item(),
                'high': row['High'].item(),
                'low': row['Low'].item(),
                'volume': row['Volume'].item(),
            })
        return records
    except:
        return None

# ============ 技术指标计算 ============
def calc_rsi(prices, period=14):
    """计算RSI"""
    import numpy as np
    prices = np.array(prices)
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calc_macd(prices, fast=12, slow=26, signal=9):
    """计算MACD"""
    import numpy as np
    prices = np.array(prices)
    # EMA 计算
    ema_fast = []
    ema_slow = []
    alpha_fast = 2 / (fast + 1)
    alpha_slow = 2 / (slow + 1)
    ema_fast.append(prices[0])
    ema_slow.append(prices[0])
    for p in prices[1:]:
        ema_fast.append(ema_fast[-1] * (1 - alpha_fast) + p * alpha_fast)
        ema_slow.append(ema_slow[-1] * (1 - alpha_slow) + p * alpha_slow)
    ema_fast = np.array(ema_fast)
    ema_slow = np.array(ema_slow)
    macd_line = ema_fast - ema_slow
    # Signal line (DEA)
    alpha_signal = 2 / (signal + 1)
    signal_line = []
    signal_line.append(macd_line[0])
    for m in macd_line[1:]:
        signal_line.append(signal_line[-1] * (1 - alpha_signal) + m * alpha_signal)
    signal_line = np.array(signal_line)
    macd_hist = (macd_line - signal_line) * 2
    return {
        'dif': macd_line[-1],
        'dea': signal_line[-1],
        'macd': macd_hist[-1],
    }

def rsi_signal(rsi):
    if rsi < 30:
        return '🟢 超卖'
    elif rsi > 70:
        return '🔴 超买'
    else:
        return '🟡 正常'

def macd_signal(dif, dea):
    if dif > dea:
        return '⚔️ 金叉'
    else:
        return '⚔️ 死叉'

# ============ 综合信号 ============
def get_signal(rsi, dif, dea):
    rsi_val = float(rsi)
    if rsi_val < 30 and dif > dea:
        return '🟢 买入', 'RSI超卖且MACD金叉，低位反弹信号较强'
    elif rsi_val > 70 and dif < dea:
        return '🔴 卖出', 'RSI超买且MACD死叉，高位回调风险较大'
    elif rsi_val < 40:
        return '🟡 持有（偏多）', 'RSI偏低但未超卖，暂无明确买点'
    elif rsi_val > 60:
        return '🟡 持有（偏空）', 'RSI偏高但未超买，注意短期回调风险'
    else:
        return '🟡 持有', '指标处于中性区域，建议观望'

# ============ 画图 ============
def draw_chart(records, code, market):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import numpy as np

    if not records or len(records) < 5:
        return None

    closes = [r['close'] for r in records]
    dates_str = [r['date'] for r in records]

    # 转换日期
    from datetime import datetime
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in dates_str]

    # 计算均线
    closes_arr = np.array(closes)
    ma5 = np.convolve(closes_arr, np.ones(5)/5, mode='valid')
    ma10 = np.convolve(closes_arr, np.ones(10)/10, mode='valid')

    # 对齐日期
    dates_ma5 = dates[len(dates)-len(ma5):]
    dates_ma10 = dates[len(dates)-len(ma10):]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, closes, color='#1f77b4', linewidth=1.5, label='Close')
    ax.fill_between(dates, closes, alpha=0.1, color='#1f77b4')
    ax.plot(dates_ma5, ma5, color='orange', linewidth=1, linestyle='--', label='MA5')
    ax.plot(dates_ma10, ma10, color='purple', linewidth=1, linestyle='--', label='MA10')

    last_close = closes[-1]
    ax.annotate(f'{last_close:.2f}',
                xy=(dates[-1], last_close),
                xytext=(8, 5), textcoords='offset points',
                fontsize=11, color='red', fontweight='bold')

    title = f'{code} - 1 Month Trend'
    if market == 'CN':
        title = f'{code} - 近一月走势'
    elif market == 'HK':
        title = f'{code} - 近一月走势'
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    ax.set_ylabel('HKD' if market == 'HK' else ('USD' if market == 'US' else 'CNY'), fontsize=11)
    ax.set_xlabel('')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.xticks(rotation=45)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=last_close, color='red', linestyle=':', alpha=0.5, linewidth=1)

    plt.tight_layout()
    output_path = '/root/.openclaw/workspace/stock_chart.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return output_path

# ============ 主函数 ============
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 stock_summary.py <stock_code>")
        sys.exit(1)

    code = sys.argv[1].strip()
    market = get_market(code)

    if market == 'UNKNOWN':
        print(f"❌ 无法识别的股票代码: {code}")
        sys.exit(1)

    # 获取行情
    if market == 'CN':
        info = get_cn_stock(code)
        history = get_cn_history(code)
    else:
        info = get_us_stock(code)
        history = get_us_history(code)

    if not info:
        print(f"❌ 获取数据失败: {code}")
        sys.exit(1)

    # 计算技术指标
    if history and len(history) >= 14:
        closes = [r['close'] for r in history]
        rsi = calc_rsi(closes)
        macd = calc_macd(closes)
        rsi_str = rsi_signal(rsi)
        macd_str = macd_signal(macd['dif'], macd['dea'])
        sig, reason = get_signal(rsi, macd['dif'], macd['dea'])
    else:
        rsi_str = '🟡 数据不足'
        macd_str = '🟡 数据不足'
        sig = '🟡 持有'
        reason = '历史数据不足，无法计算技术指标'
        rsi = 0
        macd = {'dif': 0, 'dea': 0}

    # 格式化输出
    price_str = f"¥{info['price']:.2f}" if market == 'CN' else (f"HK${info['price']:.2f}" if market == 'HK' else f"${info['price']:.2f}")
    sign = '+' if info['change'] >= 0 else ''
    pct_str = f"{sign}{info['pct']:.2f}%"
    change_str = f"{sign}{info['change']:.2f}"
    vol_str = f"{info['volume']/10000:.1f}万手" if market == 'CN' else (f"{info['volume']/100000000:.2f}亿" if info['volume'] > 100000000 else f"{info['volume']/10000:.1f}万")
    if market in ['HK', 'US']:
        vol_str = f"{info['volume']:,.0f}"

    rsi_val_str = f"{rsi:.1f}" if isinstance(rsi, float) and rsi != 0 else "N/A"

    print(f"📈 {info['name']}（{code}）当日行情")
    print()
    print(f"【实时行情】")
    print(f"├ 现价：{price_str}")
    print(f"├ 涨跌：{change_str}（{pct_str}）")
    print(f"├ 开盘：{price_str.split('$').pop().split('¥').pop().split('HK')[0] if False else price_str}")
    print(f"├ 最高：{price_str}")
    print(f"├ 最低：{price_str}")
    print(f"└ 成交量：{vol_str}")
    print()
    print(f"【技术分析】")
    print(f"├ RSI(14)：{rsi_val_str} → {rsi_str}")
    print(f"├ MACD：DIF={macd['dif']:.4f}, DEA={macd['dea']:.4f}, MACD={macd['macd']:.4f} → {macd_str}")
    print(f"└ 成交量：{vol_str}")
    print()
    print(f"【综合信号】{sig}")
    print(f"理由：{reason}")

    # 画图
    if history:
        chart_path = draw_chart(history, code, market)
        if chart_path:
            print()
            print(f"📊 走势图已生成：{chart_path}")

if __name__ == '__main__':
    main()
