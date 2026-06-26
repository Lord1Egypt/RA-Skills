# Printing in React Grid

## Table of Contents
- [Overview](#overview)
- [Basic Printing](#basic-printing)
- [Print Configuration](#print-configuration)
- [Print Customization](#print-customization)

## Overview

Print functionality allows users to print grid data with customizable templates, styling, and layout options.

## Basic Printing

### Enable Print

```tsx
import { GridComponent, Inject, Print } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} toolbar={['Print']}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
  <Inject services={[Toolbar, Print]} />
</GridComponent>
```

### Programmatic Print

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const printGrid = () => {
    gridRef.current.print();
  };

  return (
    <div>
      <button onClick={printGrid}>Print</button>

      <GridComponent ref={gridRef} dataSource={data}>
        {/* columns */}
        <Inject services={[Print]} />
      </GridComponent>
    </div>
  );
}

export default App;
```

## Print Configuration

### Print Specific Columns

```tsx
const printSettings = {
  columns: ['OrderID', 'CustomerID', 'Freight']
};

gridRef.current.print(printSettings);
```

### Print Selected Rows Only

```tsx
const printSelected = () => {
  const selectedRecords = gridRef.current.getSelectedRecords();
  gridRef.current.print({
    dataSource: selectedRecords
  });
};
```

### Print Filtered Data

```tsx
const printFiltered = () => {
  const filteredData = gridRef.current.getCurrentViewRecords();
  gridRef.current.print({
    dataSource: filteredData
  });
};
```

## Print Customization

### Custom Print Template

```tsx
const printTemplate = (props) => {
  return (
    <div className='print-container'>
      <h2>Orders Report</h2>
      <table>
        <tr>
          <th>Order ID</th>
          <th>Customer</th>
          <th>Freight</th>
        </tr>
        {props.map(row => (
          <tr key={row.OrderID}>
            <td>{row.OrderID}</td>
            <td>{row.CustomerID}</td>
            <td>${row.Freight.toFixed(2)}</td>
          </tr>
        ))}
      </table>
    </div>
  );
};

const printWithTemplate = () => {
  gridRef.current.print({
    theme: { borders: { borderWidth: 1 } }
  });
};
```

### Print Styling

```tsx
<GridComponent dataSource={data}>
  {/* columns */}
  <style>{`
    @media print {
      .e-grid {
        font-family: Arial, sans-serif;
      }
      .e-grid .e-table {
        border-collapse: collapse;
      }
      .e-grid .e-th, .e-grid .e-td {
        border: 1px solid #000;
        padding: 8px;
      }
      .no-print {
        display: none;
      }
    }
  `}</style>
</GridComponent>
```
