# Virtual Scrolling Reference - Syncfusion React Pivot Table

## Overview

Virtual scrolling is a performance optimization technique that renders only visible rows and columns instead of the entire dataset. This enables smooth scrolling and efficient memory usage even with datasets containing hundreds of thousands of rows. Virtual scrolling is essential for large-scale pivot tables where rendering all records at once would cause browser lag.

### Key Features
- **Efficient Rendering**: Only visible items rendered in DOM
- **Large Dataset Support**: Handle 100K+ rows smoothly
- **Smooth Scrolling**: No lag or jank during scroll operations
- **Memory Optimization**: Significant reduction in memory footprint
- **Automatic Pooling**: Virtual scroll pool managed automatically
- **Configuration Options**: Customize scroll behavior and performance

## Enabling Virtual Scrolling

### Basic Setup

To enable virtual scrolling, set `enableVirtualization` to **true** and provide a fixed height:

```typescript
import { PivotViewComponent, VirtualScroll, Inject } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { largeDataset } from './datasource';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: largeDataset as IDataSet[],  // 100K+ records
    rows: [{ name: 'Country' }, { name: 'City' }],
    columns: [{ name: 'Year' }],
    values: [{ name: 'Sales' }]
  };

  return (
    <PivotViewComponent
      id="PivotView"
      dataSourceSettings={dataSourceSettings}
      enableVirtualization={true}
      height={600}  // Fixed height required for virtual scrolling
      width="100%"
    >
      <Inject services={[VirtualScroll]} />
    </PivotViewComponent>
  );
}

export default App;
```

## Virtual Scrolling Configuration

### VirtualScroll Settings

```typescript
const virtualScrollSettings = {
  allowSinglePage: false, // Loads only single page on viewport which improves performance.
};

<PivotViewComponent
  enableVirtualization={true}
  virtualScrollSettings={virtualScrollSettings}
  height={600}
>
  <Inject services={[VirtualScroll]} />
</PivotViewComponent>
```

## Requirements for Virtual Scrolling

### Mandatory Properties

```typescript
<PivotViewComponent
  enableVirtualization={true}
  height={600}              // ✓ Required: Fixed pixel height
  width="100%"              // ✓ Optional: Width (percentage or pixels)
  dataSourceSettings={dataSourceSettings}
>
  <Inject services={[VirtualScroll]} />
</PivotViewComponent>
```

**Important:** Virtual scrolling requires explicit `height` in pixels. Without a fixed height, virtual scrolling will not work properly.

### Data Source Requirements

```typescript
// ✓ Works well with:
// - Large arrays (100K+)
// - Remote data with lazy loading
// - JSON data

// ✗ Limitations:
// - Requires predictable row heights
// - Best with uniform column widths
// - May not work with complex nested data
```

## Virtual Scrolling with Large Datasets

### Loading 100K+ Records

```typescript
function LargePivotTable() {
  // Generate 100,000+ records
  const generateLargeDataset = (count: number) => {
    const data = [];
    const countries = ['USA', 'Canada', 'Mexico', 'Brazil', 'Germany', 'UK', 'France', 'Japan'];
    const products = ['Laptops', 'Mobiles', 'Tablets', 'Accessories'];
    const quarters = ['Q1', 'Q2', 'Q3', 'Q4'];
    const years = [2020, 2021, 2022, 2023, 2024];

    for (let i = 0; i < count; i++) {
      data.push({
        Country: countries[Math.floor(Math.random() * countries.length)],
        Product: products[Math.floor(Math.random() * products.length)],
        Quarter: quarters[Math.floor(Math.random() * quarters.length)],
        Year: years[Math.floor(Math.random() * years.length)],
        Sales: Math.floor(Math.random() * 100000),
        Quantity: Math.floor(Math.random() * 1000)
      });
    }
    return data;
  };

  const largeDataset = React.useMemo(() => generateLargeDataset(100000), []);

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: largeDataset as IDataSet[],
    rows: [{ name: 'Country' }, { name: 'Product' }],
    columns: [{ name: 'Year' }, { name: 'Quarter' }],
    values: [
      { name: 'Sales', caption: 'Total Sales' },
      { name: 'Quantity', caption: 'Units Sold' }
    ]
  };

  return (
    <PivotViewComponent
      id="large-pivot"
      dataSourceSettings={dataSourceSettings}
      enableVirtualization={true}
      height={700}
      width="100%"
    >
      <Inject services={[VirtualScroll]} />
    </PivotViewComponent>
  );
}

export default LargePivotTable;
```

## Performance Optimization with Virtual Scrolling

