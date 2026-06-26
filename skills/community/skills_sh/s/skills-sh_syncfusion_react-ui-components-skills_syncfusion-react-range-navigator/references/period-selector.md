# Period Selector

The Period Selector allows users to quickly select predefined time ranges using buttons. This feature is particularly useful for financial charts, analytics dashboards, and any time-series data where users need quick access to common time periods.

## Table of Contents
- [Module Injection](#module-injection)
- [Periods Configuration](#periods-configuration)
- [Interval Types](#interval-types)
- [Positioning Period Selector](#positioning-period-selector)
- [Height Customization](#height-customization)
- [Visibility of Range Navigator](#visibility-of-range-navigator)

## Module Injection

To use the Period Selector feature, you must inject the `PeriodSelector` module.

```tsx
import { PeriodSelector } from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';
<Inject services={[PeriodSelector, AreaSeries, DateTime]} />
```

## Periods Configuration

Configure predefined time periods using the `periodSelectorSettings.periods` property. Each period is an object with `interval`, `text`, and `intervalType` properties.

### Basic Period Selector Implementation

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  PeriodSelector, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { date: new Date(2020, 0, 1), value: 100 },
    { date: new Date(2020, 3, 1), value: 110 },
    { date: new Date(2020, 6, 1), value: 105 },
    { date: new Date(2020, 9, 1), value: 115 },
    { date: new Date(2021, 0, 1), value: 120 },
    { date: new Date(2021, 3, 1), value: 130 },
    { date: new Date(2021, 6, 1), value: 125 },
    { date: new Date(2021, 9, 1), value: 135 },
    { date: new Date(2022, 0, 1), value: 140 },
    { date: new Date(2022, 3, 1), value: 145 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM yyyy"
      periodSelectorSettings={{
        periods: [
          { intervalType: 'Months', interval: 1, text: '1M' },
          { intervalType: 'Months', interval: 3, text: '3M' },
          { intervalType: 'Months', interval: 6, text: '6M' },
          { intervalType: 'Years', interval: 1, text: '1Y' },
          { text: 'YTD' },
          { text: 'All' }
        ]
      }}
    >
      <Inject services={[AreaSeries, DateTime, PeriodSelector]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="date"
          yName="value"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Period Object Properties

Each period object can have the following properties:

- **interval**: Number - The count value for the period (e.g., 1, 3, 6)
- **text**: String - The text displayed on the button (e.g., '1M', '3M', 'YTD')
- **intervalType**: String - The type of interval (Auto, Years, Quarter, Months, Weeks, Days, Hours, Minutes, Seconds)

### Common Period Configurations

#### Financial/Stock Chart Periods

```tsx
periodSelectorSettings={{
  periods: [
    { intervalType: 'Months', interval: 1, text: '1M' },
    { intervalType: 'Months', interval: 3, text: '3M' },
    { intervalType: 'Months', interval: 6, text: '6M' },
    { intervalType: 'Years', interval: 1, text: '1Y' },
    { intervalType: 'Years', interval: 3, text: '3Y' },
    { intervalType: 'Years', interval: 5, text: '5Y' },
    { text: 'YTD' },
    { text: 'All' }
  ]
}}
```

#### Sales/Analytics Dashboard

```tsx
periodSelectorSettings={{
  periods: [
    { intervalType: 'Days', interval: 7, text: '1W' },
    { intervalType: 'Months', interval: 1, text: '1M' },
    { intervalType: 'Months', interval: 3, text: 'Q1' },
    { intervalType: 'Months', interval: 6, text: '6M' },
    { intervalType: 'Years', interval: 1, text: '1Y' },
    { text: 'All' }
  ]
}}
```

#### Hourly/Daily Data

```tsx
periodSelectorSettings={{
  periods: [
    { intervalType: 'Hours', interval: 1, text: '1H' },
    { intervalType: 'Hours', interval: 6, text: '6H' },
    { intervalType: 'Hours', interval: 12, text: '12H' },
    { intervalType: 'Days', interval: 1, text: '1D' },
    { intervalType: 'Days', interval: 7, text: '1W' },
    { text: 'All' }
  ]
}}
```

## Interval Types

The `intervalType` property specifies the time unit for the period button. The following interval types are supported:

### Available Interval Types

- **Auto**: Automatically determined based on data
- **Years**: Yearly intervals
- **Quarter**: Quarterly intervals (3 months)
- **Months**: Monthly intervals
- **Weeks**: Weekly intervals
- **Days**: Daily intervals
- **Hours**: Hourly intervals
- **Minutes**: Minute intervals
- **Seconds**: Second intervals

### Interval Type Examples

```tsx
// 1 Year
{ intervalType: 'Years', interval: 1, text: '1Y' }

// 3 Months
{ intervalType: 'Months', interval: 3, text: '3M' }

// 2 Weeks
{ intervalType: 'Weeks', interval: 2, text: '2W' }

// 7 Days
{ intervalType: 'Days', interval: 7, text: '7D' }

// 24 Hours
{ intervalType: 'Hours', interval: 24, text: '24H' }

// 30 Minutes
{ intervalType: 'Minutes', interval: 30, text: '30Min' }
```

### Special Period Buttons

You can create special period buttons without interval/intervalType:

```tsx
// Year to Date (from January 1st of current year to now)
{ text: 'YTD' }

// All available data
{ text: 'All' }

// Custom button with specific logic
{ text: 'Q4' }
```

## Positioning Period Selector

The `position` property controls where the Period Selector appears relative to the Range Navigator.

### Available Positions

- **Top**: Period Selector above the Range Navigator (default)
- **Bottom**: Period Selector below the Range Navigator

### Position at Top

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  PeriodSelector, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 3, 1), value: 110 },
    { date: new Date(2023, 6, 1), value: 105 },
    { date: new Date(2023, 9, 1), value: 115 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      periodSelectorSettings={{
        periods: [
          { intervalType: 'Months', interval: 3, text: '3M' },
          { intervalType: 'Months', interval: 6, text: '6M' },
          { intervalType: 'Years', interval: 1, text: '1Y' },
          { text: 'All' }
        ],
        position: 'Top'
      }}
    >
      <Inject services={[AreaSeries, DateTime, PeriodSelector]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="date"
          yName="value"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Position at Bottom

```tsx
<RangeNavigatorComponent
  id="rangeNavigator"
  valueType="DateTime"
  periodSelectorSettings={{
    periods: [
      { intervalType: 'Months', interval: 1, text: '1M' },
      { intervalType: 'Months', interval: 3, text: '3M' },
      { intervalType: 'Years', interval: 1, text: '1Y' }
    ],
    position: 'Bottom'
  }}
>
  {/* Series configuration */}
</RangeNavigatorComponent>
```

## Height Customization

Customize the height of the Period Selector using the `height` property. The default height is **43 pixels**.

### Custom Height Examples

```tsx
// Compact height
periodSelectorSettings={{
  periods: [
    { intervalType: 'Months', interval: 1, text: '1M' },
    { intervalType: 'Months', interval: 3, text: '3M' }
  ],
  height: 35
}}

// Default height
periodSelectorSettings={{
  periods: [...],
  height: 43
}}

// Tall height
periodSelectorSettings={{
  periods: [...],
  height: 55
}}
```

### Complete Height Customization Example

```tsx
function App() {
  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 3, 1), value: 110 },
    { date: new Date(2023, 6, 1), value: 105 },
    { date: new Date(2023, 9, 1), value: 115 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      periodSelectorSettings={{
        periods: [
          { intervalType: 'Months', interval: 1, text: '1M' },
          { intervalType: 'Months', interval: 3, text: '3M' },
          { intervalType: 'Months', interval: 6, text: '6M' },
          { intervalType: 'Years', interval: 1, text: '1Y' }
        ],
        position: 'Top',
        height: 50
      }}
    >
      <Inject services={[AreaSeries, DateTime, PeriodSelector]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="date"
          yName="value"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}
```

## Visibility of Range Navigator

The `disableRangeSelector` property allows you to display only the Period Selector without the Range Navigator chart.

### Show Period Selector Only

```tsx
import { 
  RangeNavigatorComponent, 
  PeriodSelector, 
  DateTime, 
  Inject 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      disableRangeSelector={true}
      periodSelectorSettings={{
        periods: [
          { intervalType: 'Months', interval: 1, text: '1M' },
          { intervalType: 'Months', interval: 3, text: '3M' },
          { intervalType: 'Months', interval: 6, text: '6M' },
          { intervalType: 'Years', interval: 1, text: '1Y' },
          { text: 'YTD' },
          { text: 'All' }
        ],
        position: 'Top'
      }}
    >
      <Inject services={[PeriodSelector, DateTime]} />
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### When to Disable Range Selector

**Use `disableRangeSelector={true}` when:**
- You only need predefined period buttons
- Screen space is limited
- Simplified UI for mobile devices
- Users don't need custom range selection
- Standard periods cover all use cases

**Use `disableRangeSelector={false}` (default) when:**
- Users need custom range selection
- Flexible date filtering is required
- Visual data representation is helpful
- Users need to see data distribution

### Period Selector Only with External Chart

```tsx
import { useState } from 'react';
import { 
  RangeNavigatorComponent, 
  PeriodSelector, 
  DateTime, 
  Inject 
} from '@syncfusion/ej2-react-charts';
import { ChartComponent, SeriesCollectionDirective, SeriesDirective } from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const [selectedRange, setSelectedRange] = useState({
    start: new Date(2023, 0, 1),
    end: new Date(2023, 11, 31)
  });

  const handleRangeChange = (args) => {
    setSelectedRange({
      start: args.start,
      end: args.end
    });
  };

  return (
    <div>
      {/* Main Chart */}
      <ChartComponent>
        {/* Chart configuration with filtered data */}
      </ChartComponent>

      {/* Period Selector Only */}
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        value={[selectedRange.start, selectedRange.end]}
        disableRangeSelector={true}
        changed={handleRangeChange}
        periodSelectorSettings={{
          periods: [
            { intervalType: 'Months', interval: 1, text: '1M' },
            { intervalType: 'Months', interval: 3, text: '3M' },
            { intervalType: 'Months', interval: 6, text: '6M' },
            { intervalType: 'Years', interval: 1, text: '1Y' }
          ],
          position: 'Top'
        }}
      >
        <Inject services={[PeriodSelector, DateTime]} />
      </RangeNavigatorComponent>
    </div>
  );
}
export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Complete Period Selector Example

Here's a comprehensive example with stock data and multiple period options:

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  PeriodSelector, 
  RangeTooltip, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const stockData = [
    { date: new Date(2020, 0, 1), price: 100 },
    { date: new Date(2020, 1, 1), price: 105 },
    { date: new Date(2020, 2, 1), price: 110 },
    { date: new Date(2020, 3, 1), price: 108 },
    { date: new Date(2020, 4, 1), price: 115 },
    { date: new Date(2020, 5, 1), price: 120 },
    { date: new Date(2020, 6, 1), price: 118 },
    { date: new Date(2020, 7, 1), price: 125 },
    { date: new Date(2020, 8, 1), price: 130 },
    { date: new Date(2020, 9, 1), price: 128 },
    { date: new Date(2020, 10, 1), price: 135 },
    { date: new Date(2020, 11, 1), price: 140 },
    { date: new Date(2021, 0, 1), price: 145 },
    { date: new Date(2021, 1, 1), price: 142 },
    { date: new Date(2021, 2, 1), price: 148 },
    { date: new Date(2021, 3, 1), price: 155 },
    { date: new Date(2021, 4, 1), price: 150 },
    { date: new Date(2021, 5, 1), price: 158 },
    { date: new Date(2021, 6, 1), price: 165 },
    { date: new Date(2021, 7, 1), price: 160 },
    { date: new Date(2021, 8, 1), price: 168 },
    { date: new Date(2021, 9, 1), price: 175 },
    { date: new Date(2021, 10, 1), price: 170 },
    { date: new Date(2021, 11, 1), price: 180 }
  ];

  const handlePeriodChange = (args) => {
    console.log('Selected Period:', args.start, 'to', args.end);
  };

  return (
    <div className="App">
      <h2>Stock Price Analysis</h2>
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM yyyy"
        value={[new Date(2021, 0, 1), new Date(2021, 11, 31)]}
        tooltip={{ enable: true, displayMode: 'Always' }}
        changed={handlePeriodChange}
        periodSelectorSettings={{
          periods: [
            { intervalType: 'Months', interval: 1, text: '1M' },
            { intervalType: 'Months', interval: 3, text: '3M' },
            { intervalType: 'Months', interval: 6, text: '6M' },
            { intervalType: 'Years', interval: 1, text: '1Y' },
            { text: 'YTD' },
            { text: 'All' }
          ],
          position: 'Top',
          height: 45
        }}
      >
        <Inject services={[AreaSeries, DateTime, PeriodSelector, RangeTooltip ]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={stockData}
            xName="date"
            yName="price"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Period Selector Configuration Summary

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| periods | Array | [] | Array of period objects with interval, text, intervalType |
| position | String | 'Top' | Position of period selector ('Top' or 'Bottom') |
| height | Number | 43 | Height of period selector in pixels |

### Period Object Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| interval | Number | No | Count value for the period (e.g., 1, 3, 6) |
| text | String | Yes | Text displayed on the button |
| intervalType | String | No | Type of interval (Years, Months, Days, etc.) |

## Best Practices

1. **Use Common Periods**: Include standard periods like 1M, 3M, 6M, 1Y, YTD, All
2. **Module Injection**: Always inject PeriodSelector module
3. **DateTime Required**: Period Selector only works with DateTime valueType
4. **Position Wisely**: Place at Top for better visibility
5. **Consistent Text**: Use clear, short button labels (1M, 3M, not "One Month")
6. **Include 'All'**: Always provide an option to view all data
7. **Disable Range Navigator**: For simple UIs, use disableRangeSelector=true with period selector only

## API Links

Full Range Navigator API: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

Period Selector complex API references:
- [`periodSelectorSettings`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#periodSelectorSettings) (periods array, position, height)
- [`PeriodSelector`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#periodSelectorModule) module (injectable)
- [`disableRangeSelector`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#disableRangeSelector) (show period selector only)

