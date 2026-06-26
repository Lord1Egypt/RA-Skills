# Editing Reference - React Pivot Table

## Overview

The cell editing feature in the Syncfusion React Pivot Table component allows users to directly modify data by adding, updating, or deleting raw data items within value cells. This feature is applicable only for relational data sources.

When a user double-clicks a value cell, the underlying raw items are displayed in a data grid within a new window. Users can perform CRUD (Create, Read, Update, Delete) operations by double-clicking cells or using toolbar options. After editing, the pivot table automatically updates the aggregated values.

## Enabling Editing

Editing is enabled through the `editSettings` property. The basic configuration requires setting `allowEditing` to **true**:

```typescript
import { CellEditSettings, IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';

let editSettings: CellEditSettings = {
  allowEditing: true
} as CellEditSettings;
```

## Edit Settings Properties

The `editSettings` property provides comprehensive control over editing behavior through the following options:

### Core Properties

| Property | Type | Description |
|----------|------|-------------|
| `allowEditing` | boolean | Enables editing existing records in the data grid |
| `allowAdding` | boolean | Enables adding new rows to the data grid |
| `allowDeleting` | boolean | Enables deleting records from the data grid |
| `allowCommandColumns` | boolean | Displays built-in command buttons (edit, delete, save, cancel) in the data grid |
| `mode` | string | Sets the editing mode: 'Normal', 'Dialog', 'Batch' |
| `allowEditOnDblClick` | boolean | Enables users to start editing a cell by double-clicking it |
| `showConfirmDialog` | boolean | Shows a confirmation dialog before saving changes |
| `showDeleteConfirmDialog` | boolean | Shows a confirmation dialog before deleting a record |
| `allowInlineEditing` | boolean | Allows users to edit content directly in the value cell |

## Edit Modes

### Normal Mode

Normal edit mode allows users to edit one row at a time in an editing dialog with simple data changes and updates. When editing begins, the selected row changes to edit state. Cell values can be modified and saved by clicking the "Update" toolbar button.

**Normal** is the default mode for editing.

**Example:**

```typescript
import { CellEditSettings, IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let editSettings: CellEditSettings = {
    allowAdding: true, 
    allowDeleting: true, 
    allowEditing: true, 
    mode: 'Normal'
  } as CellEditSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent 
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      editSettings={editSettings}>
    </PivotViewComponent>
  );
}

export default App;
```

### Dialog Mode

Dialog edit mode provides a focused editing environment by displaying the selected row data in an exclusive dialog window. This ensures clear visibility and controlled data modification. Cell values can be modified and saved by clicking the "Save" button in the dialog.

**Example:**

```typescript
import { CellEditSettings, IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let editSettings: CellEditSettings = {
    allowAdding: true, 
    allowDeleting: true, 
    allowEditing: true, 
    mode: 'Dialog'
  } as CellEditSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent 
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      editSettings={editSettings}>
    </PivotViewComponent>
  );
}

export default App;
```

### Batch Mode

Batch editing enables users to make multiple changes to data grid cells and save them all at once, improving efficiency for bulk updates. When a user double-clicks any data grid cell, the target cell changes to edit state. Users can perform multiple changes and save all modifications (added, changed, and deleted data) by clicking the **Update** toolbar button.

**Example:**

```typescript
import { CellEditSettings, IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let editSettings: CellEditSettings = {
    allowAdding: true, 
    allowDeleting: true, 
    allowEditing: true, 
    mode: 'Batch'
  } as CellEditSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent 
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      editSettings={editSettings}>
    </PivotViewComponent>
  );
}

export default App;
```

### Command Column Mode

The command column option provides dedicated action buttons within the data grid for streamlined CRUD operations. An additional column appears in the data grid layout containing command buttons to perform operations.

When command column is enabled, the Edit, Delete, Update, and Cancel buttons are not shown in the toolbar. Instead, these action buttons appear in the last column of each row within the data grid.

**Available Command Buttons:**

| Command Button | Action |
|----------------|--------|
| Edit | Edit the current row |
| Delete | Delete the current row |
| Save | Update the edited row |
| Cancel | Cancel the edited state |

**Important:** To delete a record directly using the Delete button in the command column, you need to set `allowDeleting` to **true**.

**Example:**

```typescript
import { CellEditSettings, IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let editSettings: CellEditSettings = {
    allowAdding: true, 
    allowDeleting: true, 
    allowEditing: true, 
    allowCommandColumns: true
  } as CellEditSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent 
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      editSettings={editSettings}>
    </PivotViewComponent>
  );
}

export default App;
```

