# RiskGate — Monitoring & Reporting Pattern

Use this file when your agent monitors and reports without execution responsibilities.

## Recommended Schedule

Every 4 hours. Aligns with RiskGate data refresh cycle.
With demo key (10 calls/day): check BTC + ETH + SOL + 1 human-specified asset per cycle.

## Briefing Format

```
📊 RiskGate Signal Report — {TIMESTAMP}

BTC: {regime} | Confidence: {confidence} | Anomaly: {highest_anomaly_severity}
ETH: {regime} | Confidence: {confidence} | Anomaly: {highest_anomaly_severity}
SOL: {regime} | Confidence: {confidence} | Anomaly: {highest_anomaly_severity}

⚠️ Flags: {list any high/critical anomalies or bearish + confidence > 0.75}
✅ Clear: {list assets with bullish/neutral + anomaly none/low}
```

## Immediate Alert Triggers

Notify human outside scheduled cadence when:
- Any asset hits `critical` anomaly severity
- BTC or ETH shifts to `bearish` with confidence > 0.75
- ADX drops below 20 on an asset with an active position

## Demo Tier Call Budget

| Cycle | Calls | Assets |
|-------|-------|--------|
| Morning (8am) | 3 | BTC, ETH, SOL |
| Midday (12pm) | 3 | BTC, ETH, SOL |
| Evening (6pm) | 2 | BTC, ETH |
| Reserve | 2 | Alert re-checks |
