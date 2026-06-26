# Data Mapping: MMT to TradingView

Transform MMT API data types into TradingView Lightweight Charts format. MMT timestamps are already Unix seconds, which TV accepts directly as `UTCTimestamp`.

## MMT Types Reference

```typescript
interface OHLCVTPublic {
  t: number; o: number; h: number; l: number; c: number;
  vb: number; vs: number; tb: number; ts: number;
}

interface OHLCPublic {
  t: number; o: number; h: number; l: number; c: number; n: number;
}

interface TradePublic {
  id: string; t: number; p: number; q: number; b: boolean;
}

interface StatPublic {
  t: number; mp: number; lp: number; fr: number;
  lb: number; ls: number; tlb: number; tls: number;
  vb: number; vs: number; tb: number; ts: number;
  sk: number[]; as: number[]; bs: number[];
  mxt: number; mnt: number; avt: number; it: number;
}
```

## Candle Mapping (OHLCVTPublic -> CandlestickData)

```typescript
import type { CandlestickData, UTCTimestamp } from 'lightweight-charts';

function mapCandle(c: OHLCVTPublic): CandlestickData<UTCTimestamp> {
  return {
    time: c.t as UTCTimestamp,
    open: c.o,
    high: c.h,
    low: c.l,
    close: c.c,
  };
}

function mapCandles(candles: OHLCVTPublic[]): CandlestickData<UTCTimestamp>[] {
  return candles.map(mapCandle);
}
```

## Volume Mapping (OHLCVTPublic -> HistogramData)

Derive volume histogram data from candle buy/sell volumes:

```typescript
import type { HistogramData, UTCTimestamp } from 'lightweight-charts';

function mapCandleToVolume(c: OHLCVTPublic): HistogramData<UTCTimestamp> {
  const totalVolume = c.vb + c.vs;
  const isBuyDominant = c.vb > c.vs;
  return {
    time: c.t as UTCTimestamp,
    value: totalVolume,
    color: isBuyDominant
      ? 'rgba(34, 197, 94, 0.5)'   // green
      : 'rgba(239, 68, 68, 0.5)',   // red
  };
}
```

## OI / VD Candle Mapping (OHLCPublic -> LineData or CandlestickData)

```typescript
import type { LineData, UTCTimestamp } from 'lightweight-charts';

// As line series (using close value)
function mapOIToLine(oi: OHLCPublic): LineData<UTCTimestamp> {
  return {
    time: oi.t as UTCTimestamp,
    value: oi.c,
  };
}

// As candlestick series (full OHLC)
function mapOIToCandle(oi: OHLCPublic): CandlestickData<UTCTimestamp> {
  return {
    time: oi.t as UTCTimestamp,
    open: oi.o,
    high: oi.h,
    low: oi.l,
    close: oi.c,
  };
}
```

## Stats Mapping (StatPublic -> LineData)

Extract individual fields from stats as separate line series:

```typescript
function mapFundingRate(stat: StatPublic): LineData<UTCTimestamp> {
  return {
    time: stat.t as UTCTimestamp,
    value: stat.fr,
  };
}

function mapMarkPrice(stat: StatPublic): LineData<UTCTimestamp> {
  return {
    time: stat.t as UTCTimestamp,
    value: stat.mp,
  };
}
```

## Trade Mapping (TradePublic -> LineData)

```typescript
function mapTradeToLine(trade: TradePublic): LineData<UTCTimestamp> {
  return {
    time: Math.floor(trade.t / 1000) as UTCTimestamp,
    value: trade.p,
  };
}
```

## Generic Mapper

```typescript
type MapFn<TInput, TOutput> = (input: TInput) => TOutput;

function mapMMTData<TInput, TOutput>(
  data: TInput[],
  mapper: MapFn<TInput, TOutput>
): TOutput[] {
  return data.map(mapper);
}

// Usage
const tvCandles = mapMMTData(mmtCandles, mapCandle);
const tvVolumes = mapMMTData(mmtCandles, mapCandleToVolume);
```

## Rules

- MMT `t` field is Unix seconds (UTC) for candles, stats, OI, and VD — cast directly to `UTCTimestamp`. For trades and orderbook, `t` is Unix milliseconds — divide by 1000 first.
- TradingView Lightweight Charts expects seconds. Never multiply candle/stats `t` by 1000. For trades, divide `t` by 1000 since trade timestamps are in milliseconds.
- Data arrays passed to `setData()` must be sorted by `time` in ascending order.
- Deduplicate data points with the same `time` before passing to `setData()` — TV throws on duplicates.
- Volume is derived from candle data (`vb + vs`), not from the separate `/volumes` endpoint (which is price-level distribution data, not time-series totals).
- For OI and VD, use the `c` (close) field when displaying as a line series, or full OHLC for candlestick.
- Keep mapper functions pure and stateless for easy testing and reuse.
