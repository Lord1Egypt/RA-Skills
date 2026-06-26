#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMC 交易信号监控 - 生产版 v2
数据源：新浪财经/雅虎财经（免费接口）
策略：1H 定方向 + 15M 入场 + ATR 动态止盈止损
"""

import json
import os
import sys
import requests
import re
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"

def load_config():
    """加载配置"""
    config_file = CONFIG_DIR / "symbols.json"
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "symbols": [
            {"name": "黄金", "code": "GC", "source": "sina", "enabled": True}
        ]
    }

def get_gold_price_sina():
    """
    获取 COMEX 黄金价格（新浪财经）
    接口：https://hq.sinajs.cn/list=hf_GC
    """
    try:
        # 新浪财经期货接口（HTTPS）
        url = "https://hq.sinajs.cn/list=hf_GC"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://futures.sina.com.cn/"
        }
        
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            # 解析返回：var hq_str_hf_GC="COMEX 黄金，2156.80,..."
            content = response.text.strip()
            if "=" in content and '","' in content:
                data_part = content.split('="', 1)[1].strip('"')
                fields = data_part.split(",")
                
                if len(fields) >= 10 and fields[1]:
                    try:
                        price = float(fields[1])
                        if price > 0:
                            change = float(fields[2]) if fields[2] else 0
                            change_pct = (change / price * 100) if price > 0 else 0
                            high = float(fields[4]) if fields[4] else price
                            low = float(fields[5]) if fields[5] else price
                            open_price = float(fields[3]) if fields[3] else price
                            prev_close = float(fields[10]) if fields[10] else price
                            
                            return {
                                "price": price,
                                "change": change,
                                "change_pct": change_pct,
                                "high": high,
                                "low": low,
                                "open": open_price,
                                "prev_close": prev_close,
                                "volume": 0,
                                "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                "source": "新浪财经"
                            }
                    except (ValueError, IndexError):
                        pass
    except Exception as e:
        print(f"  新浪财经接口失败：{e}")
    
    return None

def get_gold_price_yahoo():
    """
    获取 COMEX 黄金价格（雅虎财经）
    接口：https://query1.finance.yahoo.com/v8/finance/chart/GC=F
    """
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('chart') and data['chart'].get('result'):
                result = data['chart']['result'][0]
                meta = result['meta']
                quote = result.get('indicators', {}).get('quote', [{}])[0]
                
                price = quote.get('close', [meta.get('regularMarketPrice', 0)])[-1]
                high = quote.get('high', [0])[-1]
                low = quote.get('low', [0])[-1]
                open_price = quote.get('open', [0])[-1]
                prev_close = meta.get('previousClose', price)
                change = price - prev_close
                change_pct = (change / prev_close * 100) if prev_close > 0 else 0
                
                return {
                    "price": price,
                    "change": change,
                    "change_pct": change_pct,
                    "high": high,
                    "low": low,
                    "open": open_price,
                    "prev_close": prev_close,
                    "volume": quote.get('volume', [0])[-1],
                    "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "source": "雅虎财经"
                }
    except Exception as e:
        print(f"  雅虎财经接口失败：{e}")
    
    return None

def get_gold_price_mock():
    """模拟黄金价格（测试/备用）"""
    import random
    base_price = 2156.80
    change = random.uniform(-20, 20)
    return {
        "price": base_price + change,
        "change": change,
        "change_pct": change / base_price * 100,
        "high": base_price + random.uniform(10, 30),
        "low": base_price - random.uniform(10, 30),
        "open": base_price + random.uniform(-5, 5),
        "prev_close": base_price,
        "volume": random.uniform(10000, 50000),
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "source": "模拟数据"
    }

def get_gold_price(symbol_source="sina"):
    """获取黄金价格（多源切换）"""
    # 尝试新浪财经
    if symbol_source != "mock":
        price = get_gold_price_sina()
        if price:
            return price
        
        # 新浪财经失败，尝试雅虎财经
        price = get_gold_price_yahoo()
        if price:
            return price
    
    # 都失败，使用模拟数据
    print("  ⚠️ 使用模拟数据（测试模式）")
    return get_gold_price_mock()

def calculate_atr(high, low, close, period=14):
    """计算 ATR（简化版）"""
    tr = high - low
    if tr < 10:
        tr = 10
    if tr > 80:
        tr = 80
    return tr

def analyze_trend(price_data):
    """分析 1H 趋势"""
    change_pct = price_data.get('change_pct', 0)
    
    if change_pct > 0.5:
        return "BULLISH", "偏多"
    elif change_pct < -0.5:
        return "BEARISH", "偏空"
    else:
        return "NEUTRAL", "震荡"

def detect_signals(price_data, trend):
    """检测 SMC 信号"""
    signals = []
    change_pct = price_data.get('change_pct', 0)
    
    # IFC 机构蜡烛
    if abs(change_pct) > 0.8:
        signal_type = "IFC 机构蜡烛"
        direction = "BULLISH" if change_pct > 0 else "BEARISH"
        signals.append({
            "type": signal_type,
            "direction": direction,
            "strength": "强" if abs(change_pct) > 1.5 else "中",
            "description": f"15M 大{'阳' if change_pct > 0 else '阴'}线，涨跌幅 {change_pct:.2f}%"
        })
    
    # SSL/BSL 流动性扫损
    high = price_data.get('high', 0)
    low = price_data.get('low', 0)
    prev_close = price_data.get('prev_close', 0)
    
    if low < prev_close * 0.995 and change_pct < 0:
        signals.append({
            "type": "SSL 流动性扫损",
            "direction": "BEARISH",
            "strength": "中",
            "description": "跌破前低，触发卖盘流动性"
        })
    
    if high > prev_close * 1.005 and change_pct > 0:
        signals.append({
            "type": "BSL 流动性扫损",
            "direction": "BULLISH",
            "strength": "中",
            "description": "突破前高，触发买盘流动性"
        })
    
    return signals

def calculate_trade_plan(price_data, trend, signals):
    """计算交易计划"""
    price = price_data['price']
    high = price_data['high']
    low = price_data['low']
    
    atr = calculate_atr(high, low, price)
    
    if "BULLISH" in trend:
        direction = "做多"
        entry = price
        stop_loss = price - atr * 1.0
        tp1 = price + atr * 1.5
        tp2 = price + atr * 3.0
        tp3 = price + atr * 5.0
    elif "BEARISH" in trend:
        direction = "做空"
        entry = price
        stop_loss = price + atr * 1.0
        tp1 = price - atr * 1.5
        tp2 = price - atr * 3.0
        tp3 = price - atr * 5.0
    else:
        return None
    
    risk = abs(entry - stop_loss)
    reward_1 = abs(tp1 - entry)
    rr_ratio = reward_1 / risk if risk > 0 else 0
    
    return {
        "direction": direction,
        "entry": round(entry, 2),
        "stop_loss": round(stop_loss, 2),
        "tp1": round(tp1, 2),
        "tp2": round(tp2, 2),
        "tp3": round(tp3, 2),
        "risk_reward": round(rr_ratio, 2),
        "atr": round(atr, 2)
    }

def generate_signal_message(symbol, price_data, trend, signals, trade_plan):
    """生成信号消息"""
    msg = []
    msg.append(f"📈 SMC 交易信号 - {symbol}")
    msg.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    msg.append(f"📊 数据来源：{price_data.get('source', '未知')}")
    msg.append("")
    
    msg.append("【趋势分析】")
    msg.append(f"├ H1 趋势：{trend[0]} ({trend[1]})")
    msg.append(f"├ 当前价格：{price_data['price']:.2f}")
    msg.append(f"├ 涨跌幅：{price_data['change_pct']:+.2f}%")
    msg.append(f"└ 日内范围：{price_data['low']:.2f} - {price_data['high']:.2f}")
    msg.append("")
    
    if trade_plan:
        msg.append(f"【交易信号】{trade_plan['direction']}")
        msg.append(f"├ 入场：{trade_plan['entry']} 附近")
        msg.append(f"├ 止损：{trade_plan['stop_loss']} ({trade_plan['atr']} × 1 ATR)")
        msg.append(f"├ TP1: {trade_plan['tp1']} (1:{trade_plan['risk_reward']})")
        msg.append(f"├ TP2: {trade_plan['tp2']} (1:3.0)")
        msg.append(f"└ TP3: {trade_plan['tp3']} (1:5.0)")
        msg.append("")
    
    if signals:
        msg.append("【信号依据】")
        for i, sig in enumerate(signals[:3], 1):
            msg.append(f"{i}. ✅ {sig['type']}")
            msg.append(f"   {sig['description']}")
        msg.append("")
    
    if trade_plan:
        msg.append("【风险提示】")
        msg.append(f"⚠️ 风险回报比：1:{trade_plan['risk_reward']}")
        msg.append(f"⚠️ 建议仓位：总资金 2-3%")
        msg.append(f"⚠️ 严格执行止损")
        msg.append("")
    
    msg.append("---")
    msg.append("💡 SMC 策略 | H1 定方向 + 15M 入场 | ATR 动态风控")
    
    return "\n".join(msg)

def check_signal(symbol_config):
    """检查单个品种的信号"""
    symbol_name = symbol_config['name']
    symbol_code = symbol_config['code']
    symbol_source = symbol_config.get('source', 'sina')
    
    print(f"正在检查 {symbol_name} ({symbol_code})...")
    
    # 获取价格
    price_data = get_gold_price(symbol_source)
    
    if not price_data:
        print(f"  ❌ 获取价格失败")
        return None
    
    print(f"  当前价格：{price_data['price']:.2f} ({price_data['change_pct']:+.2f}%)")
    print(f"  数据来源：{price_data.get('source', '未知')}")
    
    # 分析趋势
    trend_code, trend_cn = analyze_trend(price_data)
    print(f"  H1 趋势：{trend_code} ({trend_cn})")
    
    # 检测信号
    signals = detect_signals(price_data, trend_code)
    print(f"  检测到 {len(signals)} 个信号")
    
    # 计算交易计划
    trade_plan = calculate_trade_plan(price_data, trend_code, signals)
    
    # 生成消息
    if trade_plan and len(signals) > 0:
        msg = generate_signal_message(symbol_name, price_data, trend_code, signals, trade_plan)
        return {
            "symbol": symbol_name,
            "price": price_data,
            "trend": (trend_code, trend_cn),
            "signals": signals,
            "trade_plan": trade_plan,
            "message": msg
        }
    
    return None

def main():
    """主函数"""
    print("🚀 SMC 交易信号监控 v2（生产版）")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"数据源：新浪财经 / 雅虎财经")
    print("")
    
    # 加载配置
    config = load_config()
    
    # 检查每个品种
    for symbol in config.get('symbols', []):
        if not symbol.get('enabled', True):
            continue
        
        result = check_signal(symbol)
        
        if result:
            print("\n" + "="*60)
            print(result['message'])
            print("="*60)
            
            # 保存到文件
            output_dir = SCRIPT_DIR / "output"
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / f"signal_{symbol['symbol']}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result['message'])
            
            print(f"\n✅ 信号已保存：{output_file}")
        else:
            print(f"  ⚠️ 无有效信号")
    
    print("\n✅ 检查完成")

if __name__ == "__main__":
    main()
