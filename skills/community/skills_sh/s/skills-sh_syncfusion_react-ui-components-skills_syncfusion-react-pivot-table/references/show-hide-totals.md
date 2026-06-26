# Show/Hide Totals Configuration

## Table of Contents
- [Grand Totals](#grand-totals)
- [Sub-totals](#sub-totals)
- [Sub-totals Position](#sub-totals-position)
- [Toolbar Integration](#toolbar-integration)
- [Complete Example](#complete-example)

## Grand Totals

### Show or Hide Grand Totals

Allows you to show or hide grand totals in rows and columns using the `showGrandTotals` property. By default, `showGrandTotals`, `showRowGrandTotals`, and `showColumnGrandTotals` properties are set to **true**.

To hide the grand totals in rows and columns, set the `showGrandTotals` property in `dataSourceSettings` to **false**:

```ts
import { FieldList, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
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
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
    showGrandTotals: false
  }
  let pivotObj: PivotViewComponent;
  
  return (<PivotViewComponent ref={ (d: PivotViewComponent) => pivotObj = d } id='PivotView' height={350} dataSourceSettings={dataSourceSettings} showFieldList={true} ><Inject services={[FieldList]}/> </PivotViewComponent>);
}
export default App;
```

End users can also hide grand totals for rows or columns separately by setting the `showRowGrandTotals` or `showColumnGrandTotals` properties to **false** respectively:

```ts
let dataSourceSettings: DataSourceSettingsModel = {
  // ... other settings
  showRowGrandTotals: false,      // Hide row grand totals only
  showColumnGrandTotals: false    // Hide column grand totals only
};
```

## Sub-totals

### Show or Hide Sub-totals

Allows you to show or hide sub-totals in rows and columns using the `showSubTotals` property. By default, `showSubTotals`, `showRowSubTotals`, and `showColumnSubTotals` properties are set to **true**.

To hide all the sub-totals in rows and columns, set the `showSubTotals` property to **false**:

```ts
import { FieldList, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    allowLabelFilter: true,
    allowValueFilter: true,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
    showSubTotals: false
  }
  let pivotObj: PivotViewComponent;
  
  return (<PivotViewComponent ref={ (d: PivotViewComponent) => pivotObj = d } id='PivotView' height={350} dataSourceSettings={dataSourceSettings} showFieldList={true} ><Inject services={[FieldList]}/> </PivotViewComponent>);
}
export default App;
```

End users can also hide sub-totals for rows or columns separately by setting `showRowSubTotals` or `showColumnSubTotals` properties to **false**.

### Show/Hide Sub-totals for Specific Fields

To hide sub-totals for a specific field in row or column axis, set the `showSubTotals` property in the `row` or `column` object to **false**:

```ts
let dataSourceSettings: DataSourceSettingsModel = {
  columns: [{ name: 'Year', caption: 'Production Year', showSubTotals: false }, { name: 'Quarter' }],
  dataSource: pivotData as IDataSet[],
  expandAll: false,
  filters: [],
  drilledMembers: [{ name: 'Country', items: ['France'] }],
  formatSettings: [{ name: 'Amount', format: 'C0' }],
  rows: [{ name: 'Country', showSubTotals: false }, { name: 'Products' }],
  values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
}
```

## Sub-totals Position

### Show Sub-totals at Top or Bottom

Allows you to show sub-totals either at top or bottom of the header group in rows and columns using the `subTotalsPosition` property. By default, `subTotalsPosition` is set to **Auto**, which means column sub-totals are displayed at the bottom and row sub-totals are displayed at the top.

To show sub-totals at the top of the header group in rows and columns, set the `subTotalsPosition` property to **Top**:

```ts
import { FieldList, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }, { name: 'Year', items: ['FY 2015'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
    subTotalsPosition: 'Top'
  }
  let pivotObj: PivotViewComponent;
  
  return (<PivotViewComponent ref={ (d: PivotViewComponent) => pivotObj = d } id='PivotView' height={350} dataSourceSettings={dataSourceSettings} showFieldList={true} ><Inject services={[FieldList]}/> </PivotViewComponent>);
}
export default App;
```

To show sub-totals at the bottom of the header group, set `subTotalsPosition` to **Bottom**:

```ts
let dataSourceSettings: DataSourceSettingsModel = {
  // ... other settings
  subTotalsPosition: 'Bottom'
};
```

## Toolbar Integration

### Show or Hide Totals Using Toolbar

You can also achieve this using built-in toolbar options by setting the `showToolbar` property to **true** and including **GrandTotal** and **SubTotal** items within the `toolbar` property. End users can see "Show/Hide Grand totals" and "Show/Hide Sub totals" icons in the toolbar UI.

The grand totals and sub-totals can be dynamically displayed at the top or bottom of the pivot table's row and column axes using the built-in options in the toolbar.

```ts
import * as React from 'react';
import {
    PivotViewComponent, Toolbar, Inject
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
  let toolbarOptions: ToolbarItems[] = ['SubTotal', 'GrandTotal'];
  
  return (<PivotViewComponent id='PivotView' ref={ (d: PivotViewComponent) => pivotObj = d } dataSourceSettings={dataSourceSettings} width={'100%'} height={350} gridSettings={{ columnWidth: 140 }} showToolbar={true} displayOption={{ view: 'Both' }} toolbar={toolbarOptions}><Inject services={[Toolbar]} /></PivotViewComponent>);
}
export default App;
```

## Complete Example

```ts
import { FieldList, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function TotalConfiguration() {
  const [showGrand, setShowGrand] = React.useState(true);
  const [showSub, setShowSub] = React.useState(true);
  const [position, setPosition] = React.useState<'Top' | 'Bottom'>('Top');

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
    showGrandTotals: showGrand,
    showSubTotals: showSub,
    subTotalsPosition: position
  };
  let pivotObj: PivotViewComponent;

  return (
    <>
      <div style={{ marginBottom: '15px' }}>
        <label>
          <input type="checkbox" checked={showGrand} onChange={(e) => setShowGrand(e.target.checked)} />
          Show Grand Totals
        </label>
        <label style={{ marginLeft: '20px' }}>
          <input type="checkbox" checked={showSub} onChange={(e) => setShowSub(e.target.checked)} />
          Show Sub Totals
        </label>
        <select value={position} onChange={(e) => setPosition(e.target.value as any)} style={{ marginLeft: '20px' }}>
          <option value="Top">Position: Top</option>
          <option value="Bottom">Position: Bottom</option>
        </select>
      </div>
      <PivotViewComponent ref={ (d: PivotViewComponent) => pivotObj = d } id='PivotView' height={350} dataSourceSettings={dataSourceSettings} showFieldList={true} ><Inject services={[FieldList]}/> </PivotViewComponent>
    </>
  );
}
export default TotalConfiguration;
```
