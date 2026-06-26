#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tushare Pro API Helper Script

This script provides a robust interface to the Tushare Pro API.
It handles initialization, retries, error handling, and automatic
Beijing time (UTC+8) date resolution to keep data fresh.

Usage:
    python tushare_helper.py <api_name> '<json_params>'

Examples:
    python tushare_helper.py stock_basic '{"exchange": "SSE", "list_status": "L", "limit": 10}'
    python tushare_helper.py daily '{"ts_code": "000001.SZ", "start_date": "20240101", "end_date": "20240131"}'
    python tushare_helper.py fina_indicator '{"ts_code": "600519.SH"}'
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

MISSING_PACKAGES = []

try:
    import pandas as pd
except ModuleNotFoundError:
    pd = None
    MISSING_PACKAGES.append("pandas")

try:
    import tushare as ts
except ModuleNotFoundError:
    ts = None
    MISSING_PACKAGES.append("tushare")

TUSHARE_ENV_VARS = ("TUSHARE_TOKEN", "TUSHARE_PRO_TOKEN")

# Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds between retries
REQUEST_INTERVAL = 0.5  # minimum interval between API calls (rate limiting)

# Beijing timezone (UTC+8)
BEIJING_TZ = timezone(timedelta(hours=8))


# ============================================================
# Beijing Time Date Utilities
# ============================================================

def beijing_now():
    """Return the current datetime in Beijing time (UTC+8)."""
    return datetime.now(BEIJING_TZ)


def beijing_today(fmt='%Y%m%d'):
    """Return today's date string in Beijing time. Default format: YYYYMMDD."""
    return beijing_now().strftime(fmt)


def beijing_date_offset(days=0, fmt='%Y%m%d'):
    """Return a date string offset by `days` from today in Beijing time."""
    return (beijing_now() + timedelta(days=days)).strftime(fmt)


def ensure_runtime_dependencies():
    """Exit with a clear message when required runtime packages are missing."""
    if not MISSING_PACKAGES:
        return
    missing = ", ".join(MISSING_PACKAGES)
    print(f"[ERROR] Missing Python packages: {missing}")
    print("[ERROR] This skill does not auto-install dependencies. Install the missing packages manually, then rerun.")
    sys.exit(1)


def resolve_tushare_token(explicit_token=None):
    """Resolve the Tushare token from an explicit value or environment variables."""
    if explicit_token:
        return explicit_token

    for env_name in TUSHARE_ENV_VARS:
        env_value = os.getenv(env_name)
        if env_value and env_value.strip():
            return env_value.strip()

    raise ValueError(
        "Missing Tushare token. Set the TUSHARE_TOKEN environment variable, or configure skills.entries.quant-expert.apiKey in OpenClaw so it maps into TUSHARE_TOKEN."
    )


def get_latest_trade_date(pro, exchange='SSE', fallback_days=15):
    """
    Query the Tushare trade calendar to find the most recent trading date
    as of today (Beijing time). If the market has not yet closed today
    (before 15:30 Beijing time), the previous trading date is returned.

    Args:
        pro: Tushare pro_api instance
        exchange: Exchange code (default SSE)
        fallback_days: How many days back to search

    Returns:
        str: Latest trade date in YYYYMMDD format
    """
    now_bj = beijing_now()
    today_str = now_bj.strftime('%Y%m%d')
    start_str = (now_bj - timedelta(days=fallback_days)).strftime('%Y%m%d')

    try:
        df = pro.trade_cal(
            exchange=exchange,
            start_date=start_str,
            end_date=today_str,
            is_open='1'
        )
    except Exception as exc:
        raise RuntimeError(f"Failed to query the Tushare trade calendar: {exc}") from exc

    if df is None or df.empty:
        raise RuntimeError("Trade calendar query returned no open-market dates.")

    df = df.sort_values('cal_date', ascending=False)

    # If current time is before 15:30, today's data is not yet available
    market_close = now_bj.replace(hour=15, minute=30, second=0, microsecond=0)
    if now_bj < market_close:
        df = df[df['cal_date'] < today_str]

    if df.empty:
        raise RuntimeError("Unable to resolve the latest trading date from the trade calendar.")

    return df['cal_date'].iloc[0]


def print_beijing_time_info():
    """Print current Beijing time information for transparency."""
    now = beijing_now()
    print(f"[TIME] Current Beijing time: {now.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)")


# ============================================================
# TushareHelper Class
# ============================================================

