# Classic Layout Configuration

## Overview

The Classic layout (also called Tabular layout) in Syncfusion React PivotView provides a traditional spreadsheet-like presentation where row fields are displayed side by side in separate columns rather than hierarchically nested. This layout enhances readability for complex data with multiple row hierarchies and is compatible only with relational data sources.

**Key Characteristic:** Fields in the row axis appear as separate columns instead of nested hierarchies, making the data easier to interpret.

## Enabling Tabular/Classic Layout

To enable the classic layout, set the `layout` property in `gridSettings` to **`'Tabular'`**:

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';

const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: pivotData as IDataSet[],
  rows: [
    { name: 'Country', caption: 'Country' },
    { name: 'Region', caption: 'Region' }
  ],
  columns: [{ name: 'Year' }, { name: 'Quarter' }],
  values: [{ name: 'Sales', type: 'Sum' }]
};

const gridSettings = {
  layout: 'Tabular'  // ← Enables classic/tabular layout
};

<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  gridSettings={gridSettings}
  height={400}
/>
```

## Layout Comparison: Tabular vs Compact

| Aspect | Tabular (Classic) | Compact (Hierarchical) |
|--------|-------------------|--------------------------|
| **Row Display** | Separate columns | Nested/hierarchical |
| **Use Case** | Multi-level row analysis | Space-conscious layouts |
| **Readability** | Better for complex hierarchies | Compact view |
| **Default** | No (must be enabled) | Yes |
| **Data Sources** | Relational only | Relational only |

## Dynamic Layout Toggle

```typescript
function PivotLayoutToggle() {
  const [layout, setLayout] = React.useState('Compact');

  return (
    <>
      <button onClick={() => setLayout(layout === 'Compact' ? 'Tabular' : 'Compact')}>
        Switch to {layout === 'Compact' ? 'Tabular' : 'Compact'} Layout
      </button>
      <PivotViewComponent
        dataSourceSettings={dataSourceSettings}
        gridSettings={{ layout: layout }}
        height={400}
      />
    </>
  );
}
```

## UI Configuration Options

### Field List Visibility

```typescript
// Enable field list with popup mode (built-in to PivotViewComponent)
<PivotViewComponent
  showFieldList={true}  // Shows field list as popup
/>

// OR use standalone PivotFieldListComponent with renderMode
import { PivotFieldListComponent } from '@syncfusion/ej2-react-pivotview';

<PivotFieldListComponent
  renderMode="Fixed"  // ← 'Fixed' for Standalone, 'Popup' for dialog
  dataSourceSettings={dataSourceSettings}
/>
```

### Grouping Bar Configuration

The grouping bar allows users to dynamically drag and drop fields:

```typescript
<PivotViewComponent
  showGroupingBar={true}
  // With tabular layout
  gridSettings={{ layout: 'Tabular' }}
/>
```

### Row and Column Header Customization

```typescript
const gridSettings = {
  layout: 'Tabular',        // ← Tabular layout
  rowHeight: 35,            // Adjust row height
  columnHeight: 35,         // Adjust column header height
  allowResizing: true,      // Allow column resizing
  allowSelection: true,     // Allow cell selection
  allowTextWrap: true       // Enable text wrapping
};

<PivotViewComponent 
  dataSourceSettings={dataSourceSettings}
  gridSettings={gridSettings}
/>
```

## Complete Tabular Layout Example

```typescript
import { PivotViewComponent, Inject, FieldList, GroupingBar, IDataSet } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import React from 'react';

function TabularLayoutPivot() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: sampleData as IDataSet[],
    rows: [
      { name: 'Country', caption: 'Country' },
      { name: 'Region', caption: 'Region' }
    ],
    columns: [
      { name: 'Year', caption: 'Year' },
      { name: 'Quarter', caption: 'Quarter' }
    ],
    values: [
      { name: 'Sales', type: 'Sum', caption: 'Total Sales', format: 'C2' }
    ]
  };

  const gridSettings = {
    layout: 'Tabular'  // ← KEY: Enable tabular/classic layout
  };

  return (
    <PivotViewComponent
      id="tabular-layout"
      dataSourceSettings={dataSourceSettings}
      gridSettings={gridSettings}
      showGroupingBar={true}
      showFieldList={true}
      height={400}
    >
      <Inject services={[FieldList, GroupingBar]} />
    </PivotViewComponent>
  );
}
```

## Practical Example: Sales Analysis with Tabular Layout

```typescript
function SalesAnalysisPivot() {
  const gridSettings = {
    layout: 'Tabular',
    rowHeight: 30,
    columnHeight: 25,
    allowResizing: true,
    allowSelection: true
  };

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: sampleData as IDataSet[],
    rows: [
      { name: 'Product_Categories', caption: 'Category' },
      { name: 'Products', caption: 'Product' },
      { name: 'Order_Source', caption: 'Source' }
    ],
    columns: [
      { name: 'Year', caption: 'Year' },
      { name: 'Quarter', caption: 'Quarter' }
    ],
    values: [
      { name: 'Sold', type: 'Sum', caption: 'Units Sold' },
      { name: 'Amount', type: 'Sum', caption: 'Sales Amount', format: 'C0' }
    ],
    formatSettings: [
      { name: 'Amount', format: 'C0' },
      { name: 'Sold', format: 'N0' }
    ]
  };

  return (
    <PivotViewComponent
      id="tabular-layout"
      dataSourceSettings={dataSourceSettings}
      gridSettings={gridSettings}
      showGroupingBar={true}
      showFieldList={true}
      height={400}
    >
      <Inject services={[FieldList, GroupingBar]} />
    </PivotViewComponent>
  );
}
```
