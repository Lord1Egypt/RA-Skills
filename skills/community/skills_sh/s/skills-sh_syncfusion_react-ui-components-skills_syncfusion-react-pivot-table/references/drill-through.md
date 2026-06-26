# Drill-Through Reference - Syncfusion React Pivot Table

## Overview

Drill-through is a powerful feature that allows users to inspect the raw data behind any aggregated value in the pivot table. By double-clicking on a cell, users can view all individual transactions or records that contributed to that aggregated number. This feature is essential for data verification, audit trails, and detailed analysis. The drill-through view displays data in a data grid within a popup dialog, allowing users to see column-level details and apply filters if needed.

### Key Concepts
- **Raw Data Display**: View actual transactions behind summary numbers
- **Double-Click Trigger**: Access via double-click on any value cell
- **Data Grid Interface**: Interactive grid with sorting, filtering, grouping
- **Row/Column Context**: Shows headers context for the drilled cell
- **Column Chooser**: Select which columns to display
- **Measure Information**: Shows the aggregation measure for the drilled data

## Enabling Drill-Through

### Basic Setup

To enable drill-through functionality, set `allowDrillThrough` to **true** and inject the `DrillThrough` module:

```typescript
import { PivotViewComponent, DrillThrough, Inject, IDataSet } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year' }, { name: 'Quarter' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sales' }, { name: 'Amount' }],
    dataSource: pivotData as IDataSet[]
  };

  let pivotObj: PivotViewComponent;

  return (
    <PivotViewComponent
      ref={(d: PivotViewComponent) => pivotObj = d}
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
      allowDrillThrough={true}
    >
      <Inject services={[DrillThrough]} />
    </PivotViewComponent>
  );
}

export default App;
```

**How to Use:**
1. Double-click on any value cell in the pivot table
2. A popup dialog appears showing the raw data
3. View and interact with the data grid
4. Click "Close" to dismiss the drill-through view

## Drill-Through Data Grid Display

### What Gets Displayed

When a user drill-throughs a cell, the data grid shows:

1. **Row Headers**: The dimension values for the row context
   - Example: If drilling on "USA - Laptops", shows USA and Laptops
2. **Column Headers**: The dimension values for the column context
   - Example: If drilling on "Q1 - 2020", shows Q1 and 2020
3. **Measure Column**: The actual values for the selected measure
   - Example: For "Amount" measure, shows individual transaction amounts
4. **Raw Records**: All individual transactions/records matching the filters
   - All original columns from your source data

### Popup Layout

```
┌─ Drill Through Records for [USA - Laptops - Q1 - 2020] ─┐
│                                                           │
│  Country: USA                                             │
│  Products: Laptops                                        │
│  Year: 2020                                               │
│  Quarter: Q1                                              │
│                                                           │
│  ┌─ Grid with columns: Country, Products, Date, Amount  │
│  │ USA | Laptops | 01/15/2020 | $500                   │
│  │ USA | Laptops | 01/16/2020 | $750                   │
│  │ USA | Laptops | 01/17/2020 | $600                   │
│  └─────────────────────────────────────────────────────│
│                                                           │
│  [Close] [Export] [Column Chooser]                        │
└─────────────────────────────────────────────────────────┘
```

## Drill-Through Events

### drillThrough Event

This is the primary event triggered when a cell is double-clicked for drill-through. Use it to customize the data grid display:

```typescript
const onDrillThrough = (args: PivotDrillThroughEventArgs): void => {
  // args properties:
  // - rowHeaders: The row context headers
  // - columnHeaders: The column context headers
  // - rowMembers: Selected row member values
  // - columnMembers: Selected column member values
  // - measure: The measure being drilled
  // - gridColumns: Columns to display in the grid
  
  console.log('Drilling through:', args.measure);
  console.log('Row headers:', args.rowHeaders);
  console.log('Column headers:', args.columnHeaders);
  
  // Customize grid columns to display
  args.gridColumns = [
    { field: 'Date', headerText: 'Transaction Date', width: 150 },
    { field: 'Amount', headerText: 'Sale Amount', width: 120, format: 'C2' },
    { field: 'Quantity', headerText: 'Qty', width: 80 },
    { field: 'SalesPerson', headerText: 'Sales Rep', width: 150 }
  ];
};

<PivotViewComponent
  allowDrillThrough={true}
  onDrillThrough={onDrillThrough}
>
  <Inject services={[DrillThrough]} />
</PivotViewComponent>
```

