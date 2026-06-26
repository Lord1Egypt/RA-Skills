---
name: context-menu
description: 'Context Menu in React TreeGrid - built-in context menu items, custom items, header menus, and context menu events.'
---

# Context Menu

## Table of Contents
- [Built-in Context Menu](#built-in-context-menu)
- [Custom Context Menu Items](#custom-context-menu-items)
- [Header Context Menu](#header-context-menu)
- [Context Menu Events](#context-menu-events)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Built-in Context Menu

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, ContextMenu, Edit } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      contextMenuItems={['Copy', 'Edit', 'Delete']}
      editSettings={{ allowEditing: true, allowDeleting: true }}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
      </ColumnsDirective>
      <Inject services={[ContextMenu, Edit]} />
    </TreeGridComponent>
  );
}
```

## Custom Context Menu Items

Add custom menu items:

```tsx
const contextMenuItems = [
  { text: 'Edit', target: '.e-grid', command: 'Edit' },
  { text: 'Delete', target: '.e-grid', command: 'Delete' },
  { type: 'Separator' },
  { text: 'Export', target: '.e-grid', id: 'export' },
  { text: 'Refresh', target: '.e-grid', id: 'refresh' }
];

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  contextMenuItems={contextMenuItems}
  contextMenuClick={(args) => {
    if (args.item.id === 'export') {
      console.log('Export clicked');
    }
    if (args.item.id === 'refresh') {
      console.log('Refresh clicked');
    }
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[ContextMenu, Edit]} />
</TreeGridComponent>
```

## Header Context Menu

Context menu for column headers:

```tsx
const headerContextMenuItems = [
  { text: 'Sort Ascending', target: '.e-headercell', command: 'SortAscending' },
  { text: 'Sort Descending', target: '.e-headercell', command: 'SortDescending' },
  { type: 'Separator' },
  { text: 'Filter', target: '.e-headercell', command: 'Filter' }
];

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  contextMenuItems={headerContextMenuItems}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[ContextMenu]} />
</TreeGridComponent>
```

## Context Menu Events

Handle menu item selection:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  contextMenuItems={['Copy', 'Edit', 'Delete']}
  contextMenuClick={(args) => {
    console.log('Menu item clicked:', args.item);
    console.log('Row data:', args.rowInfo);
  }}
  contextMenuOpen={(args) => {
    console.log('Context menu opened at:', args.currentTarget);
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[ContextMenu, Edit]} />
</TreeGridComponent>
```

## Key APIs

| Property/Event | Type | Description |
|---|---|---|
| `contextMenuItems` | array | Menu items configuration |
| `contextMenuClick` | event | Fired when menu item is clicked |
| `contextMenuOpen` | event | Fired when menu opens |
| `text` | string | Menu item label |
| `command` | string | Built-in command (Edit, Delete, etc.) |
| `target` | string | Target selector for menu |

## Common Patterns

1. **CRUD Operations**: Edit, add, delete from context menu
2. **Export Actions**: Export selected rows
3. **Advanced Actions**: Custom business logic
4. **Conditional Menu**: Show items based on row data

