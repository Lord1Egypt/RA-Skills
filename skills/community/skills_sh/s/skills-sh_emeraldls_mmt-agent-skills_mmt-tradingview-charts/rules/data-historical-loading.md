# Historical Data Loading

Fetch historical candle data from the MMT REST API and display it on TradingView Lightweight Charts with proper loading states.

## Basic Fetch and Display

```typescript
import type { UTCTimestamp } from 'lightweight-charts';

interface FetchCandlesParams {
  exchange: string;
  symbol: string;
  tf: string;
  from?: number;
  to?: number;
}

async function fetchCandles(params: FetchCandlesParams): Promise<OHLCVTPublic[]> {
  // Fetch through your server-side proxy — never call MMT directly from browser
  const url = new URL('/api/mmt/candles', window.location.origin);
  url.searchParams.set('exchange', params.exchange);
  url.searchParams.set('symbol', params.symbol);
  url.searchParams.set('tf', params.tf);
  if (params.from) url.searchParams.set('from', params.from.toString());
  if (params.to) url.searchParams.set('to', params.to.toString());

  const resp = await fetch(url.toString());

  if (!resp.ok) {
    throw new Error(`Failed to fetch candles: ${resp.status} ${resp.statusText}`);
  }

  const json = await resp.json();
  return json.data as OHLCVTPublic[];
}

// Load and display
const candles = await fetchCandles({
  exchange: 'binancef',
  symbol: 'btc/usdt',
  tf: '1m',
});

candleSeries.setData(candles.map(c => ({
  time: c.t as UTCTimestamp,
  open: c.o,
  high: c.h,
  low: c.l,
  close: c.c,
})));

chart.timeScale().fitContent();
```

## Loading State

Show a loading indicator while fetching data:

```typescript
function showLoading(container: HTMLElement): HTMLDivElement {
  const overlay = document.createElement('div');
  overlay.style.cssText = `
    position: absolute; inset: 0; z-index: 20;
    display: flex; align-items: center; justify-content: center;
    background: rgba(10, 10, 10, 0.7); color: #d1d5db;
    font-size: 14px;
  `;
  overlay.textContent = 'Loading chart data...';
  container.style.position = 'relative';
  container.appendChild(overlay);
  return overlay;
}

function hideLoading(overlay: HTMLDivElement) {
  overlay.remove();
}

// Usage
const overlay = showLoading(chartContainer);
try {
  const candles = await fetchCandles({ exchange, symbol, tf });
  candleSeries.setData(mapCandles(candles));
  volumeSeries.setData(mapCandlesToVolume(candles));
  chart.timeScale().fitContent();
} finally {
  hideLoading(overlay);
}
```

## Pagination for Long Ranges

The MMT API has a maximum number of data points per request. For long date ranges, paginate by chunking the time range:

```typescript
async function fetchCandlesPaginated(
  exchange: string,
  symbol: string,
  tf: string,
  from: number,
  to: number,
  maxPerRequest = 10000
): Promise<OHLCVTPublic[]> {
  const TF_SECONDS: Record<string, number> = {
    '1s': 1, '5s': 5, '15s': 15, '30s': 30,
    '1m': 60, '5m': 300, '15m': 900, '30m': 1800,
    '1h': 3600, '4h': 14400, '12h': 43200, '1d': 86400, '1w': 604800,
  };
  const tfSeconds = TF_SECONDS[tf] || 60;
  const maxRangeSeconds = maxPerRequest * tfSeconds;
  const allCandles: OHLCVTPublic[] = [];

  let currentFrom = from;
  while (currentFrom < to) {
    const currentTo = Math.min(currentFrom + maxRangeSeconds, to);
    const chunk = await fetchCandles({
      exchange, symbol, tf,
      from: currentFrom,
      to: currentTo,
    });

    allCandles.push(...chunk);

    if (chunk.length === 0) break;
    currentFrom = currentTo;
  }

  // Deduplicate by timestamp
  const seen = new Set<number>();
  return allCandles.filter(c => {
    if (seen.has(c.t)) return false;
    seen.add(c.t);
    return true;
  });
}
```

## Combining Historical Load with Live Updates

The standard pattern: fetch history first, then subscribe to WebSocket for live updates.

```typescript
async function initChart(exchange: string, symbol: string, tf: string) {
  // 1. Fetch historical data
  const candles = await fetchCandles({ exchange, symbol, tf });
  candleSeries.setData(mapCandles(candles));
  chart.timeScale().fitContent();

  // 2. Subscribe for live updates
  ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'candles',
    exchange,
    symbol,
    tf,
  }));

  // 3. Handle live updates
  ws.onmessage = (event) => {
    const raw = typeof event.data === 'string' ? event.data : new TextDecoder().decode(event.data);
    const msg = JSON.parse(raw);
    if (msg.type !== 'data' || msg.channel !== 'candles') return;

    const c = msg.data as OHLCVTPublic;
    candleSeries.update({
      time: c.t as UTCTimestamp,
      open: c.o,
      high: c.h,
      low: c.l,
      close: c.c,
    });
  };
}
```

## Error Handling

```typescript
async function loadWithRetry(
  params: FetchCandlesParams,
  retries = 3,
  delay = 1000
): Promise<OHLCVTPublic[]> {
  for (let attempt = 0; attempt < retries; attempt++) {
    try {
      return await fetchCandles(params);
    } catch (err) {
      if (attempt === retries - 1) throw err;
      await new Promise(r => setTimeout(r, delay * (attempt + 1)));
    }
  }
  throw new Error('Unreachable');
}
```

## Rules

- Always call `setData()` for the initial historical load, then use `update()` for subsequent live data.
- Data passed to `setData()` must be sorted ascending by `time`. MMT returns data sorted, but verify if merging from multiple sources.
- Call `chart.timeScale().fitContent()` after `setData()` to auto-zoom to show all loaded data.
- Show a loading overlay while fetching to prevent a blank chart flash.
- For paginated fetches, deduplicate by timestamp to handle overlap at chunk boundaries.
- All REST and WebSocket calls from browser code must go through your own server-side proxy. Never call the MMT API directly from the browser or expose the API key to client-side code.
- Handle fetch errors gracefully with retry logic; do not leave the chart in a broken state.
