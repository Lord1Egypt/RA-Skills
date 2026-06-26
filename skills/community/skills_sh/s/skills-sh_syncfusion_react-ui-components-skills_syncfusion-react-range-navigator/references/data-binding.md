# Data Binding and Value Types

The Range Navigator supports three value types for the axis: Numeric (Double), Logarithmic, and DateTime. Each value type is optimized for different data scenarios and provides specific configuration options.

## Table of Contents
- [Numeric Value Type](#numeric-value-type)
- [Range Configuration](#range-configuration)
- [Numeric Label Formatting](#numeric-label-formatting)
- [Custom Label Format](#custom-label-format)
- [Logarithmic Axis](#logarithmic-axis)
- [Logarithmic Range](#logarithmic-range)
- [Logarithmic Base](#logarithmic-base)
- [DateTime Value Type](#datetime-value-type)
- [DateTime Interval Customization](#datetime-interval-customization)
- [DateTime Label Format](#datetime-label-format)

## Numeric Value Type

The numeric scale represents numeric values in the Range Navigator. By default, the `valueType` is **Double**.

### Basic Numeric Implementation

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { x: 0, y: 10 },
    { x: 10, y: 30 },
    { x: 20, y: 25 },
    { x: 30, y: 45 },
    { x: 40, y: 35 },
    { x: 50, y: 55 },
    { x: 60, y: 50 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="Double"
    >
      <Inject services={[AreaSeries]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Range Configuration

The minimum and maximum of the scale are calculated automatically based on the provided data. You can customize these values using the `minimum`, `maximum`, and `interval` properties.

### Automatic Range

```tsx
// Range is automatically calculated from data
const data = [
  { x: 0, y: 10 },
  { x: 100, y: 50 }
];

<RangeNavigatorComponent valueType="Double">
  {/* Automatic range: 0 to 100 */}
</RangeNavigatorComponent>
```

### Custom Range

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { x: 0, y: 10 },
    { x: 10, y: 30 },
    { x: 20, y: 25 },
    { x: 30, y: 45 },
    { x: 40, y: 35 },
    { x: 50, y: 55 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="Double"
      minimum={0}
      maximum={60}
      interval={10}
      value={[10, 40]}
    >
      <Inject services={[AreaSeries]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

**Properties:**
- `minimum`: Minimum value of the axis
- `maximum`: Maximum value of the axis
- `interval`: Spacing between axis labels
- `value`: Initial selected range [start, end]

## Numeric Label Formatting

Format numeric labels using the `labelFormat` property. It supports all globalized formats.

### Standard Formats

```tsx
// Number format with 1 decimal place
<RangeNavigatorComponent
  valueType="Double"
  labelFormat="n1"
>
  {/* Labels: 1000.0, 2000.0, 3000.0 */}
</RangeNavigatorComponent>

// Percentage format
<RangeNavigatorComponent
  valueType="Double"
  labelFormat="p2"
>
  {/* Labels: 1.00%, 2.00%, 3.00% */}
</RangeNavigatorComponent>

// Currency format
<RangeNavigatorComponent
  valueType="Double"
  labelFormat="c2"
>
  {/* Labels: $1,000.00, $2,000.00, $3,000.00 */}
</RangeNavigatorComponent>
```

### Label Format Reference Table

| Label Value | Format | Result | Description |
|------------|--------|--------|-------------|
| 1000 | n1 | 1000.0 | Number rounded to 1 decimal place |
| 1000 | n2 | 1000.00 | Number rounded to 2 decimal places |
| 1000 | n3 | 1000.000 | Number rounded to 3 decimal places |
| 0.01 | p1 | 1.0% | Percentage with 1 decimal place |
| 0.01 | p2 | 1.00% | Percentage with 2 decimal places |
| 0.01 | p3 | 1.000% | Percentage with 3 decimal places |
| 1000 | c1 | $1,000.0 | Currency with 1 decimal place |
| 1000 | c2 | $1,000.00 | Currency with 2 decimal places |

### Complete Example with Formatting

```tsx
function App() {
  const salesData = [
    { month: 1, sales: 15000 },
    { month: 2, sales: 18000 },
    { month: 3, sales: 22000 },
    { month: 4, sales: 25000 },
    { month: 5, sales: 28000 },
    { month: 6, sales: 32000 }
  ];

  return (
    <RangeNavigatorComponent
      valueType="Double"
      minimum={0}
      maximum={35000}
      interval={5000}
      labelFormat="c0"
    >
      <Inject services={[AreaSeries]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={salesData}
          xName="month"
          yName="sales"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}
```

## Custom Label Format

The Range Navigator supports custom label formats using placeholders like `{value}$`, where `{value}` represents the axis label value.

### Custom Format Examples

```tsx
// Append dollar sign
<RangeNavigatorComponent
  valueType="Double"
  labelFormat="{value}$"
>
  {/* Labels: 10$, 20$, 30$ */}
</RangeNavigatorComponent>

// Prepend text
<RangeNavigatorComponent
  valueType="Double"
  labelFormat="Value: {value}"
>
  {/* Labels: Value: 10, Value: 20, Value: 30 */}
</RangeNavigatorComponent>

// Custom currency
<RangeNavigatorComponent
  valueType="Double"
  labelFormat="₹{value}"
>
  {/* Labels: ₹10, ₹20, ₹30 */}
</RangeNavigatorComponent>
```

### Complete Custom Format Example

```tsx
function App() {
  const data = [
    { x: 10, y: 100 },
    { x: 20, y: 150 },
    { x: 30, y: 120 },
    { x: 40, y: 180 },
    { x: 50, y: 200 }
  ];

  return (
    <RangeNavigatorComponent
      valueType="Double"
      labelFormat="{value}K Units"
      minimum={0}
      maximum={60}
      interval={10}
    >
      <Inject services={[AreaSeries]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}
```

## Logarithmic Axis

The logarithmic scale visualizes data when the Range Navigator has numerical values in both lower (e.g., 10⁻⁶) and higher (e.g., 10⁶) orders of magnitude.

### Module Injection Required

```tsx
import { Logarithmic } from '@syncfusion/ej2-react-charts';
<Inject services={[LineSeries, Logarithmic]} />
```

### Basic Logarithmic Implementation

```tsx
import { 
  RangeNavigatorComponent, 
  LineSeries, 
  Logarithmic, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { x: 1, y: 100 },
    { x: 2, y: 1000 },
    { x: 3, y: 10000 },
    { x: 4, y: 100000 },
    { x: 5, y: 1000000 }
  ];

  return (
    <RangeNavigatorComponent
      valueType="Logarithmic"
    >
      <Inject services={[LineSeries, Logarithmic]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Line"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

**Key Points:**
1. Set `valueType="Logarithmic"`
2. Inject the `Logarithmic` module
3. Suitable for data spanning multiple orders of magnitude

## Logarithmic Range

Customize the minimum, maximum, and interval for logarithmic scales.

```tsx
import { 
  RangeNavigatorComponent, 
  LineSeries, 
  Logarithmic, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { x: 1, y: 1000 },
    { x: 2, y: 10000 },
    { x: 3, y: 100000 },
    { x: 4, y: 1000000 }
  ];

  return (
    <RangeNavigatorComponent
      valueType="Logarithmic"
      minimum={100}
      maximum={10000000}
      interval={1}
    >
      <Inject services={[LineSeries, Logarithmic]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Line"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

**Properties:**
- `minimum`: Starting logarithmic value (e.g., 100 = 10²)
- `maximum`: Ending logarithmic value (e.g., 10000000 = 10⁷)
- `interval`: Number of powers between labels (1 = every power)

## Logarithmic Base

Customize the logarithmic base using the `logBase` property. The default base is **10**.

### Custom Base Examples

```tsx
// Base 10 (default)
<RangeNavigatorComponent
  valueType="Logarithmic"
  logBase={10}
>
  {/* Labels: 10, 100, 1000, 10000 */}
</RangeNavigatorComponent>

// Base 2
<RangeNavigatorComponent
  valueType="Logarithmic"
  logBase={2}
>
  {/* Labels: 2, 4, 8, 16, 32, 64 */}
</RangeNavigatorComponent>

// Base E (natural logarithm)
<RangeNavigatorComponent
  valueType="Logarithmic"
  logBase={Math.E}
>
  {/* Labels: e, e², e³, e⁴ */}
</RangeNavigatorComponent>
```

### Complete Logarithmic Example

```tsx
function App() {
  const scientificData = [
    { x: 1, y: 10 },
    { x: 2, y: 100 },
    { x: 3, y: 1000 },
    { x: 4, y: 10000 },
    { x: 5, y: 100000 },
    { x: 6, y: 1000000 }
  ];

  return (
    <RangeNavigatorComponent
      valueType="Logarithmic"
      logBase={10}
      minimum={1}
      maximum={10000000}
      interval={1}
    >
      <Inject services={[LineSeries, Logarithmic]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={scientificData}
          xName="x"
          yName="y"
          type="Line"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}
```

## DateTime Value Type

The DateTime scale displays date and time values as labels in the specified format. This is ideal for time-series data.

### Module Injection Required

```tsx
import { DateTime } from '@syncfusion/ej2-react-charts';
<Inject services={[AreaSeries, DateTime]} />
```

### Basic DateTime Implementation

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { x: new Date(2018, 0, 1), y: 35 },
    { x: new Date(2018, 1, 1), y: 28 },
    { x: new Date(2018, 2, 1), y: 34 },
    { x: new Date(2018, 3, 1), y: 32 },
    { x: new Date(2018, 4, 1), y: 40 },
    { x: new Date(2018, 5, 1), y: 42 }
  ];

  return (
    <RangeNavigatorComponent
      valueType="DateTime"
      labelFormat="MMM"
    >
      <Inject services={[AreaSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

**Key Points:**
1. Set `valueType="DateTime"`
2. Inject the `DateTime` module
3. Use Date objects in your data array
4. Format labels with `labelFormat`

## DateTime Interval Customization

Customize DateTime intervals using the `interval` and `intervalType` properties.

### Available Interval Types

- **Auto**: Automatically determined
- **Years**: Yearly intervals
- **Quarter**: Quarterly intervals (3 months)
- **Months**: Monthly intervals
- **Weeks**: Weekly intervals
- **Days**: Daily intervals
- **Hours**: Hourly intervals
- **Minutes**: Minute intervals
- **Seconds**: Second intervals

### Interval Examples

```tsx
// Every 2 years
<RangeNavigatorComponent
  valueType="DateTime"
  interval={2}
  intervalType="Years"
  labelFormat="yyyy"
>
</RangeNavigatorComponent>

// Every 3 months
<RangeNavigatorComponent
  valueType="DateTime"
  interval={3}
  intervalType="Months"
  labelFormat="MMM yyyy"
>
</RangeNavigatorComponent>

// Every 7 days
<RangeNavigatorComponent
  valueType="DateTime"
  interval={7}
  intervalType="Days"
  labelFormat="dd MMM"
>
</RangeNavigatorComponent>
```

### Complete DateTime Interval Example

```tsx
function App() {
  const stockData = [
    { date: new Date(2020, 0, 1), price: 100 },
    { date: new Date(2020, 3, 1), price: 110 },
    { date: new Date(2020, 6, 1), price: 105 },
    { date: new Date(2020, 9, 1), price: 115 },
    { date: new Date(2021, 0, 1), price: 120 },
    { date: new Date(2021, 3, 1), price: 130 },
    { date: new Date(2021, 6, 1), price: 125 },
    { date: new Date(2021, 9, 1), price: 135 }
  ];

  return (
    <RangeNavigatorComponent
      valueType="DateTime"
      interval={3}
      intervalType="Months"
      labelFormat="MMM yyyy"
    >
      <Inject services={[AreaSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={stockData}
          xName="date"
          yName="price"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}
```

## DateTime Label Format

Use the `labelFormat` property to format and parse dates using globalized formats.

### Common DateTime Formats

```tsx
// Display day name
<RangeNavigatorComponent labelFormat="EEEE">
  {/* Monday, Tuesday, Wednesday */}
</RangeNavigatorComponent>

// Display month/day/year
<RangeNavigatorComponent labelFormat="yMd">
  {/* 04/10/2000 */}
</RangeNavigatorComponent>

// Display month abbreviation
<RangeNavigatorComponent labelFormat="MMM">
  {/* Jan, Feb, Mar */}
</RangeNavigatorComponent>

// Display time
<RangeNavigatorComponent labelFormat="hm">
  {/* 12:00 AM, 1:30 PM */}
</RangeNavigatorComponent>
```

### DateTime Format Reference Table

| Label Value | Format | Result | Description |
|------------|--------|--------|-------------|
| new Date(2000, 3, 10) | EEEE | Monday | Day name in full |
| new Date(2000, 3, 10) | yMd | 04/10/2000 | Month/date/year format |
| new Date(2000, 3, 10) | MMM | Apr | Month abbreviation |
| new Date(2000, 3, 10) | hm | 12:00 AM | Time in hours:minutes |
| new Date(2000, 3, 10) | hms | 12:00:00 AM | Time with seconds |

### Complete DateTime Format Example

```tsx
function App() {
  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 },
    { date: new Date(2023, 4, 1), value: 120 },
    { date: new Date(2023, 5, 1), value: 125 }
  ];

  return (
    <RangeNavigatorComponent
      valueType="DateTime"
      intervalType="Months"
      labelFormat="MMM yyyy"
      value={[new Date(2023, 0, 1), new Date(2023, 5, 1)]}
    >
      <Inject services={[AreaSeries, DateTime]} />
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

## Data Binding Summary

### Value Type Selection Guide

| Data Type | Use Case | Value Type | Module Required |
|-----------|----------|------------|-----------------|
| Numbers | Sales, revenue, counts | Double | None (default) |
| Scientific data | 10⁻⁶ to 10⁶ range | Logarithmic | Logarithmic |
| Dates/Times | Time-series, historical | DateTime | DateTime |

### Key Configuration Properties

- **valueType**: 'Double' | 'DateTime' | 'Logarithmic'
- **minimum**: Starting axis value
- **maximum**: Ending axis value
- **interval**: Spacing between labels
- **intervalType**: For DateTime (Years, Months, Days, etc.)
- **labelFormat**: Label display format
- **logBase**: Base for logarithmic scale (default: 10)
- **value**: Initial selected range [start, end]

## API Links

Full Range Navigator API: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

Complex properties and related API references used above:
- [`valueType`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#valueType), [`minimum`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#minimum), [`maximum`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#maximum), [`interval`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#interval), [`intervalType`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#intervalType), [`value`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#value)
- [`logBase`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#logBase), [`logarithmicModule`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#logarithmicModule)
- [`dataSource`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#dataSource), [`xName`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#xName), [`yName`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#yName), [`series`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#series), [`query`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#query)

