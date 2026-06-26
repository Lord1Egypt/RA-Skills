---
name: syncfusion-react-gantt-chart
description: Implement, configure, and customize the Syncfusion React Gantt Chart component. Use this when building project scheduling applications with task timelines, dependencies, and resource management. Covers GanttComponent setup, task constraints, taskbar customization, filtering, sorting, Excel/PDF export, critical path analysis, milestones, predecessors, resource view, and baseline tracking.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion React Gantt Chart

The Syncfusion React Gantt Chart (`GanttComponent`) is a powerful project management component for visualizing, scheduling, and managing tasks over a timeline. It supports auto/manual scheduling, task dependencies, resource planning, interactive editing, Excel/PDF export, and rich customization.

## When to Use This Skill

- Implementing a Gantt chart or project timeline in a React app
- Configuring task scheduling (auto, manual, custom modes)
- Setting up task dependencies (FS, SS, FF, SF) and constraints (ASAP, MSO, FNET, etc.)
- Binding local or remote data to the Gantt (local array, DataManager, UrlAdaptor, Ajax)
- Customizing taskbars, labels, milestones, and baselines
- Configuring resources and resource views (including multi-taskbar)
- Enabling editing (dialog, cell, taskbar drag) with validation rules
- Setting up column resize, reorder, freeze, or column menu
- Configuring WBS codes, tree column icons, or serial number columns
- Setting up filtering, sorting, or selection
- Scrolling to specific dates or controlling scroll position programmatically
- Exporting Gantt to Excel or PDF
- Handling Gantt events and enabling advanced features (undo/redo, virtual scroll, critical path, etc.)
- Globalization, localization, and RTL support

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package dependencies
- Vite / CRA project setup
- CSS theme imports (all 14 required packages)
- Basic `GanttComponent` with `taskFields` mapping
- Module injection guide (all available services)
- `gridLines` prop (`'Both'` / `'Horizontal'` / `'Vertical'` / `'None'`)
- First render walkthrough with minimal example, output summary, and common gotchas

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local array data binding
- Remote / AJAX data binding with `DataManager`
- Self-referential flat data
- `taskFields` configuration (id, name, startDate, endDate, duration, progress, child)
- Custom field mapping
- **UrlAdaptor** for server-side CRUD (`url` + `batchUrl`)
- **RemoteSaveAdaptor** for local rendering with server persistence
- Sending additional parameters to server via `Query.addParams()` in `load` event
- Binding with `Ajax` class (manual fetch)
- Load child on demand (`loadChildOnDemand={false}`, `hasChildMapping`)
- Handling HTTP errors with `actionFailure` event

### Task Scheduling
📄 **Read:** [references/task-scheduling.md](references/task-scheduling.md)
- Auto, Manual, and Custom scheduling modes (`taskMode`)
- Unscheduled tasks (duration-only, date-only, none)
- Project start date and end date configuration
- How scheduling mode affects parent task calculation
- Switching between modes dynamically

### Task Dependency
📄 **Read:** [references/task-dependency.md](references/task-dependency.md)
- Dependency types: Finish-to-Start (FS), Start-to-Start (SS), Finish-to-Finish (FF), Start-to-Finish (SF)
- Mapping `taskFields.dependency` in data source (string format: `"2FS"`, `"2FS+3d"`, `"2SS+2h"`)
- Multiple predecessors per task (comma-separated: `"2FS,3FS"`)
- Offset values with units: day, hour, minute (e.g., `"2FS+3h"`, `"2FS-1d"`)
- Drawing dependencies via UI (drag from taskbar connection points)
- Programmatic dependency management (`addPredecessor`, `removePredecessor`, `updatePredecessor`)
- Connector line customization (`connectorLineWidth`, `connectorLineBackground`)
- **Predecessor Offset Synchronization**
  - `autoUpdatePredecessorOffset={true}` — recalculate offsets on load to account for calendar rules (weekends, holidays)
  - `autoUpdatePredecessorOffset={false}` — display original offsets even if not matching rendered lines (visual inconsistency possible)
- **Offset Updates During Editing**
  - `updateOffsetOnTaskbarEdit={true}` — auto-recalculate offsets when dragging taskbars (default)
  - `updateOffsetOnTaskbarEdit={false}` — preserve offsets; manual update required via dependency dialog
