#!/usr/bin/env python3
"""
fetch_stock_data.py - 股票数据拉取模块
支持：US（Yahoo Finance）、HK（Yahoo Finance）、CN（Tushare）
"""

import os
import sys
import time
import json
import warnings
warnings.filterwarnings('ignore')

# ── 代理设置（WSL 环境） ──────────────────────────────────────────
os.environ['HTTPS_PROXY'] = os.environ.get('HTTPS_PROXY', 'http://172.30.192.1:7890')
os.environ['HTTP_PROXY'] = os.environ.get('HTTP_PROXY', 'http://172.30.192.1:7890')
# ─────────────────────────────────────────────────────────────────

MARKET_CONFIGS = {
    'US': {'source': 'yfinance', 'yfinance_ticker': None},   # ticker 直接用
    'HK': {'source': 'yfinance', 'yfinance_ticker': None},   # ticker 加 .HK
    'CN': {'source': 'tushare',  'ts_token': os.environ.get('TUSHARE_TOKEN', '')},
}

CURRENCY_SYMBOL = {'US': '$', 'HK': 'HK$', 'CN': '¥'}
CURRENCY_NAME   = {'US': 'USD', 'HK': 'HKD', 'CN': 'CNY'}


def _fetch_yfinance(ticker: str, retries: int = 3) -> dict:
    """从 Yahoo Finance 拉取数据，重试机制"""
    import yfinance as yf

    for attempt in range(retries):
        try:
            tk = yf.Ticker(ticker)
            info = tk.info or {}
            hist = tk.history(period="2y")

            # 财务报表（年报）
            try:
                income_stmt = tk.income_stmt
                if income_stmt is not None and not income_stmt.empty:
                    # DataFrame: index=指标名, columns=日期，转换为 {指标名: {日期: 值}}
                    income_stmt = income_stmt.to_dict('index')
            except Exception:
                income_stmt = None

            try:
                balance_sheet = tk.balance_sheet
                if balance_sheet is not None and not balance_sheet.empty:
                    balance_sheet = balance_sheet.to_dict('index')
            except Exception:
                balance_sheet = None

            try:
                cashflow = tk.cashflow
                if cashflow is not None and not cashflow.empty:
                    cashflow = cashflow.to_dict('index')
            except Exception:
                cashflow = None

            return {
                'info': info,
                'hist': hist.to_dict() if hist is not None else None,
                'income_stmt': income_stmt,
                'balance_sheet': balance_sheet,
                'cashflow': cashflow,
            }
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            raise


def _fetch_tushare(ts_code: str, retries: int = 3) -> dict:
    """从 Tushare 拉取 A 股数据"""
    import tushare as ts

    token = os.environ.get('TUSHARE_TOKEN', '')
    if not token:
        raise ValueError("TUSHARE_TOKEN 环境变量未设置，请设置后再试")
    pro = ts.pro_api(token)

    for attempt in range(retries):
        try:
            # 基本信息
            basic_df = pro.stock_basic(ts_code=ts_code, fields='ts_code,symbol,name,area,industry,list_date')
            info = {}
            if basic_df is not None and len(basic_df) > 0:
                row = basic_df.iloc[0]
                info = {
                    'longBusinessSummary': f"{row.get('name','')} ({row.get('area','')}) - {row.get('industry','')}",
                    'industry': row.get('industry', ''),
                    'sector': row.get('area', ''),
                    'market': 'CN',
                }

            # 财务指标（多期）
            time.sleep(1)  # 避免触发前一次调用的残留限流
            indicator_df = pro.fina_indicator(ts_code=ts_code, period_type='Q', count=8)
            indicators = []
            if indicator_df is not None and len(indicator_df) > 0:
                cols = ['ann_date','end_date','roe','roa','gross_margin','net_margin',
                        'eps','bps','debt_to_assets','current_ratio','quick_ratio',
                        'revenue','profit','netprofit_ratio','inc_revenue','inc_profit']
                existing = [c for c in cols if c in indicator_df.columns]
                indicators = indicator_df[existing].to_dict('records')

            # 日K线
            daily_df = pro.daily(ts_code=ts_code, start_date='20250501', end_date='20991231')
            hist = None
            if daily_df is not None and len(daily_df) > 0:
                hist_df = daily_df.sort_values('trade_date')
                hist = {
                    'Close': {row['trade_date']: row['close'] for _, row in hist_df.iterrows()}
                }

            return {
                'info': info,
                'hist': hist,
                'indicators': indicators,
            }
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(65)  # Tushare 限流等待
                continue
            raise


def fetch_stock_data(ticker: str, market: str = 'US') -> dict:
    """
    统一数据拉取接口
    :param ticker: 股票代码（美股如 PDD，港股如 0700.HK，A股如 600141.SH）
    :param market: 'US' | 'HK' | 'CN'
    :return: dict 包含 info, hist, financial statements
    """
    market = market.upper()
    if market not in MARKET_CONFIGS:
        raise ValueError(f"不支持的市场: {market}，支持：US/HK/CN")

    if market == 'CN':
        return _fetch_tushare(ticker)
    else:
        yf_ticker = ticker if market == 'US' else f"{ticker}.HK"
        return _fetch_yfinance(yf_ticker)


if __name__ == '__main__':
    import json
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'PDD'
    market = sys.argv[2].upper() if len(sys.argv) > 2 else 'US'
    data = fetch_stock_data(ticker, market)
    print(json.dumps(data, default=str, ensure_ascii=False))