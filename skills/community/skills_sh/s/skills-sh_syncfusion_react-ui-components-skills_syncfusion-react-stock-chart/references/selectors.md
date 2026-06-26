# Period Selector and Range Selector

Stock Chart provides two powerful navigation tools: the Period Selector for quick date range buttons and the Range Selector for precise range selection with thumb controls.

> Reference API: [references/api.md](./api.md)

## Table of Contents
- [Period Selector](#period-selector)
  - [Overview](#period-selector-overview)
  - [Periods Configuration](#periods-configuration)
  - [Interval Types](#interval-types)
  - [Enabling and Disabling](#enabling-and-disabling-period-selector)
  - [Complete Examples](#period-selector-complete-examples)
- [Range Selector](#range-selector)
  - [Overview](#range-selector-overview)
  - [Selection Methods](#selection-methods)
  - [Enabling and Disabling](#enabling-and-disabling-range-selector)
  - [Complete Examples](#range-selector-complete-examples)
- [Combining Both Selectors](#combining-both-selectors)

## Period Selector

### Period Selector Overview

The Period Selector provides quick navigation buttons (like 1D, 5D, 1M, 6M, YTD, 1Y, ALL) that allow users to instantly filter the stock chart to specific time ranges. By default, the period selector is **enabled** in Stock Chart.

**Key features:**
- Pre-configured time range buttons
- Customizable button text and intervals
- Multiple interval types (Days, Months, Years, etc.)
- Default enabled state
- Toggle visibility with `enablePeriodSelector`

### Periods Configuration

The `periods` property accepts an array of period objects, each defining a button in the selector.

**Period object structure:**
```typescript
{
  interval: number,        // Count value for the period
  intervalType: string,    // Type of interval (Days, Months, Years, etc.)
  text: string            // Button label text
}
```

### Basic Period Selector Example

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
import { type PeriodsModel } from '@syncfusion/ej2-react-charts';

function PeriodSelectorChart() {
  const stockData = [
    // Your stock data...
  ];

  const periods:  PeriodsModel[] = [
    { intervalType: 'Days', interval: 1, text: '1D' },
    { intervalType: 'Days', interval: 5, text: '5D' },
    { intervalType: 'Months', interval: 1, text: '1M' },
    { intervalType: 'Months', interval: 3, text: '3M' },
    { intervalType: 'Months', interval: 6, text: '6M' },
    { intervalType: 'Years', interval: 1, text: '1Y' },
    { text: 'All' }  // 'All' shows entire dataset
  ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price with Period Selector'
      primaryXAxis={{ valueType: 'DateTime' }}
      periods={periods}
    >
      <Inject services={[DateTime, CandleSeries, Tooltip, RangeTooltip, Crosshair]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'
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
export function PeriodSelectorChart;
```

### Interval Types

The `intervalType` property supports the following values:

1. **Auto** - Automatically determines best interval
2. **Years** - Year-based intervals (1Y, 2Y, 5Y)
3. **Quarter** - Quarter-based intervals (1Q, 2Q, 4Q)
4. **Months** - Month-based intervals (1M, 3M, 6M)
5. **Weeks** - Week-based intervals (1W, 2W, 4W)
6. **Days** - Day-based intervals (1D, 5D, 10D)
7. **Hours** - Hour-based intervals (1H, 6H, 12H)
8. **Minutes** - Minute-based intervals (15Min, 30Min, 60Min)
9. **Seconds** - Second-based intervals (30S, 60S)

### Custom Period Configurations

**Trading periods (intraday focus):**
```typescript
const intradayPeriods: PeriodsModel[] = [
  { intervalType: 'Minutes', interval: 15, text: '15Min' },
  { intervalType: 'Minutes', interval: 30, text: '30Min' },
  { intervalType: 'Hours', interval: 1, text: '1H' },
  { intervalType: 'Hours', interval: 4, text: '4H' },
  { intervalType: 'Days', interval: 1, text: '1D' }
];
```

**Long-term investment periods:**
```typescript
const longTermPeriods: PeriodsModel[] = [
  { intervalType: 'Months', interval: 1, text: '1M' },
  { intervalType: 'Months', interval: 6, text: '6M' },
  { intervalType: 'Years', interval: 1, text: '1Y' },
  { intervalType: 'Years', interval: 3, text: '3Y' },
  { intervalType: 'Years', interval: 5, text: '5Y' },
  { text: 'All' }
];
```

**Standard stock analysis periods:**
```typescript
const standardPeriods: PeriodsModel[] = [
  { intervalType: 'Days', interval: 1, text: '1D' },
  { intervalType: 'Days', interval: 5, text: '5D' },
  { intervalType: 'Months', interval: 1, text: '1M' },
  { intervalType: 'Months', interval: 3, text: '3M' },
  { intervalType: 'Months', interval: 6, text: '6M' },
  { text: 'YTD' },  // Year to date
  { intervalType: 'Years', interval: 1, text: '1Y' },
  { text: 'All' }
];
```

### Enabling and Disabling Period Selector

The period selector is **enabled by default**. Control visibility with `enablePeriodSelector`:

**Disable period selector:**
```typescript
<StockChartComponent
  id='stockchart'
  enablePeriodSelector={false}  // Hides period selector
  primaryXAxis={{ valueType: 'DateTime' }}
>
  {/* ... */}
</StockChartComponent>
```

**Explicitly enable (default behavior):**
```typescript
<StockChartComponent
  id='stockchart'
  enablePeriodSelector={true}  // Shows period selector
  periods={customPeriods}
  primaryXAxis={{ valueType: 'DateTime' }}
>
  {/* ... */}
</StockChartComponent>
```

### Period Selector Complete Examples

**Complete intraday trading chart:**
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
import { type PeriodsModel } from '@syncfusion/ej2-react-charts';
function IntradayChart() {
  const intradayData = [
    // Minute-level stock data...
  ];

  const periods: PeriodsModel[] = [
    { intervalType: 'Minutes', interval: 15, text: '15Min' },
    { intervalType: 'Minutes', interval: 30, text: '30Min' },
    { intervalType: 'Hours', interval: 1, text: '1H' },
    { intervalType: 'Hours', interval: 2, text: '2H' },
    { intervalType: 'Hours', interval: 4, text: '4H' },
    { intervalType: 'Days', interval: 1, text: '1D' }
  ];

  return (
    <StockChartComponent
            id='intradayChart'
            title='Intraday Stock Analysis'
            primaryXAxis={{ valueType: 'DateTime' }}
            periods={periods}
            enablePeriodSelector={true}
            tooltip={{ enable: true, shared: true }}
            crosshair={{ enable: true }}
          >
      <Inject services={[DateTime, LineSeries, Tooltip, Crosshair]} />
          
      <StockChartSeriesCollectionDirective>
              <StockChartSeriesDirective
                dataSource={stockData}
                type='Line'

              />
       </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

## Range Selector

### Range Selector Overview

The Range Selector (also called Range Navigator) displays a miniature view of the entire dataset with draggable thumbs on the left and right sides. Users can select precise date ranges by dragging the thumbs or clicking on labels.

**Key features:**
- Left and right draggable thumbs
- Visual preview of entire dataset
- Multiple selection methods
- Default enabled state
- Toggle visibility with `enableSelector`

### Selection Methods

Users can select ranges in three ways:

1. **Dragging thumbs** - Click and drag left/right thumb handles
2. **Tapping labels** - Click on axis labels to move thumbs
3. **Date range button** - Use date picker button for precise range selection

### Range Selector Implementation

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

function RangeSelectorChart() {
  const stockData = [
    { x: new Date('2012-01-02'), open: 85.97, high: 90.58, low: 85.97, close: 90.58 },
    { x: new Date('2012-02-02'), open: 89.02, high: 92.50, low: 88.50, close: 92.90 },
    // ... extensive dataset for full year or more
  ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Stock Price with Range Selector'
      primaryXAxis={{ valueType: 'DateTime' }}
      enableSelector={true}  // Enables range selector (default)
    >
      <Inject services={[DateTime, CandleSeries, Tooltip, RangeTooltip, Crosshair]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={stockData}
          type='Candle'
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

### Enabling and Disabling Range Selector

The range selector is **enabled by default**. Control visibility with `enableSelector`:

**Disable range selector:**
```typescript
<StockChartComponent
  id='stockchart'
  enableSelector={false}  // Hides range selector
  primaryXAxis={{ valueType: 'DateTime' }}
>
  {/* ... */}
</StockChartComponent>
```

**Explicitly enable (default behavior):**
```typescript
<StockChartComponent
  id='stockchart'
  enableSelector={true}  // Shows range selector
  primaryXAxis={{ valueType: 'DateTime' }}
>
  {/* ... */}
</StockChartComponent>
```

### Range Selector Complete Examples

**Complete range selector with styling:**
```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  AreaSeries,
  RangeAreaSeries,
  Tooltip,
  RangeTooltip,
  Crosshair
} from '@syncfusion/ej2-react-charts';

function StyledRangeSelectorChart() {
  const yearlyStockData = [
    // Full year or multi-year data...
  ];

  return (
    <StockChartComponent
      id='stockchart'
      title='Historical Stock Analysis'
      primaryXAxis={{ valueType: 'DateTime' }}
      enableSelector={true}
      tooltip={{ enable: true }}
      crosshair={{ enable: true }}
    >
      <Inject services={[DateTime, AreaSeries, RangeAreaSeries, Tooltip, RangeTooltip, Crosshair]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={yearlyStockData}
          type='Area'
          xName='x'
          yName='close'
          fill='rgba(0, 128, 255, 0.3)'
          border={{ width: 2, color: '#0080ff' }}
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
```

## Combining Both Selectors

Both Period Selector and Range Selector can work together, providing users with multiple navigation options.

### Complete Example with Both Selectors

```typescript
import { 
  StockChartComponent,
  StockChartSeriesCollectionDirective,
  StockChartSeriesDirective,
  Inject,
  DateTime,
  CandleSeries,
  LineSeries,
  Tooltip,
  RangeTooltip,
  Crosshair,
  RangeAreaSeries
} from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import { type PeriodsModel } from '@syncfusion/ej2-react-charts';
function ComprehensiveNavigationChart() {
  // Generate extensive stock data (multi-year dataset)
  const generateStockData = () => {
    const data = [];
    let date = new Date('2020-01-01');
    let open = 100;
    
    for (let i = 0; i < 500; i++) {
      const change = (Math.random() - 0.5) * 10;
      const high = open + Math.abs(change) + Math.random() * 5;
      const low = open - Math.abs(change) - Math.random() * 5;
      const close = open + change;
      
      data.push({
        x: new Date(date),
        open: open,
        high: high,
        low: low,
        close: close,
        volume: Math.floor(Math.random() * 100000000)
      });
      
      date.setDate(date.getDate() + 1);
      open = close;
    }
    
    return data;
  };

  const stockData = generateStockData();

  const periods: PeriodsModel[] = [
    { intervalType: 'Days', interval: 1, text: '1D' },
    { intervalType: 'Days', interval: 5, text: '5D' },
    { intervalType: 'Months', interval: 1, text: '1M' },
    { intervalType: 'Months', interval: 3, text: '3M' },
    { intervalType: 'Months', interval: 6, text: '6M' },
    { text: 'YTD' },
    { intervalType: 'Years', interval: 1, text: '1Y' },
    { text: 'All' }
  ];

  return (
    <div style={{ padding: '20px' }}>
      <StockChartComponent
        id='comprehensiveChart'
        title='Stock Price - Complete Navigation'
        primaryXAxis={{ valueType: 'DateTime' }}
        periods={periods}
        enablePeriodSelector={true}
        enableSelector={true}
        tooltip={{ enable: true, shared: true }}
        crosshair={{ enable: true }}
        height='450px'
      >
        <Inject services={[
          DateTime, 
          CandleSeries, 
          LineSeries, 
          RangeAreaSeries,
          Tooltip, 
          RangeTooltip, 
          Crosshair
        ]} />
        <StockChartSeriesCollectionDirective>
          <StockChartSeriesDirective
            dataSource={stockData}
            type='Candle'
            xName='x'
            high='high'
            low='low'
            open='open'
            close='close'
            volume='volume'
            name='Stock Price'
          />
        </StockChartSeriesCollectionDirective>
      </StockChartComponent>
    </div>
  );
}

export default ComprehensiveNavigationChart;
```

### Use Case: Trading Dashboard

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
    Crosshair,
} from '@syncfusion/ej2-react-charts';
import { type PeriodsModel } from '@syncfusion/ej2-react-charts';
function TradingDashboard() {
  const liveStockData = [
    // Real-time or historical data...
  ];

  const tradingPeriods: PeriodsModel[] = [
    { intervalType: 'Minutes', interval: 5, text: '5Min' },
    { intervalType: 'Minutes', interval: 15, text: '15Min' },
    { intervalType: 'Hours', interval: 1, text: '1H' },
    { intervalType: 'Hours', interval: 4, text: '4H' },
    { intervalType: 'Days', interval: 1, text: '1D' },
    { intervalType: 'Days', interval: 5, text: '5D' }
  ];

  return (
    <StockChartComponent
      id='tradingChart'
      title='Live Trading - AAPL'
      primaryXAxis={{ valueType: 'DateTime' }}
      periods={tradingPeriods}
      enablePeriodSelector={true}
      enableSelector={true}
      tooltip={{ 
        enable: true, 
        format: '${point.x}: Open: ${point.open}, High: ${point.high}, Low: ${point.low}, Close: ${point.close}'
      }}
      crosshair={{ enable: true }}
    >
      <Inject services={[DateTime, CandleSeries, Tooltip, RangeTooltip, Crosshair]} />
      <StockChartSeriesCollectionDirective>
        <StockChartSeriesDirective
          dataSource={liveStockData}
          type='Candle'
          xName='x'
          high='high'
          low='low'
          open='open'
          close='close'
          bearFillColor='#ff4444'
          bullFillColor='#44ff44'
        />
      </StockChartSeriesCollectionDirective>
    </StockChartComponent>
  );
}
export default TradingDashboard;
```

## Best Practices

### Period Selector Best Practices

1. **Choose relevant periods** - Match periods to your data granularity and user needs
2. **Limit button count** - 5-8 buttons is optimal, avoid overwhelming users
3. **Use clear labels** - Standard labels like '1D', '1M', '1Y' are intuitive
4. **Include "All" option** - Let users see the entire dataset
5. **Order logically** - Arrange from shortest to longest duration

### Range Selector Best Practices

1. **Provide sufficient data** - Range selector works best with extensive datasets
2. **Use for historical analysis** - Ideal for multi-month or multi-year data
3. **Combine with period selector** - Offer both quick and precise navigation
4. **Consider performance** - Very large datasets may need optimization

### When to Disable Selectors

**Disable Period Selector when:**
- Data spans a short, fixed time range
- Custom navigation UI is provided
- Space is limited
- Single time period is sufficient

**Disable Range Selector when:**
- Dataset is small (< 30 days)
- Fixed range is required
- Screen space is constrained
- Period selector alone is sufficient

## Troubleshooting

**Period buttons not working:**
- Verify `periods` array is properly formatted
- Check that `intervalType` values are valid
- Ensure data spans the requested period range

**Range selector thumbs not responding:**
- Confirm `enableSelector={true}` is set
- Verify dataset is large enough for range selection
- Check that `RangeTooltip` module is injected

**Navigation feels sluggish:**
- Reduce data density for range selector preview
- Consider data aggregation for large datasets
- Optimize re-rendering in React component
