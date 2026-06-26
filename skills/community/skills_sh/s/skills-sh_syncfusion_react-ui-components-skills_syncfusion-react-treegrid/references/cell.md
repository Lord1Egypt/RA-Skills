---
name: cell
description: 'Cell Operations in React TreeGrid - cell editing, cell templates, cell styling, cell selection, and cell formatting.'
---

# Cell

## Table of Contents
- [Cell Editing](#cell-editing)
- [Cell Templates](#cell-templates)
- [Cell Styling](#cell-styling)
- [Cell Selection](#cell-selection)
- [Cell Formatting](#cell-formatting)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Cell Editing

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Edit, Toolbar } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      editSettings={{ mode: 'Cell', allowEditing: true }}
      toolbar={['Edit', 'Update', 'Cancel']}
      treeColumnIndex={1}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} allowEditing={false} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} editType="dropdownedit" />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar]} />
    </TreeGridComponent>
  );
}
```

## Cell Templates

Use templates for custom cell rendering:

```tsx
const statusCell = (props) => {
  const statusColor = props.Priority === 'High' ? 'red' : 'green';
  return <span style={{ color: statusColor }}>{props.Priority}</span>;
};

<ColumnDirective 
  field="Priority" 
  headerText="Priority" 
  template={statusCell} 
  width={100} 
/>
```

## Cell Styling

Apply custom styling to cells:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  queryCellInfo={(args) => {
    if (args.column.field === 'Priority' && args.data.Priority === 'High') {
      args.cell.style.backgroundColor = 'red';
      args.cell.style.color = 'white';
    }
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Cell Selection

Enable cell-based selection:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  selectionSettings={{ type: 'Cell', mode: 'Box' }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

**Selection Modes**:
- `Single`: Select one cell
- `Multiple`: Select multiple cells with Ctrl+Click
- `Box`: Select cell range

## Cell Formatting

Format cell values:

```tsx
<ColumnsDirective>
  <ColumnDirective field="Budget" headerText="Budget" type="number" format="N2" width={120} />
  <ColumnDirective field="StartDate" headerText="Start Date" type="date" format="yMd" width={120} />
</ColumnsDirective>
```

## Key APIs

| Property/Event | Type | Description |
|---|---|---|
| `template` | JSX | Custom cell render template |
| `editType` | string | Edit type: 'textbox', 'dropdownedit', 'datepickeredit', etc. |
| `allowEditing` | boolean | Enable/disable cell editing for column |
| `queryCellInfo` | event | Customize cell styling |
| `cellDeselecting` | event | Fired before cell deselection |
| `cellSelected` | event | Fired when cell is selected |

## Common Patterns

1. **Conditional Formatting**: Use `queryCellInfo` to apply styles based on values
2. **Custom Editors**: Implement specific edit types for data input
3. **Cell Tooltips**: Add tooltips for cell content
4. **Cell Navigation**: Implement keyboard navigation between cells

