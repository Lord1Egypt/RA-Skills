---
name: selection
description: 'Selection in React TreeGrid - row selection, cell selection, checkbox selection, multi-selection, and selection events.'
---

# Selection

## Table of Contents
- [Selection Rules](#selection-rules)
- [Row Selection](#row-selection)
- [Cell Selection](#cell-selection)
- [Checkbox Selection](#checkbox-selection)
- [Multi-Selection](#multi-selection)
- [Programmatic Selection](#programmatic-selection)
- [Selection Events](#selection-events)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Selection Rules

### Rule 1: Selection is Built-In (NO Module Injection Required)
**Severity**: 🟢 IMPORTANT - Don't inject unnecessary modules; selection is a core feature

**Requirement in React**:
```jsx
// ✅ CORRECT - Selection is built-in, NO module needed
<TreeGridComponent 
  dataSource={data}
  selectionSettings={{ type: 'Multiple', mode: 'Row' }}>
  <ColumnsDirective>
    <ColumnDirective field='TaskID'></ColumnDirective>
  </ColumnsDirective>
  {/* NO <Inject services={...}> needed for selection */}
</TreeGridComponent>

// ✅ All selection types work out of the box
// Row Selection - Single
<TreeGridComponent 
  selectionSettings={{ type: 'Single', mode: 'Row' }}>
</TreeGridComponent>

// Multiple Row Selection
<TreeGridComponent 
  selectionSettings={{ type: 'Multiple', mode: 'Row' }}>
</TreeGridComponent>

// Cell Selection
<TreeGridComponent 
  selectionSettings={{ type: 'Single', mode: 'Cell' }}>
</TreeGridComponent>

// Checkbox Selection (Row mode only!)
<TreeGridComponent 
  selectionSettings={{ type: 'Checkbox', mode: 'Row' }}>
</TreeGridComponent>

// ❌ WRONG - DON'T try to inject Selection module
import { /* No Selection module exists */ } from '@syncfusion/ej2-react-treegrid';
<TreeGridComponent>
  <Inject services={[/* Selection not injectable */]} />  {/* WRONG */}
</TreeGridComponent>
```

**Selection Features (All Built-In, No Injection Needed)**:
```jsx
// Row Selection - all built-in
selectionSettings: { type: 'Single', mode: 'Row' }      // ✅ No service needed
selectionSettings: { type: 'Multiple', mode: 'Row' }    // ✅ No service needed

// Cell Selection - built-in
selectionSettings: { type: 'Single', mode: 'Cell' }     // ✅ No service needed
selectionSettings: { type: 'Multiple', mode: 'Cell' }   // ✅ No service needed

// Checkbox Selection - built-in
selectionSettings: { type: 'Checkbox', mode: 'Row' }    // ✅ No service needed
// NOTE: Checkbox ONLY works with mode='Row', NOT with mode='Cell'!
```

---

### Rule 2: Selection Persistence Requires State Management
**Severity**: 🟠 IMPORTANT - Selection state not preserved across page reload or component recreate

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

**Requirement in React**:
```jsx
// ✅ OPTION 1: Use enablePersistence
<TreeGridComponent 
  enablePersistence={true}
  selectionSettings={{ type: 'Multiple', mode: 'Row' }}>
</TreeGridComponent>

// ✅ OPTION 2: Manually save & restore selection state
import { useState, useRef } from 'react';

export default function GridWithSelection() {
  const gridRef = useRef(null);
  const [savedSelection, setSavedSelection] = useState([]);
  
  // Save selection before component unmount
  const saveSelection = () => {
    const selected = gridRef.current?.getSelectedRowIndexes();
    setSavedSelection(selected || []);
    localStorage.setItem('selection', JSON.stringify(selected));
  };
  
  // Restore selection on component mount
  const restoreSelection = () => {
    const saved = localStorage.getItem('selection');
    if (saved && gridRef.current) {
      gridRef.current.selectRows(JSON.parse(saved));
    }
  };
  
  return (
    <TreeGridComponent 
      ref={gridRef}
      dataSource={data}
      selectionSettings={{ type: 'Multiple', mode: 'Row' }}
      onDataBound={restoreSelection}>
      <ColumnsDirective>
        <ColumnDirective field='TaskID'></ColumnDirective>
      </ColumnsDirective>
    </TreeGridComponent>
  );
}

// ❌ WRONG - Selection lost on page reload
<TreeGridComponent 
  dataSource={data}
  selectionSettings={{ type: 'Multiple', mode: 'Row' }}>
  {/* Without enablePersistence or manual save, selection is lost */}
</TreeGridComponent>

// ❌ WRONG - Lost when navigating away
export default function Page() {
  return (
    <TreeGridComponent 
      selectionSettings={{ type: 'Multiple', mode: 'Row' }}>
      {/* Closing this component loses selection */}
    </TreeGridComponent>
  );
}
```

**Selection Persistence Scenarios**:
```jsx
// SCENARIO 1: User refreshes page
// Without enablePersistence → Selection LOST ❌
// With enablePersistence → Selection RESTORED ✅

// SCENARIO 2: User navigates away and back
// Without manual save → Selection LOST ❌
// With localStorage + manual restore → Selection RESTORED ✅

// SCENARIO 3: Component re-renders
// Without state persistence → Selection LOST ❌
// With component state → Selection maintained ✅
```

---

## Row Selection

Enable row selection to highlight and select rows:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Selection } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      selectionSettings={{ type: 'Single', mode: 'Row' }}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
      <Inject services={[Selection]} />
    </TreeGridComponent>
  );
}
```

## Cell Selection

Enable cell-level selection:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  selectionSettings={{ type: 'Multiple', mode: 'Cell' }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
  <Inject services={[Selection]} />
</TreeGridComponent>
```

### Single Cell Selection

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  selectionSettings={{ 
    type: 'Single', 
    mode: 'Cell'
  }}
>
  {/* columns */}
</TreeGridComponent>
```

## Checkbox Selection

Add checkboxes for row selection:

### Enable Checkbox Column

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  selectionSettings={{ 
    mode: 'Row'
  }}
>
  <ColumnsDirective>
    <ColumnDirective type="checkbox" width={50} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[Selection]} />
</TreeGridComponent>
```

### Disable Checkbox for Specific Rows

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  recordDoubleClick={(args) => {
    if (args.data.Priority === 'Critical') {
      args.cancel = true;  // Disable selection for critical rows
    }
  }}
>
  {/* checkbox column */}
</TreeGridComponent>
```

## Multi-Selection

Enable multiple row/cell selection:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  selectionSettings={{ 
    type: 'Row', 
    mode: 'Row',
    enableSimpleMultiRowSelection: true,  // Allow Ctrl+click for multi-select
    checkboxOnly: false
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[Selection]} />
</TreeGridComponent>
```

## Programmatic Selection

Select rows/cells via code:

```tsx
const treeGridRef = React.useRef();

// Select specific row
const selectRow = (index) => {
  treeGridRef.current.selectRow(index);
};

// Select multiple rows
const selectRows = (indices) => {
  treeGridRef.current.selectRows(indices);
};

// Get selected rows
const getSelectedRows = () => {
  const selectedRows = treeGridRef.current.getSelectedRows();
  console.log('Selected rows:', selectedRows);
};

// Clear selection
const clearSelection = () => {
  treeGridRef.current.clearSelection();
};

<TreeGridComponent 
  ref={treeGridRef}
  dataSource={data} 
  childMapping="Children"
  selectionSettings={{ type: 'Row', mode: 'Row' }}
>
  {/* columns */}
</TreeGridComponent>
```

## Selection Events

### Row Selected Event

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  rowSelected={(args) => {
    console.log('Row selected:', args.data);
    console.log('Row index:', args.rowIndex);
  }}
>
  {/* columns */}
</TreeGridComponent>
```

### Row Deselected Event

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  rowDeselected={(args) => {
    console.log('Row deselected:', args.data);
  }}
>
  {/* columns */}
</TreeGridComponent>
```

---

## Key APIs

| Property/Method | Type | Description |
|---|---|---|
| `selectionSettings` | object | Configure selection behavior |
| `type` | string | Selection type: Row, Cell, Checkbox |
| `mode` | string | Selection mode: Single, Multiple |
| `enableSimpleMultiRowSelection` | boolean | Allow multiple row selection |
| `checkboxOnly` | boolean | Checkbox selection only |
| `selectRow` | method | Select row by index |
| `selectRows` | method | Select multiple rows by indices |
| `getSelectedRows` | method | Get selected row indices |
| `clearSelection` | method | Clear all selections |
| `rowSelected` | event | Fires when row is selected |
| `rowDeselected` | event | Fires when row is deselected |

## Common Patterns

1. **Row Selection with Checkbox**: Enable checkbox column for visual selection
2. **Multi-Select**: Allow Ctrl+click for selecting multiple non-adjacent rows
3. **Get Selected Data**: Retrieve selected row objects after selection
4. **Programmatic Focus**: Select row on button click from external control

