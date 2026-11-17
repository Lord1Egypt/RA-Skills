# -*- coding: utf-8 -*-
"""
Unified Stock Analysis & Quantitative Toolkit MCP Server for OpenClaw (v3.8.1).

Complete Coverage of Daily Stock Analysis Capabilities:
1. Fast quantitative screening (screen_stocks: 5 multi-factor strategies across 5200+ A-shares)
2. Realtime quote & technical diagnosis (ask_stock: MA, RSI, MACD, KDJ, volume-price observations)
3. Historical K-line backtesting (backtest_strategy: SMA cross, momentum breakout, RSI, MA trend, MACD cross)
4. Macro Market Review (get_market_review: Major indices, total volume, market breadth, sentiment)
5. Portfolio & Watchlist Management (manage_portfolio: add/remove/list watchlist & holdings, calculate PnL)
6. Price & Technical Alert Management (manage_alerts: create/list/delete price & technical alerts)
7. Deep AI Report & Research Trigger (generate_ai_report: invokes local DSA engine for complete multi-agent investment reports)
8. ML short-term direction prediction (predict_stock: walk-forward RF+GB ensemble, next-5-day signal)
9. Strategy Catalog Query (get_strategies)

Zero-token standalone mode for 1-6 (via Tencent high-availability feeds + local SQLite/JSON).
Auto-connects to local DSA service (port 8000) for deep AI reports.
"""

from __future__ import annotations

import json
import hmac
import logging
import os
import re
import secrets
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlencode, urlparse

import numpy as np
import pandas as pd
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("stock-copilot")

mcp = FastMCP(
    name="stock-copilot",
)

DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_UNIVERSE_PATH = os.path.join(DIR, "stock_universe.json")
PORTFOLIO_DB_PATH = os.path.join(DIR, "user_portfolio.db")
INDEX_PATH = os.getenv(
    "DSA_INDEX_PATH",
    os.path.join(os.path.expanduser("~"), ".cache", "daily_stock_analysis", "stocks.index.json"),
)
DSA_BASE_URL = os.getenv("DSA_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
DSA_PASSWORD = os.getenv("DSA_ADMIN_PASSWORD", "")

# Official Tonghuashun/iFinD HTTP QuantAPI.  The endpoint is intentionally not
# configurable so a refresh/access token cannot be redirected to another host.
THS_API_BASE_URL = "https://quantapi.51ifind.com"
THS_REFRESH_TOKEN = os.getenv("THS_REFRESH_TOKEN", os.getenv("IFIND_REFRESH_TOKEN", "")).strip()
THS_ACCESS_TOKEN = os.getenv("THS_ACCESS_TOKEN", "").strip()
STOCK_DATA_PROVIDER = os.getenv("STOCK_DATA_PROVIDER", "auto").strip().lower()
if STOCK_DATA_PROVIDER not in {"auto", "ths", "tencent"}:
    logger.warning("Unknown STOCK_DATA_PROVIDER=%s; using auto", STOCK_DATA_PROVIDER)
    STOCK_DATA_PROVIDER = "auto"

_session_cookie: Optional[str] = None
_ths_access_token: Optional[str] = None
_ths_access_token_expires_at = 0.0

# AI4Trade is a fixed, public integration endpoint.  Do not make this base URL
# configurable: an agent token must never be redirected to an arbitrary host.
AI4TRADE_API_BASE_URL = "https://ai4trade.ai/api"
AI4TRADE_TOKEN = os.getenv("AI4TRADE_TOKEN", "").strip()

# Optional research backends.  They run in a dedicated Python 3.12+ virtual
# environment so their large ML/LLM dependency trees never alter OpenClaw's
# runtime.  None of these settings are MCP arguments, avoiding executable or
# endpoint injection through a tool call.
QUANT_STATE_DIR = os.getenv(
    "STOCK_SCREENER_STATE_DIR",
    os.path.join(os.path.expanduser("~"), ".local", "share", "stock-screener-pro"),
)
QUANT_BACKEND_PYTHON = os.getenv(
    "QUANT_BACKEND_PYTHON",
    os.path.join(QUANT_STATE_DIR, "quant-backends", "bin", "python"),
)
VIBE_TRADING_BIN = os.getenv(
    "VIBE_TRADING_BIN",
    os.path.join(QUANT_STATE_DIR, "quant-backends", "vibe-trading", "bin", "vibe-trading"),
)
QUANTAALPHA_COMMIT = "b7ceb27b1001261d7a95b209a963664ae1f8ab23"
QUANTAALPHA_STATE_DIR = os.path.join(QUANT_STATE_DIR, "quant-backends", "quantaalpha")
QUANTAALPHA_REPO_DIR = os.getenv("QUANTAALPHA_REPO_DIR", os.path.join(QUANTAALPHA_STATE_DIR, "repo"))
QUANTAALPHA_PYTHON = os.getenv(
    "QUANTAALPHA_PYTHON", os.path.join(QUANTAALPHA_STATE_DIR, "venv", "bin", "python")
)
QUANTAALPHA_DATA_DIR = os.getenv("QUANTAALPHA_DATA_DIR", os.path.join(QUANTAALPHA_STATE_DIR, "data"))
QUANTAALPHA_RESULTS_DIR = os.getenv(
    "QUANTAALPHA_RESULTS_DIR", os.path.join(QUANT_STATE_DIR, "quantaalpha-results")
)
TENCENT_FACTOR_CACHE_DIR = os.path.join(QUANT_STATE_DIR, "tencent-factor-cache")
_TENCENT_PRICE_FACTORS = {
    "momentum_20": "20 日价格动量（过去 20 日收益）",
    "reversal_5": "5 日短期反转（过去 5 日收益取反）",
    "low_volatility_20": "20 日低波动（20 日收益波动率取反）",
    "volume_ratio_20": "20 日量比（当日成交量相对 20 日均量）",
    "ma_gap_20": "20 日均线偏离（收盘价相对 MA20）",
    "qa_roc5": "QuantaAlpha Alpha158_20 ROC5（5 日收益）",
    "qa_roc20": "QuantaAlpha Alpha158_20 ROC20（20 日收益）",
    "qa_vratio5": "QuantaAlpha Alpha158_20 VRATIO5（成交量/5日均量）",
    "qa_volatility10": "QuantaAlpha Alpha158_20 VOLATILITY10（10日收盘价波动/收盘价）",
    "qa_rsv10": "QuantaAlpha Alpha158_20 RSV10（10日区间位置）",
    "qa_ma_ratio10_20": "QuantaAlpha Alpha158_20 MA_RATIO10_20（MA10/MA20-1）",
}
_QUANTAALPHA_LIVE_FACTOR_IDS = (
    "qa_roc5",
    "qa_roc20",
    "qa_vratio5",
    "qa_volatility10",
    "qa_rsv10",
    "qa_ma_ratio10_20",
)
_EXTERNAL_LLM_ENV_NAMES = (
    "OPENAI_API_KEY",
    "GOOGLE_API_KEY",
    "ANTHROPIC_API_KEY",
    "XAI_API_KEY",
    "DEEPSEEK_API_KEY",
    "DASHSCOPE_API_KEY",
    "DASHSCOPE_CN_API_KEY",
    "ZHIPU_API_KEY",
    "ZHIPU_CN_API_KEY",
    "MINIMAX_API_KEY",
    "MINIMAX_CN_API_KEY",
    "OPENROUTER_API_KEY",
    "OPENAI_COMPATIBLE_API_KEY",
    "OPENAI_BASE_URL",
    "OLLAMA_BASE_URL",
    "TRADINGAGENTS_LLM_BACKEND_URL",
)
_OPENCLAW_MODEL_REF = "openclaw/default"
_OPENCLAW_BRIDGE_MAX_REQUEST_BYTES = 1_000_000
_OPENCLAW_BRIDGE_MAX_PROMPT_CHARS = 60_000
_RESEARCH_ONLY_TERMS = re.compile(
    r"(?:\b(?:buy|sell|short|cover|order|place\s+order|live\s+trade)\b|买入|卖出|下单|委托|开仓|平仓|实盘)",
    re.IGNORECASE,
)


def _init_portfolio_db():
    """Ensure local portfolio & watchlist sqlite tables exist."""
    try:
        with sqlite3.connect(PORTFOLIO_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS watchlist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE,
                    name TEXT,
                    group_name TEXT DEFAULT '默认自选',
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS positions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE,
                    name TEXT,
                    cost_price REAL,
                    shares INTEGER,
                    group_name TEXT DEFAULT '默认持仓',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS alert_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT,
                    name TEXT,
                    rule_type TEXT, -- 'price_above', 'price_below', 'pct_chg_above', 'pct_chg_below'
                    threshold REAL,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
    except Exception as e:
        logger.error(f"Failed to init portfolio db: {e}")


_init_portfolio_db()


def _clean_code(code: str) -> tuple[str, str]:
    """Return (market_prefix, 6_digit_code)."""
    c = code.strip().lower()
    if c.startswith("sh") or c.startswith("sz"):
        market, c = c[:2], c[2:]
    elif c.endswith(".sh") or c.endswith(".ss"):
        market, c = "sh", c.rsplit(".", 1)[0]
    elif c.endswith(".sz"):
        market, c = "sz", c.rsplit(".", 1)[0]
    else:
        market = "sh" if c.startswith(("6", "9")) else "sz"
    if not re.fullmatch(r"\d{6}", c):
        raise ValueError("股票代码必须是 6 位数字，可选 sh/sz 前缀或 .SH/.SZ 后缀")
    return market, c


def _get_a_share_pool() -> List[Dict[str, str]]:
    """Load A-share universe: prefer local bundled stock_universe.json, fallback to global index."""
    if os.path.exists(LOCAL_UNIVERSE_PATH):
        try:
            with open(LOCAL_UNIVERSE_PATH, "r", encoding="utf-8") as f:
                raw = json.load(f)
                return [{"code": r[0], "name": r[1], "market": r[2]} for r in raw]
        except Exception as e:
            logger.debug(f"Failed to load bundled stock_universe.json: {e}")

    if os.path.exists(INDEX_PATH):
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            stocks = []
            for item in data:
                if len(item) >= 8:
                    sym, code, name, pinyin, abbr, aliases, region, stype = item[:8]
                    if region == "CN" and stype == "stock":
                        if code.startswith("60") or code.startswith("68"):
                            stocks.append({"code": code, "name": name, "market": "sh"})
                        elif code.startswith("00") or code.startswith("30"):
                            stocks.append({"code": code, "name": name, "market": "sz"})
            if stocks:
                return stocks
        except Exception as e:
            logger.debug(f"Failed to load global stock index: {e}")

    return [
        {"code": "600519", "name": "贵州茅台", "market": "sh"},
        {"code": "300750", "name": "宁德时代", "market": "sz"},
        {"code": "002594", "name": "比亚迪", "market": "sz"},
        {"code": "601318", "name": "中国平安", "market": "sh"},
        {"code": "000001", "name": "平安银行", "market": "sz"},
    ]


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Convert scalar/list API values to float without leaking parser errors."""
    if isinstance(value, list):
        value = value[-1] if value else None
    if value in (None, "", "--", "None"):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _first_value(value: Any) -> Any:
    if isinstance(value, list):
        return value[0] if value else None
    return value


def _ths_tables(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    tables = payload.get("tables")
    if tables is None and isinstance(payload.get("data"), dict):
        tables = payload["data"].get("tables")
    return tables if isinstance(tables, list) else []


def _get_ths_access_token(force_refresh: bool = False) -> Optional[str]:
    """Get a short-lived access token from the official iFinD endpoint."""
    global _ths_access_token, _ths_access_token_expires_at
    if THS_ACCESS_TOKEN:
        return THS_ACCESS_TOKEN
    if not force_refresh and _ths_access_token and time.time() < _ths_access_token_expires_at:
        return _ths_access_token
    if not THS_REFRESH_TOKEN:
        return None

    url = f"{THS_API_BASE_URL}/api/v1/get_access_token"
    request = urllib.request.Request(
        url,
        data=b"",
        headers={"Content-Type": "application/json", "refresh_token": THS_REFRESH_TOKEN},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        body = json.loads(response.read().decode("utf-8"))
    data = body.get("data", {}) if isinstance(body, dict) else {}
    token = data.get("access_token") if isinstance(data, dict) else None
    if not token:
        raise RuntimeError(f"同花顺 access token 获取失败: {body.get('errmsg', '响应中没有 access_token')}")
    expires_in = _safe_float(data.get("expires_in"), 1800.0)
    _ths_access_token = str(token)
    _ths_access_token_expires_at = time.time() + max(60.0, expires_in - 60.0)
    return _ths_access_token


def _ths_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """POST JSON to the fixed official iFinD QuantAPI host."""
    last_error: Optional[Exception] = None
    for attempt in range(2):
        token = _get_ths_access_token(force_refresh=attempt > 0)
        if not token:
            raise RuntimeError("未配置 THS_REFRESH_TOKEN 或 THS_ACCESS_TOKEN")
        request = urllib.request.Request(
            f"{THS_API_BASE_URL}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "access_token": token,
                "ifindlang": "cn",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                body = json.loads(response.read().decode("utf-8"))
            error_code = body.get("errorcode") if isinstance(body, dict) else None
            if error_code not in (None, 0, "0"):
                raise RuntimeError(f"同花顺 QuantAPI 错误 {error_code}: {body.get('errmsg', '')}")
            return body
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in (401, 403) or THS_ACCESS_TOKEN:
                break
    raise RuntimeError(f"同花顺 QuantAPI 请求失败: {last_error}")


def _fetch_batch_quotes_ths(stocks: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Fetch current quotes from Tonghuashun's official HTTP QuantAPI."""
    if not stocks:
        return []
    stock_by_code = {s["code"]: s for s in stocks}
    results: List[Dict[str, Any]] = []
    for start in range(0, len(stocks), 80):
        chunk = stocks[start : start + 80]
        codes = ",".join(_to_exchange_code(s["code"]) for s in chunk)
        body = _ths_post(
            "/api/v1/real_time_quotation",
            {
                "codes": codes,
                "indicators": "open,high,low,latest,preClose,changeRatio,turnoverRatio,volume,amount",
            },
        )
        for item in _ths_tables(body):
            table = item.get("table", item)
            if not isinstance(table, dict):
                continue
            raw_code = _first_value(item.get("thscode", table.get("thscode", "")))
            _, code = _clean_code(str(raw_code))
            stock = stock_by_code.get(code, {"name": code})
            price = _safe_float(table.get("latest", table.get("new", table.get("close"))))
            if price <= 0:
                continue
            previous = _safe_float(table.get("preClose", table.get("prevClose")), price)
            results.append(
                {
                    "code": code,
                    "name": stock.get("name", code),
                    "price": price,
                    "open": _safe_float(table.get("open"), price),
                    "high": _safe_float(table.get("high"), price),
                    "low": _safe_float(table.get("low"), price),
                    "prev_close": previous,
                    "pct_chg": _safe_float(
                        table.get("changeRatio"),
                        ((price - previous) / previous * 100.0) if previous else 0.0,
                    ),
                    "turnover": _safe_float(table.get("turnoverRatio")),
                    "pe_ttm": 0.0,
                    "pb": 0.0,
                    "mkt_cap_yi": 0.0,
                    "amount_wan": _safe_float(table.get("amount")) / 10000.0,
                    "vol_hand": _safe_float(table.get("volume")) / 100.0,
                    "vol_ratio": 1.0,
                    "data_source": "tonghuashun-ifind",
                }
            )
    return results


def _fetch_batch_quotes_tencent(stocks: List[Dict[str, str]], timeout: int = 6) -> List[Dict[str, Any]]:
    """Fetch realtime quotes in batch from Tencent API."""
    if not stocks:
        return []

    results = []
    batch_size = 80
    batches = [stocks[i : i + batch_size] for i in range(0, len(stocks), batch_size)]

    def fetch_chunk(chunk):
        codes_query = [f"{s['market']}{s['code']}" for s in chunk]
        url = f"https://qt.gtimg.cn/q={','.join(codes_query)}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as res:
                text = res.read().decode("gbk", errors="ignore")
            chunk_res = []
            for line in text.strip().split(";\n"):
                if not line:
                    continue
                parts = line.split("~")
                if len(parts) > 46:
                    try:
                        price = float(parts[3])
                        if price <= 0:
                            continue
                        name = parts[1]
                        code = parts[2]
                        prev_close = float(parts[4]) if parts[4] else price
                        open_p = float(parts[5]) if parts[5] else price
                        high_p = float(parts[33]) if parts[33] else price
                        low_p = float(parts[34]) if parts[34] else price
                        vol_hand = float(parts[6]) if parts[6] else 0.0
                        amount_w = float(parts[37]) if parts[37] else 0.0
                        pct_chg = float(parts[32]) if parts[32] else 0.0
                        turnover = float(parts[38]) if parts[38] else 0.0
                        pe_ttm = float(parts[39]) if parts[39] else 0.0
                        pb = float(parts[46]) if parts[46] else 0.0
                        mkt_cap = float(parts[45]) if parts[45] else 0.0
                        vol_ratio = float(parts[49]) if len(parts) > 49 and parts[49] else 1.0

                        chunk_res.append(
                            {
                                "code": code,
                                "name": name,
                                "price": price,
                                "open": open_p,
                                "high": high_p,
                                "low": low_p,
                                "prev_close": prev_close,
                                "pct_chg": pct_chg,
                                "turnover": turnover,
                                "pe_ttm": pe_ttm,
                                "pb": pb,
                                "mkt_cap_yi": mkt_cap,
                                "amount_wan": amount_w,
                                "vol_hand": vol_hand,
                                "vol_ratio": vol_ratio,
                                "data_source": "tencent-public",
                            }
                        )
                    except Exception:
                        continue
            return chunk_res
        except Exception as err:
            logger.debug(f"Fetch chunk error: {err}")
            return []

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(fetch_chunk, b) for b in batches]
        for f in as_completed(futures):
            results.extend(f.result())

    return results


def _fetch_batch_quotes(stocks: List[Dict[str, str]], timeout: int = 6) -> List[Dict[str, Any]]:
    """Fetch quotes from the selected provider, with safe auto fallback."""
    wants_ths = STOCK_DATA_PROVIDER == "ths" or (
        STOCK_DATA_PROVIDER == "auto" and bool(THS_REFRESH_TOKEN or THS_ACCESS_TOKEN)
    )
    if wants_ths:
        try:
            ths_quotes = _fetch_batch_quotes_ths(stocks)
            if ths_quotes:
                if STOCK_DATA_PROVIDER == "auto":
                    # iFinD's generic realtime endpoint does not expose PE/PB/market cap.
                    # Enrich only those missing screening fields from the legacy public feed.
                    public = {q["code"]: q for q in _fetch_batch_quotes_tencent(stocks, timeout)}
                    for quote in ths_quotes:
                        fallback = public.get(quote["code"], {})
                        for key in ("pe_ttm", "pb", "mkt_cap_yi", "vol_ratio"):
                            if not quote.get(key):
                                quote[key] = fallback.get(key, quote.get(key, 0.0))
                return ths_quotes
            raise RuntimeError("同花顺未返回有效实时行情")
        except Exception as exc:
            logger.warning("Tonghuashun quote provider unavailable: %s", exc)
            if STOCK_DATA_PROVIDER == "ths":
                return []
    return _fetch_batch_quotes_tencent(stocks, timeout)


def _fetch_kline_tencent(code: str, count: int = 120) -> List[Dict[str, Any]]:
    """Fetch daily K-lines from the legacy Tencent public feed."""
    mkt, c = _clean_code(code)
    sym = f"{mkt}{c}"
    url = f"https://ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,{count},qfq"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode("utf-8"))
        raw = data.get("data", {}).get(sym, {}).get("qfqday", [])
        if not raw:
            raw = data.get("data", {}).get(sym, {}).get("day", [])
        klines = []
        for r in raw:
            if len(r) >= 6:
                klines.append(
                    {
                        "date": r[0],
                        "open": float(r[1]),
                        "close": float(r[2]),
                        "high": float(r[3]),
                        "low": float(r[4]),
                        "vol": float(r[5]),
                        "data_source": "tencent-public",
                    }
                )
        return klines
    except Exception as e:
        logger.debug(f"Failed to fetch kline for {code}: {e}")
        return []


