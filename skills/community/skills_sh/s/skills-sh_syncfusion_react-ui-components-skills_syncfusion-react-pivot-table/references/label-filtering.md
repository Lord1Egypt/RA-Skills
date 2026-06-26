# Label Filtering Reference - Syncfusion React Pivot Table

## Overview

Label filtering enables filtering of pivot table records based on field headers and text patterns. This feature allows users to filter by specific text, date ranges, or numeric ranges in row/column headers. Label filtering is more flexible than member filtering as it supports pattern matching (contains, starts with, ends with, etc.) rather than just exact member matches.

### Key Features
- **Text Pattern Matching**: Filter using operators like contains, starts with, ends with
- **Date Range Filtering**: Filter records within or outside date ranges
- **Numeric Range Filtering**: Filter by numeric value ranges
- **UI-Based Filtering**: Built-in filter dialog in Field List
- **Flexible Operators**: Supports 12+ comparison operators
- **Multiple Conditions**: Apply multiple filters to different fields

## Enabling Label Filtering

### Basic Setup

To enable label filtering, set `allowLabelFilter` to **true**:

```typescript
import { PivotViewComponent, FieldList, LabelFilter, Inject } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales' }],
    allowLabelFilter: true
  };

  return (
    <PivotViewComponent
      id="PivotView"
      dataSourceSettings={dataSourceSettings}
      showFieldList={true}
      height={350}
    >
      <Inject services={[FieldList, LabelFilter]} />
    </PivotViewComponent>
  );
}

export default App;
```

## Filtering Operators

### Text Filtering Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `Equals` | Exact match | Country = "USA" |
| `DoesNotEquals` | Does not match | Country ≠ "USA" |
| `BeginWith` | Starts with text | Country begins with "U" |
| `DoesNotBeginWith` | Does not start with | Product does not begin with "L" |
| `EndsWith` | Ends with text | Country ends with "A" |
| `DoesNotEndsWith` | Does not end with | Product does not end with "s" |
| `Contains` | Text contains substring | Product contains "top" |
| `DoesNotContains` | Text does not contain | Product does not contain "phone" |
| `GreaterThan` | Text comparison > | "T" > "P" (ASCII) |
| `GreaterThanOrEqualTo` | Text comparison >= | "USA" >= "Canada" |
| `LessThan` | Text comparison < | "Apple" < "Banana" |
| `LessThanOrEqualTo` | Text comparison <= | "Mobile" <= "Tablet" |
| `Between` | Range between two values | 2020 between 2015 and 2025 |
| `NotBetween` | Outside range | Year not between 2020 and 2022 |

## Text Label Filtering

### Simple Text Filter

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales' }],
    allowLabelFilter: true,
    // Filter rows where Country starts with 'U'
    filterSettings: [
      {
        name: 'Country',
        type: 'Label',
        condition: 'BeginWith',
        value1: 'U'
      }
    ]
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      showFieldList={true}
    />
  );
}

export default App;
```

### Multiple Text Filters

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: pivotData as IDataSet[],
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Product' }],
  values: [{ name: 'Sales' }],
  allowLabelFilter: true,
  filterSettings: [
    {
      name: 'Country',
      type: 'Label',
      condition: 'Contains',
      value1: 'United'  // Country contains "United"
    },
    {
      name: 'Product',
      type: 'Label',
      condition: 'DoesNotContains',
      value1: 'phone'   // Product does not contain "phone"
    }
  ]
};
```

