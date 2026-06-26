# Sorting in React Grid

## Table of Contents
- [Overview](#overview)
- [Enable Sorting](#enable-sorting)
- [Sort Configuration](#sort-configuration)
- [Initial Sorting](#initial-sorting)
- [Multi-Column Sorting](#multi-column-sorting)
- [Custom Sorting](#custom-sorting)
- [Prevent Sorting](#prevent-sorting)

## Overview

Sorting enables users to arrange data in ascending or descending order by clicking column headers. It supports single-column and multi-column sorting with custom sort logic.

## Enable Sorting

### Basic Sorting Setup

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Sort } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} allowSorting={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
  <Inject services={[Sort]} />
</GridComponent>
```

### Without Module Injection

Sort functionality requires module injection:

```tsx
// ❌ Clicking headers won't sort
<GridComponent dataSource={data} allowSorting={true}>
  {/* columns */}
</GridComponent>

// ✅ Correct approach
<GridComponent dataSource={data} allowSorting={true}>
  {/* columns */}
  <Inject services={[Sort]} />
</GridComponent>
```

## Sort Configuration

### Configure Sort Settings

```tsx
const sortSettings = {
  columns: [
    { field: 'OrderID', direction: 'Ascending' }
  ],
  allowUnsort: true  // Allow removing sort by clicking again
};

<GridComponent dataSource={data} sortSettings={sortSettings} allowSorting={true}>
  {/* columns */}
  <Inject services={[Sort]} />
</GridComponent>
```

## Initial Sorting

Apply default sort order on grid load:

```tsx
const sortSettings = {
  columns: [
    { field: 'OrderDate', direction: 'Descending' },
    { field: 'Freight', direction: 'Ascending' }
  ]
};

<GridComponent
  dataSource={data}
  sortSettings={sortSettings}
  allowSorting={true}
>
  {/* columns */}
  <Inject services={[Sort]} />
</GridComponent>
```

### Sort Direction Options

```tsx
// Ascending (A → Z, 0 → 9)
{ field: 'CustomerID', direction: 'Ascending' }

// Descending (Z → A, 9 → 0)
{ field: 'Freight', direction: 'Descending' }
```

## Multi-Column Sorting

Enable sorting by multiple columns using Ctrl+Click:

```tsx
<GridComponent
  dataSource={data}
  allowSorting={true}
  allowMultiSorting={true}  // Enable multi-column sort
>
  <ColumnsDirective>
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='OrderDate' headerText='Order Date' width='130' type='date' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
  <Inject services={[Sort]} />
</GridComponent>
```

### Set Initial Multi-Column Sort

```tsx
const sortSettings = {
  columns: [
    { field: 'ShipCountry', direction: 'Ascending' },
    { field: 'CustomerID', direction: 'Ascending' },
    { field: 'Freight', direction: 'Descending' }
  ]
};

<GridComponent
  dataSource={data}
  sortSettings={sortSettings}
  allowSorting={true}
  allowMultiSorting={true}
>
  {/* columns */}
  <Inject services={[Sort]} />
</GridComponent>
```

## Custom Sorting

### Custom Comparer

Implement custom sort logic:

```tsx
const customSort = (data1, data2) => {
  // Custom comparison logic
  // Return: positive (ascending), negative (descending), 0 (equal)
  return data1.Freight > data2.Freight ? 1 : -1;
};

<ColumnDirective
  field='Freight'
  headerText='Freight'
  sortComparer={customSort}
  width='100'
/>
```

### Complex Custom Sorting

```tsx
const customComparer = (data1, data2) => {
  const val1 = data1.ShipCountry.toLowerCase();
  const val2 = data2.ShipCountry.toLowerCase();

  if (val1 < val2) return -1;
  if (val1 > val2) return 1;
  return 0;
};

<ColumnDirective
  field='ShipCountry'
  sortComparer={customComparer}
/>
```

## Prevent Sorting

### Disable Sorting for Specific Column

```tsx
// Disable sorting for Customer ID column
<ColumnDirective
  field='CustomerID'
  headerText='Customer'
  allowSorting={false}
  width='120'
/>
```

### Programmatic Sort Control

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const applySorting = () => {
    gridRef.current.sortColumn('OrderID', 'Ascending');
  };

  const clearSorting = () => {
    gridRef.current.clearSorting();
  };

  return (
    <div>
      <button onClick={applySorting}>Sort by Order ID</button>
      <button onClick={clearSorting}>Clear Sort</button>

      <GridComponent ref={gridRef} dataSource={data} allowSorting={true}>
        {/* columns */}
        <Inject services={[Sort]} />
      </GridComponent>
    </div>
  );
}

export default App;
```

## Remote Sorting

### Enable Server-Side Sorting with DataManager

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

function GridWithRemoteSorting() {
  const data = new DataManager({
    url: 'url',
    adaptor: new UrlAdaptor()
  });

  return (
    <GridComponent
      dataSource={data}
      allowSorting={true}
      allowPaging={true}
      pageSettings={{ pageSize: 20 }}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='Freight' headerText='Freight' format='C2' />
      </ColumnsDirective>
      <Inject services={[Sort, Page]} />
    </GridComponent>
  );
}

export default GridWithRemoteSorting;
```

### Server Expectations for Sorting

When a user clicks to sort, the grid sends these parameters:

```
GET /api/orders?$orderby=OrderID%20asc&$skip=0&$take=20

Response:
{
  "result": [
    { "OrderID": 10248, "CustomerID": "VINET", ... },
    ...
  ],
  "count": 830
}
```

### Multi-Column Remote Sorting

```tsx
const sortSettings = {
  columns: [
    { field: 'ShipCountry', direction: 'Ascending' },
    { field: 'CustomerID', direction: 'Ascending' }
  ]
};

<GridComponent
  dataSource={remoteData}
  sortSettings={sortSettings}
  allowSorting={true}
  allowMultiSorting={true}
  pageSettings={{ pageSize: 20 }}
>
  {/* columns */}
  <Inject services={[Sort, Page]} />
</GridComponent>
```

### Handle Sort Events

```tsx
const onActionComplete = (args) => {
  console.log('Sort column:', args.column?.field);
  console.log('Sort direction:', args.direction);
};

const onActionBegin = (args) => {
  if (args.requestType === 'sorting') {
    console.log('Sorting initiated on server');
    console.log('Sort columns:', gridRef.current.sortSettings.columns);
  }
};

<GridComponent
  dataSource={data}
  allowSorting={true}
  actionComplete={onActionComplete}
  actionBegin={onActionBegin}
>
 {/* columns */}
  <Inject services={[Sort]} />
</GridComponent>
```

### Get Current Sort State

```tsx
const getCurrentSortOrder = () => {
  return gridRef.current.sortSettings.columns;
  // Returns: [{ field: 'OrderID', direction: 'Ascending' }]
};
```
