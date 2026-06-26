# Managing Tasks in Syncfusion React Gantt Chart

## Table of Contents
- [Enable Editing](#enable-editing)
- [Edit Modes](#edit-modes)
- [Adding New Tasks](#adding-new-tasks)
- [Editing Tasks](#editing-tasks)
- [Deleting Tasks](#deleting-tasks)
- [Taskbar Drag Editing](#taskbar-drag-editing)
- [Splitting and Merging Tasks](#splitting-and-merging-tasks)
- [Server-Side CRUD Operations](#server-side-crud-operations)
- [Customizing Edit Dialog Fields](#customizing-edit-dialog-fields)
- [Validation](#validation)

---

## Enable Editing

Inject `Edit` and configure `editSettings`:

```tsx
import { GanttComponent, Inject, Edit, Toolbar, Selection } from '@syncfusion/ej2-react-gantt';
import { EditSettingsModel } from '@syncfusion/ej2-gantt';

const editSettings: EditSettingsModel = {
  allowAdding:         true,   // enable adding new tasks
  allowEditing:        true,   // enable editing existing tasks
  allowDeleting:       true,   // enable deleting tasks
  allowTaskbarEditing: true,   // enable drag editing on taskbar
  showDeleteConfirmDialog: true,
};

function App() {
  return (
    <GanttComponent
      dataSource={data}
      taskFields={taskFields}
      editSettings={editSettings}
      toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
      height="450px"
    >
      <Inject services={[Edit, Toolbar, Selection]} />
    </GanttComponent>
  );
}
```

> A primary key column is required for CRUD operations. By default, `taskFields.id` is the primary key. If you define custom columns, mark one with `isPrimaryKey={true}`.

---

## Edit Modes

| Mode | Value | Behavior |
|---|---|---|
| Cell edit | `"Auto"` | Click any cell to edit it inline |
| Dialog edit | `"Dialog"` | Opens a full edit dialog on double-click or Edit toolbar button |

```tsx
// Cell editing (default)
const editSettings = { allowEditing: true, mode: 'Auto' };

// Dialog editing
const editSettings = { allowEditing: true, mode: 'Dialog' };
```

---

## Adding New Tasks

### Via Toolbar

```tsx
toolbar={['Add']}
editSettings={{ allowAdding: true }}
```

Clicking **Add** opens the add dialog / appends a new row.

### Programmatic

```tsx
const ganttRef = React.useRef<GanttComponent>(null);

// Add below the selected row
ganttRef.current?.addRecord({
  TaskID: 10,
  TaskName: 'New Task',
  StartDate: new Date('04/02/2024'),
  Duration: 3,
});

// Add as child of task with TaskID = 2
ganttRef.current?.addRecord(
  { TaskID: 11, TaskName: 'Child Task', Duration: 2 },
  'Child',
  2,   // parent TaskID
);
```

`addRecord(data, rowPosition, rowIndex)` — `rowPosition` can be: `'Above'`, `'Below'`, `'Child'`, `'Top'`, `'Bottom'`

### Set Default Values for New Task Dialog

```tsx
function actionBegin(args: any) {
  if (args.requestType === 'beforeOpenAddDialog') {
    args.dialog.querySelector('[name="Duration"]').value = '5';
  }
}

<GanttComponent actionBegin={actionBegin} .../>
```

---

## Editing Tasks

### Cell Editing

Click a cell in `mode: 'Auto'` to edit inline. Press Enter or click away to save.

### Dialog Editing

Double-click a row or click the Edit toolbar button in `mode: 'Dialog'` to open the edit dialog.

### Programmatic Update

```tsx
// Update by TaskID
ganttRef.current?.updateRecordById({
  TaskID: 3,
  TaskName: 'Updated Task Name',
  Duration: 7,
});
```

---

## Deleting Tasks

### Via Toolbar

```tsx
toolbar={['Delete']}
editSettings={{ allowDeleting: true, showDeleteConfirmDialog: true }}
```

### Programmatic

```tsx
ganttRef.current?.deleteRow();           // deletes currently selected row
```

---

## Taskbar Drag Editing

When `allowTaskbarEditing: true`, users can drag taskbars directly in the chart:

- **Move:** Drag the taskbar body left/right to change start/end date
- **Resize:** Drag the right edge to change duration
- **Progress:** Drag the progress handle to update completion percentage
- **Connect:** Drag from a taskbar endpoint to another taskbar to create a dependency

```tsx
const editSettings = {
  allowTaskbarEditing: true,
};

<GanttComponent editSettings={editSettings} ...>
  <Inject services={[Edit]} />
</GanttComponent>
```

---

## Splitting and Merging Tasks

Split a task into multiple intervals (segments):

```tsx
// Enable splitting via context menu or programmatic API
// Ensure taskFields.segments is mapped
const taskFields = {
  ...
  segments: 'Segments',
};

// Programmatic split:
ganttRef.current?.splitTask(taskId, splitDate);

// Merge all segments:
ganttRef.current?.mergeTask(taskId, [{'firstSegmentIndex': segmentIndex1, 'secondSegmentIndex': segmentIndex2 }]);
```

Split tasks appear as separate taskbar segments with gaps between them.

---

## Server-Side CRUD Operations

### Using RemoteSaveAdaptor (Client-Side Rendering + Server Persistence)

Use `DataManager` with `RemoteSaveAdaptor` when data is rendered locally but CRUD changes must persist to a server:

```tsx
import { DataManager, RemoteSaveAdaptor } from '@syncfusion/ej2-data';

const dataSource = new DataManager({
  json: localData,
  batchUrl: '/api/gantt/BatchUpdate',
  adaptor: new RemoteSaveAdaptor,
});

// Server receives a CRUDModel:
// { added: [...], changed: [...], deleted: [...] }
```

Listen for action events to track changes:

```tsx
function actionComplete(args: any) {
  if (args.requestType === 'save') {
    console.log('Task saved:', args.data);
  }
  if (args.requestType === 'delete') {
    console.log('Task deleted:', args.data);
  }
}

<GanttComponent actionComplete={actionComplete} .../>
```

---

### Maintaining Data in Server with UrlAdaptor

Use `UrlAdaptor` with a `batchUrl` endpoint to fully manage Gantt data on the server. The server endpoint returns `{ result, count }` on load and `{ addedRecords, changedRecords, deletedRecords }` on save.

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';
import { GanttComponent, Inject, Edit, Toolbar, Selection } from '@syncfusion/ej2-react-gantt';

const dataSource = new DataManager({
  url: '/Home/UrlDatasource',      // fetch data endpoint
  adaptor: new UrlAdaptor,
  batchUrl: '/Home/BatchSave',     // CRUD batch endpoint
});

const taskFields = {
  id: 'TaskId',
  name: 'TaskName',
  startDate: 'StartDate',
  duration: 'Duration',
  dependency: 'Predecessor',
  child: 'SubTasks',
};

function App() {
  return (
    <GanttComponent
      dataSource={dataSource}
      taskFields={taskFields}
      editSettings={{ allowAdding: true, allowEditing: true, allowDeleting: true, allowTaskbarEditing: true }}
      toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel', 'ExpandAll', 'CollapseAll']}
      height="450px"
    >
      <Inject services={[Edit, Toolbar, Selection]} />
    </GanttComponent>
  );
}
```

> **Key points:**
> - The Gantt component sends `added`, `changed`, and `deleted` arrays to the `batchUrl` endpoint automatically after each CRUD operation.
> - Batch operations handle interdependent records automatically (e.g., updating a child task shifts parent dates).
> - Ensure dependency strings avoid circular references.
> - Use self-referential data (flat) with `parentID` for server-side operations.

---

## Customizing Edit Dialog Fields

Control which fields appear in the add/edit dialog:

```tsx
const editDialogFields = [
  { type: 'General',     headerText: 'General' },
  { type: 'Dependency',  headerText: 'Dependencies' },
  { type: 'Resources',   headerText: 'Resources' },
  { type: 'Notes',       headerText: 'Notes' },
];

const addDialogFields = [
  { type: 'General',    headerText: 'General' },
  { type: 'Dependency', headerText: 'Dependencies' },
];

<GanttComponent
  editDialogFields={editDialogFields}
  addDialogFields={addDialogFields}
  ...
/>
```

---

## Cell Edit Types and Custom Editors

By default the Gantt picks an edit control based on column type. Override it per column using `editType` and `edit.params`:

### Built-in `editType` Values

| `editType` | Editor Control | Use Case |
|---|---|---|
| `'stringedit'` | Text input | Default for string columns |
| `'numericedit'` | NumericTextBox | Numbers with min/max/step |
| `'datepickeredit'` | DatePicker | Date-only columns |
| `'datetimepickeredit'` | DateTimePicker | Date + time columns |
| `'dropdownedit'` | DropDownList | Fixed-value columns |
| `'booleanedit'` | CheckBox | Boolean columns |
| `'maskededit'` | MaskedTextBox | Formatted text (phone, postal) |

### Numeric Cell Editor with Min/Max/Step

```tsx
<ColumnDirective
  field="Duration"
  headerText="Duration"
  editType="numericedit"
  edit={{ params: { min: 0, max: 365, step: 1 } }}
/>
```

### Date Cell Editor with Custom Format

```tsx
<ColumnDirective
  field="StartDate"
  headerText="Start Date"
  editType="datepickeredit"
  edit={{ params: { format: 'MM/dd/yyyy', strictMode: true } }}
  format="MM/dd/yyyy"
/>
```

### DateTime Cell Editor

```tsx
<ColumnDirective
  field="StartDate"
  editType="datetimepickeredit"
  edit={{ params: { format: 'M/d/y hh:mm a' } }}
  format={{ type: 'dateTime', format: 'M/d/y hh:mm a' }}
/>
```

### DropDown Cell Editor

```tsx
const statusParams = {
  params: {
    dataSource: ['Not Started', 'In Progress', 'Completed', 'On Hold'],
    fields: { text: 'text', value: 'value' },
    allowFiltering: true,
  }
};

<ColumnDirective
  field="Status"
  headerText="Status"
  editType="dropdownedit"
  edit={statusParams}
/>
```

### Dropdown with Object DataSource

```tsx
const priorityParams = {
  params: {
    dataSource: [
      { id: 1, name: 'Low' },
      { id: 2, name: 'Medium' },
      { id: 3, name: 'High' },
    ],
    fields: { text: 'name', value: 'id' },
  }
};

<ColumnDirective
  field="Priority"
  editType="dropdownedit"
  edit={priorityParams}
/>
```

### Complete Example — Mixed Edit Types

```tsx
import React, { useRef } from 'react';
import {
  GanttComponent, ColumnsDirective, ColumnDirective,
  Inject, Edit, Toolbar, Selection
} from '@syncfusion/ej2-react-gantt';

function App() {
  const taskFields = {
    id: 'TaskID', name: 'TaskName',
    startDate: 'StartDate', duration: 'Duration',
    progress: 'Progress', parentID: 'ParentID'
  };

  const editSettings = {
    allowAdding: true, allowEditing: true,
    allowDeleting: true, mode: 'Auto' as const
  };

  const statusParams = {
    params: {
      dataSource: ['Not Started', 'In Progress', 'Completed'],
      allowFiltering: true,
    }
  };

  return (
    <GanttComponent
      dataSource={data}
      taskFields={taskFields}
      editSettings={editSettings}
      toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
      height='450px'
    >
      <ColumnsDirective>
        <ColumnDirective field='TaskID'    width='80' />
        <ColumnDirective field='TaskName'  editType='stringedit'
          validationRules={{ required: true }} />
        <ColumnDirective field='StartDate' editType='datepickeredit'
          edit={{ params: { format: 'MM/dd/yyyy' } }} format='yMd' />
        <ColumnDirective field='Duration'  editType='numericedit'
          edit={{ params: { min: 0, max: 365 } }} />
        <ColumnDirective field='Progress'  editType='numericedit'
          edit={{ params: { min: 0, max: 100 } }} />
        <ColumnDirective field='Status'    editType='dropdownedit'
          edit={statusParams} />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar, Selection]} />
    </GanttComponent>
  );
}

export default App;
```

---

## Validation

### Prevent Invalid Edits (actionBegin)

Use `actionBegin` to cancel invalid operations:

```tsx
function actionBegin(args: any) {
  if (args.requestType === 'beforeSave') {
    const task = args.newTaskData;
    if (!task.TaskName || task.TaskName.trim() === '') {
      args.cancel = true;  // prevent save
      alert('Task name is required');
    }
  }
  if (args.requestType === 'taskbarediting') {
    // args.data contains the task being edited
    if (args.data.TaskID === 1) {
      args.cancel = true;  // lock task 1 from taskbar editing
    }
  }
}
```

### Column-Level Validation Rules

Apply validation rules declaratively per column using `validationRules`. The Gantt uses the EJ2 Form Validator engine to display inline error messages during cell/dialog editing:

```tsx
// Built-in rule examples
const taskNameRules = { required: true };
const startDateRules = { required: true, date: true };
const durationRules  = { required: true, min: 1 };

<GanttComponent
  dataSource={data}
  taskFields={taskFields}
  editSettings={{ allowAdding: true, allowEditing: true }}
  toolbar={['Add', 'Edit', 'Update', 'Delete', 'Cancel']}
  height="450px"
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID"    width="80" />
    <ColumnDirective field="TaskName"  validationRules={taskNameRules} />
    <ColumnDirective field="StartDate" validationRules={startDateRules}
      editType="datetimepickeredit"
      edit={{ params: { format: 'M/d/y hh:mm a' } }}
      format={{ type: 'dateTime', format: 'M/d/y hh:mm a' }}
    />
    <ColumnDirective field="Duration"  validationRules={durationRules} />
    <ColumnDirective field="Progress"  validationRules={{ required: true }} />
  </ColumnsDirective>
  <Inject services={[Edit, Toolbar, Selection]} />
</GanttComponent>
```

**Common `validationRules` options:**

| Rule | Example | Description |
|---|---|---|
| `required` | `{ required: true }` | Field cannot be empty |
| `min` | `{ min: 1 }` | Numeric minimum value |
| `max` | `{ max: 100 }` | Numeric maximum value |
| `minLength` | `{ minLength: 3 }` | Minimum string length |
| `maxLength` | `{ maxLength: 50 }` | Maximum string length |
| `date` | `{ date: true }` | Must be a valid date |
| `regex` | `{ regex: ['^[A-Za-z]', 'msg'] }` | Regex pattern match |

### Custom Validation Rules

Define a custom validator function for domain-specific rules:

```tsx
// Custom rule: task name must start with an uppercase letter
const taskNameRules = {
  required: true,
  startsWithUpper: [
    (args: { value: string }) => /^[A-Z]/.test(args.value),
    'Task name must start with an uppercase letter',
  ],
};

<ColumnDirective field="TaskName" validationRules={taskNameRules} />
```

### Delete Confirmation Dialog

```tsx
editSettings={{ allowDeleting: true, showDeleteConfirmDialog: true }}
```

Shows a confirmation popup before deleting. Set to `false` to delete immediately without confirmation.
