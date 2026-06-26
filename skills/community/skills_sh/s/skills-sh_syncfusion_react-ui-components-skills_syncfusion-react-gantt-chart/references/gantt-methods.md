# Gantt Chart — Programmatic Methods Reference
Methods not covered in any other reference file. Use as a supplement for programmatic control.

## Table of Contents
- [autoFitColumns](#autofitcolumns)
- [cancelEdit](#canceledit)
- [changeTaskMode](#changetaskmode)
- [clearRedoCollection](#clearredocollection)
- [clearUndoCollection](#clearundocollection)
- [collapseByIndex](#collapsebyindex)
- [convertToMilestone](#converttomilestone)
- [deleteRecord](#deleterecord)
- [enableItems](#enableitems)
- [expandByIndex](#expandbyindex)
- [getCurrentViewData](#getcurrentviewdata)
- [getDurationString](#getdurationstring)
- [getExpandedRecords](#getexpandedrecords)
- [getGanttColumns](#getganttcolumns)
- [getGridColumns](#getgridcolumns)
- [getRecordByID](#getrecordbyid)
- [getRedoActions](#getredoactions)
- [getRowByID](#getrowbyid)
- [getRowByIndex](#getrowbyindex)
- [getTaskByUniqueID](#gettaskbyuniqueid)
- [getTaskInfo](#gettaskinfo)
- [getTaskbarHeight](#gettaskbarheight)
- [getUndoActions](#getundoactions)
- [getWorkString](#getworkstring)
- [openAddDialog](#openadddialog)
- [openEditDialog](#openeditdialog)
- [removeSortColumn](#removesortcolumn)
- [reorderRows](#reorderrows)
- [scrollToTask](#scrolltotask)
- [selectCells](#selectcells)
- [updateChartScrollOffset](#updatechartscrolloffset)
- [updateDataSource](#updatedatasource)
- [updateProjectDates](#updateprojectdates)
- [updateRecordByID](#updaterecordbyid)
- [updateRecordByIndex](#updaterecordbyindex)
- [updateTaskId](#updatetaskid)

---

## autoFitColumns

Adjusts column width(s) to fit content. Call inside `dataBound` for initial render.

```tsx
ganttRef.current?.autoFitColumns('TaskName');
ganttRef.current?.autoFitColumns(['TaskName', 'StartDate', 'Duration']);
ganttRef.current?.autoFitColumns(); // all columns
```

| Parameter | Type | Description |
|---|---|---|
| `fieldNames` *(optional)* | `string \| string[]` | Column field name(s) to auto-fit. Omit for all. |

---

## cancelEdit

Cancels the active edit operation and reverts unsaved changes. `ganttRef.current?.cancelEdit();`

---

## changeTaskMode

Changes the scheduling mode of a task at runtime (`Auto`, `Manual`, or `Custom`).

```tsx
const record = ganttRef.current?.getRecordByID('3');
if (record) {
  record.taskData.taskMode = 1; // 0=Auto, 1=Manual, 2=Custom
  ganttRef.current?.changeTaskMode(record.taskData);
}
```

| Parameter | Type | Description |
|---|---|---|
| `data` | `Object` | Task data object with updated `taskMode`. |

---

## clearRedoCollection

Clears the redo history stack. `ganttRef.current?.clearRedoCollection();`

> Requires `enableUndoRedo={true}` and `UndoRedo` service injected.

---

## clearUndoCollection

Clears the undo history stack. `ganttRef.current?.clearUndoCollection();`

> Requires `enableUndoRedo={true}` and `UndoRedo` service injected.

---

## collapseByIndex

Collapses a parent row at the given zero-based index. `ganttRef.current?.collapseByIndex(2);`

**Parameter:** `index` — `number`

---

## convertToMilestone

Converts a task into a milestone (sets duration to zero). `ganttRef.current?.convertToMilestone('5');`

**Parameter:** `id` — `string`

---

## deleteRecord

Deletes one or more task records by ID, index, or `IGanttData` reference.

```tsx
ganttRef.current?.deleteRecord(3);                  // single ID
ganttRef.current?.deleteRecord([2, 3, 5]);          // multiple IDs
ganttRef.current?.deleteRecord(record);             // IGanttData ref
```

**Parameter:** `taskDetail` — `number | string | number[] | string[] | IGanttData | IGanttData[]`

---

## enableItems

Enables or disables toolbar items by their item ID strings.

```tsx
ganttRef.current?.enableItems(['GanttToolbar_add', 'GanttToolbar_delete'], false);
```

**Parameters:** `items: string[]` — toolbar item IDs. `isEnable: boolean` — `true` to enable, `false` to disable.

---

## expandByIndex

Expands one or more parent rows by zero-based index. `ganttRef.current?.expandByIndex(1);` or `ganttRef.current?.expandByIndex([0, 2, 4]);`

**Parameter:** `index` — `number | number[]`

---

## getCurrentViewData

Returns visible task records after all active filters, sorts, and CRUD operations. **Returns:** `Object[]`

```tsx
const visibleRecords: Object[] = ganttRef.current?.getCurrentViewData() ?? [];
```

---

## getDurationString

Formats a duration value with its unit into a readable string (e.g. `"3 days"`).

```tsx
ganttRef.current?.getDurationString(3, 'day');   // "3 days"
ganttRef.current?.getDurationString(8, 'hour');  // "8 hours"
```

| Parameter | Type | Description |
|---|---|---|
| `duration` | `number` | Numeric duration value. |
| `durationUnit` | `string` | `'day'`, `'hour'`, or `'minute'`. |

**Returns:** `string`

---

## getExpandedRecords

Returns only expanded records from a given collection. **Returns:** `IGanttData[]`

```tsx
const expanded = ganttRef.current?.getExpandedRecords(ganttRef.current.flatData);
```

**Parameter:** `records` — `IGanttData[]`

---

## getGanttColumns

Returns the current Gantt column model definitions. **Returns:** `ColumnModel[]`

```tsx
const columns = ganttRef.current?.getGanttColumns();
```

---

## getGridColumns

Returns raw TreeGrid `Column` objects — useful for runtime updates to `visible`, `width`, or `format`. **Returns:** `Column[]`

```tsx
const gridCols = ganttRef.current?.getGridColumns();
```

---

## getRecordByID

Retrieves the `IGanttData` object for a task by its ID string. **Returns:** `IGanttData`

```tsx
const record = ganttRef.current?.getRecordByID('3');
```

**Parameter:** `id` — `string`

---

## getRedoActions

Returns the current redo stack. Each item has `action` (e.g. `'add'`, `'delete'`, `'sorting'`) and `modifiedRecords`.

```tsx
const redoStack = ganttRef.current?.getRedoActions();
redoStack?.forEach(item => console.log(item.action));
```

**Returns:** `Object[]`

> Requires `enableUndoRedo={true}` and `UndoRedo` service.

---

## getRowByID

Returns the DOM `HTMLElement` for the chart row matching the given task ID. **Returns:** `HTMLElement`

```tsx
const rowEl = ganttRef.current?.getRowByID('5');
```

**Parameter:** `id` — `string | number`

---

## getRowByIndex

Returns the DOM `HTMLElement` for the chart row at the given zero-based index. **Returns:** `HTMLElement`

```tsx
const rowEl = ganttRef.current?.getRowByIndex(0);
```

**Parameter:** `index` — `number`

---

## getTaskByUniqueID

Retrieves an `IGanttData` record using its internal unique ID (not the user-defined task ID). **Returns:** `IGanttData`

```tsx
const record = ganttRef.current?.getTaskByUniqueID('some-unique-id');
```

**Parameter:** `id` — `string`

---

## getTaskInfo

Retrieves internal rendering properties (taskbar width, left offset, segments) for a task by ID. **Returns:** `IGanttTaskInfo`

```tsx
const info = ganttRef.current?.getTaskInfo('3');
console.log(info?.width, info?.left, info?.segments);
```

**Parameter:** `taskId` — `string`

---

## getTaskbarHeight

Returns the configured taskbar row height in pixels. **Returns:** `number`

```tsx
const height: number = ganttRef.current?.getTaskbarHeight() ?? 0;
```

---

## getUndoActions

Returns the current undo stack. Each item has `action` and `modifiedRecords`.

```tsx
const undoStack = ganttRef.current?.getUndoActions();
undoStack?.forEach(item => console.log(item.action));
```

**Returns:** `Object[]`

> Requires `enableUndoRedo={true}` and `UndoRedo` service.

---

## getWorkString

Formats a work value with its unit into a readable string (e.g. `"24 hours"`).

```tsx
ganttRef.current?.getWorkString(24, 'hour'); // "24 hours"
```

| Parameter | Type | Description |
|---|---|---|
| `work` | `number` | Numeric work value. |
| `workUnit` | `string` | `'day'`, `'hour'`, or `'minute'`. |

**Returns:** `string`

---

## openAddDialog

Opens the add task dialog programmatically. `ganttRef.current?.openAddDialog();`

> Requires `editSettings.allowAdding={true}` and `Edit` service injected.

---

## openEditDialog

Opens the edit dialog for a specific task ID, or for the currently selected row if omitted.

```tsx
ganttRef.current?.openEditDialog(3);
ganttRef.current?.openEditDialog(); // selected row
```

| Parameter | Type | Description |
|---|---|---|
| `taskId` *(optional)* | `number \| string` | Task ID to open edit dialog for. |

> Requires `editSettings.allowEditing={true}` and `Edit` service injected.

---

## removeSortColumn

Removes the sort on a specific column without affecting other sorted columns.

```tsx
ganttRef.current?.removeSortColumn('StartDate');
```

**Parameter:** `columnName` — `string`

---

## reorderRows

Moves rows from source indexes to a target drop position.

```tsx
ganttRef.current?.reorderRows([2, 3], 0, 'above');
ganttRef.current?.reorderRows([4], 1, 'child');
```

| Parameter | Type | Description |
|---|---|---|
| `fromIndexes` | `number[]` | Zero-based indexes of rows to move. |
| `toIndex` | `number` | Zero-based index of the target row. |
| `position` | `string` | `'above'`, `'below'`, or `'child'`. |

> Requires `allowRowDragAndDrop={true}` and `RowDD` service injected.

---

## scrollToTask

Scrolls the chart timeline to bring the taskbar of the specified task into view.

```tsx
ganttRef.current?.scrollToTask('5');
```

**Parameter:** `taskId` — `string`

---

## selectCells

Selects multiple cells by row and column index pairs.

```tsx
ganttRef.current?.selectCells([
  { rowIndex: 0, cellIndexes: [1, 2] },
  { rowIndex: 2, cellIndexes: [0] },
]);
```

**Parameter:** `rowCellIndexes` — `ISelectedCell[]` (from `@syncfusion/ej2-grids`)

> Requires `selectionSettings.mode='Cell'` and `Selection` service.

---

## updateChartScrollOffset

Sets both horizontal and vertical scroll positions of the chart pane simultaneously.

```tsx
ganttRef.current?.updateChartScrollOffset(500, 200); // left=500px, top=200px
```

**Parameters:** `left: number` — horizontal px offset. `top: number` — vertical px offset.

---

## updateDataSource

Replaces the entire data source at runtime with optional project date bounds.

```tsx
ganttRef.current?.updateDataSource(newData, {
  projectStartDate: new Date('2024-01-01'),
  projectEndDate: new Date('2024-12-31'),
});
```

| Parameter | Type | Description |
|---|---|---|
| `dataSource` | `Object[]` | New task data collection. |
| `args` | `object` | Optional `projectStartDate` and `projectEndDate` `Date` values. |

---

## updateProjectDates

Updates the project start/end dates, optionally rounding to timeline unit boundaries.

```tsx
ganttRef.current?.updateProjectDates(
  new Date('2024-01-01'),
  new Date('2024-12-31'),
  true  // round off to nearest timeline unit
);
```

| Parameter | Type | Description |
|---|---|---|
| `startDate` | `Date` | New project start date. |
| `endDate` | `Date` | New project end date. |
| `isTimelineRoundOff` | `boolean` | Round to nearest timeline unit boundary. |
| `isFrom` *(optional)* | `string` | Origin context string. |

---

## updateRecordByID

Updates an existing task record by primary key ID. Only provided fields are updated.

```tsx
ganttRef.current?.updateRecordByID({ TaskID: 3, TaskName: 'Updated', Duration: 7 });
```

**Parameter:** `data` — `Object` (task ID + fields to update)

---

## updateRecordByIndex

Updates a task record at the specified zero-based row index.

```tsx
ganttRef.current?.updateRecordByIndex(2, { TaskName: 'Revised', Duration: 4 });
```

**Parameters:** `index: number`, `data: Object`

---

## updateTaskId

Changes an existing task ID to a new unique ID. `ganttRef.current?.updateTaskId(3, 99);`

**Parameters:** `currentId: number | string`, `newId: number | string`
