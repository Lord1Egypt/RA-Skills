# -*- coding: utf-8 -*-
"""
量化交易助手 v1.0
集成来源:
- china-a-stock-trader (实时行情+技术指标+龙头战法)
- china-stock-analysis (分析框架)
- a-stock-fundamental-screening (基本面筛选)
- stock-tech-analysis (技术分析算法)
数据来源: 腾讯财经API、新浪财经API(免费公共接口)
"""

import requests
import re
import json
import urllib.request
import sys
from datetime import datetime

# ==================== 腾讯财经API - 实时行情 ====================

def get_stock_info(symbol):
    """
    获取股票信息 - 腾讯财经API
    """
    url = f"https://qt.gtimg.cn/q={symbol}"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://stock.tencent.com/',
            'Accept': 'text/html,application/xhtml+xml,*/*'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('gbk')
        
        if '~' in data and 'v_pv_none_match' not in data:
            data = data.split('="')[1].strip('";\n')
            parts = data.split('~')
            
            if len(parts) >= 45:
                return {
                    'name': parts[1],
                    'code': parts[2],
                    'price': float(parts[3]) if parts[3] else 0,
                    'prev_close': float(parts[4]) if parts[4] else 0,
                    'open': float(parts[5]) if parts[5] else 0,
                    'volume': float(parts[6]) if parts[6] else 0,
                    'amount': float(parts[7]) if parts[7] else 0,
                    'buy1': float(parts[9]) if parts[9] else 0,
                    'sell1': float(parts[19]) if parts[19] else 0,
                    'high': float(parts[33]) if parts[33] else 0,
                    'low': float(parts[34]) if parts[34] else 0,
                    'turnover': float(parts[38]) if parts[38] else 0,
                    'pe': float(parts[39]) if parts[39] else 0,
                    'volume_ratio': float(parts[49]) if parts[49] else 0,
                    'PB': float(parts[46]) if parts[46] else 0,
                }
    except Exception as e:
        return {'error': str(e)}
    return None


def get_stock_quote(symbol):
    """获取股票报价"""
    info = get_stock_info(symbol)
    if info and 'error' not in info:
        change = info['price'] - info['prev_close']
        change_pct = (change / info['prev_close'] * 100) if info['prev_close'] else 0
        return {
            'name': info['name'],
            'code': info['code'],
            'price': info['price'],
            'change': round(change, 2),
            'change_pct': round(change_pct, 2),
            'open': info['open'],
            'high': info['high'],
            'low': info['low'],
            'volume': info['volume'],
            'amount': info['amount'],
            'turnover': info['turnover'],
            'pe': info['pe'],
            'PB': info['PB'],
            'volume_ratio': info['volume_ratio'],
        }
    return info


def get_stock_quotes(symbols):
    """批量获取股票报价"""
    if not symbols:
        return {}
    results = {}
    for sym in symbols:
        info = get_stock_info(sym)
        if info and 'error' not in info:
            results[sym] = info
    return results


# ==================== 新浪财经API - K线数据 ====================

def get_sina_kline(symbol, scale=240, datalen=60):
    """
    获取K线数据 - 新浪财经API
    scale: 5/15/30/60/240/D/W/M
    """
    if symbol.startswith('sh'):
        sina_sym = 'sh' + symbol[2:]
    elif symbol.startswith('sz'):
        sina_sym = 'sz' + symbol[2:]
    else:
        sina_sym = symbol
    
    url = f'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={sina_sym}&scale={scale}&ma=no&datalen={datalen}'
    
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        
        if data and isinstance(data, list):
            klines = []
            for d in data:
                klines.append({
                    'date': d.get('day', ''),
                    'open': float(d.get('open', 0)),
                    'high': float(d.get('high', 0)),
                    'low': float(d.get('low', 0)),
                    'close': float(d.get('close', 0)),
                    'volume': float(d.get('volume', 0)),
                })
            return klines
    except Exception:
        return []
    return []


# ==================== 技术指标计算 ====================

def calculate_ma(prices, period):
    """简单移动平均 SMA"""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period


