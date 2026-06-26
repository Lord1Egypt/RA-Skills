#!/usr/bin/env python3
"""
SAR（抛物线转向指标）计算工具
数据来源：Baostock
"""

import baostock as bs
import pandas as pd
import numpy as np
import argparse
import sys
from datetime import datetime, timedelta


def login_baostock():
    """登录Baostock"""
    lg = bs.login()
    if lg.error_code != '0':
        print(f"Baostock登录失败: {lg.error_msg}")
        return False
    return True


def logout_baostock():
    """登出Baostock"""
    bs.logout()


def get_stock_kline(stock_code, start_date=None, end_date=None, adjustflag="1"):
    """
    获取股票K线数据
    
    Args:
        stock_code: 股票代码，如 '600519'
        start_date: 开始日期，格式 'YYYY-MM-DD'
        end_date: 结束日期，格式 'YYYY-MM-DD'
        adjustflag: 复权类型 1-前复权 2-后复权 3-不复权
        
    Returns:
        DataFrame: 包含日期、开盘、收盘、最高、最低、成交量数据
    """
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d')
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    # 转换股票代码格式
    if stock_code.startswith('6'):
        bs_code = f"sh.{stock_code}"
    elif stock_code.startswith(('0', '3')):
        bs_code = f"sz.{stock_code}"
    else:
        bs_code = stock_code
    
    rs = bs.query_history_k_data_plus(
        bs_code,
        "date,open,high,low,close,volume,amount,turn",
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag=adjustflag
    )
    
    if rs.error_code != '0':
        print(f"获取数据失败: {rs.error_msg}")
        return None
    
    data_list = []
    while rs.next():
        data_list.append(rs.get_row_data())
    
    df = pd.DataFrame(data_list, columns=rs.fields)
    
    # 转换数据类型
    df['open'] = pd.to_numeric(df['open'], errors='coerce')
    df['high'] = pd.to_numeric(df['high'], errors='coerce')
    df['low'] = pd.to_numeric(df['low'], errors='coerce')
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['turn'] = pd.to_numeric(df['turn'], errors='coerce')
    
    return df


def calculate_sar(df, af_init=0.02, af_max=0.2):
    """
    计算SAR值（抛物线转向指标）
    
    Args:
        df: 包含high, low列的DataFrame
        af_init: 初始加速因子，默认0.02
        af_max: 最大加速因子，默认0.2
        
    Returns:
        DataFrame: 添加了sar列的DataFrame
    """
    df = df.copy()
    n = len(df)
    
    if n < 2:
        df['sar'] = df['close']
        df['trend'] = 0
        df['af'] = af_init
        return df
    
    # 初始化SAR数组
    sar = np.full(n, np.nan)
    trend = np.full(n, 0)  # 1: 上涨, -1: 下跌
    af = np.full(n, af_init)
    ep_arr = np.full(n, np.nan)  # 极值点数组，每行独立记录
    
    # 确定初始趋势（看前两天的走势）
    if df['close'].iloc[1] >= df['close'].iloc[0]:
        trend[0] = 1
        ep = df['high'].iloc[0]  # 极值点：上涨时用最高价
        sar[0] = df['low'].iloc[0]  # 初始SAR：第一天的最低价
    else:
        trend[0] = -1
        ep = df['low'].iloc[0]  # 极值点：下跌时用最低价
        sar[0] = df['high'].iloc[0]  # 初始SAR：第一天的最高价
    
    ep_arr[0] = ep  # 记录初始极值点
    
    # 逐日计算SAR
    for i in range(1, n):
        prev_sar = sar[i-1]
        prev_trend = trend[i-1]
        prev_af = af[i-1]
        
        # 计算当前SAR
        current_sar = prev_sar + prev_af * (ep - prev_sar)
        
        # 获取前一天的极值点
        if prev_trend == 1:  # 上涨趋势
            prev_ep = df['high'].iloc[i-1]
        else:  # 下跌趋势
            prev_ep = df['low'].iloc[i-1]
        
        # 判断是否触发转向（使用收盘价判断）
        if prev_trend == 1:  # 上涨趋势
            # 检查是否跌破SAR（收盘价跌破SAR）
            if df['close'].iloc[i] < current_sar:
                # 转向：下跌
                trend[i] = -1
                sar[i] = prev_ep  # SAR设为前一天的极值点
                ep = df['low'].iloc[i]  # 更新极值点
                ep_arr[i] = ep  # 记录当前极值点
                af[i] = af_init  # 重置加速因子
            else:
                # 继续上涨
                trend[i] = 1
                sar[i] = current_sar
                # 更新极值点和加速因子
                if df['high'].iloc[i] > ep:
                    ep = df['high'].iloc[i]
                    ep_arr[i] = ep  # 记录更新后的极值点
                    af[i] = min(prev_af + af_init, af_max)
                else:
                    af[i] = prev_af
                    ep_arr[i] = ep  # 保持极值点
        else:  # 下跌趋势
            # 检查是否涨破SAR（收盘价涨破SAR）
            if df['close'].iloc[i] > current_sar:
                # 转向：上涨
                trend[i] = 1
                sar[i] = prev_ep
                ep = df['high'].iloc[i]
                ep_arr[i] = ep  # 记录当前极值点
                af[i] = af_init
            else:
                # 继续下跌
                trend[i] = -1
                sar[i] = current_sar
                if df['low'].iloc[i] < ep:
                    ep = df['low'].iloc[i]
                    ep_arr[i] = ep  # 记录更新后的极值点
                    af[i] = min(prev_af + af_init, af_max)
                else:
                    af[i] = prev_af
                    ep_arr[i] = ep  # 保持极值点
    
    df['sar'] = sar
    df['trend'] = trend
    df['af'] = af
    df['ep'] = ep_arr  # 使用极值点数组
    
    return df


