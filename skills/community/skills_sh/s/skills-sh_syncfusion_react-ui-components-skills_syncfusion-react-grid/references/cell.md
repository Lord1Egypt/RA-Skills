# Cell Features in React Grid

## Table of Contents
- [Overview](#overview)
- [Cell Selection](#cell-selection)
- [Cell Templates](#cell-templates)
- [Cell Formatting](#cell-formatting)
- [Cell Events](#cell-events)

## Overview

Cell-level operations provide granular control over individual cell display, editing, and interaction.

## Cell Selection

### Enable Cell Selection

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-grids';

const selectionSettings = {
  type: 'Multiple',
  mode: 'Cell'
};

<GridComponent
  dataSource={data}
  selectionSettings={selectionSettings}
  allowSelection={true}
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
  </ColumnsDirective>
</GridComponent>
```

### Get Selected Cells

```tsx
const getSelectedCells = () => {
  return gridRef.current.getSelectedRows();
};
```

## Cell Templates

### Custom Cell Template

```tsx
const cellTemplate = (props) => {
  return (
    <div>
      <strong>{props.CustomerID}</strong>
    </div>
  );
};

<ColumnDirective
  field='CustomerID'
  headerText='Customer'
  template={cellTemplate}
  width='120'
/>
```

### Conditional Cell Styling

```tsx
const cellTemplate = (props) => {
  const color = props.Freight > 50 ? 'red' : 'green';
  return (
    <span style={{ color, fontWeight: 'bold' }}>
      ${props.Freight.toFixed(2)}
    </span>
  );
};

<ColumnDirective field='Freight' template={cellTemplate} />
```

### Cell with Action Button

```tsx
const actionTemplate = (props) => {
  return (
    <div>
      <button onClick={() => viewDetails(props.OrderID)}>View</button>
      <button onClick={() => deleteRecord(props.OrderID)}>Delete</button>
    </div>
  );
};

<ColumnDirective
  headerText='Actions'
  template={actionTemplate}
  width='150'
/>
```

## Cell Formatting

### Number Formatting

```tsx
<ColumnDirective
  field='Freight'
  headerText='Freight'
  format='C2'  // Currency with 2 decimals
  textAlign='Right'
/>
```

### Date Formatting

```tsx
<ColumnDirective
  field='OrderDate'
  headerText='Order Date'
  type='date'
  format='yMd'  // Year-Month-Day
/>
```

### Percent Formatting

```tsx
<ColumnDirective
  field='Discount'
  headerText='Discount'
  format='P2'  // Percent with 2 decimals
  type='number'
/>
```

## Cell Events

### Cell Selected Event

```tsx
const cellSelected = (args) => {
  console.log('Cell index:', args.cellIndex);
  console.log('Row index:', args.rowIndex);
  console.log('Cell value:', args.data[args.column.field]);
};

<GridComponent
  dataSource={data}
  cellSelected={cellSelected}
  selectionSettings={{ mode: 'Cell' }}
>
  {/* columns */}
</GridComponent>
```

### Query Cell Info Event

```tsx
const queryCellInfo = (args) => {
  if (args.data.Freight > 100) {
    args.cell.style.backgroundColor = '#ffcccc';
    args.cell.style.color = '#cc0000';
  }
};

<GridComponent queryCellInfo={queryCellInfo}>
  {/* columns */}
</GridComponent>
```

### Cell Edit Event

```tsx
const onActionBegin = (args) => {
  if (args.requestType === 'save') {
    console.log('Cell edited:', args.data);
  }
};

<GridComponent
  dataSource={data}
  actionBegin={onActionBegin}
  editSettings={{ mode: 'Dialog' }}
>
  {/* columns */}
</GridComponent>
```

### Programmatic Cell Edit

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const editCell = (rowIndex, columnName) => {
    gridRef.current.startEdit({ rowIndex, columnName });
  };

  const saveCell = () => {
    gridRef.current.endEdit();
  };

  return (
    <div>
      <button onClick={() => editCell(0, 'CustomerID')}>Edit First Cell</button>
      <button onClick={saveCell}>Save</button>

      <GridComponent ref={gridRef} dataSource={data}>
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default App;
```

### Cell Value Change

```tsx
<ColumnDirective
  field='Freight'
  headerText='Freight'
  editTemplate={
    <input
      type='number'
      onChange={(e) => {
        console.log('Value changed:', e.target.value);
      }}
    />
  }
/>
```

## Advanced Cell Operations

### Cell-Level Validation

```tsx
function GridWithCellValidation() {
  const gridRef = useRef(null);

  const onActionBegin = (args) => {
    if (args.requestType === 'save') {
      const newData = args.data;

      // Validate Freight (must be > 0)
      if (newData.Freight && newData.Freight <= 0) {
        args.cancel = true;
        alert('Freight must be greater than 0');
        return;
      }

      // Validate CustomerID (must not be empty)
      if (!newData.CustomerID || newData.CustomerID.trim() === '') {
        args.cancel = true;
        alert('Customer ID is required');
        return;
      }
    }
  };

  return (
    <GridComponent
      ref={gridRef}
      dataSource={data}
      editSettings={{ mode: 'Dialog', allowEditing: true }}
      actionBegin={onActionBegin}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' isPrimaryKey={true} />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='Freight' headerText='Freight' format='C2' width='100' />
      </ColumnsDirective>
      <Inject services={[Edit]} />
    </GridComponent>
  );
}

export default GridWithCellValidation;
```

### Cell Styling Based on Values

```tsx
function GridWithConditionalStyling() {
  const queryCellInfo = (args) => {
    if (args.column.field === 'Freight') {
      const freight = args.data.Freight;

      if (freight > 100) {
        // High value - red
        args.cell.style.backgroundColor = '#ffcccc';
        args.cell.style.color = '#cc0000';
        args.cell.style.fontWeight = 'bold';
      } else if (freight > 50) {
        // Medium value - yellow
        args.cell.style.backgroundColor = '#fff9c4';
        args.cell.style.color = '#f57f17';
      } else {
        // Low value - green
        args.cell.style.backgroundColor = '#c8e6c9';
        args.cell.style.color = '#2e7d32';
      }
    }

    if (args.column.field === 'OrderDate') {
      const orderDate = new Date(args.data.OrderDate);
      const today = new Date();
      const daysDiff = Math.floor((today - orderDate) / (1000 * 60 * 60 * 24));

      if (daysDiff > 365) {
        args.cell.style.opacity = '0.6'; // Old order
      }
    }
  };

  return (
    <GridComponent
      dataSource={data}
      queryCellInfo={queryCellInfo}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='Freight' headerText='Freight' format='C2' width='100' />
        <ColumnDirective field='OrderDate' headerText='Order Date' type='date' format='yMd' width='120' />
      </ColumnsDirective>
    </GridComponent>
  );
}

export default GridWithConditionalStyling;
```

### Custom Cell Templates with Buttons

```tsx
function GridWithActionCells() {
  const gridRef = useRef(null);

  const actionTemplate = (props) => {
    return (
      <div style={{ display: 'flex', gap: '5px' }}>
        <button
          onClick={() => {
            console.log('View:', props.OrderID);
            // Show details modal
          }}
          style={{
            padding: '4px 8px',
            background: '#1976d2',
            color: 'white',
            border: 'none',
            borderRadius: '3px',
            cursor: 'pointer',
            fontSize: '12px'
          }}
        >
          View
        </button>
        <button
          onClick={() => {
            gridRef.current.deleteRecord(props.OrderID);
          }}
          style={{
            padding: '4px 8px',
            background: '#d32f2f',
            color: 'white',
            border: 'none',
            borderRadius: '3px',
            cursor: 'pointer',
            fontSize: '12px'
          }}
        >
          Delete
        </button>
      </div>
    );
  };

  return (
    <GridComponent
      ref={gridRef}
      dataSource={data}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective headerText='Actions' template={actionTemplate} width='120' />
      </ColumnsDirective>
    </GridComponent>
  );
}

export default GridWithActionCells;
```

### Cell Range Selection and Operations

```tsx
function GridWithCellRangeOps() {
  const gridRef = useRef(null);
  const [selectedRange, setSelectedRange] = useState(null);

  const cellSelectionChange = (args) => {
    const selectedCells = gridRef.current.getSelectedRowCellIndexes();
    if (selectedCells.length > 0) {
      setSelectedRange(selectedCells);
    }
  };

  const sumSelectedCells = () => {
    if (!selectedRange) return;

    let sum = 0;
    selectedRange.forEach(index => {
      const record = gridRef.current.getCurrentViewRecords()[index.rowIndex];
      if (record && record.Freight) {
        sum += record.Freight;
      }
    });

    alert(`Sum of selected freight: $${sum.toFixed(2)}`);
  };

  return (
    <div>
      <button onClick={sumSelectedCells} style={{ marginBottom: '10px' }}>
        Sum Selected Cells
      </button>
      <GridComponent
        ref={gridRef}
        dataSource={data}
        selectionSettings={{ type: 'Multiple', mode: 'Cell' }}
        cellSelected={cellSelectionChange}
        allowSelection={true}
      >
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
          <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
          <ColumnDirective field='Freight' headerText='Freight' format='C2' width='100' />
        </ColumnsDirective>
      </GridComponent>
    </div>
  );
}

export default GridWithCellRangeOps;
```

### Cell Editing with Custom Dropdown

```tsx
function GridWithDropdownCell() {
  const statuses = ['Pending', 'Confirmed', 'Shipped', 'Delivered'];

  const statusTemplate = (props) => {
    return <span className={`status-${props.Status?.toLowerCase()}`}>{props.Status}</span>;
  };

  const statusEditTemplate = (props) => {
    return (
      <select value={props.Status} style={{ width: '100%', padding: '8px' }}>
        {statuses.map(status => (
          <option key={status} value={status}>{status}</option>
        ))}
      </select>
    );
  };

  return (
    <GridComponent
      dataSource={data}
      editSettings={{ mode: 'Dialog', allowEditing: true }}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' isPrimaryKey={true} />
        <ColumnDirective
          field='Status'
          headerText='Status'
          width='120'
          template={statusTemplate}
          editTemplate={statusEditTemplate}
        />
      </ColumnsDirective>
      <Inject services={[Edit]} />
    </GridComponent>
  );
}

export default GridWithDropdownCell;
```
