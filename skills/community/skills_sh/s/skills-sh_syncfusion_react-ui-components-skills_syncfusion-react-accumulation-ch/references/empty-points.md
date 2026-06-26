# Empty Points

## Overview

Empty points represent null, undefined, or missing data values in the chart. Syncfusion provides multiple modes to handle these gracefully without breaking the visualization.

## Handling Empty Points

Configure empty point handling using the `emptyPointSettings` property:

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries
} from '@syncfusion/ej2-react-charts';

function EmptyPointHandling() {
  const data = [
    { x: 'Jan', y: 35 },
    { x: 'Feb', y: null },  // Empty point
    { x: 'Mar', y: 34 },
    { x: 'Apr', y: undefined },  // Empty point
    { x: 'May', y: 28 }
  ];

  return (
    <AccumulationChartComponent id='empty-points'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          emptyPointSettings={{
            mode: 'Drop'  // Skip empty points
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Empty Point Modes

Control how empty points are rendered using the `mode` property:

**Drop Mode (Default):**
Removes empty points from the chart entirely.

```tsx
function DropMode() {
  const data = [
    { x: 'Product A', y: 45 },
    { x: 'Product B', y: null },
    { x: 'Product C', y: 30 },
    { x: 'Product D', y: 25 }
  ];

  return (
    <AccumulationChartComponent id='drop-mode'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          emptyPointSettings={{
            mode: 'Drop'  // Product B will not appear
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Zero Mode:**
Treats empty points as zero values.

```tsx
function ZeroMode() {
  const data = [
    { x: 'Q1', y: 35 },
    { x: 'Q2', y: null },  // Treated as 0
    { x: 'Q3', y: 42 },
    { x: 'Q4', y: 31 }
  ];

  return (
    <AccumulationChartComponent id='zero-mode'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          emptyPointSettings={{
            mode: 'Zero'  // Q2 shows as 0
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Average Mode:**
Replaces empty points with the average of adjacent points.

```tsx
function AverageMode() {
  const data = [
    { x: 'Week 1', y: 20 },
    { x: 'Week 2', y: null },  // Will be (20 + 30) / 2 = 25
    { x: 'Week 3', y: 30 },
    { x: 'Week 4', y: null },  // Will be (30 + 28) / 2 = 29
    { x: 'Week 5', y: 28 }
  ];

  return (
    <AccumulationChartComponent id='average-mode'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          emptyPointSettings={{
            mode: 'Average'  // Interpolate empty values
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

## Mode Comparison

Compare different empty point handling strategies:

```tsx
function ModeComparison() {
  const data = [
    { x: 'A', y: 25 },
    { x: 'B', y: null },
    { x: 'C', y: 35 },
    { x: 'D', y: null },
    { x: 'E', y: 20 }
  ];

  return (
    <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
      <div>
        <h3>Drop Mode</h3>
        <AccumulationChartComponent id='compare-drop' width='300'>
          <Inject services={[PieSeries]} />
          <AccumulationSeriesCollectionDirective>
            <AccumulationSeriesDirective
              dataSource={data}
              xName='x'
              yName='y'
              emptyPointSettings={{ mode: 'Drop' }}
            />
          </AccumulationSeriesCollectionDirective>
        </AccumulationChartComponent>
      </div>

      <div>
        <h3>Zero Mode</h3>
        <AccumulationChartComponent id='compare-zero' width='300'>
          <Inject services={[PieSeries]} />
          <AccumulationSeriesCollectionDirective>
            <AccumulationSeriesDirective
              dataSource={data}
              xName='x'
              yName='y'
              emptyPointSettings={{ mode: 'Zero' }}
            />
          </AccumulationSeriesCollectionDirective>
        </AccumulationChartComponent>
      </div>

      <div>
        <h3>Average Mode</h3>
        <AccumulationChartComponent id='compare-avg' width='300'>
          <Inject services={[PieSeries]} />
          <AccumulationSeriesCollectionDirective>
            <AccumulationSeriesDirective
              dataSource={data}
              xName='x'
              yName='y'
              emptyPointSettings={{ mode: 'Average' }}
            />
          </AccumulationSeriesCollectionDirective>
        </AccumulationChartComponent>
      </div>
    </div>
  );
}
```

## Styling Empty Points

Customize the appearance of empty points with distinct styling:

```tsx
function StyledEmptyPoints() {
  const data = [
    { x: 'Complete', y: 45 },
    { x: 'No Data', y: null },
    { x: 'In Progress', y: 30 },
    { x: 'Missing', y: undefined },
    { x: 'Done', y: 25 }
  ];

  return (
    <AccumulationChartComponent id='styled-empty'>
      <Inject services={[PieSeries]} />
      <AccumulationSeriesCollectionDirective>
        <AccumulationSeriesDirective
          dataSource={data}
          xName='x'
          yName='y'
          emptyPointSettings={{
            mode: 'Zero',
            fill: '#e0e0e0',  // Gray for empty points
            border: {
              width: 2,
              color: '#999999'
            }
          }}
        />
      </AccumulationSeriesCollectionDirective>
    </AccumulationChartComponent>
  );
}
```

**Styling properties:**
- `fill`: Background color for empty points
- `border`: Border styling { width, color }

## Detecting Empty Points

Identify empty points programmatically:

```tsx
function DetectEmptyPoints() {
  const [emptyCount, setEmptyCount] = React.useState(0);
  
  const data = [
    { x: 'Jan', y: 35 },
    { x: 'Feb', y: null },
    { x: 'Mar', y: 34 },
    { x: 'Apr', y: null },
    { x: 'May', y: 28 }
  ];

  React.useEffect(() => {
    const empties = data.filter(d => d.y === null || d.y === undefined).length;
    setEmptyCount(empties);
  }, []);

  return (
    <div>
      <div style={{ marginBottom: '10px', padding: '10px', background: '#fff3cd' }}>
        Warning: {emptyCount} data points are missing
      </div>

      <AccumulationChartComponent id='detect-empty'>
        <Inject services={[PieSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
            emptyPointSettings={{
              mode: 'Average',
              fill: '#ffc107',
              border: { width: 2, color: '#ff9800' }
            }}
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Handling with Custom Logic

Preprocess data with custom empty point logic:

```tsx
function CustomEmptyHandling() {
  const rawData = [
    { x: 'Product A', y: 45, fallback: 40 },
    { x: 'Product B', y: null, fallback: 35 },
    { x: 'Product C', y: 30, fallback: 30 },
    { x: 'Product D', y: undefined, fallback: 25 }
  ];

  // Custom preprocessing: use fallback values
  const processedData = rawData.map(item => ({
    x: item.x,
    y: item.y ?? item.fallback,  // Use fallback if null/undefined
    isEstimated: item.y === null || item.y === undefined
  }));

  const onPointRender = (args: any) => {
    if (args.data.isEstimated) {
      // Style estimated points differently
      args.fill = '#ffc107';
      args.border = { width: 2, color: '#ff9800', dashArray: '5,3' };
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <span style={{ 
          display: 'inline-block', 
          width: '20px', 
          height: '20px', 
          backgroundColor: '#ffc107',
          border: '2px dashed #ff9800',
          marginRight: '5px'
        }} />
        Estimated values
      </div>

      <AccumulationChartComponent 
        id='custom-empty'
        pointRender={onPointRender}
      >
        <Inject services={[PieSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={processedData}
            xName='x'
            yName='y'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Best Practices

**When to use each mode:**

| Mode | Use Case | Example Scenario |
|------|----------|------------------|
| **Drop** | Missing data is irrelevant | Discontinued products in sales chart |
| **Zero** | Absence means zero | Items with no sales in a period |
| **Average** | Estimate missing values | Interpolate missing measurements |

**Complete example with best practices:**

```tsx
function EmptyPointsBestPractices() {
  const [mode, setMode] = React.useState<'Drop' | 'Zero' | 'Average'>('Drop');
  
  const data = [
    { x: 'Jan', y: 35 },
    { x: 'Feb', y: null },
    { x: 'Mar', y: 34 },
    { x: 'Apr', y: 28 },
    { x: 'May', y: null },
    { x: 'Jun', y: 42 }
  ];

  const emptyCount = data.filter(d => d.y === null || d.y === undefined).length;

  return (
    <div>
      {emptyCount > 0 && (
        <div style={{
          padding: '10px',
          backgroundColor: '#fff3cd',
          border: '1px solid #ffc107',
          borderRadius: '4px',
          marginBottom: '15px'
        }}>
          <strong>Data Quality Notice:</strong> {emptyCount} of {data.length} data points are missing.
        </div>
      )}

      <div style={{ marginBottom: '10px' }}>
        <label>Empty Point Handling: </label>
        <select 
          value={mode} 
          onChange={(e) => setMode(e.target.value as any)}
          style={{ marginLeft: '10px', padding: '5px' }}
        >
          <option value="Drop">Drop (Remove)</option>
          <option value="Zero">Zero (Treat as 0)</option>
          <option value="Average">Average (Interpolate)</option>
        </select>
      </div>

      <AccumulationChartComponent 
        id='best-practices'
        title={`Monthly Data (${mode} mode)`}
      >
        <Inject services={[PieSeries]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
            emptyPointSettings={{
              mode: mode,
              fill: mode === 'Zero' ? '#e0e0e0' : undefined,
              border: mode === 'Zero' ? { width: 2, color: '#999' } : undefined
            }}
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Common Issues and Solutions

**Issue: Empty points breaking chart**
- Solution: Enable `emptyPointSettings` with appropriate mode
- Solution: Validate data before rendering
- Solution: Use 'Drop' mode to skip problematic points

**Issue: Zero mode making slices too small**
- Solution: Use 'Drop' mode instead to remove zeros
- Solution: Group small values including zeros
- Solution: Consider if zero is meaningful for your data

**Issue: Average mode producing unexpected values**
- Solution: Verify adjacent values exist for calculation
- Solution: Use custom preprocessing for complex logic
- Solution: Consider 'Drop' or 'Zero' for edge cases

**Issue: Can't distinguish empty from actual data**
- Solution: Use custom fill color for empty points
- Solution: Add distinct border styling
- Solution: Preprocess data and mark empty points explicitly

**Issue: Multiple consecutive empty points**
- Solution: Average mode may not work well - use Drop or Zero
- Solution: Implement custom preprocessing logic
- Solution: Consider data quality and collection process
