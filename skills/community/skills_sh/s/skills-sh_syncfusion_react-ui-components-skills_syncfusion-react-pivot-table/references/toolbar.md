# Toolbar Controls & Customization

## Table of Contents
- [Overview](#overview)
- [Built-in Toolbar Options](#built-in-toolbar-options)
- [Configure Toolbar Items](#configure-toolbar-items)
- [Chart Type Dropdown](#chart-type-dropdown)
- [Complete Example](#complete-example)

## Overview

The toolbar in the React Pivot Table component provides easy access to commonly used features, such as switching between a pivot table and a pivot chart, changing chart types, applying conditional formatting, exporting data, and more. To enable the toolbar, set the `showToolbar` property to **true**. Additionally, the `toolbar` property accepts a collection of built-in toolbar options, allowing users to interact with the Pivot Table efficiently at runtime.

To use the toolbar, you need to inject the `Toolbar` module into the Pivot Table.

## Built-in Toolbar Options

The following table lists the built-in toolbar options and their actions:

| Built-in Toolbar Options | Actions |
|--------------------------|----------|
| New | Creates a new report |
| Save | Saves the current report |
| Save As | Saves the current report with a new name |
| Rename | Changes the name of the current report |
| Delete | Removes the current report |
| Load | Opens a report from the report list |
| Grid | Displays the pivot table |
| Chart | Shows a pivot chart with options to select different chart types and enable or disable multiple axes |
| Exporting | Exports the pivot table as PDF, Excel, or CSV, or the pivot chart as a PDF or image |
| Sub-total | Shows or hides subtotals in the pivot table |
| Grand Total | Shows or hides grand totals in the pivot table |
| Conditional Formatting | Opens a pop-up to apply formatting to cells based on conditions |
| Number Formatting | Opens a pop-up to apply number formatting to cells |
| Field List | Opens the field list pop-up to configure the `dataSourceSettings` |
| MDX | Displays the MDX query used to retrieve data from an OLAP data source. **Note**: This option applies only to OLAP data sources. |

> The order of toolbar options can be changed by simply moving the position of items in the toolbar collection. Also, if you want to remove any toolbar option, it can be simply omitted from the toolbar array.

## Configure Toolbar Items

### Basic Toolbar Configuration

```ts
import * as React from 'react';
import {
    PivotViewComponent, Inject, FieldList, CalculatedField,
    Toolbar, PDFExport, ExcelExport, ConditionalFormatting, SaveReportArgs,
    FetchReportArgs, LoadReportArgs, RemoveReportArgs, RenameReportArgs, NumberFormatting
} from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { ToolbarItems } from '@syncfusion/ej2-pivotview/src/common/base/enum';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };
  let pivotObj: PivotViewComponent;
  let toolbarOptions: ToolbarItems[] = ['New', 'Save', 'SaveAs', 'Rename', 'Remove', 'Load',
        'Grid', 'Chart', 'Export', 'SubTotal', 'GrandTotal', 'ConditionalFormatting', 'NumberFormatting', 'FieldList'];

  function saveReport(args: any): void {
    let reports: SaveReportArgs[] = [];
    let isSaved: boolean = false;
    if (localStorage.pivotviewReports && localStorage.pivotviewReports !== "") {
      reports = JSON.parse(localStorage.pivotviewReports);
    }
    if (args.report && args.reportName && args.reportName !== '') {
      reports.map(function (item: any): any {
        if (args.reportName === item.reportName) {
          item.report = args.report; isSaved = true;
        }
      });
      if (!isSaved) {
        reports.push(args);
      }
      localStorage.pivotviewReports = JSON.stringify(reports);
    }
  }

  function fetchReport(args: FetchReportArgs): void {
    let reportCollection: string[] = [];
    let reeportList: string[] = [];
    if (localStorage.pivotviewReports && localStorage.pivotviewReports !== "") {
      reportCollection = JSON.parse(localStorage.pivotviewReports);
    }
    reportCollection.map(function (item: any): void { reeportList.push(item.reportName); });
    args.reportName = reeportList;
  }

  function loadReport(args: LoadReportArgs): void {
    let reportCollection: string[] = [];
    if (localStorage.pivotviewReports && localStorage.pivotviewReports !== "") {
      reportCollection = JSON.parse(localStorage.pivotviewReports);
    }
    reportCollection.map(function (item: any): void {
      if (args.reportName === item.reportName) {
        args.report = item.report;
      }
    });
    if (args.report) {
      pivotObj.dataSourceSettings = JSON.parse(args.report).dataSourceSettings;
    }
  }

  function removeReport(args: RemoveReportArgs): void {
    let reportCollection: any[] = [];
    if (localStorage.pivotviewReports && localStorage.pivotviewReports !== "") {
      reportCollection = JSON.parse(localStorage.pivotviewReports);
    }
    for (let i: number = 0; i < reportCollection.length; i++) {
      if (reportCollection[i].reportName === args.reportName) {
        reportCollection.splice(i, 1);
      }
    }
    if (localStorage.pivotviewReports && localStorage.pivotviewReports !== "") {
      localStorage.pivotviewReports = JSON.stringify(reportCollection);
    }
  }

  function renameReport(args: RenameReportArgs): void {
    let reportCollection: string[] = [];
    if (localStorage.pivotviewReports && localStorage.pivotviewReports !== "") {
      reportCollection = JSON.parse(localStorage.pivotviewReports);
    }
    reportCollection.map(function (item: any): any { if (args.reportName === item.reportName) { item.reportName = args.rename; } });
    if (localStorage.pivotviewReports && localStorage.pivotviewReports !== "") {
      localStorage.pivotviewReports = JSON.stringify(reportCollection);
    }
  }

  function newReport(): void {
    pivotObj.setProperties({ dataSourceSettings: { columns: [], rows: [], values: [], filters: [] } }, false);
  }

  return (<PivotViewComponent id='PivotView' ref={ (d: PivotViewComponent) => pivotObj = d } dataSourceSettings={dataSourceSettings} width={'100%'} height={350} showFieldList={true} gridSettings={{ columnWidth: 140 }} allowExcelExport={true} allowConditionalFormatting={true} allowNumberFormatting={true} allowPdfExport={true} showToolbar={true} allowCalculatedField={true} displayOption={{ view: 'Both' }} toolbar={toolbarOptions} newReport={newReport.bind(this)} renameReport={renameReport.bind(this)} removeReport={removeReport.bind(this)} loadReport={loadReport.bind(this)} fetchReport={fetchReport.bind(this)} saveReport={saveReport.bind(this)}><Inject services={[FieldList, CalculatedField, Toolbar, PDFExport, ExcelExport, ConditionalFormatting, NumberFormatting]} /></PivotViewComponent>);
}
export default App;
```

## Chart Type Dropdown

### Show Desired Chart Types

By default, the dropdown menu in the toolbar displays all available chart types. However, you may want to show only specific chart types based on your needs. Use the `chartTypes` property to define a list of chart types that will appear in the dropdown menu.

For example, to show only Column, Bar, Line, and Area chart types:

```ts
import * as React from 'react';
import {
    PivotViewComponent, Inject, Toolbar
} from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };
  let pivotObj: PivitViewComponent;
  let toolbarOptions: ToolbarItems[] = ['Grid','Chart'];
  let chartTypes: any = ['Column', 'Bar', 'Line', 'Area'];

  return (<PivotViewComponent id='PivotView' ref={ (d: PivitViewComponent) => pivotObj = d } dataSourceSettings={dataSourceSettings} width={'100%'} height={350} showToolbar={true} toolbar={toolbarOptions} displayOption={{ view: 'Both' }} chartTypes={chartTypes} ><Inject services={[ Toolbar]} /></PivotViewComponent>);
}
export default App;
```

To learn more about supported chart types, see the [Pivot Chart documentation](https://ej2.syncfusion.com/react/documentation/pivotview/pivot-chart#chart-types).

## Complete Example

```ts
import * as React from 'react';
import {
    PivotViewComponent, Inject, FieldList, Toolbar
} from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { pivotData } from './datasource';

function ToolbarExample() {
  const [toolbarConfig, setToolbarConfig] = React.useState<any>(['Grid', 'Chart', 'Export', 'SubTotal', 'GrandTotal']);

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };
  let pivotObj: PivotViewComponent;

  return (<PivotViewComponent id='PivotView' ref={ (d: PivotViewComponent) => pivotObj = d } dataSourceSettings={dataSourceSettings} width={'100%'} height={350} gridSettings={{ columnWidth: 140 }} showToolbar={true} displayOption={{ view: 'Both' }} toolbar={toolbarConfig}><Inject services={[FieldList, Toolbar]} /></PivotViewComponent>);
}
export default ToolbarExample;
```
