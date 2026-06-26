---
name: weather-demand
description: Weather-driven demand forecasting — correlate temperature with energy/commodity trade flows, Holt-Winters predictions
user-invocable: true
metadata: {"openclaw":{"requires":{"env":[]}},"homepage":"https://sputnikx.xyz","author":"SputnikX","version":"1.0.0","tags":["weather","forecast","demand","energy","commodities"]}
---

# Weather-Demand Forecasting

Correlate Baltic weather data with commodity trade flows. Holt-Winters time series forecasting. Temperature → energy demand predictions.

## Base URL

`https://sputnikx.xyz/api/v1/agent`

## Demand Forecast ($0.10 x402)
```bash
curl "https://sputnikx.xyz/api/v1/agent/trade/demand-forecast?reporter=LV&hs2=27&months=6"
```
Returns: Holt-Winters forecast with confidence intervals for commodity imports.

## Weather + Trade Correlation
```bash
curl "https://sputnikx.xyz/api/v1/agent/trade/seasonality?reporter=LV&hs2=27"
```
Returns: Monthly patterns showing temperature-trade correlation.

## Use Cases
- Predict heating fuel demand based on weather forecast
- Anticipate commodity import spikes before they happen
- Plan inventory based on seasonal weather patterns
- Analyze climate impact on Baltic trade flows