### beginDrillThrough Event

Triggered after the data grid is initialized, allowing you to configure grid-specific features:

```typescript
const onBeginDrillThrough = (args: PivotDrillThroughEventArgs): void => {
  // Configure grid sorting
  if (args.grid) {
    args.grid.sortSettings = [
      {
        field: 'Date',
        direction: 'Descending'
      }
    ];
    
    // Configure grid filtering
    args.grid.filterSettings = [
      {
        field: 'Amount',
        operator: 'greaterThan',
        value: 100
      }
    ];
    
    // Disable grid actions if needed
    args.grid.allowGrouping = false;
  }
};

<PivotViewComponent
  allowDrillThrough={true}
  onBeginDrillThrough={onBeginDrillThrough}
>
  <Inject services={[DrillThrough]} />
</PivotViewComponent>
```

## Drill-Through Configuration

### Maximum Rows Configuration

For OLAP data sources, configure the maximum number of rows to retrieve:

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  // ... other settings
  maxRowsInDrillThrough: 10000  // Default: 10000
};

// This setting applies only to OLAP sources
// For relational sources, all data is retrieved
```

## Customizing Drill-Through Grid

### Example 1: Custom Column Configuration

```typescript
const onDrillThrough = (args: PivotDrillThroughEventArgs): void => {
  args.gridColumns = [
    {
      field: 'Date',
      headerText: 'Transaction Date',
      width: 150,
      format: 'MMM dd, yyyy',
      textAlign: 'Right'
    },
    {
      field: 'Amount',
      headerText: 'Amount',
      width: 120,
      format: 'C2',
      textAlign: 'Right'
    },
    {
      field: 'Quantity',
      headerText: 'Units Sold',
      width: 100,
      textAlign: 'Center'
    },
    {
      field: 'Discount',
      headerText: 'Discount %',
      width: 100,
      format: 'P2'
    }
  ];
};
```

### Example 2: Grid Sorting and Filtering

```typescript
const onBeginDrillThrough = (args: PivotDrillThroughEventArgs): void => {
  if (args.grid) {
    // Sort by Date descending
    args.grid.sortSettings = [
      { field: 'Date', direction: 'Descending' }
    ];
    
    // Add search functionality
    args.grid.allowSearching = true;
    
    // Allow column selection
    args.grid.allowSelection = true;
    args.grid.selectionSettings = {
      type: 'Checkbox',
      mode: 'Row'
    };
  }
};
```

### Example 3: Export Drill-Through Data

```typescript
const onDrillThrough = (args: PivotDrillThroughEventArgs): void => {
  // Store data for export
  const drillData = args.data;
  
  // Add export method
  (window as any).exportDrillData = () => {
    if (args.grid) {
      args.grid.excelExport();
    }
  };
};
```

## Drill-Through with Pivot Charts

Drill-through also works with pivot chart data points:

```typescript
import { PivotChart, DrillThrough, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';

function PivotWithChartDrillThrough() {
  const onDrillThrough = (args: PivotDrillThroughEventArgs): void => {
    console.log('Drilled from chart:', args.measure);
  };

  return (
    <PivotViewComponent
      displayOption={{ view: 'Both' }}  // Show both table and chart
      allowDrillThrough={true}
      onDrillThrough={onDrillThrough}
    >
      <Inject services={[PivotChart, DrillThrough]} />
    </PivotViewComponent>
  );
}
```

## Column Chooser

The drill-through popup includes a column chooser feature that allows users to:

1. Select/deselect columns to display
2. Reorder columns
3. Hide sensitive columns if needed

```typescript
const onDrillThrough = (args: PivotDrillThroughEventArgs): void => {
  // Pre-select which columns are visible
  args.gridColumns = [
    { field: 'Date', headerText: 'Date' },           // Visible
    { field: 'Amount', headerText: 'Amount' },       // Visible
    { field: 'CustomerID', headerText: 'Cust ID' }   // Can be toggled
  ];
  
  // Hide sensitive data columns
  args.gridColumns = args.gridColumns.filter(
    col => col.field !== 'SSN' && col.field !== 'InternalNotes'
  );
};
```

## Practical Examples

### Example 1: Basic Drill-Through with Formatting

```typescript
import { PivotViewComponent, DrillThrough, Inject } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';

function BasicDrillThrough() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year' },  { name: 'Quarter' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sales', caption: 'Total Sales' }],
    dataSource: pivotData as IDataSet[],
    formatSettings: [{ name: 'Sales', format: 'C2' }]
  };

  const onDrillThrough = (args: PivotDrillThroughEventArgs): void => {
    args.gridColumns = [
      { field: 'Date', headerText: 'Date', width: 150 },
      { field: 'Product', headerText: 'Product', width: 150 },
      { field: 'Amount', headerText: 'Amount', width: 120, format: 'C2' },
      { field: 'Quantity', headerText: 'Qty', width: 80 }
    ];
  };

  return (
    <PivotViewComponent
      id='PivotView'
      dataSourceSettings={dataSourceSettings}
      allowDrillThrough={true}
      onDrillThrough={onDrillThrough}
      height={350}
    >
      <Inject services={[DrillThrough]} />
    </PivotViewComponent>
  );
}