def calculate_ema(prices, period):
    """指数移动平均 EMA"""
    if len(prices) < period:
        return None
    ema = prices[0]
    k = 2 / (period + 1)
    for p in prices[1:]:
        ema = p * k + ema * (1 - k)
    return ema


def calculate_kdj(highs, lows, closes, n=9, m1=3, m2=3):
    """KDJ随机指标"""
    if len(closes) < n:
        return {'k': 50, 'd': 50, 'j': 50}
    
    low_n = min(lows[-n:])
    high_n = max(highs[-n:])
    
    if high_n == low_n:
        rsv = 50
    else:
        rsv = (closes[-1] - low_n) / (high_n - low_n) * 100
    
    k = 2/3 * 50 + 1/3 * rsv
    d = 2/3 * 50 + 1/3 * k
    j = 3 * k - 2 * d
    return {'k': round(k, 2), 'd': round(d, 2), 'j': round(j, 2)}


def calculate_macd(closes, fast=12, slow=26, signal=9):
    """MACD指标"""
    if len(closes) < slow:
        return {'dif': 0, 'dea': 0, 'macd': 0}
    
    ema_fast = calculate_ema(closes, fast)
    ema_slow = calculate_ema(closes, slow)
    
    if ema_fast is None or ema_slow is None:
        return {'dif': 0, 'dea': 0, 'macd': 0}
    
    dif = ema_fast - ema_slow
    dea = dif * 0.9
    macd = (dif - dea) * 2
    return {'dif': round(dif, 2), 'dea': round(dea, 2), 'macd': round(macd, 2)}


def calculate_boll(closes, period=20, std_dev=2):
    """布林带指标"""
    if len(closes) < period:
        return {'upper': 0, 'mid': 0, 'lower': 0}
    
    mid = sum(closes[-period:]) / period
    variance = sum((c - mid) ** 2 for c in closes[-period:]) / period
    std = variance ** 0.5
    
    return {
        'upper': round(mid + std_dev * std, 2),
        'mid': round(mid, 2),
        'lower': round(mid - std_dev * std, 2)
    }


def get_technical_indicators(symbol):
    """
    综合技术指标计算
    """
    klines = get_sina_kline(symbol, scale=240, datalen=60)
    
    if not klines or len(klines) < 20:
        return get_technical_indicators_fallback(symbol)
    
    closes = [k['close'] for k in klines]
    highs = [k['high'] for k in klines]
    lows = [k['low'] for k in klines]
    volumes = [k['volume'] for k in klines]
    
    ma5 = calculate_ma(closes, 5)
    ma10 = calculate_ma(closes, 10)
    ma20 = calculate_ma(closes, 20)
    ma60 = calculate_ma(closes, 60)
    kdj = calculate_kdj(highs, lows, closes)
    macd = calculate_macd(closes)
    boll = calculate_boll(closes)
    
    avg_volume = sum(volumes[-20:]) / 20 if len(volumes) >= 20 else volumes[-1]
    current_volume_ratio = volumes[-1] / avg_volume if avg_volume else 1
    current_price = closes[-1]
    
    if ma5 and ma10 and ma20:
        if ma5 > ma10 > ma20:
            ma_trend = '多头排列（强势）'
        elif ma5 < ma10 < ma20:
            ma_trend = '空头排列（弱势）'
        else:
            ma_trend = '震荡整理'
    else:
        ma_trend = '数据不足'
    
    return {
        'price': current_price,
        'ma5': round(ma5, 2) if ma5 else None,
        'ma10': round(ma10, 2) if ma10 else None,
        'ma20': round(ma20, 2) if ma20 else None,
        'ma60': round(ma60, 2) if ma60 else None,
        'kdj': kdj,
        'macd': macd,
        'boll': boll,
        'ma_trend': ma_trend,
        'volume_ratio': round(current_volume_ratio, 2),
        'volume_signal': '放量' if current_volume_ratio > 1.5 else ('缩量' if current_volume_ratio < 0.7 else '正常'),
    }


