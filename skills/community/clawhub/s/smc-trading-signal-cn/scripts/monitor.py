#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMC 交易信号监控 - 核心脚本 v2（生产版）
策略：1H 定方向 + 15M 入场 + ATR 动态止盈止损
数据源：新浪财经 / 雅虎财经（免费接口）
"""

# 使用 v2 版本
import sys
from pathlib import Path

# 重定向到 v2
v2_script = Path(__file__).parent / "monitor_v2.py"
if v2_script.exists():
    with open(v2_script, "r", encoding="utf-8") as f:
        exec(f.read())
else:
    print("错误：monitor_v2.py 不存在")
    sys.exit(1)

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 尝试导入 akshare
try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    print("⚠️ akshare 未安装，使用模拟数据测试模式")

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
            {"name": "黄金", "code": "GC", "source": "akshare", "enabled": True}
        ]
    }

def get_gold_price_akshare():
    """获取 COMEX 黄金价格（AkShare）"""
    try:
        df = ak.futures_foreign_commodity_realtime(symbol='GC')
        if len(df) > 0:
            row = df.iloc[0]
            return {
                "price": float(row['最新价']),
                "change": float(row['涨跌额']),
                "change_pct": float(row['涨跌幅']),
                "high": float(row['最高价']),
                "low": float(row['最低价']),
                "open": float(row['开盘价']),
                "prev_close": float(row['昨日结算价']),
                "volume": float(row['成交量']) if '成交量' in row else 0,
                "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    except Exception as e:
        print(f"获取金价失败：{e}")
    return None

def get_gold_price_mock():
    """模拟黄金价格（测试用）"""
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
        "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def calculate_atr(high, low, close, period=14):
    """
    计算 ATR（平均真实波幅）
    简化版：使用当前 K 线的高低点差
    """
    # 实际应该用 N 周期的 TR 平均值
    # 这里简化为当前 K 线波动
    tr = high - low
    
    # ATR 限制范围（避免极端情况）
    if tr < 10:
        tr = 10  # 最小 10 美元
    if tr > 80:
        tr = 80  # 最大 80 美元
    
    return tr

def analyze_trend(price_data):
    """
    分析 1H 趋势
    简化版：根据价格和涨跌判断
    """
    change_pct = price_data.get('change_pct', 0)
    
    # 简化趋势判断
    if change_pct > 0.5:
        return "BULLISH", "偏多"
    elif change_pct < -0.5:
        return "BEARISH", "偏空"
    else:
        return "NEUTRAL", "震荡"
    
def detect_signals(price_data, trend):
    """
    检测 SMC 信号
    """
    signals = []
    
    change_pct = price_data.get('change_pct', 0)
    volume = price_data.get('volume', 0)
    
    # IFC 机构蜡烛检测
    if abs(change_pct) > 0.8:
        signal_type = "IFC 机构蜡烛"
        direction = "BULLISH" if change_pct > 0 else "BEARISH"
        signals.append({
            "type": signal_type,
            "direction": direction,
            "strength": "强" if abs(change_pct) > 1.5 else "中",
            "description": f"15M 大{'阳' if change_pct > 0 else '阴'}线，涨跌幅 {change_pct:.2f}%"
        })
    
    # SSL 流动性扫损检测（简化）
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
    """
    计算交易计划
    1H 定方向 + 15M 入场 + ATR 止盈止损
    """
    price = price_data['price']
    high = price_data['high']
    low = price_data['low']
    
    # 计算 ATR（15 分钟）
    atr = calculate_atr(high, low, price)
    
    # 确定交易方向（跟随 1H 趋势）
    if "BULLISH" in trend:
        direction = "做多"
        entry = price
        stop_loss = price - atr * 1.0  # 1 倍 ATR 止损
        tp1 = price + atr * 1.5  # 1:1.5
        tp2 = price + atr * 3.0  # 1:3.0
        tp3 = price + atr * 5.0  # 1:5.0
    elif "BEARISH" in trend:
        direction = "做空"
        entry = price
        stop_loss = price + atr * 1.0
        tp1 = price - atr * 1.5
        tp2 = price - atr * 3.0
        tp3 = price - atr * 5.0
    else:
        return None  # 震荡市不交易
    
    # 风险回报比
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
    """检查单个品种的 sinyal"""
    symbol_name = symbol_config['name']
    symbol_code = symbol_config['code']
    
    print(f"正在检查 {symbol_name} ({symbol_code})...")
    
    # 获取价格
    if AKSHARE_AVAILABLE and symbol_config.get('source') == 'akshare':
        price_data = get_gold_price_akshare()
    else:
        price_data = get_gold_price_mock()
    
    if not price_data:
        print(f"  ❌ 获取价格失败")
        return None
    
    print(f"  当前价格：{price_data['price']:.2f} ({price_data['change_pct']:+.2f}%)")
    
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
    print("🚀 SMC 交易信号监控 v1")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"AkShare: {'✅ 已安装' if AKSHARE_AVAILABLE else '❌ 未安装（测试模式）'}")
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
