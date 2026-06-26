---
name: ta-radar
version: 1.2.0
description: >
  Multi-Dimensional Technical Analysis Radar for cryptocurrencies. Supports spot trading pairs (Binance/Gate.io)
  and on-chain contract addresses (via DexScreener proxy). Generates objective TA reports including EMA,
  RSI, MACD, Bollinger Bands, support/resistance levels and trend analysis.
author: ClawHub Community
requires: [python3]
metadata:
  repository: https://github.com/clawhub/ta-radar
  install:
    type: python
    command: pip install -r requirements.txt
  env:
    - name: TA_SYMBOL
      description: Trading pair (e.g. BTCUSDT) or on-chain contract address (0x...)
      required: true
      sensitive: false
    - name: TA_INTERVAL
      description: Timeframe for analysis, supports 1h / 4h / 1d
      required: false
      sensitive: false
      default: "1h"
tags:
  - crypto
  - trading
  - technical-analysis
  - defi
  - binance
  - gateio
  - dexscreener
---

# TA Radar (Multi-Dimensional Technical Analysis Radar)

## Overview

This skill provides zero-dependency technical analysis for cryptocurrency assets, supporting two input types:

- **Spot Trading Pairs** (e.g. `BTC`, `ETHUSDT`): Fetches K-line data first from Binance official mirror (`api.binance.info`), automatically falls back to Gate.io API (`api.gateio.ws`) if Binance is unreachable (e.g. network restrictions in mainland China).
- **On-Chain Contract Addresses** (starts with `0x`): Resolves the base token symbol via DexScreener through the `allorigins.win` public proxy, then queries exchange K-line data using the resolved symbol.

> **GFW Compatibility**: Gate.io API is used as an automatic fallback to ensure availability for users in mainland China when Binance endpoints are blocked. DexScreener is accessed through a public proxy to avoid direct network restrictions.

> **v1.2 Updates**
> - **[NEW] Dual Data Source Fallback**: Gate.io added as backup K-line data source, automatic failover from Binance with zero user interaction.
> - **[NEW] Beginner-Friendly Annotations**: Each indicator conclusion includes plain language explanations, no financial background required to understand signals.

---

## Agent Execution Workflow

When the skill is triggered by a user request, follow these steps strictly:

### Step 1: Parse User Parameters

Extract the following parameters from user input:

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `SYMBOL` | Trading pair ticker (e.g. `BTCUSDT`) or on-chain contract address (e.g. `0xabc123...`) | **Required** |
| `INTERVAL` | Timeframe for analysis, allowed values: `1h`, `4h`, `1d` | `1h` |

**Automatic Routing (handled internally by the script, no agent action needed):**
- If input starts with `0x` → resolve symbol via DexScreener first, then fetch K-line data via dual source logic
- Otherwise → directly fetch K-line data via dual source logic, auto append `USDT` suffix if missing

---

### Step 2: Write Python Script to Temporary File

Save the complete Python code from the **Embedded Script** section below to:

```
/tmp/ta_radar_run.py
```

Use bash heredoc for writing:

```bash
cat > /tmp/ta_radar_run.py << 'PYEOF'
<PASTE COMPLETE PYTHON SCRIPT HERE>
PYEOF
```

---

### Step 3: Execute Script and Capture Output

```bash
TA_SYMBOL="<SYMBOL>" TA_INTERVAL="<INTERVAL>" python3 /tmp/ta_radar_run.py
```

- **Success (exit code 0)**: Present the full standard output of the script to the user exactly as-is, no trimming or summarization.
- **Failure (exit code non-0)**: Present the standard error output to the user and prompt to check parameter format.

---

### Step 4: Clean Up Temporary File

```bash
rm -f /tmp/ta_radar_run.py
```

---

## Embedded Script

