"""
Volume-Price Analysis - 量价关系深度分析模块

支持 8 种量价形态识别:
基础量价 (4 种):
1. 放量上涨 - 价↑量↑ - 看涨 ✅
2. 缩量上涨 - 价↑量↓ - 警惕 ⚠️
3. 放量下跌 - 价↓量↑ - 看跌 ❌
4. 缩量下跌 - 价↓量↓ - 观望 ⚠️

高级量价 (4 种):
5. 量价背离 - 价创新高/量未新高 - 反转信号
6. 天量天价 - 历史天量 + 高价 - 顶部信号
7. 地量地价 - 历史地量 + 低价 - 底部信号
8. 堆量上涨 - 连续放量上涨 - 强势信号
"""

import akshare as ak
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


def get_stock_history(code: str, start_date: str = None, end_date: str = None, period: int = 365) -> pd.DataFrame:
    """获取股票历史数据 (包含成交量)"""
    if end_date is None:
        end_date = datetime.now().strftime("%Y%m%d")
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=period)).strftime("%Y%m%d")
    
    try:
        df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        # 确保有成交量列
        if '成交量' not in df.columns and 'volume' in df.columns:
            df['成交量'] = df['volume']
        return df
    except Exception as e:
        print(f"获取历史数据失败：{e}")
        return pd.DataFrame()


def calculate_volume_ratio(df: pd.DataFrame, window: int = 5) -> float:
    """
    计算量比
    量比 = 今日成交量 / 近 N 日平均成交量
    
    Args:
        df: 包含成交量数据的数据框
        window: 计算平均成交量的窗口大小 (默认 5 日)
    
    Returns:
        量比值
    """
    if df.empty or len(df) < window:
        return 1.0
    
    today_volume = df['成交量'].iloc[-1]
    avg_volume = df['成交量'].iloc[-window:-1].mean()
    
    if avg_volume == 0:
        return 1.0
    
    return round(today_volume / avg_volume, 2)


def detect_volume_price_pattern(df: pd.DataFrame) -> Dict:
    """
    检测基础量价形态 (4 种)
    
    Returns:
        包含量价形态信息的字典
    """
    if df.empty or len(df) < 2:
        return {"error": "数据不足"}
    
    # 获取今日和昨日数据
    today = df.iloc[-1]
    yesterday = df.iloc[-2]
    
    # 计算价格和成交量变化
    price_change = today['收盘'] - yesterday['收盘']
    price_change_pct = (price_change / yesterday['收盘']) * 100
    volume_change = today['成交量'] - yesterday['成交量']
    volume_change_pct = (volume_change / yesterday['成交量']) * 100 if yesterday['成交量'] != 0 else 0
    
    # 计算量比
    volume_ratio = calculate_volume_ratio(df)
    
    # 判断涨跌
    price_up = price_change > 0
    volume_up = volume_change > 0
    
    # 识别量价形态
    pattern = ""
    signal = ""
    confidence = "中"
    
    if price_up and volume_up:
        pattern = "放量上涨"
        signal = "看涨"
        emoji = "✅"
        confidence = "高" if volume_ratio > 2 else "中"
    elif price_up and not volume_up:
        pattern = "缩量上涨"
        signal = "警惕"
        emoji = "⚠️"
        confidence = "低"
    elif not price_up and volume_up:
        pattern = "放量下跌"
        signal = "看跌"
        emoji = "❌"
        confidence = "高"
    else:  # not price_up and not volume_up
        pattern = "缩量下跌"
        signal = "观望"
        emoji = "⚠️"
        confidence = "低"
    
    return {
        "pattern": pattern,
        "signal": signal,
        "emoji": emoji,
        "confidence": confidence,
        "price_change_pct": round(price_change_pct, 2),
        "volume_change_pct": round(volume_change_pct, 2),
        "volume_ratio": volume_ratio,
        "today_close": round(today['收盘'], 2),
        "today_volume": today['成交量'],
        "yesterday_close": round(yesterday['收盘'], 2),
        "yesterday_volume": yesterday['成交量']
    }