def calculate_volume_ratio(df, period=5):
    """
    计算成交量比（今日成交量 / 5日均量）
    
    Args:
        df: 包含volume列的DataFrame
        period: 移动平均周期，默认5天
        
    Returns:
        DataFrame: 添加了volume_ma和volume_ratio列
    """
    df = df.copy()
    df['volume_ma'] = df['volume'].rolling(window=period).mean()
    df['volume_ratio'] = df['volume'] / df['volume_ma']
    return df


def analyze_sar(stock_code, df):
    """
    分析SAR指标，返回分析结果
    
    Args:
        stock_code: 股票代码
        df: 包含SAR计算结果的DataFrame
        
    Returns:
        dict: 分析结果
    """
    if df is None or len(df) < 2:
        return None
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    # 基本信息
    close = latest['close']
    sar = latest['sar']
    trend = latest['trend']
    volume = latest['volume']
    volume_ratio = latest['volume_ratio']
    
    # 判断价格与SAR位置
    price_above_sar = close > sar
    
    # 判断趋势变化
    trend_changed = trend != prev['trend']
    trend_str = "上涨" if trend == 1 else "下跌"
    
    # 计算四维评分
    scores = calculate_four_dimension_score(df)
    
    result = {
        'stock_code': stock_code,
        'date': latest['date'],
        'close': close,
        'sar': sar,
        'trend': trend_str,
        'trend_changed': trend_changed,
        'price_above_sar': price_above_sar,
        'volume': volume,
        'volume_ratio': volume_ratio,
        'scores': scores
    }
    
    return result


def calculate_four_dimension_score(df):
    """
    计算四维评分
    
    维度1: 趋势评分（SAR趋势方向）
    维度2: 位置评分（价格相对SAR位置）
    维度3: 成交量评分（成交量比）
    维度4: 动量评分（近期涨幅）
    
    Returns:
        dict: 各维度评分和总分
    """
    latest = df.iloc[-1]
    
    # 维度1: 趋势评分 (0-25分)
    trend_score = 25 if latest['trend'] == 1 else 0
    
    # 维度2: 位置评分 (0-25分)
    if latest['close'] > latest['sar']:
        position_score = 25
    else:
        position_score = 0
    
    # 维度3: 成交量评分 (0-25分)
    vol_ratio = latest['volume_ratio'] if pd.notna(latest['volume_ratio']) else 1
    if vol_ratio >= 1.5:
        volume_score = 25
    elif vol_ratio >= 1.2:
        volume_score = 18
    elif vol_ratio >= 1.0:
        volume_score = 12
    elif vol_ratio >= 0.8:
        volume_score = 6
    else:
        volume_score = 0
    
    # 维度4: 动量评分 (0-25分)
    if len(df) >= 5:
        change_5d = (latest['close'] - df['close'].iloc[-5]) / df['close'].iloc[-5] * 100
        if change_5d >= 10:
            momentum_score = 25
        elif change_5d >= 5:
            momentum_score = 20
        elif change_5d >= 0:
            momentum_score = 15
        elif change_5d >= -5:
            momentum_score = 8
        else:
            momentum_score = 0
    else:
        momentum_score = 12.5
    
    total_score = trend_score + position_score + volume_score + momentum_score
    
    return {
        'trend_score': trend_score,      # 趋势评分 (0-25)
        'position_score': position_score,  # 位置评分 (0-25)
        'volume_score': volume_score,      # 成交量评分 (0-25)
        'momentum_score': momentum_score,  # 动量评分 (0-25)
        'total_score': total_score         # 总分 (0-100)
    }


