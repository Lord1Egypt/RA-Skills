#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票技术分析工具 v1.5.1
支持A股、港股、美股、基金(ETF/LOF/开放式)的实时技术分析
数据来源：新浪财经（A股主）、yfinance（港美股主）、akshare（备用）、东财直接API（基金备用）
"""

import argparse
import json
import logging
import re
import sys
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

# ============================================================
# 配置文件模块
# ============================================================
import os

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".stock-analysis")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "watchlist": [],
    "defaults": {
        "market": "auto",
        "days": 60,
        "asset_type": "stock",
    },
}


def _load_config() -> Dict:
    """加载配置文件，不存在则创建默认配置"""
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        # 合并缺失的默认字段
        for key, val in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = val.copy() if isinstance(val, dict) else val
        for key, val in DEFAULT_CONFIG.get("defaults", {}).items():
            if key not in config.get("defaults", {}):
                config.setdefault("defaults", {})[key] = val
        return config
    except (json.JSONDecodeError, IOError) as e:
        print(f"[WARNING] 配置文件读取失败，使用默认配置: {e}", file=sys.stderr)
        return DEFAULT_CONFIG.copy()


def _save_config(config: Dict) -> None:
    """保存配置文件"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


# 标准库
import numpy as np
import pandas as pd

# 必需依赖（A 股/基金数据源核心）
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

# ============================================================
# 日志配置
# ============================================================
logger = logging.getLogger("stock_analysis")
_handler = logging.StreamHandler(sys.stderr)
_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(_handler)
logger.setLevel(logging.WARNING)


# ============================================================
# 常量定义
# ============================================================
VERSION = "1.8.0"

# A股上海交易所代码前缀
SH_PREFIXES = ("6", "5", "7", "9")

# 基金类型代码规则
ETF_PREFIXES = ("15", "51", "58")
LOF_PREFIXES = ("16",)
# 自动识别的基金前缀（ETF/LOF，高置信度）
AUTO_FUND_PREFIXES = ETF_PREFIXES + LOF_PREFIXES
# 需要显式 -t fund 指定的基金前缀（开放式基金，与股票代码重叠）
EXPLICIT_FUND_PREFIXES = AUTO_FUND_PREFIXES + ("00", "01", "11", "18")

# 评分阈值
SCORE_STRONG_UP = 75
SCORE_UP = 60
SCORE_SIDEWAYS_LOW = 40
SCORE_DOWN = 25

# 布林带位置阈值
BB_LOWER_THRESHOLD = 0.3
BB_UPPER_THRESHOLD = 0.7


