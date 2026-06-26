# Interaction & Selection

## Table of Contents

- [Selection Modes](#selection-modes)
  - [Single Cell Selection](#single-cell-selection)
  - [Selection](#selection)
  - [No Selection](#no-selection)
- [Cell Selection Handler](#cell-selection-handler)
  - [Track Selected Cell](#track-selected-cell)
  - [Get Row/Column Labels](#get-rowcolumn-labels)
- [Highlighting Patterns](#highlighting-patterns)
  - [Highlight Selected Cell](#highlight-selected-cell)
  - [Highlight Row/Column Group](#highlight-rowcolumn-group)
  - [Custom Highlight Color](#custom-highlight-color)
- [Tooltip Configuration](#tooltip-configuration)
  - [Enable Tooltips](#enable-tooltips)
  - [Disable Tooltips](#disable-tooltips)
  - [Custom Tooltip Format](#custom-tooltip-format)
  - [Advanced Tooltip Customization](#advanced-tooltip-customization)
  - [Tooltip Styling](#tooltip-styling)
- [Mouse Events](#mouse-events)
  - [Cell Click Event](#cell-click-event)
  - [Cell Mouse Hover](#cell-mouse-hover)
- [Interactive Patterns](#interactive-patterns)
  - [Pattern 1: Click to Filter Data](#pattern-1-click-to-filter-data)
  - [Pattern 2: Double-Click to Edit](#pattern-2-double-click-to-edit)
  - [Pattern 3: Drill-Down Navigation](#pattern-3-drill-down-navigation)
  - [Pattern 4: Export Selected Data](#pattern-4-export-selected-data)

## Selection Modes

### Single Cell Selection

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  cellSelected={(args) => {
    console.log(`Selected: [${args.row}, ${args.column}] = ${args.value}`);
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

Users can click any cell; the `cellSelected` event fires with cell information.

### Selection

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  allowSelection={true}
  cellSelected={(args) => {
    console.log(`Column ${args.column} selected`);
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### No Selection

```jsx
<HeatMapComponent
    id='heatmap'
    dataSource={data}
    allowSelection={false}  // Disable selection
>
    <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

## Cell Selection Handler

### Track Selected Cell

```jsx
import { useState } from 'react';

export function SelectionTracker() {
  const [selectedCell, setSelectedCell] = useState(null);

  const handleCellSelection = (args) => {
    setSelectedCell({
      row: args.row,
      column: args.column,
      value: args.value
    });
  };

  return (
    <div>
      <HeatMapComponent
        id='heatmap'
        dataSource={data}
        cellSelected={handleCellSelection}
      >
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>

      {selectedCell && (
        <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ddd' }}>
          <h3>Selected Cell Info</h3>
          <p>Row: {selectedCell.row}</p>
          <p>Column: {selectedCell.column}</p>
          <p>Value: {selectedCell.value}</p>
        </div>
      )}
    </div>
  );
}
```

### Get Row/Column Labels

```jsx
import { useRef } from 'react';

export function LabeledSelection() {
  const heatmapRef = useRef(null);

  const handleCellSelection = (args) => {
    const heatmap = heatmapRef.current;
    
    // Get axis labels
    const xLabel = heatmap.xAxis.labels[args.column];
    const yLabel = heatmap.yAxis.labels[args.row];

    console.log(`Selected: ${yLabel} (${xLabel}) = ${args.value}`);
  };

  return (
    <HeatMapComponent
      ref={heatmapRef}
      id='heatmap'
      dataSource={data}
      xAxis={{ labels: ['Q1', 'Q2', 'Q3', 'Q4'] }}
      yAxis={{ labels: ['Region A', 'Region B', 'Region C'] }}
      cellSelected={handleCellSelection}
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

## Highlighting Patterns

### Highlight Selected Cell

```jsx
import { useState } from 'react';

export function HighlightedSelection() {
  const [highlighted, setHighlighted] = useState(null);

  const handleCellSelection = (args) => {
    setHighlighted({
      row: args.row,
      column: args.column
    });
  };

  return (
    <HeatMapComponent
      id='heatmap'
      dataSource={data}
      cellSelected={handleCellSelection}
      cellRender={(args) => {
        // Add highlight styling
        if (highlighted && 
            highlighted.row === args.row && 
            highlighted.column === args.column) {
          args.cellElement.style.border = '3px solid black';
          args.cellElement.style.boxShadow = '0 0 8px rgba(0, 0, 0, 0.5)';
        }
      }}
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

### Highlight Row/Column Group

```jsx
export function GroupHighlight() {
  const [selectedRow, setSelectedRow] = useState(null);

  const handleCellSelection = (args) => {
    setSelectedRow(args.row);
  };

  return (
    <HeatMapComponent
      id='heatmap'
      dataSource={data}
      cellSelected={handleCellSelection}
      cellRender={(args) => {
        // Highlight entire row if row selected
        if (selectedRow === args.row) {
          args.cellElement.style.opacity = '1';
          args.cellElement.style.borderWidth = '2px';
        } else {
          args.cellElement.style.opacity = '0.5';  // Dim other rows
        }
      }}
    >
      <Inject services={[Legend, Tooltip]} />
    </HeatMapComponent>
  );
}
```

### Custom Highlight Color

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  cellRender={(args) => {
    // Custom highlight for high values
    if (args.value > 80) {
      args.cellElement.style.boxShadow = 'inset 0 0 0 2px #ff6b6b';
      args.cellElement.style.fontWeight = 'bold';
    }
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

## Tooltip Configuration

### Enable Tooltips

```jsx
import { Tooltip } from '@syncfusion/ej2-react-heatmap';

<HeatMapComponent id='heatmap' dataSource={data}>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

Tooltips show by default on cell hover.

### Disable Tooltips

```jsx
<HeatMapComponent 
  id='heatmap' 
  dataSource={data}
  showTooltip={false}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Custom Tooltip Format

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  tooltipSettings={{
   template: 'Value: ${value}'  // ${value}, ${row}, ${column}
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Advanced Tooltip Customization

```jsx
export function CustomTooltip() {
  const data = [
    { row: 'Product A', column: 'Q1', value: 150, status: 'Good' },
    { row: 'Product A', column: 'Q2', value: 200, status: 'Excellent' },
    { row: 'Product B', column: 'Q1', value: 100, status: 'Fair' }
  ];

  return (
      <HeatMapComponent
          id='heatmap'
          dataSource={data}
          dataSourceSettings={{ xDataMapping: 'column', yDataMapping: 'row', valueMapping: 'value' }}
          xAxis={{
              valueType: 'Category'
          }}
          yAxis={{
              valueType: 'Category'
          }}
          tooltipRender={(args) => {
              // Get the data item
              const item = data.find(d =>
                  d.row === args.content.row &&
                  d.column === args.content.column
              );

              // Custom tooltip content
              args.content = `
          <div style="padding: 10px;">
            <strong>${item.row}</strong> - ${item.column}<br/>
            Value: ${item.value}<br/>
            Status: <span style="color: ${item.status === 'Good' ? 'green' : 'orange'}">${item.status}</span>
          </div>
        `;
          }}
      >
          <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>
  );
}
```

### Tooltip Styling

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  tooltipSettings={{
    border: { width: 2, color: '#333' },
    textStyle: {
      size: '12px',
      color: '#fff'
    },
    template: 'tooltipTemplate'
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>

// In JSX, define template:
<div id='tooltipTemplate' style={{ display: 'none' }}>
  <div>
    <span style={{ color: 'red' }}>Value: ${value}</span>
  </div>
</div>
```

## Mouse Events

### Cell Click Event

```jsx
<HeatMapComponent
  id='heatmap'
  dataSource={data}
  cellClick={(args) => {
    console.log(`Clicked cell at [${args.row}, ${args.column}]`);
    // Perform custom action
    alert(`Value: ${args.value}`);
  }}
>
  <Inject services={[Legend, Tooltip]} />
</HeatMapComponent>
```

### Cell Mouse Hover

```jsx
export function HoverTracking() {
  const [hoveredCell, setHoveredCell] = useState(null);

  return (
    <div>
      <HeatMapComponent
        id='heatmap'
        dataSource={data}
        cellSelected={(args) => {
          setHoveredCell({
            row: args.row,
            column: args.column,
            value: args.value
          });
        }}
      >
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>

      {hoveredCell && (
        <div>
          <p>Hovering: {hoveredCell.value}</p>
        </div>
      )}
    </div>
  );
}
```

## Interactive Patterns

### Pattern 1: Click to Filter Data

```jsx
import { useState } from 'react';

export function FilterableHeatmap() {
  const [selectedRow, setSelectedRow] = useState(null);
  
  const allData = [
    { row: 'Product A', column: 'Q1', value: 150 },
    { row: 'Product A', column: 'Q2', value: 200 },
    { row: 'Product B', column: 'Q1', value: 100 },
    { row: 'Product B', column: 'Q2', value: 180 }
  ];

  const handleCellClick = (args) => {
    setSelectedRow(args.row);
  };

  const filteredData = selectedRow 
    ? allData.filter(d => d.row === selectedRow)
    : allData;

  return (
    <div>
      <HeatMapComponent
        id='heatmap'
        dataSource={filteredData}
        cellClick={handleCellClick}
      >
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>
      
      <div style={{ marginTop: '10px' }}>
        {selectedRow && (
          <button onClick={() => setSelectedRow(null)}>
            Clear Filter ({selectedRow})
          </button>
        )}
      </div>
    </div>
  );
}
```

### Pattern 2: Double-Click to Edit

```jsx
import { useState } from 'react';

export function EditableHeatmap() {
  const [data, setData] = useState([
    { row: 'A', column: 'X', value: 100 },
    { row: 'A', column: 'Y', value: 200 },
    { row: 'B', column: 'X', value: 150 }
  ]);

  const [editMode, setEditMode] = useState(null);
  const [newValue, setNewValue] = useState('');

  const handleDoubleClick = (args) => {
    setEditMode({ row: args.row, column: args.column });
    setNewValue(args.value);
  };

  const handleSave = () => {
    const updatedData = data.map(d => {
      if (d.row === editMode.row && d.column === editMode.column) {
        return { ...d, value: parseInt(newValue) };
      }
      return d;
    });
    
    setData(updatedData);
    setEditMode(null);
  };

  return (
    <div>
      <HeatMapComponent
        id='heatmap'
        dataSource={data}
        cellDoubleClick={handleDoubleClick}
      >
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>

      {editMode && (
        <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ddd' }}>
          <h4>Edit Value</h4>
          <input 
            type="number" 
            value={newValue}
            onChange={(e) => setNewValue(e.target.value)}
          />
          <button onClick={handleSave}>Save</button>
          <button onClick={() => setEditMode(null)}>Cancel</button>
        </div>
      )}
    </div>
  );
}
```

### Pattern 3: Drill-Down Navigation

```jsx
import { useState } from 'react';

export function DrillDownHeatmap() {
  const [level, setLevel] = useState('summary');  // 'summary' or 'detail'
  const [selectedCell, setSelectedCell] = useState(null);

  const summaryData = [
    { row: 'Region A', column: 'Q1', value: 500 },
    { row: 'Region B', column: 'Q1', value: 450 }
  ];

  const detailData = {
    'Region A-Q1': [
      { row: 'Product A', column: 'Jan', value: 150 },
      { row: 'Product B', column: 'Jan', value: 200 }
    ]
  };

  const handleCellClick = (args) => {
    const key = `${args.row}-${args.column}`;
    setSelectedCell(key);
    setLevel('detail');
  };

  const currentData = level === 'summary' 
    ? summaryData 
    : detailData[selectedCell];

  return (
    <div>
      <h3>{level === 'summary' ? 'Summary View' : 'Detail View'}</h3>
      
      <HeatMapComponent
        id='heatmap'
        dataSource={currentData}
        cellClick={handleCellClick}
      >
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>

      {level === 'detail' && (
        <button onClick={() => setLevel('summary')} style={{ marginTop: '10px' }}>
          Back to Summary
        </button>
      )}
    </div>
  );
}
```

### Pattern 4: Export Selected Data

```jsx
export function ExportableHeatmap() {
  const [selectedCells, setSelectedCells] = useState([]);

  const handleCellClick = (args) => {
    setSelectedCells([...selectedCells, {
      row: args.row,
      column: args.column,
      value: args.value
    }]);
  };

  const exportToCSV = () => {
    let csv = 'Row,Column,Value\n';
    
    selectedCells.forEach(cell => {
      csv += `${cell.row},${cell.column},${cell.value}\n`;
    });

    // Create download link
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'heatmap-data.csv';
    a.click();
  };

  return (
    <div>
      <HeatMapComponent
        id='heatmap'
        dataSource={data}
        cellClick={handleCellClick}
      >
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>

      <div style={{ marginTop: '15px' }}>
        <p>Selected cells: {selectedCells.length}</p>
        {selectedCells.length > 0 && (
          <button onClick={exportToCSV}>Export Selected as CSV</button>
        )}
      </div>
    </div>
  );
}
```
