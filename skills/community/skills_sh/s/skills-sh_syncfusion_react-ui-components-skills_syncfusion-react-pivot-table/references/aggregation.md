# Aggregation in Syncfusion React Pivot Table

## Overview

Aggregation is a powerful feature in the Syncfusion React Pivot Table component that allows end users to perform calculations on groups of values, specifically for value fields placed in the value axis. This feature is **applicable only for relational data sources** (not for OLAP data sources).

By default, values in the pivot table are combined by summing them. However, the component supports 23+ different aggregation types to provide comprehensive data analysis capabilities.

## Supported Aggregation Types

The Syncfusion React Pivot Table supports the following aggregation types:

| Aggregation Type | Description | Field Type Support |
|-----------------|-------------|-------------------|
| **Sum** | Displays the total sum for the selected field values. | Numeric |
| **Product** | Displays the product of the selected field values. | Numeric |
| **Count** | Displays the number of records for the selected field. | All types |
| **DistinctCount** | Displays the number of unique records for the selected field. | All types |
| **Min** | Displays the minimum value for the selected field. | Numeric |
| **Max** | Displays the maximum value for the selected field. | Numeric |
| **Avg** | Displays the average (mean) of the selected field values. | Numeric |
| **Median** | Displays the median value for the selected field. | Numeric |
| **Index** | Displays the index value for the selected field data. | Numeric |
| **PopulationStDev** | Displays the standard deviation of the population for the selected field. | Numeric |
| **SampleStDev** | Displays the sample standard deviation for the selected field. | Numeric |
| **PopulationVar** | Displays the variance of the population for the selected field. | Numeric |
| **SampleVar** | Displays the sample variance for the selected field. | Numeric |
| **RunningTotals** | Displays the running total for the selected field values. | Numeric |
| **DifferenceFrom** | Displays the pivot table values with difference from the value of the base item in the base field. | Numeric |
| **PercentageOfDifferenceFrom** | Displays the pivot table values with percentage difference from the value of the base item in the base field. | Numeric |
| **PercentageOfGrandTotal** | Displays the pivot table values with percentage of grand total of all values. | Numeric |
| **PercentageOfColumnTotal** | Displays the pivot table values in each column with percentage of total values for the column. | Numeric |
| **PercentageOfRowTotal** | Displays the pivot table values in each row with percentage of total values for the row. | Numeric |
| **PercentageOfParentTotal** | Displays the pivot table values with percentage of total of all values based on selected field. | Numeric |
| **PercentageOfParentColumnTotal** | Displays the pivot table values with percentage of its parent total in each column. | Numeric |
| **PercentageOfParentRowTotal** | Displays the pivot table values with percentage of its parent total in each row. | Numeric |
| **CalculatedField** | Displays the pivot table with calculated field values. It allows user to create a new calculated field alone. | N/A |

### Field Type Support

**Important Notes:**
- **Numeric fields** support all aggregation types listed above, except **CalculatedField**.
- **Non-numeric fields** (string, date, datetime, boolean, etc.) support only **Count** and **DistinctCount** aggregation types.
- By default, numeric fields use **Sum** aggregation, while non-numeric fields use **Count** aggregation.

## Setting Aggregation Type

### Using the `type` Property

You can set the aggregation type for each value field using the `type` property in the `values` array within `dataSourceSettings`:

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { name: 'Sold', caption: 'Units Sold', type: 'Sum' }, 
      { name: 'Amount', caption: 'Sold Amount', type: 'Avg' }
    ]
  }
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent  
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings}>
    </PivotViewComponent>
  );
}

export default App;
```

### Using Comparison Aggregations with `baseField` and `baseItem`

For aggregation types like **DifferenceFrom** and **PercentageOfDifferenceFrom**, you can specify a base field and base item for comparison:

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { 
        name: 'Sold', 
        caption: 'Units Sold', 
        type: 'DifferenceFrom', 
        baseField: 'Year', 
        baseItem: 'FY 2018' 
      }, 
      { 
        name: 'Amount', 
        caption: 'Sold Amount', 
        type: 'Sum' 
      }
    ]
  }
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent  
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings}>
    </PivotViewComponent>
  );
}

export default App;
```

**Key Properties for Comparison Aggregations:**
- **`type`**: Sets the aggregate type of the field (e.g., 'DifferenceFrom', 'PercentageOfDifferenceFrom')
- **`baseField`**: Specifies the field to use as a comparison base
- **`baseItem`**: Specifies the member/item within the base field to compare against

### Using `baseField` for Percentage Aggregations

For the **PercentageOfParentTotal** aggregation type, use the `baseField` property to specify the field:

```typescript
values: [
  { 
    name: 'Amount', 
    caption: 'Sold Amount', 
    type: 'PercentageOfParentTotal', 
    baseField: 'Country' 
  }
]
```

