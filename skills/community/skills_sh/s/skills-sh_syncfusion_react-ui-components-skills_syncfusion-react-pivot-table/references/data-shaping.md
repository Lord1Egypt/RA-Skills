# Data Shaping: Aggregation, hierarchical grouping of rows and columns

## Overview

Data shaping enables organizing and summarizing data through aggregation, calculated fields, and hierarchical grouping of rows and columns.

## Aggregation Functions

### Common Aggregation Types

| Type | Description |
|------|-------------|
| Sum | Total of all values |
| Avg | Average value |
| Count | Number of records |
| Min | Minimum value |
| Max | Maximum value |
| Product | Multiplication of values |
| Median | Middle value |
| DistinctCount | Unique record count |

### Setting Aggregation Type

```typescript
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';

const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: data as IDataSet[],
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Product' }],
  values: [
    { name: 'Sales', type: 'Sum', caption: 'Total Sales' },
    { name: 'Quantity', type: 'Avg', caption: 'Avg Quantity' },
    { name: 'OrderID', type: 'Count', caption: 'Order Count' }
  ]
};
```

### Advanced Aggregation

```typescript
values: [
  {
    name: 'Sales',
    type: 'PercentageOfGrandTotal',
    caption: 'Percent of Total'
  },
  {
    name: 'Quantity',
    type: 'DifferenceFrom',
    baseField: 'Year',
    baseItem: '2020',
    caption: 'Difference from 2020'
  }
]
```

## Calculated Fields

Calculated fields enable you to create custom value fields using mathematical formulas based on existing fields. Users can define them programmatically or interactively through the Field List UI.

### Overview

The calculated field feature allows:
- Creating custom value fields with arithmetic operations
- Complex calculations using existing field names
- Interactive creation via Field List dialog
- Programmatic definition using `calculatedFieldSettings`
- Real-time formula editing and renaming

### Defining Calculated Fields Programmatically

Use the `calculatedFieldSettings` property to define calculated fields. To display a calculated field in the pivot table, add it to the `values` array as well.

```typescript
import { PivotViewComponent, Inject, CalculatedField, FieldList } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';

const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: data as IDataSet[],
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Year' }],
  values: [
    { name: 'Sold', caption: 'Units Sold' },
    { name: 'Amount', caption: 'Sold Amount' },
    { name: 'Total', caption: 'Total Units', type: 'CalculatedField' }  // ← Must add to values
  ],
  calculatedFieldSettings: [
    {
      name: 'Total',
      formula: '"Sum(Amount)"+"Sum(Sold)"'  // ← Use aggregation functions in quotes
    }
  ],
  formatSettings: [
    { name: 'Total', format: 'C2' }  // ← Optional formatting
  ]
};

function PivotWithCalculatedField() {
  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      allowCalculatedField={true}  // ← Enable to allow interactive editing
      showFieldList={true}
    >
      <Inject services={[CalculatedField, FieldList]} />
    </PivotViewComponent>
  );
}
```

### Calculated Field Formula Syntax

Formulas use field names wrapped in double quotes with aggregation functions:

```typescript
calculatedFieldSettings: [
  {
    name: 'TotalRevenue',
    formula: '"Sum(Sales)"+"Sum(ServiceCharges)"'  // Addition with aggregation
  },
  {
    name: 'Profit',
    formula: '"Sum(Amount)"-"Sum(Cost)"'  // Subtraction
  },
  {
    name: 'Margin',
    formula: '("Sum(Amount)"-"Sum(Cost)")/"Sum(Amount)"*100'  // Complex calculation
  },
  {
    name: 'UnitPrice',
    formula: '"Sum(Amount)"/"Sum(Quantity)"'  // Division
  },
  {
    name: 'DoubleVolume',
    formula: '"Sum(Quantity)"*2'  // Multiplication
  }
]
```

**Important**: All field references must be wrapped in double quotes and use aggregation functions like `"Sum()"`, `"Avg()"`, `"Count()"`, etc.

### Calculated Field Examples

