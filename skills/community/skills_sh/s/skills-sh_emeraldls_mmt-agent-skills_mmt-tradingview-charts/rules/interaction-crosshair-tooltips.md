# Crosshair and Tooltips

Build custom tooltips that display MMT data fields (OHLC, buy/sell volume, trade counts) when the user hovers over the chart.

## subscribeCrosshairMove

```typescript
import type { MouseEventParams, ISeriesApi, SeriesType } from 'lightweight-charts';

chart.subscribeCrosshairMove((param: MouseEventParams) => {
  if (!param.time || !param.point) {
    hideTooltip();
    return;
  }

  const candleData = param.seriesData.get(candleSeries);
  const volumeData = param.seriesData.get(volumeSeries);

  if (candleData && 'open' in candleData) {
    showTooltip(param.point.x, param.point.y, candleData, volumeData);
  }
});
```

## Custom Tooltip Element

Create a tooltip div positioned near the crosshair:

```typescript
function createTooltipElement(container: HTMLElement): HTMLDivElement {
  const tooltip = document.createElement('div');
  tooltip.style.cssText = `
    position: absolute;
    z-index: 100;
    pointer-events: none;
    padding: 8px 12px;
    background: rgba(15, 15, 15, 0.95);
    border: 1px solid #374151;
    border-radius: 6px;
    font-size: 12px;
    font-family: 'Inter', monospace;
    color: #d1d5db;
    line-height: 1.6;
    white-space: nowrap;
    display: none;
  `;
  container.style.position = 'relative';
  container.appendChild(tooltip);
  return tooltip;
}

const tooltip = createTooltipElement(chartContainer);
```

## Display MMT Data Fields

Show OHLC plus buy/sell volume and trade counts from the original MMT data:

```typescript
// Keep a map of time → original MMT candle for tooltip access
const candleMap = new Map<number, OHLCVTPublic>();

function storeCandleData(candles: OHLCVTPublic[]) {
  for (const c of candles) {
    candleMap.set(c.t, c);
  }
}

function showTooltip(
  x: number,
  y: number,
  candle: { open: number; high: number; low: number; close: number; time: unknown },
  volumeData?: any
) {
  const mmtCandle = candleMap.get(candle.time as number);
  if (!mmtCandle) {
    tooltip.style.display = 'none';
    return;
  }

  const change = ((mmtCandle.c - mmtCandle.o) / mmtCandle.o) * 100;
  const changeColor = change >= 0 ? '#22c55e' : '#ef4444';
  const totalVol = mmtCandle.vb + mmtCandle.vs;
  const totalTrades = mmtCandle.tb + mmtCandle.ts;

  tooltip.innerHTML = `
    <div style="margin-bottom: 4px; font-weight: 600;">
      ${formatTime(mmtCandle.t)}
    </div>
    <div>O: <b>${mmtCandle.o.toFixed(2)}</b> H: <b>${mmtCandle.h.toFixed(2)}</b></div>
    <div>L: <b>${mmtCandle.l.toFixed(2)}</b> C: <b style="color: ${changeColor}">${mmtCandle.c.toFixed(2)}</b></div>
    <div style="color: ${changeColor}">Change: ${change >= 0 ? '+' : ''}${change.toFixed(2)}%</div>
    <div style="margin-top: 4px; border-top: 1px solid #374151; padding-top: 4px;">
      <div>Vol: <b>${formatNumber(totalVol)}</b></div>
      <div style="color: #22c55e">Buy: ${formatNumber(mmtCandle.vb)} (${((mmtCandle.vb / totalVol) * 100).toFixed(1)}%)</div>
      <div style="color: #ef4444">Sell: ${formatNumber(mmtCandle.vs)} (${((mmtCandle.vs / totalVol) * 100).toFixed(1)}%)</div>
    </div>
    <div style="margin-top: 4px; border-top: 1px solid #374151; padding-top: 4px;">
      <div>Trades: <b>${totalTrades}</b></div>
      <div style="color: #22c55e">Buy: ${mmtCandle.tb}</div>
      <div style="color: #ef4444">Sell: ${mmtCandle.ts}</div>
    </div>
  `;

  // Position tooltip
  const containerRect = chartContainer.getBoundingClientRect();
  const tooltipWidth = 180;
  const tooltipHeight = tooltip.offsetHeight || 200;

  let left = x + 16;
  let top = y - tooltipHeight / 2;

  // Keep within bounds
  if (left + tooltipWidth > containerRect.width) {
    left = x - tooltipWidth - 16;
  }
  if (top < 0) top = 0;
  if (top + tooltipHeight > containerRect.height) {
    top = containerRect.height - tooltipHeight;
  }

  tooltip.style.left = `${left}px`;
  tooltip.style.top = `${top}px`;
  tooltip.style.display = 'block';
}

function hideTooltip() {
  tooltip.style.display = 'none';
}
```

