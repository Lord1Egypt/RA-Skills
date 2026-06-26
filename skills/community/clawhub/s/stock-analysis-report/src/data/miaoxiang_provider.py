from __future__ import annotations

import asyncio
import logging
import re
import time
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests

from src.data.provider import MarketDataProvider
from src.models import (
    CapitalFlow,
    ChipDistribution,
    FinancialData,
    IndexData,
    MarketOverview,
    MarketStatistics,
    RealtimeQuote,
    SectorData,
    StockInfo,
    Valuation,
)

logger = logging.getLogger(__name__)

_MX_API_URL = "https://mkapi2.dfcfs.com/finskillshub/api/claw/query"
_MX_TIMEOUT = 30


def _flatten_value(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (dict, list)):
        import json
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def _format_label(key: str, name_map: Dict[str, Any], code_map: Dict[str, str]) -> str:
    mapped = name_map.get(key) or name_map.get(int(key) if key.isdigit() else key)
    if mapped not in (None, ""):
        return _flatten_value(mapped)
    mapped_code = code_map.get(key)
    if mapped_code not in (None, ""):
        return _flatten_value(mapped_code)
    return ""


def _return_code_map(block: Dict[str, Any]) -> Dict[str, str]:
    for key in ("returnCodeMap", "returnCodeNameMap", "codeMap"):
        data = block.get(key)
        if isinstance(data, dict):
            return {str(k): _flatten_value(v) for k, v in data.items()}
    return {}


def _parse_table_to_rows(block: Dict[str, Any]) -> List[Dict[str, str]]:
    table = block.get("table") or {}
    name_map = block.get("nameMap") or {}
    if isinstance(name_map, list):
        name_map = {str(i): v for i, v in enumerate(name_map)}
    elif not isinstance(name_map, dict):
        name_map = {}

    if not isinstance(table, dict):
        return []

    headers = table.get("headName") or []
    if not isinstance(headers, list):
        return []

    indicator_order = block.get("indicatorOrder") or []
    data_keys = [k for k in table.keys() if k != "headName"]
    key_map = {str(k): k for k in data_keys}

    ordered: List[str] = []
    seen: set = set()
    for key in indicator_order:
        ks = str(key)
        if ks in key_map and ks not in seen:
            ordered.append(key_map[ks])
            seen.add(ks)
    for key in data_keys:
        ks = str(key)
        if ks not in seen:
            ordered.append(key)
            seen.add(ks)

    code_map = _return_code_map(block)
    field_labels: List[Tuple[str, str]] = []
    for key in ordered:
        label = _format_label(str(key), name_map, code_map)
        if label:
            field_labels.append((key, label))

    rows: List[Dict[str, str]] = []
    for row_idx, date_val in enumerate(headers):
        row: Dict[str, str] = {"date": _flatten_value(date_val)}
        for key, label in field_labels:
            raw_values = table.get(key, [])
            value = raw_values[row_idx] if row_idx < len(raw_values) else ""
            row[label] = _flatten_value(value)
        rows.append(row)

    return rows


def _find_value_fuzzy(rows: List[Dict[str, str]], keywords: List[str], row_idx: int = 0) -> str:
    if not rows or row_idx >= len(rows):
        return ""
    row = rows[row_idx]
    for kw in keywords:
        for key, val in row.items():
            if kw in key:
                return val
    return ""


def _find_in_row(row: Dict[str, str], keywords: List[str]) -> str:
    for kw in keywords:
        for key, val in row.items():
            if kw in key:
                return val
    return ""


def _mx_parse_float(raw: str) -> float:
    if not raw or not raw.strip():
        return 0.0
    raw = raw.strip()
    if raw in ("-", "--", "N/A", "null"):
        return 0.0

    has_wan_yi = "万亿" in raw
    has_yi = "亿" in raw and not has_wan_yi
    has_wan = "万" in raw and not has_yi and not has_wan_yi
    has_pct = "%" in raw

    digits = re.sub(r"[^\d.\-]", "", raw)
    if not digits or digits == "-" or digits == ".":
        return 0.0
    try:
        value = float(digits)
    except ValueError:
        return 0.0

    if has_wan_yi:
        return value * 1e12
    if has_yi:
        return value * 1e8
    if has_wan:
        return value * 1e4
    if has_pct:
        return value
    return value