```typescript
function AdvancedCalculations() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: salesData as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Year' }],
    values: [
      { name: 'Sold', caption: 'Units Sold' },
      { name: 'Amount', caption: 'Amount' },
      { name: 'Total', caption: 'Total', type: 'CalculatedField', format: 'C2' },
      { name: 'AvgPrice', caption: 'Avg Price', type: 'CalculatedField', format: 'C2' }
    ],
    calculatedFieldSettings: [
      {
        name: 'Total',
        formula: '"Sum(Amount)"+"Sum(Sold)"'
      },
      {
        name: 'AvgPrice',
        formula: '"Sum(Amount)"/"Sum(Sold)"'
      }
    ],
    formatSettings: [
      { name: 'Total', format: 'C2' },
      { name: 'AvgPrice', format: 'C2' }
    ]
  };

  return (
    <PivotViewComponent
      dataSourceSettings={dataSourceSettings}
      allowCalculatedField={true}
      showFieldList={true}
      height={400}
    >
      <Inject services={[CalculatedField, FieldList]} />
    </PivotViewComponent>
  );
}
```

### Interactive Calculated Field Dialog

Enable users to create and edit calculated fields via the Field List UI:

```typescript
function PivotWithInteractiveCalcField() {
  const pivotRef = React.useRef<PivotViewComponent>(null);

  const openCalculatedFieldDialog = () => {
    pivotRef.current?.calculatedFieldModule?.createCalculatedFieldDialog();
  };

  return (
    <>
      <button onClick={openCalculatedFieldDialog}>Create Calculated Field</button>
      <PivotViewComponent
        ref={pivotRef}
        dataSourceSettings={dataSourceSettings}
        allowCalculatedField={true}  // ← Shows "CALCULATED FIELD" button in Field List
        showFieldList={true}
        height={400}
      >
        <Inject services={[CalculatedField, FieldList]} />
      </PivotViewComponent>
    </>
  );
}
```

When enabled, the Field List dialog displays a "CALCULATED FIELD" button that allows users to:
- Create new calculated fields
- Edit existing formulas
- Rename calculated fields
- Delete calculated fields

### Editing and Renaming Calculated Fields

Users can modify calculated fields in the Field List or Grouping Bar:
1. Locate the calculated field button
2. Click the **Edit** icon next to the field name
3. Modify the formula or field name in the dialog
4. Click **OK** to apply changes
5. The pivot table refreshes automatically

### Important Notes

- Calculated fields apply **only to value fields**
- Must be added to the `values` property to display in the pivot
- All field names in formulas must be quoted: `"FieldName"`
- Aggregation functions must wrap field names: `"Sum(Field)"`
- Format settings can be applied via `formatSettings` property
- Requires `CalculatedField` service injection
```

## hierarchical grouping of rows and columns

### Row Grouping

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  rows: [
    { name: 'Country', caption: 'Country' },
    { name: 'Region', caption: 'Region' },
    { name: 'City', caption: 'City' }
  ],
  values: [{ name: 'Sales' }]
};
```

### Column Grouping

```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  columns: [
    { name: 'Year', caption: 'Year' },
    { name: 'Quarter', caption: 'Quarter' },
    { name: 'Month', caption: 'Month' }
  ]
};
```

## Grouping Bar Configuration

### Enable Grouping Bar

```typescript
import { GroupingBar, Grouping, Inject } from '@syncfusion/ej2-react-pivotview';

<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  showGroupingBar={true}
  allowGrouping={true}
>
  <Inject services={[GroupingBar, Grouping]} />
</PivotViewComponent>
```

### Grouping Bar Options

```typescript
<PivotViewComponent
  showGroupingBar={true}
  groupingBarSettings={{
    showFilterIcon: true,
    showSortIcon: true,
    showRemoveIcon: true,
    showValueTypeIcon: true
  }}
>
  <Inject services={[GroupingBar]} />
</PivotViewComponent>
```

## Field List Configuration

The Field List provides an intuitive interface (similar to Microsoft Excel) for organizing and analyzing data in the pivot table. Users can add/remove fields and move them between different axes.

