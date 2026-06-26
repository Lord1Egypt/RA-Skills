# Trigger Conditions Reference

Programmatic entry/exit rules combining SM + TA + Market fields with AND/OR logic. Auto-filled from agent_type preset if not provided. Can be customized via `--trigger-conditions` in `agent-create` or `agent-update`.

---

## Schema

```
{
  "entry": {
    "long":  {op: "and"|"or", conditions: [...]},
    "short": {op: "and"|"or", conditions: [...]}
  },
  "exit": {
    "long":  {op: "and", conditions: [...]},   // or "close_long" — both work
    "short": {op: "and", conditions: [...]}     // or "close_short"
  }
}
```

**Condition types:**
- **Leaf:** `{field, compare, value}` — compare field vs constant
- **Cross:** `{field, compare, value_field}` — compare field vs another field (e.g. EMA cross)
- **Group:** `{op: "and"|"or", conditions: [...]}` — nested group (OR inside AND)

**Compare operators:** `>=`, `<=`, `>`, `<`, `==`, `!=`

---

## Available Fields

- **SM** (aggregated, 0-100): `sm.long_ratio`, `sm.short_ratio`, `sm.wallet_count`, `sm.long_count`, `sm.short_count`, `sm.long_volume`, `sm.short_volume`
- **SM per-timeframe** (tf: 1h, 4h, 24h): `sm.{tf}.long_count`, `sm.{tf}.short_count`, `sm.{tf}.wallet_count`, `sm.{tf}.long_volume`, `sm.{tf}.short_volume`
- **TA** (per tf: 15m, 1h, 4h, 1d): `ta.{tf}.rsi`, `ta.{tf}.macd_hist`, `ta.{tf}.stoch_k`, `ta.{tf}.stoch_d`, `ta.{tf}.supertrend_advice`, `ta.{tf}.adx`, `ta.{tf}.plus_di`, `ta.{tf}.minus_di`, `ta.{tf}.bb_upper`, `ta.{tf}.bb_middle`, `ta.{tf}.bb_lower`, `ta.{tf}.ema_9`, `ta.{tf}.ema_21`, `ta.{tf}.sma_50`, `ta.{tf}.sma_200`, `ta.{tf}.atr`, `ta.{tf}.cci`, `ta.{tf}.mfi`, `ta.{tf}.obv`, `ta.{tf}.vwap`
- **Market:** `market.funding_current`, `market.oi_change_1h`, `market.oi_change_4h`, `market.oi_change_24h`, `market.long_ratio`, `market.short_ratio`, `market.liquidation_long_24h/4h/1h`, `market.liquidation_short_24h/4h/1h`, `market.volume_24h`, `market.price_change_24h`

---

## Intent → Condition Translation Guide

| User says | Maps to |
|-----------|---------|
| "smart money is buying / bullish" | `sm.long_ratio >= 50` + `sm.wallet_count >= 3` (with TA confirm) or `sm.long_ratio >= 55` (standalone) |
| "strong smart money / high consensus" | `sm.long_ratio >= 55` + `sm.wallet_count >= 5` |
| "smart money flipped direction" | Exit AND: `sm.short_ratio >= 55` + `ta.4h.supertrend == sell`. Use AND, not OR! |
| "whales are accumulating" | `sm.wallet_count >= 5` + `sm.long_volume > sm.short_volume` |
| "RSI oversold" | `ta.4h.rsi <= 30` |
| "RSI overbought" | `ta.4h.rsi >= 70` |
| "RSI not yet overbought" | `ta.4h.rsi <= 65` |
| "MACD bullish / momentum rising" | `ta.4h.macd_hist > 0` |
| "uptrend / trend is up" | `ta.4h.supertrend_advice == "buy"` |
| "downtrend / trend is down" | `ta.4h.supertrend_advice == "sell"` |
| "strong trend" | `ta.4h.adx >= 15` (moderate) or `>= 20` (strong). AND ≥12; OR ≥18 |
| "EMA bullish cross" | `ta.4h.ema_9 > ta.4h.ema_21` (use `value_field`) |
| "high funding rate / crowded longs" | `market.funding_current >= 0.03` |
| "funding reset / crowded shorts" | `market.funding_current <= -0.03` |
| "OI rising" | `market.oi_change_4h > 0` |
| "short squeeze" | `market.liquidation_short_4h > 0` |
| "heavy shorting / crowd is short" | `market.short_ratio >= 60` |
| "contrarian / fade the crowd" | `market.long_ratio >= 65` → SHORT, or `market.short_ratio >= 65` → LONG |

---

## Recommended Threshold Ranges

| Metric | In AND (easy) | In OR (strict) | Notes |
|--------|--------------|----------------|-------|
| `sm.long_ratio` / `sm.short_ratio` | ≥50 | ≥55 | Avg 44-46% neutral. Rarely >55% |
| `sm.wallet_count` | ≥3 | ≥5 | More wallets = higher confidence |
| `ta.{tf}.rsi` | ≤68 (anti-OB) | ≤30 OS / ≥70 OB | |
| `ta.{tf}.adx` | ≥12 | ≥18 | <15=ranging. Never ≥20+ in flat AND |
| `ta.{tf}.supertrend_advice` | =="buy"/"sell" | Same | Clearest trend signal |
| `ta.{tf}.macd_hist` | Better in OR | >0 bullish | Flips often |
| `market.funding_current` | ≥0.02 / ≤-0.01 | ≥0.03 / ≤-0.03 | Extreme=rare |
| `market.oi_change_4h` | >1 / <-1 | >2 / <-2 | |
| `market.long_ratio` | ≥55 | ≥65 | Contrarian |

