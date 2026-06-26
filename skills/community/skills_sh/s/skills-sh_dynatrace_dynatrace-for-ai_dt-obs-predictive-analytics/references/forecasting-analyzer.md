# Dynatrace Forecast Analyzer

The `timeseries-forecast` tool generates time series forecasts for any numeric
metric queryable from Grail. It uses Davis AI statistical models to produce
point forecasts and confidence bands.

**⚠️ Univariate only**: Dynatrace Forecast Analyzer currently supports only
univariate forecasting. See Section 1 for details and multivariate alternatives.

**🚫 Result Analysis Rule**: After running a forecast or DQL query, always
analyse and summarise the results directly from the raw tool output.

**📊 Result Presentation Rule**: Present forecast results as a structured
Markdown table:

| Column | Content |
|--------|---------|
| Rank | 🥇 🥈 🥉 4️⃣ … ordered by urgency or magnitude of change |
| Signal / Entity | Dimension name (entity, product, service, etc.) |
| Last Actual | Most recent non-null value from the historical series |
| Forecast D+N | Point forecast at the end of the horizon |
| Range | Lower – Upper confidence band at the same horizon point |
| Trend | % change from Last Actual to Forecast D+N: 🔴 >+20%, 🟠 +5–20%, 🟢 ±5% stable, 🔵 −5–20% declining, ⚫ <−20% sharp drop |
| Action | ✅ No action / ⚠️ Monitor / 🔴 Act now |

After the table, add a **Key Findings** section (3–5 bullet points) ranked by priority.

---

## Tool Reference: `timeseries-forecast`

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | Yes | DQL `timeseries` query providing the historical series to forecast. Always include `\| limit 50` (or lower). Specify `interval:` explicitly for predictable results. |
| `forecastHorizon` | No | Steps to forecast ahead. **Max 600.** Default 100. Steps × interval = forecast time span. |
| `forecastOffset` | No | Steps to withhold from training end for validation (0–10). Default 1. |
| `generalParameters.timeframe.startTime` | No | Training window start, e.g. `now-120d`. Default: last 2 hours. |
| `generalParameters.timeframe.endTime` | No | Training window end. Default: `now`. |

### Output Fields

The result timeseries contains these fields per record:
- **`<metric_expression>`** — historical values (nulls in the forecast period)
- **`dt.davis.forecast:point`** — point forecast (nulls in the historical period)
- **`dt.davis.forecast:lower`** — lower confidence bound
- **`dt.davis.forecast:upper`** — upper confidence bound

The forecast begins at the last non-null historical value. Read the point
forecast array from the first non-null position onward.

### Common Failure: Missing Values in Recent History

The analyzer requires **at least 14 non-null values in the last third** of the
training window. If the series has too many gaps near the end, the analysis
status will be `FAILED` with a warning:

> "Too many values are missing from the most recent history."

Fix: filter entities with sufficient continuous data, or shorten the training
window to exclude inactive periods.

### Interval and Horizon Sizing

`forecastHorizon` is counted in **steps** (intervals), not in absolute time:
`forecast time = forecastHorizon × interval`.

| Forecast Target | Recommended `interval` | `forecastHorizon` | Training Window |
|-----------------|------------------------|-------------------|-----------------|
| 24 hours ahead  | `interval:1h`          | `24`              | `now-2d`        |
| 7 days ahead    | `interval:1h`          | `168`             | `now-14d`       |
| 30 days ahead   | `interval:1d`          | `30`              | `now-60d`       |
| 90 days ahead   | `interval:1d`          | `90`              | `now-180d`      |

Do not omit `interval:` from the query — without it, the tool auto-selects an
interval that may differ from what you expect, making the horizon ambiguous.

---

## 1. Forecast and Prediction

### Core Principles

#### Univariate vs. Multivariate Forecasting

