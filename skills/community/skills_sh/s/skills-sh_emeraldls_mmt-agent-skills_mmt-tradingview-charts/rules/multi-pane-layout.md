# Multi-Pane Layout

Build multi-pane chart layouts (price + volume + indicators) with synchronized time scales using separate chart instances.

## Layout Structure

Each pane is a separate `createChart()` instance stacked vertically in a container. Typical layout:

- **Price pane** (top, 60% height): Candlestick + overlays
- **Volume pane** (middle, 20% height): Volume histogram
- **Indicator pane** (bottom, 20% height): Funding rate, OI, etc.

```html
<div id="chart-wrapper" style="display: flex; flex-direction: column; width: 100%; height: 600px;">
  <div id="price-pane" style="flex: 3;"></div>
  <div id="volume-pane" style="flex: 1;"></div>
  <div id="indicator-pane" style="flex: 1;"></div>
</div>
```

## Creating Panes

```typescript
import { createChart, CandlestickSeries, HistogramSeries, LineSeries } from 'lightweight-charts';
import type { IChartApi, UTCTimestamp } from 'lightweight-charts';

function createPane(container: HTMLElement, options?: Partial<Parameters<typeof createChart>[1]>): IChartApi {
  return createChart(container, {
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
}

const priceChart = createPane(document.getElementById('price-pane')!);
const volumeChart = createPane(document.getElementById('volume-pane')!, {
  timeScale: { timeVisible: true, secondsVisible: false, borderColor: '#1f2937', visible: true },
});
const indicatorChart = createPane(document.getElementById('indicator-pane')!);

const candleSeries = priceChart.addSeries(CandlestickSeries);
const volumeSeries = volumeChart.addSeries(HistogramSeries, {
  priceFormat: { type: 'volume' },
});
const oiSeries = indicatorChart.addSeries(LineSeries, { color: '#8b5cf6' });
```

## Synchronize Time Scales

Sync scrolling and zooming across all panes using `subscribeVisibleLogicalRangeChange`:

```typescript
function syncTimeScales(charts: IChartApi[]) {
  let isSyncing = false;

  charts.forEach((sourceChart, sourceIndex) => {
    sourceChart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
      if (isSyncing || !range) return;
      isSyncing = true;

      charts.forEach((targetChart, targetIndex) => {
        if (targetIndex !== sourceIndex) {
          targetChart.timeScale().setVisibleLogicalRange(range);
        }
      });

      isSyncing = false;
    });
  });
}

syncTimeScales([priceChart, volumeChart, indicatorChart]);
```

## Synchronize Crosshair

Sync the crosshair position across panes so hovering one chart highlights the same time on all:

```typescript
function syncCrosshairs(charts: IChartApi[], seriesPerChart: any[]) {
  charts.forEach((sourceChart, sourceIndex) => {
    sourceChart.subscribeCrosshairMove((param) => {
      charts.forEach((targetChart, targetIndex) => {
        if (targetIndex === sourceIndex) return;

        if (!param.time) {
          targetChart.clearCrosshairPosition();
          return;
        }

        const series = seriesPerChart[targetIndex];
        const dataPoint = param.seriesData.get(seriesPerChart[sourceIndex]);
        if (dataPoint && 'time' in dataPoint) {
          targetChart.setCrosshairPosition(
            (dataPoint as any).value ?? (dataPoint as any).close ?? 0,
            series,
            dataPoint.time
          );
        }
      });
    });
  });
}

syncCrosshairs(
  [priceChart, volumeChart, indicatorChart],
  [candleSeries, volumeSeries, oiSeries]
);
```

## Resize Handling

Use a `ResizeObserver` on the wrapper to redistribute space:

```typescript
const wrapper = document.getElementById('chart-wrapper')!;

const resizeObserver = new ResizeObserver(() => {
  // autoSize handles each pane individually since each container resizes via flex
  // No manual chart.resize() needed when autoSize is true
});
resizeObserver.observe(wrapper);
```

## Hide Redundant Time Axes

Only show the time axis on the bottom-most pane:

```typescript
priceChart.timeScale().applyOptions({ visible: false });
volumeChart.timeScale().applyOptions({ visible: false });
// indicatorChart keeps its time axis visible (bottom pane)
```

## Rules

- Each pane is a separate `createChart()` call. There is no built-in multi-pane API in Lightweight Charts.
- Use a guard flag (`isSyncing`) in time scale sync to prevent infinite callback loops.
- Hide the time scale on upper panes to avoid redundant axes; only show it on the bottom pane.
- Use flex layout to distribute pane heights proportionally, and rely on `autoSize: true` to track changes.
- Call `chart.remove()` on every pane during cleanup — forgetting one leaks resources.
- Sync both time scale (scrolling) and crosshair (hover) for a cohesive multi-pane experience.
- The crosshair sync requires a reference to one series per chart for `setCrosshairPosition`.