## Modifying Aggregation at Runtime

End users can dynamically modify aggregation types through the UI in two ways:

### 1. Through Grouping Bar

Value fields in the grouping bar include a dropdown icon that allows users to select different aggregation types:

```typescript
import { GroupingBar, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount' }
    ]
  }
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent  
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      showGroupingBar={true}>
      <Inject services={[GroupingBar]}/>
    </PivotViewComponent>
  );
}

export default App;
```

### 2. Through Field List

Value fields in the field list also include a dropdown icon for changing aggregation types:

```typescript
import { FieldList, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount' }
    ]
  }
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent  
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      showFieldList={true}>
      <Inject services={[FieldList]}/>
    </PivotViewComponent>
  );
}

export default App;
```

## Customizing Aggregation Dropdown

### Showing Specific Aggregation Types

You can customize the dropdown menu to display only specific aggregation types using the `aggregateTypes` property:

```typescript
import { GroupingBar, FieldList, Inject, IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount', type: 'Sum' }
    ],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    filters: [],
  }
  
  let pivotObj: PivotViewComponent;
  let pivotAggregateTypes: any = ['DistinctCount', 'Avg', 'Product'];
  
  return (
    <PivotViewComponent  
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      showFieldList={true} 
      showGroupingBar={true} 
      aggregateTypes={pivotAggregateTypes}>
      <Inject services={[GroupingBar, FieldList]}/>
    </PivotViewComponent>
  );
}

export default App;
```

## UI Customization Options

### Hiding Aggregation Type from Button Text

By default, value field buttons display both the field name and aggregation type (e.g., "Sum of Units Sold"). To display only the field name:

```typescript
import { IDataSet, PivotViewComponent, Inject, GroupingBar } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount', type: 'Sum' }
    ],
    showAggregationOnValueField: false
  }
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent  
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      showGroupingBar={true}>
      <Inject services={[GroupingBar]}/>
    </PivotViewComponent>
  );
}

export default App;
```

### Hiding Aggregation Type Icon from Grouping Bar

To hide the dropdown icon for changing aggregation types in the grouping bar:

```typescript
import { GroupingBar, GroupingBarSettings, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let groupingSettings: GroupingBarSettings = {
    showValueTypeIcon: false
  } as GroupingBarSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount' }
    ]
  }
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent  
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      groupingBarSettings={groupingSettings} 
      dataSourceSettings={dataSourceSettings} 
      showGroupingBar={true}>
      <Inject services={[GroupingBar]}/>
    </PivotViewComponent>
  );
}

export default App;
```

**Note:** The aggregation type icon can only be hidden in the Grouping Bar, not in the Field List.

## Events

### AggregateCellInfo Event

The `aggregateCellInfo` event triggers each time a value cell is rendered, allowing you to override cell values or skip formatting:

```typescript
import { PivotViewComponent, GroupingBar, Inject, IDataSet } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C2' }],
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount' }
    ],
    rows: [{ name: 'Country' }, { name: 'Products' }],
  };
  
  function aggregateCell(args: any) {
    // Override cell value or skip formatting
    args.skipFormatting = true;
  }
  
  let pivotObj: PivotViewComponent;
  
  return (
    <PivotViewComponent 
      id='PivotView' 
      ref={(d: PivotViewComponent) => pivotObj = d} 
      height={350} 
      aggregateCellInfo={aggregateCell.bind(this)} 
      dataSourceSettings={dataSourceSettings} 
      showGroupingBar={true}>
      <Inject services={[GroupingBar]} />
    </PivotViewComponent>
  );
}

export default App;
```

**Event Parameters:**
- `fieldName`: Current cell's field name
- `row`: Current cell's row value
- `column`: Current cell's column value
- `value`: Value of current cell
- `cellSets`: Raw data for the aggregated value cell
- `rowCellType`: Row cell type value
- `columnCellType`: Column cell type value
- `aggregateType`: Aggregate type of the cell
- `skipFormatting`: Boolean property to skip formatting if applied

### ActionBegin Event

Triggered when a user initiates an aggregation type change:

```typescript
import { FieldList, GroupingBar, IDataSet, Inject, PivotViewComponent, PivotActionBeginEventArgs } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount' }
    ],
    filters: [],
  }
  
  let pivotObj: PivotViewComponent;
  
  function actionBegin(args: PivotActionBeginEventArgs): void {
    if (args.actionName == 'Aggregate field') {
      // Cancel the action if needed
      args.cancel = true;
    }
  }
  
  return (
    <PivotViewComponent  
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      actionBegin={actionBegin.bind(this)} 
      showFieldList={true} 
      showGroupingBar={true}>
      <Inject services={[FieldList, GroupingBar]} />
    </PivotViewComponent>
  );
}

export default App;
```

