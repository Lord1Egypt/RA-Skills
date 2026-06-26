# Value Filtering Reference - Syncfusion React Pivot Table

## Overview

Value filtering enables filtering of pivot table rows and columns based on aggregated measure values (Sum, Average, Count, etc.) rather than field labels or member names. This feature is powerful for isolating data that meets specific numeric criteria, such as showing only regions with sales above a threshold or products with average quantities below a target.

### Key Features
- **Filter by Aggregated Values**: Filter based on Sum, Average, Count, Min, Max, etc.
- **Flexible Operators**: Supports range and comparison operators
- **Multi-Field Support**: Filter by one or more value fields
- **UI-Based Filtering**: Built-in filter dialog in Field List
- **Conditional Analysis**: Quickly identify outliers and trends
- **Performance Optimized**: Efficient filtering on calculated aggregates

## Enabling Value Filtering

### Basic Setup

To enable value filtering, set `allowValueFilter` to **true**:

```typescript
import { PivotViewComponent, FieldList, ValueFilter, Inject } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales', caption: 'Total Sales' }]
  };

  return (
    <PivotViewComponent
      id="PivotView"
      dataSourceSettings={dataSourceSettings}
      allowValueFilter={true}
      showFieldList={true}
      height={350}
    >
      <Inject services={[FieldList, ValueFilter]} />
    </PivotViewComponent>
  );
}

export default App;
```

## Value Filtering Operators

| Operator | Description | Use Case |
|----------|-------------|----------|
| `Equals` | Value equals exactly | Sales = $50,000 |
| `NotEquals` | Value does not equal | Sales ≠ $25,000 |
| `GreaterThan` | Value greater than | Sales > $100,000 |
| `GreaterThanOrEqualTo` | Value >= threshold | Sales >= $50,000 |
| `LessThan` | Value less than | Sales < $10,000 |
| `LessThanOrEqualTo` | Value <= threshold | Sales <= $100,000 |
| `Between` | Value within range | Sales between $25K-$100K |
| `NotBetween` | Value outside range | Sales not between $0-$5K |
| `Top10` | Top N values | Top 10 countries by sales |
| `Bottom10` | Bottom N values | Bottom 5 products by average |
| `Top10Percent` | Top N percent | Top 10% by revenue |
| `Bottom10Percent` | Bottom N percent | Bottom 10% by quantity |
| `Top10Sum` | Top N by cumulative | Top 10 by total sales sum |
| `Bottom10Sum` | Bottom N by cumulative | Bottom 5 by total |

## Basic Value Filtering

### Filter by Single Value Threshold

```typescript
import { PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales' }],
    // Filter rows where Sales > 50000
    filterSettings: [
      {
        name: 'Sales',
        type: 'Value',
        condition: 'GreaterThan',
        value1: '50000'
      }
    ]
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      allowValueFilter={true}
    />
  );
}

export default App;
```

### Range Value Filtering

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: pivotData as IDataSet[],
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Product' }],
  values: [{ name: 'Sales' }],
  // Filter to show only countries with sales between 25K and 100K
  filterSettings: [
    {
      name: 'Sales',
      type: 'Value',
      condition: 'Between',
      value1: '25000',
      value2: '100000'
    }
  ]
};
```

## Top/Bottom N Filtering

### Top N Values

```typescript
function TopCountriesByRevenue() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: salesData as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Year' }],
    values: [{ name: 'Revenue' }],
    // Show top 10 countries by revenue
    filterSettings: [
      {
        name: 'Revenue',
        type: 'Value',
        condition: 'Top10',
        value1: '10'
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

export default TopCountriesByRevenue;
```

### Bottom N Values

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: data as IDataSet[],
  rows: [{ name: 'Product' }],
  columns: [{ name: 'Quarter' }],
  values: [{ name: 'Units' }],
  formatSettings: [
    { name: 'Units', format: 'N0' }
  ],
  // Show bottom 5 products by units sold
  filterSettings: [
    {
      name: 'Units',
      type: 'Value',
      condition: 'Bottom10',
      value1: '5'
    }
  ]
};
```

## Percentage-Based Filtering

### Top/Bottom Percentage

```typescript
function TopPercentFiltering() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: data as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales' }],
    // Show only top 20% performers
    filterSettings: [
      {
        name: 'Sales',
        type: 'Value',
        condition: 'Top10Percent',
        value1: '20'  // Top 20%
      }
    ]
  };

  return (
    <PivotViewComponent dataSourceSettings={dataSourceSettings} />
  );
}
```

## Advanced Value Filtering

### Multiple Field Filtering

```typescript
function MultiFieldValueFilter() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: data as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [
      { name: 'Sales', caption: 'Total Sales' },
      { name: 'Units', caption: 'Units Sold' }
    ],
    // Filter by multiple value columns
    filterSettings: [
      {
        name: 'Sales',
        type: 'Value',
        condition: 'GreaterThan',
        value1: '50000'  // Sales > 50K
      },
      {
        name: 'Units',
        type: 'Value',
        condition: 'GreaterThan',
        value1: '1000'   // Units > 1000
      }
    ]
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      allowValueFilter={true}
    />
  );
}
```

### Column-Level Value Filtering

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: data as IDataSet[],
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Year' }, { name: 'Quarter' }],
  values: [{ name: 'Sales' }],
  // Filter specific column combinations
  filterSettings: [
    {
      name: 'Sales',
      type: 'Value',
      condition: 'GreaterThan',
      value1: '100000',
      axis: 'Column'  // Filter on column totals
    }
  ]
};
```

## Value Filter Dialog

### Interactive Filter Customization

```typescript
function InteractiveValueFilter() {
  let pivotObj: PivotViewComponent;
  const [filterValue, setFilterValue] = React.useState(50000);
  const [operator, setOperator] = React.useState('GreaterThan');

  const applyFilter = (): void => {
    if (pivotObj && pivotObj.dataSourceSettings) {
      pivotObj.dataSourceSettings.filterSettings = [
        {
          name: 'Sales',
          type: 'Value',
          condition: operator,
          value1: filterValue.toString()
        }
      ];
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '15px' }}>
        <label>Operator: </label>
        <select value={operator} onChange={(e) => setOperator(e.target.value)}>
          <option value="GreaterThan">Greater Than</option>
          <option value="LessThan">Less Than</option>
          <option value="Between">Between</option>
          <option value="Top10">Top 10</option>
          <option value="Bottom10">Bottom 10</option>
        </select>
      </div>
      <div style={{ marginBottom: '15px' }}>
        <label>Value: </label>
        <input
          type="number"
          value={filterValue}
          onChange={(e) => setFilterValue(parseInt(e.target.value))}
        />
      </div>
      <button onClick={applyFilter}>Apply Filter</button>
      <PivotViewComponent
        ref={(d: PivotViewComponent) => pivotObj = d}
        dataSourceSettings={dataSourceSettings}
        allowValueFilter={true}
      />
    </div>
  );
}
```

## Practical Examples

### Example 1: Show Only High-Performing Regions

```typescript
import { IDataSet } from '@syncfusion/ej2-react-pivotview';