# ============================================================
# 数据获取器
# ============================================================
class StockDataFetcher:
    """多数据源股票/基金数据获取器"""

    # -------------------- 代码标准化 --------------------

    @staticmethod
    def normalize_stock_code(
        code: str, market: str = "auto", asset_type: str = "stock"
    ) -> Tuple[str, str, str]:
        """
        标准化证券代码，自动识别市场和资产类型。

        Returns:
            (标准代码, 市场, 资产类型)
        """
        code = code.strip().upper()

        # 港股识别（优先于基金，因为 00700 等以 00 开头）
        if code.startswith("HK.") or code.startswith("港."):
            clean = code.replace("HK.", "").replace("港.", "")
            return clean, "hkstock", "stock"

        # 基金识别：仅高置信度前缀（ETF/LOF）自动识别，开放式基金需 -t fund 指定
        if asset_type == "fund" or (
            len(code) == 6 and code.isdigit() and code.startswith(AUTO_FUND_PREFIXES)
        ):
            return code, "ashare", "fund"

        # 美股识别：含市场标识或纯字母
        if any(k in code for k in ("US", "NASDAQ", "NYSE", "AMEX")) or (
            code.isalpha() and len(code) > 1
        ):
            clean = code.replace("US.", "").replace("NASDAQ:", "").replace("NYSE:", "").replace("AMEX:", "")
            return clean, "usstock", "stock"

        # 指定市场
        if market != "auto":
            return code, market, asset_type

        # A股默认
        if len(code) == 6 and code.isdigit():
            return code, "ashare", "stock"

        return code, "ashare", "stock"

    # -------------------- 新浪数据源（A股） --------------------

    @staticmethod
    def _build_sina_symbol(code: str) -> str:
        """构建新浪证券代码"""
        return f"sh{code}" if code.startswith(SH_PREFIXES) else f"sz{code}"

    @staticmethod
    def fetch_stock_data_sina(
        code: str, market: str, days: int = 60
    ) -> Optional[pd.DataFrame]:
        """通过新浪接口获取A股历史K线数据（带2次重试）"""
        if market != "ashare" or not REQUESTS_AVAILABLE:
            return None

        for attempt in range(3):
            try:
                symbol = StockDataFetcher._build_sina_symbol(code)
                url = "https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData"
                params = {"symbol": symbol, "scale": "240", "ma": "no", "datalen": days}

                resp = requests.get(url, params=params, timeout=10)
                data = resp.json()

                if not data or not isinstance(data, list):
                    return None

                records = []
                for item in data:
                    records.append({
                        "date": pd.to_datetime(item.get("day", "")),
                        "open": pd.to_numeric(item.get("open", 0), errors="coerce"),
                        "high": pd.to_numeric(item.get("high", 0), errors="coerce"),
                        "low": pd.to_numeric(item.get("low", 0), errors="coerce"),
                        "close": pd.to_numeric(item.get("close", 0), errors="coerce"),
                        "volume": pd.to_numeric(item.get("volume", 0), errors="coerce"),
                        "amount": pd.to_numeric(item.get("amount", 0), errors="coerce"),
                    })

                df = pd.DataFrame(records)
                if df.empty:
                    return None

                df["pct_change"] = df["close"].pct_change() * 100
                df = df.sort_values("date").reset_index(drop=True)
                return df

            except Exception as e:
                logger.warning("新浪历史数据第%d次尝试失败 [%s]: %s", attempt + 1, code, e)
                if attempt < 2:
                    time.sleep(1)

        return None

    @staticmethod
    def fetch_realtime_quote_sina(code: str, market: str) -> Optional[Dict]:
        """通过新浪接口获取A股实时行情"""
        if market != "ashare" or not REQUESTS_AVAILABLE:
            return None

        try:
            symbol = StockDataFetcher._build_sina_symbol(code)
            url = f"https://hq.sinajs.cn/list={symbol}"
            headers = {"Referer": "https://finance.sina.com.cn"}

            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            resp.encoding = "gbk"

            match = re.search(r'="(.+)"', resp.text)
            if not match:
                return None

            parts = match.group(1).split(",")
            if len(parts) < 32:
                return None

            name = parts[0]
            open_price = float(parts[1]) if parts[1] else 0
            prev_close = float(parts[2]) if parts[2] else 0
            current = float(parts[3]) if parts[3] else 0
            high = float(parts[4]) if parts[4] else 0
            low = float(parts[5]) if parts[5] else 0
            volume = float(parts[8]) if parts[8] else 0
            amount = float(parts[9]) if parts[9] else 0

            pct_change = ((current - prev_close) / prev_close * 100) if prev_close > 0 else 0

            return {
                "name": name,
                "price": current,
                "change": round(current - prev_close, 4),
                "pct_change": round(pct_change, 2),
                "open": open_price,
                "high": high,
                "low": low,
                "prev_close": prev_close,
                "volume": volume,
                "amount": amount,
                "time": datetime.now().strftime("%H:%M:%S"),
            }

        except Exception as e:
            logger.warning("新浪实时行情失败 [%s]: %s", code, e)
            return None

    # -------------------- yfinance 数据源（港美股） --------------------

    @staticmethod
    def _build_yfinance_code(code: str, market: str) -> Optional[str]:
        """构建 yfinance 代码格式"""
        if market == "hkstock":
            return f"{code.zfill(4)}.HK"
        elif market == "usstock":
            return code
        return None

    @staticmethod
    def fetch_stock_data_yfinance(
        code: str, market: str, days: int = 60
    ) -> Optional[pd.DataFrame]:
        """通过 yfinance 获取港美股历史数据（带2次重试）"""
        if not YFINANCE_AVAILABLE:
            return None

        for attempt in range(3):
            try:
                yf_code = StockDataFetcher._build_yfinance_code(code, market)
                if yf_code is None:
                    return None

                ticker = yf.Ticker(yf_code)
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days * 2)

                df = ticker.history(start=start_date, end=end_date, period=None)
                if df.empty:
                    return None

                df = df.reset_index()
                df = df.rename(columns={
                    "Date": "date", "Open": "open", "High": "high",
                    "Low": "low", "Close": "close", "Volume": "volume",
                })
                # 补充 amount 列（yfinance 无成交额，用 0 填充）
                df["amount"] = 0
                df["pct_change"] = df["close"].pct_change() * 100
                df = df.sort_values("date").reset_index(drop=True)
                return df

            except Exception as e:
                logger.warning("yfinance历史数据第%d次尝试失败 [%s]: %s", attempt + 1, code, e)
                if attempt < 2:
                    time.sleep(2)

        return None

    @staticmethod
    def fetch_realtime_quote_yfinance(code: str, market: str) -> Optional[Dict]:
        """通过 yfinance 获取港美股实时行情"""
        if not YFINANCE_AVAILABLE:
            return None

        try:
            yf_code = StockDataFetcher._build_yfinance_code(code, market)
            if yf_code is None:
                return None

            ticker = yf.Ticker(yf_code)
            info = ticker.info

            return {
                "name": info.get("shortName", code),
                "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
                "change": info.get("regularMarketChange", 0),
                "pct_change": round(info.get("regularMarketChangePercent", 0) * 100, 2) if info.get("regularMarketChangePercent") else 0,
                "open": info.get("regularMarketOpen", info.get("open", 0)),
                "high": info.get("dayHigh", 0),
                "low": info.get("dayLow", 0),
                "prev_close": info.get("regularMarketPreviousClose", info.get("previousClose", 0)),
                "volume": info.get("volume", 0),
                "amount": 0,
                "time": datetime.now().strftime("%H:%M:%S"),
            }

        except Exception as e:
            logger.warning("yfinance实时行情失败 [%s]: %s", code, e)
            return None

    # -------------------- akshare 数据源（通用备用） --------------------

    @staticmethod
    def fetch_stock_data_akshare(
        code: str, market: str, days: int = 60
    ) -> Optional[pd.DataFrame]:
        """通过 akshare 获取股票数据（带3次重试）"""
        if not AKSHARE_AVAILABLE:
            return None

        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days * 2)).strftime("%Y%m%d")
        df = None

        for attempt in range(3):
            df = None  # 每次重试前重置，避免返回脏数据
            try:
                if market == "usstock":
                    df = ak.stock_us_hist(
                        symbol=code, period="daily",
                        start_date=start_date, end_date=end_date, adjust="",
                    )
                elif market == "hkstock":
                    df = ak.stock_hk_hist(
                        symbol=code, period="daily",
                        start_date=start_date, end_date=end_date, adjust="",
                    )
                else:
                    df = ak.stock_zh_a_hist(
                        symbol=code, period="daily",
                        start_date=start_date, end_date=end_date, adjust="",
                    )

                if df is not None and not df.empty:
                    df = df.rename(columns={
                        "日期": "date", "开盘": "open", "收盘": "close",
                        "最高": "high", "最低": "low", "成交量": "volume",
                        "成交额": "amount", "涨跌幅": "pct_change",
                    })
                    df["date"] = pd.to_datetime(df["date"])
                    df = df.sort_values("date").reset_index(drop=True)
                    return df

            except Exception as e:
                logger.warning("akshare第%d次尝试失败 [%s]: %s", attempt + 1, code, e)
                time.sleep(2)

        return df

    @staticmethod
    def fetch_realtime_quote_akshare(code: str, market: str) -> Optional[Dict]:
        """通过 akshare 获取实时行情"""
        if not AKSHARE_AVAILABLE:
            return None

        try:
            if market == "usstock":
                df = ak.stock_us_spot_em()
                row = df[df["代码"] == code]
                if row.empty:
                    row = df[df["名称"].str.contains(code, case=False, na=False)]
            elif market == "hkstock":
                df = ak.stock_hk_spot_em()
                row = df[df["代码"] == code]
            else:
                df = ak.stock_zh_a_spot_em()
                row = df[df["代码"] == code]

            if row.empty:
                return None

            row = row.iloc[0]
            return {
                "name": str(row.get("名称", code)),
                "price": float(row.get("最新价", 0)),
                "change": float(row.get("涨跌额", 0)),
                "pct_change": float(row.get("涨跌幅", 0)),
                "high": float(row.get("最高", 0)),
                "low": float(row.get("最低", 0)),
                "volume": float(row.get("成交量", 0)),
                "amount": float(row.get("成交额", 0)),
                "time": str(row.get("时间", "")),
            }

        except Exception as e:
            logger.warning("akshare实时行情失败 [%s]: %s", code, e)
            return None

    # -------------------- 东财直接API（基金备用） --------------------

    @staticmethod
    def fetch_fund_data_eastmoney_direct(
        code: str, start_date: str, end_date: str, days: int = 60
    ) -> Optional[pd.DataFrame]:
        """直接调用东财基金历史API（绕过akshare）"""
        if not REQUESTS_AVAILABLE:
            return None

        try:
            url = "https://api.fund.eastmoney.com/f10/lsjz"
            params = {
                "fundCode": code,
                "pageIndex": 1,
                "pageSize": 120,
                "startDate": start_date,
                "endDate": end_date,
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Referer": "https://fund.eastmoney.com/",
            }
            resp = requests.get(url, params=params, headers=headers, timeout=15)
            resp.encoding = "utf-8"

            match = re.search(r"\{.*\}", resp.text.strip(), re.DOTALL)
            if not match:
                return None

            data = json.loads(match.group())
            records = data.get("Data", {}).get("LSJZList", [])
            if not records:
                return None

            rows = []
            for rec in records:
                nav = float(rec.get("DWJZ", 0))
                rows.append({
                    "date": pd.to_datetime(rec.get("FSRQ", "")),
                    "open": nav,
                    "high": nav,
                    "low": nav,
                    "close": nav,
                    "volume": 0,
                    "pct_change": float(rec.get("JZZZL", 0)) if rec.get("JZZZL") else 0,
                })

            df = pd.DataFrame(rows)
            df = df.sort_values("date").reset_index(drop=True)
            if len(df) > days:
                df = df.tail(days).reset_index(drop=True)
            return df

        except Exception as e:
            logger.warning("东财基金直接API失败 [%s]: %s", code, e)
            return None

    # -------------------- 基金数据源 --------------------

    @staticmethod
    def get_fund_type(code: str) -> str:
        """
        判断基金类型。

        Returns:
            'etf' | 'lof' | 'open'
        """
        if code.startswith(ETF_PREFIXES):
            return "etf"
        elif code.startswith(LOF_PREFIXES):
            return "lof"
        return "open"

    @staticmethod
    def fetch_fund_data_akshare(code: str, days: int = 60) -> Optional[pd.DataFrame]:
        """通过 akshare 获取基金净值数据（多级回退）"""
        if not AKSHARE_AVAILABLE:
            logger.warning("akshare未安装，无法获取基金数据 [%s]", code)
            return None

        fund_type = StockDataFetcher.get_fund_type(code)
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=days * 2)).strftime("%Y%m%d")

        df = None

        if fund_type in ("etf", "lof"):
            df = StockDataFetcher._fetch_fund_etf_lof(code, fund_type, days, start_date, end_date)
        else:
            df = StockDataFetcher._fetch_fund_open(code, days, start_date, end_date)

        if df is None or df.empty:
            logger.warning("基金 %s 数据获取失败", code)
            return None

        # 统一后处理
        df["date"] = pd.to_datetime(df["date"])
        if "pct_change" in df.columns:
            df["pct_change"] = pd.to_numeric(df["pct_change"], errors="coerce")
        df = df.sort_values("date").reset_index(drop=True)
        if len(df) > days:
            df = df.tail(days).reset_index(drop=True)

        return df

    @staticmethod
    def _fetch_fund_etf_lof(
        code: str, fund_type: str, days: int, start_date: str, end_date: str
    ) -> Optional[pd.DataFrame]:
        """获取 ETF/LOF 基金数据（新浪 → 东财akshare → 东财直接API）"""
        logger.info("获取ETF/LOF数据: %s (类型: %s)", code, fund_type)
        df = None

        # 1. 尝试新浪ETF接口
        try:
            sina_symbol = StockDataFetcher._build_sina_symbol(code)
            df = ak.fund.fund_etf_sina.fund_etf_hist_sina(symbol=sina_symbol)
            if df is not None and not df.empty:
                df = df.rename(columns={
                    "date": "date", "open": "open", "close": "close",
                    "high": "high", "low": "low", "volume": "volume",
                    "amount": "amount",
                })
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                if len(df) > days:
                    df = df.tail(days).reset_index(drop=True)
                return df
        except Exception as e:
            logger.warning("新浪ETF接口失败，回退东财: %s", e)

        # 2. 东财 akshare 接口
        try:
            if fund_type == "etf":
                df = ak.fund_etf_hist_em(
                    symbol=code, period="daily",
                    start_date=start_date, end_date=end_date, adjust="",
                )
            else:
                df = ak.fund.fund_lof_em.fund_lof_hist_em(
                    symbol=code, period="daily",
                    start_date=start_date, end_date=end_date, adjust="",
                )
            if df is not None and not df.empty:
                df = df.rename(columns={
                    "日期": "date", "开盘": "open", "收盘": "close",
                    "最高": "high", "最低": "low", "成交量": "volume",
                    "成交额": "amount", "涨跌幅": "pct_change",
                })
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                return df
        except Exception as e:
            logger.warning("东财akshare ETF/LOF接口失败: %s", e)
            df = None

        # 3. 东财直接API
        df2 = StockDataFetcher.fetch_fund_data_eastmoney_direct(code, start_date, end_date, days)
        if df2 is not None and not df2.empty:
            return df2

        return None

    @staticmethod
    def _fetch_fund_open(
        code: str, days: int, start_date: str, end_date: str
    ) -> Optional[pd.DataFrame]:
        """获取开放式基金数据（fund_open_fund_info_em → 东财直接API → LOF回退）"""
        logger.info("获取开放式基金数据: %s", code)
        df = None

        # 1. fund_open_fund_info_em
        try:
            df = ak.fund.fund_em.fund_open_fund_info_em(
                symbol=code, indicator="单位净值走势", period="近1年",
            )
            if df is not None and not df.empty:
                df = df.rename(columns={
                    "净值日期": "date", "单位净值": "close", "日增长率": "pct_change",
                })
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                df["open"] = df["close"]
                df["high"] = df["close"]
                df["low"] = df["close"]
                df["volume"] = 0
                df["pct_change"] = pd.to_numeric(df["pct_change"], errors="coerce")
                df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
                if len(df) > days:
                    df = df.tail(days).reset_index(drop=True)
                return df
        except Exception as e:
            logger.warning("fund_open_fund_info_em 失败: %s", e)
            df = None

        # 2. 东财直接API
        df2 = StockDataFetcher.fetch_fund_data_eastmoney_direct(code, start_date, end_date, days)
        if df2 is not None and not df2.empty:
            return df2

        # 3. LOF 历史接口（最后回退）
        try:
            df = ak.fund.fund_lof_em.fund_lof_hist_em(
                symbol=code, period="daily",
                start_date=start_date, end_date=end_date, adjust="",
            )
            if df is not None and not df.empty:
                df = df.rename(columns={
                    "日期": "date", "开盘": "open", "收盘": "close",
                    "最高": "high", "最低": "low", "成交量": "volume",
                    "成交额": "amount", "涨跌幅": "pct_change",
                })
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                return df
        except Exception as e:
            logger.warning("LOF备用接口也失败: %s", e)

        return None

    @staticmethod
    def fetch_fund_info_akshare(code: str) -> Optional[Dict]:
        """获取基金基本信息"""
        fund_type = StockDataFetcher.get_fund_type(code)

        # ETF：优先新浪实时接口
        if fund_type == "etf" and REQUESTS_AVAILABLE:
            try:
                sina_sym = StockDataFetcher._build_sina_symbol(code)
                url = f"https://hq.sinajs.cn/list={sina_sym}"
                headers = {"Referer": "https://finance.sina.com.cn"}
                resp = requests.get(url, headers=headers, timeout=10)
                resp.raise_for_status()
                resp.encoding = "gbk"
                match = re.search(r'="(.+)"', resp.text)
                if not match:
                    return None
                parts = match.group(1).split(",")
                if len(parts) > 3:
                    return {
                        "name": parts[0],
                        "type": "ETF",
                        "price": float(parts[3]) if parts[3] else 0,
                    }
            except Exception as e:
                logger.warning("新浪ETF信息失败: %s", e)

        # ETF/LOF：东财实时列表
        if fund_type in ("etf", "lof") and AKSHARE_AVAILABLE:
            try:
                if fund_type == "etf":
                    df = ak.fund_etf_spot_em()
                else:
                    df = ak.fund.fund_lof_em.fund_lof_spot_em()
                row = df[df["代码"] == code]
                if not row.empty:
                    row = row.iloc[0]
                    return {
                        "name": str(row.get("名称", code)),
                        "type": fund_type.upper(),
                        "price": float(row.get("最新价", 0)),
                    }
                # ETF/LOF 实时列表未找到，尝试基金名称搜索
                try:
                    name_df = ak.fund_name_em()
                    row = name_df[name_df["基金代码"] == code]
                    if not row.empty:
                        return {
                            "name": str(row.iloc[0].get("基金简称", code)),
                            "type": fund_type.upper(),
                            "price": 0,
                        }
                except Exception:
                    pass
            except Exception as e:
                logger.warning("东财基金信息失败: %s", e)

        # 开放式基金：通过东财API获取基金名称
        if fund_type == "open" and AKSHARE_AVAILABLE:
            try:
                df = ak.fund.fund_em.fund_open_fund_info_em(
                    symbol=code, indicator="单位净值走势",
                )
                if df is not None and not df.empty:
                    # 尝试从 akshare 基金名称搜索接口获取名称
                    try:
                        name_df = ak.fund_name_em()
                        row = name_df[name_df["基金代码"] == code]
                        if not row.empty:
                            fund_name = str(row.iloc[0].get("基金简称", code))
                        else:
                            fund_name = code
                    except Exception:
                        fund_name = code
                    return {"name": fund_name, "type": "开放式基金"}
            except Exception as e:
                logger.warning("开放式基金信息失败: %s", e)

        return {"name": code, "type": fund_type.upper()}

    # -------------------- 统一入口 --------------------

    @staticmethod
    def fetch_data(
        code: str, market: str, asset_type: str, days: int = 60
    ) -> Optional[pd.DataFrame]:
        """获取历史数据统一入口"""
        if asset_type == "fund":
            return StockDataFetcher.fetch_fund_data_akshare(code, days)

        if market == "ashare":
            # A股：新浪 → akshare
            df = StockDataFetcher.fetch_stock_data_sina(code, market, days)
            if df is not None:
                return df
            logger.info("新浪失败，尝试akshare备用...")
            return StockDataFetcher.fetch_stock_data_akshare(code, market, days)

        # 港美股：yfinance → akshare
        df = StockDataFetcher.fetch_stock_data_yfinance(code, market, days)
        if df is not None:
            return df
        logger.info("yfinance失败，尝试akshare备用...")
        return StockDataFetcher.fetch_stock_data_akshare(code, market, days)

    @staticmethod
    def fetch_quote(code: str, market: str, asset_type: str) -> Optional[Dict]:
        """获取实时行情统一入口"""
        if asset_type == "fund":
            info = StockDataFetcher.fetch_fund_info_akshare(code)
            return info if info else None

        if market == "ashare":
            quote = StockDataFetcher.fetch_realtime_quote_sina(code, market)
            if quote:
                return quote
            return StockDataFetcher.fetch_realtime_quote_akshare(code, market)

        # 港美股
        quote = StockDataFetcher.fetch_realtime_quote_yfinance(code, market)
        if quote:
            return quote
        return StockDataFetcher.fetch_realtime_quote_akshare(code, market)


