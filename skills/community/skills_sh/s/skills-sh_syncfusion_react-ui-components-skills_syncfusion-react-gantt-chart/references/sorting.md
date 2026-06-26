# Sorting in Syncfusion React Gantt Chart

## Enable Sorting

```tsx
import { GanttComponent, Inject, Sort } from '@syncfusion/ej2-react-gantt';

<GanttComponent allowSorting={true} ...>
  <Inject services={[Sort]} />
</GanttComponent>
```

Click a column header to sort ascending → click again for descending → click again to clear.

**Multi-column sort:** Hold `Ctrl` and click additional column headers.  
**Clear a column from multi-sort:** Hold `Shift` and click that column header.

---

## Disable Sorting per Column

```tsx
<ColumnDirective field="TaskID" allowSorting={false} />
```

---

## Initial Sort State

Sort on initial render using `sortSettings`:

```tsx
import { SortSettingsModel } from '@syncfusion/ej2-gantt';

const sortSettings: SortSettingsModel = {
  columns: [
    { field: 'Duration',  direction: 'Descending' },
    { field: 'TaskName',  direction: 'Ascending' },
  ],
};

<GanttComponent allowSorting={true} sortSettings={sortSettings} ...>
  <Inject services={[Sort]} />
</GanttComponent>
```

---

## Programmatic Sorting

```tsx
// Sort a single column
ganttRef.current?.sortColumn('Duration', 'Descending', false);

// Multi-sort: pass true as third arg to add to existing sort
ganttRef.current?.sortColumn('TaskName', 'Ascending', true);

// Clear all sorting
ganttRef.current?.clearSorting();
```

---

## Custom Sort Comparer

Override the default comparison logic per column:

```tsx
function customComparer(reference: any, comparer: any) {
  // return negative if reference < comparer
  // return 0 if equal, positive if reference > comparer
  return reference.TaskName.length - comparer.TaskName.length; // sort by name length
}

<ColumnDirective field="TaskName" sortComparer={customComparer} />
```
