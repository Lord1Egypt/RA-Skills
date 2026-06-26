# Searching in React Grid

## Table of Contents
- [Overview](#overview)
- [Search Functionality](#search-functionality)
- [Search Configuration](#search-configuration)
- [Search Events](#search-events)

## Overview

Search enables users to find records quickly by entering text that is matched against all columns. It's different from filtering as it searches across all fields simultaneously.

## Search Functionality

### Enable Search

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Search, Toolbar } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} toolbar={['Search']}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
  <Inject services={[Search, Toolbar]} />
</GridComponent>
```

### Programmatic Search

```tsx
import React, { useRef } from 'react';
import { GridComponent, Inject, Search } from '@syncfusion/ej2-react-grids';

function App() {
  const gridRef = useRef(null);

  const handleSearch = (searchValue) => {
    gridRef.current.search(searchValue);
  };

  return (
    <div>
      <input
        type='text'
        placeholder='Search...'
        onChange={(e) => handleSearch(e.target.value)}
      />

      <GridComponent ref={gridRef} dataSource={data}>
        {/* columns */}
        <Inject services={[Search]} />
      </GridComponent>
    </div>
  );
}

export default App;
```

## Search Configuration

### Case-Sensitive Search

```tsx
const handleSearch = (searchValue) => {
  const searchKey = gridRef.current.search;
  // Search is case-insensitive by default
  gridRef.current.search(searchValue); // Case-insensitive
};
```

### Clear Search

> **Only valid approach:** Pass an empty string to `search()`. Methods like `clearSearching()`, `clearSearch()`, or `resetSearch()` do **not** exist and will throw a runtime error.

```tsx
const clearSearch = () => {
  gridRef.current.search('');
};
```

## Search Events

### Handle Search Changes

```tsx
const onActionComplete = (args) => {
  if (args.requestType === 'searching') {
    console.log('Search completed');
    console.log('Filtered rows:', args.data?.length);
  }
};

<GridComponent
  dataSource={data}
  actionComplete={onActionComplete}
>
  {/* columns */}
</GridComponent>
```

## Advanced Search Features

### Column-Specific Search

```tsx
import React, { useState, useRef } from 'react';

function GridWithColumnSearch() {
  const gridRef = useRef(null);
  const [searchColumn, setSearchColumn] = useState('CustomerID');
  const [searchValue, setSearchValue] = useState('');

  const handleColumnSearch = (value) => {
    setSearchValue(value);
    gridRef.current.filterByColumn(searchColumn, 'contains', value, false);
  };

  return (
    <div>
      <select value={searchColumn} onChange={(e) => setSearchColumn(e.target.value)}>
        <option value='OrderID'>Order ID</option>
        <option value='CustomerID'>Customer</option>
        <option value='Freight'>Freight</option>
      </select>

      <input
        type='text'
        placeholder={`Search by ${searchColumn}...`}
        value={searchValue}
        onChange={(e) => handleColumnSearch(e.target.value)}
      />

      <GridComponent ref={gridRef} dataSource={data} allowFiltering={true}>
        {/* columns */}
        <Inject services={[Filter]} />
      </GridComponent>
    </div>
  );
}

export default GridWithColumnSearch;
```

### Search with Debouncing

```tsx
import React, { useState, useRef } from 'react';

function GridWithDebouncedSearch() {
  const gridRef = useRef(null);
  const debounceTimeoutRef = useRef(null);
  const [searchValue, setSearchValue] = useState('');

  const handleSearch = (value) => {
    setSearchValue(value);

    // Clear previous timeout
    if (debounceTimeoutRef.current) {
      clearTimeout(debounceTimeoutRef.current);
    }

    // Set new timeout
    debounceTimeoutRef.current = setTimeout(() => {
      gridRef.current.search(value);
    }, 300); // 300ms debounce delay
  };

  return (
    <div>
      <input
        type='text'
        placeholder='Search (debounced)...'
        value={searchValue}
        onChange={(e) => handleSearch(e.target.value)}
      />

      <GridComponent ref={gridRef} dataSource={data}>
        {/* columns */}
        <Inject services={[Search]} />
      </GridComponent>
    </div>
  );
}

export default GridWithDebouncedSearch;
```

### Search with Highlighting

```tsx
function GridWithSearchHighlight() {
  const [searchTerm, setSearchTerm] = useState('');

  const queryCellInfo = (args) => {
    if (args.cell.textContent.includes(searchTerm)) {
      args.cell.classList.add('highlight-search');
    } else {
      args.cell.classList.remove('highlight-search');
    }
  };

  const handleSearch = (value) => {
    setSearchTerm(value);
    gridRef.current.search(value);
  };

  return (
    <div>
      <input
        type='text'
        onChange={(e) => handleSearch(e.target.value)}
        placeholder='Search...'
      />

      <GridComponent
        ref={gridRef}
        dataSource={data}
        queryCellInfo={queryCellInfo}
      >
        {/* columns */}
        <style>{`
          .highlight-search {
            background-color: #ffeb3b;
            font-weight: bold;
          }
        `}</style>
      </GridComponent>
    </div>
  );
}

export default GridWithSearchHighlight;
```

### Search with Highlighting

```tsx
const handleSearch = (searchValue) => {
  gridRef.current.search(searchValue);

  // Add custom highlighting logic
  const cells = document.querySelectorAll('.e-grid .e-gridcell');
  cells.forEach(cell => {
    if (cell.textContent.toLowerCase().includes(searchValue.toLowerCase())) {
      cell.classList.add('search-highlight');
    } else {
      cell.classList.remove('search-highlight');
    }
  });
};
```
