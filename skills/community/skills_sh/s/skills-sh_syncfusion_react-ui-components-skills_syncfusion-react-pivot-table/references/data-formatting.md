# Data Formatting & Display

## Table of Contents
- [Number Formatting](#number-formatting)
- [Conditional Formatting](#conditional-formatting)

## Number Formatting

The Pivot Table provides comprehensive number formatting capabilities to display numeric values in various formats, enhancing data readability and ensuring values are presented accurately for your specific needs.

### Supported Format Types

The Pivot Table supports the following display formats:

- **Number (N)**: Standard numeric formatting with optional grouping separators and configurable decimal places (e.g., 1,234.56)
- **Currency (C)**: Formats with currency symbols, optional grouping separators, and customizable decimal places (e.g., $1,234.56)
- **Percentage (P)**: Values displayed as percentages with the % symbol (e.g., 12.34%)
- **Custom**: User-defined formatting patterns for specific display requirements

### Defining Format Settings

Use the `formatSettings` property in `dataSourceSettings` to configure formats. Key properties include:

- `name`: The field name to format (must correspond to a value field)
- `format`: The format code (e.g., 'C2', 'N0', 'P1')
- `useGrouping`: Whether to display grouping separators (true/false, default: true)
- `currency`: Currency code for currency formatting (e.g., 'USD', 'EUR', 'GBP')

### Format Code Examples

| Code | Format | Example Output | Use Case |
|------|--------|--------|----------|
| C0 | Currency, no decimals | $1,235 | Whole dollar amounts |
| C2 | Currency, 2 decimals | $1,234.56 | Standard currency |
| N0 | Number, no decimals | 1,235 | Counts, quantities |
| N2 | Number, 2 decimals | 1,234.56 | Precise numbers |
| P1 | Percentage, 1 decimal | 12.3% | Percentage values |
| P2 | Percentage, 2 decimals | 12.34% | Precise percentages |
| E2 | Scientific notation | 1.23E+03 | Large numbers |

### Basic Number Formatting Example

```typescript
import { FieldList, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function PivotWithNumberFormatting() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
    formatSettings: [
      { name: 'Amount', format: 'C0' },      // ← Currency, no decimals
      { name: 'Sold', format: 'N0' }         // ← Number, no decimals
    ]
  };

  return (
    <PivotViewComponent
      ref={(d) => (pivotObj = d)}
      id="PivotView"
      height={350}
      dataSourceSettings={dataSourceSettings}
      showFieldList={true}
    >
      <Inject services={[FieldList]} />
    </PivotViewComponent>
  );
}

export default PivotWithNumberFormatting;
```

### Advanced Format Settings

Control grouping separators and currency type:

```typescript
const formatSettings = [
  {
    name: 'Amount',
    format: 'C2',
    useGrouping: false,      // ← Disables grouping: 1234.56 instead of 1,234.56
    currency: 'EUR'          // ← Specifies currency: €1,234.56
  },
  {
    name: 'Sold',
    format: 'N0',
    useGrouping: true        // ← Enables grouping: 1,235
  }
];

<PivotViewComponent
  dataSourceSettings={{ ...dataSourceSettings, formatSettings }}
/>
```

## Conditional Formatting

Conditional formatting enables you to customize the appearance of Pivot Table value cells—including background color, font color, font family, and font size—based on specific conditions. This visualization feature helps highlight important value cells and make them stand out.

### Enabling Conditional Formatting

Conditional formatting can be applied at runtime through the toolbar dialog or programmatically. To enable the toolbar option:

```typescript
import { PivotViewComponent, Inject, Toolbar, ConditionalFormatting } from '@syncfusion/ej2-react-pivotview';
import * as React from 'react';

function PivotWithConditionalFormatting() {
  const toolbarOptions = ['ConditionalFormatting'];

  return (
    <PivotViewComponent
      id="PivotView"
      dataSourceSettings={dataSourceSettings}
      height={350}
      allowConditionalFormatting={true}
      showToolbar={true}
      toolbar={toolbarOptions}
    >
      <Inject services={[Toolbar, ConditionalFormatting]} />
    </PivotViewComponent>
  );
}

export default PivotWithConditionalFormatting;
```

### Programmatic Conditional Formatting

Apply formatting rules directly through code using the `conditionalFormatSettings` property:

```typescript
import { ConditionalFormatting, PivotViewComponent, Inject, Toolbar } from '@syncfusion/ej2-react-pivotview';
import * as React from 'react';

function PivotWithProgrammaticFormatting() {
  const conditionalFormatSettings = [
    {
      measure: 'Amount',           // ← Value field name
      value1: 1000,
      value2: 5000,
      condition: 'Between',        // ← Condition type
      style: {
        backgroundColor: '#FFC7CE', // ← Light red
        color: '#9C0006',          // ← Dark red text
        fontFamily: 'Arial'
      }
    },
    {
      measure: 'Sold',
      value1: 100,
      condition: 'GreaterThan',
      style: {
        backgroundColor: '#C6EFCE', // ← Light green
        color: '#006100'            // ← Dark green text
      }
    }
  ];

  const dataSourceSettings: DataSourceSettingsModel = {
    // ... pivot configuration ...
    conditionalFormatSettings: conditionalFormatSettings
  };

  return (
    <PivotViewComponent
      id="PivotView"
      dataSourceSettings={dataSourceSettings}
      height={350}
    >
      <Inject services={[Toolbar, ConditionalFormatting]} />
    </PivotViewComponent>
  );
}

export default PivotWithProgrammaticFormatting;
```

### Conditional Formatting Operators

The Pivot Table supports the following condition operators:

| Operator | Description | Example |
|----------|-------------|----------|
| GreaterThan | Value > threshold | Highlight sales > 5000 |
| LessThan | Value < threshold | Highlight sales < 1000 |
| Equal | Value = threshold | Highlight sales = 3000 |
| NotEquals | Value ≠ threshold | Highlight non-zero values |
| GreaterThanOrEqualsTo | Value ≥ threshold | Highlight sales ≥ 5000 |
| LessThanOrEqualsTo | Value ≤ threshold | Highlight sales ≤ 1000 |
| Between | threshold1 < value < threshold2 | Highlight 1000 < sales < 5000 |
| NotBetween | Value outside range | Highlight values outside 1000-5000 |

### Style Customization

Each condition supports comprehensive style customization:

```typescript
const style = {
  backgroundColor: '#FFE6E6',        // Background color (hex code)
  color: '#CC0000',                 // Font color (hex code)
  fontFamily: 'Segoe UI',           // Font family name
  fontSize: '12px',                 // Font size with unit
  fontWeight: 'bold',               // Font weight (normal, bold, etc.)
  fontStyle: 'italic'               // Font style (normal, italic)
};
```

### Practical Example: Sales Analysis

```typescript
const conditionalFormatSettings = [
  {
    measure: 'Revenue',
    value1: 100000,
    condition: 'GreaterThan',
    style: {
      backgroundColor: '#E2EFDA',
      color: '#375623',
      fontWeight: 'bold'
    }
  },
  {
    measure: 'Revenue',
    value1: 50000,
    value2: 100000,
    condition: 'Between',
    style: {
      backgroundColor: '#FFF2CC',
      color: '#9C6500'
    }
  },
  {
    measure: 'Revenue',
    value1: 50000,
    condition: 'LessThan',
    style: {
      backgroundColor: '#FCE4D6',
      color: '#C65911'
    }
  }
];
```

## Cell Styling & Templates

### Custom Cell Template

```typescript
function customCellTemplate(args: any) {
  return (
    <div style={{
      backgroundColor: parseFloat(args.formattedValue) > 5000 ? '#E8F5E9' : '#FFEBEE',
      padding: '8px',
      textAlign: 'right'
    }}>
      {args.formattedValue}
    </div>
  );
}

<PivotViewComponent
  cellTemplate={customCellTemplate}
/>
```

### Row and Column Header Styling

```typescript
const gridSettings = {
  rowHeight: 30,           // Row height
  columnWidth: 120,        // Column width  
  allowResizing: true,     // Enable resizing
  resizeMode: 'Normal'     // Normal, NextColumn, or FixedColumns
};

<PivotViewComponent gridSettings={gridSettings} />
```

## Tooltip Customization

Tooltip defaults to displaying cell values with row/column header information. To customize the tooltip display, use the `tooltipTemplate` property. For more tooltip configuration options, see the [Tooltip guide](./tooltip.md).

### Custom Tooltip Template

```typescript
function customTooltipTemplate(args: any) {
  return `
    <div style="border: 1px solid gray; padding: 8px;">
      <p><b>Value:</b> ${args.value}</p>
      <p><b>Row:</b> ${args.rowHeaders}</p>
      <p><b>Column:</b> ${args.columnHeaders}</p>
    </div>
  `;
}

<PivotViewComponent
  showTooltip={true}
  tooltipTemplate={customTooltipTemplate}
/>
```

## Complete Formatting Example

```typescript
function FormattedPivot() {
  const dataSourceSettings = {
    dataSource: sampleData as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [
      { name: 'Sales', caption: 'Total Sales' },
      { name: 'Quantity', caption: 'Units' }
    ],
    formatSettings: [
      { name: 'Sales', format: 'C2' },
      { name: 'Quantity', format: 'N0' }
    ]
  };

  const conditionalFormatSettings = [
    {
      measure: 'Sales',
      value1: 5000,
      conditions: 'GreaterThan',      // ← Use 'conditions'
      style: {
        backgroundColor: '#E8F5E9',
        color: '#2E7D32',
        fontWeight: 'bold'
      }
    }
  ];

  function tooltipTemplate(args: any) {
    return `Value: ${args.formattedValue}`;
  }

  return (
    <PivotViewComponent
      id="formatted-pivot"
      dataSourceSettings={dataSourceSettings}
      conditionalFormatSettings={conditionalFormatSettings}
      tooltipTemplate={tooltipTemplate}
      height={400}
    >
      <Inject services={[ConditionalFormatting]} />
    </PivotViewComponent>
  );
}
```
