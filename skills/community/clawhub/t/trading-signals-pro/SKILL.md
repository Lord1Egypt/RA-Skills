---
name: trading-signals-pro
description: Crypto trading signals using CoinGecko price data, DeFiLlama TVL trends, and CCXT exchange order flow — momentum, RSI, VWAP signals for XRP, HBAR, BTC, ETH, and DeFi tokens.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - COINGECKO_API_KEY
      bins:
        - python3
    primaryEnv: COINGECKO_API_KEY
    emoji: "📈"
    homepage: https://github.com/drivenautoplex1/openclaw-skills
    install:
      - kind: uv
        package: requests
        bins: []
      - kind: uv
        package: ccxt
        bins: []
---

# Trading Signals Skill

Get trading signals for crypto assets — momentum, mean reversion, DeFi yield arbitrage, and on-chain TVL trends.

## What this skill does

Analyze:
- **Price momentum** — 1h/4h/24h momentum scoring for any CoinGecko-listed token
- **RSI-style signals** — overbought/oversold detection from OHLCV data
- **VWAP signals** — price vs volume-weighted average (exchange data via ccxt)
- **DeFi yield scan** — highest-yield stablecoin pools, TVL momentum (DeFiLlama)
- **XRP/HBAR ecosystem** — SaucerSwap LP signal, staking yield vs market rate
- **Portfolio scan** — multi-asset signal dashboard for a watchlist

## Input contract

Tell me:
1. **Mode**: momentum / rsi / vwap / defi / portfolio / scan
2. **Asset(s)**: coin IDs (CoinGecko format: "bitcoin", "ripple", "hedera-hashgraph") or tickers
3. **Timeframe** (optional): 1h / 4h / 24h / 7d (default: 24h)
4. **Exchange** (optional for ccxt modes): binance / kraken / coinbase / kucoin (default: binance public)
5. **Threshold** (optional): signal sensitivity 1-10 (default: 5)

Example prompts:
- "Momentum signal for XRP and HBAR over last 24h"
- "RSI scan on BTC, ETH, XRP — flag anything overbought or oversold"
- "DeFi yield scan — best stablecoin yield right now"
- "Portfolio dashboard for: BTC, ETH, XRP, HBAR, MATIC"
- "VWAP signal for ETH on Binance 4h"
- "SaucerSwap LP scan — current HBAR pool yields"

## Output contract

Returns JSON + human-readable summary:

```json
{
  "timestamp": "2026-03-27T12:00:00Z",
  "signals": [
    {
      "asset": "XRP",
      "coingecko_id": "ripple",
      "price_usd": 0.523,
      "momentum_24h": "+8.2%",
      "momentum_7d": "+12.4%",
      "rsi_14": 62.3,
      "signal": "BULLISH",
      "strength": "MODERATE",
      "notes": "Breaking above 30-day MA. Volume spike on 4h. Watch $0.55 resistance."
    }
  ],
  "market_context": "Risk-on sentiment. BTC dominance declining — altcoin rotation in progress.",
  "top_picks": ["XRP", "HBAR"],
  "avoid": [],
  "defi_best_yield": {
    "pool": "USDC-Aave-V3-Ethereum",
    "apy": 8.4,
    "tvl_usd": "2.1B"
  }
}
```

## How the skill works

The skill calls `trade_signals.py` (included in this skill folder) which:

1. **CoinGecko API** — price history, market cap, volume, 24h change (free tier via COINGECKO_API_KEY or demo key)
2. **DeFiLlama API** — TVL, yield pools, protocol health (no auth)
3. **ccxt** — public order book + OHLCV from any supported exchange (no auth for public endpoints)

```python
# Signal logic overview (see trade_signals.py for full implementation)

def momentum_signal(prices: list[float], volumes: list[float]) -> dict:
    """
    Returns: signal (BULLISH/BEARISH/NEUTRAL), strength (STRONG/MODERATE/WEAK),
             momentum_pct, rsi_14, vwap_deviation
    """
    rsi = calculate_rsi(prices, period=14)
    momentum = (prices[-1] - prices[-24]) / prices[-24] * 100  # 24h %
    vwap = sum(p * v for p, v in zip(prices, volumes)) / sum(volumes)
    vwap_dev = (prices[-1] - vwap) / vwap * 100

    if rsi > 70: signal = "OVERBOUGHT"
    elif rsi < 30: signal = "OVERSOLD/BULLISH_SETUP"
    elif momentum > 5 and prices[-1] > vwap: signal = "BULLISH"
    elif momentum < -5 and prices[-1] < vwap: signal = "BEARISH"
    else: signal = "NEUTRAL"

    strength = "STRONG" if abs(momentum) > 10 else "MODERATE" if abs(momentum) > 5 else "WEAK"
    return {"signal": signal, "strength": strength, "rsi_14": round(rsi, 1),
            "momentum_pct": round(momentum, 2), "vwap_deviation_pct": round(vwap_dev, 2)}
```