def _fetch_kline_ths(code: str, count: int = 120) -> List[Dict[str, Any]]:
    """Fetch adjusted daily K-lines from Tonghuashun's official QuantAPI."""
    end_date = date.today()
    start_date = end_date - timedelta(days=max(90, count * 2))
    body = _ths_post(
        "/api/v1/cmd_history_quotation",
        {
            "codes": _to_exchange_code(code),
            "indicators": "open,high,low,close,volume",
            "startdate": start_date.isoformat(),
            "enddate": end_date.isoformat(),
            "functionpara": {"Interval": "D", "CPS": "1", "Fill": "Omit"},
        },
    )
    tables = _ths_tables(body)
    if not tables:
        return []
    item = tables[0]
    table = item.get("table", item)
    if not isinstance(table, dict):
        return []
    times = item.get("time", table.get("time", []))
    times = times if isinstance(times, list) else [times]

    def values(name: str) -> List[Any]:
        value = table.get(name, [])
        return value if isinstance(value, list) else [value]

    opens, highs, lows, closes, volumes = (
        values("open"),
        values("high"),
        values("low"),
        values("close"),
        values("volume"),
    )
    size = min(len(times), len(opens), len(highs), len(lows), len(closes))
    rows = []
    for index in range(size):
        close = _safe_float(closes[index])
        if close <= 0:
            continue
        rows.append(
            {
                "date": str(times[index])[:10],
                "open": _safe_float(opens[index], close),
                "close": close,
                "high": _safe_float(highs[index], close),
                "low": _safe_float(lows[index], close),
                "vol": _safe_float(volumes[index]) if index < len(volumes) else 0.0,
                "data_source": "tonghuashun-ifind",
            }
        )
    rows.sort(key=lambda row: row["date"])
    return rows[-count:]


def _fetch_kline(code: str, count: int = 120) -> List[Dict[str, Any]]:
    """Fetch daily K-lines from the selected provider, with auto fallback."""
    wants_ths = STOCK_DATA_PROVIDER == "ths" or (
        STOCK_DATA_PROVIDER == "auto" and bool(THS_REFRESH_TOKEN or THS_ACCESS_TOKEN)
    )
    if wants_ths:
        try:
            rows = _fetch_kline_ths(code, count)
            if rows:
                return rows
            raise RuntimeError("同花顺未返回有效历史行情")
        except Exception as exc:
            logger.warning("Tonghuashun history provider unavailable for %s: %s", code, exc)
            if STOCK_DATA_PROVIDER == "ths":
                return []
    return _fetch_kline_tencent(code, count)


def _to_exchange_code(code: str) -> str:
    """Normalize to 600519.SH / 000001.SZ form."""
    mkt, c = _clean_code(code)
    return f"{c}.{'SH' if mkt == 'sh' else 'SZ'}"


