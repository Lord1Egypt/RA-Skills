#!/usr/bin/env python3
"""
A股诊股脚本 - 基于Wyckoff 2.0方法论
支持: K线数据获取、技术分析、Wyckoff结构识别
"""

import efinance as ef
import json
import sys
from datetime import datetime, timedelta

def get_stock_data(stock_code, days=250):
    """获取股票K线数据"""
    try:
        df = ef.stock.get_quote_history(stock_code)
        if df is None or len(df) == 0:
            return None
        return df.tail(days).reset_index(drop=True)
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return None

def calculate_indicators(df):
    """计算技术指标"""
    if df is None or len(df) < 20:
        return None

    # 基础指标
    df['MA5'] = df['收盘'].rolling(5).mean()
    df['MA20'] = df['收盘'].rolling(20).mean()
    df['MA60'] = df['收盘'].rolling(60).mean()
    df['VOL_MA5'] = df['成交量'].rolling(5).mean()

    # 计算涨跌幅
    df['Return'] = df['收盘'].pct_change()

    # 计算波动率
    df['Volatility'] = df['最高'] - df['最低']
    df['Volatility_Pct'] = df['Volatility'] / df['收盘'] * 100

    return df

def identify_support_resistance(df, lookback=20):
    """识别支撑和阻力位"""
    highs = df['最高'].rolling(lookback).max()
    lows = df['最低'].rolling(lookback).min()

    # 最近20天的高低点
    recent_high = df['最高'].tail(lookback).max()
    recent_low = df['最低'].tail(lookback).min()
    current_price = df['收盘'].iloc[-1]

    return {
        'recent_high': round(recent_high, 2),
        'recent_low': round(recent_low, 2),
        'current_price': round(current_price, 2),
        'resistance': round(recent_high, 2),
        'support': round(recent_low, 2)
    }

def analyze_trend(df):
    """分析趋势"""
    if df is None or len(df) < 60:
        return None

    ma5 = df['MA5'].iloc[-1]
    ma20 = df['MA20'].iloc[-1]
    ma60 = df['MA60'].iloc[-1]
    current = df['收盘'].iloc[-1]

    # 趋势判断
    if current > ma20 > ma60:
        trend = "上涨趋势"
        bias = "看涨"
    elif current < ma20 < ma60:
        trend = "下跌趋势"
        bias = "看跌"
    else:
        trend = "震荡趋势"
        bias = "中性"

    # 均线多头/空头排列
    if ma5 > ma20 > ma60:
        ma排列 = "多头排列"
    elif ma5 < ma20 < ma60:
        ma排列 = "空头排列"
    else:
        ma排列 = "混乱排列"

    return {
        'trend': trend,
        'bias': bias,
        'ma_arrangement': ma排列,
        'ma5': round(ma5, 2),
        'ma20': round(ma20, 2),
        'ma60': round(ma60, 2)
    }

def analyze_volume(df):
    """成交量分析"""
    if df is None or len(df) < 20:
        return None

    vol_ma5 = df['VOL_MA5'].iloc[-1]
    vol_today = df['成交量'].iloc[-1]

    # 放量/缩量判断
    vol_ratio = vol_today / vol_ma5 if vol_ma5 > 0 else 1

    if vol_ratio > 1.5:
        volume_signal = "放量"
    elif vol_ratio < 0.7:
        volume_signal = "缩量"
    else:
        volume_signal = "正常"

    return {
        'volume_signal': volume_signal,
        'volume_ratio': round(vol_ratio, 2),
        'vol_ma5': int(vol_ma5),
        'vol_today': int(vol_today)
    }

