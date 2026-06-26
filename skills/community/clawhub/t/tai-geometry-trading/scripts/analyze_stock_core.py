#!/usr/bin/env python3
"""
太几何交易 - 核心版分析脚本
只包含核心因子，无需大模型API
"""

import pandas as pd
import numpy as np
import requests
import json
import os
import sys

sys.path.append('/root/.openclaw/workspace/skills/tai-geometry-trading/scripts')

import config
from kline_geometry import analyze_geometry_structure
from macd_wind_tunnel import analyze_multi_period_macd
from volume_shrinkage import analyze_multi_period_shrinkage


def get_stock_data_tengxun(code, days=320):
    """使用腾讯API获取股票K线数据"""
    # 判断市场
    if code.startswith('6'):
        market = 'sh' + code
    else:
        market = 'sz' + code
    
    url = 'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get'
    params = {'_var': 'kline_dayqfq', 'param': f'{market},day,,,{days},qfq'}
    
    try:
        r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        data = json.loads(r.text.split('=')[1])
        klines = data['data'][market]['qfqday']
        
        # 过滤异常行
        clean_klines = [k for k in klines if len(k) == 6]
        
        df = pd.DataFrame(clean_klines, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        for c in ['open', 'high', 'low', 'close', 'volume']:
            df[c] = pd.to_numeric(df[c], errors='coerce')
        df = df.sort_values('date').reset_index(drop=True)
        
        return df
    except Exception as e:
        print(f"腾讯API获取失败: {e}")
        return None


def get_stock_data_akshare(stock_code):
    """使用AkShare获取股票数据 (备用)"""
    import akshare as ak
    
    if stock_code.startswith('6'):
        symbol = f"sh{stock_code}"
    else:
        symbol = f"sz{stock_code}"
    
    try:
        # 尝试使用新接口
        df = ak.stock_zh_a_hist(symbol=symbol, start_date='20240101', adjust='qfq')
        
        if df is not None and not df.empty:
            # 重命名列
            df = df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'volume',
                '成交额': 'amount',
                '振幅': 'amplitude',
                '涨跌幅': 'pct_change',
                '涨跌额': 'change',
                '换手率': 'turnover'
            })
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        else:
            return None
    except Exception as e:
        print(f"AkShare获取失败: {e}")
        return None
    
    return df


def get_stock_data_tushare(stock_code):
    """使用Tushare获取股票数据"""
    import tushare as ts
    
    ts.set_token(config.TUSHARE_TOKEN)
    pro = ts.pro_api()
    
    if stock_code.startswith('6'):
        ts_code = f"{stock_code}.SH"
    else:
        ts_code = f"{stock_code}.SZ"
    
    try:
        df = pro.daily(ts_code=ts_code, start_date='20240101', end_date='20261231')
        df = df.sort_values('trade_date')
        df = df.rename(columns={
            'trade_date': 'date',
            'vol': 'volume'
        })
        df['date'] = pd.to_datetime(df['date']).astype(str)
        return df
    except Exception as e:
        print(f"Tushare获取失败: {e}")
        return None


def get_stock_data(stock_code):
    """根据配置获取股票数据"""
    source = config.get_data_source()
    print(f"数据源: {source}")
    
    df_daily = None
    
    if source == "tushare":
        df_daily = get_stock_data_tushare(stock_code)
    elif source == "akshare":
        # 优先用腾讯API (更稳定)
        df_daily = get_stock_data_tengxun(stock_code)
        if df_daily is None:
            # 备用akshare
            df_daily = get_stock_data_akshare(stock_code)
    
    if df_daily is None or df_daily.empty:
        print("❌ 所有数据源均获取失败")
        return None
    
    # 生成各周期数据
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    
    # 周线
    df_weekly = df_daily.set_index('date').resample('W-FRI').agg({
        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
    }).dropna().reset_index()
    
    # 月线
    df_monthly = df_daily.set_index('date').resample('ME').agg({
        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
    }).dropna().reset_index()
    
    # 2日线
    df_2daily = df_daily.set_index('date').resample('2D').agg({
        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
    }).dropna().reset_index()
    
    # 8日线
    df_8daily = df_daily.set_index('date').resample('8D').agg({
        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
    }).dropna().reset_index()
    
    # 转换日期
    for df_obj in [df_daily, df_weekly, df_monthly, df_2daily, df_8daily]:
        df_obj['date'] = df_obj['date'].astype(str)
    
    return {
        'daily': df_daily,
        'weekly': df_weekly,
        'monthly': df_monthly,
        '2daily': df_2daily,
        '8daily': df_8daily
    }