def detect_price_volume_divergence(df: pd.DataFrame, lookback: int = 20) -> Dict:
    """
    检测量价背离
    价创新高但量未创新高 - 潜在反转信号
    
    Args:
        df: 历史数据
        lookback: 回看天数
    
    Returns:
        背离检测结果
    """
    if df.empty or len(df) < lookback:
        return {"divergence": False, "reason": "数据不足"}
    
    recent_data = df.iloc[-lookback:]
    
    # 找出最高价和对应的成交量
    max_price = recent_data['最高'].max()
    max_price_idx = recent_data['最高'].idxmax()
    
    # 当前价格是否接近最高价 (95% 以上)
    current_price = df['收盘'].iloc[-1]
    price_near_high = current_price >= max_price * 0.95
    
    # 当前成交量与最高价时成交量的对比
    volume_at_high = df.loc[max_price_idx, '成交量']
    current_volume = df['成交量'].iloc[-1]
    
    # 量价背离：价格接近新高但成交量明显萎缩 (低于 70%)
    volume_decline_ratio = current_volume / volume_at_high if volume_at_high != 0 else 1
    divergence = price_near_high and volume_decline_ratio < 0.7
    
    signal = ""
    if divergence:
        signal = "顶背离 - 警惕反转"
    elif current_price >= max_price * 0.98 and volume_decline_ratio > 1.2:
        signal = "量价齐升 - 强势"
    else:
        signal = "无明显背离"
    
    return {
        "divergence": divergence,
        "signal": signal,
        "price_near_high": price_near_high,
        "max_price": round(max_price, 2),
        "current_price": round(current_price, 2),
        "volume_at_high": volume_at_high,
        "current_volume": current_volume,
        "volume_decline_ratio": round(volume_decline_ratio, 2)
    }


def detect_extreme_volume(df: pd.DataFrame, lookback: int = 250) -> Dict:
    """
    检测异常量能 (天量/地量)
    
    Args:
        df: 历史数据
        lookback: 回看天数 (默认 250 日，约 1 年)
    
    Returns:
        异常量能检测结果
    """
    if df.empty or len(df) < lookback:
        lookback = min(len(df), 60)  # 至少 60 日
        if lookback < 20:
            return {"error": "数据不足"}
    
    recent_data = df.iloc[-lookback:]
    
    # 历史天量和地量
    max_volume = recent_data['成交量'].max()
    min_volume = recent_data['成交量'].min()
    avg_volume = recent_data['成交量'].mean()
    
    # 当前成交量
    current_volume = df['成交量'].iloc[-1]
    current_price = df['收盘'].iloc[-1]
    
    # 天量标准：超过历史最大成交量的 90%
    is_tianliang = current_volume >= max_volume * 0.9
    
    # 地量标准：低于历史最小成交量的 110%
    is_diliang = current_volume <= min_volume * 1.1
    
    # 天价和地价 (结合价格位置)
    max_price = recent_data['最高'].max()
    min_price = recent_data['最低'].min()
    
    is_tianjia = current_price >= max_price * 0.95
    is_dijia = current_price <= min_price * 1.05
    
    # 综合判断
    signal = "正常"
    warning_level = "无"
    
    if is_tianliang and is_tianjia:
        signal = "天量天价 - 顶部信号"
        warning_level = "高"
    elif is_tianliang:
        signal = "天量 - 关注"
        warning_level = "中"
    elif is_diliang and is_dijia:
        signal = "地量地价 - 底部信号"
        warning_level = "高"
    elif is_diliang:
        signal = "地量 - 关注"
        warning_level = "中"
    
    return {
        "signal": signal,
        "warning_level": warning_level,
        "is_tianliang": is_tianliang,
        "is_diliang": is_diliang,
        "is_tianjia": is_tianjia,
        "is_dijia": is_dijia,
        "current_volume": current_volume,
        "max_volume": max_volume,
        "min_volume": min_volume,
        "avg_volume": round(avg_volume, 0),
        "current_price": round(current_price, 2),
        "max_price": round(max_price, 2),
        "min_price": round(min_price, 2),
        "volume_percentile": round((current_volume - min_volume) / (max_volume - min_volume) * 100, 1) if max_volume != min_volume else 50
    }


