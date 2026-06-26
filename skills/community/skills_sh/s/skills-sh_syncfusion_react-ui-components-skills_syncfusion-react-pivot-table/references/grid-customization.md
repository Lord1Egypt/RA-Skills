# Grid Customization Reference - Syncfusion React Pivot Table

## Overview

The Syncfusion React Pivot Table provides extensive customization options for modifying the grid's appearance and behavior. This includes cell templates, row heights, column widths, text alignment, resizing, and reordering. These customization features allow you to create pivot tables that match your application's design and usability requirements.

### Customization Categories
- **Cell Templates**: Custom content rendering in cells
- **Dimensions**: Row heights and column widths
- **Alignment**: Text positioning and formatting
- **Interaction**: Resizing and reordering columns
- **Styling**: Colors, fonts, and conditional formatting

## Cell Template Customization

### Value Cell Template

Customize how values are displayed in the pivot table cells:

```typescript
import { PivotViewComponent, Inject, IDataSet } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function ValueCellTemplate() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year' }, { name: 'Quarter' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sales' }, { name: 'Amount' }],
    dataSource: pivotData,
    formatSettings: [
      { name: 'Amount', format: 'C2' }
    ]
  };

  const cellTemplate = (args: any) => {
    // args contains: rowIndex, colIndex, value, rowHeaders, colHeaders
    if (args.value > 5000) {
      return (
        <div style={{ 
          backgroundColor: '#90EE90', 
          padding: '8px',
          fontWeight: 'bold',
          color: '#000'
        }}>
          {args.value}
        </div>
      );
    }
    return <div>{args.value}</div>;
  };

  return (
    <PivotViewComponent
      id='PivotView'
      dataSourceSettings={dataSourceSettings}
      cellTemplate={cellTemplate}
      height={350}
    />
  );
}

export default ValueCellTemplate;
```

### Row Header Template

Customize row header cell appearance:

```typescript
const rowHeaderTemplate = (args: any) => {
  return (
    <div style={{ 
      padding: '8px',
      backgroundColor: '#E8E8E8',
      fontWeight: 'bold',
      borderRight: '1px solid #ccc'
    }}>
      {args.text}
    </div>
  );
};

<PivotViewComponent
  rowHeaderTemplate={rowHeaderTemplate}
  dataSourceSettings={dataSourceSettings}
/>
```

### Column Header Template

Customize column header cell appearance:

```typescript
const colHeaderTemplate = (args: any) => {
  return (
    <div style={{ 
      padding: '8px',
      backgroundColor: '#4472C4',
      color: '#FFF',
      fontWeight: 'bold',
      textAlign: 'center'
    }}>
      {args.text}
    </div>
  );
};

<PivotViewComponent
  colHeaderTemplate={colHeaderTemplate}
  dataSourceSettings={dataSourceSettings}
/>
```

## Row Height Customization

### Set Uniform Row Height

Apply the same height to all rows:

```typescript
import { PivotViewComponent } from '@syncfusion/ej2-react-pivotview';

const App = () => {
  const rowHeight = 40; // pixels

  return (
    <PivotViewComponent
      id='PivotView'
      dataSourceSettings={dataSourceSettings}
      height={350}
      rowHeight={rowHeight}
    />
  );
};
```

### Set Row Height for Specific Rows

Use a function to customize height based on row context:

```typescript
const getRowHeight = (index: number, name: string): number => {
  // Header rows
  if (index === 0) return 50;
  
  // Grand total row
  if (name && name.includes('Grand Total')) return 60;
  
  // Regular rows
  return 35;
};

<PivotViewComponent
  getRowHeight={getRowHeight}
  dataSourceSettings={dataSourceSettings}
/>
```

**Common Row Height Values:**
- `30px` - Compact view
- `35-40px` - Standard view (recommended)
- `50px` - Spacious view
- `60+px` - Accessibility/readability

## Column Width Customization

### Set Uniform Column Width

Apply the same width to all columns:

```typescript
import { PivotViewComponent } from '@syncfusion/ej2-react-pivotview';

const App = () => {
  const columnWidth = 120; // pixels

  return (
    <PivotViewComponent
      id='PivotView'
      dataSourceSettings={dataSourceSettings}
      height={350}
      columnWidth={columnWidth}
    />
  );
};
```

### Set Column Width for Specific Columns