### Field List Modes

The Field List can be displayed in two modes:

#### 1. Built-in Field List (Popup Mode)

Shows a field list icon in the pivot table interface. Click to open the field list in a dialog box.

```typescript
import { FieldList, Inject } from '@syncfusion/ej2-react-pivotview';

<PivotViewComponent
  id="pivotview"
  dataSourceSettings={dataSourceSettings}
  showFieldList={true}  // ← Shows field list icon
  height={400}
>
  <Inject services={[FieldList]} />
</PivotViewComponent>
```

**Field List Icon Location:**
- Top-left corner of pivot table (default)
- Top-right corner when grouping bar is enabled

#### 2. Standalone Field List (Fixed Mode)

Displays the field list in a fixed position on the page alongside the pivot table. Use the `PivotFieldListComponent` for this mode.

```typescript
import { PivotFieldListComponent, CalculatedField, Inject } from '@syncfusion/ej2-react-pivotview';

function App() {
  const pivotRef = React.useRef<PivotViewComponent>(null);
  const fieldlistRef = React.useRef<PivotFieldListComponent>(null);

  const syncComponents = () => {
    if (fieldlistRef.current && pivotRef.current) {
      if (fieldlistRef.current.isRequiredUpdate) {
        fieldlistRef.current.updateView(pivotRef.current);
      }
      pivotRef.current.notify('ui-update', pivotRef.current);
      fieldlistRef.current.notify('tree-view-update', fieldlistRef.current);
    }
  };

  const afterPivotPopulate = () => {
    if (fieldlistRef.current && pivotRef.current) {
      fieldlistRef.current.update(pivotRef.current);
    }
  };

  React.useEffect(() => {
    syncComponents();
  }, []);

  return (
    <div style={{ display: 'flex', height: '530px', gap: '10px' }}>
      {/* Pivot Table */}
      <PivotViewComponent
        ref={pivotRef}
        id="pivotview"
        dataSourceSettings={dataSourceSettings}
        enginePopulated={afterPivotPopulate}
        width="58%"
        gridSettings={{ columnWidth: 140 }}
      />
      
      {/* Fixed Field List */}
      <PivotFieldListComponent
        ref={fieldlistRef}
        id="fieldlist"
        dataSourceSettings={dataSourceSettings}
        renderMode="Fixed"  // ← Always visible
        enginePopulated={syncComponents}
        allowCalculatedField={true}
        width="42%"
      >
        <Inject services={[CalculatedField]} />
      </PivotFieldListComponent>
    </div>
  );
}
```

**Key Methods:**
- `updateView()` - Updates field list when pivot data changes
- `update()` - Syncs field list with pivot table changes
- `isRequiredUpdate` - Checks if update is needed

### Field List Features

With the Field List, users can:
- **Drag and drop** fields between Row, Column, Value, and Filter axes
- **Apply filtering** while organizing fields
- **Apply sorting** to fields
- **Create calculated fields** (when `allowCalculatedField={true}`)
- **Apply aggregation types** to value fields
- **Format fields** with number formats
- **Drill down/up** through hierarchies

### Field List with Calculated Fields

```typescript
import { FieldList, CalculatedField, Inject } from '@syncfusion/ej2-react-pivotview';

<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  showFieldList={true}
  allowCalculatedField={true}  // ← Enables "CALCULATED FIELD" button
  height={400}
>
  <Inject services={[FieldList, CalculatedField]} />
</PivotViewComponent>
```

When enabled, users can create calculated fields directly from the "CALCULATED FIELD" button in the Field List dialog.

### Field List Modes

## Deferred Updates (Field List)

Deferred layout updates allow batching multiple field configuration changes to be applied only when the user clicks "Apply", reducing unnecessary re-renders and improving performance, especially with large datasets.

### Enable Deferred Updates