**Univariate Forecasting**: Predicts a single metric based on its own historical values.
- **Best for**: Stable patterns with strong autocorrelation (e.g., daily traffic patterns)
- **Status with Dynatrace**: ✅ **Supported** via `timeseries-forecast`

**Multivariate Forecasting**: Predicts a target metric using multiple related metrics as features.
- **Best for**: Complex systems where multiple factors drive the target metric
- **Status with Dynatrace**: ⏳ **Not Supported** by Dynatrace Forecast Analyzer. Use external tools (Python, R, Azure AutoML) or approximate with multiple univariate forecasts.

#### Statistical Foundation

Time series forecasting works best when:
- **Stationarity**: Statistical properties (mean, variance) remain roughly constant
- **Seasonality**: Regular, repeating patterns exist (hourly, daily, weekly)
- **Trend**: Long-term direction (upward, downward, or flat)
- **Autocorrelation**: Current values relate to past values

### Critical Data Requirements

#### Minimum Historical Data

- **Hard minimum**: 20 non-null data points
- **Recency requirement**: At least 14 non-null values must fall in the last third of the training window
- **Practical rule**: Ensure continuous data collection with no more than 5% gaps

#### The 2:1 Rule (Data Science Best Practice)

Training history must be at least **2× the forecast horizon**:

| Forecast Horizon | Minimum Training | Example |
|-----------------|------------------|---------|
| 1 day           | 2 days           | `forecastHorizon:24` (1h interval), `startTime:now-2d` |
| 1 week          | 2 weeks          | `forecastHorizon:168` (1h interval), `startTime:now-14d` |
| 30 days         | 60 days          | `forecastHorizon:30` (1d interval), `startTime:now-60d` |

#### Data Quality Rules

1. **No more than 5% missing** data points within the training window
2. **Sufficient variance**: CV (std dev / mean) > 5%; flat metrics cannot be forecast
3. **Complete seasonal cycles**: Include ≥ 2 full cycles (e.g., 2 weeks for weekly patterns)
4. **Clean outliers**: Incidents and one-off spikes distort models; consider excluding them

### Metric Discovery

Before forecasting, use `execute-dql` to confirm which metrics are available:

```dql
fetch metric.series
| filter contains(metric.key, "cpu")
| dedup metric.key
| limit 100
```

Change `"cpu"` to any keyword (e.g., `"request"`, `"memory"`, `"kubernetes"`) to
explore other domains.

### Query Patterns for Forecast Input

Always pair a DQL query with `timeseries-forecast`. The query must return a
`timeseries` result; `limit` controls how many entities are analyzed.

**Host CPU (univariate, by host)**:
```dql
timeseries avg(dt.host.cpu.usage), by:{dt.smartscape.host}, interval:1d | limit 50
```

**Service request volume (univariate, by service)**:
```dql
timeseries sum(dt.service.request.count), by:{dt.entity.service}, interval:1h | limit 50
```

**Single entity forecast** (filter first, then forecast):
```dql
timeseries sum(dt.service.request.count), by:{dt.entity.service}, interval:1h
| filter dt.entity.service == "SERVICE-XXXXXXXX"
```

### Do's and Don'ts

#### ✅ DO

- Specify `interval:` explicitly so the horizon count is predictable
- Use at least 3× training history relative to the forecast horizon
- Include ≥ 2 complete seasonal cycles in training data
- Retrain regularly — patterns change after deployments and events
- Set `forecastOffset: 1` to validate the last point against forecast

#### ❌ DON'T

- Forecast with fewer than 20 data points
- Omit `interval:` from the query (leads to ambiguous horizon sizing)
- Set `forecastHorizon` > 600 (hard limit)
- Forecast beyond 2–3× the training window (uncertainty explodes)
- Use a metric with CV < 5% (flat signals produce meaningless forecasts)
- Mix pre/post-deployment data in the training window

---

## 2. Top Use Cases

### Capacity Planning (30 days)