**Event Parameters:**
- `dataSourceSettings`: Current data source settings
- `actionName`: Name of the current action (e.g., "Aggregate field")
- `fieldInfo`: Information about the selected value field
- `cancel`: Allows restricting the current action

### ActionComplete Event

Triggered when an aggregation type change is completed:

```typescript
import { FieldList, GroupingBar, IDataSet, Inject, PivotViewComponent, PivotActionCompleteEventArgs } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount' }
    ],
    filters: [],
  }
  
  let pivotObj: PivotViewComponent;

  function actionComplete(args: PivotActionCompleteEventArgs): void {
    if (args.actionName == 'Field aggregated') {
      // Handle post-aggregation logic
    }
  }
  
  return (
    <PivotViewComponent  
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      actionComplete={actionComplete.bind(this)} 
      showFieldList={true} 
      showGroupingBar={true}>
      <Inject services={[FieldList, GroupingBar]} />
    </PivotViewComponent>
  );
}

export default App;
```

**Event Parameters:**
- `dataSourceSettings`: Current data source settings
- `actionName`: Name of completed action (e.g., "Field aggregated")
- `fieldInfo`: Information about the selected value field
- `actionInfo`: Unique information about the current UI action

### ActionFailure Event

Triggered when an aggregation action fails:

```typescript
import { FieldList, GroupingBar, IDataSet, Inject, PivotViewComponent, PivotActionFailureEventArgs } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' }, 
      { name: 'Amount', caption: 'Sold Amount' }
    ],
    filters: [],
  }
  
  let pivotObj: PivotViewComponent;
  
  function actionFailure(args: PivotActionFailureEventArgs): void {
    if (args.actionName == 'Aggregate field') {
      // Handle failure
      console.error('Aggregation failed:', args.errorInfo);
    }
  }
  
  return (
    <PivotViewComponent  
      ref={(d: PivotViewComponent) => pivotObj = d} 
      id='PivotView' 
      height={350} 
      dataSourceSettings={dataSourceSettings} 
      actionFailure={actionFailure.bind(this)} 
      showFieldList={true} 
      showGroupingBar={true}>
      <Inject services={[FieldList, GroupingBar]} />
    </PivotViewComponent>
  );
}

export default App;
```

**Event Parameters:**
- `actionName`: Name of the failed action
- `errorInfo`: Detailed error information

## Best Practices

### Choosing the Right Aggregation Type

1. **Basic Analysis:**
   - Use **Sum** for totaling values (sales, quantities, etc.)
   - Use **Count** to count records or occurrences
   - Use **Avg** for average calculations (average sales, average scores, etc.)

2. **Statistical Analysis:**
   - Use **Min** and **Max** for range analysis
   - Use **Median** for central tendency with outliers
   - Use **PopulationStDev** or **SampleStDev** for variability analysis
   - Use **PopulationVar** or **SampleVar** for variance calculations

3. **Comparative Analysis:**
   - Use **DifferenceFrom** to compare against a baseline value
   - Use **PercentageOfDifferenceFrom** for percentage change analysis
   - Use **RunningTotals** for cumulative analysis

4. **Percentage Analysis:**
   - Use **PercentageOfGrandTotal** for overall contribution
   - Use **PercentageOfColumnTotal** for column-wise contribution
   - Use **PercentageOfRowTotal** for row-wise contribution
   - Use **PercentageOfParentTotal** for hierarchical percentage analysis

5. **Unique Values:**
   - Use **DistinctCount** to count unique values
   - Use **Product** for multiplicative calculations

### Performance Considerations

1. **Default Aggregations:** Let the component use default aggregations (Sum for numeric, Count for non-numeric) when possible for optimal performance.

2. **Complex Aggregations:** Aggregations like **DifferenceFrom** and percentage-based aggregations require additional calculations. Use them judiciously on large datasets.

3. **Multiple Aggregations:** When displaying multiple aggregations of the same field, consider the performance impact on large datasets.

### Field Type Compatibility

Always ensure you're using aggregation types compatible with your field types:

- **Numeric fields only:** Sum, Product, Min, Max, Avg, Median, Index, statistical aggregations, running totals, and all comparison/percentage aggregations
- **All field types:** Count, DistinctCount
- **Special case:** CalculatedField (for custom calculations)

### User Experience

1. **Limit Aggregation Options:** Use the `aggregateTypes` property to show only relevant aggregation types for your use case.

2. **Hide Unnecessary UI Elements:** Use `showAggregationOnValueField` and `showValueTypeIcon` properties to simplify the interface when aggregation changes aren't needed.

3. **Provide Clear Labels:** Use the `caption` property to provide user-friendly names for value fields.

4. **Handle Events:** Implement `actionBegin`, `actionComplete`, and `actionFailure` events to provide feedback and handle errors gracefully.