# ============================================================
# 技术指标计算
# ============================================================
class TechnicalIndicators:
    """股票技术指标计算器"""

    @staticmethod
    def calculate_ma(
        df: pd.DataFrame, periods: Optional[List[int]] = None
    ) -> Dict[str, Optional[float]]:
        """计算移动平均线 (MA)"""
        if periods is None:
            periods = [5, 10, 20, 60]

        result = {}
        for period in periods:
            if len(df) >= period:
                ma = df["close"].rolling(window=period).mean().iloc[-1]
                result[f"MA{period}"] = round(float(ma), 4)
            else:
                result[f"MA{period}"] = None
        return result

    @staticmethod
    def calculate_macd(
        df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9
    ) -> Dict[str, Any]:
        """计算 MACD 指标"""
        if len(df) < slow:
            return {"DIF": None, "DEA": None, "MACD": None, "signal": "数据不足"}

        ema_fast = df["close"].ewm(span=fast, adjust=False).mean()
        ema_slow = df["close"].ewm(span=slow, adjust=False).mean()

        dif = ema_fast - ema_slow
        dea = dif.ewm(span=signal, adjust=False).mean()
        macd_hist = (dif - dea) * 2

        dif_val = dif.iloc[-1]
        dea_val = dea.iloc[-1]
        macd_val = macd_hist.iloc[-1]

        # 金叉/死叉信号
        if len(dif) >= 2:
            prev_dif, prev_dea = dif.iloc[-2], dea.iloc[-2]
            if prev_dif <= prev_dea and dif_val > dea_val:
                sig = "金叉"
            elif prev_dif >= prev_dea and dif_val < dea_val:
                sig = "死叉"
            else:
                sig = "中性"
        else:
            sig = "中性"

        # 背离检测（最近20个交易日内）
        divergence = "无"
        lookback = min(20, len(df) - 1)
        if lookback >= 10:
            prices = df["close"].iloc[-lookback:]
            dif_series = dif.iloc[-lookback:]

            # 找价格局部高点（顶背离）
            price_highs_idx = []
            for i in range(2, len(prices) - 2):
                if prices.iloc[i] >= prices.iloc[i-1] and prices.iloc[i] >= prices.iloc[i-2] \
                   and prices.iloc[i] >= prices.iloc[i+1] and prices.iloc[i] >= prices.iloc[i+2]:
                    price_highs_idx.append(i)

            if len(price_highs_idx) >= 2:
                last_two = price_highs_idx[-2:]
                p1, p2 = prices.iloc[last_two[0]], prices.iloc[last_two[1]]
                d1, d2 = dif_series.iloc[last_two[0]], dif_series.iloc[last_two[1]]
                if p2 > p1 and d2 < d1:
                    divergence = "顶背离"
                elif p2 < p1 and d2 > d1:
                    divergence = "底背离"

        return {
            "DIF": round(float(dif_val), 4),
            "DEA": round(float(dea_val), 4),
            "MACD": round(float(macd_val), 4),
            "signal": sig,
            "divergence": divergence,
        }

    @staticmethod
    def calculate_rsi(
        df: pd.DataFrame, periods: Optional[List[int]] = None
    ) -> Dict[str, Optional[float]]:
        """计算 RSI 相对强弱指数"""
        if periods is None:
            periods = [6, 12, 24]

        result = {}
        delta = df["close"].diff()

        for period in periods:
            if len(df) < period:
                result[f"RSI{period}"] = None
                continue

            gain = delta.where(delta > 0, 0).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

            # 避免除零，NaN 转为 None
            rs = gain / loss.replace(0, np.nan)
            rsi = 100 - (100 / (1 + rs))
            val = rsi.iloc[-1]
            result[f"RSI{period}"] = round(float(val), 2) if pd.notna(val) else None

        return result

    @staticmethod
    def calculate_bollinger(
        df: pd.DataFrame, period: int = 20, std_dev: float = 2.0
    ) -> Dict[str, Any]:
        """计算布林带 (BOLL)"""
        if len(df) < period:
            return {"upper": None, "middle": None, "lower": None, "position": "数据不足", "bb_position": None}

        middle = df["close"].rolling(window=period).mean()
        std = df["close"].rolling(window=period).std()

        upper = middle + std_dev * std
        lower = middle - std_dev * std

        current_price = df["close"].iloc[-1]
        upper_val = upper.iloc[-1]
        middle_val = middle.iloc[-1]
        lower_val = lower.iloc[-1]

        # NaN 安全检查
        if pd.isna(upper_val) or pd.isna(lower_val) or pd.isna(middle_val) or pd.isna(current_price):
            return {"upper": None, "middle": None, "lower": None, "position": "数据不足", "bb_position": None}

        # 价格在布林带中的位置百分比 (0~1)
        bb_width = upper_val - lower_val
        bb_position = (current_price - lower_val) / bb_width if bb_width > 0 else 0.5

        # 位置判断
        if current_price > upper_val:
            position = "突破上轨"
        elif current_price >= middle_val:
            position = "高位"
        elif current_price >= lower_val:
            position = "中位"
        else:
            position = "突破下轨"

        return {
            "upper": round(float(upper_val), 4),
            "middle": round(float(middle_val), 4),
            "lower": round(float(lower_val), 4),
            "position": position,
            "bb_position": round(float(bb_position), 2),
            "bb_width": round(float(bb_width / middle_val * 100), 2) if middle_val > 0 else 0,
            "squeeze": False,
        }

    @staticmethod
    def calculate_kdj(
        df: pd.DataFrame, n: int = 9, m1: int = 3, m2: int = 3
    ) -> Dict[str, Any]:
        """计算 KDJ 随机指标"""
        if len(df) < n:
            return {"K": None, "D": None, "J": None, "signal": "数据不足"}

        low_list = df["low"].rolling(window=n, min_periods=1).min()
        high_list = df["high"].rolling(window=n, min_periods=1).max()
        rsv = (df["close"] - low_list) / (high_list - low_list) * 100
        rsv = rsv.fillna(50)

        k = rsv.ewm(com=m1 - 1, adjust=False).mean()
        d = k.ewm(com=m2 - 1, adjust=False).mean()
        j = 3 * k - 2 * d

        k_val, d_val, j_val = k.iloc[-1], d.iloc[-1], j.iloc[-1]

        if pd.isna(k_val) or pd.isna(d_val):
            return {"K": None, "D": None, "J": None, "signal": "数据不足"}

        # 信号判断
        if j_val > 100:
            signal = "超买"
        elif j_val < 0:
            signal = "超卖"
        elif k_val > d_val and k_val < 80:
            signal = "多头"
        elif k_val < d_val and k_val > 20:
            signal = "空头"
        else:
            signal = "中性"

        return {
            "K": round(float(k_val), 2),
            "D": round(float(d_val), 2),
            "J": round(float(j_val), 2),
            "signal": signal,
        }

    @staticmethod
    def calculate_atr(
        df: pd.DataFrame, period: int = 14
    ) -> Dict[str, Optional[float]]:
        """计算 ATR 真实波幅"""
        if len(df) < period + 1:
            return {"ATR": None, "ATR_percent": None}

        prev_close = df["close"].shift(1)
        tr = pd.concat([
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ], axis=1).max(axis=1)

        atr = tr.rolling(window=period).mean()
        atr_val = atr.iloc[-1]
        current_price = df["close"].iloc[-1]

        if pd.isna(atr_val) or current_price <= 0:
            return {"ATR": None, "ATR_percent": None}

        return {
            "ATR": round(float(atr_val), 4),
            "ATR_percent": round(float(atr_val / current_price * 100), 2),
        }

    @staticmethod
    def calculate_volume(
        df: pd.DataFrame, periods: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """计算成交量均线和量比"""
        if periods is None:
            periods = [5, 10]

        if "volume" not in df.columns or df["volume"].sum() == 0:
            return {"VMA5": None, "VMA10": None, "volume_ratio": None, "volume_signal": "无成交量数据"}

        result = {}
        for period in periods:
            if len(df) >= period:
                vma = df["volume"].rolling(window=period).mean().iloc[-1]
                result[f"VMA{period}"] = round(float(vma), 0)
            else:
                result[f"VMA{period}"] = None

        # 量比 = 当日成交量 / 过去5日平均成交量
        current_vol = df["volume"].iloc[-1]
        vma5 = result.get("VMA5")
        volume_ratio = round(current_vol / vma5, 2) if vma5 and vma5 > 0 else None

        # 量能信号
        if volume_ratio is None:
            vol_signal = "数据不足"
        elif volume_ratio >= 2.0:
            vol_signal = "显著放量"
        elif volume_ratio >= 1.5:
            vol_signal = "放量"
        elif volume_ratio <= 0.5:
            vol_signal = "显著缩量"
        elif volume_ratio <= 0.8:
            vol_signal = "缩量"
        else:
            vol_signal = "正常"

        result["volume_ratio"] = volume_ratio
        result["volume_signal"] = vol_signal
        return result


# ============================================================
# 支撑压力位识别
# ============================================================
class SupportResistanceFinder:
    """支撑位和压力位识别器"""

    @staticmethod
    def find_levels(df: pd.DataFrame, window: int = 5, asset_type: str = "stock") -> Dict[str, List]:
        """识别支撑位、压力位和缺口

        Args:
            df: 行情数据
            window: 局部极值窗口大小
            asset_type: 资产类型，基金类型跳过支撑压力位计算
        """
        support_levels: List[float] = []
        resistance_levels: List[float] = []
        gaps: List[Dict] = []

        if len(df) < window * 2:
            return {"support": support_levels, "resistance": resistance_levels, "gaps": gaps}

        # 开放式基金 open=high=low=close，支撑压力位无意义
        if asset_type == "fund" and "open" in df.columns:
            if (df["high"] == df["low"]).all():
                return {"support": support_levels, "resistance": resistance_levels, "gaps": gaps}

        # 局部极值识别（排除当前位置自身）
        for i in range(window, len(df) - window):
            high = df["high"].iloc[i]
            low = df["low"].iloc[i]
            # 排除位置 i，只与窗口内其他位置比较
            window_highs = (
                df["high"].iloc[i - window : i].tolist()
                + df["high"].iloc[i + 1 : i + window + 1].tolist()
            )
            window_lows = (
                df["low"].iloc[i - window : i].tolist()
                + df["low"].iloc[i + 1 : i + window + 1].tolist()
            )

            # 局部高点（压力位）：严格大于窗口内所有其他值
            if all(high >= wh for wh in window_highs):
                resistance_levels.append(round(float(high), 4))

            # 局部低点（支撑位）：严格小于窗口内所有其他值
            if all(low <= wl for wl in window_lows):
                support_levels.append(round(float(low), 4))

        # 缺口检测
        for i in range(1, len(df)):
            prev_high = df["high"].iloc[i - 1]
            prev_low = df["low"].iloc[i - 1]
            curr_high = df["high"].iloc[i]
            curr_low = df["low"].iloc[i]

            if curr_low > prev_high:
                # 向上跳空
                gaps.append({
                    "type": "向上跳空",
                    "gap_start": round(float(prev_high), 4),
                    "gap_end": round(float(curr_low), 4),
                    "size": round((curr_low - prev_high) / prev_high * 100, 2) if prev_high > 0 else 0,
                })
            elif curr_high < prev_low:
                # 向下跳空
                gaps.append({
                    "type": "向下跳空",
                    "gap_start": round(float(curr_high), 4),
                    "gap_end": round(float(prev_low), 4),
                    "size": round((prev_low - curr_high) / curr_high * 100, 2) if curr_high > 0 else 0,
                })

        # 取最近5个支撑/压力位
        support_levels = sorted(support_levels, reverse=True)[:5]
        resistance_levels = sorted(resistance_levels)[:5]

        return {
            "support": support_levels,
            "resistance": resistance_levels,
            "gaps": gaps[-3:] if len(gaps) > 3 else gaps,
        }


# ============================================================
# 综合分析器
# ============================================================
class StockAnalyzer:
    """股票综合分析器"""

    def __init__(self):
        self.data_fetcher = StockDataFetcher()
        self.indicators = TechnicalIndicators()
        self.levels_finder = SupportResistanceFinder()

    @staticmethod
    def calculate_score(
        df: pd.DataFrame, ma: Dict, macd: Dict, rsi: Dict, bollinger: Dict,
        kdj: Optional[Dict] = None, volume: Optional[Dict] = None,
    ) -> Tuple[int, str, str]:
        """
        计算综合评分。

        评分维度：
          - 基础分 50
          - 均线趋势 ±20（排列 + 价格位置 ±8）
          - MACD ±15（金叉/死叉 + 柱状方向）
          - RSI ±15（超买超卖）
          - 布林带 ±10（突破/接近轨道）

        Returns:
            (评分, 趋势, 建议)
        """
        score = 50
        current_price = df["close"].iloc[-1]

        # NaN 安全检查
        if pd.isna(current_price):
            return 50, "数据不足", "当前价格数据缺失，无法准确评分"

        # 1. 均线趋势 (±20) — 分层处理，MA60 缺失时仍评短期趋势
        if ma.get("MA5") and ma.get("MA10") and ma.get("MA20"):
            # 短期均线排列 (±12)
            if ma["MA5"] > ma["MA10"] > ma["MA20"]:
                score += 12  # 短期多头
            elif ma["MA5"] < ma["MA10"] < ma["MA20"]:
                score -= 12  # 短期空头

            # 长期均线确认 (±8)
            if ma.get("MA60") is not None:
                if ma["MA5"] > ma["MA10"] > ma["MA20"] > ma["MA60"]:
                    score += 8  # 完美多头（在短期多头基础上追加）
                elif ma["MA5"] < ma["MA10"] < ma["MA20"] < ma["MA60"]:
                    score -= 8  # 完美空头（在短期空头基础上追加）

            # 价格与均线关系 (±8)
            if current_price > ma["MA5"]:
                score += 5
            else:
                score -= 5
            if current_price > ma["MA20"]:
                score += 3
            else:
                score -= 3

        # 2. MACD (±15)
        if macd.get("signal") == "金叉":
            score += 10
        elif macd.get("signal") == "死叉":
            score -= 10

        if macd.get("MACD") is not None:
            score += 5 if macd["MACD"] > 0 else -5

        # 3. RSI (±15)
        rsi_val = rsi.get("RSI12")
        if rsi_val is not None:
            if rsi_val < 20:
                score += 15   # 严重超卖
            elif rsi_val < 30:
                score += 10   # 超卖
            elif rsi_val > 80:
                score -= 15   # 严重超买
            elif rsi_val > 70:
                score -= 10   # 超买

        # 4. 布林带 (±10)
        bb_pos = bollinger.get("bb_position")
        if bb_pos is not None:
            if bollinger["position"] == "突破下轨":
                score += 10
            elif bollinger["position"] == "突破上轨":
                score -= 10
            elif bb_pos < BB_LOWER_THRESHOLD:
                score += 5   # 接近下轨
            elif bb_pos > BB_UPPER_THRESHOLD:
                score -= 5   # 接近上轨
            # 中位 (0.3~0.7) 不加减分

        # 5. KDJ (±10)
        if kdj and kdj.get("K") is not None:
            if kdj["signal"] == "超卖":
                score += 8
            elif kdj["signal"] == "超买":
                score -= 8
            elif kdj["signal"] == "多头":
                score += 4
            elif kdj["signal"] == "空头":
                score -= 4

        # 6. 成交量/量能 (±8)
        if volume and volume.get("volume_ratio") is not None:
            vr = volume["volume_ratio"]
            if vr >= 2.0:
                score += 5   # 显著放量（关注突破）
            elif vr >= 1.5:
                score += 3   # 放量
            elif vr <= 0.5:
                score -= 3   # 显著缩量
            elif vr <= 0.8:
                score -= 1   # 缩量

        final_score = max(0, min(100, score))

        # 趋势判断
        if final_score >= SCORE_STRONG_UP:
            trend = "强势上涨"
            recommendation = "技术面强势，多指标共振偏多"
        elif final_score >= SCORE_UP:
            trend = "上涨趋势"
            recommendation = "技术面偏多，短期趋势向上"
        elif final_score >= SCORE_SIDEWAYS_LOW:
            trend = "震荡整理"
            recommendation = "技术面中性，方向不明确"
        elif final_score >= SCORE_DOWN:
            trend = "下跌趋势"
            recommendation = "技术面偏空，短期趋势向下"
        else:
            trend = "强势下跌"
            recommendation = "技术面弱势，多指标共振偏空"

        return final_score, trend, recommendation

    def analyze(
        self,
        code: str,
        market: str = "auto",
        asset_type: str = "stock",
        days: int = 60,
    ) -> Dict[str, Any]:
        """执行完整的技术分析"""
        code, market, asset_type = self.data_fetcher.normalize_stock_code(code, market, asset_type)
        logger.info("分析: %s (市场: %s, 类型: %s)", code, market, asset_type)

        df = self.data_fetcher.fetch_data(code, market, asset_type, days)
        if df is None or df.empty:
            # 区分网络问题和数据不存在
            error_msg = f"无法获取 {code} 的数据"
            if not REQUESTS_AVAILABLE and market == "ashare":
                error_msg = f"无法获取 {code} 的数据（requests 未安装，请运行: pip install requests）"
            elif not YFINANCE_AVAILABLE and market in ("hkstock", "usstock"):
                error_msg = f"无法获取 {code} 的数据（yfinance 未安装，请运行: pip install yfinance）"
            return {
                "error": error_msg,
                "stock_info": {"code": code, "market": market, "asset_type": asset_type},
            }

        logger.info("获取到 %d 条历史数据", len(df))

        quote = self.data_fetcher.fetch_quote(code, market, asset_type)

        # 基础信息
        change_pct = 0
        if "pct_change" in df.columns and pd.notna(df["pct_change"].iloc[-1]):
            change_pct = round(float(df["pct_change"].iloc[-1]), 2)

        stock_info = {
            "code": code,
            "name": quote.get("name", code) if quote else code,
            "market": market,
            "asset_type": asset_type,
            "current_price": round(float(df["close"].iloc[-1]), 4),
            "change_pct": change_pct,
            "update_time": df["date"].iloc[-1].strftime("%Y-%m-%d"),
        }

        # 实时行情覆盖
        if quote and quote.get("price"):
            stock_info["current_price"] = quote["price"]
            stock_info["change_pct"] = quote.get("pct_change", change_pct)
            stock_info["update_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 计算技术指标
        ma = self.indicators.calculate_ma(df)
        macd = self.indicators.calculate_macd(df)
        rsi = self.indicators.calculate_rsi(df)
        bollinger = self.indicators.calculate_bollinger(df)
        kdj = self.indicators.calculate_kdj(df)
        atr = self.indicators.calculate_atr(df)
        volume = self.indicators.calculate_volume(df)

        # 布林带收窄检测
        if bollinger.get("bb_width") and len(df) >= 20:
            bbw_series = (df["close"].rolling(20).std() * 4) / df["close"].rolling(20).mean() * 100
            if pd.notna(bbw_series.iloc[-1]) and len(bbw_series.dropna()) >= 20:
                bollinger["squeeze"] = bool(bbw_series.iloc[-1] <= bbw_series.iloc[-20:].min() * 1.1)

        # 支撑压力位（基金类型跳过无意义的计算）
        levels = self.levels_finder.find_levels(df, asset_type=asset_type)

        # 综合评分
        score, trend, recommendation = self.calculate_score(df, ma, macd, rsi, bollinger, kdj=kdj, volume=volume)

        return {
            "stock_info": stock_info,
            "technical_indicators": {
                "ma": ma,
                "macd": macd,
                "rsi": rsi,
                "bollinger": bollinger,
                "kdj": kdj,
                "atr": atr,
                "volume_analysis": volume,
            },
            "key_levels": levels,
            "analysis": {
                "score": score,
                "trend": trend,
                "recommendation": recommendation,
                "summary": self._generate_summary(stock_info, ma, macd, rsi, bollinger, score, kdj=kdj, volume=volume),
            },
        }

    def analyze_batch(
        self,
        codes: List[str],
        market: str = "auto",
        test: bool = False,
        asset_type: str = "stock",
        days: int = 60,
    ) -> Dict[str, Any]:
        """批量分析多只股票/基金（并发请求）"""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def _analyze_one(item: str) -> Dict:
            actual_type = asset_type
            if ":" in item:
                code, actual_type = item.split(":", 1)
                code = code.strip()
                actual_type = actual_type.strip()
            else:
                code = item.strip()

            if test:
                return self.analyze_with_mock_data(code, market, actual_type)
            else:
                return self.analyze(code, market, actual_type, days)

        results = []
        # 并发执行，最多8个线程
        max_workers = min(8, len(codes))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_analyze_one, item): item for item in codes}
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=60)
                    results.append(result)
                except Exception as e:
                    item = futures[future]
                    code = item.split(":")[0].strip() if ":" in item else item.strip()
                    results.append({"error": str(e), "stock_info": {"code": code}})

        # 汇总统计
        summary = {"强势上涨": 0, "上涨趋势": 0, "震荡整理": 0, "下跌趋势": 0, "强势下跌": 0}
        total_score = 0
        valid_count = 0
        failed: List[Dict] = []

        for result in results:
            if "analysis" in result:
                trend = result["analysis"]["trend"]
                if trend in summary:
                    summary[trend] += 1
                total_score += result["analysis"]["score"]
                valid_count += 1
            elif "error" in result:
                failed.append({
                    "code": result.get("stock_info", {}).get("code", "?"),
                    "error": result["error"],
                })

        # 失败项自动重试一轮
        if failed and not test:
            retry_codes = [f["code"] for f in failed]
            logger.info("批量分析有 %d 项失败，自动重试: %s", len(retry_codes), ", ".join(retry_codes))
            retry_results = []
            max_workers = min(4, len(retry_codes))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(_analyze_one, item): item for item in retry_codes}
                for future in as_completed(futures):
                    try:
                        result = future.result(timeout=90)
                        retry_results.append(result)
                    except Exception as e:
                        item = futures[future]
                        code = item.split(":")[0].strip() if ":" in item else item.strip()
                        retry_results.append({"error": str(e), "stock_info": {"code": code}})

            # 合并重试结果：成功的替换原失败项
            new_failed = []
            for retry_result in retry_results:
                if "analysis" in retry_result:
                    trend = retry_result["analysis"]["trend"]
                    if trend in summary:
                        summary[trend] += 1
                    total_score += retry_result["analysis"]["score"]
                    valid_count += 1
                    # 替换原 results 中的失败项
                    retry_code = retry_result.get("stock_info", {}).get("code", "")
                    for i, r in enumerate(results):
                        if r.get("error") and r.get("stock_info", {}).get("code") == retry_code:
                            results[i] = retry_result
                            break
                else:
                    new_failed.append({
                        "code": retry_result.get("stock_info", {}).get("code", "?"),
                        "error": retry_result["error"],
                    })
            failed = new_failed

        avg_score = round(total_score / valid_count, 1) if valid_count > 0 else 0

        return {
            "results": results,
            "summary": {
                **summary,
                "total": len(codes),
                "valid": valid_count,
                "failed_count": len(failed),
                "avg_score": avg_score,
            },
            "failed": failed if failed else None,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    def analyze_with_mock_data(
        self,
        code: str,
        market: str = "auto",
        asset_type: str = "stock",
        days: int = 60,
    ) -> Dict[str, Any]:
        """使用模拟数据进行离线测试（无需网络）"""
        code, market, asset_type = self.data_fetcher.normalize_stock_code(code, market, asset_type)
        logger.info("[TEST] 模拟数据: %s (市场: %s, 类型: %s, 天数: %d)", code, market, asset_type, days)

        np.random.seed(hash(code) % 2**32)
        base_price = np.random.uniform(10, 2000)

        dates = pd.date_range(end=datetime.now(), periods=days, freq="D")
        trend = np.random.uniform(-0.002, 0.003)
        returns = np.random.normal(trend, 0.02, days)
        prices = base_price * np.cumprod(1 + returns)

        df = pd.DataFrame({
            "date": dates,
            "open": prices * np.random.uniform(0.98, 1.02, days),
            "high": prices * np.random.uniform(1.0, 1.05, days),
            "low": prices * np.random.uniform(0.95, 1.0, days),
            "close": prices,
            "volume": np.random.uniform(1e6, 1e8, days).astype(int),
        })
        df["pct_change"] = df["close"].pct_change() * 100

        name_map = {
            "600519": "贵州茅台", "000001": "平安银行", "000858": "五粮液",
            "00700": "腾讯控股", "AAPL": "苹果", "TSLA": "特斯拉",
            "001316": "安信稳健增值", "000369": "国泰金龙行业",
        }

        stock_info = {
            "code": code,
            "name": name_map.get(code, f"标的{code}"),
            "market": market,
            "asset_type": asset_type,
            "current_price": round(float(prices[-1]), 4),
            "change_pct": round(float(df["pct_change"].iloc[-1]), 2),
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_mock_data": True,
        }

        ma = self.indicators.calculate_ma(df)
        macd = self.indicators.calculate_macd(df)
        rsi = self.indicators.calculate_rsi(df)
        bollinger = self.indicators.calculate_bollinger(df)
        kdj = self.indicators.calculate_kdj(df)
        atr = self.indicators.calculate_atr(df)
        volume = self.indicators.calculate_volume(df)

        levels = self.levels_finder.find_levels(df, asset_type=asset_type)
        score, trend, recommendation = self.calculate_score(df, ma, macd, rsi, bollinger, kdj=kdj, volume=volume)

        return {
            "stock_info": stock_info,
            "technical_indicators": {"ma": ma, "macd": macd, "rsi": rsi, "bollinger": bollinger, "kdj": kdj, "atr": atr, "volume_analysis": volume},
            "key_levels": levels,
            "analysis": {
                "score": score,
                "trend": trend,
                "recommendation": recommendation,
                "summary": self._generate_summary(stock_info, ma, macd, rsi, bollinger, score, kdj=kdj, volume=volume),
            },
        }

    @staticmethod
    def _generate_summary(
        stock_info: Dict, ma: Dict, macd: Dict, rsi: Dict, bollinger: Dict, score: int,
        kdj: Optional[Dict] = None, volume: Optional[Dict] = None,
    ) -> str:
        """生成中文分析摘要"""
        parts = []

        price = stock_info.get("current_price", 0)
        change = stock_info.get("change_pct", 0)
        name = stock_info.get("name", "")
        asset_type = stock_info.get("asset_type", "stock")

        price_label = "净值" if asset_type == "fund" else "现价"
        direction = "上涨" if change >= 0 else "下跌"
        parts.append(f"{name}{price_label}{price}，{direction}{abs(change):.2f}%")

        if ma.get("MA5") and ma.get("MA20"):
            ma_status = "多头" if ma["MA5"] > ma["MA20"] else "空头"
            parts.append(f"均线{ma_status}排列")

        if macd.get("signal") and macd["signal"] != "中性":
            parts.append(f"MACD{macd['signal']}")

        rsi_val = rsi.get("RSI12")
        if rsi_val is not None:
            if rsi_val > 70:
                parts.append(f"RSI超买({rsi_val:.0f})")
            elif rsi_val < 30:
                parts.append(f"RSI超卖({rsi_val:.0f})")

        if bollinger.get("position") and bollinger["position"] != "中位":
            parts.append(f"布林{bollinger['position']}")

        if bollinger.get("squeeze"):
            parts.append("布林收窄")

        if kdj and kdj.get("signal") and kdj["signal"] in ("超买", "超卖"):
            parts.append(f"KDJ{kdj['signal']}")

        if volume and volume.get("volume_signal") and volume["volume_signal"] not in ("正常", "数据不足", "无成交量数据"):
            parts.append(volume["volume_signal"])

        parts.append(f"评分{score}")

        return "；".join(parts)


# ============================================================
# ASCII 模式映射表
# ============================================================
ASCII_REPLACE_MAP = {
    # 趋势
    "强势上涨": "STRONG_UP",
    "上涨趋势": "UP",
    "震荡整理": "SIDEWAYS",
    "下跌趋势": "DOWN",
    "强势下跌": "STRONG_DOWN",
    # 信号
    "金叉": "GOLDEN_CROSS",
    "死叉": "DEATH_CROSS",
    "中性": "NEUTRAL",
    # 布林带
    "突破上轨": "ABOVE_UPPER",
    "突破下轨": "BELOW_LOWER",
    "高位": "HIGH",
    "中位": "MID",
    "低位": "LOW",
    # 缺口
    "向上跳空": "GAP_UP",
    "向下跳空": "GAP_DOWN",
    # 其他
    "数据不足": "INSUFFICIENT_DATA",
    "完美多头": "PERFECT_BULL",
    "完美空头": "PERFECT_BEAR",
    # 建议
    "技术面强势，多指标共振偏多": "STRONG_BULLISH",
    "技术面偏多，短期趋势向上": "BULLISH",
    "技术面中性，方向不明确": "NEUTRAL",
    "技术面偏空，短期趋势向下": "BEARISH",
    "技术面弱势，多指标共振偏空": "STRONG_BEARISH",
    # 摘要常用词
    "现价": "PRICE",
    "净值": "NAV",
    "上涨": "UP",
    "下跌": "DOWN",
    "均线多头排列": "MA_BULL",
    "均线空头排列": "MA_BEAR",
    "超买": "OVERBOUGHT",
    "超卖": "OVERSOLD",
    "评分": "SCORE",
    # KDJ/成交量
    "布林收窄": "BOLL_SQUEEZE",
    "显著放量": "VOL_SURGE",
    "放量": "VOL_UP",
    "显著缩量": "VOL_SHRINK",
    "缩量": "VOL_DOWN",
    "多头": "BULL",
    "空头": "BEAR",
}


# ============================================================
# 终端表格输出
# ============================================================
def _print_table(result: Dict, batch_mode: bool = False, ascii_mode: bool = False) -> None:
    """以人类可读的表格格式输出分析结果"""
    if batch_mode:
        _print_batch_table(result, ascii_mode=ascii_mode)
    else:
        _print_single_table(result, ascii_mode=ascii_mode)


def _print_single_table(d: Dict, ascii_mode: bool = False) -> None:
    """输出单个分析结果的表格"""
    if "error" in d:
        print(f"  [X] {d.get('stock_info', {}).get('code', '?')}: {d['error']}")
        return

    def _t(text: str) -> str:
        """ASCII 模式下替换中文为英文标签"""
        if not ascii_mode:
            return text
        for cn, en in ASCII_REPLACE_MAP.items():
            text = text.replace(cn, en)
        return text

    si = d["stock_info"]
    ti = d["technical_indicators"]
    an = d["analysis"]
    kl = d["key_levels"]
    W = 60  # 表格内容宽度

    type_label = _t("基金") if si.get("asset_type") == "fund" else _t("股票")
    title_text = f"{si.get('name', si['code'])} ({si['code']})  {type_label}  {si.get('market', '')}"
    print(f"+{'-'*W}+")
    print(f"| {_pad(title_text, W)}|")
    print(f"+{'-'*W}+")

    price = si.get("current_price", 0)
    change = si.get("change_pct", 0)
    direction = "^" if change >= 0 else "v"
    price_text = f"{direction} {price}  ({change:+.2f}%)  {_t('更新')}: {si.get('update_time', '')}"
    print(f"| {_pad(price_text, W)}|")

    print(f"+{'-'*W}+")
    score_text = f"{_t('评分')}: {an['score']}  {_t('趋势')}: {_t(an['trend'])}"
    print(f"| {_pad(score_text, W)}|")
    print(f"| {_pad(_t('建议') + ': ' + _t(an['recommendation']), W)}|")
    print(f"+{'-'*W}+")

    # 技术指标
    ma = ti.get("ma", {})
    macd = ti.get("macd", {})
    rsi = ti.get("rsi", {})
    boll = ti.get("bollinger", {})
    kdj = ti.get("kdj", {})
    atr = ti.get("atr", {})
    vol = ti.get("volume_analysis", {})

    ma_text = f"MA:  5={_f(ma.get('MA5'))}  10={_f(ma.get('MA10'))}  20={_f(ma.get('MA20'))}  60={_f(ma.get('MA60'))}"
    print(f"| {_pad(ma_text, W)}|")
    macd_text = f"MACD: DIF={_f(macd.get('DIF'))} DEA={_f(macd.get('DEA'))} 柱={_f(macd.get('MACD'))} {macd.get('signal', '')}"
    print(f"| {_pad(macd_text, W)}|")
    if macd.get("divergence") and macd["divergence"] != "无":
        div_text = f"       [!] {macd['divergence']}"
        print(f"| {_pad(div_text, W)}|")
    rsi_text = f"RSI:  6={_f(rsi.get('RSI6'))}  12={_f(rsi.get('RSI12'))}  24={_f(rsi.get('RSI24'))}"
    print(f"| {_pad(rsi_text, W)}|")
    kdj_text = f"KDJ:  K={_f(kdj.get('K'))}  D={_f(kdj.get('D'))}  J={_f(kdj.get('J'))}  {kdj.get('signal', '')}"
    print(f"| {_pad(kdj_text, W)}|")
    boll_text = f"BOLL: 上={_f(boll.get('upper'))} 中={_f(boll.get('middle'))} 下={_f(boll.get('lower'))}  {boll.get('position', '')}"
    print(f"| {_pad(boll_text, W)}|")
    if boll.get("squeeze"):
        print(f"| {_pad('       [!] ' + _t('布林带收窄，注意变盘'), W)}|")
    if atr.get("ATR"):
        atr_text = f"ATR:  {atr['ATR']:.2f} ({atr['ATR_percent']:.2f}%)"
        print(f"| {_pad(atr_text, W)}|")
    if vol.get("volume_ratio"):
        vol_text = f"{_t('量比')}: {vol['volume_ratio']}  {_t(vol.get('volume_signal', ''))}"
        print(f"| {_pad(vol_text, W)}|")

    # 支撑压力位
    sup = kl.get("support", [])
    res = kl.get("resistance", [])
    if sup or res:
        print(f"+{'-'*W}+")
        if sup:
            sup_text = ', '.join(str(s) for s in sup[:3])
            print(f"| {_pad(_t('支撑') + ': ' + sup_text, W)}|")
        if res:
            res_text = ', '.join(str(r) for r in res[:3])
            print(f"| {_pad(_t('压力') + ': ' + res_text, W)}|")

    print(f"+{'-'*W}+")
    print(f"| {_pad(_t(an.get('summary', '')), W)}|")
    print(f"+{'-'*W}+")


def _print_batch_table(d: Dict, ascii_mode: bool = False) -> None:
    """输出批量分析结果的汇总表格"""
    def _t(text: str) -> str:
        if not ascii_mode:
            return text
        for cn, en in ASCII_REPLACE_MAP.items():
            text = text.replace(cn, en)
        return text

    results = d.get("results", [])
    summary = d.get("summary", {})

    print(f"\n{'='*80}")
    print(f"  {_t('批量分析汇总')}  {_t('总计')}: {summary.get('total', 0)}  {_t('成功')}: {summary.get('valid', 0)}  "
          f"{_t('失败')}: {summary.get('failed_count', 0)}  {_t('平均评分')}: {summary.get('avg_score', 0)}")
    print(f"{'='*80}")

    # 表头
    print(f"  {_t('代码'):<8s} {_t('名称'):<14s} {_t('类型'):<4s} {_t('评分'):>4s} {_t('趋势'):<8s} {_t('涨跌'):>7s} {'MACD':<8s} {'KDJ':<6s} {_t('量能'):<8s} {_t('摘要')}")
    print(f"  {'-'*8} {'-'*14} {'-'*4} {'-'*4} {'-'*8} {'-'*7} {'-'*8} {'-'*6} {'-'*8} {'-'*20}")

    for r in results:
        if "error" in r:
            code = r.get("stock_info", {}).get("code", "?")
            print(f"  {code:<8s} [X] {r['error']}")
            continue

        si = r["stock_info"]
        an = r["analysis"]
        ti = r["technical_indicators"]
        macd = ti.get("macd", {})
        kdj = ti.get("kdj", {})
        vol = ti.get("volume_analysis", {})

        name = si.get("name", "")[:12]
        t = _t("基") if si.get("asset_type") == "fund" else _t("股")
        change = f"{si.get('change_pct', 0):+.2f}%"
        macd_sig = _t(macd.get("signal", ""))
        kdj_sig = _t(kdj.get("signal", "")) if kdj.get("K") else ""
        vol_sig = _t(vol.get("volume_signal", "")) if vol.get("volume_ratio") else ""
        summary_text = _t(an.get("summary", ""))[:30]

        print(f"  {si['code']:<8s} {name:<14s} {t:<4s} {an['score']:>4d} {_t(an['trend']):<8s} {change:>7s} {macd_sig:<8s} {kdj_sig:<6s} {vol_sig:<8s} {summary_text}")

    if d.get("failed"):
        print(f"\n  {_t('失败列表')}:")
        for f in d["failed"]:
            print(f"    [X] {f.get('code', '?')}: {f.get('error', '')}")

    print(f"{'='*80}")


def _f(val) -> str:
    """格式化数值，None 显示为 --"""
    if val is None:
        return "--"
    return f"{val:.2f}"


def _dw(text: str) -> int:
    """计算字符串的显示宽度（中文字符占 2 列）"""
    try:
        from wcwidth import wcswidth
        w = wcswidth(text)
        return w if w is not None else len(text)
    except ImportError:
        return len(text)


def _pad(text: str, width: int) -> str:
    """将 text 用空格填充到指定显示宽度"""
    return text + " " * max(0, width - _dw(text))


def _run_check() -> None:
    """运行环境自检，检查依赖安装和数据源连通性"""
    print(f"{'='*50}")
    print(f"  股票技术分析工具 v{VERSION} - 环境自检")
    print(f"{'='*50}")

    # 1. 依赖检查
    print(f"\n  [依赖检查]")
    deps = [
        ("pandas", "数据处理核心", True),
        ("numpy", "数值计算", True),
        ("requests", "HTTP 请求（A 股/基金数据源）", True),
        ("akshare", "A 股/基金备用数据源", False),
        ("yfinance", "港美股数据源", False),
        ("wcwidth", "终端中文对齐", False),
    ]
    all_required = True
    for mod, desc, required in deps:
        try:
            __import__(mod)
            status = "OK"
            color = "OK"
        except ImportError:
            status = "MISSING"
            color = "MISSING"
            if required:
                all_required = False
        tag = "[必需]" if required else "[可选]"
        print(f"    {tag} {mod:<12s} {desc:<30s} [{status}]")

    if not all_required:
        print(f"\n  [!] 必需依赖缺失，请安装: pip install pandas numpy requests")
        print(f"{'='*50}")
        return

    # 2. 数据源连通性检查
    print(f"\n  [数据源检查]")

    # 新浪财经
    sina_ok = False
    if REQUESTS_AVAILABLE:
        try:
            import requests as req
            resp = req.get(
                "https://hq.sinajs.cn/list=sh600519",
                headers={"Referer": "https://finance.sina.com.cn"},
                timeout=5,
            )
            sina_ok = resp.status_code == 200 and len(resp.text) > 10
        except Exception:
            pass
    print(f"    新浪财经 (A 股主源)     [{'OK' if sina_ok else 'FAIL'}]")

    # yfinance
    yf_ok = False
    if YFINANCE_AVAILABLE:
        try:
            import yfinance as yf
            t = yf.Ticker("00700.HK")
            data = t.history(period="5d")
            yf_ok = data is not None and len(data) > 0
        except Exception:
            pass
    print(f"    yfinance (港美股主源)   [{'OK' if yf_ok else 'FAIL'}]")

    # akshare
    ak_ok = False
    if AKSHARE_AVAILABLE:
        try:
            import akshare as ak
            df = ak.stock_zh_a_hist(symbol="600519", period="daily", start_date="20260101", end_date="20260110")
            ak_ok = df is not None and len(df) > 0
        except Exception:
            pass
    print(f"    akshare (通用备用源)    [{'OK' if ak_ok else 'FAIL'}]")

    # 3. 总结
    print(f"\n  [总结]")
    checks = [("新浪财经", sina_ok), ("yfinance", yf_ok), ("akshare", ak_ok)]
    ok_count = sum(1 for _, v in checks if v)
    total = len(checks)
    if ok_count == total:
        print(f"    所有数据源正常 ({ok_count}/{total})")
    elif ok_count >= 1:
        print(f"    部分数据源可用 ({ok_count}/{total})，工具可正常使用（自动切换备用源）")
    else:
        print(f"    所有数据源不可用 ({ok_count}/{total})，请检查网络连接")
        print(f"    可使用 --test 模式进行离线测试")

    print(f"{'='*50}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description=f"股票技术分析工具 v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python stock_analysis.py 600519                       # A股自动识别
  python stock_analysis.py 00700 -m hkstock             # 港股
  python stock_analysis.py AAPL -m usstock              # 美股
  python stock_analysis.py 159934 -t fund               # ETF基金
  python stock_analysis.py 001316 -t fund               # 开放式基金
  python stock_analysis.py -b 600036,600900             # 批量分析
  python stock_analysis.py -b 001316:fund,600036:stock  # 混合类型批量
  python stock_analysis.py --watchlist                   # 使用持仓列表分析
  python stock_analysis.py --add 600519                 # 添加到持仓列表
  python stock_analysis.py --add 159934:fund            # 添加基金到持仓列表
  python stock_analysis.py --remove 600519              # 从持仓列表删除
  python stock_analysis.py --list                       # 查看持仓列表
  python stock_analysis.py 600519 --test                # 离线测试
  python stock_analysis.py 600519 --ascii               # ASCII模式
        """,
    )

    parser.add_argument("stock_code", nargs="?", help="股票/基金代码")
    parser.add_argument(
        "--market", "-m", default="auto",
        choices=["auto", "ashare", "hkstock", "usstock"],
        help="市场 (默认: auto)",
    )
    parser.add_argument(
        "--type", "-t", default="stock",
        choices=["stock", "fund"],
        help="资产类型 (默认: stock)",
    )
    parser.add_argument("--days", "-d", type=int, default=60, help="历史数据天数 (默认: 60)")
    parser.add_argument("--batch", "-b", help="批量分析，逗号分隔，支持 code:type 格式")
    parser.add_argument("--pretty", "-p", action="store_true", help="格式化JSON输出（需配合 --json）")
    parser.add_argument("--test", action="store_true", help="离线测试模式（模拟数据）")
    parser.add_argument("--ascii", action="store_true", help="ASCII模式（避免中文乱码，需配合 --json）")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出（默认为终端表格模式）")
    parser.add_argument("--table", "-T", action="store_true", help="终端表格输出（默认模式，可省略）")
    parser.add_argument("--output", "-o", help="输出到文件（如 result.json）")
    parser.add_argument("--check", action="store_true", help="环境自检（检查依赖和数据源）")
    parser.add_argument("--verbose", action="store_true", help="详细输出（显示 INFO 级别日志）")
    parser.add_argument("--quiet", action="store_true", help="静默模式（仅输出错误）")

    # Watchlist 持仓管理
    wl_group = parser.add_mutually_exclusive_group()
    wl_group.add_argument("--watchlist", "-w", action="store_true", help="使用持仓列表进行分析")
    wl_group.add_argument("--add", metavar="CODE[:TYPE]", help="添加到持仓列表（如 600519 或 159934:fund）")
    wl_group.add_argument("--remove", metavar="CODE", help="从持仓列表删除")
    wl_group.add_argument("--list", action="store_true", help="查看当前持仓列表")

    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s v{VERSION}")

    args = parser.parse_args()

    # ---- Watchlist 持仓管理 ----
    if args.list or args.add or args.remove:
        config = _load_config()
        watchlist = config.get("watchlist", [])

        if args.list:
            if not watchlist:
                print("  持仓列表为空。使用 --add CODE[:TYPE] 添加。")
            else:
                print(f"  持仓列表 ({len(watchlist)} 项):")
                for i, item in enumerate(watchlist, 1):
                    if isinstance(item, str) and ":" in item:
                        code, typ = item.rsplit(":", 1)
                        label = "基金" if typ == "fund" else "股票"
                        print(f"    {i:>3d}. {code}  [{label}]")
                    else:
                        print(f"    {i:>3d}. {item}")
            print(f"\n  配置文件: {CONFIG_FILE}")
            return

        if args.add:
            entry = args.add.strip()
            if entry in watchlist:
                print(f"  {entry} 已在持仓列表中", file=sys.stderr)
                return
            watchlist.append(entry)
            config["watchlist"] = watchlist
            _save_config(config)
            print(f"  已添加: {entry}  (持仓列表: {len(watchlist)} 项)")
            return

        if args.remove:
            code = args.remove.strip()
            # 支持按纯代码删除（忽略 :type 后缀）
            new_list = []
            removed = False
            for item in watchlist:
                item_code = item.rsplit(":", 1)[0] if isinstance(item, str) and ":" in item else item
                if item_code == code:
                    removed = True
                else:
                    new_list.append(item)
            if not removed:
                print(f"  {code} 不在持仓列表中", file=sys.stderr)
                return
            config["watchlist"] = new_list
            _save_config(config)
            print(f"  已删除: {code}  (持仓列表: {len(new_list)} 项)")
            return

    # --watchlist: 从配置文件读取持仓列表，等效于 --batch
    if args.watchlist:
        config = _load_config()
        watchlist = config.get("watchlist", [])
        if not watchlist:
            print("  持仓列表为空。使用 --add CODE[:TYPE] 添加。", file=sys.stderr)
            sys.exit(1)
        args.batch = ",".join(watchlist)

    # 从配置文件读取默认参数（仅在用户未显式指定时生效）
    config = _load_config()
    defaults = config.get("defaults", {})
    # market
    if args.market == "auto" and defaults.get("market") != "auto":
        args.market = defaults["market"]
    # days
    if args.days == 60 and defaults.get("days") != 60:
        args.days = defaults["days"]
    # type
    if args.type == "stock" and defaults.get("asset_type") != "stock":
        args.type = defaults["asset_type"]

    # 参数校验
    if args.batch and args.stock_code:
        print(f"[WARNING] 同时指定了 stock_code ({args.stock_code}) 和 --batch，stock_code 将被忽略", file=sys.stderr)
    if args.json and args.table:
        print(f"[WARNING] --json 和 --table 同时指定，将使用 --json 输出", file=sys.stderr)

    # 日志级别控制
    if args.verbose:
        logger.setLevel(logging.INFO)
    elif args.quiet:
        logger.setLevel(logging.ERROR)

    # 环境自检
    if args.check:
        _run_check()
        return

    analyzer = StockAnalyzer()

    # 执行分析
    if args.batch:
        codes = [c.strip() for c in args.batch.split(",")]
        result = analyzer.analyze_batch(codes, args.market, test=args.test, asset_type=args.type, days=args.days)
    elif not args.stock_code:
        parser.print_help()
        print("\n[ERROR] 请提供股票/基金代码或使用 --batch", file=sys.stderr)
        sys.exit(1)
    elif args.test:
        result = analyzer.analyze_with_mock_data(args.stock_code, args.market, args.type, days=args.days)
    else:
        result = analyzer.analyze(args.stock_code, args.market, args.type, args.days)

    # 输出结果（默认为终端表格模式）
    use_ascii = args.ascii
    if args.json:
        # JSON 输出模式
        indent = 2 if args.pretty else None
        text = json.dumps(result, ensure_ascii=False, indent=indent)

        if use_ascii:
            for cn, en in ASCII_REPLACE_MAP.items():
                text = text.replace(cn, en)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(text)
                f.write("\n")
            print(f"结果已保存到: {args.output}", file=sys.stderr)
        else:
            print(text)
    else:
        # 默认表格输出模式
        _print_table(result, batch_mode=bool(args.batch), ascii_mode=use_ascii)
        if args.output:
            import io
            buf = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = buf
            _print_table(result, batch_mode=bool(args.batch), ascii_mode=use_ascii)
            sys.stdout = old_stdout
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(buf.getvalue())
            print(f"结果已保存到: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
