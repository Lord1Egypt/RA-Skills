# Logarithmic Axis Configuration

A logarithmic axis displays data that spans multiple orders of magnitude using a logarithmic scale, making it ideal for exponential growth, scientific data, or wide value ranges.

## Table of contents

- [Basic Logarithmic Axis](logarithmic-axis.md#basic-logarithmic-axis)
- [When to Use Logarithmic Scale](logarithmic-axis.md#when-to-use-logarithmic-scale)
- [Logarithmic Base](logarithmic-axis.md#logarithmic-base)
  - [Base 10 (Default)](logarithmic-axis.md#base-10-default)
  - [Base 2](logarithmic-axis.md#base-2)
  - [Natural Logarithm (Base e)](logarithmic-axis.md#natural-logarithm-base-e)
- [Range and Interval](logarithmic-axis.md#range-and-interval)
  - [Custom Range](logarithmic-axis.md#custom-range)
  - [Automatic Range](logarithmic-axis.md#automatic-range)
- [Label Formatting](logarithmic-axis.md#label-formatting)
  - [Standard Numeric Format](logarithmic-axis.md#standard-numeric-format)
  - [Scientific Notation](logarithmic-axis.md#scientific-notation)
  - [Custom Units](logarithmic-axis.md#custom-units)
- [Grid Lines](logarithmic-axis.md#grid-lines)
- [Complete Logarithmic Example](logarithmic-axis.md#complete-logarithmic-example)
- [Logarithmic vs Linear Comparison](logarithmic-axis.md#logarithmic-vs-linear-comparison)
- [Common Use Cases](logarithmic-axis.md#common-use-cases)
- [Common Issues](logarithmic-axis.md#common-issues)

## Basic Logarithmic Axis

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Logarithmic3D, Category3D } from '@syncfusion/ej2-react-charts';

function LogarithmicAxisChart() {
  const data = [
    { x: 'Product A', y: 10 },
    { x: 'Product B', y: 100 },
    { x: 'Product C', y: 1000 },
    { x: 'Product D', y: 10000 },
    { x: 'Product E', y: 100000 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{
        valueType: 'Category'
      }}
      primaryYAxis={{
        valueType: 'Logarithmic',
        title: 'Values (Log Scale)'
      }}
    >
      <Inject services={[ColumnSeries3D, Logarithmic3D, Category3D]} />
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

**Key requirement:** Must inject `Logarithmic3D` service and set `valueType: 'Logarithmic'`.

## When to Use Logarithmic Scale

**Use logarithmic axis when:**
- Data spans multiple orders of magnitude (1, 10, 100, 1000, etc.)
- Showing exponential growth or decay
- Comparing percentage changes rather than absolute differences
- Scientific data (pH, decibels, earthquake magnitude)
- Financial data with wide value ranges

**Example scenarios:**
- Population growth over centuries
- Stock prices over long periods
- Website traffic (10 to 10,000,000 visitors)
- Scientific measurements (0.001 to 10,000)

## Logarithmic Base

### Base 10 (Default)

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{ valueType: 'Category' }}
  primaryYAxis={{
    valueType: 'Logarithmic',
    logBase: 10  // Default, can be omitted
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Base 10 intervals:** 1, 10, 100, 1000, 10000, ...

### Base 2

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{ valueType: 'Category' }}
  primaryYAxis={{
    valueType: 'Logarithmic',
    logBase: 2,
    title: 'Values (Log₂)'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Base 2 intervals:** 1, 2, 4, 8, 16, 32, 64, 128, ...

**Use case:** Computer science (memory sizes, binary trees, algorithm complexity)

### Natural Logarithm (Base e)

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{ valueType: 'Category' }}
  primaryYAxis={{
    valueType: 'Logarithmic',
    logBase: Math.E,
    title: 'Values (ln)'
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Use case:** Natural sciences, continuous growth models

## Range and Interval

### Custom Range

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{ valueType: 'Category' }}
  primaryYAxis={{
    valueType: 'Logarithmic',
    minimum: 1,
    maximum: 100000,
    interval: 1  // Interval in logarithmic scale (powers)
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Note:** `interval: 1` with base 10 means labels at 10⁰, 10¹, 10², etc. (1, 10, 100, 1000)

### Automatic Range

Let chart calculate optimal range:

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{ valueType: 'Category' }}
  primaryYAxis={{
    valueType: 'Logarithmic'
    // Automatic min/max based on data
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Label Formatting

### Standard Numeric Format

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{ valueType: 'Category' }}
  primaryYAxis={{
    valueType: 'Logarithmic',
    labelFormat: 'n0'  // 1, 10, 100, 1,000, 10,000
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Scientific Notation

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{ valueType: 'Category' }}
  primaryYAxis={{
    valueType: 'Logarithmic',
    labelFormat: '{value}',
    // Will display as: 1e+0, 1e+1, 1e+2, etc.
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Custom Units

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{ valueType: 'Category' }}
  primaryYAxis={{
    valueType: 'Logarithmic',
    labelFormat: '{value} units',
    logBase: 10
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Grid Lines

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{ valueType: 'Category' }}
  primaryYAxis={{
    valueType: 'Logarithmic',
    majorGridLines: {
      width: 1,
      color: '#E0E0E0'
    },
    minorGridLines: {
      width: 1,
      color: '#F5F5F5'
    },
    minorTicksPerInterval: 8  // Minor ticks between logarithmic intervals
  }}
>
  {/* Series */}
</Chart3DComponent>
```

**Note:** Minor ticks in logarithmic scale appear at intermediate values (e.g., 2, 3, 4, ..., 9 between 1 and 10).

## Complete Logarithmic Example

```tsx
function ExponentialGrowth() {
  const growthData = [
    { year: '2000', users: 100 },
    { year: '2005', users: 1000 },
    { year: '2010', users: 10000 },
    { year: '2015', users: 100000 },
    { year: '2020', users: 1000000 },
    { year: '2023', users: 5000000 }
  ];

  return (
    <Chart3DComponent
      id='log-chart'
      title='User Growth (Logarithmic Scale)'
      primaryXAxis={{
        valueType: 'Category',
        title: 'Year'
      }}
      primaryYAxis={{
        valueType: 'Logarithmic',
        title: 'Number of Users (Log Scale)',
        logBase: 10,
        minimum: 10,
        maximum: 10000000,
        interval: 1,
        labelFormat: 'n0',
        majorGridLines: {
          width: 1,
          color: '#E0E0E0'
        },
        minorGridLines: {
          width: 1,
          color: '#F5F5F5'
        },
        minorTicksPerInterval: 8
      }}
      rotation={7}
      tilt={10}
    >
      <Inject services={[ColumnSeries3D, Logarithmic3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={growthData}
          xName='year'
          yName='users'
          type='Column'
          name='Users'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Logarithmic vs Linear Comparison

### Linear Scale (For Comparison)

```tsx
// Linear scale - hard to see small values
const data = [
  { x: 'A', y: 5 },
  { x: 'B', y: 50 },
  { x: 'C', y: 500 },
  { x: 'D', y: 5000 }
];

// Bars at 5, 50, 500 appear drastically different in height
// 5 is barely visible compared to 5000
```

### Logarithmic Scale (Better Visualization)

```tsx
<Chart3DComponent
  primaryYAxis={{ valueType: 'Logarithmic' }}
>
  {/* Same data, but all bars are more comparable */}
  {/* Shows relative differences and growth rates clearly */}
</Chart3DComponent>
```

**Key difference:** Logarithmic scale shows **rate of change** (percentage growth), linear scale shows **absolute change** (actual difference).

## Common Use Cases

### Scientific Data

```tsx
function PHLevels() {
  const phData = [
    { substance: 'Battery Acid', ph: 0.5 },
    { substance: 'Lemon Juice', ph: 2 },
    { substance: 'Coffee', ph: 5 },
    { substance: 'Water', ph: 7 },
    { substance: 'Baking Soda', ph: 9 },
    { substance: 'Bleach', ph: 12.5 }
  ];

  return (
    <Chart3DComponent
      id='ph-chart'
      title='pH Levels of Common Substances'
      primaryXAxis={{ valueType: 'Category' }}
      primaryYAxis={{
        valueType: 'Logarithmic',
        logBase: 10,
        title: 'pH (Logarithmic Scale)',
        minimum: 0.1,
        maximum: 14
      }}
    >
      <Inject services={[ColumnSeries3D, Logarithmic3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={phData}
          xName='substance'
          yName='ph'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

### Financial Data

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D, Logarithmic3D } from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import React, { useRef } from 'react';

function App() {
  const stockData = [
    { year: '2010', price: 10 },
    { year: '2015', price: 50 },
    { year: '2020', price: 250 },
    { year: '2023', price: 800 }
  ];

  return (
    <Chart3DComponent
      id='stock-chart'
      title='Stock Price Growth'
      primaryXAxis={{ valueType: 'Category' }}
      primaryYAxis={{
        valueType: 'Logarithmic',
        logBase: 10,
        title: 'Stock Price ($)',
        labelFormat: '${value}'
      }}
    >
      <Inject services={[ColumnSeries3D, Logarithmic3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={stockData}
          xName='year'
          yName='price'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById('charts'));
```

## Common Issues

**Negative or zero values:**
- Logarithmic scale cannot display zero or negative values
- Filter out or replace with small positive values (e.g., 0.1)
- Use linear scale if data includes zero/negative

**Chart appears compressed:**
- This is expected behavior showing proportional relationships
- Logarithmic scale emphasizes percentage changes, not absolute values

**Wrong intervals:**
- Adjust `interval` (in powers of the base)
- `interval: 1` with base 10 = 10⁰, 10¹, 10² (1, 10, 100)
- `interval: 2` with base 10 = 10⁰, 10², 10⁴ (1, 100, 10000)

**Service not found error:**
- Ensure `Logarithmic3D` is imported and injected
- Verify `valueType: 'Logarithmic'` is set correctly

---

See also: [api-reference.md](api-reference.md) | [usage-example.md](usage-example.md)
