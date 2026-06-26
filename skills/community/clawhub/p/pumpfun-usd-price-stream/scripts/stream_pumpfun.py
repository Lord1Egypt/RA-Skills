"""
Bitquery PumpFun Token Feed — Real-time streaming with USD pricing
==================================================================
Subscribe to the Bitquery WebSocket API for a live PumpFun token feed on Solana.

Every tick delivers USD-quoted pricing for every active PumpFun token:
  - USD OHLC (Open, High, Low, Close) — reference for entry/exit/stop-loss
  - USD Volume — whale activity and momentum signal
  - USD Moving Averages (Mean, SMA, EMA, WMA) — trend and momentum analysis
  - Tick-to-tick USD % change — pump/dump detection

Filters for Solana network tokens whose address contains "pump" (PumpFun tokens).
Price.IsQuotedInUsd = true for all tokens in this feed — no conversion needed.

Trader use cases served by this stream:
  1. Entry/exit signal detection (EMA/SMA crossover in USD)
  2. Momentum & pump detection (USD % change spike + volume surge)
  3. Scalping (1-second USD OHLC bars)
  4. Stop-loss / take-profit monitoring (USD close vs threshold)
  5. Volume spike / whale alert (USD volume per tick)
  6. Multi-token USD price dashboard (all PumpFun tokens at once)
  7. Mean reversion (USD close vs USD mean divergence)
  8. Token launch monitoring (first tick = new PumpFun token live)

Usage:
    python scripts/stream_pumpfun.py
    python scripts/stream_pumpfun.py --timeout 60

Environment:
    BITQUERY_API_KEY — Your Bitquery token (required). Passed as ?token= in WebSocket URL.
"""

import asyncio
import os
import sys
from urllib.parse import urlencode

from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport


BITQUERY_WS_BASE = "wss://streaming.bitquery.io/graphql"

PUMPFUN_TOKEN_SUBSCRIPTION = gql("""
subscription PumpFunTokenFeed {
  Trading {
    Tokens(
      where: {
        Interval: {Time: {Duration: {eq: 1}}},
        Token: {
          NetworkBid: {},
          Network: {is: "Solana"},
          Address: {includesCaseInsensitive: "pump"}
        }
      }
    ) {
      Token {
        Address
        Id
        IsNative
        Name
        Network
        Symbol
        TokenId
      }
      Block {
        Date
        Time
        Timestamp
      }
      Interval {
        Time {
          Start
          Duration
          End
        }
      }
      Volume {
        Base
        Quote
        Usd
      }
      Price {
        IsQuotedInUsd
        Ohlc {
          Close
          High
          Low
          Open
        }
        Average {
          ExponentialMoving
          Mean
          SimpleMoving
          WeightedSimpleMoving
        }
      }
    }
  }
}
""")


def get_api_key() -> str:
    """Read the Bitquery API key from the environment. Raises if not set."""
    key = os.getenv("BITQUERY_API_KEY")
    if not key:
        raise EnvironmentError(
            "BITQUERY_API_KEY is not set. "
            "Please export your Bitquery token:\n"
            "  export BITQUERY_API_KEY=your_token_here"
        )
    return key


def _fmt_price(value) -> str:
    """Format a price value, handling very small numbers (common for meme coins)."""
    if value is None:
        return "N/A"
    try:
        f = float(value)
        # Use scientific notation for very small values
        if 0 < abs(f) < 0.0001:
            return f"${f:.8f}"
        return f"${f:,.6f}"
    except (ValueError, TypeError):
        return str(value)


def _fmt_volume(value) -> str:
    """Format a volume in USD."""
    if value is None:
        return "N/A"
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return str(value)


def _trader_signals(close_f: float | None, avg: dict, prev_close: float | None, vol_usd_f: float | None) -> list[str]:
    """Derive simple trader signal hints from USD price data on the stream."""
    signals = []
    if close_f is None:
        return signals

    # EMA vs SMA momentum signal
    ema = avg.get("ExponentialMoving")
    sma = avg.get("SimpleMoving")
    if ema is not None and sma is not None:
        try:
            ema_f, sma_f = float(ema), float(sma)
            if ema_f > sma_f:
                signals.append("📈 EMA > SMA  → bullish USD momentum")
            elif ema_f < sma_f:
                signals.append("📉 EMA < SMA  → bearish USD momentum")
        except (ValueError, TypeError):
            pass

    # Mean reversion signal
    mean = avg.get("Mean")
    if mean is not None:
        try:
            mean_f = float(mean)
            if mean_f != 0:
                deviation_pct = ((close_f - mean_f) / mean_f) * 100
                if deviation_pct > 5:
                    signals.append(f"⚠️  USD Close is {deviation_pct:+.1f}% above Mean  → possible mean reversion down")
                elif deviation_pct < -5:
                    signals.append(f"⚠️  USD Close is {deviation_pct:+.1f}% below Mean  → possible mean reversion up")
        except (ValueError, TypeError):
            pass

    # Tick-to-tick USD % change (pump/dump detection)
    if prev_close is not None and prev_close != 0:
        pct = ((close_f - prev_close) / prev_close) * 100
        if abs(pct) >= 10:
            direction = "🚀 PUMP" if pct > 0 else "💥 DUMP"
            signals.append(f"{direction} detected: {pct:+.2f}% USD change this tick")

    return signals


