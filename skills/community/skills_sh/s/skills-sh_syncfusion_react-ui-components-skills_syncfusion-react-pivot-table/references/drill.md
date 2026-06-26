# Drilling and Editing Operations

## Table of Contents
- [Drill-Down and Drill-Up](#drill-down-and-drill-up)
- [Drill-Through](#drill-through)
- [Cell Editing](#cell-editing)
- [Events & Customization](#events--customization)
- [Properties Reference](#properties-reference)

## Drill-Down and Drill-Up

### Overview

The drill-down and drill-up features allow users to expand or collapse hierarchical data for detailed or summarized views. When a field member contains child items, expand and collapse icons automatically appear in the corresponding row or column header. This feature is built-in and works automatically, making the pivot table faster and more efficient.

### Drill Position

The drill-down and drill-up features allow you to expand or collapse data for a specific member without affecting the same member in other positions. For example, if both "FY 2015" and "FY 2016" have "Quarter 1" as a child, drilling down into "Quarter 1" under "FY 2015" expands only that specific instance.

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function DrillDownExample() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }, { name: 'Products' }],
    dataSource: pivotData as IDataSet[],
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    showSubTotals: false,
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };

  return (
    <PivotViewComponent
      height={350}
      id='PivotView'
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default DrillDownExample;
```

### Expand All Members

Display all hierarchical members in an expanded state by setting the `expandAll` property to **true**:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
  dataSource: pivotData as IDataSet[],
  expandAll: true,  // ← Expands all members by default
  filters: [],
  formatSettings: [{ name: 'Amount', format: 'C0' }],
  rows: [{ name: 'Country' }, { name: 'Products' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
};
```

> **Note:** The `expandAll` property is applicable only for relational data sources.

### Expand Specific Fields

Expand all headers for specific fields using the `expandAll` property in individual field configurations:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
  dataSource: pivotData as IDataSet[],
  expandAll: false,  // ← Default: collapsed
  filters: [],
  rows: [
    { name: 'Country', expandAll: true },  // ← Only Country expanded
    { name: 'Products' }
  ],
  columns: [
    { name: 'Year', expandAll: true }      // ← Only Year expanded
  ],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
};
```

### Expand All Except Specific Members

Expand all members while keeping specific ones collapsed using `drilledMembers`:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
  dataSource: pivotData as IDataSet[],
  expandAll: true,
  drilledMembers: [
    { name: 'Country', items: ['France'] }  // ← France stays collapsed
  ],
  filters: [],
  rows: [{ name: 'Country' }, { name: 'Products' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
};
```

### Expand or Collapse Specific Members

Control which specific members are expanded using the `drilledMembers` property with the `delimiter` property for hierarchical member specification:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: pivotData as IDataSet[],
  expandAll: false,
  drilledMembers: [
    { name: 'Year', items: ['FY 2015', 'FY 2016'] },
    { 
      name: 'Quarter', 
      delimiter: '~~',
      items: ['FY 2015~~Q1']  // ← Expand Q1 only under FY 2015
    }
  ],
  rows: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }, { name: 'Products' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
  columns: [{ name: 'Country' }],
  filters: []
};
```

## Drill-Through

### Overview

The drill-through feature allows users to view the raw, unaggregated data behind any aggregated cell in the Pivot Table. By double-clicking an aggregated cell, users can view its detailed raw data in a data grid displayed in a new window.

**Key Features:**
- View raw, underlying data for aggregated cells
- Display shows row header, column header, and measure name
- Column chooser allows including/excluding fields
- Works with Pivot Table cells and Pivot Chart data points
- Supports maximum row limit configuration

### Enabling Drill-Through

Enable drill-through by setting the `allowDrillThrough` property to **true** and injecting the `DrillThrough` module:

```typescript
import { DrillThrough, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function DrillThroughExample() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
      allowDrillThrough={true}  // ← Enable drill-through
    >
      <Inject services={[DrillThrough]} />  {/* ← Inject module */}
    </PivotViewComponent>
  );
}

