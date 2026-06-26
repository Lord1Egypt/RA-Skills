# Events

## Table of Contents
- [Event Architecture Overview](#event-architecture-overview)
- [Core Events Reference](#core-events-reference)
- [Cancellable Events Summary](#cancellable-events-summary)
- [`requestType` Quick Reference](#requesttype-quick-reference)
- [All Events Quick Reference](#all-events-quick-reference)
- [Complete Example — Multiple Events](#complete-example--multiple-events)

---

## Event Architecture Overview

Gantt events follow a **before/after pattern**:
- **`actionBegin`** — fires before an action, allows `args.cancel = true` to abort
- **`actionComplete`** — fires after an action completes

Many events have `requestType` to identify the specific operation.

---

## Core Events Reference

### `actionBegin`

Fires before: add, edit (cell/dialog/taskbar), delete, sort, filter, dependency change, zoom, time span navigation.

**`requestType` values:**
| Value | Operation |
|---|---|
| `'beforeAdd'` | Before a task is added |
| `'beforeDelete'` | Before a task is deleted |
| `'beforeSave'` | Before cell/dialog edit is saved |
| `'taskbarEditing'` | Before taskbar drag edit |
| `'filtering'` | Before filter applied |
| `'sorting'` | Before sort applied |
| `'beforeZoomIn'` | Before zoom in |
| `'beforeZoomOut'` | Before zoom out |
| `'validateDependency'` | Before dependency link drawn |

```tsx
const actionBegin = (args: any) => {
  if (args.requestType === 'beforeSave') {
    // Validate task data before saving
    if (args.data && args.data.Duration < 0) {
      args.cancel = true;  // prevent save
    }
  }
  if (args.requestType === 'beforeDelete') {
    console.log('Deleting task:', args.data);
  }
  if (args.requestType === 'validateDependency') {
    if (!args.isValidLink) {
      args.cancel = true;  // prevent invalid dependency
    }
  }
};

<GanttComponent actionBegin={actionBegin} ... />
```

**Key `actionBegin` args properties:**
| Property | Type | Description |
|---|---|---|
| `requestType` | string | Type of action |
| `cancel` | boolean | Set `true` to abort the action |
| `data` | object | Task data involved |
| `newTaskData` | object | Newly added task data |
| `recordIndex` | number | Index of affected record |
| `rowPosition` | string | `'Top'`, `'Bottom'`, `'Above'`, `'Below'` |
| `fromItem` | IGanttData | Predecessor task (dependency events) |
| `toItem` | IGanttData | Successor task (dependency events) |
| `isValidLink` | boolean | Whether dependency link is valid |
| `columnName` | string | Column name (sort/filter events) |
| `direction` | string | `'Ascending'` or `'Descending'` (sort) |

---

### `actionComplete`

Fires after: add, edit, delete, sort, filter, zoom, dependency changes.

```tsx
const actionComplete = (args: any) => {
  if (args.requestType === 'add') {
    console.log('Task added:', args.newTaskData);
    // Sync to server
  }
  if (args.requestType === 'delete') {
    console.log('Deleted records:', args.modifiedRecords);
  }
  if (args.requestType === 'sorting') {
    console.log('Sorted by:', args.columnName, args.direction);
  }
};

<GanttComponent actionComplete={actionComplete} ... />
```

**Key `actionComplete` args properties:**
| Property | Type | Description |
|---|---|---|
| `requestType` | string | Type of action completed |
| `action` | string | Action performed |
| `data` | object | Task data involved |
| `newTaskData` | object | Newly added task data |
| `modifiedRecords` | object[] | Records modified during action |
| `modifiedTaskData` | object[] | Task data after modification |
| `recordIndex` | number | Index of modified record |
| `timeline` | object | Timeline settings (zoom events) |

---

### `taskbarEditing`

Fires continuously while a taskbar is being dragged or resized.

```tsx
const taskbarEditing = (args: any) => {
  // Prevent editing tasks marked as locked
  if (args.data.taskData.IsLocked) {
    args.cancel = true;
  }
  // Log real-time editing
  console.log(`Editing: ${args.data.TaskName}, action: ${args.taskBarEditAction}`);
};
```

**`taskbarEditing` args:**
| Property | Type | Description |
|---|---|---|
| `action` | string | Type of edit in progress |
| `cancel` | boolean | Set `true` to cancel the edit |
| `data` | IGanttData | Task being edited |
| `editingFields` | ITaskData | Fields currently being modified |
| `previousData` | ITaskData | Task data before the edit |
| `recordIndex` | number | Index of the task |
| `taskBarEditAction` | string | Specific action (e.g., `'LeftResizing'`, `'RightResizing'`, `'Move'`, `'ProgressResizing'`) |

---

### `taskbarEdited`

Fires after a taskbar drag or resize is completed.

```tsx
const taskbarEdited = (args: any) => {
  console.log('Taskbar edit complete:', args.data.TaskName);
  console.log('New dates:', args.data.ganttProperties.startDate, args.data.ganttProperties.endDate);
  // Persist changes to server
};

<GanttComponent taskbarEdited={taskbarEdited} ... />
```

---

### `queryTaskbarInfo`

Fires for each taskbar render, allowing conditional styling.

```tsx
const queryTaskbarInfo = (args: any) => {
  if (args.data.Progress < 30) {
    args.taskbarBgColor = '#ff6b6b';
    args.progressBarBgColor = '#cc0000';
  }
};

<GanttComponent queryTaskbarInfo={queryTaskbarInfo} ... />
```

**`queryTaskbarInfo` args:**
| Property | Description |
|---|---|
| `data` | Task record data |
| `taskbarBgColor` | Set taskbar background color |
| `progressBarBgColor` | Set progress bar color |
| `taskbarBorderColor` | Set taskbar border color |
| `rowData` | Full row data |

---

### `rowSelected` / `rowDeselected`

```tsx
const rowSelected = (args: any) => {
  console.log('Selected row index:', args.rowIndex);
  console.log('Selected data:', args.data);
};

const rowDeselected = (args: any) => {
  console.log('Deselected:', args.data);
};

<GanttComponent rowSelected={rowSelected} rowDeselected={rowDeselected} ... />
```

---

### `cellSelected` / `cellDeselected`

```tsx
const cellSelected = (args: any) => {
  console.log('Cell selected:', args.cellIndex, args.data);
};

<GanttComponent cellSelected={cellSelected} ... />
```

---

### `created`

Fires after the Gantt is initialized and the initial render is complete.

```tsx
<GanttComponent created={() => console.log('Gantt initialized')} ... />
```

---

### `dataBound`

Fires after data binding completes (initial load or after refresh).

```tsx
<GanttComponent dataBound={() => console.log('Data bound, rows:', ganttRef.current?.currentViewData.length)} ... />
```

---

### `load`

Fires before the initial data bind and render.

```tsx
<GanttComponent load={() => console.log('Gantt loading...')} ... />
```

---

### `beforeTooltipRender`

Fires before a tooltip is displayed. Allows customizing tooltip content.

```tsx
const beforeTooltipRender = (args: any) => {
  // Customize the tooltip content
  args.content = `<b>${args.data.TaskName}</b><br/>Progress: ${args.data.Progress}%`;
};

<GanttComponent beforeTooltipRender={beforeTooltipRender} ... />
```

---

### `taskbarClick`

Fires when the user clicks on a taskbar.

```tsx
const taskbarClick = (args: any) => {
  console.log('Clicked task:', args.data.TaskName);
  console.log('Task ID:', args.data.TaskID);
};

<GanttComponent taskbarClick={taskbarClick} ... />
```

**`taskbarClick` args:**
| Property | Type | Description |
|---|---|---|
| `data` | IGanttData | The task record that was clicked |
| `target` | Element | The DOM element that was clicked |

---

### `collapsed` / `expanded`

Fires after a row is collapsed or expanded (parent task toggled).

```tsx
const onCollapsed = (args: any) => {
  console.log('Collapsed row:', args.data.TaskName);
};

const onExpanded = (args: any) => {
  console.log('Expanded row:', args.data.TaskName);
};

<GanttComponent collapsed={onCollapsed} expanded={onExpanded} ... />
```

---

### `expanding` / `collapsing`

Fires before a row expands or collapses. Set `args.cancel = true` to prevent the operation.

```tsx
const onCollapsing = (args: any) => {
  if (args.data.TaskID === 1) {
    args.cancel = true;  // prevent collapsing root task
  }
};

<GanttComponent collapsing={onCollapsing} ... />
```

---

### `splitterResized`

Fires after the splitter between TreeGrid and Chart panels is resized.

```tsx
<GanttComponent
  splitterResized={(args) => console.log('Splitter position:', args.newWidth)}
  ...
/>
```

---

### `excelExportComplete` / `pdfExportComplete`

```tsx
<GanttComponent
  excelExportComplete={(args) => console.log('Excel export done')}
  pdfExportComplete={(args) => console.log('PDF export done')}
  ...
/>
```

---

## Cancellable Events Summary

| Event | Cancel Pattern | Effect |
|---|---|---|
| `actionBegin` | `args.cancel = true` | Prevents the action (add/edit/delete/sort/filter/dependency) |
| `taskbarEditing` | `args.cancel = true` | Prevents the taskbar drag/resize change |
| `collapsing` | `args.cancel = true` | Prevents the row from collapsing |
| `expanding` | `args.cancel = true` | Prevents the row from expanding |

---

## `requestType` Quick Reference

| `requestType` | Event | Meaning |
|---|---|---|
| `beforeAdd` | `actionBegin` | Before task addition |
| `add` | `actionComplete` | After task addition |
| `beforeSave` | `actionBegin` | Before cell/dialog save |
| `save` | `actionComplete` | After edit saved |
| `beforeDelete` | `actionBegin` | Before task deletion |
| `delete` | `actionComplete` | After deletion |
| `taskbarEditing` | `actionBegin` | Taskbar drag starting |
| `filtering` | `actionBegin/Complete` | Filter operation |
| `filterAfterOpen` | `actionComplete` | Filter menu opened |
| `sorting` | `actionBegin/Complete` | Sort operation |
| `beforeZoomIn` | `actionBegin` | Before zoom in |
| `beforeZoomOut` | `actionBegin` | Before zoom out |
| `validateDependency` | `actionBegin` | Dependency link being drawn |
| `updateDependency` | `actionBegin` | Dependency being updated |
| `collapsingRecord` | `actionBegin` | Before a row collapses |
| `expandingRecord` | `actionBegin` | Before a row expands |

---

## All Events Quick Reference

| Event | Cancellable | Description |
|---|---|---|
| `load` | No | Before initial bind and render |
| `created` | No | After Gantt fully initialized |
| `dataBound` | No | After data binding completes |
| `actionBegin` | Yes (`args.cancel`) | Before any data action or navigation |
| `actionComplete` | No | After any data action completes |
| `taskbarEditing` | Yes (`args.cancel`) | During taskbar drag/resize |
| `taskbarEdited` | No | After taskbar drag/resize completes |
| `taskbarClick` | No | When user clicks a taskbar |
| `queryTaskbarInfo` | No | Per-taskbar render (apply dynamic styles) |
| `rowSelected` | No | After a row is selected |
| `rowDeselected` | No | After a row is deselected |
| `cellSelected` | No | After a cell is selected |
| `cellDeselected` | No | After a cell is deselected |
| `collapsing` | Yes (`args.cancel`) | Before a row collapses |
| `collapsed` | No | After a row collapses |
| `expanding` | Yes (`args.cancel`) | Before a row expands |
| `expanded` | No | After a row expands |
| `beforeTooltipRender` | No | Before tooltip is displayed (allows content override) |
| `splitterResizeStart` | No | Before splitter drag begins |
| `splitterResizing` | No | During splitter drag |
| `splitterResized` | No | After splitter drag ends |
| `excelExportComplete` | No | After Excel export finishes |
| `pdfExportComplete` | No | After PDF export finishes |
| `contextMenuClick` | No | When a context menu item is clicked |
| `contextMenuOpen` | No | Before context menu opens (use `args.hideItems`) |
| `toolbarClick` | No | When a toolbar item is clicked |
| `resizeStart` | No | Before column resize starts |
| `resizing` | No | During column resize |
| `resizeStop` | No | After column resize ends |
| `columnDragStart` | No | Before column reorder drag starts |
| `columnDrag` | No | During column reorder drag |
| `columnDrop` | No | After column dropped in new position |

---

## Complete Example — Multiple Events

```tsx
import React, { useRef } from 'react';
import {
  GanttComponent, Inject, Edit, Selection, Toolbar, Sort, Filter,
  IQueryTaskbarInfoEventArgs, EditSettingsModel, TaskFieldsModel
} from '@syncfusion/ej2-react-gantt';

function App() {
  const ganttRef = useRef<GanttComponent>(null);

  const taskFields: TaskFieldsModel = {
    id: 'TaskID', name: 'TaskName',
    startDate: 'StartDate', duration: 'Duration',
    progress: 'Progress', dependency: 'Predecessor', child: 'subtasks'
  };

  const editSettings: EditSettingsModel = {
    allowAdding: true, allowEditing: true,
    allowDeleting: true, allowTaskbarEditing: true
  };

  // Validation before save
  const actionBegin = (args: any) => {
    if (args.requestType === 'beforeSave') {
      if (args.data && args.data.Duration < 0) {
        args.cancel = true;
        alert('Duration must be positive.');
      }
    }
  };

  // Post-action logging
  const actionComplete = (args: any) => {
    if (args.requestType === 'add') {
      console.log('Added:', args.newTaskData);
    }
  };

  // Dynamic taskbar styling
  const queryTaskbarInfo = (args: IQueryTaskbarInfoEventArgs) => {
    const progress = (args.data as any).Progress;
    args.taskbarBgColor = progress < 30 ? '#ff6b6b' : progress < 70 ? '#ffa500' : '#4CAF50';
  };

  // Taskbar drag validation
  const taskbarEditing = (args: any) => {
    if ((args.data as any).taskData?.IsLocked) {
      args.cancel = true;
    }
  };

  return (
    <GanttComponent
      ref={ganttRef}
      dataSource={data}
      taskFields={taskFields}
      editSettings={editSettings}
      toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
      allowSorting={true}
      allowFiltering={true}
      actionBegin={actionBegin}
      actionComplete={actionComplete}
      queryTaskbarInfo={queryTaskbarInfo}
      taskbarEditing={taskbarEditing}
      dataBound={() => console.log('Data loaded')}
      height='450px'
    >
      <Inject services={[Edit, Selection, Toolbar, Sort, Filter]} />
    </GanttComponent>
  );
}

export default App;
```
