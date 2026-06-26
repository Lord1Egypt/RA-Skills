# State Management in React Grid

## Table of Contents
- [Overview](#overview)
- [Save and Restore State](#save-and-restore-state)
- [Restore Initial Grid State](#restore-initial-grid-state)
- [Prevent Columns from Persisting](#prevent-columns-from-persisting)
- [Persist Column Template and Header Text](#persist-column-template-and-header-text)

## Overview

State management allows persisting grid configuration like column order, width, sorting, filtering, grouping, and visibility across sessions. The grid provides a persistence mechanism via the `enablePersistence` property. When set to `true`, the grid automatically saves and restores its state to the browser's `localStorage`.

```tsx
<GridComponent
  dataSource={data}
  enablePersistence={true}
  id="Orders"
>
  {/* columns */}
</GridComponent>
```

> ⚠️ The `id` prop is required when using `enablePersistence`. The localStorage key is formed as `"grid" + id` (e.g., `gridOrders`). Without `id`, state cannot be correctly saved or retrieved.

> ✅ `enablePersistence={true}` is **mandatory** for grid state persistence.

### What Gets Persisted

| Setting | Persisted Properties |
|---|---|
| `pageSettings` | `currentPage`, `pageCount`, `pageSize`, `pageSizes`, `totalRecordsCount` |
| `groupSettings` | `columns`, `showDropArea`, `showGroupedColumn`, `enableLazyLoading`, etc. |
| `columns` | `field`, `visible`, `width`, `index`, `allowSorting`, `allowFiltering`, `isFrozen`, etc. |
| `sortSettings` | all |
| `filterSettings` | all |
| `searchSettings` | all |
| `selectedRowIndex` | last selected row only |

> ⚠️ Column `template`, `headerTemplate`, `headerText`, `formatter`, and `valueAccessor` are **not** persisted automatically — they must be handled manually.

## Save and Restore State

Use `getPersistData()` to get the current grid state as a JSON string, and `setProperties()` to restore it.

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

```tsx
import React from 'react';
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page, Sort, Filter, Group, Edit, Toolbar } from '@syncfusion/ej2-react-grids';

function App() {
  let grid;

  // Save grid state to localStorage
  const saveState = () => {
    const persistData = grid.getPersistData(); // returns JSON string
    window.localStorage.setItem('gridOrders', persistData); // key = "grid" + id
  };

  // Restore grid state from localStorage
  const restoreState = () => {
    const value = window.localStorage.getItem('gridOrders');
    const state = JSON.parse(value);
    if (state) {
      grid.setProperties(state);
    }
  };

  return (
    <div>
      <button onClick={saveState}>Save</button>
      <button onClick={restoreState}>Restore</button>

      <GridComponent
        id='Orders'
        dataSource={data}
        allowFiltering={true}
        allowPaging={true}
        allowSorting={true}
        allowGrouping={true}
        enablePersistence={true}
        ref={g => grid = g}
      >
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' width='100' textAlign='Right' isPrimaryKey={true} />
          <ColumnDirective field='CustomerID' headerText='Customer ID' width='100' />
          <ColumnDirective field='ShipCity' headerText='Ship City' width='100' />
          <ColumnDirective field='ShipCountry' headerText='Ship Country' width='100' />
        </ColumnsDirective>
        <Inject services={[Filter, Page, Sort, Group, Edit, Toolbar]} />
      </GridComponent>
    </div>
  );
}

export default App;
```

### Get/Set localStorage Directly

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

```tsx
// Get the persisted grid model
const value = window.localStorage.getItem('gridOrders'); // "grid" + component id
const model = JSON.parse(value);

// Set the grid model manually
window.localStorage.setItem('gridOrders', JSON.stringify(value));
```

> ✅ `enablePersistence={true}` is **mandatory** for `getItem`/`setItem`/manual approach state persistence.

### Maintain Custom Query with Persistence

When `enablePersistence` is enabled, custom query parameters are not automatically maintained after a page reload. Re-apply them in `actionBegin`:

```tsx
const actionBegin = () => {
  if (grid) {
    grid.query.addParams('dataSource', 'data');
  }
};

<GridComponent
  dataSource={data}
  enablePersistence={true}
  actionBegin={actionBegin}
>
  {/* columns */}
</GridComponent>
```

## Restore Initial Grid State

### By Clearing localStorage

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

```tsx
const restoreToInitial = () => {
  grid.enablePersistence = false;
  window.localStorage.setItem('gridGrid', ''); // "grid" + component id
  grid.destroy();
  location.reload();
};
```

### By Changing Component ID

Changing the component's `id` causes the grid to treat itself as a new instance and revert to default settings:

```tsx
const restoreToInitial = () => {
  grid.id = 'OrderDetails' + Math.floor(Math.random() * 10);
  location.reload();
};
```

## Prevent Columns from Persisting

To exclude specific properties (e.g., columns) from being persisted, override `addOnPersist` in the `dataBound` event:

```tsx
const dataBound = () => {
  let cloned = grid.addOnPersist;
  grid.addOnPersist = function (key) {
    key = key.filter((item) => item !== 'columns');
    return cloned.call(this, key);
  };
};

<GridComponent
  id='Grid'
  dataSource={data}
  allowPaging={true}
  enablePersistence={true}
  dataBound={dataBound}
  ref={g => grid = g}
>
  {/* columns */}
  <Inject services={[Page]} />
</GridComponent>
```

## Persist Column Template and Header Text

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

By default, `template`, `headerTemplate`, `headerText`, `formatter`, and `valueAccessor` are not persisted. To persist them, clone columns manually alongside `getPersistData()`:

```tsx
// Save
const saveBtn = () => {
  const persistedSettings = JSON.parse(grid.getPersistData());
  const gridColumns = Object.assign([], grid.getColumns());

  persistedSettings.columns.forEach((persistedColumn) => {
    const column = gridColumns.find((col) => col.field === persistedColumn.field);
    if (column) {
      persistedColumn.headerText = column.headerText;
      persistedColumn.template = column.template;
      persistedColumn.headerTemplate = column.headerTemplate;
    }
  });

  window.localStorage.setItem('gridOrders', JSON.stringify(persistedSettings));
  grid.setProperties(persistedSettings);
};

// Restore
const restoreBtn = () => {
  const savedSettings = window.localStorage.getItem('gridOrders');
  if (savedSettings) {
    grid.setProperties(JSON.parse(savedSettings));
  }
};
```
