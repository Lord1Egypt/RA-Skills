# Grouping Bar Reference

## Overview

The Grouping Bar is the primary drag-and-drop interface in the Syncfusion React Pivot Table component. It provides an intuitive way for users to design and modify pivot reports at runtime without needing to write code. The grouping bar displays fields from the bound data source and allows users to rearrange them between different axes (rows, columns, values, and filters) through simple drag-and-drop operations.

Key features of the Grouping Bar include:

- Visual representation of all available fields from the data source
- Drag-and-drop functionality to move fields between axes
- Interactive icons for filtering, sorting, and removing fields
- Fields panel option to show unused fields
- Aggregation type selection for value fields
- Complete runtime report customization

The grouping bar makes report creation accessible to all users by providing intuitive interactions similar to the Field List, eliminating the need for complex configuration or programming knowledge.

## Enabling Grouping Bar

To enable the grouping bar in your Pivot Table, set the `showGroupingBar` property to **true**. You must also inject the `GroupingBar` module into the Pivot Table component.

```ts
import { GroupingBar, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    allowLabelFilter: true,
    allowValueFilter: true,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }
  let pivotObj: PivotViewComponent;
    return (<PivotViewComponent ref={ (d: PivotViewComponent) => pivotObj = d } id='PivotView' height={350} dataSourceSettings={dataSourceSettings} showGroupingBar={true} ><Inject services={[GroupingBar]}/> </PivotViewComponent>);
};

export default App;
```

## Module Injection

The GroupingBar functionality requires the `GroupingBar` module to be injected into the Pivot Table. Always include the module injection in your component:

```ts
<Inject services={[GroupingBar]}/>
```

## Drag-and-Drop Operations

The grouping bar enables powerful drag-and-drop operations that allow users to:

1. **Re-arrange fields** - Move fields to different positions within the same axis
2. **Move fields between axes** - Transfer fields from rows to columns, or from columns to values, etc.
3. **Add fields from the fields panel** - Drag unused fields into any axis
4. **Remove fields** - Drag fields out of the report or use the remove icon

### Enabling/Disabling Drag-and-Drop

To disable drag-and-drop for all fields:

```ts
let groupingSettings: GroupingBarSettings = {
  allowDragAndDrop: false
} as GroupingBarSettings;
```

To disable drag-and-drop for specific fields:

```ts
let dataSourceSettings: DataSourceSettingsModel = {
  columns: [
    { name: 'Year', caption: 'Production Year', allowDragAndDrop: false }, 
    { name: 'Quarter' }
  ],
  rows: [
    { name: 'Country' }, 
    { name: 'Products', allowDragAndDrop: false }
  ],
  // ... other settings
}
```

## Filter Icon Functionality

The filter icon appears next to each field in the grouping bar, allowing users to filter members of that field. By default, the filter icon is enabled for all fields.

### Show/Hide All Filter Icons

To hide filter icons for all fields:

```ts
let groupingSettings: GroupingBarSettings = {
  showFilterIcon: false
} as GroupingBarSettings;
```

### Show/Hide Specific Filter Icons

To hide filter icons for specific fields only:

```ts
let dataSourceSettings: DataSourceSettingsModel = {
  columns: [
    { name: 'Year', caption: 'Production Year' }, 
    { name: 'Quarter', showFilterIcon: false }
  ],
  rows: [
    { name: 'Country' }, 
    { name: 'Products', showFilterIcon: false }
  ],
  // ... other settings
}
```

## Sort Icon Functionality

The sort icon allows users to sort field members in ascending or descending order. By default, members are sorted in ascending order.

### Show/Hide All Sort Icons

To hide sort icons for all fields:

```ts
let groupingSettings: GroupingBarSettings = {
  showSortIcon: false
} as GroupingBarSettings;
```

### Show/Hide Specific Sort Icons

To hide sort icons for specific fields:

```ts
let dataSourceSettings: DataSourceSettingsModel = {
  columns: [
    { name: 'Year', caption: 'Production Year' }, 
    { name: 'Quarter', showSortIcon: false }
  ],
  rows: [
    { name: 'Country', showSortIcon: false }, 
    { name: 'Products' }
  ],
  // ... other settings
}
```

## Remove Field Functionality

