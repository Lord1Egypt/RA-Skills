# Series and Data Binding

## Data Binding Fundamentals

Data binding maps your JavaScript objects to chart visualization. Each series represents one dataset and uses `xName` and `yName` to specify which object properties map to axes.

### Basic Data Structure

```jsx
const data = [
  { month: 'Jan', revenue: 35000, profit: 8000 },
  { month: 'Feb', revenue: 28000, profit: 6500 },
  { month: 'Mar', revenue: 34000, profit: 7200 }
];

<SeriesDirective
  dataSource={data}
  xName='month'    // property used for X-axis
  yName='revenue'  // property used for Y-axis
  type='Column'
/>
```

**Key concepts:**
- `dataSource`: Array of objects containing your data
- `xName`: Property name for X-axis (must exist in every object)
- `yName`: Property name for Y-axis (must exist in every object)
- Property names are **case-sensitive**

### Multiple Series from Same Data

Use the same `dataSource` array for multiple series, just map different `yName` properties:

```jsx
<SeriesCollectionDirective>
  <SeriesDirective
    dataSource={data}
    xName='month'
    yName='revenue'
    name='Revenue'
    type='Column'
  />
  <SeriesDirective
    dataSource={data}
    xName='month'
    yName='profit'
    name='Profit'
    type='Line'
  />
</SeriesCollectionDirective>
```

---

## Series Configuration

### Basic Series Properties

```jsx
<SeriesDirective
  dataSource={data}
  xName='x'
  yName='y'
  name='My Series'
  type='Column'
  fill='#3B82F6'
  opacity={0.85}
  width={2}
  marker={{
    visible: true,
    shape: 'Circle',
    width: 8,
    height: 8
  }}
/>
```

**Common properties:**
- `name`: Series name (appears in legend)
- `fill`: Series color
- `opacity`: Transparency (0-1)
- `width`: Line width or marker size
- `marker`: Point markers (see below)
- `border`: Border styling
- `yAxisName`: For secondary axis series

### Marker Configuration

Markers are visual indicators at data points (dots, squares, triangles, etc.).

```jsx
<SeriesDirective
  marker={{
    visible: true,
    shape: 'Circle', // or 'Square', 'Diamond', 'Triangle', 'Pentagon', 'Cross', 'Plus'
    width: 10,
    height: 10,
    fill: '#FF5722',
    border: {
      width: 2,
      color: '#fff'
    }
  }}
  type='Line'
/>
```

**When to use markers:**
- Line charts with few data points
- Scatter plots for emphasis
- When exact point values matter

**Don't use for:**
- Large datasets (>100 points)
- Dense line charts (hard to read)

### Data Labels

Display values directly on the chart. Data labels must be configured inside the `marker` property using the `dataLabel` key. Inject the `DataLabel` service to enable this feature.

```jsx
import { LineSeries, Category, DataLabel, } from '@syncfusion/ej2-react-charts';

<ChartComponent>
  <Inject services={[LineSeries, Category, DataLabel]} />
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={data}
      xName='month'
      yName='sales'
      type='Line'
      marker={{
        dataLabel: {
          visible: true,
          position: 'Top' // or 'Bottom', 'Middle', 'Outer'
        }
      }}
    />
  </SeriesCollectionDirective>
</ChartComponent>
```

**Position options:**
- `Top`, `Bottom`, `Left`, `Right`: Around the point
- `Middle`: Inside the point
- `Outer`: Outside the point (for area/line series)

---

## Dynamic Data Updates

### addPoint — Add a Single Data Point

Use `addPoint` on a series instance (accessed via chart ref) to append a data point with optional animation. This is more efficient than replacing the entire `dataSource` for live data feeds.

```jsx
import React, { useRef } from 'react';
import { ChartComponent, SeriesCollectionDirective, SeriesDirective, Inject, LineSeries, Category } from '@syncfusion/ej2-react-charts';

export default function AddPointExample() {
  const chartRef = useRef(null);

  const handleAddPoint = () => {
    // addPoint(dataPoint, animationDuration?)
    chartRef.current.series[0].addPoint({ month: 'Jun', value: 45 });
  };

  return (
    <>
      <button onClick={handleAddPoint}>Add Point</button>
      <ChartComponent ref={chartRef} id='charts' primaryXAxis={{ valueType: 'Category' }}>
        <Inject services={[LineSeries, Category]} />
        <SeriesCollectionDirective>
          <SeriesDirective
            dataSource={[
              { month: 'Jan', value: 35 },
              { month: 'Feb', value: 28 },
              { month: 'Mar', value: 34 }
            ]}
            xName='month' yName='value' type='Line'
          />
        </SeriesCollectionDirective>
      </ChartComponent>
    </>
  );
}
```

### removePoint — Remove a Data Point by Index

Use `removePoint` to delete a specific data point at the given index with optional animation.

