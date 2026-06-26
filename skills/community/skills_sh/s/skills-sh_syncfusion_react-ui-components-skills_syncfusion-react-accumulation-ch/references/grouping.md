# Grouping

## Table of Contents
- [Overview](#overview)
- [Group by Value](#group-by-value)
- [Group by Count](#group-by-count)
- [Grouping Modes](#grouping-modes)
- [Custom Group Names](#custom-group-names)
- [Group Click Event](#group-click-event)

## Overview

Grouping consolidates small or less significant data points into a single "Others" category, simplifying the chart and improving readability when dealing with many small slices.

## Group by Value

Group data points below a threshold value into an "Others" category:

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries
} from '@syncfusion/ej2-react-charts';

function GroupByValue() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 },
    { x: 'Edge', y: 5.0 },
    { x: 'Opera', y: 3.0 },
    { x: 'UC Browser', y: 2.5 },
    { x: 'Samsung Internet', y: 1.5 }
  ];

  return (
    <AccumulationChartComponent id='group-by-value'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          groupTo='5'  // Group values below 5
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Result:** Opera, UC Browser, and Samsung Internet (all < 5) are combined into "Others" slice.

**How it works:**
- `groupTo` specifies the threshold value
- All points with y-value below this threshold are grouped
- Grouped points appear as a single "Others" slice
- The "Others" slice shows the sum of all grouped values

## Group by Count

Group data based on the number of points to keep, placing the rest into "Others":

```tsx
function GroupByCount() {
  const data = [
    { x: 'Product A', y: 35 },
    { x: 'Product B', y: 28 },
    { x: 'Product C', y: 22 },
    { x: 'Product D', y: 15 },
    { x: 'Product E', y: 10 },
    { x: 'Product F', y: 8 },
    { x: 'Product G', y: 5 },
    { x: 'Product H', y: 3 }
  ];

  return (
    <AccumulationChartComponent id='group-by-count'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          groupTo='4'  // Keep top 4 points
          groupMode='Point'  // Group by point count
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Result:** Top 4 products (A, B, C, D) shown separately; remaining 4 (E, F, G, H) grouped into "Others".

**When to use:**
- Show only top N categories
- Limit chart complexity
- Focus on most significant data

## Grouping Modes

Control grouping behavior using the `groupMode` property:

```tsx
groupMode='Value'  // Group by threshold value (default)
groupMode='Point'  // Group by point count
```

**Value mode (default):**
- Groups points below `groupTo` value
- `groupTo='10'` means values < 10 are grouped
- Best for: Percentage-based data, filtering insignificant values

**Point mode:**
- Keeps top N points, groups the rest
- `groupTo='5'` means show top 5, group others
- Best for: Ranking data, top performers, limited display space

**Comparison example:**

```tsx
function GroupModeComparison() {
  const data = [
    { x: 'Item A', y: 45 },
    { x: 'Item B', y: 30 },
    { x: 'Item C', y: 15 },
    { x: 'Item D', y: 7 },
    { x: 'Item E', y: 3 }
  ];

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <AccumulationChartComponent 
        id='value-mode'
        title='Value Mode (< 10)'
      >
        <Inject services={[PieSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
            groupTo='10'
            groupMode='Value'  // D and E grouped (< 10)
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>

      <AccumulationChartComponent 
        id='point-mode'
        title='Point Mode (Top 3)'
      >
        <Inject services={[PieSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
            groupTo='3'
            groupMode='Point'  // Keep A, B, C; group D, E
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Custom Group Names

Customize the "Others" label using the `name` property on grouped data:

**Method 1: Using pointRender event**

```tsx
import { IAccPointRenderEventArgs } from '@syncfusion/ej2-react-charts';

function CustomGroupName() {
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 },
    { x: 'Edge', y: 5.0 },
    { x: 'Opera', y: 2.0 },
    { x: 'Others', y: 3.0 }
  ];

  const onPointRender = (args: IAccPointRenderEventArgs): void => {
    if (args.point.x === 'Others') {
      args.point.x = 'Minor Browsers';  // Custom name
      args.fill = '#cccccc';  // Custom color for grouped slice
    }
  };

  return (
    <AccumulationChartComponent 
      id='custom-group-name'
      pointRender={onPointRender}
    >
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          groupTo='5'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Method 2: Using data source with custom field**

```tsx
function CustomGroupNameData() {
  const data = [
    { browser: 'Chrome', share: 61.3 },
    { browser: 'Safari', share: 24.6 },
    { browser: 'Firefox', share: 14.1 },
    { browser: 'Edge', share: 5.0 },
    { browser: 'Opera', share: 2.0 },
    { browser: 'Remaining Browsers', share: 3.0 }  // Custom name in data
  ];

  return (
    <AccumulationChartComponent id='custom-group-data'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='browser'
          yName='share'
          groupTo='5'
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Group Click Event

Handle clicks on the grouped "Others" slice using the `pointClick` event:

```tsx
import { IAccPointEventArgs } from '@syncfusion/ej2-react-charts';

function GroupClickEvent() {
  const [showDetails, setShowDetails] = React.useState(false);
  const [groupedData, setGroupedData] = React.useState<any[]>([]);

  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 },
    { x: 'Edge', y: 5.0 },
    { x: 'Opera', y: 3.0 },
    { x: 'UC Browser', y: 2.5 },
    { x: 'Samsung', y: 1.5 }
  ];

  const onPointClick = (args: IAccPointEventArgs): void => {
    if (args.point.x === 'Others') {
      // Extract grouped data
      const grouped = data.filter(d => d.y < 5);
      setGroupedData(grouped);
      setShowDetails(true);
    }
  };

  return (
    <div>
      <AccumulationChartComponent 
        id='group-click'
        pointClick={onPointClick}
      >
        <Inject services={[PieSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
            groupTo='5'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>

      {showDetails && (
        <div style={{
          marginTop: '20px',
          padding: '15px',
          backgroundColor: '#f5f5f5',
          borderRadius: '8px'
        }}>
          <h3>Grouped Items</h3>
          <button onClick={() => setShowDetails(false)}>Close</button>
          <ul>
            {groupedData.map((item, index) => (
              <li key={index}>
                {item.x}: {item.y}%
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
```

**Use cases for group click:**
- Show drill-down details of grouped items
- Display modal with breakdown
- Navigate to detailed page
- Toggle between grouped and ungrouped views

**Advanced example with toggle:**

```tsx
function ToggleGrouping() {
  const [groupEnabled, setGroupEnabled] = React.useState(true);

  const data = [
    { x: 'Category A', y: 35 },
    { x: 'Category B', y: 28 },
    { x: 'Category C', y: 22 },
    { x: 'Category D', y: 8 },
    { x: 'Category E', y: 4 },
    { x: 'Category F', y: 3 }
  ];

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => setGroupEnabled(!groupEnabled)}>
          {groupEnabled ? 'Show All Items' : 'Enable Grouping'}
        </button>
      </div>

      <AccumulationChartComponent 
        id='toggle-grouping'
        title={groupEnabled ? 'Grouped View' : 'All Items'}
      >
        <Inject services={[PieSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
            groupTo={groupEnabled ? '10' : null}  // Conditional grouping
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Common Issues and Solutions

**Issue: Grouping not working**
- Solution: Ensure `groupTo` value is appropriate for your data range
- Solution: Check data values are numbers, not strings
- Solution: Verify `groupMode` matches your intent ('Value' vs 'Point')

**Issue: Too many items grouped**
- Solution: Decrease `groupTo` value in Value mode
- Solution: Increase `groupTo` value in Point mode
- Solution: Review data distribution to find appropriate threshold

**Issue: "Others" slice too large**
- Solution: Adjust `groupTo` threshold to be more selective
- Solution: Consider not grouping if "Others" dominates
- Solution: Review if grouping is appropriate for your data

**Issue: Can't customize "Others" label**
- Solution: Use `pointRender` event to modify point.x property
- Solution: Ensure event fires before rendering completes
- Solution: Check that point identification (x === 'Others') is correct

**Issue: Group click not detecting "Others"**
- Solution: Verify point.x comparison in pointClick handler
- Solution: Check that grouped points are correctly identified
- Solution: Use console.log to inspect args.point structure
