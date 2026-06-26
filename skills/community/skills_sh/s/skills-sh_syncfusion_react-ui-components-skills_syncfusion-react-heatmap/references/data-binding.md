# Data Binding & Setup

## Table of Contents

- [Data Formats](#data-formats)
- [2D Array Binding](#2d-array-binding)
  - [Basic 2D Array](#basic-2d-array)
  - [2D Array with React Hooks](#2d-array-with-react-hooks)
- [JSON Data Binding](#json-data-binding)
  - [Basic JSON Format](#basic-json-format)
  - [JSON with Additional Properties](#json-with-additional-properties)
- [Dynamic Data Loading](#dynamic-data-loading)
  - [Fetching from API](#fetching-from-api)
  - [Real-time Data Updates](#real-time-data-updates)
- [Data Transformation](#data-transformation)
  - [Filtering Data](#filtering-data)
  - [Normalizing Values (0-100 scale)](#normalizing-values-0-100-scale)
  - [Grouping and Aggregating](#grouping-and-aggregating)
- [Working with Large Datasets](#working-with-large-datasets)
  - [Canvas Rendering Mode (for >1000 cells)](#canvas-rendering-mode-for-1000-cells)
  - [Limiting Visible Cells](#limiting-visible-cells)
  - [Pagination Pattern](#pagination-pattern)
- [Best Practices](#best-practices)

## Data Formats

The HeatMap component supports two primary data formats:

1. **2D Array** - Simple numeric arrays (recommended for simple data)
2. **JSON Array** - Object-based format with flexibility (recommended for labeled data)

## 2D Array Binding

### Basic 2D Array

The simplest format: a JavaScript array of arrays where each inner array represents a row.

```jsx
const data = [
  [10, 20, 30, 40],
  [50, 60, 70, 80],
  [90, 100, 110, 120]
];

<HeatMapComponent
  id='heatmap'
  dataSource={data}
  xAxis={{ labels: ['Jan', 'Feb', 'Mar', 'Apr'] }}
  yAxis={{ labels: ['North', 'South', 'East'] }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

**Characteristics:**
- 3 rows × 4 columns
- Values automatically colored based on range
- X-axis labels correspond to columns
- Y-axis labels correspond to rows

### 2D Array with React Hooks

```jsx
import { useState, useEffect } from 'react';

export function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Initialize data
    const initialData = [
      [73, 39, 26],
      [93, 58, 53],
      [54, 39, 26]
    ];
    setData(initialData);
  }, []);

  return (
    <HeatMapComponent id='heatmap' dataSource={data}>
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

## JSON Data Binding

### Basic JSON Format

For more structured data with explicit row/column identifiers:

```jsx
const data = [
  { 'row': 'North', 'column': 'Jan', 'value': 73 },
  { 'row': 'North', 'column': 'Feb', 'value': 39 },
  { 'row': 'North', 'column': 'Mar', 'value': 26 },
  { 'row': 'South', 'column': 'Jan', 'value': 93 },
  { 'row': 'South', 'column': 'Feb', 'value': 58 },
  { 'row': 'South', 'column': 'Mar', 'value': 53 }
];

<HeatMapComponent
    id='heatmap'
    dataSource={data}
    dataSourceSettings={{ xDataMapping: 'column', yDataMapping: 'row', valueMapping: 'value' }}
    xAxis={{ valueType: 'Category' }}
    yAxis={{ valueType: 'Category' }}
>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

**Benefits:**
- Self-documenting data structure
- Flexible data shapes (not limited to rectangular grids)
- Easy to filter, sort, or transform
- Better for sparse data

### JSON with Additional Properties

```jsx
const data = [
  { 
    row: 'Product A', 
    column: 'Q1', 
    value: 150,
    category: 'Electronics',
    status: 'growth'
  },
  { 
    row: 'Product B', 
    column: 'Q1', 
    value: 80,
    category: 'Electronics',
    status: 'stable'
  },
  // More records...
];

<HeatMapComponent
    id='heatmap'
    dataSource={data}
    dataSourceSettings={{ xDataMapping: 'column', yDataMapping: 'row', valueMapping: 'value' }}
    xAxis={{ valueType: 'Category' }}
    yAxis={{ valueType: 'Category' }}
    cellRender={(args) => {
        // Access custom properties
        const status = data.find(d =>
            d.row === args.row && d.column === args.column
        )?.status;

        if (status === 'growth') {
            args.displayText = '📈 ' + args.value;
        }
    }}
>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

## Dynamic Data Loading

### Fetching from API

```jsx
import { useState, useEffect } from 'react';
import { HeatMapComponent, Inject, Legend, Tooltip } from '@syncfusion/ej2-react-heatmap';

export function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data from API
    fetch('/api/heatmap-data')
      .then(response => response.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error loading data:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading heatmap...</div>;
  }

  return (
    <HeatMapComponent
      id='heatmap'
      dataSource={data}
      xAxis={{ type: 'Category' }}
      yAxis={{ type: 'Category' }}
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

### Real-time Data Updates

```jsx
import { useEffect, useRef } from 'react';

export function App() {
  const heatmapRef = useRef(null);

  useEffect(() => {
    // Simulate real-time updates every 5 seconds
    const interval = setInterval(() => {
      const newData = generateRandomData();
      
      if (heatmapRef.current) {
        heatmapRef.current.dataSource = newData;
      }
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  function generateRandomData() {
    const rows = 5;
    const cols = 5;
    const data = [];
    
    for (let i = 0; i < rows * cols; i++) {
      data.push(Math.floor(Math.random() * 100));
    }
    
    return data;
  }

  return (
    <HeatMapComponent
      ref={heatmapRef}
      id='heatmap'
      dataSource={generateRandomData()}
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

## Data Transformation

### Filtering Data

```jsx
// Only show high-value cells
const rawData = [
  { row: 'A', column: 'X', value: 150 },
  { row: 'A', column: 'Y', value: 50 },
  { row: 'B', column: 'X', value: 200 },
  { row: 'B', column: 'Y', value: 30 }
];

const filteredData = rawData.filter(d => d.value > 75);
// Result: [{ row: 'A', column: 'X', value: 150 }, { row: 'B', column: 'X', value: 200 }]

<HeatMapComponent id='heatmap' dataSource={filteredData} />
```

### Normalizing Values (0-100 scale)

```jsx
function normalizeData(data, min = 0, max = 100) {
  const values = data.map(d => d.value);
  const dataMin = Math.min(...values);
  const dataMax = Math.max(...values);
  const range = dataMax - dataMin;

  return data.map(d => ({
    ...d,
    value: ((d.value - dataMin) / range) * (max - min) + min
  }));
}

const data = [
  { row: 'A', column: 'X', value: 1000 },
  { row: 'A', column: 'Y', value: 5000 }
];

const normalized = normalizeData(data);
// Values now between 0-100 for consistent color scaling
```

### Grouping and Aggregating

```jsx
// Group by category and sum values
function aggregateData(data) {
  const grouped = {};

  data.forEach(item => {
    const key = `${item.row}-${item.column}`;
    if (!grouped[key]) {
      grouped[key] = { ...item };
    } else {
      grouped[key].value += item.value;
    }
  });

  return Object.values(grouped);
}

const rawData = [
  { row: 'Q1', column: 'Region A', value: 50 },
  { row: 'Q1', column: 'Region A', value: 30 },  // Duplicate
  { row: 'Q1', column: 'Region B', value: 75 }
];

const aggregated = aggregateData(rawData);
// Q1-Region A now has combined value: 80
```

## Working with Large Datasets

### Canvas Rendering Mode (for >1000 cells)

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={largeData}
  renderingMode='Canvas'  // Switch to Canvas for performance
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

**Why Canvas?**
- SVG creates DOM elements for each cell (slow with large data)
- Canvas renders to bitmap (efficient with large data)
- Automatic switching based on data size

### Limiting Visible Cells

```jsx
// Only display a subset of data
const allData = generateLargeDataset(); // 1000+ rows
const visibleData = allData.slice(0, 100); // Show first 100

<HeatMapComponent
  id='heatmap'
  dataSource={visibleData}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Pagination Pattern

```jsx
import { useState } from 'react';

export function PaginatedHeatmap() {
  const [page, setPage] = useState(0);
  const pageSize = 50;
  const allData = generateLargeDataset();
  
  const visibleData = allData.slice(
    page * pageSize,
    (page + 1) * pageSize
  );

  return (
    <div>
      <HeatMapComponent id='heatmap' dataSource={visibleData} />
      <button onClick={() => setPage(page + 1)}>Next Page</button>
      <button onClick={() => setPage(page - 1)} disabled={page === 0}>
        Previous Page
      </button>
    </div>
  );
}
```

## Best Practices

1. **Choose the right format:**
   - Use 2D arrays for simple, rectangular data
   - Use JSON for complex, labeled data

2. **Keep data clean:**
   - Validate values before binding
   - Handle missing/null values explicitly

3. **Performance considerations:**
   - Use Canvas rendering for >1000 cells
   - Implement pagination for very large datasets
   - Update data references (not mutations) for React reactivity

4. **Data updates:**
   - Always create new references when data changes
   - Avoid mutating data arrays directly
   - Use state management for complex data flows
