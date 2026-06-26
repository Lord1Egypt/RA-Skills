# Taskbar, Labels, Markers & Critical Path

## Table of Contents
- [Taskbar Customization](#taskbar-customization)
- [Task Labels](#task-labels)
- [Baseline](#baseline)
- [Data Markers (Task-Level Indicators)](#data-markers-task-level-indicators)
- [Event Markers (Project-Wide Timeline Markers)](#event-markers-project-wide-timeline-markers)
- [Critical Path](#critical-path)
- [Complete Example — Taskbar, Labels, Baseline, Event Markers & Critical Path](#complete-example--taskbar-labels-baseline-event-markers--critical-path)
- [Common Pitfalls](#common-pitfalls)

---

## Taskbar Customization

### Taskbar Height
```tsx
<GanttComponent
  dataSource={data}
  taskFields={taskFields}
  rowHeight={50}
  taskbarHeight={40}   // must be less than rowHeight
  height='450px'
/>
```

### Conditional Formatting via `queryTaskbarInfo`
Use the `queryTaskbarInfo` event to dynamically style taskbars:
```tsx
const queryTaskbarInfo = (args: IQueryTaskbarInfoEventArgs) => {
  if (args.data.Progress < 30) {
    args.taskbarBgColor = '#ff4d4d';
    args.progressBarBgColor = '#cc0000';
  } else if (args.data.Progress < 70) {
    args.taskbarBgColor = '#ffa500';
    args.progressBarBgColor = '#cc7a00';
  } else {
    args.taskbarBgColor = '#4CAF50';
    args.progressBarBgColor = '#388E3C';
  }
};

<GanttComponent
  queryTaskbarInfo={queryTaskbarInfo}
  ...
/>
```

**`queryTaskbarInfo` args properties:**
| Property | Description |
|---|---|
| `args.taskbarBgColor` | Background color of the taskbar |
| `args.progressBarBgColor` | Color of the progress portion |
| `args.taskbarBorderColor` | Border color of taskbar |
| `args.data` | Task record data |
| `args.rowData` | Full row data including gantt properties |

### Custom Taskbar Templates
```tsx
const taskbarTemplate = (props: any) => (
  <div className="custom-taskbar" style={{ height: '100%', background: '#6f42c1' }}>
    <span>{props.TaskName}</span>
    <span className="progress" style={{ width: `${props.Progress}%` }} />
  </div>
);

const parentTaskbarTemplate = (props: any) => (
  <div className="parent-taskbar" style={{ height: '100%', background: '#343a40' }}>
    <span>{props.TaskName}</span>
  </div>
);

const milestoneTemplate = (props: any) => (
  <div className="milestone-diamond" />
);

<GanttComponent
  taskbarTemplate={taskbarTemplate}
  parentTaskbarTemplate={parentTaskbarTemplate}
  milestoneTemplate={milestoneTemplate}
  ...
/>
```

### Connector Lines (Dependency Arrows)
```tsx
<GanttComponent
  connectorLineWidth={2}
  connectorLineBackground='#ff6347'
  ...
/>
```

### Tooltip Settings
```tsx
// Safe formatter: supports both Date objects and ISO/string inputs.
const formatDate = (value: any) => {
  if (!value) return '';
  const d = value instanceof Date ? value : new Date(value);
  return isNaN(d.getTime()) ? '' : d.toDateString();
};

const tooltipSettings = {
  showTooltip: true,

  // Taskbar tooltip
  taskbar: (props: any) => (
    <div>
      <b>{props.TaskName}</b>
      <p>Start: {formatDate(props.StartDate)}</p>
      <p>End: {formatDate(props.EndDate)}</p>
      {props.Duration != null && <p>Duration: {props.Duration}</p>}
      <p>Progress: {props.Progress}%</p>
    </div>
  ),

  // Connector line tooltip (dependency arrows)
  connectorLine: (props: any) => (
    <div>
      <p>Offset: {props.offsetString}</p>
    </div>
  ),

  // Baseline tooltip
  baseline: (props: any) => (
    <div>
      <p>Baseline Start: {formatDate(props.BaselineStartDate)}</p>
      <p>Baseline End: {formatDate(props.BaselineEndDate)}</p>
    </div>
  ),

  // Timeline tooltip (top/bottom tier)
  timeline: (props: any) => (
    <div style={{ padding: 5 }}>
      <div style={{ fontWeight: 700 }}>{props.tier === 'topTier' ? props.value : props.date}</div>
      <div style={{ marginTop: 4 }}>Label: {props.value}</div>
    </div>
  )
};

<GanttComponent tooltipSettings={tooltipSettings} ... />
```

Optional: Disable taskbar tooltip for specific UI targets (taskbars and resizers) using `beforeTooltipRender`.

```tsx
import { BeforeTooltipRenderEventArgs } from '@syncfusion/ej2-react-gantt';

const beforeTooltipRender = (args: BeforeTooltipRenderEventArgs): void => {
  const classList = (args.args?.target as HTMLElement | undefined)?.classList;
  if (
    classList?.contains('e-gantt-child-taskbar') ||
    classList?.contains('e-gantt-parent-taskbar') ||
    classList?.contains('e-taskbar-left-resizer') ||
    classList?.contains('e-taskbar-right-resizer')
  ) {
    args.cancel = true;
  }
};

<GanttComponent tooltipSettings={tooltipSettings} beforeTooltipRender={beforeTooltipRender} ... />
```

---

## Task Labels

Configure labels via `labelSettings`:

| Position | Property | Description |
|---|---|---|
| Left of taskbar | `leftLabel` | Identifiers like task name or ID |
| Right of taskbar | `rightLabel` | Metrics like progress or duration |
| On taskbar | `taskLabel` | Overlaid on the bar (clips for short tasks) |

### Field Reference Labels
```tsx
const labelSettings = {
  leftLabel: 'Task Id: ${TaskID}',
  rightLabel: 'Task Name: ${taskData.TaskName}',
  taskLabel: '${Progress}%'
};

<GanttComponent labelSettings={labelSettings} ... />
```

### Template Labels
```tsx
const labelSettings = {
  leftLabel: (props: any) => (
    <span style={{ color: props.Priority === 'High' ? 'red' : 'green' }}>
      {props.TaskName}
    </span>
  ),
  rightLabel: (props: any) => (
    <div style={{ display: 'flex', alignItems: 'center' }}>
      <div style={{ width: `${props.Progress}%`, background: '#4CAF50', height: 6 }} />
      <span>{props.Progress}%</span>
    </div>
  ),
  taskLabel: '${Progress}%'
};
```

---

## Baseline

Show planned vs actual dates side-by-side.

### Data Source Fields
```typescript
const data = [
  {
    TaskID: 1,
    TaskName: 'Project Planning',
    StartDate: new Date('02/04/2019'),
    EndDate: new Date('02/08/2019'),
    baselineStartDate: new Date('02/02/2019'),
    baselineEndDate: new Date('02/06/2019'),
    baselineDuration: '5'  // regular baseline
  },
  {
    TaskID: 2,
    TaskName: 'Milestone Review',
    StartDate: new Date('02/10/2019'),
    EndDate: new Date('02/10/2019'),
    baselineStartDate: new Date('02/09/2019'),
    baselineEndDate: new Date('02/09/2019'),
    baselineDuration: '0'  // baseline milestone — must be '0'
  }
];
```

> **Milestone Baseline Rule:** Set `baselineDuration: '0'` explicitly. Same start/end dates without this results in a 1-day task, not a milestone.

### Configuration
```tsx
const taskFields = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  endDate: 'EndDate',
  baselineStartDate: 'baselineStartDate',
  baselineEndDate: 'baselineEndDate',
  baselineDuration: 'baselineDuration',
};

<GanttComponent
  dataSource={data}
  taskFields={taskFields}
  renderBaseline={true}
  baselineColor='rgba(255, 107, 107, 0.8)'
  height='450px'
/>
```

### Baseline CSS Customization
```css
.e-gantt .e-gantt-chart .e-baseline-bar {
  height: 4px;
  border-radius: 2px;
  opacity: 0.9;
  background-color: #4CAF50;
}
```

---

## Data Markers (Task-Level Indicators)

Data markers appear within individual task rows at a specific date, showing icons with tooltips.

### Data Structure
```typescript
const data = [
  {
    TaskID: 1,
    TaskName: 'Planning',
    StartDate: new Date('04/02/2019'),
    EndDate: new Date('04/21/2019'),
    Indicators: [
      {
        date: new Date('04/10/2019'),
        iconClass: 'e-btn-icon e-notes-info e-icons e-icon-left e-gantt e-notes-info::before',
        name: 'Review',
        tooltip: 'Mid-phase review meeting'
      },
      {
        date: new Date('04/18/2019'),
        iconClass: 'e-btn-icon e-milestone e-icons',
        name: 'Gate',
        tooltip: 'Phase gate checkpoint'
      }
    ]
  }
];
```

### taskFields Mapping
```tsx
const taskFields = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  endDate: 'EndDate',
  indicators: 'Indicators'   // maps the indicators array
};
```

### Indicator Object Properties
| Property | Type | Description |
|---|---|---|
| `date` | Date | Timeline position of the marker |
| `iconClass` | string | CSS class for icon appearance |
| `name` | string | Unique identifier for the marker |
| `tooltip` | string | Hover tooltip text (empty = no tooltip) |

---

## Event Markers (Project-Wide Timeline Markers)

Event markers render as vertical lines spanning the entire chart height, unlike data markers which are task-scoped.

### Required Module Injection
```tsx
import { DayMarkers } from '@syncfusion/ej2-react-gantt';

<GanttComponent ...>
  <Inject services={[DayMarkers]} />
</GanttComponent>
```

### Configuration
```tsx
const eventMarkers = [
  { day: new Date('2019-04-20'), label: 'Research phase ends' },
  { day: new Date('2019-05-18'), label: 'Design phase ends', cssClass: 'design-end' },
  { day: new Date('2019-06-05'), label: 'Production phase ends', top: 20 },
  { day: new Date('2019-06-20'), label: 'Sales phase starts' }
];

<GanttComponent eventMarkers={eventMarkers} ...>
  <Inject services={[DayMarkers]} />
</GanttComponent>
```

### Event Marker Properties
| Property | Description |
|---|---|
| `day` | Date where vertical line appears |
| `label` | Descriptive text for the marker |
| `cssClass` | Custom CSS class for styling |
| `top` | Vertical offset (px) to avoid overlap on same-date markers |

### CSS Customization
```css
.design-end .e-span-label {
  color: #ff6347;
  font-weight: bold;
}
```

---

## Critical Path

Highlights the longest chain of dependent tasks that determines project duration. Critical tasks appear in red with emphasized connector lines.

### Required Module Injection
```tsx
import { CriticalPath } from '@syncfusion/ej2-react-gantt';

<GanttComponent ...>
  <Inject services={[CriticalPath]} />
</GanttComponent>
```

### Enable Critical Path
```tsx
// Option 1: Always visible
<GanttComponent
  enableCriticalPath={true}
  ...
>
  <Inject services={[CriticalPath]} />
</GanttComponent>

// Option 2: Toolbar toggle
<GanttComponent
  toolbar={['CriticalPath']}
  ...
>
  <Inject services={[CriticalPath]} />
</GanttComponent>
```

### Programmatic Access
```tsx
const ganttRef = useRef<GanttComponent>(null);

// Get all critical tasks at runtime
const criticalTasks = ganttRef.current?.getCriticalTasks();
console.log(criticalTasks);
```

### How Criticality Is Determined
| Condition | Result |
|---|---|
| Slack = 0 | Task is critical (any delay shifts project end) |
| Slack < 0 | Task is already behind schedule |
| Progress = 100% | Task is excluded (completed tasks cannot cause future delays) |
| Task end date ≥ project end date | Always critical |

### Critical Path with `projectEndDate`
```tsx
<GanttComponent
  projectEndDate={new Date('2019-06-30')}
  enableCriticalPath={true}
  ...
>
  <Inject services={[CriticalPath]} />
</GanttComponent>
```

> If `projectEndDate` is omitted, the latest task end date is used as the reference.

---

## Complete Example — Taskbar, Labels, Baseline, Event Markers & Critical Path

```tsx
import React, { useRef } from 'react';
import {
  GanttComponent, ColumnsDirective, ColumnDirective,
  Inject, DayMarkers, CriticalPath,
  TaskFieldsModel, IQueryTaskbarInfoEventArgs
} from '@syncfusion/ej2-react-gantt';

const data = [
  {
    TaskID: 1, TaskName: 'Project Init',
    StartDate: new Date('04/02/2019'), EndDate: new Date('04/21/2019'),
    baselineStartDate: new Date('04/01/2019'), baselineEndDate: new Date('04/20/2019'),
    Indicators: [{ date: new Date('04/10/2019'), iconClass: 'e-btn-icon e-notes-info e-icons', name: 'Review', tooltip: 'Phase review' }]
  },
  {
    TaskID: 2, TaskName: 'Development',
    StartDate: new Date('04/22/2019'), EndDate: new Date('05/10/2019'),
    Predecessor: '1FS', Progress: 45,
    baselineStartDate: new Date('04/21/2019'), baselineEndDate: new Date('05/08/2019'),
  }
];

function App() {
  const ganttRef = useRef<GanttComponent>(null);

  const taskFields: TaskFieldsModel = {
    id: 'TaskID', name: 'TaskName',
    startDate: 'StartDate', endDate: 'EndDate',
    progress: 'Progress', dependency: 'Predecessor',
    baselineStartDate: 'baselineStartDate',
    baselineEndDate: 'baselineEndDate',
    indicators: 'Indicators'
  };

  const labelSettings = {
    leftLabel: '${TaskName}',
    taskLabel: '${Progress}%'
  };

  const eventMarkers = [
    { day: new Date('2019-04-15'), label: 'Sprint 1 ends' },
    { day: new Date('2019-05-01'), label: 'Sprint 2 ends', cssClass: 'sprint-end' }
  ];

  const queryTaskbarInfo = (args: IQueryTaskbarInfoEventArgs) => {
    if ((args.data as any).Progress < 50) {
      args.taskbarBgColor = '#ff6b6b';
    }
  };

  return (
    <GanttComponent
      ref={ganttRef}
      dataSource={data}
      taskFields={taskFields}
      labelSettings={labelSettings}
      eventMarkers={eventMarkers}
      renderBaseline={true}
      baselineColor='#ff6347'
      enableCriticalPath={true}
      taskbarHeight={32}
      rowHeight={50}
      queryTaskbarInfo={queryTaskbarInfo}
      height='450px'
    >
      <ColumnsDirective>
        <ColumnDirective field='TaskID' width='60' />
        <ColumnDirective field='TaskName' width='200' />
        <ColumnDirective field='StartDate' />
        <ColumnDirective field='Duration' />
        <ColumnDirective field='Progress' />
      </ColumnsDirective>
      <Inject services={[DayMarkers, CriticalPath]} />
    </GanttComponent>
  );
}

export default App;
```

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| Baseline not visible | `renderBaseline` not set or missing `taskFields` mappings | Set `renderBaseline={true}` and map all baseline fields |
| Baseline milestone shows as 1-day task | Missing `baselineDuration: '0'` | Always set `baselineDuration` to `'0'` for milestones |
| Event markers not rendering | `DayMarkers` service not injected | Add `<Inject services={[DayMarkers]} />` |
| Critical path not shown | `CriticalPath` service not injected | Add `<Inject services={[CriticalPath]} />` |
| Data marker tooltips not appearing | Empty `tooltip` property | Provide a non-empty string to `tooltip` |
| `queryTaskbarInfo` styles not applying | Template taskbar overrides event | Avoid mixing `taskbarTemplate` and `queryTaskbarInfo` |