- **Dependency Validation Modes** (in `actionBegin` event with `requestType === 'validateLinkedTask'`)
  - `respectLink={true}` — revert invalid edits to maintain dependency integrity
  - `removeLink={true}` — remove conflicting dependencies to allow edits
  - `preserveLinkWithEditing={true}` — update offsets to maintain links (default mode)
- **Validation Dialog** — disable all modes to show user-choice dialog (cancel edit, remove link, adjust offset)
- **Parent Dependencies** — `allowParentDependency={true}` allows cross-parent dependencies; `false` restricts to siblings only
- **Show/Hide Dependencies Dynamically** — toggle `.e-gantt-dependency-view-container` CSS visibility
- **Disable Validation** — `enablePredecessorValidation={false}` disables auto-date validation based on predecessor links

### Task Constraints
📄 **Read:** [references/task-constraints.md](references/task-constraints.md)
- Eight constraint types: ASAP, ALAP, MSO, MFO, SNET, SNLT, FNET, FNLT
- Mapping `taskFields.constraintType` and `taskFields.constraintDate`
- How constraints interact with dependencies and `taskMode`
- Editing constraints via dialog
- Validation and conflict handling

### Timeline and Zooming
📄 **Read:** [references/timeline.md](references/timeline.md)
- `timelineViewMode` quick presets (`Hour`, `Day`, `Week`, `Month`, `Year`)
- Top tier and bottom tier independent configuration (`unit`, `format`, `count`, `formatter`)
- Combining timeline cells using `count` (merge multiple units per cell)
- Custom timeline cell formatting using `formatter` (tier + mode aware)
- Timeline view dates with `viewStartDate` / `viewEndDate` (lock visible range)
- `weekStartDay` — controls which day starts a week column (0=Sun, 1=Mon…)
- Automatic timescale updates using `updateTimescaleView`
- Dynamic timeline mode change at runtime (update `timelineViewMode` + `refresh()`)
- Timeline cell tooltip visibility using `showTooltip`
- Timeline template customization using `timelineTemplate` ({ date, value, tier })
- Timeline navigation using `previousTimeSpan()` / `nextTimeSpan()`
- Zooming with toolbar (`ZoomIn`, `ZoomOut`, `ZoomToFit`)
- Customizing zoom steps with `zoomingLevels` (`ZoomTimelineSettings`)
- Programmatic zoom methods: `zoomIn()`, `zoomOut()`, `fitToProject()`
- Timeline cell width using `timelineUnitSize`
- Weekend handling:
  - Highlight weekends with `highlightWeekends={true}`
  - Hide weekends using `timelineSettings.showWeekend` (with noted limitations)

### Columns
📄 **Read:** [references/columns.md](references/columns.md)
- Column types overview (tree column, WBS, custom columns)
- Auto-generated columns (omit `ColumnsDirective`)
- Column rendering with `valueAccessor` (custom display values, concatenation)
- Expression columns (calculated values via `valueAccessor`)
- Display serial numbers via `rowDataBound`
- Tree column configuration (`treeColumnIndex`)
  - Customize expand/collapse icons (CSS override)
  - Customize indentation via `queryCellInfo`
  - `collapseAllParentTasks` — collapse all on load
  - `taskFields.expandState` — per-row initial expand/collapse
  - Persist expand/collapse state in `localStorage`
- WBS (Work Breakdown Structure) column
  - `enableWBS` + `enableAutoWbsUpdate` APIs
  - Manual WBS with `taskFields.wbsPredecessor`
- Column headers, format, and alignment
  - `headerTemplate` for custom header rendering
  - Header text wrapping (`treeGrid.textWrapSettings.wrapMode`)
  - Dynamic header text update (`getColumnByField` + `refreshHeader`)
- Column templates (custom cell rendering) and `editTemplate`
- Column spanning and frozen columns (`frozenColumns`, inject `Freeze`)

### Column Interactions
📄 **Read:** [references/column-interactions.md](references/column-interactions.md)
- Column resizing (`allowResizing`, inject `Resize`)
  - Restrict with `minWidth` / `maxWidth` per column
  - Prevent resize per column (`allowResizing={false}`)
  - Resize modes: Normal vs Auto (`resizeSettings.mode`)
  - Programmatic resize (`reorderColumns`, `refreshColumns`)
  - Resize events: `resizeStart`, `resizing`, `resizeStop`
