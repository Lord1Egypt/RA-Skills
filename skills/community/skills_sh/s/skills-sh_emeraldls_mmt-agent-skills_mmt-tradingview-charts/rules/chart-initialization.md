# Chart Initialization

Configure and create a TradingView Lightweight Charts instance optimized for MMT crypto market data.

## Installation

```bash
npm install lightweight-charts
```

## Basic Setup

```typescript
import { createChart, ColorType } from 'lightweight-charts';
import type { IChartApi, DeepPartial, ChartOptions } from 'lightweight-charts';

function createMMTChart(
  container: HTMLElement,
  theme: 'dark' | 'light' = 'dark'
): IChartApi {
  const isDark = theme === 'dark';

  const chart = createChart(container, {
    autoSize: true,
    layout: {
      background: {
        type: ColorType.Solid,
        color: isDark ? '#0a0a0a' : '#ffffff',
      },
      textColor: isDark ? '#d1d5db' : '#374151',
      fontFamily: "'Inter', -apple-system, sans-serif",
      fontSize: 12,
    },
    grid: {
      vertLines: { color: isDark ? '#1f2937' : '#e5e7eb' },
      horzLines: { color: isDark ? '#1f2937' : '#e5e7eb' },
    },
    timeScale: {
      timeVisible: true,
      secondsVisible: false,
      borderColor: isDark ? '#1f2937' : '#d1d5db',
      rightOffset: 5,
      barSpacing: 8,
      minBarSpacing: 2,
    },
    rightPriceScale: {
      borderColor: isDark ? '#1f2937' : '#d1d5db',
      scaleMargins: {
        top: 0.1,
        bottom: 0.1,
      },
    },
    crosshair: {
      mode: 0, // Normal crosshair
      vertLine: {
        color: isDark ? '#4b5563' : '#9ca3af',
        width: 1,
        style: 2, // Dashed
        labelBackgroundColor: isDark ? '#374151' : '#e5e7eb',
      },
      horzLine: {
        color: isDark ? '#4b5563' : '#9ca3af',
        width: 1,
        style: 2,
        labelBackgroundColor: isDark ? '#374151' : '#e5e7eb',
      },
    },
  });

  return chart;
}
```

## Container Setup

The container element must have explicit dimensions. Use CSS to set width/height, then rely on `autoSize: true` to track changes.

```html
<div id="chart-container" style="width: 100%; height: 500px;"></div>
```

```typescript
const container = document.getElementById('chart-container')!;
const chart = createMMTChart(container, 'dark');
```

## Watermark

Add an exchange/symbol watermark for context:

```typescript
const chart = createChart(container, {
  // ...other options
  watermark: {
    visible: true,
    text: 'BTC/USDT - Binance Futures',
    fontSize: 48,
    color: isDark ? 'rgba(255, 255, 255, 0.04)' : 'rgba(0, 0, 0, 0.04)',
    horzAlign: 'center',
    vertAlign: 'center',
  },
});
```

## Crypto-Specific Price Formatting

For crypto assets with varying decimal precision:

```typescript
function getPriceFormat(symbol: string) {
  const base = symbol.split('/')[0].toLowerCase();
  // High-value assets: 2 decimals, others: more
  if (['btc', 'eth'].includes(base)) {
    return { type: 'price' as const, precision: 2, minMove: 0.01 };
  }
  return { type: 'price' as const, precision: 5, minMove: 0.00001 };
}
```

## Rules

- Always set `autoSize: true` for responsive charts instead of manually handling resize.
- Use `ColorType.Solid` for background — gradient backgrounds are not supported.
- Set `timeScale.timeVisible: true` for intraday timeframes so hours/minutes display.
- Set `rightOffset: 5` or more to leave space for incoming real-time candles.
- Set `crosshair.mode: 0` (Normal) for full crosshair; use `1` (Magnet) to snap to candle values.
- Container must have non-zero width and height before calling `createChart`.
- Call `chart.remove()` when destroying the chart to release WebGL and DOM resources.