### Combined with Data Compression

```typescript
function CompressedLargePivot() {
  const largeDataset = React.useMemo(() => generateDataset(1000000), []);

  return (
    <PivotViewComponent
      dataSourceSettings={{
        dataSource: largeDataset as IDataSet[],
        rows: [{ name: 'ProductID' }],
        columns: [{ name: 'Year' }],
        values: [{ name: 'Sales' }]
      }}
      // Data compression reduces unique values
      allowDataCompression={true}
      // Virtual scrolling renders efficiently
      enableVirtualization={true}
      height={600}
    >
      <Inject services={[VirtualScroll]} />
    </PivotViewComponent>
  );
}
```

## Practical Examples

### Example 1: High-Performance Dashboard

```typescript
function HighPerformanceDashboard() {
  const largeDataset = React.useMemo(
    () => generateSalesData(250000),
    []
  );

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: largeDataset as IDataSet[],
    rows: [{ name: 'Region' }, { name: 'Country' }],
    columns: [{ name: 'Year' }, { name: 'Quarter' }],
    values: [
      { name: 'Sales', caption: 'Total Sales', type: 'Sum', format: 'C2' },
      { name: 'Units', caption: 'Units Sold', type: 'Sum', format: 'N0' }
    ]
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1 style={{ marginBottom: '20px' }}>Sales Dashboard - Virtual Scrolling</h1>
      <PivotViewComponent
        id="performance-dashboard"
        dataSourceSettings={dataSourceSettings}
        enableVirtualization={true}
        showGroupingBar={true}
        showFieldList={true}
        height={700}
        width="100%"
      >
        <Inject services={[VirtualScroll, GroupingBar, FieldList]} />
      </PivotViewComponent>
    </div>
  );
}

export default HighPerformanceDashboard;
```

### Example 2: Real-Time Data with Virtual Scrolling

```typescript
function RealtimeVirtualPivot() {
  const [data, setData] = React.useState(() => generateInitialData(100000));

  React.useEffect(() => {
    // Simulate real-time data updates
    const interval = setInterval(() => {
      setData(prev => {
        // Update with new records or modify existing
        return [...prev.slice(1), generateNewRecord()];
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: data as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Year' }],
    values: [{ name: 'Sales' }]
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      enableVirtualization={true}
      height={600}
    >
      <Inject services={[VirtualScroll]} />
    </PivotViewComponent>
  );
}
```

## Troubleshooting

### Virtual Scrolling Not Working

**Issue:** Scrolling is not smooth or data appears frozen

**Solutions:**
- Verify `height` is set to a fixed pixel value
- Check that `enableVirtualization={true}`
- Ensure `VirtualScroll` module is injected
- Verify container has sufficient height

```typescript
// ✓ Correct
<PivotViewComponent
  enableVirtualization={true}
  height={600}  // Fixed pixels
/>

// ✗ Wrong - these won't work with virtual scrolling
<PivotViewComponent
  enableVirtualization={true}
  height="100%"  // Percentage won't trigger virtualization
/>
```

### Memory Still High with Large Datasets

**Issue:** Memory usage remains high despite virtual scrolling

**Solutions:**
- Combine with data compression: `allowDataCompression={true}`
- Implement paging: `enablePaging={true}`
- Use lazy loading for data
- Monitor with DevTools

### Scrolling Performance Issues

**Issue:** Scrolling is still laggy or jank visible

**Solutions:**
1. Reduce value field count
2. Simplify row/column hierarchies
3. Disable unnecessary UI features
4. Use consistent row heights
5. Check for large cell templates

```typescript
const optimizedSettings = {
  enableVirtualization: true,
  allowDataCompression: true,  // Add compression
  gridSettings: {
    rowHeight: 30,             // Fixed height
    columnWidth: 100           // Standard width
  },
  height: 600
};
```

## Best Practices

✅ **Do:**
- Use virtual scrolling for datasets > 10K rows
- Combine with paging for very large datasets (> 1M)
- Set fixed heights and widths
- Use data compression with virtualization
- Monitor performance with DevTools

❌ **Don't:**
- Use percentage heights with virtual scrolling
- Disable virtual scrolling for large datasets
- Use overly complex cell templates with virtualization
- Apply every aggregation type with large data
- Forget to handle responsive resizing

## Related Features

- **Paging**: Navigate large tables by pages
- **Data Compression**: Reduce unique values for faster processing
- **Performance Optimization**: Overall performance tuning guide
- **Lazy Loading**: Load data on-demand as user scrolls
- **Responsive Design**: Handle various screen sizes
