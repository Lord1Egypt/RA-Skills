---
name: sorting
description: 'Sorting in React TreeGrid - enable sorting, multi-level sort, sort directions, programmatic sorting, and custom sort comparators.'
---

# Sorting

## Table of Contents
- [Enable Sorting](#enable-sorting)
- [Multi-level Sorting](#multi-level-sorting)
- [Sort Direction](#sort-direction)
- [Sort Events](#sort-events)
- [Programmatic Sorting](#programmatic-sorting)
- [Custom Sorting](#custom-sorting)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Enable Sorting

### Basic Sorting

Enable sorting on TreeGrid by setting `allowSorting` to true:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Sort } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 3, TaskName: 'Design', Priority: 'High', Children: [] },
    { TaskID: 1, TaskName: 'Planning', Priority: 'Normal', Children: [] },
    { TaskID: 2, TaskName: 'Development', Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      allowSorting={true}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
      </ColumnsDirective>
      <Inject services={[Sort]} />
    </TreeGridComponent>
  );
}
```

### Disable Sorting on Specific Column

Prevent sorting on individual columns using `allowSorting={false}`:

```tsx
<ColumnDirective 
  field="TaskID" 
  headerText="Task ID"
  allowSorting={false}
  width={80}
/>
```

## Multi-level Sorting

Sort by multiple columns with different sort directions:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  allowSorting={true}
  sortSettings={{
    columns: [
      { field: 'Priority', direction: 'Ascending' },
      { field: 'TaskName', direction: 'Ascending' }
    ]
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
  <Inject services={[Sort]} />
</TreeGridComponent>
```

## Sort Direction

### Ascending Sort

Sort values in ascending order (A-Z, 0-9):

```javascript
{ field: 'TaskName', direction: 'Ascending' }
```

### Descending Sort

Sort values in descending order (Z-A, 9-0):

```javascript
{ field: 'TaskName', direction: 'Descending' }
```

### Set Initial Sort Direction

Specify initial sort when TreeGrid loads:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  sortSettings={{
    columns: [
      { field: 'Priority', direction: 'Ascending' },
      { field: 'TaskName', direction: 'Descending' }
    ]
  }}
>
  {/* columns */}
</TreeGridComponent>
```

## Sort Events

### Sort Change Event

Listen to sort changes when user clicks column header:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  allowSorting={true}
  sortChange={(args) => {
    console.log('Sort changed:', args);
    console.log('Columns:', args.columns);
    console.log('Direction:', args.direction);
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[Sort]} />
</TreeGridComponent>
```

### Action Complete Event

Detect when sort action completes:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  actionComplete={(args) => {
    if (args.requestType === 'sorting') {
      console.log('Sorting completed');
      console.log('Sorted data:', args.data);
    }
  }}
>
  {/* columns */}
</TreeGridComponent>
```

## Programmatic Sorting

### Sort by Column

Sort a specific column from code:

```tsx
const treeGridRef = React.useRef();

const sortByPriority = () => {
  treeGridRef.current.sortByColumn('Priority', 'Ascending', true);
};

<TreeGridComponent ref={treeGridRef} dataSource={data} childMapping="Children">
  <ColumnsDirective>
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
</TreeGridComponent>
```

### Clear Sorting

Remove all sort columns:

```javascript
treeGridRef.current.clearSorting();
```

### Get Sort Settings

Retrieve current sort configuration:

```javascript
const sortColumns = treeGridRef.current.sortSettings.columns;
console.log('Current sort columns:', sortColumns);
```

## Custom Sorting

### Custom Sort Comparer

Implement custom sort logic for specific data types:

```tsx
const customComparer = (a, b) => {
  // Custom comparison logic for Priority
  const priorityOrder = { 'High': 3, 'Normal': 2, 'Low': 1 };
  return priorityOrder[b.Priority] - priorityOrder[a.Priority];
};

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  sortComparer={customComparer}
>
  <ColumnsDirective>
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
</TreeGridComponent>
```

### Sort with Case Insensitivity

Case-insensitive sorting for string columns:

```javascript
const caseInsensitiveSort = (a, b) => {
  const aValue = (a.TaskName || '').toLowerCase();
  const bValue = (b.TaskName || '').toLowerCase();
  return aValue.localeCompare(bValue);
};
```

### Prevent Initial Sort

Load TreeGrid without any initial sorting:

```tsx
<TreeGridComponent 
  dataSource={data}
  childMapping="Children"
  sortSettings={{ columns: [] }}
>
  {/* columns */}
</TreeGridComponent>
```

---

## Key APIs

| Property/Method | Type | Description |
|---|---|---|
| `allowSorting` | boolean | Enable sorting on TreeGrid |
| `sortSettings` | object | Configure sort columns and direction |
| `columns` | array | Array of sort column definitions |
| `field` | string | Column field to sort by |
| `direction` | string | 'Ascending' or 'Descending' |
| `sortByColumn` | method | Sort by column name |
| `clearSorting` | method | Remove all sorting |
| `sortChange` | event | Fired when sort changes |
| `actionComplete` | event | Fired when sort action completes |

## Common Patterns

1. **Stable Sorting**: Maintain original order for equal values
2. **Multi-level Sorting**: Combine primary and secondary sort columns
3. **Locale-aware Sorting**: Use localeCompare for proper string sorting
4. **Performance**: Add sorting carefully on large datasets to avoid lags