def analyze_weis_wave(df, lookback=60):
    """Weis Wave 分析 - 努力vs结果法则"""
    if df is None or len(df) < 20:
        return None

    recent = df.tail(lookback).copy().reset_index(drop=True)

    # 简化Weis Wave: 识别推动浪和回调浪
    waves = []
    current_direction = None
    wave_start_idx = 0

    for i in range(1, len(recent)):
        change = recent['收盘'].iloc[i] - recent['收盘'].iloc[i-1]

        if current_direction is None:
            if abs(change) > recent['收盘'].iloc[i-1] * 0.005:  # 0.5%阈值
                current_direction = 'up' if change > 0 else 'down'
                wave_start_idx = i - 1
        elif current_direction == 'up' and change < 0:
            # 上推结束,计算回调
            wave_up = recent['收盘'].iloc[i-1] - recent['收盘'].iloc[wave_start_idx]
            wave_up_vol = recent['成交量'].iloc[wave_start_idx:i].sum()
            waves.append({'type': 'up', 'start': wave_start_idx, 'end': i-1, 'change': wave_up, 'volume': wave_up_vol})
            current_direction = 'down'
            wave_start_idx = i - 1
        elif current_direction == 'down' and change > 0:
            # 下推结束,计算反弹
            wave_down = recent['收盘'].iloc[wave_start_idx] - recent['收盘'].iloc[i-1]
            wave_down_vol = recent['成交量'].iloc[wave_start_idx:i].sum()
            waves.append({'type': 'down', 'start': wave_start_idx, 'end': i-1, 'change': wave_down, 'volume': wave_down_vol})
            current_direction = 'up'
            wave_start_idx = i - 1

    if len(waves) < 4:
        return {'signal': '数据不足', 'details': []}

    # 分析最近几个浪
    recent_waves = waves[-6:] if len(waves) >= 6 else waves

    # 计算推动vs回调的音量比
    up_waves = [w for w in recent_waves if w['type'] == 'up']
    down_waves = [w for w in recent_waves if w['type'] == 'down']

    if len(up_waves) >= 2 and len(down_waves) >= 2:
        # 检查推动浪是否放量,回调浪是否缩量(健康趋势)
        last_up = up_waves[-1]
        prev_up = up_waves[-2] if len(up_waves) > 1 else None
        last_down = down_waves[-1]
        prev_down = down_waves[-2] if len(down_waves) > 1 else None

        # 推动浪应该放量
        if prev_up:
            thrust_momentum = last_up['volume'] / prev_up['volume'] if prev_up['volume'] > 0 else 0
        else:
            thrust_momentum = 1

        # 回调浪应该缩量
        if prev_down:
            pullback_quality = prev_down['volume'] / last_down['volume'] if last_down['volume'] > 0 else 0
        else:
            pullback_quality = 1

        # 判断信号
        if thrust_momentum > 1.2 and pullback_quality > 1.2:
            signal = "✅ 健康上涨(放量推动+缩量回调)"
        elif thrust_momentum > 1.2 and pullback_quality < 1:
            signal = "⚠️ 上涨乏力(推动无力)"
        elif thrust_momentum < 1 and pullback_quality > 1.2:
            signal = "⚠️ 下跌中(缩量推动+放量回调)"
        elif thrust_momentum < 1 and pullback_quality < 1:
            signal = "🔴 弱势(推动缩量+回调放量)"
        else:
            signal = "➖ 中性"
    else:
        signal = "➖ 趋势不明确"
        thrust_momentum = 0
        pullback_quality = 0

    # 计算平均浪幅
    avg_up_change = sum(w['change'] for w in up_waves) / len(up_waves) if up_waves else 0
    avg_down_change = sum(w['change'] for w in down_waves) / len(down_waves) if down_waves else 0

    return {
        'signal': signal,
        'thrust_momentum': round(thrust_momentum, 2),
        'pullback_quality': round(pullback_quality, 2),
        'avg_up_change': round(avg_up_change, 2),
        'avg_down_change': round(avg_down_change, 2),
        'recent_up_waves': len(up_waves),
        'recent_down_waves': len(down_waves)
    }

