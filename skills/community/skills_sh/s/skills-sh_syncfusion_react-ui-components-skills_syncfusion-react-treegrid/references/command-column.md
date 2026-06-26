---
name: command-column
description: 'Command Column in React TreeGrid - built-in command buttons (Edit, Delete, Save, Cancel), custom commands, and command events.'
---

# Command Column

## Table of Contents
- [Built-in Commands](#built-in-commands)
- [Custom Commands Columns](#custom-commands-columns)
- [Handle Command Actions Events](#handle-command-actions-events)
- [Icon Customization](#icon-customization)
- [Command Column with Template](#command-column-with-template)
- [Built-in Command Types](#built-in-command-types)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Built-in Commands

Command column provides action buttons:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Edit, Toolbar, CommandColumn } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      editSettings={{ allowEditing: true, allowDeleting: true, allowAdding: true }}
      toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} type="number" />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
        <ColumnDirective 
          type="checkbox" 
          width={50} 
        />
        <ColumnDirective
          type="CommandColumn"
          headerText="Commands"
          width={120}
          commands={[
            { type: 'Edit', buttonOption: { cssClass: 'e-flat', iconCss: 'e-icons e-edit' } },
            { type: 'Delete', buttonOption: { cssClass: 'e-flat', iconCss: 'e-icons e-delete' } },
            { type: 'Save', buttonOption: { cssClass: 'e-flat', iconCss: 'e-icons e-save' } },
            { type: 'Cancel', buttonOption: { cssClass: 'e-flat', iconCss: 'e-icons e-cancel' } }
          ]}
        />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar, CommandColumn]} />
    </TreeGridComponent>
  );
}
```

## Custom Commands Columns

Add custom action buttons:

```tsx
<ColumnDirective
  type="CommandColumn"
  headerText="Actions"
  width={150}
  commands={[
    { type: 'Edit', buttonOption: { cssClass: 'e-flat' } },
    { 
      text: 'Copy', 
      buttonOption: { cssClass: 'e-flat' },
      id: 'copy'
    },
    { 
      text: 'Details', 
      buttonOption: { cssClass: 'e-flat' },
      id: 'details'
    }
  ]}
/>
```

## Handle Command Actions Events

Get command click events:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  commandClick={(args) => {
    console.log('Command:', args.commandColumn.type);
    console.log('Row Data:', args.rowData);
    
    if (args.commandColumn.type === 'Edit') {
      // Handle edit
    } else if (args.commandColumn.id === 'copy') {
      // Handle custom copy command
      const rowData = args.rowData;
      console.log('Copying row:', rowData);
    } else if (args.commandColumn.id === 'details') {
      // Show details dialog
      console.log('Showing details for:', args.rowData.TaskID);
    }
  }}
>
  <ColumnsDirective>
    <ColumnDirective 
      type="CommandColumn"
      headerText="Actions"
      width={150}
      commands={[
        { type: 'Edit' },
        { text: 'Copy', id: 'copy' },
        { text: 'Details', id: 'details' }
      ]}
    />
  </ColumnsDirective>
  <Inject services={[Edit, CommandColumn]} />
</TreeGridComponent>
```

## Icon Customization

Customize command button icons:

```tsx
<ColumnDirective
  type="CommandColumn"
  headerText="Commands"
  width={150}
  commands={[
    { 
      type: 'Edit', 
      buttonOption: { 
        cssClass: 'e-outline',
        iconCss: 'e-icons e-edit',
        tooltip: 'Edit this row'
      } 
    },
    { 
      type: 'Delete', 
      buttonOption: { 
        cssClass: 'e-danger e-outline',
        iconCss: 'e-icons e-delete',
        tooltip: 'Delete this row'
      } 
    },
    { 
      text: 'Export', 
      buttonOption: { 
        cssClass: 'e-info e-outline',
        iconCss: 'e-icons e-export-excel',
        tooltip: 'Export row'
      }
    }
  ]}
/>
```

## Command Column with Template

Custom action templates:

```tsx
const commandTemplate = (props) => {
  return (
    <div>
      <button 
        onClick={() => handleEdit(props)}
        style={{ marginRight: '5px' }}
      >
        Edit
      </button>
      <button 
        onClick={() => handleDelete(props)}
        style={{ marginRight: '5px' }}
      >
        Delete
      </button>
      <button onClick={() => handleView(props)}>
        View
      </button>
    </div>
  );
};

const handleEdit = (rowData) => console.log('Edit:', rowData);
const handleDelete = (rowData) => console.log('Delete:', rowData);
const handleView = (rowData) => console.log('View:', rowData);

<ColumnDirective
  headerText="Commands"
  width={200}
  template={commandTemplate}
/>
```

## Built-in Command Types

Available command types:

```tsx
// Standard commands:
{ type: 'Edit' }       // Edit the row
{ type: 'Delete' }     // Delete the row
{ type: 'Save' }       // Save edited row
{ type: 'Cancel' }     // Cancel editing
{ type: 'Add' }        // Add new row

// Custom command:
{ text: 'Custom', id: 'custom' }
```

## Key APIs

| Property/Event | Type | Description |
|---|---|---|
| `type` | string | Column type: 'CommandColumn' |
| `commands` | array | Array of command objects |
| `commandClick` | event | Fired when command is clicked |
| `type` (command) | string | 'Edit', 'Delete', 'Save', 'Cancel', 'Add' |
| `buttonOption` | object | Button styling and icons |

## Common Patterns

1. **Row Actions**: Edit, Delete, View buttons
2. **Bulk Operations**: Select multiple rows with checkboxes
3. **Custom Workflows**: Status change, Approve, Reject buttons
4. **Context Actions**: Actions based on row status

