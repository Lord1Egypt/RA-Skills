# RiskGate — Agent Gate Decision Logic

Use this file when your agent has execution or trading responsibilities.

## Pre-Execution Gate

Call `GET /v1/analysis/current?asset={ASSET}` before any trade or significant action.

Apply rules in this exact order:

```
1. IF highest_anomaly_severity == "CRITICAL"
   → HALT. Do not execute.
   → Notify human: "RiskGate critical anomaly on {ASSET} (count: {anomaly_score}). Execution paused."

2. IF highest_anomaly_severity == "HIGH"
   → PAUSE. Surface to human for approval before proceeding.
   → Notify human: "RiskGate elevated anomaly on {ASSET}. Confirm to proceed."

3. IF regime == "TRENDING_DOWN" AND confidence > 0.75
   → Reduce position size or apply conservative parameters.
   → Notify human: "Downtrend confirmed on {ASSET} (confidence: {confidence})."

4. IF regime == "VOLATILE"
   → Widen risk parameters or pause. Re-check in 2 hours.

5. IF regime == "TRENDING_UP" AND highest_anomaly_severity IN ["NONE","LOW"] AND confidence > 0.6
   → Proceed with normal parameters.

6. IF regime == "RANGING" OR confidence < 0.5
   → Treat as uncertain. Apply conservative defaults.
```

## Sentiment Divergence Pattern

When `regime == "TRENDING_UP"` but `sentiment_signal == "BEARISH"`:
→ Flag to human as a divergence signal. Do not halt, but reduce confidence in the trend.
→ Notify human: "Price trending up on {ASSET} but sentiment is bearish — potential reversal risk."

## Field Reference

| Field | Type | Values |
|-------|------|--------|
| `regime` | string | `TRENDING_UP` / `TRENDING_DOWN` / `RANGING` / `VOLATILE` |
| `confidence` | float | 0.0 – 1.0 |
| `adx_4h` | float | 0 – 100 (>25 = trending, <20 = ranging) |
| `highest_anomaly_severity` | string | `NONE` / `LOW` / `MEDIUM` / `HIGH` / `CRITICAL` |
| `anomaly_score` | int | raw anomaly count |
| `sentiment_score` | float | 0.0 – 1.0 |
| `sentiment_signal` | string | `BULLISH` / `BEARISH` / `NEUTRAL` |

## Demo Tier Constraints

Demo key allows 10 calls/day per IP. Prioritize: BTC, ETH, SOL, then active positions.
If credits exhausted mid-session, halt execution and notify human.

## Disclaimer

RiskGate signals are market intelligence inputs, not financial advice.
Your human retains full responsibility for all execution decisions.
When in doubt, surface to human.
