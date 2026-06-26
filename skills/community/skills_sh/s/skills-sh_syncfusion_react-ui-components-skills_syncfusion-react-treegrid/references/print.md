---
name: print
description: 'Print in React TreeGrid - print configuration, custom templates, print range selection, hierarchy printing, and print events.'
---

# Print

## Table of Contents
- [Basic Print](#basic-print)
- [Custom Print Configuration](#custom-print-configuration)
- [Print Specific Ranges](#print-specific-ranges)
- [Hierarchy Printing](#hierarchy-printing)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Basic Print

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Print, Toolbar } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      toolbar={['Print']}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
      </ColumnsDirective>
      <Inject services={[Print, Toolbar]} />
    </TreeGridComponent>
  );
}
```

## Custom Print Configuration

Programmatic printing with options:

```tsx
const treeGridRef = React.useRef();

const customPrint = () => {
  treeGridRef.current.print();
};

<TreeGridComponent ref={treeGridRef} dataSource={data} childMapping="Children">
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[Print]} />
</TreeGridComponent>
```

## Print Specific Ranges

Print selected rows or ranges:

```tsx
const printSelectedRows = () => {
  const treeGrid = treeGridRef.current;
  const selectedIndexes = treeGrid.getSelectedRowIndexes();
  
  // Print only selected rows
  treeGrid.print();
};

<TreeGridComponent ref={treeGridRef} dataSource={data} childMapping="Children">
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Hierarchy Printing

Control printing of hierarchical levels:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  printMode="AllPages"  // 'AllPages', 'CurrentPage', 'ExternalExport'
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Key APIs

| Property/Method | Type | Description |
|---|---|---|
| `print` | method | Trigger print dialog |
| `printMode` | string | 'AllPages', 'CurrentPage', 'ExternalExport' |
| `toolbar` | array | Add print button to toolbar |

## Common Patterns

1. **Print Preview**: Preview before printing
2. **Sheet Orientation**: Set portrait/landscape per page
3. **Include Totals**: Print with aggregate row

