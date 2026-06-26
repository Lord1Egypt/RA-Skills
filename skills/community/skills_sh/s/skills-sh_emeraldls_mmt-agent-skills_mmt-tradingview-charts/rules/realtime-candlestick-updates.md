# Live Candlestick Updates

Stream real-time candle data from MMT WebSocket to TradingView Lightweight Charts using `series.update()`.

## How MMT Candle Streaming Works

MMT sends candle updates as each candle is forming, not only on close. Each message contains the current state of the candle (partial OHLCVT). When the candle period ends, a new `t` value appears, finalizing the previous candle automatically.

## Basic Real-Time Pattern

```typescript
import { createChart, CandlestickSeries } from 'lightweight-charts';
import type { UTCTimestamp } from 'lightweight-charts';

const chart = createChart(container, { autoSize: true });
const candleSeries = chart.addSeries(CandlestickSeries);

// 1. Load historical data first (through your server-side proxy)
const historicalData = await fetchCandles('binancef', 'btc/usdt', '1m');
candleSeries.setData(historicalData.map(mapCandle));
chart.timeScale().fitContent();

// 2. Connect to your own server's WS proxy (never connect to MMT directly from browser)
const ws = new WebSocket(`${location.protocol === 'https:' ? 'wss:' : 'ws:'}//${location.host}/ws`);
ws.binaryType = 'arraybuffer';

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'candles',
    exchange: 'binancef',
    symbol: 'btc/usdt',
    tf: '1m',
  }));
};

ws.onmessage = (event) => {
  const raw = typeof event.data === 'string' ? event.data : new TextDecoder().decode(event.data);
  const msg = JSON.parse(raw);
  if (msg.type !== 'data' || msg.channel !== 'candles') return;

  const candle = msg.data as OHLCVTPublic;
  candleSeries.update({
    time: candle.t as UTCTimestamp,
    open: candle.o,
    high: candle.h,
    low: candle.l,
    close: candle.c,
  });
};
```

## How series.update() Works

`series.update()` behaves differently based on the `time` value:

- **Same time as last data point**: Updates the existing candle in place (in-progress candle).
- **New time greater than last**: Appends a new candle (previous candle is finalized).
- **Time earlier than last**: Ignored. TV does not allow out-of-order updates.

This aligns with how MMT streams candles: repeated updates at the same `t` while forming, then a new `t` when the period rolls over.

## Updating Volume Alongside Price

When streaming candles, update the volume histogram series in tandem:

```typescript
import { HistogramSeries } from 'lightweight-charts';

const volumeSeries = chart.addSeries(HistogramSeries, {
  priceScaleId: 'volume',
  priceFormat: { type: 'volume' },
});
chart.priceScale('volume').applyOptions({
  scaleMargins: { top: 0.8, bottom: 0 },
});

ws.onmessage = (event) => {
  const raw = typeof event.data === 'string' ? event.data : new TextDecoder().decode(event.data);
  const msg = JSON.parse(raw);
  if (msg.type !== 'data' || msg.channel !== 'candles') return;

  const c = msg.data as OHLCVTPublic;
  const time = c.t as UTCTimestamp;

  candleSeries.update({
    time, open: c.o, high: c.h, low: c.l, close: c.c,
  });

  volumeSeries.update({
    time,
    value: c.vb + c.vs,
    color: c.vb > c.vs
      ? 'rgba(34, 197, 94, 0.5)'
      : 'rgba(239, 68, 68, 0.5)',
  });
};
```

## Handling Reconnection Gaps

When the WebSocket reconnects after a disconnect, there may be missing candles. Fetch the gap from REST before resuming live updates:

```typescript
let lastCandleTime = 0;

function onCandleUpdate(candle: OHLCVTPublic) {
  lastCandleTime = candle.t;
  candleSeries.update(mapCandle(candle));
}

async function onReconnect() {
  if (lastCandleTime > 0) {
    const now = Math.floor(Date.now() / 1000);
    const missing = await fetchCandles('binancef', 'btc/usdt', '1m', lastCandleTime, now);
    // Update each candle to fill the gap
    for (const c of missing) {
      candleSeries.update(mapCandle(c));
    }
  }
  // Re-subscribe
  ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'candles',
    exchange: 'binancef',
    symbol: 'btc/usdt',
    tf: '1m',
  }));
}
```

## Rules

- Always load historical data with `setData()` before starting live updates with `update()`.
- Use `series.update()` for every incoming candle message — it handles both in-progress and new candles.
- Never call `setData()` for individual live updates. It replaces the entire dataset and causes a full re-render.
- Track `lastCandleTime` to detect gaps on reconnection and backfill from REST.
- Update all related series (price, volume, indicators) in the same message handler to keep them in sync.
- MMT sends candle updates while the candle is forming, so `update()` calls with the same `time` are normal and expected.
- Never connect to the MMT WebSocket directly from browser code. Connect to your own server's WS proxy endpoint. See [Authentication](../../../mmt-api-best-practices/rules/connection-authentication.md) for proxy patterns.