def analyze_volume_profile(df, lookback=60):
    """Volume Profile 分析"""
    if df is None or len(df) < lookback:
        return None
    
    recent = df.tail(lookback).copy()
    
    # 创建价格区间（分成20个bin）
    min_price = recent['最低'].min()
    max_price = recent['最高'].max()
    price_range = max_price - min_price
    bin_size = price_range / 20
    
    # 计算每个价格区间的成交量
    volume_by_price = {}
    for _, row in recent.iterrows():
        # 计算价格落在哪个bin
        for i in range(20):
            bin_low = min_price + i * bin_size
            bin_high = bin_low + bin_size
            if bin_low <= row['收盘'] < bin_high:
                price_level = round((bin_low + bin_high) / 2, 2)
                volume_by_price[price_level] = volume_by_price.get(price_level, 0) + row['成交量']
                break
    
    if not volume_by_price:
        return None
    
    # 找VPOC（成交量最大的价格）
    vpoc = max(volume_by_price, key=volume_by_price.get)
    total_volume = sum(volume_by_price.values())
    
    # 计算价值区域（占70%成交量的价格区间）
    sorted_prices = sorted(volume_by_price.items(), key=lambda x: x[0])
    cumulative = 0
    val = min_price
    vah = max_price
    
    for price, vol in sorted_prices:
        cumulative += vol
        if cumulative < total_volume * 0.35:
            val = price
        if cumulative <= total_volume * 0.70:
            vah = price
    
    current_price = df['收盘'].iloc[-1]
    
    # 判断当前位置与VPOC的关系
    if current_price > vah:
        position_vpoc = "价格高于价值区上沿，看涨"
    elif current_price < val:
        position_vpoc = "价格低于价值区下沿，看跌"
    elif current_price > vpoc:
        position_vpoc = "价格在VPOC上方，偏强"
    else:
        position_vpoc = "价格在VPOC下方，偏弱"
    
    return {
        'vpoc': round(vpoc, 2),
        'vah': round(vah, 2),
        'val': round(val, 2),
        'total_volume': int(total_volume),
        'position_vpoc': position_vpoc,
        'current_vs_vpoc': round((current_price - vpoc) / vpoc * 100, 1)
    }