## Inline Editing

The inline editing option provides streamlined data modification by allowing direct editing of value cells without opening an external dialog. This improves workflow efficiency for quick data updates.

This editing mode applies only when a single raw data item corresponds to the value of the cell and works with all editing modes including normal, batch, dialog, and command columns.

**Example:**

```typescript
import { CellEditSettings, IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivot_flatdata } from './datasource';

function App() {
  let editSettings: CellEditSettings = {
    allowEditing: true, 
    allowInlineEditing: true
  } as CellEditSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivot_flatdata as IDataSet[],
    expandAll: true,
    rows: [{ name: 'Country'}],
    columns: [{ name: 'Date' }, { name: 'Product' }],
    values: [
      { name: 'Quantity', caption:'Units Sold' },
      { name: 'Amount', caption:'Sold Amount' }
    ],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    showColumnSubTotals: false
  };
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent 
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      editSettings={editSettings}>
    </PivotViewComponent>
  );
}

export default App;
```

## Editing Using Pivot Chart

Pivot chart editing provides an alternative way to update, add, or remove underlying data associated with any chart data point. Users can perform CRUD operations on raw items linked to visualized data points.

Clicking a data point in the pivot chart displays the underlying raw items in a data grid within a popup window. Users can then add, update, or delete these items using any of the supported edit types.

**Example:**

```typescript
import { CellEditSettings, IDataSet, PivotViewComponent, Inject, DisplayOption, PivotChart } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';
import { ChartSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/chartSettings';

function App() {
  let editSettings: CellEditSettings = {
    allowAdding: true, 
    allowDeleting: true, 
    allowEditing: true, 
    mode: 'Normal'
  } as CellEditSettings;

  let displayOption: DisplayOption = {
    view: 'Chart'
  } as DisplayOption;

  let chartSettings: ChartSettings = {
    chartSeries: { type: 'Column' }
  } as ChartSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent 
      height={350} 
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      chartSettings={chartSettings} 
      displayOption={displayOption} 
      dataSourceSettings={dataSourceSettings} 
      editSettings={editSettings}>
      <Inject services={[PivotChart]}/>
    </PivotViewComponent>
  );
}

export default App;
```

## Events

### editCompleted

The `editCompleted` event triggers when value cells are edited completely. It provides edited cell(s) information along with previous cell values and helps perform CRUD operations by manually updating the connected data source.

**Event Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `currentData` | object | Current raw data of the edited cells |
| `previousData` | object | Previous raw data of the edited cells |
| `previousPosition` | number | Index of the raw data whose values are edited |
| `cancel` | boolean | If set to **true**, editing won't be reflected in the pivot table |

**Example:**

```typescript
import { DrillThrough, IDataSet, Inject, PivotViewComponent, CellEditSettings, EditCompletedEventArgs } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let editSettings: CellEditSettings = {
    allowAdding: true, 
    allowDeleting: true, 
    allowEditing: true, 
    mode: 'Normal'
  } as CellEditSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };
  
  let pivotObj: PivotViewComponent;
  
  function editCompleted(args: EditCompletedEventArgs): void {
    // Triggers when a value cell is edited
    console.log('Current Data:', args.currentData);
    console.log('Previous Data:', args.previousData);
  }
  
  return (
    <PivotViewComponent 
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      editCompleted={editCompleted.bind(this)} 
      editSettings={editSettings}>
    </PivotViewComponent>
  );
}

export default App;
```

### actionBegin

The `actionBegin` event triggers when editing actions (add, edit, save, delete) are started through the UI. This event allows monitoring the editing workflow and taking action before the operation completes.

**Event Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `dataSourceSettings` | object | Current data source settings |
| `actionName` | string | Name of the editing action |
| `cancel` | boolean | Set to **true** to stop the action |

**Action Names:**

| Action | Action Name |
|--------|-------------|
| Editing | Edit record |
| Save | Save edited records |
| Add | Add new record |
| Delete | Remove record |

**Example:**

