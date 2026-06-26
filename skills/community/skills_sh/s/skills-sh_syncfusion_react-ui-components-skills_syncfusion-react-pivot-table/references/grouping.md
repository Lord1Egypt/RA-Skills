# Data Grouping

## Table of Contents
- [Overview](#overview)
- [Enable Grouping Feature](#enable-grouping-feature)
- [Number Grouping](#number-grouping)
- [Date Grouping](#date-grouping)
- [Programmatic Configuration](#programmatic-configuration)
- [Ungrouping Data](#ungrouping-data)

## Overview

Grouping organizes data into meaningful categories. The PivotView supports grouping for:
- **Numbers**: Range-based grouping (1-5, 6-10, etc.)
- **Dates**: Hierarchical grouping (Year, Quarter, Month, Day, Hour, Minute, Second)
- **Custom**: User-defined grouping rules

> This feature applies only to relational data sources.

## Enable Grouping Feature

Enable grouping by setting the `allowGrouping` property to `true` and injecting the `Grouping` module:

```typescript
import { PivotViewComponent, GroupingBar, Grouping, Inject } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: data as IDataSet[],
    rows: [{ name: 'Date', caption: 'Date' }],
    columns: [{ name: 'Product_ID', caption: 'Product ID' }],
    values: [{ name: 'Sold', caption: 'Unit Sold' }]
  };

  return (
    <PivotViewComponent
      allowGrouping={true}
      showGroupingBar={true}
      dataSourceSettings={dataSourceSettings}
    >
      <Inject services={[GroupingBar, Grouping]} />
    </PivotViewComponent>
  );
}
```

### UI Grouping
Right-click on any row or column header and select **Group** to open the grouping dialog. Configure options and click **OK**. To ungroup, right-click the grouped header and select **Ungroup**.

## Number Grouping

Group numeric data by ranges and intervals.

### Basic Number Grouping

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: data as IDataSet[],
  rows: [{ name: 'Product_ID', caption: 'Product ID' }],
  columns: [{ name: 'Products' }],
  values: [{ name: 'Sold', caption: 'Unit Sold' }],
  groupSettings: [
    {
      name: 'Product_ID',
      type: 'Number',
      rangeInterval: 2  // Groups as 1001-1002, 1003-1004, etc.
    }
  ]
};
```

### Range Selection

Limit grouping to a specific range:

```typescript
groupSettings: [
  {
    name: 'Product_ID',
    type: 'Number',
    rangeInterval: 2,
    startingAt: 1004,  // Start grouping from 1004
    endingAt: 1008     // End grouping at 1008
    // Values outside range grouped as "Out of Range"
  }
]
```

**Key Properties**:
- `rangeInterval`: Interval between groups (e.g., 2 creates 1001-1002, 1003-1004)
- `startingAt`: First number in range
- `endingAt`: Last number in range

## Date Grouping

Organize date/time data hierarchically.

### Basic Date Grouping

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: data as IDataSet[],
  rows: [{ name: 'Date' }],
  columns: [{ name: 'Product_Categories', caption: 'Product Categories' }],
  values: [{ name: 'Sold', caption: 'Unit Sold' }],
  groupSettings: [
    {
      name: 'Date',
      type: 'Date',
      dateInterval: ['Years', 'Months']  // Hierarchical grouping
    }
  ]
};
```

### Available Date Intervals

Group dates by any combination of:
- Years
- Quarters
- Months
- Days
- Hours
- Minutes
- Seconds

**Example**: Group by year first, then by month within each year:

```typescript
groupSettings: [
  {
    name: 'Date',
    type: 'Date',
    dateInterval: ['Years', 'Months']
  }
]
```

## Programmatic Configuration

Configure grouping through code using the `groupSettings` property:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: groupData as IDataSet[],
  rows: [{ name: 'Date' }],
  columns: [{ name: 'Product_Categories' }],
  values: [
    { name: 'Sold', caption: 'Unit Sold' },
    { name: 'Amount', caption: 'Sold Amount' }
  ],
  groupSettings: [
    {
      name: 'Product_ID',
      type: 'Number',
      rangeInterval: 5,
      startingAt: 1001,
      endingAt: 1010
    },
    {
      name: 'Date',
      type: 'Date',
      dateInterval: ['Years', 'Months']
    }
  ]
};
```

## Ungrouping Data

### UI Ungrouping
Right-click on a grouped header and select **Ungroup** to remove grouping.

### Programmatic Ungrouping
Remove grouping by clearing or updating the `groupSettings`:

```typescript
// Clear all grouping
dataSourceSettings.groupSettings = [];

// Or update pivot instance
pivotObj.dataSourceSettings.groupSettings = [];
```

## Common Patterns

### Pattern 1: Number Ranges
```typescript
groupSettings: [
  {
    name: 'ProductID',
    type: 'Number',
    rangeInterval: 10,  // 1-10, 11-20, 21-30, etc.
    startingAt: 1,
    endingAt: 100
  }
]
```

### Pattern 2: Multi-Level Date Grouping
```typescript
groupSettings: [
  {
    name: 'OrderDate',
    type: 'Date',
    dateInterval: ['Years', 'Quarters', 'Months']  // Year > Quarter > Month
  }
]
```

### Pattern 3: Mixed Grouping
```typescript
groupSettings: [
  { name: 'Date', type: 'Date', dateInterval: ['Years', 'Months'] },
  { name: 'Quantity', type: 'Number', rangeInterval: 5 }
]
```

## Important Notes

- Only one grouping type per field (either Number, Date, or Custom)
- Grouped fields function as individual fields and can be moved between axes
- "Out of Range" values appear automatically for number grouping with specified ranges
- Date grouping creates hierarchies that expand/collapse dynamically
