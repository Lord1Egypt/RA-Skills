#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chinese Holiday & Trading Day Helper Script

Uses the free timor.tech Holiday API to determine whether a given date
is a trading day for the Chinese A-share stock market.

Trading day logic:
  - A trading day is a normal workday (type=0) or a make-up workday (type=3).
  - Non-trading days include weekends (type=1) and public holidays (type=2).

API source: https://timor.tech/api/holiday/

Usage (CLI):
    # Check if a specific date is a trading day
    python holiday_helper.py check 2026-03-06

    # Check today (Beijing time)
    python holiday_helper.py check

    # Get the next trading day after a date (exclusive)
    python holiday_helper.py next 2026-03-06

    # Get the next trading day after today
    python holiday_helper.py next

    # List all holidays in a given year
    python holiday_helper.py year 2026

    # List all non-trading days in a given month
    python holiday_helper.py month 2026-03

Usage (as module):
    from holiday_helper import HolidayHelper
    hh = HolidayHelper()
    hh.is_trading_day('2026-03-06')   # True / False
    hh.next_trading_day('2026-03-06') # '2026-03-09'
    hh.date_info('2026-03-06')        # dict with full info
"""

import sys
import time
import argparse
from datetime import datetime, timedelta, timezone

try:
    import requests
except ModuleNotFoundError:
    print("[ERROR] Missing Python package: requests")
    print("[ERROR] This skill does not auto-install dependencies. Install requests manually, then rerun.")
    sys.exit(1)

# Beijing timezone (UTC+8)
BEIJING_TZ = timezone(timedelta(hours=8))

API_BASE = "https://timor.tech/api/holiday"

# Type mapping
TYPE_MAP = {
    0: "Workday",
    1: "Weekend",
    2: "Public Holiday",
    3: "Make-up Workday",
}


def _beijing_now():
    """Return the current datetime in Beijing time (UTC+8)."""
    return datetime.now(BEIJING_TZ)


def _beijing_today_str():
    """Return today's date string in Beijing time, format: YYYY-MM-DD."""
    return _beijing_now().strftime('%Y-%m-%d')


def _normalize_date(date_str):
    """
    Normalize a date string to YYYY-MM-DD format.
    Accepts: YYYYMMDD, YYYY-MM-DD, YYYY/MM/DD.
    """
    if date_str is None:
        return _beijing_today_str()
    date_str = date_str.strip().replace('/', '-')
    if len(date_str) == 8 and date_str.isdigit():
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    return date_str


