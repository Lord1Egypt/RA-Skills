# Chart Lifecycle

Manage chart creation, resize, cleanup, and memory across component lifecycles in any framework.

## Creation

Always create the chart after the container element is in the DOM with non-zero dimensions:

```typescript
import { createChart, CandlestickSeries } from 'lightweight-charts';
import type { IChartApi } from 'lightweight-charts';

let chart: IChartApi | null = null;

function initChart(container: HTMLElement) {
  if (container.clientWidth === 0 || container.clientHeight === 0) {
    console.warn('Container has zero dimensions; deferring chart creation');
    return;
  }

  chart = createChart(container, { autoSize: true });
  const series = chart.addSeries(CandlestickSeries);
  return { chart, series };
}
```

## Resize Handling

With `autoSize: true`, the chart automatically tracks container size changes via `ResizeObserver` internally. No manual resize code is needed.

If you must use manual sizing (e.g., `autoSize: false`):

```typescript
const chart = createChart(container, { width: 800, height: 500 });

const resizeObserver = new ResizeObserver((entries) => {
  for (const entry of entries) {
    const { width, height } = entry.contentRect;
    chart.resize(width, height);
  }
});
resizeObserver.observe(container);

// Cleanup
function destroy() {
  resizeObserver.disconnect();
  chart.remove();
}
```

## WebSocket Cleanup

Always pair chart destruction with WS unsubscription:

```typescript
class ChartLifecycle {
  private chart: IChartApi | null = null;
  private ws: WebSocket | null = null;
  private subscriptions: { channel: string; exchange: string; symbol: string; tf?: string }[] = [];

  create(container: HTMLElement, ws: WebSocket) {
    this.chart = createChart(container, { autoSize: true });
    this.ws = ws;
  }

  subscribe(channel: string, exchange: string, symbol: string, tf?: string) {
    const sub = { channel, exchange, symbol, tf };
    this.subscriptions.push(sub);
    this.ws?.send(JSON.stringify({ type: 'subscribe', ...sub }));
  }

  destroy() {
    // Unsubscribe all
    for (const sub of this.subscriptions) {
      this.ws?.send(JSON.stringify({ type: 'unsubscribe', ...sub }));
    }
    this.subscriptions = [];

    // Remove chart
    if (this.chart) {
      this.chart.remove();
      this.chart = null;
    }
  }
}
```

## Memory Management

Calling `chart.remove()` releases:
- All series and their data
- Internal `ResizeObserver` (when `autoSize` is used)
- Canvas/WebGL rendering context
- Event subscriptions (crosshair, click handlers)

After `remove()`, the chart instance is invalid. Do not call any methods on it.

```typescript
// Correct cleanup order
function cleanup() {
  // 1. Clear custom event handlers and timers
  clearInterval(pingInterval);
  clearTimeout(pongTimeout);

  // 2. Remove custom DOM elements (tooltips, legends)
  tooltip?.remove();
  legend?.remove();

  // 3. Unsubscribe WS channels
  for (const sub of subscriptions) {
    ws.send(JSON.stringify({ type: 'unsubscribe', ...sub }));
  }

  // 4. Remove chart (releases canvas, WebGL, internal observers)
  chart.remove();

  // 5. Close WS if this component owns it
  // ws.close(1000);
}
```

## Re-creation

If chart options change significantly (e.g., switching between dark/light theme), remove and recreate:

```typescript
function recreateChart(container: HTMLElement, newOptions: any) {
  if (chart) {
    chart.remove();
  }
  chart = createChart(container, newOptions);
  // Re-add series, re-load data, re-subscribe
}
```

## Error Handling

Wrap chart creation in try/catch and show a fallback:

```typescript
function safeInitChart(container: HTMLElement) {
  try {
    const chart = createChart(container, { autoSize: true });
    return chart;
  } catch (err) {
    console.error('Failed to create chart:', err);
    container.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:center;height:100%;color:#9ca3af;">
        Chart failed to load. Please refresh.
      </div>
    `;
    return null;
  }
}
```

## Vanilla JS Complete Example

```typescript
const container = document.getElementById('chart')!;
const lifecycle = new ChartLifecycle();

// Create
lifecycle.create(container, ws);
const series = lifecycle.chart!.addSeries(CandlestickSeries);

// Load data
const candles = await fetchCandles({ exchange: 'binancef', symbol: 'btc/usdt', tf: '1m' });
series.setData(mapCandles(candles));
lifecycle.chart!.timeScale().fitContent();

// Subscribe live
lifecycle.subscribe('candles', 'binancef', 'btc/usdt', '1m');

// Later: cleanup
lifecycle.destroy();
```

## Rules

- Always call `chart.remove()` when the chart is no longer needed. Skipping this leaks canvas, WebGL context, and observers.
- Prefer `autoSize: true` over manual `ResizeObserver` + `chart.resize()` — it handles the common case.
- Container must have non-zero width and height before `createChart()` is called; otherwise the canvas initializes at 0x0.
- Clean up in order: timers/handlers first, then WS unsubscribe, then `chart.remove()`, then DOM elements.
- After `chart.remove()`, do not reference the chart or any series objects. Set references to `null`.
- On chart creation failure, display a fallback message instead of leaving a blank container.
- Do not close the WebSocket on chart destroy if the WebSocket is shared across multiple components.
