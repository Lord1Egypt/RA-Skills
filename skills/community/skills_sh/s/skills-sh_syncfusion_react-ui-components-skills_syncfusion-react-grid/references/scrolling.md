# Scrolling in React Grid

## Table of Contents
- [Overview](#overview)
- [Standard Scrolling](#standard-scrolling)
- [Virtual Scrolling](#virtual-scrolling)
- [Infinite Scrolling](#infinite-scrolling)
- [Configuration](#configuration)

## Overview

Scrolling modes determine how the grid handles large datasets. Options include standard, virtual, and infinite scrolling for optimal performance.

## Standard Scrolling

Default scrolling behavior:

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} height='400'>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
</GridComponent>
```

### Set Grid Height

```tsx
<GridComponent dataSource={data} height='500'>
  {/* columns */}
</GridComponent>
```

### Set Grid Width

```tsx
<GridComponent dataSource={data} width='100%' height='500'>
  {/* columns */}
</GridComponent>
```

## Virtual Scrolling

Load and render only visible rows for large datasets (10,000+ rows). Requires `VirtualScroll` module:

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, VirtualScroll } from '@syncfusion/ej2-react-grids';

<GridComponent
  dataSource={largeData}
  enableVirtualization={true}
  height='500'
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
  <Inject services={[VirtualScroll]} />
</GridComponent>
```

### Virtual Scrolling with Grouping

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, VirtualScroll, Group } from '@syncfusion/ej2-react-grids';

<GridComponent
  dataSource={data}
  enableVirtualization={true}
  allowGrouping={true}
  height='500'
>
  {/* columns */}
  <Inject services={[VirtualScroll, Group]} />
</GridComponent>
```

## Infinite Scrolling

Load data on demand as user scrolls. Requires `InfiniteScroll` module:

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, InfiniteScroll } from '@syncfusion/ej2-react-grids';

<GridComponent
  dataSource={remoteDataManager}
  enableInfiniteScrolling={true}
  infiniteScrollSettings={{ enableCache: true }}
  pageSettings={{ pageSize: 50 }}
  height='500'
>
  {/* columns */}
  <Inject services={[InfiniteScroll]} />
</GridComponent>
```

### Infinite Scrolling Configuration

```tsx
const infiniteScrollSettings = {
  enableCache: true,     // Cache loaded data
  maxBlocks: 5,          // Maximum rows to keep in memory
  initialBlocks: 1       // Initial data blocks to load
};

<GridComponent
  dataSource={remoteDataManager}
  enableInfiniteScrolling={true}
  infiniteScrollSettings={infiniteScrollSettings}
  pageSettings={{ pageSize: 50 }}
>
  {/* columns */}
</GridComponent>
```

## Configuration

### Scrollbar Styling

```tsx
<GridComponent dataSource={data} height='500'>
  {/* columns */}
  <style>{`
    .e-grid .e-gridscroll {
      scrollbar-width: thin;
      scrollbar-color: #888 #f1f1f1;
    }
    .e-grid .e-gridscroll::-webkit-scrollbar {
      width: 8px;
    }
    .e-grid .e-gridscroll::-webkit-scrollbar-track {
      background: #f1f1f1;
    }
    .e-grid .e-gridscroll::-webkit-scrollbar-thumb {
      background: #888;
      border-radius: 4px;
    }
  `}</style>
</GridComponent>
```

### Performance Tuning Guide

Optimize scrolling for different dataset sizes:

```tsx
// For 1,000 - 10,000 rows: Use Pagination
<GridComponent
  dataSource={data}
  allowPaging={true}
  pageSettings={{ pageSize: 50 }}
/>

// For 10,000 - 100,000 rows: Use Virtual Scrolling  
<GridComponent
  dataSource={data}
  enableVirtualization={true}
  height='500'
  pageSettings={{ pageSize: 100 }}
/>

// For 100,000+ rows: Use Infinite Scrolling
<GridComponent
  dataSource={remoteData}
  enableInfiniteScrolling={true}
  pageSettings={{ pageSize: 200 }}
/>
```

### Virtual Scrolling Limitations

Virtual scrolling is incompatible with:
- Grouping with virtualization
- Batch editing
- Print functionality
- Server-side operations with aggregates

For these scenarios, use Pagination or Lazy Grouping instead.

### Scroll to Row

```tsx
import React, { useRef } from 'react';

function GridWithScrollNavigation() {
  const gridRef = useRef(null);

  const scrollToRow = (rowIndex) => {
    const row = gridRef.current.getRowByIndex(rowIndex);
    if (row) {
      row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  };

  const scrollToCell = (rowIndex, columnIndex) => {
    const cell = gridRef.current.getCellFromIndex(rowIndex, columnIndex);
    if (cell) {
      cell.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  };

  const scrollToTop = () => {
    const contentDiv = gridRef.current.getContent();
    contentDiv.scrollTop = 0;
  };

  const scrollToBottom = () => {
    const contentDiv = gridRef.current.getContent();
    contentDiv.scrollTop = contentDiv.scrollHeight;
  };

  return (
    <div>
      <button onClick={() => scrollToRow(0)}>Go to First Row</button>
      <button onClick={() => scrollToRow(100)}>Go to Row 100</button>
      <button onClick={() => scrollToCell(50, 2)}>Go to Row 50, Col 2</button>
      <button onClick={scrollToTop}>Scroll to Top</button>
      <button onClick={scrollToBottom}>Scroll to Bottom</button>

      <GridComponent ref={gridRef} dataSource={data} height='500'>
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default GridWithScrollNavigation;
```

### Frozen Columns with Scrolling

```tsx
<GridComponent dataSource={data} height='500'>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' isFrozen={true} />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
    {/* more columns that will scroll */}
  </ColumnsDirective>
  <Inject services={[Freeze]} />
</GridComponent>
```