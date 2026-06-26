---
name: state-persistence
description: 'State Persistence in React TreeGrid - global and local persistence, expandState tracking, sort/filter/paging state restoration.'
---

# State Persistence

## Table of Contents
- [Global Persistence](#global-persistence)
- [Local State Persistence](#local-state-persistence)
- [Expand State Persistence](#expand-state-persistence)
- [Filter And Sort State Persistence](#filter-and-sort-state-Persistence)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Global Persistence

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

```tsx
import React, { useEffect, useState } from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    {
      TaskID: 1,
      TaskName: 'Planning',
      expandState: true,
      Children: [
        { TaskID: 2, TaskName: 'Plan timeline' }
      ]
    }
  ];

  useEffect(() => {
    // Load state from localStorage on mount
    const savedState = localStorage.getItem('treegridState');
    if (savedState) {
      const state = JSON.parse(savedState);
      // Restore state...
    }
  }, []);

  const handleStateChange = () => {
    // Get current state
    const state = treeGridRef.current.getCurrentViewRecords();
    // Save to localStorage
    localStorage.setItem('treegridState', JSON.stringify(state));
  };

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      enablePersistence={true}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
    </TreeGridComponent>
  );
}
```

## Local State Persistence

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

Persist state locally within session:

```tsx
const [expandedRows, setExpandedRows] = useState([]);

const handleRowExpand = (args) => {
  setExpandedRows([...expandedRows, args.data.TaskID]);
  // Save to session storage
  sessionStorage.setItem('expandedRows', JSON.stringify([...expandedRows, args.data.TaskID]));
};

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  rowExpanded={handleRowExpand}
  rowCollapsed={(args) => {
    const filtered = expandedRows.filter(id => id !== args.data.TaskID);
    setExpandedRows(filtered);
    sessionStorage.setItem('expandedRows', JSON.stringify(filtered));
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Expand State Persistence

Track and restore expand state:

```tsx
const data = [
  {
    TaskID: 1,
    TaskName: 'Planning',
    expandState: true,  // Starts expanded
    Children: [
      { TaskID: 2, TaskName: 'Plan timeline', expandState: false }
    ]
  }
];

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  expandStateMapping="expandState"
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Filter And Sort State Persistence

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

Persist sorting and filtering:

```tsx
const persistState = () => {
  const gridState = {
    sort: treeGridRef.current.sortSettings,
    filter: treeGridRef.current.filterSettings,
    page: treeGridRef.current.pageSettings,
    expand: treeGridRef.current.getCurrentViewRecords()
  };
  
  localStorage.setItem('treegridFullState', JSON.stringify(gridState));
};

const restoreState = () => {
  const saved = localStorage.getItem('treegridFullState');
  if (saved) {
    const gridState = JSON.parse(saved);
    treeGridRef.current.sortSettings = gridState.sort;
    treeGridRef.current.filterSettings = gridState.filter;
  }
};
```

## Key APIs

| Property/Method | Type | Description |
|---|---|---|
| `enablePersistence` | boolean | Auto-persist state |
| `expandStateMapping` | string | Map expand state to data property |
| `getCurrentViewRecords` | method | Get current row data |
| `sortSettings` | object | Current sort configuration |
| `filterSettings` | object | Current filter configuration |

## Common Patterns

1. **Session Persistence**: Save state during user session
2. **User Preferences**: Store per-user expand/filter preferences
3. **Restore on Reload**: Restore state when page reloads
4. **Clear on Logout**: Clear persisted state on logout