class HolidayHelper:
    """Helper class for querying Chinese holiday / trading day information."""

    def __init__(self, timeout=10, max_retries=3):
        self.timeout = timeout
        self.max_retries = max_retries
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (QuantExpert/1.0)'
        })
        self._last_call_time = 0
        self._min_interval = 0.6  # seconds between API calls

    def _rate_limit(self):
        """Enforce minimum interval between API calls to avoid 429."""
        elapsed = time.time() - self._last_call_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_call_time = time.time()

    def _get_json(self, url):
        """GET request with automatic retry on 429 rate-limit errors."""
        for attempt in range(self.max_retries + 1):
            self._rate_limit()
            resp = self._session.get(url, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            if data.get('code') == 429:
                if attempt < self.max_retries:
                    wait = 2 * (attempt + 1)
                    print(f"[WARN] 429 rate limited, retrying in {wait}s... ({attempt+1}/{self.max_retries})")
                    time.sleep(wait)
                    continue
                else:
                    raise RuntimeError(f"API rate limited after {self.max_retries} retries: {data}")
            return data
        return data  # fallback

    # ------------------------------------------------------------------
    # Core API calls
    # ------------------------------------------------------------------

    def date_info(self, date_str=None):
        """
        Get holiday information for a specific date.

        Args:
            date_str: Date string (YYYYMMDD or YYYY-MM-DD). None = today.

        Returns:
            dict with keys: date, type_code, type_name, is_holiday,
                            holiday_name, is_trading_day, week
        """
        date_str = _normalize_date(date_str)
        url = f"{API_BASE}/info/{date_str}"
        data = self._get_json(url)

        if data.get('code') != 0:
            raise RuntimeError(f"API error: {data}")

        type_info = data.get('type', {})
        holiday_info = data.get('holiday')

        type_code = type_info.get('type', -1)
        result = {
            'date': date_str,
            'type_code': type_code,
            'type_name': TYPE_MAP.get(type_code, 'Unknown'),
            'week_day': type_info.get('week', -1),
            'week_name': type_info.get('name', ''),
            'is_holiday': holiday_info is not None and holiday_info.get('holiday', False),
            'holiday_name': holiday_info.get('name', '') if holiday_info else '',
            'is_trading_day': type_code in (0, 3),  # workday or make-up workday
        }
        return result

    def is_trading_day(self, date_str=None):
        """
        Check if a date is a trading day.

        Args:
            date_str: Date string (YYYYMMDD or YYYY-MM-DD). None = today.

        Returns:
            bool: True if the date is a trading day.
        """
        info = self.date_info(date_str)
        return info['is_trading_day']

    def next_trading_day(self, date_str=None):
        """
        Get the next trading day after the given date (exclusive).

        Uses the timor.tech /workday/next API which returns the next
        workday (normal workday or make-up workday), excluding the given date.

        Args:
            date_str: Date string (YYYYMMDD or YYYY-MM-DD). None = today.

        Returns:
            str: Next trading day in YYYY-MM-DD format.
        """
        date_str = _normalize_date(date_str)
        url = f"{API_BASE}/workday/next/{date_str}"
        data = self._get_json(url)

        if data.get('code') != 0:
            raise RuntimeError(f"API error: {data}")

        workday = data.get('workday')
        if workday and 'date' in workday:
            return workday['date']
        raise RuntimeError("No next workday found within 30 days.")

    def year_holidays(self, year=None, include_weekends=False):
        """
        Get all holidays for a given year.

        Args:
            year: Year string or int (e.g., 2026). None = current year.
            include_weekends: Whether to include regular weekends.

        Returns:
            list of dict: Each dict has date, name, holiday (bool), wage.
        """
        if year is None:
            year = _beijing_now().year
        week_param = 'Y' if include_weekends else 'N'
        url = f"{API_BASE}/year/{year}/?type=Y&week={week_param}"
        data = self._get_json(url)

        if data.get('code') != 0:
            raise RuntimeError(f"API error: {data}")

        holidays = data.get('holiday', {})
        type_info = data.get('type', {})
        results = []
        for key, val in sorted(holidays.items()):
            entry = {
                'date_key': key,
                'name': val.get('name', ''),
                'is_holiday': val.get('holiday', False),
                'wage': val.get('wage', 1),
                'date': val.get('date', ''),
            }
            # Add type info if available
            full_date = val.get('date', '')
            if full_date in type_info:
                t = type_info[full_date]
                entry['type_code'] = t.get('type', -1)
                entry['type_name'] = TYPE_MAP.get(t.get('type', -1), 'Unknown')
            results.append(entry)
        return results

    def month_non_trading_days(self, year_month=None):
        """
        Get all non-trading days for a given month.

        Args:
            year_month: Format 'YYYY-MM'. None = current month.

        Returns:
            list of dict with date, type_name, holiday_name.
        """
        if year_month is None:
            now = _beijing_now()
            year_month = now.strftime('%Y-%m')

        url = f"{API_BASE}/year/{year_month}?type=Y&week=Y"
        data = self._get_json(url)

        if data.get('code') != 0:
            raise RuntimeError(f"API error: {data}")

        holidays = data.get('holiday', {})
        type_info = data.get('type', {})

        results = []
        for key, val in sorted(holidays.items()):
            full_date = val.get('date', '')
            t_code = -1
            if full_date in type_info:
                t_code = type_info[full_date].get('type', -1)
            # Non-trading: type 1 (weekend) or type 2 (holiday)
            if t_code in (1, 2):
                results.append({
                    'date': full_date,
                    'type_code': t_code,
                    'type_name': TYPE_MAP.get(t_code, 'Unknown'),
                    'name': val.get('name', ''),
                })
        return results

    def trading_days_range(self, start_date, end_date):
        """
        Get all trading days in a date range by batch-checking.
        Uses the batch API for efficiency (max 50 dates per call).

        Args:
            start_date: Start date (YYYYMMDD or YYYY-MM-DD), inclusive.
            end_date: End date (YYYYMMDD or YYYY-MM-DD), inclusive.

        Returns:
            list of str: Trading day dates in YYYY-MM-DD format.
        """
        start = datetime.strptime(_normalize_date(start_date), '%Y-%m-%d')
        end = datetime.strptime(_normalize_date(end_date), '%Y-%m-%d')

        all_dates = []
        current = start
        while current <= end:
            all_dates.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)

        trading_days = []
        # Batch API supports max 50 dates per call
        batch_size = 50
        for i in range(0, len(all_dates), batch_size):
            batch = all_dates[i:i + batch_size]
            d_params = '&'.join([f'd={d}' for d in batch])
            url = f"{API_BASE}/batch?{d_params}&type=Y"
            data = self._get_json(url)

            if data.get('code') != 0:
                raise RuntimeError(f"API error: {data}")

            type_data = data.get('type', {})
            for d in batch:
                t = type_data.get(d, {})
                t_code = t.get('type', -1) if isinstance(t, dict) else -1
                if t_code in (0, 3):  # workday or make-up workday
                    trading_days.append(d)

        return trading_days