def format_tick(data: dict, prev_close: float | None) -> str:
    """Format one subscription tick with USD pricing prominently displayed."""
    trading = (data or {}).get("Trading") or {}
    tokens = trading.get("Tokens") or []
    if not tokens:
        return ""

    t = tokens[0]
    token = t.get("Token", {})
    block = t.get("Block", {})
    volume = t.get("Volume", {})
    price = t.get("Price", {})
    ohlc = price.get("Ohlc", {})
    avg = price.get("Average", {})
    is_usd = price.get("IsQuotedInUsd", True)

    name = token.get("Name") or "Unknown"
    symbol = token.get("Symbol") or "???"
    address = token.get("Address") or "N/A"
    network = token.get("Network", "Solana")
    ts = block.get("Time", block.get("Date", "?"))
    usd_label = " [USD]" if is_usd else ""

    # Truncate long addresses for display
    addr_display = address if len(address) <= 20 else f"{address[:8]}...{address[-8:]}"

    close = ohlc.get("Close")
    try:
        close_f = float(close) if close is not None else None
    except (ValueError, TypeError):
        close_f = None

    vol_usd = volume.get("Usd")
    try:
        vol_usd_f = float(vol_usd) if vol_usd is not None else None
    except (ValueError, TypeError):
        vol_usd_f = None

    sep = "━" * 52

    # Tick-to-tick USD % change
    pct_str = ""
    if prev_close is not None and close_f is not None and prev_close != 0:
        pct = ((close_f - prev_close) / prev_close) * 100
        pct_str = f"   Tick Δ: {pct:+.4f}% USD"

    lines = [
        sep,
        f"PumpFun: {symbol}  ({addr_display})  [{network}]{usd_label}",
        f"Time: {ts}",
        sep,
        f"USD Price  │  Open:  {_fmt_price(ohlc.get('Open'))}   High: {_fmt_price(ohlc.get('High'))}",
        f"           │  Low:   {_fmt_price(ohlc.get('Low'))}   Close: {_fmt_price(close)}  ← entry/exit ref{pct_str}",
    ]

    # USD moving averages (Bitquery-provided)
    if avg:
        lines.append("USD Averages")
        if avg.get("Mean") is not None:
            lines.append(f"  Mean:    {_fmt_price(avg.get('Mean'))}")
        if avg.get("SimpleMoving") is not None:
            lines.append(f"  SMA:     {_fmt_price(avg.get('SimpleMoving'))}")
        if avg.get("ExponentialMoving") is not None:
            lines.append(f"  EMA:     {_fmt_price(avg.get('ExponentialMoving'))}")
        if avg.get("WeightedSimpleMoving") is not None:
            lines.append(f"  WMA:     {_fmt_price(avg.get('WeightedSimpleMoving'))}")

    # USD volume (whale / momentum signal)
    if vol_usd_f is not None:
        vol_note = ""
        if vol_usd_f >= 10_000:
            vol_note = "  ← 🐳 high USD volume"
        elif vol_usd_f >= 1_000:
            vol_note = "  ← elevated USD volume"
        lines.append(f"\nUSD Volume:  {_fmt_volume(vol_usd)}{vol_note}")

    # Trader signal hints derived from USD data
    signals = _trader_signals(close_f, avg, prev_close, vol_usd_f)
    if signals:
        lines.append("\nTrader Signals:")
        for s in signals:
            lines.append(f"  {s}")

    lines.append("")
    return "\n".join(lines)


async def run_stream(timeout_seconds: int | None = None) -> None:
    api_key = get_api_key()
    url = f"{BITQUERY_WS_BASE}?{urlencode({'token': api_key})}"
    transport = WebsocketsTransport(
        url=url,
        headers={"Sec-WebSocket-Protocol": "graphql-ws"},
    )

    prev_close: float | None = None
    tick_count = 0

    async with Client(transport=transport) as session:
        print("Connected. Streaming PumpFun token feed (Solana, 1s ticks). Ctrl+C to stop.\n")

        async def consume():
            nonlocal prev_close, tick_count
            try:
                async for result in session.subscribe(PUMPFUN_TOKEN_SUBSCRIPTION):
                    tick_count += 1
                    out = format_tick(result, prev_close)
                    if out:
                        print(out)
                        # Track close for next tick % change
                        trading = (result or {}).get("Trading") or {}
                        tokens = trading.get("Tokens") or []
                        if tokens:
                            close = (tokens[0].get("Price") or {}).get("Ohlc") or {}
                            c = close.get("Close")
                            if c is not None:
                                try:
                                    prev_close = float(c)
                                except (ValueError, TypeError):
                                    pass
            except asyncio.CancelledError:
                pass

        if timeout_seconds is not None:
            try:
                await asyncio.wait_for(consume(), timeout=float(timeout_seconds))
            except asyncio.TimeoutError:
                print(f"\nStopped after {timeout_seconds}s ({tick_count} ticks).")
        else:
            await consume()


def main() -> None:
    timeout: int | None = None
    if len(sys.argv) > 1 and sys.argv[1] == "--timeout" and len(sys.argv) > 2:
        try:
            timeout = int(sys.argv[2])
        except ValueError:
            print("Usage: python stream_pumpfun.py [--timeout SECONDS]", file=sys.stderr)
            sys.exit(2)

    try:
        asyncio.run(run_stream(timeout_seconds=timeout))
    except EnvironmentError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStream stopped by user.")


if __name__ == "__main__":
    main()
