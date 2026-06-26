# Technical Analysis: Stock Events, Technical Indicators, and Trend Lines

Stock Chart provides comprehensive technical analysis tools including stock event markers, 10+ technical indicators, and 6 types of trend lines for in-depth financial data analysis.

> Reference API: [references/api.md](./api.md)

**Additional features from API:** `stockEvents`, `stockEventRender`, `StockChartIndicatorsDirective`, `StockChartTrendlinesDirective`, `indicatorType`

## Table of Contents
- [Stock Events](#stock-events)
  - [Overview](#stock-events-overview)
  - [Configuration](#stock-event-configuration)
  - [Events for Specific Series](#events-for-individual-series)
  - [Complete Examples](#stock-events-complete-examples)
- [Technical Indicators](#technical-indicators)
  - [Overview](#technical-indicators-overview)
  - [Available Indicators](#available-indicator-types)
  - [Configuration](#indicator-configuration)
  - [Multiple Indicators](#using-multiple-indicators)
- [Trend Lines](#trend-lines)
  - [Overview](#trend-lines-overview)
  - [Trend Line Types](#trend-line-types)
  - [Configuration](#trend-line-configuration)
  - [Complete Examples](#trend-lines-complete-examples)

## Stock Events

### Stock Events Overview

Stock Events visualize significant market events (earnings, dividends, splits, acquisitions) directly on the stock chart. Events are displayed as markers with customizable shapes, colors, and descriptions.

**Key features:**
- Multiple event types (Flag, Circle, Square, Triangle, etc.)
- Customizable colors and text
- Event descriptions on hover
- Support for specific series targeting
- Visual timeline of market events

### Stock Event Configuration

Stock events are configured using the `stockEvents` property:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  SplineSeries,
  Tooltip
} from '@syncfusion/ej2-react-charts';

function StockEventsChart() {
  const stockData = [
    { x: new Date('2012-01-01'), close: 125.50 },
    { x: new Date('2012-02-01'), close: 128.30 },
    { x: new Date('2012-03-01'), close: 132.00 },
    { x: new Date('2012-04-01'), close: 135.75 },
    { x: new Date('2012-05-01'), close: 130.25 },
    // More data...
  ];

  const events: StockEventsSettingsModel[] = [
    {
      date: new Date('2012-02-01'),
      text: 'Q1 Earnings',
      description: 'Quarterly earnings release',
      type: 'Flag',
      background: '#6c757d',
      border: { color: '#6c757d', width: 2 }
    },
    {
      date: new Date('2012-04-01'),
      text: 'Dividend',
      description: 'Dividend payout announcement',
      type: 'Circle',
      background: '#28a745',
      border: { color: '#28a745', width: 2 }
    }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price with Events'
      primaryXAxis={{ valueType: 'DateTime' }}
      stockEvents={events}
    >
      <Inject services={[DateTime, SplineSeries, Tooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Spline'
          xName='x'
          yName='close'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

**Stock Event Properties:**
- `date` - Date when event occurred (Date object)
- `text` - Short label for the event
- `description` - Detailed description (shown on hover)
- `type` - Event marker shape ('Flag', 'Circle', 'Square', 'Triangle', 'InvertedTriangle', 'ArrowUp', 'ArrowDown')
- `background` - Background color
- `border` - Border configuration (color, width)

### Event Marker Types

```typescript
const eventMarkerTypes = [
  { type: 'Flag', description: 'General events, announcements' },
  { type: 'Circle', description: 'Positive events, dividends' },
  { type: 'Square', description: 'Milestones, achievements' },
  { type: 'Triangle', description: 'Warnings, important dates' },
  { type: 'InvertedTriangle', description: 'Negative events, losses' },
  { type: 'ArrowUp', description: 'Price increases, upgrades' },
  { type: 'ArrowDown', description: 'Price decreases, downgrades' }
];
```

### Events for Individual Series

By default, stock events appear for all series. Target specific series using `seriesIndexes`:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  LineSeries,
  Tooltip
} from '@syncfusion/ej2-react-charts';

function MultiSeriesEventsChart() {
  const applData = [ /* AAPL data */ ];
  const googData = [ /* GOOG data */ ];

  const events = [
    {
      date: new Date('2012-02-01'),
      text: 'AAPL Event',
      description: 'Apple product launch',
      type: 'Flag',
      background: '#0080ff',
      seriesIndexes: [0]  // Only for first series (AAPL)
    },
    {
      date: new Date('2012-03-01'),
      text: 'GOOG Event',
      description: 'Google acquisition',
      type: 'Circle',
      background: '#ff8000',
      seriesIndexes: [1]  // Only for second series (GOOG)
    }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Multiple Series with Events'
      primaryXAxis={{ valueType: 'DateTime' }}
      stockEvents={events}
    >
      <Inject services={[DateTime, LineSeries, Tooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={applData}
          type='Line'
          xName='x'
          yName='close'
          name='AAPL'
        />
        <StockChartSeriesDirective
          dataSource={googData}
          type='Line'
          xName='x'
          yName='close'
          name='GOOG'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

### Stock Events Complete Examples

**Financial calendar events:**
```typescript
function FinancialCalendarChart() {
  const stockData = [ /* yearly data */ ];

  const financialEvents = [
    {
      date: new Date('2012-02-15'),
      text: 'Q1',
      description: 'Q1 Earnings: $2.5B revenue, EPS $1.20',
      type: 'Flag',
      background: '#6c757d'
    },
    {
      date: new Date('2012-03-10'),
      text: 'DIV',
      description: 'Dividend: $0.50 per share',
      type: 'Circle',
      background: '#28a745'
    },
    {
      date: new Date('2012-05-15'),
      text: 'Q2',
      description: 'Q2 Earnings: $2.8B revenue, EPS $1.35',
      type: 'Flag',
      background: '#6c757d'
    },
    {
      date: new Date('2012-07-20'),
      text: 'SPLIT',
      description: '2-for-1 stock split',
      type: 'Square',
      background: '#007bff'
    },
    {
      date: new Date('2012-08-15'),
      text: 'Q3',
      description: 'Q3 Earnings: $3.1B revenue, EPS $1.55',
      type: 'Flag',
      background: '#6c757d'
    }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price with Financial Calendar'
      primaryXAxis={{ valueType: 'DateTime' }}
      stockEvents={financialEvents}
      tooltip={{ enable: true }}
    >
      <Inject services={[DateTime, SplineSeries, Tooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Spline'
          xName='x'
          yName='close'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

## Technical Indicators

### Technical Indicators Overview

Technical indicators are mathematical calculations based on historical price, volume, or open interest data that help forecast market direction and identify trading opportunities.

**Supported indicators (10 types):**
1. **Accumulation Distribution** - Money flow indicator
2. **ATR (Average True Range)** - Volatility measure
3. **EMA (Exponential Moving Average)** - Trend direction
4. **SMA (Simple Moving Average)** - Trend direction
5. **TMA (Triangular Moving Average)** - Smoothed trend
6. **Momentum** - Rate of price change
7. **MACD** - Trend and momentum
8. **RSI (Relative Strength Index)** - Overbought/oversold
9. **Stochastic** - Momentum oscillator
10. **Bollinger Bands** - Volatility bands

### Available Indicator Types

#### 1. Accumulation Distribution

Combines price and volume to show money flow:

```typescript
const accumulationDistribution = {
  type: 'AccumulationDistribution',
  field: 'Close',
  seriesName: 'Stock',
  fill: '#6063ff',
  period: 14,
  volume: 'volume'  // Required: volume field
};
```

**Module:** `AccumulationDistributionIndicator`

#### 2. Average True Range (ATR)

Measures volatility:

```typescript
const atr = {
  type: 'Atr',
  field: 'Close',
  seriesName: 'Stock',
  fill: '#ff6347',
  period: 14
};
```

**Module:** `AtrIndicator`

#### 3. Exponential Moving Average (EMA)

Weighted moving average giving more weight to recent data:

```typescript
const ema = {
  type: 'Ema',
  field: 'Close',
  seriesName: 'Stock',
  fill: '#ff0000',
  period: 14
};
```

**Module:** `EmaIndicator`

#### 4. Simple Moving Average (SMA)

Average price over a specified period:

```typescript
const sma = {
  type: 'Sma',
  field: 'Close',
  seriesName: 'Stock',
  fill: '#0000ff',
  period: 14
};
```

**Module:** `SmaIndicator`

#### 5. Triangular Moving Average (TMA)

Doubly smoothed moving average:

```typescript
const tma = {
  type: 'Tma',
  field: 'Close',
  seriesName: 'Stock',
  fill: '#00ff00',
  period: 14
};
```

**Module:** `TmaIndicator`

#### 6. Momentum

Shows rate of price change:

```typescript
const momentum = {
  type: 'Momentum',
  field: 'Close',
  seriesName: 'Stock',
  fill: '#ff00ff',
  period: 14,
  upperLine: { color: '#ff0000' },
  lowerLine: { color: '#00ff00' }
};
```

**Module:** `MomentumIndicator`

#### 7. MACD (Moving Average Convergence Divergence)

Trend and momentum indicator:

```typescript
const macd = {
  type: 'Macd',
  field: 'Close',
  seriesName: 'Stock',
  fill: '#ff6347',
  fastPeriod: 12,
  slowPeriod: 26,
  period: 9,
  macdLine: { color: '#ff0000', width: 2 },
  macdPositiveColor: '#00ff00',
  macdNegativeColor: '#ff0000'
};
```

**Module:** `MacdIndicator`

#### 8. RSI (Relative Strength Index)

Measures momentum and overbought/oversold conditions:

```typescript
const rsi = {
  type: 'Rsi',
  field: 'Close',
  seriesName: 'Stock',
  fill: '#6063ff',
  period: 14,
  overBought: 70,  // Overbought threshold
  overSold: 30,    // Oversold threshold
  upperLine: { color: '#ff0000' },
  lowerLine: { color: '#00ff00' }
};
```

**Module:** `RsiIndicator`

#### 9. Stochastic

Compares closing price to price range:

```typescript
const stochastic = {
  type: 'Stochastic',
  field: 'Close',
  seriesName: 'Stock',
  fill: '#ff00ff',
  kPeriod: 14,
  dPeriod: 3,
  overBought: 80,
  overSold: 20,
  upperLine: { color: '#ff0000' },
  lowerLine: { color: '#00ff00' },
  periodLine: { color: '#0000ff' }
};
```

**Module:** `StochasticIndicator`

#### 10. Bollinger Bands

Shows volatility bands around price:

```typescript
const bollingerBands = {
  type: 'BollingerBands',
  field: 'Close',
  seriesName: 'Stock',
  fill: 'rgba(0, 128, 255, 0.2)',
  period: 14,
  standardDeviation: 2,
  upperLine: { color: '#ff0000', width: 1 },
  lowerLine: { color: '#00ff00', width: 1 }
};
```

**Module:** `BollingerBands`

### Indicator Configuration

Complete example with indicator:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  StockChartIndicatorDirective,
  StockChartIndicatorsDirective,
  Inject,
  DateTime,
  CandleSeries,
  LineSeries,
  EmaIndicator,
  SmaIndicator,
  Tooltip
} from '@syncfusion/ej2-react-charts';

function IndicatorChart() {
  const stockData = [ /* OHLC data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price with Indicators'
      primaryXAxis={{ valueType: 'DateTime' }}
      tooltip={{ enable: true }}
    >
      <Inject services={[DateTime, CandleSeries, LineSeries, EmaIndicator, SmaIndicator, Tooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'
          xName='x'
          high='high'
          low='low'
          open='open'
          close='close'
          name='Stock'
        />
      </StockChartSeriesCollectionDirective>
      <StockChartIndicatorsDirective>
        <StockChartIndicatorDirective
          type='Ema'
          field='Close'
          seriesName='Stock'
          fill='#ff0000'
          period={14}
        />
        <StockChartIndicatorDirective
          type='Sma'
          field='Close'
          seriesName='Stock'
          fill='#0000ff'
          period={50}
        />
      </StockChartIndicatorsDirective>
    </StockChartComponent>
  );
}
```

### Using Multiple Indicators

Combine multiple indicators for comprehensive analysis:

```typescript
import { 
    StockChartComponent,
    StockChartSeriesCollectionDirective,
    StockChartSeriesDirective,
    StockChartIndicatorDirective,
    StockChartIndicatorsDirective,
    Inject,
    DateTime,
    CandleSeries,
    LineSeries,
    EmaIndicator,
    SmaIndicator,
    Tooltip, RsiIndicator,MacdIndicator, BollingerBands
  } from '@syncfusion/ej2-react-charts'
export function MultipleIndicatorsChart() {
  const stockData = [ /* data with volume */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Comprehensive Technical Analysis'
      primaryXAxis={{ valueType: 'DateTime' }}
      tooltip={{ enable: true, shared: true }}
    >
      <Inject services={[
        DateTime, CandleSeries, LineSeries,
        SmaIndicator, EmaIndicator, RsiIndicator, MacdIndicator,
        BollingerBands, Tooltip
      ]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'
          name='Stock'
        />
      </StockChartSeriesCollectionDirective>
      <StockChartIndicatorsDirective>
        {/* Bollinger Bands */}
        <StockChartIndicatorDirective
          type='BollingerBands'
          field='Close'
          seriesName='Stock'
          fill='rgba(0, 128, 255, 0.1)'
          period={20}
          standardDeviation={2}
        />
        {/* SMA 50 */}
        <StockChartIndicatorDirective
          type='Sma'
          field='Close'
          seriesName='Stock'
          fill='#0080ff'
          period={50}
        />
        {/* EMA 20 */}
        <StockChartIndicatorDirective
          type='Ema'
          field='Close'
          seriesName='Stock'
          fill='#ff8000'
          period={20}
        />
        {/* RSI */}
        <StockChartIndicatorDirective
          type='Rsi'
          field='Close'
          seriesName='Stock'
          fill='#6063ff'
          period={14}
          overBought={70}
          overSold={30}
        />
      </StockChartIndicatorsDirective>
    </StockChartComponent>
  );
}
```

## Trend Lines

### Trend Lines Overview

Trend lines show the direction and speed of price movement. They help identify support/resistance levels and potential breakouts.

**Supported trend line types (6 types):**
1. **Linear** - Best fit straight line
2. **Exponential** - Curved line for exponential growth
3. **Logarithmic** - Curved line for logarithmic growth
4. **Polynomial** - Polynomial curve for fluctuating data
5. **Power** - Power curve for specific rate measurements
6. **Moving Average** - Smoothed average trend

### Trend Line Types

#### 1. Linear Trend Line

Best fit straight line for simpler datasets:

```typescript
const linearTrend = {
  type: 'Linear',
  name: 'Linear Trend',
  fill: '#ff0000',
  width: 2
};
```

#### 2. Exponential Trend Line

For data rising/falling at increasing rates:

```typescript
const exponentialTrend = {
  type: 'Exponential',
  name: 'Exponential Trend',
  fill: '#00ff00',
  width: 2
};
```

**Note:** Cannot use with zero or negative values.

#### 3. Logarithmic Trend Line

For data that increases/decreases quickly then levels out:

```typescript
const logarithmicTrend = {
  type: 'Logarithmic',
  name: 'Logarithmic Trend',
  fill: '#0000ff',
  width: 2
};
```

#### 4. Polynomial Trend Line

For fluctuating data:

```typescript
const polynomialTrend = {
  type: 'Polynomial',
  name: 'Polynomial Trend',
  fill: '#ff00ff',
  width: 2,
  polynomialOrder: 3  // Polynomial degree (2-6)
};
```

#### 5. Power Trend Line

For measurements increasing at specific rates:

```typescript
const powerTrend = {
  type: 'Power',
  name: 'Power Trend',
  fill: '#ffff00',
  width: 2
};
```

#### 6. Moving Average Trend Line

Smooths fluctuations to show clearer trends:

```typescript
const movingAverageTrend = {
  type: 'MovingAverage',
  name: 'Moving Average',
  fill: '#00ffff',
  width: 2,
  period: 14  // Period for averaging
};
```

### Trend Line Configuration

Complete example with trend lines:

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  StockChartTrendlineDirective,
  StockChartTrendlinesDirective,
  Inject,
  DateTime,
  LineSeries,
  Trendlines,
  Tooltip
} from '@syncfusion/ej2-react-charts';

function TrendLineChart() {
  const stockData = [ /* price data */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price with Trend Lines'
      primaryXAxis={{ valueType: 'DateTime' }}
      tooltip={{ enable: true }}
    >
      <Inject services={[DateTime, LineSeries, Trendlines, Tooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Line'
          xName='x'
          yName='close'
          name='Stock Price'
        >
          <StockChartTrendlinesDirective>
            <StockChartTrendlineDirective
              type='Linear'
              name='Linear Trend'
              fill='#ff0000'
              width={2}
            />
            <StockChartTrendlineDirective
              type='MovingAverage'
              name='MA(20)'
              fill='#0000ff'
              width={2}
              period={20}
            />
          </StockChartTrendlinesDirective>
        </StockChartSeriesDirective>
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

### Trend Lines Complete Examples

**Multiple trend lines for analysis:**
```typescript
function ComprehensiveTrendAnalysis() {
  const stockData = [ /* extensive dataset */ ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Comprehensive Trend Analysis'
      primaryXAxis={{ valueType: 'DateTime' }}
    >
      <Inject services={[DateTime, LineSeries, Trendlines, Tooltip]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Line'
          xName='x'
          yName='close'
          name='Price'
          fill='#666666'
          width={1}
        >
          <StockChartTrendlinesDirective>
            {/* Linear trend */}
            <StockChartTrendlineDirective
              type='Linear'
              name='Linear'
              fill='#ff0000'
              width={2}
            />
            {/* Short-term MA */}
            <StockChartTrendlineDirective
              type='MovingAverage'
              name='MA(10)'
              fill='#0080ff'
              width={2}
              period={10}
            />
            {/* Long-term MA */}
            <StockChartTrendlineDirective
              type='MovingAverage'
              name='MA(50)'
              fill='#ff8000'
              width={2}
              period={50}
            />
            {/* Polynomial for pattern */}
            <StockChartTrendlineDirective
              type='Polynomial'
              name='Polynomial'
              fill='#00ff00'
              width={2}
              polynomialOrder={3}
              dashArray='3,3'
            />
          </StockChartTrendlinesDirective>
        </StockChartSeriesDirective>
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

## Combining All Analysis Tools

Complete example with events, indicators, and trend lines:

```typescript
import {
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  StockChartIndicatorsDirective,
  StockChartIndicatorDirective,
  StockChartTrendlinesDirective,
  StockChartTrendlineDirective,
  Inject,
  DateTime,
  CandleSeries,
  LineSeries,
  SplineSeries,
  SmaIndicator,
  EmaIndicator,
  RsiIndicator,
  MacdIndicator,
  BollingerBands,
  Trendlines,
  Tooltip,
  Crosshair
} from '@syncfusion/ej2-react-charts';

function CompleteTechnicalAnalysis() {

  const stockData = [
    { x: new Date('2012-04-02'), open: 320.71, high: 324.07, low: 317.74, close: 323.78 },
    { x: new Date('2012-04-03'), open: 323.03, high: 324.30, low: 319.64, close: 321.63 }
  ];

  const marketEvents = [
    { date: new Date('2012-02-15'), text: 'Q1', description: 'Q1 Earnings', type: 'Flag', background: '#6c757d' },
    { date: new Date('2012-05-15'), text: 'Q2', description: 'Q2 Earnings', type: 'Flag', background: '#6c757d' },
    { date: new Date('2012-03-10'), text: 'DIV', description: 'Dividend', type: 'Circle', background: '#28a745' }
  ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Complete Technical Analysis Dashboard'
      primaryXAxis={{ valueType: 'DateTime' }}
      tooltip={{ enable: true, shared: true }}
      crosshair={{ enable: true }}
      stockEvents={marketEvents}
    >
      <Inject services={[
        DateTime,
        CandleSeries,
        LineSeries,
        SplineSeries,
        SmaIndicator,
        EmaIndicator,
        RsiIndicator,
        MacdIndicator,
        BollingerBands,
        Trendlines,
        Tooltip,
        Crosshair
      ]} />

      {/* MAIN SERIES */}
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'
          name='Price'   
          xName='x'
          open='open'
          high='high'
          low='low'
          close='close'
        >
          <StockChartTrendlinesDirective>
            <StockChartTrendlineDirective
              type='Linear'
              fill='#ff0000'
              width={2}
            />
          </StockChartTrendlinesDirective>
        </StockChartSeriesDirective>
      </StockChartSeriesCollectionDirective>

      {/* INDICATORS */}
      <StockChartIndicatorsDirective>
        <StockChartIndicatorDirective
          type='Sma'
          field='close'  
          seriesName='Price'
          fill='#0080ff'
          period={20}
        />
        <StockChartIndicatorDirective
          type='BollingerBands'
          field='close'
          seriesName='Price'
          fill='rgba(0,128,255,0.1)'
          period={20}
        />
        <StockChartIndicatorDirective
          type='Rsi'
          field='close'
          seriesName='Price'
          period={14}
        />
      </StockChartIndicatorsDirective>

    </StockChartComponent>
  );
}

```

## Best Practices

**Stock Events:**
- Use consistent color coding (green for positive, red for negative)
- Limit events to significant milestones
- Provide descriptive text and details
- Use appropriate marker types for event categories

**Technical Indicators:**
- Don't overload with too many indicators (3-5 maximum)
- Choose complementary indicators (trend + momentum + volatility)
- Adjust periods based on trading timeframe
- Use consistent color schemes

**Trend Lines:**
- Combine short and long-term moving averages
- Use linear trends for overall direction
- Apply polynomial for complex patterns
- Limit to 2-3 trend lines for clarity

**Performance:**
- Indicators add minimal overhead
- Trend lines calculate client-side
- Events are lightweight visual markers
- Consider data aggregation for very large datasets
