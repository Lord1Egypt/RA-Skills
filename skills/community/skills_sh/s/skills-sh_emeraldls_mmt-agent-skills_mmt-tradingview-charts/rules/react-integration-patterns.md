# React Integration Patterns

Integrate TradingView Lightweight Charts with React using hooks, refs, and proper lifecycle management.

## useChart Hook

A reusable hook that creates and manages the chart lifecycle:

```typescript
import { useEffect, useRef, useCallback } from 'react';
import { createChart, ColorType } from 'lightweight-charts';
import type { IChartApi, DeepPartial, ChartOptions } from 'lightweight-charts';

function useChart(
  containerRef: React.RefObject<HTMLDivElement | null>,
  options?: DeepPartial<ChartOptions>
) {
  const chartRef = useRef<IChartApi | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      autoSize: true,
      layout: {
        background: { type: ColorType.Solid, color: '#0a0a0a' },
        textColor: '#d1d5db',
      },
      grid: {
        vertLines: { color: '#1f2937' },
        horzLines: { color: '#1f2937' },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
        borderColor: '#1f2937',
      },
      rightPriceScale: { borderColor: '#1f2937' },
      ...options,
    });

    chartRef.current = chart;

    return () => {
      chart.remove();
      chartRef.current = null;
    };
  }, []); // Empty deps — create once

  return chartRef;
}
```

## Series Refs

Store series references in `useRef`, not `useState`. Series are mutable objects that should not trigger re-renders:

```typescript
import { useRef } from 'react';
import type { ISeriesApi, SeriesType } from 'lightweight-charts';

function useSeries() {
  const candleSeriesRef = useRef<ISeriesApi<SeriesType> | null>(null);
  const volumeSeriesRef = useRef<ISeriesApi<SeriesType> | null>(null);
  return { candleSeriesRef, volumeSeriesRef };
}
```

## Complete Chart Component

