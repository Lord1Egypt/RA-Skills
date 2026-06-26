---
name: row
description: 'Row Operations in React TreeGrid - row templates, row height configuration, row spanning, detail templates, drag-drop, and row styling.'
---

# Row

## Table of Contents
- [Row Templates](#row-templates)
- [Row Height](#row-height)
- [Row Spanning](#row-spanning)
- [Detail Templates](#detail-templates)
- [Row Drag and Drop](#row-drag-and-drop)
- [Indent and Outdent](#indent-and-outdent)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Overview

Rows represent individual records in TreeGrid. Control row appearance, behavior, and interactions through row operations.

## Row Templates

Customize entire row rendering:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [{ TaskID: 1, TaskName: 'Planning', Priority: 'High', Children: [] }];

  const rowTemplate = (props) => {
    return (
      <tr style={{ backgroundColor: props.Priority === 'High' ? '#ffcccc' : 'white' }}>
        <td>{props.TaskID}</td>
        <td>{props.TaskName}</td>
        <td><strong>{props.Priority}</strong></td>
      </tr>
    );
  };

  return (
    <TreeGridComponent dataSource={data} childMapping="Children" rowTemplate={rowTemplate}>
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
      </ColumnsDirective>
      <Inject services={[Page]} />
    </TreeGridComponent>
  );
}
```

## Row Height

Configure row height settings:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  rowHeight={40}
  treeColumnIndex={1}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

**Properties**:
- `rowHeight`: Number (pixels) or 'auto' for automatic height

## Row Spanning

Span cells across multiple columns:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  queryCellInfo={(args) => {
    if (args.rowIndex === 0) {
      args.colSpan = 2; // Span 2 columns for first row
    }
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Detail Templates

Display additional details in expandable rows:

```tsx

const detailTemplate = (props) => {
  return (
    <div style={{ padding: '10px' }}>
      <h4>Details for {props.TaskName}</h4>
      <p>Duration: {props.Duration} days</p>
      <p>Progress: {props.Progress}%</p>
    </div>
  );
};

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  detailTemplate={detailTemplate}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Row Drag and Drop

Enable dragging rows to reorder:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, RowDD } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    {
      TaskID: 1,
      TaskName: 'Task 1',
      Children: [{ TaskID: 2, TaskName: 'Task 2' }]
    }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      allowRowDragAndDrop={true}
      treeColumnIndex={1}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
      <Inject services={[RowDD]} />
    </TreeGridComponent>
  );
}
```

**Properties**:
- `allowRowDragAndDrop`: Enable drag and drop
- `rowDrop`: Event fired when row is dropped

## Indent and Outdent

Move rows within hierarchy:

```tsx
const toolbarOptions = ['Indent', 'Outdent'];
<TreeGridComponent ref={treeGridRef} dataSource={data} childMapping="Children"  toolbar={toolbarOptions} >
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[Toolbar, RowDD]}/>
</TreeGridComponent>
```

## Key APIs

| Property/Event | Type | Description |
|---|---|---|
| `rowTemplate` | JSX | Custom template for entire row |
| `rowHeight` | number/string | Height of each row |
| `detailTemplate` | JSX | Template for detail row expansion |
| `allowRowDragAndDrop` | boolean | Enable row drag and drop |
| `rowDrop` | event | Fired when row is dropped |
| `rowDataBound` | event | Fired after row is bound to data |
| `rowSelecting` | event | Fired before row selection |

## Common Patterns

1. **Conditional Row Styling**: Use `rowDataBound` event to apply styles based on data
2. **Master-Detail View**: Combine row with detail template for expandable details
3. **Row Grouping**: Use row templates to group visually
4. **Drag Between Trees**: Implement cross-tree drag and drop logic

