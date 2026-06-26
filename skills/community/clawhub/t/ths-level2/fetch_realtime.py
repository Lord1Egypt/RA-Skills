# -*- coding: utf-8 -*-
"""
获取5只股票的实时数据深度分析
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

STOCKS = [
    ('600760.SH', '中航沈飞', '航空军工'),
    ('601888.SH', '中国中免', '免税零售'),
    ('600276.SH', '恒瑞医药', '医药'),
    ('002202.SZ', '金风科技', '风电设备'),
    ('688235.SH', '百济神州', '生物医药'),
]

def get_daily(code, days=60):
    """获取日线数据"""
    end = datetime.now().strftime('%Y%m%d')
    start = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    try:
        df = pro.daily(ts_code=code, start_date=start, end_date=end)
        if df is not None and len(df) > 0:
            return df.sort_values('trade_date')
    except:
        pass
    return None

def get_moneyflow(code, days=30):
    """获取资金流向"""
    end = datetime.now().strftime('%Y%m%d')
    start = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    try:
        df = pro.moneyflow(ts_code=code, start_date=start, end_date=end)
        if df is not None and len(df) > 0:
            return df.sort_values('trade_date')
    except:
        pass
    return None

def analyze_stock(code, name, industry):
    """深度分析单只股票"""
    print(f"\n{'='*70}")
    print(f" {name} ({code}) - {industry}")
    print('='*70)
    
    result = {'code': code, 'name': name, 'industry': industry}
    
    # 1. 日线数据
    print("\n[1] 行情数据 (近60天):")
    daily = get_daily(code, 60)
    if daily is not None and len(daily) > 0:
        result['daily'] = daily
        
        latest = daily.iloc[-1]
        prev_5 = daily.iloc[-6] if len(daily) > 5 else daily.iloc[0]
        prev_20 = daily.iloc[-21] if len(daily) > 20 else daily.iloc[0]
        prev_60 = daily.iloc[0]
        
        change_1d = ((latest['close'] - daily.iloc[-2]['close']) / daily.iloc[-2]['close'] * 100) if len(daily) > 1 else 0
        change_5d = ((latest['close'] - prev_5['close']) / prev_5['close'] * 100)
        change_20d = ((latest['close'] - prev_20['close']) / prev_20['close'] * 100)
        change_60d = ((latest['close'] - prev_60['close']) / prev_60['close'] * 100)
        
        print(f"  最新价: {latest['close']:.2f}")
        print(f"  1日涨跌: {change_1d:+.2f}%")
        print(f"  5日涨跌: {change_5d:+.2f}%")
        print(f"  20日涨跌: {change_20d:+.2f}%")
        print(f"  60日涨跌: {change_60d:+.2f}%")
        
        # 成交量分析
        vol_5d = daily.tail(5)['vol'].mean()
        vol_20d = daily.tail(20)['vol'].mean()
        vol_ratio = vol_5d / vol_20d if vol_20d > 0 else 1
        
        print(f"\n  成交量分析:")
        print(f"    5日均量: {vol_5d/10000:.0f}万手")
        print(f"    20日均量: {vol_20d/10000:.0f}万手")
        print(f"    量比: {vol_ratio:.2f}")
        
        # 价格位置
        high_60 = daily['high'].max()
        low_60 = daily['low'].min()
        price_position = (latest['close'] - low_60) / (high_60 - low_60) * 100
        
        print(f"\n  价格位置:")
        print(f"    60日最高: {high_60:.2f}")
        print(f"    60日最低: {low_60:.2f}")
        print(f"    当前位置: {price_position:.1f}% ({'高位' if price_position > 70 else '中位' if price_position > 30 else '低位'})")
        
        result['price'] = latest['close']
        result['change_1d'] = change_1d
        result['change_5d'] = change_5d
        result['change_20d'] = change_20d
        result['change_60d'] = change_60d
        result['vol_ratio'] = vol_ratio
        result['price_position'] = price_position
        
        # 技术指标
        close_5 = daily.tail(5)['close'].mean()
        close_10 = daily.tail(10)['close'].mean()
        close_20 = daily.tail(20)['close'].mean()
        
        print(f"\n  均线分析:")
        print(f"    MA5: {close_5:.2f} {'↑' if latest['close'] > close_5 else '↓'}")
        print(f"    MA10: {close_10:.2f} {'↑' if latest['close'] > close_10 else '↓'}")
        print(f"    MA20: {close_20:.2f} {'↑' if latest['close'] > close_20 else '↓'}")
        
        ma_trend = '多头排列' if close_5 > close_10 > close_20 else '空头排列' if close_5 < close_10 < close_20 else '交叉整理'
        print(f"    均线形态: {ma_trend}")
        result['ma_trend'] = ma_trend
    
    # 2. 资金流向
    print("\n[2] 资金流向分析:")
    mf = get_moneyflow(code, 30)
    if mf is not None and len(mf) > 0:
        result['moneyflow'] = mf
        
        # 计算净流入
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
        
        print(f"  近30日资金流向 (亿元):")
        print(f"    小单净流入: {sm_net:+.2f}")
        print(f"    中单净流入: {md_net:+.2f}")
        print(f"    大单净流入: {lg_net:+.2f}")
        print(f"    特大单净流入: {elg_net:+.2f}")
        print(f"    主力净流入: {main_net:+.2f}")
        print(f"    总净流入: {total_net:+.2f}")
        
        # 最近5天资金流向
        print(f"\n  最近5天资金流向 (万元):")
        for _, row in mf.tail(5).iterrows():
            net = row.get('net_mf_vol', 0)
            if pd.notna(net):
                print(f"    {row['trade_date']}: {net/10000:+.0f}")
        
        result['main_net_inflow'] = main_net
        result['total_net_inflow'] = total_net
    else:
        print("  无资金流向数据 (需要更高级别权限)")
    
    # 3. 筹码分析 (基于价格分布)
    print("\n[3] 筹码分布分析:")
    if daily is not None and len(daily) >= 20:
        # 简单的筹码分布估计
        close_prices = daily['close']
        vol = daily['vol']
        
        # 成交量加权平均价
        vwap = (close_prices * vol).sum() / vol.sum()
        
        # 价格区间分布
        latest_price = latest['close']
        high = daily['high'].max()
        low = daily['low'].min()
        
        # 获利盘比例估计
        profitable = len(daily[daily['close'] < latest_price]) / len(daily) * 100
        
        print(f"  成交量加权均价: {vwap:.2f}")
        print(f"  当前价格偏离VWAP: {(latest_price - vwap) / vwap * 100:+.2f}%")
        print(f"  预估获利盘比例: {profitable:.1f}%")
        
        # 换手率估算
        avg_turnover = daily.tail(20)['vol'].sum()
        print(f"  20日累计换手估算: {avg_turnover/10000:.0f}万手")
        
        result['vwap'] = vwap
        result['profitable_ratio'] = profitable
    
    return result

def main():
    print("=" * 70)
    print(" 5只股票深度分析 - 筹码/资金/成交量")
    print(f" 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    results = []
    
    for code, name, industry in STOCKS:
        try:
            result = analyze_stock(code, name, industry)
            results.append(result)
        except Exception as e:
            print(f"\n分析 {name} 出错: {e}")
    
    # 汇总对比
    print("\n" + "=" * 70)
    print(" 汇总对比")
    print("=" * 70)
    
    print("\n| 股票 | 最新价 | 5日涨跌 | 20日涨跌 | 量比 | 价格位置 | 主力资金 |")
    print("|------|--------|---------|----------|------|----------|----------|")
    
    for r in results:
        name = r.get('name', 'N/A')
        price = r.get('price', 0)
        c5 = r.get('change_5d', 0)
        c20 = r.get('change_20d', 0)
        vr = r.get('vol_ratio', 0)
        pos = r.get('price_position', 0)
        main = r.get('main_net_inflow', None)
        main_str = f"{main:+.2f}亿" if main is not None else "N/A"
        
        print(f"| {name} | {price:.2f} | {c5:+.1f}% | {c20:+.1f}% | {vr:.2f} | {pos:.0f}% | {main_str} |")
    
    # 保存结果
    output = {
        'analysis_time': datetime.now().isoformat(),
        'stocks': results
    }
    
    output_path = r"D:\Cadence\SPB_Data\.openclaw\workspace\ths_level2\realtime_analysis.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n结果已保存到: {output_path}")

if __name__ == '__main__':
    main()