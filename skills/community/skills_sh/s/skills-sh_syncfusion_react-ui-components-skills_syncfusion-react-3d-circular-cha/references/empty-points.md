# Empty Points

This guide covers handling empty, null, or undefined data points in 3D Circular Charts, including different empty point modes and custom styling.

## Table of contents

- [Overview](empty-points.md#overview)
- [Understanding Empty Points](empty-points.md#understanding-empty-points)
  - [What Are Empty Points?](empty-points.md#what-are-empty-points)
- [Empty Point Modes](empty-points.md#empty-point-modes)
  - [Gap Mode](empty-points.md#gap-mode)
  - [Average Mode](empty-points.md#average-mode)
  - [Drop Mode](empty-points.md#drop-mode)
  - [Zero Mode](empty-points.md#zero-mode)
- [Mode Comparison](empty-points.md#mode-comparison)
- [Custom Fill Color for Empty Points](empty-points.md#custom-fill-color-for-empty-points)
- [Practical Examples](empty-points.md#practical-examples)
- [Mode Selection Guide](empty-points.md#mode-selection-guide)
- [Complete Configuration Example](empty-points.md#complete-configuration-example)
- [Summary](empty-points.md#summary)

## Overview

Empty points are data values that are `null`, `undefined`, or missing in your dataset. The 3D Circular Chart provides several strategies to handle these gaps in your data gracefully.

## Understanding Empty Points

### What Are Empty Points?

Empty points occur when:
- A data value is `null`
- A data value is `undefined`
- A data value is missing from the data object

```tsx
const dataWithEmptyPoints = [
  { category: 'A', value: 30 },      // Valid
  { category: 'B', value: null },    // Empty point
  { category: 'C', value: undefined },// Empty point
  { category: 'D', value: 25 },      // Valid
  { category: 'E' },                 // Empty point (no value property)
];
```

### Default Behavior

By default, empty points use **Gap** mode - they are ignored and not plotted.

## Empty Point Modes

Configure how empty points are handled using `emptyPointSettings.mode`:

### Available Modes

- **`Gap`** (default): Skip empty points, leaving gaps
- **`Average`**: Use average of neighboring values
- **`Drop`**: Remove empty points completely
- **`Zero`**: Treat empty points as zero value

## Gap Mode

The default mode. Empty points are ignored and not rendered.

```tsx
function GapModeExample() {
  const data = [
    { product: 'Product A', sales: 35 },
    { product: 'Product B', sales: null },    // Will be skipped
    { product: 'Product C', sales: 25 },
    { product: 'Product D', sales: undefined }, // Will be skipped
    { product: 'Product E', sales: 15 }
  ];

  return (
    <CircularChart3DComponent
      id="chart"
      title="Sales Data (Gap Mode)"
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="product"
          yName="sales"
          emptyPointSettings={{
            mode: 'Gap'  // Default behavior
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Result**: Chart shows only Products A, C, and E. Products B and D are not displayed.

**Use when**: You want to show that data is missing without substituting values.

## Average Mode

Empty points are filled with the average of their neighboring points.

```tsx
function AverageModeExample() {
  const data = [
    { month: 'Jan', revenue: 30 },
    { month: 'Feb', revenue: null },     // Will use average of Jan (30) and Mar (50) = 40
    { month: 'Mar', revenue: 50 },
    { month: 'Apr', revenue: undefined }, // Will use average of Mar (50) and May (40) = 45
    { month: 'May', revenue: 40 }
  ];

  return (
    <CircularChart3DComponent
      title="Monthly Revenue (Average Mode)"
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="month"
          yName="revenue"
          emptyPointSettings={{
            mode: 'Average'
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Calculation**:
- **Feb**: (30 + 50) / 2 = 40
- **Apr**: (50 + 40) / 2 = 45

**Use when**: Missing data should be interpolated from surrounding values.

## Drop Mode

Empty points are completely removed from the dataset.

```tsx
function DropModeExample() {
  const data = [
    { category: 'Category A', value: 35 },
    { category: 'Category B', value: null },    // Completely removed
    { category: 'Category C', value: 28 },
    { category: 'Category D', value: undefined }, // Completely removed
    { category: 'Category E', value: 22 }
  ];

  return (
    <CircularChart3DComponent
      title="Data Distribution (Drop Mode)"
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="value"
          emptyPointSettings={{
            mode: 'Drop'
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Result**: Only A, C, and E appear. B and D are removed entirely from the chart and legend.

**Use when**: Missing data points are irrelevant and should be hidden completely.

## Zero Mode

Empty points are treated as having a value of zero.

```tsx
function ZeroModeExample() {
  const data = [
    { quarter: 'Q1', profit: 45 },
    { quarter: 'Q2', profit: null },      // Treated as 0
    { quarter: 'Q3', profit: 38 },
    { quarter: 'Q4', profit: undefined }  // Treated as 0
  ];

  return (
    <CircularChart3DComponent
      title="Quarterly Profits (Zero Mode)"
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="quarter"
          yName="profit"
          emptyPointSettings={{
            mode: 'Zero'
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Result**: Q2 and Q4 appear as slices with value 0 (very small or invisible depending on other values).

**Use when**: Missing data should be interpreted as "no value" or "none".

## Mode Comparison

```tsx
function ModeComparison() {
  const data = [
    { item: 'A', value: 30 },
    { item: 'B', value: null },
    { item: 'C', value: 40 },
    { item: 'D', value: undefined },
    { item: 'E', value: 20 }
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
      <CircularChart3DComponent title="Gap Mode">
        <Inject services={[PieSeries3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="item"
            yName="value"
            emptyPointSettings={{ mode: 'Gap' }}
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>

      <CircularChart3DComponent title="Average Mode">
        <Inject services={[PieSeries3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="item"
            yName="value"
            emptyPointSettings={{ mode: 'Average' }}
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>

      <CircularChart3DComponent title="Drop Mode">
        <Inject services={[PieSeries3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="item"
            yName="value"
            emptyPointSettings={{ mode: 'Drop' }}
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>

      <CircularChart3DComponent title="Zero Mode">
        <Inject services={[PieSeries3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="item"
            yName="value"
            emptyPointSettings={{ mode: 'Zero' }}
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>
    </div>
  );
}
```

## Custom Fill Color for Empty Points

Style empty points with a custom color to make them visually distinct.

### Setting Custom Fill

```tsx
function CustomColorEmpty() {
  const data = [
    { category: 'A', value: 35 },
    { category: 'B', value: null },    // Will be gray
    { category: 'C', value: 28 },
    { category: 'D', value: undefined }, // Will be gray
    { category: 'E', value: 22 }
  ];

  return (
    <CircularChart3DComponent
      title="Sales Distribution"
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="category"
          yName="value"
          emptyPointSettings={{
            mode: 'Zero',
            fill: '#CCCCCC'  // Gray color for empty points
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Note**: Fill color only applies when empty points are rendered (Zero or Average modes).

### Color with Average Mode

```tsx
function AverageWithColor() {
  const data = [
    { month: 'Jan', sales: 30 },
    { month: 'Feb', sales: null },
    { month: 'Mar', sales: 50 },
    { month: 'Apr', sales: undefined },
    { month: 'May', sales: 40 }
  ];

  return (
    <CircularChart3DComponent
      title="Monthly Sales (Estimated)"
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={data}
          xName="month"
          yName="sales"
          emptyPointSettings={{
            mode: 'Average',
            fill: '#FFE082'  // Light orange for estimated values
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

**Use case**: Distinguish interpolated/estimated values from actual data.

## Practical Examples

### Handling API Data with Gaps

```tsx
function APIDataWithGaps() {
  const [chartData, setChartData] = React.useState([]);

  React.useEffect(() => {
    // Simulate API call that returns incomplete data
    const apiData = [
      { region: 'North', revenue: 45000 },
      { region: 'South', revenue: null },      // Missing
      { region: 'East', revenue: 52000 },
      { region: 'West', revenue: undefined },  // Missing
      { region: 'Central', revenue: 38000 }
    ];
    setChartData(apiData);
  }, []);

  return (
    <CircularChart3DComponent
      title="Regional Revenue"
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={chartData}
          xName="region"
          yName="revenue"
          emptyPointSettings={{
            mode: 'Average',
            fill: '#B0BEC5'  // Gray for estimated regions
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Survey Data with Non-Responses

```tsx
function SurveyData() {
  const surveyResults = [
    { option: 'Very Satisfied', count: 45 },
    { option: 'Satisfied', count: 32 },
    { option: 'Neutral', count: null },      // No responses
    { option: 'Dissatisfied', count: 8 },
    { option: 'Very Dissatisfied', count: 5 }
  ];

  return (
    <CircularChart3DComponent
      title="Customer Satisfaction Survey"
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={surveyResults}
          xName="option"
          yName="count"
          emptyPointSettings={{
            mode: 'Zero',
            fill: '#E0E0E0'  // Show as "no data"
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

### Time Series with Missing Periods

```tsx
function TimeSeriesMissing() {
  const monthlyData = [
    { month: 'Jan', orders: 120 },
    { month: 'Feb', orders: 135 },
    { month: 'Mar', orders: null },       // System downtime
    { month: 'Apr', orders: undefined },  // System downtime
    { month: 'May', orders: 165 }
  ];

  return (
    <CircularChart3DComponent
      title="Monthly Orders"
    >
      <Inject services={[PieSeries3D]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={monthlyData}
          xName="month"
          yName="orders"
          emptyPointSettings={{
            mode: 'Gap'  // Show missing data explicitly
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Mode Selection Guide

### When to Use Each Mode

**Gap Mode**:
- ✅ Data is genuinely missing and shouldn't be estimated
- ✅ You want to highlight data gaps visually
- ✅ Interpolation would be misleading

**Average Mode**:
- ✅ Missing values should be estimated
- ✅ Data follows a trend
- ✅ Gaps are temporary/accidental

**Drop Mode**:
- ✅ Missing data points are irrelevant
- ✅ You want a clean chart without gaps
- ✅ Empty points don't need to be acknowledged

**Zero Mode**:
- ✅ Missing data means "no activity"
- ✅ Zero is a meaningful value
- ✅ You want to show all categories

## Complete Configuration Example

```tsx
function CompleteEmptyPointHandling() {
  const productData = [
    { product: 'Laptops', q1: 45, q2: 52, q3: null, q4: 48 },
    { product: 'Phones', q1: 38, q2: null, q3: 42, q4: 45 },
    { product: 'Tablets', q1: 28, q2: 30, q3: 32, q4: undefined }
  ];

  // Use Q1 data for example
  const chartData = productData.map(p => ({
    product: p.product,
    sales: p.q1
  }));

  return (
    <CircularChart3DComponent
      title="Product Sales - Q1"
      width="600px"
      height="450px"
      legendSettings={{ visible: true }}
      tooltip={{ enable: true, format: '${point.x}: ${point.y} units' }}
    >
      <Inject services={[
        PieSeries3D,
        CircularChartLegend3D,
        CircularChartTooltip3D
      ]} />
      <CircularChart3DSeriesCollectionDirective>
        <CircularChart3DSeriesDirective
          dataSource={chartData}
          xName="product"
          yName="sales"
          emptyPointSettings={{
            mode: 'Average',
            fill: '#FFB74D'  // Orange for estimated data
          }}
        />
      </CircularChart3DSeriesCollectionDirective>
    </CircularChart3DComponent>
  );
}
```

## Summary

You've learned how to:
- ✅ Understand what empty points are (null, undefined, missing)
- ✅ Use Gap mode to skip empty points
- ✅ Use Average mode to interpolate missing values
- ✅ Use Drop mode to remove empty points entirely
- ✅ Use Zero mode to treat empty points as zero
- ✅ Apply custom colors to empty points
- ✅ Choose appropriate modes for different scenarios

**Best Practices:**
- **Gap**: Use when data gaps are significant
- **Average**: Use for smooth trend lines
- **Drop**: Use for clean, simplified charts
- **Zero**: Use when absence means zero
- Always document which mode you're using
- Style empty points differently to show they're estimated