```tsx
import React, { useEffect, useRef, useState } from 'react';
import {
  createChart, CandlestickSeries, HistogramSeries, ColorType,
} from 'lightweight-charts';
import type { IChartApi, ISeriesApi, SeriesType, UTCTimestamp } from 'lightweight-charts';

interface CandleChartProps {
  exchange: string;
  symbol: string;
  tf: string;
}

export function CandleChart({ exchange, symbol, tf }: CandleChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candleRef = useRef<ISeriesApi<SeriesType> | null>(null);
  const volumeRef = useRef<ISeriesApi<SeriesType> | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const [loading, setLoading] = useState(true);

  // Create chart
  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      autoSize: true,
      layout: {
        background: { type: ColorType.Solid, color: '#0a0a0a' },
        textColor: '#d1d5db',
      },
      timeScale: { timeVisible: true, secondsVisible: false },
    });

    const candleSeries = chart.addSeries(CandlestickSeries);
    const volumeSeries = chart.addSeries(HistogramSeries, {
      priceScaleId: 'volume',
      priceFormat: { type: 'volume' },
      lastValueVisible: false,
      priceLineVisible: false,
    });

    chart.priceScale('volume').applyOptions({
      scaleMargins: { top: 0.8, bottom: 0 },
    });

    chartRef.current = chart;
    candleRef.current = candleSeries;
    volumeRef.current = volumeSeries;

    return () => {
      chart.remove();
      chartRef.current = null;
      candleRef.current = null;
      volumeRef.current = null;
    };
  }, []);

  // Load data and subscribe when exchange/symbol/tf change
  useEffect(() => {
    const chart = chartRef.current;
    const candleSeries = candleRef.current;
    const volumeSeries = volumeRef.current;
    if (!chart || !candleSeries || !volumeSeries) return;

    let cancelled = false;

    async function loadData() {
      setLoading(true);

      try {
        // Fetch through your own server-side proxy — never call MMT directly from browser
        const params = new URLSearchParams({ exchange, symbol, tf });
        const resp = await fetch(`/api/mmt/candles?${params}`);
        const { data } = await resp.json();
        if (cancelled) return;

        const candles = data as OHLCVTPublic[];

        candleSeries.setData(candles.map(c => ({
          time: c.t as UTCTimestamp,
          open: c.o, high: c.h, low: c.l, close: c.c,
        })));

        volumeSeries.setData(candles.map(c => ({
          time: c.t as UTCTimestamp,
          value: c.vb + c.vs,
          color: c.vb > c.vs
            ? 'rgba(34, 197, 94, 0.5)'
            : 'rgba(239, 68, 68, 0.5)',
        })));

        chart.timeScale().fitContent();
      } catch (err) {
        console.error('Failed to load candles:', err);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadData();

    // Connect to your own server's WS proxy — never expose MMT API key to browser
    const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws`;
    const ws = new WebSocket(wsUrl);
    ws.binaryType = 'arraybuffer';

    ws.onopen = () => {
      ws.send(JSON.stringify({
        type: 'subscribe',
        channel: 'candles',
        exchange, symbol, tf,
      }));
    };

    ws.onmessage = (event) => {
      const raw = typeof event.data === 'string' ? event.data : new TextDecoder().decode(event.data);
      const msg = JSON.parse(raw);
      if (msg.type !== 'data' || msg.channel !== 'candles') return;

      const c = msg.data as OHLCVTPublic;
      const time = c.t as UTCTimestamp;

      candleRef.current?.update({
        time, open: c.o, high: c.h, low: c.l, close: c.c,
      });

      volumeRef.current?.update({
        time,
        value: c.vb + c.vs,
        color: c.vb > c.vs
          ? 'rgba(34, 197, 94, 0.5)'
          : 'rgba(239, 68, 68, 0.5)',
      });
    };

    wsRef.current = ws;

    return () => {
      cancelled = true;
      ws.close(1000);
      wsRef.current = null;
    };
  }, [exchange, symbol, tf]);

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
      {loading && (
        <div style={{
          position: 'absolute', inset: 0,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          background: 'rgba(10, 10, 10, 0.7)', color: '#d1d5db',
          fontSize: 14, zIndex: 20,
        }}>
          Loading...
        </div>
      )}
    </div>
  );
}
```

## Key Patterns

### Separate chart creation from data loading

The chart is created once (empty deps `[]`). Data loading reacts to prop changes (`[exchange, symbol, tf]`). This avoids destroying and recreating the chart DOM on every prop change.

### Use cancelled flag for async cleanup

The `cancelled` flag prevents state updates after the component unmounts or the effect re-runs:

```typescript
useEffect(() => {
  let cancelled = false;
  async function load() {
    const data = await fetchData();
    if (!cancelled) setData(data);
  }
  load();
  return () => { cancelled = true; };
}, [deps]);
```

### Access series via refs in callbacks

WebSocket `onmessage` callbacks capture refs, not state. Using `useRef` ensures the callback always has the latest series reference:

```typescript
// Use candleRef.current (always current)
// NOT candleSeries from useState (stale in closure)
ws.onmessage = () => {
  candleRef.current?.update(data);
};
```

## Dynamic Import for Chart Components

Always lazy-load chart components — `lightweight-charts` is ~45KB gzipped and requires canvas APIs unavailable during SSR:

```typescript
import { Suspense, lazy } from 'react';

const CandleChart = lazy(() => import('./CandleChart'));

function TradingDashboard() {
  return (
    <Suspense fallback={
      <div style={{ width: '100%', height: 400, background: '#111' }} />
    }>
      <CandleChart exchange="binancef" symbol="btc/usdt" tf="1m" />
    </Suspense>
  );
}
```

In Next.js, use `dynamic` with `ssr: false`:

```typescript
import dynamic from 'next/dynamic';

