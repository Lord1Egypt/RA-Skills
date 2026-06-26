# Editing in React Grid

## Table of Contents
- [Rules](#rules)
- [Overview](#overview)
- [Setup Editing](#setup-editing)
- [Edit Modes](#edit-modes)
- [Edit Configuration](#edit-configuration)
- [Validation](#validation)
- [Advanced Editing](#advanced-editing)

## Rules

> ⚠️ Do not use `allowEditing` on `<GridComponent>`.

## Overview

Editing enables users to create, update, and delete records directly in the grid with multiple edit modes and validation support.

## Setup Editing

### Inject Edit Module

```tsx
import { GridComponent, Inject, Edit } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data}>
  <Inject services={[Edit]} />
</GridComponent>
```

### Enable Editing

```tsx
const editSettings = {
  allowEditing: true,
  allowAdding: true,
  allowDeleting: true,
  mode: 'Dialog'
};

<GridComponent
  dataSource={data}
  editSettings={editSettings}
  toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' isPrimaryKey={true} />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
  <Inject services={[Edit, Toolbar]} />
</GridComponent>
```

## Edit Modes

### Inline Editing

Edit single row inline:

```tsx
const editSettings = {
  mode: 'Inline',
  allowEditing: true,
  allowAdding: true,
  allowDeleting: true
};

<GridComponent editSettings={editSettings}>
  {/* columns */}
  <Inject services={[Edit]} />
</GridComponent>
```

### Batch Editing

Edit multiple rows at once:

```tsx
const editSettings = {
  mode: 'Batch',
  allowEditing: true,
  allowAdding: true,
  allowDeleting: true
};

<GridComponent editSettings={editSettings}>
  {/* columns */}
  <Inject services={[Edit]} />
</GridComponent>
```

### Dialog Editing

Edit in a modal dialog:

```tsx
const editSettings = {
  mode: 'Dialog',
  allowEditing: true,
  allowAdding: true,
  allowDeleting: true
};

<GridComponent editSettings={editSettings}>
  {/* columns */}
  <Inject services={[Edit]} />
</GridComponent>
```

## Edit Configuration

### Edit Triggers

- Double-click: Open edit dialog
- Toolbar buttons: Click Edit/Add/Delete buttons
- Keyboard: Press F2 to edit, Insert for add, Delete to remove
- Programmatic: Call methods

```tsx
const editSettings = {
  allowEditOnDblClick: true,  // Enable double-click editing
  allowEditing: true,
  mode: 'Dialog'
};

<GridComponent editSettings={editSettings}>
  {/* columns */}
</GridComponent>
```

### Primary Key Requirement

```tsx
<ColumnDirective
  field='OrderID'
  headerText='Order ID'
  width='100'
  isPrimaryKey={true}  // Mark as primary key for CRUD
/>
```

### Read-Only Columns

```tsx
<ColumnDirective
  field='OrderID'
  headerText='Order ID'
  width='100'
  isPrimaryKey={true}
  allowEditing={false}  // Can't edit primary key
/>
```

## Validation

### Column Validation Rules

Always match the validation rule to the column's data type. Using the wrong rule causes incorrect validation messages (e.g., applying `min`/`max` to a string column shows a number-based message like "ShipName must be at least 3" instead of "must have at least 3 characters").

```tsx
{/* ✅ Number column — use min/max */}
<ColumnDirective
  field='Freight'
  headerText='Freight'
  width='100'
  type='number'
  validationRules={{ required: true, min: 0, max: 10000 }}
/>

{/* ✅ String column — use minLength/maxLength, NOT min/max */}
<ColumnDirective
  field='CustomerID'
  headerText='Customer ID'
  width='120'
  type='string'
  validationRules={{ required: true, minLength: 5, maxLength: 5 }}
/>

{/* ✅ Date column — only required applies */}
<ColumnDirective
  field='OrderDate'
  headerText='Order Date'
  width='130'
  type='date'
  format='yMd'
  validationRules={{ required: true }}
/>

{/* ❌ Wrong — min/max applied to a string column produces wrong message */}
{/* <ColumnDirective field='ShipName' validationRules={{ min: 3 }} /> */}

{/* ❌ Wrong — minLength/maxLength applied to a number column produces wrong message */}
{/* <ColumnDirective field='Freight' validationRules={{ minLength: 1 }} /> */}
```

### Validation Rules Reference

| Rule | Applies to | Description | Example |
|------|-----------|-------------|---------|
| `required` | All types | Field must not be empty | `{ required: true }` |
| `minLength` | **String only** | Minimum character count | `{ minLength: 3 }` |
| `maxLength` | **String only** | Maximum character count | `{ maxLength: 50 }` |
| `min` | **Number only** | Minimum numeric value | `{ min: 0 }` |
| `max` | **Number only** | Maximum numeric value | `{ max: 10000 }` |

### Custom Validation

```tsx
const customFn = (args) => {
  return args['value'].length >=5;
};
const orderIDRules = { required: true };
const customerIDRules = {
  minLength: [customFn, 'Need atleast 5 letters'],
  required: true
};
<ColumnDirective
  field='CustomerID'
  customValidate={customerIDRules}
/>
```

## Advanced Editing

### Custom Edit Dialog Templates

```tsx
import React, { useRef } from 'react';

function GridWithCustomEditDialog() {
  const gridRef = useRef(null);

  const dialogTemplate = (props) => {
    return (
      <div style={{ padding: '20px' }}>
        <div>
          <label>Order ID:</label>
          <input
            type='text'
            value={props.OrderID}
            disabled
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>
        <div style={{ marginTop: '15px' }}>
          <label>Customer:</label>
          <input
            type='text'
            value={props.CustomerID}
            onChange={(e) => props.CustomerID = e.target.value}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>
        <div style={{ marginTop: '15px' }}>
          <label>Freight:</label>
          <input
            type='number'
            value={props.Freight}
            onChange={(e) => props.Freight = parseFloat(e.target.value)}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>
      </div>
    );
  };

  return (
    <GridComponent
      ref={gridRef}
      dataSource={data}
      editSettings={{
        mode: 'Dialog',
        template: dialogTemplate,
        allowEditing: true,
        allowAdding: true,
        allowDeleting: true
      }}
    >
      {/* columns */}
      <Inject services={[Edit, Toolbar]} />
    </GridComponent>
  );
}

export default GridWithCustomEditDialog;
```

### Batch Editing with Validation

```tsx
import React, { useRef } from 'react';

function GridWithBatchEditing() {
  const gridRef = useRef(null);

  const batchAdd = () => {
    const newRecords = [
      { OrderID: 10251, CustomerID: 'VICTE', Freight: 41.34 },
      { OrderID: 10252, CustomerID: 'SUPRD', Freight: 51.30 }
    ];
    gridRef.current.addRecord(newRecords);
  };

  const batchSave = () => {
    const changedRecords = gridRef.current.getBatchChanges();
    console.log('Changed Records:', changedRecords);
    // Send to server
  };

  return (
    <div>
      <button onClick={batchAdd}>Add Multiple</button>
      <button onClick={batchSave}>Save Changes</button>

      <GridComponent
        ref={gridRef}
        dataSource={data}
        editSettings={{
          mode: 'Batch',
          allowEditing: true,
          allowAdding: true,
          allowDeleting: true
        }}
        actionComplete={(args) => {
          if (args.requestType === 'save') {
            console.log('Batch save completed');
          }
        }}
      >
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' isPrimaryKey={true} />
          <ColumnDirective
            field='Freight'
            headerText='Freight'
            validationRules={{ required: true, min: 0 }}
          />
        </ColumnsDirective>
        <Inject services={[Edit, Toolbar]} />
      </GridComponent>
    </div>
  );
}

export default GridWithBatchEditing;
```

### Edit Events

Handle edit lifecycle events:

```tsx
function GridWithEditEvents() {
  const handleActionBegin = (args) => {
    if (args.requestType === 'save') {
      console.log('Before save:', args.data);
    } else if (args.requestType === 'beginEdit') {
      console.log('Edit started:', args.rowData);
    } else if (args.requestType === 'add') {
      console.log('Add started');
    }
  };

  const handleActionComplete = (args) => {
    if (args.requestType === 'save') {
      console.log('Save completed');
    } else if (args.requestType === 'cancel') {
      console.log('Edit cancelled');
    }
  };

  const handleActionFailure = (args) => {
    console.error('Action failed:', args.error);
  };

  return (
    <GridComponent
      dataSource={data}
      editSettings={{ mode: 'Dialog', allowEditing: true }}
      actionBegin={handleActionBegin}
      actionComplete={handleActionComplete}
      actionFailure={handleActionFailure}
    >
      {/* columns */}
      <Inject services={[Edit]} />
    </GridComponent>
  );
}
```

### Remote Editing with Server Persistence

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

function GridWithRemoteEditing() {
  const data = new DataManager({
    url: 'url',
    adaptor: new UrlAdaptor(),
    insertUrl: 'url',
    updateUrl: 'url',
    removeUrl: 'url',
    batchUrl: 'url/batch'
  });

  return (
    <GridComponent
      dataSource={data}
      editSettings={{
        allowEditing: true,
        allowAdding: true,
        allowDeleting: true,
        mode: 'Batch'
      }}
      actionFailure={(args) => {
        console.error('Server error:', args.error);
      }}
    >
      {/* columns */}
      <Inject services={[Edit, Toolbar, Page]} />
    </GridComponent>
  );
}
```

### Edit Row Selection

Customize which rows can be edited:

```tsx
function GridWithConditionalEditing() {
  const handleActionBegin = (args) => {
    if (args.requestType === 'beginEdit') {
      const data = args.rowData;
      
      // Prevent editing of completed orders
      if (data.Status === 'Completed') {
        args.cancel = true;
        alert('Cannot edit completed orders');
      }
    }
  };

  return (
    <GridComponent
      dataSource={data}
      editSettings={{ mode: 'Dialog', allowEditing: true }}
      actionBegin={handleActionBegin}
    >
      {/* columns */}
      <Inject services={[Edit]} />
    </GridComponent>
  );
}
```

### Editor Components

Use custom editor components for different data types:

```tsx
const dropdownTemplate = (props) => {
  return (
    <select
      value={props.Status}
      onChange={(e) => props.Status = e.target.value}
    >
      <option value='Pending'>Pending</option>
      <option value='Processing'>Processing</option>
      <option value='Completed'>Completed</option>
      <option value='Cancelled'>Cancelled</option>
    </select>
  );
};

const dateTemplate = (props) => {
  return (
    <input
      type='date'
      value={props.OrderDate?.toISOString().split('T')[0] || ''}
      onChange={(e) => props.OrderDate = new Date(e.target.value)}
    />
  );
};

<GridComponent editSettings={{ mode: 'Dialog', allowEditing: true }}>
  <ColumnsDirective>
    <ColumnDirective
      field='Status'
      headerText='Status'
      editTemplate={dropdownTemplate}
    />
    <ColumnDirective
      field='OrderDate'
      headerText='Order Date'
      editTemplate={dateTemplate}
    />
  </ColumnsDirective>
  <Inject services={[Edit]} />
</GridComponent>
```

### Grid State Persistence with Editing

> 🔒 **Security Warning:** `localStorage` and `sessionStorage` store data **unencrypted** in the browser. **Never store sensitive data** (passwords, tokens, PII, payment info, user secrets, authentication credentials) in persisted TreeGrid state. State persistence is safe for **UI state only** (expand/collapse state, page number, sort order, column visibility, filter selections). For sensitive configuration or user data, use secure server-side session storage instead.

Save and restore grid state including edited changes:

```tsx
function GridWithStatePersistence() {
  const gridRef = useRef(null);

  const saveGridState = () => {
    const state = {
      pageSettings: gridRef.current.pageSettings,
      sortSettings: gridRef.current.sortSettings,
      filterSettings: gridRef.current.filterSettings,
      groupSettings: gridRef.current.groupSettings
    };
    localStorage.setItem('gridState', JSON.stringify(state));
  };

  const restoreGridState = () => {
    const state = JSON.parse(localStorage.getItem('gridState'));
    if (state) {
      gridRef.current.pageSettings = state.pageSettings;
      gridRef.current.sortSettings = state.sortSettings;
      gridRef.current.filterSettings = state.filterSettings;
      gridRef.current.groupSettings = state.groupSettings;
    }
  };

  useEffect(() => {
    restoreGridState();
  }, []);

  return (
    <div>
      <button onClick={saveGridState}>Save State</button>
      <GridComponent
        ref={gridRef}
        dataSource={data}
        editSettings={{ allowEditing: true }}
      >
        {/* columns */}
      </GridComponent>
    </div>
  );
}
```

### Handle Edit Events

```tsx
const onActionBegin = (args) => {
  if (args.requestType === 'save') {
    console.log('Saving record:', args.data);
  }
  if (args.requestType === 'delete') {
    console.log('Deleting record:', args.data);
  }
};

const onActionComplete = (args) => {
  if (args.requestType === 'save') {
    console.log('Record saved successfully');
  }
};

<GridComponent
  dataSource={data}
  actionBegin={onActionBegin}
  actionComplete={onActionComplete}
  editSettings={{ mode: 'Dialog', allowEditing: true }}
>
  {/* columns */}
  <Inject services={[Edit]} />
</GridComponent>
```

### Server-Side Editing

```tsx
const editSettings = {
  mode: 'Dialog',
  allowEditing: true
};

const dataManager = new DataManager({
  url: 'url',
  updateUrl: 'url',
  insertUrl: 'url',
  removeUrl: 'url'
});

<GridComponent
  dataSource={dataManager}
  editSettings={editSettings}
>
  {/* columns */}
  <Inject services={[Edit]} />
</GridComponent>
```
