# Capacity Forecasting

Forecast resource saturation for hosts, Kubernetes workloads, and billing
metrics. Use `timeseries-forecast` for forward-looking projections; use
the DQL patterns below for immediate risk classification.

---

## Dynatrace Forecast Analyzer

Use `timeseries-forecast` for all capacity forecasts. See
`references/forecasting-analyzer.md` for the full parameter reference,
feasibility decision tree, and horizon sizing rules.

**Key rule**: For 30-day forecasts, use `interval:1d` and `forecastHorizon:30`.
`forecastHorizon` is in steps (intervals), not absolute days.

### Host CPU — 30-Day Saturation Forecast

Training: 120 days. Interval: `1d`. Horizon: 30 daily steps.

**Tool**: `timeseries-forecast`
- `query`: `timeseries avg(dt.host.cpu.usage), by:{dt.entity.host}, interval:1d | limit 500`
- `forecastHorizon`: `30`
- `forecastOffset`: `1`
- `generalParameters.timeframe.startTime`: `now-60d`

### Host Memory — 30-Day Saturation Forecast

**Tool**: `timeseries-forecast`
- `query`: `timeseries avg(dt.host.memory.usage), by:{dt.entity.host}, interval:1d | limit 500`
- `forecastHorizon`: `30`
- `forecastOffset`: `1`
- `generalParameters.timeframe.startTime`: `now-120d`

### Kubernetes Container CPU — Namespace Forecast

**Tool**: `timeseries-forecast`
- `query`: `timeseries avg(dt.kubernetes.container.cpu_usage), by:{k8s.namespace.name, k8s.workload.name}, interval:1d | limit 500`
- `forecastHorizon`: `30`
- `forecastOffset`: `1`
- `generalParameters.timeframe.startTime`: `now-60d`

### Kubernetes PVC Storage Saturation

**Tool**: `timeseries-forecast`
- `query`: `timeseries avg(dt.kubernetes.persistentvolumeclaim.used), by:{k8s.namespace.name}, interval:1d | limit 500`
- `forecastHorizon`: `30`
- `forecastOffset`: `1`
- `generalParameters.timeframe.startTime`: `now-60d`

---

## Result Presentation

| Column | Content |
|--------|---------|
| Rank | 🥇 🥈 🥉 by days to saturation (ascending) |
| Host / Workload | Entity identifier |
| Current (%) | Latest measured utilization |
| Growth/Day | Daily growth rate in percentage points |
| Days to 90% | Estimated days until saturation at current growth |
| Action | ✅ Safe / ⚠️ Plan ahead / 🔴 Act now |

---

## Best Practices

- Use at least 60 days of history for 30-day forecasts (2:1 rule)
- Use `interval:1d` for 30-day forecasts; `interval:1h` for 7-day
- Saturation threshold is typically 90%; adjust per SLA
- Always `filter isNotNull(field)` before `sort`
- Use `if(daily_growth > 0, ..., else: 9999)` — negative growth = no saturation risk
- Entities with data gaps in the most recent third of the training window will
  fail forecasting; filter them out or shorten the training window
