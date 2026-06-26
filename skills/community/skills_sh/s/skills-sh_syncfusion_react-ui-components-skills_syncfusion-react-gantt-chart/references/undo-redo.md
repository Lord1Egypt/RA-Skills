# Undo / Redo in Syncfusion React Gantt Chart

## Table of Contents
- [Overview](#overview)
- [Basic Setup](#basic-setup)
- [undoRedoActions Options](#undoredoactions-options)
- [Toolbar Undo / Redo Buttons](#toolbar-undo--redo-buttons)
- [Programmatic Undo / Redo](#programmatic-undo--redo)
- [Common Pitfalls](#common-pitfalls)

---

## Overview

The Gantt component supports undo and redo for tracked operations via `enableUndoRedo={true}` and the `UndoRedo` service. Users can revert or reapply changes using keyboard shortcuts (`Ctrl+Z` / `Ctrl+Y`) or toolbar buttons.

---

## Basic Setup

```tsx
import {
  GanttComponent, Inject,
  UndoRedo, Edit, Sort, Filter, Toolbar
} from '@syncfusion/ej2-react-gantt';

function App() {
  return (
    <GanttComponent
      dataSource={data}
      taskFields={taskFields}
      enableUndoRedo={true}
      undoRedoStepsCount={10}
      undoRedoActions={['Add', 'Edit', 'Delete', 'Sorting', 'Filtering']}
      toolbar={['Undo', 'Redo', 'Add', 'Edit', 'Delete', 'Update', 'Cancel']}
      editSettings={{ allowAdding: true, allowEditing: true, allowDeleting: true }}
      allowSorting={true}
      allowFiltering={true}
      height='450px'
    >
      <Inject services={[UndoRedo, Edit, Sort, Filter, Toolbar]} />
    </GanttComponent>
  );
}
```

### Key Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `enableUndoRedo` | boolean | `false` | Enable undo/redo tracking |
| `undoRedoStepsCount` | number | `10` | Maximum steps stored in history stack (set `0` to disable limit) |
| `undoRedoActions` | string[] | — | Actions to track (see full list below) |

---

## undoRedoActions Options

Only actions listed in `undoRedoActions` are tracked. Each action also requires its corresponding service to be injected:

| Action String | Description | Required Service |
|---|---|---|
| `'Add'` | Task addition | `Edit` |
| `'Edit'` | Task cell / dialog edit | `Edit` |
| `'Delete'` | Task deletion | `Edit` |
| `'Indent'` | Indent task (promote to child) | `Edit` |
| `'Outdent'` | Outdent task (promote to sibling) | `Edit` |
| `'TaskbarDragAndDrop'` | Taskbar move / resize | `Edit` |
| `'RowDragAndDrop'` | Row drag and drop reorder | `RowDD` |
| `'ColumnReorder'` | Column drag reorder | `Reorder` |
| `'ColumnResize'` | Column width resize | `Resize` |
| `'Sorting'` | Column sort | `Sort` |
| `'Filtering'` | Column filter | `Filter` |
| `'Search'` | Toolbar search | — |
| `'ZoomIn'` | Timeline zoom in | — |
| `'ZoomOut'` | Timeline zoom out | — |
| `'ZoomToFit'` | Timeline zoom to fit | — |
| `'ColumnState'` | Column show/hide | — |
| `'PreviousTimeSpan'` | Navigate timeline backward | — |
| `'NextTimeSpan'` | Navigate timeline forward | — |

---

## Toolbar Undo / Redo Buttons

Add `'Undo'` and `'Redo'` to the `toolbar` array to show buttons in the toolbar:

```tsx
<GanttComponent
  toolbar={['Undo', 'Redo']}
  enableUndoRedo={true}
  undoRedoActions={['Add', 'Edit', 'Delete']}
  ...
>
  <Inject services={[UndoRedo, Edit, Toolbar]} />
</GanttComponent>
```

> Keyboard shortcuts work regardless of whether toolbar buttons are shown: `Ctrl+Z` (undo), `Ctrl+Y` (redo).

---

## Programmatic Undo / Redo

Trigger undo or redo from code using the component ref:

```tsx
import React, { useRef } from 'react';
import { GanttComponent } from '@syncfusion/ej2-react-gantt';

function App() {
  const ganttRef = useRef<GanttComponent>(null);

  return (
    <>
      <button onClick={() => ganttRef.current?.undo()}>Undo</button>
      <button onClick={() => ganttRef.current?.redo()}>Redo</button>
      <GanttComponent
        ref={ganttRef}
        enableUndoRedo={true}
        undoRedoActions={['Add', 'Edit', 'Delete']}
        ...
      >
        <Inject services={[UndoRedo, Edit, Toolbar]} />
      </GanttComponent>
    </>
  );
}
```

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| Undo not working | `UndoRedo` service not injected | Add `UndoRedo` to `services` array |
| Undo not working | `enableUndoRedo` not set | Set `enableUndoRedo={true}` |
| Action not tracked | Action not listed in `undoRedoActions` | Add the action string to `undoRedoActions` |
| Undo for sort not working | `Sort` service not injected | Inject `Sort` when tracking `'Sorting'` |
| Undo for filter not working | `Filter` service not injected | Inject `Filter` when tracking `'Filtering'` |
| Undo for row DnD not working | `RowDD` service not injected | Inject `RowDD` when tracking `'RowDragAndDrop'` |
| History stack runs out quickly | `undoRedoStepsCount` too low | Increase `undoRedoStepsCount` (e.g. `20`) |