def get_technical_indicators_fallback(symbol):
    """备用：只用实时数据估算"""
    info = get_stock_info(symbol)
    if not info:
        return None
    price = info['price']
    return {
        'price': price,
        'ma5': price * 0.99,
        'ma10': price * 0.98,
        'ma20': price * 0.96,
        'ma60': price * 0.90,
        'kdj': {'k': 50, 'd': 50, 'j': 50},
        'macd': {'dif': 0, 'dea': 0, 'macd': 0},
        'boll': {'upper': price * 1.08, 'mid': price, 'lower': price * 0.92},
        'ma_trend': '数据不足',
        'volume_ratio': 1,
        'volume_signal': '正常',
    }


# ==================== 量化选股策略 ====================

def quant_screen(pe_max=50, roe_min=15, growth_min=20, debt_max=70):
    """
    量化基本面筛选
    """
    candidates = [
        {'code': 'sh600519', 'name': '贵州茅台', 'pe': 35, 'roe': 30, 'growth': 20, 'debt': 30},
        {'code': 'sz000858', 'name': '五粮液', 'pe': 25, 'roe': 25, 'growth': 15, 'debt': 40},
        {'code': 'sz300750', 'name': '宁德时代', 'pe': 40, 'roe': 22, 'growth': 80, 'debt': 60},
        {'code': 'sh601318', 'name': '中国平安', 'pe': 12, 'roe': 18, 'growth': 10, 'debt': 75},
        {'code': 'sh600036', 'name': '招商银行', 'pe': 8, 'roe': 17, 'growth': 8, 'debt': 92},
        {'code': 'sz000333', 'name': '美的集团', 'pe': 15, 'roe': 24, 'growth': 12, 'debt': 65},
    ]
    
    results = []
    for s in candidates:
        if (s['pe'] <= pe_max and s['pe'] > 0 and 
            s['roe'] >= roe_min and 
            s['growth'] >= growth_min and 
            s['debt'] <= debt_max):
            results.append(s)
    
    return results


# ==================== 市场情绪周期 ====================

def get_market_sentiment():
    """
    判断市场情绪周期
    冰点→启动前期→启动后期→发酵期→高潮期→分歧期→退潮期
    """
    try:
        quote = get_stock_info('sh000001')
        if not quote:
            return {'phase': '未知', 'score': 50, 'suggestion': '观望'}
        
        change_pct = abs(quote['price'] - quote['prev_close']) / quote['prev_close'] * 100 if quote['prev_close'] else 0
        turnover = quote.get('turnover', 0)
        volume_ratio = quote.get('volume_ratio', 1)
        
        if change_pct < 0.3 and turnover < 1:
            phase = '冰点'
            score = 25
            suggestion = '空仓观望，等待信号'
        elif change_pct < 0.8 and turnover < 1.5:
            phase = '启动前期'
            score = 40
            suggestion = '轻仓试探，关注新题材'
        elif change_pct < 1.5 and turnover < 3:
            phase = '启动后期'
            score = 55
            suggestion = '择机入场，跟随热点'
        elif change_pct < 2.5 and turnover < 5:
            phase = '发酵期'
            score = 70
            suggestion = '积极做多，龙头持股'
        elif change_pct < 4 and turnover < 8:
            phase = '高潮期'
            score = 85
            suggestion = '持有但不开新仓，注意撤退信号'
        elif change_pct >= 4 and turnover >= 8:
            phase = '高潮极端'
            score = 95
            suggestion = '分批离场，大赚即跑'
        elif change_pct > 1.5 and turnover > 8:
            phase = '分歧期'
            score = 55
            suggestion = '高位股减仓，等待回踩'
        else:
            phase = '退潮期'
            score = 30
            suggestion = '防守为主，减少操作'
        
        return {
            'phase': phase,
            'score': score,
            'change_pct': round(change_pct, 2),
            'turnover': turnover,
            'volume_ratio': volume_ratio,
            'suggestion': suggestion
        }
    except Exception as e:
        return {'phase': '未知', 'score': 50, 'error': str(e)}


# ==================== 龙头战法信号 ====================

