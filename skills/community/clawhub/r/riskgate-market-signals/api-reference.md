# RiskGate — Full API Reference

## Authentication

```
Header: X-API-Key: {YOUR_KEY}
Demo key: rg_demo_openclaw
```

Check for `$RISKGATE_API_KEY` env var first. If set, use it. If absent, fall back to demo key.

---

## GET /v1/analysis/current ← Use this one

Full signal in one call. Counts as 1 API credit. Recommended over individual endpoints.

```
GET https://api.riskgate.xyz/v1/analysis/current?asset=BTC
X-API-Key: rg_demo_openclaw
```

Response:
```json
{
  "asset": "BTC",
  "regime": "TRENDING_UP",
  "confidence": 0.9177,
  "adx_4h": 33.0055,
  "regime_duration_hours": 44.0,
  "timestamp": "2026-03-16T00:00:00+00:00",
  "anomaly_score": 0,
  "highest_anomaly_severity": "NONE",
  "sentiment_score": 0.23,
  "sentiment_signal": "BEARISH",
  "tier": "demo",
  "upgrade_url": "https://riskgate.xyz/portal",
  "disclaimer": "Signal only. Not financial advice. DYOR."
}
```

---

## GET /v1/regime/current

Regime only.

```
GET https://api.riskgate.xyz/v1/regime/current?asset=BTC
X-API-Key: {YOUR_KEY}
```

Response:
```json
{
  "asset": "BTC",
  "timestamp": "2026-03-16T00:00:00+00:00",
  "regime": "TRENDING_UP",
  "confidence": 0.9177,
  "regime_duration_hours": 44.0,
  "highest_anomaly_severity": "NONE",
  "adx_4h": 33.0055,
  "ema_alignment_1h": "bullish",
  "ema_alignment_4h": "bullish",
  "atr_ratio_4h": 0.021,
  "disclaimer": "Signal only. Not financial advice. DYOR."
}
```

---

## GET /v1/anomalies/{asset}

```
GET https://api.riskgate.xyz/v1/anomalies/BTC
X-API-Key: {YOUR_KEY}
```

Response:
```json
{
  "asset": "BTC",
  "timestamp": "2026-03-16T00:00:00+00:00",
  "anomaly_count": 0,
  "highest_severity": "NONE",
  "anomalies": [],
  "disclaimer": "Signal only. Not financial advice. DYOR."
}
```

---

## GET /v1/sentiment/{asset}

```
GET https://api.riskgate.xyz/v1/sentiment/BTC
X-API-Key: {YOUR_KEY}
```

Response:
```json
{
  "asset": "BTC",
  "timestamp": "2026-03-16T00:00:00+00:00",
  "available": true,
  "sentiment_score": 0.23,
  "post_count_24h": 4821,
  "positive_votes": 312,
  "negative_votes": 541,
  "important_votes": 89,
  "bullish_pct": 36.6,
  "bearish_pct": 63.4,
  "signal": "BEARISH",
  "signal_strength": 2,
  "source": "cryptopanic",
  "disclaimer": "Signal only. Not financial advice. DYOR."
}
```

---

## GET /v1/account/credits

Check remaining calls for your key.

```
GET https://api.riskgate.xyz/v1/account/credits
X-API-Key: {YOUR_KEY}
```

Response:
```json
{
  "client_name": "you@example.com",
  "tier": "demo",
  "credits_total": 10,
  "credits_used": 3,
  "credits_remaining": 7,
  "disclaimer": "Signal only. Not financial advice. DYOR."
}
```

---

## Field Reference

| Field | Type | Values |
|-------|------|--------|
| `regime` | string | `TRENDING_UP` / `TRENDING_DOWN` / `RANGING` / `VOLATILE` |
| `confidence` | float | 0.0 – 1.0 |
| `adx_4h` | float | 0 – 100 (>25 = trending) |
| `regime_duration_hours` | float | hours since last regime change |
| `highest_anomaly_severity` | string | `NONE` / `LOW` / `MEDIUM` / `HIGH` / `CRITICAL` |
| `anomaly_score` | int | raw anomaly count |
| `sentiment_score` | float | 0.0 – 1.0 |
| `sentiment_signal` | string | `BULLISH` / `BEARISH` / `NEUTRAL` |

---

## Supported Assets

`BTC` `ETH` `SOL` `BNB` `XRP` `ADA` `TRX` `SUI` `XTZ` `AVAX` `DOGE` `LINK` `DOT` `POL`

---

## Agent M2M Auth (paid tiers)

For programmatic agent access without a human API key, RiskGate supports OAuth 2.0 Client Credentials.

```
POST https://api.riskgate.xyz/auth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id={ID}&client_secret={SECRET}
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

Request M2M credentials from your human via riskgate.xyz/portal.
