# -*- coding: utf-8 -*-
"""
美亚柏科(300188.SZ) 深度分析
"""
import os
import sys
import json
from datetime import datetime, timedelta

os.environ['PYTHONIOENCODING'] = 'utf-8'

import tushare as ts
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

token = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(token)
pro = ts.pro_api()

CODE = '300188.SZ'
NAME = '美亚柏科'
INDUSTRY = '电子数据取证/网络安全'

print("=" * 70)
print(f" {NAME} ({CODE}) 深度分析")
print(f" 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)

# 1. 基本信息
print("\n[1] 公司基本信息")
print("-" * 50)
print(f"  股票代码: {CODE}")
print(f"  股票名称: {NAME}")
print(f"  所属行业: {INDUSTRY}")
print(f"  所属市场: 深圳创业板(USZA)")

# 2. 日线数据
print("\n[2] 行情数据 (近60天)")
print("-" * 50)

end = datetime.now().strftime('%Y%m%d')
start = (datetime.now() - timedelta(days=80)).strftime('%Y%m%d')

daily = pro.daily(ts_code=CODE, start_date=start, end_date=end)
if daily is not None and len(daily) > 0:
    daily = daily.sort_values('trade_date')
    
    latest = daily.iloc[-1]
    prev_5 = daily.iloc[-6] if len(daily) > 5 else daily.iloc[0]
    prev_10 = daily.iloc[-11] if len(daily) > 10 else daily.iloc[0]
    prev_20 = daily.iloc[-21] if len(daily) > 20 else daily.iloc[0]
    prev_60 = daily.iloc[0]
    
    change_1d = ((latest['close'] - daily.iloc[-2]['close']) / daily.iloc[-2]['close'] * 100) if len(daily) > 1 else 0
    change_5d = ((latest['close'] - prev_5['close']) / prev_5['close'] * 100)
    change_10d = ((latest['close'] - prev_10['close']) / prev_10['close'] * 100)
    change_20d = ((latest['close'] - prev_20['close']) / prev_20['close'] * 100)
    change_60d = ((latest['close'] - prev_60['close']) / prev_60['close'] * 100)
    
    print(f"  最新价: {latest['close']:.2f}元")
    print(f"  今开: {latest['open']:.2f}  最高: {latest['high']:.2f}  最低: {latest['low']:.2f}")
    print(f"\n  涨跌幅:")
    print(f"    1日: {change_1d:+.2f}%")
    print(f"    5日: {change_5d:+.2f}%")
    print(f"    10日: {change_10d:+.2f}%")
    print(f"    20日: {change_20d:+.2f}%")
    print(f"    60日: {change_60d:+.2f}%")
    
    # 成交量分析
    vol_5d = daily.tail(5)['vol'].mean()
    vol_10d = daily.tail(10)['vol'].mean()
    vol_20d = daily.tail(20)['vol'].mean()
    vol_ratio = vol_5d / vol_20d if vol_20d > 0 else 1
    
    print(f"\n  成交量分析:")
    print(f"    5日均量: {vol_5d/10000:.1f}万手")
    print(f"    10日均量: {vol_10d/10000:.1f}万手")
    print(f"    20日均量: {vol_20d/10000:.1f}万手")
    print(f"    量比: {vol_ratio:.2f}")
    
    # 价格位置
    high_60 = daily['high'].max()
    low_60 = daily['low'].min()
    price_position = (latest['close'] - low_60) / (high_60 - low_60) * 100 if high_60 != low_60 else 50
    
    print(f"\n  价格位置:")
    print(f"    60日最高: {high_60:.2f}元")
    print(f"    60日最低: {low_60:.2f}元")
    print(f"    当前位置: {price_position:.1f}% ({'高位' if price_position > 70 else '中位' if price_position > 30 else '低位'})")
    
    # 均线分析
    close_5 = daily.tail(5)['close'].mean()
    close_10 = daily.tail(10)['close'].mean()
    close_20 = daily.tail(20)['close'].mean()
    close_60 = daily.tail(60)['close'].mean() if len(daily) >= 60 else daily['close'].mean()
    
    print(f"\n  均线系统:")
    print(f"    MA5: {close_5:.2f} {'↑' if latest['close'] > close_5 else '↓'}")
    print(f"    MA10: {close_10:.2f} {'↑' if latest['close'] > close_10 else '↓'}")
    print(f"    MA20: {close_20:.2f} {'↑' if latest['close'] > close_20 else '↓'}")
    print(f"    MA60: {close_60:.2f} {'↑' if latest['close'] > close_60 else '↓'}")
    
    ma_trend = '多头排列' if close_5 > close_10 > close_20 else '空头排列' if close_5 < close_10 < close_20 else '交叉整理'
    print(f"    均线形态: {ma_trend}")
    
    # VWAP和筹码
    vwap = (daily['close'] * daily['vol']).sum() / daily['vol'].sum()
    vwap_offset = (latest['close'] - vwap) / vwap * 100
    profitable = len(daily[daily['close'] < latest_price]) / len(daily) * 100 if 'latest_price' in dir() else 0
    profitable = len(daily[daily['close'] < latest['close']]) / len(daily) * 100
    
    print(f"\n  筹码分析:")
    print(f"    60日VWAP: {vwap:.2f}元")
    print(f"    当前偏离VWAP: {vwap_offset:+.2f}%")
    print(f"    预估获利盘: {profitable:.1f}%")

# 3. 最近交易明细
print("\n[3] 最近10个交易日明细")
print("-" * 50)
if daily is not None and len(daily) > 0:
    print(f"{'日期':<12} {'开盘':>8} {'最高':>8} {'最低':>8} {'收盘':>8} {'涨跌%':>8} {'成交量(万手)':>12}")
    for _, row in daily.tail(10).iterrows():
        print(f"{row['trade_date']:<12} {row['open']:>8.2f} {row['high']:>8.2f} {row['low']:>8.2f} {row['close']:>8.2f} {row['pct_chg']:>+7.2f}% {row['vol']/10000:>10.1f}")

# 4. 资金流向
print("\n[4] 资金流向分析")
print("-" * 50)
try:
    mf = pro.moneyflow(ts_code=CODE, start_date=start, end_date=end)
    if mf is not None and len(mf) > 0:
        mf = mf.sort_values('trade_date')
        
        buy_sm = mf['buy_sm_vol'].sum() if 'buy_sm_vol' in mf.columns else 0
        sell_sm = mf['sell_sm_vol'].sum() if 'sell_sm_vol' in mf.columns else 0
        buy_md = mf['buy_md_vol'].sum() if 'buy_md_vol' in mf.columns else 0
        sell_md = mf['sell_md_vol'].sum() if 'sell_md_vol' in mf.columns else 0
        buy_lg = mf['buy_lg_vol'].sum() if 'buy_lg_vol' in mf.columns else 0
        sell_lg = mf['sell_lg_vol'].sum() if 'sell_lg_vol' in mf.columns else 0
        buy_elg = mf['buy_elg_vol'].sum() if 'buy_elg_vol' in mf.columns else 0
        sell_elg = mf['sell_elg_vol'].sum() if 'sell_elg_vol' in mf.columns else 0
        
        sm_net = (buy_sm - sell_sm) / 100000000
        md_net = (buy_md - sell_md) / 100000000
        lg_net = (buy_lg - sell_lg) / 100000000
        elg_net = (buy_elg - sell_elg) / 100000000
        main_net = lg_net + elg_net
        total_net = sm_net + md_net + main_net
        
        print(f"  近期资金流向 (亿元):")
        print(f"    小单净流入: {sm_net:+.2f}")
        print(f"    中单净流入: {md_net:+.2f}")
        print(f"    大单净流入: {lg_net:+.2f}")
        print(f"    特大单净流入: {elg_net:+.2f}")
        print(f"    主力净流入: {main_net:+.2f}")
        print(f"    总净流入: {total_net:+.2f}")
        
        print(f"\n  最近5天资金流向:")
        for _, row in mf.tail(5).iterrows():
            net = row.get('net_mf_vol', 0)
            if pd.notna(net):
                print(f"    {row['trade_date']}: {net/10000:+.0f}万元")
    else:
        print("  无资金流向数据 (需更高级别权限)")
except Exception as e:
    print(f"  资金流向获取失败: {e}")

# 5. 技术指标
print("\n[5] 技术指标分析")
print("-" * 50)
if daily is not None and len(daily) >= 20:
    # RSI
    delta = daily['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    latest_rsi = rsi.iloc[-1]
    
    print(f"  RSI(14): {latest_rsi:.1f} ({'超买' if latest_rsi > 70 else '超卖' if latest_rsi < 30 else '中性'})")
    
    # MACD
    ema12 = daily['close'].ewm(span=12).mean()
    ema26 = daily['close'].ewm(span=26).mean()
    dif = ema12 - ema26
    dea = dif.ewm(span=9).mean()
    macd = (dif - dea) * 2
    
    latest_dif = dif.iloc[-1]
    latest_dea = dea.iloc[-1]
    latest_macd = macd.iloc[-1]
    
    print(f"  MACD: DIF={latest_dif:.3f}, DEA={latest_dea:.3f}, MACD={latest_macd:.3f}")
    macd_signal = '金叉' if latest_dif > latest_dea and dif.iloc[-2] <= dea.iloc[-2] else '死叉' if latest_dif < latest_dea and dif.iloc[-2] >= dea.iloc[-2] else '多头' if latest_dif > latest_dea else '空头'
    print(f"  MACD信号: {macd_signal}")
    
    # 布林带
    ma20 = daily['close'].rolling(20).mean()
    std20 = daily['close'].rolling(20).std()
    upper = ma20 + 2 * std20
    lower = ma20 - 2 * std20
    
    print(f"  布林带: 上轨={upper.iloc[-1]:.2f}, 中轨={ma20.iloc[-1]:.2f}, 下轨={lower.iloc[-1]:.2f}")
    bb_position = (latest['close'] - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1]) * 100
    print(f"  布林带位置: {bb_position:.1f}%")

# 6. 支撑压力位
print("\n[6] 支撑与压力位")
print("-" * 50)
if daily is not None and len(daily) > 0:
    # 近期高低点
    high_20 = daily.tail(20)['high'].max()
    low_20 = daily.tail(20)['low'].min()
    high_60 = daily['high'].max()
    low_60 = daily['low'].min()
    
    # 均线支撑压力
    print(f"  支撑位:")
    print(f"    强支撑: {low_60:.2f}元 (60日最低)")
    print(f"    支撑: {low_20:.2f}元 (20日最低)")
    if daily is not None and len(daily) >= 20:
        print(f"    MA20支撑: {close_20:.2f}元")
    
    print(f"\n  压力位:")
    if daily is not None and len(daily) >= 20:
        print(f"    MA5压力: {close_5:.2f}元" if latest['close'] < close_5 else f"    MA5支撑: {close_5:.2f}元")
        print(f"    MA10压力: {close_10:.2f}元" if latest['close'] < close_10 else f"    MA10支撑: {close_10:.2f}元")
    print(f"    压力: {high_20:.2f}元 (20日最高)")
    print(f"    强压力: {high_60:.2f}元 (60日最高)")

# 7. 综合评分
print("\n[7] 综合评分与建议")
print("-" * 50)

# 计算各维度得分
scores = {}

# 技术面
if daily is not None and len(daily) >= 20:
    tech_score = 50
    if ma_trend == '多头排列':
        tech_score += 20
    elif ma_trend == '空头排列':
        tech_score -= 20
    
    if latest_rsi < 30:
        tech_score += 10  # 超卖反弹机会
    elif latest_rsi > 70:
        tech_score -= 10  # 超买风险
    
    if latest_dif > latest_dea:
        tech_score += 10
    
    if vol_ratio > 1.2:
        tech_score += 5  # 放量
    elif vol_ratio < 0.8:
        tech_score -= 5  # 缩量
    
    scores['技术面'] = min(100, max(0, tech_score))

# 价格位置
if price_position < 20:
    pos_score = 80  # 低位机会
elif price_position < 40:
    pos_score = 60
elif price_position < 60:
    pos_score = 50
elif price_position < 80:
    pos_score = 40
else:
    pos_score = 20  # 高位风险
scores['价格位置'] = pos_score

# 成交活跃度
if vol_ratio > 1.5:
    vol_score = 90
elif vol_ratio > 1.2:
    vol_score = 70
elif vol_ratio > 0.8:
    vol_score = 50
else:
    vol_score = 30
scores['成交活跃'] = vol_score

# 综合得分
total_score = sum(scores.values()) / len(scores)

print(f"  技术面: {scores['技术面']}/100")
print(f"  价格位置: {scores['价格位置']}/100")
print(f"  成交活跃: {scores['成交活跃']}/100")
print(f"\n  综合评分: {total_score:.0f}/100")

# 操作建议
if total_score >= 70:
    suggestion = "积极关注，可考虑建仓"
elif total_score >= 50:
    suggestion = "中性观望，等待机会"
else:
    suggestion = "谨慎回避，等待企稳"

print(f"\n  操作建议: {suggestion}")

print("\n" + "=" * 70)
print(" 分析完成")
print("=" * 70)