The remove icon allows users to remove fields from the report at runtime. By default, this icon is visible for all fields.

### Show/Hide All Remove Icons

To hide remove icons for all fields:

```ts
let groupingSettings: GroupingBarSettings = {
  showRemoveIcon: false
} as GroupingBarSettings;
```

### Show/Hide Specific Remove Icons

To hide remove icons for specific fields:

```ts
let dataSourceSettings: DataSourceSettingsModel = {
  columns: [
    { name: 'Year', caption: 'Production Year', showRemoveIcon: false }, 
    { name: 'Quarter' }
  ],
  values: [
    { name: 'Sold', caption: 'Units Sold', showRemoveIcon: false }, 
    { name: 'Amount', caption: 'Sold Amount' }
  ],
  rows: [
    { name: 'Country' }, 
    { name: 'Products', showRemoveIcon: false }
  ],
  // ... other settings
}
```

## Fields Panel Option

The fields panel displays all available fields from the data source that are not currently used in the pivot table. Users can drag fields from this panel into any axis to add them to the report.

To enable the fields panel:

```ts
let groupingSettings: GroupingBarSettings = {
  showFieldsPanel: true
} as GroupingBarSettings;
```

```ts
import { GroupingBar, GroupingBarSettings, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let groupingSettings: GroupingBarSettings = {
    showFieldsPanel: true
  } as GroupingBarSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }
  let pivotObj: PivotViewComponent;
    return (<PivotViewComponent  ref={ (d: PivotViewComponent) => pivotObj = d } id='PivotView' height={350} groupingBarSettings={groupingSettings} dataSourceSettings={dataSourceSettings} showGroupingBar={true} ><Inject services={[GroupingBar]}/> </PivotViewComponent>);
};

export default App;
```

## Value Type Icon (Aggregation)

Each value field in the grouping bar displays a dropdown icon that allows users to change the aggregation type (Sum, Average, Count, etc.) at runtime.

### Show/Hide All Value Type Icons

To hide the aggregation dropdown for all value fields:

```ts
let groupingSettings: GroupingBarSettings = {
  showValueTypeIcon: false
} as GroupingBarSettings;
```

### Show/Hide Specific Value Type Icons

To hide the aggregation dropdown for specific value fields:

```ts
let dataSourceSettings: DataSourceSettingsModel = {
  values: [
    { name: 'Sold', caption: 'Units Sold', showValueTypeIcon: false }, 
    { name: 'Amount', caption: 'Sold Amount' }
  ],
  // ... other settings
}
```

## Values Button

The Values button appears in the grouping bar when multiple fields are added to the values axis. This button can be repositioned among fields in either the column or row axis.

To enable the Values button:

```ts
<PivotViewComponent 
  showGroupingBar={true} 
  showValuesButton={true}
  dataSourceSettings={dataSourceSettings}
>
  <Inject services={[GroupingBar]}/>
</PivotViewComponent>
```

**Note:** The Values button is only available for relational data sources and only appears when multiple fields are in the values axis.

## Excluding Specific Fields

To hide specific fields from the grouping bar:

```ts
let dataSourceSettings: DataSourceSettingsModel = {
  columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
  dataSource: pivotData as IDataSet[],
  rows: [{ name: 'Country' }, { name: 'Products' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
  excludeFields: ['In_Stock']
}
```

**Note:** Fields excluded using `excludeFields` will also be hidden in the field list UI.

## Grouping Bar Customization Options

All grouping bar customization options are configured through the `groupingBarSettings` property:

```ts
let groupingSettings: GroupingBarSettings = {
  showFieldsPanel: true,
  showFilterIcon: true,
  showSortIcon: true,
  showRemoveIcon: true,
  showValueTypeIcon: true,
  allowDragAndDrop: true
} as GroupingBarSettings;
```

## Complete Code Example

