from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.data.provider import MarketDataProvider
from src.data.utils import (
    RealtimeCache,
    calc_market_stats,
    calculate_chip_from_daily,
    enforce_rate_limit,
    safe_float,
)
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
    "sh000001": "上证指数",
    "sz399001": "深证成指",
    "sz399006": "创业板指",
}


class AkShareProvider(MarketDataProvider):

    def __init__(self, sleep_min: float = 1.5, sleep_max: float = 3.0):
        self.sleep_min = sleep_min
        self.sleep_max = sleep_max
        self._realtime_cache = RealtimeCache()

    def _enforce_rate_limit(self) -> None:
        enforce_rate_limit(self.sleep_min, self.sleep_max)

    def _run_sync(self, func, *args, **kwargs):
        return asyncio.to_thread(func, *args, **kwargs)

    def _get_realtime_df(self):
        import akshare as ak

        cached = self._realtime_cache.get()
        if cached is not None:
            logger.debug("AkShare 全市场实时行情缓存命中")
            return cached
        self._enforce_rate_limit()
        logger.debug("AkShare 调用 ak.stock_zh_a_spot_em()...")
        df = ak.stock_zh_a_spot_em()
        logger.debug("AkShare 全市场实时行情获取完成: %d行 %d列", len(df), len(df.columns))
        self._realtime_cache.set(df)
        logger.debug("AkShare 全市场实时行情已缓存")
        return df

    async def get_stock_info(self, code: str) -> StockInfo:
        start = time.monotonic()
        code = self.normalize_code(code)
        logger.debug("AkShare 获取股票信息: code=%s", code)
        try:
            def _fetch():
                import akshare as ak
                self._enforce_rate_limit()
                try:
                    info_df = ak.stock_individual_info_em(symbol=code)
                except Exception:
                    info_df = None
                spot_df = self._get_realtime_df()
                return info_df, spot_df

            info_df, spot_df = await self._run_sync(_fetch)

            name = code
            industry = ""
            market_cap = 0.0
            list_date = ""

            if info_df is not None and not info_df.empty:
                info_dict = {}
                if "item" in info_df.columns and "value" in info_df.columns:
                    for _, r in info_df.iterrows():
                        info_dict[str(r["item"])] = str(r["value"])
                name = info_dict.get("股票简称", code)
                industry = info_dict.get("行业", "")
                list_date = info_dict.get("上市时间", "")

            if spot_df is not None and not spot_df.empty:
                row = spot_df[spot_df["代码"] == code]
                if not row.empty:
                    row = row.iloc[0]
                    market_cap = safe_float(row.get("总市值", 0))
                    if not name or name == code:
                        name = str(row.get("名称", code))

            logger.debug("AkShare 股票信息: name=%s, industry=%s, market_cap=%.0f", name, industry, market_cap)
            return StockInfo(
                code=code, name=name, industry=industry,
                market_cap=market_cap, list_date=list_date,
            )
        except Exception as e:
            logger.warning("AkShareProvider 获取股票信息失败 %s: %s", code, e)
            return StockInfo(code=code, name=code)
        finally:
            elapsed = time.monotonic() - start
            logger.debug("AkShare get_stock_info 完成 耗时%.2fs", elapsed)

    async def get_daily_data(self, code: str, days: int = 120) -> pd.DataFrame:
        start = time.monotonic()
        code = self.normalize_code(code)
        try:
            def _fetch():
                import akshare as ak
                self._enforce_rate_limit()
                end_date = datetime.now().strftime("%Y%m%d")
                start_date = (datetime.now() - timedelta(days=days * 2)).strftime("%Y%m%d")
                logger.debug("AkShare 获取日K线: code=%s, days=%d, date_range=%s~%s", code, days, start_date, end_date)
                return ak.stock_zh_a_hist(
                    symbol=code,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                    adjust="qfq",
                )

            df = await self._run_sync(_fetch)
            if df is None or df.empty:
                return pd.DataFrame()

            logger.debug("AkShare 日K线获取完成: %d条原始数据", len(df))

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
            logger.debug("AkShare 日K线处理完成: %d条最终数据", len(result))
            return result
        except Exception as e:
            logger.error("AkShareProvider 获取日K线数据失败 %s: %s", code, e)
            return pd.DataFrame()
        finally:
            elapsed = time.monotonic() - start
            logger.debug("AkShare get_daily_data 完成 耗时%.2fs", elapsed)

    async def get_realtime_quote(self, code: str) -> RealtimeQuote:
        start = time.monotonic()
        code = self.normalize_code(code)
        logger.debug("AkShare 获取实时行情: code=%s", code)
        try:
            df = await self._run_sync(self._get_realtime_df)
            if df is None or df.empty:
                return RealtimeQuote()

            row = df[df["代码"] == code]
            if row.empty:
                logger.debug("AkShare 实时行情未找到股票: code=%s", code)
                return RealtimeQuote()
            row = row.iloc[0]

            prev_close = safe_float(row.get("昨收", 0))
            high = safe_float(row.get("最高", 0))
            low = safe_float(row.get("最低", 0))
            amplitude = safe_float(row.get("振幅", 0))
            if not amplitude and prev_close > 0:
                amplitude = (high - low) / prev_close * 100

            price = safe_float(row.get("最新价"))
            change_pct = safe_float(row.get("涨跌幅"))
            logger.debug("AkShare 实时行情: price=%.2f, change_pct=%.2f%%", price, change_pct)

            return RealtimeQuote(
                price=price,
                change_pct=change_pct,
                change_amt=safe_float(row.get("涨跌额")),
                volume=safe_float(row.get("成交量")),
                turnover=safe_float(row.get("成交额")),
                high=high,
                low=low,
                open=safe_float(row.get("今开")),
                prev_close=prev_close,
                amplitude=amplitude,
                turnover_rate=safe_float(row.get("换手率")),
            )
        except Exception as e:
            logger.error("AkShareProvider 获取实时行情失败 %s: %s", code, e)
            return RealtimeQuote()
        finally:
            elapsed = time.monotonic() - start
            logger.debug("AkShare get_realtime_quote 完成 耗时%.2fs", elapsed)

    async def get_chip_distribution(self, code: str) -> Optional[ChipDistribution]:
        start = time.monotonic()
        code = self.normalize_code(code)
        logger.debug("AkShare 获取筹码分布: code=%s", code)
        try:
            def _fetch():
                import akshare as ak
                self._enforce_rate_limit()
                return ak.stock_cyq_em(symbol=code)

            df = await self._run_sync(_fetch)
            if df is None or df.empty:
                logger.debug("AkShare 筹码接口无数据，回退K线估算: code=%s", code)
                return await self._calculate_chip_from_daily(code)

            logger.debug("AkShare 筹码接口返回数据: %d行", len(df))
            latest = df.iloc[-1]
            return ChipDistribution(
                profit_ratio=safe_float(latest.get("获利比例")) * 100,
                avg_cost=safe_float(latest.get("平均成本")),
                concentration=safe_float(latest.get("90集中度")) * 100,
                profit_90_cost=safe_float(latest.get("90成本-高")),
                profit_10_cost=safe_float(latest.get("90成本-低")),
            )
        except Exception as e:
            logger.warning("AkShareProvider 筹码接口失败 %s: %s，尝试K线估算", code, e)
            return await self._calculate_chip_from_daily(code)
        finally:
            elapsed = time.monotonic() - start
            logger.debug("AkShare get_chip_distribution 完成 耗时%.2fs", elapsed)

    async def _calculate_chip_from_daily(self, code: str) -> Optional[ChipDistribution]:
        try:
            df = await self.get_daily_data(code, 90)
        except Exception:
            return None

        logger.debug("AkShare K线估算筹码: code=%s, 数据%d条", code, len(df))
        return calculate_chip_from_daily(df)

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
        try:
            def _fetch_em():
                import akshare as ak
                self._enforce_rate_limit()
                return ak.stock_board_industry_name_em()

            logger.debug("AkShare 获取板块排名(东财)...")
            df = await self._run_sync(_fetch_em)
            if df is not None and not df.empty:
                change_col = "涨跌幅"
                name_col = "板块名称"
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
                logger.debug("AkShare 东财板块排名: 领涨%d个, 领跌%d个", len(top_sectors), len(bottom_sectors))
                elapsed = time.monotonic() - start
                logger.debug("AkShare get_sector_rankings 完成 耗时%.2fs", elapsed)
                return top_sectors, bottom_sectors
        except Exception as e:
            logger.warning("AkShareProvider 东财板块接口失败: %s，尝试新浪接口", e)

        try:
            def _fetch_sina():
                import akshare as ak
                self._enforce_rate_limit()
                return ak.stock_sector_spot(indicator="行业")

            logger.debug("AkShare 获取板块排名(新浪)...")
            df = await self._run_sync(_fetch_sina)
            if df is not None and not df.empty:
                change_col = "涨跌幅"
                name_col = "板块"
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
                logger.debug("AkShare 新浪板块排名: 领涨%d个, 领跌%d个", len(top_sectors), len(bottom_sectors))
                elapsed = time.monotonic() - start
                logger.debug("AkShare get_sector_rankings 完成 耗时%.2fs", elapsed)
                return top_sectors, bottom_sectors
        except Exception as e:
            logger.warning("AkShareProvider 新浪板块接口也失败: %s", e)

        elapsed = time.monotonic() - start
        logger.debug("AkShare get_sector_rankings 完成 耗时%.2fs", elapsed)
        return [], []

    async def get_market_statistics(self) -> MarketStatistics:
        start = time.monotonic()
        try:
            logger.debug("AkShare 获取市场统计(东财)...")
            df = await self._run_sync(self._get_realtime_df)
            if df is not None and not df.empty:
                stats = calc_market_stats(df, self)
                logger.debug("AkShare 东财市场统计: 涨%d 跌%d 平%d 涨停%d 跌停%d", stats.up_count, stats.down_count, stats.flat_count, stats.limit_up_count, stats.limit_down_count)
                elapsed = time.monotonic() - start
                logger.debug("AkShare get_market_statistics 完成 耗时%.2fs", elapsed)
                return stats
        except Exception as e:
            logger.warning("AkShareProvider 东财市场统计失败: %s，尝试新浪接口", e)

        try:
            def _fetch_sina():
                import akshare as ak
                self._enforce_rate_limit()
                return ak.stock_zh_a_spot()

            logger.debug("AkShare 获取市场统计(新浪)...")
            df = await self._run_sync(_fetch_sina)
            if df is not None and not df.empty:
                stats = calc_market_stats(df, self)
                logger.debug("AkShare 新浪市场统计: 涨%d 跌%d 平%d 涨停%d 跌停%d", stats.up_count, stats.down_count, stats.flat_count, stats.limit_up_count, stats.limit_down_count)
                elapsed = time.monotonic() - start
                logger.debug("AkShare get_market_statistics 完成 耗时%.2fs", elapsed)
                return stats
        except Exception as e:
            logger.warning("AkShareProvider 新浪市场统计也失败: %s", e)

        elapsed = time.monotonic() - start
        logger.debug("AkShare get_market_statistics 完成 耗时%.2fs", elapsed)
        return MarketStatistics()

    async def get_indices(self) -> list[IndexData]:
        start = time.monotonic()
        try:
            def _fetch():
                import akshare as ak
                self._enforce_rate_limit()
                return ak.stock_zh_index_spot_sina()

            logger.debug("AkShare 获取指数数据(新浪)...")
            df = await self._run_sync(_fetch)
            if df is None or df.empty:
                return []

            results: list[IndexData] = []
            for idx_code, idx_name in _INDICES_MAP.items():
                row = df[df["代码"] == idx_code]
                if row.empty:
                    continue
                item = row.iloc[0]

                close_val = safe_float(item.get("最新价"))
                prev_close = safe_float(item.get("昨收"))
                change_amt = safe_float(item.get("涨跌额"))
                change_pct = safe_float(item.get("涨跌幅"))

                results.append(IndexData(
                    name=idx_name,
                    code=idx_code,
                    close=close_val,
                    change_pct=change_pct,
                    change_amt=change_amt,
                ))
            logger.debug("AkShare 指数数据: %d个", len(results))
            elapsed = time.monotonic() - start
            logger.debug("AkShare get_indices 完成 耗时%.2fs", elapsed)
            return results
        except Exception as e:
            logger.warning("AkShareProvider 获取指数数据失败: %s", e)
            elapsed = time.monotonic() - start
            logger.debug("AkShare get_indices 完成 耗时%.2fs", elapsed)
            return []