- Column reorder (`allowReordering`, inject `Reorder`)
  - Disable reorder per column (`allowReordering={false}`)
  - Programmatic reorder: `reorderColumns`, `reorderColumnByIndex`, `reorderColumnByTargetIndex`
  - Reorder drag events: `columnDragStart`, `columnDrag`, `columnDrop`
- Column menu (`showColumnMenu`, inject `ColumnMenu`)
  - Built-in items: SortAscending, SortDescending, AutoFit, AutoFitAll, ColumnChooser, Filter
  - Custom column menu items + `columnMenuClick` event
  - Disable per column (`showColumnMenu={false}`)
- Toggling column visibility (show/hide columns)

### Rows
📄 **Read:** [references/rows.md](references/rows.md)
- Row drag-and-drop (reorder and reparent tasks)
- Indent and outdent (change task hierarchy)
- Row spanning via `queryCellInfo` event
  - `QueryCellInfoEventArgs` with `rowSpan`, `colSpan`, `cell`, `data`, `column`
  - Horizontal spanning (`colSpan`) and vertical spanning (`rowSpan`)
- Row height configuration
- Row styling via `rowDataBound`
- Expand and collapse rows programmatically

### Managing Tasks
📄 **Read:** [references/managing-tasks.md](references/managing-tasks.md)
- Adding new tasks (toolbar, context menu, programmatic `addRecord()`)
- Editing tasks — dialog edit (`mode: 'Dialog'`), cell edit (`mode: 'Auto'`), taskbar drag
- Deleting tasks (toolbar, `deleteRow()`, `showDeleteConfirmDialog`)
- Taskbar drag editing: move, resize right edge, progress handle, dependency drawing
- Splitting and merging tasks (`taskFields.segments`, `splitTask()`, `mergeTask()`)
- **Cell edit types** (`editType`): `stringedit`, `numericedit`, `datepickeredit`, `datetimepickeredit`, `dropdownedit`, `booleanedit`
  - `edit.params` for min/max/step/format/dataSource per column
- Customizing add/edit dialog fields (`addDialogFields`, `editDialogFields`)
- Server-side CRUD with `UrlAdaptor` (`url` + `batchUrl`)
  - Server receives `added`, `changed`, `deleted` arrays in the batch request body
- Column-level validation rules (`validationRules` on `ColumnDirective`)
  - Built-in rules: `required`, `min`, `max`, `minLength`, `date`, `regex`
  - Custom validator functions (`[fn, 'message']` callback pattern)

### Filtering and Searching
📄 **Read:** [references/filtering-searching.md](references/filtering-searching.md)
- Basic column filtering (`allowFiltering={true}`, inject `Filter`)
- Filter hierarchy modes: `Parent`, `Child`, `Both`, `None`
- Filter menu (string, number, date operators) and Excel-like checklist filter
- Toolbar search box (`searchSettings`: `fields`, `operator`, `ignoreCase`)
- Initial filter state on load (`filterSettings.columns` array)
- Programmatic filter API: `filterByColumn()`, `clearFiltering()`
- Custom multi-column filter predicates

### Sorting
📄 **Read:** [references/sorting.md](references/sorting.md)
- Single-column and multi-column sorting
- Initial sort state (`sortSettings`)
- Custom sort comparers
- Programmatic sorting API

### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- Row selection modes (single, multiple)
- Cell selection
- Keyboard-based selection
- Programmatic selection API (`selectRow`, `selectCell`)

### Taskbar, Labels, and Markers
📄 **Read:** [references/taskbar-labels-markers.md](references/taskbar-labels-markers.md)
- Taskbar template (custom rendering)
- Parent taskbar and milestone customization
- Tooltip settings and templates (`tooltipSettings` for taskbar, connector line, baseline, timeline)
- Disable/hide tooltips for specific UI targets using `beforeTooltipRender`
- Left, right, and task label configuration
- Data markers / indicators
- Event markers (deadlines, holidays on timeline)
- Baseline rendering
- Critical path highlighting

### Resources
📄 **Read:** [references/resources.md](references/resources.md)
- Defining resource collection (`resources` property)
- Assigning resources to tasks (`taskFields.resourceInfo`) — single or multiple with custom units
- Resource view layout (`viewType='ResourceView'`, resource groups)
- Multi-taskbar (`enableMultiTaskbar={true}`) — multiple taskbars per collapsed resource row
- Over-allocation highlighting (`showOverAllocatedTasks={true}`)
- Resource unit and work fields (`resourceFields.unit`, `resourceFields.group`)
- Custom resource taskbar styling via `queryTaskbarInfo`

