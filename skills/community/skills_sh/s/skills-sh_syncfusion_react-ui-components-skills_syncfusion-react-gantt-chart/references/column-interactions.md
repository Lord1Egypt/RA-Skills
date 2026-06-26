# Column Interactions in Syncfusion React Gantt Chart

## Table of Contents
- [Column Resizing](#column-resizing)
- [Restrict Resizing with Min/Max Width](#restrict-resizing-with-minmax-width)
- [Prevent Resizing per Column](#prevent-resizing-per-column)
- [Column Resizing Modes](#column-resizing-modes)
- [Resize Columns Programmatically](#resize-columns-programmatically)
- [Column Resize Events](#column-resize-events)
- [Column Reorder (Drag-to-Reorder)](#column-reorder-drag-to-reorder)
- [Disable Reorder per Column](#disable-reorder-per-column)
- [Reorder Columns Programmatically](#reorder-columns-programmatically)
- [Column Reorder Events](#column-reorder-events)
- [Column Menu](#column-menu)
- [Column Visibility Toggle (Column Chooser)](#column-visibility-toggle-column-chooser)

---

## Column Resizing

Allow users to drag column borders to resize:

```tsx
import { Resize } from '@syncfusion/ej2-react-gantt';

<GanttComponent allowResizing={true} ...>
  <Inject services={[Resize]} />
</GanttComponent>
```

Disable resize per column:

```tsx
<ColumnDirective field="TaskID" allowResizing={false} width="80" />
```

> In RTL mode, drag the left edge of the header cell to resize.

---

## Restrict Resizing with Min/Max Width

Set `minWidth` and `maxWidth` on a column to clamp its resize range:

```tsx
<GanttComponent allowResizing={true} ...>
  <ColumnsDirective>
    <ColumnDirective field="TaskID"   width="100" />
    <ColumnDirective field="TaskName" headerText="Task Name" minWidth="200" width="250" maxWidth="300" />
    <ColumnDirective field="Duration" minWidth="100" maxWidth="200" />
    <ColumnDirective field="Progress" />
  </ColumnsDirective>
  <Inject services={[Resize]} />
</GanttComponent>
```

---

## Prevent Resizing per Column

Set `allowResizing={false}` on a specific `ColumnDirective` to lock it:

```tsx
<GanttComponent allowResizing={true} ...>
  <ColumnsDirective>
    <ColumnDirective field="TaskID"   width="100" allowResizing={false} />
    <ColumnDirective field="TaskName" width="250" />
  </ColumnsDirective>
  <Inject services={[Resize]} />
</GanttComponent>
```

You can also cancel resizing programmatically in the `resizeStart` event by setting `args.cancel = true`.

---

## Column Resizing Modes

Two modes control how remaining space is redistributed during resize:

| Mode | Behavior |
|---|---|
| `Normal` | Columns keep defined widths; extra space or scrollbar appears as needed |
| `Auto` | Columns auto-fill available space; no leftover empty space |

Set the mode via the underlying TreeGrid's `resizeSettings`:

```tsx
function load() {
  ganttRef.current!.treeGrid.grid.resizeSettings.mode = 'Auto'; // or 'Normal'
}

<GanttComponent load={load} allowResizing={true} ref={ganttRef} ...>
  <Inject services={[Resize]} />
</GanttComponent>
```

> When `autoFit={true}` is set on the grid, columns auto-size to content. In `Normal` mode leftover space is preserved; in `Auto` mode it is consumed.

---

## Resize Columns Programmatically

Access the column by field name and update its `width`, then call `refreshColumns()`:

```tsx
const ganttRef = React.useRef<GanttComponent>(null);

function resizeTaskName(newWidth: string) {
  const col = (ganttRef.current as any).treeGrid.grid.getColumnByField('TaskName');
  col.width = newWidth;
  (ganttRef.current as any).treeGrid.grid.refreshColumns();
}

<GanttComponent ref={ganttRef} allowResizing={true} ...>
  <Inject services={[Resize]} />
</GanttComponent>
```

---

## Column Resize Events

Three events fire during a resize operation:

| Event | Trigger | Cancel support |
|---|---|---|
| `resizeStart` | User starts dragging | `args.cancel = true` to prevent |
| `resizing` | Fires repeatedly while dragging | — |
| `resizeStop` | User releases the drag | — |

```tsx
function resizeStart(args: any) {
  if (args.column.field === 'TaskID') {
    args.cancel = true; // prevent resizing TaskID
  }
}

function resizeStop(args: any) {
  // Apply custom style after resize
  const header = (ganttRef.current as any).treeGrid.grid
    .getColumnHeaderByField(args.column.field);
  header.classList.add('resized-col');
}

function resizing(args: any) {
  console.log('Resizing column:', args.column.field);
}

<GanttComponent
  allowResizing={true}
  resizeStart={resizeStart}
  resizing={resizing}
  resizeStop={resizeStop}
  ref={ganttRef}
  ...
>
  <Inject services={[Resize]} />
</GanttComponent>
```

---

## Column Reorder (Drag-to-Reorder)

Allow users to drag column headers to change order:

```tsx
import { Reorder } from '@syncfusion/ej2-react-gantt';

<GanttComponent allowReordering={true} ...>
  <Inject services={[Reorder]} />
</GanttComponent>
```

> After reordering, any logic that depends on column position should be updated to reflect the new order.

---

## Disable Reorder per Column

Set `allowReordering={false}` on a specific `ColumnDirective`:

```tsx
<GanttComponent allowReordering={true} ...>
  <ColumnsDirective>
    <ColumnDirective field="TaskID"   width="90" />
    <ColumnDirective field="TaskName" width="290" allowReordering={false} />  {/* locked */}
    <ColumnDirective field="Duration" width="90" />
  </ColumnsDirective>
  <Inject services={[Reorder]} />
</GanttComponent>
```

---

## Reorder Columns Programmatically

### By Field Name (`reorderColumns`)

Move one or more columns before a target column using field names:

```tsx
const ganttRef = React.useRef<GanttComponent>(null);

// Single column: move TaskName before TaskID
ganttRef.current?.reorderColumns('TaskName', 'TaskID');

// Multiple columns: move TaskName, StartDate, Duration before TaskID
ganttRef.current?.reorderColumns(['TaskName', 'StartDate', 'Duration'], 'TaskID');
```

### By Column Index (`reorderColumnByIndex`)

Move the column at `fromIndex` to `toIndex` via the underlying grid:

```tsx
// Move column at index 1 to index 3
(ganttRef.current as any).treeGrid.grid.reorderColumnByIndex(1, 3);
```

### By Target Index (`reorderColumnByTargetIndex`)

Move one or more columns (by field name) to a specific target index:

```tsx
// Move single column TaskID to index 3
(ganttRef.current as any).treeGrid.grid.reorderColumnByTargetIndex('TaskID', 3);

// Move multiple columns to index 3
(ganttRef.current as any).treeGrid.grid.reorderColumnByTargetIndex(['TaskID', 'TaskName'], 3);
```

---

## Column Reorder Events

Three events fire during drag-based column reorder:

| Event | Trigger |
|---|---|
| `columnDragStart` | User starts dragging a column header |
| `columnDrag` | Fires continuously while dragging |
| `columnDrop` | User drops the column at a new position |

```tsx
import { ColumnDragEventArgs } from '@syncfusion/ej2-react-gantt';

function columnDragStart(args: ColumnDragEventArgs) {
  // Example: change header text on drag start
  if (args.column.field === 'TaskName') {
    args.column.headerText = 'Project Task';
  }
}

function columnDrag(args: ColumnDragEventArgs) {
  // Example: prevent dragging the Duration column
  if (args.column.field === 'Duration') {
    args.column.allowReordering = false;
  }
}

function columnDrop(args: ColumnDragEventArgs) {
  // Example: cancel drop for TaskID column
  if (args.column.field === 'TaskID') {
    args.column.allowReordering = false;
  }
}

<GanttComponent
  allowReordering={true}
  columnDragStart={columnDragStart}
  columnDrag={columnDrag}
  columnDrop={columnDrop}
  ...
>
  <Inject services={[Reorder]} />
</GanttComponent>
```

---

## Column Menu

The column menu shows a dropdown on each column header with options (sort, filter, column chooser, etc.):

```tsx
import { ColumnMenu, Sort, Filter } from '@syncfusion/ej2-react-gantt';

<GanttComponent showColumnMenu={true} allowSorting={true} allowFiltering={true} ...>
  <Inject services={[ColumnMenu, Sort, Filter]} />
</GanttComponent>
```

### Customize Column Menu Items

```tsx
const columnMenuItems = ['SortAscending', 'SortDescending', 'ColumnChooser', 'Filter'];

<GanttComponent
  showColumnMenu={true}
  columnMenuItems={columnMenuItems}
  ...
>
  <Inject services={[ColumnMenu, Sort, Filter]} />
</GanttComponent>
```

Disable column menu per column:

```tsx
<ColumnDirective field="TaskID" showColumnMenu={false} />
```

---

## Column Visibility Toggle (Column Chooser)

Let users show/hide columns via a column chooser dialog:

```tsx
<GanttComponent showColumnChooser={true} toolbar={['ColumnChooser']} ...>
  <Inject services={[Toolbar, ColumnMenu]} />
</GanttComponent>
```

Programmatic show/hide:

```tsx
ganttRef.current?.showColumn(['Notes', 'Resources']);
ganttRef.current?.hideColumn(['Notes']);
```
