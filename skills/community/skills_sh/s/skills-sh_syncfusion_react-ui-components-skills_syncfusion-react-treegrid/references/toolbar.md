---
name: toolbar
description: 'Toolbar in React TreeGrid - built-in items (Add, Edit, Delete, Export), custom items, toolbar templates, and toolbar events.'
---

# Toolbar

## Table of Contents
- [Mandatory Rules](#mandatory-rules)
- [Built-in Toolbar Items](#built-in-toolbar-items)
- [Custom Toolbar Items](#custom-toolbar-items)
- [Toolbar Configuration](#toolbar-configuration)
- [Toolbar Events](#toolbar-events)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Mandatory Rules
 
### Rule 1: TreeGridComponent ID is REQUIRED for Toolbar Click Events (Export/Import)
 
When using toolbar click events to handle export (Excel, PDF) or custom actions, you **MUST** provide an `id` attribute on the `<TreeGridComponent>` element.
 
❌ **WRONG** - No ID, toolbar event cannot find the treegrid:
```tsx
<TreeGridComponent dataSource={data} toolbar={['ExcelExport', 'PdfExport']}>
  {/* columns */}
  <Inject services={[Toolbar, ExcelExport, PdfExport]} />
</TreeGridComponent>
```
 
✅ **CORRECT** - ID attribute provided:
```tsx
<TreeGridComponent
  id='grid'
  dataSource={data}
  toolbar={['ExcelExport', 'PdfExport']}
  toolbarClick={onToolbarClick}
>
  {/* columns */}
  <Inject services={[Toolbar, ExcelExport, PdfExport]} />
</TreeGridComponent>
```
 
## Built-in Toolbar Items

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Toolbar, Edit } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      editSettings={{ allowEditing: true, allowAdding: true, allowDeleting: true }}
      toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel', 'Search', 'ExcelExport', 'PdfExport']}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
      </ColumnsDirective>
      <Inject services={[Toolbar, Edit]} />
    </TreeGridComponent>
  );
}
```

## Custom Toolbar Items

Add custom buttons:

```tsx
const customToolbar = [
  { 
    text: 'Custom Action', 
    tooltipText: 'Custom Action',
    id: 'customAction',
    align: 'Right'
  }
];

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  toolbar={customToolbar}
  toolbarClick={(args) => {
    if (args.item.id === 'customAction') {
      console.log('Custom action clicked');
    }
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[Toolbar]} />
</TreeGridComponent>
```

## Toolbar Configuration

Different toolbar Configuration:

```tsx

const toolbar = [
  { text: 'Add', tooltipText: 'Add', prefixIcon: 'e-plus', id: 'add' },
  { type: 'Separator' },
  { 
    text: 'Actions',
    type: 'DropDown',
    items: [
      { text: 'Print', id: 'print' },
      { text: 'Export', id: 'export' }
    ]
  },
  { type: 'Input', text: 'Search' }
];

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  toolbar={toolbar}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[Toolbar]} />
</TreeGridComponent>
```

## Toolbar Events

Handle toolbar interactions:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  toolbar={['Add', 'Edit', 'Delete']}
  toolbarClick={(args) => {
    if (args.item.text === 'Add') {
      console.log('Add clicked');
    }
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[Toolbar, Edit]} />
</TreeGridComponent>
```

## Key APIs

| Property/Event | Type | Description |
|---|---|---|
| `toolbar` | array | Toolbar items configuration |
| `toolbarClick` | event | Fired when toolbar item is clicked |
| `text` | string | Button label |
| `id` | string | Unique identifier |
| `align` | string | 'Left', 'Right', 'Center' |
| `type` | string | 'Button', 'DropDown', 'Separator', 'Input' |

## Common Patterns

1. **Quick Actions**: Add export and print buttons
2. **Search Toolbar**: Add search input for filtering
3. **Grouped Actions**: Use dropdown for related actions