def analyze_historical_signals(df):
    """历史信号统计分析"""
    if df is None or len(df) < 120:
        return None

    results = {}

    # 1. VPOC突破后上涨概率
    vpoc_hits = 0
    vpoc_up_after = 0
    for i in range(20, len(df)):
        recent = df.iloc[max(0, i-60):i]
        vpoc = recent['成交量'].sum() / 60
        if df['成交量'].iloc[i] > vpoc * 1.5:
            vpoc_hits += 1
            if i + 5 < len(df):
                if df['收盘'].iloc[i+5] > df['收盘'].iloc[i]:
                    vpoc_up_after += 1

    results['vpoc_break_accuracy'] = round(vpoc_up_after / vpoc_hits * 100, 1) if vpoc_hits > 0 else 0
    results['vpoc_total_signals'] = vpoc_hits

    # 2. VAH/VAL 反弹统计
    vah_touches = 0
    val_touches = 0
    vah_rebound = 0
    val_rebound = 0

    for i in range(20, len(df)):
        recent = df.iloc[max(0, i-60):i]
        max_price = recent['最高'].max()
        min_price = recent['最低'].min()
        vah = min_price + (max_price - min_price) * 0.7
        val = min_price + (max_price - min_price) * 0.3

        if abs(df['最高'].iloc[i] - vah) / vah < 0.02:
            vah_touches += 1
            if i + 3 < len(df) and df['收盘'].iloc[i+3] < df['收盘'].iloc[i]:
                vah_rebound += 1

        if abs(df['最低'].iloc[i] - val) / val < 0.02:
            val_touches += 1
            if i + 3 < len(df) and df['收盘'].iloc[i+3] > df['收盘'].iloc[i]:
                val_rebound += 1

    results['vah_rebound_rate'] = round(vah_rebound / vah_touches * 100, 1) if vah_touches > 0 else 0
    results['vah_touches'] = vah_touches
    results['val_rebound_rate'] = round(val_rebound / val_touches * 100, 1) if val_touches > 0 else 0
    results['val_touches'] = val_touches

    # 3. 突破后3日趋势统计
    breakouts = 0
    breakout_success = 0
    for i in range(30, len(df)):
        if i + 3 < len(df):
            prev_range = df['最高'].iloc[i-20:i].max() - df['最低'].iloc[i-20:i].min()
            if df['收盘'].iloc[i] > df['最高'].iloc[i-20:i].max():
                breakouts += 1
                if df['收盘'].iloc[i+3] > df['收盘'].iloc[i]:
                    breakout_success += 1

    results['breakout_3day_success'] = round(breakout_success / breakouts * 100, 1) if breakouts > 0 else 0
    results['breakout_total'] = breakouts

    # 4. 支撑/阻力有效性
    support_tests = 0
    support_holds = 0
    for i in range(20, len(df)):
        recent_low = df['最低'].iloc[max(0, i-20):i].min()
        if abs(df['最低'].iloc[i] - recent_low) / recent_low < 0.01:
            support_tests += 1
            if i + 5 < len(df) and df['收盘'].iloc[i] > recent_low:
                support_holds += 1

    results['support_hold_rate'] = round(support_holds / support_tests * 100, 1) if support_tests > 0 else 0
    results['support_tests'] = support_tests

    return results

    """Volume Profile 分析"""
    if df is None or len(df) < lookback:
        return None

    recent = df.tail(lookback).copy()

    # 创建价格区间(分成20个bin)
    min_price = recent['最低'].min()
    max_price = recent['最高'].max()
    price_range = max_price - min_price
    bin_size = price_range / 20

    # 计算每个价格区间的成交量
    volume_by_price = {}
    for _, row in recent.iterrows():
        # 计算价格落在哪个bin
        for i in range(20):
            bin_low = min_price + i * bin_size
            bin_high = bin_low + bin_size
            if bin_low <= row['收盘'] < bin_high:
                price_level = round((bin_low + bin_high) / 2, 2)
                volume_by_price[price_level] = volume_by_price.get(price_level, 0) + row['成交量']
                break

    if not volume_by_price:
        return None

    # 找VPOC(成交量最大的价格)
    vpoc = max(volume_by_price, key=volume_by_price.get)
    total_volume = sum(volume_by_price.values())

    # 计算价值区域(占70%成交量的价格区间)
    sorted_prices = sorted(volume_by_price.items(), key=lambda x: x[0])
    cumulative = 0
    val = min_price
    vah = max_price

    for price, vol in sorted_prices:
        cumulative += vol
        if cumulative < total_volume * 0.35:
            val = price
        if cumulative <= total_volume * 0.70:
            vah = price

    current_price = df['收盘'].iloc[-1]

    # 判断当前位置与VPOC的关系
    if current_price > vah:
        position_vpoc = "价格高于价值区上沿,看涨"
    elif current_price < val:
        position_vpoc = "价格低于价值区下沿,看跌"
    elif current_price > vpoc:
        position_vpoc = "价格在VPOC上方,偏强"
    else:
        position_vpoc = "价格在VPOC下方,偏弱"

    return {
        'vpoc': round(vpoc, 2),
        'vah': round(vah, 2),
        'val': round(val, 2),
        'total_volume': int(total_volume),
        'position_vpoc': position_vpoc,
        'current_vs_vpoc': round((current_price - vpoc) / vpoc * 100, 1)
    }