## Helper Formatters

```typescript
function formatTime(unixSeconds: number): string {
  const d = new Date(unixSeconds * 1000);
  return d.toLocaleString('en-US', {
    month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
    hour12: false,
  });
}

function formatNumber(value: number): string {
  if (value >= 1_000_000) return (value / 1_000_000).toFixed(2) + 'M';
  if (value >= 1_000) return (value / 1_000).toFixed(2) + 'K';
  return value.toFixed(2);
}
```

## Updating the Candle Map with Live Data

```typescript
ws.onmessage = (event) => {
  const raw = typeof event.data === 'string' ? event.data : new TextDecoder().decode(event.data);
  const msg = JSON.parse(raw);
  if (msg.type !== 'data' || msg.channel !== 'candles') return;

  const c = msg.data as OHLCVTPublic;
  candleMap.set(c.t, c); // Update map for tooltip access
  candleSeries.update(mapCandle(c));
};
```

## React: Isolating Tooltip Re-renders

`subscribeCrosshairMove` fires on every pixel of mouse movement (~60fps). If the crosshair callback calls `setState` in the chart component, the **entire** chart component (all effects, config, series setup) re-renders 60 times per second on hover. This is the single biggest performance mistake in React chart integrations.

Fix: isolate the tooltip into its own component using `forwardRef` + `useImperativeHandle`. The crosshair callback writes to a ref, which only re-renders the tiny tooltip host — not the parent chart:

```typescript
import { forwardRef, useImperativeHandle, useState } from 'react';

interface TooltipData {
  x: number;
  y: number;
  time: number;
  candle: OHLCVTPublic;
}

const TooltipHost = forwardRef<
  { update: (d: TooltipData | null) => void },
  {}
>(function TooltipHost(_, ref) {
  const [data, setData] = useState<TooltipData | null>(null);
  useImperativeHandle(ref, () => ({ update: setData }), []);
  if (!data) return null;
  return <ChartTooltip {...data} />;
});
```

In the chart component, use a ref to the tooltip host:

```typescript
function CandleChart({ exchange, symbol, tf }: CandleChartProps) {
  const tooltipRef = useRef<{ update: (d: TooltipData | null) => void }>(null);
  // ... chart setup ...

  useEffect(() => {
    if (!chartRef.current) return;

    chart.subscribeCrosshairMove((param) => {
      if (!param.time || !param.point) {
        tooltipRef.current?.update(null);
        return;
      }
      const candle = candleMap.get(param.time as number);
      if (candle) {
        tooltipRef.current?.update({
          x: param.point.x,
          y: param.point.y,
          time: param.time as number,
          candle,
        });
      }
    });
  }, []);

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
      <TooltipHost ref={tooltipRef} />
    </div>
  );
}
```

The crosshair callback now only re-renders `TooltipHost` (a few DOM nodes), never the parent `CandleChart` component.

### Candle Map: Mutate In Place

The `candleMap` is only read imperatively inside the crosshair callback (not via React subscription). Mutate it directly — do not clone it into state:

```typescript
// GOOD: mutate in place — no re-render, no allocation
const candleMap = useRef(new Map<number, OHLCVTPublic>());

ws.onmessage = (event) => {
  const raw = typeof event.data === 'string' ? event.data : new TextDecoder().decode(event.data);
  const msg = JSON.parse(raw);
  if (msg.type === 'data' && msg.channel === 'candles') {
    const c = msg.data as OHLCVTPublic;
    candleMap.current.set(c.t, c); // In-place mutation
    candleSeriesRef.current?.update(mapCandle(c));
  }
};

// BAD: cloning the Map on every WS message triggers re-render
// setCandleMap(new Map(candleMap)); // O(n) clone + re-render — DO NOT DO THIS
```

## Rules

- `subscribeCrosshairMove` fires on every mouse movement. Keep the handler fast; avoid heavy computations.
- Store original MMT candle data in a `Map<time, OHLCVTPublic>` so tooltips can access buy/sell breakdown, which is not available from the TV series data.
- Position the tooltip relative to `param.point.x/y` with boundary checks to keep it inside the container.
- Set `pointer-events: none` on the tooltip so it does not interfere with chart mouse events.
- Update the candle map with live data so tooltips for the current candle reflect the latest values.
- Hide the tooltip when `param.time` is `undefined` (crosshair leaves the chart).
- Use `display: none/block` rather than adding/removing the element to avoid layout thrashing.
- In React, isolate the tooltip into a `forwardRef` + `useImperativeHandle` component so crosshair updates only re-render the tooltip, not the parent chart.
- Never put the candle map in React state. It is only read imperatively — mutate in place via a ref.
