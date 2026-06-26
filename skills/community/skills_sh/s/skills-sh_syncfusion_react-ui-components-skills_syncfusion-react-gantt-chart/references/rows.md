# Rows in Syncfusion React Gantt Chart

## Table of Contents
- [Row Drag and Drop](#row-drag-and-drop)
- [Indent and Outdent](#indent-and-outdent)
- [Row Spanning](#row-spanning)
- [Row Height](#row-height)
- [Row Styling](#row-styling)
- [Expand and Collapse Rows](#expand-and-collapse-rows)

---

## Row Drag and Drop

Enable drag-and-drop to reorder or reparent tasks:

```tsx
import { RowDD, Edit, Selection } from '@syncfusion/ej2-react-gantt';

<GanttComponent
  allowRowDragAndDrop={true}
  editSettings={{ allowEditing: true }}
  ...
>
  <Inject services={[RowDD, Edit, Selection]} />
</GanttComponent>
```

**What it does:**
- Drag a row to reorder among siblings
- Drag onto a parent task to reparent (make a child of the target)
- Dropping between rows creates a sibling; dropping onto a task makes it a child

**Drag multiple rows:**
```tsx
<GanttComponent allowRowDragAndDrop={true} selectionSettings={{ type: 'Multiple' }} ...>
  <Inject services={[RowDD, Edit, Selection]} />
</GanttComponent>
```

**Using toolbar for indent/outdent during drag:**
```tsx
toolbar={['Indent', 'Outdent']}
```

---

## Indent and Outdent

Indent moves a task down one level (becomes a child of the task above it).  
Outdent moves a task up one level (becomes a sibling of its parent).

Enable via toolbar buttons:

```tsx
<GanttComponent toolbar={['Indent', 'Outdent']} editSettings={{ allowEditing: true }} ...>
  <Inject services={[Edit, Toolbar]} />
</GanttComponent>
```

Programmatic indent/outdent:

```tsx
const ganttRef = React.useRef<GanttComponent>(null);

ganttRef.current?.indent();   // indent selected task
ganttRef.current?.outdent();  // outdent selected task
```

> The task above the indented row automatically becomes the parent. If there is no task above, indent is not allowed.

---

## Row Spanning

Row spanning allows grid cells to merge across multiple rows, useful for displaying shared labels without duplication. Use the `queryCellInfo` event and set `args.rowSpan`:

```tsx
import { QueryCellInfoEventArgs } from '@syncfusion/ej2-react-gantt';

function queryCellInfo(args: QueryCellInfoEventArgs) {
  // Span TaskID 4's TaskName cell across 2 rows
  if ((args.data as any).TaskID === 4 && args.column.field === 'TaskName') {
    args.rowSpan = 2;
  }
}

<GanttComponent
  dataSource={data}
  taskFields={taskFields}
  gridLines="Both"
  queryCellInfo={queryCellInfo}
  height="400px"
/>
```

**`queryCellInfo` args properties:**

| Property | Description |
|---|---|
| `args.data` | Row data object |
| `args.column` | Column definition object (`field`, `headerText`, etc.) |
| `args.rowSpan` | Number of rows this cell should span (vertical merge) |
| `args.colSpan` | Number of columns this cell should span (horizontal merge) |
| `args.cell` | The actual DOM `<td>` element |

**Combining rowSpan and colSpan:**

```tsx
function queryCellInfo(args: QueryCellInfoEventArgs) {
  if ((args.data as any).TaskID === 2 && args.column.field === 'StartDate') {
    args.rowSpan = 2;   // span 2 rows
    args.colSpan = 2;   // span 2 columns simultaneously
  }
}
```

> Row spanning does not affect the Gantt chart panel — only the TreeGrid (left-side) cells are affected.

---

## Row Height

Set a uniform row height:

```tsx
<GanttComponent rowHeight={40} ... />  {/* pixels */}
```

---

## Row Styling

Customize row appearance per-row using `rowDataBound`:

```tsx
function rowDataBound(args: any) {
  if (args.data.Progress < 50) {
    args.row.style.backgroundColor = '#fff3cd';  // yellow highlight for low progress
  }
  if (args.data.TaskName === 'Critical Milestone') {
    args.row.style.fontWeight = 'bold';
  }
}

<GanttComponent rowDataBound={rowDataBound} .../>
```

---

## Expand and Collapse Rows

**Toolbar buttons:**
```tsx
<GanttComponent toolbar={['ExpandAll', 'CollapseAll']} ...>
  <Inject services={[Toolbar]} />
</GanttComponent>
```

**Programmatic control:**
```tsx
const ganttRef = React.useRef<GanttComponent>(null);

ganttRef.current?.expandAll();            // expand all rows
ganttRef.current?.collapseAll();          // collapse all rows
ganttRef.current?.expandByID(1);          // expand row with TaskID = 1
ganttRef.current?.collapseByID(5);        // collapse row with TaskID = 5
ganttRef.current?.expandAtLevel(2);       // expand rows to depth level 2
```