def identify_wyckoff_structure(df):
    """识别Wyckoff结构"""
    if df is None or len(df) < 120:
        return None

    # 取最近120天数据分析
    recent = df.tail(120).copy()

    # 计算区间
    max_price = recent['最高'].max()
    min_price = recent['最低'].min()
    current_price = df['收盘'].iloc[-1]

    # 在区间的位置
    range_position = (current_price - min_price) / (max_price - min_price) * 100 if max_price > min_price else 50

    # 判断阶段
    if range_position < 20:
        phase = "Phase A (底部区域)"
        wyckoff_bias = "积累可能性大"
    elif range_position > 80:
        phase = "Phase E (顶部区域)"
        wyckoff_bias = "派发可能性大"
    elif range_position < 50:
        phase = "Phase B (中下区域)"
        wyckoff_bias = "震荡筑底中"
    else:
        phase = "Phase D (中上区域)"
        wyckoff_bias = "等待突破确认"

    # 检查是否有创新高/新低
    recent_20 = recent.tail(20)
    highest_20 = recent_20['最高'].max()
    lowest_20 = recent_20['最低'].min()

    making_highs = highest_20 >= max_price * 0.98
    making_lows = lowest_20 <= min_price * 1.02

    return {
        'phase': phase,
        'wyckoff_bias': wyckoff_bias,
        'range_position_pct': round(range_position, 1),
        'max_price': round(max_price, 2),
        'min_price': round(min_price, 2),
        'making_higher_highs': making_highs,
        'making_lower_lows': making_lows,
        'range_width_pct': round((max_price - min_price) / min_price * 100, 1)
    }

def calculate_risk_reward(df, support, resistance):
    """计算风险收益比"""
    if df is None:
        return None

    current = df['收盘'].iloc[-1]

    # 潜在上涨空间
    upside = (resistance - current) / current * 100
    # 潜在下跌空间
    downside = (current - support) / current * 100

    # 风险收益比
    rr_ratio = upside / downside if downside > 0 else 0

    return {
        'upside_pct': round(upside, 1),
        'downside_pct': round(downside, 1),
        'risk_reward_ratio': round(rr_ratio, 2),
        'assessment': '优质' if rr_ratio >= 2 else '一般' if rr_ratio >= 1 else '较差'
    }

def generate_diagnosis(stock_code):
    """生成完整诊股报告"""
    print(f"正在获取 {stock_code} 数据...", file=sys.stderr)

    df = get_stock_data(stock_code)
    if df is None:
        return {"error": f"无法获取 {stock_code} 的数据"}

    # 基本信息
    stock_name = df['股票名称'].iloc[-1] if '股票名称' in df.columns else stock_code

    # 执行各项分析
    indicators = calculate_indicators(df)
    support_resistance = identify_support_resistance(df)
    trend = analyze_trend(df)
    volume = analyze_volume(df)
    # Volume Profile (60天和120天)
    volume_profile_60 = analyze_volume_profile(df, lookback=60)
    volume_profile_120 = analyze_volume_profile(df, lookback=120)
    
    wyckoff = identify_wyckoff_structure(df)
    risk_reward = calculate_risk_reward(df, support_resistance['support'], support_resistance['resistance'])
    
    # Weis Wave 和历史信号分析
    weis_wave = analyze_weis_wave(df)
    historical_signals = analyze_historical_signals(df)

    # 汇总结果
    result = {
        "stock_code": stock_code,
        "stock_name": stock_name,
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "price_data": support_resistance,
        "trend_analysis": trend,
        "volume_analysis": volume,
        "volume_profile_60": volume_profile_60,
        "volume_profile_120": volume_profile_120,
        "wyckoff_analysis": wyckoff,
        "risk_reward": risk_reward,
        "weis_wave": weis_wave,
        "historical_signals": historical_signals,
        "summary": generate_summary(stock_name, trend, wyckoff, risk_reward)
    }

    return result

def generate_summary(name, trend, wyckoff, risk_reward):
    """生成简明摘要"""
    summary_parts = []

    if trend:
        summary_parts.append(f"趋势:{trend['trend']}({trend['bias']})")

    if wyckoff:
        summary_parts.append(f"结构:{wyckoff['wyckoff_bias']}")

    if risk_reward:
        summary_parts.append(f"风险收益:{risk_reward['assessment']}(1:{risk_reward['risk_reward_ratio']})")

    return " | ".join(summary_parts)

