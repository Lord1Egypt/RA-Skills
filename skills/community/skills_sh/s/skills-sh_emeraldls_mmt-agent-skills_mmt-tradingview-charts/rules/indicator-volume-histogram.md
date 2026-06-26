# Volume Histogram

Display buy/sell volume from MMT candle data as a colored histogram overlaid on the price chart.

## Volume from Candle Data

MMT candles (`OHLCVTPublic`) include buy volume (`vb`) and sell volume (`vs`) per candle. Total volume is `vb + vs`. Color by whether buyers or sellers dominated the candle.

## Setup as Bottom Overlay

Place the volume histogram at the bottom of the price chart using a separate price scale with margins:

```typescript
import { createChart, CandlestickSeries, HistogramSeries, ColorType } from 'lightweight-charts';
import type { UTCTimestamp } from 'lightweight-charts';

const chart = createChart(container, {
  autoSize: true,
  layout: {
    background: { type: ColorType.Solid, color: '#0a0a0a' },
    textColor: '#d1d5db',
  },
});

// Price series
const candleSeries = chart.addSeries(CandlestickSeries);

// Volume series on a separate price scale
const volumeSeries = chart.addSeries(HistogramSeries, {
  priceScaleId: 'volume',
  priceFormat: { type: 'volume' },
  lastValueVisible: false,
  priceLineVisible: false,
});

// Position volume at the bottom 20% of the chart
chart.priceScale('volume').applyOptions({
  scaleMargins: {
    top: 0.8,
    bottom: 0,
  },
});
```

## Map MMT Candle Data to Volume Histogram

```typescript
interface VolumeBar {
  time: UTCTimestamp;
  value: number;
  color: string;
}

const VOLUME_COLORS = {
  buy: 'rgba(34, 197, 94, 0.5)',   // Semi-transparent green
  sell: 'rgba(239, 68, 68, 0.5)',  // Semi-transparent red
};

function mapCandlesToVolume(candles: OHLCVTPublic[]): VolumeBar[] {
  return candles.map((c) => ({
    time: c.t as UTCTimestamp,
    value: c.vb + c.vs,
    color: c.vb > c.vs ? VOLUME_COLORS.buy : VOLUME_COLORS.sell,
  }));
}
```

## Load and Display

```typescript
async function loadChart(exchange: string, symbol: string, tf: string) {
  // Fetch through your server-side proxy — never call MMT directly from browser
  const params = new URLSearchParams({ exchange, symbol, tf });
  const resp = await fetch(`/api/mmt/candles?${params}`);
  const { data } = await resp.json();
  const candles = data as OHLCVTPublic[];

  candleSeries.setData(candles.map(c => ({
    time: c.t as UTCTimestamp,
    open: c.o,
    high: c.h,
    low: c.l,
    close: c.c,
  })));

  volumeSeries.setData(mapCandlesToVolume(candles));
  chart.timeScale().fitContent();
}
```

## Real-Time Volume Updates

Update volume in sync with candle updates:

```typescript
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
    color: c.vb > c.vs ? VOLUME_COLORS.buy : VOLUME_COLORS.sell,
  });
};
```

## Split Buy/Sell Stacked Volume (Two Series)

For separate buy and sell volume bars:

```typescript
const buySeries = chart.addSeries(HistogramSeries, {
  priceScaleId: 'volume',
  color: 'rgba(34, 197, 94, 0.6)',
  priceFormat: { type: 'volume' },
  lastValueVisible: false,
  priceLineVisible: false,
});

const sellSeries = chart.addSeries(HistogramSeries, {
  priceScaleId: 'volume',
  color: 'rgba(239, 68, 68, 0.6)',
  priceFormat: { type: 'volume' },
  lastValueVisible: false,
  priceLineVisible: false,
});

chart.priceScale('volume').applyOptions({
  scaleMargins: { top: 0.8, bottom: 0 },
});

// Set data
buySeries.setData(candles.map(c => ({
  time: c.t as UTCTimestamp,
  value: c.vb,
})));

sellSeries.setData(candles.map(c => ({
  time: c.t as UTCTimestamp,
  value: c.vs,
})));
```

Note: Lightweight Charts does not natively stack histograms. Two histogram series on the same scale will overlap, not stack. The single combined series with color-coding is the recommended approach.

## Rules

- Use `priceScaleId: 'volume'` with `scaleMargins: { top: 0.8, bottom: 0 }` to overlay volume at the bottom 20% of the chart.
- Derive volume from candle data (`vb + vs`), not from the `/volumes` REST endpoint. The `/volumes` endpoint returns price-level distribution, not time-series totals.
- Use semi-transparent colors (`rgba` with alpha 0.5) so volume bars do not obscure the price chart.
- Color by buy/sell dominance: green when `vb > vs`, red when `vs > vb`.
- Set `lastValueVisible: false` and `priceLineVisible: false` on the volume series to avoid cluttering the price axis.
- Update volume series in the same handler as candle updates to keep them in sync.
