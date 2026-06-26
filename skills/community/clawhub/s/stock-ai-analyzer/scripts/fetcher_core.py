#!/usr/bin/env python3
"""Core data fetcher: StockDataFetcher wraps Tushare Pro and CNInfo APIs."""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

try:
    import requests
except ImportError:
    requests = None

from cache import JsonTTLCache
from cninfo import (
    DEFAULT_CNINFO_PAGE_SIZE,
    DEFAULT_CNINFO_TIMEOUT,
    CNINFO_ALLOWED_TAB_TYPES,
    CNINFO_REPORT_CATEGORIES,
    CNINFO_REPORT_TYPES,
    announcement_needs_original_text,
    build_cninfo_url,
    build_report_date_range,
    classify_cninfo_fulltext,
    classify_cninfo_relation,
    classify_report_title,
    cninfo_headers,
    report_sort_key,
    require_requests,
    validate_cninfo_date_range,
)
from common import (
    classify_board,
    dataframe_to_records,
    normalize_ts_code,
    normalize_yyyymmdd,
    sanitize_filename,
    _num,
)
from pdf_extractor import extract_pdf_text
from retry import request_with_retry
from tushare_client import _TushareProxy, get_tushare_pro

class StockDataFetcher:
    """Atomic data access wrapper around Tushare Pro."""

    def __init__(self, token: Optional[str] = None, cache_dir: Optional[str] = None):
        self.pro = _TushareProxy(get_tushare_pro(token))
        self._stock_list_cache: Optional[pd.DataFrame] = None
        self._cache = JsonTTLCache(Path(cache_dir or os.path.join(os.getcwd(), ".cache", "a_stock_analyzer")))
        self._session = require_requests().Session() if requests else None

    def get_all_stocks(self) -> pd.DataFrame:
        """Fetch listed A-share stocks (cached 24h)."""
        if self._stock_list_cache is not None:
            return self._stock_list_cache

        cached = self._cache.get("stock_basic:list_status=L", 86400)
        if cached is not None:
            self._stock_list_cache = pd.DataFrame(cached)
            return self._stock_list_cache

        df = self.pro.stock_basic(
            list_status="L",
            fields="ts_code,symbol,name,area,industry,market,list_date",
        )
        if df is None or df.empty:
            self._stock_list_cache = pd.DataFrame()
            return self._stock_list_cache

        df = df.copy()
        df["code6"] = df["ts_code"].str.split(".").str[0]
        df["board"] = df["code6"].map(classify_board)
        self._stock_list_cache = df
        self._cache.set("stock_basic:list_status=L", dataframe_to_records(df))
        return df

    def search_stock(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search by six-digit code, ts_code, or Chinese stock name."""
        query = str(query).strip()
        if not query:
            return []

        stocks = self.get_all_stocks()
        if stocks.empty:
            return []

        upper = query.upper()
        if query.isdigit() and len(query) == 6:
            matched = stocks[stocks["code6"] == query]
        elif "." in upper:
            matched = stocks[stocks["ts_code"] == normalize_ts_code(upper)]
        else:
            by_name = stocks[stocks["name"].str.contains(query, case=False, na=False)]
            by_code = stocks[stocks["code6"].str.contains(query, na=False)]
            matched = pd.concat([by_name, by_code]).drop_duplicates(subset=["ts_code"])

        return dataframe_to_records(matched.head(limit))

    def resolve_ts_code(self, query: str) -> str:
        """Resolve a query to the first matching ts_code."""
        if "." in str(query) or (str(query).isdigit() and len(str(query)) == 6):
            return normalize_ts_code(str(query))

        matches = self.search_stock(query, limit=1)
        if not matches:
            raise ValueError(f"No stock matched query: {query}")
        return str(matches[0]["ts_code"])

    def get_company(self, ts_code: str) -> Optional[Dict[str, Any]]:
        """Fetch listed company profile."""
        df = self.pro.stock_company(ts_code=normalize_ts_code(ts_code))
        records = dataframe_to_records(df)
        return records[0] if records else None

    def get_financial_indicators(self, ts_code: str, limit: int = 12) -> pd.DataFrame:
        """Fetch financial indicator periods."""
        df = self.pro.fina_indicator(ts_code=normalize_ts_code(ts_code), limit=limit)
        return self._sort_by_date(df, "end_date", ascending=False)

    def get_income(self, ts_code: str, limit: int = 12) -> pd.DataFrame:
        """Fetch income statement periods."""
        df = self.pro.income(ts_code=normalize_ts_code(ts_code), limit=limit)
        return self._sort_by_date(df, "end_date", ascending=False)

    def get_balance(self, ts_code: str, limit: int = 12) -> pd.DataFrame:
        """Fetch balance sheet periods."""
        df = self.pro.balancesheet(ts_code=normalize_ts_code(ts_code), limit=limit)
        return self._sort_by_date(df, "end_date", ascending=False)

    def get_cashflow(self, ts_code: str, limit: int = 12) -> pd.DataFrame:
        """Fetch cash flow statement periods."""
        df = self.pro.cashflow(ts_code=normalize_ts_code(ts_code), limit=limit)
        return self._sort_by_date(df, "end_date", ascending=False)

    def get_main_business(self, ts_code: str, bz_type: str = "P", limit: int = 30) -> pd.DataFrame:
        """Fetch main business composition by product (P) or region (D)."""
        df = self.pro.fina_mainbz(ts_code=normalize_ts_code(ts_code), type=bz_type)
        df = self._sort_by_date(df, "end_date", ascending=False)
        return df.head(limit) if not df.empty else df

    def get_top10_holders(self, ts_code: str, periods: int = 4) -> pd.DataFrame:
        """Fetch top 10 holders for recent reporting periods."""
        df = self.pro.top10_holders(ts_code=normalize_ts_code(ts_code))
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.sort_values(["end_date", "hold_ratio"], ascending=[False, False])
        latest_periods = list(df["end_date"].dropna().unique()[:periods])
        return df[df["end_date"].isin(latest_periods)]

    def get_managers(self, ts_code: str) -> pd.DataFrame:
        """Fetch current disclosed managers."""
        df = self.pro.stk_managers(ts_code=normalize_ts_code(ts_code))
        if df is None or df.empty or "ann_date" not in df.columns:
            return pd.DataFrame()
        latest = df["ann_date"].max()
        return df[df["ann_date"] == latest]

    def get_rewards(self, ts_code: str) -> pd.DataFrame:
        """Fetch latest management rewards and holdings."""
        df = self.pro.stk_rewards(ts_code=normalize_ts_code(ts_code))
        if df is None or df.empty or "end_date" not in df.columns:
            return pd.DataFrame()
        latest = df["end_date"].max()
        return df[df["end_date"] == latest]

    def get_share_float(self, ts_code: str, days: int = 1095, limit: int = 50) -> pd.DataFrame:
        """Fetch upcoming restricted-share unlocks."""
        start_date = datetime.now().strftime("%Y%m%d")
        end_date = (datetime.now() + timedelta(days=days)).strftime("%Y%m%d")
        df = self.pro.share_float(
            ts_code=normalize_ts_code(ts_code),
            start_date=start_date,
            end_date=end_date,
        )
        df = self._sort_by_date(df, "float_date", ascending=True)
        return df.head(limit) if not df.empty else df

    def get_block_trade(self, ts_code: str, days: int = 90, limit: int = 100) -> pd.DataFrame:
        """Fetch recent block trades."""
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        df = self.pro.block_trade(
            ts_code=normalize_ts_code(ts_code),
            start_date=start_date,
            end_date=end_date,
        )
        df = self._sort_by_date(df, "trade_date", ascending=False)
        return df.head(limit) if not df.empty else df

    def get_holder_trade(self, ts_code: str, days: int = 365, limit: int = 100) -> pd.DataFrame:
        """Fetch shareholder increase/decrease records."""
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        df = self.pro.stk_holdertrade(
            ts_code=normalize_ts_code(ts_code),
            start_date=start_date,
            end_date=end_date,
        )
        df = self._sort_by_date(df, "ann_date", ascending=False)
        return df.head(limit) if not df.empty else df

    def get_holder_number(self, ts_code: str, limit: int = 50) -> pd.DataFrame:
        """Fetch shareholder count periods."""
        df = self.pro.stk_holdernumber(ts_code=normalize_ts_code(ts_code))
        df = self._sort_by_date(df, "end_date", ascending=False)
        return df.head(limit) if not df.empty else df

    def get_institutional_research(
        self,
        ts_code: str,
        *,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        trade_date: Optional[str] = None,
        limit: int = 50,
    ) -> pd.DataFrame:
        """Fetch institutional research records from Tushare stk_surv."""
        normalized = normalize_ts_code(ts_code)
        request_args: Dict[str, Any] = {"ts_code": normalized}
        normalized_trade_date = normalize_yyyymmdd(trade_date)
        if normalized_trade_date:
            request_args["trade_date"] = normalized_trade_date
        else:
            request_args["start_date"] = normalize_yyyymmdd(start_date) or (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
            request_args["end_date"] = normalize_yyyymmdd(end_date) or datetime.now().strftime("%Y%m%d")

        df = self.pro.stk_surv(**request_args)
        df = self._sort_by_date(df, "trade_date", ascending=False)
        return df.head(limit) if not df.empty else df

    def get_daily(self, ts_code: str, limit: int = 120) -> pd.DataFrame:
        """Fetch daily OHLCV bars."""
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=max(limit * 2, 30))).strftime("%Y%m%d")
        df = self.pro.daily(
            ts_code=normalize_ts_code(ts_code),
            start_date=start_date,
            end_date=end_date,
        )
        df = self._sort_by_date(df, "trade_date", ascending=False)
        return df.head(limit) if not df.empty else df

    def get_daily_basic(self, ts_code: str, limit: int = 60) -> pd.DataFrame:
        """Fetch daily valuation and market snapshot fields."""
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=max(limit * 2, 30))).strftime("%Y%m%d")
        df = self.pro.daily_basic(
            ts_code=normalize_ts_code(ts_code),
            start_date=start_date,
            end_date=end_date,
            fields=(
                "ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pe_ttm,"
                "pb,ps,ps_ttm,dv_ratio,dv_ttm,total_share,float_share,total_mv,circ_mv"
            ),
        )
        df = self._sort_by_date(df, "trade_date", ascending=False)
        return df.head(limit) if not df.empty else df

    def get_valuation_band(self, ts_code: str, years: int = 5) -> Dict[str, Any]:
        """Compute historical valuation percentile bands from daily_basic history.

        Tushare exposes no dedicated valuation-percentile / PE-band endpoint for
        individual stocks (only index_dailybasic covers indices). This derives the
        bands deterministically from daily_basic history. It only computes ranges
        and percentiles; interpreting them (cheap vs. expensive, which metric to
        trust per company type) is the model's job.
        """
        code = normalize_ts_code(ts_code)
        cache_key = f"valuation_band:{code}:{years}"
        cached = self._cache.get(cache_key, 3600 * 6)  # 6h TTL (one trading day)
        if cached is not None:
            return cached

        end = datetime.now()
        start = end - timedelta(days=int(years * 365.25) + 5)
        df = self.pro.daily_basic(
            ts_code=code,
            start_date=start.strftime("%Y%m%d"),
            end_date=end.strftime("%Y%m%d"),
            fields="ts_code,trade_date,close,pe_ttm,pb,ps_ttm,dv_ttm",
        )
        if df is None or df.empty:
            return {"ts_code": code, "error": "no daily_basic history returned"}

        df = df.sort_values("trade_date")
        latest_date = str(df["trade_date"].iloc[-1])
        # Metrics whose meaningful samples must be positive (a negative PE is a
        # loss, not a "cheap" reading); dividend yield keeps zeros.
        metrics = {"pe_ttm": True, "pb": True, "ps_ttm": True, "dv_ttm": False}
        windows = [w for w in (1, 3, 5) if w <= years] or [years]

        def _window_stats(series: "pd.Series", current: Optional[float]) -> Dict[str, Any]:
            s = pd.to_numeric(series, errors="coerce").dropna()
            if s.empty:
                return {"sample_size": 0}
            stats = {
                "sample_size": int(s.size),
                "min": round(float(s.min()), 4),
                "p25": round(float(s.quantile(0.25)), 4),
                "median": round(float(s.median()), 4),
                "mean": round(float(s.mean()), 4),
                "p75": round(float(s.quantile(0.75)), 4),
                "max": round(float(s.max()), 4),
            }
            if current is not None:
                stats["current_percentile"] = round(float((s <= current).mean()) * 100, 1)
            return stats

        bands: Dict[str, Any] = {}
        for metric, positive_only in metrics.items():
            col = pd.to_numeric(df[metric], errors="coerce")
            # FIX: use latest trading-day value, not latest positive sample
            latest_raw = _num(df[metric].iloc[-1])
            if positive_only and (latest_raw is None or latest_raw <= 0):
                current = None
            else:
                current = latest_raw
            per_window: Dict[str, Any] = {}
            for w in windows:
                cutoff = (end - timedelta(days=int(w * 365.25))).strftime("%Y%m%d")
                window_df = df[df["trade_date"] >= cutoff]
                window_col = pd.to_numeric(window_df[metric], errors="coerce")
                window_series = window_col[window_col > 0] if positive_only else window_col
                per_window[f"{w}y"] = _window_stats(window_series, current)
            bands[metric] = {
                "current": current,
                "positive_only": positive_only,
                "windows": per_window,
            }

        # Daily valuation series for the date-axis band charts (PE/PB/PS over time).
        # Downsampled to bound payload size; the last observation is always kept.
        series_df = df[["trade_date", "pe_ttm", "pb", "ps_ttm"]].copy()
        max_points = 320
        step = max(1, int(len(series_df) / max_points))
        sampled = series_df.iloc[::step]
        if not series_df.empty and sampled.index[-1] != series_df.index[-1]:
            sampled = pd.concat([sampled, series_df.iloc[[-1]]])

        series = [
            {
                "trade_date": str(row.trade_date),
                "pe_ttm": _num(row.pe_ttm),
                "pb": _num(row.pb),
                "ps_ttm": _num(row.ps_ttm),
            }
            for row in sampled.itertuples(index=False)
        ]

        result = {
            "ts_code": code,
            "latest_trade_date": latest_date,
            "requested_years": years,
            "history_start": str(df["trade_date"].iloc[0]),
            "total_trade_days": int(df.shape[0]),
            "bands": bands,
            "series": series,
            "model_responsibility": (
                "脚本只给区间和分位。贵贱判断、用哪个指标（成熟龙头看 PE/PB 分位、红利股看 dv_ttm 分位、"
                "成长股 PE 分位仅作下行参考）、是否因增速降档而历史中枢失效，全部由模型按公司类型判断。"
            ),
        }
        self._cache.set(cache_key, result)
        return result

    def get_cninfo_orgid(self, stock_code: str, timeout: int = DEFAULT_CNINFO_TIMEOUT) -> Optional[str]:
        """Resolve a stock code to CNInfo orgId (cached 7d)."""
        cache_key = f"cninfo_orgid:{stock_code}"
        cached = self._cache.get(cache_key, 604800)
        if cached is not None:
            return cached

        http = self._session or require_requests()
        response = request_with_retry(
            http.post,
            "http://www.cninfo.com.cn/new/information/topSearch/query",
            data={"keyWord": stock_code, "maxNum": 10},
            headers=cninfo_headers(),
            timeout=timeout,
        )
        results = response.json()
        if not isinstance(results, list) or not results:
            return None

        for item in results:
            if item.get("code") == stock_code and item.get("orgId"):
                org_id = str(item["orgId"])
                self._cache.set(cache_key, org_id)
                return org_id

        first_org_id = results[0].get("orgId")
        if first_org_id:
            org_id = str(first_org_id)
            self._cache.set(cache_key, org_id)
            return org_id
        return None

    def resolve_cninfo_stock(self, ts_code: str, timeout: int = DEFAULT_CNINFO_TIMEOUT) -> str:
        """Resolve a Tushare ts_code to CNInfo stock argument format."""
        normalized = normalize_ts_code(ts_code)
        stock_code = normalized.split(".", 1)[0]
        org_id = self.get_cninfo_orgid(stock_code, timeout=timeout)
        return f"{stock_code},{org_id}" if org_id else stock_code

    def query_cninfo_announcement_page(
        self,
        *,
        stock: str,
        tab_type: str = "fulltext",
        searchkey: str = "",
        category: str = "",
        trade: str = "",
        date_range: Optional[str] = None,
        page_num: int = 1,
        page_size: int = DEFAULT_CNINFO_PAGE_SIZE,
        timeout: int = DEFAULT_CNINFO_TIMEOUT,
    ) -> Dict[str, Any]:
        """Query one CNInfo announcement page for one stock only."""
        if not stock:
            raise ValueError("CNInfo announcement queries require one stock.")
        if tab_type not in CNINFO_ALLOWED_TAB_TYPES:
            raise ValueError(f"Unsupported CNInfo tabtype: {tab_type}")

        http = self._session or require_requests()
        response = request_with_retry(
            http.post,
            "http://www.cninfo.com.cn/new/hisAnnouncement/query",
            data={
                "pageNum": int(page_num),
                "pageSize": int(page_size),
                "column": "szse",
                "tabName": tab_type,
                "plate": "",
                "stock": stock,
                "searchkey": str(searchkey or "").strip(),
                "secid": "",
                "category": str(category or "").strip(),
                "trade": str(trade or "").strip(),
                "seDate": validate_cninfo_date_range(date_range),
                "sortName": "",
                "sortType": "",
                "isHLtitle": "true",
            },
            headers=cninfo_headers(),
            timeout=timeout,
        )
        results = response.json()
        announcements = results.get("announcements") or []

        normalized_items: List[Dict[str, Any]] = []
        for item in announcements:
            announcement_time = item.get("announcementTime")
            publish_date = ""
            if announcement_time:
                publish_date = datetime.fromtimestamp(announcement_time / 1000).strftime("%Y-%m-%d")

            adjunct_url = item.get("adjunctUrl") or ""
            normalized_item = {
                "announcement_time": publish_date,
                "sec_name": item.get("secName", ""),
                "sec_code": item.get("secCode", ""),
                "title": item.get("announcementTitle", ""),
                "adjunct_url": build_cninfo_url(adjunct_url) if adjunct_url else "",
                "announcement_id": item.get("announcementId", ""),
                "cninfo_tabtype": tab_type,
                "cninfo_category": category,
            }
            rule_result = classify_cninfo_fulltext(normalized_item["title"]) if tab_type == "fulltext" else classify_cninfo_relation()
            normalized_item.update(rule_result)
            normalized_item["needs_original_text"] = announcement_needs_original_text(normalized_item)
            normalized_items.append(normalized_item)

        return {
            "total_pages": results.get("totalpages"),
            "total_records": results.get("totalRecordNum"),
            "announcements": normalized_items,
        }

    def get_announcements(
        self,
        ts_code: str,
        *,
        tab_type: str = "fulltext",
        date_range: Optional[str] = None,
        searchkey: str = "",
        category: str = "",
        trade: str = "",
        page_num: int = 1,
        page_size: int = DEFAULT_CNINFO_PAGE_SIZE,
        limit: int = 30,
        include_excluded: bool = False,
        timeout: int = DEFAULT_CNINFO_TIMEOUT,
    ) -> Dict[str, Any]:
        """Fetch classified CNInfo announcements for one stock."""
        normalized = normalize_ts_code(ts_code)
        cninfo_stock = self.resolve_cninfo_stock(normalized, timeout=timeout)
        result = self.query_cninfo_announcement_page(
            stock=cninfo_stock,
            tab_type=tab_type,
            searchkey=searchkey,
            category=category,
            trade=trade,
            date_range=date_range,
            page_num=page_num,
            page_size=page_size,
            timeout=timeout,
        )
        announcements = result.get("announcements", [])
        if not include_excluded:
            announcements = [item for item in announcements if not item.get("excluded")]
        if limit > 0:
            announcements = announcements[:limit]
        return {
            "query": {
                "ts_code": normalized,
                "cninfo_stock": cninfo_stock,
                "tabtype": tab_type,
                "date": validate_cninfo_date_range(date_range),
                "searchkey": str(searchkey or "").strip(),
                "category": str(category or "").strip(),
                "trade": str(trade or "").strip(),
                "page_num": int(page_num),
                "page_size": int(page_size),
                "include_excluded": include_excluded,
                "limit": int(limit),
            },
            "total_pages": result.get("total_pages"),
            "total_records": result.get("total_records"),
            "filtered_count": len(announcements),
            "announcements": announcements,
        }

    def get_raw_announcement(
        self,
        ts_code: str,
        *,
        tab_type: str = "fulltext",
        date_range: Optional[str] = None,
        searchkey: str = "",
        category: str = "",
        trade: str = "",
        announcement_index: int = 1,
        include_excluded: bool = False,
        download_dir: Optional[str] = None,
        timeout: int = DEFAULT_CNINFO_TIMEOUT,
    ) -> Dict[str, Any]:
        """Return one announcement metadata record and optionally download its PDF."""
        if announcement_index < 1:
            raise ValueError("announcement-index must be >= 1.")
        result = self.get_announcements(
            ts_code,
            tab_type=tab_type,
            date_range=date_range,
            searchkey=searchkey,
            category=category,
            trade=trade,
            page_num=1,
            page_size=max(DEFAULT_CNINFO_PAGE_SIZE, announcement_index * 2),
            limit=max(DEFAULT_CNINFO_PAGE_SIZE, announcement_index),
            include_excluded=include_excluded,
            timeout=timeout,
        )
        announcements = result.get("announcements") or []
        if not announcements:
            raise ValueError("No matching CNInfo announcements were found.")
        if announcement_index > len(announcements):
            raise ValueError(f"announcement_index out of range: {announcement_index} (available: {len(announcements)})")

        selected = dict(announcements[announcement_index - 1])
        selected["selected_index"] = announcement_index
        selected["candidate_count"] = len(announcements)
        selected["download_url"] = selected.get("adjunct_url", "")
        selected["saved_path"] = None
        if not download_dir:
            return selected

        report_bytes = self.download_report_bytes(selected["download_url"], timeout=timeout)
        output_dir = Path(download_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = sanitize_filename(f"{selected.get('sec_code', '')}_{selected.get('title', '')}.pdf")
        file_path = output_dir / filename
        file_path.write_bytes(report_bytes)
        selected["saved_path"] = str(file_path.resolve())
        selected["file_size_bytes"] = len(report_bytes)
        return selected

    def get_announcement_text(
        self,
        ts_code: str,
        *,
        tab_type: str = "fulltext",
        date_range: Optional[str] = None,
        searchkey: str = "",
        category: str = "",
        trade: str = "",
        announcement_index: int = 1,
        include_excluded: bool = False,
        max_pages: int = 120,
        max_chars: int = 60000,
        to_markdown: bool = False,
        section: Optional[str] = None,
        timeout: int = DEFAULT_CNINFO_TIMEOUT,
    ) -> Dict[str, Any]:
        """Download one announcement PDF and extract plain text."""
        selected = self.get_raw_announcement(
            ts_code,
            tab_type=tab_type,
            date_range=date_range,
            searchkey=searchkey,
            category=category,
            trade=trade,
            announcement_index=announcement_index,
            include_excluded=include_excluded,
            download_dir=None,
            timeout=timeout,
        )
        report_bytes = self.download_report_bytes(selected["download_url"], timeout=timeout)
        selected.update(extract_pdf_text(report_bytes, max_pages=max_pages, max_chars=max_chars, to_markdown=to_markdown, section=section))
        return selected

    def query_cninfo_announcements(
        self,
        *,
        stock: str,
        category: str,
        date_range: str,
        page_size: int,
        timeout: int,
    ) -> List[Dict[str, Any]]:
        """Query CNInfo announcements for one stock and one category."""
        http = self._session or require_requests()
        response = request_with_retry(
            http.post,
            "http://www.cninfo.com.cn/new/hisAnnouncement/query",
            data={
                "pageNum": 1,
                "pageSize": int(page_size),
                "column": "szse",
                "tabName": "fulltext",
                "plate": "",
                "stock": stock,
                "searchkey": "",
                "secid": "",
                "category": category,
                "trade": "",
                "seDate": date_range,
                "sortName": "",
                "sortType": "",
                "isHLtitle": "true",
            },
            headers=cninfo_headers(),
            timeout=timeout,
        )
        results = response.json()
        announcements = results.get("announcements") or []

        normalized_items: List[Dict[str, Any]] = []
        for item in announcements:
            announcement_time = item.get("announcementTime")
            publish_date = ""
            if announcement_time:
                publish_date = datetime.fromtimestamp(announcement_time / 1000).strftime("%Y-%m-%d")

            adjunct_url = item.get("adjunctUrl") or ""
            report_meta = classify_report_title(item.get("announcementTitle") or "")

            normalized_items.append(
                {
                    "announcement_time": publish_date,
                    "sec_name": item.get("secName", ""),
                    "sec_code": item.get("secCode", ""),
                    "title": item.get("announcementTitle", ""),
                    "adjunct_url": build_cninfo_url(adjunct_url) if adjunct_url else "",
                    "announcement_id": item.get("announcementId", ""),
                    "cninfo_category": category,
                    **report_meta,
                }
            )

        return normalized_items

    def get_report_announcements(
        self,
        ts_code: str,
        *,
        report_type: str = "all",
        report_year: Optional[int] = None,
        limit: int = 12,
        include_variants: bool = False,
        timeout: int = DEFAULT_CNINFO_TIMEOUT,
    ) -> List[Dict[str, Any]]:
        """Fetch annual/quarter report announcement metadata from CNInfo."""
        normalized_type = str(report_type or "all").strip().lower()
        if normalized_type not in CNINFO_REPORT_TYPES:
            raise ValueError(f"Unsupported report type: {normalized_type}")

        cninfo_stock = self.resolve_cninfo_stock(ts_code, timeout=timeout)
        date_range = build_report_date_range(report_year)
        requested_types = [normalized_type] if normalized_type != "all" else ["annual", "half", "q3", "q1"]
        page_size = max(50, min(max(limit, 1) * 8, 100))
        deduped: Dict[str, Dict[str, Any]] = {}

        for current_type in requested_types:
            items = self.query_cninfo_announcements(
                stock=cninfo_stock,
                category=CNINFO_REPORT_CATEGORIES[current_type],
                date_range=date_range,
                page_size=page_size,
                timeout=timeout,
            )
            for item in items:
                if report_year and item.get("report_year") != report_year:
                    continue
                if not include_variants and not item.get("is_full_report"):
                    continue
                key = str(item.get("announcement_id") or item.get("adjunct_url") or item.get("title"))
                deduped[key] = item

        reports = sorted(deduped.values(), key=report_sort_key, reverse=True)
        return reports[:limit]

    def get_raw_report(
        self,
        ts_code: str,
        *,
        report_type: str = "all",
        report_year: Optional[int] = None,
        report_index: int = 1,
        include_variants: bool = False,
        download_dir: Optional[str] = None,
        timeout: int = DEFAULT_CNINFO_TIMEOUT,
    ) -> Dict[str, Any]:
        """Return one report metadata record and optionally download the PDF."""
        reports = self.get_report_announcements(
            ts_code,
            report_type=report_type,
            report_year=report_year,
            limit=max(report_index, 20),
            include_variants=include_variants,
            timeout=timeout,
        )
        if not reports:
            raise ValueError("No matching annual/quarter reports were found.")
        if report_index < 1 or report_index > len(reports):
            raise ValueError(f"report_index out of range: {report_index} (available: {len(reports)})")

        selected = dict(reports[report_index - 1])
        selected["selected_index"] = report_index
        selected["candidate_count"] = len(reports)
        selected["download_url"] = selected.get("adjunct_url", "")
        selected["saved_path"] = None
        if not download_dir:
            return selected

        report_bytes = self.download_report_bytes(selected["download_url"], timeout=timeout)
        output_dir = Path(download_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = sanitize_filename(f"{selected.get('sec_code', '')}_{selected.get('title', '')}.pdf")
        file_path = output_dir / filename
        file_path.write_bytes(report_bytes)
        selected["saved_path"] = str(file_path.resolve())
        selected["file_size_bytes"] = len(report_bytes)
        return selected

    def get_report_text(
        self,
        ts_code: str,
        *,
        report_type: str = "all",
        report_year: Optional[int] = None,
        report_index: int = 1,
        include_variants: bool = False,
        max_pages: int = 120,
        max_chars: int = 60000,
        to_markdown: bool = False,
        section: Optional[str] = None,
        timeout: int = DEFAULT_CNINFO_TIMEOUT,
    ) -> Dict[str, Any]:
        """Download one report PDF and extract plain text."""
        selected = self.get_raw_report(
            ts_code,
            report_type=report_type,
            report_year=report_year,
            report_index=report_index,
            include_variants=include_variants,
            download_dir=None,
            timeout=timeout,
        )
        report_bytes = self.download_report_bytes(selected["download_url"], timeout=timeout)
        selected.update(extract_pdf_text(report_bytes, max_pages=max_pages, max_chars=max_chars, to_markdown=to_markdown, section=section))
        return selected

    def download_report_bytes(self, url: str, timeout: int = DEFAULT_CNINFO_TIMEOUT) -> bytes:
        """Download one CNInfo PDF file and return its raw bytes (with retry)."""
        http = self._session or require_requests()
        normalized_url = build_cninfo_url(url)
        response = request_with_retry(
            http.get,
            normalized_url,
            timeout=timeout,
        )
        content_type = str(response.headers.get("Content-Type") or "")
        if "pdf" not in content_type.lower():
            raise RuntimeError(f"Unexpected report content type: {content_type or 'unknown'}")
        return response.content

    @staticmethod
    def _sort_by_date(df: Optional[pd.DataFrame], column: str, ascending: bool) -> pd.DataFrame:
        if df is None or df.empty:
            return pd.DataFrame()
        if column not in df.columns:
            return df
        return df.sort_values(column, ascending=ascending)

