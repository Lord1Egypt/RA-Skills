#!/usr/bin/env python3
"""QinYu Pro - 全能加密货币分析系统 v2.0"""

import json
import urllib.request
from typing import Dict, List, Optional, Tuple
import sys

class QinYuPro:
    """QinYu Pro - 加密货币全能分析器 v2.0"""
    
    def __init__(self):
        self.cache = {}
        
    def fetch_binance_price(self, symbol: str) -> Optional[Dict]:
        try:
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
            with urllib.request.urlopen(url, timeout=10) as response:
                return json.loads(response.read())
        except:
            return None
    
    def fetch_binance_klines(self, symbol: str, interval: str = "4h", limit: int = 100) -> Optional[List]:
        try:
            url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
            with urllib.request.urlopen(url, timeout=10) as response:
                return json.loads(response.read())
        except:
            return None
    
    def fetch_coingecko_global(self) -> Optional[Dict]:
        try:
            url = "https://api.coingecko.com/api/v3/global"
            with urllib.request.urlopen(url, timeout=10) as response:
                return json.loads(response.read())
        except:
            return None
    
    def fetch_coingecko_trending(self) -> Optional[List]:
        try:
            url = "https://api.coingecko.com/api/v3/search/trending"
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read())
                return data.get('coins', [])
        except:
            return None
    
    def fetch_fear_greed(self) -> Optional[Dict]:
        try:
            url = "https://api.alternative.me/fng/?limit=2"
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read())
                if data and 'data' in data and len(data['data']) > 0:
                    return data['data'][0]
            return None
        except:
            return None
    
    def fetch_funding_rate(self, symbol: str) -> Optional[List]:
        try:
            url = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&limit=1"
            with urllib.request.urlopen(url, timeout=10) as response:
                return json.loads(response.read())
        except:
            return None
    
    def fetch_defi_tvl(self) -> Optional[List]:
        try:
            url = "https://api.llama.fi/protocols"
            with urllib.request.urlopen(url, timeout=10) as response:
                return json.loads(response.read())
        except:
            return None
    
    def fetch_defi_yields(self) -> Optional[List]:
        try:
            url = "https://yields.llama.fi/pools"
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read())
                pools = [p for p in data.get('data', []) if p.get('tvlUsd', 0) > 1000000]
                return sorted(pools, key=lambda x: x.get('apy', 0), reverse=True)[:20]
        except:
            return None
    
    def fetch_gas_prices(self) -> Optional[Dict]:
        try:
            url = "https://api.etherscan.io/api?module=gastracker&action=gasoracle"
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read())
                if data.get('status') == '1':
                    return data['result']
            return None
        except:
            return None
    
    def fetch_premium_index(self, symbol: str) -> Optional[Dict]:
        try:
            url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
            with urllib.request.urlopen(url, timeout=10) as response:
                return json.loads(response.read())
        except:
            return None
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        if len(prices) < period + 1:
            return 50.0
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    
    def calculate_ma(self, prices: List[float], period: int) -> float:
        if len(prices) < period:
            return sum(prices) / len(prices)
        return sum(prices[-period:]) / period
    
    def calculate_ema(self, prices: List[float], period: int) -> float:
        if len(prices) < period:
            return prices[-1] if prices else 0
        multiplier = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        for price in prices[period:]:
            ema = (price - ema) * multiplier + ema
        return ema
    
    def calculate_macd(self, prices: List[float]) -> Tuple[float, float, float]:
        ema12 = self.calculate_ema(prices, 12)
        ema26 = self.calculate_ema(prices, 26)
        macd_line = ema12 - ema26
        signal_line = self.calculate_ema([macd_line] + prices[-9:], 9) if len(prices) >= 9 else macd_line
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    def calculate_bollinger(self, prices: List[float], period: int = 20) -> Tuple[float, float, float]:
        if len(prices) < period:
            mid = sum(prices) / len(prices)
            return mid, mid * 1.02, mid * 0.98
        sma = sum(prices[-period:]) / period
        variance = sum([(p - sma) ** 2 for p in prices[-period:]]) / period
        std = variance ** 0.5
        return sma, sma + (2 * std), sma - (2 * std)
    
    def calculate_atr(self, highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> float:
        if len(closes) < 2:
            return 0
        tr_list = []
        for i in range(1, len(closes)):
            tr1 = highs[i] - lows[i]
            tr2 = abs(highs[i] - closes[i-1])
            tr3 = abs(lows[i] - closes[i-1])
            tr_list.append(max(tr1, tr2, tr3))
        if len(tr_list) < period:
            return sum(tr_list) / len(tr_list)
        return sum(tr_list[-period:]) / period
    
    def calculate_fibonacci(self, high: float, low: float) -> Dict[str, float]:
        diff = high - low
        return {
            '0': high, '0.236': high - 0.236 * diff, '0.382': high - 0.382 * diff,
            '0.5': high - 0.5 * diff, '0.618': high - 0.618 * diff,
            '0.786': high - 0.786 * diff, '1': low
        }
    
    def detect_cross_signals(self, prices: List[float]) -> List[str]:
        signals = []
        ma7 = [sum(prices[max(0,i-7):i+1]) / min(7, i+1) for i in range(len(prices))]
        ma14 = [sum(prices[max(0,i-14):i+1]) / min(14, i+1) for i in range(len(prices))]
        ma30 = [sum(prices[max(0,i-30):i+1]) / min(30, i+1) for i in range(len(prices))]
        
        if len(ma7) >= 2 and len(ma14) >= 2:
            if ma7[-2] <= ma14[-2] and ma7[-1] > ma14[-1]:
                signals.append("金叉 (MA7上穿MA14)")
            elif ma7[-2] >= ma14[-2] and ma7[-1] < ma14[-1]:
                signals.append("死叉 (MA7下穿MA14)")
        
        if len(ma7) >= 2 and len(ma30) >= 2:
            if ma7[-2] <= ma30[-2] and ma7[-1] > ma30[-1]:
                signals.append("长期金叉 (MA7上穿MA30)")
            elif ma7[-2] >= ma30[-2] and ma7[-1] < ma30[-1]:
                signals.append("长期死叉 (MA7下穿MA30)")
        
        return signals
    
    def analyze_market_sentiment(self, rsi: float, funding_rate: float = 0, fear_greed: int = 50) -> Dict:
        score = 0
        signals = []
        
        if rsi > 70:
            score -= 2
            signals.append("RSI超买")
        elif rsi < 30:
            score += 2
            signals.append("RSI超卖")
        
        if funding_rate > 0.01:
            score -= 1
            signals.append("多头过热")
        elif funding_rate < -0.01:
            score += 1
            signals.append("空头过热")
        
        if fear_greed < 20:
            score += 2
            signals.append("极度恐惧")
        elif fear_greed < 40:
            score += 1
            signals.append("恐惧")
        elif fear_greed > 80:
            score -= 2
            signals.append("极度贪婪")
        elif fear_greed > 60:
            score -= 1
            signals.append("贪婪")
        
        if score >= 4:
            sentiment = "极度看涨"
            action = "强烈买入"
        elif score >= 2:
            sentiment = "看涨"
            action = "买入"
        elif score == 0:
            sentiment = "中性"
            action = "观望"
        elif score <= -4:
            sentiment = "极度看跌"
            action = "强烈卖出"
        else:
            sentiment = "看跌"
            action = "卖出"
        
        return {'score': score, 'sentiment': sentiment, 'action': action, 'signals': signals}
    
    def generate_trading_strategy(self, analysis: Dict) -> Dict:
        current_price = analysis['current_price']
        support_levels = analysis['support_levels']
        resistance_levels = analysis['resistance_levels']
        rsi = analysis['rsi']
        atr = analysis['atr']
        sentiment = analysis['sentiment_analysis']
        
        strategies = {'spot': {}, 'futures': {}, 'scenarios': {}}
        
        if rsi < 30 and sentiment['score'] > 0:
            strategies['spot'] = {
                'action': '买入/定投', 'entry': f"${support_levels[0]:.2f} - ${current_price:.2f}",
                'target': f"${resistance_levels[0]:.2f}", 'stop_loss': f"${support_levels[1]:.2f}",
                'allocation': '30%仓位', 'reason': 'RSI超卖+情绪恐慌'
            }
        elif rsi > 70:
            strategies['spot'] = {
                'action': '获利了结', 'entry': '等待回调',
                'target': f"${resistance_levels[0]:.2f}", 'stop_loss': f"${support_levels[0]:.2f}",
                'allocation': '减仓50%', 'reason': 'RSI超买'
            }
        else:
            strategies['spot'] = {
                'action': '持有/观望', 'entry': f"${current_price:.2f}",
                'target': f"${resistance_levels[0]:.2f}", 'stop_loss': f"${support_levels[0]:.2f}",
                'allocation': '维持仓位', 'reason': '震荡行情'
            }
        
        volatility = atr / current_price
        leverage = "5x-10x" if volatility < 0.03 else "3x-5x" if volatility < 0.05 else "1x-3x"
        
        if rsi < 25 and sentiment['score'] >= 2:
            strategies['futures'] = {
                'action': '低多（强烈推荐）', 'direction': '做多',
                'entry': f"${support_levels[0]:.2f}", 'target': f"${resistance_levels[0]:.2f}",
                'stop_loss': f"${support_levels[1]:.2f}", 'leverage': leverage,
                'margin': '5%-8%', 'reason': '极度超卖+高盈亏比'
            }
        elif rsi > 75 and sentiment['score'] <= -2:
            strategies['futures'] = {
                'action': '高空', 'direction': '做空',
                'entry': f"${resistance_levels[0]:.2f}", 'target': f"${support_levels[0]:.2f}",
                'stop_loss': f"${resistance_levels[1]:.2f}", 'leverage': leverage,
                'margin': '5%-8%', 'reason': '极度超买'
            }
        else:
            strategies['futures'] = {
                'action': '区间操作', 'direction': '高抛低吸',
                'entry': f"${support_levels[0]:.2f}-${resistance_levels[0]:.2f}",
                'target': '区间上下沿', 'stop_loss': '突破区间外1%',
                'leverage': '3x-5x', 'margin': '3%-5%', 'reason': '震荡行情'
            }
        
        strategies['scenarios'] = {
            'bullish': {'name': '剧本A（向上突破）', 'trigger': f'突破 ${resistance_levels[0]:.2f}', 'action': '追多'},
            'bearish': {'name': '剧本B（向下变盘）', 'trigger': f'跌破 ${support_levels[0]:.2f}', 'action': '止损/做空'},
            'range': {'name': '剧本C（震荡延续）', 'trigger': f'区间波动', 'action': '高抛低吸'}
        }
        
        return strategies
    
    def analyze(self, symbol: str = "BTCUSDT", coin_id: str = "bitcoin") -> Dict:
        print(f"🔍 QinYu Pro 分析 {symbol}...")
        
        price_data = self.fetch_binance_price(symbol)
        klines_4h = self.fetch_binance_klines(symbol, "4h", 100)
        global_data = self.fetch_coingecko_global()
        trending = self.fetch_coingecko_trending()
        fear_greed = self.fetch_fear_greed()
        funding = self.fetch_funding_rate(symbol)
        premium = self.fetch_premium_index(symbol)
        defi_data = self.fetch_defi_tvl()
        defi_yields = self.fetch_defi_yields()
        gas_data = self.fetch_gas_prices()
        
        if not price_data or not klines_4h:
            return {"error": "无法获取数据"}
        
        current_price = float(price_data['lastPrice'])
        price_change_24h = float(price_data['priceChangePercent'])
        high_24h = float(price_data['highPrice'])
        low_24h = float(price_data['lowPrice'])
        volume_24h = float(price_data['volume'])
        quote_volume = float(price_data['quoteVolume'])
        
        closes_4h = [float(k[4]) for k in klines_4h]
        highs_4h = [float(k[2]) for k in klines_4h]
        lows_4h = [float(k[3]) for k in klines_4h]
        
        rsi = self.calculate_rsi(closes_4h)
        ma7 = self.calculate_ma(closes_4h, 7)
        ma14 = self.calculate_ma(closes_4h, 14)
        ma30 = self.calculate_ma(closes_4h, 30)
        ma50 = self.calculate_ma(closes_4h, 50)
        bb_mid, bb_upper, bb_lower = self.calculate_bollinger(closes_4h)
        macd_line, signal_line, macd_hist = self.calculate_macd(closes_4h)
        atr = self.calculate_atr(highs_4h, lows_4h, closes_4h)
        
        fib_high = max(highs_4h[-30:])
        fib_low = min(lows_4h[-30:])
        fib_levels = self.calculate_fibonacci(fib_high, fib_low)
        
        support_levels = [low_24h, fib_levels['0.618'], fib_levels['0.786'], fib_low]
        resistance_levels = [high_24h, fib_levels['0.382'], fib_levels['0.236'], fib_high]
        
        if current_price > ma7 > ma14 > ma30 > ma50:
            trend = "强势上涨"
        elif current_price > ma7 > ma14:
            trend = "短期看涨"
        elif current_price < ma7 < ma14 < ma30 < ma50:
            trend = "强势下跌"
        elif current_price < ma7 < ma14:
            trend = "短期看跌"
        else:
            trend = "震荡整理"
        
        cross_signals = self.detect_cross_signals(closes_4h)
        
        funding_rate = float(funding[0]['fundingRate']) * 100 if funding else 0
        mark_price = float(premium.get('markPrice', current_price)) if premium else current_price
        index_price = float(premium.get('indexPrice', current_price)) if premium else current_price
        premium_rate = ((mark_price - index_price) / index_price) * 100 if premium else 0
        
        fg_value = int(fear_greed.get('value', 50)) if fear_greed else 50
        sentiment_analysis = self.analyze_market_sentiment(rsi, funding_rate, fg_value)
        
        market_cap_data = global_data.get('data', {}).get('total_market_cap', {}).get('usd', 0) if global_data else 0
        market_cap_change = global_data.get('data', {}).get('market_cap_change_percentage_24h_usd', 0) if global_data else 0
        btc_dominance = global_data.get('data', {}).get('market_cap_percentage', {}).get('btc', 0) if global_data else 0
        
        total_defi_tvl = sum([p.get('tvl', 0) for p in defi_data[:100]]) if defi_data else 0
        
        gas_safe = gas_data.get('SafeGasPrice', 'N/A') if gas_data else 'N/A'
        
        analysis_data = {
            'current_price': current_price, 'support_levels': support_levels,
            'resistance_levels': resistance_levels, 'rsi': rsi, 'atr': atr,
            'sentiment_analysis': sentiment_analysis
        }
        strategies = self.generate_trading_strategy(analysis_data)
        
        return {
            'symbol': symbol, 'current_price': current_price,
            'price_change_24h': price_change_24h, 'high_24h': high_24h, 'low_24h': low_24h,
            'volume_24h': volume_24h, 'quote_volume': quote_volume,
            'rsi': rsi, 'ma7': ma7, 'ma14': ma14, 'ma30': ma30, 'ma50': ma50,
            'bb_upper': bb_upper, 'bb_lower': bb_lower, 'macd_hist': macd_hist, 'atr': atr,
            'support_levels': support_levels, 'resistance_levels': resistance_levels,
            'trend': trend, 'cross_signals': cross_signals,
            'sentiment': sentiment_analysis['sentiment'], 'sentiment_score': sentiment_analysis['score'],
            'funding_rate': funding_rate, 'mark_price': mark_price, 'premium_rate': premium_rate,
            'market_cap': market_cap_data, 'market_cap_change': market_cap_change,
            'btc_dominance': btc_dominance, 'fear_greed_value': fg_value,
            'total_defi_tvl': total_defi_tvl, 'gas_safe': gas_safe,
            'trending_coins': trending[:10] if trending else [],
            'defi_yields': defi_yields[:10] if defi_yields else [],
            'strategies': strategies
        }
    
    def print_full_report(self, analysis: Dict):
        print("\n" + "="*70)
        print(f"           🔮 QinYu Pro 全能加密货币分析报告 v2.0")
        print("="*70)
        
        print(f"\n💰 {analysis['symbol']}: ${analysis['current_price']:.2f} ({analysis['price_change_24h']:+.2f}%)")
        print(f"   高: ${analysis['high_24h']:.2f} | 低: ${analysis['low_24h']:.2f} | 成交: ${analysis['quote_volume']/1e6:.2f}M")
        
        print(f"\n📊 合约: 标记${analysis['mark_price']:.2f} | 资金费{analysis['funding_rate']:.4f}% | 溢价{analysis['premium_rate']:.4f}%")
        
        print(f"\n🌍 市场: 市值${analysis['market_cap']/1e12:.2f}T ({analysis['market_cap_change']:+.2f}%) | BTC占比{analysis['btc_dominance']:.1f}% | 恐惧贪婪{analysis['fear_greed_value']}")
        
        print(f"\n📈 技术: RSI {analysis['rsi']:.1f} | 趋势: {analysis['trend']}")
        print(f"   MA7/14/30/50: ${analysis['ma7']:.0f}/${analysis['ma14']:.0f}/${analysis['ma30']:.0f}/${analysis['ma50']:.0f}")
        
        if analysis['cross_signals']:
            print(f"   信号: {', '.join(analysis['cross_signals'])}")
        
        print(f"\n💭 情绪: {analysis['sentiment']} (评分{analysis['sentiment_score']})")
        
        print(f"\n🔴 压力: ${analysis['resistance_levels'][0]:.2f} | ${analysis['resistance_levels'][1]:.2f} | ${analysis['resistance_levels'][2]:.2f}")
        print(f"🟢 支撑: ${analysis['support_levels'][0]:.2f} | ${analysis['support_levels'][1]:.2f} | ${analysis['support_levels'][2]:.2f}")
        
        spot = analysis['strategies']['spot']
        fut = analysis['strategies']['futures']
        
        print(f"\n🪙 现货: {spot['action']} | 入场: {spot['entry']} | 目标: {spot['target']}")
        print(f"📜 合约: {fut['action']} ({fut['direction']}) | 杠杆: {fut['leverage']} | 入场: {fut['entry']}")
        
        print(f"\n📋 预案: A突破追多 | B跌破止损 | C区间操作")
        
        if analysis['trending_coins']:
            print(f"\n🔥 趋势: ", end="")
            for i, coin in enumerate(analysis['trending_coins'][:5], 1):
                item = coin.get('item', {})
                print(f"{item.get('symbol', 'N/A')} ", end="")
            print()
        
        print(f"\n" + "="*70)
        print("⚠️ 风险提示: 以上分析仅供参考，不构成投资建议")
        print("="*70 + "\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='QinYu Pro v2.0')
    parser.add_argument('command', choices=['analyze', 'price', 'market'], default='analyze')
    parser.add_argument('symbol', nargs='?', default='BTCUSDT')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    
    qinyu = QinYuPro()
    
    if args.command == 'analyze':
        analysis = qinyu.analyze(args.symbol)
        if 'error' in analysis:
            print(f"❌ 错误: {analysis['error']}")
            sys.exit(1)
        if args.json:
            print(json.dumps(analysis, indent=2, default=str))
        else:
            qinyu.print_full_report(analysis)
    elif args.command == 'price':
        data = qinyu.fetch_binance_price(args.symbol)
        if data:
            print(f"{args.symbol}: ${float(data['lastPrice']):.2f}")

if __name__ == '__main__':
    main()
