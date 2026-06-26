# Selection and Interaction

Enable user interaction through data point selection, highlighting, and event handling in 3D charts.

## Table of contents

- [Selection](selection-interaction.md#selection)
  - [Basic Selection](selection-interaction.md#basic-selection)
  - [Selection Modes](selection-interaction.md#selection-modes)
  - [Multi-Select](selection-interaction.md#multi-select)
  - [Selection Pattern](selection-interaction.md#selection-pattern)
  - [Pre-Select Data Points](selection-interaction.md#pre-select-data-points)
- [Highlighting](selection-interaction.md#highlighting)
  - [Basic Highlighting](selection-interaction.md#basic-highlighting)
  - [Highlight Modes](selection-interaction.md#highlight-modes)
  - [Highlight Pattern](selection-interaction.md#highlight-pattern)
- [Event Handling](selection-interaction.md#event-handling)
  - [Point Click Event](selection-interaction.md#point-click-event)
  - [Selection Complete Event](selection-interaction.md#selection-complete-event)
  - [Loaded Event](selection-interaction.md#loaded-event)
- [Complete Interactive Example](selection-interaction.md#complete-interactive-example)
- [Use Cases](selection-interaction.md#use-cases)
- [Best Practices](selection-interaction.md#best-practices)
- [Common Issues](selection-interaction.md#common-issues)

## Selection

### Basic Selection

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D, Selection3D } from '@syncfusion/ej2-react-charts';

function SelectionChart() {
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 42 },
    { month: 'Mar', sales: 38 },
    { month: 'Apr', sales: 48 },
    { month: 'May', sales: 45 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
      selectionMode='Point'  // Enable point selection
    >
      <Inject services={[ColumnSeries3D, Category3D, Selection3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='sales'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key requirement:** Must inject `Selection3D` service for selection to work.

### Selection Modes

```tsx
<Chart3DComponent
  selectionMode='Point'  // Options: 'None', 'Point', 'Series', 'Cluster'
>
  {/* Series */}
</Chart3DComponent>
```

**Selection modes:**
- `None`: Disable selection (default)
- `Point`: Select individual data points
- `Series`: Select entire series
- `Cluster`: Select all points at same X-axis value (across series)

### Multi-Select

Allow selecting multiple items:

```tsx
<Chart3DComponent
  selectionMode='Point'
  isMultiSelect={true}  // Enable multi-selection (Ctrl/Cmd + click)
>
  {/* Series */}
</Chart3DComponent>
```

### Selection Pattern

Customize selected item appearance:

```tsx
<Chart3DComponent
  selectionMode='Point'
  selectionPattern='DiagonalForward'  // Options: 'None', 'Dots', 'DiagonalBackward', 'Crosshatch', etc.
>
  {/* Series */}
</Chart3DComponent>
```

**Pattern options:**
- `None`: No pattern (solid color)
- `Dots`: Dotted pattern
- `DiagonalBackward`: Diagonal lines (\)
- `DiagonalForward`: Diagonal lines (/)
- `Crosshatch`: Cross-hatched pattern
- `HorizontalDash`: Horizontal dashes
- `VerticalDash`: Vertical dashes
- `Rectangle`: Rectangular pattern
- `Box`: Box pattern
- `Triangle`: Triangle pattern

### Pre-Select Data Points

Set initial selection on load:

```tsx
function PreSelectedChart() {
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 42 },
    { month: 'Mar', sales: 38 },
    { month: 'Apr', sales: 48 },
    { month: 'May', sales: 45 }
  ];
  const [chart, setChart] = React.useState(null);

  React.useEffect(() => {
    if (chart) {
      // Select point at index 2 in series 0
      chart.setSelected(0, 2, true);
    }
  }, [chart]);

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
      selectionMode='Point'
    >
      <Inject services={[ColumnSeries3D, Category3D, Selection3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='sales'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Highlighting

### Basic Highlighting

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D, Highlight3D } from '@syncfusion/ej2-react-charts';

function HighlightChart() {
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 42 },
    { month: 'Mar', sales: 38 },
    { month: 'Apr', sales: 48 }
  ];

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
      highlightMode='Point'  // Enable highlighting on hover
    >
      <Inject services={[ColumnSeries3D, Category3D, Highlight3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='sales'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

**Key requirement:** Must inject `Highlight3D` service for highlighting.

### Highlight Modes

```tsx
<Chart3DComponent
  highlightMode='Series'  // Options: 'None', 'Point', 'Series', 'Cluster'
>
  {/* Series */}
</Chart3DComponent>
```

**Same modes as selection:** None, Point, Series, Cluster

### Highlight Pattern

```tsx
<Chart3DComponent
  highlightMode='Point'
  highlightPattern='Dots'  // Same pattern options as selection
>
  {/* Series */}
</Chart3DComponent>
```

### Combining Selection and Highlighting

```tsx
function SelectAndHighlight() {
  const data = [
    { category: 'Product A', sales: 45, profit: 18 },
    { category: 'Product B', sales: 52, profit: 22 },
    { category: 'Product C', sales: 38, profit: 15 },
    { category: 'Product D', sales: 65, profit: 28 }
  ];

  return (
    <Chart3DComponent
      id='interactive-chart'
      title='Interactive Product Performance'
      primaryXAxis={{ valueType: 'Category' }}
      selectionMode='Cluster'  // Click to select
      highlightMode='Point'    // Hover to highlight
      isMultiSelect={true}
    >
      <Inject services={[ColumnSeries3D, Category3D, Selection3D, Highlight3D, Legend3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='category'
          yName='sales'
          type='Column'
          name='Sales'
        />
        <Chart3DSeriesDirective
          dataSource={data}
          xName='category'
          yName='profit'
          type='Column'
          name='Profit'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

## Event Handling

### Point Click Event

```tsx
function ClickEventChart() {
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 42 },
    { month: 'Mar', sales: 38 },
    { month: 'Apr', sales: 48 }
  ];

  const onPointClick = (args: any) => {
    console.log('Clicked point:', {
      x: args.point.x,
      y: args.point.y,
      seriesIndex: args.seriesIndex,
      pointIndex: args.pointIndex
    });
    alert(`Clicked: ${args.point.x} - ${args.point.y}`);
  };

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
      pointClick={onPointClick}
    >
      <Inject services={[ColumnSeries3D, Category3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='sales'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

### Selection Complete Event

```tsx
function SelectionEventChart() {
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 42 },
    { month: 'Mar', sales: 38 }
  ];

  const onSelectionComplete = (args: any) => {
    console.log('Selection changed:', {
      selectedDataPoints: args.selectedDataValues,
      seriesIndex: args.seriesIndex
    });
  };

  return (
    <Chart3DComponent
      id='chart'
      primaryXAxis={{ valueType: 'Category' }}
      selectionMode='Point'
      selectionComplete={onSelectionComplete}
    >
      <Inject services={[ColumnSeries3D, Category3D, Selection3D]} />
      <Chart3DSeriesCollectionDirective>
        <Chart3DSeriesDirective
          dataSource={data}
          xName='month'
          yName='sales'
          type='Column'
        />
      </Chart3DSeriesCollectionDirective>
    </Chart3DComponent>
  );
}
```

### Loaded Event

Fires when chart completes rendering:

```tsx
const onChartLoad = (args: any) => {
  console.log('Chart loaded successfully');
  // Perform post-load operations
};

<Chart3DComponent
  id='chart'
  loaded={onChartLoad}
>
  {/* Series */}
</Chart3DComponent>
```

## Complete Interactive Example

```tsx
function ComprehensiveInteractiveChart() {
  const [selectedData, setSelectedData] = React.useState<any>(null);
  
  const salesData = [
    { quarter: 'Q1', revenue: 120, cost: 80 },
    { quarter: 'Q2', revenue: 150, cost: 95 },
    { quarter: 'Q3', revenue: 135, cost: 88 },
    { quarter: 'Q4', revenue: 165, cost: 102 }
  ];

  const onPointClick = (args: any) => {
    const clicked = {
      quarter: args.point.x,
      value: args.point.y,
      series: args.series.name
    };
    setSelectedData(clicked);
  };

  const onSelectionComplete = (args: any) => {
    console.log('Selected:', args.selectedDataValues);
  };

  return (
    <div>
      <Chart3DComponent
        id='interactive-chart'
        title='Quarterly Financial Performance (Click to Select)'
        primaryXAxis={{
          valueType: 'Category',
          title: 'Quarter'
        }}
        primaryYAxis={{
          title: 'Amount ($K)',
          minimum: 0,
          maximum: 200
        }}
        selectionMode='Cluster'
        highlightMode='Point'
        isMultiSelect={true}
        highlightPattern='Dots'
        chart3DPointClick={onPointClick}
        chart3DSelectionComplete={onSelectionComplete}
        rotation={7}
        tilt={10}
      >
        <Inject services={[ColumnSeries3D, Category3D, Selection3D, Highlight3D, Legend3D, Tooltip3D]} />
        <Chart3DSeriesCollectionDirective>
          <Chart3DSeriesDirective
            dataSource={salesData}
            xName='quarter'
            yName='revenue'
            type='Column'
            name='Revenue'
          />
          <Chart3DSeriesDirective
            dataSource={salesData}
            xName='quarter'
            yName='cost'
            type='Column'
            name='Cost'
          />
        </Chart3DSeriesCollectionDirective>
      </Chart3DComponent>

      {selectedData && (
        <div style={{ marginTop: '20px', padding: '15px', background: '#F5F5F5', borderRadius: '5px' }}>
          <h3>Selected Data Point:</h3>
          <p><strong>Quarter:</strong> {selectedData.quarter}</p>
          <p><strong>Series:</strong> {selectedData.series}</p>
          <p><strong>Value:</strong> ${selectedData.value}K</p>
        </div>
      )}
    </div>
  );
}
```

## Use Cases

**Data exploration:**
- Allow users to click points for detailed view
- Multi-select for comparison
- Highlight on hover for quick insights

**Filtering:**
- Select points to filter related data elsewhere
- Cluster selection to compare all series at specific X-value

**Dashboard integration:**
- Click event triggers other component updates
- Selection state synced across multiple charts

**Analytics:**
- Track which data points users interact with
- Log selection patterns for UX insights

## Best Practices

**Selection vs highlighting:**
- Use **highlighting** for quick preview (hover)
- Use **selection** for persistent choice (click)
- Combine both for best user experience

**Selection mode:**
- Use **Point** for detailed data analysis
- Use **Series** for comparing entire datasets
- Use **Cluster** for cross-series comparison at specific X-values

**Multi-select:**
- Enable for comparison scenarios
- Provide clear visual feedback (patterns, colors)
- Add UI to show selected items count

**Events:**
- Keep event handlers lightweight for performance
- Debounce rapid events if needed
- Provide user feedback for actions (status messages, highlights)

## Common Issues

**Selection not working:**
- Ensure `Selection3D` service is injected
- Set `selectionMode` to something other than 'None'
- Check that chart has rendered (use loaded event)

**Highlighting not visible:**
- Inject `Highlight3D` service
- Set `highlightMode` properly
- Verify `highlightPattern` or color provides contrast

**Events not firing:**
- Check event name spelling (case-sensitive)
- Ensure event handler is properly bound
- Verify TypeScript types if using TypeScript

**Multi-select not working:**
- Set `isMultiSelect={true}`
- Users must hold Ctrl (Windows) or Cmd (Mac) while clicking
- Document this behavior for users

---

See also: [api-reference.md](api-reference.md) | [usage-example.md](usage-example.md)