```typescript
import { CellEditSettings, IDataSet, PivotViewComponent, PivotActionBeginEventArgs } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let editSettings: CellEditSettings = {
    allowAdding: true, 
    allowDeleting: true, 
    allowEditing: true, 
    mode: 'Dialog'
  } as CellEditSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };
  
  let pivotObj: PivotViewComponent;
  
  function actionBegin(args: PivotActionBeginEventArgs): void {
    if (args.actionName == 'Add new record' || args.actionName == 'Save edited records') {
      args.cancel = true;  // Prevent add and save actions
    }
  }
  
  return (
    <PivotViewComponent 
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      actionBegin={actionBegin.bind(this)} 
      editSettings={editSettings}>
    </PivotViewComponent>
  );
}

export default App;
```

### actionComplete

The `actionComplete` event triggers when a UI action (add, update, remove, save) is finished. This event provides detailed information about the completed action.

**Event Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `dataSourceSettings` | object | Current data source settings |
| `actionName` | string | Name of the completed action |
| `actionInfo` | object | Unique information about the current UI action |

**Action Names:**

| Action | Action Name |
|--------|-------------|
| Save | Edited records saved |
| Add | New record added |
| Delete | Record removed |
| Update | Records updated |

**Example:**

```typescript
import { CellEditSettings, IDataSet, PivotViewComponent, PivotActionCompleteEventArgs } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let editSettings: CellEditSettings = {
    allowAdding: true, 
    allowDeleting: true, 
    allowEditing: true, 
    mode: 'Dialog'
  } as CellEditSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };
  
  let pivotObj: PivotViewComponent;
  
  function actionComplete(args: PivotActionCompleteEventArgs): void {
    if (args.actionName == 'New record added' || args.actionName == 'Edited records saved') {
      // Handle completed editing actions
      console.log('Action completed:', args.actionName);
    }
  }
  
  return (
    <PivotViewComponent 
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      actionComplete={actionComplete.bind(this)} 
      editSettings={editSettings}>
    </PivotViewComponent>
  );
}

export default App;
```

### actionFailure

The `actionFailure` event is triggered when a UI action fails to produce the expected result. This event provides detailed information about the failure.

**Event Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `actionName` | string | Name of the failed action |
| `errorInfo` | object | Error information of the current UI action |

**Action Names:**

| Action | Action Name |
|--------|-------------|
| Editing | Edit record |
| Save | Save edited records |
| Add | Add new record |
| Delete | Remove record |

**Example:**

```typescript
import { CellEditSettings, IDataSet, PivotViewComponent, PivotActionFailureEventArgs } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let editSettings: CellEditSettings = {
    allowAdding: true, 
    allowDeleting: true, 
    allowEditing: true, 
    mode: 'Dialog'
  } as CellEditSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };
  
  let pivotObj: PivotViewComponent;
  
  function actionFailure(args: PivotActionFailureEventArgs): void {
    if (args.actionName == 'Add new record' || args.actionName == 'Save edited records') {
      // Handle failed editing actions
      console.error('Action failed:', args.actionName);
      console.error('Error:', args.errorInfo);
    }
  }
  
  return (
    <PivotViewComponent 
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      actionFailure={actionFailure.bind(this)} 
      editSettings={editSettings}>
    </PivotViewComponent>
  );
}

export default App;
```

## Validation Patterns

### Basic Validation

Implement validation in the `actionBegin` event to prevent invalid data entry:

```typescript
function actionBegin(args: PivotActionBeginEventArgs): void {
  if (args.actionName === 'Save edited records') {
    // Add validation logic here
    const isValid = validateData(args);
    if (!isValid) {
      args.cancel = true;
      alert('Invalid data. Please correct the values.');
    }
  }
}
```

### Confirmation Dialogs

Use built-in confirmation dialogs for better user experience:

```typescript
let editSettings: CellEditSettings = {
  allowEditing: true,
  allowDeleting: true,
  showConfirmDialog: true,
  showDeleteConfirmDialog: true
} as CellEditSettings;
```

## Best Practices

### 1. Choose Appropriate Edit Mode

- **Normal Mode**: Best for simple, single-row edits
- **Dialog Mode**: Ideal when you need focused editing with more fields
- **Batch Mode**: Recommended for bulk updates
- **Command Column**: Use when you want inline action buttons for each row

### 2. Enable Confirmation Dialogs

Always enable confirmation dialogs for critical operations:

```typescript
let editSettings: CellEditSettings = {
  allowEditing: true,
  showConfirmDialog: true,
  showDeleteConfirmDialog: true
} as CellEditSettings;
```

### 3. Handle Events Properly

Implement event handlers to:
- Validate data before saving
- Update external data sources
- Log changes for audit trails
- Handle errors gracefully

