# -*- coding: utf-8 -*-
"""
美亚柏科(300188.SZ) 财报与主力资金深度分析
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
pd.set_option('display.float_format', lambda x: '%.2f' % x)

token = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(token)
pro = ts.pro_api()

CODE = '300188.SZ'
NAME = '美亚柏科'

print("=" * 80)
print(f" {NAME} ({CODE}) 财报与主力资金深度分析")
print(f" 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 80)

# ==================== 财报分析 ====================
print("\n" + "=" * 80)
print(" 第一部分: 财务报表分析")
print("=" * 80)

# 1. 利润表
print("\n[1] 利润表数据 (近4个季度)")
print("-" * 60)

try:
    income = pro.income(ts_code=CODE, start_date='20250101', end_date='20260321')
    if income is not None and len(income) > 0:
        print(f"\n{'报告期':<12} {'营业收入(亿)':>12} {'净利润(亿)':>12} {'毛利率%':>10} {'净利率%':>10} {'同比%':>10}")
        print("-" * 70)
        for _, row in income.head(4).iterrows():
            revenue = row['revenue'] / 100000000 if pd.notna(row['revenue']) else 0
            net_profit = row['net_profit'] / 100000000 if pd.notna(row['net_profit']) else 0
            gross_margin = row['grossprofit_margin'] if pd.notna(row['grossprofit_margin']) else 0
            net_margin = row['netprofit_margin'] if pd.notna(row['netprofit_margin']) else 0
            yoy_sales = row['yoy_sales'] if pd.notna(row['yoy_sales']) else 0
            
            print(f"{row['end_date']:<12} {revenue:>12.2f} {net_profit:>12.2f} {gross_margin:>10.2f} {net_margin:>10.2f} {yoy_sales:>+10.2f}")
    else:
        print("  无利润表数据")
except Exception as e:
    print(f"  利润表获取失败: {e}")

# 2. 资产负债表
print("\n[2] 资产负债表 (近4个季度)")
print("-" * 60)

try:
    balancesheet = pro.balancesheet(ts_code=CODE, start_date='20250101', end_date='20260321')
    if balancesheet is not None and len(balancesheet) > 0:
        print(f"\n{'报告期':<12} {'总资产(亿)':>12} {'总负债(亿)':>12} {'净资产(亿)':>12} {'负债率%':>10}")
        print("-" * 60)
        for _, row in balancesheet.head(4).iterrows():
            total_assets = row['total_assets'] / 100000000 if pd.notna(row['total_assets']) else 0
            total_liab = row['total_liab'] / 100000000 if pd.notna(row['total_liab']) else 0
            total_hldr_eqy = row['total_hldr_eqy_exc_min_int'] / 100000000 if pd.notna(row['total_hldr_eqy_exc_min_int']) else 0
            debt_ratio = (total_liab / total_assets * 100) if total_assets > 0 else 0
            
            print(f"{row['end_date']:<12} {total_assets:>12.2f} {total_liab:>12.2f} {total_hldr_eqy:>12.2f} {debt_ratio:>10.2f}")
    else:
        print("  无资产负债表数据")
except Exception as e:
    print(f"  资产负债表获取失败: {e}")

# 3. 财务指标
print("\n[3] 关键财务指标 (近4个季度)")
print("-" * 60)

try:
    fina = pro.fina_indicator(ts_code=CODE, start_date='20250101', end_date='20260321')
    if fina is not None and len(fina) > 0:
        print(f"\n{'报告期':<12} {'ROE%':>8} {'ROA%':>8} {'毛利率%':>10} {'净利率%':>10} {'每股收益':>10}")
        print("-" * 60)
        for _, row in fina.head(4).iterrows():
            roe = row['roe'] if pd.notna(row['roe']) else 0
            roa = row['roa'] if pd.notna(row['roa']) else 0
            gross = row['grossprofit_margin'] if pd.notna(row['grossprofit_margin']) else 0
            net = row['netprofit_margin'] if pd.notna(row['netprofit_margin']) else 0
            eps = row['eps'] if pd.notna(row['eps']) else 0
            
            print(f"{row['end_date']:<12} {roe:>8.2f} {roa:>8.2f} {gross:>10.2f} {net:>10.2f} {eps:>10.3f}")
        
        # 保存最新财务指标
        latest_fina = fina.iloc[0]
        print(f"\n最新财务指标详解:")
        print(f"  ROE (净资产收益率): {latest_fina['roe']:.2f}% {'良好' if latest_fina['roe'] > 10 else '一般'}")
        print(f"  ROA (总资产收益率): {latest_fina['roa']:.2f}%")
        print(f"  毛利率: {latest_fina['grossprofit_margin']:.2f}%")
        print(f"  净利率: {latest_fina['netprofit_margin']:.2f}%")
        print(f"  每股收益(EPS): {latest_fina['eps']:.3f}元")
        if pd.notna(latest_fina.get('bps')):
            print(f"  每股净资产(BPS): {latest_fina['bps']:.2f}元")
        if pd.notna(latest_fina.get('cfps')):
            print(f"  每股现金流: {latest_fina['cfps']:.2f}元")
    else:
        print("  无财务指标数据")
except Exception as e:
    print(f"  财务指标获取失败: {e}")

# 4. 现金流量表
print("\n[4] 现金流量表 (近4个季度)")
print("-" * 60)

try:
    cashflow = pro.cashflow(ts_code=CODE, start_date='20250101', end_date='20260321')
    if cashflow is not None and len(cashflow) > 0:
        print(f"\n{'报告期':<12} {'经营现金流(亿)':>14} {'投资现金流(亿)':>14} {'筹资现金流(亿)':>14}")
        print("-" * 58)
        for _, row in cashflow.head(4).iterrows():
            ocf = row['n_cashflow_act'] / 100000000 if pd.notna(row['n_cashflow_act']) else 0
            icf = row['n_cashflow_inv_act'] / 100000000 if pd.notna(row['n_cashflow_inv_act']) else 0
            fcf = row['n_cash_flows_fnc_act'] / 100000000 if pd.notna(row['n_cash_flows_fnc_act']) else 0
            
            print(f"{row['end_date']:<12} {ocf:>+14.2f} {icf:>+14.2f} {fcf:>+14.2f}")
    else:
        print("  无现金流量表数据")
except Exception as e:
    print(f"  现金流量表获取失败: {e}")

# ==================== 主力资金分析 ====================
print("\n" + "=" * 80)
print(" 第二部分: 主力资金分析")
print("=" * 80)

# 1. 日线数据获取
end = datetime.now().strftime('%Y%m%d')
start = (datetime.now() - timedelta(days=120)).strftime('%Y%m%d')

daily = pro.daily(ts_code=CODE, start_date=start, end_date=end)
if daily is not None and len(daily) > 0:
    daily = daily.sort_values('trade_date')

# 2. 成交量与价格关系分析
print("\n[1] 成交量与价格关系")
print("-" * 60)

if daily is not None and len(daily) > 0:
    # 计算不同周期的成交变化
    vol_5d = daily.tail(5)['vol'].sum()
    vol_20d = daily.tail(20)['vol'].sum()
    vol_60d = daily.tail(60)['vol'].sum()
    
    avg_5d = daily.tail(5)['vol'].mean()
    avg_20d = daily.tail(20)['vol'].mean()
    avg_60d = daily.tail(60)['vol'].mean()
    
    print(f"\n成交量统计:")
    print(f"  近5日总成交: {vol_5d/10000:.1f}万手")
    print(f"  近20日总成交: {vol_20d/10000:.1f}万手")
    print(f"  近60日总成交: {vol_60d/10000:.1f}万手")
    
    print(f"\n日均成交量:")
    print(f"  5日均量: {avg_5d/10000:.1f}万手")
    print(f"  20日均量: {avg_20d/10000:.1f}万手")
    print(f"  60日均量: {avg_60d/10000:.1f}万手")
    
    vol_ratio_5_20 = avg_5d / avg_20d if avg_20d > 0 else 1
    vol_ratio_20_60 = avg_20d / avg_60d if avg_60d > 0 else 1
    
    print(f"\n量比分析:")
    print(f"  5日/20日量比: {vol_ratio_5_20:.2f} ({'放量' if vol_ratio_5_20 > 1.2 else '缩量' if vol_ratio_5_20 < 0.8 else '正常'})")
    print(f"  20日/60日量比: {vol_ratio_20_60:.2f}")

# 3. 价格与成交量的关系
print("\n[2] 量价关系分析")
print("-" * 60)

if daily is not None and len(daily) >= 20:
    # 上涨日vs下跌日成交量对比
    up_days = daily.tail(20)[daily.tail(20)['pct_chg'] > 0]
    down_days = daily.tail(20)[daily.tail(20)['pct_chg'] < 0]
    
    up_vol = up_days['vol'].mean() if len(up_days) > 0 else 0
    down_vol = down_days['vol'].mean() if len(down_days) > 0 else 0
    
    print(f"\n近20日量价关系:")
    print(f"  上涨天数: {len(up_days)}天, 平均成交: {up_vol/10000:.1f}万手")
    print(f"  下跌天数: {len(down_days)}天, 平均成交: {down_vol/10000:.1f}万手")
    
    if up_vol > 0 and down_vol > 0:
        vol_ratio = up_vol / down_vol
        print(f"  上涨日/下跌日量比: {vol_ratio:.2f}")
        if vol_ratio > 1.5:
            print("  → 上涨放量，主力可能做多")
        elif vol_ratio < 0.67:
            print("  → 下跌放量，主力可能出逃")
        else:
            print("  → 量价均衡，多空僵持")
    
    # 大涨大跌日分析
    big_up = daily.tail(60)[daily.tail(60)['pct_chg'] > 5]
    big_down = daily.tail(60)[daily.tail(60)['pct_chg'] < -5]
    
    print(f"\n近60日大涨大跌统计:")
    print(f"  涨幅>5%天数: {len(big_up)}天")
    print(f"  跌幅>5%天数: {len(big_down)}天")

# 4. 资金流向尝试
print("\n[3] 主力资金流向 (尝试获取)")
print("-" * 60)

try:
    mf = pro.moneyflow(ts_code=CODE, start_date=start, end_date=end)
    if mf is not None and len(mf) > 0:
        mf = mf.sort_values('trade_date')
        
        # 计算累计资金流向
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
        
        print(f"\n近{len(mf)}日资金流向 (亿元):")
        print(f"  小单净流入: {sm_net:+.2f}")
        print(f"  中单净流入: {md_net:+.2f}")
        print(f"  大单净流入: {lg_net:+.2f}")
        print(f"  特大单净流入: {elg_net:+.2f}")
        print(f"  ────────────────────")
        print(f"  主力净流入: {main_net:+.2f}")
        print(f"  总净流入: {total_net:+.2f}")
        
        # 最近资金流向趋势
        print(f"\n最近5日资金流向:")
        for _, row in mf.tail(5).iterrows():
            net = row.get('net_mf_vol', 0)
            if pd.notna(net):
                print(f"  {row['trade_date']}: {net/10000:+.0f}万元")
    else:
        print("  无资金流向数据 (需要更高级别Tushare权限)")
except Exception as e:
    print(f"  资金流向获取失败: {str(e)[:50]}")

# 5. 基于成交量的主力行为推断
print("\n[4] 主力行为推断 (基于量价分析)")
print("-" * 60)

if daily is not None and len(daily) >= 60:
    latest = daily.iloc[-1]
    
    # 成交量趋势
    vol_trend_20 = daily.tail(20)['vol'].values
    vol_ma5 = daily.tail(5)['vol'].mean()
    vol_ma20 = daily.tail(20)['vol'].mean()
    
    # 价格趋势
    price_trend = daily.tail(20)['close'].values
    price_change = (price_trend[-1] - price_trend[0]) / price_trend[0] * 100
    
    print(f"\n量价趋势判断:")
    
    # 放量下跌
    if vol_ma5 > vol_ma20 * 1.2 and price_change < -5:
        print("  状态: 放量下跌")
        print("  推断: 主力可能在出货或市场恐慌性抛售")
    # 缩量下跌
    elif vol_ma5 < vol_ma20 * 0.8 and price_change < -5:
        print("  状态: 缩量下跌")
        print("  推断: 卖盘稀少，可能接近底部，但也可能继续阴跌")
    # 放量上涨
    elif vol_ma5 > vol_ma20 * 1.2 and price_change > 5:
        print("  状态: 放量上涨")
        print("  推断: 主力资金积极介入，趋势向好")
    # 缩量上涨
    elif vol_ma5 < vol_ma20 * 0.8 and price_change > 5:
        print("  状态: 缩量上涨")
        print("  推断: 上涨动力不足，需警惕回调")
    # 横盘整理
    elif abs(price_change) < 3:
        print("  状态: 横盘整理")
        print("  推断: 多空平衡，等待方向选择")
    else:
        print(f"  状态: 一般 ({price_change:+.1f}%)")
        print("  推断: 需要更多信号确认")
    
    # 筹码成本分析
    vwap = (daily['close'] * daily['vol']).sum() / daily['vol'].sum()
    current_price = latest['close']
    
    print(f"\n筹码成本分析:")
    print(f"  60日VWAP: {vwap:.2f}元")
    print(f"  当前价格: {current_price:.2f}元")
    print(f"  偏离成本: {(current_price - vwap) / vwap * 100:+.2f}%")
    
    if current_price < vwap * 0.9:
        print("  → 价格严重低于成本区，筹码被套")
    elif current_price < vwap:
        print("  → 价格低于成本区，大部分筹码被套")
    elif current_price > vwap * 1.1:
        print("  → 价格高于成本区，获利盘较多")

# ==================== 综合分析 ====================
print("\n" + "=" * 80)
print(" 第三部分: 综合分析结论")
print("=" * 80)

print("\n[财务状况评估]")
print("-" * 60)
try:
    if fina is not None and len(fina) > 0:
        latest_fina = fina.iloc[0]
        
        # 财务健康度评分
        scores = {}
        
        # ROE评分
        roe = latest_fina['roe'] if pd.notna(latest_fina['roe']) else 0
        if roe > 15:
            scores['ROE'] = ('优秀', 90)
        elif roe > 10:
            scores['ROE'] = ('良好', 70)
        elif roe > 5:
            scores['ROE'] = ('一般', 50)
        else:
            scores['ROE'] = ('较差', 30)
        
        # 毛利率评分
        gross = latest_fina['grossprofit_margin'] if pd.notna(latest_fina['grossprofit_margin']) else 0
        if gross > 50:
            scores['毛利率'] = ('优秀', 90)
        elif gross > 30:
            scores['毛利率'] = ('良好', 70)
        elif gross > 20:
            scores['毛利率'] = ('一般', 50)
        else:
            scores['毛利率'] = ('较差', 30)
        
        # 输出评分
        for name, (level, score) in scores.items():
            print(f"  {name}: {level} ({score}分)")
        
        avg_score = sum(s[1] for s in scores.values()) / len(scores)
        print(f"\n  财务综合评分: {avg_score:.0f}分")
except:
    print("  财务数据不足，无法评估")

print("\n[资金面评估]")
print("-" * 60)
if daily is not None and len(daily) >= 20:
    vol_ratio_5_20 = avg_5d / avg_20d if avg_20d > 0 else 1
    
    if vol_ratio_5_20 < 0.6:
        print("  成交活跃度: 极低 (严重缩量)")
        print("  资金态度: 撤退或观望")
    elif vol_ratio_5_20 < 0.8:
        print("  成交活跃度: 较低 (缩量)")
        print("  资金态度: 谨慎")
    elif vol_ratio_5_20 > 1.5:
        print("  成交活跃度: 极高 (放量)")
        print("  资金态度: 积极参与")
    else:
        print("  成交活跃度: 正常")
        print("  资金态度: 中性")

print("\n[操作建议]")
print("-" * 60)
print("  当前状态: 弱势探底，等待企稳")
print("  建议策略: 观望为主，等待以下信号:")
print("    1. 成交量恢复 (量比>0.8)")
print("    2. 放量阳线突破13.50元")
print("    3. 主力资金连续净流入")

print("\n" + "=" * 80)
print(" 分析完成")
print("=" * 80)