def _fetch_klines_extended_tencent(symbol_code: str, max_page: int = 12) -> pd.DataFrame:
    """Fetch paginated qfq daily bars from Tencent for ML prediction."""

    def fetch(start: str, end: str, count: int = 800) -> List:
        url = (
            f"https://ifzq.gtimg.cn/appstock/app/fqkline/get"
            f"?param={symbol_code},day,{start},{end},{count},qfq"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://gu.qq.com/"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            d = json.loads(resp.read().decode("utf-8"))
        node = d.get("data", {}).get(symbol_code, {})
        return node.get("qfqday") or node.get("day", [])

    all_bars: List = []
    prev_start: Optional[str] = None
    for _ in range(max_page):
        part = fetch("", prev_start or "", 800)
        if not part:
            break
        if prev_start:
            keep = [b for b in part if b[0] < prev_start]
            if not keep:
                break
            part = keep
        all_bars.extend(part)
        prev_start = part[0][0]
        if len(part) < 800:
            break

    rows = [
        {
            "date": pd.Timestamp(b[0]),
            "o": float(b[1]),
            "c": float(b[2]),
            "h": float(b[3]),
            "l": float(b[4]),
            "v": float(b[5]),
        }
        for b in reversed(all_bars)
    ]
    return pd.DataFrame(rows).sort_values("date").drop_duplicates("date").reset_index(drop=True)


def _fetch_klines_extended(symbol_code: str, max_page: int = 12) -> pd.DataFrame:
    """Fetch long daily history from the selected provider."""
    wants_ths = STOCK_DATA_PROVIDER == "ths" or (
        STOCK_DATA_PROVIDER == "auto" and bool(THS_REFRESH_TOKEN or THS_ACCESS_TOKEN)
    )
    if wants_ths:
        try:
            rows = _fetch_kline_ths(symbol_code, count=5000)
            if rows:
                return pd.DataFrame(
                    [
                        {
                            "date": pd.Timestamp(row["date"]),
                            "o": row["open"],
                            "c": row["close"],
                            "h": row["high"],
                            "l": row["low"],
                            "v": row["vol"],
                        }
                        for row in rows
                    ]
                ).sort_values("date").drop_duplicates("date").reset_index(drop=True)
            raise RuntimeError("同花顺未返回足够的历史行情")
        except Exception as exc:
            logger.warning("Tonghuashun ML history unavailable for %s: %s", symbol_code, exc)
            if STOCK_DATA_PROVIDER == "ths":
                return pd.DataFrame(columns=["date", "o", "c", "h", "l", "v"])
    return _fetch_klines_extended_tencent(symbol_code, max_page)


def _parse_research_date(value: str, field: str) -> pd.Timestamp:
    """Parse a date-only research boundary without accepting arbitrary strings."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value or ""):
        raise ValueError(f"{field} must be YYYY-MM-DD")
    try:
        return pd.Timestamp(value).normalize()
    except ValueError as exc:
        raise ValueError(f"{field} is not a valid calendar date") from exc


def _tencent_factor_cache_file(stock_code: str) -> str:
    market, code = _clean_code(stock_code)
    return os.path.join(TENCENT_FACTOR_CACHE_DIR, f"{market}{code}.csv")


def _load_tencent_factor_bars(
    stock_code: str,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    refresh_cache: bool = False,
) -> pd.DataFrame:
    """Load cached Tencent qfq bars, refreshing only when the requested range is absent."""
    cache_file = _tencent_factor_cache_file(stock_code)
    cached = pd.DataFrame()
    if not refresh_cache and os.path.isfile(cache_file):
        try:
            cached = pd.read_csv(cache_file, parse_dates=["date"])
            cached = cached[["date", "o", "c", "h", "l", "v"]].dropna(subset=["date", "c"])
        except (OSError, ValueError, KeyError, pd.errors.ParserError):
            cached = pd.DataFrame()
    required_start = start_date - pd.Timedelta(days=100)
    if cached.empty or cached["date"].min() > required_start or cached["date"].max() < end_date:
        market, code = _clean_code(stock_code)
        fetched = _fetch_klines_extended_tencent(f"{market}{code}")
        if fetched.empty:
            return fetched
        fetched = fetched[["date", "o", "c", "h", "l", "v"]].copy()
        fetched["date"] = pd.to_datetime(fetched["date"]).dt.normalize()
        os.makedirs(TENCENT_FACTOR_CACHE_DIR, mode=0o700, exist_ok=True)
        temporary = f"{cache_file}.{os.getpid()}.tmp"
        try:
            fetched.to_csv(temporary, index=False)
            os.replace(temporary, cache_file)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        cached = fetched
    cached["date"] = pd.to_datetime(cached["date"]).dt.normalize()
    return cached.sort_values("date").drop_duplicates("date").reset_index(drop=True)


def _build_tencent_factor_rows(
    stock_code: str,
    bars: pd.DataFrame,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    forward_days: int,
) -> pd.DataFrame:
    """Build point-in-time OHLCV factors and next-close-to-next-close forward returns."""
    if bars.empty:
        return pd.DataFrame()
    data = _calculate_tencent_price_factors(bars)
    if data.empty:
        return data
    close = data["c"]
    # The signal uses the completed bar at t.  Return therefore starts at t+1,
    # not at t, so a close-derived factor cannot see its own entry return.
    data["forward_return"] = close.shift(-(forward_days + 1)) / close.shift(-1) - 1.0
    data["forward_return_end_date"] = data["date"].shift(-(forward_days + 1))
    _, code = _clean_code(stock_code)
    data["stock_code"] = code
    return data[
        (data["date"] >= start_date)
        & (data["date"] <= end_date)
        & (data["forward_return_end_date"] <= end_date)
    ].copy()


def _calculate_tencent_price_factors(bars: pd.DataFrame) -> pd.DataFrame:
    """Calculate the local OHLCV factor set without adding future returns."""
    if bars.empty:
        return pd.DataFrame()
    data = bars.copy().sort_values("date").drop_duplicates("date")
    for column in ("o", "c", "h", "l", "v"):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data = data.dropna(subset=["date", "c", "h", "l", "v"])
    data = data[data["c"] > 0].copy()
    close, high, low, volume = data["c"], data["h"], data["l"], data["v"]
    returns = close.pct_change()
    data["momentum_20"] = close.pct_change(20)
    data["reversal_5"] = -close.pct_change(5)
    data["low_volatility_20"] = -returns.rolling(20, min_periods=20).std()
    data["volume_ratio_20"] = volume / volume.rolling(20, min_periods=20).mean() - 1.0
    data["ma_gap_20"] = close / close.rolling(20, min_periods=20).mean() - 1.0
    data["qa_roc5"] = close.pct_change(5)
    data["qa_roc20"] = close.pct_change(20)
    data["qa_vratio5"] = volume / volume.rolling(5, min_periods=5).mean()
    data["qa_volatility10"] = close.rolling(10, min_periods=10).std() / close
    data["qa_rsv10"] = (close - low.rolling(10, min_periods=10).min()) / (
        high.rolling(10, min_periods=10).max() - low.rolling(10, min_periods=10).min() + 1e-12
    )
    data["qa_ma_ratio10_20"] = (
        close.rolling(10, min_periods=10).mean() / close.rolling(20, min_periods=20).mean() - 1.0
    )
    return data


def _max_drawdown_from_returns(returns: List[float]) -> float:
    if not returns:
        return 0.0
    equity = np.cumprod(1.0 + np.asarray(returns, dtype=float))
    peaks = np.maximum.accumulate(equity)
    return float(np.max(1.0 - equity / peaks))


def _summarize_factor_period(observations: List[Dict[str, Any]], direction: int) -> Dict[str, Any]:
    if not observations:
        return {
            "observations": 0,
            "mean_rank_ic": None,
            "rank_ic_t_stat": None,
            "top_group_cumulative_return": None,
            "top_minus_bottom_cumulative_return": None,
            "top_group_max_drawdown": None,
            "top_group_positive_period_ratio": None,
        }
    adjusted_ic = [float(item["rank_ic"]) * direction for item in observations]
    top_returns = [float(item["top_return"] if direction > 0 else item["bottom_return"]) for item in observations]
    spreads = [float(item["top_return"] - item["bottom_return"]) * direction for item in observations]
    ic_std = float(np.std(adjusted_ic, ddof=1)) if len(adjusted_ic) > 1 else 0.0
    ic_t_stat = (float(np.mean(adjusted_ic)) / (ic_std / np.sqrt(len(adjusted_ic)))) if ic_std > 0 else None
    return {
        "observations": len(observations),
        "mean_rank_ic": round(float(np.mean(adjusted_ic)), 6),
        "rank_ic_t_stat": round(ic_t_stat, 4) if ic_t_stat is not None else None,
        "top_group_cumulative_return": round(float(np.prod(1.0 + np.asarray(top_returns)) - 1.0), 6),
        "top_minus_bottom_cumulative_return": round(float(np.prod(1.0 + np.asarray(spreads)) - 1.0), 6),
        "top_group_max_drawdown": round(_max_drawdown_from_returns(top_returns), 6),
        "top_group_positive_period_ratio": round(float(np.mean(np.asarray(top_returns) > 0.0)), 4),
    }


def _tencent_factor_random_control(
    observations: List[Dict[str, Any]], seeds: int) -> Dict[str, Any]:
    """Estimate a simple cross-sectional random top-minus-bottom baseline."""
    if not observations:
        return {"seeds": seeds, "mean_cumulative_return": None}
    cumulative_returns = []
    for seed in range(seeds):
        rng = np.random.default_rng(seed)
        trial = []
        for item in observations:
            values = np.asarray(item["forward_returns"], dtype=float)
            group_size = int(item["group_size"])
            if len(values) < group_size * 2:
                continue
            shuffled = rng.permutation(values)
            trial.append(float(np.mean(shuffled[:group_size]) - np.mean(shuffled[group_size : group_size * 2])))
        if trial:
            cumulative_returns.append(float(np.prod(1.0 + np.asarray(trial)) - 1.0))
    return {
        "seeds": seeds,
        "mean_cumulative_return": round(float(np.mean(cumulative_returns)), 6) if cumulative_returns else None,
    }


def _run_tencent_factor_research(
    stock_codes: List[str],
    start_date: str,
    end_date: str,
    factor_ids: Optional[List[str]] = None,
    forward_days: int = 20,
    rebalance_days: int = 20,
    oos_split: Optional[str] = None,
    random_seeds: int = 20,
    refresh_cache: bool = False,
) -> Dict[str, Any]:
    """Evaluate OHLCV factors over a caller-defined cross-section using Tencent qfq daily bars."""
    try:
        start = _parse_research_date(start_date, "start_date")
        end = _parse_research_date(end_date, "end_date")
    except ValueError as exc:
        return {"status": "error", "message": str(exc)}
    if start >= end:
        return {"status": "error", "message": "start_date must be earlier than end_date"}
    if not 5 <= forward_days <= 60 or not 5 <= rebalance_days <= 60:
        return {"status": "error", "message": "forward_days and rebalance_days must each be 5-60"}
    if not 5 <= random_seeds <= 100:
        return {"status": "error", "message": "random_seeds must be 5-100"}
    requested_factors = factor_ids or list(_TENCENT_PRICE_FACTORS)
    if not requested_factors or any(factor not in _TENCENT_PRICE_FACTORS for factor in requested_factors):
        return {"status": "error", "message": f"factor_ids must be chosen from {sorted(_TENCENT_PRICE_FACTORS)}"}
    normalized_codes = []
    invalid_codes = []
    for raw_code in stock_codes or []:
        try:
            _, code = _clean_code(str(raw_code))
            if code not in normalized_codes:
                normalized_codes.append(code)
        except ValueError:
            invalid_codes.append(str(raw_code))
    if invalid_codes:
        return {"status": "error", "message": f"invalid stock codes: {invalid_codes[:5]}"}
    if not 20 <= len(normalized_codes) <= 120:
        return {"status": "error", "message": "stock_codes must contain 20-120 unique A-share codes for cross-sectional research"}

    fetched: Dict[str, pd.DataFrame] = {}
    failed_codes: List[str] = []
    with ThreadPoolExecutor(max_workers=min(8, len(normalized_codes))) as executor:
        future_to_code = {
            executor.submit(_load_tencent_factor_bars, code, start, end, refresh_cache): code for code in normalized_codes
        }
        for future in as_completed(future_to_code):
            code = future_to_code[future]
            try:
                bars = future.result()
                if bars.empty:
                    failed_codes.append(code)
                else:
                    fetched[code] = bars
            except Exception as exc:
                logger.info("Tencent factor history unavailable for %s: %s", code, type(exc).__name__)
                failed_codes.append(code)
    # Futures complete in nondeterministic order.  Sort before constructing the
    # panel so seeded random controls are reproducible across identical runs.
    rows = [
        _build_tencent_factor_rows(code, fetched[code], start, end, forward_days)
        for code in sorted(fetched)
    ]
    panel = pd.concat([row for row in rows if not row.empty], ignore_index=True) if rows else pd.DataFrame()
    if panel.empty:
        return {"status": "error", "message": "Tencent returned no usable adjusted daily bars for the requested range", "failed_stock_codes": failed_codes}
    signal_dates = sorted(pd.Timestamp(value).normalize() for value in panel["date"].dropna().unique())
    if oos_split:
        try:
            split = _parse_research_date(oos_split, "oos_split")
        except ValueError as exc:
            return {"status": "error", "message": str(exc)}
    else:
        split = signal_dates[int(len(signal_dates) * 0.70)]
    if not start < split < end:
        return {"status": "error", "message": "oos_split must fall inside the research interval"}
    rebalance_dates = set(signal_dates[::rebalance_days])
    panel = panel[panel["date"].isin(rebalance_dates)].copy()
    observations: Dict[str, List[Dict[str, Any]]] = {factor: [] for factor in requested_factors}
    for signal_date, group in panel.groupby("date"):
        group = group.dropna(subset=["forward_return"] + requested_factors)
        if len(group) < 20:
            continue
        group_size = max(1, int(np.ceil(len(group) * 0.2)))
        forward_returns = group["forward_return"].to_numpy(dtype=float)
        forward_rank = group["forward_return"].rank(method="average")
        for factor in requested_factors:
            factor_rank = group[factor].rank(method="average")
            rank_ic = factor_rank.corr(forward_rank, method="pearson")
            if pd.isna(rank_ic):
                continue
            sorted_group = group.sort_values(factor)
            observations[factor].append(
                {
                    "date": pd.Timestamp(signal_date),
                    "rank_ic": float(rank_ic),
                    "bottom_return": float(sorted_group.head(group_size)["forward_return"].mean()),
                    "top_return": float(sorted_group.tail(group_size)["forward_return"].mean()),
                    "forward_returns": forward_returns.tolist(),
                    "group_size": group_size,
                }
            )
    results = []
    for factor in requested_factors:
        factor_observations = observations[factor]
        train = [item for item in factor_observations if item["date"] < split]
        oos = [item for item in factor_observations if item["date"] >= split]
        if not train or not oos:
            continue
        direction = 1 if float(np.mean([item["rank_ic"] for item in train])) >= 0.0 else -1
        train_summary = _summarize_factor_period(train, direction)
        oos_summary = _summarize_factor_period(oos, direction)
        random_control = _tencent_factor_random_control(oos, random_seeds)
        top_positive = (oos_summary["top_group_cumulative_return"] or 0.0) > 0.0
        spread_positive = (oos_summary["top_minus_bottom_cumulative_return"] or 0.0) > 0.0
        ic_positive = (oos_summary["mean_rank_ic"] or 0.0) > 0.0
        baseline = random_control["mean_cumulative_return"]
        beats_random = baseline is not None and (oos_summary["top_minus_bottom_cumulative_return"] or 0.0) > baseline
        results.append(
            {
                "factor_id": factor,
                "factor_name": _TENCENT_PRICE_FACTORS[factor],
                "direction_selected_in_train": "high" if direction > 0 else "low",
                "train": train_summary,
                "out_of_sample": oos_summary,
                "out_of_sample_random_control": random_control,
                "eligible_for_further_validation": bool(top_positive and spread_positive and ic_positive and beats_random),
            }
        )
    if not results:
        return {
            "status": "error",
            "message": "not enough shared cross-sectional observations after factor warm-up and forward-return alignment",
            "failed_stock_codes": failed_codes,
        }
    results.sort(
        key=lambda item: (item["out_of_sample"]["top_minus_bottom_cumulative_return"] or float("-inf")), reverse=True
    )
    return {
        "status": "success",
        "backend": "Tencent public adjusted daily bars + local deterministic factor evaluator",
        "data_source": "tencent-public",
        "price_adjustment": "qfq when Tencent provides it; otherwise unadjusted daily bars",
        "universe_type": "caller_supplied_current_or_archived_code_list",
        "stock_codes_requested": normalized_codes,
        "stock_codes_with_usable_history": sorted(fetched),
        "failed_stock_codes": sorted(failed_codes),
        "period": {"start_date": start.date().isoformat(), "end_date": end.date().isoformat()},
        "oos_split": split.date().isoformat(),
        "signal_lag_days": 1,
        "forward_days": forward_days,
        "rebalance_days": rebalance_days,
        "factor_results": results,
        "research_only": True,
        "no_llm": True,
        "no_broker_orders": True,
        "limitations": [
            "腾讯公开接口不提供经核验的历史 CSI300 成分；请传入当期归档股票池，避免幸存者偏差。",
            "仅含 OHLCV 价量因子；不含财务、行业中性化、停牌、涨跌停成交、借券或完整交易成本。",
            "分组多空收益是因子有效性的理论衡量，不是 A 股可直接执行的空头策略；历史结果不代表未来。",
        ],
    }


def _normalize_a_share_codes(values: Optional[List[str]]) -> Tuple[List[str], List[str]]:
    normalized: List[str] = []
    invalid: List[str] = []
    for raw_code in values or []:
        try:
            _, code = _clean_code(str(raw_code))
            if code not in normalized:
                normalized.append(code)
        except ValueError:
            invalid.append(str(raw_code))
    return normalized, invalid


def _score_portfolio_factors(
    portfolio_codes: List[str],
    peer_codes: List[str],
    start_date: str,
    as_of_date: str,
    factor_ids: Optional[List[str]] = None,
    oos_split: Optional[str] = None,
    position_weights: Optional[List[float]] = None,
    refresh_cache: bool = False,
) -> Dict[str, Any]:
    """Score holdings against a caller-supplied peer pool using validated live OHLCV factors."""
    holdings, invalid_holdings = _normalize_a_share_codes(portfolio_codes)
    peers, invalid_peers = _normalize_a_share_codes(peer_codes)
    invalid = invalid_holdings + invalid_peers
    if invalid:
        return {"status": "error", "message": f"invalid stock codes: {invalid[:5]}"}
    if not 1 <= len(holdings) <= 20:
        return {"status": "error", "message": "portfolio_codes must contain 1-20 unique A-share codes"}
    universe = list(holdings)
    for code in peers:
        if code not in universe:
            universe.append(code)
    if not 20 <= len(universe) <= 120:
        return {
            "status": "error",
            "message": "portfolio_codes plus peer_codes must contain 20-120 unique stocks for meaningful percentiles",
        }
    requested_factors = factor_ids or list(_QUANTAALPHA_LIVE_FACTOR_IDS)
    if not requested_factors or any(factor not in _QUANTAALPHA_LIVE_FACTOR_IDS for factor in requested_factors):
        return {
            "status": "error",
            "message": f"factor_ids must be chosen from {list(_QUANTAALPHA_LIVE_FACTOR_IDS)}",
        }
    try:
        start = _parse_research_date(start_date, "start_date")
        as_of = _parse_research_date(as_of_date, "as_of_date")
    except ValueError as exc:
        return {"status": "error", "message": str(exc)}
    if start >= as_of:
        return {"status": "error", "message": "start_date must be earlier than as_of_date"}
    if as_of > pd.Timestamp.now().normalize():
        return {"status": "error", "message": "as_of_date cannot be in the future"}

    if position_weights is None:
        normalized_weights = [1.0 / len(holdings)] * len(holdings)
    else:
        if len(position_weights) != len(holdings):
            return {"status": "error", "message": "position_weights must align with portfolio_codes"}
        try:
            raw_weights = [float(value) for value in position_weights]
        except (TypeError, ValueError):
            return {"status": "error", "message": "position_weights must contain finite non-negative numbers"}
        if any(not np.isfinite(value) or value < 0 for value in raw_weights) or sum(raw_weights) <= 0:
            return {"status": "error", "message": "position_weights must contain finite non-negative numbers"}
        normalized_weights = [value / sum(raw_weights) for value in raw_weights]

    validation = _run_tencent_factor_research(
        universe,
        start.date().isoformat(),
        as_of.date().isoformat(),
        requested_factors,
        20,
        20,
        oos_split,
        20,
        refresh_cache,
    )
    if validation.get("status") != "success":
        return {
            "status": "error",
            "message": "factor validation failed before portfolio scoring",
            "validation_error": validation,
        }

    factor_validation = {item["factor_id"]: item for item in validation["factor_results"]}
    validated_factors = [factor for factor in requested_factors if factor in factor_validation]
    omitted_factors = [factor for factor in requested_factors if factor not in factor_validation]
    eligible = [
        factor
        for factor in validated_factors
        if factor_validation[factor].get("eligible_for_further_validation")
        and (factor_validation[factor]["out_of_sample"].get("mean_rank_ic") or 0.0) >= 0.02
        and (factor_validation[factor]["out_of_sample"].get("observations") or 0) >= 8
        and (factor_validation[factor]["out_of_sample"].get("top_group_max_drawdown") or 1.0) <= 0.30
    ]
    active_factors = eligible or validated_factors
    if not active_factors:
        return {"status": "error", "message": "no factors had sufficient train and out-of-sample observations"}
    raw_importance = {
        factor: max(float(factor_validation[factor]["out_of_sample"]["mean_rank_ic"] or 0.0), 0.001)
        for factor in active_factors
    }
    importance_total = sum(raw_importance.values())
    factor_weights = {factor: value / importance_total for factor, value in raw_importance.items()}

    latest_rows: List[Dict[str, Any]] = []
    failed_codes: List[str] = []
    with ThreadPoolExecutor(max_workers=min(8, len(universe))) as executor:
        future_to_code = {
            executor.submit(_load_tencent_factor_bars, code, start, as_of, False): code for code in universe
        }
        for future in as_completed(future_to_code):
            code = future_to_code[future]
            try:
                calculated = _calculate_tencent_price_factors(future.result())
                calculated = calculated[calculated["date"] <= as_of].dropna(subset=validated_factors)
                if calculated.empty:
                    failed_codes.append(code)
                    continue
                latest = calculated.iloc[-1]
                row: Dict[str, Any] = {"stock_code": code, "data_date": pd.Timestamp(latest["date"]).normalize()}
                row.update({factor: float(latest[factor]) for factor in validated_factors})
                latest_rows.append(row)
            except Exception as exc:
                logger.info("Portfolio factor scoring unavailable for %s: %s", code, type(exc).__name__)
                failed_codes.append(code)
    if len(latest_rows) < 20:
        return {
            "status": "error",
            "message": "fewer than 20 stocks had complete latest factor observations",
            "stock_codes_with_usable_data": sorted(row["stock_code"] for row in latest_rows),
            "failed_stock_codes": sorted(failed_codes),
        }

    latest_panel = pd.DataFrame(latest_rows)
    for factor in validated_factors:
        direction = 1 if factor_validation[factor]["direction_selected_in_train"] == "high" else -1
        latest_panel[f"{factor}__percentile"] = (latest_panel[factor] * direction).rank(pct=True, method="average") * 100.0
    latest_panel["relative_exposure_score"] = sum(
        latest_panel[f"{factor}__percentile"] * factor_weights[factor] for factor in active_factors
    )

    name_by_code = {item["code"]: item["name"] for item in _get_a_share_pool()}
    score_by_code = {str(row["stock_code"]): row for _, row in latest_panel.iterrows()}
    positions = []
    portfolio_score = 0.0
    scored_weight = 0.0
    for code, weight in zip(holdings, normalized_weights):
        row = score_by_code.get(code)
        if row is None:
            positions.append({"stock_code": code, "stock_name": name_by_code.get(code, code), "status": "no_current_score"})
            continue
        score = float(row["relative_exposure_score"])
        portfolio_score += score * weight
        scored_weight += weight
        band = "high_relative_exposure" if score >= 70 else ("low_relative_exposure" if score < 30 else "middle_relative_exposure")
        factor_details = []
        for factor in validated_factors:
            factor_details.append(
                {
                    "factor_id": factor,
                    "factor_name": _TENCENT_PRICE_FACTORS[factor],
                    "raw_value": round(float(row[factor]), 6),
                    "direction_selected_in_train": factor_validation[factor]["direction_selected_in_train"],
                    "peer_percentile": round(float(row[f"{factor}__percentile"]), 2),
                    "used_in_composite": factor in active_factors,
                }
            )
        positions.append(
            {
                "stock_code": code,
                "stock_name": name_by_code.get(code, code),
                "status": "scored",
                "data_date": pd.Timestamp(row["data_date"]).date().isoformat(),
                "stale_calendar_days": int((as_of - pd.Timestamp(row["data_date"])).days),
                "normalized_position_weight": round(weight, 6),
                "relative_exposure_score": round(score, 2),
                "exposure_band": band,
                "factor_details": factor_details,
            }
        )

    compact_validation = []
    for factor in validated_factors:
        item = factor_validation[factor]
        compact_validation.append(
            {
                "factor_id": factor,
                "direction_selected_in_train": item["direction_selected_in_train"],
                "out_of_sample_mean_rank_ic": item["out_of_sample"]["mean_rank_ic"],
                "out_of_sample_spread_return": item["out_of_sample"]["top_minus_bottom_cumulative_return"],
                "out_of_sample_max_drawdown": item["out_of_sample"]["top_group_max_drawdown"],
                "eligible_for_further_validation": item["eligible_for_further_validation"],
                "composite_weight": round(factor_weights.get(factor, 0.0), 6),
            }
        )
    return {
        "status": "success",
        "backend": "QuantaAlpha Alpha158_20-compatible OHLCV factors + Tencent qfq daily bars",
        "quantaalpha_reference": {"factor_source": "alpha158_20", "pinned_commit": QUANTAALPHA_COMMIT},
        "data_source": "tencent-public",
        "as_of_date": as_of.date().isoformat(),
        "history_start_date": start.date().isoformat(),
        "oos_split": validation["oos_split"],
        "universe_size_requested": len(universe),
        "universe_size_scored": len(latest_rows),
        "portfolio_codes": holdings,
        "failed_stock_codes": sorted(set(validation.get("failed_stock_codes", [])) | set(failed_codes)),
        "factor_validation": compact_validation,
        "factors_without_sufficient_validation": omitted_factors,
        "portfolio_composite_gate": {
            "requires_factor_validation_gate": True,
            "minimum_out_of_sample_mean_rank_ic": 0.02,
            "minimum_out_of_sample_observations": 8,
            "maximum_out_of_sample_top_group_drawdown": 0.30,
        },
        "composite_uses_oos_eligible_factors": bool(eligible),
        "active_composite_factors": active_factors,
        "portfolio_relative_exposure_score": round(portfolio_score / scored_weight, 2) if scored_weight else None,
        "positions": positions,
        "research_only": True,
        "no_llm": True,
        "no_broker_orders": True,
        "limitations": [
            "该分数是对照池内的相对因子暴露，不是上涨概率、目标价或买卖建议。",
            "仅重算 QuantaAlpha Alpha158_20 中可由 OHLCV 映射的六个因子，不等同于完整模型预测或自定义因子库评分。",
            "当前未做行业、市值或基本面中性化；peer_codes 必须由调用者提供可复原且合理的对照池。",
            "样本外期参与因子准入筛选，因此组合分数是探索性结果，不是未经选择偏差污染的最终检验。",
            "腾讯公开复权数据、停牌和最新交易日覆盖可能不完整；历史样本外表现不代表未来。",
        ],
    }


_PREDICT_FEATURES = [
    "ret1", "ret5", "ret10", "ret20", "ret60",
    "ma5_dev", "ma10_dev", "ma20_dev", "ma60_dev",
    "vol20", "rsi14", "vchg5", "vprice", "pos20",
]
_PREDICT_CACHE: Dict[str, Dict[str, Any]] = {}


def _build_predict_features(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    c, h, l, v = d["c"], d["h"], d["l"], d["v"]
    d["ret1"] = c.pct_change(1)
    d["ret5"] = c.pct_change(5)
    d["ret10"] = c.pct_change(10)
    d["ret20"] = c.pct_change(20)
    d["ret60"] = c.pct_change(60)
    for w in (5, 10, 20, 60):
        ma = c.rolling(w).mean()
        d[f"ma{w}_dev"] = (c - ma) / ma
    d["vol20"] = d["ret1"].rolling(20).std()
    delta = c.diff()
    up = delta.clip(lower=0)
    dn = -delta.clip(upper=0)
    rs = up.rolling(14).mean() / (dn.rolling(14).mean() + 1e-12)
    d["rsi14"] = 100 - 100 / (1 + rs)
    d["vchg5"] = v.pct_change(5)
    d["vprice"] = v.rolling(5).mean() / (c * 1e4 + 1e-9)
    d["pos20"] = (c - l.rolling(20).max()) / (h.rolling(20).max() - l.rolling(20).min() + 1e-9) + 0.5
    d["fwd5"] = c.shift(-5) / c - 1.0
    return d


def _walk_forward_accuracy(X: pd.DataFrame, y: pd.Series, train_size: int, step: int = 5) -> Tuple[float, int, float]:
    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
    from sklearn.preprocessing import StandardScaler

    preds, trues = [], []
    Xv, yv = X.values, y.values
    rf = RandomForestClassifier(
        n_estimators=150, max_depth=5, min_samples_leaf=20,
        random_state=42, n_jobs=-1, class_weight="balanced_subsample",
    )
    gb = GradientBoostingClassifier(n_estimators=100, max_depth=2, learning_rate=0.05, random_state=42)
    i = train_size
    while i < len(y) - 5:
        ix = np.arange(i - train_size, i)
        if yv[ix].std() == 0:
            i += step
            continue
        sc = StandardScaler().fit(Xv[ix])
        Xt = sc.transform(Xv[ix])
        Xp = sc.transform(Xv[i : i + 1])
        for m in (rf, gb):
            m.fit(Xt, yv[ix])
        p = 0.5 * rf.predict_proba(Xp)[0, 1] + 0.5 * gb.predict_proba(Xp)[0, 1]
        preds.append(1 if p >= 0.5 else 0)
        trues.append(yv[i])
        i += step
    if not trues:
        return 0.0, 0, 0.0
    acc = float(np.mean(np.array(preds) == np.array(trues)))
    pos = float(np.mean(np.array(trues)))
    return acc, len(trues), pos


def _predict_symbol(code: str, force: bool = False) -> Dict[str, Any]:
    target = _to_exchange_code(code)
    mkt, c = _clean_code(code)
    symbol_code = f"{mkt}{c}"

    if not force and target in _PREDICT_CACHE:
        return _PREDICT_CACHE[target]

    df = _fetch_klines_extended(symbol_code)
    if len(df) < 300:
        result = {
            "code": target,
            "status": "error",
            "message": f"数据不足（仅 {len(df)} 根），无法训练",
        }
        return result

    f = _build_predict_features(df)
    last_close = float(f["c"].iloc[-1])
    last_date = str(f["date"].iloc[-1].date())

    model_df = f.dropna(subset=_PREDICT_FEATURES).reset_index(drop=True)
    X = model_df[_PREDICT_FEATURES].reset_index(drop=True)
    cut = len(f) - len(model_df)
    y_a = ((f["fwd5"] > 0).astype(int)).iloc[cut:].reset_index(drop=True)

    train_size = int(len(X) * 0.7)
    acc, n, _pos_rate = _walk_forward_accuracy(X, y_a, train_size=train_size, step=5)

    from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
    from sklearn.preprocessing import StandardScaler

    rf = RandomForestClassifier(
        n_estimators=500, max_depth=5, min_samples_leaf=20,
        random_state=42, n_jobs=-1, class_weight="balanced_subsample",
    )
    gb = GradientBoostingClassifier(n_estimators=250, max_depth=2, learning_rate=0.05, random_state=42)
    sc = StandardScaler().fit(X.values)
    Xt = sc.transform(X.values)
    Xlast = sc.transform(X.iloc[-1:].values)
    rf.fit(Xt, y_a.values)
    gb.fit(Xt, y_a.values)
    p_up = 0.5 * rf.predict_proba(Xlast)[0, 1] + 0.5 * gb.predict_proba(Xlast)[0, 1]

    verdict = "偏多" if p_up >= 0.55 else ("偏空" if p_up <= 0.45 else "方向不明")
    summary = (
        f"{target}: 最新收盘 {last_close:.2f}（{last_date}），未来5日上涨概率 {p_up:.1%}，"
        f"OOS准确率 {acc:.1%}（{n}点）→ {verdict}"
    )
    result = {
        "code": target,
        "status": "success",
        "last_close": round(last_close, 2),
        "last_date": last_date,
        "up_probability": round(p_up, 4),
        "oos_accuracy": round(acc, 4),
        "oos_samples": n,
        "verdict": verdict,
        "summary": summary,
        "disclaimer": "统计方向信号，非投资建议",
    }
    _PREDICT_CACHE[target] = result
    return result


def _get_dsa_cookie() -> Optional[str]:
    """Obtain session cookie from local DSA server if auth is enabled."""
    global _session_cookie
    if _session_cookie:
        return _session_cookie
    if not DSA_PASSWORD:
        return None

    safe_base_url, validation_error = _validated_dsa_base_url()
    if validation_error:
        logger.error("DSA connection blocked: %s", validation_error)
        return None

    try:
        url = f"{safe_base_url}/api/v1/auth/login"
        payload = json.dumps({"password": DSA_PASSWORD}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=4) as res:
            cookie_header = res.headers.get("Set-Cookie", "")
            if "dsa_session=" in cookie_header:
                for part in cookie_header.split(";"):
                    part = part.strip()
                    if part.startswith("dsa_session="):
                        _session_cookie = part.split("=")[1]
                        return _session_cookie
    except Exception as e:
        logger.debug(f"DSA auth login bypass/error: {e}")
    return None


def _validated_dsa_base_url() -> Tuple[Optional[str], Optional[str]]:
    """Allow DSA credentials only for a loopback service over HTTP(S)."""
    parsed = urlparse(DSA_BASE_URL)
    host = (parsed.hostname or "").lower()
    if parsed.scheme not in {"http", "https"} or not host:
        return None, "DSA_BASE_URL 必须是有效的 http(s) URL"
    is_loopback = host in {"localhost", "127.0.0.1", "::1"}
    if not is_loopback:
        return None, "DSA_BASE_URL 仅允许 localhost、127.0.0.1 或 ::1；不会向远程主机发送凭据"
    return DSA_BASE_URL, None


def _ai4trade_request(
    method: str,
    path: str,
    *,
    query: Optional[Dict[str, Any]] = None,
    payload: Optional[Dict[str, Any]] = None,
    requires_auth: bool = False,
) -> Dict[str, Any]:
    """Call a fixed AI4Trade API route without logging credentials or response bodies."""
    if not path.startswith("/") or "//" in path:
        return {"status": "error", "message": "Invalid AI4Trade API path"}
    if requires_auth and not AI4TRADE_TOKEN:
        return {
            "status": "error",
            "message": "AI4TRADE_TOKEN is not configured. Store it in the host secret manager or environment; do not pass it as a tool argument.",
        }
    url = f"{AI4TRADE_API_BASE_URL}{path}"
    if query:
        clean_query = {key: value for key, value in query.items() if value is not None and value != ""}
        if clean_query:
            url = f"{url}?{urlencode(clean_query, doseq=True)}"
    headers = {"Accept": "application/json"}
    if AI4TRADE_TOKEN:
        headers["Authorization"] = f"Bearer {AI4TRADE_TOKEN}"
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
    try:
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(request, timeout=20) as response:
            decoded = response.read().decode("utf-8")
        return {
            "status": "success",
            "source": "ai4trade",
            "untrusted_external_data": True,
            "data": json.loads(decoded),
        }
    except urllib.error.HTTPError as exc:
        return {"status": "error", "message": f"AI4Trade request failed (HTTP {exc.code})"}
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {"status": "error", "message": f"AI4Trade request failed: {type(exc).__name__}"}


def _require_ai4trade_confirmation(action: str, confirm: bool) -> Optional[Dict[str, Any]]:
    if confirm:
        return None
    return {
        "status": "confirmation_required",
        "message": f"{action} changes AI4Trade state. Obtain explicit user approval for this exact action, then call again with confirm=true.",
    }


def _ensure_quant_state_dir() -> str:
    """Create the local-only research artifact directory with private permissions."""
    os.makedirs(QUANT_STATE_DIR, mode=0o700, exist_ok=True)
    try:
        os.chmod(QUANT_STATE_DIR, 0o700)
    except OSError:
        pass
    return QUANT_STATE_DIR


def _quant_backend_python() -> Optional[str]:
    """Return the configured dedicated backend interpreter only when executable."""
    # Keep the venv entry-point symlink intact.  Resolving it would point to
    # uv's base interpreter and silently bypass the venv's site-packages.
    candidate = os.path.abspath(os.path.expanduser(QUANT_BACKEND_PYTHON))
    if not os.path.isabs(candidate) or not os.path.isfile(candidate) or not os.access(candidate, os.X_OK):
        return None
    return candidate


def _vibe_trading_command() -> Optional[str]:
    """Prefer the Skill-owned Vibe-Trading environment, then fall back to PATH."""
    candidate = os.path.abspath(os.path.expanduser(VIBE_TRADING_BIN))
    if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
        return candidate
    return shutil.which("vibe-trading")


def _quantaalpha_python() -> Optional[str]:
    """Return only the configured isolated QuantaAlpha interpreter."""
    candidate = os.path.abspath(os.path.expanduser(QUANTAALPHA_PYTHON))
    if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
        return candidate
    return None


def _quantaalpha_paths() -> Dict[str, str]:
    data_root = os.path.abspath(os.path.expanduser(QUANTAALPHA_DATA_DIR))
    return {
        "repo": os.path.abspath(os.path.expanduser(QUANTAALPHA_REPO_DIR)),
        "qlib": os.path.join(data_root, "qlib", "cn_data"),
        "factor_full": os.path.join(data_root, "factor_source"),
        "factor_debug": os.path.join(data_root, "factor_source_debug"),
        "results": os.path.abspath(os.path.expanduser(QUANTAALPHA_RESULTS_DIR)),
    }


def _quantaalpha_status() -> Dict[str, Any]:
    paths = _quantaalpha_paths()
    python = _quantaalpha_python()
    package_ready = _python_has_module(python, "quantaalpha")
    config_ready = os.path.isfile(os.path.join(paths["repo"], "configs", "experiment.yaml"))
    qlib_ready = all(
        os.path.isdir(os.path.join(paths["qlib"], name)) for name in ("calendars", "features", "instruments")
    )
    full_hdf5_ready = os.path.isfile(os.path.join(paths["factor_full"], "daily_pv.h5"))
    debug_hdf5_ready = os.path.isfile(os.path.join(paths["factor_debug"], "daily_pv.h5"))
    return {
        "pinned_commit": QUANTAALPHA_COMMIT,
        "package_available": package_ready,
        "config_available": config_ready,
        "qlib_data_available": qlib_ready,
        "full_factor_data_available": full_hdf5_ready,
        "debug_factor_data_available": debug_hdf5_ready,
        "ready_for_full_mining": package_ready and config_ready and qlib_ready and full_hdf5_ready,
        "ready_for_backtest": package_ready and config_ready and qlib_ready,
        "repo_dir": paths["repo"],
        "results_dir": paths["results"],
    }


def _backend_env() -> Dict[str, str]:
    """Pass only explicitly supported LLM settings to optional local backends."""
    env = {
        "HOME": os.path.expanduser("~"),
        "PATH": os.environ.get("PATH", ""),
        "LANG": os.environ.get("LANG", "en_US.UTF-8"),
        "LC_ALL": os.environ.get("LC_ALL", ""),
        "PYTHONIOENCODING": "utf-8",
        "TRADINGAGENTS_MEMORY_LOG_PATH": os.path.join(_ensure_quant_state_dir(), "tradingagents_memory.md"),
        "TRADINGAGENTS_CACHE_DIR": os.path.join(_ensure_quant_state_dir(), "tradingagents_cache"),
    }
    for name in _EXTERNAL_LLM_ENV_NAMES:
        if os.getenv(name):
            env[name] = os.environ[name]
    return {key: value for key, value in env.items() if value != ""}


def _openclaw_cli() -> Optional[str]:
    """Return the local OpenClaw CLI only when it is available on PATH."""
    return shutil.which("openclaw")


def _openclaw_result_text(raw: str) -> str:
    """Extract a bounded textual response from OpenClaw's JSON CLI output."""
    try:
        value: Any = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return raw.strip()

    def find_text(item: Any) -> Optional[str]:
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            for key in ("text", "content", "output", "response", "message"):
                found = find_text(item.get(key))
                if found:
                    return found
            for child in item.values():
                found = find_text(child)
                if found:
                    return found
        if isinstance(item, list):
            for child in item:
                found = find_text(child)
                if found:
                    return found
        return None

    return (find_text(value) or "").strip()


class _OpenClawInferenceBridge:
    """Short-lived, token-scoped OpenAI-compatible bridge to the local model.

    The TradingAgents subprocess only receives a random one-run token.  It
    never receives the Gateway token or a provider API key; the bridge invokes
    OpenClaw's local inference CLI, which reads the existing credential store.
    """

    def __init__(self, timeout_seconds: int):
        self.cli = _openclaw_cli()
        self.timeout_seconds = min(max(timeout_seconds, 30), 300)
        self.token = secrets.token_urlsafe(32)
        self._server: Optional[ThreadingHTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    @property
    def base_url(self) -> str:
        if not self._server:
            raise RuntimeError("OpenClaw bridge is not running")
        return f"http://127.0.0.1:{self._server.server_port}/v1"

    def __enter__(self) -> "_OpenClawInferenceBridge":
        if not self.cli:
            raise RuntimeError("OpenClaw CLI is unavailable")
        bridge = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: Any) -> None:
                return

            def _respond(self, status: int, payload: Dict[str, Any]) -> None:
                encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

            def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
                if self.path != "/v1/chat/completions":
                    self._respond(404, {"error": {"message": "not found"}})
                    return
                if not hmac.compare_digest(self.headers.get("Authorization", ""), f"Bearer {bridge.token}"):
                    self._respond(401, {"error": {"message": "unauthorized"}})
                    return
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                except ValueError:
                    length = 0
                if not 0 < length <= _OPENCLAW_BRIDGE_MAX_REQUEST_BYTES:
                    self._respond(413, {"error": {"message": "invalid request size"}})
                    return
                try:
                    request = json.loads(self.rfile.read(length).decode("utf-8"))
                    messages = request.get("messages", [])
                    if not isinstance(messages, list):
                        raise ValueError("messages must be a list")
                    chunks = []
                    for message in messages:
                        if not isinstance(message, dict) or not isinstance(message.get("content"), str):
                            raise ValueError("only text messages are supported")
                        chunks.append(f"{message.get('role', 'user')}: {message['content']}")
                    prompt = "\n\n".join(chunks)
                    if not prompt or len(prompt) > _OPENCLAW_BRIDGE_MAX_PROMPT_CHARS:
                        raise ValueError("prompt is empty or too long")
                except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
                    self._respond(400, {"error": {"message": f"invalid request: {exc}"}})
                    return
                try:
                    completed = subprocess.run(
                        [bridge.cli, "infer", "model", "run", "--gateway", "--json", "--prompt", prompt],
                        capture_output=True,
                        text=True,
                        timeout=bridge.timeout_seconds,
                        env={"HOME": os.path.expanduser("~"), "PATH": os.environ.get("PATH", "")},
                        check=False,
                    )
                    if completed.returncode != 0:
                        raise RuntimeError(_trim_backend_output(completed.stderr, 500) or "OpenClaw inference failed")
                    text = _openclaw_result_text(completed.stdout)
                    if not text:
                        raise RuntimeError("OpenClaw inference returned no text")
                except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
                    self._respond(502, {"error": {"message": f"OpenClaw inference unavailable: {type(exc).__name__}"}})
                    return
                self._respond(200, {
                    "id": f"stock-screener-{secrets.token_hex(8)}",
                    "object": "chat.completion",
                    "choices": [{"index": 0, "message": {"role": "assistant", "content": text}, "finish_reason": "stop"}],
                })

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()
        if self._thread:
            self._thread.join(timeout=2)


def _python_has_module(python: Optional[str], module: str) -> bool:
    if not python or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", module):
        return False
    try:
        result = subprocess.run(
            [python, "-c", f"import importlib.util; raise SystemExit(not bool(importlib.util.find_spec({module!r})))"],
            capture_output=True,
            text=True,
            timeout=10,
            env=_backend_env(),
            cwd=_ensure_quant_state_dir(),
            check=False,
        )
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _trim_backend_output(value: str, limit: int = 12000) -> str:
    value = (value or "").strip()
    return value if len(value) <= limit else f"…{value[-limit:]}"


def _run_research_backend(
    command: List[str],
    timeout_seconds: int,
    *,
    environment: Optional[Dict[str, str]] = None,
    cwd: Optional[str] = None,
) -> Dict[str, Any]:
    """Run a fixed local command without a shell and label its output untrusted."""
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=environment or _backend_env(),
            cwd=cwd or _ensure_quant_state_dir(),
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "message": f"研究后端超过 {timeout_seconds} 秒仍未完成，已终止。"}
    except OSError as exc:
        return {"status": "error", "message": f"无法启动本地研究后端: {type(exc).__name__}"}
    return {
        "status": "success" if completed.returncode == 0 else "error",
        "exit_code": completed.returncode,
        "untrusted_external_data": True,
        "stdout": _trim_backend_output(completed.stdout),
        "stderr": _trim_backend_output(completed.stderr, limit=4000),
    }