### Toolbar and Context Menu
📄 **Read:** [references/toolbar-context-menu.md](references/toolbar-context-menu.md)
- Built-in toolbar items: `Add`, `Edit`, `Delete`, `Update`, `Cancel`, `Search`, `ExpandAll`, `CollapseAll`, `Indent`, `Outdent`, `ZoomIn`, `ZoomOut`, `ZoomToFit`, `CriticalPath`, `ExcelExport`, `CsvExport`, `PdfExport`, `ColumnChooser`, `Undo`, `Redo`, `SplitTask`, `MergeTask`
- Required services per toolbar item (e.g. `Undo`/`Redo` → `UndoRedo`, `SplitTask` → `Edit`)
- Custom toolbar buttons (`ItemModel`) and `toolbarClick` handler
- Default context menu items including `SplitTask`, `MergeTask`, `Convert`, `DeleteDependency`
- Custom context menu items, `contextMenuClick`, `contextMenuOpen` (`args.hideItems`)
- Enabling/disabling toolbar items dynamically

### Excel Export
📄 **Read:** [references/excel-export.md](references/excel-export.md)
- Basic Excel export
- Export properties and customization
- Exporting multiple Gantt charts to a single Excel workbook
- Custom data source export

### PDF Export
📄 **Read:** [references/pdf-export.md](references/pdf-export.md)
- Basic PDF export
- Customizing PDF (fonts, columns, styles)
- Header and footer configuration
- Page settings (orientation, size)

### Holidays, Working Time & Timezone
📄 **Read:** [references/holidays-working-time.md](references/holidays-working-time.md)
- Defining holidays (`holidays` prop, `HolidayModel`, `DayMarkers` service)
- Work week configuration (`workWeek`, `includeWeekend`)
- Daily working time (`dayWorkingTime`)
- Effort-based scheduling (`taskFields.work`, `workUnit`, task types: FixedWork / FixedDuration / FixedUnit)
- Timezone support (`timezone` prop, IANA timezone strings)

### Splitter
📄 **Read:** [references/splitter.md](references/splitter.md)
- Position-based split (`splitterSettings.position` — percentage or pixels)
- Column-based split (`splitterSettings.columnIndex`)
- View mode (`splitterSettings.view` — Default / Grid / Chart)
- Programmatic resize (`setSplitterPosition()`)
- Splitter events (`splitterResizeStart`, `splitterResizing`, `splitterResized`)

### Scrolling
📄 **Read:** [references/scrolling.md](references/scrolling.md)
- Setting `width` and `height` for scrollbar control
- Responsive container (`width='100%'`, `height='100%'` with CSS parent height)
- Scroll to a date (`scrollToDate('MM/dd/yyyy')`)
- Set vertical scroll position (`ganttChartModule.scrollObject.setScrollTop(px)`)

### Virtual Scroll
📄 **Read:** [references/virtual-scroll.md](references/virtual-scroll.md)
- Row virtualization (`enableVirtualization={true}`, `VirtualScroll` service)
- Timeline virtualization (`enableTimelineVirtualization={true}`, requires `projectStartDate` / `projectEndDate`)
- Combining row + timeline virtualization
- Accessing filtered record count with virtual scroll (`treeGrid.filterModule.filteredResult`)
- Virtual scroll limitations (browser memory, cell selection, pixel height, expand state)

### Undo / Redo
📄 **Read:** [references/undo-redo.md](references/undo-redo.md)
- Enable undo/redo (`enableUndoRedo`, `UndoRedo` service)
- `undoRedoActions` — full list of trackable actions and required services
- `undoRedoStepsCount` — history stack size
- Toolbar `'Undo'` / `'Redo'` buttons and `Ctrl+Z` / `Ctrl+Y` keyboard shortcuts
- Programmatic `undo()` / `redo()` via component ref

### State Persistence, Immutable Mode & Loading
📄 **Read:** [references/state-persistence.md](references/state-persistence.md)
- State persistence (`enablePersistence={true}`, unique `id` prop, localStorage)
- Resetting persisted state (change `id` or clear localStorage entry)
- Immutable mode (`enableImmutableMode={true}`, requires `isPrimaryKey={true}`)
- Loading animation (`loadingIndicator.indicatorType`: `'Spinner'` or `'Shimmer'`)
- Manual spinner control (`showSpinner()` / `hideSpinner()`)

