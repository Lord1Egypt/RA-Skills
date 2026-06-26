# Value Sorting Reference - Syncfusion React Pivot Table

## Overview

Value sorting allows sorting individual columns or rows based on their values in ascending or descending order. Enable by setting `enableValueSorting` to **true** on the component.

## Enabling Value Sorting

### Basic Setup

```typescript
import { PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { IDataSet } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    valueSortSettings: {
      headerText: 'FY 2015##Sold Amount',
      headerDelimiter: '##',
      sortOrder: 'Descending'
    },
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
      id="PivotView"
      height={350}
      enableValueSorting={true}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

## valueSortSettings Properties

### Single Axis Sorting (Basic)

| Property | Description |
|----------|-------------|
| `headerText` | Column header names with delimiter (e.g., 'FY 2015##Sold Amount') |
| `headerDelimiter` | Delimiter string to separate header text |
| `sortOrder` | Sort direction: **Ascending** or **Descending** |

### Multiple Axis Sorting (Advanced)

| Property | Description |
|----------|-------------|
| `columnHeaderText` | Column header hierarchy with delimiter (e.g., 'FY 2015##Units Sold') |
| `headerDelimiter` | Delimiter string to separate header text |
| `columnSortOrder` | Sort direction for the column header |
| `rowHeaderText` | Specific row header to sort (e.g., 'France') |
| `rowSortOrder` | Sort direction for the row header |

## How headerText Works

The `headerText` format is: `{ColumnHeaderLevel1}##...##{ValueFieldCaption}`

Examples:
- `'FY 2015##Sold Amount'` - Sort by 'Sold Amount' for column header 'FY 2015'
- `'FY 2015##Q1##Units Sold'` - Sort by 'Units Sold' for column headers 'FY 2015' and 'Q1'

## Multiple Axis Sorting

Sort by both column and row values simultaneously:

```typescript
let dataSourceSettings: DataSourceSettingsModel = {
  dataSource: pivotData as IDataSet[],
  valueSortSettings: {
    columnHeaderText: 'FY 2015##Units Sold',
    headerDelimiter: '##',
    columnSortOrder: 'Descending',
    rowHeaderText: 'France',
    rowSortOrder: 'Ascending',
  },
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Year' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
};
```

## Programmatic Value Sorting

### Sort by Specific Header

```typescript
let dataSourceSettings: DataSourceSettingsModel = {
  dataSource: pivotData as IDataSet[],
  valueSortSettings: {
    headerText: 'France##Sold Amount',
    headerDelimiter: '##',
    sortOrder: 'Descending'
  },
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Year' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
};
```

### Change Sort Order

```typescript
// Ascending order
valueSortSettings: {
  headerText: 'France##Sold Amount',
  headerDelimiter: '##',
  sortOrder: 'Ascending'
}

// Descending order
valueSortSettings: {
  headerText: 'France##Sold Amount',
  headerDelimiter: '##',
  sortOrder: 'Descending'
}
```

### Dynamic Sort Change

```typescript
function DynamicValueSort() {
  let pivotObj: PivotViewComponent;

  const applySort = (headerText: string, order: 'Ascending' | 'Descending'): void => {
    if (pivotObj && pivotObj.dataSourceSettings) {
      pivotObj.dataSourceSettings.valueSortSettings = {
        headerText: headerText,
        headerDelimiter: '##',
        sortOrder: order
      };
    }
  };

  return (
    <div>
      <button onClick={() => applySort('France##Sold Amount', 'Descending')}>
        Sort France by Sold Amount (High to Low)
      </button>
      <button onClick={() => applySort('Germany##Sold Amount', 'Ascending')}>
        Sort Germany by Sold Amount (Low to High)
      </button>
      <PivotViewComponent
        ref={(d: PivotViewComponent) => pivotObj = d}
        id="PivotView"
        height={350}
        enableValueSorting={true}
        dataSourceSettings={dataSourceSettings}
      />
    </div>
  );
}
```

## Interactive Value Sorting

Click on column headers to sort values:

```typescript
// User clicks column header → Pivot sorts by that column value
// Click again → Toggle between Ascending and Descending
```

## Format Settings with Value Sorting

When using value sorting, ensure value fields have `formatSettings`:

```typescript
let dataSourceSettings: DataSourceSettingsModel = {
  dataSource: pivotData as IDataSet[],
  formatSettings: [{ name: 'Amount', format: 'C0' }],
  valueSortSettings: {
    headerText: 'FY 2015##Sold Amount',
    headerDelimiter: '##',
    sortOrder: 'Descending'
  },
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Year' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
};
```

## Performance Tips

1. **Enable value sorting only when needed**: It adds sorting computation
2. **Use formatSettings**: Ensures consistent value display
3. **Delimiters**: Use consistent `headerDelimiter` (e.g., '##')

## Best Practices

✅ **Do:**
- Use `enableValueSorting={true}` on the PivotViewComponent
- Set `headerText` as `{ColumnHeader}##{ValueFieldCaption}`
- Use consistent `headerDelimiter` string
- Use `columnHeaderText`/`rowHeaderText` for multi-axis sorting

❌ **Don't:**
- Use `sortSettings` for value sorting - use `valueSortSettings`
- Forget to enable `enableValueSorting` on component
- Use wrong delimiter format in `headerText`
- Mix up `sortOrder` with `columnSortOrder`/`rowSortOrder`

## Common Issues

**Value sorting not working?**
- Verify `enableValueSorting={true}` is set on component
- Check `headerText` format is correct: `{ColumnHeader}##{ValueFieldCaption}`
- Ensure `headerDelimiter` matches what you use in `headerText`

**Sort doesn't change on click?**
- Verify `enableValueSorting` is enabled
- Check if `valueSortSettings` has valid values

**Wrong column sorted?**
- Verify `headerText` has correct column header and value field caption
- Check `formatSettings` for correct value field names

## Related Features

- **Sorting**: General sorting configuration
- **Label Filtering**: Filter by field labels
- **Value Filtering**: Filter by aggregated values
- **Field List**: UI for interactive configuration
