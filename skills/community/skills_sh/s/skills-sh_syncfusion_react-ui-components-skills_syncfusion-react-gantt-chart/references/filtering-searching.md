# Filtering and Searching in Syncfusion React Gantt Chart

## Table of Contents
- [Enable Filtering](#enable-filtering)
- [Filter Hierarchy Modes](#filter-hierarchy-modes)
- [Filter Menu](#filter-menu)
- [Excel-Like Filter](#excel-like-filter)
- [Toolbar Search](#toolbar-search)
- [Programmatic Filtering](#programmatic-filtering)
- [Initial Filter State (Pre-filtered on Load)](#initial-filter-state-pre-filtered-on-load)
- [Custom Filter Predicates](#custom-filter-predicates)

---

## Enable Filtering

```tsx
import { GanttComponent, Inject, Filter } from '@syncfusion/ej2-react-gantt';

<GanttComponent allowFiltering={true} ...>
  <Inject services={[Filter]} />
</GanttComponent>
```

When enabled, each column header shows a filter icon. Click it to open the filter menu.

---

## Filter Hierarchy Modes

Control how parent/child rows are shown with filtered results:

| Mode | Behavior |
|---|---|
| `"Parent"` (default) | Shows filtered records + their parent records |
| `"Child"` | Shows filtered records + their child records |
| `"Both"` | Shows filtered records + both parents and children |
| `"None"` | Shows only the filtered records (no hierarchy) |

```tsx
import { FilterSettingsModel } from '@syncfusion/ej2-gantt';

const filterSettings: FilterSettingsModel = {
  hierarchyMode: 'Both',
};

<GanttComponent allowFiltering={true} filterSettings={filterSettings} ...>
  <Inject services={[Filter]} />
</GanttComponent>
```

---

## Filter Menu

The filter menu appears when clicking a column's filter icon. It supports operators based on column type:

- **String columns:** Contains, Does Not Contain, Starts With, Ends With, Equal, Not Equal
- **Number columns:** Equal, Not Equal, Greater Than, Greater Than or Equal, Less Than, Less Than or Equal
- **Date columns:** Equal, Not Equal, Greater Than, Less Than, etc.

```tsx
// Filter type is automatically set based on column type
// Customize per column:
<ColumnDirective
  field="Duration"
  type="number"
  filter={{ type: 'Menu' }}  // explicit 'Menu' or 'CheckBox' or 'Excel'
/>
```

---

## Excel-Like Filter

The Excel-like filter shows a checklist of unique values per column for quick filtering:

```tsx
const filterSettings: FilterSettingsModel = {
  type: 'Excel',  // enables Excel-like filter across all columns
};

<GanttComponent allowFiltering={true} filterSettings={filterSettings} ...>
  <Inject services={[Filter]} />
</GanttComponent>
```

Or enable per column:

```tsx
<ColumnDirective field="TaskName" filter={{ type: 'Excel' }} />
```

---

## Toolbar Search

Add a search box to the toolbar to filter rows by text across all columns:

```tsx
<GanttComponent
  toolbar={['Search']}
  searchSettings={{ fields: ['TaskName', 'Duration'], operator: 'contains', ignoreCase: true }}
  ...
>
  <Inject services={[Toolbar]} />
</GanttComponent>
```

### Search Settings

| Prop | Default | Description |
|---|---|---|
| `fields` | all columns | Which fields to search in |
| `operator` | `'contains'` | Search operator |
| `key` | `''` | Initial search value |
| `ignoreCase` | `true` | Case-insensitive search |

### Programmatic Search

```tsx
ganttRef.current?.search('Design');    // search for "Design"
ganttRef.current?.clearSearching();    // clear search
```

---

## Programmatic Filtering

```tsx
import { Predicate } from '@syncfusion/ej2-data';

// Filter a single column
ganttRef.current?.filterByColumn('Duration', 'greaterthan', 3);

// Clear all filters
ganttRef.current?.clearFiltering();

// Clear filter for a specific column
ganttRef.current?.clearFiltering(['Duration']);
```

---

## Initial Filter State (Pre-filtered on Load)

Use `filterSettings.columns` to apply filters when the Gantt first renders — no user interaction needed:

```tsx
import { FilterSettingsModel } from '@syncfusion/ej2-gantt';

const filterSettings: FilterSettingsModel = {
  columns: [
    { field: 'Duration', matchCase: false, operator: 'greaterthan', predicate: 'and', value: 2 },
    { field: 'Progress', matchCase: false, operator: 'greaterthan', predicate: 'and', value: 50 },
  ],
};

<GanttComponent
  allowFiltering={true}
  filterSettings={filterSettings}
  ...
>
  <Inject services={[Filter]} />
</GanttComponent>
```

**Column filter object properties:**
| Property | Type | Description |
|---|---|---|
| `field` | string | Column field name to filter |
| `operator` | string | Filter operator (`'contains'`, `'equal'`, `'greaterthan'`, `'lessthan'`, etc.) |
| `value` | any | Filter value |
| `predicate` | `'and'` \| `'or'` | Logic used to chain with other filter conditions |
| `matchCase` | boolean | Case-sensitive matching |

---

## Custom Filter Predicates

```tsx
import { Predicate } from '@syncfusion/ej2-data';

// Apply complex filter: Duration > 3 AND Progress < 50
const predicate1 = new Predicate('Duration',  'greaterthan', 3);
const predicate2 = new Predicate('Progress',  'lessthan',    50);

ganttRef.current?.filterByColumn('Duration', 'greaterthan', 3);
// Chain predicates for multi-column filter via filterSettings.columns:
const filterSettings = {
  columns: [
    { field: 'Duration', matchCase: false, operator: 'greaterthan', predicate: 'and', value: 3 },
    { field: 'Progress', matchCase: false, operator: 'lessthan',    predicate: 'and', value: 50 },
  ],
};

<GanttComponent allowFiltering={true} filterSettings={filterSettings} .../>
```