def _require_external_ai_confirmation(action: str, confirm_external_ai: bool) -> Optional[Dict[str, Any]]:
    if confirm_external_ai:
        return None
    return {
        "status": "confirmation_required",
        "message": (
            f"{action} may send the prompt/ticker to configured LLM and market-data providers and can incur cost. "
            "Obtain explicit approval for this exact research run, then call again with confirm_external_ai=true."
        ),
    }


def _require_research_only(prompt: str) -> Optional[Dict[str, Any]]:
    if not prompt or len(prompt.strip()) > 2400:
        return {"status": "error", "message": "研究提示词不能为空且不得超过 2400 个字符"}
    if _RESEARCH_ONLY_TERMS.search(prompt):
        return {
            "status": "error",
            "message": "量化后端适配层仅限研究、回测和模拟；拒绝包含实盘交易或下单意图的提示词。",
        }
    return None


def _a_share_ticker(stock_code: str) -> str:
    market, code = _clean_code(stock_code)
    return f"{code}.SS" if market == "sh" else f"{code}.SZ"


def _ema_series(values: List[float], period: int) -> List[float]:
    """Return a deterministic EMA series without depending on a charting package."""
    if not values:
        return []
    alpha = 2.0 / (period + 1.0)
    result = [float(values[0])]
    for value in values[1:]:
        result.append(alpha * float(value) + (1.0 - alpha) * result[-1])
    return result


def _latest_local_low_indexes(values: List[float], window: int = 35) -> List[int]:
    """Find the last two local lows for a research flag, not a trading signal."""
    start = max(1, len(values) - window)
    lows = [i for i in range(start, len(values) - 1) if values[i] <= values[i - 1] and values[i] < values[i + 1]]
    return lows[-2:]


def _technical_research_snapshot(klines: List[Dict[str, Any]], quote: Dict[str, Any]) -> Dict[str, Any]:
    """Compute transparent daily-bar observations for the book-inspired research templates."""
    if len(klines) < 30:
        return {"status": "insufficient_daily_bars", "required_bars": 30, "available_bars": len(klines)}

    closes = [float(k["close"]) for k in klines]
    highs = [float(k["high"]) for k in klines]
    lows = [float(k["low"]) for k in klines]
    volumes = [float(k.get("vol", 0.0)) for k in klines]
    ma5 = sum(closes[-5:]) / 5.0
    ma10 = sum(closes[-10:]) / 10.0
    ma20 = sum(closes[-20:]) / 20.0
    ma60 = sum(closes[-60:]) / min(len(closes), 60)

    ema12 = _ema_series(closes, 12)
    ema26 = _ema_series(closes, 26)
    dif = [a - b for a, b in zip(ema12, ema26)]
    dea = _ema_series(dif, 9)
    macd_hist = [(a - b) * 2.0 for a, b in zip(dif, dea)]
    macd_gold_cross = dif[-2] <= dea[-2] and dif[-1] > dea[-1]
    macd_dead_cross = dif[-2] >= dea[-2] and dif[-1] < dea[-1]
    macd_lows = _latest_local_low_indexes(dif)
    price_lows = _latest_local_low_indexes(closes)
    macd_bottom_divergence = False
    if len(macd_lows) == 2 and len(price_lows) == 2:
        macd_bottom_divergence = closes[price_lows[-1]] < closes[price_lows[-2]] and dif[macd_lows[-1]] > dif[macd_lows[-2]]

    raw_k, d_values, k_values = [], [], []
    prev_k = prev_d = 50.0
    for i in range(len(closes)):
        lo = min(lows[max(0, i - 8) : i + 1])
        hi = max(highs[max(0, i - 8) : i + 1])
        rsv = 50.0 if hi == lo else (closes[i] - lo) / (hi - lo) * 100.0
        prev_k = prev_k * 2.0 / 3.0 + rsv / 3.0
        prev_d = prev_d * 2.0 / 3.0 + prev_k / 3.0
        raw_k.append(rsv)
        k_values.append(prev_k)
        d_values.append(prev_d)
    j_values = [3 * k - 2 * d for k, d in zip(k_values, d_values)]
    kdj_lows = _latest_local_low_indexes(k_values)
    price_highs = [i for i in range(max(1, len(closes) - 35), len(closes) - 1) if closes[i] >= closes[i - 1] and closes[i] > closes[i + 1]][-2:]
    kdj_highs = [i for i in range(max(1, len(k_values) - 35), len(k_values) - 1) if k_values[i] >= k_values[i - 1] and k_values[i] > k_values[i + 1]][-2:]
    kdj_top_divergence = False
    if len(price_highs) == 2 and len(kdj_highs) == 2:
        kdj_top_divergence = closes[price_highs[-1]] > closes[price_highs[-2]] and k_values[kdj_highs[-1]] < k_values[kdj_highs[-2]]

    avg_vol_5 = sum(volumes[-5:]) / 5.0
    avg_vol_20 = sum(volumes[-20:]) / 20.0
    price_up = quote.get("pct_chg", 0.0) > 0
    current_vol = volumes[-1]
    if current_vol >= avg_vol_20 * 1.3 and price_up:
        volume_price_state = "量增价涨：仅作趋势延续观察"
    elif current_vol < avg_vol_5 * 0.8 and not price_up:
        volume_price_state = "缩量回调：观察回调力度，非买卖指令"
    elif current_vol >= avg_vol_20 * 1.3 and not price_up:
        volume_price_state = "放量走弱：需要复核供需与风险"
    elif current_vol < avg_vol_5 * 0.8 and price_up:
        volume_price_state = "缩量上涨：需警惕量价背离"
    else:
        volume_price_state = "量价中性"

    bar = klines[-1]
    one_yang_crosses_ma = bar["close"] > bar["open"] and bar["open"] < min(ma5, ma10, ma20) and bar["close"] > max(ma5, ma10, ma20)
    alignment = "多头排列" if ma5 > ma10 > ma60 else ("空头排列" if ma5 < ma10 < ma60 else "非顺序排列")
    return {
        "status": "success",
        "timeframe": "daily_adjusted_bars",
        "ma_5_10_60": {"ma5": round(ma5, 2), "ma10": round(ma10, 2), "ma60": round(ma60, 2), "alignment": alignment},
        "macd_12_26_9": {"dif": round(dif[-1], 4), "dea": round(dea[-1], 4), "histogram": round(macd_hist[-1], 4), "gold_cross": macd_gold_cross, "dead_cross": macd_dead_cross, "bottom_divergence_watch": macd_bottom_divergence},
        "kdj_9_3_3": {"k": round(k_values[-1], 2), "d": round(d_values[-1], 2), "j": round(j_values[-1], 2), "top_divergence_watch": kdj_top_divergence},
        "volume_price": {"latest_volume": round(current_vol, 2), "average_volume_5d": round(avg_vol_5, 2), "average_volume_20d": round(avg_vol_20, 2), "state": volume_price_state, "quote_volume_ratio": quote.get("vol_ratio", 0.0)},
        "breakout_observation": {"one_yang_crosses_ma5_10_20": one_yang_crosses_ma, "current_bar_complete": False, "note": "当日K线在收盘前可能变化；仅作观察，收盘后再验证。"},
        "ma_reference": {"ma5": round(ma5, 2), "ma10": round(ma10, 2), "note": "均线是波动参考线，不是自动止损或委托价格。"},
        "data_limits": ["宝塔线因不同软件的反转参数不一致，未在此统一计算。", "盘口五档、板块出现频率、振幅、流通股本及20日涨停历史需要额外的Level-2/结构化数据，当前公共行情不作伪筛选。"],
        "research_only": True,
    }