### Localization and RTL
📄 **Read:** [references/localization-rtl.md](references/localization-rtl.md)
- Setting locale (`locale` prop)
- Loading custom translations (`L10n.load()` with `'gantt'` namespace keys)
- Gantt locale key reference (all translatable UI strings)
- RTL support (`enableRtl={true}`)
- Column date formatting (`format='yMd'`, `format='dd/MM/yyyy'`)
- Column number formatting (`format='C2'`, `format='N2'`, `format='P0'`)

### Programmatic Methods
📄 **Read:** [references/gantt-methods.md](references/gantt-methods.md)
- Column utilities: `autoFitColumns()`
- Edit control: `cancelEdit()`, `openAddDialog()`, `openEditDialog()`
- Task management: `deleteRecord()`, `convertToMilestone()`, `changeTaskMode()`, `updateRecordByID()`, `updateRecordByIndex()`, `updateTaskId()`, `updateDataSource()`, `updateProjectDates()`
- Toolbar control: `enableItems()`
- Expand/Collapse: `expandByIndex()`, `collapseByIndex()`
- Undo/Redo stacks: `clearUndoCollection()`, `clearRedoCollection()`, `getUndoActions()`, `getRedoActions()`
- Data retrieval: `getCurrentViewData()`, `getRecordByID()`, `getTaskByUniqueID()`, `getTaskInfo()`, `getTaskbarHeight()`, `getExpandedRecords()`, `getGanttColumns()`, `getGridColumns()`
- Formatting helpers: `getDurationString()`, `getWorkString()`
- DOM access: `getRowByID()`, `getRowByIndex()`
- Sorting: `removeSortColumn()`
- Selection: `selectCells()`
- Row reorder: `reorderRows()`
- Scrolling: `scrollToTask()`, `updateChartScrollOffset()`

### Events
📄 **Read:** [references/events.md](references/events.md)
- Lifecycle events (`load`, `created`, `dataBound`)
- Task editing events (`actionBegin`, `actionComplete`) with `requestType` reference table
- Taskbar events: `taskbarEditing`, `taskbarEdited`, `taskbarClick`
- Row expand/collapse events: `expanding`, `collapsing`, `expanded`, `collapsed`
- Selection events: `rowSelected`, `rowDeselected`, `cellSelected`, `cellDeselected`
- Export events: `excelExportComplete`, `pdfExportComplete`
- Column interaction events: `resizeStart`, `resizing`, `resizeStop`, `columnDragStart`, `columnDrag`, `columnDrop`
- Event cancellation patterns (`args.cancel = true`)
- **Complete all-events quick reference table** (30+ events)

---

## Quick Start Example

```tsx
import * as React from 'react';
import { GanttComponent, ColumnsDirective, ColumnDirective, Inject, Edit, Toolbar, Selection } from '@syncfusion/ej2-react-gantt';
import { TaskFieldsModel, EditSettingsModel } from '@syncfusion/ej2-gantt';

// In App.css:
// @import "../node_modules/@syncfusion/ej2-gantt/styles/tailwind3.css";
// (plus base, buttons, calendars, dropdowns, grids, inputs, layouts,
//  lists, navigations, notifications, popups, richtexteditor, treegrid)

const data = [
  {
    TaskID: 1, TaskName: 'Project Initiation',
    StartDate: new Date('04/02/2024'), EndDate: new Date('04/21/2024'),
    subtasks: [
      { TaskID: 2, TaskName: 'Identify Site Location', StartDate: new Date('04/02/2024'), Duration: 4, Progress: 50 },
      { TaskID: 3, TaskName: 'Perform Soil Test', StartDate: new Date('04/02/2024'), Duration: 4, Progress: 50, Predecessor: '2' },
      { TaskID: 4, TaskName: 'Soil Test Approval', StartDate: new Date('04/08/2024'), Duration: 0, Predecessor: '3FS', Progress: 50 },
    ]
  }
];

const taskFields: TaskFieldsModel = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  endDate: 'EndDate',
  duration: 'Duration',
  progress: 'Progress',
  dependency: 'Predecessor',
  child: 'subtasks',
};

const editSettings: EditSettingsModel = { allowEditing: true, allowAdding: true, allowDeleting: true, allowTaskbarEditing: true };

function App() {
  return (
    <GanttComponent
      dataSource={data}
      taskFields={taskFields}
      editSettings={editSettings}
      toolbar={['Add', 'Edit', 'Delete', 'Cancel', 'Update', 'Search', 'ZoomIn', 'ZoomOut', 'ZoomToFit']}
      height="450px"
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" width="80" />
        <ColumnDirective field="TaskName" headerText="Task Name" width="250" />
        <ColumnDirective field="StartDate" />
        <ColumnDirective field="Duration" />
        <ColumnDirective field="Progress" />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar, Selection]} />
    </GanttComponent>
  );
}

export default App;
```