### Range Filtering

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: pivotData as IDataSet[],
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Product' }],
  values: [{ name: 'Sales' }],
  allowLabelFilter: true,
  filterSettings: [
    {
      name: 'Country',
      type: 'Label',
      condition: 'Between',
      value1: 'Canada',
      value2: 'USA'     // Countries between Canada and USA
    }
  ]
};
```

## Date Label Filtering

### Date Range Filter

```typescript
function DateFilterExample() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: data as IDataSet[],  // Data with date fields
    rows: [{ name: 'Country' }],
    columns: [{ name: 'OrderDate' }],
    values: [{ name: 'Sales' }],
    allowLabelFilter: true,
    formatSettings: [
      {
        name: 'OrderDate',
        type: 'date',
        format: 'MM/dd/yyyy'
      }
    ],
    filterSettings: [
      {
        name: 'OrderDate',
        type: 'Date',
        condition: 'Between',
        value1: new Date(2023, 0, 1),    // January 1, 2023
        value2: new Date(2023, 11, 31)   // December 31, 2023
      }
    ]
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
    />
  );
}
```

### Date Operators

| Operator | Description |
|----------|-------------|
| `Equals` | Records on specific date |
| `DoesNotEquals` | Records not on specific date |
| `Before` | Records before given date |
| `BeforeOrEqualTo` | Records before or on given date |
| `After` | Records after given date |
| `AfterOrEqualTo` | Records after or on given date |
| `Between` | Records within date range |
| `NotBetween` | Records outside date range |

## Number Label Filtering

### Numeric Range Filter

```typescript
function NumericFilterExample() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: data as IDataSet[],
    rows: [{ name: 'Year' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales' }],
    allowLabelFilter: true,
    filterSettings: [
      {
        name: 'Year',
        type: 'Number',
        condition: 'Between',
        value1: 2020,
        value2: 2024  // Years between 2020 and 2024
      }
    ]
  };

  return (
    <PivotViewComponent dataSourceSettings={dataSourceSettings} />
  );
}
```

### Numeric Operators

| Operator | Description |
|----------|-------------|
| `Equals` | Exact numeric match |
| `DoesNotEquals` | Not equal to value |
| `GreaterThan` | Greater than value |
| `GreaterThanOrEqualTo` | Greater than or equal |
| `LessThan` | Less than value |
| `LessThanOrEqualTo` | Less than or equal |
| `Between` | Within numeric range |
| `NotBetween` | Outside numeric range |

## Label Filter Dialog UI

### Accessing Filter Dialog

Users can access the label filter dialog by clicking the filter icon in the Field List:

```typescript
// Automatically available in Field List when allowLabelFilter={true}
// Steps for user:
// 1. Click filter icon next to field in Field List
// 2. Select filtering type (Label, Date, Number)
// 3. Choose operator and enter values
// 4. Click Apply
```

### Programmatic Filter Dialog

```typescript
function ProgrammaticFilter() {
  let pivotObj: PivotViewComponent;

  const openFilterDialog = (): void => {
    // Trigger filter dialog programmatically
    if (pivotObj) {
      // Access field list to open filter
      const fieldListObj = (pivotObj as any).fieldList;
      if (fieldListObj) {
        // Dialog opens automatically when filter icon is clicked
      }
    }
  };

  return (
    <div>
      <button onClick={openFilterDialog}>Add Filter</button>
      <PivotViewComponent
        ref={(d: PivotViewComponent) => pivotObj = d}
        dataSourceSettings={dataSourceSettings}
        showFieldList={true}
      />
    </div>
  );
}
```

## Dynamic Filter Management

### Add/Remove Filters Programmatically

```typescript
function DynamicFiltering() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales' }],
    allowLabelFilter: true
  };

  let pivotObj: PivotViewComponent;

  const addFilter = (): void => {
    if (pivotObj && pivotObj.dataSourceSettings) {
      const currentFilters = pivotObj.dataSourceSettings.filterSettings || [];
      
      const newFilter = {
        name: 'Country',
        type: 'Label',
        condition: 'Contains',
        value1: 'United'
      };

      pivotObj.dataSourceSettings.filterSettings = [...currentFilters, newFilter];
    }
  };

  const clearAllFilters = (): void => {
    if (pivotObj && pivotObj.dataSourceSettings) {
      pivotObj.dataSourceSettings.filterSettings = [];
    }
  };

  return (
    <div>
      <button onClick={addFilter}>Add Filter</button>
      <button onClick={clearAllFilters}>Clear Filters</button>
      <PivotViewComponent
        ref={(d: PivotViewComponent) => pivotObj = d}
        dataSourceSettings={dataSourceSettings}
      />
    </div>
  );
}
```

## Practical Examples

### Example 1: Filter Products Containing "Laptop"

```typescript
import { IDataSet } from '@syncfusion/ej2-react-pivotview';