### 4. Use Inline Editing for Quick Updates

For scenarios where users need to quickly update single values, enable inline editing:

```typescript
let editSettings: CellEditSettings = {
  allowEditing: true,
  allowInlineEditing: true
} as CellEditSettings;
```

### 5. Restrict Editing When Necessary

Use the `actionBegin` event to restrict certain operations based on business logic:

```typescript
function actionBegin(args: PivotActionBeginEventArgs): void {
  if (args.actionName === 'Remove record' && !userHasDeletePermission) {
    args.cancel = true;
    alert('You do not have permission to delete records.');
  }
}
```

### 6. Double-Click Configuration

Control double-click behavior based on your use case:

```typescript
let editSettings: CellEditSettings = {
  allowEditing: true,
  allowEditOnDblClick: true  // Enable or disable as needed
} as CellEditSettings;
```

### 7. Data Source Updates

Remember that the pivot table automatically updates aggregated values after editing. Ensure your data source maintains consistency:

```typescript
function editCompleted(args: EditCompletedEventArgs): void {
  // Update your external data source if needed
  updateExternalDataSource(args.currentData);
  
  // Refresh pivot table if necessary
  pivotObj.refresh();
}
```

### 8. Error Handling

Always implement `actionFailure` event handler for robust error handling:

```typescript
function actionFailure(args: PivotActionFailureEventArgs): void {
  console.error('Edit operation failed:', args.errorInfo);
  // Show user-friendly error message
  showNotification('Failed to save changes. Please try again.');
}
```

### 9. Relational Data Source Only

Remember that editing features work only with relational data sources. For OLAP data sources, editing is not supported.

### 10. Performance Considerations

For large datasets:
- Use batch mode for bulk operations
- Implement pagination in the data grid
- Consider lazy loading for better performance
- Minimize unnecessary refreshes

## Data Source Example

```typescript
export let pivotData: object[] = [
  { 
    'In_Stock': 34, 
    'Sold': 51, 
    'Amount': 383, 
    'Country': 'France', 
    'Product_Categories': 'Accessories', 
    'Products': 'Bottles and Cages', 
    'Order_Source': 'Retail Outlets', 
    'Year': 'FY 2015', 
    'Quarter': 'Q1' 
  },
  { 
    'In_Stock': 4, 
    'Sold': 423, 
    'Amount': 3595.5, 
    'Country': 'France', 
    'Product_Categories': 'Accessories', 
    'Products': 'Cleaners', 
    'Order_Source': 'Sales Person', 
    'Year': 'FY 2016', 
    'Quarter': 'Q1' 
  }
  // Additional data items...
];
```

## Common Scenarios

### Scenario 1: Read-Only Editing

Enable editing but restrict add and delete operations:

```typescript
let editSettings: CellEditSettings = {
  allowEditing: true,
  allowAdding: false,
  allowDeleting: false
} as CellEditSettings;
```

### Scenario 2: Custom Validation

Implement custom validation before saving:

```typescript
function actionBegin(args: PivotActionBeginEventArgs): void {
  if (args.actionName === 'Save edited records') {
    // Custom validation logic
    if (!validateBusinessRules(args)) {
      args.cancel = true;
      showValidationError();
    }
  }
}
```

### Scenario 3: Audit Trail

Track all editing operations:

```typescript
function editCompleted(args: EditCompletedEventArgs): void {
  logAuditTrail({
    action: 'EDIT',
    timestamp: new Date(),
    previousData: args.previousData,
    currentData: args.currentData,
    user: getCurrentUser()
  });
}
```

### Scenario 4: Conditional Editing

Enable editing based on user permissions:

```typescript
const editSettings = useMemo(() => {
  return {
    allowEditing: userHasEditPermission,
    allowAdding: userHasAddPermission,
    allowDeleting: userHasDeletePermission,
    mode: 'Dialog'
  } as CellEditSettings;
}, [userHasEditPermission, userHasAddPermission, userHasDeletePermission]);
```

## Related Documentation

- [Drill Through](./drill-through.md)
- [Data Grid Options on Editing Mode](./how-to/configure-data-grid-options-on-editing-mode)
- [API Reference - editSettings](https://ej2.syncfusion.com/react/documentation/api/pivotview/#editsettings)
- [API Reference - CellEditSettings](https://ej2.syncfusion.com/react/documentation/api/pivotview/cellEditSettingsModel/)