class TushareHelper:
    """Helper class for interacting with the Tushare Pro API."""

    def __init__(self, token=None, show_time=True):
        ensure_runtime_dependencies()
        self.token = resolve_tushare_token(token)
        self.pro = ts.pro_api(self.token)
        self._last_call_time = 0
        if show_time:
            print_beijing_time_info()

    def _rate_limit(self):
        """Enforce minimum interval between API calls."""
        elapsed = time.time() - self._last_call_time
        if elapsed < REQUEST_INTERVAL:
            time.sleep(REQUEST_INTERVAL - elapsed)
        self._last_call_time = time.time()

    def get_today(self):
        """Get today's date in Beijing time (YYYYMMDD)."""
        return beijing_today()

    def get_latest_trade_date(self):
        """Get the most recent trading date considering Beijing time and market hours."""
        return get_latest_trade_date(self.pro)

    def query(self, api_name, params=None, fields=None, retry=MAX_RETRIES):
        """
        Execute a Tushare API query with retry logic.

        Args:
            api_name (str): API name (e.g., 'daily', 'income')
            params (dict): Parameters for the API call
            fields (str or list): Specific fields to return (optional)
            retry (int): Number of retries on failure

        Returns:
            pd.DataFrame or None
        """
        if params is None:
            params = {}

        # Add fields parameter if specified
        if fields:
            if isinstance(fields, list):
                params['fields'] = ','.join(fields)
            else:
                params['fields'] = fields

        for attempt in range(retry + 1):
            try:
                self._rate_limit()
                api_func = getattr(self.pro, api_name)
                df = api_func(**params)
                if df is not None and not df.empty:
                    return df
                elif df is not None and df.empty:
                    print(f"[INFO] API '{api_name}' returned empty DataFrame.")
                    return df
                else:
                    print(f"[WARN] API '{api_name}' returned None.")
                    return pd.DataFrame()
            except AttributeError:
                print(f"[ERROR] API '{api_name}' does not exist in Tushare Pro.")
                return None
            except Exception as e:
                if attempt < retry:
                    wait = RETRY_DELAY * (attempt + 1)
                    print(f"[WARN] Attempt {attempt + 1} failed: {e}. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"[ERROR] All {retry + 1} attempts failed for API '{api_name}': {e}")
                    return None

    def query_latest(self, api_name, params=None, fields=None, date_field='trade_date'):
        """
        Execute a query using the latest available trading date (Beijing time).
        Automatically fills the date_field parameter with the most recent trade date.

        Args:
            api_name (str): API name
            params (dict): Parameters (date_field will be auto-filled if not present)
            fields (str or list): Fields to return
            date_field (str): Name of the date parameter to auto-fill (default: 'trade_date')

        Returns:
            pd.DataFrame or None
        """
        if params is None:
            params = {}

        if date_field not in params or not params[date_field]:
            latest = self.get_latest_trade_date()
            params[date_field] = latest
            print(f"[INFO] Auto-filled {date_field} = {latest} (latest trading date, Beijing time)")

        return self.query(api_name, params, fields)

    def batch_query(self, api_name, ts_codes, params_template=None, delay=0.3):
        """
        Query the same API for multiple stock codes and concatenate results.

        Args:
            api_name (str): API name
            ts_codes (list): List of stock codes
            params_template (dict): Base parameters (ts_code will be added)
            delay (float): Delay between calls in seconds

        Returns:
            pd.DataFrame
        """
        if params_template is None:
            params_template = {}

        results = []
        total = len(ts_codes)
        for i, code in enumerate(ts_codes):
            params = {**params_template, 'ts_code': code}
            df = self.query(api_name, params)
            if df is not None and not df.empty:
                results.append(df)
            if i < total - 1:
                time.sleep(delay)
            if (i + 1) % 50 == 0:
                print(f"[INFO] Progress: {i + 1}/{total}")

        if results:
            return pd.concat(results, ignore_index=True)
        return pd.DataFrame()


def main():
    parser = argparse.ArgumentParser(
        description="Tushare Pro API Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s stock_basic '{"exchange": "SSE", "list_status": "L", "limit": 5}'
  %(prog)s daily '{"ts_code": "000001.SZ", "start_date": "20240101", "end_date": "20240131"}'
  %(prog)s fina_indicator '{"ts_code": "600519.SH"}'
  %(prog)s daily_basic '{"trade_date": "20240301"}'
        """
    )
    parser.add_argument("api_name", help="Tushare API name (e.g., daily, income, stock_basic)")
    parser.add_argument("params", nargs='?', default='{}',
                        help="JSON string of parameters (default: {})")
    parser.add_argument("--fields", "-f", default=None,
                        help="Comma-separated list of fields to return")
    parser.add_argument("--output", "-o", default=None,
                        help="Output file path (CSV format)")
    parser.add_argument("--head", "-n", type=int, default=None,
                        help="Only show first N rows")

    args = parser.parse_args()

    # Parse parameters
    try:
        params_dict = json.loads(args.params)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON parameters: {e}")
        sys.exit(1)

    ensure_runtime_dependencies()

    try:
        helper = TushareHelper()
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)

    # Execute query
    df = helper.query(args.api_name, params_dict, fields=args.fields)

    if df is None:
        print("[ERROR] Query failed.")
        sys.exit(1)

    if df.empty:
        print("[INFO] No data returned.")
        sys.exit(0)

    # Apply head limit
    if args.head:
        df = df.head(args.head)

    # Output
    if args.output:
        df.to_csv(args.output, index=False, encoding='utf-8-sig')
        print(f"[INFO] Data saved to {args.output} ({len(df)} rows)")
    else:
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 30)
        print(df.to_string(index=False))
        print(f"\n[INFO] Total rows: {len(df)}")


if __name__ == '__main__':
    main()