```ts
import { GroupingBar, GroupingBarSettings, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let groupingSettings: GroupingBarSettings = {
    showFieldsPanel: true,
    showFilterIcon: true,
    showSortIcon: true,
    showRemoveIcon: true,
    showValueTypeIcon: true,
    allowDragAndDrop: true
  } as GroupingBarSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [
      { name: 'Year', caption: 'Production Year' }, 
      { name: 'Quarter' }
    ],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    allowLabelFilter: true,
    allowValueFilter: true,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [
      { name: 'Country' }, 
      { name: 'Products' }
    ],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount' }
    ]
  }
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent  
      ref={ (d: PivotViewComponent) => pivotObj = d } 
      id='PivotView' 
      height={350} 
      groupingBarSettings={groupingSettings} 
      dataSourceSettings={dataSourceSettings} 
      showGroupingBar={true}
      showValuesButton={true}
    >
      <Inject services={[GroupingBar]}/> 
    </PivotViewComponent>
  );
};

export default App;
```

```ts
// datasource.ts
export let pivotData: object[] = [
    { 'In_Stock': 34, 'Sold': 51, 'Amount': 383, 'Country': 'France', 'Product_Categories': 'Accessories', 'Products': 'Bottles and Cages', 'Order_Source': 'Retail Outlets', 'Year': 'FY 2015', 'Quarter': 'Q1' },
    { 'In_Stock': 4, 'Sold': 423, 'Amount': 3595.5, 'Country': 'France', 'Product_Categories': 'Accessories', 'Products': 'Cleaners', 'Order_Source': 'Sales Person', 'Year': 'FY 2016', 'Quarter': 'Q1' },
    { 'In_Stock': 11, 'Sold': 19, 'Amount': 85.5, 'Country': 'France', 'Product_Categories': 'Bikes', 'Products': 'Touring Bikes', 'Order_Source': 'Retail Outlets', 'Year': 'FY 2017', 'Quarter': 'Q4' },
    { 'In_Stock': 10, 'Sold': 64, 'Amount': 320, 'Country': 'France', 'Product_Categories': 'Bikes', 'Products': 'Mountain Bikes', 'Order_Source': 'Sales Person', 'Year': 'FY 2018', 'Quarter': 'Q4' },
    { 'In_Stock': 2, 'Sold': 141, 'Amount': 1692, 'Country': 'France', 'Product_Categories': 'Clothing', 'Products': 'Jerseys', 'Order_Source': 'Sales Person', 'Year': 'FY 2015', 'Quarter': 'Q1' },
    // ... more data
];
```

## Events

### onFieldDropped

Triggered when a field is dragged and dropped into a new axis:

```ts
function onFieldDropped(args: FieldDroppedEventArgs): void {
  args.droppedField.caption = args.droppedField.name + " --> " + args.droppedAxis;
}

<PivotViewComponent 
  onFieldDropped={onFieldDropped.bind(this)}
  showGroupingBar={true}
>
  <Inject services={[GroupingBar]}/>
</PivotViewComponent>
```

### fieldDragStart

Triggered when a field drag operation begins:

```ts
function fieldDragStart(args: FieldDragStartEventArgs): void {
  if(args.axis === 'rows') {
    args.cancel = true; // Prevent dragging from rows axis
  }
}

<PivotViewComponent 
  fieldDragStart={fieldDragStart.bind(this)}
  showGroupingBar={true}
>
  <Inject services={[GroupingBar]}/>
</PivotViewComponent>
```

### fieldDrop

Triggered when a field is dropped into an axis:

```ts
function fieldDrop(args: FieldDropEventArgs): void {
  if(args.dropAxis === 'values') {
    args.cancel = true; // Prevent dropping into values axis
  }
}

<PivotViewComponent 
  fieldDrop={fieldDrop.bind(this)}
  showGroupingBar={true}
>
  <Inject services={[GroupingBar]}/>
</PivotViewComponent>
```

### fieldRemove

Triggered when a field is being removed:

```ts
function fieldRemove(args: FieldRemoveEventArgs): void {
  if(args.fieldName === 'Country') {
    args.cancel = true; // Prevent removal of Country field
  }
}

<PivotViewComponent 
  fieldRemove={fieldRemove.bind(this)}
  showGroupingBar={true}
>
  <Inject services={[GroupingBar]}/>
</PivotViewComponent>
```

### aggregateMenuOpen

Triggered when the aggregation menu dropdown opens:

```ts
function aggregateMenuOpen(args: AggregateMenuOpenEventArgs): void {
  args.displayMenuCount = 4;
  if(args.fieldName === 'Amount') {
    args.aggregateTypes = ['Sum', 'Avg', 'Max'];
  }
}

<PivotViewComponent 
  aggregateMenuOpen={aggregateMenuOpen.bind(this)}
  showGroupingBar={true}
>
  <Inject services={[GroupingBar]}/>
</PivotViewComponent>
```

