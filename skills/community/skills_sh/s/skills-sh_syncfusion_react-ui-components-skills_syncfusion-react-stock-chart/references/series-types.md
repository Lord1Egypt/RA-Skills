# Series Types

Stock Chart supports 6 major series types for visualizing financial data. Each series type is designed for specific visualization needs and data patterns.

> Reference API: [references/api.md](./api.md)

## Table of Contents
- [Overview](#overview)
- [Line Series](#line-series)
- [Spline Series](#spline-series)
- [Hilo Series](#hilo-series)
- [HiloOpenClose Series](#hiloopenclose-series)
- [Hollow Candle Series](#hollow-candle-series)
- [Candle Series](#candle-series)
- [Series Dropdown Navigation](#series-dropdown-navigation)
- [Choosing the Right Series Type](#choosing-the-right-series-type)

## Overview

The Stock Chart provides a series dropdown button that allows users to switch between different visualization types. All six series types can be made available for users to navigate between them dynamically.

**Available series types:**
1. **Line** - Continuous line connecting close prices
2. **Spline** - Smooth curved line for close prices
3. **Hilo** - Vertical bars showing high-low range
4. **HiloOpenClose** - OHLC bars with open/close ticks
5. **Hollow Candle** - Traditional hollow/filled candles
6. **Candle** - Solid candles showing OHLC data

## Line Series

Line series displays a continuous line connecting data points, typically used for close prices.

### When to Use Line Series

- Showing price trends over time
- Emphasizing overall direction rather than intraday volatility
- Comparing multiple stocks with clean visualization
- Reducing visual complexity for long time periods

### Implementation

Set the series `type` to `'Line'` and inject `LineSeries` module:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  LineSeries,
  Tooltip,
  RangeTooltip,
  Crosshair
} from '@syncfusion/ej2-react-charts';

function LineSeriesChart() {
  const data = [
    { x: new Date('2012-04-02'), close: 323.78 },
    { x: new Date('2012-04-03'), close: 321.63 },
    { x: new Date('2012-04-04'), close: 317.89 },
    { x: new Date('2012-04-05'), close: 316.48 }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
    >
      <Inject services={[DateTime, LineSeries, Tooltip, RangeTooltip, Crosshair]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={data}
          type='Line'
          xName='x'
          yName='close'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

**Note:** Line series only requires `xName` and `yName` (typically 'close' for stock data).

## Spline Series

Spline series displays a smooth curved line through data points, providing an aesthetically pleasing visualization.

### When to Use Spline Series

- Creating smooth, professional-looking trend lines
- Reducing visual noise from sharp price movements
- Presentations and reports where smooth curves are preferred
- Highlighting overall trends with elegant curves

### Implementation

Set the series `type` to `'Spline'` and inject `SplineSeries` module:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  SplineSeries,
  Tooltip,
  RangeTooltip,
  Crosshair
} from '@syncfusion/ej2-react-charts';

function SplineSeriesChart() {
  const data = [
    { x: new Date('2012-04-02'), close: 323.78 },
    { x: new Date('2012-04-03'), close: 321.63 },
    { x: new Date('2012-04-04'), close: 317.89 },
    { x: new Date('2012-04-05'), close: 316.48 }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
    >
      <Inject services={[DateTime, SplineSeries, Tooltip, RangeTooltip, Crosshair]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={data}
          type='Spline'
          xName='x'
          yName='close'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

## Hilo Series

Hilo series displays vertical bars showing the high-low range for each time period.

### When to Use Hilo Series

- Emphasizing price volatility and range
- Showing intraday high-low spreads
- Analyzing price ranges without open/close details
- Simplifying OHLC data to just range information

### Implementation

Set the series `type` to `'Hilo'` and inject `HiloSeries` module:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  HiloSeries,
  Tooltip,
  RangeTooltip,
  Crosshair
} from '@syncfusion/ej2-react-charts';

function HiloSeriesChart() {
  const data = [
    { x: new Date('2012-04-02'), high: 324.07, low: 317.74 },
    { x: new Date('2012-04-03'), high: 324.30, low: 319.64 },
    { x: new Date('2012-04-04'), high: 319.82, low: 315.87 },
    { x: new Date('2012-04-05'), high: 318.53, low: 314.60 }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
    >
      <Inject services={[DateTime, HiloSeries, Tooltip, RangeTooltip, Crosshair]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={data}
          type='Hilo'
          xName='x'
          high='high'
          low='low'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

**Required fields:** `xName`, `high`, `low`

## HiloOpenClose Series

HiloOpenClose series displays OHLC (Open-High-Low-Close) bars with horizontal ticks for open and close values.

### When to Use HiloOpenClose Series

- Traditional OHLC bar charts
- Showing all four price points clearly
- Technical analysis requiring precise open/close levels
- Preference for OHLC bars over candlesticks

### Implementation

Set the series `type` to `'HiloOpenClose'` and inject `HiloOpenCloseSeries` module:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  HiloOpenCloseSeries,
  Tooltip,
  RangeTooltip,
  Crosshair
} from '@syncfusion/ej2-react-charts';

function HiloOpenCloseChart() {
  const data = [
    { x: new Date('2012-04-02'), open: 320.71, high: 324.07, low: 317.74, close: 323.78 },
    { x: new Date('2012-04-03'), open: 323.03, high: 324.30, low: 319.64, close: 321.63 },
    { x: new Date('2012-04-04'), open: 319.54, high: 319.82, low: 315.87, close: 317.89 },
    { x: new Date('2012-04-05'), open: 316.44, high: 318.53, low: 314.60, close: 316.48 }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
    >
      <Inject services={[DateTime, HiloOpenCloseSeries, Tooltip, RangeTooltip, Crosshair]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={data}
          type='HiloOpenClose'
          xName='x'
          high='high'
          low='low'
          open='open'
          close='close'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

**Required fields:** `xName`, `high`, `low`, `open`, `close`

## Hollow Candle Series

Hollow Candle series displays traditional candlesticks where hollow (empty) candles indicate price increase and filled candles indicate price decrease.

### When to Use Hollow Candle Series

- Traditional candlestick charting with hollow/filled distinction
- Quickly identifying bullish (hollow) vs bearish (filled) periods
- Technical analysis with classic candlestick patterns
- Preference for hollow candles over solid candles

### Implementation

Set the series `type` to `'Candle'` and set `enableSolidCandle` to `false`:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries,
  Tooltip,
  RangeTooltip,
  Crosshair
} from '@syncfusion/ej2-react-charts';

function HollowCandleChart() {
  const data = [
    { x: new Date('2012-04-02'), open: 320.71, high: 324.07, low: 317.74, close: 323.78 },
    { x: new Date('2012-04-03'), open: 323.03, high: 324.30, low: 319.64, close: 321.63 },
    { x: new Date('2012-04-04'), open: 319.54, high: 319.82, low: 315.87, close: 317.89 },
    { x: new Date('2012-04-05'), open: 316.44, high: 318.53, low: 314.60, close: 316.48 }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      primaryXAxis={{ valueType: 'DateTime' }}
    >
      <Inject services={[DateTime, CandleSeries, Tooltip, RangeTooltip, Crosshair]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={data}
          type='Candle'
          enableSolidCandle={false}  // Makes candles hollow
          xName='x'
          high='high'
          low='low'
          open='open'
          close='close'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

**Key difference:** `enableSolidCandle={false}` creates hollow candles instead of solid.

## Candle Series

Candle series displays solid candlesticks showing OHLC data. This is the most common and default series type for stock charts.

### When to Use Candle Series

- Standard stock price visualization (most common choice)
- Showing all OHLC data with clear visual distinction
- Technical analysis and candlestick pattern recognition
- Default choice for most stock trading applications

### Implementation

Set the series `type` to `'Candle'` and inject `CandleSeries` module:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries,
  Tooltip,
  RangeTooltip,
  Crosshair
} from '@syncfusion/ej2-react-charts';

function CandleSeriesChart() {
  const data = [
    { x: new Date('2012-04-02'), open: 320.71, high: 324.07, low: 317.74, close: 323.78, volume: 45638000 },
    { x: new Date('2012-04-03'), open: 323.03, high: 324.30, low: 319.64, close: 321.63, volume: 40857000 },
    { x: new Date('2012-04-04'), open: 319.54, high: 319.82, low: 315.87, close: 317.89, volume: 32519000 },
    { x: new Date('2012-04-05'), open: 316.44, high: 318.53, low: 314.60, close: 316.48, volume: 46327000 }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price - Candle Chart'
      primaryXAxis={{ valueType: 'DateTime' }}
    >
      <Inject services={[DateTime, CandleSeries, Tooltip, RangeTooltip, Crosshair]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={data}
          type='Candle'
          xName='x'
          high='high'
          low='low'
          open='open'
          close='close'
          volume='volume'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

**Required fields:** `xName`, `high`, `low`, `open`, `close`  
**Optional field:** `volume` for volume-based features

## Series Dropdown Navigation

Stock Chart includes a built-in series dropdown that allows users to switch between different series types dynamically.

### Complete Example with All Series Types

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  LineSeries,
  SplineSeries,
  HiloSeries,
  HiloOpenCloseSeries,
  CandleSeries,
  Tooltip,
  RangeTooltip,
  Crosshair
} from '@syncfusion/ej2-react-charts';

function AllSeriesTypesChart() {
  const stockData = [
    { x: new Date('2012-04-02'), open: 85.97, high: 90.58, low: 85.97, close: 90.58, volume: 660187068 },
    { x: new Date('2012-04-09'), open: 89.02, high: 92.50, low: 88.50, close: 92.90, volume: 490033264 },
    { x: new Date('2012-04-16'), open: 92.52, high: 93.00, low: 88.50, close: 92.52, volume: 450167016 },
    { x: new Date('2012-04-23'), open: 92.26, high: 94.00, low: 90.50, close: 93.58, volume: 510440639 }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      title='AAPL Stock Price - Multiple Series Types'
      primaryXAxis={{ valueType: 'DateTime' }}
      tooltip={{ enable: true }}
      crosshair={{ enable: true }}
    >
      <Inject services={[
        DateTime, 
        LineSeries, 
        SplineSeries, 
        HiloSeries, 
        HiloOpenCloseSeries, 
        CandleSeries, 
        Tooltip, 
        RangeTooltip, 
        Crosshair
      ]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'  // Default type
          xName='x'
          high='high'
          low='low'
          open='open'
          close='close'
          volume='volume'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

When all series modules are injected, users can switch between them using the series dropdown button in the chart toolbar.

## Choosing the Right Series Type

| Series Type | Best For | Data Requirements |
|-------------|----------|-------------------|
| **Line** | Simple trends, comparisons | x, close |
| **Spline** | Smooth trends, presentations | x, close |
| **Hilo** | Price ranges, volatility | x, high, low |
| **HiloOpenClose** | OHLC bars, technical analysis | x, open, high, low, close |
| **Hollow Candle** | Traditional candlesticks | x, open, high, low, close |
| **Candle** | Most common, standard visualization | x, open, high, low, close |

**General recommendations:**
- **For beginners:** Start with Line or Candle series
- **For traders:** Use Candle or HiloOpenClose
- **For presentations:** Use Spline for smooth appearance
- **For volatility analysis:** Use Hilo or Candle
- **For comparisons:** Use Line series for multiple stocks

## Series Customization

You can customize series appearance:

```typescript
<StockChartSeriesDirective
  dataSource={data}
  type='Candle'
  xName='x'
  high='high'
  low='low'
  open='open'
  close='close'
  bearFillColor='#ff0000'  // Color for bearish candles
  bullFillColor='#00ff00'  // Color for bullish candles
  name='Stock Price'       // Name for legend
/>
```

All series types support color, opacity, and styling customization to match your application's design.