---

## Common Patterns

### Enable Editing with Dialog
```tsx
<GanttComponent
  editSettings={{ allowEditing: true, mode: 'Dialog' }}
>
  <Inject services={[Edit]} />
</GanttComponent>
```

### Enable Cell Editing
```tsx
<GanttComponent
  editSettings={{ allowEditing: true, mode: 'Auto' }}
>
  <Inject services={[Edit]} />
</GanttComponent>
```

### Programmatically Add a Task
```tsx
const ganttRef = React.useRef<GanttComponent>(null);

const addTask = () => {
  ganttRef.current?.addRecord({ TaskID: 10, TaskName: 'New Task', Duration: 3 }, 'Below', 1);
};
```

### Export to Excel
```tsx
<GanttComponent toolbar={['ExcelExport']} allowExcelExport={true}>
  <Inject services={[ExcelExport, Toolbar]} />
</GanttComponent>
```

### Export to PDF
```tsx
<GanttComponent toolbar={['PdfExport']} allowPdfExport={true}>
  <Inject services={[PdfExport, Toolbar]} />
</GanttComponent>
```

### Column-Level Validation Rules
```tsx
<ColumnsDirective>
  <ColumnDirective field="TaskName" validationRules={{ required: true }} />
  <ColumnDirective field="Duration"  validationRules={{ min: 1, max: 100 }} />
</ColumnsDirective>
```

### Scroll to Date Programmatically
```tsx
const ganttRef = React.useRef<GanttComponent>(null);

ganttRef.current?.scrollToDate('04/28/2024');
```

### Column Resize with Min/Max Width
```tsx
<ColumnDirective field="TaskName" minWidth="100" maxWidth="400" allowResizing={true} />
```

### Reorder Columns Programmatically
```tsx
const ganttRef = React.useRef<GanttComponent>(null);

// By field names:
(ganttRef.current as any).treeGrid.reorderColumns(['Duration', 'Progress'], 'TaskName');

// By index:
(ganttRef.current as any).treeGrid.reorderColumnByIndex(2, 0);
```

### Persist Tree Expand/Collapse State
```tsx
// In taskFields — map a boolean field that controls initial expand state:
const taskFields = { ..., expandState: 'isExpand' };

// Or collapse all on load:
<GanttComponent collapseAllParentTasks={true} .../>
```

---

## Key Module Injections

| Feature | Service to Inject |
|---------|------------------|
| Editing (add/edit/delete/taskbar drag) | `Edit` |
| Filtering | `Filter` |
| Sorting | `Sort` |
| Toolbar | `Toolbar` |
| Selection | `Selection` |
| Day Markers / Holidays / Event Markers | `DayMarkers` |
| Critical Path | `CriticalPath` |
| Excel / CSV Export | `ExcelExport` |
| PDF Export | `PdfExport` |
| Undo / Redo | `UndoRedo` |
| Column Menu | `ColumnMenu` |
| Context Menu | `ContextMenu` |
| Virtual Scrolling | `VirtualScroll` |
| Row Drag and Drop | `RowDD` |
| Column Reordering | `Reorder` |
| Frozen Columns | `Freeze` |
| Column Resizing | `Resize` |

Usage pattern:
```tsx
import { GanttComponent, Inject, Edit, Filter, Sort, Toolbar, Selection } from '@syncfusion/ej2-react-gantt';

<GanttComponent ...>
  <Inject services={[Edit, Filter, Sort, Toolbar, Selection]} />
</GanttComponent>
```

---

## Key Props Reference