def detect_continuous_volume_increase(df: pd.DataFrame, min_days: int = 3) -> Dict:
    """
    检测堆量上涨 (连续放量上涨)
    
    Args:
        df: 历史数据
        min_days: 最小连续天数
    
    Returns:
        堆量上涨检测结果
    """
    if df.empty or len(df) < min_days + 5:
        return {"signal": "数据不足", "is_duiliang": False}
    
    # 计算 5 日平均成交量作为基准
    recent_data = df.iloc[-(min_days + 10):]
    baseline_volume = recent_data['成交量'].iloc[:-min_days].mean()
    
    # 检测连续放量上涨
    consecutive_days = 0
    total_price_gain = 0
    details = []
    
    for i in range(len(df) - min_days, len(df)):
        if i == 0:
            continue
        
        today = df.iloc[i]
        yesterday = df.iloc[i-1]
        
        # 放量：今日成交量 > 5 日均量 * 1.2
        volume_up = today['成交量'] > baseline_volume * 1.2
        
        # 上涨：今日收盘价 > 昨日收盘价
        price_up = today['收盘'] > yesterday['收盘']
        
        if volume_up and price_up:
            consecutive_days += 1
            daily_gain = (today['收盘'] - yesterday['收盘']) / yesterday['收盘'] * 100
            total_price_gain += daily_gain
            details.append({
                "date": today['日期'] if '日期' in df.columns else i,
                "volume_ratio": round(today['成交量'] / baseline_volume, 2),
                "price_gain": round(daily_gain, 2)
            })
        else:
            consecutive_days = 0
            total_price_gain = 0
            details = []
    
    is_duiliang = consecutive_days >= min_days
    
    signal = "正常"
    strength = "无"
    
    if is_duiliang:
        if consecutive_days >= 5:
            signal = f"堆量上涨 - 连续{consecutive_days}日 - 强势信号"
            strength = "很强"
        elif consecutive_days >= 3:
            signal = f"堆量上涨 - 连续{consecutive_days}日"
            strength = "强"
    
    return {
        "signal": signal,
        "is_duiliang": is_duiliang,
        "consecutive_days": consecutive_days,
        "total_price_gain": round(total_price_gain, 2),
        "strength": strength,
        "baseline_volume": round(baseline_volume, 0),
        "details": details[-5:]  # 最近 5 天详情
    }


def analyze_volume_price_comprehensive(code: str, lookback: int = 250) -> Dict:
    """
    综合量价分析 (包含所有 8 种形态)
    
    Args:
        code: 股票代码
        lookback: 回看天数
    
    Returns:
        综合分析报告
    """
    # 获取历史数据
    df = get_stock_history(code, period=lookback)
    
    if df.empty:
        return {"error": "数据获取失败", "code": code}
    
    # 1-4. 基础量价形态
    basic_pattern = detect_volume_price_pattern(df)
    
    # 5. 量价背离
    divergence = detect_price_volume_divergence(df)
    
    # 6-7. 天量天价/地量地价
    extreme_volume = detect_extreme_volume(df)
    
    # 8. 堆量上涨
    continuous_volume = detect_continuous_volume_increase(df)
    
    # 量比
    volume_ratio = calculate_volume_ratio(df)
    
    # 综合评分
    score = 50  # 基础分
    signals = []
    
    # 根据形态调整评分
    if basic_pattern.get("pattern") == "放量上涨":
        score += 15
        signals.append("✅ 放量上涨")
    elif basic_pattern.get("pattern") == "缩量上涨":
        score += 5
        signals.append("⚠️ 缩量上涨 (警惕)")
    elif basic_pattern.get("pattern") == "放量下跌":
        score -= 15
        signals.append("❌ 放量下跌")
    elif basic_pattern.get("pattern") == "缩量下跌":
        score -= 5
        signals.append("⚠️ 缩量下跌 (观望)")
    
    if divergence.get("divergence"):
        score -= 10
        signals.append("⚠️ 量价背离")
    
    if extreme_volume.get("is_tianliang") and extreme_volume.get("is_tianjia"):
        score -= 20
        signals.append("❌ 天量天价")
    elif extreme_volume.get("is_diliang") and extreme_volume.get("is_dijia"):
        score += 20
        signals.append("✅ 地量地价")
    
    if continuous_volume.get("is_duiliang"):
        score += 15
        signals.append("✅ 堆量上涨")
    
    # 量比评估
    volume_status = "正常"
    if volume_ratio > 3:
        volume_status = "异常放量"
    elif volume_ratio > 2:
        volume_status = "放量"
    elif volume_ratio < 0.3:
        volume_status = "异常缩量"
    elif volume_ratio < 0.5:
        volume_status = "缩量"
    
    # 综合建议
    if score >= 80:
        recommendation = "强烈看涨"
        level = "很高"
    elif score >= 65:
        recommendation = "看涨"
        level = "高"
    elif score >= 55:
        recommendation = "中性偏多"
        level = "中"
    elif score >= 45:
        recommendation = "中性"
        level = "中"
    elif score >= 35:
        recommendation = "中性偏空"
        level = "中"
    elif score >= 20:
        recommendation = "看跌"
        level = "高"
    else:
        recommendation = "强烈看跌"
        level = "很高"
    
    return {
        "code": code,
        "updated": datetime.now().isoformat(),
        "current_price": round(df['收盘'].iloc[-1], 2),
        "volume_ratio": volume_ratio,
        "volume_status": volume_status,
        "basic_pattern": basic_pattern,
        "divergence": divergence,
        "extreme_volume": extreme_volume,
        "continuous_volume": continuous_volume,
        "comprehensive_score": score,
        "recommendation": recommendation,
        "confidence_level": level,
        "signals": signals
    }


