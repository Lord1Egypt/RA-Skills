#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_fetcher.py — 统一数据获取层

封装 Wind AIFin Market / tushare / akshare 三种数据源,提供统一接口,
并实现自动降级(Wind -> tushare -> akshare)与简单文件缓存机制。

对外函数:
    get_realtime_quote(stock_code)      实时行情
    get_stock_fundamentals(code)        个股基本面
    get_dragon_tiger_list(date)         龙虎榜
    get_north_flow(date)                北向资金
    get_market_breadth()                市场涨跌家数
    get_sector_rotation()               板块轮动
    get_financial_report(code, report_type) 财务报表

设计说明:
    - 三个数据源以"可选依赖"方式导入,缺失时自动跳过,不影响其它源。
    - 每个函数内部按 Wind -> tushare -> akshare 顺序尝试,首个成功即返回。
    - 文件缓存默认放在 .cache/data_fetcher/,通过 cache_ttl 控制有效期。
    - 所有函数均返回 dict(统一字段名),失败时返回带 "error" 字段的 dict。

用法:
    from data_fetcher import DataFetcher
    df = DataFetcher()
    quote = df.get_realtime_quote("600519")
"""

from __future__ import annotations

import os
import json
import time
import hashlib
import logging
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Callable

# ----------------------------------------------------------------------------
# 日志配置
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("data_fetcher")


# ----------------------------------------------------------------------------
# 数据源可用性探测(可选依赖)
# ----------------------------------------------------------------------------

def _import_akshare() -> Optional[Any]:
    """尝试导入 akshare,失败返回 None。"""

    try:
        import akshare as ak  # type: ignore
        return ak
    except Exception as exc:  # noqa: BLE001
        logger.debug("akshare 不可用: %s", exc)
        return None


def _import_tushare() -> Optional[Any]:
    """尝试导入 tushare,失败返回 None。"""

    try:
        import tushare as ts  # type: ignore
        return ts
    except Exception as exc:  # noqa: BLE001
        logger.debug("tushare 不可用: %s", exc)
        return None


class WindClient:
    """Wind AIFin Market 数据源客户端(MCP/Skill 形式)。

    实际环境中由 install.sh 安装的 wind-mcp-skill 提供,这里封装为可选调用。
    若未配置 API Key 或 skill 未安装,所有方法返回 None 表示"不可用"。
    """

    def __init__(self, api_key: str = "") -> None:
        self.api_key = api_key or os.environ.get("WIND_API_KEY", "")
        self.available = bool(self.api_key)
        if self.available:
            logger.info("Wind 数据源就绪(API Key 已配置)")
        else:
            logger.info("Wind 数据源未配置(无 WIND_API_KEY),将降级到 tushare/akshare")

    def call(self, func_name: str, **params: Any) -> Optional[Dict[str, Any]]:
        """调用 Wind skill 函数(占位实现)。

        真实环境应通过 MCP 协议调用 wind-mcp-skill 暴露的工具。
        此处返回 None 表示当前环境不可用,触发降级。
        """

        if not self.available:
            return None
        # 占位:真实调用由 wind-mcp-skill 在 Agent 环境中完成
        logger.debug("Wind call %s %s (占位,需在 Agent 环境中调用)", func_name, params)
        return None


# ----------------------------------------------------------------------------
# 主数据获取类
# ----------------------------------------------------------------------------

class DataFetcher:
    """统一数据获取层。

    Attributes:
        wind:     Wind 数据源客户端。
        tushare:  tushare 接口(已设置 token 时可用)。
        akshare:  akshare 接口(开箱即用)。
        cache_dir:缓存目录。
        cache_ttl:缓存有效期(秒)。
    """

    def __init__(
        self,
        wind_api_key: str = "",
        tushare_token: str = "",
        cache_dir: str = "",
        cache_ttl: int = 300,
    ) -> None:
        # Wind
        self.wind = WindClient(api_key=wind_api_key)
        # tushare
        self.tushare = _import_tushare()
        token = tushare_token or os.environ.get("TUSHARE_TOKEN", "")
        if self.tushare is not None and token:
            try:
                self.tushare.set_token(token)
                logger.info("tushare 数据源就绪(token 已设置)")
            except Exception as exc:  # noqa: BLE001
                logger.warning("tushare token 设置失败: %s", exc)
                self.tushare = None
        elif self.tushare is not None:
            logger.info("tushare 已安装但未配置 token,部分接口将不可用")
        # akshare
        self.akshare = _import_akshare()
        if self.akshare is not None:
            logger.info("akshare 数据源就绪")
        # 缓存
        self.cache_dir = cache_dir or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".cache",
            "data_fetcher",
        )
        self.cache_ttl = cache_ttl
        os.makedirs(self.cache_dir, exist_ok=True)

        if not (self.wind.available or self.tushare or self.akshare):
            logger.warning("未发现任何可用数据源!请运行 install.sh 安装依赖。")

    # =====================================================================
    # 缓存机制
    # =====================================================================

    def _cache_key(self, name: str, **params: Any) -> str:
        """根据函数名与参数生成缓存文件名。"""

        raw = json.dumps({"name": name, "params": params}, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(raw.encode("utf-8")).hexdigest()

    def _cache_get(self, name: str, **params: Any) -> Optional[Any]:
        """读取缓存,过期或不存在返回 None。"""

        key = self._cache_key(name, **params)
        path = os.path.join(self.cache_dir, f"{name}_{key}.json")
        if not os.path.exists(path):
            return None
        age = time.time() - os.path.getmtime(path)
        if age > self.cache_ttl:
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:  # noqa: BLE001
            logger.debug("缓存读取失败: %s", exc)
            return None

    def _cache_set(self, name: str, data: Any, **params: Any) -> None:
        """写入缓存。"""

        key = self._cache_key(name, **params)
        path = os.path.join(self.cache_dir, f"{name}_{key}.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, default=str)
        except Exception as exc:  # noqa: BLE001
            logger.debug("缓存写入失败: %s", exc)

    def _try_sources(
        self,
        cache_name: str,
        sources: List[Callable[[], Optional[Dict[str, Any]]]],
        **cache_params: Any,
    ) -> Dict[str, Any]:
        """通用降级执行:依次尝试各数据源,首个成功结果缓存后返回。"""

        # 1. 命中缓存
        cached = self._cache_get(cache_name, **cache_params)
        if cached is not None:
            logger.debug("命中缓存: %s", cache_name)
            cached["_source"] = cached.get("_source", "cache")
            return cached
        # 2. 依次尝试数据源
        for idx, src_fn in enumerate(sources):
            try:
                result = src_fn()
            except Exception as exc:  # noqa: BLE001
                logger.warning("数据源[%d]调用异常: %s", idx, exc)
                result = None
            if result is not None:
                self._cache_set(cache_name, result, **cache_params)
                return result
        # 3. 全部失败
        return {"error": f"所有数据源均无法获取 {cache_name}", "_source": "none"}

    # =====================================================================
    # 对外接口
    # =====================================================================

    def get_realtime_quote(self, stock_code: str) -> Dict[str, Any]:
        """获取个股实时行情。

        Args:
            stock_code: 股票代码,如 "600519"(沪深可自动识别)。

        Returns:
            dict,字段: stock_code, name, price, change_pct, volume, amount, _source。
        """

        def from_wind() -> Optional[Dict[str, Any]]:
            res = self.wind.call("get_realtime_quote", code=stock_code)
            return res

        def from_tushare() -> Optional[Dict[str, Any]]:
            if not self.tushare:
                return None
            try:
                ts_code = _to_ts_code(stock_code)
                pro = self.tushare.pro_api()
                df = pro.daily(ts_code=ts_code)  # type: ignore[attr-defined]
                if df is None or len(df) == 0:
                    return None
                row = df.iloc[0]
                return {
                    "stock_code": stock_code,
                    "name": "",
                    "price": float(row.get("close", 0)),
                    "change_pct": float(row.get("pct_chg", 0)) / 100.0,
                    "volume": float(row.get("vol", 0)),
                    "amount": float(row.get("amount", 0)) * 1000.0,
                    "_source": "tushare",
                }
            except Exception as exc:  # noqa: BLE001
                logger.debug("tushare realtime 失败: %s", exc)
                return None

        def from_akshare() -> Optional[Dict[str, Any]]:
            if not self.akshare:
                return None
            try:
                df = self.akshare.stock_zh_a_spot_em()  # type: ignore[attr-defined]
                if df is None or len(df) == 0:
                    return None
                row = df[df["代码"] == stock_code]
                if len(row) == 0:
                    return None
                row = row.iloc[0]
                return {
                    "stock_code": stock_code,
                    "name": str(row.get("名称", "")),
                    "price": float(row.get("最新价", 0) or 0),
                    "change_pct": float(row.get("涨跌幅", 0) or 0) / 100.0,
                    "volume": float(row.get("成交量", 0) or 0),
                    "amount": float(row.get("成交额", 0) or 0),
                    "_source": "akshare",
                }
            except Exception as exc:  # noqa: BLE001
                logger.debug("akshare realtime 失败: %s", exc)
                return None

        return self._try_sources(
            "realtime_quote", [from_wind, from_tushare, from_akshare],
            stock_code=stock_code,
        )

    def get_stock_fundamentals(self, code: str) -> Dict[str, Any]:
        """获取个股基本面数据(PE/PB/市值/行业等)。

        Args:
            code: 股票代码。

        Returns:
            dict,字段: stock_code, name, pe, pb, total_mv, industry, _source。
        """

        def from_wind() -> Optional[Dict[str, Any]]:
            return self.wind.call("get_stock_fundamentals", code=code)

        def from_tushare() -> Optional[Dict[str, Any]]:
            if not self.tushare:
                return None
            try:
                ts_code = _to_ts_code(code)
                pro = self.tushare.pro_api()
                df = pro.daily_basic(ts_code=ts_code)  # type: ignore[attr-defined]
                if df is None or len(df) == 0:
                    return None
                row = df.iloc[0]
                return {
                    "stock_code": code,
                    "name": "",
                    "pe": float(row.get("pe", 0) or 0),
                    "pb": float(row.get("pb", 0) or 0),
                    "total_mv": float(row.get("total_mv", 0) or 0) * 10000.0,
                    "industry": "",
                    "_source": "tushare",
                }
            except Exception as exc:  # noqa: BLE001
                logger.debug("tushare fundamentals 失败: %s", exc)
                return None

        def from_akshare() -> Optional[Dict[str, Any]]:
            if not self.akshare:
                return None
            try:
                df = self.akshare.stock_zh_a_spot_em()  # type: ignore[attr-defined]
                if df is None:
                    return None
                row = df[df["代码"] == code]
                if len(row) == 0:
                    return None
                row = row.iloc[0]
                return {
                    "stock_code": code,
                    "name": str(row.get("名称", "")),
                    "pe": float(row.get("市盈率-动态", 0) or 0),
                    "pb": float(row.get("市净率", 0) or 0),
                    "total_mv": float(row.get("总市值", 0) or 0),
                    "industry": "",
                    "_source": "akshare",
                }
            except Exception as exc:  # noqa: BLE001
                logger.debug("akshare fundamentals 失败: %s", exc)
                return None

        return self._try_sources(
            "stock_fundamentals", [from_wind, from_tushare, from_akshare],
            code=code,
        )

    def get_dragon_tiger_list(self, date_str: str) -> Dict[str, Any]:
        """获取龙虎榜数据。

        Args:
            date_str: 日期字符串,格式 "YYYYMMDD" 或 "YYYY-MM-DD"。

        Returns:
            dict,字段: date, items(list), _source。
        """

        date_str = _normalize_date(date_str)

        def from_wind() -> Optional[Dict[str, Any]]:
            return self.wind.call("get_dragon_tiger_list", date=date_str)

        def from_tushare() -> Optional[Dict[str, Any]]:
            if not self.tushare:
                return None
            try:
                pro = self.tushare.pro_api()
                df = pro.top_list(trade_date=date_str)  # type: ignore[attr-defined]
                if df is None or len(df) == 0:
                    return None
                items = df.to_dict(orient="records")
                return {"date": date_str, "items": items, "_source": "tushare"}
            except Exception as exc:  # noqa: BLE001
                logger.debug("tushare dragon_tiger 失败: %s", exc)
                return None

        def from_akshare() -> Optional[Dict[str, Any]]:
            if not self.akshare:
                return None
            try:
                df = self.akshare.stock_lhb_detail_em(  # type: ignore[attr-defined]
                    start_date=date_str, end_date=date_str
                )
                if df is None or len(df) == 0:
                    return None
                items = df.to_dict(orient="records")
                return {"date": date_str, "items": items, "_source": "akshare"}
            except Exception as exc:  # noqa: BLE001
                logger.debug("akshare dragon_tiger 失败: %s", exc)
                return None

        return self._try_sources(
            "dragon_tiger_list", [from_wind, from_tushare, from_akshare],
            date_str=date_str,
        )

    def get_north_flow(self, date_str: str) -> Dict[str, Any]:
        """获取北向资金流入数据。

        Args:
            date_str: 日期字符串。

        Returns:
            dict,字段: date, net_buy, sh_buy, sz_buy, _source。
        """

        date_str = _normalize_date(date_str)

        def from_wind() -> Optional[Dict[str, Any]]:
            return self.wind.call("get_north_flow", date=date_str)

        def from_tushare() -> Optional[Dict[str, Any]]:
            if not self.tushare:
                return None
            try:
                pro = self.tushare.pro_api()
                df = pro.moneyflow_hsgt(trade_date=date_str)  # type: ignore[attr-defined]
                if df is None or len(df) == 0:
                    return None
                row = df.iloc[0]
                return {
                    "date": date_str,
                    "net_buy": float(row.get("north_money", 0) or 0),
                    "sh_buy": float(row.get("hgt_buy_amount", 0) or 0),
                    "sz_buy": float(row.get("sgt_buy_amount", 0) or 0),
                    "_source": "tushare",
                }
            except Exception as exc:  # noqa: BLE001
                logger.debug("tushare north_flow 失败: %s", exc)
                return None

        def from_akshare() -> Optional[Dict[str, Any]]:
            if not self.akshare:
                return None
            try:
                df = self.akshare.stock_hsgt_north_net_flow_in_em(  # type: ignore[attr-defined]
                    symbol="北上"
                )
                if df is None or len(df) == 0:
                    return None
                df = df.sort_values("日期", ascending=False)
                row = df.iloc[0]
                return {
                    "date": date_str,
                    "net_buy": float(row.get("当日成交净买额", 0) or 0),
                    "sh_buy": 0.0,
                    "sz_buy": 0.0,
                    "_source": "akshare",
                }
            except Exception as exc:  # noqa: BLE001
                logger.debug("akshare north_flow 失败: %s", exc)
                return None

        return self._try_sources(
            "north_flow", [from_wind, from_tushare, from_akshare],
            date_str=date_str,
        )

    def get_market_breadth(self) -> Dict[str, Any]:
        """获取市场涨跌家数(广度)。

        Returns:
            dict,字段: advance, decline, flat, total, _source。
        """

        def from_wind() -> Optional[Dict[str, Any]]:
            return self.wind.call("get_market_breadth")

        def from_akshare() -> Optional[Dict[str, Any]]:
            if not self.akshare:
                return None
            try:
                df = self.akshare.stock_zh_a_spot_em()  # type: ignore[attr-defined]
                if df is None or len(df) == 0:
                    return None
                changes = df["涨跌幅"]
                advance = int((changes > 0).sum())
                decline = int((changes < 0).sum())
                flat = int((changes == 0).sum())
                return {
                    "advance": advance,
                    "decline": decline,
                    "flat": flat,
                    "total": int(len(df)),
                    "_source": "akshare",
                }
            except Exception as exc:  # noqa: BLE001
                logger.debug("akshare breadth 失败: %s", exc)
                return None

        return self._try_sources(
            "market_breadth", [from_wind, from_akshare],
        )

    def get_sector_rotation(self) -> Dict[str, Any]:
        """获取板块轮动数据(行业板块涨跌幅排名)。

        Returns:
            dict,字段: sectors(list of {name, change_pct}), _source。
        """

        def from_wind() -> Optional[Dict[str, Any]]:
            return self.wind.call("get_sector_rotation")

        def from_akshare() -> Optional[Dict[str, Any]]:
            if not self.akshare:
                return None
            try:
                df = self.akshare.stock_board_industry_name_em()  # type: ignore[attr-defined]
                if df is None or len(df) == 0:
                    return None
                cols = df.columns
                name_col = "板块名称" if "板块名称" in cols else cols[0]
                chg_col = "涨跌幅" if "涨跌幅" in cols else cols[2]
                df = df.sort_values(by=chg_col, ascending=False)
                sectors = [
                    {"name": str(r[name_col]), "change_pct": float(r[chg_col] or 0)}
                    for _, r in df.head(20).iterrows()
                ]
                return {"sectors": sectors, "_source": "akshare"}
            except Exception as exc:  # noqa: BLE001
                logger.debug("akshare sector_rotation 失败: %s", exc)
                return None

        return self._try_sources(
            "sector_rotation", [from_wind, from_akshare],
        )

    def get_financial_report(self, code: str, report_type: str = "income") -> Dict[str, Any]:
        """获取财务报表。

        Args:
            code:        股票代码。
            report_type: 报表类型 income(利润表)/ balancesheet(资产负债表) /
                         cashflow(现金流量表)。

        Returns:
            dict,字段: stock_code, report_type, items(list), _source。
        """

        def from_wind() -> Optional[Dict[str, Any]]:
            return self.wind.call(
                "get_financial_report", code=code, report_type=report_type
            )

        def from_tushare() -> Optional[Dict[str, Any]]:
            if not self.tushare:
                return None
            try:
                ts_code = _to_ts_code(code)
                pro = self.tushare.pro_api()
                api_map = {
                    "income": "income",
                    "balancesheet": "balancesheet",
                    "cashflow": "cashflow",
                }
                api_name = api_map.get(report_type, "income")
                df = getattr(pro, api_name)(ts_code=ts_code, period="")
                if df is None or len(df) == 0:
                    return None
                items = df.head(4).to_dict(orient="records")
                return {
                    "stock_code": code,
                    "report_type": report_type,
                    "items": items,
                    "_source": "tushare",
                }
            except Exception as exc:  # noqa: BLE001
                logger.debug("tushare financial_report 失败: %s", exc)
                return None

        def from_akshare() -> Optional[Dict[str, Any]]:
            if not self.akshare:
                return None
            try:
                fn_map = {
                    "income": "stock_financial_report_sina",
                    "balancesheet": "stock_financial_report_sina",
                    "cashflow": "stock_financial_report_sina",
                }
                fn_name = fn_map.get(report_type, "stock_financial_report_sina")
                fn = getattr(self.akshare, fn_name, None)
                if fn is None:
                    return None
                df = fn(stock=f"sh{code}" if code.startswith("6") else f"sz{code}",
                        symbol=report_type)
                if df is None or len(df) == 0:
                    return None
                items = df.head(4).to_dict(orient="records")
                return {
                    "stock_code": code,
                    "report_type": report_type,
                    "items": items,
                    "_source": "akshare",
                }
            except Exception as exc:  # noqa: BLE001
                logger.debug("akshare financial_report 失败: %s", exc)
                return None

        return self._try_sources(
            "financial_report", [from_wind, from_tushare, from_akshare],
            code=code, report_type=report_type,
        )


# ----------------------------------------------------------------------------
# 工具函数
# ----------------------------------------------------------------------------

def _to_ts_code(stock_code: str) -> str:
    """将简短代码转换为 tushare 的 ts_code 格式(带交易所后缀)。

    示例:
        "600519" -> "600519.SH"
        "000001" -> "000001.SZ"
        "300750" -> "300750.SZ"
        "688981" -> "688981.SH"
    """

    code = stock_code.strip().upper()
    if "." in code:
        return code
    if code.startswith(("6", "9", "11", "13")):
        return f"{code}.SH"
    return f"{code}.SZ"


def _normalize_date(date_str: str) -> str:
    """将日期统一为 YYYYMMDD 格式。"""

    date_str = date_str.strip()
    if "-" in date_str:
        return date_str.replace("-", "")
    if "/" in date_str:
        return date_str.replace("/", "")
    return date_str


# ----------------------------------------------------------------------------
# 模块级便捷实例(懒加载)
# ----------------------------------------------------------------------------

_default_fetcher: Optional[DataFetcher] = None


def get_fetcher() -> DataFetcher:
    """获取默认的 DataFetcher 单例(从环境变量读取 token)。"""

    global _default_fetcher
    if _default_fetcher is None:
        _default_fetcher = DataFetcher(
            wind_api_key=os.environ.get("WIND_API_KEY", ""),
            tushare_token=os.environ.get("TUSHARE_TOKEN", ""),
        )
    return _default_fetcher


# ----------------------------------------------------------------------------
# 自测入口
# ----------------------------------------------------------------------------

def _demo() -> None:
    """演示:尝试获取贵州茅台实时行情与市场广度。"""

    df = get_fetcher()
    print("== 实时行情 600519 ==")
    print(json.dumps(df.get_realtime_quote("600519"), ensure_ascii=False, indent=2, default=str))
    print("== 市场广度 ==")
    print(json.dumps(df.get_market_breadth(), ensure_ascii=False, indent=2, default=str))
    print("== 板块轮动 ==")
    print(json.dumps(df.get_sector_rotation(), ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    _demo()