# ==========================================
# Tool 1: 智能选股 (Screening)
# ==========================================
@mcp.tool()
def screen_stocks(
    strategy: str = "bull_momentum",
    market_cap_min_yi: float = 50.0,
    market_cap_max_yi: float = 50000.0,
    pe_min: float = 0.0,
    pe_max: float = 120.0,
    price_min: float = 3.0,
    price_max: float = 500.0,
    turnover_min: float = 1.0,
    top_n: int = 10,
) -> Dict[str, Any]:
    """
    全市场量化智能选股（覆盖 A 股 5200+ 标的，秒级扫描，免 Token）。

    Args:
        strategy: 选股策略:
            - 'bull_momentum': 多头突破动量（均线多头、换手活跃、放量突破、涨幅稳健，默认）
            - 'low_valuation_value': 低估值白马/高股息（PE<25, PB<2.8, 市值>150亿, 稳健防御）
            - 'volume_breakout': 放量异动启动（量比>1.4, 换手>2%, 当日涨幅2.5%~8.5%）
            - 'growth_tech': 科技成长高弹性（成长龙头，适度估值，高换手）
            - 'oversold_rebound': 超跌反弹潜伏（低位企稳，今日温和放量回升）
            - 'book_volume_turnover': 量比换手观察（换手>=3%、量比>=1.5%，仅覆盖可得硬条件）
            - 'volume_ratio_watch': 强量比观察（量比>2、换手1%~5%，仅作候选初筛）
        market_cap_min_yi: 最低总市值（亿元），默认 50
        market_cap_max_yi: 最高总市值（亿元），默认 50000
        pe_min: 最低 PE(TTM)，默认 0 (排除亏损股)
        pe_max: 最高 PE(TTM)，默认 120
        price_min: 最低股价（元），默认 3.0 (排除退市仙股)
        price_max: 最高股价（元），默认 500.0
        turnover_min: 最低换手率%，默认 1.0%
        top_n: 返回前 N 只最优质股票，默认 10
    """
    all_stocks = _get_a_share_pool()
    if not all_stocks:
        return {"error": "Failed to load A-share pool", "results": []}

    quotes = _fetch_batch_quotes(all_stocks)
    if not quotes:
        return {"error": "Failed to fetch realtime quotes", "results": []}

    candidates = []
    for q in quotes:
        if "ST" in q["name"] or "退" in q["name"]:
            continue
        if not (price_min <= q["price"] <= price_max):
            continue
        if not (market_cap_min_yi <= q["mkt_cap_yi"] <= market_cap_max_yi):
            continue
        if not (pe_min <= q["pe_ttm"] <= pe_max):
            continue
        if q["turnover"] < turnover_min:
            continue
        candidates.append(q)

    scored_candidates = []
    if strategy == "bull_momentum":
        for c in candidates:
            if 1.5 <= c["pct_chg"] <= 9.5 and c["turnover"] >= 1.5:
                score = (c["pct_chg"] * 4.0) + min(c["turnover"] * 2.0, 20.0) + (100.0 / (c["pe_ttm"] + 10)) * 2.0
                scored_candidates.append({**c, "score": round(score, 1), "reason": f"涨幅{c['pct_chg']}%且换手{c['turnover']}%活跃"})
    elif strategy == "low_valuation_value":
        for c in candidates:
            if 0 < c["pe_ttm"] <= 25.0 and 0 < c["pb"] <= 2.8 and c["mkt_cap_yi"] >= 150.0:
                score = (30.0 - c["pe_ttm"]) * 2.0 + (3.0 - c["pb"]) * 10.0 + min(c["mkt_cap_yi"] / 500.0, 20.0)
                scored_candidates.append({**c, "score": round(score, 1), "reason": f"低PE({c['pe_ttm']})低PB({c['pb']})大市值龙头"})
    elif strategy == "volume_breakout":
        for c in candidates:
            if c["vol_ratio"] >= 1.4 and 2.5 <= c["pct_chg"] <= 8.5 and c["turnover"] >= 2.0:
                score = (c["vol_ratio"] * 15.0) + (c["pct_chg"] * 3.0) + (c["turnover"] * 1.5)
                scored_candidates.append({**c, "score": round(score, 1), "reason": f"量比{c['vol_ratio']}显著放大，涨幅{c['pct_chg']}%"})
    elif strategy == "growth_tech":
        for c in candidates:
            if 80.0 <= c["mkt_cap_yi"] <= 3000.0 and 2.0 <= c["turnover"] <= 15.0 and c["pct_chg"] > 0:
                score = (c["pct_chg"] * 3.5) + (c["turnover"] * 2.5) + (150.0 / (c["pe_ttm"] + 15))
                scored_candidates.append({**c, "score": round(score, 1), "reason": f"高弹性成长股，换手{c['turnover']}%, 涨幅{c['pct_chg']}%"})
    elif strategy == "oversold_rebound":
        for c in candidates:
            if 0.5 <= c["pct_chg"] <= 4.5 and c["turnover"] >= 1.2:
                score = (5.0 - abs(c["pct_chg"] - 2.5)) * 5.0 + c["turnover"] * 2.0 + (100.0 / (c["pe_ttm"] + 10))
                scored_candidates.append({**c, "score": round(score, 1), "reason": f"低位温和放量企稳，涨幅{c['pct_chg']}%"})
    elif strategy == "book_volume_turnover":
        for c in candidates:
            if c["turnover"] >= 3.0 and c["vol_ratio"] >= 1.5:
                score = c["vol_ratio"] * 14.0 + c["turnover"] * 2.0 + max(c["pct_chg"], 0.0)
                scored_candidates.append({**c, "score": round(score, 1), "reason": f"研究模板：换手{c['turnover']}%、量比{c['vol_ratio']}；振幅/流通盘/涨停历史未参与筛选"})
    elif strategy == "volume_ratio_watch":
        for c in candidates:
            if c["vol_ratio"] > 2.0 and 1.0 <= c["turnover"] < 5.0:
                score = c["vol_ratio"] * 18.0 + c["turnover"] * 1.5
                scored_candidates.append({**c, "score": round(score, 1), "reason": f"研究模板：量比{c['vol_ratio']}、换手{c['turnover']}%；不等同交易信号"})
    else:
        for c in candidates:
            score = c["pct_chg"] * 3.0 + c["turnover"] * 2.0
            scored_candidates.append({**c, "score": round(score, 1), "reason": "满足基础量化过滤条件"})

    scored_candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
    top_candidates = scored_candidates[:top_n]

    final_results = []
    for item in top_candidates:
        klines = _fetch_kline(item["code"], count=30)
        ma_info = {}
        if len(klines) >= 20:
            closes = [k["close"] for k in klines]
            ma5 = sum(closes[-5:]) / 5.0
            ma10 = sum(closes[-10:]) / 10.0
            ma20 = sum(closes[-20:]) / 20.0
            ma_trend = "多头排列(MA5>MA10>MA20)" if ma5 > ma10 > ma20 else "震荡/整理"
            ma_info = {
                "ma5": round(ma5, 2),
                "ma10": round(ma10, 2),
                "ma20": round(ma20, 2),
                "ma_trend": ma_trend,
            }

        final_results.append(
            {
                "code": item["code"],
                "name": item["name"],
                "price": item["price"],
                "pct_chg": f"{item['pct_chg']}%",
                "turnover": f"{item['turnover']}%",
                "pe_ttm": item["pe_ttm"],
                "pb": item["pb"],
                "mkt_cap_yi": f"{item['mkt_cap_yi']}亿",
                "vol_ratio": item.get("vol_ratio", 1.0),
                "score": item.get("score", 0),
                "signal_reason": item.get("reason", ""),
                **ma_info,
            }
        )

    return {
        "status": "success",
        "data_source": quotes[0].get("data_source", "unknown") if quotes else "unknown",
        "strategy": strategy,
        "universe_count": len(all_stocks),
        "filtered_count": len(candidates),
        "matched_count": len(scored_candidates),
        "top_stocks": final_results,
        "research_only": True,
        "data_limit_note": "当前公共行情未统一提供振幅、流通股本和20日涨停历史，相关书中硬条件未被伪装为已筛选。",
    }


# ==========================================
# Tool 2: 问股票 (Stock QA & Technical Diagnosis)
# ==========================================
@mcp.tool()
def ask_stock(stock_code_or_name: str) -> Dict[str, Any]:
    """
    实时查询单只股票的实时行情数据、量价关系、均线多空形态、RSI 与 20日支撑/压力位。

    Args:
        stock_code_or_name: 股票代码（如 '600519', '000001', '300750'）或名称（如 '贵州茅台', '宁德时代'）
    """
    target = stock_code_or_name.strip()
    code = None
    name = None

    if not (target.isdigit() or target.startswith("sh") or target.startswith("sz")):
        all_stocks = _get_a_share_pool()
        for s in all_stocks:
            if target in s["name"]:
                code = s["code"]
                name = s["name"]
                break
        if not code:
            return {"error": f"未能找到与 '{target}' 匹配的A股股票代码，请提供6位股票代码"}
    else:
        mkt, code = _clean_code(target)

    mkt, c = _clean_code(code)
    quotes = _fetch_batch_quotes([{"code": c, "market": mkt, "name": name or c}])
    if not quotes:
        return {"error": f"获取股票 {code} 实时行情失败"}
    quote = quotes[0]

    klines = _fetch_kline(c, count=60)
    diagnosis = {}
    if len(klines) >= 20:
        closes = [k["close"] for k in klines]
        ma5 = round(sum(closes[-5:]) / 5.0, 2)
        ma10 = round(sum(closes[-10:]) / 10.0, 2)
        ma20 = round(sum(closes[-20:]) / 20.0, 2)
        ma60 = round(sum(closes[-60:]) / len(closes[-60:]), 2) if len(closes) >= 30 else None

        cur_p = quote["price"]
        trend_label = "强势多头" if cur_p > ma5 > ma10 > ma20 else ("弱势空头" if cur_p < ma5 < ma10 < ma20 else "震荡整理")

        if len(closes) >= 15:
            diffs = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
            recent_diffs = diffs[-14:]
            gains = [d for d in recent_diffs if d > 0]
            losses = [-d for d in recent_diffs if d < 0]
            avg_gain = sum(gains) / 14.0 if gains else 0.0001
            avg_loss = sum(losses) / 14.0 if losses else 0.0001
            rs = avg_gain / avg_loss
            rsi14 = round(100 - (100 / (1 + rs)), 1)
        else:
            rsi14 = 50.0

        rsi_state = "超买预警" if rsi14 >= 80 else ("超跌反弹区" if rsi14 <= 25 else "合理区间")
        recent_high_20 = max(closes[-20:])
        recent_low_20 = min(closes[-20:])

        diagnosis = {
            "ma5": ma5,
            "ma10": ma10,
            "ma20": ma20,
            "ma60": ma60,
            "trend": trend_label,
            "rsi14": rsi14,
            "rsi_state": rsi_state,
            "support_level_20d": recent_low_20,
            "pressure_level_20d": recent_high_20,
        }
        diagnosis["book_technique_research"] = _technical_research_snapshot(klines, quote)

    return {
        "status": "success",
        "data_source": quote.get("data_source", "unknown"),
        "code": quote["code"],
        "name": quote["name"],
        "price": quote["price"],
        "pct_chg": f"{quote['pct_chg']}%",
        "open": quote["open"],
        "high": quote["high"],
        "low": quote["low"],
        "prev_close": quote["prev_close"],
        "turnover": f"{quote['turnover']}%",
        "pe_ttm": quote["pe_ttm"],
        "pb": quote["pb"],
        "mkt_cap_yi": f"{quote['mkt_cap_yi']}亿",
        "vol_ratio": quote.get("vol_ratio", 1.0),
        "technical_diagnosis": diagnosis,
        "summary": f"{quote['name']}({quote['code']}) 当前价 {quote['price']}元，涨跌幅 {quote['pct_chg']}%，形态呈现【{diagnosis.get('trend', '正常')}】，RSI(14)={diagnosis.get('rsi14', 50)}处于【{diagnosis.get('rsi_state', '正常')}】。",
    }


