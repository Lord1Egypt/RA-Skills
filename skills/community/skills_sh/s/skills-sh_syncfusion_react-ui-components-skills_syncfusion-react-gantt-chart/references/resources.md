# Resources

## Table of Contents
- [Overview](#overview)
- [Resource Collection Setup](#resource-collection-setup)
- [Assigning Resources to Tasks](#assigning-resources-to-tasks)
- [Basic Resource Display](#basic-resource-display)
- [Resource View](#resource-view)
- [Multi-Taskbar (Resource View)](#multi-taskbar-resource-view)
- [Managing Resources via Editing](#managing-resources-via-editing)
- [Custom Resource Styling](#custom-resource-styling)
- [Over-Allocation Highlighting](#over-allocation-highlighting)
- [`resourceFields` Properties](#resourcefields-properties)
- [Common Pitfalls](#common-pitfalls)

---

## Overview

Resources represent people, equipment, or materials assigned to tasks. They are visualized in taskbars and labels for workload tracking.

**Key props:**
- `resources` — Array of resource objects
- `resourceFields` — Maps resource object keys to internal roles
- `taskFields.resourceInfo` — Maps task data field containing resource assignments

---

## Resource Collection Setup

```typescript
import { ResourceFieldsModel } from '@syncfusion/ej2-react-gantt';

const projectResources = [
  { resourceId: 1, resourceName: 'Martin Tamer', resourceGroup: 'Planning Team', resourceUnit: 50 },
  { resourceId: 2, resourceName: 'Rose Fuller', resourceGroup: 'Testing Team', resourceUnit: 70 },
  { resourceId: 3, resourceName: 'Margaret Buchanan', resourceGroup: 'Approval Team' },
  { resourceId: 4, resourceName: 'Fuller King', resourceGroup: 'Development Team' },
  { resourceId: 5, resourceName: 'Van Jack', resourceGroup: 'Development Team', resourceUnit: 40 }
];

const resourceFields: ResourceFieldsModel = {
  id: 'resourceId',       // unique identifier
  name: 'resourceName',   // display name
  unit: 'resourceUnit',   // work capacity % per day (0-100), default: 100
  group: 'resourceGroup'  // category for grouping
};
```

---

## Assigning Resources to Tasks

Resources are assigned via the `taskFields.resourceInfo` mapped field in the data source.

### Single Resource (default 100% unit)
```typescript
{ TaskID: 2, TaskName: 'Site Survey', StartDate: new Date('04/02/2019'), Duration: 3, resources: [1] }
```

### Multiple Resources with Custom Units
```typescript
{ TaskID: 3, TaskName: 'Development', StartDate: new Date('04/05/2019'), Duration: 5,
  resources: [{ resourceId: 1, unit: 70 }, { resourceId: 4, unit: 50 }] }
```

> Units from the resource collection apply unless overridden at the task level.

### taskFields Mapping
```tsx
const taskFields = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  duration: 'Duration',
  progress: 'Progress',
  resourceInfo: 'resources',  // maps to the resources array in data
  parentID: 'ParentID'
};
```

---

## Basic Resource Display

```tsx
import React from 'react';
import { GanttComponent, Inject, Selection } from '@syncfusion/ej2-react-gantt';
import { TaskFieldsModel, ResourceFieldsModel, LabelSettingsModel } from '@syncfusion/ej2-react-gantt';

function App() {
  const taskFields: TaskFieldsModel = {
    id: 'TaskID', name: 'TaskName',
    startDate: 'StartDate', endDate: 'EndDate',
    duration: 'Duration', progress: 'Progress',
    resourceInfo: 'resources', parentID: 'ParentID'
  };

  const resourceFields: ResourceFieldsModel = {
    id: 'resourceId', name: 'resourceName', unit: 'Unit'
  };

  const labelSettings: LabelSettingsModel = {
    leftLabel: 'TaskName',
    rightLabel: 'resources'   // shows resource names to the right of taskbars
  };

  const columns = [
    { field: 'TaskID', visible: false },
    { field: 'TaskName', headerText: 'Task Name', width: '180' },
    { field: 'resources', headerText: 'Resources', width: '160' },
    { field: 'Duration', width: '100' }
  ];

  return (
    <GanttComponent
      dataSource={data}
      taskFields={taskFields}
      resourceFields={resourceFields}
      resources={projectResources}
      labelSettings={labelSettings}
      columns={columns}
      height='450px'
    >
      <Inject services={[Selection]} />
    </GanttComponent>
  );
}
```

---

## Resource View

Resource view organizes the Gantt hierarchically by resource — each resource is a parent node with its assigned tasks as children.

### Enable Resource View
```tsx
<GanttComponent
  viewType='ResourceView'
  dataSource={data}
  taskFields={taskFields}
  resourceFields={resourceFields}
  resources={projectResources}
  height='450px'
>
  <Inject services={[Edit, Selection, Toolbar]} />
</GanttComponent>
```

**Behavior:**
- Resources appear as parent rows
- Assigned tasks appear as child rows under each resource
- Unassigned tasks group under an **Unassigned Task** node
- Parent tasks are not supported in resource view
- All tasks must have `startDate` and `duration`

### Resource View with Groups
```tsx
const resourceFields: ResourceFieldsModel = {
  id: 'resourceId',
  name: 'resourceName',
  unit: 'resourceUnit',
  group: 'resourceGroup'  // resources grouped by this field in the view
};
```

### Full Resource View Example
```tsx
import React from 'react';
import {
  GanttComponent, Inject, Edit, Selection, Toolbar,
  TaskFieldsModel, ResourceFieldsModel, EditSettingsModel,
  LabelSettingsModel, SplitterSettingsModel
} from '@syncfusion/ej2-react-gantt';

function App() {
  const taskFields: TaskFieldsModel = {
    id: 'TaskID', name: 'TaskName',
    startDate: 'StartDate', endDate: 'EndDate',
    duration: 'Duration', progress: 'Progress',
    dependency: 'Predecessor', resourceInfo: 'resources',
    work: 'work', parentID: 'ParentID'
  };

  const resourceFields: ResourceFieldsModel = {
    id: 'resourceId', name: 'resourceName',
    unit: 'Unit', group: 'resourceGroup'
  };

  const editSettings: EditSettingsModel = {
    allowAdding: true, allowEditing: true,
    allowDeleting: true, allowTaskbarEditing: true,
    showDeleteConfirmDialog: true
  };

  const labelSettings: LabelSettingsModel = { rightLabel: 'resources' };
  const splitterSettings: SplitterSettingsModel = { columnIndex: 3 };

  return (
    <GanttComponent
      height='430px'
      dataSource={data}
      taskFields={taskFields}
      resourceFields={resourceFields}
      resources={projectResources}
      viewType='ResourceView'
      editSettings={editSettings}
      toolbar={['Add', 'Edit', 'Update', 'Delete', 'Cancel', 'ExpandAll', 'CollapseAll']}
      labelSettings={labelSettings}
      splitterSettings={splitterSettings}
      projectStartDate={new Date('03/25/2019')}
      projectEndDate={new Date('07/28/2019')}
    >
      <Inject services={[Edit, Selection, Toolbar]} />
    </GanttComponent>
  );
}
```

---

## Multi-Taskbar (Resource View)

When a resource row is collapsed in resource view, all assigned tasks are shown in a single row. Enable with `enableMultiTaskbar`.

```tsx
<GanttComponent
  viewType='ResourceView'
  enableMultiTaskbar={true}
  dataSource={data}
  taskFields={taskFields}
  resourceFields={resourceFields}
  resources={projectResources}
  height='450px'
>
  <Inject services={[Edit, Selection, Toolbar, RowDD]} />
</GanttComponent>
```

**Behavior:**
- Collapsed resource row: all tasks shown in one row
- Expanded resource row: tasks shown individually
- Editing still works in collapsed rows
- `enableMultiTaskbar` defaults to `false`

**taskFields extra fields for multi-taskbar:**
```tsx
const taskFields: TaskFieldsModel = {
  ...
  expandState: 'IsExpand',  // field controlling expand/collapse state
};
```

## Configure taskbar overlap

When `enableMultiTaskbar` is enabled and the resource row is collapsed, the [allowTaskbarOverlap](https://ej2.syncfusion.com/react/documentation/api/gantt#allowtaskbaroverlap) property controls how multiple taskbars are rendered in the same resource row:

- **Overlapping mode (true, default):** Multiple taskbars overlap within the standard row height, keeping the timeline compact. Dependency connections (including between tasks of the same resource) remain supported.
- **Non-overlapping mode (false):** Taskbars are stacked vertically using an extended row height, preventing overlaps for clearer visibility of overallocation. Dependencies between tasks of the same resource are not supported.

Example (non-overlapping mode):

```tsx
<GanttComponent
  viewType='ResourceView'
  enableMultiTaskbar={true}
  allowTaskbarOverlap={false}
  dataSource={data}
  taskFields={taskFields}
  resourceFields={resourceFields}
  resources={projectResources}
  height='450px'
>
  <Inject services={[Edit, Selection, Toolbar, RowDD]} />
</GanttComponent>
```

---

## Managing Resources via Editing

Resources can be added/removed via:

| Method | Description |
|---|---|
| Cell editing | Double-click the resource cell in the grid |
| Dialog editing | Use the **Resource** tab in the Edit dialog |

---

## Custom Resource Styling

Use `queryTaskbarInfo` to color-code taskbars by resource:
```tsx
const queryTaskbarInfo = (args: any) => {
  const resourceColors: Record<number, string> = {
    1: '#4CAF50', 2: '#2196F3', 3: '#FF9800', 4: '#9C27B0'
  };
  const resourceId = args.data?.resources?.[0]?.resourceId;
  if (resourceId && resourceColors[resourceId]) {
    args.taskbarBgColor = resourceColors[resourceId];
  }
};

<GanttComponent queryTaskbarInfo={queryTaskbarInfo} ... />
```

---

## Over-Allocation Highlighting

When a resource is assigned to tasks that overlap in time and their combined units exceed 100%, they are considered **over-allocated**.

```tsx
<GanttComponent
  viewType='ResourceView'
  showOverAllocatedTasks={true}   // highlights over-allocated resource rows
  dataSource={data}
  taskFields={taskFields}
  resourceFields={resourceFields}
  resources={projectResources}
  height='450px'
>
  <Inject services={[Edit, Selection, Toolbar]} />
</GanttComponent>
```

**Behavior:**
- Only applies in `viewType='ResourceView'`
- Over-allocated rows are visually highlighted (typically red or warning color)
- Use with `resourceFields.unit` to accurately compute allocation percentages
- Defaults to `false`

---

## `resourceFields` Properties

| Property | Maps to | Description |
|---|---|---|
| `id` | Resource identifier field | Unique resource ID used in task assignments |
| `name` | Display name field | Shown in labels, columns, dialogs |
| `unit` | Work capacity field | Percentage of daily capacity (0–100), default 100 |
| `group` | Group/category field | Used for grouping in resource view |

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| Resources not appearing in labels | `labelSettings.rightLabel` not set to `'resources'` | Set `rightLabel: 'resources'` |
| Resource view shows flat list | `viewType` not set to `'ResourceView'` | Set `viewType='ResourceView'` |
| Multi-taskbar not working | `enableMultiTaskbar` false or not in ResourceView mode | Set both `viewType='ResourceView'` and `enableMultiTaskbar={true}` |
| Unassigned tasks missing | Expected — they group under "Unassigned Task" node | This is default behavior |
| Unit not applying | Unit specified only at resource level | Override at task level with `{ resourceId: 1, unit: 80 }` |