Use a function to customize width based on column context:

```typescript
const getColumnWidth = (field: string, index: number): number => {
  // Row headers need more space
  if (field === 'GroupIndent') return 40;
  if (field === 'RowSpacing') return 50;
  
  // Value columns
  if (field === 'Amount') return 150;
  if (field === 'Sales') return 130;
  
  // Default
  return 100;
};

<PivotViewComponent
  getColumnWidth={getColumnWidth}
  dataSourceSettings={dataSourceSettings}
/>
```

### Auto-fit Column Width

Automatically adjust columns to content:

```typescript
const autoFitColumns = (index: number): void => {
  if (pivotObj && pivotObj.grid) {
    pivotObj.grid.autoFitColumns([index]);
  }
};

// Or fit all columns
const autoFitAllColumns = (): void => {
  if (pivotObj && pivotObj.grid) {
    pivotObj.grid.autoFitColumns(); // No index = all columns
  }
};
```

**Common Column Width Values:**
- `80px` - Narrow (compact data)
- `100-120px` - Standard (readable)
- `150px` - Wide (comfortable)
- `200+px` - Extra wide (detailed content)

## Text Alignment

### Text Alignment Configuration

Set horizontal and vertical text alignment:

```typescript
import { PivotViewComponent, Inject } from '@syncfusion/ej2-react-pivotview';

const App = () => {
  const textAlignment = (args: any) => {
    // args properties: cellIndex, rowIndex, colIndex, dataField, aggregationType, isGrandTotal

    // Right-align all numeric values
    if (args.dataField === 'Amount' || args.dataField === 'Sales') {
      args.style = {
        textAlign: 'right',
        verticalAlign: 'middle'
      };
    }
    
    // Left-align row headers
    if (args.rowIndex >= 0 && args.colIndex === -1) {
      args.style = {
        textAlign: 'left',
        verticalAlign: 'middle'
      };
    }
    
    // Center-align column headers
    if (args.colIndex >= 0 && args.rowIndex === -1) {
      args.style = {
        textAlign: 'center',
        verticalAlign: 'middle'
      };
    }
  };

  return (
    <PivotViewComponent
      id='PivotView'
      dataSourceSettings={dataSourceSettings}
      cellTemplate={textAlignment}
      height={350}
    />
  );
};
```

### Alignment Rules

```typescript
// Numbers: right-aligned (right)
// Text: left-aligned (left)
// Headers: center-aligned (center)
// Vertical options: top, middle, bottom
```

## Column Resizing

### Enable Column Resizing

Allow users to resize columns interactively:

```typescript
import { PivotViewComponent, Inject, Resize } from '@syncfusion/ej2-react-pivotview';

const App = () => {
  return (
    <PivotViewComponent
      id='PivotView'
      dataSourceSettings={dataSourceSettings}
      allowResizing={true}
      allowColumnResizing={true}  // Enable column resize
      resizeSettings={{
        mode: 'Normal'  // 'Normal' or 'FixedColumns'
      }}
      height={350}
    >
      <Inject services={[Resize]} />
    </PivotViewComponent>
  );
};
```

### Customize Resize Behavior

```typescript
const resizeSettings = {
  mode: 'FixedColumns',           // Keep column widths fixed
  minWidth: 80,                   // Minimum column width (pixels)
  maxWidth: 300,                  // Maximum column width (pixels)
  enableAutoResize: true          // Auto-resize columns to fit content
};

<PivotViewComponent
  resizeSettings={resizeSettings}
  allowResizing={true}
/>
```

## Column Reordering

### Enable Column Reordering

Allow users to drag and drop columns to reorder them:

```typescript
import { PivotViewComponent, Inject, Reorder } from '@syncfusion/ej2-react-pivotview';

const App = () => {
  return (
    <PivotViewComponent
      id='PivotView'
      dataSourceSettings={dataSourceSettings}
      allowReordering={true}
      height={350}
    >
      <Inject services={[Reorder]} />
    </PivotViewComponent>
  );
};
```

### Programmatic Column Reordering

```typescript
const reorderColumn = (fromIndex: number, toIndex: number): void => {
  if (pivotObj && pivotObj.grid) {
    pivotObj.grid.reorderColumns(fromIndex, toIndex);
  }
};

// Move second column to position 5
reorderColumn(1, 4);
```

## Grid Styling