> Full Python 3 script with zero third-party dependencies, all indicator calculations implemented manually using built-in libraries.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TA Radar v1.2
Zero-dependency TA engine: EMA / RSI / MACD / Bollinger Bands
Data sources: Binance (api.binance.info) first, auto fallback to Gate.io (api.gateio.ws)
DEX contract resolution: DexScreener via allorigins public proxy

Changelog v1.2:
  [NEW-1] Dual data source fallback: fetch_klines() encapsulates Binance + Gate.io logic,
          any Binance error (HTTP/Timeout/URLError) automatically switches to Gate.io,
          warning is rendered only if both sources fail.
  [NEW-2] Beginner-friendly annotations: Each indicator conclusion includes
          plain language explanation of signal meaning, no jargon or metaphors.
"""

import os
import sys
import json
import math
import socket
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, UTC

# ─────────────────────────────────────────────
#  Environment Variables
# ─────────────────────────────────────────────
SYMBOL   = os.environ.get("TA_SYMBOL", "").strip()
INTERVAL = os.environ.get("TA_INTERVAL", "1h").strip().lower()
LIMIT    = 300 # Sufficient historical data for accurate EMA/MACD convergence

VALID_INTERVALS = {"1h", "4h", "1d"}


# ─────────────────────────────────────────────
#  Network Request: Returns (data, error_msg) tuple
# ─────────────────────────────────────────────

def safe_fetch(url: str, timeout: int = 12):
    """
    Perform HTTP GET request, returns (parsed_json, error_msg) tuple.

    Success:  (dict|list, None)
    Failure:  (None, error string)
      - HTTP error   → "HTTP {code}: {msg}"
      - Timeout      → "Timeout ({n}s): {base_url}"
      - URLError     → "URLError: {reason}"
      - JSON error   → "JSONDecodeError: {detail}"
      - Other        → "UnexpectedError: {type}: {msg}"
    """
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 ta-radar/1.2"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
        try:
            return json.loads(raw), None
        except json.JSONDecodeError as e:
            return None, f"JSONDecodeError: {e}"

    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8")
            detail = json.loads(body).get("msg", body[:200])
        except Exception:
            detail = str(e.reason)
        return None, f"HTTP {e.code}: {detail}"

    except urllib.error.URLError as e:
        reason = str(e.reason)
        base = url.split("?")[0]
        if "timed out" in reason.lower() or isinstance(e.reason, socket.timeout):
            return None, f"Timeout ({timeout}s): {base}"
        return None, f"URLError: {reason}"

    except socket.timeout:
        return None, f"Timeout ({timeout}s): {url.split('?')[0]}"

    except Exception as e:
        return None, f"UnexpectedError: {type(e).__name__}: {e}"


# ─────────────────────────────────────────────
#  Input Validation
# ─────────────────────────────────────────────

def validate_inputs():
    if not SYMBOL:
        print("❌ Error: TA_SYMBOL environment variable not provided. Specify a trading pair or contract address.", file=sys.stderr)
        sys.exit(1)
    if INTERVAL not in VALID_INTERVALS:
        print(
            f"❌ Error: Unsupported timeframe '{INTERVAL}'. Use 1h / 4h / 1d.",
            file=sys.stderr
        )
        sys.exit(1)


# ─────────────────────────────────────────────
#  Data Fetching Layer
# ─────────────────────────────────────────────

def is_contract_address(s: str) -> bool:
    """Check if input is an on-chain contract address: starts with 0x and length >=10."""
    return s.startswith("0x") and len(s) >= 10


def fetch_binance_klines(symbol: str, interval: str, limit: int):
    """
    Fetch closing price list from Binance official mirror.
    Endpoint: api.binance.info
    Returns (closes: list | None, error_msg: str | None).
    """
    sym = symbol.strip().upper()
    if not sym.endswith("USDT"):
        sym += "USDT"

    url = (
        f"https://api.binance.info/api/v3/klines"
        f"?symbol={sym}&interval={interval}&limit={limit}"
    )
    data, err = safe_fetch(url)

    if err:
        return None, f"Binance [{sym}] → {err}"
    if not isinstance(data, list) or len(data) == 0:
        return None, f"Binance [{sym}] returned empty or invalid data"
    try:
        closes = [float(c[4]) for c in data]
    except (IndexError, ValueError, TypeError) as e:
        return None, f"Binance [{sym}] K-line parse error: {e}"
    if len(closes) < 26:
        return None, f"Binance [{sym}] insufficient K-line data ({len(closes)} bars, minimum 26 required)"

    return closes, None


def fetch_gate_klines(symbol: str, interval: str, limit: int):
    """
    Fetch closing price list from Gate.io as fallback data source.
    Endpoint: api.gateio.ws (accessible in mainland China)
    Gate.io K-line interval mapping: 1h -> 1h, 4h -> 4h, 1d -> 1d
    Returns (closes: list | None, error_msg: str | None).
    """
    sym = symbol.strip().upper()
    if not sym.endswith("USDT"):
        sym += "USDT"

    # Gate.io pair format: BTC_USDT (underscore separated)
    gate_pair = sym[:-4] + "_USDT"

    url = (
        f"https://api.gateio.ws/api/v4/spot/candlesticks"
        f"?currency_pair={urllib.parse.quote(gate_pair)}"
        f"&interval={interval}&limit={limit}"
    )
    data, err = safe_fetch(url)

    if err:
        return None, f"Gate.io [{gate_pair}] → {err}"
    if not isinstance(data, list) or len(data) == 0:
        return None, f"Gate.io [{gate_pair}] returned empty or invalid data"

    # Gate.io candlestick format (v4):
    # [timestamp, volume, close, high, low, open, ...]
    # Close price at index 2
    try:
        closes = [float(c[2]) for c in data]
    except (IndexError, ValueError, TypeError) as e:
        return None, f"Gate.io [{gate_pair}] K-line parse error: {e}"

    if len(closes) < 26:
        return None, f"Gate.io [{gate_pair}] insufficient K-line data ({len(closes)} bars, minimum 26 required)"

    return closes, None


def fetch_klines(symbol: str, interval: str, limit: int):
    """
    Dual data source K-line entry point.
    Tries Binance first, automatically falls back to Gate.io on failure.
    Returns (closes: list | None, source_name: str, debug_msgs: list).
      - closes = None means both sources failed.
      - source_name = name of the data source actually used, for report header.
      - debug_msgs = collection of error messages from each step.
    """
    debug_msgs = []

    # Try Binance
    closes, binance_err = fetch_binance_klines(symbol, interval, limit)
    if closes is not None:
        return closes, "Binance", debug_msgs

    debug_msgs.append(f"Binance unavailable: {binance_err}")
    print(f"  ⚠  Binance data source unavailable, switching to Gate.io...\n")

    # Fallback to Gate.io
    closes, gate_err = fetch_gate_klines(symbol, interval, limit)
    if closes is not None:
        return closes, "Gate.io", debug_msgs

    debug_msgs.append(f"Gate.io unavailable: {gate_err}")
    return None, "", debug_msgs


def resolve_symbol_from_dex(address: str):
    """
    Resolve baseToken.symbol and pair label from contract address via DexScreener through allorigins proxy.
    Returns (base_symbol: str | None, pair_label: str, error_msg: str | None).
    """
    dex_url = (
        f"https://api.dexscreener.com/latest/dex/search"
        f"?q={urllib.parse.quote(address)}"
    )
    proxy_url = (
        f"https://api.allorigins.win/raw"
        f"?url={urllib.parse.quote(dex_url)}"
    )

    data, err = safe_fetch(proxy_url, timeout=18)

    if err:
        return None, "", f"DexScreener proxy request failed → {err}"
    if not isinstance(data, dict):
        return None, "", f"DexScreener returned invalid format (expected dict, got {type(data).__name__})"

    pairs = data.get("pairs")
    if not pairs or not isinstance(pairs, list) or len(pairs) == 0:
        return None, "", f"DexScreener found no pairs for address {address[:20]}..."

    def get_liq(p):
        try:
            return float(p.get("liquidity", {}).get("usd", 0) or 0)
        except (TypeError, ValueError):
            return 0.0

    top = sorted(pairs, key=get_liq, reverse=True)[0]
    base_symbol  = (top.get("baseToken", {}).get("symbol") or "").strip().upper()
    quote_symbol = top.get("quoteToken", {}).get("symbol", "?")
    dex_id       = top.get("dexId", "?")
    chain_id     = top.get("chainId", "?")
    liq_usd      = get_liq(top)

    pair_label = (
        f"{base_symbol}/{quote_symbol} on {dex_id} "
        f"(chain={chain_id}, liq=${liq_usd:,.0f})"
    )

    if not base_symbol:
        return None, pair_label, "DexScreener returned empty baseToken.symbol"

    return base_symbol, pair_label, None


# ─────────────────────────────────────────────
#  Pure Python Technical Indicators (zero dependencies)
# ─────────────────────────────────────────────

def calc_ema(prices: list, period: int) -> list:
    """Exponential Moving Average (EMA). First value is SMA, k = 2 / (period+1)."""
    if len(prices) < period:
        return []
    k = 2.0 / (period + 1)
    result = [sum(prices[:period]) / period]
    for p in prices[period:]:
        result.append(p * k + result[-1] * (1 - k))
    return result


def calc_rsi(prices: list, period: int = 14):
    """Relative Strength Index (RSI), Wilder's smoothing method. Returns latest value, None if insufficient data."""
    if len(prices) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        d = prices[i] - prices[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    ag = sum(gains[:period]) / period
    al = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        ag = (ag * (period - 1) + gains[i]) / period
        al = (al * (period - 1) + losses[i]) / period
    if al == 0:
        return 100.0
    return 100.0 - (100.0 / (1 + ag / al))


def calc_macd(prices: list, fast: int = 12, slow: int = 26, signal: int = 9):
    """Moving Average Convergence Divergence (MACD). Returns (dif, dea, hist) latest values, None if insufficient data."""
    ef = calc_ema(prices, fast)
    es = calc_ema(prices, slow)
    if not ef or not es:
        return None
    offset = len(ef) - len(es)
    dif_series = [f - s for f, s in zip(ef[offset:], es)]
    if len(dif_series) < signal:
        return None
    dea_series = calc_ema(dif_series, signal)
    if not dea_series:
        return None
    dif  = dif_series[-1]
    dea  = dea_series[-1]
    return dif, dea, dif - dea


def calc_bollinger(prices: list, period: int = 20, num_std: float = 2.0):
    """Bollinger Bands. Returns (upper, middle, lower) latest values, None if insufficient data."""
    if len(prices) < period:
        return None
    w = prices[-period:]
    mid = sum(w) / period
    std = math.sqrt(sum((p - mid) ** 2 for p in w) / period)
    return mid + num_std * std, mid, mid - num_std * std


# ─────────────────────────────────────────────
#  Formatting Utilities
# ─────────────────────────────────────────────

def fmt(val: float) -> str:
    """Format price, automatically adapts to magnitude."""
    if val == 0:
        return "0"
    a = abs(val)
    if a >= 1000:  return f"{val:,.2f}"
    elif a >= 1:   return f"{val:.4f}"
    elif a >= 0.01: return f"{val:.6f}"
    else:           return f"{val:.8f}"


# ─────────────────────────────────────────────
#  [NEW-2] Beginner-Friendly Explanation Library
#  Each explanation is objective, plain language, no metaphors or jargon.
# ─────────────────────────────────────────────

EMA_EXPLAIN = {
    "bull": "Short-term EMA above long-term EMA indicates recent price strength.",
    "bear": "Short-term EMA below long-term EMA indicates recent price weakness.",
    "flat": "Mixed EMA alignment indicates sideways consolidation, no clear trend.",
}

RSI_EXPLAIN = {
    "ob":  "RSI above 70 indicates recent large gains, potential short-term pullback risk.",
    "os":  "RSI below 30 indicates recent large losses, potential short-term bounce opportunity.",
    "mid": "RSI between 30-70 indicates normal momentum, neutral signal.",
}

MACD_EXPLAIN = {
    "bull_above": "MACD above signal line and zero line indicates strong upward momentum.",
    "bear_below": "MACD below signal line and zero line indicates strong downward momentum.",
    "bull_below": "MACD crossed above signal line but still below zero line, improving momentum but not confirmed.",
    "bear_above": "MACD crossed below signal line but still above zero line, weakening momentum, monitor closely.",
}

BOLL_EXPLAIN = {
    "near_upper": "Price near upper Bollinger Band indicates limited upside potential, watch for resistance.",
    "near_lower": "Price near lower Bollinger Band indicates statistical support area, watch for bounce.",
    "squeeze":    "Narrow Bollinger Band width indicates low volatility, often precursor to directional move.",
    "mid_above":  "Price above middle Bollinger Band indicates short-term relative strength.",
    "mid_below":  "Price below middle Bollinger Band indicates short-term relative weakness.",
}


# ─────────────────────────────────────────────
#  Report Rendering
# ─────────────────────────────────────────────

def render_report(
    display_sym: str,
    interval: str,
    closes: list,
    data_source: str = "Binance",
    source_note: str = "",
):
    price = closes[-1]
    ts    = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    # ── Calculate Indicators ──────────────────────────
    ema7_s  = calc_ema(closes, 7)
    ema25_s = calc_ema(closes, 25)
    ema99_s = calc_ema(closes, 99)
    rsi     = calc_rsi(closes, 14)
    macd_r  = calc_macd(closes)
    boll_r  = calc_bollinger(closes, 20)

    ema7_v  = ema7_s[-1]  if ema7_s  else None
    ema25_v = ema25_s[-1] if ema25_s else None
    ema99_v = ema99_s[-1] if ema99_s else None

    # ── Trend Signals ──────────────────────────────
    ema_bull   = bool(ema7_v and ema25_v and ema99_v and ema7_v > ema25_v > ema99_v)
    ema_bear   = bool(ema7_v and ema25_v and ema99_v and ema7_v < ema25_v < ema99_v)
    rsi_ob     = rsi is not None and rsi > 70
    rsi_os     = rsi is not None and rsi < 30
    macd_bull  = bool(macd_r and macd_r[0] > 0 and macd_r[2] > 0)
    macd_bear  = bool(macd_r and macd_r[0] < 0 and macd_r[2] < 0)
    boll_up    = bool(boll_r and price > boll_r[1])
    near_upper = bool(boll_r and price >= boll_r[0] * 0.995)
    near_lower = bool(boll_r and price <= boll_r[2] * 1.005)
    boll_squeeze = bool(boll_r and (boll_r[0] - boll_r[2]) / boll_r[1] * 100 < 5)

    # ── Composite Trend Voting ──────────────────────────
    bull_votes = sum([
        ema_bull,
        macd_bull,
        boll_up,
        rsi is not None and 40 <= rsi <= 60,
    ])
    bear_votes = sum([
        ema_bear,
        macd_bear,
        not boll_up and boll_r is not None,
        rsi_ob,
    ])

    if bull_votes >= 3:
        trend_label = "Bullish (Bulls in control)"
    elif bear_votes >= 3:
        trend_label = "Bearish (Bears in control)"
    elif bull_votes == bear_votes:
        trend_label = "Neutral (Range bound)"
    elif bull_votes > bear_votes:
        trend_label = "Neutral (Slightly bullish)"
    else:
        trend_label = "Neutral (Slightly bearish)"

    # ── Support / Resistance Levels ─────────────────────────
    sup, res = [], []
    if boll_r:
        ub, mb, lb = boll_r
        (sup if lb < price else res).append(("Lower Bollinger", lb))
        (sup if mb < price else res).append(("Middle Bollinger", mb))
        (res if ub > price else sup).append(("Upper Bollinger", ub))
    if ema25_v:
        (sup if ema25_v < price else res).append(("EMA25", ema25_v))
    if ema99_v:
        (sup if ema99_v < price else res).append(("EMA99", ema99_v))

    sup = sorted(sup, key=lambda x: x[1], reverse=True)[:3]
    res = sorted(res, key=lambda x: x[1])[:3]

    def fmt_levels(lvls):
        if not lvls:
            return "No valid levels available"
        return "  /  ".join(f"{n} {fmt(v)}" for n, v in lvls)

    # ── Composite Analysis Text ──────────────────────────
    parts = []

    if ema7_v and ema25_v and ema99_v:
        if ema_bull:
            parts.append(
                f"EMA alignment is bullish (EMA7 {fmt(ema7_v)} > EMA25 {fmt(ema25_v)} > "
                f"EMA99 {fmt(ema99_v)}), indicating an established uptrend structure."
            )
        elif ema_bear:
            parts.append(
                f"EMA alignment is bearish (EMA7 {fmt(ema7_v)} < EMA25 {fmt(ema25_v)} < "
                f"EMA99 {fmt(ema99_v)}), indicating an established downtrend structure."
            )
        else:
            parts.append(
                f"EMA alignment is mixed (EMA7 {fmt(ema7_v)}, EMA25 {fmt(ema25_v)}, "
                f"EMA99 {fmt(ema99_v)}), indicating sideways consolidation with no clear directional signal."
            )

    if rsi is not None:
        if rsi_ob:
            parts.append(
                f"RSI reading is {rsi:.1f}, in overbought territory (threshold 70). "
                f"Short-term momentum is overextended, potential for pullback or consolidation."
            )
        elif rsi_os:
            parts.append(
                f"RSI reading is {rsi:.1f}, in oversold territory (threshold 30). "
                f"Short-term momentum is excessively negative, potential for technical bounce."
            )
        else:
            parts.append(
                f"RSI reading is {rsi:.1f}, in neutral territory (between 30 and 70). "
                f"Current momentum is not extreme."
            )

    if macd_r:
        dif, dea, hist = macd_r
        if dif > dea and dif > 0:
            parts.append(
                f"MACD line ({fmt(dif)}) is above signal line ({fmt(dea)}) and both are above zero line. "
                f"Histogram is positive ({fmt(hist)}), confirming upward momentum, golden cross valid."
            )
        elif dif < dea and dif < 0:
            parts.append(
                f"MACD line ({fmt(dif)}) is below signal line ({fmt(dea)}) and both are below zero line. "
                f"Histogram is negative ({fmt(hist)}), confirming downward momentum, death cross valid."
            )
        elif dif > dea:
            parts.append(
                f"MACD line ({fmt(dif)}) has crossed above signal line ({fmt(dea)}) but remains below zero line. "
                f"Histogram turned positive ({fmt(hist)}), momentum is improving but not yet confirmed above zero."
            )
        else:
            parts.append(
                f"MACD line ({fmt(dif)}) has crossed below signal line ({fmt(dea)}) but remains above zero line. "
                f"Histogram turned negative ({fmt(hist)}), upward momentum is weakening, direction pending confirmation."
            )

    if boll_r:
        ub, mb, lb = boll_r
        bw = (ub - lb) / mb * 100
        if near_upper:
            parts.append(
                f"Current price ({fmt(price)}) is near or touching upper Bollinger Band ({fmt(ub)}). "
                f"Band width is {bw:.1f}%, statistical resistance overhead, watch for volume confirmation on breakout attempts."
            )
        elif near_lower:
            parts.append(
                f"Current price ({fmt(price)}) is near or touching lower Bollinger Band ({fmt(lb)}). "
                f"Band width is {bw:.1f}%, near statistical support area, watch for bounce confirmation at this level."
            )
        elif boll_squeeze:
            parts.append(
                f"Bollinger Band width has narrowed to {bw:.1f}%, price is in low volatility consolidation phase. "
                f"This pattern typically precedes a directional expansion, monitor volume for breakout direction clues."
            )
        else:
            pos = "above" if price > mb else "below"
            parts.append(
                f"Current price ({fmt(price)}) is {pos} middle Bollinger Band ({fmt(mb)}). "
                f"Band width is {bw:.1f}%, volatility is within normal range."
            )

    analysis_text = "\n".join(f"  {p}" for p in parts)

    # ── Print Report ────────────────────────
    SEP = "─" * 60
    EQ  = "═" * 60

    print(f"\n{EQ}")
    print(f"  TA Radar v1.2  |  {display_sym}  |  {interval.upper()}")
    print(f"  Data Source: {data_source}" + (f"  |  {source_note}" if source_note else ""))
    print(f"  Generated: {ts}")
    print(f"{EQ}\n")

    # ── Core Data Panel ──────────────────────
    print("【Core Data Panel】")
    print(SEP)
    print(f"  Current Price  : {fmt(price)}")
    print()

    # EMA
    print("  ▸ EMA (7 / 25 / 99)")
    if ema7_v and ema25_v and ema99_v:
        if ema_bull:
            label   = "Bullish alignment ↑"
            explain = EMA_EXPLAIN["bull"]
        elif ema_bear:
            label   = "Bearish alignment ↓"
            explain = EMA_EXPLAIN["bear"]
        else:
            label   = "Mixed alignment ↔"
            explain = EMA_EXPLAIN["flat"]
        print(f"    EMA7  = {fmt(ema7_v)}")
        print(f"    EMA25 = {fmt(ema25_v)}")
        print(f"    EMA99 = {fmt(ema99_v)}")
        print(f"    Conclusion  : {label}")
        print(f"    Explanation : {explain}")
    else:
        print("    Insufficient data to calculate")
    print()

    # RSI
    print("  ▸ RSI (14)")
    if rsi is not None:
        if rsi_ob:
            label   = "Overbought ⚠"
            explain = RSI_EXPLAIN["ob"]
        elif rsi_os:
            label   = "Oversold ⚠"
            explain = RSI_EXPLAIN["os"]
        else:
            label   = "Neutral ✓"
            explain = RSI_EXPLAIN["mid"]
        print(f"    RSI   = {rsi:.2f}")
        print(f"    Conclusion  : {label}")
        print(f"    Explanation : {explain}")
    else:
        print("    Insufficient data to calculate")
    print()

    # MACD
    print("  ▸ MACD (12 / 26 / 9)")
    if macd_r:
        dif, dea, hist = macd_r
        if dif > dea and dif > 0:
            label   = "Golden cross (above zero line) ↑"
            explain = MACD_EXPLAIN["bull_above"]
        elif dif < dea and dif < 0:
            label   = "Death cross (below zero line) ↓"
            explain = MACD_EXPLAIN["bear_below"]
        elif dif > dea:
            label   = "Golden cross (below zero line, pending confirmation) ↗"
            explain = MACD_EXPLAIN["bull_below"]
        else:
            label   = "Death cross (above zero line, weakening momentum) ↘"
            explain = MACD_EXPLAIN["bear_above"]
        print(f"    MACD Line  = {fmt(dif)}")
        print(f"    Signal Line = {fmt(dea)}")
        print(f"    Histogram   = {fmt(hist)}")
        print(f"    Conclusion  : {label}")
        print(f"    Explanation : {explain}")
    else:
        print("    Insufficient