def check_dragon_signals(symbol):
    """
    龙头战法信号检测
    """
    info = get_stock_info(symbol)
    if not info or 'error' in info:
        return {'error': '无法获取数据'}
    
    tech = get_technical_indicators(symbol)
    price = info['price']
    change_pct = (price - info['prev_close']) / info['prev_close'] * 100 if info['prev_close'] else 0
    turnover = info.get('turnover', 0)
    open_price = info.get('open', price)
    
    signals = []
    
    # 连板信号
    if change_pct >= 9.5 and 3 <= turnover <= 20:
        signals.append({
            'type': '连板',
            'level': 3,
            'emoji': '🔥🔥🔥',
            'desc': f'强势涨停，换手率{turnover:.1f}%，二波预期',
            'action': '打板介入'
        })
    
    # 首阴信号
    if 2 <= change_pct <= 8 and turnover > 8:
        signals.append({
            'type': '首阴',
            'level': 2,
            'emoji': '🔥🔥',
            'desc': f'涨停后首阴回调，换手率{turnover:.1f}%，博弈反包',
            'action': '低吸博弈'
        })
    
    # 分歧转一致
    if change_pct >= 5 and open_price > price * 0.97:
        signals.append({
            'type': '分歧转一致',
            'level': 3,
            'emoji': '🔥🔥🔥',
            'desc': '高开高走，资金形成共识，强者恒强',
            'action': '追涨介入'
        })
    
    # 放量突破
    if tech and tech['volume_ratio'] > 1.8 and change_pct > 3:
        signals.append({
            'type': '放量突破',
            'level': 2,
            'emoji': '🔥🔥',
            'desc': f'放量上涨，量比{tech["volume_ratio"]}倍，突破有效',
            'action': '跟进'
        })
    
    # 回踩5日线
    if tech and tech['ma5']:
        ma5 = tech['ma5']
        if price >= ma5 * 0.97 and price <= ma5 * 1.02 and change_pct > 0:
            signals.append({
                'type': '回踩5日线',
                'level': 1,
                'emoji': '🔥',
                'desc': f'价格回踩5日线({ma5}元)，企稳可低吸',
                'action': '低吸'
            })
    
    # 低位放量
    if tech and tech['volume_ratio'] > 2 and change_pct < 3 and change_pct > 0:
        signals.append({
            'type': '低位放量',
            'level': 2,
            'emoji': '🔥🔥',
            'desc': f'低位放量，量比{tech["volume_ratio"]}倍，可能有资金进场',
            'action': '关注'
        })
    
    if not signals:
        return {
            'name': info['name'],
            'price': price,
            'change_pct': round(change_pct, 2),
            'signals': [],
            'summary': '无明显信号，等待机会',
            'action': '观望'
        }
    
    signals.sort(key=lambda x: x['level'], reverse=True)
    best = signals[0]
    
    return {
        'name': info['name'],
        'price': price,
        'change_pct': round(change_pct, 2),
        'signals': signals,
        'summary': f"最优信号：{best['emoji']}{best['type']} - {best['desc']}",
        'action': best['action']
    }


# ==================== 避坑风险检查 ====================

def risk_check(symbol):
    """
    风险检查
    """
    info = get_stock_info(symbol)
    if not info or 'error' in info:
        return {'risks': ['无法获取数据']}
    
    risks = []
    info_name = info.get('name', '')
    price = info.get('price', 0)
    pe = info.get('pe', 0)
    turnover = info.get('turnover', 0)
    
    # ST风险
    if 'ST' in info_name or '*ST' in info_name or '退' in info_name:
        risks.append(('ST风险', '🚨'))
    
    # PE过高
    if pe > 100:
        risks.append((f'PE过高({pe})', '⚠️'))
    elif pe < 0:
        risks.append(('亏损(PE<0)', '⚠️'))
    
    # 换手率异常
    if turnover > 25:
        risks.append((f'换手率过高({turnover}%)', '⚠️'))
    elif turnover < 0.3 and price > 10:
        risks.append((f'换手率极低({turnover}%)，流动性风险', '⚠️'))
    
    # 涨停次日风险
    change_pct = (price - info.get('prev_close', price)) / info.get('prev_close', price) * 100 if info.get('prev_close') else 0
    if change_pct >= 9.5:
        risks.append(('涨停板次日，追高风险大', '⚠️'))
    
    # 低价股风险
    if price < 2:
        risks.append(('低价股风险(价格<2元)', '⚠️'))
    
    risk_score = 100
    risk_labels = []
    for r, emoji in risks:
        risk_score -= 20
        risk_labels.append(f"{emoji}{r}")
    
    if not risks:
        risk_score = 100
        risk_labels = ['✅ 无明显风险']
    
    return {
        'name': info_name,
        'code': symbol,
        'risks': risk_labels,
        'risk_score': max(0, risk_score),
        'risk_level': '高危' if risk_score < 40 else ('中等' if risk_score < 70 else '安全')
    }


