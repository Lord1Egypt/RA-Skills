# Filtering and Sorting

## Table of Contents
- [Member Filtering](#member-filtering)
- [Label Filtering](#label-filtering)
- [Value Filtering](#value-filtering)
- [Member Sorting](#member-sorting)
- [Custom Sorting](#custom-sorting)
- [Value Sorting](#value-sorting)
- [Performance Optimization](#performance-optimization)
- [Properties Reference](#properties-reference)

## Member Filtering

### Overview

Member filtering displays the Pivot Table with selective records based on the members you choose to include or exclude in each field. By default, member filtering is enabled through the `allowMemberFilter` property.

Users can apply member filters at runtime by clicking the filter icon next to any field in the row, column, and filter axes, available in both the field list and grouping bar interfaces.

### Programmatic Member Filtering

Configure filtering using the `filterSettings` property. The essential settings required are:

* `name`: Sets the appropriate field name for filtering
* `type`: Specifies the filter type as **Include** or **Exclude**
* `items`: Defines the members that need to be either included or excluded
* `levelCount`: Sets the level count for OLAP data sources (optional for relational data)

```typescript
import { IDataSet, PivotViewComponent, Inject, FieldList } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function MemberFilterExample() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filterSettings: [{ name: 'Country', type: 'Exclude', items: ['United States'] }],
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
      showFieldList={true}
    >
      <Inject services={[FieldList]} />
    </PivotViewComponent>
  );
}

export default MemberFilterExample;
```

### Select/Deselect All Members

The member filter dialog includes an **All** option that allows you to select or deselect all available members with a single click. When unchecked, all members become deselected, and the **OK** button becomes disabled. You must select at least one member to apply the filter.

### Search Members

The member filter dialog includes a built-in search box that allows you to find members by typing part of their name. This makes it easy to locate specific members, especially when dealing with large datasets.

### Sort Members

The member filter dialog provides built-in sort icons that let you arrange members in ascending or descending order. When neither sorting option is selected, members appear in their original order as retrieved from the data source.

### Performance Optimization for Large Datasets

Control member display using the `maxNodeLimitInMemberEditor` property (default: 1000). When data contains more members than the limit, only the specified number will be shown initially with a message indicating additional members available:

```typescript
<PivotViewComponent
  id='PivotView'
  height={350}
  dataSourceSettings={dataSourceSettings}
  maxNodeLimitInMemberEditor={500}
  showFieldList={true}
>
  <Inject services={[VirtualScroll, FieldList]} />
</PivotViewComponent>
```

### Load Members On-Demand (OLAP Only)

Enable on-demand loading with the `loadOnDemandInMemberEditor` property (default: true). Only first level members load initially, improving performance:

```typescript
<PivotViewComponent
  id='PivotView'
  height={350}
  dataSourceSettings={dataSourceSettings}
  loadOnDemandInMemberEditor={true}
  showFieldList={true}
>
  <Inject services={[FieldList]} />
</PivotViewComponent>
```

**Expand members individually** or **Load by level selection** to access deeper hierarchy levels.

### Load Members by Level Count (OLAP Only)

Specify the `levelCount` property in `filterSettings` to control depth of member loading:

```typescript
filterSettings: [
  {
    name: '[Customer].[Customer Geography]',
    items: ['[Customer].[Customer Geography].[State-Province].&[NSW]&[AU]'],
    type: 'Exclude',
    levelCount: 2  // ← Loads Country and State-Province levels
  }
]
```

## Label Filtering

### Overview

Label filtering allows you to display only the data with specific header text across row and column fields. Enable with the `allowLabelFilter` property.

Supports three data types:
- String data type
- Number data type
- Date data type

Access filtering through the filter icon in field list or grouping bar, then navigate to the "Label" tab.

### Text/Label Filtering through Code

Enable and configure text filtering with these properties:

* `name`: Sets the field name
* `type`: Sets the filter type as **Label**
* `condition`: Defines the operator (Equals, Contains, Between, etc.)
* `value1`: Sets the primary value
* `value2`: Sets the secondary value (for Between, NotBetween operators)

**Text Filter Operators:**

| Operator | Description |
|----------|-------------|
| Equals | Matches exact text |
| DoesNotEquals | Does not match the text |
| BeginWith | Begins with text |
| DoesNotBeginWith | Does not begin with text |
| EndsWith | Ends with text |
| DoesNotEndsWith | Does not end with text |
| Contains | Contains text |
| DoesNotContains | Does not contain text |
| GreaterThan | Text is greater |
| GreaterThanOrEqualTo | Text is greater than or equal |
| LessThan | Text is lesser |
| LessThanOrEqualTo | Text is lesser than or equal |
| Between | Between start and end text |
| NotBetween | Not between start and end text |

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: pivotData as IDataSet[],
  expandAll: false,
  allowLabelFilter: true,
  filterSettings: [{ name: 'Country', type: 'Label', condition: 'GreaterThan', value1: 'United Kingdom' }],
  columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
  rows: [{ name: 'Country' }, { name: 'Products' }],
  filters: []
};
```

### Date Filtering through Code

Date filtering displays records based on date values. Configure with the `filterSettings` property:

* `name`: Sets the field name
* `type`: Sets the filter type as **Date**
* `condition`: Defines the operator (Equals, Before, After, Between, etc.)
* `value1`: Sets the start date
* `value2`: Sets the end date (for Between, NotBetween operators)

> Date filtering is enabled only when the field has **date** type `formatSettings`.

**Date Filter Operators:**

| Operator | Description |
|----------|-------------|
| Equals | Matches the given date |
| DoesNotEquals | Does not match the given date |
| Before | Before the given date |
| BeforeOrEqualTo | Before or equal to the given date |
| After | After the given date |
| AfterOrEqualTo | After or equal to the given date |
| Between | Between start and end dates |
| NotBetween | Not between start and end dates |

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: pivotData as IDataSet[],
  expandAll: false,
  allowLabelFilter: true,
  formatSettings: [{ name: 'Year', format: 'dd/MM/yyyy-hh:mm', type: 'date' }],
  filterSettings: [{ name: 'Year', type: 'Date', condition: 'Before', value1: new Date('2016') }],
  columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
  rows: [{ name: 'Country' }, { name: 'Products' }],
  filters: []
};
```

### Number Filtering through Code

Number filtering displays records based on number values. Configure similarly to text filtering:

* `name`: Sets the field name
* `type`: Sets the filter type as **Number**
* `condition`: Defines the operator (Equals, GreaterThan, LessThan, Between, etc.)
* `value1`: Sets the start value
* `value2`: Sets the end value (for Between, NotBetween operators)

> Number filtering is enabled only when the field contains the **number** format.

**Number Filter Operators:**

| Operator | Description |
|----------|-------------|
| Equals | Matches the number |
| DoesNotEquals | Does not match the number |
| GreaterThan | Greater than the number |
| GreaterThanOrEqualTo | Greater than or equal |
| LessThan | Lesser than the number |
| LessThanOrEqualTo | Lesser than or equal |
| Between | Between start and end numbers |
| NotBetween | Not between start and end numbers |

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: pivotData as IDataSet[],
  expandAll: false,
  allowLabelFilter: true,
  filterSettings: [{ name: 'Amount', type: 'Number', condition: 'LessThan', value1: '40000' }],
  columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }],
  rows: [{ name: 'Amount', caption: 'Sold Amount' }],
  filters: [{ name: 'Country' }, { name: 'Products' }]
};
```

## Value Filtering

### Overview

Value filtering performs filtering operations based on the aggregate values. For example, to show data where the total sum of units sold for each country exceeds 2000, apply a value filter with condition **GreaterThan** and value **2000** on the country field.

Enable with the `allowValueFilter` property set to **true**.

### Programmatic Value Filtering

Configure value filtering through the `filterSettings` property. The required settings are:

* `name`: Sets the normal field name
* `type`: Sets the filter type as **Value**
* `measure`: Sets the value field name
* `condition`: Sets the operator type
* `value1`: Sets the start value
* `value2`: Sets the end value (for Between and NotBetween operators only)

**Value Filter Operators:**

| Operator | Description |
|----------|-------------|
| Equals | Matches the value |
| DoesNotEquals | Does not match the value |
| GreaterThan | Value is greater |
| GreaterThanOrEqualTo | Value is greater than or equal |
| LessThan | Value is lesser |
| LessThanOrEqualTo | Value is lesser than or equal |
| Between | Between start and end values |
| NotBetween | Not between start and end values |

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: pivotData as IDataSet[],
  expandAll: false,
  allowValueFilter: true,
  drilledMembers: [{ name: 'Country', items: ['France'] }],
  filterSettings: [{ name: 'Country', measure: 'Sold', type: 'Value', condition: 'GreaterThan', value1: '2000' }],
  columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
  rows: [{ name: 'Country' }, { name: 'Products' }],
  filters: []
};
```

## Member Sorting

### Overview

Member sorting enables you to arrange field members in the rows and columns of a pivot table in either **ascending** or **descending** order. By default, field members are sorted in ascending order.

Enable with the `enableSorting` property set to **true** (default: true).

### Configuring Member Sorting

Configure during initial rendering using the `sortSettings` property. Required settings:

* `name`: Specifies the name of the field to sort
* `order`: Defines the sort direction (**Ascending**, **Descending**, or **None**)

```typescript
import { GroupingBar, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function MemberSortExample() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    enableSorting: true,
    sortSettings: [{ name: 'Country', order: 'Descending' }],
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
      showGroupingBar={true}
      enableSorting={true}
      dataSourceSettings={dataSourceSettings}
    >
      <Inject services={[GroupingBar]} />
    </PivotViewComponent>
  );
}

export default MemberSortExample;
```

> By default, `enableSorting` is set to **true**. If you set it to **false**, field members arrange as they appear in the data source, and sort icons are removed from the grouping bar and field list.

### Alphanumeric Sorting

Set the `dataType` property to **number** for a specific field to sort members numerically based on numbers at the beginning of their names:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: alphanumericData as IDataSet[],
  rows: [{ name: 'ProductID', dataType: 'number' }],  // ← Numeric sorting
  columns: [{ name: 'Country' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
  formatSettings: [{ name: 'Amount', format: 'C0' }],
  filters: []
};
```

This enables correct numerical sequence (36-SW, 71-AJ, 209-FB) instead of alphabetical order (209-FB, 36-SW, 71-AJ).

## Custom Sorting

### Overview

Custom sorting allows you to sort field members in a user-defined order rather than alphabetical or numerical sequence. Configure using the `sortSettings` property with the `membersOrder` array.

### Configuring Custom Sorting

Required properties:

* `name`: Specifies the field name to apply custom sorting
* `membersOrder`: An array of member values in the user-defined sequence
* `order`: Determines if the member array is arranged in ascending or descending order

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
  dataSource: pivotData as IDataSet[],
  expandAll: false,
  enableSorting: true,
  sortSettings: [
    { name: 'Country', order: 'Ascending', membersOrder: ['United Kingdom', 'France'] },
    { name: 'Year', order: 'Descending', membersOrder: ['FY 2015', 'FY 2017'] }
  ],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
  rows: [{ name: 'Country' }, { name: 'Products' }],
  filters: []
};
```

## Value Sorting

### Overview

Value sorting allows users to sort a specific value field and its aggregated values in the row or column axis, in ascending or descending order. Enable with the `enableValueSorting` property set to **true**.

Once enabled, users can sort values by clicking the header of a value field in the pivot table's row or column axis.

### Configuring Value Sorting

Configure programmatically using the `valueSortSettings` option. Required settings:

* `headerText`: Set header names with delimiters, arranged from Level 1 to Level N
* `headerDelimiter`: Sets the delimiter string to separate header text between levels
* `sortOrder`: Sets the sort direction of the value field

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
  dataSource: pivotData as IDataSet[],
  expandAll: false,
  enableValueSorting: true,
  valueSortSettings: {
    headerText: 'FY 2015##Sold Amount',  // ← Header path with delimiter
    headerDelimiter: '##',
    sortOrder: 'Descending'
  },
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
  rows: [{ name: 'Country' }, { name: 'Products' }],
  filters: []
};
```

> Value fields are set to the column axis by default. Place value fields in the row axis to perform row-wise value sorting.

## Performance Optimization

### Member Display Limits

For large datasets, control the number of displayed members:

```typescript
<PivotViewComponent
  maxNodeLimitInMemberEditor={500}  // ← Show 500 members initially
  showFieldList={true}
>
  <Inject services={[VirtualScroll, FieldList]} />
</PivotViewComponent>
```

### On-Demand Loading (OLAP)

Load members only when needed rather than all at once:

```typescript
<PivotViewComponent
  loadOnDemandInMemberEditor={true}  // ← Default behavior
  showFieldList={true}
>
  <Inject services={[FieldList]} />
</PivotViewComponent>
```

### Level-Based Loading (OLAP)

Specify level depth for initial member loading:

```typescript
filterSettings: [
  {
    name: '[Customer].[Customer Geography]',
    levelCount: 2  // ← Load Country and State-Province only
  }
]
```

## Properties Reference

### Member Filtering Properties

| Property | Type | Description |
|----------|------|-------------|
| `allowMemberFilter` | boolean | Enables member filtering (default: true) |
| `filterSettings` | FilterModel[] | Array of filter criteria |
| `filterSettings.name` | string | Field name for filtering |
| `filterSettings.type` | 'Include' \| 'Exclude' | Filter type |
| `filterSettings.items` | string[] | Members to include/exclude |
| `filterSettings.levelCount` | number | Hierarchy depth (OLAP only) |
| `maxNodeLimitInMemberEditor` | number | Members displayed initially (default: 1000) |
| `loadOnDemandInMemberEditor` | boolean | Load members on-demand (OLAP, default: true) |

### Label Filtering Properties

| Property | Type | Description |
|----------|------|-------------|
| `allowLabelFilter` | boolean | Enables label filtering (default: false) |
| `filterSettings.type` | 'Label' | Filter type for label filtering |
| `filterSettings.condition` | string | Operator (Equals, Contains, Between, etc.) |
| `filterSettings.value1` | string \| number \| Date | Primary filter value |
| `filterSettings.value2` | string \| number \| Date | Secondary value (Between operators) |

### Value Filtering Properties

| Property | Type | Description |
|----------|------|-------------|
| `allowValueFilter` | boolean | Enables value filtering (default: false) |
| `filterSettings.type` | 'Value' | Filter type for value filtering |
| `filterSettings.measure` | string | Measure field name for value filtering |
| `filterSettings.condition` | string | Operator (GreaterThan, LessThan, Between, etc.) |
| `filterSettings.value1` | number | Start value |
| `filterSettings.value2` | number | End value (Between operators) |

### Member Sorting Properties

| Property | Type | Description |
|----------|------|-------------|
| `enableSorting` | boolean | Enables member sorting (default: true) |
| `sortSettings` | SortModel[] | Array of sort criteria |
| `sortSettings.name` | string | Field name to sort |
| `sortSettings.order` | 'Ascending' \| 'Descending' \| 'None' | Sort direction |
| `sortSettings.membersOrder` | string[] | Custom member order |
| `dataType` | 'string' \| 'number' | Field data type for sorting |

### Value Sorting Properties

| Property | Type | Description |
|----------|------|-------------|
| `enableValueSorting` | boolean | Enables value sorting (default: false) |
| `valueSortSettings` | ValueSortSettingsModel | Value sort configuration |
| `valueSortSettings.headerText` | string | Header path with delimiters |
| `valueSortSettings.headerDelimiter` | string | Delimiter for header levels |
| `valueSortSettings.sortOrder` | 'Ascending' \| 'Descending' | Sort direction |