```jsx
const handleRemovePoint = () => {
  // removePoint(index, animationDuration?)
  chartRef.current.series[0].removePoint(0); // removes the first point
};
```

### setData — Replace All Series Data

Use `setData` to swap the entire data source for a series in one call, with optional animation. This is preferred over reassigning `dataSource` via state when you need animation control.

```jsx
const newData = [
  { month: 'Apr', value: 50 },
  { month: 'May', value: 60 },
  { month: 'Jun', value: 55 }
];

const handleSetData = () => {
  // setData(dataArray, animationDuration?)
  chartRef.current.series[0].setData(newData, 500);
};
```

### React State — Full Re-render Approach

Use React state for simpler scenarios where animation is not a priority:

```jsx
import React, { useState } from 'react';

export default function DynamicChart() {
  const [data, setData] = useState([
    { month: 'Jan', value: 35 },
    { month: 'Feb', value: 28 }
  ]);

  const addDataPoint = () => {
    setData(prev => [...prev, { month: 'Mar', value: 40 }]);
  };

  return (
    <>
      <button onClick={addDataPoint}>Add Data</button>
      <ChartComponent id='charts' primaryXAxis={{ valueType: 'Category' }}>
        <Inject services={[LineSeries, Category]} />
        <SeriesCollectionDirective>
          <SeriesDirective dataSource={data} xName='month' yName='value' type='Line' />
        </SeriesCollectionDirective>
      </ChartComponent>
    </>
  );
}
```