def backtest_volume_price_strategy(code: str, start_date: str, end_date: str, 
                                    strategy: str = "放量上涨", 
                                    hold_days: int = 5) -> Dict:
    """
    量价策略回测
    
    Args:
        code: 股票代码
        start_date: 回测开始日期 (YYYYMMDD)
        end_date: 回测结束日期 (YYYYMMDD)
        strategy: 策略名称 ("放量上涨", "缩量上涨", "放量下跌", "缩量下跌", "地量地价", "堆量上涨")
        hold_days: 持有天数
    
    Returns:
        回测结果
    """
    df = get_stock_history(code, start_date=start_date, end_date=end_date)
    
    if df.empty or len(df) < hold_days + 10:
        return {"error": "数据不足"}
    
    # 计算 5 日平均成交量
    df['vol_ma5'] = df['成交量'].rolling(window=5).mean()
    df['price_change'] = df['收盘'].pct_change() * 100
    
    trades = []
    signals = []
    
    for i in range(10, len(df) - hold_days):
        today = df.iloc[i]
        yesterday = df.iloc[i-1]
        
        # 计算量比
        volume_ratio = today['成交量'] / df['vol_ma5'].iloc[i-1] if df['vol_ma5'].iloc[i-1] != 0 else 1
        
        signal = None
        
        # 根据策略判断信号
        if strategy == "放量上涨":
            if today['收盘'] > yesterday['收盘'] and volume_ratio > 2:
                signal = "买入"
        elif strategy == "缩量上涨":
            if today['收盘'] > yesterday['收盘'] and volume_ratio < 0.5:
                signal = "买入"
        elif strategy == "放量下跌":
            if today['收盘'] < yesterday['收盘'] and volume_ratio > 2:
                signal = "卖出"
        elif strategy == "缩量下跌":
            if today['收盘'] < yesterday['收盘'] and volume_ratio < 0.5:
                signal = "观望"
        elif strategy == "地量地价":
            min_vol = df['成交量'].iloc[max(0, i-60):i].min()
            min_price = df['最低'].iloc[max(0, i-60):i].min()
            if today['成交量'] <= min_vol * 1.1 and today['收盘'] <= min_price * 1.05:
                signal = "买入"
        elif strategy == "堆量上涨":
            # 连续 3 日放量上涨
            if i >= 3:
                consecutive = True
                for j in range(3):
                    day = df.iloc[i-j]
                    prev_day = df.iloc[i-j-1]
                    vol_ratio = day['成交量'] / df['vol_ma5'].iloc[i-j-1] if df['vol_ma5'].iloc[i-j-1] != 0 else 1
                    if not (day['收盘'] > prev_day['收盘'] and vol_ratio > 1.2):
                        consecutive = False
                        break
                if consecutive:
                    signal = "买入"
        
        if signal:
            signals.append({
                "date": today['日期'] if '日期' in df.columns else i,
                "price": round(today['收盘'], 2),
                "signal": signal,
                "volume_ratio": round(volume_ratio, 2)
            })
            
            # 计算持有收益
            buy_price = today['收盘']
            sell_price = df.iloc[i + hold_days]['收盘'] if i + hold_days < len(df) else buy_price
            return_pct = (sell_price - buy_price) / buy_price * 100
            
            trades.append({
                "buy_date": today['日期'] if '日期' in df.columns else i,
                "buy_price": round(buy_price, 2),
                "sell_date": df.iloc[i + hold_days]['日期'] if '日期' in df.columns and i + hold_days < len(df) else "N/A",
                "sell_price": round(sell_price, 2),
                "return_pct": round(return_pct, 2),
                "hold_days": hold_days
            })
    
    # 计算回测统计
    if not trades:
        return {
            "strategy": strategy,
            "code": code,
            "total_trades": 0,
            "message": "无交易信号"
        }
    
    total_trades = len(trades)
    winning_trades = sum(1 for t in trades if t['return_pct'] > 0)
    win_rate = winning_trades / total_trades * 100 if total_trades > 0 else 0
    avg_return = np.mean([t['return_pct'] for t in trades])
    total_return = np.sum([t['return_pct'] for t in trades])
    max_win = max([t['return_pct'] for t in trades])
    max_loss = min([t['return_pct'] for t in trades])
    
    return {
        "strategy": strategy,
        "code": code,
        "period": f"{start_date} - {end_date}",
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": total_trades - winning_trades,
        "win_rate": round(win_rate, 2),
        "avg_return": round(avg_return, 2),
        "total_return": round(total_return, 2),
        "max_win": round(max_win, 2),
        "max_loss": round(max_loss, 2),
        "hold_days": hold_days,
        "signals_count": len(signals),
        "sample_trades": trades[:10]  # 前 10 笔交易详情
    }