| Prop | Type | Purpose |
|---|---|---|
| `dataSource` | object[] / DataManager | Task data (local or remote via DataManager) |
| `taskFields` | TaskFieldsModel | Field mapping for task properties |
| `editSettings` | EditSettingsModel | Enable add/edit/delete/taskbar editing |
| `toolbar` | string[] | Toolbar items to render |
| `taskMode` | Auto / Manual / Custom | Scheduling mode |
| `resources` | object[] | Resource data collection |
| `resourceFields` | ResourceFieldsModel | Resource field mapping |
| `allowSorting` | boolean | Enable sorting |
| `allowFiltering` | boolean | Enable filtering |
| `allowReordering` | boolean | Enable column reorder |
| `allowResizing` | boolean | Enable column resize |
| `allowExcelExport` | boolean | Enable Excel export |
| `allowPdfExport` | boolean | Enable PDF export |
| `undoRedoActions` | string[] | Actions tracked by undo/redo |
| `timelineSettings` | TimelineSettingsModel | Timeline tiers and unit config |
| `splitterSettings` | SplitterSettingsModel | Grid/chart panel ratio |
| `highlightWeekends` | boolean | Shade weekend columns |
| `holidays` | HolidayModel[] | Mark holiday dates |
| `eventMarkers` | EventMarkerModel[] | Vertical markers on timeline |
| `treeColumnIndex` | number | Column index showing expand/collapse icons |
| `collapseAllParentTasks` | boolean | Collapse all parent rows on initial load |
| `enableWBS` | boolean | Auto-generate WBS codes from task hierarchy |
| `enableAutoWbsUpdate` | boolean | Recalculate WBS codes after CRUD/sort/DnD |
| `frozenColumns` | number | Number of left-pinned (frozen) columns |
| `enableMultiTaskbar` | boolean | Show multiple taskbars per resource row |
| `allowTaskbarOverlap` | boolean | Controls whether multiple taskbars overlap (true, default) or stack with extended row height (false) in resource rows |
| `viewType` | string | `'ProjectView'` or `'ResourceView'` |
| `showColumnMenu` | boolean | Show column-level menu (sort, filter, autofit) |
| `columnMenuItems` | string[] | Restrict which column menu items are shown |
| `showColumnChooser` | boolean | Enable column chooser dialog via toolbar `ColumnChooser` item |
| `allowSelection` | boolean | Enable row/cell selection |
| `selectionSettings` | SelectionSettingsModel | Selection mode (`Row`/`Cell`), type (`Single`/`Multiple`) |
| `gridLines` | string | Grid lines style: `'Both'` \| `'Horizontal'` \| `'Vertical'` \| `'None'` |
| `renderBaseline` | boolean | Show baseline bars alongside actual taskbars |
| `baselineColor` | string | CSS color for baseline bars |
| `enableCriticalPath` | boolean | Highlight critical path tasks and connectors |
| `enableRtl` | boolean | Enable right-to-left layout |
| `locale` | string | Locale code (e.g. `'fr'`, `'de'`, `'ar'`) |
| `allowRowDragAndDrop` | boolean | Enable row drag-and-drop reordering/reparenting |
| `enableImmutableMode` | boolean | Only re-render changed rows on data updates (requires `isPrimaryKey`) |
| `enablePersistence` | boolean | Persist UI state (sort, filter, column widths) to localStorage |
| `loadingIndicator` | object | Loading animation type: `{ indicatorType: 'Spinner' \| 'Shimmer' }` |
| `workWeek` | string[] | Working days, e.g. `['Monday','Tuesday','Wednesday','Thursday','Friday']` |
| `includeWeekend` | boolean | Count weekends as working days for duration calculation |
| `timezone` | string | IANA timezone for the Gantt (e.g. `'America/New_York'`) |
| `showOverAllocatedTasks` | boolean | Highlight over-allocated resources in ResourceView |
| `enableUndoRedo` | boolean | Enable undo/redo tracking (inject `UndoRedo` service) |
| `undoRedoStepsCount` | number | Maximum undo/redo history steps (default: 10) |
| `enableVirtualization` | boolean | Row virtualization for large data sets |
| `enableTimelineVirtualization` | boolean | Timeline (horizontal) virtualization |
| `rowHeight` | number | Uniform row height in pixels |
| `taskbarHeight` | number | Height of taskbars in pixels (must be ≤ `rowHeight`) |
| `connectorLineWidth` | number | Width of dependency connector lines |
| `connectorLineBackground` | string | Color of dependency connector lines |