# ==========================================
# Tool 3: 策略历史回测 (Backtest)
# ==========================================
@mcp.tool()
def backtest_strategy(
    stock_code: str,
    strategy: str = "sma_cross",
    lookback_bars: int = 120,
    initial_cash: float = 100000.0,
) -> Dict[str, Any]:
    """
    对个股进行历史日 K 线的量化交易策略回测，输出总收益、Alpha 超额、最大回撤与胜率。

    Args:
        stock_code: 股票代码（如 '600519', '300750'）
        strategy: 回测策略:
            - 'sma_cross': 双均线金叉策略（MA5上穿MA20全仓买入，下穿卖出）
            - 'momentum_breakout': 动量突破策略（创20日新高买入，跌破10日均线止损）
            - 'rsi_mean_reversion': RSI均值回归策略（RSI<30超卖买入，RSI>70超买卖出）
            - 'ma_5_10_60_trend': 三均线趋势过滤（价格与MA5>MA10>MA60进入，破MA10或趋势反转退出）
            - 'macd_cross_trend': MACD交叉趋势研究（DIF上穿DEA且价格高于MA20进入，死叉退出）
        lookback_bars: 回测历史K线根数（默认 120 根，约半年~大半年交易日，最大 200）
        initial_cash: 初始资金（默认 100,000 元）
    """
    mkt, c = _clean_code(stock_code)
    lookback_bars = min(max(lookback_bars, 30), 200)
    klines = _fetch_kline(c, count=lookback_bars)
    if len(klines) < 30:
        return {"error": f"股票 {stock_code} 历史K线不足（仅{len(klines)}根），无法完成回测"}

    cash = initial_cash
    shares = 0
    trades = []
    equity_curve = []
    peak_equity = initial_cash
    max_drawdown = 0.0

    closes = [k["close"] for k in klines]
    dates = [k["date"] for k in klines]

    ma5 = [sum(closes[max(0, i - 4) : i + 1]) / len(closes[max(0, i - 4) : i + 1]) for i in range(len(closes))]
    ma10 = [sum(closes[max(0, i - 9) : i + 1]) / len(closes[max(0, i - 9) : i + 1]) for i in range(len(closes))]
    ma20 = [sum(closes[max(0, i - 19) : i + 1]) / len(closes[max(0, i - 19) : i + 1]) for i in range(len(closes))]
    ma60 = [sum(closes[max(0, i - 59) : i + 1]) / len(closes[max(0, i - 59) : i + 1]) for i in range(len(closes))]
    dif = [a - b for a, b in zip(_ema_series(closes, 12), _ema_series(closes, 26))]
    dea = _ema_series(dif, 9)

    rsi = [50.0] * len(closes)
    for i in range(14, len(closes)):
        diffs = [closes[j] - closes[j - 1] for j in range(i - 13, i + 1)]
        gains = [d for d in diffs if d > 0]
        losses = [-d for d in diffs if d < 0]
        avg_g = sum(gains) / 14.0 if gains else 0.0001
        avg_l = sum(losses) / 14.0 if losses else 0.0001
        rs = avg_g / avg_l
        rsi[i] = 100 - (100 / (1 + rs))

    start_idx = 20
    winning_trades = 0
    total_round_trips = 0
    last_buy_price = 0.0

    for i in range(start_idx, len(klines)):
        dt = dates[i]
        price = closes[i]
        buy_signal = False
        sell_signal = False

        if strategy == "sma_cross":
            if ma5[i - 1] <= ma20[i - 1] and ma5[i] > ma20[i]:
                buy_signal = True
            elif ma5[i - 1] >= ma20[i - 1] and ma5[i] < ma20[i]:
                sell_signal = True
        elif strategy == "momentum_breakout":
            high_20 = max(closes[i - 20 : i])
            if price > high_20 and price > ma20[i]:
                buy_signal = True
            elif price < ma10[i]:
                sell_signal = True
        elif strategy == "rsi_mean_reversion":
            if rsi[i] < 32 and price > ma5[i]:
                buy_signal = True
            elif rsi[i] > 68 or price < ma20[i] * 0.96:
                sell_signal = True
        elif strategy == "ma_5_10_60_trend":
            if i >= 59 and price > ma5[i] > ma10[i] > ma60[i]:
                buy_signal = True
            elif i >= 59 and (price < ma10[i] or ma10[i] < ma60[i]):
                sell_signal = True
        elif strategy == "macd_cross_trend":
            if dif[i - 1] <= dea[i - 1] and dif[i] > dea[i] and price > ma20[i]:
                buy_signal = True
            elif dif[i - 1] >= dea[i - 1] and dif[i] < dea[i]:
                sell_signal = True

        if buy_signal and shares == 0 and cash > price * 100:
            buy_shares = int((cash * 0.95) // (price * 100)) * 100
            if buy_shares > 0:
                cost = buy_shares * price * 1.0003
                cash -= cost
                shares = buy_shares
                last_buy_price = price
                trades.append({"date": dt, "action": "BUY", "price": price, "shares": buy_shares, "cash_left": round(cash, 2)})

        elif sell_signal and shares > 0:
            revenue = shares * price * 0.9987
            cash += revenue
            pnl = (price - last_buy_price) / last_buy_price * 100
            if pnl > 0:
                winning_trades += 1
            total_round_trips += 1
            trades.append(
                {
                    "date": dt,
                    "action": "SELL",
                    "price": price,
                    "shares": shares,
                    "pnl_pct": f"{round(pnl, 2)}%",
                    "cash_after": round(cash, 2),
                }
            )
            shares = 0

        current_equity = cash + (shares * price)
        if current_equity > peak_equity:
            peak_equity = current_equity
        dd = (peak_equity - current_equity) / peak_equity * 100.0
        if dd > max_drawdown:
            max_drawdown = dd
        equity_curve.append({"date": dt, "equity": round(current_equity, 2)})

    final_price = closes[-1]
    final_equity = cash + (shares * final_price)
    total_return_pct = (final_equity - initial_cash) / initial_cash * 100.0

    bench_initial_price = closes[start_idx]
    bench_return_pct = (final_price - bench_initial_price) / bench_initial_price * 100.0
    win_rate = (winning_trades / total_round_trips * 100.0) if total_round_trips > 0 else 0.0

    return {
        "status": "success",
        "data_source": klines[-1].get("data_source", "unknown"),
        "stock_code": c,
        "strategy": strategy,
        "start_date": dates[start_idx],
        "end_date": dates[-1],
        "total_trading_days": len(dates) - start_idx,
        "initial_capital": initial_cash,
        "final_capital": round(final_equity, 2),
        "total_return": f"{round(total_return_pct, 2)}%",
        "benchmark_buy_and_hold_return": f"{round(bench_return_pct, 2)}%",
        "alpha": f"{round(total_return_pct - bench_return_pct, 2)}%",
        "max_drawdown": f"{round(max_drawdown, 2)}%",
        "win_rate": f"{round(win_rate, 1)}%",
        "total_trades": total_round_trips,
        "recent_trades": trades[-8:],
        "research_only": True,
        "limitations": "简化日线回测，未覆盖涨跌停成交约束、完整税费、滑点、停牌及幸存者偏差；历史表现不代表未来。",
        "summary": f"回测区间 {dates[start_idx]} ~ {dates[-1]}，策略总收益率【{round(total_return_pct, 2)}%】（基准买入持有【{round(bench_return_pct, 2)}%】），Alpha 超额收益【{round(total_return_pct - bench_return_pct, 2)}%】，最大回撤【{round(max_drawdown, 2)}%】，交易胜率【{round(win_rate, 1)}%】。",
    }


# ==========================================
# Tool 4: 宏观大盘与复盘 (Market Review)
# ==========================================
@mcp.tool()
def get_market_review() -> Dict[str, Any]:
    """
    获取 A 股大盘宏观行情与全市场复盘数据（上证指数、深证成指、创业板指、科创50、沪深300点位与成交额、全市场涨跌统计与多空情绪）。
    """
    index_symbols = [
        {"code": "000001", "name": "上证指数", "market": "sh"},
        {"code": "399001", "name": "深证成指", "market": "sz"},
        {"code": "399006", "name": "创业板指", "market": "sz"},
        {"code": "000300", "name": "沪深300", "market": "sh"},
        {"code": "000688", "name": "科创50", "market": "sh"},
    ]
    quotes = _fetch_batch_quotes(index_symbols)
    total_amount_yi = sum(q.get("amount_wan", 0) / 10000.0 for q in quotes if q["code"] in ["000001", "399001"])

    indices_data = []
    for q in quotes:
        indices_data.append(
            {
                "name": q["name"],
                "code": q["code"],
                "price": q["price"],
                "pct_chg": f"{q['pct_chg']}%",
                "amount_yi": f"{round(q.get('amount_wan', 0) / 10000.0, 1)}亿",
            }
        )

    # Sample market breadth using top stocks
    sample_pool = _get_a_share_pool()[:200]
    sample_quotes = _fetch_batch_quotes(sample_pool)
    up_count = sum(1 for q in sample_quotes if q.get("pct_chg", 0) > 0)
    down_count = sum(1 for q in sample_quotes if q.get("pct_chg", 0) < 0)
    flat_count = len(sample_quotes) - up_count - down_count

    sentiment = "多头强势" if up_count > down_count * 1.5 else ("空头偏弱" if down_count > up_count * 1.5 else "震荡分化")

    return {
        "status": "success",
        "data_source": quotes[0].get("data_source", "unknown") if quotes else "unknown",
        "market_sentiment": sentiment,
        "sh_sz_total_amount_yi": f"{round(total_amount_yi, 1)}亿",
        "indices": indices_data,
        "market_breadth_sample": {
            "sample_size": len(sample_quotes),
            "up_count": up_count,
            "down_count": down_count,
            "flat_count": flat_count,
        },
        "summary": f"A股主要指数呈现【{sentiment}】，沪深两市合计成交约【{round(total_amount_yi, 1)}亿元】。样本个股上涨 {up_count} 家，下跌 {down_count} 家。",
    }


# ==========================================
# Tool 5: 自选股与持仓管理 (Portfolio & Watchlist)
# ==========================================
@mcp.tool()
def manage_portfolio(
    action: str = "list_all",
    target_type: str = "watchlist",
    stock_code: Optional[str] = None,
    cost_price: Optional[float] = None,
    shares: Optional[int] = None,
    group_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    管理本地自选股与持仓组合，并实时计算最新盈亏与市值。

    Args:
        action: 操作类型:
            - 'list_all': 查看所有自选股与持仓明细（含最新实时价格与盈亏计算）
            - 'add_watchlist': 添加股票到自选列表 (需 stock_code)
            - 'remove_watchlist': 从自选列表中移除 (需 stock_code)
            - 'add_position': 添加/更新持仓 (需 stock_code, cost_price, shares)
            - 'remove_position': 移除/清仓持仓 (需 stock_code)
        target_type: 'watchlist' (自选) 或 'position' (持仓)
        stock_code: 股票代码（如 '600519' 或 '000001'）
        cost_price: 持仓成本价（元）
        shares: 持仓股数（股）
        group_name: 分组名称（可选，默认 '默认自选' / '默认持仓'）
    """
    _init_portfolio_db()
    with sqlite3.connect(PORTFOLIO_DB_PATH) as conn:
        cursor = conn.cursor()

        if action == "add_watchlist" and stock_code:
            mkt, c = _clean_code(stock_code)
            q = _fetch_batch_quotes([{"code": c, "market": mkt, "name": c}])
            name = q[0]["name"] if q else c
            grp = group_name or "默认自选"
            cursor.execute(
                "INSERT OR REPLACE INTO watchlist (code, name, group_name) VALUES (?, ?, ?)",
                (c, name, grp),
            )
            conn.commit()
            return {"status": "success", "message": f"已成功添加 {name}({c}) 到自选分组【{grp}】"}

        elif action == "remove_watchlist" and stock_code:
            mkt, c = _clean_code(stock_code)
            cursor.execute("DELETE FROM watchlist WHERE code = ?", (c,))
            conn.commit()
            return {"status": "success", "message": f"已从自选股中移除 {c}"}

        elif action == "add_position" and stock_code:
            if cost_price is None or shares is None:
                return {"status": "error", "message": "添加持仓必须提供 cost_price (成本价) 和 shares (股数)"}
            mkt, c = _clean_code(stock_code)
            q = _fetch_batch_quotes([{"code": c, "market": mkt, "name": c}])
            name = q[0]["name"] if q else c
            grp = group_name or "默认持仓"
            cursor.execute(
                "INSERT OR REPLACE INTO positions (code, name, cost_price, shares, group_name) VALUES (?, ?, ?, ?, ?)",
                (c, name, cost_price, shares, grp),
            )
            conn.commit()
            return {"status": "success", "message": f"已成功记录持仓 {name}({c}): 成本 {cost_price}元, 数量 {shares}股"}

        elif action == "remove_position" and stock_code:
            mkt, c = _clean_code(stock_code)
            cursor.execute("DELETE FROM positions WHERE code = ?", (c,))
            conn.commit()
            return {"status": "success", "message": f"已成功清空持仓 {c}"}

        else:
            # list_all
            cursor.execute("SELECT code, name, group_name, added_at FROM watchlist")
            wl_rows = cursor.fetchall()
            cursor.execute("SELECT code, name, cost_price, shares, group_name, updated_at FROM positions")
            pos_rows = cursor.fetchall()

            # Batch fetch latest quotes for watchlist & positions
            all_codes = list(set([r[0] for r in wl_rows] + [r[0] for r in pos_rows]))
            quote_map = {}
            if all_codes:
                q_list = [{"code": c, "market": "sh" if c.startswith("6") else "sz", "name": c} for c in all_codes]
                live_quotes = _fetch_batch_quotes(q_list)
                quote_map = {q["code"]: q for q in live_quotes}

            watchlist_res = []
            for r in wl_rows:
                code, name, grp, added_at = r
                lq = quote_map.get(code, {})
                watchlist_res.append(
                    {
                        "code": code,
                        "name": lq.get("name", name),
                        "price": lq.get("price", 0.0),
                        "pct_chg": f"{lq.get('pct_chg', 0.0)}%",
                        "pe_ttm": lq.get("pe_ttm", 0.0),
                        "group": grp,
                    }
                )

            positions_res = []
            total_market_val = 0.0
            total_cost_val = 0.0
            for r in pos_rows:
                code, name, cost_p, num_shares, grp, updated_at = r
                lq = quote_map.get(code, {})
                cur_p = lq.get("price", cost_p)
                mkt_val = cur_p * num_shares
                cost_val = cost_p * num_shares
                pnl_val = mkt_val - cost_val
                pnl_pct = (pnl_val / cost_val * 100.0) if cost_val > 0 else 0.0

                total_market_val += mkt_val
                total_cost_val += cost_val

                positions_res.append(
                    {
                        "code": code,
                        "name": lq.get("name", name),
                        "cost_price": cost_p,
                        "current_price": cur_p,
                        "shares": num_shares,
                        "market_value": round(mkt_val, 2),
                        "pnl_amount": round(pnl_val, 2),
                        "pnl_pct": f"{round(pnl_pct, 2)}%",
                        "group": grp,
                    }
                )

            total_pnl = total_market_val - total_cost_val
            total_pnl_pct = (total_pnl / total_cost_val * 100.0) if total_cost_val > 0 else 0.0

            return {
                "status": "success",
                "watchlist_count": len(watchlist_res),
                "watchlist": watchlist_res,
                "positions_count": len(positions_res),
                "portfolio_summary": {
                    "total_market_value": round(total_market_val, 2),
                    "total_cost_value": round(total_cost_val, 2),
                    "total_pnl_amount": round(total_pnl, 2),
                    "total_pnl_pct": f"{round(total_pnl_pct, 2)}%",
                },
                "positions": positions_res,
            }


# ==========================================
# Tool 6: 价格与异动预警规则 (Alerts)
# ==========================================
@mcp.tool()
def manage_alerts(
    action: str = "list",
    stock_code: Optional[str] = None,
    rule_type: str = "price_above",
    threshold: Optional[float] = None,
    rule_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    管理股票价格监控与异动提醒规则（突破压力位预警、跌破止损位预警、涨跌幅异动监控）。

    Args:
        action: 'list' (查看当前所有预警及触发状态), 'create' (新增监控规则), 'delete' (删除规则)
        stock_code: 股票代码（如 '600519'）
        rule_type: 规则类型:
            - 'price_above': 股价突破/高于某价格
            - 'price_below': 股价跌破/低于某价格
            - 'pct_chg_above': 当日涨幅超过某百分比（如 5.0 代表涨超5%）
            - 'pct_chg_below': 当日跌幅超过某百分比（如 -4.0 代表跌超4%）
        threshold: 触发数值阈值
        rule_id: 规则 ID（删除时需要）
    """
    _init_portfolio_db()
    with sqlite3.connect(PORTFOLIO_DB_PATH) as conn:
        cursor = conn.cursor()

        if action == "create" and stock_code and threshold is not None:
            mkt, c = _clean_code(stock_code)
            q = _fetch_batch_quotes([{"code": c, "market": mkt, "name": c}])
            name = q[0]["name"] if q else c
            cursor.execute(
                "INSERT INTO alert_rules (code, name, rule_type, threshold, status) VALUES (?, ?, ?, ?, 'active')",
                (c, name, rule_type, threshold),
            )
            conn.commit()
            return {"status": "success", "message": f"已成功为 {name}({c}) 创建预警规则：当【{rule_type} {threshold}】时触发提醒"}

        elif action == "delete" and rule_id:
            cursor.execute("DELETE FROM alert_rules WHERE id = ?", (rule_id,))
            conn.commit()
            return {"status": "success", "message": f"已删除规则 ID {rule_id}"}

        else:
            # list and evaluate
            cursor.execute("SELECT id, code, name, rule_type, threshold, status, created_at FROM alert_rules")
            rows = cursor.fetchall()
            if not rows:
                return {"status": "success", "count": 0, "alerts": []}

            codes = list(set([r[1] for r in rows]))
            q_list = [{"code": c, "market": "sh" if c.startswith("6") else "sz", "name": c} for c in codes]
            live_quotes = _fetch_batch_quotes(q_list)
            q_map = {q["code"]: q for q in live_quotes}

            results = []
            for r in rows:
                rid, c, name, rtype, thresh, st, created = r
                lq = q_map.get(c, {})
                cur_p = lq.get("price", 0.0)
                cur_pct = lq.get("pct_chg", 0.0)

                triggered = False
                trigger_msg = ""
                if rtype == "price_above" and cur_p >= thresh:
                    triggered = True
                    trigger_msg = f"当前价 {cur_p} 已突破设定目标价 {thresh}"
                elif rtype == "price_below" and cur_p <= thresh:
                    triggered = True
                    trigger_msg = f"当前价 {cur_p} 已跌破设定止损价 {thresh}"
                elif rtype == "pct_chg_above" and cur_pct >= thresh:
                    triggered = True
                    trigger_msg = f"当前涨幅 {cur_pct}% 已超过设定阈值 {thresh}%"
                elif rtype == "pct_chg_below" and cur_pct <= thresh:
                    triggered = True
                    trigger_msg = f"当前跌幅 {cur_pct}% 已跌超设定阈值 {thresh}%"

                results.append(
                    {
                        "id": rid,
                        "code": c,
                        "name": lq.get("name", name),
                        "rule_type": rtype,
                        "threshold": thresh,
                        "current_price": cur_p,
                        "current_pct_chg": f"{cur_pct}%",
                        "triggered": triggered,
                        "trigger_message": trigger_msg if triggered else "未触发 (监控中)",
                    }
                )

            return {"status": "success", "count": len(results), "alerts": results}


# ==========================================
# Tool 7: 深度 AI 投研报告与问股 (Deep AI Analysis)
# ==========================================
@mcp.tool()
def generate_ai_report(
    stock_code: str,
    report_type: str = "detailed",
    async_mode: bool = False,
) -> Dict[str, Any]:
    """
    触发本地 DSA 大模型投研分析引擎，生成深度个股研究决策报告（包含基本面评分、风险排查、操作战术点位与核心逻辑）。

    Args:
        stock_code: 股票代码（如 '600519', 'AAPL', 'hk00700'）
        report_type: 报告类型 ('detailed' 完整深度报告, 'simple' 简版, 'brief' 摘要)
        async_mode: 是否异步提交。若为 True 则立即返回 task_id；若为 False 则同步等待完成（通常需 1~3 分钟）。
    """
    mkt, c = _clean_code(stock_code)
    code = stock_code.strip()
    if not (code.startswith("hk") or code.isupper()):
        code = c

    safe_base_url, validation_error = _validated_dsa_base_url()
    if validation_error:
        return {"status": "error", "message": f"DSA 连接已阻止: {validation_error}"}

    cookie = _get_dsa_cookie()
    headers = {"Content-Type": "application/json"}
    if cookie:
        headers["Cookie"] = f"dsa_session={cookie}"

    url = f"{safe_base_url}/api/v1/analysis/analyze"
    payload = json.dumps(
        {
            "stock_code": code,
            "report_type": report_type,
            "force_refresh": False,
            "async_mode": async_mode,
        }
    ).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=payload, headers=headers)
        timeout = 10 if async_mode else 300
        with urllib.request.urlopen(req, timeout=timeout) as res:
            data = json.loads(res.read().decode("utf-8"))
            return {"status": "success", "result": data}
    except Exception as e:
        logger.error(f"Failed to trigger AI report: {e}")
        return {
            "status": "error",
            "message": f"触发本地 DSA AI 分析失败: {e}。请确认本地 dsa-webui 服务（端口 8000）是否正常运行。",
        }


# ==========================================
# Tool 8: ML 短期方向预测 (Walk-forward RF+GB)
# ==========================================
@mcp.tool()
def predict_stock(codes: List[str], force: bool = False) -> Dict[str, Any]:
    """
    基于严格 walk-forward 机器学习的 A 股未来 5 个交易日方向预测（RandomForest + GradientBoosting 集成）。

    Args:
        codes: 股票代码列表，支持 '600519'、'600519.SH'、'sh600519' 等格式
        force: 是否强制重新拉取数据并训练（默认 False，同代码命中内存缓存）

    Returns:
        每只股票的上涨概率、样本外准确率与方向判断。首次训练约 1-2 分钟/股。
        输出为统计信号，非投资建议。
    """
    results = []
    for code in codes:
        try:
            results.append(_predict_symbol(code, force=force))
        except Exception as exc:
            target = _to_exchange_code(code)
            results.append({
                "code": target,
                "status": "error",
                "message": f"预测失败: {type(exc).__name__}: {exc}",
            })
    ok = [r for r in results if r.get("status") == "success"]
    return {
        "status": "success" if ok else "error",
        "count": len(results),
        "predictions": results,
        "summary": "\n".join(r.get("summary", r.get("message", "")) for r in results),
        "disclaimer": "统计方向信号，非投资建议（OOS 准确率通常约 55-60%）",
    }


def predict_cache_status() -> Dict[str, Any]:
    """查看当前已缓存的 ML 预测结果（无网络请求）。"""
    if not _PREDICT_CACHE:
        return {"status": "success", "cached_count": 0, "cached": []}
    cached = [
        {"code": k, "verdict": v.get("verdict"), "up_probability": v.get("up_probability"), "summary": v.get("summary")}
        for k, v in _PREDICT_CACHE.items()
    ]
    return {"status": "success", "cached_count": len(cached), "cached": cached}


# ==========================================
# Tool 9: 策略清单
# ==========================================
def get_strategies() -> Dict[str, Any]:
    """获取所有支持的选股与回测策略清单及说明。"""
    return {
        "screening_strategies": [
            {"id": "bull_momentum", "name": "多头突破动量策略", "desc": "均线多头、换手充分、量价齐升主升浪"},
            {"id": "low_valuation_value", "name": "低估值价值/高股息策略", "desc": "低PE/PB、大市值稳健白马资产"},
            {"id": "volume_breakout", "name": "量比异动突破策略", "desc": "量比明显放大、主力进场起涨点"},
            {"id": "growth_tech", "name": "科技成长高弹性龙头策略", "desc": "科技成长中盘龙头，高弹性"},
            {"id": "oversold_rebound", "name": "超跌反弹低吸策略", "desc": "底部温和放量企稳修复"},
            {"id": "book_volume_turnover", "name": "量比换手观察模板", "desc": "换手>=3%、量比>=1.5%；仅应用当前可得字段"},
            {"id": "volume_ratio_watch", "name": "强量比观察模板", "desc": "量比>2、换手1%~5%；用于候选初筛，不是买卖信号"},
        ],
        "backtest_strategies": [
            {"id": "sma_cross", "name": "双均线金叉策略 (MA5/MA20)", "desc": "经典顺势均线交叉，金叉买入死叉卖出"},
            {"id": "momentum_breakout", "name": "动量突破策略 (20日新高)", "desc": "突破20日最高价进场，跌破10日线离场"},
            {"id": "rsi_mean_reversion", "name": "RSI 均值回归策略", "desc": "RSI超卖低吸，RSI超买止盈"},
            {"id": "ma_5_10_60_trend", "name": "MA5/10/60 趋势过滤研究", "desc": "以三均线顺序作为历史趋势过滤，日线简化回测"},
            {"id": "macd_cross_trend", "name": "MACD 交叉趋势研究", "desc": "DIF/DEA 金叉结合MA20过滤，死叉退出的日线简化回测"},
        ],
    }


# ==========================================
# Tool 10: 数据源与安全状态
# ==========================================
def get_data_provider_status(verify_connection: bool = False) -> Dict[str, Any]:
    """
    查看当前行情数据源、同花顺授权和 DSA 安全状态；不会返回任何密钥。

    Args:
        verify_connection: 为 True 时仅验证同花顺 access token 获取，不拉取行情数据。
    """
    credentials_configured = bool(THS_REFRESH_TOKEN or THS_ACCESS_TOKEN)
    if STOCK_DATA_PROVIDER == "tencent":
        active_provider = "tencent-public"
    elif credentials_configured:
        active_provider = "tonghuashun-ifind"
    elif STOCK_DATA_PROVIDER == "ths":
        active_provider = "unavailable-missing-ths-token"
    else:
        active_provider = "tencent-public-auto-fallback"

    connection = "not_checked"
    if verify_connection:
        if not credentials_configured:
            connection = "missing_credentials"
        else:
            try:
                connection = "ok" if _get_ths_access_token(force_refresh=True) else "failed"
            except Exception as exc:
                connection = f"failed: {type(exc).__name__}: {exc}"

    _, dsa_error = _validated_dsa_base_url()
    return {
        "status": "success",
        "configured_provider": STOCK_DATA_PROVIDER,
        "active_provider": active_provider,
        "tonghuashun": {
            "official_api": THS_API_BASE_URL,
            "credentials_configured": credentials_configured,
            "connection": connection,
        },
        "dsa": {
            "url_scope": "blocked" if dsa_error else "allowed",
            "password_configured": bool(DSA_PASSWORD),
            "validation_error": dsa_error,
        },
    }


# ==========================================
# Tool 11: AI4Trade read-only integration
# ==========================================
def get_ai4trade_status() -> Dict[str, Any]:
    """查看 AI4Trade 集成状态，不返回 token 或其他凭据。"""
    return {
        "status": "success",
        "api_base": AI4TRADE_API_BASE_URL,
        "token_configured": bool(AI4TRADE_TOKEN),
        "safety": {
            "fixed_api_host": True,
            "persistent_monitoring": False,
            "automatic_copy_trading": False,
            "credential_tool_arguments_allowed": False,
        },
    }


def get_ai4trade_signal_feed(
    limit: int = 20,
    message_type: Optional[str] = None,
    symbol: Optional[str] = None,
    keyword: Optional[str] = None,
    sort: str = "new",
) -> Dict[str, Any]:
    """读取 AI4Trade 信号流；仅查询，不会关注、发布或下单。"""
    if not 1 <= limit <= 100:
        return {"status": "error", "message": "limit must be between 1 and 100"}
    if message_type is not None and message_type not in {"operation", "strategy", "discussion"}:
        return {"status": "error", "message": "message_type must be operation, strategy, or discussion"}
    if sort not in {"new", "active", "following"}:
        return {"status": "error", "message": "sort must be new, active, or following"}
    if sort == "following" and not AI4TRADE_TOKEN:
        return {"status": "error", "message": "sort=following requires AI4TRADE_TOKEN"}
    return _ai4trade_request(
        "GET",
        "/signals/feed",
        query={"limit": limit, "message_type": message_type, "symbol": symbol, "keyword": keyword, "sort": sort},
    )


def get_ai4trade_market_intel(
    view: str = "overview",
    symbol: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 10,
) -> Dict[str, Any]:
    """读取 AI4Trade 金融事件板、宏观信号、ETF 流或单股快照。"""
    if not 1 <= limit <= 50:
        return {"status": "error", "message": "limit must be between 1 and 50"}
    allowed_views = {"overview", "macro-signals", "etf-flows", "featured-stocks", "stock-latest", "stock-history", "news"}
    if view not in allowed_views:
        return {"status": "error", "message": f"view must be one of {sorted(allowed_views)}"}
    if view in {"stock-latest", "stock-history"}:
        if not symbol or not re.fullmatch(r"[A-Za-z0-9._-]{1,48}", symbol):
            return {"status": "error", "message": "stock-latest and stock-history require a safe symbol"}
        suffix = "latest" if view == "stock-latest" else "history"
        return _ai4trade_request("GET", f"/market-intel/stocks/{symbol}/{suffix}", query={"limit": limit})
    path_map = {
        "overview": "/market-intel/overview",
        "macro-signals": "/market-intel/macro-signals",
        "etf-flows": "/market-intel/etf-flows",
        "featured-stocks": "/market-intel/stocks/featured",
        "news": "/market-intel/news",
    }
    return _ai4trade_request("GET", path_map[view], query={"category": category, "limit": limit})


def get_ai4trade_polymarket_market(
    slug: Optional[str] = None,
    condition_id: Optional[str] = None,
    token_id: Optional[str] = None,
) -> Dict[str, Any]:
    """读取 Polymarket 公开市场元数据或订单簿，不经过 AI4Trade 且不交易。"""
    chosen = [value for value in (slug, condition_id, token_id) if value]
    if len(chosen) != 1:
        return {"status": "error", "message": "provide exactly one of slug, condition_id, or token_id"}
    if slug:
        if not re.fullmatch(r"[a-z0-9-]{1,160}", slug):
            return {"status": "error", "message": "invalid Polymarket slug"}
        url = f"https://gamma-api.polymarket.com/markets?{urlencode({'slug': slug})}"
    elif condition_id:
        if not re.fullmatch(r"0x[a-fA-F0-9]{1,128}", condition_id):
            return {"status": "error", "message": "invalid condition_id"}
        url = f"https://gamma-api.polymarket.com/markets?{urlencode({'conditionId': condition_id})}"
    else:
        if not re.fullmatch(r"[0-9]{1,128}", token_id or ""):
            return {"status": "error", "message": "invalid token_id"}
        url = f"https://clob.polymarket.com/book?{urlencode({'token_id': token_id})}"
    try:
        request = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(request, timeout=20) as response:
            return {
                "status": "success",
                "source": "polymarket-public-api",
                "untrusted_external_data": True,
                "data": json.loads(response.read().decode("utf-8")),
            }
    except urllib.error.HTTPError as exc:
        return {"status": "error", "message": f"Polymarket request failed (HTTP {exc.code})"}
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {"status": "error", "message": f"Polymarket request failed: {type(exc).__name__}"}


def get_ai4trade_account() -> Dict[str, Any]:
    """读取已配置 AI4Trade 账户资料和模拟资金；不会返回 token。"""
    return _ai4trade_request("GET", "/claw/agents/me", requires_auth=True)


def get_ai4trade_positions() -> Dict[str, Any]:
    """读取 AI4Trade 模拟账户的自有和已复制持仓。"""
    return _ai4trade_request("GET", "/positions", requires_auth=True)


def get_ai4trade_following() -> Dict[str, Any]:
    """读取当前 AI4Trade 关注列表；不会修改关注关系。"""
    return _ai4trade_request("GET", "/signals/following", requires_auth=True)


# ==========================================
# Tool 12: AI4Trade explicitly confirmed mutations
# ==========================================
def manage_ai4trade_follow(leader_id: int, action: str = "follow", confirm: bool = False) -> Dict[str, Any]:
    """关注或取消关注 AI4Trade 信号提供者；必须先取得针对该 leader 的明确同意。"""
    if leader_id <= 0 or action not in {"follow", "unfollow"}:
        return {"status": "error", "message": "leader_id must be positive and action must be follow or unfollow"}
    blocked = _require_ai4trade_confirmation(f"AI4Trade {action} for leader_id={leader_id}", confirm)
    if blocked:
        return blocked
    return _ai4trade_request("POST", f"/signals/{action}", payload={"leader_id": leader_id}, requires_auth=True)


def publish_ai4trade_strategy(
    market: str,
    title: str,
    content: str,
    symbols: List[str],
    tags: Optional[List[str]] = None,
    confirm: bool = False,
) -> Dict[str, Any]:
    """发布 AI4Trade 策略文章；必须先确认文本、市场和标的。"""
    if not market or not title.strip() or not content.strip() or not symbols:
        return {"status": "error", "message": "market, title, content, and at least one symbol are required"}
    blocked = _require_ai4trade_confirmation("publishing an AI4Trade strategy", confirm)
    if blocked:
        return blocked
    payload = {"market": market, "title": title.strip(), "content": content.strip(), "symbols": symbols, "tags": tags or []}
    return _ai4trade_request("POST", "/signals/strategy", payload=payload, requires_auth=True)


def publish_ai4trade_discussion(
    title: str,
    content: str,
    tags: Optional[List[str]] = None,
    confirm: bool = False,
) -> Dict[str, Any]:
    """发布 AI4Trade 讨论；必须先确认完整文本和标签。"""
    if not title.strip() or not content.strip():
        return {"status": "error", "message": "title and content are required"}
    blocked = _require_ai4trade_confirmation("publishing an AI4Trade discussion", confirm)
    if blocked:
        return blocked
    return _ai4trade_request(
        "POST",
        "/signals/discussion",
        payload={"title": title.strip(), "content": content.strip(), "tags": tags or []},
        requires_auth=True,
    )


def manage_ai4trade_reply(
    signal_id: int,
    content: str,
    action: str = "create",
    reply_id: Optional[int] = None,
    confirm: bool = False,
) -> Dict[str, Any]:
    """创建或接受 AI4Trade 回复；两种操作均需明确确认。"""
    if signal_id <= 0 or action not in {"create", "accept"}:
        return {"status": "error", "message": "signal_id must be positive and action must be create or accept"}
    if action == "create" and not content.strip():
        return {"status": "error", "message": "content is required when creating a reply"}
    if action == "accept" and (reply_id is None or reply_id <= 0):
        return {"status": "error", "message": "a positive reply_id is required when accepting a reply"}
    blocked = _require_ai4trade_confirmation(f"AI4Trade reply action={action} for signal_id={signal_id}", confirm)
    if blocked:
        return blocked
    if action == "create":
        return _ai4trade_request(
            "POST", "/signals/reply", payload={"signal_id": signal_id, "content": content.strip()}, requires_auth=True
        )
    return _ai4trade_request("POST", f"/signals/{signal_id}/replies/{reply_id}/accept", payload={}, requires_auth=True)


def exchange_ai4trade_points(amount: int, confirm: bool = False) -> Dict[str, Any]:
    """将 AI4Trade 积分兑换为模拟资金；积分扣减不可逆，必须明确确认。"""
    if amount <= 0:
        return {"status": "error", "message": "amount must be positive"}
    blocked = _require_ai4trade_confirmation(f"exchanging {amount} AI4Trade points for simulated cash", confirm)
    if blocked:
        return blocked
    return _ai4trade_request("POST", "/agents/points/exchange", payload={"amount": amount}, requires_auth=True)


def publish_ai4trade_realtime_signal(
    market: str,
    action: str,
    symbol: str,
    price: float,
    quantity: float,
    executed_at: str,
    content: Optional[str] = None,
    outcome: Optional[str] = None,
    token_id: Optional[str] = None,
    confirm: bool = False,
) -> Dict[str, Any]:
    """发布 AI4Trade 实时模拟信号；不会触达真实券商，但可能影响跟随者。"""
    if market not in {"us-stock", "crypto", "polymarket"} or action not in {"buy", "sell", "short", "cover"}:
        return {"status": "error", "message": "invalid market or action"}
    if market == "polymarket" and action not in {"buy", "sell"}:
        return {"status": "error", "message": "Polymarket supports only buy or sell"}
    if not symbol.strip() or quantity <= 0 or price < 0 or not executed_at.strip():
        return {"status": "error", "message": "symbol, positive quantity, non-negative price, and executed_at are required"}
    blocked = _require_ai4trade_confirmation(
        f"publishing AI4Trade {market} {action} signal for {symbol} at price={price}, quantity={quantity}", confirm
    )
    if blocked:
        return blocked
    payload = {
        "market": market,
        "action": action,
        "symbol": symbol.strip(),
        "price": price,
        "quantity": quantity,
        "executed_at": executed_at.strip(),
    }
    if content:
        payload["content"] = content
    if outcome:
        payload["outcome"] = outcome
    if token_id:
        payload["token_id"] = token_id
    return _ai4trade_request("POST", "/signals/realtime", payload=payload, requires_auth=True)


def get_ai4trade_heartbeat_once(confirm: bool = False) -> Dict[str, Any]:
    """读取一次 AI4Trade 通知；该接口会标记已返回消息为已读，必须确认。"""
    blocked = _require_ai4trade_confirmation("reading and marking AI4Trade heartbeat messages", confirm)
    if blocked:
        return blocked
    return _ai4trade_request("POST", "/claw/agents/heartbeat", payload={}, requires_auth=True)


def run_vibe_trading_research(
    prompt: str,
    confirm_external_ai: bool = False,
    max_iterations: int = 6,
    timeout_seconds: int = 600,
) -> Dict[str, Any]:
    """通过已安装的 Vibe-Trading 执行一次研究或回测提示词；禁止实盘交易和后台调度。"""
    blocked = _require_research_only(prompt)
    if blocked:
        return blocked
    confirmation = _require_external_ai_confirmation("Vibe-Trading 研究", confirm_external_ai)
    if confirmation:
        return confirmation
    if not 1 <= max_iterations <= 12 or not 30 <= timeout_seconds <= 1200:
        return {"status": "error", "message": "max_iterations must be 1-12 and timeout_seconds must be 30-1200"}
    command = _vibe_trading_command()
    if not command:
        return {"status": "error", "message": "未找到 vibe-trading 命令；请先安装 vibe-trading-ai。"}
    guarded_prompt = (
        "Research-only request. Do not select or use broker connectors, place orders, or schedule background jobs. "
        "Return assumptions, data limitations, methodology, and backtest caveats.\n\n"
        + prompt.strip()
    )
    result = _run_research_backend(
        [command, "run", "--json", "--no-rich", "--max-iter", str(max_iterations), "-p", guarded_prompt],
        timeout_seconds,
    )
    result.update(
        {
            "backend": "HKUDS/Vibe-Trading",
            "mode": "one-shot research/backtest",
            "research_only": True,
            "disclaimer": "远端模型和市场数据返回均为不可信外部数据；请独立核验，不构成投资建议。",
        }
    )
    return result


_VIBE_ALPHA_ZOOS = frozenset({"academic", "alpha101", "fundamental", "gtja191", "qlib158"})
_VIBE_ALPHA_UNIVERSES = frozenset({"csi300", "sp500", "btc-usdt"})
_VIBE_ALPHA_PERIOD = re.compile(r"^(?:\d{4}-\d{4}|\d{4}-\d{2}-\d{2}/\d{4}-\d{2}-\d{2})$")
_VIBE_ALPHA_ID = re.compile(r"^[a-z][a-z0-9_]{2,79}$")
_VIBE_ALPHA_THEME = re.compile(r"^[a-z][a-z0-9_-]{1,63}$")


def run_vibe_factor_research(
    action: str = "benchmark",
    zoo: Optional[str] = None,
    universe: str = "csi300",
    period: Optional[str] = None,
    top_n: int = 20,
    factor_id: Optional[str] = None,
    theme: Optional[str] = None,
    limit: int = 50,
    timeout_seconds: int = 900,
) -> Dict[str, Any]:
    """Run fixed Alpha Zoo commands without an LLM, chat session, or broker access."""
    if action not in {"benchmark", "list", "show"}:
        return {"status": "error", "message": "action must be benchmark, list, or show"}
    if universe not in _VIBE_ALPHA_UNIVERSES:
        return {"status": "error", "message": f"universe must be one of {sorted(_VIBE_ALPHA_UNIVERSES)}"}
    if not 1 <= timeout_seconds <= 1200:
        return {"status": "error", "message": "timeout_seconds must be between 1 and 1200"}

    command = _vibe_trading_command()
    if not command:
        return {"status": "error", "message": "未找到 vibe-trading 命令；请先运行 scripts/bootstrap_vibe_trading.py。"}

    if action == "benchmark":
        if zoo not in _VIBE_ALPHA_ZOOS:
            return {"status": "error", "message": f"zoo must be one of {sorted(_VIBE_ALPHA_ZOOS)}"}
        if not period or not _VIBE_ALPHA_PERIOD.fullmatch(period):
            return {"status": "error", "message": "period must be YYYY-YYYY or YYYY-MM-DD/YYYY-MM-DD"}
        if not 1 <= top_n <= 100:
            return {"status": "error", "message": "top_n must be between 1 and 100"}
        args = [command, "alpha", "bench", "--zoo", zoo, "--universe", universe, "--period", period, "--top", str(top_n)]
    elif action == "list":
        if zoo is not None and zoo not in _VIBE_ALPHA_ZOOS:
            return {"status": "error", "message": f"zoo must be one of {sorted(_VIBE_ALPHA_ZOOS)}"}
        if theme is not None and not _VIBE_ALPHA_THEME.fullmatch(theme):
            return {"status": "error", "message": "theme must contain only lowercase letters, digits, _ or -"}
        if not 1 <= limit <= 100:
            return {"status": "error", "message": "limit must be between 1 and 100"}
        args = [command, "alpha", "list", "--universe", universe, "--limit", str(limit), "--json"]
        if zoo:
            args.extend(["--zoo", zoo])
        if theme:
            args.extend(["--theme", theme])
    else:
        if not factor_id or not _VIBE_ALPHA_ID.fullmatch(factor_id):
            return {"status": "error", "message": "factor_id must be a registered lowercase Alpha Zoo id"}
        args = [command, "alpha", "show", factor_id, "--brief"]

    result = _run_research_backend(args, timeout_seconds)
    result.update(
        {
            "backend": "HKUDS/Vibe-Trading Alpha Zoo",
            "operation": action,
            "research_only": True,
            "no_llm": True,
            "no_broker_orders": True,
            "disclaimer": "因子评价与回测依赖外部行情及历史样本；不构成投资建议，历史表现不代表未来。",
        }
    )
    return result


def run_vibe_trading_swarm(
    preset: str,
    topic: str,
    confirm_external_ai: bool = False,
    timeout_seconds: int = 900,
) -> Dict[str, Any]:
    """执行受限的 Vibe-Trading 多智能体投研团队；只允许研究类预设，不接入券商。"""
    allowed_presets = {
        "investment_committee",
        "quant_strategy_desk",
        "global_equities_desk",
        "earnings_research_desk",
        "macro_rates_fx_desk",
    }
    if preset not in allowed_presets:
        return {"status": "error", "message": f"preset must be one of {sorted(allowed_presets)}"}
    blocked = _require_research_only(topic)
    if blocked:
        return blocked
    confirmation = _require_external_ai_confirmation("Vibe-Trading 多智能体投研", confirm_external_ai)
    if confirmation:
        return confirmation
    if not 60 <= timeout_seconds <= 1800:
        return {"status": "error", "message": "timeout_seconds must be between 60 and 1800"}
    command = _vibe_trading_command()
    if not command:
        return {"status": "error", "message": "未找到 vibe-trading 命令；请先安装 vibe-trading-ai。"}
    # Each upstream preset has a different variable schema.  Map the single
    # MCP topic into its complete, non-secret required schema so a run does not
    # fail on an unresolved template variable.
    topic_text = topic.strip()
    payload_by_preset = {
        "investment_committee": {"target": topic_text, "market": "A-share / global market as applicable"},
        "quant_strategy_desk": {"goal": topic_text, "market": "A-share"},
        "global_equities_desk": {"goal": topic_text, "risk_tolerance": "moderate"},
        "earnings_research_desk": {"target": topic_text},
        "macro_rates_fx_desk": {"goal": topic_text, "timeframe": "3 months"},
    }
    payload = json.dumps(payload_by_preset[preset], ensure_ascii=False)
    result = _run_research_backend([command, "--json", "--no-rich", "--swarm-run", preset, payload], timeout_seconds)
    result.update(
        {
            "backend": "HKUDS/Vibe-Trading",
            "preset": preset,
            "research_only": True,
            "disclaimer": "多智能体结论可能出错或相互矛盾，不能视为下单指令或投资建议。",
        }
    )
    return result


_QUANTAALPHA_FACTOR_SOURCES = frozenset({"alpha158", "alpha158_20", "alpha360", "custom", "combined"})


def _quantaalpha_env() -> Dict[str, str]:
    paths = _quantaalpha_paths()
    environment = _backend_env()
    environment.update(
        {
            "QLIB_DATA_DIR": paths["qlib"],
            "QLIB_PROVIDER_URI": paths["qlib"],
            "DATA_RESULTS_DIR": paths["results"],
            "FACTOR_CACHE_DIR": os.path.join(paths["results"], "factor_cache"),
            "FACTOR_CoSTEER_DATA_FOLDER": paths["factor_full"],
            "FACTOR_CoSTEER_DATA_FOLDER_DEBUG": paths["factor_debug"],
            "FACTOR_CoSTEER_PYTHON_BIN": QUANTAALPHA_PYTHON,
        }
    )
    return environment


def _latest_quantaalpha_factor_library() -> Optional[str]:
    """Select only a generated factor library below the fixed result root."""
    result_root = os.path.realpath(_quantaalpha_paths()["results"])
    if not os.path.isdir(result_root):
        return None
    candidates: List[Tuple[float, str]] = []
    visited = 0
    for root, directories, files in os.walk(result_root):
        directories[:] = [name for name in directories if not name.startswith(".")]
        for filename in files:
            visited += 1
            if visited > 20_000:
                break
            if not re.fullmatch(r"all_factors_library(?:_[A-Za-z0-9_-]+)?\.json", filename):
                continue
            path = os.path.realpath(os.path.join(root, filename))
            if os.path.commonpath([result_root, path]) != result_root:
                continue
            try:
                candidates.append((os.path.getmtime(path), path))
            except OSError:
                continue
        if visited > 20_000:
            break
    return max(candidates)[1] if candidates else None


def _run_quantaalpha_research(
    action: str = "status",
    direction: Optional[str] = None,
    step_n: int = 5,
    factor_source: str = "alpha158_20",
    dry_run: bool = False,
    confirm_external_ai: bool = False,
    timeout_seconds: int = 1800,
) -> Dict[str, Any]:
    """Run a pinned QuantaAlpha mining or backtest job in its isolated runtime."""
    if action == "status":
        return {
            "status": "success",
            "backend": "QuantaAlpha/QuantaAlpha",
            "runtime": _quantaalpha_status(),
            "research_only": True,
            "no_broker_orders": True,
        }
    if action not in {"mine", "backtest"}:
        return {"status": "error", "message": "action must be status, mine, or backtest"}
    if not 60 <= timeout_seconds <= 7200:
        return {"status": "error", "message": "timeout_seconds must be between 60 and 7200"}
    topic = (direction or "").strip()
    if action == "mine":
        blocked = _require_research_only(topic)
        if blocked:
            return blocked
        confirmation = _require_external_ai_confirmation("QuantaAlpha 因子挖掘", confirm_external_ai)
        if confirmation:
            return confirmation
        if not 1 <= step_n <= 25:
            return {"status": "error", "message": "step_n must be between 1 and 25"}
    elif factor_source not in _QUANTAALPHA_FACTOR_SOURCES:
        return {"status": "error", "message": f"factor_source must be one of {sorted(_QUANTAALPHA_FACTOR_SOURCES)}"}

    runtime = _quantaalpha_status()
    python = _quantaalpha_python()
    paths = _quantaalpha_paths()
    if not python or not runtime["package_available"] or not runtime["config_available"]:
        return {
            "status": "error",
            "message": "QuantaAlpha 后端尚未安装；请先运行 scripts/bootstrap_quantaalpha.py。",
            "runtime": runtime,
        }
    if not runtime["qlib_data_available"]:
        return {
            "status": "error",
            "message": "QuantaAlpha 的 Qlib CSI300 数据尚未准备好；请运行 bootstrap_quantaalpha.py --data full。",
            "runtime": runtime,
        }

    environment = _quantaalpha_env()
    os.makedirs(paths["results"], mode=0o700, exist_ok=True)
    config_path = os.path.join(paths["repo"], "configs", "experiment.yaml")
    bridge: Optional[_OpenClawInferenceBridge] = None

    if action == "mine":
        if not runtime["full_factor_data_available"]:
            return {
                "status": "error",
                "message": "完整因子源 daily_pv.h5 尚未安装；正式挖掘需运行 bootstrap_quantaalpha.py --data full。",
                "runtime": runtime,
            }
        if not _openclaw_cli():
            return {"status": "error", "message": "未找到 OpenClaw CLI；无法调用当前默认模型进行因子挖掘。"}
        guarded_direction = (
            "Research-only factor discovery. Do not issue trading instructions or connect to a broker. "
            "Use point-in-time-safe features, document data leakage risks, and require out-of-sample validation.\n\n"
            + topic
        )
        command = [
            python,
            "-m",
            "quantaalpha.cli",
            "mine",
            f"--direction={guarded_direction}",
            f"--step_n={step_n}",
            f"--config_path={config_path}",
        ]
        bridge = _OpenClawInferenceBridge(timeout_seconds=min(timeout_seconds, 300))
        with bridge:
            environment.update(
                {
                    "OPENAI_API_KEY": bridge.token,
                    "OPENAI_BASE_URL": bridge.base_url,
                    "CHAT_MODEL": _OPENCLAW_MODEL_REF,
                    "REASONING_MODEL": _OPENCLAW_MODEL_REF,
                    "CHAT_STREAM": "false",
                    "LOG_LLM_CHAT_CONTENT": "false",
                    "DUMP_CHAT_CACHE": "false",
                    "USE_CHAT_CACHE": "false",
                    "FACTOR_MINING_TIMEOUT": str(timeout_seconds),
                }
            )
            result = _run_research_backend(
                command, timeout_seconds, environment=environment, cwd=paths["results"]
            )
        result.update(
            {
                "backend": "QuantaAlpha/QuantaAlpha",
                "pinned_commit": QUANTAALPHA_COMMIT,
                "operation": "mine",
                "model_provider": "openclaw/default",
                "factor_library": _latest_quantaalpha_factor_library(),
                "results_dir": paths["results"],
                "research_only": True,
                "no_broker_orders": True,
                "disclaimer": "自动挖掘容易产生过拟合和数据泄漏；必须复核样本外、交易成本与稳定性，不构成投资建议。",
            }
        )
        return result

    factor_library = None
    if factor_source in {"custom", "combined"}:
        factor_library = _latest_quantaalpha_factor_library()
        if not factor_library:
            return {"status": "error", "message": "未找到由 QuantaAlpha 生成的 all_factors_library*.json。"}
        confirmation = _require_external_ai_confirmation("QuantaAlpha 自定义因子回测", confirm_external_ai)
        if confirmation:
            return confirmation
    backtest_config = os.path.join(paths["repo"], "configs", "backtest.yaml")
    command = [
        python,
        "-m",
        "quantaalpha.backtest.run_backtest",
        "--config",
        backtest_config,
        "--factor-source",
        factor_source,
    ]
    if factor_library:
        command.extend(["--factor-json", factor_library])
    if dry_run:
        command.append("--dry-run")
    result = _run_research_backend(command, timeout_seconds, environment=environment, cwd=paths["results"])
    result.update(
        {
            "backend": "QuantaAlpha/QuantaAlpha",
            "pinned_commit": QUANTAALPHA_COMMIT,
            "operation": "backtest",
            "factor_source": factor_source,
            "factor_library": factor_library,
            "dry_run": dry_run,
            "results_dir": os.path.join(paths["results"], "data", "results", "backtest_v2_results"),
            "research_only": True,
            "no_broker_orders": True,
            "disclaimer": "历史回测不代表未来表现；需要独立检查幸存者偏差、成本、滑点、停牌和样本外稳定性。",
        }
    )
    return result


def run_tradingagents_research(
    stock_code: str,
    analysis_date: str,
    confirm_external_ai: bool = False,
    llm_provider: str = "openclaw",
    max_debate_rounds: int = 1,
    timeout_seconds: int = 900,
) -> Dict[str, Any]:
    """调用 TradingAgents 的多角色分析、牛熊辩论、风控与组合经理模拟决策；不连接真实交易所。"""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", analysis_date):
        return {"status": "error", "message": "analysis_date must be YYYY-MM-DD"}
    if llm_provider not in {"openclaw", "auto", "openai", "google", "anthropic", "deepseek", "groq", "ollama", "openai_compatible"}:
        return {"status": "error", "message": "unsupported llm_provider"}
    if not 1 <= max_debate_rounds <= 3 or not 60 <= timeout_seconds <= 1800:
        return {"status": "error", "message": "max_debate_rounds must be 1-3 and timeout_seconds must be 60-1800"}
    try:
        ticker = _a_share_ticker(stock_code)
    except ValueError as exc:
        return {"status": "error", "message": str(exc)}
    confirmation = _require_external_ai_confirmation("TradingAgents 多角色研究", confirm_external_ai)
    if confirmation:
        return confirmation
    python = _quant_backend_python()
    if not _python_has_module(python, "tradingagents"):
        return {"status": "error", "message": "未在专用后端环境安装 tradingagents；请通过 get_skill_status 检查后端状态。"}
    runner = """
import json
import os
from pathlib import Path
from tradingagents.config import TradingAgentsConfig
from tradingagents.graph.trading_graph import TradingAgentsGraph
config = TradingAgentsConfig(
    results_dir=Path(os.environ['TRADINGAGENTS_CACHE_DIR']),
    llm_provider=os.environ['STOCK_SCREENER_TA_PROVIDER'],
    deep_think_llm=os.environ['STOCK_SCREENER_TA_DEEP_MODEL'],
    quick_think_llm=os.environ['STOCK_SCREENER_TA_QUICK_MODEL'],
    response_language='zh-CN',
    max_debate_rounds=int(os.environ['STOCK_SCREENER_TA_DEBATE_ROUNDS']),
    max_risk_discuss_rounds=1,
    max_recur_limit=30,
)
graph = TradingAgentsGraph(debug=False, config=config)
_, decision = graph.propagate(os.environ['STOCK_SCREENER_TA_TICKER'], os.environ['STOCK_SCREENER_TA_DATE'])
print(json.dumps({'ticker': os.environ['STOCK_SCREENER_TA_TICKER'], 'analysis_date': os.environ['STOCK_SCREENER_TA_DATE'], 'decision': decision}, ensure_ascii=False, default=str))
""".strip()
    environment = _backend_env()
    environment.update(
        {
            "STOCK_SCREENER_TA_TICKER": ticker,
            "STOCK_SCREENER_TA_DATE": analysis_date,
            "STOCK_SCREENER_TA_PROVIDER": "openai" if llm_provider in {"openclaw", "auto"} else llm_provider,
            "STOCK_SCREENER_TA_DEEP_MODEL": _OPENCLAW_MODEL_REF if llm_provider in {"openclaw", "auto"} else "gpt-4o",
            "STOCK_SCREENER_TA_QUICK_MODEL": _OPENCLAW_MODEL_REF if llm_provider in {"openclaw", "auto"} else "gpt-4o-mini",
            "STOCK_SCREENER_TA_DEBATE_ROUNDS": str(max_debate_rounds),
        }
    )
    bridge: Optional[_OpenClawInferenceBridge] = None
    if llm_provider in {"openclaw", "auto"}:
        if not _openclaw_cli():
            return {"status": "error", "message": "未找到 OpenClaw CLI；无法使用已配置的 OpenClaw 模型。"}
        bridge = _OpenClawInferenceBridge(timeout_seconds=min(timeout_seconds, 300))
    try:
        if bridge:
            with bridge:
                environment.update({"OPENAI_API_KEY": bridge.token, "OPENAI_BASE_URL": bridge.base_url})
                completed = subprocess.run(
                    [python, "-c", runner], capture_output=True, text=True, timeout=timeout_seconds,
                    env=environment, cwd=_ensure_quant_state_dir(), check=False,
                )
        else:
            completed = subprocess.run(
                [python, "-c", runner], capture_output=True, text=True, timeout=timeout_seconds,
                env=environment, cwd=_ensure_quant_state_dir(), check=False,
            )
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "message": f"TradingAgents 超过 {timeout_seconds} 秒仍未完成，已终止。"}
    except OSError as exc:
        return {"status": "error", "message": f"无法启动 TradingAgents: {type(exc).__name__}"}
    return {
        "status": "success" if completed.returncode == 0 else "error",
        "backend": "TauricResearch/TradingAgents",
        "ticker": ticker,
        "analysis_date": analysis_date,
        "llm_provider": "openclaw/default" if llm_provider in {"openclaw", "auto"} else llm_provider,
        "max_debate_rounds": max_debate_rounds,
        "exit_code": completed.returncode,
        "untrusted_external_data": True,
        "stdout": _trim_backend_output(completed.stdout),
        "stderr": _trim_backend_output(completed.stderr, limit=4000),
        "research_only": True,
        "disclaimer": "该框架的 simulated exchange/组合决策仅用于研究；本 Skill 不发送真实订单，结论不构成投资建议。",
    }


