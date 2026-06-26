# Advanced Features & Events

## Table of Contents

- [Bubble HeatMap](#bubble-heatmap)
  - [Creating a Bubble HeatMap](#creating-a-bubble-heatmap)
  - [Bubble Sizing Configuration](#bubble-sizing-configuration)
  - [Use Cases for Bubble HeatMaps](#use-cases-for-bubble-heatmaps)
- [Event Handling](#event-handling)
  - [Core Events](#core-events)
  - [Created Event (Component Initialization)](#created-event-component-initialization)
  - [Multi-Event Handler](#multi-event-handler)
- [Rendering Mode Switching](#rendering-mode-switching)
  - [Automatic Switching](#automatic-switching)
  - [Manual Canvas Mode](#manual-canvas-mode)
  - [SVG Mode with Performance Tips](#svg-mode-with-performance-tips)
- [Custom Cell Rendering](#custom-cell-rendering)
  - [Basic Cell Rendering](#basic-cell-rendering)
  - [Custom Icons/Emojis in Cells](#custom-iconsemojis-in-cells)
  - [Complex Cell Rendering with Data Lookup](#complex-cell-rendering-with-data-lookup)
- [Data Binding Events](#data-binding-events)
  - [After Data Bind](#after-data-bind)
  - [Dynamic Data Updates](#dynamic-data-updates)
- [Performance Optimization](#performance-optimization)
  - [Large Dataset Handling](#large-dataset-handling)
  - [Lazy Loading Pattern](#lazy-loading-pattern)
  - [Debounced Refresh](#debounced-refresh)
- [Complete Advanced Example](#complete-advanced-example)

## Bubble HeatMap

### Creating a Bubble HeatMap

A bubble heatmap combines cell color with bubble size for bivariate data visualization. There are several bubble types:
- **Size**: Bubble size varies with data, color is gradient
- **Color**: Bubble size is fixed, color varies with data
- **Sector**: Bubble sector angle represents data value
- **SizeAndColor**: Both bubble size and color vary with data

### Array Binding with SizeAndColor Type

For array binding, use 2D arrays where each cell contains [colorValue, sizeValue]:

```jsx
import { HeatMapComponent, Inject, Legend, Tooltip, Adaptor } from '@syncfusion/ej2-react-heatmap';

export function BubbleHeatmap() {
  // Array of arrays: each cell is [value1, value2]
  const data = [
    [[4, 39], [3, 8], [1, 3], [1, 10]],
    [[4, 28], [5, 92], [5, 73], [3, 1]],
    [[4, 45], [5, 152], [0, 44], [4, 54]]
  ];

  return (
    <HeatMapComponent
      id='heatmap'
      dataSource={data}
      xAxis={{ labels: ['Year1', 'Year2', 'Year3'] }}
      yAxis={{ labels: ['Q1', 'Q2', 'Q3', 'Q4'] }}
      paletteSettings={{
        palette: [
          { color: '#C06C84' },
          { color: '#6C5B7B' },
          { color: '#355C7D' }
        ],
        type: 'Gradient'
      }}
      legendSettings={{ visible: true }}
      cellSettings={{
        tileType: 'Bubble',
        bubbleType: 'SizeAndColor',
        border: { width: 1 }
      }}
      showTooltip={true}
    >
      <Inject services={[Legend, Tooltip, Adaptor]} />
    </HeatMapComponent>
  );
}
```

### Bubble Size Type (Size Variation Only)

Use 2D array data with `bubbleType: 'Size'` for variable bubble sizes:

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={[[73, 39, 26], [93, 58, 53], [54, 39, 26]]}
  cellSettings={{
    tileType: 'Bubble',
    bubbleType: 'Size',
    border: { width: 1 }
  }}
  paletteSettings={{
    palette: [
      { color: '#C06C84' },
      { color: '#6C5B7B' },
      { color: '#355C7D' }
    ],
    type: 'Gradient'
  }}
  legendSettings={{ visible: true }}
>
  <Inject services={[Legend, Tooltip, Adaptor]} />
</HeatMapComponent>
```

### Bubble Color Type (Color Variation Only)

Use 2D array data with `bubbleType: 'Color'` for variable colors with fixed size:

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={[[73, 39, 26], [93, 58, 53], [54, 39, 26]]}
  cellSettings={{
    tileType: 'Bubble',
    bubbleType: 'Color',
    border: { width: 1 }
  }}
  paletteSettings={{
    palette: [
      { color: '#C06C84' },
      { color: '#6C5B7B' },
      { color: '#355C7D' }
    ],
    type: 'Gradient'
  }}
  legendSettings={{ visible: true }}
>
  <Inject services={[Legend, Tooltip, Adaptor]} />
</HeatMapComponent>
```

### Key Properties for Bubble HeatMaps

| Property | Type | Values | Description |
|----------|------|--------|-------------|
| `tileType` | string | 'Rect' \| 'Bubble' | Cell rendering type |
| `bubbleType` | string | 'Size' \| 'Color' \| 'Sector' \| 'SizeAndColor' | Bubble variation type |
| `bubbleSize` | object | { minimum, maximum } | Bubble size range (for Size type) |
| `isInversedbubblesize` | boolean | true \| false | Inverts bubble size mapping |
| `showLabel` | boolean | true \| false | Display cell labels |

### Use Cases for Bubble HeatMaps

- **Correlation with Intensity**: Color = correlation strength, Bubble = frequency
- **Financial Data**: Color = return %, Size = volatility
- **Network Analysis**: Color = traffic volume, Size = node importance
- **Aviation Safety**: Color = fatalities, Size = accidents
- **Scientific Data**: Two dimensions of measurement combined
- **Labor Force Analysis**: Color = participation rate, Size = population

### Custom Tooltip for Bubble Data

For SizeAndColor bubble maps, customize tooltip to show both values:

```jsx
tooltipRender={(args) => {
  if (args.value) {
    args.content = [
      'Category : ' + args.xLabel + '<br/>',
      'Period : ' + args.yLabel + '<br/>',
      'Value 1 (Bubble Size) : ' + args.value[0].bubbleData + '<br/>',
      'Value 2 (Color) : ' + args.value[1].bubbleData
    ];
  }
}}
```

## Event Handling

### Core Events

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  created={(args) => {
    console.log('HeatMap created successfully');
  }}
  cellClick={(args) => {
    console.log(`Cell clicked: [${args.row}, ${args.column}] = ${args.value}`);
  }}
  cellSelected={(args) => {
    console.log(`Cell selected: [${args.row}, ${args.column}]`);
  }}
  cellDoubleClick={(args) => {
    console.log(`Cell double clicked: [${args.row}, ${args.column}]`);
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Created Event (Component Initialization)

```jsx
import { useRef, useEffect } from 'react';

export function InitializationTracking() {
  const heatmapRef = useRef(null);

  const handleCreated = (args) => {
    console.log('HeatMap initialization complete');
    console.log('Axes:', {
      xAxisLabels: heatmapRef.current.xAxis.labels,
      yAxisLabels: heatmapRef.current.yAxis.labels
    });
  };

  return (
    <HeatMapComponent
      ref={heatmapRef}
      id='heatmap'
      dataSource={data}
      created={handleCreated}
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

### Multi-Event Handler

```jsx
import { useState } from 'react';

export function EventLogger() {
  const [events, setEvents] = useState([]);

  const logEvent = (eventName, details) => {
    const timestamp = new Date().toLocaleTimeString();
    setEvents(prev => [...prev.slice(-9), {
      timestamp,
      event: eventName,
      details
    }]);
  };

  return (
    <div>
      <HeatMapComponent
        id='heatmap'
        dataSource={data}
        cellClick={(args) => {
          logEvent('cellClick', `[${args.row}, ${args.column}]`);
        }}
      >
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>

      <div style={{ marginTop: '20px', maxHeight: '200px', overflow: 'auto', border: '1px solid #ddd', padding: '10px' }}>
        <h4>Event Log:</h4>
        {events.map((e, idx) => (
          <div key={idx} style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>
            [{e.timestamp}] {e.event}: {e.details}
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Rendering Mode Switching

### Automatic Switching

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={largeData}  // 1000+ cells
  renderingMode='Auto'    // Automatically chooses SVG or Canvas
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

**Auto behavior:**
- < 1000 cells → SVG (better styling)
- ≥ 1000 cells → Canvas (better performance)

### Manual Canvas Mode

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={veryLargeData}  // 10,000+ cells
  renderingMode='Canvas'      // Force Canvas for performance
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

**Canvas advantages:**
- Handles 10,000+ cells efficiently
- Single bitmap rendering
- Lower memory usage

**Canvas limitations:**
- Less detailed cell styling
- No direct CSS for cells
- Use `cellRender` event for customization

### SVG Mode with Performance Tips

```jsx
// For detailed styling with smaller datasets
<HeatMapComponent
  id='heatmap'
  dataSource={data}  // < 500 cells for best performance
  renderingMode='SVG'
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

## Custom Cell Rendering

### Basic Cell Rendering

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  cellRender={(args) => {
    // Modify cell content
    args.displayText = args.value + '%';
    
    // Conditional styling
    if (args.value > 80) {
      args.cellElement.style.fontWeight = 'bold';
    }
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Custom Icons/Emojis in Cells

```jsx
export function IconHeatmap() {
  const statusMap = {
    100: '✓✓',   // Excellent
    75: '✓',     // Good
    50: '~',     // Fair
    25: '✗'      // Poor
  };

  return (
    <HeatMapComponent
        id='heatmap'
        dataSource={data}
        cellRender={(args: ICellEventArgs) => {

            let icon = '?';

            if (typeof args.value === 'number') {
                for (const [thresholdStr, symbol] of Object.entries(statusMap)) {
                    const threshold = Number(thresholdStr);

                    if (args.value >= threshold) {
                        icon = symbol as string;
                        break;
                    }
                }
            }


            args.displayText = icon;
            args.heatmap.cellSettings.textStyle.size = '20px'
            args.heatmap.cellSettings.textStyle.textAlignment = 'Center'
        }}
    >
        <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

### Complex Cell Rendering with Data Lookup

```jsx
export function DataLookupHeatmap() {
  const data = [
    { row: 'Product A', column: 'Q1', value: 150, trend: 'up' },
    { row: 'Product A', column: 'Q2', value: 200, trend: 'up' },
    { row: 'Product B', column: 'Q1', value: 100, trend: 'down' }
  ];

  const trendIcons = { up: '📈', down: '📉', flat: '→' };

  return (
    <HeatMapComponent
      id='heatmap'
      dataSource={data}
      cellRender={(args) => {
        // Find the data item for this cell
        const item = data.find(d => 
          d.row === args.row && d.column === args.column
        );

        if (item) {
          const icon = trendIcons[item.trend];
          args.displayText = `${icon} ${item.value}`;
        }
      }}
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

## Data Binding Events

### After Data Bind

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  load={(args) => {
    console.log('Data loaded successfully');
    // Perform post-load operations
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Dynamic Data Updates

```jsx
import { useState, useRef } from 'react';

export function DynamicDataHeatmap() {
  const [data, setData] = useState(initialData);
  const heatmapRef = useRef(null);

  const updateData = (newData) => {
    setData(newData);
    
    if (heatmapRef.current) {
      // Refresh heatmap with new data
      heatmapRef.current.refresh();
    }
  };

  const handleRealTimeUpdate = () => {
    const updated = data.map(item => ({
      ...item,
      value: Math.floor(Math.random() * 100)
    }));
    
    updateData(updated);
  };

  return (
    <div>
      <button onClick={handleRealTimeUpdate}>Refresh Data</button>
      
      <HeatMapComponent
        ref={heatmapRef}
        id='heatmap'
        dataSource={data}
      >
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>
    </div>
  );
}
```

## Performance Optimization

### Large Dataset Handling

```jsx
export function OptimizedLargeHeatmap() {
  // Generate 10,000 cells
  const largeData = Array.from({ length: 100 }, (_, i) => 
    Array.from({ length: 100 }, () => Math.floor(Math.random() * 100))
  );

  return (
    <HeatMapComponent
      id='heatmap'
      dataSource={largeData}
      renderingMode='Canvas'           // Use Canvas, not SVG      
      showTooltip = {false}
      legendSettings={{
        visible: true                    // Keep legend
      }}
    >
      <Inject services={[Legend]} />
    </HeatMapComponent>
  );
}
```

### Lazy Loading Pattern

```jsx
import { useState, useEffect } from 'react';

export function LazyLoadHeatmap() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate async data loading
    const timer = setTimeout(() => {
      setData(generateData());
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <div>Loading heatmap...</div>;
  }

  return (
    <HeatMapComponent
      id='heatmap'
      dataSource={data}
      renderingMode='Canvas'
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}

function generateData() {
  const rows = 50;
  const cols = 50;
  const data = [];

  for (let i = 0; i < rows; i++) {
    const row = [];
    for (let j = 0; j < cols; j++) {
      row.push(Math.floor(Math.random() * 100));
    }
    data.push(row);
  }

  return data;
}
```

### Debounced Refresh

```jsx
import { useRef } from 'react';

export function DebouncedHeatmap() {
  const heatmapRef = useRef(null);
  const refreshTimeoutRef = useRef(null);

  const handleDataChange = (newData) => {
    // Clear previous timeout
    if (refreshTimeoutRef.current) {
      clearTimeout(refreshTimeoutRef.current);
    }

    // Debounce refresh by 500ms
    refreshTimeoutRef.current = setTimeout(() => {
      if (heatmapRef.current) {
        heatmapRef.current.dataSource = newData;
        heatmapRef.current.refresh();
      }
    }, 500);
  };

  return (
    <HeatMapComponent
      ref={heatmapRef}
      id='heatmap'
      dataSource={data}
      renderingMode='Canvas'
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

## Complete Advanced Example

```jsx
import { useRef, useState, useEffect } from 'react';
import { HeatMapComponent, Inject, Legend, Tooltip } from '@syncfusion/ej2-react-heatmap';

export function AdvancedHeatmap() {
  const heatmapRef = useRef(null);
  const [stats, setStats] = useState({
    cellsRendered: 0,
    renderTime: 0,
    eventCount: 0
  });

  const largeData = generateMatrixData(100, 100);

  useEffect(() => {
    const startTime = performance.now();

    return () => {
      const endTime = performance.now();
      setStats(prev => ({
        ...prev,
        renderTime: (endTime - startTime).toFixed(2)
      }));
    };
  }, []);

  const handleCellClick = (args) => {
    setStats(prev => ({
      ...prev,
      eventCount: prev.eventCount + 1
    }));
  };

  return (
    <div>
      <div style={{ marginBottom: '20px', padding: '10px', background: '#f0f0f0' }}>
        <h3>Performance Stats</h3>
        <p>Render Time: {stats.renderTime}ms</p>
        <p>Events Handled: {stats.eventCount}</p>
      </div>

      <HeatMapComponent
        ref={heatmapRef}
        id='heatmap'
        dataSource={largeData}
        renderingMode='Canvas'
        cellClick={handleCellClick}
        cellRender={(args) => {
          if (args.value > 75) {
            args.displayText = '●';
          }
        }}
      >
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>
    </div>
  );
}

function generateMatrixData(rows, cols) {
  const data = [];
  for (let i = 0; i < rows * cols; i++) {
    data.push(Math.floor(Math.random() * 100));
  }
  return data;
}
```
