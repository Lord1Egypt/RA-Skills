---
name: column-chooser
description: 'Column Chooser in React TreeGrid - enable column visibility toggle, show/hide columns, column chooser dialog, and programmatic column control.'
---

# Column Chooser

## Table of Contents
- [Enable Column Chooser](#enable-column-chooser)
- [Column Chooser Dialog](#column-chooser-dialog)
- [Show/Hide Columns](#showhide-columns)
- [Visibility Events](#visibility-events)
- [Show/Hide Columns Programmatically](#showhide-columns-programmatically)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Enable Column Chooser

Enable users to toggle column visibility:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, ColumnChooser, Toolbar } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', StartDate: new Date(2018, 2, 3), EndDate: new Date(2018, 2, 7), Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      toolbar={['ColumnChooser']}
      showColumnChooser={true}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="StartDate" headerText="Start Date" width={120} type="date" format="yMd" />
        <ColumnDirective field="EndDate" headerText="End Date" width={120} type="date" format="yMd" />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
      </ColumnsDirective>
      <Inject services={[ColumnChooser, Toolbar]} />
    </TreeGridComponent>
  );
}
```

## Column Chooser Dialog

Configure column chooser settings:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  showColumnChooser={true}
  columnChooserSettings={{
    title: 'Column Visibility',
    columnsItemsCount: 5,  // Items per scroll
    search: true,          // Search box in dialog
    hideColumns: []        // Columns hidden by default
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} showInColumnChooser={true} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} showInColumnChooser={true} />
    <ColumnDirective field="Priority" headerText="Priority" width={100} showInColumnChooser={true} />
  </ColumnsDirective>
  <Inject services={[ColumnChooser]} />
</TreeGridComponent>
```

## Show/Hide Columns

Hide columns from column chooser:

```tsx
<ColumnsDirective>
  <ColumnDirective 
    field="TaskID" 
    headerText="Task ID" 
    width={80} 
    showInColumnChooser={false}  // Not shown in chooser
  />
  <ColumnDirective field="TaskName" headerText="Task Name" width={160} showInColumnChooser={true} />
</ColumnsDirective>
```

## Show/Hide Columns Programmatically

Control column visibility via code:

```tsx
const treeGridRef = React.useRef();

const hideColumn = (fieldName) => {
  const column = treeGridRef.current.columns.find(col => col.field === fieldName);
  if (column) {
    column.visible = false;
    treeGridRef.current.refreshColumns();
  }
};

const showColumn = (fieldName) => {
  const column = treeGridRef.current.columns.find(col => col.field === fieldName);
  if (column) {
    column.visible = true;
    treeGridRef.current.refreshColumns();
  }
};

const toggleColumn = (fieldName) => {
  const column = treeGridRef.current.columns.find(col => col.field === fieldName);
  if (column) {
    column.visible = !column.visible;
    treeGridRef.current.refreshColumns();
  }
};

<TreeGridComponent 
  ref={treeGridRef}
  dataSource={data} 
  childMapping="Children"
  showColumnChooser={true}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[ColumnChooser]} />
</TreeGridComponent>
```

## Visibility Events

Listen to column visibility changes:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  showColumnChooser={true}
  columnHide={(args) => {
    console.log('Column hidden:', args.column.field);
  }}
  columnShow={(args) => {
    console.log('Column shown:', args.column.field);
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[ColumnChooser]} />
</TreeGridComponent>
```

## Key APIs

| Property/Event | Type | Description |
|---|---|---|
| `showColumnChooser` | boolean | Enable column chooser |
| `columnChooserSettings` | object | Configure chooser dialog |
| `showInColumnChooser` | boolean | Show column in chooser dialog |
| `visible` | boolean | Column visibility |
| `columnHide` | event | Fired when column is hidden |
| `columnShow` | event | Fired when column is shown |

## Common Patterns

1. **User Preferences**: Save visible columns per user
2. **Report Builder**: Let users select columns to display
3. **Mobile Optimization**: Hide columns on small screens
4. **Role-based Visibility**: Show different columns per role

