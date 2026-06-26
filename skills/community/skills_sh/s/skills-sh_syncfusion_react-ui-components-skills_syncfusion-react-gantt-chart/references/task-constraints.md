# Task Constraints in Syncfusion React Gantt Chart

## Table of Contents
- [Overview](#overview)
- [Constraint Types](#constraint-types)
- [Configuring Constraints in Data Source](#configuring-constraints-in-data-source)
- [Mapping constraintType and constraintDate](#mapping-constrainttype-and-constraintdate)
- [Full Example](#full-example)
- [Handling Constraint Violations](#handling-constraint-violations)
- [Displaying Constraint Type in a Column](#displaying-constraint-type-in-a-column)
- [Interaction with taskMode and Dependencies](#interaction-with-taskmode-and-dependencies)

---

## Overview

Task constraints define scheduling rules that control when a task may start or finish. They enforce project realities like fixed deadlines, regulatory compliance dates, or resource availability windows.

Constraints affect:
- Taskbar positioning in the chart
- Dependency scheduling and critical path calculations
- Validation popup behavior when editing conflicting tasks

---

## Constraint Types

Eight constraint types are available via the `ConstraintType` enum (numeric values 0–7):

| Constraint | Enum Value | Rule |
|---|---|---|
| As Soon As Possible (ASAP) | `0` | Task starts as soon as dependencies are satisfied (default for Auto mode) |
| As Late As Possible (ALAP) | `1` | Task is delayed until the latest possible start without delaying successors |
| Must Start On (MSO) | `2` | Task must begin on the specified `constraintDate` |
| Must Finish On (MFO) | `3` | Task must end on the specified `constraintDate` |
| Start No Earlier Than (SNET) | `4` | Task cannot start before the specified `constraintDate` |
| Start No Later Than (SNLT) | `5` | Task must start on or before the specified `constraintDate` |
| Finish No Earlier Than (FNET) | `6` | Task cannot finish before the specified `constraintDate` |
| Finish No Later Than (FNLT) | `7` | Task must finish on or before the specified `constraintDate` |

> ASAP (0) is the default for auto-scheduled tasks and requires no `constraintDate`.

---

## Configuring Constraints in Data Source

Add `ConstraintType` (numeric) and `ConstraintDate` (Date) fields to each task record:

```tsx
const data = [
  {
    TaskID: 1,
    TaskName: 'Design Approval',
    StartDate: new Date('2025-07-01'),
    EndDate: new Date('2025-07-02'),
    Duration: 1,
    ConstraintType: 2,                     // Must Start On
    ConstraintDate: new Date('2025-07-01'), // must start on July 1
  },
  {
    TaskID: 2,
    TaskName: 'Submit Compliance Report',
    StartDate: new Date('2025-07-10'),
    Duration: 3,
    ConstraintType: 7,                     // Finish No Later Than
    ConstraintDate: new Date('2025-07-31'), // must finish by July 31
  },
  {
    TaskID: 3,
    TaskName: 'Standard Task',
    StartDate: new Date('2025-07-05'),
    Duration: 4,
    ConstraintType: 0,                     // ASAP (default, no constraintDate needed)
  },
];
```

---

## Mapping constraintType and constraintDate

Map both fields in `taskFields`:

```tsx
import { TaskFieldsModel } from '@syncfusion/ej2-gantt';

const taskFields: TaskFieldsModel = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  endDate: 'EndDate',
  duration: 'Duration',
  progress: 'Progress',
  dependency: 'Predecessor',
  parentID: 'ParentID',
  constraintType: 'ConstraintType',   // numeric enum value field
  constraintDate: 'ConstraintDate',   // Date field for the constraint anchor
};
```

---

## Full Example

```tsx
import * as React from 'react';
import {
  GanttComponent, ColumnsDirective, ColumnDirective, Inject,
  Edit, Toolbar, Selection, DayMarkers
} from '@syncfusion/ej2-react-gantt';
import { TaskFieldsModel, EditSettingsModel } from '@syncfusion/ej2-gantt';

const data = [
  { TaskID: 1, TaskName: 'Project Kickoff',    StartDate: new Date('07/01/2025'), Duration: 1,  ConstraintType: 2, ConstraintDate: new Date('07/01/2025'), ParentID: null },
  { TaskID: 2, TaskName: 'Requirements',       StartDate: new Date('07/02/2025'), Duration: 5,  ConstraintType: 0, ParentID: null },
  { TaskID: 3, TaskName: 'Design',             StartDate: new Date('07/09/2025'), Duration: 7,  ConstraintType: 4, ConstraintDate: new Date('07/09/2025'), ParentID: null },
  { TaskID: 4, TaskName: 'Compliance Review',  StartDate: new Date('07/18/2025'), Duration: 4,  ConstraintType: 7, ConstraintDate: new Date('07/25/2025'), ParentID: null },
];

const taskFields: TaskFieldsModel = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  duration: 'Duration',
  constraintType: 'ConstraintType',
  constraintDate: 'ConstraintDate',
  parentID: 'ParentID',
};

const editSettings: EditSettingsModel = {
  allowAdding: true,
  allowEditing: true,
  allowDeleting: true,
  allowTaskbarEditing: true,
};

function App() {
  return (
    <GanttComponent
      dataSource={data}
      taskFields={taskFields}
      editSettings={editSettings}
      toolbar={['Add', 'Edit', 'Update', 'Delete', 'Cancel']}
      gridLines="Both"
      highlightWeekends={true}
      treeColumnIndex={1}
      height="450px"
      projectStartDate={new Date('06/25/2025')}
      projectEndDate={new Date('08/10/2025')}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID"         visible={false} />
        <ColumnDirective field="TaskName"       headerText="Task Name"       width="200" />
        <ColumnDirective field="StartDate" />
        <ColumnDirective field="Duration" />
        <ColumnDirective field="ConstraintType" headerText="Constraint Type" width="180" />
        <ColumnDirective field="ConstraintDate" headerText="Constraint Date" />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar, Selection, DayMarkers]} />
    </GanttComponent>
  );
}

export default App;
```

---

## Handling Constraint Violations

When a user drags a taskbar into a position that violates a strict constraint (MSO, MFO, SNLT, FNLT), Gantt shows a validation popup by default.

To suppress the popup and silently reject the move, use `actionBegin` with `requestType === 'validateTaskViolation'`:

```tsx
function actionBegin(args: any) {
  if (args.requestType === 'validateTaskViolation') {
    // Set to true to silently reject (no popup)
    args.validateMode.respectMustStartOn      = true;  // suppress MSO popup
    args.validateMode.respectMustFinishOn     = true;  // suppress MFO popup
    args.validateMode.respectStartNoLaterThan = true;  // suppress SNLT popup
    args.validateMode.respectFinishNoLaterThan = true; // suppress FNLT popup
  }
}

<GanttComponent actionBegin={actionBegin} ... />
```

Setting a flag to `false` (default) shows the popup and lets the user choose to accept or reject.

---

## Displaying Constraint Type in a Column

Constraint type is stored as a number. Use a template or value accessor to display a human-readable label:

```tsx
const constraintLabels: Record<number, string> = {
  0: 'As Soon As Possible',
  1: 'As Late As Possible',
  2: 'Must Start On',
  3: 'Must Finish On',
  4: 'Start No Earlier Than',
  5: 'Start No Later Than',
  6: 'Finish No Earlier Than',
  7: 'Finish No Later Than',
};

// Use as a right label template on taskbar:
const RightLabel = (props: any) => (
  <span>{constraintLabels[props.ganttProperties.constraintType] ?? ''}</span>
);

const labelSettings = {
  leftLabel: 'TaskName',
  rightLabel: RightLabel,
};

<GanttComponent labelSettings={labelSettings} ... />
```

---

## Interaction with taskMode and Dependencies

- **Auto mode + ASAP:** Default behavior — tasks schedule as early as possible after predecessors finish.
- **Auto mode + MSO/MFO:** Task is pinned to the constraint date regardless of predecessor completion.
- **Manual mode:** Constraints are recorded in data but have no automatic scheduling effect (dates are fixed). They become relevant when `validateManualTasksOnLinking={true}` is set.
- **Constraints vs. Dependencies conflict:** When a dependency would push a task past a SNLT/FNLT constraint, a validation popup appears and the user must resolve the conflict.