```typescript
import { FieldList, Inject } from '@syncfusion/ej2-react-pivotview';

// Built-in Field List (Popup)
<PivotViewComponent
  showFieldList={true}
  allowDeferLayoutUpdate={true}
>
  <Inject services={[FieldList]} />
</PivotViewComponent>

// Standalone Field List (Fixed)
import { PivotFieldListComponent } from '@syncfusion/ej2-react-pivotview';

<PivotFieldListComponent 
  renderMode="Fixed"
  allowDeferLayoutUpdate={true}
  dataSourceSettings={dataSourceSettings}
/>
```

### Benefits

- Batches multiple field operations (drag/drop, filter, sort)
- Reduces unnecessary pivot table re-renders
- Improved performance with large datasets
- Smooth user experience - changes apply only on "Apply" click
- Controls render through Field List interface

### Built-in Field List with Deferred Updates

```typescript
function PivotWithDeferredUpdates() {
  return (
    <PivotViewComponent
      id="pivot-defer"
      dataSourceSettings={dataSourceSettings}
      showFieldList={true}
      allowDeferLayoutUpdate={true}  // ← Enable deferred updates
      height={400}
    >
      <Inject services={[FieldList]} />
    </PivotViewComponent>
  );
}
```

### Standalone Field List with Deferred Updates

```typescript
function StandaloneFieldListWithDefer() {
  const pivotRef = React.useRef<PivotViewComponent>(null);
  const fieldlistRef = React.useRef<PivotFieldListComponent>(null);

  const syncComponents = () => {
    if (fieldlistRef.current && pivotRef.current) {
      if (fieldlistRef.current.isRequiredUpdate) {
        fieldlistRef.current.updateView(pivotRef.current);
      }
      pivotRef.current.notify('ui-update', pivotRef.current);
      fieldlistRef.current.notify('tree-view-update', fieldlistRef.current);
    }
  };

  const afterPivotPopulate = () => {
    if (fieldlistRef.current && pivotRef.current) {
      fieldlistRef.current.update(pivotRef.current);
    }
  };

  React.useEffect(() => {
    syncComponents();
  }, []);

  return (
    <div style={{ display: 'flex', height: '500px' }}>
      {/* Pivot View */}
      <PivotViewComponent
        ref={pivotRef}
        id="pivot"
        dataSourceSettings={dataSourceSettings}
        enginePopulated={afterPivotPopulate}
        height="100%"
        width="60%"
        style={{ float: 'left' }}
      />
      
      {/* Fixed Field List */}
      <PivotFieldListComponent
        ref={fieldlistRef}
        id="fieldlist"
        dataSourceSettings={dataSourceSettings}
        renderMode="Fixed"
        allowDeferLayoutUpdate={true}  // ← Enable deferred updates
        enginePopulated={syncComponents}
        height="100%"
        width="40%"
        style={{ float: 'right' }}
      />
    </div>
  );
}
```

### How Deferred Updates Works

When enabled, users can:
1. Drag/drop fields between Row, Column, Value, and Filter axes
2. Apply sorting and filtering within the Field List
3. Make multiple configuration changes
4. Click "Apply" button to apply all changes at once
5. Pivot table refreshes only once after "Apply" is clicked

This approach significantly reduces multiple renders and improves performance during complex data operations.

## Complete Data Shaping Example

```typescript
function DataShapingPivot() {
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
      { name: 'Sales', type: 'Sum', caption: 'Total Sales', format: 'C2' },
      { name: 'Quantity', type: 'Avg', caption: 'Average Quantity' },
      {
        name: 'Profit',
        type: 'CalculatedField',
        caption: 'Estimated Profit (15% of Sales)'
      }
    ],
    calculatedFieldSettings: [
      {
        name: 'Profit',
        formula: '"Sum(Sales)" * 0.15',
      }
    ],
  };

  return (
    <PivotViewComponent
      id="data-shaping"
      dataSourceSettings={dataSourceSettings}
      showGroupingBar={true}
      showFieldList={true}
      allowGrouping={true}
      height={500}
    >
      <Inject services={[GroupingBar, FieldList, Grouping]} />
    </PivotViewComponent>
  );
}
```