### actionBegin

Triggered when a UI action begins in the grouping bar:

```ts
function actionBegin(args: PivotActionBeginEventArgs): void {
  if (args.actionName == 'Sort field' || args.actionName == 'Filter field') {
    args.cancel = true; // Prevent sorting and filtering
  }
}

<PivotViewComponent 
  actionBegin={actionBegin.bind(this)}
  showGroupingBar={true}
>
  <Inject services={[GroupingBar]}/>
</PivotViewComponent>
```

### actionComplete

Triggered when a UI action completes in the grouping bar:

```ts
function actionComplete(args: PivotActionCompleteEventArgs): void {
  if (args.actionName == 'Field sorted' || args.actionName == 'Field filtered') {
    // Handle completed actions
    console.log('Action completed:', args.actionName);
  }
}

<PivotViewComponent 
  actionComplete={actionComplete.bind(this)}
  showGroupingBar={true}
>
  <Inject services={[GroupingBar]}/>
</PivotViewComponent>
```

## Best Practices for User Interaction

1. **Enable the Fields Panel** - Always show the fields panel (`showFieldsPanel: true`) to give users easy access to all available fields

2. **Use Clear Field Captions** - Provide meaningful captions for fields to help users understand the data:
   ```ts
   { name: 'Year', caption: 'Production Year' }
   ```

3. **Control Critical Fields** - Prevent accidental removal or modification of essential fields:
   ```ts
   { name: 'Country', showRemoveIcon: false, allowDragAndDrop: false }
   ```

4. **Limit Available Aggregations** - Use the `aggregateMenuOpen` event to show only relevant aggregation types for each field

5. **Provide Visual Feedback** - Use events like `actionBegin` and `actionComplete` to provide user feedback during operations

6. **Handle Field Dependencies** - Use the `fieldDrop` or `fieldRemove` events to enforce business rules about field placement

7. **Enable Values Button** - When working with multiple value fields, enable the Values button for better organization

8. **Consider User Permissions** - Hide or disable specific icons based on user roles or permissions

9. **Maintain Field Organization** - Group related fields together and use meaningful names to improve user experience

10. **Test Drag-and-Drop Scenarios** - Ensure all drag-and-drop operations work smoothly across different axes

## API Properties Reference

| Property | Type | Description |
|----------|------|-------------|
| `showGroupingBar` | boolean | Enables/disables the grouping bar |
| `showValuesButton` | boolean | Shows/hides the Values button |
| `groupingBarSettings.showFieldsPanel` | boolean | Shows/hides the fields panel |
| `groupingBarSettings.showFilterIcon` | boolean | Shows/hides filter icons for all fields |
| `groupingBarSettings.showSortIcon` | boolean | Shows/hides sort icons for all fields |
| `groupingBarSettings.showRemoveIcon` | boolean | Shows/hides remove icons for all fields |
| `groupingBarSettings.showValueTypeIcon` | boolean | Shows/hides aggregation dropdowns for all value fields |
| `groupingBarSettings.allowDragAndDrop` | boolean | Enables/disables drag-and-drop for all fields |
| `fieldOptions.showFilterIcon` | boolean | Shows/hides filter icon for specific field |
| `fieldOptions.showSortIcon` | boolean | Shows/hides sort icon for specific field |
| `fieldOptions.showRemoveIcon` | boolean | Shows/hides remove icon for specific field |
| `fieldOptions.showValueTypeIcon` | boolean | Shows/hides aggregation dropdown for specific value field |
| `fieldOptions.allowDragAndDrop` | boolean | Enables/disables drag-and-drop for specific field |
| `dataSourceSettings.excludeFields` | string[] | Array of field names to hide from grouping bar |

## Related Features

- **Field List** - Alternative UI for field management with a dialog interface
- **Filtering** - Use the filter icon to apply label or value filters
- **Sorting** - Use the sort icon to arrange field members
- **Aggregation** - Change calculations for value fields
- **Calculated Fields** - Create custom fields with formulas
- **Conditional Formatting** - Apply formatting rules to cells
- **Drill-Through** - View raw data behind aggregated values
