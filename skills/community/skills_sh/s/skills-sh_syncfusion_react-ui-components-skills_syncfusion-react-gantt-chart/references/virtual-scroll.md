# Virtual Scroll in Syncfusion React Gantt Chart

## Table of Contents
- [Overview](#overview)
- [Row Virtualization](#row-virtualization)
- [Timeline Virtualization](#timeline-virtualization)
- [Row + Timeline Virtualization Together](#row--timeline-virtualization-together)
- [Accessing Filtered Data with Virtual Scroll](#accessing-filtered-data-with-virtual-scroll)
- [Virtual Scroll Limitations](#virtual-scroll-limitations)
- [Common Pitfalls](#common-pitfalls)

---

## Overview

Virtual scroll optimizes rendering performance for large datasets. The Gantt component supports two independent virtualization modes:

| Mode | Prop | Purpose |
|---|---|---|
| **Row virtualization** | `enableVirtualization={true}` | Renders only visible rows in the DOM |
| **Timeline virtualization** | `enableTimelineVirtualization={true}` | Renders timeline cells on-demand as user scrolls |

Both require the `VirtualScroll` service to be injected.

---

## Row Virtualization

Only the rows visible within the component height are rendered in the DOM. The full dataset is held in memory, and the DOM updates as the user scrolls vertically.

```tsx
import {
  GanttComponent, Inject, VirtualScroll, Selection
} from '@syncfusion/ej2-react-gantt';

function App() {
  return (
    <GanttComponent
      enableVirtualization={true}
      dataSource={largeDataset}      // thousands of records
      taskFields={taskFields}
      height='450px'                 // fixed pixel height required
    >
      <Inject services={[VirtualScroll, Selection]} />
    </GanttComponent>
  );
}
```

### Key Behavior

- All records are fetched up-front; only visible rows are rendered in the DOM
- The number of rendered rows is determined by the component `height`
- As the user scrolls, old rows are removed and new rows are inserted into the DOM
- `height` must be set in **pixels** — percentage values do not work for row count calculation

---

## Timeline Virtualization

The timeline (horizontal axis) renders only the cells covering 3× the component width initially. As the user scrolls horizontally, additional timeline cells are rendered on-demand. This is ideal for projects spanning years or decades.

```tsx
<GanttComponent
  enableTimelineVirtualization={true}
  projectStartDate={new Date('2024-01-01')}
  projectEndDate={new Date('2030-12-31')}
  autoCalculateDateScheduling={false}
  dataSource={data}
  taskFields={taskFields}
  height='450px'
>
  <Inject services={[VirtualScroll]} />
</GanttComponent>
```

### Requirements

| Requirement | Reason |
|---|---|
| `projectStartDate` + `projectEndDate` | Defines the total timespan for virtual rendering |
| `autoCalculateDateScheduling={false}` | Prevents Gantt from overriding the explicit date range |
| `VirtualScroll` service injected | Required for timeline virtualization to work |

### Behavior

- Initially renders timeline cells covering **3× the visible component width**
- As user scrolls horizontally, cells beyond the initial render area are created on-demand
- Significantly reduces initial DOM size for multi-year projects

---

## Row + Timeline Virtualization Together

Combine both for maximum performance on large, long-running projects:

```tsx
import {
  GanttComponent, Inject, VirtualScroll, Selection
} from '@syncfusion/ej2-react-gantt';

function App() {
  return (
    <GanttComponent
      enableVirtualization={true}          // row virtualization
      enableTimelineVirtualization={true}  // timeline virtualization
      projectStartDate={new Date('2024-01-01')}
      projectEndDate={new Date('2030-12-31')}
      autoCalculateDateScheduling={false}
      dataSource={largeDataset}
      taskFields={taskFields}
      height='450px'
    >
      <Inject services={[VirtualScroll, Selection]} />
    </GanttComponent>
  );
}
```

---

## Accessing Filtered Data with Virtual Scroll

When filtering is combined with virtual scroll, use `actionComplete` to get the accurate filtered record count from the internal filter module:

```tsx
const ganttRef = React.useRef<GanttComponent>(null);

const actionComplete = (args: any) => {
  if (args.requestType === 'filtering') {
    const filteredCount =
      ganttRef.current?.treeGrid.filterModule.filteredResult.length;
    console.log('Filtered record count:', filteredCount);
  }
};

<GanttComponent
  ref={ganttRef}
  enableVirtualization={true}
  allowFiltering={true}
  actionComplete={actionComplete}
  ...
>
  <Inject services={[VirtualScroll, Filter]} />
</GanttComponent>
```

> Do not rely on `dataSource.length` after filtering — use `treeGrid.filterModule.filteredResult` for accuracy.

---

## Virtual Scroll Limitations

| Limitation | Details | Workaround |
|---|---|---|
| Max records limited by browser memory | Typically 10K–100K rows depending on browser and device | Use server-side filtering or pagination for very large datasets |
| Cell selection not persisted | On-demand row rendering discards cell selection state on scroll | Use row selection instead, or re-select after scrolling |
| Height must be in pixels | Percentage heights (`'100%'`) do not work for row count calculation | Always set a fixed `height='450px'` or similar |
| Expand/collapse state may reset | Virtual re-renders can lose expand/collapse state | Map `taskFields.expandState` to a boolean field in your data |
| Filtered count access | Standard length checks are inaccurate after filtering | Use `actionComplete` + `treeGrid.filterModule.filteredResult.length` |

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| Virtual scroll not working | `VirtualScroll` service not injected | Add `VirtualScroll` to `services` |
| No performance improvement | `height` not set in pixels | Set `height='450px'` (fixed pixels) |
| Timeline virtualization broken | `projectStartDate` / `projectEndDate` not set | Set both to define the full project timespan |
| Timeline cells missing on scroll | `autoCalculateDateScheduling` not disabled | Set `autoCalculateDateScheduling={false}` |
| Expand state lost on scroll | No `expandState` field mapped | Add `taskFields.expandState: 'isExpand'` to your data |
