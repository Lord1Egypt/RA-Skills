# Data Binding in React Grid

## Table of Contents
- [Overview](#overview)
- [Local Data Binding](#local-data-binding)
- [Remote Data Binding](#remote-data-binding)
- [DataManager Configuration](#datamanager-configuration)
- [Loading Indicators](#loading-indicators)
- [Handling Data Source Changes](#handling-data-source-changes)

## Overview

Data binding is the process of connecting the Grid component to a data source. The React Grid supports both local data (JavaScript arrays) and remote data (REST API services) through the DataManager component.

## ⚠️ Data Source Selection Rule — Choose the Right Approach

**Always default to local array data unless the prompt explicitly mentions a remote API, REST endpoint, or server-side data source.**

| Scenario | Use | How |
|----------|-----|-----|
| Prompt provides sample data, static list, or does NOT mention an API | **Local array** | `dataSource={data}` where `data` is a plain JS array |
| Prompt explicitly mentions REST API, remote endpoint, server-side, or URL | **DataManager** | `dataManager = new DataManager({ url: '...', adaptor: new UrlAdaptor() })` |

- ✅ **Local array**: Used when data is hardcoded, provided inline, or when no remote source is mentioned. No imports from `@syncfusion/ej2-data` needed.
- ✅ **DataManager**: Used **only** when the prompt explicitly mentions connecting to a REST API, remote URL, or server-side data source.
- ❌ **Never** use `DataManager` with a remote URL when the prompt asks for local/static data — it will cause data not to load because the URL does not exist.

## Local Data Binding

### Binding Array Data

The simplest way to bind data is to pass a JavaScript array to the `dataSource` property:

```tsx
import { ColumnDirective, ColumnsDirective, GridComponent } from '@syncfusion/ej2-react-grids';
import React from 'react';

const data = [
  { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 },
  { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61 },
  { OrderID: 10250, CustomerID: 'HANAR', Freight: 65.83 }
];

function App() {
  return (
    <GridComponent dataSource={data}>
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='Freight' headerText='Freight' width='120' format='C2' />
      </ColumnsDirective>
    </GridComponent>
  );
}

export default App;
```

### Dynamic Data Updates

Update grid data dynamically using state management:

```tsx
import { ColumnDirective, ColumnsDirective, GridComponent } from '@syncfusion/ej2-react-grids';
import React, { useState } from 'react';

function App() {
  const [gridData, setGridData] = useState([
    { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 }
  ]);

  const addRow = () => {
    setGridData([...gridData, { OrderID: 10251, CustomerID: 'VICTE', Freight: 41.34 }]);
  };

  return (
    <div>
      <button onClick={addRow}>Add Row</button>
      <GridComponent dataSource={gridData}>
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
          <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
          <ColumnDirective field='Freight' headerText='Freight' width='120' format='C2' />
        </ColumnsDirective>
      </GridComponent>
    </div>
  );
}

export default App;
```

## Remote Data Binding

### Remote DataManager Quick Checklist

> **Only use DataManager when the prompt explicitly mentions a REST API, remote endpoint, or server-side data. For local/static data use a plain array.**

1. Import `DataManager` and the appropriate adaptor from `@syncfusion/ej2-data`
2. **Always replace the `url` with the actual API endpoint** — never leave a placeholder or demo URL
3. **Match `field` names on `<ColumnDirective>` exactly to the JSON property names returned by the API** — any mismatch causes empty columns
4. Choose the correct adaptor based on your API response shape:
   - `UrlAdaptor` → API returns `{ result: [...], count: N }`
   - `WebApiAdaptor` → API returns a plain array or `{ value: [...], Count: N }`
5. For paging with `UrlAdaptor`, the API **must** return a `count` field with the total record count — without it the pager shows incorrect page numbers
6. Add `loadingIndicator={{ indicatorType: 'Spinner' }}` or `'Shimmer'` **only when** the prompt asks for a loading indicator or the scenario explicitly involves async API fetching — never add it for local data
7. With `UrlAdaptor`, all operations (filter, search, sort, page) are **automatically sent server-side** — inject `Filter`, `Search`, `Sort`, `Page` modules as normal; no custom query logic needed
8. For server-side error handling use the `actionFailure` event: `<GridComponent actionFailure={(args) => console.error(args.error)} />`

### Using DataManager

Connect to remote REST API endpoints using DataManager:

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';
import { ColumnDirective, ColumnsDirective, GridComponent, Inject, Page } from '@syncfusion/ej2-react-grids';
import React from 'react';

function App() {
  const data = new DataManager({
    url: 'url',
    adaptor: new UrlAdaptor()
  });

  return (
    <GridComponent dataSource={data} allowPaging={true}>
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='Freight' headerText='Freight' width='120' format='C2' />
      </ColumnsDirective>
      <Inject services={[Page]} />
    </GridComponent>
  );
}

export default App;
```

### Adaptor Types

The Grid supports multiple adaptor types for different backend architectures:

**1. UrlAdaptor** - Standard REST API

```tsx
const data = new DataManager({
  url: 'url',
  adaptor: new UrlAdaptor()
});
```

**2. ODataV4Adaptor** - OData v4 services with advanced filtering

```tsx
import { ODataV4Adaptor } from '@syncfusion/ej2-data';

const data = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor()
});
```

**3. WebApiAdaptor** - ASP.NET Web API

```tsx
import { WebApiAdaptor } from '@syncfusion/ej2-data';

const data = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  crossDomain: true
});
```

**4. GraphQLAdaptor** - GraphQL endpoints

```tsx
import { GraphQLAdaptor } from '@syncfusion/ej2-data';

const data = new DataManager({
  url: 'url',
  adaptor: new GraphQLAdaptor(),
  query: `{
    orders {
      id
      customer
      amount
      date
    }
  }`
});
```

For detailed examples of all adaptor types, see [references/adaptors.md](adaptors.md)

### Error Handling

Handle data loading errors gracefully:

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';
import { GridComponent, Inject, Page } from '@syncfusion/ej2-react-grids';
import React, { useState } from 'react';

function App() {
  const [error, setError] = useState(null);

  const data = new DataManager({
    url: 'url',
    adaptor: new UrlAdaptor()
  });

  const handleActionFailure = (args) => {
    console.error('Data loading failed:', args.error);
    setError('Failed to load data. Please try again.');
  };

  return (
    <div>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      
      <GridComponent
        dataSource={data}
        actionFailure={handleActionFailure}
        allowPaging={true}
      >
        {/* columns */}
        <Inject services={[Page]} />
      </GridComponent>
    </div>
  );
}

export default App;
```

### Loading States

Display loading indicators while data is being fetched:

```tsx
import { GridComponent } from '@syncfusion/ej2-react-grids';
import { Spinner } from '@syncfusion/ej2-react-popups';
import React, { useState } from 'react';

function App() {
  const [isLoading, setIsLoading] = useState(false);

  const handleDataBound = () => {
    setIsLoading(false);
  };

  const handleActionBegin = (args) => {
    if (args.requestType === 'beforesend') {
      setIsLoading(true);
    }
  };

  return (
    <div>
      {isLoading && <Spinner type='Bootstrap'></Spinner>}
      
      <GridComponent
        dataSource={data}
        actionBegin={handleActionBegin}
        dataBound={handleDataBound}
      >
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default App;
```

### Shimmer Loading

Show skeleton loading during data fetch:

```tsx
function ShimmerGrid() {
  const [isLoading, setIsLoading] = useState(true);

  setTimeout(() => setIsLoading(false), 2000);

  if (isLoading) {
    return (
      <div style={{ padding: '20px' }}>
        {[...Array(5)].map((_, i) => (
          <div key={i} style={{ 
            height: '40px', 
            marginBottom: '10px',
            backgroundColor: '#e0e0e0',
            borderRadius: '4px',
            animation: 'pulse 1.5s infinite'
          }} />
        ))}
        <style>{`
          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
          }
        `}</style>
      </div>
    );
  }

  return <GridComponent dataSource={data}>{/* columns */}</GridComponent>;
}
```

### Custom Adaptor

Create a custom adaptor for specialized data handling:

```tsx
import { DataManager, Adaptor } from '@syncfusion/ej2-data';

class CustomAdaptorExample extends Adaptor {
  constructor() {
    super();
    this.baseUrl = 'url';
  }

  // Override processResponse to transform data
  processResponse(response: any, dm?: DataManager, query?: Query, xhr?: XMLHttpRequest, request?: Request, params?: any): any {
    const result = super.processResponse(response, dm, query, xhr, request, params);
    
    // Transform result
    if (result && result.result) {
      result.result = result.result.map((item: any) => ({
        ...item,
        processed: true
      }));
    }
    
    return result;
  }

}

// Use in DataManager
const dataManager = new DataManager({
  adaptor: new CustomAdaptorExample(),
  crossDomain: true
});
```


## DataManager Configuration

### Choosing the Right Adaptor

| Adaptor | Use When | Expected API Response |
|---------|----------|-----------------------|
| `UrlAdaptor` | Your API is built to work with Syncfusion DataManager | `{ result: [...], count: N }` |
| `WebApiAdaptor` | Standard Web API returning plain arrays or OData-like responses | `{ value: [...], Count: N }` or plain array |
| `ODataAdaptor` | OData v3 service | OData XML/JSON format |
| `ODataV4Adaptor` | OData v4 service | OData v4 JSON format |
| `JsonAdaptor` | Local array already in memory | Plain JS array |

> ⚠️ **If data is not loading**, the most common causes are:
> 1. **Wrong URL** — the `url` is a placeholder or demo URL, not your real API
> 2. **Wrong adaptor** — your API returns a plain array but you are using `UrlAdaptor` (use `WebApiAdaptor` instead)
> 3. **Wrong field names** — `field` values on `<ColumnDirective>` don't match JSON property names returned by the API
> 4. **Missing `count`** — `UrlAdaptor` requires the response to include `"count"` for paging to work


### Offline Mode

Load data once and work offline:

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new UrlAdaptor(),
  offline: true
});
```

### CRUD Operations

DataManager supports automatic CRUD operations:

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new UrlAdaptor(),
  insertUrl: 'url',
  updateUrl: 'url',
  removeUrl: 'url'
});
```

