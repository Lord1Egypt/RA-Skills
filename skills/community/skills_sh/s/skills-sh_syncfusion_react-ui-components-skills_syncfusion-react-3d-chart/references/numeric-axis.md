# Numeric Axis Configuration

A numeric axis displays continuous numerical values with automatic scaling, range calculation, and interval determination.

## Table of contents

- [Basic Numeric Axis](numeric-axis.md#basic-numeric-axis)
- [Range Configuration](numeric-axis.md#range-configuration)
  - [Automatic Range (Default)](numeric-axis.md#automatic-range-default)
  - [Custom Range](numeric-axis.md#custom-range)
  - [Range Padding](numeric-axis.md#range-padding)
- [Interval Configuration](numeric-axis.md#interval-configuration)
  - [Automatic Interval](numeric-axis.md#automatic-interval)
  - [Custom Interval](numeric-axis.md#custom-interval)
  - [Desired Intervals Count](numeric-axis.md#desired-intervals-count)
- [Label Formatting](numeric-axis.md#label-formatting)
  - [Currency Format](numeric-axis.md#currency-format)
  - [Thousands Separator](numeric-axis.md#thousands-separator)
  - [Decimal Precision](numeric-axis.md#decimal-precision)
  - [Percentage Format](numeric-axis.md#percentage-format)
  - [Custom Formatting](numeric-axis.md#custom-formatting)
- [Axis Line and Grid](numeric-axis.md#axis-line-and-grid)
- [Tick Configuration](numeric-axis.md#tick-configuration)
- [Multiple Axes](numeric-axis.md#multiple-axes)
- [Opposed Axis](numeric-axis.md#opposed-axis)
- [Complete Numeric Axis Example](numeric-axis.md#complete-numeric-axis-example)
- [Common Issues](numeric-axis.md#common-issues)

## Basic Numeric Axis

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D } from '@syncfusion/ej2-react-charts';

function NumericAxisChart() {
  const data = [
    { x: 2018, y: 45000 },
    { x: 2019, y: 52000 },
    { x: 2020, y: 48000 },
    { x: 2021, y: 58000 },
    { x: 2022, y: 63000 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{
        valueType: 'Double',  // Numeric axis (default)
        title: 'Year'
      }}
      primaryYAxis={{
        title: 'Revenue ($)'
      }}
    >
      <Inject services={[ColumnSeries3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Note:** Numeric axis is the default type; `valueType: 'Double'` can be omitted.

## Range Configuration

### Automatic Range (Default)

Chart automatically calculates minimum and maximum:

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    // Auto range based on data
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Custom Range

Set explicit minimum and maximum values:

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    minimum: 0,
    maximum: 100,
    interval: 20  // Show labels at 0, 20, 40, 60, 80, 100
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Use custom range when:**
- You want consistent scale across multiple charts
- Need to emphasize certain value ranges
- Comparing charts with different data ranges

### Range Padding

Add padding around automatic range:

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    rangePadding: 'Additional'  // Options: 'None', 'Round', 'Additional', 'Normal', 'Auto'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Range padding options:**
- `None`: No padding, tight fit to data
- `Round`: Round to nice numbers
- `Additional`: Add 10% padding
- `Normal`: Standard padding (default)
- `Auto`: Automatic based on data

## Interval Configuration

### Automatic Interval

Chart calculates optimal interval:

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    // Automatic interval calculation
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Custom Interval

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    minimum: 0,
    maximum: 100,
    interval: 25  // Labels at 0, 25, 50, 75, 100
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Desired Intervals Count

Suggest number of intervals without setting exact value:

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    desiredIntervals: 5  // Approximately 5 intervals
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Label Formatting

### Currency Format

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    labelFormat: '${value}',  // $1000, $2000, etc.
    title: 'Revenue'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Thousands Separator

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    labelFormat: 'n0',  // 1,000  2,000  etc.
    title: 'Population'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Decimal Precision

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    labelFormat: 'n2',  // 1.25, 2.50, etc. (2 decimal places)
    title: 'Average Score'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Percentage Format

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    labelFormat: '{value}%',  // 10%, 20%, etc.
    title: 'Growth Rate'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Custom Formatting

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    labelFormat: '{value}K',  // 10K, 20K, etc.
    title: 'Users'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Axis Line and Grid

### Grid Lines

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    majorGridLines: {
      width: 1,
      color: '#E0E0E0'
    },
    minorGridLines: {
      width: 1,
      color: '#F5F5F5'
    },
    minorTicksPerInterval: 4  // 4 minor ticks between major ticks
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Tick Configuration

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    majorTickLines: {
      width: 1,
      height: 8,
      color: '#333'
    },
    minorTickLines: {
      width: 1,
      height: 4,
      color: '#999'
    },
    minorTicksPerInterval: 4
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Multiple Axes

Add secondary Y-axis for different value ranges:

```tsx
function MultipleAxesChart() {
  const data = [
    { x: 'Jan', temperature: 15, rainfall: 45 },
    { x: 'Feb', temperature: 18, rainfall: 38 },
    { x: 'Mar', temperature: 22, rainfall: 30 },
    { x: 'Apr', temperature: 28, rainfall: 22 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
      primaryYAxis={{
        title: 'Temperature (°C)',
        minimum: 0,
        maximum: 40,
        interval: 10
      }}
      axes={[
        {
          name: 'yAxis2',
          opposedPosition: true,
          title: 'Rainfall (mm)',
          minimum: 0,
          maximum: 60,
          interval: 15,
          labelFormat: '{value}mm'
        }
      ]}
    >
      <Inject services={[ColumnSeries3D, Category3D, Legend3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='x'
          yName='temperature'
          type='Column'
          name='Temperature'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='x'
          yName='rainfall'
          type='Column'
          name='Rainfall'
          yAxisName='yAxis2'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Opposed Axis

Place axis on opposite side (right for Y-axis):

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    opposedPosition: true,
    title: 'Values'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Complete Numeric Axis Example

```tsx
function AdvancedNumericAxis() {
  const revenueData = [
    { year: 2018, revenue: 45000 },
    { year: 2019, revenue: 52000 },
    { year: 2020, revenue: 48000 },
    { year: 2021, revenue: 58000 },
    { year: 2022, revenue: 63000 },
    { year: 2023, revenue: 71000 }
  ];

  return (
    <Chart3DComponent
      id='advanced-numeric'
      title='Annual Revenue Growth'
      primaryXAxis={{
        valueType: 'Double',
        title: 'Year',
        minimum: 2017.5,
        maximum: 2023.5,
        interval: 1,
        labelFormat: '{value}',
        majorGridLines: { width: 1, color: '#E0E0E0' },
        edgeLabelPlacement: 'Shift'
      }}
      primaryYAxis={{
        title: 'Revenue',
        minimum: 0,
        maximum: 80000,
        interval: 20000,
        labelFormat: '${value}',
        rangePadding: 'None',
        majorGridLines: {
          width: 1,
          color: '#E0E0E0'
        },
        minorGridLines: {
          width: 1,
          color: '#F5F5F5'
        },
        minorTicksPerInterval: 3,
        labelStyle: {
          size: '12px',
          fontWeight: '500'
        }
      }}
      rotation={7}
      tilt={10}
    >
      <Inject services={[ColumnSeries3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={revenueData}
          xName='year'
          yName='revenue'
          type='Column'
          name='Revenue'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Common Issues

**Axis not showing expected range:**
- Set `minimum` and `maximum` explicitly
- Check `rangePadding` setting
- Verify data values are numbers, not strings

**Too many/few labels:**
- Adjust `interval` value
- Set `desiredIntervals` for approximate count
- Use `labelIntersectAction` to handle overlap

**Wrong number format:**
- Use `labelFormat: 'n0'` for thousands separator
- Use `labelFormat: 'n2'` for decimals
- Use `labelFormat: '${value}'` for currency

**Minor grid lines not showing:**
- Set `minorTicksPerInterval` > 0
- Configure `minorGridLines.width` > 0

---

See also: [api-reference.md](api-reference.md) | [usage-example.md](usage-example.md)