const CandleChart = dynamic(() => import('./CandleChart'), {
  ssr: false,
  loading: () => <div style={{ width: '100%', height: 400, background: '#111' }} />,
});
```

## High-Frequency Display Values: Refs + requestAnimationFrame

For values that update faster than the screen refreshes (prices, volumes, P&L), bypass React's render cycle entirely. Write directly to the DOM via refs:

```typescript
function RealtimePrice({ wsRef }: { wsRef: React.RefObject<WebSocket> }) {
  const priceRef = useRef<HTMLSpanElement>(null);
  const rafId = useRef(0);
  const latest = useRef(0);

  useEffect(() => {
    function onMessage(event: MessageEvent) {
      const raw = typeof event.data === 'string' ? event.data : new TextDecoder().decode(event.data);
      const msg = JSON.parse(raw);
      if (msg.channel !== 'stats') return;
      latest.current = msg.data.mp;

      cancelAnimationFrame(rafId.current);
      rafId.current = requestAnimationFrame(() => {
        if (priceRef.current) priceRef.current.textContent = latest.current.toFixed(2);
      });
    }

    wsRef.current?.addEventListener('message', onMessage);
    return () => {
      wsRef.current?.removeEventListener('message', onMessage);
      cancelAnimationFrame(rafId.current);
    };
  }, []);

  return <span ref={priceRef} />;
}
```

This produces at most 60 DOM writes per second regardless of message rate. Use `useState` only when the value must trigger child re-renders.

## State Management for Trading UIs

Trading terminals have data flowing at different frequencies — some drives UI re-renders, most does not. Use these patterns to prevent unnecessary work.

### Individual Zustand Selectors

Never destructure the whole store. Each field should be its own selector:

```typescript
// BAD: re-renders when ANY store field changes
const { asks, bids, spread, isReady } = useOrderbookStore();

// GOOD: only re-renders when this specific field changes
const asks = useOrderbookStore((s) => s.asks);
const bids = useOrderbookStore((s) => s.bids);
const spread = useOrderbookStore((s) => s.spread);
```

### Imperative Store Access for Actions

Store actions (setters, updaters) should be called via `getState()` in callbacks and effects, not subscribed to reactively:

```typescript
// BAD: subscribes to setLoading reactively (it's an action, not render data)
const { loading, setLoading, setCandleMap } = useChartStore();

// GOOD: only subscribe to data that drives render output
const loading = useChartStore((s) => s.loading);

// Access actions imperatively in effects/callbacks
useEffect(() => {
  useChartStore.getState().setLoading(true);
  fetchCandles().then((data) => {
    useChartStore.getState().setCandleMap(data);
    useChartStore.getState().setLoading(false);
  });
}, []);
```

### Mutate In Place for Non-Reactive Data

If data is only read imperatively via `getState()` (never via React subscription), mutate it directly. Do not call `set()` — it triggers subscriber notifications and re-renders for nothing:

```typescript
// BAD: clones the entire Map (O(n)) on every WS message + notifies all subscribers
updateCandle: (candle) => set({ candleMap: new Map(get().candleMap) }),

// GOOD: mutate in place — O(1), no re-render
updateCandle: (candle) => get().candleMap.set(candle.t, candle),
```

Use this only when the data is read via `useChartStore.getState().candleMap` (e.g., in a tooltip callback), never via `useChartStore((s) => s.candleMap)`.

### React.memo on List Items

Always wrap list item components and leaf components rendered inside frequently-updating parents. **Pass primitive props only** — `React.memo` does shallow comparison of references. A new `{ price, size, total }` object every cycle defeats memo entirely:

```typescript
// GOOD: primitive props — memo can compare values directly
const OrderbookRow = React.memo(function OrderbookRow({
  price, size, total, side, maxTotal,
}: {
  price: number; size: number; total: number; side: string; maxTotal: number;
}) {
  const width = (total / maxTotal) * 100;
  return (
    <div className={`ob-row ${side}`}>
      <div className="ob-depth" style={{ width: `${width}%` }} />
      <span>{price.toFixed(2)}</span>
      <span>{size.toFixed(4)}</span>
      <span>{total.toFixed(4)}</span>
    </div>
  );
});