# ==================================================================
# CLI Interface
# ==================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Chinese Holiday & Trading Day Helper (timor.tech API)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  check [DATE]   Check if a date is a trading day (default: today)
  next  [DATE]   Get the next trading day after a date (default: today)
  year  [YEAR]   List all holidays in a year (default: current year)
  month [YYYY-MM] List non-trading days in a month (default: current month)
  range START END List all trading days in a date range

Date formats: YYYYMMDD, YYYY-MM-DD

Examples:
  %(prog)s check 2026-03-06
  %(prog)s check 20260306
  %(prog)s next
  %(prog)s year 2026
  %(prog)s month 2026-03
  %(prog)s range 2026-03-01 2026-03-31
        """
    )
    parser.add_argument("command", choices=["check", "next", "year", "month", "range"],
                        help="Command to execute")
    parser.add_argument("args", nargs='*', help="Command arguments")

    args = parser.parse_args()
    hh = HolidayHelper()

    # Print current Beijing time
    now = _beijing_now()
    print(f"[TIME] Current Beijing time: {now.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)")

    try:
        if args.command == 'check':
            date_str = args.args[0] if args.args else None
            info = hh.date_info(date_str)
            trading = info['is_trading_day']
            status = "Yes - Trading Day" if trading else "No - Non-trading Day"
            print(f"\nDate: {info['date']}")
            print(f"Type: {info['type_name']} (code={info['type_code']})")
            print(f"Weekday: {info['week_name']}")
            if info['holiday_name']:
                print(f"Holiday: {info['holiday_name']}")
            print(f"Trading Day: {status}")

        elif args.command == 'next':
            date_str = args.args[0] if args.args else None
            from_date = _normalize_date(date_str)
            next_day = hh.next_trading_day(date_str)
            print(f"\nQuery Date: {from_date}")
            print(f"Next Trading Day: {next_day}")

        elif args.command == 'year':
            year = args.args[0] if args.args else None
            holidays = hh.year_holidays(year)
            print(f"\nHoliday / Make-up Workday List for {year or _beijing_now().year}:\n")
            print(f"{'Date':<14} {'Name':<18} {'Type':<18} {'Holiday':<10} {'Pay Multiplier'}")
            print("-" * 60)
            for h in holidays:
                is_off = "Holiday" if h['is_holiday'] else "Make-up Day"
                t_name = h.get('type_name', '')
                print(f"{h.get('date', h['date_key']):<14} {h['name']:<18} {t_name:<18} {is_off:<10} {h['wage']}x")
            print(f"\nTotal records: {len(holidays)}")

        elif args.command == 'month':
            ym = args.args[0] if args.args else None
            days = hh.month_non_trading_days(ym)
            print(f"\nNon-trading Days for {ym or _beijing_now().strftime('%Y-%m')}:\n")
            print(f"{'Date':<14} {'Type':<18} {'Name'}")
            print("-" * 40)
            for d in days:
                print(f"{d['date']:<14} {d['type_name']:<18} {d['name']}")
            print(f"\nTotal non-trading days: {len(days)}")

        elif args.command == 'range':
            if len(args.args) < 2:
                print("[ERROR] The range command requires two arguments: START END")
                sys.exit(1)
            start, end = args.args[0], args.args[1]
            days = hh.trading_days_range(start, end)
            print(f"\nTrading days from {_normalize_date(start)} to {_normalize_date(end)}:\n")
            for d in days:
                print(f"  {d}")
            print(f"\nTotal trading days: {len(days)}")

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