function HighPerformingRegions() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: [
      { Region: 'North', Sales: 150000 },
      { Region: 'South', Sales: 45000 },
      { Region: 'East', Sales: 120000 },
      { Region: 'West', Sales: 30000 },
      { Region: 'Central', Sales: 200000 }
    ] as IDataSet[],
    rows: [{ name: 'Region' }],
    values: [{ name: 'Sales', caption: 'Total Sales' }],
    // Show only regions with sales > $100,000
    filterSettings: [
      {
        name: 'Sales',
        type: 'Value',
        condition: 'GreaterThan',
        value1: '100000'
      }
    ]
  };

  return (
    <PivotViewComponent
      id="high-performers"
      dataSourceSettings={dataSourceSettings}
      allowValueFilter={true}
      height={300}
    >
      <Inject services={[ValueFilter]} />
    </PivotViewComponent>
  );
}

export default HighPerformingRegions;
```

### Example 2: Top 10 Products by Revenue

```typescript
function TopProductsReport() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: productData as IDataSet[],
    rows: [{ name: 'Product' }],
    columns: [{ name: 'Category' }],
    values: [
      { name: 'Revenue', caption: 'Total Revenue', format: 'C2' },
      { name: 'Units', caption: 'Units Sold', format: 'N0' }
    ],
    // Show top 10 products by revenue
    filterSettings: [
      {
        name: 'Revenue',
        type: 'Value',
        condition: 'Top10',
        value1: '10'
      }
    ]
  };

  return (
    <PivotViewComponent
      id="top-products"
      dataSourceSettings={dataSourceSettings}
      allowValueFilter={true}
      showFieldList={true}
      height={500}
    >
      <Inject services={[FieldList, ValueFilter]} />
    </PivotViewComponent>
  );
}

export default TopProductsReport;
```

### Example 3: Filter by Average Value Range

```typescript
function AverageValueRange() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: salesData as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [
      { name: 'Amount', caption: 'Sales Amount' }
    ],
    // Filter to show countries averaging between $50K-$150K per product
    filterSettings: [
      {
        name: 'Amount',
        type: 'Value',
        condition: 'Between',
        value1: '50000',
        value2: '150000'
      }
    ]
  };

  return (
    <PivotViewComponent
      id="avg-range"
      dataSourceSettings={dataSourceSettings}
      height={400}
    />
  );
}

export default AverageValueRange;
```

## Performance Considerations

1. **Top/Bottom Filtering**: Computed efficiently even on large datasets
2. **Range Filters**: Generally faster than multiple conditions
3. **Percentage Filtering**: Requires full data scan but still efficient
4. **Multiple Value Fields**: Each adds slight overhead

```typescript
// Optimize by filtering data before pivot
const filteredData = rawData.filter(item => item.Sales > 50000);

<PivotViewComponent
  dataSourceSettings={{
    dataSource: filteredData as IDataSet[],  // Pre-filtered data
    rows: [{ name: 'Country' }],
    values: [{ name: 'Sales' }]
  }}
  allowValueFilter={true}
/>
```

## Best Practices

✅ **Do:**
- Use Top/Bottom N for comparative analysis (outlier identification)
- Combine with member filtering for multi-criteria analysis
- Use range filtering for excluding outliers
- Apply value filters after evaluating all aggregations
- Use clear thresholds aligned with business metrics

❌ **Don't:**
- Filter out all data with overly restrictive thresholds
- Use value filtering where label filtering is more appropriate
- Apply excessive value filters without understanding data distribution
- Forget to consider which value field is being filtered

## Common Issues

**Filter excludes all rows?**
- Verify threshold values are within data range
- Check data aggregation (Sum vs Avg vs Count)
- Review format settings (currency might have $ sign)

**Unexpected results with Top/Bottom?**
- Verify N value is appropriate for your dataset
- Check if ties exist (multiple values at threshold)
- Consider total row/column counts

**Performance slow?**
- Simplify filter conditions
- Use pre-filtered data when possible
- Consider server-side filtering for OLAP data

## Related Features

- **Label Filtering**: Filter by field headers/text
- **Member Filtering**: Filter by exact member values
- **Value Sorting**: Sort by measure values
- **Conditional Formatting**: Highlight cells meeting value criteria