// BAD: passing an object prop defeats memo — new object ref every render
// <OrderbookRow data={{ price, size, total }} /> — NEVER DO THIS

const TradeRow = React.memo(function TradeRow({
  price, size, time, side,
}: {
  price: number; size: number; time: number; side: string;
}) {
  return (
    <div className={`trade-row ${side}`}>
      <span>{price.toFixed(2)}</span>
      <span>{size.toFixed(4)}</span>
      <span>{formatTime(time)}</span>
    </div>
  );
});
```

Components to always memo: `OrderbookRow`, `TradeRow`, `StatItem`, `ChartLegend`, `WidgetFrame`, and any component rendered 20+ times inside a parent that re-renders at data-feed frequency.

### useMemo for Derived Calculations

Memoize derived values that iterate arrays, keyed on the data they depend on:

```typescript
function OrderbookWidget({ asks, bids }: { asks: Level[]; bids: Level[] }) {
  const maxTotal = useMemo(() => {
    const maxAsk = asks.length ? asks[asks.length - 1].total : 0;
    const maxBid = bids.length ? bids[bids.length - 1].total : 0;
    return Math.max(maxAsk, maxBid);
  }, [asks, bids]);

  return (
    <>
      {asks.map((a, i) => (
        <OrderbookRow key={i} {...a} side="ask" maxTotal={maxTotal} />
      ))}
      {bids.map((b, i) => (
        <OrderbookRow key={i} {...b} side="bid" maxTotal={maxTotal} />
      ))}
    </>
  );
}
```

### CSS content-visibility for Scrollable Lists

For lists with 20-200 items of fixed height, apply `content-visibility: auto`. The browser skips layout and paint for off-screen rows — zero JS required:

```css
.cv-auto {
  content-visibility: auto;
  contain-intrinsic-size: auto 18px; /* estimated row height */
}
```

```tsx
{trades.map((t, i) => (
  <TradeRow key={i} className="cv-auto" {...t} />
))}
```

For 200+ items, use `react-window` virtualization instead — `content-visibility` still measures all items on scroll, while virtualization only renders the visible window.

## High-Frequency List Rendering

Orderbook and trade lists update at WS message rate (10-100+/sec) but humans cannot distinguish list updates faster than ~10fps. Throttle store updates to 100-120ms using `setTimeout`, not `requestAnimationFrame` — rAF fires at display refresh rate (60-144fps) which is overkill for text-based lists.

### Batch WS Messages in a Ref, Flush on Timer

Buffer incoming messages in a `useRef` array and flush to the store on a timer. One `addTrades(batch)` call is dramatically cheaper than N individual `addTrade()` calls because each `set()` triggers a full React reconciliation pass:

```typescript
function useThrottledWsFeed(
  ws: WebSocket | null,
  channel: string,
  onFlush: (batch: any[]) => void,
  intervalMs: number = 120
) {
  const bufferRef = useRef<any[]>([]);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (!ws) return;

    function onMessage(event: MessageEvent) {
      const raw = typeof event.data === 'string'
        ? event.data : new TextDecoder().decode(event.data);
      const msg = JSON.parse(raw);
      if (msg.channel !== channel) return;

      bufferRef.current.push(msg.data);

      // Schedule flush if not already scheduled
      if (!timerRef.current) {
        timerRef.current = setTimeout(() => {
          const batch = bufferRef.current;
          bufferRef.current = [];
          timerRef.current = null;
          if (batch.length > 0) onFlush(batch);
        }, intervalMs);
      }
    }

    ws.addEventListener('message', onMessage);
    return () => {
      ws.removeEventListener('message', onMessage);
      if (timerRef.current) {
        clearTimeout(timerRef.current);
        timerRef.current = null;
      }
      bufferRef.current = [];
    };
  }, [ws, channel, onFlush, intervalMs]);
}