export default DrillThroughExample;
```

### Drill-Through with Pivot Chart

Access drill-through data through pivot chart by clicking on any data point:

```typescript
import { DrillThrough, IDataSet, PivotViewComponent, Inject, DisplayOption, PivotChart } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { ChartSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/chartSettings';
import * as React from 'react';
import { pivotData } from './datasource';

function DrillThroughChartExample() {
  const displayOption: DisplayOption = {
    view: 'Chart'
  };

  const chartSettings: ChartSettings = {
    chartSeries: { type: 'Column' }
  };

  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      allowDrillThrough={true}
      chartSettings={chartSettings}
      displayOption={displayOption}
      dataSourceSettings={dataSourceSettings}
    >
      <Inject services={[PivotChart, DrillThrough]} />
    </PivotViewComponent>
  );
}

export default DrillThroughChartExample;
```

### Maximum Rows in Drill-Through

Control the maximum number of rows returned during drill-through using the `maxRowsInDrillThrough` property (default: 10,000):

```typescript
<PivotViewComponent
  id='PivotView'
  dataSourceSettings={dataSourceSettings}
  allowDrillThrough={true}
  maxRowsInDrillThrough={10}  // ← Limit to 10 rows per drill-through
>
  <Inject services={[DrillThrough]} />
</PivotViewComponent>
```

> **Note:** The `maxRowsInDrillThrough` property is applicable primarily for OLAP data sources.

## Cell Editing

### Overview

The cell editing option allows users to directly change data in the pivot table by adding, updating, or deleting raw data items within any value cell. When you double-click a value cell, the raw items appear in a data grid within a new window. In this data grid, you can perform CRUD operations. After finishing the edits, the pivot table automatically updates the aggregated values.

**Requirements:**
- Applicable only for relational data sources
- Set the `allowEditing` property in `editSettings` to **true**

### Editing Properties

The `editSettings` property provides comprehensive control through:

| Property | Description |
|----------|-------------|
| `allowAdding` | Enables adding new rows to the data grid |
| `allowEditing` | Allows editing existing records in the data grid |
| `allowDeleting` | Enables deleting records from the data grid |
| `allowCommandColumns` | Displays built-in command buttons (edit, delete, save, cancel) |
| `mode` | Sets the editing mode (Normal, Dialog, Batch) |
| `allowEditOnDblClick` | Enables cell editing by double-clicking |
| `showConfirmDialog` | Shows confirmation dialog before saving changes |
| `showDeleteConfirmDialog` | Shows confirmation dialog before deleting records |
| `allowInlineEditing` | Allows editing content directly in the cell |

### Normal Edit Mode

Normal edit mode allows users to edit one row at a time in the editing dialog:

```typescript
import { CellEditSettings, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function NormalEditExample() {
  const editSettings: CellEditSettings = {
    allowAdding: true, 
    allowDeleting: true, 
    allowEditing: true, 
    mode: 'Normal'
  } as CellEditSettings;

  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
      editSettings={editSettings}
    />
  );
}

export default NormalEditExample;
```

### Dialog Edit Mode

Dialog edit mode displays the selected row data in an exclusive dialog window:

```typescript
const editSettings: CellEditSettings = {
  allowAdding: true, 
  allowDeleting: true, 
  allowEditing: true, 
  mode: 'Dialog'
} as CellEditSettings;

// Use in PivotViewComponent
<PivotViewComponent
  id='PivotView'
  height={350}
  dataSourceSettings={dataSourceSettings}
  editSettings={editSettings}
/>
```

### Batch Edit Mode

Batch editing enables users to make multiple changes and save them all at once:

```typescript
const editSettings: CellEditSettings = {
  allowAdding: true, 
  allowDeleting: true, 
  allowEditing: true, 
  mode: 'Batch'
} as CellEditSettings;

// Use in PivotViewComponent
<PivotViewComponent
  id='PivotView'
  height={350}
  dataSourceSettings={dataSourceSettings}
  editSettings={editSettings}
/>
```

### Command Column

Enable command columns for dedicated action buttons in each row:

```typescript
const editSettings: CellEditSettings = {
  allowAdding: true, 
  allowDeleting: true, 
  allowEditing: true, 
  allowCommandColumns: true
} as CellEditSettings;

