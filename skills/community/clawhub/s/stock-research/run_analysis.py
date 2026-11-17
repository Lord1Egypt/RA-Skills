#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
沪深300投研分析脚本
获取真实市场数据，计算技术指标，多因子评分，输出TOP 10潜力个股
"""

import akshare as ak
import pandas as pd
import numpy as np
import json
import time
import traceback
from datetime import datetime, timedelta

print("=" * 60)
print("沪深300投研分析脚本")
print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# ============================================================
# 1. 获取沪深300成分股列表
# ============================================================
print("\n[1/6] 获取沪深300成分股列表...")
try:
    cons_df = ak.index_stock_cons_csindex(symbol="000300")
    stock_list = cons_df[['成分券代码', '成分券名称']].copy()
    stock_list.columns = ['code', 'name']
    # 确保代码是6位字符串
    stock_list['code'] = stock_list['code'].astype(str).str.zfill(6)
    print(f"  获取到 {len(stock_list)} 只成分股")
except Exception as e:
    print(f"  获取成分股列表失败: {e}")
    traceback.print_exc()
    stock_list = pd.DataFrame(columns=['code', 'name'])

# ============================================================
# 2. 获取沪深300指数K线数据（判断大盘环境）
# ============================================================
print("\n[2/6] 获取沪深300指数K线数据...")
index_data = None
try:
    index_data = ak.stock_zh_index_daily(symbol="sh000300")
    if index_data is not None and len(index_data) > 0:
        index_data = index_data.tail(60).copy()
        index_data.columns = [c.lower() for c in index_data.columns]
        print(f"  获取到沪深300指数 {len(index_data)} 条K线数据")
        print(f"  最新日期: {index_data['date'].iloc[-1] if 'date' in index_data.columns else 'N/A'}")
    else:
        print("  沪深300指数数据为空，尝试备选接口...")
        index_data = ak.index_zh_a_hist(symbol="000300", period="daily", start_date="20260601", end_date="20260801")
        if index_data is not None and len(index_data) > 0:
            index_data = index_data.tail(60).copy()
            print(f"  备选接口获取到 {len(index_data)} 条数据")
except Exception as e:
    print(f"  获取沪深300指数数据失败: {e}")
    try:
        print("  尝试备选接口...")
        index_data = ak.index_zh_a_hist(symbol="000300", period="daily", start_date="20260601", end_date="20260801")
        if index_data is not None and len(index_data) > 0:
            index_data = index_data.tail(60).copy()
            print(f"  备选接口获取到 {len(index_data)} 条数据")
    except Exception as e2:
        print(f"  备选接口也失败: {e2}")

# ============================================================
# 技术指标计算函数
# ============================================================
def calc_macd(close, fast=12, slow=26, signal=9):
    """计算MACD"""
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd_bar = 2 * (dif - dea)
    return dif, dea, macd_bar

def calc_kdj(high, low, close, n=9, m1=3, m2=3):
    """计算KDJ"""
    lowest_low = low.rolling(window=n, min_periods=1).min()
    highest_high = high.rolling(window=n, min_periods=1).max()
    rsv = (close - lowest_low) / (highest_high - lowest_low + 1e-10) * 100
    k = rsv.ewm(com=m1-1, adjust=False).mean()
    d = k.ewm(com=m2-1, adjust=False).mean()
    j = 3 * k - 2 * d
    return k, d, j

def check_golden_cross(series1, series2):
    """检查最近一次是否为金叉（series1上穿series2）"""
    if len(series1) < 2:
        return False
    return series1.iloc[-1] > series2.iloc[-1] and series1.iloc[-2] <= series2.iloc[-2]

def check_ma_bullish(close):
    """检查均线多头排列（5>10>20>60）"""
    if len(close) < 60:
        return False
    ma5 = close.iloc[-5:].mean()
    ma10 = close.iloc[-10:].mean()
    ma20 = close.iloc[-20:].mean()
    ma60 = close.mean()
    return ma5 > ma10 > ma20 > ma60

# ============================================================
# 3. 获取成分股K线数据并计算技术指标
# ============================================================
print("\n[3/6] 获取成分股K线数据并计算技术指标...")

stock_results = []
macd_golden_count = 0
kdj_golden_count = 0
ma_bullish_count = 0
total_stocks = len(stock_list)

# 分批处理
batch_size = 50
for batch_idx in range(0, total_stocks, batch_size):
    batch = stock_list.iloc[batch_idx:batch_idx + batch_size]
    if batch_idx > 0:
        print(f"  批次 {batch_idx // batch_size + 1}: 等待1秒...")
        time.sleep(1)
    
    for idx, row in batch.iterrows():
        code = row['code']
        name = row['name']
        
        try:
            # 确定市场
            if code.startswith('6'):
                market = "sh"
            else:
                market = "sz"
            
            # 获取日K线数据
            kline_df = None
            retry = 0
            while retry < 2:
                try:
                    kline_df = ak.stock_zh_a_hist(symbol=code, period="daily", 
                                                   start_date="20260501", end_date="20260801",
                                                   adjust="qfq")
                    break
                except Exception as e:
                    retry += 1
                    if retry < 2:
                        time.sleep(0.5)
                    else:
                        raise e
            
            if kline_df is None or len(kline_df) < 20:
                continue
            
            kline_df = kline_df.tail(60).copy()
            
            # 标准化列名
            col_map = {}
            for c in kline_df.columns:
                cl = str(c).lower()
                if '日期' in cl or 'date' in cl:
                    col_map[c] = 'date'
                elif '收盘' in cl or 'close' in cl:
                    col_map[c] = 'close'
                elif '开盘' in cl or 'open' in cl:
                    col_map[c] = 'open'
                elif '最高' in cl or 'high' in cl:
                    col_map[c] = 'high'
                elif '最低' in cl or 'low' in cl:
                    col_map[c] = 'low'
                elif '成交量' in cl or 'volume' in cl or 'vol' in cl:
                    col_map[c] = 'volume'
                elif '换手率' in cl or 'turnover' in cl:
                    col_map[c] = 'turnover'
                elif '涨跌幅' in cl:
                    col_map[c] = 'pct_chg'
            
            kline_df = kline_df.rename(columns=col_map)
            
            if 'close' not in kline_df.columns:
                continue
            
            close = kline_df['close'].astype(float)
            high = kline_df['high'].astype(float) if 'high' in kline_df.columns else close
            low = kline_df['low'].astype(float) if 'low' in kline_df.columns else close
            volume = kline_df['volume'].astype(float) if 'volume' in kline_df.columns else pd.Series([0]*len(close))
            
            # 计算MACD
            dif, dea, macd_bar = calc_macd(close)
            macd_golden = check_golden_cross(dif, dea)
            
            # 计算KDJ
            k, d, j = calc_kdj(high, low, close)
            kdj_golden = check_golden_cross(k, d)
            
            # 均线多头排列
            ma_bullish = check_ma_bullish(close)
            
            # 动量指标（近20日涨幅）
            momentum_20 = (close.iloc[-1] / close.iloc[-20] - 1) * 100 if len(close) >= 20 else 0
            
            # 近5日涨幅
            momentum_5 = (close.iloc[-1] / close.iloc[-5] - 1) * 100 if len(close) >= 5 else 0
            
            # 波动率（20日标准差）
            volatility = close.pct_change().tail(20).std() * np.sqrt(252) * 100 if len(close) >= 20 else 0
            
            # 量比（5日均量/20日均量）
            vol_ratio = 1.0
            if 'volume' in kline_df.columns and len(volume) >= 20:
                vol_5 = volume.tail(5).mean()
                vol_20 = volume.tail(20).mean()
                if vol_20 > 0:
                    vol_ratio = vol_5 / vol_20
            
            # 换手率
            avg_turnover = 0
            if 'turnover' in kline_df.columns:
                avg_turnover = kline_df['turnover'].astype(float).tail(20).mean()
            
            # 统计
            if macd_golden:
                macd_golden_count += 1
            if kdj_golden:
                kdj_golden_count += 1
            if ma_bullish:
                ma_bullish_count += 1
            
            # MACD趋势得分（DIF>0且上升为正趋势）
            macd_score = 50
            if dif.iloc[-1] > 0:
                macd_score += 25
            if dif.iloc[-1] > dif.iloc[-2]:
                macd_score += 25
            
            # 趋势得分（价格在均线上方）
            trend_score = 50
            ma5 = close.tail(5).mean()
            ma10 = close.tail(10).mean()
            ma20 = close.tail(20).mean()
            if close.iloc[-1] > ma5:
                trend_score += 15
            if close.iloc[-1] > ma10:
                trend_score += 15
            if close.iloc[-1] > ma20:
                trend_score += 20
            
            stock_results.append({
                'code': code,
                'name': name,
                'market': market,
                'close': float(close.iloc[-1]),
                'momentum_5': float(momentum_5),
                'momentum_20': float(momentum_20),
                'volatility': float(volatility),
                'vol_ratio': float(vol_ratio),
                'avg_turnover': float(avg_turnover),
                'macd_golden': macd_golden,
                'kdj_golden': kdj_golden,
                'ma_bullish': ma_bullish,
                'macd_score': float(macd_score),
                'trend_score': float(trend_score),
                'dif': float(dif.iloc[-1]),
                'dea': float(dea.iloc[-1]),
                'k': float(k.iloc[-1]),
                'd': float(d.iloc[-1]),
                'j': float(j.iloc[-1]),
            })
            
        except Exception as e:
            # 单只失败不影响整体
            continue
    
    processed = min(batch_idx + batch_size, total_stocks)
    print(f"  已处理 {processed}/{total_stocks} 只股票, 成功获取 {len(stock_results)} 只")

print(f"\n  技术指标统计:")
print(f"    MACD金叉: {macd_golden_count} 只")
print(f"    KDJ金叉: {kdj_golden_count} 只")
print(f"    均线多头排列: {ma_bullish_count} 只")

# ============================================================
# 4. 获取估值数据（PE/PB）
# ============================================================
print("\n[4/6] 获取估值数据...")

# 使用实时行情获取PE/PB数据
valuation_data = {}
try:
    spot_df = ak.stock_zh_a_spot_em()
    if spot_df is not None and len(spot_df) > 0:
        print(f"  获取到 {len(spot_df)} 只A股实时行情")
        # 标准化列名
        col_map2 = {}
        for c in spot_df.columns:
            cl = str(c)
            if '代码' in cl:
                col_map2[c] = 'code'
            elif '名称' in cl:
                col_map2[c] = 'name'
            elif cl == '最新价':
                col_map2[c] = 'price'
            elif '市盈率' in cl and '动' in cl:
                col_map2[c] = 'pe'
            elif '市净率' in cl:
                col_map2[c] = 'pb'
            elif '涨跌幅' in cl:
                col_map2[c] = 'pct_chg'
            elif '换手率' in cl:
                col_map2[c] = 'turnover'
            elif '成交量' in cl:
                col_map2[c] = 'volume'
            elif '成交额' in cl:
                col_map2[c] = 'amount'
            elif '总市值' in cl:
                col_map2[c] = 'total_mv'
            elif '流通市值' in cl:
                col_map2[c] = 'circ_mv'
            elif '60日涨跌幅' in cl:
                col_map2[c] = 'pct_60d'
        
        spot_df = spot_df.rename(columns=col_map2)
        
        for _, row in spot_df.iterrows():
            code = str(row.get('code', '')).zfill(6)
            valuation_data[code] = {
                'price': row.get('price', None),
                'pe': row.get('pe', None),
                'pb': row.get('pb', None),
                'pct_chg': row.get('pct_chg', None),
                'turnover': row.get('turnover', None),
                'volume': row.get('volume', None),
                'amount': row.get('amount', None),
                'total_mv': row.get('total_mv', None),
                'pct_60d': row.get('pct_60d', None),
            }
        print(f"  估值数据覆盖 {len(valuation_data)} 只股票")
except Exception as e:
    print(f"  获取估值数据失败: {e}")
    traceback.print_exc()

# 合并估值数据到stock_results
for stock in stock_results:
    code = stock['code']
    if code in valuation_data:
        vd = valuation_data[code]
        stock['pe'] = vd.get('pe', None)
        stock['pb'] = vd.get('pb', None)
        stock['pct_chg'] = vd.get('pct_chg', None)
        stock['total_mv'] = vd.get('total_mv', None)
        stock['amount'] = vd.get('amount', None)
        if vd.get('pct_60d') is not None:
            stock['momentum_60d'] = vd.get('pct_60d')
    else:
        stock['pe'] = None
        stock['pb'] = None

# ============================================================
# 5. 判断市场环境
# ============================================================
print("\n[5/6] 判断市场环境...")

market_env = {
    'type': '震荡市',
    'position': 50,
    'reasons': []
}

if index_data is not None and len(index_data) > 0:
    try:
        # 确保有close列
        if 'close' not in index_data.columns:
            for c in index_data.columns:
                if '收盘' in str(c) or 'close' in str(c).lower():
                    index_data = index_data.rename(columns={c: 'close'})
                    break
        
        if 'close' in index_data.columns:
            idx_close = index_data['close'].astype(float)
            idx_ma20 = idx_close.tail(20).mean()
            idx_latest = idx_close.iloc[-1]
            
            if idx_latest > idx_ma20:
                market_env['reasons'].append(f"沪深300指数({idx_latest:.2f})在20日均线({idx_ma20:.2f})上方，偏多")
                market_env['type'] = '偏多'
            else:
                market_env['reasons'].append(f"沪深300指数({idx_latest:.2f})在20日均线({idx_ma20:.2f})下方，偏空")
                market_env['type'] = '偏空'
    except Exception as e:
        print(f"  判断指数位置失败: {e}")

# MACD金叉数量判断
if macd_golden_count > 150:
    market_env['type'] = '牛市'
    market_env['position'] = 80
    market_env['reasons'].append(f"MACD金叉数({macd_golden_count})>150，牛市信号")
elif macd_golden_count < 100:
    market_env['type'] = '熊市'
    market_env['position'] = 30
    market_env['reasons'].append(f"MACD金叉数({macd_golden_count})<100，熊市信号")
else:
    if market_env['type'] in ['偏多']:
        market_env['position'] = 65
    elif market_env['type'] in ['偏空']:
        market_env['position'] = 35
    else:
        market_env['position'] = 50
    market_env['reasons'].append(f"MACD金叉数({macd_golden_count})在100-150之间，震荡市")

print(f"  市场环境判断: {market_env['type']}")
print(f"  建议仓位: {market_env['position']}%")
for r in market_env['reasons']:
    print(f"    - {r}")

# ============================================================
# 6. 多因子评分
# ============================================================
print("\n[6/6] 多因子评分...")

# 收集有效PE/PB数据用于排名
valid_pe = [s['pe'] for s in stock_results if s.get('pe') is not None and isinstance(s.get('pe'), (int, float)) and s['pe'] > 0]
valid_pb = [s['pb'] for s in stock_results if s.get('pb') is not None and isinstance(s.get('pb'), (int, float)) and s['pb'] > 0]

if valid_pe:
    pe_median = np.median(valid_pe)
    pe_25 = np.percentile(valid_pe, 25)
    pe_75 = np.percentile(valid_pe, 75)
else:
    pe_median = 30
    pe_25 = 15
    pe_75 = 50

if valid_pb:
    pb_median = np.median(valid_pb)
    pb_25 = np.percentile(valid_pb, 25)
    pb_75 = np.percentile(valid_pb, 75)
else:
    pb_median = 3
    pb_25 = 1.5
    pb_75 = 5

for stock in stock_results:
    scores = {}
    
    # 1. 估值因子 (15%) - PE越低越好（合理范围内）
    pe = stock.get('pe')
    if pe is not None and isinstance(pe, (int, float)) and pe > 0:
        if pe < pe_25:
            scores['valuation'] = 90
        elif pe < pe_median:
            scores['valuation'] = 70
        elif pe < pe_75:
            scores['valuation'] = 50
        elif pe < 200:
            scores['valuation'] = 30
        else:
            scores['valuation'] = 10
    else:
        scores['valuation'] = 40  # 无数据给中间分
    
    # 2. 质量因子 (15%) - ROE（这里用PB/PE近似）
    pb = stock.get('pb')
    if pe and pb and pe > 0 and pb > 0:
        approx_roe = pb / pe * 100  # ROE ≈ PB/PE
        stock['approx_roe'] = approx_roe
        if approx_roe > 20:
            scores['quality'] = 90
        elif approx_roe > 15:
            scores['quality'] = 75
        elif approx_roe > 10:
            scores['quality'] = 60
        elif approx_roe > 5:
            scores['quality'] = 45
        else:
            scores['quality'] = 30
    else:
        scores['quality'] = 40
        stock['approx_roe'] = None
    
    # 3. 成长因子 (15%) - 动量
    m20 = stock.get('momentum_20', 0)
    m60 = stock.get('momentum_60d', 0)
    growth_score = 50
    if m20 > 10:
        growth_score += 25
    elif m20 > 5:
        growth_score += 15
    elif m20 > 0:
        growth_score += 5
    elif m20 < -10:
        growth_score -= 25
    elif m20 < -5:
        growth_score -= 15
    
    if m60 and isinstance(m60, (int, float)):
        if m60 > 20:
            growth_score += 25
        elif m60 > 10:
            growth_score += 15
        elif m60 > 0:
            growth_score += 5
    
    scores['growth'] = max(0, min(100, growth_score))
    
    # 4. 动量因子 (10%)
    m5 = stock.get('momentum_5', 0)
    if m5 > 5:
        scores['momentum'] = 85
    elif m5 > 2:
        scores['momentum'] = 70
    elif m5 > 0:
        scores['momentum'] = 55
    elif m5 > -2:
        scores['momentum'] = 40
    else:
        scores['momentum'] = 25
    
    # 5. 趋势因子 (10%)
    scores['trend'] = stock.get('trend_score', 50)
    
    # 6. 波动率因子 (10%) - 低波动更好
    vol = stock.get('volatility', 50)
    if vol < 20:
        scores['volatility'] = 85
    elif vol < 30:
        scores['volatility'] = 70
    elif vol < 40:
        scores['volatility'] = 55
    elif vol < 60:
        scores['volatility'] = 40
    else:
        scores['volatility'] = 25
    
    # 7. 技术因子 (15%)
    tech_score = 0
    if stock.get('macd_golden'):
        tech_score += 35
    if stock.get('kdj_golden'):
        tech_score += 30
    if stock.get('ma_bullish'):
        tech_score += 35
    # MACD得分也加入
    tech_score = min(100, tech_score * 0.7 + stock.get('macd_score', 50) * 0.3)
    scores['technical'] = tech_score
    
    # 8. 量能因子 (10%)
    vr = stock.get('vol_ratio', 1.0)
    if 1.0 < vr < 2.0:
        scores['volume'] = 75
    elif 0.8 <= vr <= 1.0:
        scores['volume'] = 55
    elif 2.0 <= vr < 3.0:
        scores['volume'] = 65
    elif vr >= 3.0:
        scores['volume'] = 40  # 过度放量
    else:
        scores['volume'] = 35  # 缩量
    
    # 综合得分
    total_score = (
        scores.get('valuation', 50) * 0.15 +
        scores.get('quality', 50) * 0.15 +
        scores.get('growth', 50) * 0.15 +
        scores.get('momentum', 50) * 0.10 +
        scores.get('trend', 50) * 0.10 +
        scores.get('volatility', 50) * 0.10 +
        scores.get('technical', 50) * 0.15 +
        scores.get('volume', 50) * 0.10
    )
    
    stock['scores'] = scores
    stock['total_score'] = round(total_score, 2)
    stock['factor_scores'] = scores

# 排序获取TOP 10
stock_results.sort(key=lambda x: x.get('total_score', 0), reverse=True)
top10 = stock_results[:10]

# 计算基本面统计
all_pe = [s['pe'] for s in stock_results if s.get('pe') is not None and isinstance(s.get('pe'), (int, float)) and s['pe'] > 0]
all_pb = [s['pb'] for s in stock_results if s.get('pb') is not None and isinstance(s.get('pb'), (int, float)) and s['pb'] > 0]
all_roe = [s['approx_roe'] for s in stock_results if s.get('approx_roe') is not None and isinstance(s.get('approx_roe'), (int, float))]

fundamentals = {
    'avg_pe': round(np.mean(all_pe), 2) if all_pe else None,
    'median_pe': round(np.median(all_pe), 2) if all_pe else None,
    'avg_pb': round(np.mean(all_pb), 2) if all_pb else None,
    'median_pb': round(np.median(all_pb), 2) if all_pb else None,
    'avg_roe': round(np.mean(all_roe), 2) if all_roe else None,
    'pe_count': len(all_pe),
    'pb_count': len(all_pb),
    'roe_count': len(all_roe),
}

# PE历史分位估算（简化处理：用当前PE在成分股中的位置估算）
if fundamentals['avg_pe'] and valid_pe:
    from scipy import stats
    fundamentals['pe_percentile'] = round(stats.percentileofscore(valid_pe, fundamentals['avg_pe']), 1)
else:
    fundamentals['pe_percentile'] = None

print(f"\n  基本面统计:")
print(f"    平均PE: {fundamentals['avg_pe']}")
print(f"    平均PB: {fundamentals['avg_pb']}")
print(f"    平均ROE(近似): {fundamentals['avg_roe']}%")

# ============================================================
# 保存结果
# ============================================================
result = {
    'analysis_date': '2026-07-31',
    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_stocks': total_stocks,
    'analyzed_stocks': len(stock_results),
    'market_env': market_env,
    'technical_stats': {
        'macd_golden_count': macd_golden_count,
        'kdj_golden_count': kdj_golden_count,
        'ma_bullish_count': ma_bullish_count,
        'macd_golden_pct': round(macd_golden_count / max(len(stock_results), 1) * 100, 2),
        'kdj_golden_pct': round(kdj_golden_count / max(len(stock_results), 1) * 100, 2),
        'ma_bullish_pct': round(ma_bullish_count / max(len(stock_results), 1) * 100, 2),
    },
    'fundamentals': fundamentals,
    'top10': [],
    'all_stocks_count': len(stock_results),
}

for stock in top10:
    risk_level = '低风险'
    if stock.get('volatility', 0) > 50:
        risk_level = '高风险'
    elif stock.get('volatility', 0) > 35:
        risk_level = '中高风险'
    elif stock.get('volatility', 0) > 25:
        risk_level = '中风险'
    
    top10_entry = {
        'code': stock['code'],
        'name': stock['name'],
        'close': stock['close'],
        'pe': round(stock.get('pe', 0) or 0, 2),
        'pb': round(stock.get('pb', 0) or 0, 2),
        'approx_roe': round(stock.get('approx_roe', 0) or 0, 2),
        'total_score': stock['total_score'],
        'risk_level': risk_level,
        'momentum_5': round(stock.get('momentum_5', 0), 2),
        'momentum_20': round(stock.get('momentum_20', 0), 2),
        'factor_scores': stock.get('factor_scores', {}),
        'macd_golden': stock.get('macd_golden', False),
        'kdj_golden': stock.get('kdj_golden', False),
        'ma_bullish': stock.get('ma_bullish', False),
        'pct_chg': stock.get('pct_chg'),
    }
    result['top10'].append(top10_entry)

# 保存完整stock_results供quant_selector使用
result['all_stocks'] = [{
    'code': s['code'],
    'name': s['name'],
    'market': s['market'],
    'close': s['close'],
    'pe': s.get('pe'),
    'pb': s.get('pb'),
    'approx_roe': s.get('approx_roe'),
    'total_score': s['total_score'],
    'momentum_5': s.get('momentum_5', 0),
    'momentum_20': s.get('momentum_20', 0),
    'volatility': s.get('volatility', 0),
    'vol_ratio': s.get('vol_ratio', 1),
    'avg_turnover': s.get('avg_turnover', 0),
    'macd_golden': s.get('macd_golden', False),
    'kdj_golden': s.get('kdj_golden', False),
    'ma_bullish': s.get('ma_bullish', False),
    'macd_score': s.get('macd_score', 50),
    'trend_score': s.get('trend_score', 50),
    'factor_scores': s.get('factor_scores', {}),
    'pct_chg': s.get('pct_chg'),
    'total_mv': s.get('total_mv'),
    'amount': s.get('amount'),
} for s in stock_results]

with open('analysis_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n{'=' * 60}")
print(f"分析完成！结果已保存到 analysis_result.json")
print(f"  分析股票数: {len(stock_results)}")
print(f"  TOP 10 已生成")
print(f"{'=' * 60}")

# 打印TOP 10
print("\n🏆 潜力个股 TOP 10:")
print(f"{'排名':<4} {'代码':<8} {'名称':<10} {'PE':<8} {'ROE%':<8} {'得分':<8} {'风险'}")
print("-" * 60)
for i, s in enumerate(result['top10'], 1):
    print(f"{i:<4} {s['code']:<8} {s['name']:<10} {s['pe']:<8} {s['approx_roe']:<8} {s['total_score']:<8} {s['risk_level']}")
