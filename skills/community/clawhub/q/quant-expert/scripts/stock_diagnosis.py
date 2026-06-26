#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock Diagnosis - Provides a structured diagnosis snapshot for a single stock.
All date logic uses Beijing time (UTC+8) to ensure data freshness.

Usage:
    python stock_diagnosis.py <ts_code> [--output <file>]

Examples:
    python stock_diagnosis.py 600519.SH
    python stock_diagnosis.py 000001.SZ --output diagnosis.md
"""

import sys
import os
import argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tushare_helper import (
    TushareHelper, beijing_now, beijing_today, beijing_date_offset
)

try:
    import pandas as pd
except ModuleNotFoundError:
    print("[ERROR] Missing Python package: pandas")
    print("[ERROR] This skill does not auto-install dependencies. Install pandas manually, then rerun.")
    sys.exit(1)


def diagnose_stock(helper, ts_code, output_file=None):
    """
    Perform a structured diagnosis snapshot for a single stock.

    Args:
        helper: TushareHelper instance
        ts_code: Stock code (e.g., '600519.SH')
        output_file: Optional output file path for the report
    """
    report_lines = []

    def log(text):
        print(text)
        report_lines.append(text)

    # Use Beijing time for all date calculations
    now_bj = beijing_now()
    today = beijing_today()
    one_year_ago = beijing_date_offset(days=-365)
    three_years_ago = beijing_date_offset(days=-365 * 3)
    future_90d = beijing_date_offset(days=90)

    log(f"\n{'='*70}")
    log(f"  Stock Diagnosis Report: {ts_code}")
    log(f"  Generated: {now_bj.strftime('%Y-%m-%d %H:%M:%S')} (Beijing Time)")
    log(f"{'='*70}\n")

    # ==================== 1. Basic Information ====================
    log("## 1. Basic Information\n")

    df_company = helper.query('stock_company', {'ts_code': ts_code})
    df_basic = helper.query('stock_basic', {'ts_code': ts_code})

    if df_basic is not None and not df_basic.empty:
        row = df_basic.iloc[0]
        log(f"  Stock Code:    {row.get('ts_code', 'N/A')}")
        log(f"  Stock Name:    {row.get('name', 'N/A')}")
        log(f"  Industry:      {row.get('industry', 'N/A')}")
        log(f"  Area:          {row.get('area', 'N/A')}")
        log(f"  List Date:     {row.get('list_date', 'N/A')}")
        log(f"  Exchange:      {row.get('exchange', 'N/A')}")

    if df_company is not None and not df_company.empty:
        row = df_company.iloc[0]
        log(f"  Chairman:      {row.get('chairman', 'N/A')}")
        log(f"  Reg Capital:   {row.get('reg_capital', 'N/A')}")
        log(f"  Employees:     {row.get('employees', 'N/A')}")
        if 'introduction' in row and pd.notna(row['introduction']):
            intro = str(row['introduction'])[:200]
            log(f"  Introduction:  {intro}...")

    log("")

    # ==================== 2. Market Performance ====================
    log("## 2. Market Performance\n")

    df_daily = helper.query('daily', {
        'ts_code': ts_code,
        'start_date': one_year_ago,
        'end_date': today
    })

    if df_daily is not None and not df_daily.empty:
        df_daily = df_daily.sort_values('trade_date')
        latest = df_daily.iloc[-1]
        high_52w = df_daily['high'].max()
        low_52w = df_daily['low'].min()

        log(f"  Latest Close:       {latest.get('close', 'N/A')}")
        log(f"  Latest Change:      {latest.get('pct_chg', 'N/A')}%")
        log(f"  Latest Trade Date:  {latest.get('trade_date', 'N/A')}")
        log(f"  52-Week High:       {high_52w}")
        log(f"  52-Week Low:        {low_52w}")

        # Calculate returns
        if len(df_daily) >= 5:
            ret_5d = ((df_daily['close'].iloc[-1] / df_daily['close'].iloc[-5]) - 1) * 100
            log(f"  5-Day Return:       {ret_5d:.2f}%")
        if len(df_daily) >= 20:
            ret_20d = ((df_daily['close'].iloc[-1] / df_daily['close'].iloc[-20]) - 1) * 100
            log(f"  20-Day Return:      {ret_20d:.2f}%")
        if len(df_daily) >= 60:
            ret_60d = ((df_daily['close'].iloc[-1] / df_daily['close'].iloc[-60]) - 1) * 100
            log(f"  60-Day Return:      {ret_60d:.2f}%")

    log("")

    # ==================== 3. Valuation Metrics ====================
    log("## 3. Valuation Metrics\n")

    df_valuation = helper.query('daily_basic', {'ts_code': ts_code, 'limit': 1})

    if df_valuation is not None and not df_valuation.empty:
        row = df_valuation.iloc[0]
        log(f"  PE (TTM):           {row.get('pe_ttm', 'N/A')}")
        log(f"  PB:                 {row.get('pb', 'N/A')}")
        log(f"  PS (TTM):           {row.get('ps_ttm', 'N/A')}")
        log(f"  Dividend Yield:     {row.get('dv_ttm', 'N/A')}%")
        total_mv = row.get('total_mv', 0) or 0
        circ_mv = row.get('circ_mv', 0) or 0
        log(f"  Total MV:           {total_mv / 10000:.2f} 100m CNY")
        log(f"  Circ MV:            {circ_mv / 10000:.2f} 100m CNY")
        log(f"  Turnover Rate:      {row.get('turnover_rate', 'N/A')}%")
        log(f"  Volume Ratio:       {row.get('volume_ratio', 'N/A')}")

    log("")

    # ==================== 4. Financial Health ====================
    log("## 4. Financial Health\n")

    # Income statement
    df_income = helper.query('income', {
        'ts_code': ts_code,
        'start_date': three_years_ago,
        'end_date': today
    })

    if df_income is not None and not df_income.empty:
        df_income = df_income.sort_values('end_date', ascending=False)
        log("  ### Income Statement (Recent Periods)")
        for i, row in df_income.head(4).iterrows():
            log(f"    {row.get('end_date', 'N/A')}: Revenue={row.get('revenue', 'N/A')}, "
                f"Net Profit={row.get('net_profit', 'N/A')}")

    log("")

    # Financial indicators
    df_fina = helper.query('fina_indicator', {
        'ts_code': ts_code,
        'start_date': three_years_ago,
        'end_date': today
    })

    if df_fina is not None and not df_fina.empty:
        df_fina = df_fina.sort_values('end_date', ascending=False)
        log("  ### Key Financial Ratios (Recent Periods)")
        for i, row in df_fina.head(4).iterrows():
            log(f"    {row.get('end_date', 'N/A')}: "
                f"ROE={row.get('roe', 'N/A')}%, "
                f"Net Margin={row.get('net_profit_ratio', 'N/A')}%, "
                f"Gross Margin={row.get('gross_profit_rate', 'N/A')}%")

    log("")

    # ==================== 5. Shareholder Analysis ====================
    log("## 5. Shareholder Analysis\n")

    df_holders = helper.query('top10_holders', {'ts_code': ts_code, 'limit': 10})

    if df_holders is not None and not df_holders.empty:
        log("  ### Top 10 Shareholders")
        for i, row in df_holders.head(10).iterrows():
            log(f"    {row.get('holder_name', 'N/A')}: "
                f"{row.get('hold_ratio', 'N/A')}%")

    # Shareholder count trend
    df_holdernum = helper.query('stk_holdernumber', {
        'ts_code': ts_code,
        'start_date': one_year_ago,
        'end_date': today
    })

    if df_holdernum is not None and not df_holdernum.empty:
        df_holdernum = df_holdernum.sort_values('end_date', ascending=False)
        log("\n  ### Shareholder Count Trend")
        for i, row in df_holdernum.head(4).iterrows():
            log(f"    {row.get('end_date', 'N/A')}: {row.get('holder_num', 'N/A')} holders")

    log("")

    # ==================== 6. Capital Flow ====================
    log("## 6. Capital Flow\n")

    df_flow = helper.query('moneyflow', {
        'ts_code': ts_code,
        'start_date': beijing_date_offset(days=-30),
        'end_date': today
    })

    if df_flow is not None and not df_flow.empty:
        df_flow = df_flow.sort_values('trade_date', ascending=False)
        log("  ### Recent Money Flow (Last 5 Trading Days)")
        for i, row in df_flow.head(5).iterrows():
            log(f"    {row.get('trade_date', 'N/A')}: "
                f"Main Net={row.get('net_inflow_main', 'N/A')}, "
                f"Large Net={row.get('net_inflow_large', 'N/A')}")

    log("")

    # ==================== 7. Risk Assessment ====================
    log("## 7. Risk Assessment\n")

    # ST status
    df_st = helper.query('stock_st', {'ts_code': ts_code})
    if df_st is not None and not df_st.empty:
        log("  [WARNING] This stock has ST history!")
        for i, row in df_st.iterrows():
            log(f"    ST Date: {row.get('st_date', 'N/A')}, End: {row.get('end_date', 'N/A')}")
    else:
        log("  [OK] No ST history.")

    # Pledge status
    df_pledge = helper.query('pledge_stat', {'ts_code': ts_code})
    if df_pledge is not None and not df_pledge.empty:
        row = df_pledge.iloc[0]
        pledge_ratio = row.get('pledge_ratio', 0)
        log(f"  Pledge Ratio: {pledge_ratio}%")
        if pledge_ratio and float(pledge_ratio) > 50:
            log("  [WARNING] High pledge ratio!")
    else:
        log("  [OK] No significant pledge data.")

    # Restricted shares
    df_restricted = helper.query('share_float', {
        'ts_code': ts_code,
        'start_date': today,
        'end_date': future_90d
    })
    if df_restricted is not None and not df_restricted.empty:
        log(f"  [WARNING] Upcoming restricted share unlocks in next 90 days: {len(df_restricted)} events")
    else:
        log("  [OK] No upcoming restricted share unlocks in next 90 days.")

    log("")

    # ==================== 8. Summary ====================
    log("## 8. Summary\n")
    log(f"  Report date (Beijing time): {now_bj.strftime('%Y-%m-%d %H:%M:%S')}")
    log("  This report provides a structured, data-driven snapshot of the stock.")
    log("  For decision support, combine this with external news/industry/global event intelligence.")
    log("  This built-in report does not generate an automatic buy/sell rating.")
    log("  Investment decisions should not be based solely on this report.")
    log(f"\n{'='*70}\n")

    # Save report
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        print(f"\n[INFO] Report saved to {output_file}")

    return '\n'.join(report_lines)


def main():
    parser = argparse.ArgumentParser(description="Structured stock diagnosis snapshot tool")
    parser.add_argument("ts_code", help="Stock code (e.g., 600519.SH)")
    parser.add_argument("--output", "-o", default=None, help="Output file path")

    args = parser.parse_args()

    helper = TushareHelper()
    diagnose_stock(helper, args.ts_code, args.output)


if __name__ == '__main__':
    main()