## Loading Indicators

Display loading state while fetching remote data using `loadingIndicator`:

### Spinner Indicator (Default)

```tsx
const loadingIndicator = { indicatorType: 'Spinner' };

<GridComponent
  dataSource={dataManager}
  loadingIndicator={loadingIndicator}
  allowPaging={true}
>
  {/* columns */}
</GridComponent>
```

### Shimmer Indicator

```tsx
const loadingIndicator = { indicatorType: 'Shimmer' };

<GridComponent
  dataSource={dataManager}
  loadingIndicator={loadingIndicator}
  allowPaging={true}
>
  {/* columns */}
</GridComponent>
```

### Control Loading State

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const showLoading = () => {
    // Grid automatically shows loading while fetching
  };

  return (
    <GridComponent
      ref={gridRef}
      dataSource={dataManager}
      loadingIndicator={{ indicatorType: 'Spinner' }}
    >
      {/* columns */}
    </GridComponent>
  );
}

export default App;
```

## Handling Data Source Changes

### Update Data Source

Change data source dynamically:

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const changeData = () => {
    const newData = new DataManager({
      url: 'url',
      adaptor: new UrlAdaptor()
    });
    gridRef.current.setProperties({ dataSource: newData });
  };

  return (
    <div>
      <button onClick={changeData}>Switch Data Source</button>
      <GridComponent ref={gridRef} dataSource={initialData}>
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default App;
```

### Refresh Data

Reload data from the source:

```tsx
const refreshData = () => {
  gridRef.current.refresh();
};
```

### Query with Additional Parameters

```tsx
const dataManager = new DataManager({
  url: 'url',
  adaptor: new UrlAdaptor()
});

// Add query parameters
dataManager.executeQuery(
  new Query().where('CustomerID', 'equal', 'VINET')
);
```