// Available command buttons: Edit, Delete, Save, Cancel

// Use in PivotViewComponent
<PivotViewComponent
  id='PivotView'
  height={350}
  dataSourceSettings={dataSourceSettings}
  editSettings={editSettings}
/>
```

> **Note:** When command columns are enabled, Edit, Delete, Update, and Cancel buttons are not shown in the toolbar. These action buttons appear in the last column of each row.

## Events & Customization

### drill Event

The `drill` event is triggered each time a field member is expanded or collapsed:

```typescript
import { IDataSet, PivotViewComponent, DrillArgs } from '@syncfusion/ej2-react-pivotview';
import * as React from 'react';

function DrillEventExample() {
  const handleDrill = (args: DrillArgs) => {
    // args.drillInfo contains drill information
    // Customize behavior
    args.dataSourceSettings.columns[0].caption = "Custom Caption";
    args.dataSourceSettings.expandAll = true;
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      drill={handleDrill}
      height={350}
    />
  );
}

export default DrillEventExample;
```

### drillThrough Event

The `drillThrough` event is triggered immediately after a user double-clicks a value cell:

```typescript
function DrillThroughEventExample() {
  const handleDrillThrough = (args: DrillThroughEventArgs) => {
    // Access drill-through details
    // args.columnHeaders - column header of clicked cell
    // args.rowHeaders - row header of clicked cell
    // args.value - value of clicked cell
    // args.rawData - raw unaggregated data
    // args.gridColumns - columns to display in data grid
    // args.cancel - set true to prevent dialog
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      allowDrillThrough={true}
      drillThrough={handleDrillThrough}
    >
      <Inject services={[DrillThrough]} />
    </PivotViewComponent>
  );
}

export default DrillThroughEventExample;
```

### beginDrillThrough Event

The `beginDrillThrough` event triggers after the data grid is initialized in the drill-through popup, allowing you to customize the grid with sorting, filtering, and grouping:

```typescript
function BeginDrillThroughExample() {
  const handleBeginDrillThrough = (args: BeginDrillThroughEventArgs) => {
    // args.gridObj - data grid instance
    // args.cellInfo - clicked cell details (rawData, rowHeaders, columnHeaders, value)
    
    // Enable sorting, filtering, grouping in the grid
    // Inject Sort, Filter, Group services to grid as needed
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      allowDrillThrough={true}
      beginDrillThrough={handleBeginDrillThrough}
    >
      <Inject services={[DrillThrough]} />
    </PivotViewComponent>
  );
}

export default BeginDrillThroughExample;
```

## Properties Reference

### Drill-Down/Up Properties

| Property | Type | Description |
|----------|------|-------------|
| `expandAll` | boolean | Expands or collapses all hierarchical members (default: false) |
| `drilledMembers` | DrillOptions[] | Specifies members that should be expanded or collapsed |
| `drilledMembers.name` | string | Field name whose members are being configured |
| `drilledMembers.items` | string[] | Specific member names to expand/collapse |
| `drilledMembers.delimiter` | string | Separator for hierarchical member names (e.g., '~~') |

### Drill-Through Properties

| Property | Type | Description |
|----------|------|-------------|
| `allowDrillThrough` | boolean | Enables drill-through feature (default: false) |
| `maxRowsInDrillThrough` | number | Maximum number of rows to return (default: 10000) |
| `drillThrough` | event | Triggered when drill-through is initiated |
| `beginDrillThrough` | event | Triggered when data grid is initialized in popup |

### Edit Settings Properties

| Property | Type | Description |
|----------|------|-------------|
| `allowAdding` | boolean | Enables adding new rows |
| `allowEditing` | boolean | Allows editing existing records |
| `allowDeleting` | boolean | Enables deleting records |
| `allowCommandColumns` | boolean | Displays command action buttons |
| `mode` | string | Edit mode: 'Normal' \| 'Dialog' \| 'Batch' |
| `allowEditOnDblClick` | boolean | Allows editing by double-clicking |
| `showConfirmDialog` | boolean | Shows confirmation before saving |
| `showDeleteConfirmDialog` | boolean | Shows confirmation before deleting |