def analyze_stock_core(stock_code):
    """核心版分析 - 只使用核心因子"""
    print("=" * 60)
    print("  太几何交易 - 核心版")
    print("  (无需大模型API，仅核心因子)")
    print("=" * 60)
    
    # 检查配置
    if config.get_data_source() == "tushare" and not config.TUSHARE_TOKEN:
        print("❌ 请先在 config.py 中配置 TUSHARE_TOKEN")
        return
    
    print()
    
    # 获取数据
    data_dict = get_stock_data(stock_code)
    
    if not data_dict:
        print("❌ 数据获取失败")
        return
    
    daily = data_dict['daily']
    
    if daily.empty:
        print("❌ 无数据")
        return
    
    latest = daily.iloc[-1]
    
    # 获取股票名称 (使用akshare)
    try:
        import akshare as ak
        info = ak.stock_individual_info_em(symbol=stock_code)
        stock_name = info[info['item'] == '股票简称']['value'].values[0]
    except:
        stock_name = "未知"
    
    print(f"\n{'='*55}")
    print(f"  {stock_name} ({stock_code}) 股票分析")
    print(f"{'='*55}")
    print(f"最新价格: {latest['close']}元")
    
    # 核心因子分析
    print(f"\n【核心因子分析】")
    
    # 1. 几何结构
    geometry = analyze_geometry_structure(data_dict['daily'])
    geo_score = geometry['total_score']
    geo_desc = geometry.get('description', ['无描述'])
    print(f"  几何结构: {geo_score}/25 - {geo_desc[0] if geo_desc else '无'}")
    
    # 2. MACD风洞
    macd = analyze_multi_period_macd(data_dict)
    macd_score = macd['resonance_score']
    macd_dir = macd.get('resonance_type', 'neutral')
    macd_desc = macd.get('description', ['无描述'])
    print(f"  MACD风洞: {macd_score}/30 ({'看涨' if macd_dir=='bullish' else ('看跌' if macd_dir=='bearish' else '中性')})")
    print(f"  MACD详情:")
    for p in ['monthly', 'weekly', 'daily']:
        if p in macd:
            r = macd[p]
            direction = r.get('direction', '-')
            desc = r.get('description', [])
            desc_str = desc[0] if desc else '无'
            print(f"    {p}: {direction} - {desc_str}")
    
    # 3. 缩量短线
    shrink = analyze_multi_period_shrinkage(data_dict)
    shrink_score = shrink['total_score']
    shrink_desc = shrink.get('description', ['无描述'])
    print(f"  缩量短线: {shrink_score}/15 - {shrink_desc[0] if isinstance(shrink_desc, list) and shrink_desc else '无'}")
    
    # 计算总分 (核心因子70分制)
    core_score = geo_score + macd_score + shrink_score
    
    # 根据MACD方向调整
    if macd_dir == 'bearish':
        adjusted_macd = -abs(macd_score)
        tech_score = (geo_score + adjusted_macd + shrink_score) * 0.6
        total = max(0, tech_score)
    elif macd_dir == 'bullish':
        total = geo_score + macd_score + shrink_score
    else:
        total = geo_score + macd_score + shrink_score
    
    # 判断建议 (核心版70分制)
    # 70分以上制: 52.5以上=强烈看涨(75%), 35以上=看涨(50%), 17.5以上=中性(25%)
    if total >= 52.5:
        recommendation = "强烈看涨"
        emoji = "🚀"
    elif total >= 35:
        recommendation = "看涨"
        emoji = "📈"
    elif total >= 17.5:
        recommendation = "中性"
        emoji = "➡️"
    else:
        recommendation = "看跌"
        emoji = "📉"
    
    print(f"\n{'='*55}")
    print(f"【核心评分】{int(total)}/70分")
    print(f"【技术判断】{emoji} {recommendation}")
    print(f"{'='*55}")
    print(f"\n→ 如需完整AI分析(基本面+情绪+预测)，")
    print(f"  请在 config.py 中配置 MINIMAX_API_KEY")
    print(f"  然后运行: python analyze_stock.py {stock_code}")


if __name__ == '__main__':
    import sys
    code = sys.argv[1] if len(sys.argv) > 1 else '002378'
    analyze_stock_core(code)