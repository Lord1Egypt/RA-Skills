"""Offline fixtures prove that unavailable or malformed data never becomes a stock conclusion."""
import importlib.util
from datetime import datetime, date, timedelta
from pathlib import Path
import unittest
import pandas as pd

spec = importlib.util.spec_from_file_location("s", Path(__file__).parents[1] / "scripts/stock_analyzer.py")
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
NOW = datetime(2026, 9, 5, 10, tzinfo=s.TZ)
CAL = ["2026-09-03", "2026-09-04", "2026-09-07"]

def bars(n=260):
    start = date(2026, 9, 4) - timedelta(days=n - 1)
    return pd.DataFrame([{"date": (start + timedelta(days=i)).isoformat(), "open": 100+i*.1,
                          "high": 101+i*.1, "low": 99+i*.1, "close": 100+i*.1, "volume": 1000+i}
                         for i in range(n)])

class API:
    def tool_trade_date_hist_sina(self): return pd.DataFrame({"trade_date": CAL})
    def stock_zh_a_daily(self, **kwargs): return bars()
    def stock_zh_a_hist(self, **kwargs):
        return bars().rename(columns={"date":"日期","open":"开盘","high":"最高","low":"最低","close":"收盘","volume":"成交量"})

class Tests(unittest.TestCase):
    def test_valid_symbol_only(self):
        for bad in ["60093", "sh600938", "ABCDEF", "6009387"]:
            with self.assertRaises(ValueError): s.valid_symbol(bad)

    def test_all_sources_fail(self):
        class Broken(API):
            def stock_zh_a_daily(self, **k): raise RuntimeError()
            def stock_zh_a_hist(self, **k): raise RuntimeError()
        out=s.collect(Broken(),"600938",now=NOW)
        self.assertEqual(out["status"],"unavailable")
        self.assertIsNone(out["trade_date"])
        self.assertNotIn("推荐", out["conclusion"])

    def test_calendar_fail(self):
        class Broken(API):
            def tool_trade_date_hist_sina(self): raise RuntimeError()
        self.assertEqual(s.collect(Broken(),"600938",now=NOW)["status"],"unavailable")

    def test_success_partial(self):
        out=s.collect(API(),"600938",now=NOW)
        self.assertEqual(out["status"],"partial")
        self.assertEqual(out["trade_date"],"2026-09-04")
        self.assertIn("新浪",out["source"])
        self.assertIn("实时行情",out["missing"])
        self.assertNotIn("score",out)

    def test_eastmoney_fallback(self):
        class Fallback(API):
            def stock_zh_a_daily(self, **k): raise RuntimeError()
        out=s.collect(Fallback(),"600938",now=NOW)
        self.assertEqual(out["status"],"partial")
        self.assertIn("东方财富",out["source"])

    def test_empty_data(self):
        class Empty(API):
            def stock_zh_a_daily(self, **k): return pd.DataFrame()
            def stock_zh_a_hist(self, **k): return pd.DataFrame()
        self.assertEqual(s.collect(Empty(),"600938",now=NOW)["status"],"unavailable")

    def test_duplicate_date(self):
        frame=bars(2); frame.loc[1,"date"]=frame.loc[0,"date"]
        with self.assertRaises(ValueError): s.normalize_rows(frame,"sina")

    def test_nan_and_ohlc_rejected(self):
        frame=bars(2); frame.loc[1,"close"]=float("nan")
        with self.assertRaises(ValueError): s.normalize_rows(frame,"sina")
        frame=bars(2); frame.loc[1,"high"]=1
        with self.assertRaises(ValueError): s.normalize_rows(frame,"sina")

    def test_weekend_and_future_rejected(self):
        self.assertEqual(s.collect(API(),"600938","2026-09-05",NOW)["status"],"unavailable")
        self.assertEqual(s.collect(API(),"600938","2026-09-07",NOW)["status"],"unavailable")

    def test_stale_calendar_rejected(self):
        class Stale(API):
            def tool_trade_date_hist_sina(self): return pd.DataFrame({"trade_date":CAL[:2]})
        self.assertEqual(s.collect(Stale(),"600938",now=NOW)["status"],"unavailable")

    def test_missing_target_day_rejected(self):
        class Gap(API):
            def stock_zh_a_daily(self, **k): return bars().query("date != '2026-09-04'")
            def stock_zh_a_hist(self, **k): return pd.DataFrame()
        self.assertEqual(s.collect(Gap(),"600938",now=NOW)["status"],"unavailable")

    def test_insufficient_history_does_not_invent_ma(self):
        class Short(API):
            def stock_zh_a_daily(self, **k):
                return pd.DataFrame([{"date":"2026-09-03","open":100,"high":101,"low":99,"close":100,"volume":1},{"date":"2026-09-04","open":100,"high":101,"low":99,"close":101,"volume":1}])
        out=s.collect(Short(),"600938",now=NOW)
        self.assertEqual(out["status"],"partial")
        self.assertIsNone(out["observation"]["ma250"])
        self.assertIsNone(out["observation"]["rsi14"])

    def test_premarket_uses_previous_completed_day(self):
        target,_=s.select_day(CAL,None,datetime(2026,9,7,8,30,tzinfo=s.TZ))
        self.assertEqual(target,date(2026,9,4))

if __name__ == "__main__": unittest.main()