if __name__ == "__main__":
    # 测试示例
    # 设置 UTF-8 编码
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 60)
    print("量价关系深度分析模块测试")
    print("=" * 60)
    
    test_code = "300308"  # 中际旭创
    print(f"\n测试股票：{test_code}")
    print("-" * 60)
    
    # 1. 综合量价分析
    print("\n【综合量价分析】")
    result = analyze_volume_price_comprehensive(test_code)
    
    if "error" not in result:
        print(f"当前价格：{result['current_price']}")
        print(f"量比：{result['volume_ratio']} ({result['volume_status']})")
        print(f"\n基础量价形态:")
        print(f"  形态：{result['basic_pattern'].get('pattern')}")
        print(f"  信号：{result['basic_pattern'].get('signal')}")
        print(f"  置信度：{result['basic_pattern'].get('confidence')}")
        
        print(f"\n量价背离：{result['divergence'].get('signal')}")
        print(f"异常量能：{result['extreme_volume'].get('signal')} (预警级别：{result['extreme_volume'].get('warning_level')})")
        print(f"堆量上涨：{result['continuous_volume'].get('signal')}")
        
        print(f"\n【综合评分】: {result['comprehensive_score']}")
        print(f"【操作建议】: {result['recommendation']} (信心级别：{result['confidence_level']})")
        
        if result['signals']:
            print(f"\n检测到的信号:")
            for sig in result['signals']:
                print(f"  - {sig}")
    
    # 2. 回测验证
    print("\n" + "=" * 60)
    print("【策略回测验证】")
    print("-" * 60)
    
    # 回测放量上涨策略
    backtest_result = backtest_volume_price_strategy(
        code=test_code,
        start_date="20250101",
        end_date="20260313",
        strategy="放量上涨",
        hold_days=5
    )
    
    if "error" not in backtest_result:
        print(f"\n策略：{backtest_result.get('strategy')}")
        print(f"回测区间：{backtest_result.get('period')}")
        print(f"总交易次数：{backtest_result.get('total_trades')}")
        print(f"胜率：{backtest_result.get('win_rate')}%")
        print(f"平均收益：{backtest_result.get('avg_return')}%")
        print(f"总收益：{backtest_result.get('total_return')}%")
        print(f"最大单笔盈利：{backtest_result.get('max_win')}%")
        print(f"最大单笔亏损：{backtest_result.get('max_loss')}%")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)
