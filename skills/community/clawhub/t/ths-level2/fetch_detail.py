# -*- coding: utf-8 -*-
import os
import sys
os.environ['PYTHONIOENCODING'] = 'utf-8'

import tushare as ts
import pandas as pd

token = os.environ.get('TUSHARE_TOKEN', '')
ts.set_token(token)
pro = ts.pro_api()

stocks = [
    ('600760.SH', '中航沈飞'),
    ('601888.SH', '中国中免'),
    ('600276.SH', '恒瑞医药'),
    ('002202.SZ', '金风科技'),
    ('688235.SH', '百济神州'),
]

print('='*80)
print('财务指标对比')
print('='*80)

for code, name in stocks:
    print(f'\n{name} ({code}):')
    try:
        # 财务指标
        df = pro.fina_indicator(ts_code=code, start_date='20250101', end_date='20260321')
        if df is not None and len(df) > 0:
            row = df.iloc[0]
            roe = row.get('roe', None)
            gross = row.get('grossprofit_margin', None)
            net_margin = row.get('netprofit_margin', None)
            print(f"  ROE: {roe:.2f}%" if pd.notna(roe) else "  ROE: N/A")
            print(f"  毛利率: {gross:.2f}%" if pd.notna(gross) else "  毛利率: N/A")
            print(f"  净利率: {net_margin:.2f}%" if pd.notna(net_margin) else "  净利率: N/A")
        else:
            print("  无财务数据")
    except Exception as e:
        print(f"  获取失败: {e}")

print('\n' + '='*80)
print('估值指标')
print('='*80)

for code, name in stocks:
    print(f'\n{name} ({code}):')
    try:
        df = pro.daily_basic(ts_code=code, trade_date='20260320')
        if df is not None and len(df) > 0:
            row = df.iloc[0]
            pe = row.get('pe', None)
            pb = row.get('pb', None)
            turnover = row.get('turnover_rate', None)
            total_mv = row.get('total_mv', None)
            circ_mv = row.get('circ_mv', None)
            print(f"  PE: {pe:.2f}" if pd.notna(pe) else "  PE: N/A")
            print(f"  PB: {pb:.2f}" if pd.notna(pb) else "  PB: N/A")
            print(f"  换手率: {turnover:.2f}%" if pd.notna(turnover) else "  换手率: N/A")
            print(f"  总市值: {total_mv:.0f}亿" if pd.notna(total_mv) else "  总市值: N/A")
        else:
            print("  无估值数据")
    except Exception as e:
        print(f"  获取失败: {e}")

print('\n' + '='*80)
print('资金流向 (近10日)')
print('='*80)

for code, name in stocks:
    print(f'\n{name} ({code}):')
    try:
        df = pro.moneyflow(ts_code=code, start_date='20260301', end_date='20260320')
        if df is not None and len(df) > 0:
            # 汇总
            buy_sm = df['buy_sm_vol'].sum() if 'buy_sm_vol' in df.columns else 0
            sell_sm = df['sell_sm_vol'].sum() if 'sell_sm_vol' in df.columns else 0
            buy_md = df['buy_md_vol'].sum() if 'buy_md_vol' in df.columns else 0
            sell_md = df['sell_md_vol'].sum() if 'sell_md_vol' in df.columns else 0
            buy_lg = df['buy_lg_vol'].sum() if 'buy_lg_vol' in df.columns else 0
            sell_lg = df['sell_lg_vol'].sum() if 'sell_lg_vol' in df.columns else 0
            buy_elg = df['buy_elg_vol'].sum() if 'buy_elg_vol' in df.columns else 0
            sell_elg = df['sell_elg_vol'].sum() if 'sell_elg_vol' in df.columns else 0
            
            sm_net = (buy_sm - sell_sm) / 100000000
            md_net = (buy_md - sell_md) / 100000000
            lg_net = (buy_lg - sell_lg) / 100000000
            elg_net = (buy_elg - sell_elg) / 100000000
            total_net = sm_net + md_net + lg_net + elg_net
            
            print(f"  小单净流入: {sm_net:.2f}亿")
            print(f"  中单净流入: {md_net:.2f}亿")
            print(f"  大单净流入: {lg_net:.2f}亿")
            print(f"  特大单净流入: {elg_net:.2f}亿")
            print(f"  总净流入: {total_net:.2f}亿")
        else:
            print("  无资金流向数据")
    except Exception as e:
        print(f"  获取失败: {e}")