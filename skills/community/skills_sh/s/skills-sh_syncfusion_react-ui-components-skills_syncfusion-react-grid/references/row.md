# Row Features in React Grid

## Table of Contents
- [Overview](#overview)
- [Row Templates](#row-templates)
- [Detail Templates](#detail-templates)
- [Row Operations](#row-operations)
- [Advanced Features](#advanced-features)

## Overview

Row features provide rich customization options including templates, drag-drop, pinning, spanning, and detail view expansion.

## Row Templates

### Custom Row Template

```tsx
const rowTemplate = (props) => {
  return (
    <tr>
      <td>{props.OrderID}</td>
      <td><strong>{props.CustomerID}</strong></td>
      <td style={{ color: props.Freight > 50 ? 'red' : 'green' }}>
        ${props.Freight.toFixed(2)}
      </td>
    </tr>
  );
};

<GridComponent dataSource={data} rowTemplate={rowTemplate}>
  {/* columns */}
</GridComponent>
```

## Detail Templates

### Expand/Collapse Detail View

```tsx
const detailTemplate = (props) => {
  return (
    <div style={{ padding: '20px', backgroundColor: '#f9f9f9' }}>
      <h4>Order Details for {props.OrderID}</h4>
      <p><strong>Customer:</strong> {props.CustomerID}</p>
      <p><strong>Employee:</strong> {props.EmployeeID}</p>
      <p><strong>Ship Country:</strong> {props.ShipCountry}</p>
      <p><strong>Freight:</strong> ${props.Freight}</p>
    </div>
  );
};

<GridComponent dataSource={data} detailTemplate={detailTemplate}>
  {/* columns */}
</GridComponent>
```

### Nested Grid in Detail View

```tsx
const detailTemplate = (props) => {
  const childData = getChildOrders(props.OrderID);

  return (
    <GridComponent dataSource={childData}>
      <ColumnsDirective>
        <ColumnDirective field='ProductCode' headerText='Product' width='150' />
        <ColumnDirective field='Quantity' headerText='Qty' width='100' />
        <ColumnDirective field='Price' headerText='Price' width='100' format='C2' />
      </ColumnsDirective>
    </GridComponent>
  );
};

<GridComponent detailTemplate={detailTemplate}>
  {/* columns */}
</GridComponent>
```

## Row Operations

### Row Drag and Drop

```tsx
import { GridComponent, Inject, RowDD } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} allowRowDragAndDrop={true}>
  <ColumnsDirective>
    {/* columns */}
  </ColumnsDirective>
  <Inject services={[RowDD]} />
</GridComponent>
```

### Row Pinning

Pin rows to keep them visible:

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective,  Inject, Page} from '@syncfusion/ej2-react-grids';
import { data } from './datasource';
import * as React from 'react';

function App() {
    const isRowPinned=(data)=>
    {
      if (data && data.Status === 'Open' && data.Priority === 'Critical') {
        return true;
      }
      return false;
    }
    return (<div className='control-pane'>
      <div className='control-section'>
        <GridComponent dataSource={data} allowPaging={true} pageSettings={ {pageSize:15} } height='200' isRowPinned={isRowPinned}>
          <ColumnsDirective>
            <ColumnDirective field='TaskID' headerText='Task ID' width={100} textAlign='Right' isPrimaryKey={true} />
            <ColumnDirective field='Title' headerText='Title' width={100} />
            <ColumnDirective field='Status' headerText='Status' width={100} />
            <ColumnDirective field='Assignee' headerText='Assignee' width={100} />
            <ColumnDirective field='Priority' headerText='Priority' width={100} />
          </ColumnsDirective>
          <Inject services={[Page]}/>
        </GridComponent>
      </div>
    </div>);
}
export default App;
```

### Row Spanning

Merge cells across rows:

```tsx
const queryCellInfo = (args) => {
  if (args.data.OrderID === 10248 && args.cell.index === 0) {
    args.rowSpan = 2;  // Span 2 rows
  }
};

<GridComponent queryCellInfo={queryCellInfo}>
  {/* columns */}
</GridComponent>
```

## Advanced Features

### Row Selection and Events

```tsx
const onRowSelected = (args) => {
  console.log('Selected row:', args.data);
  console.log('Row index:', args.rowIndex);
};

const onRowDeselected = (args) => {
  console.log('Deselected row:', args.data);
};

<GridComponent
  allowSelection={true}
  rowSelected={onRowSelected}
  rowDeselected={onRowDeselected}
>
  {/* columns */}
</GridComponent>
```

### Row Click Events

```tsx
const recordClick = (args) => {
  console.log('Row clicked:', args.rowData, args.rowIndex);
};

const recordDoubleClick = (args) => {
  console.log('Row double-clicked');
};

<GridComponent
  recordClick={recordClick}
  recordDoubleClick={recordDoubleClick}
>
  {/* columns */}
</GridComponent>
```

### Conditional Row Styling

Apply CSS classes based on row data:

```tsx
const rowDataBound = (args) => {
  if (args.data.Freight > 50) {
    args.row.classList.add('high-freight');
  } else {
    args.row.classList.add('low-freight');
  }
};

<GridComponent rowDataBound={rowDataBound}>
  {/* columns */}
  <style>{`
    .high-freight { background-color: #ffcccc; }
    .low-freight { background-color: #ccffcc; }
  `}</style>
</GridComponent>
```

### Get Row by Index

```tsx
const getRowData = (rowIndex) => {
  const rowElement = gridRef.current.getRowByIndex(rowIndex);
  return rowElement?.data;
};
```

### Row Height Configuration

```tsx
<GridComponent
  dataSource={data}
  rowHeight={32}  // Compact
>
  {/* columns */}
</GridComponent>
```

### Hide Rows

```tsx
const rowDataBound = (args) => {
  if (args.data.Archived === true) {
    args.row.style.display = 'none';
  }
};

<GridComponent rowDataBound={rowDataBound}>
  {/* columns */}
</GridComponent>
```

```tsx
const onRowDeselected = (args) => {
  console.log('Deselected row:', args.data);
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

### Programmatically Select Rows

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const selectAllRows = () => {
    gridRef.current.selectAll();
  };

  const clearRowSelection = () => {
    gridRef.current.clearSelection();
  };

  return (
    <div>
      <button onClick={selectAllRows}>Select All</button>
      <button onClick={clearRowSelection}>Clear Selection</button>

      <GridComponent ref={gridRef} dataSource={data} allowSelection={true}>
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default App;
```

### Row CSS Classes

Apply CSS classes to rows:

```tsx
const rowDataBound = (args) => {
  if (args.data.Freight > 50) {
    args.row.classList.add('high-freight');
  } else {
    args.row.classList.add('low-freight');
  }
};

<GridComponent rowDataBound={rowDataBound}>
  {/* columns */}
  <style>{`
    .high-freight { background-color: #ffcccc; }
    .low-freight { background-color: #ccffcc; }
  `}</style>
</GridComponent>
```

### Get Row by Index

```tsx
const getRowData = (rowIndex) => {
  const rowElement = gridRef.current.getRowByIndex(rowIndex);
  return rowElement?.data;
};
```

### Handle Row Events

```tsx
const onQueryCellInfo = (args) => {
  if (args.data.Freight > 100) {
    args.cell.style.backgroundColor = '#ffe6e6';
  }
};

<GridComponent querycellInfo={onQueryCellInfo}>
  {/* columns */}
</GridComponent>
```
