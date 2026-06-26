# Task Scheduling in Syncfusion React Gantt Chart

## Table of Contents
- [Scheduling Modes Overview](#scheduling-modes-overview)
- [Auto Scheduling (Default)](#auto-scheduling-default)
- [Manual Scheduling](#manual-scheduling)
- [Custom Scheduling (Mixed Mode)](#custom-scheduling-mixed-mode)
- [Unscheduled Tasks](#unscheduled-tasks)
- [Project Start and End Dates](#project-start-and-end-dates)
- [Choosing the Right Mode](#choosing-the-right-mode)

---

## Scheduling Modes Overview

The `taskMode` prop controls how task dates are calculated and validated:

| Mode | Value | Description |
|---|---|---|
| **Auto** | `"Auto"` (default) | Dates auto-validated from dependencies, working time, holidays, weekends |
| **Manual** | `"Manual"` | Dates fixed as given in data source; no auto-recalculation |
| **Custom** | `"Custom"` | Per-task: each task can be auto or manual, driven by a boolean field |

---

## Auto Scheduling (Default)

In **Auto** mode:
- Parent task dates are calculated from child tasks (min start → max end)
- Dates adjust automatically when predecessors change
- You cannot manually edit parent task dates/progress (they are derived)
- Dependencies, holidays, weekends, and working time all affect calculated dates

```tsx
import { GanttComponent, ColumnsDirective, ColumnDirective, Inject, Edit, Toolbar, Selection } from '@syncfusion/ej2-react-gantt';
import { TaskFieldsModel, EditSettingsModel } from '@syncfusion/ej2-gantt';

const taskFields: TaskFieldsModel = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  endDate: 'EndDate',
  duration: 'Duration',
  progress: 'Progress',
  parentID: 'ParentID',
};

const editSettings: EditSettingsModel = {
  allowEditing: true,
  allowDeleting: true,
  allowTaskbarEditing: true,
};

function App() {
  return (
    <GanttComponent
      dataSource={projectData}
      taskFields={taskFields}
      taskMode="Auto"
      editSettings={editSettings}
      toolbar={['Add', 'Edit', 'Update', 'Delete', 'Cancel', 'ExpandAll', 'CollapseAll']}
      height="450px"
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID"   headerText="Task ID"   width="100" />
        <ColumnDirective field="TaskName" headerText="Task Name" width="250" />
        <ColumnDirective field="StartDate" />
        <ColumnDirective field="Duration" />
        <ColumnDirective field="Progress" />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar, Selection]} />
    </GanttComponent>
  );
}
```

---

## Manual Scheduling

In **Manual** mode:
- Start and end dates are taken directly from the data source, with no auto-recalculation
- Parent task dates are also taken from data (not derived from children)
- Predecessors do NOT automatically shift successor dates
- Use `validateManualTasksOnLinking={true}` to enable predecessor-based validation only (dates adjust on linking, but not on other changes)

```tsx
function App() {
  return (
    <GanttComponent
      dataSource={data}
      taskFields={taskFields}
      taskMode="Manual"
      validateManualTasksOnLinking={true}  // optional: enable predecessor shifts
      editSettings={editSettings}
      toolbar={['Add', 'Edit', 'Update', 'Delete', 'Cancel']}
      height="450px"
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskName"  headerText="Task Name" width="250" />
        <ColumnDirective field="StartDate" />
        <ColumnDirective field="Duration" />
        <ColumnDirective field="Progress" />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar, Selection]} />
    </GanttComponent>
  );
}
```

> **When to use Manual mode:** When your project data has fixed dates that should not be recalculated — e.g., contractually fixed milestones or imported schedules from external tools.

---

## Custom Scheduling (Mixed Mode)

In **Custom** mode, each task independently decides whether it is auto or manually scheduled, driven by a boolean field in the data source.

Map the boolean field using `taskFields.manual`:

```tsx
// Data example:
const data = [
  { TaskID: 1, TaskName: 'Design Phase',    StartDate: new Date('04/02/2024'), Duration: 5, isManual: false }, // auto
  { TaskID: 2, TaskName: 'Fixed Milestone', StartDate: new Date('04/10/2024'), Duration: 0, isManual: true  }, // manual
  { TaskID: 3, TaskName: 'Development',     StartDate: new Date('04/11/2024'), Duration: 7, isManual: false }, // auto
];

const taskFields: TaskFieldsModel = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  duration: 'Duration',
  progress: 'Progress',
  manual: 'isManual',   // <-- boolean field per task
};

function App() {
  return (
    <GanttComponent
      dataSource={data}
      taskFields={taskFields}
      taskMode="Custom"
      validateManualTasksOnLinking={true}
      editSettings={editSettings}
      height="450px"
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskName" headerText="Task Name" width="250" />
        <ColumnDirective field="isManual" headerText="Manual"    width="100" />
        <ColumnDirective field="StartDate" />
        <ColumnDirective field="Duration" />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar, Selection]} />
    </GanttComponent>
  );
}
```

> **When to use Custom mode:** When a project has a mix — some tasks are fixed (milestones, contractual deliverables) and others should auto-schedule around dependencies.

---

## Unscheduled Tasks

A task is "unscheduled" when its date/duration information is incomplete. Gantt renders these as special taskbars.

| Scenario | Data | Rendering |
|---|---|---|
| Duration only | `Duration: 3` (no dates) | Taskbar positioned at project start |
| Start date only | `StartDate: ...` (no duration/end) | Open-ended taskbar |
| End date only | `EndDate: ...` (no start/duration) | Taskbar ending at given date |
| No dates at all | No start, end, or duration | Milestone at project start |

Enable unscheduled task support by providing `allowUnscheduledTasks={true}`:

```tsx
<GanttComponent
  dataSource={data}
  taskFields={taskFields}
  allowUnscheduledTasks={true}
  height="450px"
/>
```

---

## Project Start and End Dates

Explicitly set the visible timeline range using `projectStartDate` and `projectEndDate`:

```tsx
<GanttComponent
  dataSource={data}
  taskFields={taskFields}
  projectStartDate={new Date('03/25/2024')}
  projectEndDate={new Date('07/28/2024')}
  height="450px"
/>
```

Without these, Gantt auto-calculates the range from the earliest start and latest end date in your data.

---

## Choosing the Right Mode

| Need | Use |
|---|---|
| Standard project plan that auto-adjusts when tasks change | `taskMode="Auto"` |
| Fixed schedule imported from another tool (e.g., Excel) | `taskMode="Manual"` |
| Mix of fixed milestones and flexible tasks | `taskMode="Custom"` |
| Predecessor changes should still shift manual tasks | Add `validateManualTasksOnLinking={true}` |
| Tasks with incomplete date info | Add `allowUnscheduledTasks={true}` |
