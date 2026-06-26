---
name: column-reorder
description: 'Column Reorder in React TreeGrid - enable column drag-and-drop reordering, reorder events, programmatic column reorder, and reorder restrictions.'
---

# Column Reorder

## Table of Contents
- [Enable Column Reorder](#enable-column-reorder)
- [Reorder Configuration](#reorder-configuration)
- [Prevent Specific Columns from Reordering](#prevent-specific-columns-from-reordering)
- [Reorder Events](#reorder-events)
- [Programmatic Column Reordering](#programmatic-column-reordering)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Enable Column Reorder

Enable users to reorder columns by dragging:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Reorder } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', StartDate: new Date(2018, 2, 3), Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      allowReordering={true}
      treeColumnIndex={1}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="StartDate" headerText="Start Date" width={120} type="date" format="yMd" />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
      </ColumnsDirective>
      <Inject services={[Reorder]} />
    </TreeGridComponent>
  );
}
```

## Reorder Configuration

Configure column reorder behavior:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  allowReordering={true}
  reorderSettings={{
    allowReordering: true,
    allowKeyboard: true,  // Keyboard navigation for reorder
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} allowReordering={false} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} allowReordering={true} />
  </ColumnsDirective>
  <Inject services={[Reorder]} />
</TreeGridComponent>
```

## Prevent Specific Columns from Reordering

Disable reorder for specific columns:

```tsx
<ColumnsDirective>
  <ColumnDirective 
    field="TaskID" 
    headerText="Task ID" 
    width={80} 
    allowReordering={false}  // This column cannot be reordered
  />
  <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
</ColumnsDirective>
```

## Reorder Events

Listen to reorder events:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  allowReordering={true}
  columnDragStart={(args) => {
    console.log('Dragging column:', args.column.field);
  }}
  columnDrag={(args) => {
    console.log('Column being dragged over:', args.column);
  }}
  columnDrop={(args) => {
    console.log('Column dropped');
    console.log('From index:', args.fromColumn);
    console.log('To index:', args.toColumn);
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[Reorder]} />
</TreeGridComponent>
```

## Programmatic Column Reordering

Reorder columns via code:

```tsx
const treeGridRef = React.useRef();

const reorderColumns = () => {
  // Move column at index 0 to position 2
  treeGridRef.current.reorderColumns([1, 2, 0]);
};

<TreeGridComponent 
  ref={treeGridRef}
  dataSource={data} 
  childMapping="Children"
  allowReordering={true}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
  <Inject services={[Reorder]} />
</TreeGridComponent>
```


## Key APIs

| Property/Event | Type | Description |
|---|---|---|
| `allowReordering` | boolean | Enable column reordering |
| `reorderSettings` | object | Reorder configuration |
| `allowReordering` (column) | boolean | Allow reordering for specific column |
| `columnDragStart` | event | Fired when column drag starts |
| `columnDrag` | event | Fired while dragging column |
| `columnDrop` | event | Fired when column is dropped |
| `reorderColumns` | method | Programmatically reorder columns |

## Common Patterns

1. **User Preferences**: Save reordered columns per user
2. **Fixed First Column**: Disable reordering for ID columns
3. **Keyboard Navigation**: Allow reordering via arrow keys
4. **Visual Feedback**: Show drop position during drag

