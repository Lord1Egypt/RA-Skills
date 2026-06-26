# DateTime Axis Configuration

A DateTime axis displays time-based data with automatic interval calculation, date formatting, and intelligent label placement.
 
## Table of contents

- [Basic DateTime Axis](datetime-axis.md#basic-datetime-axis)
- [Date Data Formats](datetime-axis.md#date-data-formats)
  - [JavaScript Date Objects (Recommended)](datetime-axis.md#javascript-date-objects-recommended)
  - [ISO Date Strings](datetime-axis.md#iso-date-strings)
  - [Timestamp Milliseconds](datetime-axis.md#timestamp-milliseconds)
- [Label Formatting](datetime-axis.md#label-formatting)
  - [Standard Date Formats](datetime-axis.md#standard-date-formats)
  - [Month and Year](datetime-axis.md#month-and-year)
  - [Time Format](datetime-axis.md#time-format)
- [Interval Configuration](datetime-axis.md#interval-configuration)
  - [Automatic Intervals](datetime-axis.md#automatic-intervals)
  - [Manual Interval with Interval Type](datetime-axis.md#manual-interval-with-interval-type)
- [Range Configuration](datetime-axis.md#range-configuration)
  - [Custom Date Range](datetime-axis.md#custom-date-range)
  - [Range Padding](datetime-axis.md#range-padding)
- [Label Rotation and Styling](datetime-axis.md#label-rotation-and-styling)
- [Complete DateTime Example](datetime-axis.md#complete-datetime-example)
- [Hourly/Minute Data Example](datetime-axis.md#hourlyminute-data-example)
- [Common Issues](datetime-axis.md#common-issues)

## Basic DateTime Axis

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, DateTime3D } from '@syncfusion/ej2-react-charts';

function DateTimeAxisChart() {
  const data = [
    { date: new Date(2023, 0, 1), value: 30 },
    { date: new Date(2023, 1, 1), value: 35 },
    { date: new Date(2023, 2, 1), value: 32 },
    { date: new Date(2023, 3, 1), value: 38 },
    { date: new Date(2023, 4, 1), value: 42 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{
        valueType: 'DateTime',
        title: 'Month'
      }}
      primaryYAxis={{
        title: 'Sales'
      }}
    >
      <Inject services={[ColumnSeries3D, DateTime3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='date'
          yName='value'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key requirement:** Must inject `DateTime3D` service and set `valueType: 'DateTime'`.

## Date Data Formats

### JavaScript Date Objects (Recommended)

```tsx
const data = [
  { date: new Date(2023, 0, 15), sales: 120 },  // Jan 15, 2023
  { date: new Date(2023, 1, 15), sales: 135 },  // Feb 15, 2023
  { date: new Date(2023, 2, 15), sales: 142 }   // Mar 15, 2023
];
```

### ISO Date Strings

```tsx
const data = [
  { date: new Date('2023-01-15T00:00:00'), sales: 120 },
  { date: new Date('2023-02-15T00:00:00'), sales: 135 },
  { date: new Date('2023-03-15T00:00:00'), sales: 142 }
];
```

### Timestamp Milliseconds

```tsx
const data = [
  { date: new Date(1673740800000), sales: 120 },  // Timestamp
  { date: new Date(1676419200000), sales: 135 },
  { date: new Date(1678838400000), sales: 142 }
];
```

## Label Formatting

### Standard Date Formats

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'DateTime',
    labelFormat: 'MMM dd',  // Jan 15, Feb 15, etc.
    // OR
    // labelFormat: 'dd/MM/yyyy',  // 15/01/2023
    // OR
    // labelFormat: 'yyyy',  // 2023
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Common format patterns:**
- `MMM dd`: Jan 15, Feb 15
- `dd MMM`: 15 Jan, 15 Feb
- `MMM yyyy`: Jan 2023, Feb 2023
- `dd/MM/yyyy`: 15/01/2023
- `MM/dd/yyyy`: 01/15/2023
- `yyyy-MM-dd`: 2023-01-15
- `hh:mm a`: 02:30 PM
- `HH:mm`: 14:30

### Month and Year

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'DateTime',
    labelFormat: 'MMM yyyy',  // Jan 2023, Feb 2023
    intervalType: 'Months',
    interval: 1
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Time Format

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'DateTime',
    labelFormat: 'hh:mm:ss',  // 02:30:45
    intervalType: 'Hours'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Interval Configuration

#### Automatic Intervals

The chart automatically determines the most suitable interval based on the data range.

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'DateTime',
    // Automatic interval calculation
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Manual Interval with Interval Type

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'DateTime',
    intervalType: 'Months',  // Options: 'Auto', 'Years', 'Months', 'Days', 'Hours', 'Minutes', 'Seconds'
    interval: 3  // Every 3 months
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Interval types:**
- `Auto`: Automatically determine based on data range
- `Years`: Yearly intervals
- `Months`: Monthly intervals
- `Days`: Daily intervals
- `Hours`: Hourly intervals
- `Minutes`: Minute intervals
- `Seconds`: Second intervals

### Examples for Different Time Ranges

**Daily data:**
```tsx
primaryXAxis={{
  valueType: 'DateTime',
  intervalType: 'Days',
  interval: 1,
  labelFormat: 'dd MMM'
}}
```

**Weekly data:**
```tsx
primaryXAxis={{
  valueType: 'DateTime',
  intervalType: 'Days',
  interval: 7,
  labelFormat: 'dd MMM'
}}
```

**Quarterly data:**
```tsx
primaryXAxis={{
  valueType: 'DateTime',
  intervalType: 'Months',
  interval: 3,
  labelFormat: 'MMM yyyy'
}}
```

**Yearly data:**
```tsx
primaryXAxis={{
  valueType: 'DateTime',
  intervalType: 'Years',
  interval: 1,
  labelFormat: 'yyyy'
}}
```

## Range Configuration

### Custom Date Range

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'DateTime',
    minimum: new Date(2023, 0, 1),  // Jan 1, 2023
    maximum: new Date(2023, 11, 31),  // Dec 31, 2023
    intervalType: 'Months',
    interval: 2
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Range Padding

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'DateTime',
    rangePadding: 'Additional'  // Add padding around date range
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Label Rotation and Styling

Handle long date labels:

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{
    valueType: 'DateTime',
    labelFormat: 'dd MMM yyyy',
    labelRotation: -45,
    labelStyle: {
      size: '11px',
      fontWeight: '500'
    }
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Complete DateTime Example

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, DateTime3D, ColumnSeries3D } from '@syncfusion/ej2-react-charts';
import * as React from "react";
import { createRoot } from 'react-dom/client';

function App() {
    const salesData = [
        { date: new Date(2023, 0, 1), sales: 45000 },
        { date: new Date(2023, 1, 1), sales: 52000 },
        { date: new Date(2023, 2, 1), sales: 48000 },
        { date: new Date(2023, 3, 1), sales: 58000 },
        { date: new Date(2023, 4, 1), sales: 63000 },
        { date: new Date(2023, 5, 1), sales: 59000 },
        { date: new Date(2023, 6, 1), sales: 68000 },
        { date: new Date(2023, 7, 1), sales: 72000 },
        { date: new Date(2023, 8, 1), sales: 70000 },
        { date: new Date(2023, 9, 1), sales: 78000 },
        { date: new Date(2023, 10, 1), sales: 82000 },
        { date: new Date(2023, 11, 1), sales: 88000 }
      ];
    
      return (
        <Chart3DComponent
          id='datetime-chart'
          title='Monthly Sales - 2023'
          primaryXAxis={{
            valueType: 'DateTime',
            title: 'Month',
            labelFormat: 'MMM',
            intervalType: 'Months',
            interval: 1,
            edgeLabelPlacement: 'Shift',
            majorGridLines: {
              width: 1,
              color: '#E0E0E0'
            },
            labelStyle: {
              size: '12px'
            }
          }}
          primaryYAxis={{
            title: 'Sales ($)',
            labelFormat: '${value}K',
            minimum: 0,
            maximum: 100000,
            interval: 20000
          }}
          rotation={7}
          tilt={10}
        >
          <Inject services={[ColumnSeries3D, DateTime3D]} />
          <Chart3DSeriesCollectionDirective>
            <Chart3DSeriesDirective
              dataSource={salesData}
              xName='date'
              yName='sales'
              type='Column'
              name='Sales'
            />
          </Chart3DSeriesCollectionDirective>
        </Chart3DComponent>
      );
}
;
export default App;
createRoot(document.getElementById('charts')).render(<App />);
```

## Hourly/Minute Data Example

```tsx
function HourlyTraffic() {
  const data = [
    { time: new Date(2023, 5, 15, 8, 0), visitors: 120 },
    { time: new Date(2023, 5, 15, 10, 0), visitors: 245 },
    { time: new Date(2023, 5, 15, 12, 0), visitors: 380 },
    { time: new Date(2023, 5, 15, 14, 0), visitors: 310 },
    { time: new Date(2023, 5, 15, 16, 0), visitors: 290 },
    { time: new Date(2023, 5, 15, 18, 0), visitors: 420 }
  ];

  return (
    <Chart3DComponent
      id='hourly-chart'
      title='Website Traffic - June 15, 2023'
      primaryXAxis={{
        valueType: 'DateTime',
        title: 'Time',
        labelFormat: 'hh:mm a',
        intervalType: 'Hours',
        interval: 2,
        minimum: new Date(2023, 5, 15, 7, 0),
        maximum: new Date(2023, 5, 15, 19, 0)
      }}
      primaryYAxis={{
        title: 'Visitors',
        minimum: 0,
        maximum: 500,
        interval: 100
      }}
    >
      <Inject services={[ColumnSeries3D, DateTime3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='time'
          yName='visitors'
          type='Column'
          name='Visitors'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Common Issues

**Dates not displaying correctly:**
- Ensure data contains actual Date objects: `new Date(...)`
- Verify `valueType: 'DateTime'` is set
- Check `DateTime3D` service is injected

**Labels overlapping:**
- Use `labelRotation: -45` or `-90`
- Reduce label density with larger `interval`
- Use shorter `labelFormat` (e.g., 'MMM' instead of 'MMM yyyy')

**Wrong date range:**
- Set `minimum` and `maximum` explicitly
- Adjust `rangePadding` setting
- Verify date objects are valid

**Incorrect intervals:**
- Set `intervalType` to match your data granularity
- Adjust `interval` value
- Use `edgeLabelPlacement: 'Shift'` for edge labels

---

See also: [api-reference.md](api-reference.md) | [usage-example.md](usage-example.md)
