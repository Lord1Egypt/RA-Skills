# Lightweight Mode

By default, when the `dataSource` for `series` is empty, a lightweight Range Selector will be displayed without the chart series. This mode is particularly useful for mobile devices, reduced data scenarios, or when you only need the range selection interface without data visualization.

## Table of contents
- [What is Lightweight Mode?](#what-is-lightweight-mode)
- [When to Use Lightweight Mode](#when-to-use-lightweight-mode)
- [Basic Lightweight Implementation](#basic-lightweight-implementation)
- [Lightweight with Numeric Data](#lightweight-with-numeric-data)
- [Lightweight with Customization](#lightweight-with-customization)
- [Lightweight with Tooltip](#lightweight-with-tooltip)
- [Lightweight with Period Selector](#lightweight-with-period-selector)
- [Lightweight for Mobile Devices](#lightweight-for-mobile-devices)
- [Lightweight with External Chart](#lightweight-with-external-chart)
- [Configuration Requirements for Lightweight Mode](#configuration-requirements-for-lightweight-mode)
- [Performance Benefits](#performance-benefits)
- [Complete Lightweight Example](#complete-lightweight-example)
- [Key Points](#key-points)
- [Lightweight vs Full Mode Comparison](#lightweight-vs-full-mode-comparison)
- [API Links](#api-links)

## What is Lightweight Mode?

Lightweight mode provides a simplified Range Navigator that:
- Displays only the range selection interface (sliders and axis)
- Removes the chart series visualization
- Reduces rendering overhead and improves performance
- Ideal for mobile devices with limited screen space
- Useful when data visualization is handled elsewhere

## When to Use Lightweight Mode

**Use lightweight mode when:**
- Deploying on mobile devices where performance matters
- Chart data is displayed in a separate component
- You only need range selection functionality
- Minimizing UI complexity
- Reducing initial load time
- Screen space is constrained

**Don't use lightweight mode when:**
- Users need to see data distribution
- Visual context helps with range selection
- Desktop application with ample resources
- Data preview is essential for decision-making

## Basic Lightweight Implementation

When no series or dataSource is provided, Range Navigator automatically enters lightweight mode:

```tsx
import { 
  RangeNavigatorComponent, 
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
      minimum={new Date(2023, 0, 1)}
      maximum={new Date(2023, 11, 31)}
      value={[new Date(2023, 2, 1), new Date(2023, 9, 1)]}
      labelFormat="MMM yyyy"
    >
      <Inject services={[DateTime]} />
      {/* No series - lightweight mode */}
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Lightweight with Numeric Data

```tsx
import { RangeNavigatorComponent } from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="Double"
      minimum={0}
      maximum={100}
      interval={10}
      value={[20, 80]}
    >
      {/* No series - lightweight numeric range selector */}
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Lightweight with Customization

You can still customize the appearance in lightweight mode:

```tsx
import { 
  RangeNavigatorComponent, 
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
      minimum={new Date(2023, 0, 1)}
      maximum={new Date(2023, 11, 31)}
      value={[new Date(2023, 3, 1), new Date(2023, 8, 1)]}
      labelFormat="MMM"
      
      // Customization
      navigatorStyleSettings={{
        selectedRegionColor: 'rgba(33, 150, 243, 0.3)',
        thumb: {
          type: 'Circle',
          width: 20,
          height: 20,
          fill: '#2196F3',
          border: { width: 2, color: '#ffffff' }
        }
      }}
      navigatorBorder={{ width: 2, color: '#2196F3' }}
    >
      <Inject services={[DateTime]} />
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Lightweight with Tooltip

```tsx
import { 
  RangeNavigatorComponent, 
  DateTime, 
  RangeTooltip, 
  Inject
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      minimum={new Date(2023, 0, 1)}
      maximum={new Date(2023, 11, 31)}
      value={[new Date(2023, 0, 1), new Date(2023, 5, 1)]}
      labelFormat="MMM yyyy"
      tooltip={{ 
        enable: true,
        displayMode: 'Always'
      }}
    >
      <Inject services={[DateTime, RangeTooltip ]} />
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Lightweight with Period Selector

Combine lightweight mode with period selector for a clean, button-based interface:

```tsx
import { 
  RangeNavigatorComponent, 
  DateTime, 
  PeriodSelector, 
  Inject 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      minimum={new Date(2020, 0, 1)}
      maximum={new Date(2023, 11, 31)}
      value={[new Date(2022, 0, 1), new Date(2023, 11, 31)]}
      periodSelectorSettings={{
        periods: [
          { intervalType: 'Months', interval: 1, text: '1M' },
          { intervalType: 'Months', interval: 3, text: '3M' },
          { intervalType: 'Months', interval: 6, text: '6M' },
          { intervalType: 'Years', interval: 1, text: '1Y' },
          { text: 'All' }
        ],
        position: 'Top'
      }}
    >
      <Inject services={[DateTime, PeriodSelector]} />
      {/* Lightweight with period selector */}
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Lightweight for Mobile Devices

```tsx
import { useState, useEffect } from 'react';
import { 
  RangeNavigatorComponent, 
  DateTime, 
  RangeTooltip, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

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
      minimum={new Date(2023, 0, 1)}
      maximum={new Date(2023, 11, 31)}
      value={[new Date(2023, 0, 1), new Date(2023, 9, 1)]}
      labelFormat="MMM"
      tooltip={{ enable: true }}
    >
      <Inject services={[DateTime, RangeTooltip ]} />
      {!isMobile && (
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      )}
      {/* Shows series on desktop, lightweight on mobile */}
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Lightweight with External Chart

Use lightweight Range Navigator to control a separate chart component:

```tsx
import { useState } from 'react';
import { 
  RangeNavigatorComponent, 
  DateTime, 
  Inject 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';
import { 
  ChartComponent, 
  SeriesCollectionDirective, 
  SeriesDirective,
  LineSeries,
  DateTime as ChartDateTime,
  Inject as ChartInject
} from '@syncfusion/ej2-react-charts';

function App() {
  const [selectedRange, setSelectedRange] = useState({
    start: new Date(2023, 0, 1),
    end: new Date(2023, 5, 1)
  });

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 },
    { date: new Date(2023, 4, 1), value: 120 },
    { date: new Date(2023, 5, 1), value: 125 },
    { date: new Date(2023, 6, 1), value: 130 },
    { date: new Date(2023, 7, 1), value: 128 },
    { date: new Date(2023, 8, 1), value: 135 },
    { date: new Date(2023, 9, 1), value: 140 },
    { date: new Date(2023, 10, 1), value: 138 },
    { date: new Date(2023, 11, 1), value: 145 }
  ];

  const filteredData = data.filter(
    item => item.date >= selectedRange.start && item.date <= selectedRange.end
  );

  const handleRangeChange = (args) => {
    setSelectedRange({
      start: args.start,
      end: args.end
    });
  };

  return (
    <div>
      {/* Main Chart */}
      <ChartComponent
        primaryXAxis={{ valueType: 'DateTime' }}
        title="Sales Data"
      >
        <ChartInject services={[LineSeries, ChartDateTime]} />
        <SeriesCollectionDirective>
          <SeriesDirective
            dataSource={filteredData}
            xName="date"
            yName="value"
            type="Line"
          />
        </SeriesCollectionDirective>
      </ChartComponent>

      {/* Lightweight Range Navigator */}
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        minimum={new Date(2023, 0, 1)}
        maximum={new Date(2023, 11, 31)}
        value={[selectedRange.start, selectedRange.end]}
        labelFormat="MMM"
        changed={handleRangeChange}
      >
        <Inject services={[DateTime]} />
        {/* Lightweight - no series */}
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Configuration Requirements for Lightweight Mode

When using lightweight mode, you must explicitly set:

### For DateTime

```tsx
<RangeNavigatorComponent
  valueType="DateTime"
  minimum={new Date(2023, 0, 1)}    // Required
  maximum={new Date(2023, 11, 31)}   // Required
  value={[startDate, endDate]}       // Optional initial range
  labelFormat="MMM yyyy"             // Optional format
>
  <Inject services={[DateTime]} />
</RangeNavigatorComponent>
```

### For Numeric

```tsx
<RangeNavigatorComponent
  valueType="Double"
  minimum={0}          // Required
  maximum={100}        // Required
  interval={10}        // Optional
  value={[20, 80]}     // Optional initial range
>
</RangeNavigatorComponent>
```

## Performance Benefits

Lightweight mode provides:

- **Faster Rendering**: No series data to process or render
- **Reduced Memory**: Smaller memory footprint without chart data
- **Smaller Bundle**: Only core Range Navigator modules needed
- **Better Mobile Experience**: Simplified UI for small screens
- **Quick Initialization**: Instant load without data processing

## Complete Lightweight Example

```tsx
import { 
  RangeNavigatorComponent, 
  DateTime, 
  RangeTooltip, 
  Inject
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';
import { useState } from 'react';

function App() {
  const [selectedRange, setSelectedRange] = useState({
    start: new Date(2023, 0, 1),
    end: new Date(2023, 5, 1)
  });

  const handleChange = (args) => {
    setSelectedRange({
      start: args.start,
      end: args.end
    });
    console.log('Selected:', args.start, 'to', args.end);
  };

  return (
    <div className="App">
      <h2>Lightweight Range Navigator</h2>
      <p>Performance-optimized for mobile devices</p>
      
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        minimum={new Date(2023, 0, 1)}
        maximum={new Date(2023, 11, 31)}
        value={[selectedRange.start, selectedRange.end]}
        labelFormat="MMM yyyy"
        intervalType="Months"
        tooltip={{ 
          enable: true,
          displayMode: 'Always'
        }}
        navigatorStyleSettings={{
          selectedRegionColor: 'rgba(33, 150, 243, 0.3)',
          thumb: {
            type: 'Circle',
            width: 20,
            height: 20,
            fill: '#2196F3',
            border: { width: 2, color: '#ffffff' }
          }
        }}
        changed={handleChange}
      >
        <Inject services={[DateTime, RangeTooltip]} />
      </RangeNavigatorComponent>

      <div style={{ marginTop: '20px' }}>
        <h3>Selected Range:</h3>
        <p>From: {selectedRange.start.toLocaleDateString()}</p>
        <p>To: {selectedRange.end.toLocaleDateString()}</p>
      </div>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Key Points

1. **Automatic Activation**: Lightweight mode activates automatically when no series is provided
2. **Module Injection**: Still inject required modules (DateTime, Logarithmic, etc.) for value type
3. **Explicit Range**: Set minimum and maximum explicitly
4. **Full Customization**: All appearance and behavior customizations work in lightweight mode
5. **No Performance Loss**: Removing series has no negative impact
6. **Mobile Friendly**: Ideal for responsive designs
7. **Works with Period Selector**: Combine with period selector for button-based selection
8. **External Data**: Use with external charts or data grids

## Lightweight vs Full Mode Comparison

| Feature | Lightweight | Full (with Series) |
|---------|-------------|-------------------|
| Series Visualization | ❌ No | ✅ Yes |
| Range Selection | ✅ Yes | ✅ Yes |
| Tooltip | ✅ Yes | ✅ Yes |
| Period Selector | ✅ Yes | ✅ Yes |
| Customization | ✅ Yes | ✅ Yes |
| Performance | ⚡ Fast | ✓ Standard |
| Memory Usage | 🔽 Low | ✓ Normal |
| Mobile Friendly | ✅ Excellent | ✓ Good |
| Data Context | ❌ No visual | ✅ Visual context |

## API Links

Full Range Navigator API: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

Lightweight and related complex API references:
- [`valueType`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#valueType), [`minimum`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#minimum), [`maximum`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#maximum), [`value`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#value) (required for explicit ranges in lightweight mode)
- [`periodSelectorSettings`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#periodSelectorSettings), [`disableRangeSelector`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#disableRangeSelector) (period selector only mode)
- [`tooltip`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#tooltip) settings and [`RangeTooltip`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#rangeTooltipModule) module for lightweight tooltips