# ==========================================
# Compact public MCP surface
# ==========================================
@mcp.tool()
def get_skill_status(verify_tonghuashun: bool = False, include_details: bool = False) -> Dict[str, Any]:
    """统一查看行情、DSA、AI4Trade 及可选量化后端状态；可附带策略清单和预测缓存。"""
    backend_python = _quant_backend_python()
    result = {
        "status": "success",
        "market_data": get_data_provider_status(verify_connection=verify_tonghuashun),
        "ai4trade": get_ai4trade_status(),
        "agent_research": {
            "research_only": True,
            "no_background_jobs": True,
            "no_broker_orders": True,
            "vibe_trading_command_available": bool(_vibe_trading_command()),
            "tradingagents_package_available": _python_has_module(backend_python, "tradingagents"),
            "quantaalpha": _quantaalpha_status(),
            "openclaw_model_bridge_available": bool(_openclaw_cli()),
            "backend_python_configured": bool(backend_python),
            "artifact_dir": QUANT_STATE_DIR,
        },
    }
    if include_details:
        result["strategy_catalog"] = get_strategies()
        result["prediction_cache"] = predict_cache_status()
    return result


@mcp.tool()
def get_ai4trade(
    resource: str = "status",
    limit: int = 20,
    message_type: Optional[str] = None,
    symbol: Optional[str] = None,
    keyword: Optional[str] = None,
    sort: str = "new",
    view: str = "overview",
    category: Optional[str] = None,
    slug: Optional[str] = None,
    condition_id: Optional[str] = None,
    token_id: Optional[str] = None,
) -> Dict[str, Any]:
    """统一读取 AI4Trade 状态、信号、市场情报、Polymarket、账户、持仓或关注列表。"""
    if resource == "status":
        return get_ai4trade_status()
    if resource == "signals":
        return get_ai4trade_signal_feed(limit, message_type, symbol, keyword, sort)
    if resource == "market_intel":
        return get_ai4trade_market_intel(view, symbol, category, limit)
    if resource == "polymarket":
        return get_ai4trade_polymarket_market(slug, condition_id, token_id)
    if resource == "account":
        return get_ai4trade_account()
    if resource == "positions":
        return get_ai4trade_positions()
    if resource == "following":
        return get_ai4trade_following()
    return {
        "status": "error",
        "message": "resource must be status, signals, market_intel, polymarket, account, positions, or following",
    }