// Usage: batch trades at 120ms intervals (~8fps)
useThrottledWsFeed(ws, 'trades', (batch) => {
  useTradeStore.getState().addTrades(batch);
});
```

### Store Setter: Enforce Caps on Accumulating Arrays

Every store that accumulates data (trades, liquidations) must enforce a cap in the setter itself:

```typescript
const useTradeStore = create<TradeStore>((set, get) => ({
  trades: [] as Trade[],
  addTrades: (batch: Trade[]) => {
    const MAX_TRADES = 200;
    const current = get().trades;
    const merged = [...batch, ...current].slice(0, MAX_TRADES);
    set({ trades: merged });
  },
}));
```

## Cleanup Checklist

Trading terminals run for hours. Every uncleaned resource compounds into a crash. On unmount:

1. Close WebSocket connections (`ws.close()`)
2. Clear all `setInterval` and `setTimeout` handles
3. Cancel all `requestAnimationFrame` handles
4. Remove DOM event listeners (`resize`, `mousemove`)
5. Call `chart.remove()` on chart instances (releases canvas + listeners)
6. Abort in-flight `fetch` requests via `AbortController`
7. Terminate Web Workers

## Rules

- Create the chart in a `useEffect` with empty dependencies. Return `chart.remove()` in the cleanup function.
- Store series references in `useRef`, not `useState`. Series mutations should not trigger re-renders.
- Close WebSocket connections in the `useEffect` cleanup that created them.
- Use a `cancelled` flag to prevent async callbacks from updating state after unmount.
- Separate chart creation (once) from data loading (on prop change) into different `useEffect` hooks.
- Access series via `.current` on refs inside WebSocket callbacks to avoid stale closures.
- Container div needs explicit height (e.g., `height: 100%` with a parent that has a defined height, or a fixed pixel value).
- Never call `chart.remove()` during a render. Always do it in effect cleanup.
- Lazy-load chart components with `React.lazy()` or Next.js `dynamic()` with `ssr: false`.
- For high-frequency display values (prices, tickers), use `useRef` + `requestAnimationFrame` instead of `useState` to avoid unnecessary re-renders.
- Use virtualized lists (`react-window`) for 200+ items. For 20-200 items, use `content-visibility: auto` CSS.
- Clean up ALL side effects on unmount: WebSockets, timers, rAF handles, chart instances, event listeners, AbortControllers.
- Always use individual Zustand selectors `useStore((s) => s.field)`. Never destructure `useStore()`.
- Access store actions via `useStore.getState().action()` in callbacks/effects — do not subscribe to actions reactively.
- If data is only read via `getState()` (never via React subscription), mutate it in place. Do not call `set()`.
- Wrap all list item components and leaf components in `React.memo()` — especially `OrderbookRow`, `TradeRow`, `StatItem`.
- Memoize derived calculations with `useMemo()` keyed on their data dependencies.
- Isolate high-frequency UI updates (crosshair tooltips, scroll-linked elements) into their own components with `forwardRef` + `useImperativeHandle`. Never let high-frequency state updates propagate through parent components.
- Never put chart data (candle maps, series data) in React state. Use refs for data that is only read imperatively.
- Throttle list store updates (orderbook, trades) to ~8-10fps (100-120ms) using `setTimeout`. Do not use `requestAnimationFrame` for text lists — 60fps is wasted work.
- Batch WS messages in a `useRef` array and flush to the store on a timer. One `addTrades(batch)` is cheaper than N individual `addTrade()` calls.
- Never pass object props to `React.memo` components — use primitive props (number, string) so shallow comparison works.
- Enforce caps on all accumulating arrays in store setters (e.g., 200 trades, 50 liquidations). Never rely on consumers to trim.
