#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock Screener - Implements common stock screening strategies using Tushare Pro API.
All date logic uses Beijing time (UTC+8) to ensure data freshness.

Usage:
    python stock_screener.py --strategy <strategy_name> [options]

Strategies:
    value       - Value investing screen (low PE/PB, high ROE)
    growth      - Growth stock screen (high revenue/profit growth)
    dividend    - High dividend yield screen
    momentum    - Technical momentum screen

Examples:
    python stock_screener.py --strategy value --pe-max 20 --roe-min 15 --mv-min 100
    python stock_screener.py --strategy dividend --yield-min 3
    python stock_screener.py --strategy growth --rev-growth-min 20
"""

import sys
import os
import argparse
import time

# Add the scripts directory to path for importing tushare_helper
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tushare_helper import TushareHelper

try:
    import pandas as pd
except ModuleNotFoundError:
    print("[ERROR] Missing Python package: pandas")
    print("[ERROR] This skill does not auto-install dependencies. Install pandas manually, then rerun.")
    sys.exit(1)


def _to_numeric(series):
    return pd.to_numeric(series, errors='coerce')


def _latest_by_code(df, code_col='ts_code', date_col='end_date'):
    if df is None or df.empty:
        return pd.DataFrame()
    if code_col not in df.columns:
        return df
    result = df.copy()
    if date_col in result.columns:
        result[date_col] = result[date_col].astype(str)
        result = result.sort_values([code_col, date_col], ascending=[True, False])
    return result.drop_duplicates(subset=[code_col], keep='first')


def _pick_existing_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def _consecutive_dividend_years(df_dividend):
    if df_dividend is None or df_dividend.empty:
        return 0

    year_col = _pick_existing_column(df_dividend, ['end_date', 'ann_date', 'record_date'])
    if year_col is None:
        return 0

    years = (
        df_dividend[year_col]
        .dropna()
        .astype(str)
        .str.slice(0, 4)
    )
    valid_years = sorted({int(y) for y in years if y.isdigit()}, reverse=True)
    if not valid_years:
        return 0

    consecutive = 1
    for idx in range(1, len(valid_years)):
        if valid_years[idx - 1] - valid_years[idx] == 1:
            consecutive += 1
        else:
            break
    return consecutive


def _sort_by_available_columns(df, sort_specs):
    columns = [column for column, _ in sort_specs if column in df.columns]
    ascending = [direction for column, direction in sort_specs if column in df.columns]
    if not columns:
        return df
    return df.sort_values(columns, ascending=ascending)


def value_screen(helper, pe_max=20, pb_max=3, roe_min=15, mv_min=100, top_n=30):
    """
    Value investing screen.

    Args:
        pe_max: Maximum PE_TTM ratio
        pb_max: Maximum PB ratio
        roe_min: Minimum ROE (%)
        mv_min: Minimum total market cap (in 100 million CNY)
        top_n: Number of top results to return
    """
    print(f"\n{'='*60}")
    print(f"Value Investing Screen")
    print(f"Criteria: PE < {pe_max}, PB < {pb_max}, ROE > {roe_min}%, MV > {mv_min} x 100m CNY")
    print(f"{'='*60}\n")

    # Use Beijing time to get the latest trade date
    trade_date = helper.get_latest_trade_date()
    print(f"[INFO] Latest trading date (Beijing time): {trade_date}")

    # Step 1: Get daily basic indicators
    print("[INFO] Fetching daily basic indicators...")
    df_basic = helper.query('daily_basic', {'trade_date': trade_date})
    if df_basic is None or df_basic.empty:
        print("[ERROR] Failed to fetch daily basic data.")
        return None

    for col in ['pe_ttm', 'pb', 'total_mv']:
        if col in df_basic.columns:
            df_basic[col] = _to_numeric(df_basic[col])

    # Convert total_mv from 10k CNY to 100m CNY
    df_basic['total_mv_yi'] = df_basic['total_mv'] / 10000

    # Step 2: Filter by PE, PB, and market cap
    filtered = df_basic[
        (df_basic['pe_ttm'] > 0) & (df_basic['pe_ttm'] < pe_max) &
        (df_basic['pb'] > 0) & (df_basic['pb'] < pb_max) &
        (df_basic['total_mv_yi'] > mv_min)
    ].copy()

    print(f"[INFO] After PE/PB/MV filter: {len(filtered)} stocks")

    # Exclude ST stocks when data is available
    df_st = helper.query('stock_st', {})
    if df_st is not None and not df_st.empty and 'ts_code' in df_st.columns:
        st_codes = set(df_st['ts_code'].dropna().astype(str))
        if st_codes:
            before = len(filtered)
            filtered = filtered[~filtered['ts_code'].astype(str).isin(st_codes)].copy()
            print(f"[INFO] Excluded ST stocks: {before - len(filtered)}")

    if filtered.empty:
        print("[INFO] No stocks match the criteria.")
        return pd.DataFrame()

    # Step 3: Get financial indicators for ROE
    print("[INFO] Fetching latest ROE snapshot...")
    df_fina = helper.query(
        'fina_indicator',
        {'limit': 10000},
        fields='ts_code,end_date,roe'
    )

    if df_fina is None or df_fina.empty:
        print("[WARN] Could not fetch ROE data.")
        result = filtered
    else:
        df_fina = _latest_by_code(df_fina, code_col='ts_code', date_col='end_date')
        df_fina['roe'] = _to_numeric(df_fina['roe'])
        df_roe = df_fina[['ts_code', 'roe']].dropna(subset=['roe'])
        df_roe = df_roe[df_roe['roe'] > roe_min]
        result = filtered.merge(df_roe, on='ts_code', how='inner')

    # Step 4: Get stock names
    print("[INFO] Fetching stock names...")
    df_names = helper.query('stock_basic', {'list_status': 'L', 'fields': 'ts_code,name,industry'})
    if df_names is not None and not df_names.empty:
        result = result.merge(df_names, on='ts_code', how='left')

    # Step 5: Sort and present
    result = _sort_by_available_columns(
        result,
        [('pe_ttm', True), ('pb', True), ('roe', False), ('total_mv_yi', False)]
    ).head(top_n)

    display_cols = ['ts_code', 'name', 'industry', 'pe_ttm', 'pb', 'total_mv_yi']
    if 'roe' in result.columns:
        display_cols.append('roe')

    available_cols = [c for c in display_cols if c in result.columns]
    result = result[available_cols]

    # Rename for display
    rename_map = {
        'ts_code': 'Stock Code', 'name': 'Stock Name', 'industry': 'Industry',
        'pe_ttm': 'PE(TTM)', 'pb': 'PB', 'total_mv_yi': 'Total MV (100m CNY)',
        'roe': 'ROE(%)'
    }
    result = result.rename(columns={k: v for k, v in rename_map.items() if k in result.columns})

    print(f"\n[RESULT] Found {len(result)} stocks matching criteria:\n")
    print(result.to_string(index=False))
    return result


def dividend_screen(helper, yield_min=3, years_min=3, top_n=30):
    """High dividend yield screen."""
    print(f"\n{'='*60}")
    print(f"Dividend Yield Screen")
    print(f"Criteria: Yield > {yield_min}%, Consecutive years >= {years_min}")
    print(f"{'='*60}\n")

    # Use Beijing time to get the latest trade date
    trade_date = helper.get_latest_trade_date()
    print(f"[INFO] Latest trading date (Beijing time): {trade_date}")

    # Get daily basic for dividend yield
    print("[INFO] Fetching dividend yield data...")
    df_basic = helper.query('daily_basic', {'trade_date': trade_date})
    if df_basic is None or df_basic.empty:
        print("[ERROR] Failed to fetch data.")
        return None

    # Filter by dividend yield
    if 'dv_ttm' not in df_basic.columns:
        print("[ERROR] daily_basic does not include dv_ttm field.")
        return None
    df_basic['dv_ttm'] = _to_numeric(df_basic['dv_ttm'])

    filtered = df_basic[
        (df_basic['dv_ttm'].notna()) & (df_basic['dv_ttm'] > yield_min)
    ].copy()

    print(f"[INFO] Stocks with yield > {yield_min}%: {len(filtered)}")

    if filtered.empty:
        print("[INFO] No stocks match the dividend yield filter.")
        return pd.DataFrame()

    # Verify consecutive dividend years
    if years_min > 1:
        candidate_limit = max(top_n * 8, 200)
        candidates = filtered.sort_values('dv_ttm', ascending=False).head(candidate_limit).copy()
        ts_codes = candidates['ts_code'].dropna().astype(str).tolist()

        print(f"[INFO] Checking consecutive dividend years for {len(ts_codes)} candidates...")
        year_rows = []
        for idx, code in enumerate(ts_codes):
            df_dividend = helper.query('dividend', {'ts_code': code})
            years = _consecutive_dividend_years(df_dividend)
            if years >= years_min:
                year_rows.append({'ts_code': code, 'dividend_years': years})

            if (idx + 1) % 30 == 0:
                print(f"[INFO] Dividend continuity progress: {idx + 1}/{len(ts_codes)}")
            time.sleep(0.2)

        if not year_rows:
            print("[INFO] No stocks meet the consecutive dividend years requirement.")
            return pd.DataFrame()

        df_years = pd.DataFrame(year_rows)
        filtered = candidates.merge(df_years, on='ts_code', how='inner')
        print(f"[INFO] Stocks with >= {years_min} consecutive dividend years: {len(filtered)}")
    else:
        filtered['dividend_years'] = None

    # Get stock names
    df_names = helper.query('stock_basic', {'list_status': 'L', 'fields': 'ts_code,name,industry'})
    if df_names is not None:
        filtered = filtered.merge(df_names, on='ts_code', how='left')

    # Sort by dividend yield
    filtered = filtered.sort_values('dv_ttm', ascending=False).head(top_n)

    display_cols = ['ts_code', 'name', 'industry', 'dv_ttm', 'dividend_years', 'pe_ttm', 'pb', 'total_mv']
    available_cols = [c for c in display_cols if c in filtered.columns]
    result = pd.DataFrame(filtered[available_cols]).copy()
    if 'total_mv' in result.columns:
        result['total_mv'] = _to_numeric(result['total_mv'])
        result['total_mv'] = result['total_mv'] / 10000  # Convert to 100m CNY

    rename_map = {
        'ts_code': 'Stock Code', 'name': 'Stock Name', 'industry': 'Industry',
        'dv_ttm': 'Dividend Yield (TTM %)', 'dividend_years': 'Consecutive Dividend Years', 'pe_ttm': 'PE(TTM)', 'pb': 'PB',
        'total_mv': 'Total MV (100m CNY)'
    }
    result = result.rename(columns={k: v for k, v in rename_map.items() if k in result.columns})

    print(f"\n[RESULT] Found {len(result)} high-dividend stocks:\n")
    print(result.to_string(index=False))
    return result


def growth_screen(helper, rev_growth_min=20, profit_growth_min=25, roe_min=10, top_n=30):
    """Growth stock screen based on latest financial YoY metrics."""
    print(f"\n{'='*60}")
    print("Growth Stock Screen")
    print(f"Criteria: Revenue YoY > {rev_growth_min}%, Profit YoY > {profit_growth_min}%, ROE > {roe_min}%")
    print(f"{'='*60}\n")

    trade_date = helper.get_latest_trade_date()
    print(f"[INFO] Latest trading date (Beijing time): {trade_date}")

    print("[INFO] Fetching financial growth indicators...")
    df_fina = helper.query(
        'fina_indicator',
        {'limit': 10000},
        fields='ts_code,end_date,roe,or_yoy,tr_yoy,netprofit_yoy,dt_netprofit_yoy'
    )
    if df_fina is None or df_fina.empty:
        print("[ERROR] Failed to fetch fina_indicator data.")
        return None

    df_fina = _latest_by_code(df_fina, code_col='ts_code', date_col='end_date')
    rev_col = _pick_existing_column(df_fina, ['or_yoy', 'tr_yoy'])
    profit_col = _pick_existing_column(df_fina, ['netprofit_yoy', 'dt_netprofit_yoy'])

    if rev_col is None or profit_col is None or 'roe' not in df_fina.columns:
        print("[ERROR] Required growth fields are missing in fina_indicator data.")
        return None

    rev_col = str(rev_col)
    profit_col = str(profit_col)

    for col in ['roe', rev_col, profit_col]:
        df_fina[col] = _to_numeric(df_fina[col])

    filtered = df_fina[
        (df_fina[rev_col] > rev_growth_min) &
        (df_fina[profit_col] > profit_growth_min) &
        (df_fina['roe'] > roe_min)
    ].copy()

    print(f"[INFO] Stocks after growth filter: {len(filtered)}")
    if filtered.empty:
        print("[INFO] No stocks match the growth criteria.")
        return pd.DataFrame()

    print("[INFO] Fetching valuation snapshot...")
    df_basic = helper.query(
        'daily_basic',
        {'trade_date': trade_date},
        fields='ts_code,pe_ttm,pb,total_mv'
    )
    if df_basic is not None and not df_basic.empty:
        for col in ['pe_ttm', 'pb', 'total_mv']:
            if col in df_basic.columns:
                df_basic[col] = _to_numeric(df_basic[col])
        df_basic['total_mv_yi'] = df_basic['total_mv'] / 10000
        filtered = filtered.merge(df_basic[['ts_code', 'pe_ttm', 'pb', 'total_mv_yi']], on='ts_code', how='left')

    print("[INFO] Fetching stock names...")
    df_names = helper.query('stock_basic', {'list_status': 'L', 'fields': 'ts_code,name,industry'})
    if df_names is not None and not df_names.empty:
        filtered = filtered.merge(df_names, on='ts_code', how='left')

    filtered = _sort_by_available_columns(
        filtered,
        [(profit_col, False), (rev_col, False), ('roe', False), ('pe_ttm', True)]
    ).head(top_n)

    display_cols = ['ts_code', 'name', 'industry', rev_col, profit_col, 'roe', 'pe_ttm', 'pb', 'total_mv_yi']
    available_cols = [c for c in display_cols if c in filtered.columns]
    result = pd.DataFrame(filtered[available_cols]).copy()

    rename_map = {
        'ts_code': 'Stock Code',
        'name': 'Stock Name',
        'industry': 'Industry',
        rev_col: 'Revenue YoY (%)',
        profit_col: 'Net Profit YoY (%)',
        'roe': 'ROE(%)',
        'pe_ttm': 'PE(TTM)',
        'pb': 'PB',
        'total_mv_yi': 'Total MV (100m CNY)'
    }
    result = result.rename(columns={k: v for k, v in rename_map.items() if k in result.columns})

    print(f"\n[RESULT] Found {len(result)} growth stocks:\n")
    print(result.to_string(index=False))
    return result


def momentum_screen(helper, pct_chg_min=3, volume_ratio_min=1.2, turnover_min=2, top_n=30):
    """Technical momentum screen using daily gain + liquidity confirmation."""
    print(f"\n{'='*60}")
    print("Momentum Screen")
    print(f"Criteria: PctChg > {pct_chg_min}%, VolumeRatio > {volume_ratio_min}, Turnover > {turnover_min}%")
    print(f"{'='*60}\n")

    trade_date = helper.get_latest_trade_date()
    print(f"[INFO] Latest trading date (Beijing time): {trade_date}")

    print("[INFO] Fetching daily price change data...")
    df_daily = helper.query('daily', {'trade_date': trade_date}, fields='ts_code,close,pct_chg,vol,amount')
    if df_daily is None or df_daily.empty:
        print("[ERROR] Failed to fetch daily data.")
        return None

    print("[INFO] Fetching turnover and volume ratio data...")
    df_basic = helper.query('daily_basic', {'trade_date': trade_date}, fields='ts_code,volume_ratio,turnover_rate,pe_ttm,pb,total_mv')
    if df_basic is not None and not df_basic.empty:
        merged = df_daily.merge(df_basic, on='ts_code', how='left')
    else:
        merged = df_daily.copy()

    for col in ['pct_chg', 'volume_ratio', 'turnover_rate', 'total_mv']:
        if col in merged.columns:
            merged[col] = _to_numeric(merged[col])

    condition = merged['pct_chg'] > pct_chg_min
    if 'volume_ratio' in merged.columns:
        condition &= merged['volume_ratio'] > volume_ratio_min
    if 'turnover_rate' in merged.columns:
        condition &= merged['turnover_rate'] > turnover_min

    filtered = merged[condition].copy()
    print(f"[INFO] Stocks after momentum filter: {len(filtered)}")

    if filtered.empty:
        print("[INFO] No stocks match the momentum criteria.")
        return pd.DataFrame()

    if 'total_mv' in filtered.columns:
        filtered['total_mv_yi'] = filtered['total_mv'] / 10000

    print("[INFO] Fetching stock names...")
    df_names = helper.query('stock_basic', {'list_status': 'L', 'fields': 'ts_code,name,industry'})
    if df_names is not None and not df_names.empty:
        filtered = filtered.merge(df_names, on='ts_code', how='left')

    filtered = _sort_by_available_columns(
        filtered,
        [('pct_chg', False), ('volume_ratio', False), ('turnover_rate', False), ('amount', False)]
    ).head(top_n)

    display_cols = [
        'ts_code', 'name', 'industry', 'close', 'pct_chg', 'volume_ratio',
        'turnover_rate', 'pe_ttm', 'pb', 'total_mv_yi'
    ]
    available_cols = [c for c in display_cols if c in filtered.columns]
    result = filtered[available_cols].copy()

    rename_map = {
        'ts_code': 'Stock Code',
        'name': 'Stock Name',
        'industry': 'Industry',
        'close': 'Close',
        'pct_chg': 'Pct Change (%)',
        'volume_ratio': 'Volume Ratio',
        'turnover_rate': 'Turnover Rate (%)',
        'pe_ttm': 'PE(TTM)',
        'pb': 'PB',
        'total_mv_yi': 'Total MV (100m CNY)'
    }
    result = result.rename(columns={k: v for k, v in rename_map.items() if k in result.columns})

    print(f"\n[RESULT] Found {len(result)} momentum stocks:\n")
    print(result.to_string(index=False))
    return result


def main():
    parser = argparse.ArgumentParser(description="Stock Screener using Tushare Pro API")
    parser.add_argument("--strategy", "-s", required=True,
                        choices=['value', 'growth', 'dividend', 'momentum'],
                        help="Screening strategy to use")
    parser.add_argument("--pe-max", type=float, default=20, help="Max PE ratio (value strategy)")
    parser.add_argument("--pb-max", type=float, default=3, help="Max PB ratio (value strategy)")
    parser.add_argument("--roe-min", type=float, default=15, help="Min ROE %% (value strategy)")
    parser.add_argument("--mv-min", type=float, default=100, help="Min market cap in 100m CNY (value strategy)")
    parser.add_argument("--yield-min", type=float, default=3, help="Min dividend yield %% (dividend strategy)")
    parser.add_argument("--years-min", type=int, default=3, help="Min consecutive dividend years (dividend strategy)")
    parser.add_argument("--rev-growth-min", type=float, default=20, help="Min revenue growth %% (growth strategy)")
    parser.add_argument("--profit-growth-min", type=float, default=25, help="Min net profit growth %% (growth strategy)")
    parser.add_argument("--pct-chg-min", type=float, default=3, help="Min daily pct change %% (momentum strategy)")
    parser.add_argument("--volume-ratio-min", type=float, default=1.2, help="Min volume ratio (momentum strategy)")
    parser.add_argument("--turnover-min", type=float, default=2, help="Min turnover rate %% (momentum strategy)")
    parser.add_argument("--top-n", type=int, default=30, help="Number of top results to show")
    parser.add_argument("--output", "-o", default=None, help="Output CSV file path")

    args = parser.parse_args()

    helper = TushareHelper()
    result = None

    if args.strategy == 'value':
        result = value_screen(helper, args.pe_max, args.pb_max, args.roe_min, args.mv_min, args.top_n)
    elif args.strategy == 'dividend':
        result = dividend_screen(helper, args.yield_min, years_min=args.years_min, top_n=args.top_n)
    elif args.strategy == 'growth':
        result = growth_screen(
            helper,
            rev_growth_min=args.rev_growth_min,
            profit_growth_min=args.profit_growth_min,
            top_n=args.top_n
        )
    elif args.strategy == 'momentum':
        result = momentum_screen(
            helper,
            pct_chg_min=args.pct_chg_min,
            volume_ratio_min=args.volume_ratio_min,
            turnover_min=args.turnover_min,
            top_n=args.top_n
        )

    if isinstance(result, pd.DataFrame) and not result.empty and args.output:
        result.to_csv(args.output, index=False, encoding='utf-8-sig')
        print(f"\n[INFO] Results saved to {args.output}")


if __name__ == '__main__':
    main()