### Apply Custom CSS Classes

```typescript
import { PivotViewComponent } from '@syncfusion/ej2-react-pivotview';

// CSS
const styling = `
  .e-pivotvgrid .e-rowsheader { background-color: #F0F0F0; }
  .e-pivotvgrid .e-columnsheader { background-color: #4472C4; color: white; }
  .e-pivotvgrid .e-valuescells { background-color: #FAFAFA; }
  .e-pivotvgrid .e-gtotalcells { background-color: #E8E8E8; font-weight: bold; }
`;

const App = () => {
  return (
    <>
      <style>{styling}</style>
      <PivotViewComponent
        id='PivotView'
        dataSourceSettings={dataSourceSettings}
        cssClass='custom-pivot-grid'
        height={350}
      />
    </>
  );
};
```

### Dynamic Cell Styling

```typescript
const cellStyling = (args: any) => {
  const value = args.value;
  
  // Highlight cells with values > threshold
  if (value > 10000) {
    args.style = { backgroundColor: '#90EE90', fontWeight: 'bold' };
  }
  // Highlight cells with low values
  else if (value < 1000) {
    args.style = { backgroundColor: '#FFB6C6' };
  }
};

<PivotViewComponent
  cellTemplate={cellStyling}
  dataSourceSettings={dataSourceSettings}
/>
```

## Dimension Configuration

### Configure Row/Column Dimensions

```typescript
import { Dimension } from '@syncfusion/ej2-react-pivotview';

const dimensionSettings: Dimension = {
  columns: [
    {
      field: 'Year',
      width: 100,
      cssClass: 'year-column'
    },
    {
      field: 'Quarter',
      width: 80,
      cssClass: 'quarter-column'
    }
  ],
  rows: [
    {
      field: 'Country',
      width: 120,
      cssClass: 'country-row'
    }
  ]
};

<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  dimensions={dimensionSettings}
/>
```

## Complete Customization Example

```typescript
import { PivotViewComponent, Inject, Toolbar } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function GridCustomization() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year' }, { name: 'Quarter' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Amount', caption: 'Total Amount' }, { name: 'Sales' }],
    dataSource: pivotData,
    formatSettings: [
      { name: 'Amount', format: 'C2' },
      { name: 'Sales', format: 'N0' }
    ]
  };

  let pivotObj: PivotViewComponent;

  // Cell template with conditional styling
  const cellTemplate = (args: any) => {
    const styles: React.CSSProperties = {
      padding: '10px',
      textAlign: args.dataField === 'Country' ? 'left' : 'right'
    };

    if (args.value > 5000) {
      styles.backgroundColor = '#90EE90';
      styles.fontWeight = 'bold';
    }

    return <div style={styles}>{args.value}</div>;
  };

  return (
    <PivotViewComponent
      ref={(d: PivotViewComponent) => pivotObj = d}
      id='PivotView'
      dataSourceSettings={dataSourceSettings}
      height={500}
      rowHeight={40}
      columnWidth={150}
      allowResizing={true}
      allowReordering={true}
      cellTemplate={cellTemplate}
      toolbar={['Print', 'Export']}
    >
      <Inject services={[Toolbar]} />
    </PivotViewComponent>
  );
}

export default GridCustomization;
```

## Best Practices

1. **Consistent Styling**: Use uniform row heights and column widths for professional appearance
2. **Readability**: Ensure adequate spacing and font size for data visibility
3. **Responsive**: Consider mobile views when setting dimensions
4. **Performance**: Complex templates may impact performance with large datasets
5. **Accessibility**: Maintain adequate contrast and readable fonts
6. **Testing**: Test customizations across different browsers

## Troubleshooting

**Row heights not applying?**
- Check that Inject services includes necessary modules
- Verify rowHeight is set as a number (not string)
- Confirm grid is fully rendered before applying height

**Column reordering not working?**
- Ensure Reorder module is injected
- Check allowReordering is set to true
- Verify column definitions are correct

**Template styles not applying?**
- Check CSS specificity - may need higher specificity
- Verify inline styles aren't conflicting
- Check browserdevtools for CSS cascade issues

## Related Features

- **Conditional Formatting**: Apply styling based on data values
- **Cell Formatting**: Format numbers, dates, and text
- **Row and Column Templates**: Customize content rendering
- **Responsive Design**: Adapt grid to different screen sizes
