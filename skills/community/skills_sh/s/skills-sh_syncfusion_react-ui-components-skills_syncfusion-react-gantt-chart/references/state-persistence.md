# State Persistence, Immutable Mode & Loading Animation

## Table of Contents
- [State Persistence](#state-persistence)
- [Resetting Persisted State](#resetting-persisted-state)
- [Immutable Mode](#immutable-mode)
- [Loading Animation](#loading-animation)
- [Common Pitfalls](#common-pitfalls)

---

## State Persistence

Enable `enablePersistence={true}` to automatically save and restore the Gantt's UI state (column widths, sort order, filter state, column visibility, splitter position) across browser sessions using `localStorage`.

```tsx
<GanttComponent
  id='projectGantt'          // unique ID — used as the localStorage key
  enablePersistence={true}
  dataSource={data}
  taskFields={taskFields}
  height='450px'
/>
```

> The `id` prop is **required** when using `enablePersistence`. It is used as the localStorage key prefix. If two Gantt instances share the same `id`, they will overwrite each other's state.

### What Gets Persisted

| State | Persisted |
|---|---|
| Column widths | ✅ |
| Column visibility (show/hide) | ✅ |
| Column order (after reorder) | ✅ |
| Sort columns and direction | ✅ |
| Active filters | ✅ |
| Splitter position | ✅ |
| Search text | ✅ |

---

## Resetting Persisted State

To clear persisted state, change the component's `id` — this creates a new localStorage entry and the old state is ignored:

```tsx
import React, { useState } from 'react';
import { GanttComponent } from '@syncfusion/ej2-react-gantt';

function App() {
  const [ganttId, setGanttId] = useState('projectGantt');

  const resetState = () => {
    setGanttId(`projectGantt_${Date.now()}`);
  };

  return (
    <>
      <button onClick={resetState}>Reset State</button>
      <GanttComponent
        id={ganttId}
        enablePersistence={true}
        dataSource={data}
        taskFields={taskFields}
        height='450px'
      />
    </>
  );
}
```

Alternatively, clear the localStorage entry directly:
```tsx
localStorage.removeItem('projectGantt-gantt-persistence');
```

---

## Immutable Mode

Immutable mode optimizes re-render performance: when `dataSource` updates, only the rows whose data has changed are re-rendered. Unchanged rows remain in the DOM without re-painting.

```tsx
import { GanttComponent, ColumnsDirective, ColumnDirective, Inject, Edit, Toolbar } from '@syncfusion/ej2-react-gantt';

function App() {
  return (
    <GanttComponent
      enableImmutableMode={true}
      dataSource={data}
      taskFields={taskFields}
      editSettings={{ allowAdding: true, allowEditing: true, allowDeleting: true }}
      toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
      height='450px'
    >
      <ColumnsDirective>
        <ColumnDirective field='TaskID'   isPrimaryKey={true} width='80' />  {/* required */}
        <ColumnDirective field='TaskName' width='250' />
        <ColumnDirective field='StartDate' />
        <ColumnDirective field='Duration' />
        <ColumnDirective field='Progress' />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar]} />
    </GanttComponent>
  );
}
```

### Requirements

- `isPrimaryKey={true}` **must** be set on the ID column — Gantt uses it to compare records and detect which rows changed
- Works best when data updates are frequent and only a small subset of rows change at a time

---

## Loading Animation

Customize the loading indicator shown while data is being fetched or the component is initializing:

```tsx
// Default spinner
<GanttComponent
  loadingIndicator={{ indicatorType: 'Spinner' }}
  dataSource={data}
  taskFields={taskFields}
  height='450px'
/>

// Shimmer effect (skeleton loading)
<GanttComponent
  loadingIndicator={{ indicatorType: 'Shimmer' }}
  dataSource={data}
  taskFields={taskFields}
  height='450px'
/>
```

| `indicatorType` | Description |
|---|---|
| `'Spinner'` | Default rotating spinner overlay |
| `'Shimmer'` | Skeleton shimmer rows — better for perceived performance |

### Manually Show / Hide Spinner

Use `showSpinner()` and `hideSpinner()` for manual control (e.g., during custom async operations):

```tsx
const ganttRef = React.useRef<GanttComponent>(null);

// Show the spinner before a custom async operation
ganttRef.current?.showSpinner();

// Hide it when done
ganttRef.current?.hideSpinner();
```

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| State not persisting | `id` prop not set | Set a stable unique `id` on `GanttComponent` |
| Two instances overwrite each other | Same `id` on both | Use distinct `id` values for each Gantt instance |
| Old state shows after data update | Persisted state cached in localStorage | Reset state by changing `id` or clearing localStorage entry |
| Immutable mode not working | `isPrimaryKey` not set on ID column | Add `isPrimaryKey={true}` to the TaskID column |
| Shimmer not showing | `loadingIndicator` not set | Set `loadingIndicator={{ indicatorType: 'Shimmer' }}` |
