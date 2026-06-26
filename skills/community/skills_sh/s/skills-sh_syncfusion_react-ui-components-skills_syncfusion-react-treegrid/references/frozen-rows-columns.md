---
name: frozen-rows-columns
description: 'Frozen Rows and Columns in React TreeGrid - freeze top rows, lock specific columns, isFrozen property, and freeze direction configuration.'
---

# Frozen Rows and Columns

## Table of Contents
- [Freeze Rows](#freeze-rows)
- [Freeze Columns](#freeze-columns)
- [Freeze Direction](#freeze-direction)
- [Lock Specific Columns](#lock-specific-columns)
- [Common Patterns](#common-patterns)
- [Key APIs](#key-apis)

## Freeze Rows

Freeze rows from the top:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Children: [] },
    // ... many records
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      height={400}
      frozenRows={1}  // Freeze first row
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
    </TreeGridComponent>
  );
}
```

## Freeze Columns

Freeze columns from the left:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  height={400}
  frozenColumns={1}  // Freeze first column
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} isFrozen={true} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
    <ColumnDirective field="StartDate" headerText="Start Date" width={120} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Lock Specific Columns

Lock individual columns:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  height={400}
>
  <ColumnsDirective>
    <ColumnDirective 
      field="TaskID" 
      headerText="Task ID" 
      width={80} 
      lockColumn={true}
    />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Freeze Direction
Configure freeze direction for columns:

```tsx
<TreeGridComponent 
  dataSource={data} 
  childMapping="Children" 
  height='310'
>
        <ColumnsDirective>
            <ColumnDirective field='taskID' headerText='Task ID' width='110' textAlign='Right'></ColumnDirective>
            <ColumnDirective field='taskName' headerText='Task Name' width='230' freeze='Left'></ColumnDirective>
            <ColumnDirective field='priority' headerText='Priority' width='110' freeze='Right'></ColumnDirective>
            </ColumnsDirective>
    </TreeGridComponent>;

```


## Key APIs

| Property | Type | Description |
|---|---|---|
| `frozenRows` | number | Number of rows to freeze from top |
| `frozenColumns` | number | Number of columns to freeze from left |
| `isFrozen` | boolean | Freeze specific column |
| `lockColumn` | boolean | Lock column from dragging |

## Common Patterns

1. **Freeze ID Column**: Keep identifier visible when scrolling
2. **Fixed Headers**: Freeze header row for navigation
3. **Multi-freeze**: Combine frozen rows and columns for complex layouts

