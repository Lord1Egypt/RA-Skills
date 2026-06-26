# Open Interest Overlay

Display open interest data from MMT as an area or line series, typically on a separate pane below the price chart.

## Data Source

Open interest is available as OHLC candles (`OHLCPublic`) via:
- **REST**: `GET /api/v1/oi?exchange=binancef&symbol=btc/usdt&tf=1m`
- **WebSocket**: subscribe to the `oi` channel

```typescript
interface OHLCPublic {
  t: number; o: number; h: number; l: number; c: number; n: number;
}
```

The `c` (close) field represents the current OI value at the end of each candle period.

## Area Series Setup

```typescript
import { createChart, AreaSeries, ColorType } from 'lightweight-charts';
import type { UTCTimestamp } from 'lightweight-charts';

const oiChart = createChart(oiContainer, {
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

const oiSeries = oiChart.addSeries(AreaSeries, {
  lineColor: '#8b5cf6',
  topColor: 'rgba(139, 92, 246, 0.4)',
  bottomColor: 'rgba(139, 92, 246, 0.0)',
  lineWidth: 2,
  priceFormat: {
    type: 'custom',
    formatter: (price: number) => formatCompact(price),
  },
});

function formatCompact(value: number): string {
  if (value >= 1_000_000_000) return (value / 1_000_000_000).toFixed(2) + 'B';
  if (value >= 1_000_000) return (value / 1_000_000).toFixed(2) + 'M';
  if (value >= 1_000) return (value / 1_000).toFixed(1) + 'K';
  return value.toFixed(0);
}
```

## Load Historical OI

```typescript
async function loadOpenInterest(exchange: string, symbol: string, tf: string) {
  // Fetch through your server-side proxy — never call MMT directly from browser
  const params = new URLSearchParams({ exchange, symbol, tf });
  const resp = await fetch(`/api/mmt/oi?${params}`);
  const { data } = await resp.json();
  const oiCandles = data as OHLCPublic[];

  const oiData = oiCandles.map((oi) => ({
    time: oi.t as UTCTimestamp,
    value: oi.c, // Close = current OI at candle end
  }));

  oiSeries.setData(oiData);
  oiChart.timeScale().fitContent();
}
```

## Real-Time OI Updates

```typescript
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'oi',
  exchange: 'binancef',
  symbol: 'btc/usdt',
  tf: '1m',
}));

ws.onmessage = (event) => {
  const raw = typeof event.data === 'string' ? event.data : new TextDecoder().decode(event.data);
  const msg = JSON.parse(raw);
  if (msg.type !== 'data' || msg.channel !== 'oi') return;

  const oi = msg.data as OHLCPublic;
  oiSeries.update({
    time: oi.t as UTCTimestamp,
    value: oi.c,
  });
};
```

## Color by OI Change Direction

Highlight whether OI is increasing or decreasing by tracking the previous value:

```typescript
import { LineSeries } from 'lightweight-charts';

const oiLineSeries = oiChart.addSeries(LineSeries, {
  color: '#8b5cf6',
  lineWidth: 2,
});

let previousOI = 0;

function onOIUpdate(oi: OHLCPublic) {
  const isIncreasing = oi.c > previousOI;
  previousOI = oi.c;

  // Update line color based on direction
  oiLineSeries.applyOptions({
    color: isIncreasing ? '#22c55e' : '#ef4444',
  });

  oiLineSeries.update({
    time: oi.t as UTCTimestamp,
    value: oi.c,
  });
}
```

Note: `applyOptions` changes color for the entire series, not per data point. For per-point coloring, use a histogram series or use the baseline series approach.

## OI as Full OHLC Candlestick

For more detail, render OI as its own candlestick series:

```typescript
import { CandlestickSeries } from 'lightweight-charts';

const oiCandleSeries = oiChart.addSeries(CandlestickSeries, {
  upColor: '#22c55e',
  downColor: '#ef4444',
  wickUpColor: '#22c55e',
  wickDownColor: '#ef4444',
  borderVisible: false,
});

oiCandleSeries.setData(oiCandles.map(oi => ({
  time: oi.t as UTCTimestamp,
  open: oi.o,
  high: oi.h,
  low: oi.l,
  close: oi.c,
})));
```

## Rules

- Use the `c` (close) field from OI candles for line/area series representing current OI value.
- OI values are typically large numbers (millions/billions); use a compact formatter to display as M/B/K.
- Always display OI on a separate price scale or separate pane since OI values are a different magnitude than price.
- OI is only available on futures exchanges (binancef, bybitf, okxf, etc.). Spot exchanges do not have OI data.
- When combining OI with price in a multi-pane layout, sync time scales for coordinated scrolling.
- OI increasing with price rising suggests strong trend conviction. OI decreasing suggests position unwinding. Use this context when building tooltips.
