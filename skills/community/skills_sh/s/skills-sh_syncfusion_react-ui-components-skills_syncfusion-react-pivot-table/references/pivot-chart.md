# Pivot Chart Visualization

## Table of Contents
- [Overview](#overview)
- [Chart Types](#chart-types)
- [Accumulation Charts](#accumulation-charts)
- [Display Options](#display-options)
- [Chart Configuration](#chart-configuration)
- [Complete Example](#complete-example)

## Overview

The Pivot Chart in the Syncfusion React Pivot Table component helps users visualize aggregated values in a clear and graphical format. It provides essential options like drill down and drill up operations, over 21 chart types, and various display settings for series, axes, legends, export, print, and tooltips. The main purpose of the Pivot Chart is to present Pivot Table data in a way that is easy to understand and interact with.

Users can display the pivot chart component individually with pivot values and modify the report dynamically using the field list and grouping bar. To use the Pivot Chart, you must inject the `PivotChart` module into your application.

### Basic Setup

```ts
import { IDataSet, PivotViewComponent, Inject, DisplayOption, PivotChart } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';
import { ChartSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/chartSettings';

function App() {
  let displayOption: DisplayOption = {
    view: 'Chart'
  } as DisplayOption;

  let chartSettings: ChartSettings = {
    chartSeries: { type: 'Column' }
  } as ChartSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }
  let pivotObj: PivotViewComponent;
  return (<PivotViewComponent height={350} ref={ (d: PivotViewComponent) => pivotObj = d } id='PivotView' chartSettings={chartSettings} displayOption={displayOption} dataSourceSettings={dataSourceSettings} ><Inject services={[PivotChart]}/></PivotViewComponent>);
}
export default App;
```

## Display Options

The `displayOption` property controls the visibility of both the grid and chart components:

- **view: 'Table'** - Display only the pivot table
- **view: 'Chart'** - Display only the pivot chart
- **view: 'Both'** - Display both table and chart (default)
- **primary: 'Table'** - Set Table as primary view when showing both
- **primary: 'Chart'** - Set Chart as primary view when showing both

```ts
let displayOption: DisplayOption = {
  view: 'Both',
  primary: 'Chart'  // Chart appears first when showing both
} as DisplayOption;
```

## Chart Types

The Pivot Chart offers 21 different chart types, allowing users to visualize and analyze data in various ways:

### Standard Chart Types
- **Line** - Display trends over time
- **Column** - Vertical bar comparison (default)
- **Area** - Stacked area visualization
- **Bar** - Horizontal bar comparison
- **StepArea** - Step pattern areas
- **StackingLine** - Accumulated line trends
- **StackingColumn** - Accumulated vertical bars
- **StackingArea** - Accumulated areas
- **StackingBar** - Accumulated horizontal bars
- **StepLine** - Step line trends
- **Pareto** - Pareto principle visualization
- **Bubble** - Multi-dimensional bubble analysis
- **Scatter** - Correlation analysis
- **Spline** - Curved line visualization
- **SplineArea** - Curved area visualization
- **StackingLine100** - 100% stacked lines
- **StackingColumn100** - 100% stacked columns
- **StackingBar100** - 100% stacked bars
- **StackingArea100** - 100% stacked areas
- **Polar** - Polar coordinate visualization
- **Radar** - Radar chart visualization

By default, the **Line** chart type is displayed. You can change the chart type using the `type` property under `chartSeries`.

### Configuring Chart Type

```ts
import { IDataSet, PivotViewComponent, Inject, DisplayOption, PivotChart } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';
import { ChartSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/chartSettings';

function App() {
  let displayOption: DisplayOption = {
    view: 'Chart'
  } as DisplayOption;

  let chartSettings: ChartSettings = {
    chartSeries: { type: 'Bar' }
  } as ChartSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }
  let pivotObj: PivotViewComponent;
  return (<PivotViewComponent height={350} ref={ (d: PivotViewComponent) => pivotObj = d } id='PivotView' chartSettings={chartSettings} displayOption={displayOption} dataSourceSettings={dataSourceSettings} ><Inject services={[PivotChart]}/></PivotViewComponent>);
}
export default App;
```

## Accumulation Charts

Pivot Chart supports four types of accumulation charts for showing parts of a whole:

- **Pie** - Circular chart showing proportions
- **Doughnut** - Ring-shaped pie variant
- **Funnel** - Funnel-shaped data visualization
- **Pyramid** - Pyramid-shaped data visualization

```ts
import { IDataSet, PivotViewComponent, Inject, DisplayOption, PivotChart } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';
import { pivotData } from './datasource';
import { ChartSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/chartSettings';

function App() {
  let displayOption: DisplayOption = {
    view: 'Chart'
  } as DisplayOption;

  let chartSettings: ChartSettings = {
    chartSeries: { type: 'Pie' }
  } as ChartSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }
  let pivotObj: PivotViewComponent;
  return (<PivotViewComponent height={350} ref={ (d: PivotViewComponent) => pivotObj = d } id='PivotView' chartSettings={chartSettings} displayOption={displayOption} dataSourceSettings={dataSourceSettings} ><Inject services={[PivotChart]}/></PivotViewComponent>);
}
export default App;
```

## Chart Configuration

### Data Binding

The Pivot Chart supports both local and remote data binding options. You can bind data using the `dataSource` property which accepts either a `DataManager` instance for remote data or a JavaScript object array for local data.

### Drill Operations

Pivot Chart supports drill down and drill up operations for dimensional analysis. Users can click on chart segments to drill down into detailed data or drill up to see aggregated views.

## Complete Example

```ts
import { IDataSet, PivotViewComponent, Inject, DisplayOption, PivotChart } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';
import { ChartSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/chartSettings';

function PivotChartExample() {
  const [chartType, setChartType] = React.useState<string>('Column');
  const [viewMode, setViewMode] = React.useState<string>('Both');

  let displayOption: DisplayOption = {
    view: viewMode as any,
    primary: 'Chart'
  } as DisplayOption;

  let chartSettings: ChartSettings = {
    chartSeries: { type: chartType as any }
  } as ChartSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }
  let pivotObj: PivotViewComponent;

  return (
    <>
      <div style={{ marginBottom: '15px' }}>
        <label>Select Chart Type: 
          <select value={chartType} onChange={(e) => setChartType(e.target.value)}>
            <option>Column</option>
            <option>Bar</option>
            <option>Line</option>
            <option>Area</option>
            <option>Pie</option>
            <option>Doughnut</option>
          </select>
        </label>
        <label style={{ marginLeft: '20px' }}>View Mode:
          <select value={viewMode} onChange={(e) => setViewMode(e.target.value)}>
            <option>Grid</option>
            <option>Chart</option>
            <option>Both</option>
          </select>
        </label>
      </div>
      <PivotViewComponent 
        height={350} 
        ref={(d: PivotViewComponent) => pivotObj = d} 
        id='PivotView' 
        chartSettings={chartSettings} 
        displayOption={displayOption} 
        dataSourceSettings={dataSourceSettings}
      >
        <Inject services={[PivotChart]}/>
      </PivotViewComponent>
    </>
  );
}
export default PivotChartExample;
      </div>
      <PivotViewComponent
        displayOption={{ view: view as 'Both' | 'Table' | 'Chart' }}
      >
        <Inject services={[PivotChart]} />
      </PivotViewComponent>
    </>
  );
}
```

## Complete Chart Example

```typescript
import { PivotViewComponent, Inject, PivotChart, IDataSet } from '@syncfusion/ej2-react-pivotview';

function ChartPivot() {
  const chartSettings = {
    type: 'Column',
    title: 'Sales Analysis',
    primaryXAxis: {
      title: 'Products'
    },
    primaryYAxis: {
      title: 'Sales'
    },
    legendSettings: {
      visible: true,
      position: 'Bottom'
    }
  };

  return (
    <PivotViewComponent
      id="chart-pivot"
      dataSourceSettings={{
        dataSource: sampleData as IDataSet[],
        rows: [{ name: 'Country' }],
        columns: [{ name: 'Product' }],
        values: [{ name: 'Sales' }]
      }}
      displayOption={{ view: 'Both' }}
      chartSettings={chartSettings}
      height={500}
    >
      <Inject services={[PivotChart]} />
    </PivotViewComponent>
  );
}
```
