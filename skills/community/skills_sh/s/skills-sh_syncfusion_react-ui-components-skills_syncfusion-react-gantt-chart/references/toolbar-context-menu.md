# Toolbar & Context Menu

## Table of Contents
- [Toolbar](#toolbar)
- [Custom Toolbar Items](#custom-toolbar-items)
- [Override Built-in Toolbar Behavior](#override-built-in-toolbar-behavior)
- [Toolbar Styling](#toolbar-styling)
- [Context Menu](#context-menu)
- [Custom Context Menu Items](#custom-context-menu-items)
- [Toolbar + Context Menu Together](#toolbar--context-menu-together)
- [Common Pitfalls](#common-pitfalls)

---

## Toolbar

### Required Module Injection
```tsx
import { Toolbar } from '@syncfusion/ej2-react-gantt';

<GanttComponent ...>
  <Inject services={[Toolbar]} />
</GanttComponent>
```

### Built-in Toolbar Items

| Item | Action |
|---|---|
| `Add` | Adds a new record |
| `Edit` | Edits the selected record |
| `Delete` | Deletes the selected record |
| `Update` | Saves the edited record |
| `Cancel` | Cancels the edit state |
| `Search` | Shows search box to filter records |
| `ExpandAll` | Expands all rows |
| `CollapseAll` | Collapses all rows |
| `Indent` | Indents selected record one level |
| `Outdent` | Outdents selected record one level |
| `PrevTimeSpan` | Navigates timeline to previous time span |
| `NextTimeSpan` | Navigates timeline to next time span |
| `ZoomIn` | Zooms in the timeline |
| `ZoomOut` | Zooms out the timeline |
| `ZoomToFit` | Fits all tasks in the visible timeline |
| `CriticalPath` | Toggles critical path highlighting |
| `ExcelExport` | Triggers Excel export |
| `CsvExport` | Triggers CSV export |
| `PdfExport` | Triggers PDF export |
| `ColumnChooser` | Opens column chooser dialog |
| `Undo` | Undoes the last tracked action (requires `UndoRedo` service) |
| `Redo` | Redoes the last undone action (requires `UndoRedo` service) |
| `SplitTask` | Splits the selected task at a chosen date (requires split-task data) |
| `MergeTask` | Merges a split task segment back into the task |

> **Required services for special toolbar items:**
> - `Undo` / `Redo` → inject `UndoRedo` service
> - `SplitTask` / `MergeTask` → inject `Edit` service; `taskFields.segments` must be mapped
> - `CriticalPath` → inject `CriticalPath` service
> - `ExcelExport` / `CsvExport` → inject `ExcelExport` service; set `allowExcelExport={true}`
> - `PdfExport` → inject `PdfExport` service; set `allowPdfExport={true}`
> - `ColumnChooser` → inject `ColumnMenu` service; set `showColumnChooser={true}`

### Basic Toolbar Setup
```tsx
import {
  GanttComponent, Inject, Edit, Toolbar, Selection,
  TaskFieldsModel, EditSettingsModel, ToolbarItem
} from '@syncfusion/ej2-react-gantt';

function App() {
  const taskFields: TaskFieldsModel = {
    id: 'TaskID', name: 'TaskName',
    startDate: 'StartDate', endDate: 'EndDate',
    duration: 'Duration', progress: 'Progress',
    parentID: 'ParentID'
  };

  const editSettings: EditSettingsModel = {
    allowAdding: true, allowEditing: true,
    allowDeleting: true, allowTaskbarEditing: true,
    showDeleteConfirmDialog: true
  };

  const toolbar: ToolbarItem[] = [
    'Add', 'Edit', 'Delete', 'Update', 'Cancel',
    'ExpandAll', 'CollapseAll', 'PrevTimeSpan', 'NextTimeSpan',
    'Indent', 'Outdent', 'Search'
  ];

  return (
    <GanttComponent
      dataSource={data}
      taskFields={taskFields}
      editSettings={editSettings}
      toolbar={toolbar}
      height='430px'
    >
      <Inject services={[Edit, Toolbar, Selection]} />
    </GanttComponent>
  );
}
```

---

## Custom Toolbar Items

Add custom buttons using `ItemModel` objects in the `toolbar` array:

```tsx
import { ItemModel } from '@syncfusion/ej2-navigations';
import { ClickEventArgs } from '@syncfusion/ej2-navigations';

const toolbar: (ToolbarItem | ItemModel)[] = [
  'Add', 'Edit', 'Delete',
  {
    text: 'Refresh',
    tooltipText: 'Refresh Data',
    id: 'toolbar_refresh',
    prefixIcon: 'e-refresh'
  },
  {
    text: 'Export CSV',
    tooltipText: 'Export to CSV',
    id: 'toolbar_csv',
    prefixIcon: 'e-export-csv'
  }
];

const toolbarClick = (args: ClickEventArgs) => {
  if (args.item.id === 'toolbar_refresh') {
    // Custom refresh logic
    ganttRef.current?.reloadProjectData?.();
  }
  if (args.item.id === 'toolbar_csv') {
    // Custom CSV export logic
  }
};

<GanttComponent
  toolbar={toolbar}
  toolbarClick={toolbarClick}
  ...
>
  <Inject services={[Toolbar]} />
</GanttComponent>
```

---

## Override Built-in Toolbar Behavior

Cancel default toolbar actions and run custom logic:
```tsx
const toolbarClick = (args: ClickEventArgs) => {
  if (args.item.id === 'ganttDefault_add') {
    args.cancel = true;  // cancel default add
    // Custom add logic
    const newRecord = {
      TaskID: Math.floor(Math.random() * 1000),
      TaskName: 'New Task',
      StartDate: new Date(),
      Duration: 1, Progress: 0
    };
    ganttRef.current?.addRecord(newRecord);
  }
};
```

> **Tip:** Built-in toolbar item IDs follow the format `{ganttId}_{itemName}` e.g. `ganttDefault_add`, `ganttDefault_delete`.

---

## Toolbar Styling

### Show Icons Only (Hide Text)
```css
.e-gantt .e-toolbar .e-tbar-btn-text,
.e-gantt .e-toolbar .e-toolbar-items .e-toolbar-item .e-tbar-btn-text {
  display: none;
}
```

### Custom Button Appearance
```css
.e-gantt .e-toolbar .e-tbar-btn .e-icons,
.e-gantt .e-toolbar .e-toolbar-items .e-toolbar-item .e-tbar-btn {
  background: #add8e6;
}
```

---

## Context Menu

Right-click context menu for row and header operations.

### Required Module Injection
```tsx
import { ContextMenu } from '@syncfusion/ej2-react-gantt';

<GanttComponent enableContextMenu={true} ...>
  <Inject services={[ContextMenu]} />
</GanttComponent>
```

### Default Context Menu Items

| Item | Description |
|---|---|
| `AutoFit` | Auto-fits the current column |
| `AutoFitAll` | Auto-fits all columns |
| `SortAscending` | Sorts column ascending |
| `SortDescending` | Sorts column descending |
| `TaskInformation` | Opens task edit dialog |
| `Add` | Adds a new row |
| `Indent` | Indents selected record |
| `Outdent` | Outdents selected record |
| `DeleteTask` | Deletes the task |
| `Save` | Saves the edited task |
| `Cancel` | Cancels the edit |
| `DeleteDependency` | Deletes current dependency link |
| `Convert` | Converts task to milestone or vice-versa |
| `SplitTask` | Splits the selected task into segments |
| `MergeTask` | Merges a split segment back into the main task |

### Enable Default Context Menu
```tsx
import { GanttComponent, Inject, Edit, Selection, ContextMenu, Sort, Resize } from '@syncfusion/ej2-react-gantt';

<GanttComponent
  dataSource={data}
  taskFields={taskFields}
  editSettings={{ allowAdding: true, allowEditing: true, allowDeleting: true }}
  allowSorting={true}
  allowResizing={true}
  enableContextMenu={true}
  height='450px'
>
  <Inject services={[Edit, ContextMenu, Selection, Sort, Resize]} />
</GanttComponent>
```

---

## Custom Context Menu Items

Extend with custom items using `contextMenuItems`. Use `target` to scope items to content rows (`.e-content`) or column headers (`.e-gridheader`).

```tsx
const contextMenuItems: any[] = [
  // Built-in items
  'AutoFitAll', 'AutoFit', 'TaskInformation', 'DeleteTask',
  'Save', 'Cancel', 'SortAscending', 'SortDescending',
  'Add', 'DeleteDependency', 'Convert',
  // Custom items for row content
  { text: 'Collapse Row', target: '.e-content', id: 'collapserow' },
  { text: 'Expand Row', target: '.e-content', id: 'expandrow' },
  // Custom item for column header
  { text: 'Hide Column', target: '.e-gridheader', id: 'hidecol' }
];

const contextMenuClick = (args: any) => {
  const record = args.rowData;
  if (args.item.id === 'collapserow') {
    ganttRef.current?.collapseByID(Number(record.ganttProperties.taskId));
  }
  if (args.item.id === 'expandrow') {
    ganttRef.current?.expandByID(Number(record.ganttProperties.taskId));
  }
  if (args.item.id === 'hidecol') {
    ganttRef.current?.hideColumn(args.column.headerText);
  }
};

// Control which custom items are shown per row
const contextMenuOpen = (args: any) => {
  const record = args.rowData;
  if (record && !record.hasChildRecords) {
    // Hide expand/collapse for leaf rows
    args.hideItems = ['Collapse Row', 'Expand Row'];
  }
};

<GanttComponent
  contextMenuItems={contextMenuItems}
  contextMenuClick={contextMenuClick}
  contextMenuOpen={contextMenuOpen}
  enableContextMenu={true}
  ...
>
  <Inject services={[Edit, ContextMenu, Selection, Sort, Resize]} />
</GanttComponent>
```

---

## Toolbar + Context Menu Together

```tsx
import React, { useRef } from 'react';
import {
  GanttComponent, Inject, Edit, Toolbar, Selection,
  ContextMenu, Sort, Resize,
  TaskFieldsModel, EditSettingsModel, ToolbarItem
} from '@syncfusion/ej2-react-gantt';

function App() {
  const ganttRef = useRef<GanttComponent>(null);

  const taskFields: TaskFieldsModel = {
    id: 'TaskID', name: 'TaskName',
    startDate: 'StartDate', duration: 'Duration',
    progress: 'Progress', dependency: 'Predecessor',
    parentID: 'ParentID'
  };

  const editSettings: EditSettingsModel = {
    allowAdding: true, allowEditing: true,
    allowDeleting: true, allowTaskbarEditing: true
  };

  const toolbar: ToolbarItem[] = [
    'Add', 'Edit', 'Delete', 'Update', 'Cancel',
    'ExpandAll', 'CollapseAll', 'Search'
  ];

  return (
    <GanttComponent
      ref={ganttRef}
      dataSource={data}
      taskFields={taskFields}
      editSettings={editSettings}
      toolbar={toolbar}
      allowSorting={true}
      allowResizing={true}
      enableContextMenu={true}
      height='450px'
    >
      <Inject services={[Edit, Toolbar, Selection, ContextMenu, Sort, Resize]} />
    </GanttComponent>
  );
}

export default App;
```

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| Toolbar buttons not showing | `Toolbar` service not injected | Add `Toolbar` to `services` array |
| Context menu not appearing | `enableContextMenu` not set | Set `enableContextMenu={true}` |
| Context menu items not working | `ContextMenu` service not injected | Add `ContextMenu` to `services` |
| `SortAscending`/`SortDescending` in context menu not working | `Sort` service not injected | Add `Sort` to `services` |
| `AutoFit`/`AutoFitAll` not working | `Resize` service not injected | Add `Resize` to `services` |
| Custom item fires for all rows | Missing `contextMenuOpen` visibility control | Use `args.hideItems` in `contextMenuOpen` to filter |
| `Undo`/`Redo` toolbar buttons not working | `UndoRedo` service not injected or `enableUndoRedo` not set | Inject `UndoRedo` and set `enableUndoRedo={true}` |
| `SplitTask`/`MergeTask` not working | `taskFields.segments` not mapped | Map `segments` in `taskFields` and inject `Edit` |