function FilterLaptops() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: [
      { Country: 'USA', Product: 'Laptop Pro', Sales: 5000 },
      { Country: 'USA', Product: 'Laptop Air', Sales: 3000 },
      { Country: 'USA', Product: 'Mobile X', Sales: 2000 },
      { Country: 'Canada', Product: 'Laptop Pro', Sales: 2500 },
      { Country: 'Canada', Product: 'Tablet', Sales: 1500 }
    ] as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales' }],
    allowLabelFilter: true,
    filterSettings: [
      {
        name: 'Product',
        type: 'Label',
        condition: 'Contains',
        value1: 'Laptop'  // Only show products containing "Laptop"
      }
    ]
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      showFieldList={true}
    />
  );
}

export default FilterLaptops;
```

### Example 2: Filter Years Within Range

```typescript
function FilterYearRange() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: salesData as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Year' }],
    values: [{ name: 'Sales' }],
    allowLabelFilter: true,
    filterSettings: [
      {
        name: 'Year',
        type: 'Number',
        condition: 'Between',
        value1: 2020,
        value2: 2023  // Only show years 2020-2023
      }
    ]
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      height={400}
    />
  );
}

export default FilterYearRange;
```

### Example 3: Complex Multi-Filter

```typescript
function ComplexFiltering() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: data as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales' }],
    allowLabelFilter: true,
    filterSettings: [
      {
        name: 'Country',
        type: 'Label',
        condition: 'BeginWith',
        value1: 'U'  // Countries starting with "U"
      },
      {
        name: 'Product',
        type: 'Label',
        condition: 'DoesNotContains',
        value1: 'old'  // Products not containing "old"
      }
    ]
  };

  return (
    <PivotViewComponent
      id="complex-filter-pivot"
      dataSourceSettings={dataSourceSettings}
      showFieldList={true}
      height={400}
    >
      <Inject services={[FieldList, LabelFilter]} />
    </PivotViewComponent>
  );
}

export default ComplexFiltering;
```

## Performance Considerations

1. **Large Datasets**: Label filters are evaluated server-side for OLAP data
2. **Pattern Matching**: Complex patterns may impact performance slightly
3. **Multiple Filters**: Each filter adds computational overhead
4. **Date Filtering**: Use closed date ranges for better performance

## Best Practices

✅ **Do:**
- Use specific operators (BeginWith, EndsWith) for better performance than Contains
- Combine label filtering with member filtering for precise results
- Use text search features in filter dialog for ease of use
- Apply filters early in analysis workflow
- Test filter combinations before sharing reports

❌ **Don't:**
- Use overly broad filters that include almost all data
- Mix label and member filtering without understanding interaction
- Create circular filtering conditions
- Apply excessive pattern matching on very large datasets

## Common Issues

**Filter not applying?**
- Verify the filter field exists in data
- Check that operator and values are valid
- Ensure data types match (text vs number vs date)

**Performance degradation?**
- Simplify filter conditions
- Use specific operators instead of pattern matching
- Consider server-side filtering for OLAP data

**Unexpected filter results?**
- Verify filter criteria match expected data values
- Check case sensitivity (product vs Product)
- Review data format (dates might be strings)

## Related Features

- **Member Filtering**: Filter by exact member values
- **Value Filtering**: Filter by aggregated measure values
- **Field List**: UI for managing filters
- **Data Formatting**: Format fields for consistent filtering