Moving averages and Bollinger Bands are price-level — compare to each other via `value_field`.

---

## AND/OR Design Guidelines (CRITICAL)

| Rule | Guideline | Example |
|------|-----------|---------|
| **AND = easy** | Each ~70-80% pass rate. Relaxed thresholds. | `sm.long_ratio >= 50`, `sm.wallet_count >= 3`, `ta.4h.rsi <= 68` |
| **OR inside AND = strict** | Only 1 of N needs to pass. Flexibility. | `OR(adx >= 15, supertrend == buy, sm >= 55)` |
| **Max AND depth** | 2-4 items (including OR groups). Never 5+ flat AND. | `AND(easy_sm, easy_ta, OR(strict_a, strict_b))` |
| **Exit = AND** | Require 2+ reversal confirmations. SL/TP is primary exit. | `AND(sm.short_ratio >= 56, supertrend == sell)` |
| **⚠️ Exit OR = premature** | Single indicator triggers close on noise. | ❌ `OR(macd<0, rsi≥70)` |
| **⚠️ Strict AND = dead agent** | 5 strict ANDs: 0.3^5 ≈ 0.2% chance. Never trades. | ❌ `AND(sm≥60, wallets≥5, adx≥22, rsi≤50, macd>0)` |
| **value_field** | Compare two fields: `{"field": "ta.1h.ema_9", "compare": ">", "value_field": "ta.1h.ema_21"}` | EMA cross, DI cross |

---

## Pattern Template

```
entry.long = AND(
  sm.long_ratio >= 50,           // SM filter
  sm.wallet_count >= 3,          // wallet filter
  OR(                            // at least 1 strict confirmation
    ta.4h.supertrend == buy,
    ta.1h.adx >= 15,
    sm.long_ratio >= 55
  )
)
exit.long = AND(                 // require 2 confirmations
  sm.short_ratio >= 55,
  ta.4h.supertrend == sell
)
// SL/TP on exchange is PRIMARY exit. TC exit is SUPPLEMENTARY.
```

---

## Common Strategy Patterns

| Strategy | Entry | Exit |
|----------|-------|------|
| **Momentum** | AND(sm≥50, wallets≥3, OR(ADX≥15, SuperTrend=buy)) + RSI≤68 | AND(sm.short≥55, supertrend==sell) |
| **Mean reversion** | AND(RSI≤30, OR(funding negative, sm≥55)) | AND(rsi≥65, sm.short≥55) |
| **Whale following** | AND(sm≥50, wallets≥3, OR(supertrend=buy, rsi≤65)) | AND(sm.short≥55, supertrend==sell) |
| **Contrarian** | AND(market.long≥60, OR(funding≥0.03, sm.short≥55)) → SHORT | AND(market.short≥55, rsi≤35) |
| **Scalping** | AND(RSI 35-65, OR(MACD>0, SuperTrend=buy, adx≥15)) | AND(supertrend==sell, rsi≥65) |

---

## Full JSON Examples

**Example 1: "Buy when SM is strong + RSI not overbought, exit when SM flips"**

```json
{"entry":{"long":{"op":"and","conditions":[
  {"field":"sm.long_ratio","compare":">=","value":50},
  {"field":"sm.wallet_count","compare":">=","value":3},
  {"field":"ta.4h.rsi","compare":"<=","value":68},
  {"op":"or","conditions":[
    {"field":"sm.long_ratio","compare":">=","value":55},
    {"field":"ta.4h.supertrend_advice","compare":"==","value":"buy"},
    {"field":"ta.1h.supertrend_advice","compare":"==","value":"buy"}
  ]}
]}},
"exit":{"long":{"op":"and","conditions":[
  {"field":"sm.short_ratio","compare":">=","value":55},
  {"field":"ta.4h.supertrend_advice","compare":"==","value":"sell"}
]}}}
```

**Example 2: "Contrarian — buy when fearful, sell when greedy"**

```json
{"entry":{"long":{"op":"and","conditions":[
  {"field":"market.short_ratio","compare":">=","value":60},
  {"op":"or","conditions":[
    {"field":"market.funding_current","compare":"<=","value":-0.02},
    {"field":"ta.4h.rsi","compare":"<=","value":35},
    {"field":"sm.long_ratio","compare":">=","value":55}
  ]}
]},
"short":{"op":"and","conditions":[
  {"field":"market.long_ratio","compare":">=","value":60},
  {"op":"or","conditions":[
    {"field":"market.funding_current","compare":">=","value":0.02},
    {"field":"ta.4h.rsi","compare":">=","value":65},
    {"field":"sm.short_ratio","compare":">=","value":55}
  ]}
]}},
"exit":{"long":{"op":"and","conditions":[
  {"field":"market.long_ratio","compare":">=","value":58},
  {"field":"ta.4h.rsi","compare":">=","value":65}
]},
"short":{"op":"and","conditions":[
  {"field":"market.short_ratio","compare":">=","value":58},
  {"field":"ta.4h.rsi","compare":"<=","value":35}
]}}}
```