## Integration with agent infrastructure

**Via Telegram (direct command):**
```
@openclaw trading-signals momentum "XRP HBAR BTC" 24h
```

**Via Claude Code:**
```bash
openclaw run trading-signals "portfolio dashboard: BTC ETH XRP HBAR"
```

**Via Python (direct script):**
```bash
python3 trade_signals.py --mode=momentum --assets=ripple,hedera-hashgraph --timeframe=24h
python3 trade_signals.py --mode=defi --min-tvl=100 --min-apy=5
python3 trade_signals.py --mode=portfolio --assets=bitcoin,ethereum,ripple,hedera-hashgraph
```

**Via existing ccxt MCP (agent-to-agent):**
```
# Agents with ccxt MCP access can call:
mcp__ccxt__fetchOHLCV(symbol="XRP/USDT", timeframe="1h", limit=100)
mcp__ccxt__fetchTicker(symbol="XRP/USDT")
mcp__ccxt__fetchOrderBook(symbol="XRP/USDT", limit=20)
# Then pipe results into trade_signals.py for signal calculation
```

## Signal interpretation guide

| Signal | RSI | Action |
|--------|-----|--------|
| STRONG BULLISH | 50-65 | Entry zone, momentum confirmed |
| OVERBOUGHT | >70 | Wait for pullback, tighten stops |
| OVERSOLD/BULLISH_SETUP | <30 | Watch for reversal confirmation |
| STRONG BEARISH | 35-50 | Exit or hedge |
| NEUTRAL | 45-55 | Range-bound, wait for breakout |

## SaucerSwap LP Integration

For HBAR ecosystem signals, the skill also checks SaucerSwap pool yields:

```python
# SaucerSwap public API (no auth)
SAUCER_POOLS_URL = "https://api.saucerswap.finance/pools"

def saucer_lp_signal(pools: list) -> dict:
    """Returns best LP opportunities with impermanent loss risk rating."""
    scored = []
    for p in pools:
        apy = p.get('apr7d', 0)
        tvl = p.get('tvlUsd', 0)
        il_risk = estimate_il_risk(p['token0'], p['token1'])
        score = apy - (il_risk * 10)  # penalize high IL pairs
        scored.append({**p, 'score': score, 'il_risk': il_risk})
    return sorted(scored, key=lambda x: x['score'], reverse=True)[:5]
```

## Example outputs

### Momentum scan — XRP + HBAR

```
TRADING SIGNALS — 2026-03-27 12:00 UTC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

XRP  $0.523  ↑ +8.2% (24h)  RSI: 62  BULLISH/MODERATE
  Volume: 2.1x avg | VWAP: $0.498 (price above) | Watch: $0.55 resistance

HBAR $0.082  ↑ +5.1% (24h)  RSI: 57  BULLISH/WEAK
  Volume: 1.4x avg | VWAP: $0.079 (price above) | Wyoming integration catalysts

MARKET: Risk-on. BTC dominance -1.2% → altcoin rotation. XRP leads on volume.

TOP SIGNAL: XRP — strongest momentum + volume confirmation this week.
```

### DeFi yield scan

```
DEFI YIELD SCAN — 2026-03-27 12:00 UTC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STABLECOIN YIELDS (no IL risk):
1. USDC / Aave V3 / Ethereum    8.4% APY  TVL: $2.1B  ✓ Safe
2. USDT / Compound / Base       7.2% APY  TVL: $890M  ✓ Safe
3. DAI  / Spark / Ethereum      6.8% APY  TVL: $1.4B  ✓ Safe
4. USDS / Sky / Ethereum        5.9% APY  TVL: $780M  ✓ Safe

VOLATILE PAIRS (IL risk noted):
5. ETH/WETH / Curve / Ethereum  12.1% APY  TVL: $3.2B  IL: minimal (correlated pair)
6. WBTC/ETH / Uniswap V3       9.4% APY   TVL: $445M  IL: moderate

AVOID: Pools <$10M TVL, APY >50% (likely unsustainable emissions)
```
