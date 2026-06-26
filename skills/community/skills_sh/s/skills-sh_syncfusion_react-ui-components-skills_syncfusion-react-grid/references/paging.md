# Paging in React Grid

## Table of Contents
- [Overview](#overview)
- [Enable Paging](#enable-paging)
- [Paging Configuration](#paging-configuration)
- [Pager Customization](#pager-customization)
- [Page Events](#page-events)
- [Programmatic Control](#programmatic-control)

## Overview

Paging divides large datasets into manageable pages, improving load performance and user experience. It displays a specified number of records per page with navigation controls.

> **CSS Requirement:** The Pager (page number buttons, navigation arrows, page-size dropdown) relies on `@syncfusion/ej2-react-grids/styles/material3.css`. If this import is missing from your CSS file, the pager will render without any styling. Always include the full set of CSS imports — see [Getting Started CSS References](getting-started.md#css-references) for the complete list.

## Enable Paging

### Basic Paging Setup

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} allowPaging={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
  <Inject services={[Page]} />
</GridComponent>
```

### Without Module Injection

The `Page` module must be injected for paging to work. Without it, the pager will not render.

```tsx
// ❌ This won't work
<GridComponent dataSource={data} allowPaging={true}>
  {/* columns */}
</GridComponent>

// ✅ This will work
<GridComponent dataSource={data} allowPaging={true}>
  {/* columns */}
  <Inject services={[Page]} />
</GridComponent>
```

## Paging Configuration

### Configure Page Settings

```tsx
const pageSettings = {
  pageSize: 12,        // Records per page (default: 12)
  pageCount: 5,        // Pages to display in pager
  currentPage: 1,      // Currently active page
  pageSizes: [10, 20, 30, 40], // Page size options
  enableQueryString: true  // Include page in URL
};

<GridComponent dataSource={data} pageSettings={pageSettings} allowPaging={true}>
  {/* columns */}
  <Inject services={[Page]} />
</GridComponent>
```

### Change Page Size

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const changePageSize = (size) => {
    gridRef.current.pageSettings.pageSize = size;
  };

  return (
    <div>
      <button onClick={() => changePageSize(10)}>10 per page</button>
      <button onClick={() => changePageSize(20)}>20 per page</button>
      <button onClick={() => changePageSize(50)}>50 per page</button>

      <GridComponent ref={gridRef} dataSource={data} allowPaging={true}>
        {/* columns */}
        <Inject services={[Page]} />
      </GridComponent>
    </div>
  );
}
```

### Set Initial Page

```tsx
const pageSettings = {
  pageSize: 12,
  currentPage: 2  // Start on page 2
};

<GridComponent dataSource={data} pageSettings={pageSettings} allowPaging={true}>
  {/* columns */}
  <Inject services={[Page]} />
</GridComponent>
```

## Server-Side Paging

### Enable Server-Side Paging with DataManager

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

function GridWithServerPaging() {
  const data = new DataManager({
    url: 'url',
    adaptor: new UrlAdaptor()
  });

  return (
    <GridComponent
      dataSource={data}
      allowPaging={true}
      pageSettings={{ pageSize: 20 }}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='Freight' headerText='Freight' format='C2' />
      </ColumnsDirective>
      <Inject services={[Page]} />
    </GridComponent>
  );
}

export default GridWithServerPaging;
```

### Server Endpoint Expectations

The server should accept these parameters and return paginated results:

```
GET /api/orders?$skip=0&$take=20

Response:
{
  "result": [
    { "OrderID": 10248, "CustomerID": "VINET", ... },
    ...
  ],
  "count": 830  // Total records available
}
```

### Handle Paging Events

```tsx
const onActionComplete = (args) => {
  console.log('Current page:', args.currentPage);
};

const onActionBegin = (args) => {
  if (args.requestType === 'paging') {
    console.log('Navigating to page:', args.currentPage);
  }
};

<GridComponent
  dataSource={data}
  pageSettings={{ pageSize: 20 }}
  actionComplete={onActionComplete}
  actionBegin={onActionBegin}
  allowPaging={true}
>
  {/* columns */}
  <Inject services={[Page]} />
</GridComponent>
```

### Jump to Page Programmatically

```tsx
import React, { useRef } from 'react';

function GridWithPageNavigation() {
  const gridRef = useRef(null);

  const goToPage = (pageNumber) => {
    gridRef.current.pageSettings.currentPage = pageNumber;
  };

  const goToFirstPage = () => {
    goToPage(1);
  };

  const goToLastPage = () => {
    const totalPages = Math.ceil(
      gridRef.current.pageSettings.totalRecordsCount /
      gridRef.current.pageSettings.pageSize
    );
    goToPage(totalPages);
  };

  return (
    <div>
      <button onClick={goToFirstPage}>First Page</button>
      <button onClick={goToLastPage}>Last Page</button>
      <input
        type='number'
        placeholder='Go to page...'
        onChange={(e) => goToPage(parseInt(e.target.value))}
      />

      <GridComponent
        ref={gridRef}
        dataSource={data}
        allowPaging={true}
        pageSettings={{ pageSize: 20 }}
      >
        {/* columns */}
        <Inject services={[Page]} />
      </GridComponent>
    </div>
  );
}

export default GridWithPageNavigation;
```
};

<GridComponent dataSource={data} pageSettings={pageSettings} allowPaging={true}>
  {/* columns */}
</GridComponent>
```

## Pager Customization

### Custom Pager Template

```tsx
const pagerTemplate = () => {
  return (
    <div className='custom-pager'>
      <span>Showing page</span>
      <input type='text' />
      <span>of</span>
      <span>{/* total pages */}</span>
    </div>
  );
};

<GridComponent pagerTemplate={pagerTemplate}>
  {/* columns */}
</GridComponent>
```

### Hide Pager

```tsx
<GridComponent allowPaging={true} showPagerContainer={false}>
  {/* columns */}
</GridComponent>
```

### Pager Style Customization

```tsx
<GridComponent dataSource={data} allowPaging={true}>
  {/* columns */}
  <style>{`
    .e-gridpager {
      background-color: #f5f5f5;
    }
    .e-pagercontainer .e-pageritem.e-active {
      background-color: #007bff;
      color: white;
    }
  `}</style>
</GridComponent>
```

## Page Events

### Page Change Event

```tsx
const onActionComplete = (args) => {
  console.log('Page changed to:', args.currentPage);
  console.log('Page size:', args.pageSize);
};

<GridComponent dataSource={data} actionComplete={onActionComplete}>
  {/* columns */}
  <Inject services={[Page]} />
</GridComponent>
```

## Programmatic Control

### Navigate to Specific Page

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const goToPage = (pageNumber) => {
    gridRef.current.goToPage(pageNumber);
  };

  return (
    <div>
      <input type='number' id='pageInput' />
      <button onClick={() => goToPage(parseInt(pageInput.value))}>Go</button>

      <GridComponent ref={gridRef} dataSource={data} allowPaging={true}>
        {/* columns */}
        <Inject services={[Page]} />
      </GridComponent>
    </div>
  );
}

export default App;
```

### Get Current Page Info

```tsx
const getCurrentPageInfo = () => {
  const pageSettings = gridRef.current.pageSettings;
  return {
    currentPage: pageSettings.currentPage,
    pageSize: pageSettings.pageSize,
    totalRecords: gridRef.current.getCurrentViewRecords().length
  };
};
```

### Paging with Remote Data

```tsx
const pageSettings = {
  pageSize: 20,
  enableQueryString: true // Include page in URL query
};

<GridComponent
  dataSource={remoteDataManager}
  pageSettings={pageSettings}
  allowPaging={true}
>
  {/* columns */}
  <Inject services={[Page]} />
</GridComponent>
```

### Server-Side Paging

For large datasets, implement server-side paging:

```tsx
const handlePageChange = (args) => {
  // Send request to server with page number and size
  fetch(`/api/orders?page=${args.currentPage}&pageSize=${args.pageSize}`)
    .then(response => response.json())
    .then(data => {
      gridRef.current.setProperties({ dataSource: data });
    });
};
```
