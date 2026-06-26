# Clipboard Operations in React Grid

## Table of Contents
- [Overview](#overview)
- [Copy and Paste](#copy-and-paste)
- [Clipboard Events](#clipboard-events)
- [Advanced Operations](#advanced-operations)

## Overview

Clipboard operations enable copying and pasting data between the grid and external applications.

## Copy and Paste

### Copy Selected Cell

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-grids';

// Select cell and press Ctrl+C to copy
<GridComponent
  dataSource={data}
  selectionSettings={{ mode: 'Cell', type: 'Multiple' }}
  allowSelection={true}
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
  </ColumnsDirective>
</GridComponent>
```

### Copy with Headers

```tsx
const contextMenuItems = [
  'Copy',           // Copy selected cells
  'CopyWithHeader'  // Copy with column headers
];

<GridComponent
  dataSource={data}
  contextMenuItems={contextMenuItems}
>
  {/* columns */}
  <Inject services={[ContextMenu]} />
</GridComponent>
```

### Programmatic Copy

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const copySelectedCells = () => {
    const selectedCells = gridRef.current.getSelectedRows();
    const text = selectedCells.map(cell => cell.toString()).join('\n');
    navigator.clipboard.writeText(text);
  };

  return (
    <div>
      <button onClick={copySelectedCells}>Copy</button>

      <GridComponent ref={gridRef} dataSource={data}>
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default App;
```

### Paste Data

```tsx
const handlePaste = (e) => {
  e.preventDefault();
  const clipboardData = e.clipboardData.getData('text');
  const rows = clipboardData.split('\n');

  rows.forEach(row => {
    const values = row.split('\t');
    // Process pasted data
    gridRef.current.addRecord({
      OrderID: values[0],
      CustomerID: values[1],
      Freight: parseFloat(values[2])
    });
  });
};

<GridComponent
  dataSource={data}
  beforePaste ={handlePaste}
>
  {/* columns */}
</GridComponent>
```

## Clipboard Events

### Before Copy Event

```tsx
const beforeCopy = (args) => {
  console.log('Copying:', args.data);
  // Modify clipboard data if needed
};

<GridComponent
  dataSource={data}
  beforeCopy={beforeCopy}
>
  {/* columns */}
</GridComponent>
```

## Advanced Operations

### Copy Full Row

```tsx
const copyFullRow = () => {
  const selectedRecord = gridRef.current.getSelectedRecords()[0];
  const rowText = Object.values(selectedRecord).join('\t');
  navigator.clipboard.writeText(rowText);
};
```

### Copy Filtered Data

```tsx
const copyFilteredData = () => {
  const filteredData = gridRef.current.getCurrentViewRecords();
  const csvData = filteredData.map(row =>
    Object.values(row).join(',')
  ).join('\n');
  navigator.clipboard.writeText(csvData);
};
```


### Copy with Formatting

```tsx
const copyFormattedData = () => {
  const selectedCells = gridRef.current.getSelectedRows();
  
  const formattedData = selectedCells.map(row => ({
    ...row,
    Freight: `$${row.Freight.toFixed(2)}`,
    OrderDate: row.OrderDate?.toLocaleDateString()
  }));

  const csv = [
    Object.keys(formattedData[0]).join(','),
    ...formattedData.map(row => Object.values(row).join(','))
  ].join('\n');

  navigator.clipboard.writeText(csv);
};
```

## Custom Clipboard Behavior

### Custom Copy Formatter

```tsx
function GridWithCustomCopy() {
  const gridRef = useRef(null);

  const beforeCopy = (args) => {
    // Format numbers with currency symbol
    const formattedData = args.data.map(row => ({
      ...row,
      Freight: new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(row.Freight)
    }));

    // Update args to use formatted data
    args.data = formattedData;
  };

  return (
    <GridComponent
      ref={gridRef}
      dataSource={data}
      selectionSettings={{ mode: 'Cell', type: 'Multiple' }}
      beforeCopy={beforeCopy}
      allowSelection={true}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='Freight' headerText='Freight' format='C2' width='100' />
      </ColumnsDirective>
    </GridComponent>
  );
}

export default GridWithCustomCopy;
```

### Copy with Headers

```tsx
function GridWithCopyHeaders() {
  const gridRef = useRef(null);

  const copyWithHeaders = () => {
    const columns = gridRef.current.getColumns();
    const columnNames = columns.map(col => col.field).join('\t');
    
    const selectedData = gridRef.current.getSelectedRecords();
    const dataRows = selectedData.map(row =>
      columns.map(col => row[col.field]).join('\t')
    ).join('\n');

    const fullText = `${columnNames}\n${dataRows}`;
    navigator.clipboard.writeText(fullText);
    alert('Data copied with headers!');
  };

  return (
    <div>
      <button onClick={copyWithHeaders} style={{ marginBottom: '10px' }}>
        Copy With Headers
      </button>
      <GridComponent
        ref={gridRef}
        dataSource={data}
        selectionSettings={{ mode: 'Row', type: 'Multiple' }}
        allowSelection={true}
      >
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
          <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
          <ColumnDirective field='Freight' headerText='Freight' width='100' />
        </ColumnsDirective>
      </GridComponent>
    </div>
  );
}

export default GridWithCopyHeaders;
```

### Smart Paste with Validation

```tsx
function GridWithSmartPaste() {
  const gridRef = useRef(null);
  const [pasteError, setPasteError] = useState('');

  const handlePaste = (e) => {
    e.preventDefault();
    setPasteError('');

    const clipboardData = e.clipboardData.getData('text');
    const rows = clipboardData.split('\n').filter(row => row.trim());

    try {
      const newRecords = [];

      for (const row of rows) {
        const [orderId, customerId, freight] = row.split('\t');

        // Validate data
        if (!orderId || !customerId || !freight) {
          throw new Error('Invalid data format. Expected: OrderID, CustomerID, Freight');
        }

        if (isNaN(freight)) {
          throw new Error(`Invalid freight value: ${freight}`);
        }

        newRecords.push({
          OrderID: parseInt(orderId),
          CustomerID: customerId.trim(),
          Freight: parseFloat(freight)
        });
      }

      // Add all valid records
      newRecords.forEach(record => {
        gridRef.current.addRecord(record);
      });

      alert(`Successfully pasted ${newRecords.length} records`);
    } catch (error) {
      setPasteError(`Paste error: ${error.message}`);
    }
  };

  return (
    <div>
      {pasteError && (
        <div style={{
          background: '#ffebee',
          color: '#c62828',
          padding: '10px',
          marginBottom: '10px',
          borderRadius: '4px'
        }}>
          {pasteError}
        </div>
      )}
      <div
        onPaste={handlePaste}
        style={{
          padding: '20px',
          background: '#f5f5f5',
          marginBottom: '10px',
          borderRadius: '4px',
          textAlign: 'center',
          color: '#666'
        }}
      >
        Paste data here (Tab-delimited format)
      </div>
      <GridComponent
        ref={gridRef}
        dataSource={data}
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

export default GridWithSmartPaste;
```

### Copy to CSV Format

```tsx
function GridWithCSVCopy() {
  const gridRef = useRef(null);

  const copyAsCSV = () => {
    const columns = gridRef.current.getColumns();
    const selectedRecords = gridRef.current.getSelectedRecords();

    // Create CSV-safe values
    const csvEscape = (value) => {
      if (value === null || value === undefined) return '';
      const stringValue = String(value);
      if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
        return `"${stringValue.replace(/"/g, '""')}"`;
      }
      return stringValue;
    };

    // Build CSV
    const headerRow = columns.map(col => csvEscape(col.headerText)).join(',');
    const dataRows = selectedRecords.map(record =>
      columns.map(col => csvEscape(record[col.field])).join(',')
    ).join('\n');

    const csv = `${headerRow}\n${dataRows}`;
    navigator.clipboard.writeText(csv);
    alert('Data copied as CSV!');
  };

  return (
    <div>
      <button onClick={copyAsCSV} style={{ marginBottom: '10px' }}>
        Copy as CSV
      </button>
      <GridComponent
        ref={gridRef}
        dataSource={data}
        selectionSettings={{ mode: 'Row', type: 'Multiple' }}
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

export default GridWithCSVCopy;
```

### Copy with Custom Formatting

```tsx
const beforeCopy = (args) => {
  // Add timestamp and metadata
  const timestamp = new Date().toLocaleString();
  const metadata = `\n\n--- Copied on ${timestamp} ---`;
  
  // Format each row
  args.data = args.data.map(row => ({
    OrderID: row.OrderID,
    Customer: row.CustomerID,
    Amount: `$${row.Freight.toFixed(2)}`,
    Date: new Date(row.OrderDate).toLocaleDateString()
  }));

  args.copiedData = JSON.stringify(args.data, null, 2) + metadata;
};
```