@mcp.tool()
def manage_ai4trade(
    action: str,
    confirm: bool = False,
    leader_id: Optional[int] = None,
    signal_id: Optional[int] = None,
    reply_id: Optional[int] = None,
    market: Optional[str] = None,
    signal_action: Optional[str] = None,
    title: Optional[str] = None,
    content: Optional[str] = None,
    symbols: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    symbol: Optional[str] = None,
    price: Optional[float] = None,
    quantity: Optional[float] = None,
    executed_at: Optional[str] = None,
    outcome: Optional[str] = None,
    token_id: Optional[str] = None,
    amount: Optional[int] = None,
) -> Dict[str, Any]:
    """统一执行需确认的 AI4Trade 状态变更；不会接触真实券商。"""
    if action in {"follow", "unfollow"}:
        return manage_ai4trade_follow(leader_id or 0, action, confirm)
    if action == "publish_strategy":
        return publish_ai4trade_strategy(market or "", title or "", content or "", symbols or [], tags, confirm)
    if action == "publish_discussion":
        return publish_ai4trade_discussion(title or "", content or "", tags, confirm)
    if action in {"reply_create", "reply_accept"}:
        return manage_ai4trade_reply(
            signal_id or 0, content or "", "create" if action == "reply_create" else "accept", reply_id, confirm
        )
    if action == "publish_signal":
        return publish_ai4trade_realtime_signal(
            market or "", signal_action or "", symbol or "", price if price is not None else -1,
            quantity if quantity is not None else 0, executed_at or "", content, outcome, token_id, confirm,
        )
    if action == "exchange_points":
        return exchange_ai4trade_points(amount or 0, confirm)
    if action == "heartbeat_once":
        return get_ai4trade_heartbeat_once(confirm)
    return {
        "status": "error",
        "message": "action must be follow, unfollow, publish_strategy, publish_discussion, reply_create, reply_accept, publish_signal, exchange_points, or heartbeat_once",
    }


@mcp.tool()
def run_factor_research(
    action: str = "benchmark",
    zoo: Optional[str] = None,
    universe: str = "csi300",
    period: Optional[str] = None,
    top_n: int = 20,
    factor_id: Optional[str] = None,
    theme: Optional[str] = None,
    limit: int = 50,
    timeout_seconds: int = 900,
) -> Dict[str, Any]:
    """直接运行 Vibe-Trading Alpha Zoo 的因子横评、目录查询或因子说明；不使用 LLM/对话/券商。"""
    return run_vibe_factor_research(action, zoo, universe, period, top_n, factor_id, theme, limit, timeout_seconds)


@mcp.tool()
def run_tencent_factor_research(
    stock_codes: List[str],
    start_date: str,
    end_date: str,
    factor_ids: Optional[List[str]] = None,
    forward_days: int = 20,
    rebalance_days: int = 20,
    oos_split: Optional[str] = None,
    random_seeds: int = 20,
    refresh_cache: bool = False,
) -> Dict[str, Any]:
    """用腾讯复权日线横评价量因子；需显式提供 20-120 只股票的当期或历史归档股票池。"""
    return _run_tencent_factor_research(
        stock_codes,
        start_date,
        end_date,
        factor_ids,
        forward_days,
        rebalance_days,
        oos_split,
        random_seeds,
        refresh_cache,
    )


@mcp.tool()
def run_quantaalpha_research(
    action: str = "status",
    direction: Optional[str] = None,
    step_n: int = 5,
    factor_source: str = "alpha158_20",
    dry_run: bool = False,
    confirm_external_ai: bool = False,
    timeout_seconds: int = 1800,
) -> Dict[str, Any]:
    """运行隔离的 QuantaAlpha 状态检查、自动因子挖掘或因子回测；仅研究，不接券商。"""
    return _run_quantaalpha_research(
        action, direction, step_n, factor_source, dry_run, confirm_external_ai, timeout_seconds
    )


@mcp.tool()
def score_portfolio(
    portfolio_codes: List[str],
    peer_codes: List[str],
    start_date: str,
    as_of_date: str,
    factor_ids: Optional[List[str]] = None,
    oos_split: Optional[str] = None,
    position_weights: Optional[List[float]] = None,
    refresh_cache: bool = False,
) -> Dict[str, Any]:
    """用 QuantaAlpha 兼容价量因子和腾讯复权日线评估持仓的对照池相对暴露；不输出涨跌概率或买卖指令。"""
    return _score_portfolio_factors(
        portfolio_codes,
        peer_codes,
        start_date,
        as_of_date,
        factor_ids,
        oos_split,
        position_weights,
        refresh_cache,
    )


@mcp.tool()
def run_agent_research(
    engine: str,
    confirm_external_ai: bool = False,
    prompt: Optional[str] = None,
    preset: Optional[str] = None,
    stock_code: Optional[str] = None,
    analysis_date: Optional[str] = None,
    llm_provider: str = "openclaw",
    max_iterations: int = 6,
    max_debate_rounds: int = 1,
    timeout_seconds: int = 900,
) -> Dict[str, Any]:
    """统一运行 Vibe 单次研究、Vibe 团队投研或 TradingAgents 多角色研究。"""
    if engine == "vibe":
        return run_vibe_trading_research(prompt or "", confirm_external_ai, max_iterations, timeout_seconds)
    if engine == "vibe_swarm":
        return run_vibe_trading_swarm(preset or "", prompt or "", confirm_external_ai, timeout_seconds)
    if engine == "tradingagents":
        return run_tradingagents_research(
            stock_code or "", analysis_date or "", confirm_external_ai, llm_provider, max_debate_rounds, timeout_seconds
        )
    return {"status": "error", "message": "engine must be vibe, vibe_swarm, or tradingagents"}


if __name__ == "__main__":
    mcp.run()