def print_result(result, quiet=False):
    """打印分析结果"""
    if result is None:
        print("分析失败")
        return
    
    scores = result['scores']
    
    if quiet:
        # 简短输出
        print(f"{result['stock_code']}: 收盘={result['close']:.2f} SAR={result['sar']:.2f} "
              f"趋势={result['trend']} 位置={'高于' if result['price_above_sar'] else '低于'} "
              f"量比={result['volume_ratio']:.2f} 评分={scores['total_score']}")
    else:
        # 完整输出
        print(f"\n{'='*60}")
        print(f"股票代码: {result['stock_code']}")
        print(f"分析日期: {result['date']}")
        print(f"{'='*60}")
        print(f"收盘价: {result['close']:.2f}")
        print(f"SAR值:   {result['sar']:.2f}")
        print(f"趋势:    {result['trend']} {'⚡ 转向' if result['trend_changed'] else ''}")
        print(f"价格位置: {'✅ 价格在SAR上方' if result['price_above_sar'] else '🔻 价格在SAR下方'}")
        print(f"成交量:   {result['volume']:,.0f}")
        print(f"成交量比: {result['volume_ratio']:.2f}")
        print(f"\n{'='*60}")
        print(f"四维评分:")
        print(f"  趋势评分:   {scores['trend_score']:>2}/25  {'⬆️ 上涨' if scores['trend_score'] > 0 else '⬇️ 下跌'}")
        print(f"  位置评分:   {scores['position_score']:>2}/25  {'✅ 强势' if scores['position_score'] > 0 else '❌ 弱势'}")
        print(f"  成交量评分: {scores['volume_score']:>2}/25  {'🔥 放量' if scores['volume_score'] >= 18 else '📉 缩量'}")
        print(f"  动量评分:   {scores['momentum_score']:>2}/25  {'💪 强劲' if scores['momentum_score'] >= 15 else '⚠️ 疲软'}")
        print(f"  ─────────────────")
        print(f"  总分:       {scores['total_score']:>2}/100")
        
        # 综合建议
        if scores['total_score'] >= 75:
            print(f"\n📈 综合建议: 强烈看多")
        elif scores['total_score'] >= 50:
            print(f"\n📊 综合建议: 谨慎看多")
        elif scores['total_score'] >= 25:
            print(f"\n📉 综合建议: 谨慎看空")
        else:
            print(f"\n🔻 综合建议: 强烈看空")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='SAR指标计算工具')
    parser.add_argument('--stock', '-s', nargs='+', required=True, help='股票代码')
    parser.add_argument('--start', default=None, help='开始日期 YYYY-MM-DD')
    parser.add_argument('--end', default=None, help='结束日期 YYYY-MM-DD')
    parser.add_argument('--quiet', '-q', action='store_true', help='简短输出')
    parser.add_argument('--af-init', type=float, default=0.02, help='初始加速因子')
    parser.add_argument('--af-max', type=float, default=0.2, help='最大加速因子')
    
    args = parser.parse_args()
    
    # 登录Baostock
    if not login_baostock():
        sys.exit(1)
    
    try:
        for stock_code in args.stock:
            # 获取K线数据
            df = get_stock_kline(stock_code, args.start, args.end)
            
            if df is None or len(df) < 2:
                print(f"股票 {stock_code}: 数据获取失败或数据不足")
                continue
            
            # 计算SAR
            df = calculate_sar(df, args.af_init, args.af_max)
            
            # 计算成交量比
            df = calculate_volume_ratio(df)
            
            # 分析SAR
            result = analyze_sar(stock_code, df)
            
            # 打印结果
            print_result(result, args.quiet)
    
    finally:
        logout_baostock()


if __name__ == '__main__':
    main()
