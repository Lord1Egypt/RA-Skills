import urllib.request
import json
import time

def get_stock_data(symbol, name):
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=3mo'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as f:
            data = json.loads(f.read().decode())
            result = data['chart']['result'][0]
            meta = result['meta']
            timestamps = result['timestamp']
            indicators = result['indicators']['quote'][0]
            
            closes = [c for c in indicators['close'] if c]
            
            if len(closes) < 20:
                print(f'⚠️ {name} 数据不足')
                return None
            
            # 计算技术指标
            current = closes[-1]
            prev_close = closes[-2]
            sma20 = sum(closes[-20:]) / 20
            sma50 = sum(closes[-50:]) / 50 if len(closes) >= 50 else None
            high20 = max(closes[-20:])
            low20 = min(closes[-20:])
            
            # RSI (14-day)
            gains = []
            losses = []
            for i in range(1, len(closes)):
                change = closes[i] - closes[i-1]
                if change > 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(abs(change))
            
            rsi = None
            if len(gains) >= 14:
                avg_gain = sum(gains[-14:]) / 14
                avg_loss = sum(losses[-14:]) / 14 if sum(losses[-14:]) > 0 else 0.001
                rs = avg_gain / avg_loss if avg_loss > 0 else 100
                rsi = 100 - (100 / (1 + rs))
            
            return {
                'name': name,
                'symbol': symbol,
                'current': current,
                'prev_close': prev_close,
                'change': current - prev_close,
                'change_pct': ((current - prev_close) / prev_close) * 100,
                'sma20': sma20,
                'sma50': sma50,
                'high20': high20,
                'low20': low20,
                'rsi': rsi,
                'closes': closes
            }
            
    except Exception as e:
        print(f'❌ {name} 获取失败: {e}')
        return None

def print_analysis(stock):
    if not stock:
        return
    
    print('=' * 60)
    print(f'📊 {stock["name"]} ({stock["symbol"]}) 技术面分析')
    print('=' * 60)
    
    currency = 'HKD' if '.HK' in stock['symbol'] else 'USD'
    
    print(f'💵 当前价格: {stock["current"]:.2f} {currency}')
    print(f'📈 涨跌: {stock["change"]:+.2f} ({stock["change_pct"]:+.2f}%)')
    print()
    
    # 均线分析
    print('📊 均线系统:')
    print(f'   SMA20: {stock["sma20"]:.2f}')
    if stock['sma50']:
        print(f'   SMA50: {stock["sma50"]:.2f}')
    
    if stock['current'] > stock['sma20']:
        print('   ✅ 价格在 SMA20 之上 (看多)')
    else:
        print('   ⚠️ 价格在 SMA20 之下 (看空)')
    
    if stock['sma50']:
        if stock['sma20'] > stock['sma50']:
            print('   ✅ SMA20 > SMA50 (金叉)')
        else:
            print('   ⚠️ SMA20 < SMA50 (死叉)')
    print()
    
    # 位置分析
    print('📍 位置分析:')
    print(f'   20日最高: {stock["high20"]:.2f}')
    print(f'   20日最低: {stock["low20"]:.2f}')
    
    position = ((stock['current'] - stock['low20']) / (stock['high20'] - stock['low20'])) * 100
    print(f'   当前位置: {position:.1f}% (0%=最低, 100%=最高)')
    
    if position > 80:
        print('   ⚠️ 接近20日高点，注意回调风险')
    elif position < 20:
        print('   💡 接近20日低点，关注反弹机会')
    else:
        print('   📍 在20日区间中部')
    print()
    
    # RSI 分析
    if stock['rsi']:
        print('🔄 RSI (14日):')
        print(f'   RSI: {stock["rsi"]:.1f}')
        
        if stock['rsi'] > 70:
            print('   ⚠️ RSI > 70 (超买区域)')
        elif stock['rsi'] < 30:
            print('   💡 RSI < 30 (超卖区域)')
        else:
            print('   📊 RSI 在正常区间 (30-70)')
        print()
    
    # 总结
    print('🎯 总结:')
    bullish_signals = 0
    bearish_signals = 0
    
    if stock['current'] > stock['sma20']:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    if stock['sma50']:
        if stock['sma20'] > stock['sma50']:
            bullish_signals += 1
        else:
            bearish_signals += 1
    
    if stock['rsi']:
        if stock['rsi'] < 30:
            bullish_signals += 1
        elif stock['rsi'] > 70:
            bearish_signals += 1
    
    if position < 30:
        bullish_signals += 1
    elif position > 70:
        bearish_signals += 1
    
    if bullish_signals > bearish_signals:
        print(f'   🟢 偏多信号 ({bullish_signals}:{bearish_signals})')
    elif bearish_signals > bullish_signals:
        print(f'   🔴 偏空信号 ({bullish_signals}:{bearish_signals})')
    else:
        print(f'   🟡 中性信号 ({bullish_signals}:{bearish_signals})')
    
    print()
    print('⚠️ 免责声明: 这只是技术指标的简单分析，不构成投资建议！')
    print('=' * 60)
    print()

# 主要股票列表
stocks = [
    ('0700.HK', '腾讯控股'),
    ('1810.HK', '小米集团'),
    ('TSLA', '特斯拉'),
    ('NVDA', '英伟达')
]

print('📊 股票技术面分析')
print('=' * 60)
print()

for symbol, name in stocks:
    data = get_stock_data(symbol, name)
    print_analysis(data)
    time.sleep(1)

print('✅ 分析完成！')
