# Multi-Symbol Comparison

Overlay multiple symbols or exchanges on one chart, with optional price normalization for comparison.

## Multiple Series on One Chart

Add a separate line or candlestick series for each symbol:

```typescript
import { createChart, LineSeries } from 'lightweight-charts';
import type { UTCTimestamp } from 'lightweight-charts';

const chart = createChart(container, { autoSize: true });

const SYMBOLS = [
  { exchange: 'binancef', symbol: 'btc/usdt', color: '#f59e0b', label: 'BTC' },
  { exchange: 'binancef', symbol: 'eth/usdt', color: '#8b5cf6', label: 'ETH' },
  { exchange: 'binancef', symbol: 'sol/usdt', color: '#06b6d4', label: 'SOL' },
];

const seriesMap = new Map<string, ReturnType<typeof chart.addSeries>>();

for (const sym of SYMBOLS) {
  const series = chart.addSeries(LineSeries, {
    color: sym.color,
    lineWidth: 2,
    title: sym.label,
  });
  seriesMap.set(sym.symbol, series);
}
```

## Price Normalization (Percentage Change)

When comparing assets with different price magnitudes (e.g., BTC at $60K vs SOL at $150), normalize to percentage change from the first data point:

```typescript
function normalizeToPercent(
  candles: OHLCVTPublic[]
): { time: UTCTimestamp; value: number }[] {
  if (candles.length === 0) return [];

  const basePrice = candles[0].c;
  return candles.map((c) => ({
    time: c.t as UTCTimestamp,
    value: ((c.c - basePrice) / basePrice) * 100,
  }));
}

// Load and normalize each symbol
for (const sym of SYMBOLS) {
  const candles = await fetchCandles(sym.exchange, sym.symbol, '1h');
  const normalized = normalizeToPercent(candles);
  const series = seriesMap.get(sym.symbol)!;
  series.setData(normalized);
}

chart.timeScale().fitContent();
```

## Same Symbol, Multiple Exchanges

Compare the same pair across exchanges to spot price divergence:

```typescript
const EXCHANGES = [
  { exchange: 'binancef', color: '#f59e0b', label: 'Binance' },
  { exchange: 'bybitf',   color: '#8b5cf6', label: 'Bybit' },
  { exchange: 'okxf',     color: '#06b6d4', label: 'OKX' },
];

for (const ex of EXCHANGES) {
  const series = chart.addSeries(LineSeries, {
    color: ex.color,
    lineWidth: 2,
    title: ex.label,
    priceScaleId: 'right', // All share same price scale
  });

  const candles = await fetchCandles(ex.exchange, 'btc/usdt', '1m');
  series.setData(candles.map(c => ({
    time: c.t as UTCTimestamp,
    value: c.c,
  })));
}
```

## Custom Legend Overlay

TradingView Lightweight Charts does not have a built-in legend. Create one with HTML:

```typescript
function createLegend(
  chartContainer: HTMLElement,
  symbols: { label: string; color: string }[]
): HTMLDivElement {
  const legend = document.createElement('div');
  legend.style.cssText = `
    position: absolute; top: 8px; left: 8px; z-index: 10;
    display: flex; gap: 12px; padding: 6px 10px;
    background: rgba(10, 10, 10, 0.8); border-radius: 4px;
    font-size: 12px; color: #d1d5db;
  `;

  for (const sym of symbols) {
    const item = document.createElement('span');
    item.innerHTML = `<span style="color:${sym.color};">&#9679;</span> ${sym.label}`;
    legend.appendChild(item);
  }

  chartContainer.style.position = 'relative';
  chartContainer.appendChild(legend);
  return legend;
}
```

## Data Alignment

Ensure all series cover the same time range for fair comparison:

```typescript
function alignTimeRange(datasets: OHLCVTPublic[][]): { from: number; to: number } {
  const maxFrom = Math.max(...datasets.map(d => d[0]?.t ?? 0));
  const minTo = Math.min(...datasets.map(d => d[d.length - 1]?.t ?? Infinity));
  return { from: maxFrom, to: minTo };
}

// Trim each dataset to the common range
function trimToRange(candles: OHLCVTPublic[], from: number, to: number): OHLCVTPublic[] {
  return candles.filter(c => c.t >= from && c.t <= to);
}
```

## Live Updates for Multiple Symbols

Subscribe to multiple WS channels and route updates to the correct series:

```typescript
for (const sym of SYMBOLS) {
  ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'candles',
    exchange: sym.exchange,
    symbol: sym.symbol,
    tf: '1h',
  }));
}

ws.onmessage = (event) => {
  const raw = typeof event.data === 'string' ? event.data : new TextDecoder().decode(event.data);
  const msg = JSON.parse(raw);
  if (msg.type !== 'data' || msg.channel !== 'candles') return;

  const series = seriesMap.get(msg.id);
  if (!series) return;

  const c = msg.data as OHLCVTPublic;
  series.update({ time: c.t as UTCTimestamp, value: c.c });
};
```

## Rules

- Use percentage-change normalization when comparing assets with different price magnitudes.
- All series sharing a price scale must have comparable value ranges, so normalize first.
- Align time ranges across datasets for fair visual comparison.
- Use distinct, high-contrast colors for each series — avoid colors that are too similar.
- Build a custom HTML legend; there is no built-in legend in Lightweight Charts.
- When subscribing to multiple WS channels, route each update to the correct series using the `id` field from the data message.
- Limit overlaid series to 4-5 maximum for readability.
