# Data Binding in Syncfusion React Gantt Chart

## Table of Contents
- [Overview](#overview)
- [Hierarchical Data Binding](#hierarchical-data-binding)
- [Self-Referential (Flat) Data Binding](#self-referential-flat-data-binding)
- [Remote Data Binding](#remote-data-binding)
- [URL Adaptor](#url-adaptor)
- [Sending Additional Parameters to Server](#sending-additional-parameters-to-server)
- [Binding with Ajax](#binding-with-ajax)
- [Handling HTTP Errors](#handling-http-errors)
- [Load Child on Demand](#load-child-on-demand)
- [Split Tasks in Data Source](#split-tasks-in-data-source)
- [Performance: Disable Auto Validation](#performance-disable-auto-validation)
- [Common Pitfalls](#common-pitfalls)

---

## Overview

The Gantt component accepts data via the `dataSource` prop. Two formats are supported:
- **Local data:** JavaScript object array (hierarchical or flat)
- **Remote data:** A `DataManager` instance pointing to a REST API

---

## Hierarchical Data Binding

Tasks are nested using a child array. Map the array property name to `taskFields.child`.

```tsx
import * as React from 'react';
import { GanttComponent } from '@syncfusion/ej2-react-gantt';
import { TaskFieldsModel } from '@syncfusion/ej2-gantt';

const hierarchyData = [
  {
    TaskID: 1,
    TaskName: 'Project Initiation',
    StartDate: new Date('04/02/2024'),
    EndDate: new Date('04/21/2024'),
    subtasks: [
      { TaskID: 2, TaskName: 'Identify Site Location', StartDate: new Date('04/02/2024'), Duration: 4, Progress: 50 },
      { TaskID: 3, TaskName: 'Perform Soil Test',      StartDate: new Date('04/02/2024'), Duration: 4, Progress: 50 },
      { TaskID: 4, TaskName: 'Soil Test Approval',     StartDate: new Date('04/08/2024'), Duration: 0, Progress: 50 },
    ],
  },
];

const taskFields: TaskFieldsModel = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  duration: 'Duration',
  progress: 'Progress',
  child: 'subtasks',  // <-- maps the nested children array
};

function App() {
  return <GanttComponent dataSource={hierarchyData} taskFields={taskFields} height="400px" />;
}
```

---

## Self-Referential (Flat) Data Binding

All tasks are in a flat array. Parent–child relationships are expressed via a `parentID` field. Use `taskFields.parentID` to map it.

```tsx
const flatData = [
  { TaskID: 1, TaskName: 'Project Initiation',     StartDate: new Date('04/02/2024'), EndDate: new Date('04/21/2024') },
  { TaskID: 2, TaskName: 'Identify Site Location', StartDate: new Date('04/02/2024'), Duration: 4, Progress: 50, ParentID: 1 },
  { TaskID: 3, TaskName: 'Perform Soil Test',      StartDate: new Date('04/02/2024'), Duration: 4, Progress: 50, ParentID: 1 },
  { TaskID: 4, TaskName: 'Soil Test Approval',     StartDate: new Date('04/08/2024'), Duration: 4, Progress: 50, ParentID: 1 },
  { TaskID: 5, TaskName: 'Project Estimation',     StartDate: new Date('04/02/2024'), EndDate: new Date('04/21/2024') },
  { TaskID: 6, TaskName: 'Develop Floor Plan',     StartDate: new Date('04/04/2024'), Duration: 3, Progress: 50, ParentID: 5 },
];

const taskFields: TaskFieldsModel = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  duration: 'Duration',
  progress: 'Progress',
  parentID: 'ParentID',  // <-- flat data parent reference
};

function App() {
  return <GanttComponent dataSource={flatData} taskFields={taskFields} height="400px" />;
}
```

> **Note:** Do NOT map both `child` and `parentID` at the same time. If both are mapped, `parentID` takes priority and hierarchical nesting is ignored.

---

## Remote Data Binding

Use `DataManager` with an adaptor to connect to a REST API.

### WebApiAdaptor

```tsx
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

const dataSource = new DataManager({
  url: '/api/GanttData',
  adaptor: new WebApiAdaptor,
  crossDomain: true,
});

const taskFields: TaskFieldsModel = {
  id: 'TaskId',
  name: 'TaskName',
  startDate: 'StartDate',
  duration: 'Duration',
  dependency: 'Predecessor',
  child: 'SubTasks',
};

function App() {
  return <GanttComponent dataSource={dataSource} taskFields={taskFields} height="450px" />;
}
```

### RemoteSaveAdaptor (client-side data, server-side CRUD)

Use this when you want local rendering but persist changes via server:

```tsx
import { DataManager, RemoteSaveAdaptor } from '@syncfusion/ej2-data';

const dataSource = new DataManager({
  json: localData,           // local data array
  batchUrl: '/api/BatchUpdate', // server endpoint for CRUD
  adaptor: new RemoteSaveAdaptor,
});
```

The server endpoint receives a payload with `added`, `changed`, and `deleted` arrays and should return `{ addedRecords, changedRecords, deletedRecords }`.

### Handling Server Errors

```tsx
function actionFailure(args: any) {
  console.error('Gantt server error:', args);
}

<GanttComponent actionFailure={actionFailure} ... />
```

---

## URL Adaptor

Use `UrlAdaptor` to bind Gantt to an ADO.NET Entity Data Model / MVC controller endpoint. The server returns `{ result, count }` JSON:

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

const dataSource = new DataManager({
  url: '/Home/UrlDatasource',
  adaptor: new UrlAdaptor,
  batchUrl: '/Home/BatchSave',   // for CRUD operations
});

const taskFields: TaskFieldsModel = {
  id: 'TaskId',
  name: 'TaskName',
  startDate: 'StartDate',
  duration: 'Duration',
  dependency: 'Predecessor',
  child: 'SubTasks',
};

function App() {
  return <GanttComponent dataSource={dataSource} taskFields={taskFields} height="450px" />;
}
```

> The server endpoint should return `{ result: [...], count: N }` JSON.

---

## Sending Additional Parameters to Server

Pass custom parameters to the server using `Query.addParams()` in the `load` event:

```tsx
import { DataManager, UrlAdaptor, Query } from '@syncfusion/ej2-data';
import { GanttComponent, Inject, Edit, Toolbar } from '@syncfusion/ej2-react-gantt';

const dataSource = new DataManager({
  url: '/Home/UrlDatasource',
  adaptor: new UrlAdaptor,
  batchUrl: '/Home/BatchSave',
});

function App() {
  let ganttInstance: GanttComponent;

  function load() {
    ganttInstance.query = new Query().addParams('ej2Gantt', 'customValue');
  }

  return (
    <GanttComponent
      dataSource={dataSource}
      taskFields={taskFields}
      load={load}
      ref={gantt => (ganttInstance = gantt!)}
      editSettings={{ allowAdding: true, allowEditing: true, allowDeleting: true }}
      toolbar={['Add', 'Edit', 'Delete', 'Cancel', 'Update', 'ExpandAll', 'CollapseAll']}
      height="450px"
    >
      <Inject services={[Edit, Toolbar]} />
    </GanttComponent>
  );
}
```

> The server receives the extra parameter alongside the standard `DataManagerRequest` payload and can read it by name (e.g., `ej2Gantt`).

---

## Binding with Ajax

Fetch data via Ajax and assign it to `dataSource` at runtime. The component behaves like a local data source after assignment:

```tsx
import { Ajax } from '@syncfusion/ej2-base';
import { GanttComponent } from '@syncfusion/ej2-react-gantt';

function App() {
  let ganttInstance: any;

  function clickHandler() {
    const ajax = new Ajax('/api/GanttData', 'GET');
    ganttInstance.showSpinner();
    ajax.send();
    ajax.onSuccess = (data: string) => {
      ganttInstance.hideSpinner();
      ganttInstance.dataSource = (JSON.parse(data)).Items;
      ganttInstance.refresh();
    };
  }

  return (
    <div>
      <button onClick={clickHandler}>Bind Data</button>
      <GanttComponent
        taskFields={taskFields}
        projectStartDate="02/24/2019"
        projectEndDate="07/20/2019"
        height="450px"
        ref={gantt => (ganttInstance = gantt)}
      />
    </div>
  );
}
```

> **Note:** Data loaded via Ajax acts as local data — server-side CRUD is not supported after assignment this way.

---

## Handling HTTP Errors

Use the `actionFailure` event to catch server-side errors (e.g., 404, 500) and display a user-facing message:

```tsx
import { DataManager } from '@syncfusion/ej2-data';

const dataSource = new DataManager({ url: '/api/GanttData' });

function App() {
  let ganttInstance: any;

  function actionFailure(args: any) {
    const span = document.createElement('span');
    ganttInstance.element.parentNode.insertBefore(span, ganttInstance.element);
    span.style.color = '#FF0000';
    span.innerHTML = 'Server exception: ' + (args.error?.status ?? 'Unknown error');
  }

  return (
    <GanttComponent
      dataSource={dataSource}
      taskFields={taskFields}
      actionFailure={actionFailure}
      height="450px"
      ref={gantt => (ganttInstance = gantt)}
    />
  );
}
```

---

## Load Child on Demand

Renders only root nodes initially and loads children from the server on expand. Useful for very large datasets.

```tsx
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';
import { VirtualScroll, Selection } from '@syncfusion/ej2-react-gantt';

const dataSource = new DataManager({
  url: '/api/GanttLoadOnDemand',
  adaptor: new WebApiAdaptor,
  crossDomain: true,
});

const taskFields: TaskFieldsModel = {
  id: 'taskId',
  name: 'taskName',
  startDate: 'startDate',
  endDate: 'endDate',
  duration: 'duration',
  progress: 'progress',
  parentID: 'parentID',
  hasChildMapping: 'isParent',   // tells Gantt which records have children
  expandState: 'IsExpanded',     // persists expand/collapse state
};

function App() {
  return (
    <GanttComponent
      dataSource={dataSource}
      taskFields={taskFields}
      enableVirtualization={true}
      loadChildOnDemand={false}   // false = load children on expand
      height="460px"
    >
      <Inject services={[Selection, VirtualScroll]} />
    </GanttComponent>
  );
}
```

> **Limitations of load-on-demand:** Filtering, sorting, and searching are not supported. Only self-referential data works.

---

## Split Tasks in Data Source

Define task segments to split a task into multiple intervals.

### Hierarchical (inline)

```tsx
const data = [
  {
    TaskID: 1,
    TaskName: 'Development',
    StartDate: new Date('04/02/2024'),
    Duration: 6,
    Segments: [
      { StartDate: new Date('04/02/2024'), Duration: 2 },
      { StartDate: new Date('04/05/2024'), Duration: 4 },
    ],
  },
];

const taskFields: TaskFieldsModel = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  duration: 'Duration',
  segments: 'Segments',  // map the segments field
};
```

### Self-referential (flat segment data)

```tsx
const segmentData = [
  { SegmentId: 1, StartDate: new Date('04/02/2024'), Duration: 2 },
  { SegmentId: 1, StartDate: new Date('04/05/2024'), Duration: 2 },
];

const taskFields: TaskFieldsModel = {
  segmentId: 'SegmentId',
};

<GanttComponent taskFields={taskFields} segmentData={segmentData} ... />
```

---

## Performance: Disable Auto Validation

For very large datasets where all dates/durations are already correct, disable auto-validation to speed up initial load:

```tsx
<GanttComponent
  dataSource={largeData}
  taskFields={taskFields}
  autoCalculateDateScheduling={false}
  height="450px"
/>
```

> When `autoCalculateDateScheduling={false}`, parent-child validation, data validation, and predecessor validation are all skipped. Ensure your data source has correct `StartDate`, `EndDate`, and `Duration` values for every task before using this.

---

## Common Pitfalls

| Issue | Cause | Fix |
|---|---|---|
| Tasks not rendered | Wrong field name in `taskFields` | Check exact field name matches (case-sensitive) |
| All tasks appear as root | `parentID` field not mapped or wrong name | Verify `taskFields.parentID` matches data field |
| Parent dates wrong in auto mode | Parent dates in data conflict with child dates | Remove parent `StartDate`/`EndDate`; they are auto-calculated |
| Remote data not loading | CORS or wrong adaptor | Verify API URL and use correct adaptor type |
| Segments not showing | `segments` field not mapped | Add `taskFields.segments: 'Segments'` |
