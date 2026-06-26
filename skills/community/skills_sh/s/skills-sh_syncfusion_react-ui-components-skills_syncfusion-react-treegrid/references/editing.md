---
name: editing
description: 'Editing in React TreeGrid - five editing modes (cell, row, dialog, batch, template), validation, command columns, and edit events.'
---

# Editing

## Table of Contents
- [CRUD & Editing Rules](#crud--editing-rules)
- [Overview](#overview)
- [Cell Editing](#cell-editing)
- [Row Editing](#row-editing)
- [Dialog Editing](#dialog-editing)
- [Batch Editing](#batch-editing)
- [Template Editing](#template-editing)
- [Validation](#validation)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## CRUD & Editing Rules

### Rule 1: EditSettings is MANDATORY for Editing
**Severity**: 🔴 CRITICAL - Editing won't work without configuration

**Requirement**:
```jsx
// ✅ REQUIRED - Must define editSettings
const editSettings = {
  mode: 'Cell',          // Required: 'Cell', 'Dialog', 'Row', 'Batch'
  allowEditing: true,    // Required: Enable editing
  allowAdding: true,     // Optional: Enable adding rows
  allowDeleting: true    // Optional: Enable deleting rows
};

<TreeGridComponent 
  dataSource={data}
  editSettings={editSettings}
  childMapping='subtasks'>
  <ColumnsDirective>
    {/* Columns */}
  </ColumnsDirective>
  <Inject services={[Edit]} />  {/* MUST also inject Edit module */}
</TreeGridComponent>

// ❌ WRONG - No editSettings = No editing possible
<TreeGridComponent 
  dataSource={data}>
  {/* No editing functionality without editSettings */}
</TreeGridComponent>
```

**Additional Requirements**:
```jsx
// ✅ MUST inject Edit module for any editing mode
import { Edit } from '@syncfusion/ej2-react-treegrid';

<TreeGridComponent>
  <Inject services={[Edit]} />  {/* REQUIRED */}
</TreeGridComponent>
```

**Edit Mode Rules**:
```jsx
// Cell Mode - Edit individual cells
editSettings={{ mode: 'Cell', allowEditing: true }}

// Dialog Mode - Edit in popup dialog
editSettings={{ mode: 'Dialog', allowEditing: true }}

// Row Mode - Edit full row inline
editSettings={{ mode: 'Row', allowEditing: true }}

// Batch Mode - Edit multiple rows, save all at once
editSettings={{ mode: 'Batch', allowEditing: true }}
```

---

### Rule 2: Inject Module is MANDATORY for Editing
**Severity**: 🔴 CRITICAL - Editing features won't initialize without Inject module

**Requirement**:
```jsx
// ✅ REQUIRED - Edit module must be injected
import { Edit } from '@syncfusion/ej2-react-treegrid';

<TreeGridComponent
  editSettings={editSettings}>
  {/* ... */}
  <Inject services={[Edit]} />  {/* MANDATORY for editing */}
</TreeGridComponent>

// ❌ WRONG - Missing Edit module injection
<TreeGridComponent
  editSettings={editSettings}>
  {/* ... */}
  {/* No <Inject> = Editing fails */}
</TreeGridComponent>
```

---

### Rule 3: Column EditType Must Match Data Type
**Severity**: 🟠 IMPORTANT - Validation fails with mismatched editTypes

**Requirement**:
```jsx
// ✅ CORRECT - EditType matches data type
<ColumnsDirective>
  <ColumnDirective field='TaskName' 
    headerText='Task' 
    editType='defaultedit'></ColumnDirective>
    
  <ColumnDirective field='Duration' 
    headerText='Duration' 
    editType='numericedit'
    validationRules={{ required: true, min: 1, max: 1000 }}></ColumnDirective>
    
  <ColumnDirective field='Priority' 
    headerText='Priority' 
    editType='dropdownedit'></ColumnDirective>
    
  <ColumnDirective field='StartDate' 
    headerText='Start Date' 
    editType='datepickeredit'
    format='yMd'></ColumnDirective>
    
  <ColumnDirective field='IsCompleted' 
    headerText='Completed' 
    editType='booleanedit'></ColumnDirective>
</ColumnsDirective>

// ❌ WRONG - EditType mismatch
<ColumnDirective field='Duration' 
  headerText='Duration' 
  type='number'
  editType='defaultedit'  {/* Should be numericedit */}
></ColumnDirective>
```

**Valid EditTypes**:
| EditType | Best For | Validation |
|----------|----------|------------|
| defaultedit | String fields | max length |
| numericedit | Numbers | min, max, decimals |
|dropdownedit | Fixed options | required |
| datepickeredit | Dates | date range |
| booleanedit | Booleans | true/false |
| datetimepickeredit| Date and Time| date and time range|

---

### Rule 4: Primary Key (isPrimaryKey) is MANDATORY for CRUD Operations
**Severity**: 🔴 CRITICAL - Editing/Deleting fails silently without this

**Requirement**:
```jsx
// ✅ REQUIRED - Exactly ONE column must have isPrimaryKey={true}
<ColumnsDirective>
  <ColumnDirective field='TaskID' headerText='ID' isPrimaryKey={true}></ColumnDirective>
  <ColumnDirective field='TaskName' headerText='Task'></ColumnDirective>
</ColumnsDirective>

// ❌ WRONG - No primary key = CRUD operations fail silently
<ColumnsDirective>
  <ColumnDirective field='TaskID' headerText='ID'></ColumnDirective>
  <ColumnDirective field='TaskName' headerText='Task'></ColumnDirective>
</ColumnsDirective>
```

**Rules**:
- ✅ Only ONE primary key allowed per grid
- ✅ Primary key value must be UNIQUE for each row
- ✅ Primary key must not be NULL/undefined
- ✅ Must match a field in data source
- ❌ Do NOT mark multiple columns as primary key
- ❌ Do NOT use composite/multi-column primary keys

**Impact Without This**:
```typescript
// What fails without isPrimaryKey:
- Edit operations (beginEdit fails silently)
- Delete operations (no row deleted)
- Update operations (data not persisted)
- Row selection preservation
- State persistence
```

---

## Overview

TreeGrid supports multiple editing modes for updating hierarchical data with proper CRUD operations.

## Cell Editing

Edit data inline at the cell level:

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
      editSettings={{ mode: 'Cell', allowEditing: true, allowDeleting: true, allowAdding: true }}
      toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} type="number" allowEditing={false} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} editType="dropdownedit" />
        <ColumnDirective type="checkbox" width={50} />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar]} />
    </TreeGridComponent>
  );
}
```

## Row Editing

Edit entire rows in a dialog or inline form:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  editSettings={{ mode: 'Row', allowEditing: true, allowDeleting: true }}
  toolbar={['Edit', 'Delete', 'Update', 'Cancel']}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} type="number" />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
  <Inject services={[Edit, Toolbar]} />
</TreeGridComponent>
```

## Dialog Editing

Edit data in a modal dialog:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  editSettings={{
    mode: 'Dialog',
    allowEditing: true,
    allowAdding: true,
    allowDeleting: true,
    newRowPosition: 'Child'
  }}
  toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
  <Inject services={[Edit, Toolbar]} />
</TreeGridComponent>
```

## Batch Editing

Edit multiple rows and save in batch:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  editSettings={{
    mode: 'Batch',
    allowEditing: true,
    allowAdding: true,
    allowDeleting: true
  }}
  toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
    <ColumnDirective type="checkbox" width={50} />
  </ColumnsDirective>
  <Inject services={[Edit, Toolbar]} />
</TreeGridComponent>
```

## Template Editing

Use custom templates for edit forms:

```tsx

const editTemplate = (props) => {
  return (
    <div>
      <label>Task Name:</label>
      <input value={props.TaskName} defaultValue={props.TaskName} />
    </div>
  );
};

<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  editSettings={{ mode: 'Cell', allowEditing: true }}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" editTemplate={editTemplate} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Validation

Add validation rules to edited data:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  editSettings={{ mode: 'Dialog', allowEditing: true }}
>
  <ColumnsDirective>
    <ColumnDirective 
      field="TaskName" 
      headerText="Task Name" 
      validationRules={{ required: true, min: 3 }}
    />
    <ColumnDirective 
      field="Priority" 
      headerText="Priority" 
      validationRules={{ required: true }}
    />
  </ColumnsDirective>
  <Inject services={[Edit, Toolbar]} />
</TreeGridComponent>
```

## Key APIs

| Property/Event | Type | Description |
|---|---|---|
| `editSettings` | object | Configure edit mode and behavior |
| `mode` | string | 'Cell', 'Row', 'Dialog', 'Batch' |
| `allowEditing` | boolean | Enable row/cell editing |
| `allowAdding` | boolean | Allow adding new rows |
| `allowDeleting` | boolean | Allow deleting rows |
| `newRowPosition` | string | 'Top', 'Bottom', 'Child' for new rows |
| `validationRules` | object | Validation rules per column |
| `actionComplete` | event | Fired after edit action completes |
| `actionFailure` | event | Fired when edit action fails |

## Common Patterns

1. **Server Persistence**: Handle `actionComplete` to save to server
2. **Parent-Child Add**: Use `newRowPosition: 'Child'` for adding child records
3. **Custom Validators**: Implement custom validation logic in `validationRules`
4. **Batch Operations**: Collect edits in batch mode before saving

