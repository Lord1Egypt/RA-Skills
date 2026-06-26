# Print Reference - Syncfusion React Pivot Table

## Overview

The printing feature in the Syncfusion React Pivot Table enables users to generate print-friendly output of their pivot table and pivot charts. The component captures the current state of the pivot table (including all applied filters, sorting, and formatting) and provides flexible printing options. Printing can be triggered through the toolbar or programmatically from your application code.

### Key Features
- **Pivot Table Printing**: Print the complete pivot table with all configurations
- **Pivot Chart Printing**: Print visualizations alongside or separately from data
- **State Preservation**: Maintains all filters, sorting, and formatting during print
- **Formatting Support**: Colors, fonts, and styling are preserved in print output
- **Flexible Triggers**: Both toolbar button and programmatic API support

## Printing Pivot Table

### How to Print

#### Method 1: Using the Grid Print Method

Access the underlying Grid component through the PivotView reference and call its print method:

```typescript
import { PivotViewComponent, Inject, Toolbar } from '@syncfusion/ej2-react-pivotview';
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

  const printPivot = () => {
    if (pivotObj && pivotObj.grid) {
      pivotObj.grid.print();
    }
  };

  return (
    <>
      <button onClick={printPivot}>Print Pivot Table</button>
      <PivotViewComponent
        ref={(d: PivotViewComponent) => pivotObj = d}
        id='PivotView'
        height={350}
        dataSourceSettings={dataSourceSettings}
      >
        <Inject services={[Toolbar]} />
      </PivotViewComponent>
    </>
  );
}

export default App;
```

#### Method 2: Using Print Method with Options

The print method accepts parameters for customization:

```typescript
const printWithOptions = () => {
  if (pivotObj && pivotObj.grid) {
    pivotObj.grid.print({
      type: 'CurrentPage',  // Print current page or all rows
      hierarchy: false      // Include hierarchy indicators
    });
  }
};
```

## Printing Pivot Charts

### Basic Chart Printing

To print the pivot chart visualization, access the Chart component and call its print method:

```typescript
import { PivotViewComponent, PivotChart, Inject } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year' }, { name: 'Quarter' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sales' }],
    dataSource: pivotData as IDataSet[]
  };

  let pivotObj: PivotViewComponent;

  const printChart = () => {
    if (pivotObj && pivotObj.chart) {
      pivotObj.chart.print();
    }
  };

  return (
    <>
      <button onClick={printChart}>Print Chart</button>
      <PivotViewComponent
        ref={(d: PivotViewComponent) => pivotObj = d}
        id='PivotView'
        height={350}
        dataSourceSettings={dataSourceSettings}
        displayOption={{ view: 'Chart' }}
      >
        <Inject services={[PivotChart]} />
      </PivotViewComponent>
    </>
  );
}

export default App;
```

### Printing Both Table and Chart

To print both pivot table and chart together:

```typescript
const printBoth = () => {
  if (pivotObj && pivotObj.grid) {
    pivotObj.grid.print();
  }
  setTimeout(() => {
    if (pivotObj && pivotObj.chart) {
      pivotObj.chart.print();
    }
  }, 1000); // Delay chart print to ensure grid print dialog closes
};
```

## Print Configuration

### Display Option Settings

Control what is shown on the page when printing:

```typescript
import { DisplayOption } from '@syncfusion/ej2-react-pivotview';

// Display only table
const displayOption: DisplayOption = {
  view: 'Table'
};

// Display only chart
const displayOption: DisplayOption = {
  view: 'Chart'
};

// Display both table and chart
const displayOption: DisplayOption = {
  view: 'Both'
};

<PivotViewComponent
  displayOption={displayOption}
  dataSourceSettings={dataSourceSettings}
>
  <Inject services={[PivotChart]} />
</PivotViewComponent>
```

## Related Features

- **Export to Excel**: Export data in spreadsheet format
- **PDF Export**: Generate professional PDF reports  
- **Toolbar**: Provides print button in UI
- **Display Options**: Control what views are available for printing
