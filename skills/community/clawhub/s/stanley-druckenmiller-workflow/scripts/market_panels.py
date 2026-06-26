#!/usr/bin/env python3
"""Build dashboard-style market panels with source fallback and cache.

Primary source (default mode):
- finshare (controlled by --finshare-mode / FINSHARE_MODE)

Fallback sources:
- Yahoo chart API
- Stooq daily CSV (where available)
- FRED proxy series for selected macro symbols
- AkShare for A-share structure / liquidity / northbound / margin panels
- Local cache from previous successful runs
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import random
import time
import urllib.error
import urllib.parse
import urllib.request
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import akshare as ak  # type: ignore
except Exception:  # noqa: BLE001
    ak = None

USER_AGENT = "Mozilla/5.0 (OpenClaw stanley-druckenmiller-workflow/1.1)"

SYMBOLS = {
    "rates": ["^IRX", "^FVX", "^TNX", "^TYX"],
    "fx": ["DX-Y.NYB", "AUDJPY=X", "EURUSD=X", "USDJPY=X", "USDCNH=X", "USDCNY=X"],
    "equities": ["^GSPC", "^IXIC", "^RUT", "^VIX", "SPY", "IWM", "RSP", "SPHB", "SPLV", "UUP"],
    "credit": ["HYG", "LQD"],
    "internals": ["XHB", "ITB", "IYT", "XRT", "SMH", "KRE", "XLY", "XLP"],
    "commodities": ["CL=F", "GC=F", "HG=F"],
    "global_equities": ["FEZ", "EWJ", "FXI", "EWH", "EEM", "VGK", "KWEB", "ASHR"],
    "global_rates_proxy": ["BNDX", "BWX", "EMB"],
}

A_SHARE_INDEX_CODES = {
    "sh000001": {"name": "Shanghai Composite", "yahoo": "000001.SS"},
    "sh000300": {"name": "CSI 300", "yahoo": "000300.SS"},
    "sz399001": {"name": "Shenzhen Component", "yahoo": "399001.SZ"},
    "sz399006": {"name": "ChiNext", "yahoo": "399006.SZ"},
    "sh000852": {"name": "CSI 1000", "yahoo": None},
}

HK_INDEX_SYMBOLS = {
    "HSI": "Hang Seng Index",
    "HSCEI": "Hang Seng China Enterprises Index",
}

A_SHARE_LEADER_BASKETS = {
    "property": ["600048", "000002", "001979"],
    "banks_joint_stock": ["600036", "601166"],
    "banks_big4": ["601398", "601288"],
    "brokers": ["300059", "600030"],
    "machinery": ["600031", "000425"],
    "transport": ["601598", "600018", "601006"],
    "heavy_truck": ["000338", "600166", "601633"],
    "consumer_premium": ["600519", "000858"],
    "consumer_mass": ["600887", "603288", "000651"],
    "credit_sensitive": ["600048", "000002", "300059", "600030"],
}

FRED_SERIES = [
    "WALCL",
    "RRPONTSYD",
    "WTREGEN",
    "M2SL",
    "GDP",
    "DGS2",
    "DGS10",
    "T10Y2Y",
    "BAMLH0A0HYM2",
    "MORTGAGE30US",
    "HOUST",
    "PERMIT",
    "RSAFS",
    "TOTALSA",
    "PCEC96",
    "TSIFRGHT",
    "INDPRO",
    "TCU",
    "DGORDER",
    "CP",
    "ULCNFB",
    "OPHNFB",
]

# Proxy map used when Yahoo/Stooq are unavailable.
FRED_PROXY_MAP = {
    "^IRX": "DGS3MO",
    "^FVX": "DGS5",
    "^TNX": "DGS10",
    "^TYX": "DGS30",
    "^VIX": "VIXCLS",
    "DX-Y.NYB": "DTWEXBGS",
    "CL=F": "DCOILWTICO",
    "GC=F": "GOLDAMGBD228NLBM",
    "HG=F": "PCOPPUSDM",
}

STOOQ_MAP = {
    "SPY": "spy.us",
    "IWM": "iwm.us",
    "HYG": "hyg.us",
    "LQD": "lqd.us",
    "XHB": "xhb.us",
    "ITB": "itb.us",
    "IYT": "iyt.us",
    "XRT": "xrt.us",
    "SMH": "smh.us",
    "KRE": "kre.us",
    "XLY": "xly.us",
    "XLP": "xlp.us",
    "^GSPC": "^spx",
    "^IXIC": "^ndq",
    "AUDJPY=X": "audjpy",
}

BREADTH_PROXY_UNIVERSE = [
    "SPY",
    "IWM",
    "XHB",
    "ITB",
    "IYT",
    "XRT",
    "SMH",
    "KRE",
    "XLY",
    "XLP",
    "HYG",
    "LQD",
]

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNTIME_DIR = SKILL_ROOT / ".runtime"
RUNTIME_DIR = Path(os.getenv("STANLEY_RUNTIME_DIR", str(DEFAULT_RUNTIME_DIR))).expanduser().resolve()
CACHE_PATH = RUNTIME_DIR / "market-snapshots" / "market-panels-cache.json"
CN_FLOW_HISTORY_PATH = RUNTIME_DIR / "market-snapshots" / "a-share-flow-history.json"
CACHE_FRESH_HOURS = 96
CACHE_STALE_HOURS = 336


class HttpError(RuntimeError):
    pass


def http_get(url: str, timeout: int = 20, retries: int = 5, backoff: float = 0.6) -> str:
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            last_err = exc
            retryable = exc.code in (429, 500, 502, 503, 504)
            if not retryable or attempt == retries - 1:
                break
            sleep_s = backoff * (2**attempt) + random.uniform(0.05, 0.25)
            time.sleep(sleep_s)
        except (urllib.error.URLError, TimeoutError) as exc:
            last_err = exc
            if attempt == retries - 1:
                break
            sleep_s = backoff * (2**attempt) + random.uniform(0.05, 0.25)
            time.sleep(sleep_s)
    raise HttpError(str(last_err))


def compute_changes(points: list[tuple[int, float]]) -> tuple[float | None, float | None, float | None]:
    vals = [v for _, v in points]
    latest = vals[-1]

    def pct(old: float | None) -> float | None:
        if old in (None, 0):
            return None
        return ((latest - old) / old) * 100.0

    chg_1d = pct(vals[-2]) if len(vals) >= 2 else None
    chg_5d = pct(vals[-6]) if len(vals) >= 6 else None
    chg_20d = pct(vals[-21]) if len(vals) >= 21 else None
    return chg_1d, chg_5d, chg_20d


def yahoo_series(symbol: str, range_: str = "1y", interval: str = "1d") -> dict:
    encoded = urllib.parse.quote(symbol, safe="")
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded}"
        f"?range={range_}&interval={interval}&includePrePost=false"
    )
    try:
        payload = json.loads(http_get(url))
        result = payload["chart"]["result"][0]
        ts = result.get("timestamp", [])
        close = result["indicators"]["quote"][0].get("close", [])
        points = [(int(t), float(v)) for t, v in zip(ts, close) if v is not None]
        if len(points) < 2:
            return {"ok": False, "symbol": symbol, "url": url, "error": "insufficient data"}

        latest_ts, latest = points[-1]
        chg_1d, chg_5d, chg_20d = compute_changes(points)
        return {
            "ok": True,
            "symbol": symbol,
            "url": url,
            "source": "yahoo",
            "asof_utc": datetime.fromtimestamp(latest_ts, tz=timezone.utc).isoformat(),
            "latest": latest,
            "chg_1d_pct": chg_1d,
            "chg_5d_pct": chg_5d,
            "chg_20d_pct": chg_20d,
            "series_close": [v for _, v in points],
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "symbol": symbol, "url": url, "error": str(exc)}


def finshare_series(symbol: str) -> dict:
    """Fetch series from finshare when available.

    finshare is optional. This function fails closed with structured errors when
    package/API is unavailable for the target symbol.
    """
    try:
        import finshare as fs  # type: ignore
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "symbol": symbol, "error": f"finshare unavailable: {exc}"}

    candidates = [symbol]
    if symbol.startswith("^"):
        candidates.append(symbol[1:])
    if symbol.endswith("=X"):
        candidates.append(symbol.replace("=X", ""))
    if symbol.endswith(".NYB"):
        candidates.append(symbol.split(".")[0])

    end_dt = datetime.now(timezone.utc).date()
    start_dt = end_dt - timedelta(days=420)

    last_err: str | None = None
    for code in dict.fromkeys(candidates):
        try:
            df = fs.get_historical_data(code, start=start_dt.isoformat(), end=end_dt.isoformat())
            if df is None or len(df) < 2:
                last_err = f"insufficient data for {code}"
                continue

            close_col = None
            for c in ("close_price", "close", "Close", "\u6536\u76d8"):
                if c in df.columns:
                    close_col = c
                    break
            if close_col is None:
                last_err = f"close column missing for {code}"
                continue

            series = [float(v) for v in df[close_col].tolist() if v is not None]
            if len(series) < 2:
                last_err = f"insufficient close series for {code}"
                continue

            date_col = None
            for c in ("trade_date", "date", "Date", "datetime", "time"):
                if c in df.columns:
                    date_col = c
                    break

            latest_ts = int(datetime.now(timezone.utc).timestamp())
            if date_col is not None:
                raw_date = str(df[date_col].iloc[-1])
                try:
                    parsed = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                    if parsed.tzinfo is None:
                        parsed = parsed.replace(tzinfo=timezone.utc)
                    latest_ts = int(parsed.timestamp())
                except Exception:
                    pass

            chg_1d, chg_5d, chg_20d = compute_changes(list(enumerate(series, start=1)))
            return {
                "ok": True,
                "symbol": symbol,
                "url": "finshare://get_historical_data",
                "source": "finshare",
                "asof_utc": datetime.fromtimestamp(latest_ts, tz=timezone.utc).isoformat(),
                "latest": series[-1],
                "chg_1d_pct": chg_1d,
                "chg_5d_pct": chg_5d,
                "chg_20d_pct": chg_20d,
                "series_close": series,
                "finshare_code": code,
            }
        except Exception as exc:  # noqa: BLE001
            last_err = str(exc)
            continue

    return {"ok": False, "symbol": symbol, "error": last_err or "finshare failed"}


def stooq_series(symbol: str) -> dict:
    stooq_symbol = STOOQ_MAP.get(symbol)
    if not stooq_symbol:
        return {"ok": False, "symbol": symbol, "error": "stooq mapping unavailable"}

    url = f"https://stooq.com/q/d/l/?s={stooq_symbol}&i=d"
    try:
        text = http_get(url)
        reader = csv.DictReader(io.StringIO(text))
        points: list[tuple[int, float]] = []
        for row in reader:
            raw_date = (row.get("Date") or "").strip()
            raw_close = (row.get("Close") or "").strip()
            if not raw_date or not raw_close:
                continue
            try:
                dt = datetime.fromisoformat(raw_date).replace(tzinfo=timezone.utc)
                close_val = float(raw_close)
            except ValueError:
                continue
            points.append((int(dt.timestamp()), close_val))

        if len(points) < 2:
            return {"ok": False, "symbol": symbol, "url": url, "error": "insufficient stooq data"}

        latest_ts, latest = points[-1]
        chg_1d, chg_5d, chg_20d = compute_changes(points)
        return {
            "ok": True,
            "symbol": symbol,
            "url": url,
            "source": "stooq",
            "asof_utc": datetime.fromtimestamp(latest_ts, tz=timezone.utc).isoformat(),
            "latest": latest,
            "chg_1d_pct": chg_1d,
            "chg_5d_pct": chg_5d,
            "chg_20d_pct": chg_20d,
            "series_close": [v for _, v in points],
            "stooq_symbol": stooq_symbol,
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "symbol": symbol, "url": url, "error": str(exc)}


def fred_points(series_id: str) -> list[tuple[int, float]]:
    """Fetch FRED series points.

    Preference order:
    1) FRED JSON API (when FRED_API_KEY is present)
    2) Public fredgraph CSV fallback (no key)
    """
    api_key = os.getenv("FRED_API_KEY", "").strip()
    if api_key:
        try:
            params = urllib.parse.urlencode(
                {
                    "series_id": series_id,
                    "api_key": api_key,
                    "file_type": "json",
                    "sort_order": "asc",
                }
            )
            url = f"https://api.stlouisfed.org/fred/series/observations?{params}"
            payload = json.loads(http_get(url))
            observations = payload.get("observations", [])
            out: list[tuple[int, float]] = []
            for row in observations:
                raw_date = str(row.get("date", "")).strip()
                raw_val = str(row.get("value", "")).strip()
                if not raw_date or not raw_val or raw_val == ".":
                    continue
                try:
                    dt = datetime.fromisoformat(raw_date).replace(tzinfo=timezone.utc)
                    val = float(raw_val)
                except ValueError:
                    continue
                out.append((int(dt.timestamp()), val))
            if out:
                return out
        except Exception:
            # fall through to public CSV path
            pass

    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    text = http_get(url)
    reader = csv.DictReader(io.StringIO(text))
    fields = reader.fieldnames or []
    if len(fields) < 2:
        return []

    date_key = fields[0]
    value_key = fields[1]

    out: list[tuple[int, float]] = []
    for row in reader:
        raw_date = (row.get(date_key) or "").strip()
        raw_val = (row.get(value_key) or "").strip()
        if not raw_date or not raw_val or raw_val == ".":
            continue
        try:
            dt = datetime.fromisoformat(raw_date).replace(tzinfo=timezone.utc)
            val = float(raw_val)
        except ValueError:
            continue
        out.append((int(dt.timestamp()), val))
    return out


def fred_proxy_series(symbol: str) -> dict:
    # Derived AUDJPY from FRED pairs when possible.
    if symbol == "AUDJPY=X":
        try:
            # DEXJPUS: JPY per USD, DEXUSAL: USD per AUD.
            jpy = fred_points("DEXJPUS")
            aud = fred_points("DEXUSAL")
            if len(jpy) < 2 or len(aud) < 2:
                return {"ok": False, "symbol": symbol, "error": "insufficient FRED FX points"}
            aud_map = {ts: val for ts, val in aud}
            points: list[tuple[int, float]] = []
            for ts, jpy_per_usd in jpy:
                usd_per_aud = aud_map.get(ts)
                if usd_per_aud is None:
                    continue
                points.append((ts, jpy_per_usd * usd_per_aud))
            if len(points) < 2:
                return {"ok": False, "symbol": symbol, "error": "no aligned FRED FX dates"}
            latest_ts, latest = points[-1]
            chg_1d, chg_5d, chg_20d = compute_changes(points)
            return {
                "ok": True,
                "symbol": symbol,
                "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXJPUS",
                "source": "fred-proxy",
                "asof_utc": datetime.fromtimestamp(latest_ts, tz=timezone.utc).isoformat(),
                "latest": latest,
                "chg_1d_pct": chg_1d,
                "chg_5d_pct": chg_5d,
                "chg_20d_pct": chg_20d,
                "series_close": [v for _, v in points],
                "proxy_series": ["DEXJPUS", "DEXUSAL"],
            }
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "symbol": symbol, "error": str(exc)}

    series_id = FRED_PROXY_MAP.get(symbol)
    if not series_id:
        return {"ok": False, "symbol": symbol, "error": "fred proxy mapping unavailable"}

    try:
        points = fred_points(series_id)
        if len(points) < 2:
            return {"ok": False, "symbol": symbol, "error": "insufficient FRED proxy data"}

        latest_ts, latest = points[-1]
        chg_1d, chg_5d, chg_20d = compute_changes(points)
        return {
            "ok": True,
            "symbol": symbol,
            "url": f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}",
            "source": "fred-proxy",
            "asof_utc": datetime.fromtimestamp(latest_ts, tz=timezone.utc).isoformat(),
            "latest": latest,
            "chg_1d_pct": chg_1d,
            "chg_5d_pct": chg_5d,
            "chg_20d_pct": chg_20d,
            "series_close": [v for _, v in points],
            "proxy_series": [series_id],
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "symbol": symbol, "error": str(exc)}


def load_cache() -> dict[str, dict]:
    if not CACHE_PATH.exists():
        return {}
    try:
        payload = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        symbols = payload.get("symbols")
        if isinstance(symbols, dict):
            return symbols
    except Exception:
        return {}
    return {}


def _cache_age_hours(asof_utc: str) -> float | None:
    try:
        ts = datetime.fromisoformat(asof_utc.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        return (now - ts.astimezone(timezone.utc)).total_seconds() / 3600.0
    except Exception:
        return None


def cache_series(symbol: str, cache: dict[str, dict]) -> dict:
    item = deepcopy(cache.get(symbol) or {})
    if not item:
        return {"ok": False, "symbol": symbol, "error": "cache miss"}

    asof = item.get("asof_utc")
    if not asof:
        return {"ok": False, "symbol": symbol, "error": "cache missing asof_utc"}

    age_h = _cache_age_hours(asof)
    if age_h is None or age_h > CACHE_STALE_HOURS:
        return {"ok": False, "symbol": symbol, "error": "cache too old"}

    item["ok"] = True
    item["symbol"] = symbol
    item["source"] = f"cache:{item.get('source', 'unknown')}"
    item["cache_age_hours"] = round(age_h, 2)
    item["stale"] = age_h > CACHE_FRESH_HOURS
    return item


def save_cache(flat: dict[str, dict]) -> None:
    symbols: dict[str, dict] = {}
    for sym, item in flat.items():
        if not item.get("ok"):
            continue
        if not item.get("series_close"):
            continue
        symbols[sym] = deepcopy(item)

    if not symbols:
        return

    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        "symbols": symbols,
    }
    CACHE_PATH.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def resolve_finshare_mode(finshare_mode: str | None) -> str:
    mode = (finshare_mode or os.getenv("FINSHARE_MODE") or "first").strip().lower()
    if mode not in {"first", "auto", "off"}:
        return "first"
    return mode


def fetch_symbol_with_fallback(symbol: str, cache: dict[str, dict], finshare_mode: str = "first") -> dict:
    attempts: list[str] = []

    if finshare_mode == "first":
        alt_finshare = finshare_series(symbol)
        if alt_finshare.get("ok"):
            alt_finshare["fallback_chain"] = attempts
            return alt_finshare
        attempts.append(f"finshare:{alt_finshare.get('error', 'unknown')}" )

    primary = yahoo_series(symbol)
    if primary.get("ok"):
        primary["fallback_chain"] = attempts
        return primary
    attempts.append(f"yahoo:{primary.get('error', 'unknown')}" )

    if finshare_mode == "auto":
        alt_finshare = finshare_series(symbol)
        if alt_finshare.get("ok"):
            alt_finshare["fallback_chain"] = attempts
            return alt_finshare
        attempts.append(f"finshare:{alt_finshare.get('error', 'unknown')}" )
    elif finshare_mode == "off":
        attempts.append("finshare:disabled")

    alt_stooq = stooq_series(symbol)
    if alt_stooq.get("ok"):
        alt_stooq["fallback_chain"] = attempts
        return alt_stooq
    attempts.append(f"stooq:{alt_stooq.get('error', 'unknown')}" )

    alt_fred = fred_proxy_series(symbol)
    if alt_fred.get("ok"):
        alt_fred["fallback_chain"] = attempts
        return alt_fred
    attempts.append(f"fred-proxy:{alt_fred.get('error', 'unknown')}" )

    cached = cache_series(symbol, cache)
    if cached.get("ok"):
        cached["fallback_chain"] = attempts
        return cached
    attempts.append(f"cache:{cached.get('error', 'unknown')}" )

    return {
        "ok": False,
        "symbol": symbol,
        "url": primary.get("url"),
        "error": "all sources failed",
        "fallback_chain": attempts,
    }


def fred_latest(series_id: str) -> dict:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        points = fred_points(series_id)
        if not points:
            return {"ok": False, "series": series_id, "url": url, "error": "no numeric value"}
        latest_ts, latest = points[-1]
        prev = points[-2][1] if len(points) >= 2 else None
        date_val = datetime.fromtimestamp(latest_ts, tz=timezone.utc).date().isoformat()
        out = {
            "ok": True,
            "series": series_id,
            "date": date_val,
            "value": latest,
            "url": url,
        }
        if prev is not None:
            out["prev"] = prev
            out["chg"] = latest - prev
        return out
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "series": series_id, "url": url, "error": str(exc)}


def safe_latest(data: dict, symbol: str) -> float | None:
    item = data.get(symbol)
    if not item or not item.get("ok"):
        return None
    return item.get("latest")


def calc_breadth_proxy(flat: dict[str, dict]) -> dict:
    available = []
    for sym in BREADTH_PROXY_UNIVERSE:
        item = flat.get(sym)
        if not item or not item.get("ok"):
            continue
        closes = item.get("series_close") or []
        if len(closes) < 210:
            continue
        available.append((sym, closes))

    if not available:
        return {
            "ok": False,
            "error": "insufficient proxy breadth history",
            "universe": BREADTH_PROXY_UNIVERSE,
        }

    advancers = 0
    decliners = 0
    above_200d = 0
    new_highs_20d = 0
    new_lows_20d = 0

    for _, closes in available:
        latest = closes[-1]
        prev = closes[-2]
        ma200 = sum(closes[-200:]) / 200.0

        if latest > prev:
            advancers += 1
        elif latest < prev:
            decliners += 1

        if latest > ma200:
            above_200d += 1

        if latest >= max(closes[-20:]):
            new_highs_20d += 1
        if latest <= min(closes[-20:]):
            new_lows_20d += 1

    total = len(available)
    return {
        "ok": True,
        "method": "proxy-universe",
        "universe": [sym for sym, _ in available],
        "advancers_1d": advancers,
        "decliners_1d": decliners,
        "ad_line_1d": advancers - decliners,
        "pct_above_200d": (above_200d / total) * 100.0,
        "new_highs_20d": new_highs_20d,
        "new_lows_20d": new_lows_20d,
        "sample_size": total,
    }


def calc_realized_vol_pct(series_close: list[float], lookback: int = 20) -> float | None:
    if len(series_close) < lookback + 1:
        return None
    window = series_close[-(lookback + 1):]
    rets = []
    for prev, cur in zip(window[:-1], window[1:]):
        if prev in (None, 0) or cur is None:
            continue
        rets.append((cur / prev) - 1.0)
    if len(rets) < max(5, lookback // 2):
        return None
    mean = sum(rets) / len(rets)
    var = sum((r - mean) ** 2 for r in rets) / len(rets)
    return (var ** 0.5) * (252 ** 0.5) * 100.0


def calc_realized_vol_bp(series_close: list[float], lookback: int = 20) -> float | None:
    if len(series_close) < lookback + 1:
        return None
    window = series_close[-(lookback + 1):]
    changes_bp = []
    for prev, cur in zip(window[:-1], window[1:]):
        if prev is None or cur is None:
            continue
        changes_bp.append((cur - prev) * 100.0)
    if len(changes_bp) < max(5, lookback // 2):
        return None
    mean = sum(changes_bp) / len(changes_bp)
    var = sum((x - mean) ** 2 for x in changes_bp) / len(changes_bp)
    return (var ** 0.5) * (252 ** 0.5)


def _to_iso_date(value) -> str:
    try:
        if hasattr(value, "isoformat"):
            return value.isoformat()
    except Exception:
        pass
    return str(value)


def _to_float(value) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except Exception:
        return None


def akshare_stock_hist_snapshot(symbol: str, days: int = 40) -> dict:
    if ak is None:
        return {"ok": False, "symbol": symbol, "error": "akshare unavailable"}
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=days * 3)).strftime("%Y%m%d")
    try:
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        if df is None or len(df) < 2:
            return {"ok": False, "symbol": symbol, "error": "insufficient akshare history"}
        points: list[tuple[int, float]] = []
        turnover = None
        for _, row in df.iterrows():
            raw_date = row.get("\u65e5\u671f")
            close_val = _to_float(row.get("\u6536\u76d8"))
            if close_val is None:
                continue
            try:
                dt = datetime.fromisoformat(str(raw_date)).replace(tzinfo=timezone.utc)
            except Exception:
                continue
            points.append((int(dt.timestamp()), close_val))
            turnover = _to_float(row.get("\u6362\u624b\u7387"))
        if len(points) < 2:
            return {"ok": False, "symbol": symbol, "error": "insufficient akshare close points"}
        latest_ts, latest = points[-1]
        chg_1d, chg_5d, chg_20d = compute_changes(points)
        return {
            "ok": True,
            "symbol": symbol,
            "source": "akshare",
            "asof_utc": datetime.fromtimestamp(latest_ts, tz=timezone.utc).isoformat(),
            "latest": latest,
            "chg_1d_pct": chg_1d,
            "chg_5d_pct": chg_5d,
            "chg_20d_pct": chg_20d,
            "turnover_pct": turnover,
            "series_close": [v for _, v in points],
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "symbol": symbol, "error": str(exc)}


def akshare_basket_snapshot(name: str, symbols: list[str]) -> dict:
    members = []
    for symbol in symbols:
        snap = akshare_stock_hist_snapshot(symbol)
        if snap.get("ok"):
            members.append(snap)
    if not members:
        return {"ok": False, "name": name, "symbols": symbols, "error": "no basket members available"}

    def avg(field: str) -> float | None:
        vals = [m.get(field) for m in members if m.get(field) is not None]
        if not vals:
            return None
        return sum(vals) / len(vals)

    return {
        "ok": True,
        "name": name,
        "symbols": symbols,
        "available": [m["symbol"] for m in members],
        "sample_size": len(members),
        "chg_1d_pct": avg("chg_1d_pct"),
        "chg_5d_pct": avg("chg_5d_pct"),
        "chg_20d_pct": avg("chg_20d_pct"),
        "avg_turnover_pct": avg("turnover_pct"),
        "asof_utc": members[-1].get("asof_utc"),
    }


def akshare_northbound_snapshot() -> dict:
    if ak is None:
        return {"ok": False, "error": "akshare unavailable"}
    try:
        df = ak.stock_hsgt_fund_flow_summary_em()
        if df is None or df.empty:
            return {"ok": False, "error": "empty northbound frame"}
        north = df[df["\u8d44\u91d1\u65b9\u5411"] == "\u5317\u5411"].copy()
        if north.empty:
            return {"ok": False, "error": "no northbound rows"}
        latest_date = north["\u4ea4\u6613\u65e5"].max()
        latest = north[north["\u4ea4\u6613\u65e5"] == latest_date]
        rows = latest[["\u677f\u5757", "\u76f8\u5173\u6307\u6570", "\u6307\u6570\u6da8\u8dcc\u5e45", "\u6210\u4ea4\u51c0\u4e70\u989d", "\u8d44\u91d1\u51c0\u6d41\u5165"]].copy()
        rows.columns = ["board", "related_index", "index_change_pct", "net_buy_amt", "net_inflow"]
        return {
            "ok": True,
            "date": _to_iso_date(latest_date),
            "net_buy_amt": float(latest["\u6210\u4ea4\u51c0\u4e70\u989d"].fillna(0).sum()),
            "net_inflow": float(latest["\u8d44\u91d1\u51c0\u6d41\u5165"].fillna(0).sum()),
            "advancers": int(latest["\u4e0a\u6da8\u6570"].fillna(0).sum()),
            "decliners": int(latest["\u4e0b\u8dcc\u6570"].fillna(0).sum()),
            "rows": rows.to_dict(orient="records"),
            "source": "akshare",
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}


def akshare_liquidity_snapshot() -> dict:
    if ak is None:
        return {"ok": False, "error": "akshare unavailable"}
    out: dict = {"ok": True, "source": "akshare"}
    try:
        shibor = ak.macro_china_shibor_all()
        if shibor is not None and not shibor.empty:
            row = shibor.iloc[-1]
            out["shibor"] = {
                "date": _to_iso_date(row.get("\u65e5\u671f")),
                "1w": _to_float(row.get("1W-\u5b9a\u4ef7")),
                "1w_change_bp": _to_float(row.get("1W-\u6da8\u8dcc\u5e45")),
                "overnight": _to_float(row.get("O/N-\u5b9a\u4ef7")),
            }
    except Exception as exc:  # noqa: BLE001
        out["shibor_error"] = str(exc)
    try:
        rates = ak.bond_zh_us_rate()
        if rates is not None and not rates.empty:
            row = rates.iloc[-1]
            out["rates"] = {
                "date": _to_iso_date(row.get("\u65e5\u671f")),
                "cn_2y": _to_float(row.get("\u4e2d\u56fd\u56fd\u503a\u6536\u76ca\u73872\u5e74")),
                "cn_10y": _to_float(row.get("\u4e2d\u56fd\u56fd\u503a\u6536\u76ca\u738710\u5e74")),
                "cn_30y": _to_float(row.get("\u4e2d\u56fd\u56fd\u503a\u6536\u76ca\u738730\u5e74")),
                "cn_10y_minus_2y": _to_float(row.get("\u4e2d\u56fd\u56fd\u503a\u6536\u76ca\u738710\u5e74-2\u5e74")),
            }
    except Exception as exc:  # noqa: BLE001
        out["rates_error"] = str(exc)
    return out


def akshare_margin_snapshot() -> dict:
    if ak is None:
        return {"ok": False, "error": "akshare unavailable"}

    def _latest_with_delta(df):
        if df is None or len(df) < 1:
            return None
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) >= 2 else None
        latest_balance = _to_float(latest.get("\u878d\u8d44\u4f59\u989d"))
        prev_balance = _to_float(prev.get("\u878d\u8d44\u4f59\u989d")) if prev is not None else None
        return {
            "date": _to_iso_date(latest.get("\u65e5\u671f")),
            "margin_buy_amt": _to_float(latest.get("\u878d\u8d44\u4e70\u5165\u989d")),
            "margin_balance": latest_balance,
            "margin_and_short_balance": _to_float(latest.get("\u878d\u8d44\u878d\u5238\u4f59\u989d")),
            "margin_balance_change": (latest_balance - prev_balance) if latest_balance is not None and prev_balance is not None else None,
        }

    out: dict = {"ok": True, "source": "akshare"}
    try:
        out["sh"] = _latest_with_delta(ak.macro_china_market_margin_sh())
    except Exception as exc:  # noqa: BLE001
        out["sh_error"] = str(exc)
    try:
        out["sz"] = _latest_with_delta(ak.macro_china_market_margin_sz())
    except Exception as exc:  # noqa: BLE001
        out["sz_error"] = str(exc)
    return out


def akshare_a_share_structure_snapshot() -> dict:
    if ak is None:
        return {"ok": False, "error": "akshare unavailable"}
    baskets = {name: akshare_basket_snapshot(name, symbols) for name, symbols in A_SHARE_LEADER_BASKETS.items()}
    premium = baskets.get("consumer_premium", {})
    mass = baskets.get("consumer_mass", {})
    joint = baskets.get("banks_joint_stock", {})
    big4 = baskets.get("banks_big4", {})
    property_b = baskets.get("property", {})
    brokers = baskets.get("brokers", {})
    machinery = baskets.get("machinery", {})
    transport = baskets.get("transport", {})
    heavy_truck = baskets.get("heavy_truck", {})

    premium_minus_mass = None
    if premium.get("ok") and mass.get("ok") and premium.get("chg_1d_pct") is not None and mass.get("chg_1d_pct") is not None:
        premium_minus_mass = premium["chg_1d_pct"] - mass["chg_1d_pct"]

    joint_minus_big4 = None
    if joint.get("ok") and big4.get("ok") and joint.get("chg_1d_pct") is not None and big4.get("chg_1d_pct") is not None:
        joint_minus_big4 = joint["chg_1d_pct"] - big4["chg_1d_pct"]

    credit_proxy_vals = [
        property_b.get("chg_1d_pct"),
        brokers.get("chg_1d_pct"),
        joint_minus_big4,
    ]
    credit_proxy_vals = [v for v in credit_proxy_vals if v is not None]
    credit_risk_proxy = sum(credit_proxy_vals) / len(credit_proxy_vals) if credit_proxy_vals else None

    industry_proxy_vals = [
        machinery.get("chg_1d_pct"),
        transport.get("chg_1d_pct"),
        heavy_truck.get("chg_1d_pct"),
        premium_minus_mass,
    ]
    industry_proxy_vals = [v for v in industry_proxy_vals if v is not None]
    industry_expression_proxy = sum(industry_proxy_vals) / len(industry_proxy_vals) if industry_proxy_vals else None

    return {
        "ok": any(v.get("ok") for v in baskets.values()),
        "source": "akshare",
        "baskets": baskets,
        "derived": {
            "premium_minus_mass_1d_pct": premium_minus_mass,
            "joint_stock_minus_big4_1d_pct": joint_minus_big4,
            "credit_risk_proxy_1d_pct": credit_risk_proxy,
            "industry_expression_proxy_1d_pct": industry_expression_proxy,
        },
    }


def build_snapshot(pause_s: float = 0.25, finshare_mode: str = "first") -> dict:
    finshare_mode = resolve_finshare_mode(finshare_mode)
    out: dict = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "primary": "finshare" if finshare_mode == "first" else "yahoo_chart_api_public",
            "fallbacks": ["yahoo_chart_api_public", "finshare(optional)", "stooq_csv_public", "fred_proxy_public", "local_cache"],
            "finshare_mode": finshare_mode,
            "fred": "fredgraph_csv_public",
            "akshare": "enabled" if ak is not None else "unavailable",
            "cache_path": str(CACHE_PATH),
        },
        "panels": {},
        "ratios": {},
        "fred": {},
        "a_share": {},
        "derived": {},
    }

    cache = load_cache()
    flat: dict[str, dict] = {}

    for panel, symbols in SYMBOLS.items():
        bucket = {}
        for sym in symbols:
            bucket[sym] = fetch_symbol_with_fallback(sym, cache, finshare_mode=finshare_mode)
            flat[sym] = bucket[sym]
            time.sleep(pause_s)
        out["panels"][panel] = bucket

    ratio_defs = [
        ("IWM_SPY", "IWM", "SPY"),
        ("XLY_XLP", "XLY", "XLP"),
        ("XHB_SPY", "XHB", "SPY"),
        ("SMH_SPY", "SMH", "SPY"),
        ("KRE_SPY", "KRE", "SPY"),
        ("COPPER_GOLD", "HG=F", "GC=F"),
        ("EEM_SPY", "EEM", "SPY"),
        ("FEZ_SPY", "FEZ", "SPY"),
        ("EWJ_SPY", "EWJ", "SPY"),
        ("FXI_SPY", "FXI", "SPY"),
        ("VGK_SPY", "VGK", "SPY"),
    ]

    for name, a, b in ratio_defs:
        va = safe_latest(flat, a)
        vb = safe_latest(flat, b)
        if va is None or vb in (None, 0):
            out["ratios"][name] = {"ok": False, "a": a, "b": b}
        else:
            out["ratios"][name] = {"ok": True, "a": a, "b": b, "value": va / vb}

    out["panels"]["breadth_proxy"] = calc_breadth_proxy(flat)

    # Market-structure / volatility proxies for when direct series are unavailable.
    tnx = flat.get('^TNX', {})
    if tnx.get('ok'):
        rv_bp = calc_realized_vol_bp(tnx.get('series_close') or [], lookback=20)
        if rv_bp is not None:
            out["derived"]["move_proxy_20d_realized_vol_bp_ann"] = rv_bp

    usdjpy = flat.get('USDJPY=X', {})
    if usdjpy.get('ok'):
        jpy_rv = calc_realized_vol_pct(usdjpy.get('series_close') or [], lookback=20)
        if jpy_rv is not None:
            out["derived"]["usdjpy_realized_vol_20d_pct_ann"] = jpy_rv

    # Europe breadth proxy from regional ETFs when direct internals are unavailable.
    europe_syms = ['FEZ', 'VGK', 'EWJ']
    europe_available = []
    for sym in europe_syms:
        item = flat.get(sym, {})
        if item.get('ok') and item.get('series_close') and len(item.get('series_close')) >= 60:
            europe_available.append((sym, item.get('series_close')))
    if europe_available:
        adv = 0
        dec = 0
        above_50d = 0
        for sym, closes in europe_available:
            latest = closes[-1]
            prev = closes[-2]
            ma50 = sum(closes[-50:]) / 50.0
            if latest > prev:
                adv += 1
            elif latest < prev:
                dec += 1
            if latest > ma50:
                above_50d += 1
        out["derived"]["europe_breadth_proxy"] = {
            "ok": True,
            "universe": [sym for sym, _ in europe_available],
            "advancers_1d": adv,
            "decliners_1d": dec,
            "pct_above_50d": (above_50d / len(europe_available)) * 100.0,
        }

    out["a_share"] = {
        "internal_structure": akshare_a_share_structure_snapshot(),
        "northbound": akshare_northbound_snapshot(),
        "liquidity": akshare_liquidity_snapshot(),
        "margin": akshare_margin_snapshot(),
    }

    nb = out["a_share"].get("northbound", {})
    internal = out["a_share"].get("internal_structure", {})
    if internal.get("ok"):
        internal_d = internal.get("derived", {})
        northbound_proxy = {
            "ok": True,
            "source": "proxy",
            "stock_connect_breadth": None,
            "credit_risk_proxy_1d_pct": internal_d.get("credit_risk_proxy_1d_pct"),
            "industry_expression_proxy_1d_pct": internal_d.get("industry_expression_proxy_1d_pct"),
            "premium_minus_mass_1d_pct": internal_d.get("premium_minus_mass_1d_pct"),
        }
        if nb.get("ok"):
            up = nb.get("advancers")
            down = nb.get("decliners")
            if isinstance(up, int) and isinstance(down, int):
                northbound_proxy["stock_connect_breadth"] = up - down
            if (nb.get("net_buy_amt") in (0, 0.0) and nb.get("net_inflow") in (0, 0.0)) or not nb.get("ok"):
                northbound_proxy["status"] = "proxy_used_due_to_invalid_or_missing_truth"
            else:
                northbound_proxy["status"] = "truth_plus_proxy_context"
        else:
            northbound_proxy["status"] = "proxy_used_due_to_missing_truth"
        out["a_share"]["northbound_proxy"] = northbound_proxy

    # Persist successful series for future fallback before stripping output payload.
    save_cache(flat)

    # Remove raw close arrays from output payload to keep output compact.
    for item in flat.values():
        if isinstance(item, dict):
            item.pop("series_close", None)

    for sid in FRED_SERIES:
        out["fred"][sid] = fred_latest(sid)
        time.sleep(0.1)

    f = out["fred"]
    if f.get("WALCL", {}).get("ok") and f.get("RRPONTSYD", {}).get("ok") and f.get("WTREGEN", {}).get("ok"):
        out["derived"]["net_liquidity_proxy_WALCL_minus_RRP_minus_TGA_mn_usd"] = (
            f["WALCL"]["value"] - f["RRPONTSYD"]["value"] - f["WTREGEN"]["value"]
        )

    if f.get("DGS10", {}).get("ok") and f.get("DGS2", {}).get("ok"):
        out["derived"]["curve_10y_minus_2y_pct_pts"] = f["DGS10"]["value"] - f["DGS2"]["value"]

    if f.get("M2SL", {}).get("ok") and f.get("GDP", {}).get("ok") and f["GDP"]["value"] != 0:
        out["derived"]["m2_to_gdp_ratio"] = f["M2SL"]["value"] / f["GDP"]["value"]

    # Fundamental-validation proxy for cases where daily earnings-revision breadth is unavailable.
    if all(f.get(s, {}).get("ok") for s in ["CP", "ULCNFB", "OPHNFB"]):
        out["derived"]["fundamental_validation_proxy"] = {
            "corporate_profits": {
                "value": f["CP"].get("value"),
                "chg": f["CP"].get("chg"),
            },
            "unit_labor_costs": {
                "value": f["ULCNFB"].get("value"),
                "chg": f["ULCNFB"].get("chg"),
            },
            "productivity": {
                "value": f["OPHNFB"].get("value"),
                "chg": f["OPHNFB"].get("chg"),
            },
            "sector_ratios": {
                "xly_xlp": out["ratios"].get("XLY_XLP"),
                "smh_spy": out["ratios"].get("SMH_SPY"),
            },
        }

    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Stanley workflow panel snapshot")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    parser.add_argument("--output", help="Write output JSON to file path")
    parser.add_argument("--pause", type=float, default=0.25, help="Pause seconds between symbol calls")
    parser.add_argument(
        "--finshare-mode",
        choices=["first", "auto", "off"],
        default=None,
        help="finshare adapter mode: first (prefer finshare), auto (fallback after Yahoo), or off",
    )
    args = parser.parse_args()

    data = build_snapshot(pause_s=args.pause, finshare_mode=args.finshare_mode)
    text = json.dumps(data, ensure_ascii=False, indent=2 if args.pretty else None)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + ("\n" if not text.endswith("\n") else ""), encoding="utf-8")

    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
