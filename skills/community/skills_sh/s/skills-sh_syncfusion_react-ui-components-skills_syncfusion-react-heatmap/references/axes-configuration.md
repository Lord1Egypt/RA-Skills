# Axes Configuration

## Table of Contents

- [Axis Types](#axis-types)
- [Numerical Axis](#numerical-axis)
  - [Basic Numerical Axis](#basic-numerical-axis)
  - [Numerical Axis with Custom Intervals](#numerical-axis-with-custom-intervals)
  - [Use Case: Temperature Range](#use-case-temperature-range)
- [Categorical Axis](#categorical-axis)
  - [Basic Categorical Axis](#basic-categorical-axis)
  - [Categorical Axis with JSON Data](#categorical-axis-with-json-data)
  - [Use Case: Sales by Product and Month](#use-case-sales-by-product-and-month)
- [DateTime Axis](#datetime-axis)
  - [Basic DateTime Axis](#basic-datetime-axis)
  - [DateTime with Hourly Data](#datetime-with-hourly-data)
  - [DateTime Format Options](#datetime-format-options)
- [Axis Properties](#axis-properties)
  - [Common Axis Properties](#common-axis-properties)
- [Advanced Positioning](#advanced-positioning)
  - [Inverted Axes](#inverted-axes)
  - [Opposed Position](#opposed-position)
  - [Rotated Labels](#rotated-labels)
- [Labels and Formatting](#labels-and-formatting)
  - [Custom Label Styling](#custom-label-styling)
- [Common Axis Configuration Patterns](#common-axis-configuration-patterns)
  - [Pattern 1: Time Series with Monthly Data](#pattern-1-time-series-with-monthly-data)
  - [Pattern 2: Performance Matrix with Inversed Y-Axis](#pattern-2-performance-matrix-with-inversed-y-axis)
  - [Pattern 3: Multi-Dimensional Data with Numeric Range](#pattern-3-multi-dimensional-data-with-numeric-range)

## Axis Types

HeatMap supports three axis types, each suited for different data scenarios:

| Axis Type | Use Case | Example |
|-----------|----------|---------|
| **Numerical** | Continuous numeric ranges | Temperature (0-100), Score (0-1000) |
| **Categorical** | Discrete labels/categories | Months, Regions, Products |
| **DateTime** | Time-based data | Dates, Hours, Timestamps |

## Numerical Axis

### Basic Numerical Axis

```jsx
<HeatMapComponent id='heatmap'
  xAxis={{
    valueType: 'Numeric',
    minimum: 0,
    maximum: 100,
  }}
  yAxis ={{
    valueType: 'Numeric',
    minimum: 0,
    maximum: 100,
  }}>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Numerical Axis with Custom Intervals

```jsx
<HeatMapComponent id='heatmap' dataSource={data}
xAxis={{
    valueType: 'Numeric',
    minimum: 0,
    maximum: 100,
    interval: 10,  // Label every 10 units
    labels: ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100']
}}
yAxis={{
    valueType: 'Numeric',
    minimum: 0,
    maximum: 50,
    interval: 5,
}}>>
<Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Use Case: Temperature Range

```jsx
// Temperature data from 0°C to 40°C
const temperatureData = [
  [5, 15, 25, 35],
  [8, 18, 28, 38],
  [10, 20, 30, 40]
];

<HeatMapComponent
  id='heatmap'
  dataSource={temperatureData}
  xAxis={{
      valueType: 'Numeric',
      minimum: 0,
      maximum: 40,
      interval: 10,
      title: { text: 'Temperature (°C)' }
  }}
  yAxis={{
      valueType: 'Numeric',
      minimum: 0,
      maximum: 3,
      title: { text: 'Time Period' }
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

## Categorical Axis

### Basic Categorical Axis

Categorical axes use explicit labels for each row/column:

```jsx
const data = [
  [73, 39, 26, 39],
  [93, 58, 53, 38],
  [54, 39, 26, 40]
];

<HeatMapComponent 
  id='heatmap' 
  dataSource={data}
  xAxis={{
    valueType: 'Category',
    labels: ['Q1', 'Q2', 'Q3', 'Q4']
  }}
  yAxis={{
    valueType: 'Category',
    labels: ['North Region', 'South Region', 'East Region']
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Categorical Axis with JSON Data

```jsx
const data = [
  { row: 'Product A', column: 'Jan', value: 150 },
  { row: 'Product A', column: 'Feb', value: 120 },
  { row: 'Product A', column: 'Mar', value: 180 },
  { row: 'Product B', column: 'Jan', value: 200 },
  { row: 'Product B', column: 'Feb', value: 190 },
  { row: 'Product B', column: 'Mar', value: 220 }
];

<HeatMapComponent
    id='heatmap'
    dataSource={data}

    xAxis={{
        valueType: 'Category'
    }}
    yAxis={{
        valueType: 'Category',
    }}
    dataSourceSettings={{ xDataMapping: 'column', yDataMapping: 'row', valueMapping: 'value' }}
>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

**Benefits:**
- Automatically extracts unique labels from data
- Maintains correspondence with data rows/columns
- No manual label management

### Use Case: Sales by Product and Month

```jsx
const salesData = [
  { row: 'Laptop', column: 'January', value: 450 },
  { row: 'Laptop', column: 'February', value: 520 },
  { row: 'Laptop', column: 'March', value: 480 },
  { row: 'Monitor', column: 'January', value: 320 },
  { row: 'Monitor', column: 'February', value: 380 },
  { row: 'Monitor', column: 'March', value: 410 },
  { row: 'Keyboard', column: 'January', value: 280 },
  { row: 'Keyboard', column: 'February', value: 300 },
  { row: 'Keyboard', column: 'March', value: 350 }
];

<HeatMapComponent
    id='heatmap'
    dataSource={salesData}
    dataSourceSettings={{ xDataMapping: 'column', yDataMapping: 'row', valueMapping: 'value' }}
    xAxis={{
        valueType: 'Category'
    }}
    yAxis={{
        valueType: 'Category'
    }}
    title={{ text: 'Monthly Sales by Product' }}
>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

## DateTime Axis

### Basic DateTime Axis

```jsx
const datetimeData = [
  { 
    row: 'Server 1', 
    column: new Date(2024, 0, 1), 
    value: 75 
  },
  { 
    row: 'Server 1', 
    column: new Date(2024, 0, 2), 
    value: 82 
  },
  // More data...
];

<HeatMapComponent
  id='heatmap'
  dataSource={datetimeData}
  dataSourceSettings={{xDataMapping: 'column', yDataMapping: 'row', valueMapping: 'value'}}
  xAxis={{
    valueType: 'DateTime',
    labelFormat: 'M/d'  // MM/dd format
  }}
  yAxis={{
    valueType: 'Category'
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### DateTime with Hourly Data

```jsx
const hourlyData = [];
const startDate = new Date(2024, 0, 1);

for (let hour = 0; hour < 24; hour++) {
  const date = new Date(startDate);
  date.setHours(hour);
  
  hourlyData.push({
    row: 'CPU Usage',
    column: date,
    value: Math.floor(Math.random() * 100)
  });
}

<HeatMapComponent
    id='heatmap'
    dataSource={hourlyData}
    dataSourceSettings={{ xDataMapping: 'column', yDataMapping: 'row', valueMapping: 'value' }}
    xAxis={{
        valueType: 'DateTime',
        labelFormat: 'h:mm tt'  // 12-hour format with AM/PM
    }}
    yAxis={{
        valueType: 'Category'
    }}
>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### DateTime Format Options

```jsx
// Common DateTime label formats:
labelFormat: 'M/d'           // 1/1, 1/2, etc.
labelFormat: 'M/d/y'         // 1/1/24
labelFormat: 'MMM'           // Jan, Feb, Mar
labelFormat: 'MMMM'          // January, February
labelFormat: 'ddd'           // Mon, Tue, Wed
labelFormat: 'dddd'          // Monday, Tuesday
labelFormat: 'h:mm tt'       // 1:30 PM
labelFormat: 'HH:mm'         // 13:30 (24-hour)
labelFormat: 'M/d h:mm tt'   // 1/1 1:30 PM
```

## Axis Properties

### Common Axis Properties

```jsx
<HeatMapComponent id='heatmap' dataSource={data}
    xAxis={{
        valueType: 'Category',
        labels: ['A', 'B', 'C'],
        // Title and labels
        title: {
            text: 'Column Headers',
            textStyle: { size: '14px' }
        },
        // Appearance
        labelRotation: 45,       // Rotate labels
        isInversed: false,         // Reverse order?
        opposedPosition: false,    // Position opposite side?
        // Intervals
        labelIntersectAction: 'Rotate45'  // 'Hide' or 'Rotate'
    }}>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

## Advanced Positioning

### Inverted Axes

Reverse the order of axis labels:

```jsx
<HeatMapComponent id='heatmap' dataSource={data}
    xAxis={{
        valueType: 'Category',
        labels: ['A', 'B', 'C', 'D'],
        isInversed: true  // Labels now: D, C, B, A
    }}>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Opposed Position

Place axis on opposite side (right for X, top for Y):

```jsx
<HeatMapComponent id='heatmap' dataSource={data}
    xAxis={{
        opposedPosition: true,  // X-axis at top
        valueType: 'Category',
        labels: ['Q1', 'Q2', 'Q3', 'Q4']
    }}

    yAxis={{
        opposedPosition: true,  // Y-axis at right
        valueType: 'Category',
        labels: ['North', 'South', 'East', 'West']
    }}>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Rotated Labels

```jsx
<HeatMapComponent id='heatmap' dataSource={data}
    xAxis={{
        labelRotation: 45,  // Rotate 45 degrees
        labels: ['Very Long Column Header 1', 'Very Long Column Header 2']
    }}>
</HeatMapComponent>
```

## Labels and Formatting

### Custom Label Styling

```jsx
<HeatMapComponent id='heatmap' dataSource={data}
    xAxis={{
        labels: ['Jan', 'Feb', 'Mar', 'Apr'],
        textStyle: {
            size: '12px',
            color: '#333',
            fontWeight: 'bold'
        },
        title: {
            text: 'Months',
            textStyle: {
                size: '14px',
                color: '#666'
            }
        }
    }}
>
</HeatMapComponent>
```

## Common Axis Configuration Patterns

### Pattern 1: Time Series with Monthly Data

```jsx
const monthlyData = generateMonthlyData();

<HeatMapComponent
    id='heatmap'
    dataSource={monthlyData}
    dataSourceSettings={{ xDataMapping: 'month', yDataMapping: 'metric', valueMapping: 'Category' }}
    xAxis={{
        valueType: 'DateTime',
        labelFormat: 'MMM yyyy'
    }}
    yAxis={{
        valueType: 'Category'
    }}
>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Pattern 2: Performance Matrix with Inversed Y-Axis

```jsx
// High performance at top, low at bottom
<HeatMapComponent
  id='heatmap'
  dataSource={performanceData}
  xAxis={{
    valueType: 'Category',
    labels: ['CPU', 'Memory', 'Disk', 'Network'],
    title: { text: 'System Resources' }
  }}
  yAxis={{
    valueType: 'Category',
    labels: ['Server 1', 'Server 2', 'Server 3'],
    isInversed:  true,,  // Reverse to show best at top
    title: { text: 'Servers' }
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Pattern 3: Multi-Dimensional Data with Numeric Range

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  xAxis={{
    valueType: 'Numeric',
    minimum: 0,
    maximum: 100,
    interval: 20
  }}
  yAxis={{
    valueType: 'Category',
    labels: generateLabels()
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```