**Tool**: `timeseries-forecast`
- `query`: `timeseries avg(dt.host.cpu.usage), by:{dt.entity.host}, interval:1d | limit 500`
- `forecastHorizon`: `30` (30 daily steps = 30 days)
- `forecastOffset`: `1`
- `generalParameters.timeframe.startTime`: `now-60d`

Repeat for memory (`dt.host.memory.usage`) and disk (`dt.host.disk.used.percent`).
See `references/capacity-forecasting.md` for multi-resource patterns.

### Traffic Forecasting (7 days)

**Tool**: `timeseries-forecast`
- `query`: `timeseries sum(dt.service.request.count), by:{dt.entity.service}, interval:1h | limit 500`
- `forecastHorizon`: `168` (168 hourly steps = 7 days)
- `forecastOffset`: `1`
- `generalParameters.timeframe.startTime`: `now-14d`

### SLA / Response Time Forecast (24 hours)

**Tool**: `timeseries-forecast`
- `query`: `timeseries avg(dt.service.request.response_time), by:{dt.entity.service}, interval:1h | limit 500`
- `forecastHorizon`: `24` (24 hourly steps = 24 hours)
- `forecastOffset`: `1`
- `generalParameters.timeframe.startTime`: `now-7d`

Note: `dt.service.request.response_time` is in microseconds — divide by 1 000 for milliseconds in DQL before displaying.

### Anomaly Baseline Forecasting

Generate a dynamic baseline by running a short-horizon forecast, then alert
when actuals exceed `dt.davis.forecast:upper`:

**Tool**: `timeseries-forecast`
- `query`: `timeseries avg(dt.host.cpu.usage), by:{dt.entity.host}, interval:1h | limit 500`
- `forecastHorizon`: `24`
- `forecastOffset`: `1`
- `generalParameters.timeframe.startTime`: `now-2d`

Retrain daily. Alert when `actual > dt.davis.forecast:upper`.

---

## 3. Feasibility Decision Tree

```
Q: Should we forecast this metric?
├─ Do we have ≥ 20 historical data points?
│  ├─ No  → Wait and collect more data
│  └─ Yes → Continue
├─ Does the last third of the window have ≥ 14 non-null values?
│  ├─ No  → Shorten the training window or filter to active entities
│  └─ Yes → Continue
├─ Does the metric have meaningful variance? (CV > 5%)
│  ├─ No  → Skip forecasting; use static thresholds instead
│  └─ Yes → Continue
├─ Is training history ≥ 2× the forecast horizon?
│  ├─ No  → Reduce forecastHorizon or extend startTime
│  └─ Yes → Proceed
└─ Single or multiple metrics?
   ├─ Single → Univariate forecast with timeseries-forecast ✅
   └─ Multiple → External tools (multivariate not supported) ⏳
```

---

## 4. Monitoring Forecast Accuracy

Track these metrics post-deployment:

| Metric | Calculation | Target |
|--------|-----------|--------|
| **MAPE** | `avg(\|actual − forecast\| / actual)` | < 15% |
| **Interval Coverage** | `% of actuals within forecast bounds` | 85–95% |
| **Forecast Bias** | `avg(forecast − actual)` | Near 0 |

Retrain after significant business events (launches, incidents, major config changes).

---

## 5. Common Pitfalls

| Pitfall | Why It Fails | Fix |
|---------|-------------|-----|
| Too many nulls in recent history | Analyzer rejects the series | Filter entities with continuous data or shorten window |
| Omitting `interval:` from query | Horizon count becomes ambiguous | Always specify `interval:` explicitly |
| `forecastHorizon` > 600 | Hard tool limit | Use coarser interval (e.g., `1d` instead of `1h`) |
| Training < 2× horizon | Uncertainty too high | Extend `startTime` |
| Flat metric (CV < 5%) | No pattern to model | Use rule-based alerts instead |
| Pre/post-deployment mix | Model learns old patterns | Set `startTime` after the change |
| Ignoring seasonality | Model misses weekly cycles | Include ≥ 2 weeks of history |
