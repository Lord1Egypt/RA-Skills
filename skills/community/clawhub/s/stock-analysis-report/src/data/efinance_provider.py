from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.data.provider import MarketDataProvider
from src.data.utils import RealtimeCache, calc_market_stats, enforce_rate_limit, safe_float
from src.models import (
    ChipDistribution,
    IndexData,
    MarketOverview,
    MarketStatistics,
    RealtimeQuote,
    SectorData,
    StockInfo,
)

logger = logging.getLogger(__name__)

_INDICES_MAP = {
    "000001": "上证指数",
    "399001": "深证成指",
    "399006": "创业板指",
}


class EfinanceProvider(MarketDataProvider):

    def __init__(self, sleep_min: float = 1.5, sleep_max: float = 3.0):
        self.sleep_min = sleep_min
        self.sleep_max = sleep_max
        self._realtime_cache = RealtimeCache()

    def _enforce_rate_limit(self) -> None:
        enforce_rate_limit(self.sleep_min, self.sleep_max)

    def _run_sync(self, func, *args, **kwargs):
        return asyncio.to_thread(func, *args, **kwargs)

    def _get_realtime_df(self):
        import efinance as ef

        cached = self._realtime_cache.get()
        if cached is not None:
            logger.debug("Efinance 全市场实时行情缓存命中")
            return cached
        self._enforce_rate_limit()
        logger.debug("Efinance 调用 ef.stock.get_realtime_quotes()...")
        df = ef.stock.get_realtime_quotes()
        logger.debug("Efinance 全市场实时行情获取完成: %d行 %d列", len(df), len(df.columns))
        self._realtime_cache.set(df)
        logger.debug("Efinance 全市场实时行情已缓存")
        return df

    async def get_stock_info(self, code: str) -> StockInfo:
        start = time.monotonic()
        code = self.normalize_code(code)
        logger.debug("Efinance 获取股票信息: code=%s", code)
        try:
            def _fetch():
                import efinance as ef
                self._enforce_rate_limit()
                info = ef.stock.get_base_info(code)
                df = self._get_realtime_df()
                return info, df

            info, df = await self._run_sync(_fetch)

            name = code
            industry = ""
            market_cap = 0.0

            if info is not None:
                if isinstance(info, pd.Series):
                    info = info.to_dict()
                elif isinstance(info, pd.DataFrame) and not info.empty:
                    info = info.iloc[0].to_dict()
                else:
                    info = {}
                name = str(info.get("股票名称", code))
                industry = str(info.get("所处行业", ""))

            if df is not None and not df.empty:
                code_col = "股票代码" if "股票代码" in df.columns else "code"
                row = df[df[code_col].astype(str) == code]
                if not row.empty:
                    row = row.iloc[0]
                    mv_col = "总市值" if "总市值" in df.columns else "total_mv"
                    market_cap = safe_float(row.get(mv_col, 0))
                    if not name or name == code:
                        n_col = "股票名称" if "股票名称" in df.columns else "name"
                        name = str(row.get(n_col, code))

            logger.debug("Efinance 股票信息: name=%s, industry=%s, market_cap=%.0f", name, industry, market_cap)
            logger.debug("Efinance get_stock_info 完成 耗时%.2fs", time.monotonic() - start)
            return StockInfo(code=code, name=name, industry=industry, market_cap=market_cap)
        except Exception as e:
            logger.warning("EfinanceProvider 获取股票信息失败 %s: %s", code, e)
            return StockInfo(code=code, name=code)

    async def get_daily_data(self, code: str, days: int = 120) -> pd.DataFrame:
        start = time.monotonic()
        code = self.normalize_code(code)
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days * 2)).strftime("%Y%m%d")
        logger.debug("Efinance 获取日K线: code=%s, days=%d, date_range=%s~%s", code, days, start_date, end_date)
        try:
            def _fetch():
                import efinance as ef
                self._enforce_rate_limit()
                return ef.stock.get_quote_history(
                    stock_codes=code,
                    beg=start_date,
                    end=end_date,
                    klt=101,
                    fqt=1,
                )

            df = await self._run_sync(_fetch)
            logger.debug("Efinance 日K线获取完成: %d条原始数据", len(df) if df is not None and not df.empty else 0)
            if df is None or df.empty:
                return pd.DataFrame()

            column_mapping = {
                "日期": "trade_date",
                "开盘": "open",
                "收盘": "close",
                "最高": "high",
                "最低": "low",
                "成交量": "volume",
                "涨跌幅": "change_pct",
            }
            df = df.rename(columns=column_mapping)
            df["trade_date"] = pd.to_datetime(df["trade_date"])
            df = df.sort_values("trade_date").reset_index(drop=True)
            result = df.tail(days).reset_index(drop=True)
            logger.debug("Efinance 日K线处理完成: %d条最终数据", len(result))
            logger.debug("Efinance get_daily_data 完成 耗时%.2fs", time.monotonic() - start)
            return result
        except Exception as e:
            logger.error("EfinanceProvider 获取日K线数据失败 %s: %s", code, e)
            return pd.DataFrame()

    async def get_realtime_quote(self, code: str) -> RealtimeQuote:
        start = time.monotonic()
        code = self.normalize_code(code)
        logger.debug("Efinance 获取实时行情: code=%s", code)
        try:
            df = await self._run_sync(self._get_realtime_df)
            if df is None or df.empty:
                return RealtimeQuote()

            code_col = "股票代码" if "股票代码" in df.columns else "code"
            row = df[df[code_col].astype(str) == code]
            if row.empty:
                logger.debug("Efinance 实时行情未找到股票: code=%s", code)
                return RealtimeQuote()
            row = row.iloc[0]

            price = safe_float(row.get("最新价" if "最新价" in df.columns else "price"))
            change_pct = safe_float(row.get("涨跌幅" if "涨跌幅" in df.columns else "pct_chg"))
            change_amt = safe_float(row.get("涨跌额" if "涨跌额" in df.columns else "change"))
            volume = safe_float(row.get("成交量" if "成交量" in df.columns else "volume"))
            turnover = safe_float(row.get("成交额" if "成交额" in df.columns else "amount"))
            high = safe_float(row.get("最高" if "最高" in df.columns else "high"))
            low = safe_float(row.get("最低" if "最低" in df.columns else "low"))
            open_price = safe_float(row.get("开盘" if "开盘" in df.columns else "open"))
            amplitude = safe_float(row.get("振幅" if "振幅" in df.columns else "amplitude"))
            turnover_rate = safe_float(row.get("换手率" if "换手率" in df.columns else "turnover_rate"))

            prev_close = price - change_amt if price and change_amt else 0.0

            logger.debug("Efinance 实时行情: price=%.2f, change_pct=%.2f%%", price, change_pct)
            logger.debug("Efinance get_realtime_quote 完成 耗时%.2fs", time.monotonic() - start)
            return RealtimeQuote(
                price=price,
                change_pct=change_pct,
                change_amt=change_amt,
                volume=volume,
                turnover=turnover,
                high=high,
                low=low,
                open=open_price,
                prev_close=prev_close,
                amplitude=amplitude,
                turnover_rate=turnover_rate,
            )
        except Exception as e:
            logger.error("EfinanceProvider 获取实时行情失败 %s: %s", code, e)
            return RealtimeQuote()

    async def get_chip_distribution(self, code: str) -> Optional[ChipDistribution]:
        logger.debug("Efinance 不支持筹码分布，返回 None")
        return None

    async def get_market_overview(self) -> MarketOverview:
        indices = await self.get_indices()
        statistics = await self.get_market_statistics()
        top_sectors, bottom_sectors = await self.get_sector_rankings()
        return MarketOverview(
            indices=indices,
            statistics=statistics,
            top_sectors=top_sectors,
            bottom_sectors=bottom_sectors,
        )

    async def get_sector_rankings(self) -> tuple[list[SectorData], list[SectorData]]:
        start = time.monotonic()
        logger.debug("Efinance 获取板块排名...")
        try:
            def _fetch():
                import efinance as ef
                self._enforce_rate_limit()
                return ef.stock.get_realtime_quotes(["行业板块"])

            df = await self._run_sync(_fetch)
            if df is None or df.empty:
                return [], []

            change_col = "涨跌幅" if "涨跌幅" in df.columns else "pct_chg"
            name_col = "股票名称" if "股票名称" in df.columns else "name"
            if change_col not in df.columns or name_col not in df.columns:
                return [], []

            df[change_col] = pd.to_numeric(df[change_col], errors="coerce")
            df = df.dropna(subset=[change_col])

            top = df.nlargest(5, change_col)
            bottom = df.nsmallest(5, change_col)

            top_sectors = [
                SectorData(name=str(r[name_col]), change_pct=float(r[change_col]))
                for _, r in top.iterrows()
            ]
            bottom_sectors = [
                SectorData(name=str(r[name_col]), change_pct=float(r[change_col]))
                for _, r in bottom.iterrows()
            ]
            logger.debug("Efinance 板块排名: 领涨%d个, 领跌%d个", len(top_sectors), len(bottom_sectors))
            logger.debug("Efinance get_sector_rankings 完成 耗时%.2fs", time.monotonic() - start)
            return top_sectors, bottom_sectors
        except Exception as e:
            logger.warning("EfinanceProvider 获取板块涨跌榜失败: %s", e)
            return [], []

    async def get_market_statistics(self) -> MarketStatistics:
        start = time.monotonic()
        logger.debug("Efinance 获取市场统计...")
        try:
            df = await self._run_sync(self._get_realtime_df)
            if df is None or df.empty:
                return MarketStatistics()
            result = calc_market_stats(df, self)
            logger.debug(
                "Efinance 市场统计: 涨%d 跌%d 平%d 涨停%d 跌停%d",
                result.up_count, result.down_count, result.flat_count, result.limit_up_count, result.limit_down_count,
            )
            logger.debug("Efinance get_market_statistics 完成 耗时%.2fs", time.monotonic() - start)
            return result
        except Exception as e:
            logger.warning("EfinanceProvider 获取市场统计失败: %s", e)
            return MarketStatistics()

    async def get_indices(self) -> list[IndexData]:
        start = time.monotonic()
        logger.debug("Efinance 获取指数数据...")
        try:
            def _fetch():
                import efinance as ef
                self._enforce_rate_limit()
                return ef.stock.get_realtime_quotes(["沪深系列指数"])

            df = await self._run_sync(_fetch)
            if df is None or df.empty:
                return []

            code_col = "股票代码" if "股票代码" in df.columns else "code"
            code_series = df[code_col].astype(str).str.zfill(6)

            results: list[IndexData] = []
            for idx_code, idx_name in _INDICES_MAP.items():
                row = df[code_series == idx_code]
                if row.empty:
                    continue
                item = row.iloc[0]
                price_col = "最新价" if "最新价" in df.columns else "price"
                pct_col = "涨跌幅" if "涨跌幅" in df.columns else "pct_chg"
                chg_col = "涨跌额" if "涨跌额" in df.columns else "change"

                close_val = safe_float(item.get(price_col))
                change_pct = safe_float(item.get(pct_col))
                change_amt = safe_float(item.get(chg_col))

                results.append(IndexData(
                    name=idx_name,
                    code=idx_code,
                    close=close_val,
                    change_pct=change_pct,
                    change_amt=change_amt,
                ))
            logger.debug("Efinance 指数数据: %d个", len(results))
            logger.debug("Efinance get_indices 完成 耗时%.2fs", time.monotonic() - start)
            return results
        except Exception as e:
            logger.warning("EfinanceProvider 获取指数数据失败: %s", e)
            return []
