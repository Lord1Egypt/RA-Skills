# Working with Data in 3D Charts

## Table of Contents
- [Data Source Formats](#data-source-formats)
- [Data Binding Approaches](#data-binding-approaches)
- [Dynamic Data Updates](#dynamic-data-updates)
- [Empty Data Points](#empty-data-points)
- [Data Formatting](#data-formatting)
- [Performance Optimization](#performance-optimization)

This guide covers data binding patterns, dynamic updates, and data handling best practices for 3D charts.

## Data Source Formats

### Array of Objects (Recommended)

The most common and flexible format:

```tsx
const salesData = [
  { month: 'Jan', sales: 30000, expenses: 18000 },
  { month: 'Feb', sales: 35000, expenses: 20000 },
  { month: 'Mar', sales: 32000, expenses: 19000 },
  { month: 'Apr', sales: 38000, expenses: 21000 }
];

<Chart3DSeriesDirective
  dataSource={salesData}
  xName='month'
  yName='sales'
  type='Column'
/>
```

**Advantages:**
- Clear property-to-axis mapping
- Easy to maintain and read
- TypeScript-friendly
- Supports multiple series from same data

### Array of Arrays

Less common, but valid:

```tsx
const data = [
  ['Product A', 45, 30],
  ['Product B', 38, 25],
  ['Product C', 52, 35]
];

// Access by index
<Chart3DSeriesDirective
  dataSource={data}
  xName='0'
  yName='1'
  type='Column'
/>
```

**Use when:** Data comes from CSV parsing or external sources in array format.

## Data Binding Approaches

### Single Series Binding

```tsx
function SingleSeriesChart() {
  const data = [
    { category: 'Q1', value: 120 },
    { category: 'Q2', value: 145 },
    { category: 'Q3', value: 132 },
    { category: 'Q4', value: 158 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='category'
          yName='value'
          type='Column'
          name='Quarterly Revenue'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

### Multiple Series from Single Data Source

```tsx
function MultiSeriesChart() {
  const data = [
    { quarter: 'Q1', actual: 120, target: 110, forecast: 115 },
    { quarter: 'Q2', actual: 145, target: 135, forecast: 140 },
    { quarter: 'Q3', actual: 132, target: 140, forecast: 138 },
    { quarter: 'Q4', actual: 158, target: 150, forecast: 155 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
    >
      <Inject services={[ColumnSeries3D, Category3D, Legend3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='quarter'
          yName='actual'
          type='Column'
          name='Actual'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='quarter'
          yName='target'
          type='Column'
          name='Target'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='quarter'
          yName='forecast'
          type='Column'
          name='Forecast'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

### Separate Data Sources per Series

```tsx
function SeparateDataSources() {
  const salesData = [
    { month: 'Jan', value: 30 },
    { month: 'Feb', value: 35 },
    { month: 'Mar', value: 32 }
  ];

  const expenseData = [
    { month: 'Jan', value: 18 },
    { month: 'Feb', value: 20 },
    { month: 'Mar', value: 19 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
    >
      <Inject services={[ColumnSeries3D, Category3D, Legend3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={salesData}
          xName='month'
          yName='value'
          type='Column'
          name='Sales'
        />
        <Chart3DSeriesDirective
          dataSource={expenseData}
          xName='month'
          yName='value'
          type='Column'
          name='Expenses'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Dynamic Data Updates

### Updating Data with State

```tsx
import { useState, useEffect } from 'react';
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D } from '@syncfusion/ej2-react-charts';

function DynamicChart() {
  const [chartData, setChartData] = useState([
    { x: 'A', y: 10 },
    { x: 'B', y: 20 },
    { x: 'C', y: 15 }
  ]);

  const updateData = () => {
    const newData = chartData.map(item => ({
      ...item,
      y: Math.floor(Math.random() * 50) + 10
    }));
    setChartData(newData);
  };

  return (
    <div>
      <button onClick={updateData}>Update Data</button>
      <Chart3DComponent
        id='dynamic-chart'
        primaryXAxis={{ valueType: 'Category' }}
      >
        <Inject services={[ColumnSeries3D, Category3D]} />
        <Chart3DSeriesCollectionDirective>
          <Chart3DSeriesDirective
            dataSource={chartData}
            xName='x'
            yName='y'
            type='Column'
          />
        </Chart3DSeriesCollectionDirective>
      </Chart3DComponent>
    </div>
  );
}
```

### Real-Time Data Updates

```tsx
function RealTimeChart() {
  const [data, setData] = useState([
    { time: '10:00', value: 25 },
    { time: '10:05', value: 30 },
    { time: '10:10', value: 28 }
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setData(prevData => {
        const newPoint = {
          time: new Date().toLocaleTimeString(),
          value: Math.floor(Math.random() * 40) + 20
        };
        
        // Keep last 10 points
        return [...prevData.slice(-9), newPoint];
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <Chart3DComponent
      id='realtime-chart'
      primaryXAxis={{ valueType: 'Category' }}
      title='Real-Time Monitoring'
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='time'
          yName='value'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

### Fetching Data from API

```tsx
function ApiDataChart() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/sales-data')
      .then(res => res.json())
      .then(apiData => {
        setData(apiData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading chart...</div>;

  return (
    <Chart3DComponent
      id='api-chart'
      primaryXAxis={{ valueType: 'Category' }}
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='category'
          yName='value'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Empty Data Points

Handle null, undefined, or missing data:

```tsx
const dataWithGaps = [
  { month: 'Jan', sales: 30 },
  { month: 'Feb', sales: null },  // Empty point
  { month: 'Mar', sales: 35 },
  { month: 'Apr', sales: undefined },  // Empty point
  { month: 'May', sales: 40 }
];

<Chart3DSeriesDirective
  dataSource={dataWithGaps}
  xName='month'
  yName='sales'
  type='Column'
  emptyPointSettings={{
    mode: 'Zero'  // Options: 'Zero', 'Gap', 'Average', 'Drop'
  }}
/>
```

**Empty point modes:**
- `Zero`: Show as zero value
- `Gap`: Leave empty space
- `Average`: Fill with average of neighbors
- `Drop`: Remove from series

## Data Formatting

### Format Axis Labels

```tsx
<Chart3DComponent
  id='chart'
  primaryXAxis={{ valueType: 'Category' }}
  primaryYAxis={{
    labelFormat: '${value}K',  // Format as currency
    // OR
    // labelFormat: '{value}%',  // Format as percentage
    // OR
    // labelFormat: 'n2'  // Numeric with 2 decimals
  }}
>
  {/* Series */}
</Chart3DComponent>
```

### Custom Label Formatting

```tsx
<Chart3DComponent
  id='chart'
  primaryYAxis={{
    labelFormat: '{value}',
    labelStyle: { size: '12px' }
  }}
  axisLabelRender={(args) => {
    // Custom formatting logic
    args.text = '$' + (args.value / 1000).toFixed(1) + 'K';
  }}
>
  {/* Series */}
</Chart3DComponent>
```

## Performance Optimization

### Large Datasets

For datasets with 100+ points:

```tsx
function LargeDataChart() {
  const data = generateLargeDataset(500);  // 500 points

  return (
    <Chart3DComponent
      id='large-chart'
      primaryXAxis={{ valueType: 'Category' }}
      enableAnimation={false}  // Disable for better performance
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
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

function generateLargeDataset(count) {
  return Array.from({ length: count }, (_, i) => ({
    x: `Item${i}`,
    y: Math.floor(Math.random() * 100)
  }));
}
```

**Optimization tips:**
- Disable animations for >200 points
- Use memoization for data transformations
- Implement pagination or data windowing
- Consider data aggregation for very large datasets

### Memoizing Data

```tsx
import { useMemo } from 'react';

function OptimizedChart({ rawData }) {
  const processedData = useMemo(() => {
    return rawData.map(item => ({
      category: item.name,
      value: item.amount * 1000
    }));
  }, [rawData]);

  return (
    <Chart3DComponent id='chart' primaryXAxis={{ valueType: 'Category' }}>
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={processedData}
          xName='category'
          yName='value'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Common Data Issues

**Issue: Chart shows no data**
- Verify `xName` and `yName` match property names exactly (case-sensitive)
- Check dataSource is not empty, null, or undefined
- Ensure numeric values are numbers, not strings

**Issue: Categories not appearing**
- Set `primaryXAxis.valueType = 'Category'` for string categories
- Verify `xName` points to string property

**Issue: Data updates not reflecting**
- Create new array reference: `setData([...newData])` instead of mutating
- Ensure state is properly updated before re-render

---

See also: [api-reference.md](api-reference.md) | [usage-example.md](usage-example.md)
