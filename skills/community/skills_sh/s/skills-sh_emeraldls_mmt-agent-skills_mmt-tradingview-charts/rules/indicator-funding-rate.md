# Funding Rate Overlay

Display the funding rate from MMT stats data as a baseline series that crosses zero, highlighting when longs pay shorts and vice versa.

## Data Source

Funding rate is the `fr` field in `StatPublic`, available via:
- **REST**: `GET /api/v1/stats?exchange=binancef&symbol=btc/usdt&tf=1m`
- **WebSocket**: subscribe to the `stats` channel

```typescript
interface StatPublic {
  t: number; mp: number; lp: number; fr: number;
  // ... other fields
}
```

## Baseline Series Setup

A baseline series renders above and below a base value with different colors, perfect for funding rate which oscillates around zero:

```typescript
import { createChart, BaselineSeries, ColorType } from 'lightweight-charts';
import type { UTCTimestamp } from 'lightweight-charts';

const chart = createChart(container, {
  autoSize: true,
  layout: {
    background: { type: ColorType.Solid, color: '#0a0a0a' },
    textColor: '#d1d5db',
  },
});

const fundingSeries = chart.addSeries(BaselineSeries, {
  baseValue: {
    type: 'price',
    price: 0,
  },
  topLineColor: '#22c55e',       // Green above zero (longs pay shorts)
  topFillColor1: 'rgba(34, 197, 94, 0.3)',
  topFillColor2: 'rgba(34, 197, 94, 0.0)',
  bottomLineColor: '#ef4444',    // Red below zero (shorts pay longs)
  bottomFillColor1: 'rgba(239, 68, 68, 0.0)',
  bottomFillColor2: 'rgba(239, 68, 68, 0.3)',
  lineWidth: 2,
  priceFormat: {
    type: 'custom',
    formatter: (price: number) => (price * 100).toFixed(4) + '%',
  },
});
```

## Load Historical Funding Rate

```typescript
async function loadFundingRate(exchange: string, symbol: string, tf: string) {
  // Fetch through your server-side proxy — never call MMT directly from browser
  const params = new URLSearchParams({ exchange, symbol, tf });
  const resp = await fetch(`/api/mmt/stats?${params}`);
  const { data } = await resp.json();
  const stats = data as StatPublic[];

  const fundingData = stats.map((s) => ({
    time: s.t as UTCTimestamp,
    value: s.fr,
  }));

  fundingSeries.setData(fundingData);
  chart.timeScale().fitContent();
}
```

## Real-Time Funding Rate Updates

```typescript
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'stats',
  exchange: 'binancef',
  symbol: 'btc/usdt',
  tf: '1m',
}));

ws.onmessage = (event) => {
  const raw = typeof event.data === 'string' ? event.data : new TextDecoder().decode(event.data);
  const msg = JSON.parse(raw);
  if (msg.type !== 'data' || msg.channel !== 'stats') return;

  const stat = msg.data as StatPublic;
  fundingSeries.update({
    time: stat.t as UTCTimestamp,
    value: stat.fr,
  });
};
```

## Funding Rate in a Separate Pane

For a multi-pane layout, create a dedicated chart for funding rate below the price chart:

```typescript
const fundingChart = createChart(fundingContainer, {
  autoSize: true,
  layout: {
    background: { type: ColorType.Solid, color: '#0a0a0a' },
    textColor: '#d1d5db',
  },
  rightPriceScale: {
    borderColor: '#1f2937',
  },
  timeScale: { timeVisible: true, borderColor: '#1f2937' },
});

const fundingPaneSeries = fundingChart.addSeries(BaselineSeries, {
  baseValue: { type: 'price', price: 0 },
  topLineColor: '#22c55e',
  topFillColor1: 'rgba(34, 197, 94, 0.3)',
  topFillColor2: 'rgba(34, 197, 94, 0.0)',
  bottomLineColor: '#ef4444',
  bottomFillColor1: 'rgba(239, 68, 68, 0.0)',
  bottomFillColor2: 'rgba(239, 68, 68, 0.3)',
  priceFormat: {
    type: 'custom',
    formatter: (price: number) => (price * 100).toFixed(4) + '%',
  },
});

// Add a zero line for reference
fundingPaneSeries.createPriceLine({
  price: 0,
  color: '#4b5563',
  lineWidth: 1,
  lineStyle: 2,
  axisLabelVisible: false,
});
```

## Funding Rate Interpretation

| Condition | Meaning | Color |
|-----------|---------|-------|
| `fr > 0`  | Longs pay shorts. More demand for long positions. | Green |
| `fr < 0`  | Shorts pay longs. More demand for short positions. | Red |
| `fr = 0`  | Balanced / no funding premium. | Neutral |

## Rules

- Use `BaselineSeries` with `baseValue: { type: 'price', price: 0 }` for funding rate so the zero crossing is visually clear.
- Funding rate values from MMT are raw decimals (e.g., `0.0001` = 0.01%). Use a custom formatter to display as percentage.
- Green for positive (longs pay shorts), red for negative (shorts pay longs) is the standard convention.
- Funding rate is available only on futures exchanges (binancef, bybitf, okxf, etc.), not spot exchanges.
- Add a zero price line for visual reference when using a separate pane.
- The stats channel includes many fields; only extract `fr` for the funding rate series.
