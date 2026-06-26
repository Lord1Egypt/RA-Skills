# User Interactions

## Table of Contents
- [Selection](#selection)
- [Zooming and Panning](#zooming-and-panning)
- [Tooltip](#tooltip)
- [Crosshair](#crosshair)
- [Synchronized Charts](#synchronized-charts)
- [Event Handling](#event-handling)
- [Common Patterns](#common-patterns)

---

## Selection

Allow users to click on chart elements to highlight or interact with data.

### Highlighting vs Selection

**Highlighting:** Temporary visual emphasis when hovering over elements.
**Selection:** Persistent selection that remains after clicking.

```jsx
import { Selection, Highlight } from '@syncfusion/ej2-react-charts';

<ChartComponent
  selectionMode='Point'
  highlightMode='Series'
  highlightColor='#FFD700'
  highlightPattern='Dots'
>
  <Inject services={[Selection, Highlight]} />
  {/* chart content */}
</ChartComponent>
```

### Point Selection

```jsx
import { Selection } from '@syncfusion/ej2-react-charts';

<ChartComponent selectionMode='Point'>
  <Inject services={[Selection]} />
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={data}
      type='Column'
      selected={{
        color: '#FFD700' // highlight color
      }}
    />
  </SeriesCollectionDirective>
</ChartComponent>
```

**Selection modes:**
- `Point`: Individual data points
- `Series`: Entire series
- `Cluster`: All points in a category
- `DragXY`: Drag selection with respect to both axes
- `DragX`: Drag selection horizontally
- `DragY`: Drag selection vertically
- `Lasso`: Free-form drag selection
- `None`: No selection

### Multi-Selection

Enable selecting multiple points or series:

```jsx
<ChartComponent
  selectionMode='Point'
  isMultiSelect={true}  // Enable multi-selection
  selectedDataIndexes={[
    { series: 0, point: 1 },
    { series: 0, point: 3 }
  ]}
>
  <Inject services={[Selection]} />
  {/* chart content */}
</ChartComponent>
```

### Drag Selection

Enable drag-to-select multiple data points:

```jsx
<ChartComponent
  selectionMode='DragXY'  // or 'DragX', 'DragY'
  allowMultiSelection={true}
>
  <Inject services={[Selection]} />
  {/* chart content */}
</ChartComponent>
```

### Selection Patterns

Apply visual patterns to selected elements:

```jsx
<ChartComponent
  selectionMode='Point'
  selectionPattern='Chessboard'  // or 'Dots', 'DiagonalForward', 'Grid', etc.
>
  <Inject services={[Selection]} />
  {/* chart content */}
</ChartComponent>
```

**Available patterns:**
- None, Chessboard, Dots, DiagonalForward, DiagonalBackward
- Crosshatch, Pacman, Grid, Turquoise, Star, Triangle
- Circle, Tile, HorizontalDash, VerticalDash, Rectangle
- Box, VerticalStripe, HorizontalStripe, Bubble

### Selection Customization

```jsx
<ChartComponent
  selectionMode='Point'
  selectedDataIndexes={[
    { series: 0, point: 2 }, // pre-select points
    { series: 1, point: 3 }
  ]}
>
  <Inject services={[Selection]} />
  {/* series */}
</ChartComponent>
```

### Handling Selection Events

```jsx
const handlePointRender = (args) => {
  if (args.border) {
    args.border.width = 2;
    args.border.color = '#000';
  }
};

<ChartComponent
  pointRender={handlePointRender}
  selectionMode='Point'
>
  {/* chart */}
</ChartComponent>
```

---

## Zooming and Panning

Enable users to zoom into specific regions and pan around.

### Basic Zooming

```jsx
import { Zoom } from '@syncfusion/ej2-react-charts';

<ChartComponent
  zoomSettings={{
    enableSelectionZooming: true, // drag to zoom
    enablePinchZooming: true, // touch pinch zoom
    enableMouseWheelZooming: true, // mouse wheel zoom
    mode: 'XY' // or 'X', 'Y'
  }}
>
  <Inject services={[Zoom]} />
  {/* chart */}
</ChartComponent>
```

**Zoom modes:**
- `XY`: Zoom both axes
- `X`: Zoom horizontal axis only
- `Y`: Zoom vertical axis only

### Zoom Customization

```jsx
<ChartComponent
  zoomSettings={{
    enableSelectionZooming: true,
    enablePinchZooming: true,
    enableMouseWheelZooming: false, // disable mouse wheel
    enableDeferredZooming: true, // smooth animation
    enableScrollbar: true, // show scrollbar when zoomed
    toolbarItems: ['ZoomIn', 'ZoomOut', 'Pan', 'Reset'] // toolbar buttons
  }}
>
  {/* chart */}
</ChartComponent>
```

### Scrollbar with Zoom

Enable scrollbar for easier navigation when zoomed:

```jsx
import { ScrollBar } from '@syncfusion/ej2-react-charts';

<ChartComponent
  zoomSettings={{
    enableSelectionZooming: true,
    enableScrollbar: true
  }}
>
  <Inject services={[Zoom, ScrollBar]} />
  {/* chart */}
</ChartComponent>
```

### Programmatic Zooming

```jsx
const chartRef = useRef(null);

const handleZoom = () => {
  // Zoom to specific range
  chartRef.current?.primaryXAxis?.zoomRange({
    start: 0.2,
    end: 0.8
  });
};

<ChartComponent ref={chartRef}>
  {/* chart */}
</ChartComponent>
```

---

## Tooltip

Display information when hovering over data points.

### Basic Tooltip

```jsx
import { Tooltip } from '@syncfusion/ej2-react-charts';

<ChartComponent tooltip={{ enable: true }}>
  <Inject services={[Tooltip]} />
  {/* chart */}
</ChartComponent>
```

### Tooltip Customization

```jsx
<ChartComponent
  tooltip={{
    enable: true,
    shared: false, // true for multi-series
    enableMarker: true,
    backgroundColor: '#ffffff',
    border: {
      color: '#cccccc',
      width: 1
    },
    opacity: 1,
    format: '${series.name}: ${point.y}',
    template: `
      <div style="background: white; padding: 10px; border-radius: 4px;">
        <div><b>${point.x}</b></div>
        <div>${series.name}: ${point.y}</div>
      </div>
    `
  }}
>
  <Inject services={[Tooltip]} />
  {/* chart */}
</ChartComponent>
```

### Shared Tooltip (Multi-Series)

```jsx
<ChartComponent
  tooltip={{
    enable: true,
    shared: true, // show all series at once
  }}
>
  {/* multiple series */}
</ChartComponent>
```

## Crosshair

Display vertical and horizontal lines to help read values.

### Basic Crosshair

```jsx
import { Crosshair } from '@syncfusion/ej2-react-charts';

<ChartComponent
  crosshair={{
    enable: true,
    lineStyle: {
      width: 1,
      color: '#999',
      dashArray: '5,5'
    }
  }}
>
  <Inject services={[Crosshair]} />
  {/* chart */}
</ChartComponent>
```

### Crosshair with Trackball

```jsx
<ChartComponent
  crosshair={{
    enable: true,
    lineType: 'Vertical', // or 'Horizontal', 'Both'
    line: {
      width: 1,
      color: '#999'
    },
    lineStyle: {
      dashArray: '5,5'
    }
  }}
  tooltip={{
    enable: true,
    shared: true
  }}
>
  <Inject services={[Crosshair, Tooltip]} />
  {/* chart */}
</ChartComponent>
```

### Track Ball (Following Cursor)

```jsx
<ChartComponent
  tooltip={{
    enable: true
  }}
>
  {/* chart */}
</ChartComponent>
```

---

## Synchronized Charts

Link multiple charts so interactions in one affect others.

### Basic Synchronization

```jsx
import React, { useState } from 'react';

export default function SynchronizedCharts() {
  const [zoomRange, setZoomRange] = useState({ start: 0, end: 1 });

  const handleZoom = (range) => {
    setZoomRange(range);
  };

  return (
    <>
      <ChartComponent
        zoomSettings={{
          enableSelectionZooming: true
        }}
        // Handle zoom and update both
      >
        {/* chart 1 */}
      </ChartComponent>
      
      <ChartComponent
        // Use same zoomRange state
      >
        {/* chart 2 */}
      </ChartComponent>
    </>
  );
}
```

### Advanced Synchronization with Refs

```jsx
export default function SyncCharts() {
  const chart1Ref = useRef(null);
  const chart2Ref = useRef(null);

  const handleScroll1 = (args) => {
    // Mirror scroll to chart 2
    if (chart2Ref.current) {
      chart2Ref.current.primaryXAxis.zoomRange({
        start: args.zoomStart,
        end: args.zoomEnd
      });
    }
  };

  return (
    <>
      <ChartComponent ref={chart1Ref}>
        {/* chart 1 with handlers */}
      </ChartComponent>
      <ChartComponent ref={chart2Ref}>
        {/* chart 2 */}
      </ChartComponent>
    </>
  );
}
```

---

## Event Handling

Respond to chart interactions programmatically.

### Chart Events

```jsx
<ChartComponent
  chartMouseClick={(args) => {
    console.log('Chart clicked at:', args.pageX, args.pageY);
  }}
  chartMouseUp={(args) => {
    console.log('Mouse up');
  }}
  chartMouseDown={(args) => {
    console.log('Mouse down');
  }}
  chartMouseMove={(args) => {
    console.log('Mouse moving');
  }}
>
  {/* chart */}
</ChartComponent>
```

### Point/Series Events

```jsx
<ChartComponent
  pointRender={(args) => {
    // Called when point is rendered
    if (args.point.y > 50) {
      args.fill = '#4CAF50'; // highlight high values
    }
  }}
  seriesRender={(args) => {
    // Called when series is rendered
    console.log('Series rendered:', args.series.name);
  }}
>
  {/* chart */}
</ChartComponent>
```

### Selection Events

```jsx
<ChartComponent
  selectionMode='Point'
  selectionComplete={(args) => {
    console.log('Selected points:', args.selectedDataIndexes);
    // Handle selection
  }}
>
  <Inject services={[Selection]} />
  {/* chart */}
</ChartComponent>
```

### Zoom Events

```jsx
<ChartComponent
  zoomSettings={{ enableSelectionZooming: true }}
  zoomStart={(args) => {
    console.log('Zoom started');
  }}
  zoomEnd={(args) => {
    console.log('Zoom ended');
  }}
  zoomComplete={(args) => {
    console.log('New range:', args.zoomStart, args.zoomEnd);
  }}
>
  <Inject services={[Zoom]} />
  {/* chart */}
</ChartComponent>
```

---

## Common Patterns

### Pattern 1: Drill-Down Navigation

```jsx
const [selectedCategory, setSelectedCategory] = useState(null);
const [data, setData] = useState(categoryData);

const handlePointClick = (args) => {
  const category = args.pointIndex;
  setSelectedCategory(category);
  // Load detailed data for category
  setData(detailDataByCategory[category]);
};

<ChartComponent
  pointRender={(args) => {
    args.enableTooltip = true;
  }}
  chartMouseClick={handlePointClick}
>
  {/* chart */}
</ChartComponent>
```

### Pattern 2: Linked Dashboard

```jsx
export default function Dashboard() {
  const [selectedRegion, setSelectedRegion] = useState('All');

  const filteredData = selectedRegion === 'All'
    ? data
    : data.filter(d => d.region === selectedRegion);

  const handleSelection = (region) => {
    setSelectedRegion(region);
  };

  return (
    <>
      <ChartComponent
        selectionMode='Point'
        selectionComplete={(args) => {
          const region = data[args.selectedDataIndexes[0].point]?.region;
          handleSelection(region);
        }}
      >
        {/* Region selector chart */}
      </ChartComponent>
      
      <ChartComponent>
        <SeriesDirective dataSource={filteredData} />
        {/* Detail chart based on selection */}
      </ChartComponent>
    </>
  );
}
```

### Pattern 3: Time Range Selector

```jsx
export default function TimeRangeChart() {
  const [range, setRange] = useState({ start: 0, end: 1 });

  return (
    <>
      <ChartComponent
        zoomSettings={{
          enableSelectionZooming: true
        }}
        zoomComplete={(args) => {
          setRange({
            start: args.zoomStart,
            end: args.zoomEnd
          });
        }}
      >
        {/* Main chart with zooming */}
      </ChartComponent>
      
      <div>Selected range: {Math.round(range.start * 100)}% - {Math.round(range.end * 100)}%</div>
    </>
  );
}
```

### Pattern 4: Tooltip with Custom Content

```jsx
<ChartComponent
  tooltip={{
    enable: true,
    template: (args) => {
      const point = args.point;
      return `
        <div style="padding: 10px; background: #f5f5f5; border-radius: 4px;">
          <div><b>${point.x}</b></div>
          <div>Value: $${point.y?.toLocaleString()}</div>
          <div>% of total: ${((point.y / totalSum) * 100).toFixed(1)}%</div>
        </div>
      `;
    }
  }}
>
  {/* chart */}
</ChartComponent>
```

### Pattern 5: Context Menu on Right-Click

```jsx
<ChartComponent
  chartMouseClick={(args) => {
    if (args.event?.button === 2) { // right-click
      args.cancel = true; // prevent default context menu
      // Show custom menu
      showContextMenu({
        x: args.pageX,
        y: args.pageY
      });
    }
  }}
>
  {/* chart */}
</ChartComponent>
```

---

## Performance Considerations

- **Too many tooltips?** Debounce tooltip updates
- **Zooming slow?** Use `enableDeferredZoom: true`
- **Selection sluggish?** Limit number of selectable points
- **Many series?** Use `shared: false` for tooltips

---

## Data Editing (Drag and Drop)

Enable users to edit data by dragging points on the chart:

```jsx
import { DataEditing } from '@syncfusion/ej2-react-charts';

<ChartComponent
  dragStart={(args) => {
    console.log('Drag started:', args.seriesIndex, args.pointIndex);
  }}
  drag={(args) => {
    console.log('Dragging:', args.newY);
  }}
  dragEnd={(args) => {
    console.log('Drag ended, new value:', args.newY);
    // Update your data source here
  }}
>
  <Inject services={[LineSeries, DataEditing]} />
  <SeriesCollectionDirective>
    <SeriesDirective
      dataSource={data}
      dragSettings={{
        enable: true
      }}
      type='Line'
    />
  </SeriesCollectionDirective>
</ChartComponent>
```

---

## Browser Compatibility

- **Desktop:** Full support for all interactions
- **Mobile/Touch:** Use pinch zoom, tap selection
- **Accessibility:** Keyboard navigation for selection/zoom

---

## API Reference

For complete details on all interaction properties, methods, and events:
- **User Interaction API:** https://ej2.syncfusion.com/react/documentation/api/chart/overview
- **Selection API:** https://ej2.syncfusion.com/react/documentation/api/chart/selection
- **Zoom API:** https://ej2.syncfusion.com/react/documentation/api/chart/zoom
- **Tooltip API:** https://ej2.syncfusion.com/react/documentation/api/chart/tooltipsettingsmodel
