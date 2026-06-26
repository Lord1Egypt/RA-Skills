# Getting Started with Syncfusion React Gantt Chart

## Table of Contents
- [Dependencies](#dependencies)
- [Project Setup](#project-setup)
- [Install the Package](#install-the-package)
- [Add CSS Imports](#add-css-imports)
- [Basic Gantt Implementation](#basic-gantt-implementation)
- [taskFields Mapping](#taskfields-mapping)
- [Module Injection](#module-injection)
- [Common Setup Gotchas](#common-setup-gotchas)
- [Grid Lines](#grid-lines)

---

## Dependencies

Install the Gantt package and its peer dependencies:

```bash
npm install @syncfusion/ej2-react-gantt --save
```

The component relies on packages such as `@syncfusion/ej2-gantt`, `@syncfusion/ej2-grids`, `@syncfusion/ej2-layouts`, and `@syncfusion/ej2-treegrid`.

---

## Project Setup

Use Vite for a quick React setup:

```bash
# JavaScript
npm create vite@latest my-gantt-app -- --template react
cd my-gantt-app
npm install

# TypeScript
npm create vite@latest my-gantt-app -- --template react-ts
cd my-gantt-app
npm install
```

Run the app with:

```bash
npm run dev
```

---

## Install the Package

```bash
npm install @syncfusion/ej2-react-gantt --save
```

---

## Add CSS Imports

Add the required theme styles to `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-calendars/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-gantt/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-grids/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-layouts/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-lists/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-notifications/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-richtexteditor/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-treegrid/styles/tailwind3.css";
```

Then import the stylesheet in `src/App.tsx`:

```tsx
import './App.css';
```

> Replace `tailwind3` with your preferred theme if needed.

---

## Basic Gantt Implementation

Minimal working example using hierarchical data:

```tsx
import * as React from 'react';
import { GanttComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-gantt';
import { TaskFieldsModel } from '@syncfusion/ej2-gantt';
import './App.css';

const data = [
  {
    TaskID: 1,
    TaskName: 'Project Initiation',
    StartDate: new Date('04/02/2024'),
    EndDate: new Date('04/21/2024'),
    subtasks: [
      { TaskID: 2, TaskName: 'Identify Site Location', StartDate: new Date('04/02/2024'), Duration: 4, Progress: 50 },
      { TaskID: 3, TaskName: 'Perform Soil Test', StartDate: new Date('04/02/2024'), Duration: 4, Progress: 50 },
      { TaskID: 4, TaskName: 'Soil Test Approval', StartDate: new Date('04/08/2024'), Duration: 0, Progress: 50 },
    ],
  },
  {
    TaskID: 5,
    TaskName: 'Project Estimation',
    StartDate: new Date('04/02/2024'),
    EndDate: new Date('04/21/2024'),
    subtasks: [
      { TaskID: 6, TaskName: 'Develop Floor Plan', StartDate: new Date('04/04/2024'), Duration: 3, Progress: 50 },
      { TaskID: 7, TaskName: 'List Materials', StartDate: new Date('04/04/2024'), Duration: 3, Progress: 50 },
    ],
  },
];

const taskFields: TaskFieldsModel = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  endDate: 'EndDate',
  duration: 'Duration',
  progress: 'Progress',
  child: 'subtasks',
};

function App() {
  return (
    <GanttComponent dataSource={data} taskFields={taskFields} height="450px">
      <ColumnsDirective>
        <ColumnDirective field="TaskID" width="80" />
        <ColumnDirective field="TaskName" headerText="Task Name" width="250" />
        <ColumnDirective field="StartDate" />
        <ColumnDirective field="Duration" />
        <ColumnDirective field="Progress" />
      </ColumnsDirective>
    </GanttComponent>
  );
}

export default App;
```

---

## taskFields Mapping

`taskFields` maps your data source fields to the Gantt model. The required fields are `id` and `name`.

```tsx
const taskFields: TaskFieldsModel = {
  id: 'TaskID',           // Unique task identifier (required)
  name: 'TaskName',       // Task display name (required)
  startDate: 'StartDate', // Task start date
  endDate: 'EndDate',     // Task end date
  duration: 'Duration',   // Duration in days (or with unit: "3 days", "5 hours")
  progress: 'Progress',   // Completion percentage (0-100)
  dependency: 'Predecessor', // Predecessor task IDs for dependencies
  child: 'subtasks',      // Nested child array (hierarchical data)
  parentID: 'ParentID',   // Parent task ID (self-referential/flat data)
  resourceInfo: 'Resources', // Assigned resources
  notes: 'Notes',         // Task notes
  cssClass: 'CssClass',   // Custom CSS class per task
  indicators: 'Indicators', // Task indicator icons/labels
  segments: 'Segments',   // Split task segments
  constraintType: 'ConstraintType', // Task constraint type
  constraintDate: 'ConstraintDate', // Constraint date
  baselineStartDate: 'BaselineStartDate', // Baseline start
  baselineEndDate: 'BaselineEndDate',     // Baseline end
  manual: 'isManual',     // Manual scheduling flag
};
```

Use either `child` for hierarchical data or `parentID` for flat data, not both.

---

## Module Injection

Inject only the services you need:

```tsx
import {
  GanttComponent,
  Inject,
  Edit,         // Cell/dialog/taskbar editing
  Filter,       // Column filtering
  Sort,         // Column sorting
  Toolbar,      // Toolbar items
  Selection,    // Row/cell selection
  ColumnMenu,   // Column header menu
  Reorder,      // Column drag-reorder
  Resize,       // Column resizing
  DayMarkers,   // Event markers and holidays
  ExcelExport,  // Excel export
  PdfExport,    // PDF export
  ContextMenu,  // Right-click context menu
  VirtualScroll, // Virtual scrolling
  UndoRedo,     // Undo/redo support
  RowDD,        // Row drag-and-drop
  CriticalPath, // Critical path highlighting
} from '@syncfusion/ej2-react-gantt';

function App() {
  return (
    <GanttComponent ...>
      <Inject services={[Edit, Filter, Sort, Toolbar, Selection]} />
    </GanttComponent>
  );
}
```

---

## Common Setup Gotchas

- Ensure `App.css` is imported in `App.tsx`.
- Missing any required CSS package can break the UI.
- Start task IDs from `1`; avoid `0` and `undefined`.
- Match `taskFields.id` and `taskFields.name` exactly to your data.
- Set a height such as `height="450px"`; the Gantt needs a fixed height to render.
- In Auto mode, parent task dates are calculated from child tasks.

---

## Grid Lines

Control the TreeGrid grid lines with `gridLines`:

```tsx
<GanttComponent
  gridLines='Both'
  dataSource={data}
  taskFields={taskFields}
  height='450px'
/>
```

| Value | Effect |
|---|---|
| `'Both'` | Horizontal and vertical lines |
| `'Horizontal'` | Horizontal lines only |
| `'Vertical'` | Vertical lines only |
| `'None'` | No grid lines |

Default is `'Horizontal'`.

---

## Output

After rendering, the Gantt chart displays:

- A task hierarchy with parent and child records
- A timeline with taskbars sized by start date and duration
- Progress indicators on each task
- Auto-calculated parent dates in Auto scheduling mode

This provides a simple baseline sample for learning how to bind and render Gantt data in React.

**Parent task dates:**
- In Auto mode, parent task dates are calculated from child tasks and cannot be manually set.
- To set parent dates manually, use `taskMode="Manual"` or `taskMode="Custom"`.
