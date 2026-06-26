# Live Trade Ticker

Display real-time individual trades from MMT on TradingView Lightweight Charts as markers, line overlays, or volume histograms.

## Subscribe to Trades

```typescript
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'trades',
  exchange: 'binancef',
  symbol: 'btc/usdt',
}));
```

Trades arrive as `TradePublic`: `{ id, t, p, q, b }` where `b: true` = buy, `b: false` = sell.

## Large Trade Markers on Candlestick Chart

Show markers for trades exceeding a size threshold:

```typescript
import type { SeriesMarker, UTCTimestamp } from 'lightweight-charts';

const LARGE_TRADE_THRESHOLD = 10; // e.g., 10 BTC

let markers: SeriesMarker<UTCTimestamp>[] = [];
const MAX_MARKERS = 100;

function onTrade(trade: TradePublic) {
  if (trade.q < LARGE_TRADE_THRESHOLD) return;

  const marker: SeriesMarker<UTCTimestamp> = {
    time: Math.floor(trade.t / 1000) as UTCTimestamp,
    position: trade.b ? 'belowBar' : 'aboveBar',
    color: trade.b ? '#22c55e' : '#ef4444',
    shape: trade.b ? 'arrowUp' : 'arrowDown',
    text: `${trade.q.toFixed(2)} @ ${trade.p.toFixed(0)}`,
  };

  markers.push(marker);

  // Keep bounded; sort by time (required by TV)
  if (markers.length > MAX_MARKERS) {
    markers = markers.slice(-MAX_MARKERS);
  }
  markers.sort((a, b) => (a.time as number) - (b.time as number));

  candleSeries.setMarkers(markers);
}
```

## Last Trade Price Line

Overlay a line series showing the most recent trade price:

```typescript
import { LineSeries } from 'lightweight-charts';

const tradeLineSeries = chart.addSeries(LineSeries, {
  color: '#fbbf24',
  lineWidth: 1,
  lineStyle: 2, // Dashed
  priceScaleId: 'right', // Share scale with candles
  lastValueVisible: true,
  priceLineVisible: true,
});

// Buffer recent trades for the line
const tradeLineData: { time: UTCTimestamp; value: number }[] = [];
const MAX_LINE_POINTS = 500;

function onTradeForLine(trade: TradePublic) {
  const point = { time: Math.floor(trade.t / 1000) as UTCTimestamp, value: trade.p };

  // TV requires unique, ascending times — update in place if same second
  if (tradeLineData.length > 0) {
    const last = tradeLineData[tradeLineData.length - 1];
    if (last.time === point.time) {
      last.value = point.value;
      tradeLineSeries.update(last);
      return;
    }
  }

  tradeLineData.push(point);
  if (tradeLineData.length > MAX_LINE_POINTS) {
    tradeLineData.shift();
  }
  tradeLineSeries.update(point);
}
```

## Trade Volume Histogram (Time-Bucketed)

Aggregate trades into time buckets and display as a histogram:

```typescript
import { HistogramSeries } from 'lightweight-charts';

const tradeVolSeries = chart.addSeries(HistogramSeries, {
  priceScaleId: 'trade-vol',
  priceFormat: { type: 'volume' },
});
chart.priceScale('trade-vol').applyOptions({
  scaleMargins: { top: 0.85, bottom: 0 },
});

const BUCKET_SECONDS = 5;
let currentBucket: { time: number; buyVol: number; sellVol: number } | null = null;

function onTradeForHistogram(trade: TradePublic) {
  const tradeTimeSec = Math.floor(trade.t / 1000);
  const bucketTime = Math.floor(tradeTimeSec / BUCKET_SECONDS) * BUCKET_SECONDS;

  if (!currentBucket || currentBucket.time !== bucketTime) {
    currentBucket = { time: bucketTime, buyVol: 0, sellVol: 0 };
  }

  if (trade.b) {
    currentBucket.buyVol += trade.q;
  } else {
    currentBucket.sellVol += trade.q;
  }

  const total = currentBucket.buyVol + currentBucket.sellVol;
  const isBuyDominant = currentBucket.buyVol > currentBucket.sellVol;

  tradeVolSeries.update({
    time: currentBucket.time as UTCTimestamp,
    value: total,
    color: isBuyDominant ? '#22c55e' : '#ef4444',
  });
}
```

## Color Convention

Use consistent colors for trade direction:

```typescript
const TRADE_COLORS = {
  buy: '#22c55e',   // Green
  sell: '#ef4444',  // Red
  buyAlpha: 'rgba(34, 197, 94, 0.5)',
  sellAlpha: 'rgba(239, 68, 68, 0.5)',
};
```

## Rules

- The `trades` channel is WebSocket-only; there is no REST endpoint for individual trades.
- Trades arrive at high frequency on active pairs. Always cap buffers (markers, line points) to prevent memory growth.
- Markers must be sorted by `time` ascending before calling `setMarkers()`. TV throws on unsorted markers.
- Multiple trades can share the same Unix-second timestamp. For line series, keep only the latest price per second.
- Use `belowBar` position for buys and `aboveBar` for sells so markers don't overlap candle bodies.
- Filter by a size threshold to avoid visual noise from small trades.
- Dollar-value thresholds (e.g., > $100K) require multiplying `q * p` since `q` is in base currency.
