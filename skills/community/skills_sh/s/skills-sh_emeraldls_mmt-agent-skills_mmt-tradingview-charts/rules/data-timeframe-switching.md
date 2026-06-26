# Timeframe and Symbol Switching

Handle timeframe, symbol, and exchange changes by clearing all state, flushing timers, fetching new data, and re-subscribing to the WebSocket.

## Switching Pattern

When the user changes timeframe, the complete cycle is:
1. Unsubscribe from the current WS channel
2. Fetch historical data for the new timeframe
3. Replace chart data with `setData()`
4. Subscribe to the new WS channel
5. Resume live updates

```typescript
import type { UTCTimestamp, ISeriesApi, SeriesType } from 'lightweight-charts';

class ChartManager {
  private ws: WebSocket;
  private candleSeries: ISeriesApi<SeriesType>;
  private volumeSeries: ISeriesApi<SeriesType>;
  private currentTf: string;
  private exchange: string;
  private symbol: string;
  private isLoading = false;

  constructor(
    ws: WebSocket,
    candleSeries: ISeriesApi<SeriesType>,
    volumeSeries: ISeriesApi<SeriesType>,
    exchange: string,
    symbol: string,
    initialTf: string
  ) {
    this.ws = ws;
    this.candleSeries = candleSeries;
    this.volumeSeries = volumeSeries;
    this.exchange = exchange;
    this.symbol = symbol;
    this.currentTf = initialTf;
  }

  async switchTimeframe(newTf: string) {
    if (this.isLoading || newTf === this.currentTf) return;
    this.isLoading = true;

    try {
      // 1. Unsubscribe current
      this.ws.send(JSON.stringify({
        type: 'unsubscribe',
        channel: 'candles',
        exchange: this.exchange,
        symbol: this.symbol,
        tf: this.currentTf,
      }));

      // 2. Fetch new data
      const candles = await fetchCandles({
        exchange: this.exchange,
        symbol: this.symbol,
        tf: newTf,
      });

      // 3. Replace data
      this.candleSeries.setData(candles.map(c => ({
        time: c.t as UTCTimestamp,
        open: c.o, high: c.h, low: c.l, close: c.c,
      })));

      this.volumeSeries.setData(candles.map(c => ({
        time: c.t as UTCTimestamp,
        value: c.vb + c.vs,
        color: c.vb > c.vs
          ? 'rgba(34, 197, 94, 0.5)'
          : 'rgba(239, 68, 68, 0.5)',
      })));

      chart.timeScale().fitContent();

      // 4. Subscribe new
      this.ws.send(JSON.stringify({
        type: 'subscribe',
        channel: 'candles',
        exchange: this.exchange,
        symbol: this.symbol,
        tf: newTf,
      }));

      this.currentTf = newTf;
    } finally {
      this.isLoading = false;
    }
  }
}
```

## Preserve Scroll Position

Optionally save and restore the visible time range across timeframe switches:

```typescript
async switchTimeframePreservePosition(newTf: string) {
  // Save current visible range
  const visibleRange = chart.timeScale().getVisibleRange();

  // ... fetch and set new data (same as above) ...

  // Restore range if possible
  if (visibleRange) {
    chart.timeScale().setVisibleRange(visibleRange);
  } else {
    chart.timeScale().fitContent();
  }
}
```

## Debounce Rapid Changes

Prevent fetching data for intermediate timeframes when the user clicks through options quickly:

```typescript
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timer: ReturnType<typeof setTimeout>;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

const debouncedSwitch = debounce(
  (tf: string) => chartManager.switchTimeframe(tf),
  200
);

// UI handler
tfButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    debouncedSwitch(btn.dataset.tf!);
  });
});
```

## Timeframe Button Bar

Common timeframes for crypto charts:

```typescript
const TIMEFRAMES = [
  { label: '1s',  value: '1s' },
  { label: '5s',  value: '5s' },
  { label: '15s', value: '15s' },
  { label: '30s', value: '30s' },
  { label: '1m',  value: '1m' },
  { label: '5m',  value: '5m' },
  { label: '15m', value: '15m' },
  { label: '30m', value: '30m' },
  { label: '1h',  value: '1h' },
  { label: '4h',  value: '4h' },
  { label: '12h', value: '12h' },
  { label: '1d',  value: '1d' },
  { label: '1w',  value: '1w' },
];
```

## Loading State During Transition

```typescript
async switchTimeframe(newTf: string) {
  if (this.isLoading) return;
  this.isLoading = true;

  const overlay = showLoading(chartContainer);

  try {
    // ... switch logic ...
  } catch (err) {
    console.error('Failed to switch timeframe:', err);
    // Stay on current timeframe, do not update this.currentTf
  } finally {
    hideLoading(overlay);
    this.isLoading = false;
  }
}
```

## Symbol / Exchange Switching: Data Cleanup

When the user changes symbol or exchange, **every widget** that owns a WS subscription or accumulates data must fully reset. Old symbol data is never valid for the new symbol.

### Clear All Stores

Every store that holds market data must clear on dependency change:

```typescript
// In each store that holds per-symbol data
const useOrderbookStore = create<OrderbookStore>((set) => ({
  asks: [],
  bids: [],
  spread: 0,
  isReady: false,
  clear: () => set({ asks: [], bids: [], spread: 0, isReady: false }),
  // ...
}));

const useTradeStore = create<TradeStore>((set) => ({
  trades: [],
  clear: () => set({ trades: [] }),
  // ...
}));
```

### Flush Batching Timers

Any `setTimeout` used for throttling (trade batching, orderbook throttling) must be cleared when deps change. Otherwise stale data from the old symbol leaks into the new symbol's store:

```typescript
useEffect(() => {
  // Clear all stores immediately
  useOrderbookStore.getState().clear();
  useTradeStore.getState().clear();
  useStatsStore.getState().clear();
  useChartStore.getState().clear();

  // Set up subscriptions for new symbol...
  const timerRef = { current: null as ReturnType<typeof setTimeout> | null };

  // ... batching logic with timerRef ...

  return () => {
    // Flush timer on cleanup to prevent stale data leak
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  };
}, [exchange, symbol, tf]);
```

### Complete Switch Sequence

```
1. Clear all per-symbol stores (orderbook, trades, stats, chart)
2. Flush all batching timers
3. Unsubscribe from current WS channels
4. Cancel in-flight REST fetches (AbortController)
5. Fetch new historical data
6. Replace chart data with setData()
7. Subscribe to new WS channels
8. Resume live updates
```

## Rules

- Always unsubscribe the current WS channel before subscribing to the new one to avoid receiving stale data.
- Use `setData()` (not repeated `update()`) when switching timeframes — it replaces the entire dataset.
- Guard against concurrent switches with an `isLoading` flag; reject new switches while one is in progress.
- Debounce rapid timeframe changes (200ms) to avoid unnecessary API requests.
- Show a loading state during the transition so the chart does not appear frozen or empty.
- Timeframe values sent to MMT use named format strings: `"1m"` for 1 minute, `"1h"` for 1 hour.
- Valid timeframes are a fixed set: `1s`, `5s`, `15s`, `30s`, `1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `12h`, `1d`, `1w`.
- On error, stay on the current timeframe rather than leaving the chart in an empty state.
- On symbol/exchange switch, clear ALL per-symbol stores immediately. Old data is never valid for the new symbol.
- Flush all batching timers (`setTimeout`) on switch to prevent stale data from leaking across symbols.
- Cancel in-flight REST requests via `AbortController` on switch — their responses are no longer relevant.
- Bound all accumulating arrays (trades, liquidations) in store setters. Pick the minimum cap that makes visual sense (50 liquidation events, 200 trades).
