---
name: column-menu
description: 'Column Menu in React TreeGrid - enable column menu, sort/filter options, custom menu items, menu events, and hide/show columns.'
---

# Column Menu

## Table of Contents
- [Enable Column Menu](#enable-column-menu)
- [Menu Items](#menu-items)
- [Disable Column Menu for Specific Columns](#disable-column-menu-for-specific-columns)
- [Custom Menu Items](#custom-menu-items)
- [Menu Events](#menu-events)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Enable Column Menu

Enable column header dropdown menu:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, ColumnMenu, Sort, Filter } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      showColumnMenu={true}
      allowSorting={true}
      allowFiltering={true}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} showColumnMenu={true} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} showColumnMenu={true} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} showColumnMenu={true} />
      </ColumnsDirective>
      <Inject services={[ColumnMenu, Sort, Filter]} />
    </TreeGridComponent>
  );
}
```

## Menu Items

Default menu items available:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  showColumnMenu={true}
>
  {/* Default menu includes:
    - Sort Ascending
    - Sort Descending
    - Clear Sorting
    - Filter
    - Column Chooser
    - Auto Fit
  */}
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[ColumnMenu]} />
</TreeGridComponent>
```

## Disable Column Menu for Specific Columns

```tsx
<ColumnsDirective>
  <ColumnDirective 
    field="TaskID" 
    headerText="Task ID" 
    width={80} 
    showColumnMenu={false}  // No menu for this column
  />
  <ColumnDirective 
    field="TaskName" 
    headerText="Task Name" 
    width={160} 
    showColumnMenu={true}   // Menu enabled
  />
</ColumnsDirective>
```

## Custom Menu Items

Add custom items to column menu:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  showColumnMenu={true}
  columnMenuItems={[
    'SortAscending',
    'SortDescending',
    'SortByCellValue',
    'Filter',
    'Separator',
    'ColumnChooser',
    'Separator',
    { text: 'Copy to Clipboard', id: 'copyToClipboard' },
    { text: 'Export Column', id: 'exportColumn' }
  ]}
  columnMenuItemClick={(args) => {
    if (args.item.id === 'copyToClipboard') {
      console.log('Copying column:', args.column.field);
      // Implement copy logic
    }
    if (args.item.id === 'exportColumn') {
      console.log('Exporting column:', args.column.field);
      // Implement export logic
    }
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[ColumnMenu]} />
</TreeGridComponent>
```

## Menu Events

Handle column menu interactions:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  showColumnMenu={true}
  columnMenuOpen={(args) => {
    console.log('Menu opened for column:', args.column.field);
  }}
  columnMenuItemClick={(args) => {
    console.log('Menu item clicked:', args.item.text);
  }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[ColumnMenu]} />
</TreeGridComponent>
```

## Key APIs

| Property/Event | Type | Description |
|---|---|---|
| `showColumnMenu` | boolean | Enable column menu |
| `showColumnMenu` (column) | boolean | Enable menu for specific column |
| `columnMenuItems` | array | Custom menu configuration |
| `columnMenuOpen` | event | Fired when menu opens |
| `columnMenuItemClick` | event | Fired when menu item is clicked |

## Common Patterns

1. **Quick Sort**: Add sort options directly
2. **Column Control**: Hide/show columns from menu
3. **Export Column**: Export specific columns
4. **Quick Actions**: Custom operations per column