def print_report(result):
    """格式化输出报告"""
    if "error" in result:
        print(f"错误: {result['error']}")
        return

    print("=" * 60)
    print(f"📊 {result['stock_name']}({result['stock_code']}) 诊股报告")
    print(f"📅 日期: {result['report_date']}")
    print("=" * 60)

    # 价格数据
    pd = result['price_data']
    print(f"\n💰 当前价格: {pd['current_price']}")
    print(f"   支撑位: {pd['support']} | 阻力位: {pd['resistance']}")

    # 趋势分析
    if result['trend_analysis']:
        ta = result['trend_analysis']
        print(f"\n📈 趋势分析:")
        print(f"   趋势状态: {ta['trend']}")
        print(f"   市场偏向: {ta['bias']}")
        print(f"   均线排列: {ta['ma_arrangement']}")
        print(f"   MA5: {ta['ma5']} | MA20: {ta['ma20']} | MA60: {ta['ma60']}")

    # 成交量
    if result['volume_analysis']:
        va = result['volume_analysis']
        print(f"\n📊 成交量分析:")
        print(f"   信号: {va['volume_signal']} (放量比: {va['volume_ratio']}x)")

    # Volume Profile
    if result['volume_profile_60']:
        vp = result['volume_profile_60']
        print(f"\n📉 Volume Profile (60天):")
        print(f"   VPOC: {vp['vpoc']} | VAH: {vp['vah']} | VAL: {vp['val']}")
        print(f"   位置: {vp['position_vpoc']}")

    if result['volume_profile_120']:
        vp = result['volume_profile_120']
        print(f"\n📉 Volume Profile (120天):")
        print(f"   VPOC: {vp['vpoc']} | VAH: {vp['vah']} | VAL: {vp['val']}")
        print(f"   位置: {vp['position_vpoc']}")

    # Wyckoff结构
    if result['wyckoff_analysis']:
        wa = result['wyckoff_analysis']
        print(f"\n🔍 Wyckoff结构:")
        print(f"   当前阶段: {wa['phase']}")
        print(f"   结构判断: {wa['wyckoff_bias']}")
        print(f"   区间位置: {wa['range_position_pct']}%")
        print(f"   区间幅度: {wa['range_width_pct']}%")
        print(f"   创新高: {'是' if wa['making_higher_highs'] else '否'} | 创新低: {'是' if wa['making_lower_lows'] else '否'}")
    
    # Weis Wave
    if result['weis_wave']:
        ww = result['weis_wave']
        print(f"\n🌊 Weis Wave:")
        print(f"   信号: {ww['signal']}")
        if ww.get('thrust_momentum', 0) > 0:
            print(f"   推动动力: {ww['thrust_momentum']}x ({'放量' if ww['thrust_momentum'] > 1 else '缩量'})")
            print(f"   回调质量: {ww['pullback_quality']}x ({'缩量回调' if ww['pullback_quality'] > 1 else '放量回调'})")
    
    # 历史信号统计
    if result['historical_signals']:
        hs = result['historical_signals']
        print(f"\n📈 历史信号统计:")
        print(f"   VAH触碰{hs.get('vah_touches', 0)}次，反弹率{hs.get('vah_rebound_rate', 0)}%")
        print(f"   VAL触碰{hs.get('val_touches', 0)}次，反弹率{hs.get('val_rebound_rate', 0)}%")
        print(f"   突破成功率(3日){hs.get('breakout_3day_success', 0)}%")
        print(f"   支撑守住率{hs.get('support_hold_rate', 0)}%")

    # 风险收益
    if result['risk_reward']:
        rr = result['risk_reward']
        print(f"\n⚖️ 风险收益:")
        print(f"   评估: {rr['assessment']}")
        print(f"   上涨空间: +{rr['upside_pct']}%")
        print(f"   下跌空间: -{rr['downside_pct']}%")
        print(f"   风险收益比: 1:{rr['risk_reward_ratio']}")

    print("\n" + "=" * 60)
    print(f"📋 总结: {result['summary']}")
    print("=" * 60)
    print("\n⚠️ 仅供参考,不构成投资建议")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python diagnose.py <股票代码>")
        print("示例: python diagnose.py 601985")
        sys.exit(1)

    stock_code = sys.argv[1]
    result = generate_diagnosis(stock_code)
    print_report(result)