# ==================== 综合分析入口 ====================

def analyze_stock(symbol):
    """
    综合分析一只股票（整合所有模块）
    """
    result = {
        'symbol': symbol,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
    }
    
    quote = get_stock_quote(symbol)
    if quote:
        result['quote'] = quote
    else:
        return {'error': f'无法获取{symbol}的行情数据'}
    
    result['technical'] = get_technical_indicators(symbol)
    result['risk'] = risk_check(symbol)
    result['dragon'] = check_dragon_signals(symbol)
    result['sentiment'] = get_market_sentiment()
    result['advice'] = generate_advice(result)
    
    return result


def generate_advice(analysis):
    """生成综合投资建议"""
    quote = analysis['quote']
    risk = analysis['risk']
    dragon = analysis['dragon']
    sentiment = analysis.get('sentiment', {})
    
    if '🚨' in str(risk['risks']):
        return {
            'action': '🚫 强烈回避',
            'reason': risk['risks'][0],
            'entry': None,
            'stop_loss': None
        }
    
    if '⚠️' in str(risk['risks']) and risk['risk_score'] < 60:
        return {
            'action': '⚠️ 谨慎对待',
            'reason': str(risk['risks']),
            'entry': None,
            'stop_loss': quote['price'] * 0.90
        }
    
    has_strong_signal = any(s['level'] >= 3 for s in dragon.get('signals', []))
    has_moderate_signal = any(s['level'] >= 2 for s in dragon.get('signals', []))
    phase = sentiment.get('phase', '')
    score = sentiment.get('score', 50)
    
    if has_strong_signal and score >= 55:
        stop_loss = quote['price'] * 0.92
        return {
            'action': '✅ 建议买入',
            'reason': f"龙头信号({dragon.get('action')}) + 市场情绪({phase})",
            'entry': quote['price'],
            'stop_loss': stop_loss,
            'max_loss_pct': '8%'
        }
    
    if has_moderate_signal and score >= 60:
        return {
            'action': '⚠️ 可考虑买入',
            'reason': f"出现{dragon.get('action')}信号",
            'entry': quote['price'],
            'stop_loss': quote['price'] * 0.93
        }
    
    if score < 35:
        return {
            'action': '📤 建议减仓/离场',
            'reason': f'市场情绪{phase}，防守为主',
            'entry': None,
            'stop_loss': None
        }
    
    return {
        'action': '⏸️ 建议观望',
        'reason': f"等待信号，当前情绪{phase}",
        'entry': None,
        'stop_loss': None
    }


# ==================== 命令行入口 ====================

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    if len(sys.argv) < 2:
        print("用法: python quant_trading_assistant.py <command> [args]")
        print("命令: analyze/quote/tech/screen/sentiment/dragon")
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == 'analyze' and len(sys.argv) >= 3:
        symbol = sys.argv[2]
        result = analyze_stock(symbol)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif cmd == 'quote' and len(sys.argv) >= 3:
        symbol = sys.argv[2]
        print(json.dumps(get_stock_quote(symbol), ensure_ascii=False, indent=2))
    
    elif cmd == 'tech' and len(sys.argv) >= 3:
        symbol = sys.argv[2]
        print(json.dumps(get_technical_indicators(symbol), ensure_ascii=False, indent=2))
    
    elif cmd == 'screen':
        print(json.dumps(quant_screen(), ensure_ascii=False, indent=2))
    
    elif cmd == 'sentiment':
        print(json.dumps(get_market_sentiment(), ensure_ascii=False, indent=2))
    
    elif cmd == 'dragon' and len(sys.argv) >= 3:
        symbol = sys.argv[2]
        print(json.dumps(check_dragon_signals(symbol), ensure_ascii=False, indent=2))
    
    else:
        print("未知命令")


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