export default BasicDrillThrough;
```

### Example 2: Advanced Drill-Through with Grid Configuration

```typescript
import { PivotViewComponent, DrillThrough, Inject } from '@syncfusion/ej2-react-pivotview';

function AdvancedDrillThrough() {
  const onDrillThrough = (args: PivotDrillThroughEventArgs): void => {
    // Customize columns
    args.gridColumns = [
      { field: 'TransactionID', headerText: 'ID', width: 80 },
      { field: 'Date', headerText: 'Date', width: 150, format: 'MMM dd, yyyy' },
      { field: 'SalesPerson', headerText: 'Sales Rep', width: 150 },
      { field: 'Amount', headerText: 'Amount', width: 120, format: 'C2', textAlign: 'Right' },
      { field: 'Discount', headerText: 'Discount', width: 100, format: 'P2' }
    ];
  };

  const onBeginDrillThrough = (args: PivotDrillThroughEventArgs): void => {
    if (args.grid) {
      // Allow sorting
      args.grid.allowSorting = true;
      
      // Allow filtering
      args.grid.allowFiltering = true;
      args.grid.filterSettings = [
        { field: 'Amount', operator: 'GreaterThan', value: 0 }
      ];
      
      // Allow pagination
      args.grid.pageSettings = { pageSize: 20 };
      
      // Style the grid
      args.grid.rowHeight = 35;
    }
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      allowDrillThrough={true}
      onDrillThrough={onDrillThrough}
      onBeginDrillThrough={onBeginDrillThrough}
      height={350}
    >
      <Inject services={[DrillThrough]} />
    </PivotViewComponent>
  );
}

export default AdvancedDrillThrough;
```

## Performance Considerations

1. **Large Datasets**: Drill-through queries on millions of rows may be slow
2. **OLAP Limits**: Use `maxRowsInDrillThrough` to limit result set size
3. **Grid Features**: Disable unnecessary grid features (grouping, editing) for performance
4. **Async Loading**: Consider pagination for very large result sets

## Best Practices

1. **User Feedback**: Show loading indicator during drill-through data fetch
2. **Clear Headers**: Display context information clearly (row/column values)
3. **Column Selection**: Show only relevant columns to reduce clutter
4. **Data Limits**: For OLAP, set reasonable maxRowsInDrillThrough values
5. **Audit Trail**: Log drill-through actions for security/compliance

## Troubleshooting

**Drill-through not working?**
- Verify `allowDrillThrough` is set to `true`
- Check that `DrillThrough` module is injected
- Ensure you're double-clicking on a value cell (not header)
- Check browser console for errors

**Data grid not appearing?**
- Verify double-click triggered on correct cell type
- Check that data source has underlying records
- Verify column definitions in gridColumns event

**Performance issues?**
- Reduce `maxRowsInDrillThrough` for OLAP sources
- Check backend query performance for database sources
- Disable unnecessary grid features
- Consider server-side filtering before drill-through

## Related Features

- **Drill-Down**: Navigate hierarchical data structures
- **Formatting**: Format drill-through data display
- **Export**: Export drill-through data to Excel/PDF
- **Editing**: Edit data directly in drill-through grid (if enabled)

## API Reference

### Properties
- `allowDrillThrough`: boolean - Enable/disable drill-through
- `maxRowsInDrillThrough`: number - Maximum rows for OLAP sources (default: 10000)

### Events
- `onDrillThrough`: Handle drill-through initiation and grid customization
- `onBeginDrillThrough`: Configure grid after initialization

### Methods
- `Inject(services=[DrillThrough])` - Required module injection
