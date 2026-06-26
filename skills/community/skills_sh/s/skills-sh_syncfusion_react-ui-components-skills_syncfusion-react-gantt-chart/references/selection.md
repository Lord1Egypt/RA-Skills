# Selection in Syncfusion React Gantt Chart

## Table of Contents
- [Enable Selection](#enable-selection)
- [Row Selection](#row-selection)
- [Cell Selection](#cell-selection)
- [Selection Settings](#selection-settings)
- [Programmatic Selection API](#programmatic-selection-api)
- [Selection Events](#selection-events)

---

## Enable Selection

Selection is enabled by injecting the `Selection` module:

```tsx
import { GanttComponent, Inject, Selection } from '@syncfusion/ej2-react-gantt';

<GanttComponent allowSelection={true} ...>
  <Inject services={[Selection]} />
</GanttComponent>
```

---

## Row Selection

Single row selection (default):

```tsx
const selectionSettings = {
  mode: 'Row',
  type: 'Single',
};

<GanttComponent selectionSettings={selectionSettings} ...>
  <Inject services={[Selection]} />
</GanttComponent>
```

Multiple row selection:

```tsx
const selectionSettings = {
  mode: 'Row',
  type: 'Multiple',  // hold Ctrl to select multiple rows
};
```

Checkbox row selection:

```tsx
// Add a checkbox column for selection
<ColumnsDirective>
  <ColumnDirective type="checkbox" width="50" />
  <ColumnDirective field="TaskName" .../>
</ColumnsDirective>
```

---

## Cell Selection

```tsx
const selectionSettings = {
  mode: 'Cell',
  type: 'Multiple',
};

<GanttComponent selectionSettings={selectionSettings} ...>
  <Inject services={[Selection]} />
</GanttComponent>
```

---

## Selection Settings

| Prop | Values | Default | Description |
|---|---|---|---|
| `mode` | `'Row'` \| `'Cell'` | `'Row'` | Selection scope |
| `type` | `'Single'` \| `'Multiple'` | `'Single'` | How many items can be selected |
| `enableToggle` | boolean | `true` | Click selected row again to deselect |
| `persistSelection` | boolean | `false` | Maintain selection across data operations |

---

## Programmatic Selection API

```tsx
const ganttRef = React.useRef<GanttComponent>(null);

// Select rows by index
ganttRef.current?.selectRow(0);           // select first row
ganttRef.current?.selectRows([0, 2, 4]); // select multiple rows by index

// Select a specific cell: row index, column index
ganttRef.current?.selectCell({ rowIndex: 1, cellIndex: 2 });

// Clear all selections
ganttRef.current?.clearSelection();

// Get selected row indexes
const selectedIndexes = ganttRef.current?.getSelectedRowIndexes();
// Get selected records
const selectedRecords = ganttRef.current?.getSelectedRecords();
```

---

## Selection Events

```tsx
function rowSelected(args: any) {
  console.log('Selected row data:', args.data);
  console.log('Selected row index:', args.rowIndex);
}

function rowDeselected(args: any) {
  console.log('Deselected row data:', args.data);
}

function cellSelected(args: any) {
  console.log('Selected cell:', args.cellIndex, args.data);
}

<GanttComponent
  rowSelected={rowSelected}
  rowDeselected={rowDeselected}
  cellSelected={cellSelected}
  ...
/>
```
