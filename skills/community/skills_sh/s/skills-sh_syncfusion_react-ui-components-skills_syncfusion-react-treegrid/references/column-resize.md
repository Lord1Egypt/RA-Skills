---
name: column-resize
description: 'Column Resize in React TreeGrid - enable column drag resize, auto-fit columns, minimum/maximum width, resize events, and programmatic resize.'
---

# Column Resize

## Table of Contents
- [Enable Column Resize](#enable-column-resize)
- [Resize Configuration](#resize-configuration)
- [Disable Resize for Specific Columns](#disable-resize-for-specific-columns)
- [Auto-fit Columns](#auto-fit-columns)
- [Column Width Constraints](#column-width-constraints)
- [Resize Events](#resize-events)
- [Programmatic Column Width Change](#programmatic-column-width-change)

## Enable Column Resize

Enable users to resize columns by dragging:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Resize } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Description: 'Project planning and preparation', Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      allowResizing={true}
      treeColumnIndex={1}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Description" headerText="Description" width={200} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
      </ColumnsDirective>
      <Inject services={[Resize]} />
    </TreeGridComponent>
  );
}
```

## Resize Configuration

Configure resize behavior:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  allowResizing={true}
  resizeSettings={{
    mode: 'Normal'  // 'Normal' or 'Auto'
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} allowResizing={true} />
  </ColumnsDirective>
  <Inject services={[Resize]} />
</TreeGridComponent>
```

## Disable Resize for Specific Columns

Prevent resizing on individual columns:

```tsx
<ColumnsDirective>
  <ColumnDirective 
    field="TaskID" 
    headerText="Task ID" 
    width={80} 
    allowResizing={false}  // This column cannot be resized
  />
  <ColumnDirective field="TaskName" headerText="Task Name" width={160} allowResizing={true} />
</ColumnsDirective>
```

## Auto-fit Columns

Automatically fit columns to content:

```tsx
const treeGridRef = React.useRef();

const autoFitColumns = () => {
  treeGridRef.current.autoFitColumns();  // All columns
};

const autoFitSpecificColumns = () => {
  treeGridRef.current.autoFitColumns(['TaskName', 'Description']);  // Specific columns
};

<TreeGridComponent ref={treeGridRef} dataSource={data} childMapping="Children" allowResizing={true}>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
    <ColumnDirective field="Description" headerText="Description" width={200} />
  </ColumnsDirective>
  <Inject services={[Resize]} />
</TreeGridComponent>
```

## Column Width Constraints

Set minimum and maximum width:

```tsx
<ColumnsDirective>
  <ColumnDirective 
    field="TaskName" 
    headerText="Task Name" 
    width={160}
    minWidth={100}   // Minimum width on resize
    maxWidth={300}   // Maximum width on resize
  />
  <ColumnDirective 
    field="Description" 
    headerText="Description" 
    width={200}
    minWidth={150}
    maxWidth={500}
  />
</ColumnsDirective>
```

## Resize Events

Listen to column resize events:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  allowResizing={true}
  resizeStart={(args) => {
    console.log('Resize started for column:', args.column.field);
    console.log('Current width:', args.column.width);
  }}
  resizing={(args) => {
    console.log('Resizing column:', args.column.field);
    console.log('New width:', args.newWidth);
  }}
  resizeStop={(args) => {
    console.log('Resize completed for column:', args.column.field);
    console.log('Final width:', args.column.width);
    // Save new width to database
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[Resize]} />
</TreeGridComponent>
```

## Programmatic Column Width Change

Set column width via code:

```tsx
const setColumnWidth = (fieldName, width) => {
  const column = treeGridRef.current.columns.find(col => col.field === fieldName);
  if (column) {
    column.width = width;
    treeGridRef.current.refreshColumns();
  }
};

// Usage:
setColumnWidth('TaskName', 250);
```

## Key APIs

| Property/Event | Type | Description |
|---|---|---|
| `allowResizing` | boolean | Enable column resizing |
| `resizeSettings` | object | Resize configuration |
| `allowResizing` (column) | boolean | Allow resize for specific column |
| `minWidth` | number/string | Minimum column width |
| `maxWidth` | number/string | Maximum column width |
| `resizeStart` | event | Fired when resize starts |
| `resizing` | event | Fired while resizing |
| `resizeStop` | event | Fired when resize completes |
| `autoFitColumns` | method | Auto-fit to content |

## Common Patterns

1. **Responsive Resize**: Adjust widths based on screen size
2. **User Preferences**: Save column widths per user
3. **Min/Max Constraints**: Ensure columns stay readable
4. **Content-based Auto-fit**: Resize to fit longest content
5. **Fixed Column Width**: Lock specific columns