**Important:** When updating data via state:
1. Create a new array (don't mutate the existing one)
2. Use `setData(prev => [...prev, newPoint])` pattern
3. React detects the change and re-renders the chart

### Real-Time Data Stream

```jsx
useEffect(() => {
  const interval = setInterval(() => {
    setData(prevData => {
      const updated = [...prevData];
      updated.push({ timestamp: new Date(), value: Math.random() * 100 });
      
      // Keep last 50 points
      if (updated.length > 50) updated.shift();
      return updated;
    });
  }, 1000);

  return () => clearInterval(interval);
}, []);
```

---

## Remote Data Binding

Bind data from a remote service using `DataManager` from `@syncfusion/ej2-data`. Assign a `DataManager` instance to `dataSource` and use `query` to filter, sort, or paginate data on the server. `DataManager` handles all request/response processing automatically.

### Basic Remote Data (Default Adaptor)

```jsx
import { DataManager, Query } from '@syncfusion/ej2-data';
import { ChartComponent, SeriesCollectionDirective, SeriesDirective, Inject, ColumnSeries, Category } from '@syncfusion/ej2-react-charts';

export default function RemoteChart() {
  const dataManager = new DataManager({
    url: 'Add your data source URL link'
  });
  const query = new Query().take(5).where('Estimate', 'lessThan', 3, false);

  return (
    <ChartComponent
      id='charts'
      primaryXAxis={{ valueType: 'Category' }}
      title='Container Freight Rate'
    >
      <Inject services={[ColumnSeries, Category]} />
      <SeriesCollectionDirective>
        <SeriesDirective
          dataSource={dataManager}
          xName='CustomerID'
          yName='Freight'
          type='Column'
          query={query}
        />
      </SeriesCollectionDirective>
    </ChartComponent>
  );
}
```

### ODataAdaptor

Use `ODataAdaptor` to consume OData v3.0 services. The adaptor automatically constructs the correct OData query syntax.

```jsx
import { DataManager, Query, ODataAdaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'https://services.odata.org/V3/Northwind/Northwind.svc/Orders/',
  adaptor: new ODataAdaptor(),
  crossDomain: true
});
const query = new Query();

<SeriesDirective dataSource={dataManager} xName='CustomerID' yName='Freight' type='Column' query={query} />
```

### ODataV4Adaptor

Use `ODataV4Adaptor` for OData v4.0 services, which provide enhanced query capabilities and better JSON support.

```jsx
import { DataManager, Query, ODataV4Adaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'https://services.odata.org/V4/Northwind/Northwind.svc/Orders',
  adaptor: new ODataV4Adaptor()
});
const query = new Query();

<SeriesDirective dataSource={dataManager} xName='CustomerID' yName='Freight' type='Column' query={query} />
```

### WebApiAdaptor

Use `WebApiAdaptor` for custom REST APIs that return a JSON object with `Items` (data array) and `Count` (total records) properties.

```jsx
import { DataManager, Query, WebApiAdaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'your data source URL link',
  adaptor: new WebApiAdaptor()
});
const query = new Query();

<SeriesDirective dataSource={dataManager} xName='CustomerID' yName='Freight' type='Column' query={query} />
```

**Expected Web API response format:**
```json
{
  "Items": [{ "CustomerID": "ALFKI", "Freight": 32.38 }, ...],
  "Count": 830
}
```

### Custom Adaptor

Extend a built-in adaptor to add custom request/response processing, such as adding computed fields or reformatting dates before the chart renders data.

```jsx
import { ODataAdaptor } from '@syncfusion/ej2-data';

class SerialNoAdaptor extends ODataAdaptor {
  processResponse(data, ds, query, xhr, request, changes) {
    let result = super.processResponse(data, ds, query, xhr, request, changes);
    result.result = result.result.map((item, index) => ({
      ...item,
      Sno: index + 1 // add serial number field
    }));
    return result;
  }
}

const dataManager = new DataManager({
  url: 'your data source URL link',
  adaptor: new SerialNoAdaptor()
});

<SeriesDirective dataSource={dataManager} xName='CustomerID' yName='Sno' type='Column' query={new Query()} />
```

### Offline Mode

Enable offline mode to load the full dataset once and handle all filtering/sorting client-side, eliminating repeated server requests during user interactions.

```jsx
import { DataManager, ODataAdaptor } from '@syncfusion/ej2-data';

const dataManager = new DataManager({
  url: 'your data source URL link',
  adaptor: new ODataAdaptor(),
  offline: true  // loads all data upfront; interactions run client-side
});

<SeriesDirective dataSource={dataManager} xName='CustomerID' yName='Freight' type='Column' />
```

**When to use offline mode:** Small-to-medium datasets where network latency hurts UX and you want instant client-side interactions without server round-trips.

### Common Datasource (Chart-Level)

Bind the same JSON data to all series by setting `dataSource` on `ChartComponent` instead of on each `SeriesDirective`. Each series independently maps its own `xName` and `yName`.

```jsx
import { ColumnSeries, Category } from '@syncfusion/ej2-react-charts';

const chartData = [
  { month: 'Jan', sales: 35, sales1: 28 },
  { month: 'Feb', sales: 28, sales1: 22 }
];

<ChartComponent id='charts' primaryXAxis={{ valueType: 'Category' }} dataSource={chartData}>
  <Inject services={[ColumnSeries, Category]} />
  <SeriesCollectionDirective>
    <SeriesDirective xName='month' yName='sales' type='Column' />
    <SeriesDirective xName='month' yName='sales1' type='Column' />
  </SeriesCollectionDirective>
</ChartComponent>
```

---

## Multiple Series Patterns

### Side-by-Side Series (Grouped)

```jsx
<SeriesCollectionDirective>
  <SeriesDirective
    dataSource={data}
    xName='category'
    yName='q1'
    type='Column'
    name='Q1'
  />
  <SeriesDirective
    dataSource={data}
    xName='category'
    yName='q2'
    type='Column'
    name='Q2'
  />
</SeriesCollectionDirective>
```

Columns appear side-by-side by default.

### Stacked Series

```jsx
<SeriesDirective
  dataSource={data}
  type='StackingColumn' // or StackingColumn100
/>
```

### Overlapping Series (Different Types)

```jsx
<SeriesCollectionDirective>
  <SeriesDirective
    dataSource={revenueData}
    type='Column'
    yName='amount'
  />
  <SeriesDirective
    dataSource={trendData}
    type='Line'
    yName='trend'
  />
</SeriesCollectionDirective>
```

---

## Complex Data Scenarios

### Conditional Series Rendering

Show/hide series based on state:

```jsx
const [showProfit, setShowProfit] = useState(true);

<SeriesCollectionDirective>
  <SeriesDirective dataSource={data} yName='revenue' type='Column' />
  {showProfit && (
    <SeriesDirective dataSource={data} yName='profit' type='Line' />
  )}
</SeriesCollectionDirective>
```

### Data Transformation

Transform raw data before binding:

```jsx
const rawData = [
  { date: '2024-01-01', value: 100 },
  { date: '2024-01-02', value: 110 }
];

const transformedData = rawData.map(item => ({
  ...item,
  date: new Date(item.date),
  formattedValue: item.value.toFixed(2)
}));

<SeriesDirective dataSource={transformedData} ... />
```

### Filtering Data

Show only specific data points:

```jsx
const [monthFilter, setMonthFilter] = useState('all');

const filteredData = monthFilter === 'all' 
  ? data 
  : data.filter(d => d.month === monthFilter);

<SeriesDirective dataSource={filteredData} ... />
```

### Data from API (Fetch)

```jsx
const [data, setData] = useState([]);

useEffect(() => {
  fetch('/api/chart-data')
    .then(res => res.json())
    .then(json => setData(json))
    .catch(err => console.error(err));
}, []);

// Chart renders empty initially and updates once data is loaded
<SeriesDirective dataSource={data} xName='x' yName='y' type='Line' />
```

> **Tip:** For production remote data scenarios, prefer `DataManager` with the appropriate adaptor (see [Remote Data Binding](#remote-data-binding)) instead of manual `fetch` calls. `DataManager` handles queries, pagination, and adaptor-specific response parsing automatically.

### Lazy Loading

Lazy loading retrieves only the data needed for the visible range. Listen to the `scrollEnd` event, fetch the new range from your server, and append to the existing dataset.

```jsx
import { LineSeries, ScrollBar, Zoom, DateTime } from '@syncfusion/ej2-react-charts';

<ChartComponent
  ref={chartRef}
  primaryXAxis={{
    valueType: 'DateTime',
    scrollbarSettings: {
      range: { minimum: new Date(2009, 0, 1), maximum: new Date(2014, 0, 1) },
      enable: true
    }
  }}
  scrollEnd={(args) => {
    // args.currentRange contains { minimum, maximum } of the new visible range
    const newData = fetchDataForRange(args.currentRange.minimum, args.currentRange.maximum);
    chartRef.current.series[0].dataSource = [
      ...chartRef.current.series[0].dataSource,
      ...newData
    ];
    chartRef.current.dataBind();
  }}
>
  <Inject services={[LineSeries, DateTime, ScrollBar, Zoom]} />
  <SeriesCollectionDirective>
    <SeriesDirective dataSource={initialData} xName='x' yName='y' type='Line' />
  </SeriesCollectionDirective>
</ChartComponent>
```

---

## Special Data Types

### Financial Data (OHLC)

```jsx
const financialData = [
  { date: '2024-01-01', open: 100, high: 105, low: 98, close: 103 },
  { date: '2024-01-02', open: 103, high: 108, low: 101, close: 107 }
];

<SeriesDirective
  dataSource={financialData}
  xName='date'
  low='low'
  high='high'
  open='open'
  close='close'
  type='Candle'
/>
```

### Range Data

```jsx
const rangeData = [
  { x: 'A', low: 20, high: 40 },
  { x: 'B', low: 15, high: 50 }
];

<SeriesDirective
  dataSource={rangeData}
  xName='x'
  low='low'
  high='high'
  type='RangeColumn'
/>
```

### Bubble Data (3D)

```jsx
const bubbleData = [
  { x: 10, y: 20, size: 50, name: 'Point A' },
  { x: 20, y: 30, size: 100, name: 'Point B' }
];

<SeriesDirective
  dataSource={bubbleData}
  xName='x'
  yName='y'
  size='size'
  type='Bubble'
/>
```

---

## Data Validation and Edge Cases

### Empty Data

```jsx
const data = []; // or null

<SeriesDirective
  dataSource={data}
  ... 
/>
// Chart renders empty, no error
```

### Missing Properties

```jsx
const data = [
  { month: 'Jan' }, // missing 'value'
  { month: 'Feb', value: 50 }
];

<SeriesDirective
  dataSource={data}
  xName='month'
  yName='value'
  ...
/>
// Points with missing yName values won't display
```

**Solution:** Validate data before binding:

```jsx
const validData = data.filter(d => d.month && d.value !== undefined);

<SeriesDirective dataSource={validData} ... />
```

### Duplicate X Values

```jsx
const data = [
  { month: 'Jan', value: 35 },
  { month: 'Jan', value: 40 }, // duplicate
  { month: 'Feb', value: 28 }
];
// Chart displays both points, may overlap
```

**Solution:** Group or aggregate duplicates:

```jsx
const aggregated = data.reduce((acc, item) => {
  const existing = acc.find(d => d.month === item.month);
  if (existing) {
    existing.value = (existing.value + item.value) / 2; // average
  } else {
    acc.push(item);
  }
  return acc;
}, []);
```

### Large Datasets (1000+ points)

- Use virtual scrolling with zooming
- Consider category axis instead of datetime
- Group data by time periods (hourly → daily)
- Implement data sampling or aggregation

---

## Performance Tips

- **Update data efficiently:** Use state correctly to avoid unnecessary re-renders
- **Data size:** Keep chart data under 5,000 points for optimal performance
- **Lazy loading:** Load data as needed, don't load entire year at once
- **Aggregation:** Combine small data points into larger time buckets
- **Memoization:** Use `useMemo` for complex data transformations

```jsx
const transformedData = useMemo(() => {
  return data.map(item => ({
    ...item,
    formatted: formatValue(item.value)
  }));
}, [data]);
```

---

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Data not showing | Wrong property names or case mismatch | Verify `xName` and `yName` match data object properties exactly |
| Points don't update | Mutating array instead of creating new | Use `[...data]` or `setData([...])` |
| Some points missing | Missing properties in some objects | Validate data, ensure all points have required properties |
| Chart too slow | Too many data points | Aggregate data, use category axis, or implement virtual scrolling |
| Labels cut off | Data labels overlapping | Adjust `datalabels.position` or reduce number of labels |

