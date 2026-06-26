# Command Column in React Grid

## Table of Contents
- [Overview](#overview)
- [Enable Command Column](#enable-command-column)
- [Built-in Commands](#built-in-commands)
- [Custom Commands](#custom-commands)
- [Command Events](#command-events)
- [Conditional Commands](#conditional-commands)
- [Styling Commands](#styling-commands)
- [Complete Example](#complete-example)
- [Best Practives](#best-practices)

## Overview

Command column provides buttons for common grid actions like Edit, Delete, and custom operations. It simplifies row-level interactions without needing custom templates.

---

## Enable Command Column

### Basic Setup

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Edit, Toolbar } from '@syncfusion/ej2-react-grids';

<GridComponent
  dataSource={data}
  editSettings={{ mode: 'Dialog', allowEditing: true, allowDeleting: true }}
>
  <ColumnsDirective>
    <ColumnDirective type='checkbox' width='50' />
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' isPrimaryKey={true} />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective
      headerText='Actions'
      width='150'
      commands={[
        { type: 'Edit', buttonOption: { cssClass: 'e-flat' } },
        { type: 'Delete', buttonOption: { cssClass: 'e-flat' } },
        { type: 'Save', buttonOption: { cssClass: 'e-flat' } },
        { type: 'Cancel', buttonOption: { cssClass: 'e-flat' } }
      ]}
    />
  </ColumnsDirective>
  <Inject services={[Edit, Toolbar]} />
</GridComponent>
```

---

## Built-in Commands

### Available Built-in Commands

| Command | Available In | Action |
|---------|--------------|--------|
| `Edit` | Normal mode | Start editing row |
| `Delete` | Normal mode | Delete row |
| `Save` | Edit mode | Save changes |
| `Cancel` | Edit mode | Cancel editing |

### Edit/Delete Commands

```tsx
<ColumnDirective
  headerText='Edit/Delete'
  width='120'
  commands={[
    { type: 'Edit', buttonOption: { cssClass: 'e-flat' } },
    { type: 'Delete', buttonOption: { cssClass: 'e-flat' } }
  ]}
/>
```

### Save/Cancel Commands

```tsx
<ColumnDirective
  headerText='Save/Cancel'
  width='120'
  commands={[
    { type: 'Save', buttonOption: { cssClass: 'e-flat' } },
    { type: 'Cancel', buttonOption: { cssClass: 'e-flat' } }
  ]}
/>
```

### All Commands

```tsx
<ColumnDirective
  headerText='Actions'
  width='200'
  commands={[
    { type: 'Edit', buttonOption: { cssClass: 'e-flat', iconCss: 'e-icons e-edit' } },
    { type: 'Save', buttonOption: { cssClass: 'e-flat', iconCss: 'e-icons e-save' } },
    { type: 'Cancel', buttonOption: { cssClass: 'e-flat', iconCss: 'e-icons e-cancel' } },
    { type: 'Delete', buttonOption: { cssClass: 'e-flat e-flat-danger', iconCss: 'e-icons e-delete' } }
  ]}
/>
```

---

## Custom Commands

### Duplicate Row Command

```tsx
<ColumnDirective
  headerText='Actions'
  width='150'
  commands={[
    { type: 'Edit', buttonOption: { cssClass: 'e-flat' } },
    {
      buttonOption: {
        content: 'Copy',
        cssClass: 'e-flat',
        click: onDuplicate
      }
    },
    { type: 'Delete', buttonOption: { cssClass: 'e-flat' } }
  ]}
/>

const onDuplicate = (args) => {
  const gridInstance = gridRef.current;
  const rowData = args.rowData;
  const newData = { ...rowData };
  delete newData[gridInstance.getPrimaryKeyFieldNames()[0]];
  
  gridInstance.addRecord(newData);
};
```

### View Details Command

```tsx
const onViewDetails = (args) => {
  const rowData = args.rowData;
  showDetailModal(rowData);
};

<ColumnDirective
  headerText='Actions'
  width='150'
  commands={[
    {
      buttonOption: {
        content: 'Details',
        cssClass: 'e-flat e-info',
        click: onViewDetails
      }
    },
    { type: 'Edit', buttonOption: { cssClass: 'e-flat' } },
    { type: 'Delete', buttonOption: { cssClass: 'e-flat' } }
  ]}
/>
```

### Download/Export Command

```tsx
const onDownload = (args) => {
  const rowData = args.rowData;
  const csv = convertToCSV(rowData);
  downloadCSV(csv, `order-${rowData.OrderID}.csv`);
};

<ColumnDirective
  headerText='Actions'
  width='150'
  commands={[
    {
      buttonOption: {
        content: 'Download',
        cssClass: 'e-flat e-success',
        iconCss: 'e-icons e-download',
        click: onDownload
      }
    },
    { type: 'Edit', buttonOption: { cssClass: 'e-flat' } }
  ]}
/>
```

### Multi-Action Button

```tsx
const commandOptions = [
  {
    buttonOption: {
      content: 'More Actions',
      cssClass: 'e-flat e-outline',
      click: (args) => showActionMenu(args)
    }
  }
];

const showActionMenu = (args) => {
  const menu = new ContextMenu({
    target: args.target,
    items: [
      { text: 'Print', id: 'print', click: () => printRow(args.rowData) },
      { text: 'Email', id: 'email', click: () => emailRow(args.rowData) },
      { text: 'Archive', id: 'archive', click: () => archiveRow(args.rowData) },
      { text: 'Share', id: 'share', click: () => shareRow(args.rowData) }
    ]
  });
  menu.open(args.target);
};

<ColumnDirective
  headerText='Actions'
  width='150'
  commands={commandOptions}
/>
```

---

## Command Events

### Click Event

```tsx
const handleCommandClick = (args) => {
  console.log('Command type:', args.commandType);
  console.log('Row data:', args.rowData);
  console.log('Button element:', args.target);
};

<GridComponent
  dataSource={data}
  commandClick={handleCommandClick}
>
  {/* columns */}
</GridComponent>
```

### Command Type Checking

```tsx
const handleCommand = (args) => {
  if (args.commandType === 'Edit') {
    console.log('Edit command:', args.rowData);
  } else if (args.commandType === 'Delete') {
    console.log('Delete command:', args.rowData);
  } else if (args.commandType === 'Custom') {
    console.log('Custom command:', args.commandType);
  }
};

<GridComponent commandClick={handleCommand}>
  {/* columns */}
</GridComponent>
```

---

## Conditional Commands

### Show/Hide Based on Row Data

```tsx
<ColumnDirective
  headerText='Actions'
  width='150'
  template={(props) => (
    <div>
      <button
        className='e-btn e-small'
        onClick={() => editRow(props)}
        style={{ marginRight: '5px' }}
      >
        Edit
      </button>
      
      {props.Status !== 'Completed' && (
        <button
          className='e-btn e-small e-danger'
          onClick={() => deleteRow(props)}
        >
          Delete
        </button>
      )}
      
      {props.Status === 'Pending' && (
        <button
          className='e-btn e-small e-success'
          onClick={() => completeRow(props)}
        >
          Complete
        </button>
      )}
    </div>
  )}
/>
```

### Role-Based Commands

```tsx
const userRole = getCurrentUserRole();

<ColumnDirective
  headerText='Actions'
  width='150'
  commands={
    userRole === 'admin'
      ? [
          { type: 'Edit', buttonOption: { cssClass: 'e-flat' } },
          { type: 'Delete', buttonOption: { cssClass: 'e-flat' } },
          { buttonOption: { content: 'Audit', cssClass: 'e-flat', click: viewAudit } }
        ]
      : [
          { type: 'Edit', buttonOption: { cssClass: 'e-flat' } },
          { buttonOption: { content: 'View', cssClass: 'e-flat', click: viewDetails } }
        ]
  }
/>
```

### Status-Based Commands

```tsx
function getCommandsForStatus(status) {
  const baseCommands = [{ type: 'Edit', buttonOption: { cssClass: 'e-flat' } }];

  if (status === 'Draft') {
    baseCommands.push({ type: 'Delete', buttonOption: { cssClass: 'e-flat' } });
  }

  if (status === 'Pending') {
    baseCommands.push({
      buttonOption: { content: 'Approve', cssClass: 'e-flat e-success', click: approveRow }
    });
  }

  if (status === 'Approved') {
    baseCommands.push({
      buttonOption: { content: 'Publish', cssClass: 'e-flat e-info', click: publishRow }
    });
  }

  return baseCommands;
}

<ColumnDirective
  headerText='Actions'
  width='200'
  template={(props) => {
    const commands = getCommandsForStatus(props.Status);
    return (
      <div>
        {commands.map((cmd, i) => (
          <button key={i} className='e-btn e-small'>
            {cmd.type || cmd.buttonOption.content}
          </button>
        ))}
      </div>
    );
  }}
/>
```

---

## Styling Commands

### Button Styling

```tsx
<ColumnDirective
  headerText='Actions'
  width='200'
  commands={[
    {
      type: 'Edit',
      buttonOption: {
        cssClass: 'e-flat e-outline',
        iconCss: 'e-icons e-edit'
      }
    },
    {
      type: 'Delete',
      buttonOption: {
        cssClass: 'e-flat e-danger',
        iconCss: 'e-icons e-delete'
      }
    },
    {
      buttonOption: {
        content: 'Archive',
        cssClass: 'e-flat e-warning',
        iconCss: 'e-icons e-archive'
      }
    }
  ]}
/>
```

### CSS Classes

```css
/* Button sizes */
.e-btn.e-small { padding: 4px 8px; font-size: 12px; }
.e-btn.e-large { padding: 12px 16px; font-size: 16px; }

/* Button styles */
.e-btn.e-flat { background-color: transparent; border: 1px solid #ddd; }
.e-btn.e-outline { border: 2px solid currentColor; }
.e-btn.e-primary { background-color: #007bff; color: white; }
.e-btn.e-success { background-color: #28a745; color: white; }
.e-btn.e-danger { background-color: #dc3545; color: white; }
.e-btn.e-warning { background-color: #ffc107; color: black; }
.e-btn.e-info { background-color: #17a2b8; color: white; }

/* Hover effects */
.e-btn:hover { opacity: 0.8; cursor: pointer; }
.e-btn:disabled { opacity: 0.5; cursor: not-allowed; }
```

### Inline Styling

```tsx
const commandButtonStyle = {
  padding: '6px 10px',
  fontSize: '12px',
  marginRight: '4px',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer'
};

const editButtonStyle = { ...commandButtonStyle, backgroundColor: '#007bff', color: 'white' };
const deleteButtonStyle = { ...commandButtonStyle, backgroundColor: '#dc3545', color: 'white' };

<ColumnDirective
  headerText='Actions'
  width='150'
  template={(props) => (
    <div>
      <button style={editButtonStyle} onClick={() => editRow(props)}>Edit</button>
      <button style={deleteButtonStyle} onClick={() => deleteRow(props)}>Delete</button>
    </div>
  )}
/>
```

---

## Complete Example

```tsx
import React, { useRef } from 'react';
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Edit, Toolbar } from '@syncfusion/ej2-react-grids';

function GridWithCommands() {
  const gridRef = useRef(null);

  const handleCommandClick = (args) => {
    switch (args.commandType) {
      case 'Edit':
        console.log('Editing:', args.rowData);
        break;
      case 'Delete':
        if (window.confirm('Are you sure you want to delete this record?')) {
          gridRef.current.deleteRecord();
        }
        break;
      default:
        console.log('Custom command:', args.commandType);
    }
  };

  const onDuplicate = (args) => {
    const newData = { ...args.rowData };
    delete newData.OrderID;
    gridRef.current.addRecord(newData);
  };

  const onViewDetails = (args) => {
    alert(`Order ID: ${args.rowData.OrderID}\nCustomer: ${args.rowData.CustomerID}`);
  };

  return (
    <GridComponent
      ref={gridRef}
      dataSource={data}
      editSettings={{ mode: 'Dialog', allowEditing: true, allowDeleting: true }}
      commandClick={handleCommandClick}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' isPrimaryKey={true} />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
        <ColumnDirective
          headerText='Actions'
          width='250'
          commands={[
            { 
              type: 'Edit', 
              buttonOption: { cssClass: 'e-flat', iconCss: 'e-icons e-edit' } 
            },
            { 
              buttonOption: { 
                content: 'Duplicate', 
                cssClass: 'e-flat e-info',
                click: onDuplicate 
              } 
            },
            { 
              buttonOption: { 
                content: 'Details', 
                cssClass: 'e-flat e-primary',
                click: onViewDetails 
              } 
            },
            { 
              type: 'Delete', 
              buttonOption: { cssClass: 'e-flat e-danger', iconCss: 'e-icons e-delete' } 
            }
          ]}
        />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar]} />
    </GridComponent>
  );
}

export default GridWithCommands;
```

---

## Best Practices

1. **Keep command column width fixed** (~150-250px)
2. **Order commands logically** (Edit → Save/Cancel, Delete at end)
3. **Use icons with text** for clarity
4. **Confirm destructive actions** (delete)
5. **Disable commands** when not applicable
6. **Show loading state** for async operations
7. **Provide keyboard shortcuts** (accessibility)
8. **Test with touch devices** (small button sizing)
9. **Group related commands** visually
10. **Provide tooltips** for clarity
