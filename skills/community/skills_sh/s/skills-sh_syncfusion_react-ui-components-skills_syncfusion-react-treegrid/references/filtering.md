---
name: filtering
description: 'Filtering in React TreeGrid - enable filter bar, filter menu, excel-like filtering, custom filters, and programmatic filtering.'
---

# Filtering

## Table of Contents
- [Enable Filtering](#enable-filtering)
- [Filter Bar](#filter-bar)
- [Filter Menu](#filter-menu)
- [Excel-like Filtering](#excel-like-filtering)
- [Filter Events](#filter-events)
- [Programmatic Filtering](#programmatic-filtering)
- [Custom Filters](#custom-filters)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)


## Enable Filtering

Enable filtering on TreeGrid to allow users to filter data:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Filter } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Priority: 'High', Status: 'In Progress', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      allowFiltering={true}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} allowFiltering={true} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
      </ColumnsDirective>
      <Inject services={[Filter]} />
    </TreeGridComponent>
  );
}
```

### Disable Filtering on Specific Column

Prevent filtering on individual columns:

```tsx
<ColumnDirective 
  field="TaskID" 
  headerText="Task ID"
  allowFiltering={false}
  width={80}
/>
```

## Filter Bar

Display filter input box in column headers:

### Basic Filter Bar

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  allowFiltering={true}
  filterSettings={{ type: 'FilterBar' }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
  <Inject services={[Filter]} />
</TreeGridComponent>
```

## Filter Menu

Dropdown filter menu in column headers:

### Filter Menu Configuration

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  allowFiltering={true}
  filterSettings={{ type: 'Menu' }}
>
  <ColumnsDirective>
    <ColumnDirective field="Priority" headerText="Priority" width={100} filter={{ type: 'Menu' }} />
  </ColumnsDirective>
  <Inject services={[Filter]} />
</TreeGridComponent>
```

## Excel-like Filtering

Excel-style filter interface with advanced options:

### Excel Filter Configuration

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  allowFiltering={true}
  filterSettings={{ type: 'Excel' }}
>
  <ColumnsDirective>
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
  <Inject services={[Filter]} />
</TreeGridComponent>
```

## Filter Events

### Action Complete Event

Detect when filter action completes:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  actionComplete={(args) => {
    if (args.requestType === 'filtering') {
      console.log('Filtering completed');
    }
  }}
>
  {/* columns */}
</TreeGridComponent>
```

## Programmatic Filtering

### Filter by Column

Apply filter from code:

```tsx
const treeGridRef = React.useRef();

const filterByPriority = (priority) => {
  treeGridRef.current.filterByColumn('Priority', 'equal', priority);
};

const filterByText = (text) => {
  treeGridRef.current.filterByColumn('TaskName', 'contains', text);
};

<TreeGridComponent ref={treeGridRef} dataSource={data} childMapping="Children">
  <ColumnsDirective>
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
</TreeGridComponent>
```

### Clear Filtering

Remove all filters:

```javascript
treeGridRef.current.clearFiltering();
```

### Get Filter Settings

Retrieve current filter configuration:

```javascript
const filterColumns = treeGridRef.current.filterSettings.columns;
console.log('Current filters:', filterColumns);
```

## Custom Filters

### Implement Custom Filter Logic

Create filters with custom operators:

## Custom Filters

### Implement Custom Filter Logic

Create filters with custom operators:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  filterSettings={{
    type: 'FilterBar',
    columns: [
      {
        field: 'Priority',
        operator: 'equal',
        value: 'High'
      }
    ]
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
  <Inject services={[Filter]} />
</TreeGridComponent>
```

### Filter Operators

Common filter operators:
- `equal` - Exact match
- `notequal` - Not equal to
- `contains` - Contains text
- `startswith` - Starts with
- `endswith` - Ends with
- `lessthan` - Less than
- `greaterthan` - Greater than
- `between` - Between values

---

## Key APIs

| Property/Method | Type | Description |
|---|---|---|
| `allowFiltering` | boolean | Enable filtering on TreeGrid |
| `filterSettings` | object | Configure filter type and columns |
| `type` | string | 'FilterBar', 'Menu', 'Excel' |
| `columns` | array | Array of filter column definitions |
| `filterByColumn` | method | Apply filter to specific column |
| `clearFiltering` | method | Remove all filters |
| `filterChange` | event | Fired when filter changes |
| `actionComplete` | event | Fired when filter action completes |

## Common Patterns

1. **Multi-column Filtering**: Combine filters across multiple columns
2. **Date Range Filters**: Filter between date ranges
3. **Contains Filters**: Case-insensitive partial match filters
4. **Dynamic Filters**: Update filters based on user input

