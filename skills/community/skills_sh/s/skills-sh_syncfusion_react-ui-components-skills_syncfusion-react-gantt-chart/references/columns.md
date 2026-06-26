# Columns in Syncfusion React Gantt Chart

## Table of Contents
- [Column Types](#column-types)
- [Defining Columns](#defining-columns)
- [Auto-Generated Columns](#auto-generated-columns)
- [Column Rendering with valueAccessor](#column-rendering-with-valueaccessor)
- [Expression Column](#expression-column)
- [Display Serial Numbers](#display-serial-numbers)
- [Tree Column](#tree-column)
- [WBS (Work Breakdown Structure) Column](#wbs-work-breakdown-structure-column)
- [Column Headers and Formatting](#column-headers-and-formatting)
- [Column Templates (Custom Cell Rendering)](#column-templates-custom-cell-rendering)
- [Column Spanning](#column-spanning)
- [Frozen (Pinned) Columns](#frozen-pinned-columns)
- [Showing and Hiding Columns](#showing-and-hiding-columns)

---

## Column Types

Each column can have an explicit `type` for correct rendering and formatting:

| Type | Use Case |
|---|---|
| `string` | Default; text values |
| `number` | Numeric values with optional format |
| `boolean` | Renders as checkbox |
| `date` | Date values |
| `datetime` | Date + time values |
| `checkbox` | Checkbox selection column |

```tsx
<ColumnDirective field="TaskID"    type="number"   width="80" />
<ColumnDirective field="TaskName"  type="string"   width="250" />
<ColumnDirective field="StartDate" type="date"     format="yMd" />
<ColumnDirective field="Verified"  type="boolean"  width="100" />
<ColumnDirective                   type="checkbox" width="50" />  {/* selection column */}
```

---

## Defining Columns

Use `ColumnsDirective` + `ColumnDirective` to declare columns declaratively:

```tsx
import {
  GanttComponent, ColumnsDirective, ColumnDirective
} from '@syncfusion/ej2-react-gantt';

function App() {
  return (
    <GanttComponent dataSource={data} taskFields={taskFields} height="450px">
      <ColumnsDirective>
        <ColumnDirective field="TaskID"    headerText="ID"        width="80"  textAlign="Right" />
        <ColumnDirective field="TaskName"  headerText="Task Name" width="250" clipMode="EllipsisWithTooltip" />
        <ColumnDirective field="StartDate" headerText="Start"     width="130" format="yMd" />
        <ColumnDirective field="Duration"  headerText="Duration"  width="100" />
        <ColumnDirective field="Progress"  headerText="Progress"  width="100" />
      </ColumnsDirective>
    </GanttComponent>
  );
}
```

### Key ColumnDirective Props

| Prop | Type | Purpose |
|---|---|---|
| `field` | string | Maps to data source field |
| `headerText` | string | Column header label |
| `width` | string / number | Column width (px or %) |
| `textAlign` | Left / Right / Center | Cell alignment |
| `format` | string | Date/number format (e.g., `"yMd"`, `"C2"`) |
| `type` | string | Data type |
| `visible` | boolean | Show/hide column |
| `allowEditing` | boolean | Enable cell editing for this column |
| `isPrimaryKey` | boolean | Mark as primary key |
| `clipMode` | Clip / Ellipsis / EllipsisWithTooltip | Overflow behavior |
| `template` | ReactElement | Custom cell renderer |

---

## Auto-Generated Columns

If `ColumnsDirective` is omitted (or the `columns` prop is empty/undefined), the Gantt automatically creates one column for every field in the data source:

```tsx
// No <ColumnsDirective> → all data source fields become columns automatically
<GanttComponent
  dataSource={data}
  taskFields={taskFields}
  treeColumnIndex={1}
  height="450px"
/>
```

This is useful for quick prototyping. For production use, define columns explicitly for full control over order, width, and formatting.

---

## Column Rendering with valueAccessor

The `valueAccessor` property accepts a `(field, data) => value` function that returns a custom display string for a cell — without affecting the underlying data:

```tsx
import { getValue } from '@syncfusion/ej2-base';

// Append "%" to Progress values
const percentageFormatter = (field: string, data: any) => `${data[field]}%`;

// Combine TaskName with TaskID
const concatenateFields = (field: string, data: any) =>
  `${data[field]} - ${getValue('TaskID', data)}`;

<GanttComponent dataSource={data} taskFields={taskFields} height="450px">
  <ColumnsDirective>
    <ColumnDirective field="TaskID" />
    <ColumnDirective field="TaskName"  width="180" valueAccessor={concatenateFields} />
    <ColumnDirective field="StartDate" width="180" />
    <ColumnDirective field="Duration"  width="100" />
    <ColumnDirective field="Progress"  width="120" valueAccessor={percentageFormatter} />
  </ColumnsDirective>
</GanttComponent>
```

> **Note:** Columns with custom `valueAccessor` display computed values — sorting and filtering operate on the raw field value, not the formatted string.

### Display Array-Type Column Values

When a field contains an array of objects, use `valueAccessor` to flatten or join them:

```tsx
const resourceNames = (field: string, data: any) =>
  Array.isArray(data[field])
    ? data[field].map((r: any) => r.resourceName).join(', ')
    : '';

<ColumnDirective field="resources" headerText="Resources" valueAccessor={resourceNames} />
```

---

## Expression Column

Calculate a derived value from multiple fields using `valueAccessor`:

```tsx
// Total Price = Units × Unit Price
const totalPrice = (field: string, data: any) =>
  Number(data.Units) * Number(data.UnitPrice);

<GanttComponent dataSource={data} taskFields={taskFields} height="450px">
  <ColumnsDirective>
    <ColumnDirective field="TaskID"     headerText="Task ID"    width="100" />
    <ColumnDirective field="TaskName"   headerText="Task Name"  width="250" />
    <ColumnDirective field="Units"      headerText="Units"      width="100" textAlign="Right" />
    <ColumnDirective field="UnitPrice"  headerText="Unit Price" width="120" textAlign="Right" />
    <ColumnDirective
      field="TotalPrice"
      headerText="Total Price"
      width="120"
      format="c2"
      type="number"
      textAlign="Right"
      valueAccessor={totalPrice}
    />
  </ColumnsDirective>
</GanttComponent>
```

> Sorting and filtering are not supported on expression columns because the displayed value is computed client-side.

---

## Display Serial Numbers

Use `rowDataBound` to write sequential row numbers into a dedicated column cell:

```tsx
function rowDataBound(args: any) {
  const row = args.row;
  if (row) {
    const rowIndex = parseInt(row.getAttribute('aria-rowindex') || '0', 10);
    const cells = row.querySelectorAll('.e-rowcell');
    if (cells.length > 0) {
      cells[0].textContent = rowIndex.toString();
    }
  }
}

<GanttComponent
  dataSource={data}
  taskFields={taskFields}
  treeColumnIndex={1}
  rowDataBound={rowDataBound}
  height="450px"
>
  <ColumnsDirective>
    <ColumnDirective field="SNo"      headerText="S.No"      width="80" />
    <ColumnDirective field="TaskName" headerText="Task Name" width="250" />
    <ColumnDirective field="StartDate" />
    <ColumnDirective field="Duration" />
    <ColumnDirective field="Progress" />
  </ColumnsDirective>
</GanttComponent>
```

> Serial number columns do not support sorting or filtering because the value is injected via the DOM after data binding.

---

## Tree Column

The tree column shows the hierarchical expand/collapse icons. By default it's the first column (`treeColumnIndex={0}`). Change it with `treeColumnIndex`:

```tsx
<GanttComponent
  treeColumnIndex={1}   // TaskName column (index 1) becomes the tree column
  ...
/>
```

### Customize Expand/Collapse Icons

Override the default CSS to use custom icons on the tree column:

```css
.e-gantt .e-grid .e-treegridexpand::before {
  content: "\2795";   /* ➕ */
}
.e-gantt .e-grid .e-treegridcollapse::before {
  content: "\2796";   /* ➖ */
}
```

### Customize Indentation of Tree Column Text

Use `queryCellInfo` to apply custom CSS classes for indentation styling on tree column cells:

```tsx
const queryCellInfo = (args: any): void => {
  const rowData = args.data;
  const columnIndex = args.column.index;
  const treeColumnIndex = ganttRef.current?.treeColumnIndex;
  // Add custom indentation class only to leaf rows in the tree column
  if (!rowData.hasChildRecords && columnIndex === treeColumnIndex) {
    args.cell.classList.add('custom-indent');
  }
};

<GanttComponent queryCellInfo={queryCellInfo} treeColumnIndex={1} ...>
```

### Render Parent Rows in Collapsed State

Collapse all parent rows on initial load using `collapseAllParentTasks`:

```tsx
<GanttComponent
  collapseAllParentTasks={true}
  ...
/>
```

### Retain Expand/Collapse State per Row

Use `taskFields.expandState` to map a data field that controls whether each row starts expanded or collapsed:

```tsx
const taskFields = {
  id: 'TaskID',
  name: 'TaskName',
  // ...
  expandState: 'isExpand',  // boolean field in your data — true = expanded, false = collapsed
  parentID: 'ParentID',
};
```

Data example:
```ts
{ TaskID: 1, TaskName: 'Planning', isExpand: false }  // starts collapsed
{ TaskID: 2, TaskName: 'Design',   isExpand: true  }  // starts expanded
```

### Persist Expand/Collapse State via localStorage

Use the `collapsed`/`expanded` events + `dataBound` to save and restore row states across page refreshes:

```tsx
import { GanttComponent, CollapsingEventArgs } from '@syncfusion/ej2-react-gantt';

const ganttRef = React.useRef<GanttComponent>(null);
const collapsingData: number[] = [];

const onDataBound = (): void => {
  if (ganttRef.current?.treeGrid.initialRender && window.localStorage) {
    const stored = JSON.parse(localStorage.getItem('collapsingData') || '[]');
    stored.forEach((key: number) => {
      ganttRef.current?.treeGrid.collapseByKey(key);
    });
  }
};

const onCollapsed = (args: CollapsingEventArgs): void => {
  collapsingData.push((args.data as any).TaskID);
  localStorage.setItem('collapsingData', JSON.stringify(collapsingData));
};

const onExpanded = (args: CollapsingEventArgs): void => {
  const i = collapsingData.findIndex(id => id === (args.data as any).TaskID);
  if (i !== -1) {
    collapsingData.splice(i, 1);
    localStorage.setItem('collapsingData', JSON.stringify(collapsingData));
  }
};

<GanttComponent
  ref={ganttRef}
  dataBound={onDataBound}
  collapsed={onCollapsed}
  expanded={onExpanded}
  ...
/>
```

**Events used:**

| Event | Trigger | Use |
|---|---|---|
| `dataBound` | After data renders | Restore collapsed state from storage |
| `collapsed` | Row collapses | Save collapsed row ID to storage |
| `expanded` | Row expands | Remove row ID from storage |

---

## WBS (Work Breakdown Structure) Column

WBS displays hierarchical numbering (e.g., 1, 1.1, 1.1.1) to identify tasks.

### Enable WBS with `enableWBS`

Set `enableWBS={true}` to automatically generate unique WBS codes for each task based on hierarchy, and `enableAutoWbsUpdate={true}` to keep codes accurate after operations like sorting, editing, or drag-and-drop:

```tsx
import {
  GanttComponent, ColumnsDirective, ColumnDirective, Inject,
  Selection, Toolbar, Edit, Filter, Sort, DayMarkers
} from '@syncfusion/ej2-react-gantt';

const taskFields = {
  id: 'TaskID',
  name: 'TaskName',
  startDate: 'StartDate',
  endDate: 'EndDate',
  duration: 'Duration',
  progress: 'Progress',
  dependency: 'Predecessor',
  parentID: 'ParentID',
};

function App() {
  return (
    <GanttComponent
      dataSource={WBSData}
      taskFields={taskFields}
      enableWBS={true}            // auto-generate WBS codes from hierarchy
      enableAutoWbsUpdate={true}  // recalculate codes after edits/sorting/DnD
      treeColumnIndex={2}
      height="550px"
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID"          visible={false} />
        <ColumnDirective field="WBSCode"         width="150px" />
        <ColumnDirective field="TaskName"        headerText="Task Name" width="260px" />
        <ColumnDirective field="StartDate"       headerText="Start Date" width="140px" />
        <ColumnDirective field="WBSPredecessor"  headerText="WBS Predecessor" width="190px" />
        <ColumnDirective field="Duration"        headerText="Duration" width="130px" />
        <ColumnDirective field="Progress"        headerText="Progress" />
      </ColumnsDirective>
      <Inject services={[Selection, Toolbar, Edit, Filter, Sort, DayMarkers]} />
    </GanttComponent>
  );
}
```

**Key WBS APIs:**

| Property | Type | Description |
|---|---|---|
| `enableWBS` | `boolean` | Auto-generates WBS codes from task hierarchy |
| `enableAutoWbsUpdate` | `boolean` | Recalculates WBS codes after CRUD, sort, DnD |
| `WBSCode` field | column field | Displays the auto-calculated WBS code |
| `WBSPredecessor` field | column field | Shows WBS-based predecessor codes |

### Manual WBS with `wbsPredecessor` in taskFields

Use `taskFields.wbsPredecessor` when your data has pre-defined WBS codes:

```tsx
const taskFields = {
  id: 'TaskID',
  name: 'TaskName',
  wbsPredecessor: 'WBSCode',  // map if your data has pre-defined WBS codes
};

// Also add the WBS column:
<ColumnDirective field="WBSCode" headerText="WBS" width="120" />
```

> **Note:** Gantt calculates WBS codes automatically based on tree structure depth when `enableWBS` is true. No manual data mapping is needed in that case.

---

## Column Headers and Formatting

### Date Formatting

```tsx
<ColumnDirective field="StartDate" format="yMd"         />  {/* locale-aware */}
<ColumnDirective field="StartDate" format="dd/MM/yyyy"  />  {/* custom pattern */}
<ColumnDirective field="StartDate" format={{ type: 'date', skeleton: 'full' }} />
```

### Number Formatting

```tsx
<ColumnDirective field="Cost"     format="C2"  />  {/* currency 2 decimals */}
<ColumnDirective field="Progress" format="P2"  />  {/* percentage 2 decimals */}
<ColumnDirective field="Rate"     format="N2"  />  {/* number 2 decimals */}
```

### Header Text Alignment

```tsx
<ColumnDirective field="TaskName" headerTextAlign="Center" textAlign="Left" />
```

Programmatic alignment change (affects all columns):

```tsx
const ganttRef = React.useRef<GanttComponent>(null);

function changeAllHeaderAlignment(align: string) {
  (ganttRef.current as any).treeGrid.grid.columns.forEach((col: any) => {
    col.headerTextAlign = align;  // 'Left' | 'Center' | 'Right' | 'Justify'
  });
  (ganttRef.current as any).treeGrid.grid.refreshHeader();
}
```

### Header Template

Render custom React elements inside column headers using `headerTemplate`:

```tsx
const headerTemplate = (props: any) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
    <img src={`${props.field}.png`} style={{ height: 20 }} />
    <span>{props.field}</span>
  </div>
);

<ColumnDirective
  field="TaskName"
  headerText="Task Name"
  headerTemplate={headerTemplate}
/>
```

> `headerTemplate` takes precedence over `headerText`. Use it for icon-augmented or rich headers.

### Header Text Wrapping

Enable text wrapping on long column headers so they wrap at word boundaries:

```tsx
// Control via treeGrid instance after load
function load() {
  (ganttRef.current as any).treeGrid.allowTextWrap = true;
  (ganttRef.current as any).treeGrid.textWrapSettings = { wrapMode: 'Header' };
  // wrapMode: 'Header' | 'Content' | 'Both'
}

<GanttComponent ref={ganttRef} load={load} .../>
```

### Dynamic Header Text Update

Update column header text at runtime using `getColumnByField` + `refreshHeader`:

```tsx
const ganttRef = React.useRef<GanttComponent>(null);

function renameHeader(field: string, newText: string) {
  const col = (ganttRef.current as any).treeGrid.grid.getColumnByField(field);
  if (col) {
    col.headerText = newText;
    (ganttRef.current as any).treeGrid.grid.refreshHeader();
  }
}
```

**Useful column/header lookup methods:**

| Method | Returns |
|---|---|
| `getColumnByField(field)` | Column object by field name |
| `getColumnHeaderByField(field)` | Header DOM element by field name |
| `getColumnIndexByField(field)` | Column index by field name |
| `getColumnByUid(uid)` | Column object by UID |
| `getColumnHeaderByIndex(index)` | Header DOM element by index |

---

## Column Templates (Custom Cell Rendering)

Render custom React elements inside cells:

```tsx
// Progress bar template
const progressTemplate = (props: any) => {
  return (
    <div style={{ background: '#e0e0e0', borderRadius: 4, height: 10 }}>
      <div
        style={{
          width: `${props.Progress}%`,
          background: '#4caf50',
          height: 10,
          borderRadius: 4,
        }}
      />
    </div>
  );
};

<ColumnDirective
  field="Progress"
  headerText="Progress"
  width="150"
  template={progressTemplate}
/>
```

### Edit Cell Template

For custom editing input inside a cell:

```tsx
const editTemplate = (props: any) => (
  <input
    type="number"
    min={0} max={100}
    defaultValue={props.Progress}
    className="e-input"
  />
);

<ColumnDirective
  field="Progress"
  template={progressTemplate}
  editTemplate={editTemplate}
/>
```

---

## Column Spanning

Make a cell span across multiple columns using `colSpanAttributes` on `ColumnDirective`:

```tsx
// Row spanning: set colSpan per-row in rowDataBound or via custom attributes
```

Or use `columns.customAttributes` with a span value. For header spanning, use `headerTemplate`:

```tsx
// Group columns under a common header using stacked headers:
const stackedColumns = [
  {
    headerText: 'Schedule',
    columns: [
      { field: 'StartDate', headerText: 'Start', width: 130 },
      { field: 'EndDate',   headerText: 'End',   width: 130 },
    ],
  },
];
```

---

## Frozen (Pinned) Columns

Pin the first N columns so they remain visible while scrolling horizontally:

```tsx
import { Freeze } from '@syncfusion/ej2-react-gantt';

<GanttComponent
  frozenColumns={2}   // first 2 columns are frozen
  ...
>
  <Inject services={[Freeze]} />
</GanttComponent>
```

> Inject the `Freeze` module to enable frozen columns.

---

## Showing and Hiding Columns

**Declarative (initial state):**
```tsx
<ColumnDirective field="Notes" visible={false} />  {/* hidden by default */}
```

**Programmatic toggle:**
```tsx
const ganttRef = React.useRef<GanttComponent>(null);

ganttRef.current?.showColumn(['TaskID', 'Notes']);   // show by headerText
ganttRef.current?.hideColumn(['Notes']);             // hide by headerText
```
