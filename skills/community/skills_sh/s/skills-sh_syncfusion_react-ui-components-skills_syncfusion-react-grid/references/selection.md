# Selection in React Grid

## Table of Contents
- [Overview](#overview)
- [Enable Selection](#enable-selection)
- [Selection Modes](#selection-modes)
- [Checkbox Selection](#checkbox-selection)
- [Programmatic Selection](#programmatic-selection)
- [Selection Events](#selection-events)

## Overview

Selection allows users to select rows, cells, or columns. It supports single and multiple selection modes with programmatic control.

## Enable Selection

### Basic Selection Setup

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} allowSelection={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
</GridComponent>
```

## Selection Modes

### Selection Types

| Type | Target | Default |
|------|--------|---------|
| `Row` | Entire rows | Yes |
| `Cell` | Individual cells | No |
| `Column` | Entire columns | No |

### Selection Mode Configuration

```tsx
const selectionSettings = {
  type: 'Multiple',  // Single or Multiple
  mode: 'Row'        // Row, Cell, or Column
};

<GridComponent
  dataSource={data}
  selectionSettings={selectionSettings}
  allowSelection={true}
>
  {/* columns */}
</GridComponent>
```

### Single Row Selection

```tsx
const selectionSettings = {
  type: 'Single',
  mode: 'Row'
};

<GridComponent selectionSettings={selectionSettings}>
  {/* columns */}
</GridComponent>
```

### Multiple Row Selection

```tsx
const selectionSettings = {
  type: 'Multiple',
  mode: 'Row'
};

<GridComponent selectionSettings={selectionSettings}>
  {/* columns */}
</GridComponent>
```

### Cell Selection

```tsx
const selectionSettings = {
  type: 'Multiple',
  mode: 'Cell'
};

<GridComponent selectionSettings={selectionSettings}>
  {/* columns */}
</GridComponent>
```

### Column Selection

```tsx
const selectionSettings = {
  type: 'Multiple',
  allowColumnSelection : true
};

<GridComponent selectionSettings={selectionSettings}>
  {/* columns */}
</GridComponent>
```

## Checkbox Selection

Enable checkboxes for row selection:

```tsx
<GridComponent dataSource={data} allowSelection={true}>
  <ColumnsDirective>
    <ColumnDirective type='checkbox' width='50' />  {/* Checkbox column */}
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
  </ColumnsDirective>
</GridComponent>
```

### Configure Checkbox Column

```tsx
<ColumnDirective
  type='checkbox'
  width='50'
  allowSorting={false}
  allowFiltering={false}
/>
```

## Programmatic Selection

### Select Rows Programmatically

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const selectRows = () => {
    gridRef.current.selectRows([0, 2, 4]);  // Select rows by index
  };

  const selectByID = () => {
    gridRef.current.selectRows([10248, 10249]);  // Select by primary key
  };

  const clearSelection = () => {
    gridRef.current.clearSelection();
  };

  return (
    <div>
      <button onClick={selectRows}>Select Rows 0,2,4</button>
      <button onClick={selectByID}>Select by ID</button>
      <button onClick={clearSelection}>Clear Selection</button>

      <GridComponent ref={gridRef} dataSource={data} allowSelection={true}>
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default App;
```

### Get Selected Rows

```tsx
const getSelectedRows = () => {
  return gridRef.current.getSelectedRows();
};

const getSelectedRecords = () => {
  return gridRef.current.getSelectedRecords();
};
```

## Selection Events

### Handle Selection Change

```tsx
const onRowSelected = (args) => {
  console.log('Row selected:', args.data);
  console.log('Row index:', args.rowIndex);
};

const onRowDeselected = (args) => {
  console.log('Row deselected:', args.data);
};

<GridComponent
  dataSource={data}
  rowSelected={onRowSelected}
  rowDeselecting={onRowDeselected}
  allowSelection={true}
>
  {/* columns */}
</GridComponent>
```

### Cell Selection Event

```tsx
const onCellSelected = (args) => {
  console.log('Cell selected:', args.cellIndex);
  console.log('Row index:', args.rowIndex);
  console.log('Cell value:', args.data);
};

<GridComponent
  dataSource={data}
  cellSelected={onCellSelected}
  selectionSettings={{ mode: 'Cell' }}
  allowSelection={true}
>
  {/* columns */}
</GridComponent>
```

### Handle Selection on Actions

```tsx
const onActionComplete = (args) => {
  if (args.requestType === 'save') {
    // Clear selection after save
    gridRef.current.clearSelection();
  }
};

<GridComponent
  dataSource={data}
  actionComplete={onActionComplete}
  allowSelection={true}
>
  {/* columns */}
</GridComponent>
```

### Multi-Select with Checkbox

```tsx
const selectionSettings = {
  type: 'Multiple',
  mode: 'Row',
  checkboxOnly: true  // Select only via checkbox
};

<GridComponent
  dataSource={data}
  selectionSettings={selectionSettings}
  allowSelection={true}
>
  <ColumnsDirective>
    <ColumnDirective type='checkbox' width='50' />
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
  </ColumnsDirective>
</GridComponent>
```

## Advanced Selection Patterns

### Conditional Selection

```tsx
import React, { useRef } from 'react';

function GridWithConditionalSelection() {
  const gridRef = useRef(null);

  const onRowSelecting = (args) => {
    // Prevent selecting archived orders
    if (args.data.Status === 'Archived') {
      args.cancel = true;
      alert('Cannot select archived records');
    }
  };

  return (
    <GridComponent
      dataSource={data}
      allowSelection={true}
      rowSelecting={onRowSelecting}
    >
      {/* columns */}
    </GridComponent>
  );
}

export default GridWithConditionalSelection;
```

### Selection with Custom Styling

```tsx
function GridWithStyledSelection() {
  const [customSelection, setCustomSelection] = useState([]);

  const onRowSelected = (args) => {
    setCustomSelection(prev => [...prev, args.data.OrderID]);
    args.row.classList.add('custom-selected-row');
  };

  const onRowDeselected = (args) => {
    setCustomSelection(prev => prev.filter(id => id !== args.data.OrderID));
    args.row.classList.remove('custom-selected-row');
  };

  return (
    <div>
      <GridComponent
        dataSource={data}
        allowSelection={true}
        rowSelected={onRowSelected}
        rowDeselecting={onRowDeselected}
      >
        {/* columns */}
        <style>{`
          .custom-selected-row {
            background-color: #1976d2 !important;
            color: white;
          }
          .custom-selected-row td {
            color: white;
          }
        `}</style>
      </GridComponent>
    </div>
  );
}
```

### Select All / Deselect All

```tsx
import React, { useRef } from 'react';

function GridWithSelectAll() {
  const gridRef = useRef(null);

  const selectAll = () => {
    gridRef.current.selectAll();
  };

  const deselectAll = () => {
    gridRef.current.clearSelection();
  };

  const invertSelection = () => {
    const allRows = gridRef.current.getRows();
    const selectedIndices = gridRef.current.getSelectedRowIndexes();
    const indicesToSelect = allRows
      .map((_, i) => i)
      .filter(i => !selectedIndices.includes(i));
    
    gridRef.current.clearSelection();
    gridRef.current.selectRows(indicesToSelect);
  };

  return (
    <div>
      <button onClick={selectAll}>Select All</button>
      <button onClick={deselectAll}>Deselect All</button>
      <button onClick={invertSelection}>Invert Selection</button>

      <GridComponent
        ref={gridRef}
        dataSource={data}
        allowSelection={true}
        selectionSettings={{ type: 'Multiple' }}
      >
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default GridWithSelectAll;
```

### Selection Change Handler

```tsx
const onSelectionChanged = (args) => {
  const selectedIndexes = gridRef.current.getSelectedRowIndexes();
  const selectedRecords = gridRef.current.getSelectedRecords();

  console.log('Selected count:', selectedIndexes.length);
  console.log('Selected records:', selectedRecords);

  // Update UI
  const totalCount = gridRef.current.getCurrentViewRecords().length;
  const selectedCount = selectedIndexes.length;
  const allSelected = totalCount === selectedCount && totalCount > 0;

  console.log('All rows selected:', allSelected);
};

<GridComponent
  selectionSettings={{ type: 'Multiple' }}
  rowSelected={onSelectionChanged}
>
  {/* columns */}
</GridComponent>
```