class MiaoxiangProvider(MarketDataProvider):

    def __init__(self, api_key: str):
        self.api_key = api_key
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "apikey": self.api_key,
        })
        logger.info("MiaoxiangProvider 初始化成功")

    def __repr__(self) -> str:
        masked = self.api_key[-4:] if len(self.api_key) >= 4 else "****"
        return f"MiaoxiangProvider(api_key='***{masked}')"

    def _query(self, tool_query: str) -> Dict[str, Any]:
        logger.debug("Miaoxiang 查询: %s", tool_query)
        resp = self._session.post(_MX_API_URL, json={"toolQuery": tool_query}, timeout=_MX_TIMEOUT)
        resp.raise_for_status()
        result = resp.json()
        status = result.get("status")
        if status != 0:
            msg = result.get("message", "")
            raise RuntimeError(f"Miaoxiang API error: status={status}, message={msg}")
        return result

    def _query_and_parse(self, tool_query: str) -> List[Dict[str, Any]]:
        result = self._query(tool_query)
        data = result.get("data", {})
        inner = data.get("data", {})
        search = inner.get("searchDataResultDTO", {})
        dto_list = search.get("dataTableDTOList", [])
        return dto_list if isinstance(dto_list, list) else []

    @staticmethod
    def _extract_entity_name(dto: Dict[str, Any]) -> str:
        entity = dto.get("entityTagDTO")
        if isinstance(entity, dict) and entity.get("fullName"):
            return entity["fullName"]
        entity_list = dto.get("entityTagDTOList")
        if isinstance(entity_list, list) and entity_list:
            first = entity_list[0]
            if isinstance(first, dict) and first.get("fullName"):
                return first["fullName"]
        raw = dto.get("entityName") or ""
        return raw.split("(")[0] if raw else ""

    async def get_stock_info(self, code: str) -> StockInfo:
        start = time.monotonic()
        logger.debug("Miaoxiang 获取股票信息: code=%s", code)
        try:
            dto_list = await asyncio.to_thread(
                self._query_and_parse,
                f"{code} 公司简介 行业 总市值 流通市值"
            )
            name = ""
            industry = ""
            market_cap = 0.0

            for dto in dto_list:
                rows = _parse_table_to_rows(dto)
                if not rows:
                    continue

                if not name:
                    name = self._extract_entity_name(dto)
                    if not name:
                        name = _find_value_fuzzy(rows, ["公司名称", "名称", "简称"])

                if not industry:
                    industry = (
                        _find_value_fuzzy(rows, ["所属中信行业", "所属GICS行业", "所属中证行业"])
                        or _find_value_fuzzy(rows, ["行业"])
                    )
                    if industry and "-" in industry:
                        parts = industry.split("-")
                        industry = parts[-1] if len(parts) <= 3 else "-".join(parts[1:])

                if market_cap <= 0:
                    cap_str = _find_value_fuzzy(rows, ["总市值"])
                    if cap_str:
                        market_cap = _mx_parse_float(cap_str)

            if not name:
                name = code
            logger.debug("Miaoxiang 股票信息: name=%s, industry=%s, market_cap=%.0f", name, industry, market_cap)
            logger.debug("Miaoxiang get_stock_info 完成 耗时%.2fs", time.monotonic() - start)
            return StockInfo(code=code, name=name, industry=industry, market_cap=market_cap)
        except Exception as e:
            logger.warning("Miaoxiang get_stock_info 失败: %s", e)
            raise
        logger.debug("Miaoxiang get_stock_info 完成 耗时%.2fs", time.monotonic() - start)
        return StockInfo(code=code, name=code)

    async def get_daily_data(self, code: str, days: int = 120) -> pd.DataFrame:
        start = time.monotonic()
        logger.debug("Miaoxiang 获取日K线: code=%s, days=%d", code, days)
        try:
            capped = min(days, 55)
            df = await self._fetch_daily_chunk(code, capped)

            if df.empty and days > 55:
                logger.debug("Miaoxiang 55天日K线为空, 尝试30天")
                df = await self._fetch_daily_chunk(code, 30)

            if not df.empty:
                valid_count = int((df["close"] > 0).sum())
                logger.debug("Miaoxiang 日K线处理完成: %d条 (有效%d条, 请求%d天, 上限55天)",
                             len(df), valid_count, days)
            logger.debug("Miaoxiang get_daily_data 完成 耗时%.2fs", time.monotonic() - start)
            return df
        except Exception as e:
            logger.warning("Miaoxiang get_daily_data 失败: %s", e)
            raise
        logger.debug("Miaoxiang get_daily_data 完成 耗时%.2fs", time.monotonic() - start)
        return pd.DataFrame()

    async def _fetch_daily_chunk(self, code: str, days: int) -> pd.DataFrame:
        dto_list = await asyncio.to_thread(
            self._query_and_parse,
            f"{code} 最近{days}个交易日 开盘价 收盘价 最高价 最低价 成交量 成交额"
        )
        for dto in dto_list:
            rows = _parse_table_to_rows(dto)
            if len(rows) < 2:
                continue

            has_close = any(_find_in_row(r, ["收盘价"]) for r in rows)
            if not has_close:
                continue

            is_daily = True
            first_date = rows[0].get("date", "")
            if "(月" in first_date or "月)" in first_date:
                is_daily = False
            if not is_daily:
                logger.debug("Miaoxiang 跳过月度数据 (rows=%d)", len(rows))
                continue

            records = []
            for row in rows:
                date_str = row.get("date", "")
                close_val = _mx_parse_float(_find_in_row(row, ["收盘价"]))
                if close_val <= 0:
                    continue
                records.append({
                    "date": re.sub(r"\(.*?\)", "", date_str).strip(),
                    "open": _mx_parse_float(_find_in_row(row, ["开盘价"])),
                    "close": close_val,
                    "high": _mx_parse_float(_find_in_row(row, ["最高价"])),
                    "low": _mx_parse_float(_find_in_row(row, ["最低价"])),
                    "volume": _mx_parse_float(_find_in_row(row, ["成交量"])),
                    "turnover": _mx_parse_float(_find_in_row(row, ["成交额"])),
                })

            if records:
                df = pd.DataFrame(records)
                if "date" in df.columns:
                    df["date"] = pd.to_datetime(df["date"], errors="coerce")
                    df = df.sort_values("date").reset_index(drop=True)
                return df

        return pd.DataFrame()

    async def get_realtime_quote(self, code: str) -> RealtimeQuote:
        start = time.monotonic()
        logger.debug("Miaoxiang 获取实时行情: code=%s", code)
        try:
            dto_list = await asyncio.to_thread(
                self._query_and_parse,
                f"{code} 最新价 涨跌幅 涨跌额 成交量 成交额 今开 最高 最低 换手率 振幅 昨收"
            )
            price = 0.0
            change_pct = 0.0
            change_amt = 0.0
            volume = 0.0
            turnover = 0.0
            open_price = 0.0
            high = 0.0
            low = 0.0
            prev_close = 0.0
            turnover_rate = 0.0
            amplitude = 0.0

            for dto in dto_list:
                rows = _parse_table_to_rows(dto)
                if not rows:
                    continue
                row = rows[-1]

                if price <= 0:
                    price = _mx_parse_float(_find_in_row(row, ["最新价"]))
                if change_pct <= 0:
                    change_pct = _mx_parse_float(_find_in_row(row, ["涨跌幅"]))
                if change_amt <= 0:
                    change_amt = _mx_parse_float(_find_in_row(row, ["涨跌额", "涨跌值"]))
                if volume <= 0:
                    volume = _mx_parse_float(_find_in_row(row, ["成交量"]))
                if turnover <= 0:
                    turnover = _mx_parse_float(_find_in_row(row, ["成交额"]))
                if open_price <= 0:
                    open_price = _mx_parse_float(_find_in_row(row, ["今开", "开盘价"]))
                if high <= 0:
                    high = _mx_parse_float(_find_in_row(row, ["最高", "最高价"]))
                if low <= 0:
                    low = _mx_parse_float(_find_in_row(row, ["最低", "最低价"]))
                if prev_close <= 0:
                    prev_close = _mx_parse_float(_find_in_row(row, ["昨收", "昨收价", "昨收盘"]))
                if turnover_rate <= 0:
                    turnover_rate = _mx_parse_float(_find_in_row(row, ["换手率"]))
                if amplitude <= 0:
                    amplitude = _mx_parse_float(_find_in_row(row, ["振幅"]))

            quote = RealtimeQuote(
                price=price,
                change_pct=change_pct,
                change_amt=change_amt,
                volume=volume,
                turnover=turnover,
                open=open_price,
                high=high,
                low=low,
                prev_close=prev_close,
                turnover_rate=turnover_rate,
                amplitude=amplitude,
            )
            logger.debug("Miaoxiang 实时行情: price=%.2f, change_pct=%.2f%%", quote.price, quote.change_pct)
            if quote.price <= 0:
                logger.warning("Miaoxiang 实时行情价格无效: price=%.2f", quote.price)
            logger.debug("Miaoxiang get_realtime_quote 完成 耗时%.2fs", time.monotonic() - start)
            return quote
        except Exception as e:
            logger.warning("Miaoxiang get_realtime_quote 失败: %s", e)
            raise
        logger.debug("Miaoxiang get_realtime_quote 完成 耗时%.2fs", time.monotonic() - start)
        return RealtimeQuote()

    async def get_chip_distribution(self, code: str) -> Optional[ChipDistribution]:
        logger.debug("Miaoxiang 不支持筹码分布，返回 None")
        return None

    async def get_indices(self) -> list[IndexData]:
        start = time.monotonic()
        logger.debug("Miaoxiang 获取指数数据...")
        indices: list[IndexData] = []
        try:
            dto_list = await asyncio.to_thread(
                self._query_and_parse,
                "上证指数 深证成指 创业板指 最新点位 涨跌幅 涨跌额"
            )
            name_to_code = {
                "上证指数": "000001",
                "上证综合指数": "000001",
                "深证成指": "399001",
                "深证成份指数": "399001",
                "创业板指": "399006",
                "创业板指数": "399006",
            }
            code_to_name = {
                "000001": "上证指数",
                "399001": "深证成指",
                "399006": "创业板指",
            }
            seen_codes: set[str] = set()

            realtime_indices: list[IndexData] = []
            historical_indices: list[IndexData] = []
            realtime_dtos = []
            historical_dtos = []

            for dto in dto_list:
                rows = _parse_table_to_rows(dto)
                if not rows:
                    continue
                first_date = rows[0].get("date", "") if rows else ""
                has_realtime_format = any(kw in first_date for kw in [".SH", ".SZ", ".BJ"])
                if has_realtime_format and "最新价" in (rows[0].keys() if rows else []):
                    realtime_dtos.append(dto)
                else:
                    historical_dtos.append(dto)

            for dto in realtime_dtos:
                rows = _parse_table_to_rows(dto)
                if not rows:
                    continue
                for row in rows:
                    label = row.get("date", "")
                    code = ""
                    for candidate in ["000001", "399001", "399006"]:
                        if candidate in label:
                            code = candidate
                            break
                    if not code or code in seen_codes:
                        continue
                    close_val = _mx_parse_float(row.get("最新价", ""))
                    if close_val <= 0:
                        continue
                    change_pct = _mx_parse_float(row.get("涨跌幅", ""))
                    change_amt = _mx_parse_float(row.get("涨跌额", row.get("涨跌", "")))
                    if change_amt == 0.0 and close_val > 0 and change_pct != 0.0:
                        change_amt = round(close_val * change_pct / 100, 2)
                    seen_codes.add(code)
                    realtime_indices.append(IndexData(
                        name=code_to_name.get(code, label),
                        code=code,
                        close=close_val,
                        change_pct=change_pct,
                        change_amt=change_amt,
                    ))

            for dto in historical_dtos:
                rows = _parse_table_to_rows(dto)
                if not rows:
                    continue

                entity = dto.get("entityTagDTO") or {}
                full_name = entity.get("fullName") or ""
                name = full_name or (dto.get("entityName") or "").split("(")[0]
                index_code = name_to_code.get(name, entity.get("secuCode", ""))
                if not index_code or index_code in seen_codes:
                    continue

                row = rows[-1]
                close_val = _mx_parse_float(_find_in_row(row, ["最新价", "最新", "收盘", "点位"]))

                is_daily = "(日)" in row.get("date", "") or "(周" in row.get("date", "") or "(月" in row.get("date", "")
                if is_daily:
                    realtime_val = _mx_parse_float(_find_in_row(row, ["最新价", "最新"]))
                    if realtime_val > 0:
                        close_val = realtime_val

                if close_val <= 0:
                    continue

                change_pct = _mx_parse_float(_find_in_row(row, ["涨跌幅"]))
                change_amt = _mx_parse_float(_find_in_row(row, ["涨跌额", "涨跌值", "涨跌"]))

                seen_codes.add(index_code)
                historical_indices.append(IndexData(
                    name=name,
                    code=index_code,
                    close=close_val,
                    change_pct=change_pct,
                    change_amt=change_amt,
                ))
                logger.debug("Miaoxiang 指数 %s: close=%.2f, change_pct=%.2f%%", name, close_val, change_pct)

            indices = realtime_indices + historical_indices

            logger.debug("Miaoxiang 指数数据: %d个", len(indices))
        except Exception as e:
            logger.warning("Miaoxiang get_indices 失败: %s", e)
            raise
        logger.debug("Miaoxiang get_indices 完成 耗时%.2fs", time.monotonic() - start)
        return indices

    async def get_sector_rankings(self) -> tuple[list[SectorData], list[SectorData]]:
        logger.debug("Miaoxiang 不支持板块排名")
        return [], []

    async def get_market_statistics(self) -> MarketStatistics:
        logger.debug("Miaoxiang 不支持市场统计")
        return MarketStatistics()

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

    async def get_capital_flow(self, code: str) -> Optional[CapitalFlow]:
        start = time.monotonic()
        logger.debug("Miaoxiang 获取主力资金流向: code=%s", code)
        try:
            dto_list = await asyncio.to_thread(
                self._query_and_parse,
                f"{code} 主力资金流向 超大单净额 大单净额 中单净额 小单净额 DDX DDY DDZ"
            )
            super_large_net = 0.0
            large_net = 0.0
            medium_net = 0.0
            small_net = 0.0
            super_large_in = 0.0
            super_large_out = 0.0
            large_in = 0.0
            large_out = 0.0
            ddx = 0.0
            ddy = 0.0
            ddz = 0.0

            for dto in dto_list:
                rows = _parse_table_to_rows(dto)
                if not rows:
                    continue
                row = rows[-1]

                if super_large_net == 0.0:
                    super_large_net = _mx_parse_float(_find_in_row(row, ["超大单净额", "超大单净流入"]))
                if large_net == 0.0:
                    large_net = _mx_parse_float(_find_in_row(row, ["大单净额", "大单净流入"]))
                if medium_net == 0.0:
                    medium_net = _mx_parse_float(_find_in_row(row, ["中单净额", "中单净流入"]))
                if small_net == 0.0:
                    small_net = _mx_parse_float(_find_in_row(row, ["小单净额", "小单净流入"]))
                if super_large_in == 0.0:
                    super_large_in = _mx_parse_float(_find_in_row(row, ["超大单流入"]))
                if super_large_out == 0.0:
                    super_large_out = _mx_parse_float(_find_in_row(row, ["超大单流出"]))
                if large_in == 0.0:
                    large_in = _mx_parse_float(_find_in_row(row, ["大单流入"]))
                if large_out == 0.0:
                    large_out = _mx_parse_float(_find_in_row(row, ["大单流出"]))
                if ddx == 0.0:
                    ddx = _mx_parse_float(_find_in_row(row, ["DDX"]))
                if ddy == 0.0:
                    ddy = _mx_parse_float(_find_in_row(row, ["DDY"]))
                if ddz == 0.0:
                    ddz = _mx_parse_float(_find_in_row(row, ["DDZ"]))

            has_data = any(v != 0.0 for v in [
                super_large_net, large_net, medium_net, small_net,
                ddx, ddy, ddz,
            ])
            if not has_data:
                logger.debug("Miaoxiang 主力资金: 无有效数据")
                return None

            result = CapitalFlow(
                super_large_net=super_large_net,
                large_net=large_net,
                medium_net=medium_net,
                small_net=small_net,
                super_large_in=super_large_in,
                super_large_out=super_large_out,
                large_in=large_in,
                large_out=large_out,
                ddx=ddx,
                ddy=ddy,
                ddz=ddz,
            )
            logger.debug("Miaoxiang 主力资金: 超大单净=%.0f, 大单净=%.0f, DDX=%.2f",
                         result.super_large_net, result.large_net, result.ddx)
            logger.debug("Miaoxiang get_capital_flow 完成 耗时%.2fs", time.monotonic() - start)
            return result
        except Exception as e:
            logger.warning("Miaoxiang get_capital_flow 失败: %s", e)
            raise

    async def get_valuation(self, code: str) -> Optional[Valuation]:
        start = time.monotonic()
        logger.debug("Miaoxiang 获取估值数据: code=%s", code)
        try:
            dto_list = await asyncio.to_thread(
                self._query_and_parse,
                f"{code} 市盈率 市净率"
            )
            pe_ttm = 0.0
            pb = 0.0
            pe_percentile = 0.0
            pb_percentile = 0.0

            for dto in dto_list:
                rows = _parse_table_to_rows(dto)
                if not rows:
                    continue
                row = rows[-1]

                if pe_ttm == 0.0:
                    pe_ttm = _mx_parse_float(_find_in_row(row, ["市盈率", "PE(TTM)", "滚动市盈率"]))
                if pb == 0.0:
                    pb = _mx_parse_float(_find_in_row(row, ["市净率", "PB"]))
                if pe_percentile == 0.0:
                    pe_percentile = _mx_parse_float(_find_in_row(row, ["市盈率分位", "PE分位"]))
                if pb_percentile == 0.0:
                    pb_percentile = _mx_parse_float(_find_in_row(row, ["市净率分位", "PB分位"]))

            if pe_ttm <= 0.0 and pb <= 0.0:
                logger.debug("Miaoxiang 估值数据: 无有效数据")
                return None

            result = Valuation(
                pe_ttm=pe_ttm,
                pb=pb,
                pe_percentile=pe_percentile,
                pb_percentile=pb_percentile,
            )
            logger.debug("Miaoxiang 估值: PE=%.1f, PB=%.1f", result.pe_ttm, result.pb)
            logger.debug("Miaoxiang get_valuation 完成 耗时%.2fs", time.monotonic() - start)
            return result
        except Exception as e:
            logger.warning("Miaoxiang get_valuation 失败: %s", e)
            raise

    async def get_financial_data(self, code: str) -> Optional[FinancialData]:
        start = time.monotonic()
        logger.debug("Miaoxiang 获取财务数据: code=%s", code)
        try:
            dto_list = await asyncio.to_thread(
                self._query_and_parse,
                f"{code} 净利润 营业收入 同比增长率 净资产收益率 毛利率 资产负债率 机构持股比例"
            )
            net_profit = 0.0
            revenue = 0.0
            net_profit_yoy = 0.0
            revenue_yoy = 0.0
            roe = 0.0
            gross_margin = 0.0
            debt_ratio = 0.0
            forecast_profit = 0.0
            forecast_growth = 0.0
            institution_holding_pct = 0.0

            for dto in dto_list:
                rows = _parse_table_to_rows(dto)
                if not rows:
                    continue
                row = rows[-1]

                if net_profit == 0.0:
                    net_profit = _mx_parse_float(_find_in_row(row, ["归母净利润", "净利润"]))
                if revenue == 0.0:
                    revenue = _mx_parse_float(_find_in_row(row, ["营业收入", "营收"]))
                if net_profit_yoy == 0.0:
                    net_profit_yoy = _mx_parse_float(_find_in_row(row, ["净利润同比增长", "归母净利润同比增长"]))
                if revenue_yoy == 0.0:
                    revenue_yoy = _mx_parse_float(_find_in_row(row, ["营业收入同比增长", "营收同比增长"]))
                if roe == 0.0:
                    roe = _mx_parse_float(_find_in_row(row, ["净资产收益率", "ROE"]))
                if gross_margin == 0.0:
                    gross_margin = _mx_parse_float(_find_in_row(row, ["销售毛利率", "毛利率"]))
                if debt_ratio == 0.0:
                    debt_ratio = _mx_parse_float(_find_in_row(row, ["资产负债率"]))
                if forecast_profit == 0.0:
                    forecast_profit = _mx_parse_float(_find_in_row(row, ["预测归母净利润中值", "预测净利润"]))
                if forecast_growth == 0.0:
                    forecast_growth = _mx_parse_float(_find_in_row(row, ["预测增长率", "预测净利润增长率"]))
                if institution_holding_pct == 0.0:
                    institution_holding_pct = _mx_parse_float(_find_in_row(row, ["机构持股比例"]))

            has_data = any(v != 0.0 for v in [
                net_profit, revenue, roe, gross_margin, debt_ratio,
            ])
            if not has_data:
                logger.debug("Miaoxiang 财务数据: 无有效数据")
                return None

            result = FinancialData(
                net_profit=net_profit,
                revenue=revenue,
                net_profit_yoy=net_profit_yoy,
                revenue_yoy=revenue_yoy,
                roe=roe,
                gross_margin=gross_margin,
                debt_ratio=debt_ratio,
                forecast_profit=forecast_profit,
                forecast_growth=forecast_growth,
                institution_holding_pct=institution_holding_pct,
            )
            logger.debug("Miaoxiang 财务: 净利润=%.0f, 营收=%.0f, ROE=%.1f%%, 毛利率=%.1f%%",
                         result.net_profit, result.revenue, result.roe, result.gross_margin)
            logger.debug("Miaoxiang get_financial_data 完成 耗时%.2fs", time.monotonic() - start)
            return result
        except Exception as e:
            logger.warning("Miaoxiang get_financial_data 失败: %s", e)
            raise
