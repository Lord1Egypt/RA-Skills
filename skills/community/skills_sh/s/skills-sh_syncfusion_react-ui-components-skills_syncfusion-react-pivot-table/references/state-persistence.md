# State Persistence

## Table of Contents
- [Overview](#overview)
- [Enable Persistence](#enable-persistence)
- [Save and Load Pivot Layout](#save-and-load-pivot-layout)
- [Complete Example](#complete-example)

## Overview

State persistence enables users to automatically retain the entire configuration of the Pivot Table component in the browser's local storage (cookies). This includes the current layout, field arrangements, sorting, applied filters, and the expanded or collapsed states of fields. By enabling the `enablePersistence` property in the Pivot Table component, all these interactive states and settings are saved automatically. As a result, users can refresh the browser or navigate to different pages and return at any time, knowing that all modified report settings will be retained—ensuring a seamless and uninterrupted data analysis experience.

## Enable Persistence

### Automatic State Persistence

To enable automatic state persistence, set the `enablePersistence` property to **true**:

```ts
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    enableSorting: true,
    drilledMembers: [{ name: 'Country', items: ['France', 'Germany'] }],
    columns: [{ name: 'Year' }, { name: 'Order_Source', caption: 'Order Source' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'In_Stock', caption: 'In Stock' },
    { name: 'Sold', caption: 'Units Sold' }],
    filters: [{ name: 'Product_Categories', caption: 'Product Categories' }]
  }
  let pivotObj: PivotViewComponent;

  return (<PivotViewComponent ref={ (d: PivotViewComponent) => pivotObj = d } id='PivotView' height={350} enablePersistence={true} dataSourceSettings={dataSourceSettings}></PivotViewComponent>);
}
export default App;
```

When `enablePersistence` is enabled, the Pivot Table automatically saves the following to local storage:
- Row and column field configurations
- Field aggregation types
- Applied filters and drill states
- Sorting settings
- Visible and hidden field states
- User preferences and layout changes

## Save and Load Pivot Layout

In addition to automatic state persistence, the Pivot Table component allows you to save and restore the current layout programmatically. By using the `getPersistData` method, you can retrieve the complete state of the Pivot Table component as a serialized string. This string can be stored and later re-applied by passing it to the `loadPersistData` method. This approach offers flexibility for saving user-specific layouts, restoring previous configurations, or implementing custom workflows.

### Save Configuration

use the `getPersistData()` method to save the current configuration:

```ts
const saveConfiguration = () => {
  const persistedData = pivotObj.getPersistData();
  // Store persistedData (in localStorage, database, etc.)
  localStorage.setItem('pivotLayout', persistedData);
};
```

### Load Configuration

use the `loadPersistData()` method to restore a saved configuration:

```ts
const loadConfiguration = () => {
  const persistedData = localStorage.getItem('pivotLayout');
  if (persistedData) {
    pivotObj.loadPersistData(persistedData);
  }
};
```

## Complete Example

```ts
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    enableSorting: true,
    drilledMembers: [{ name: 'Country', items: ['France', 'Germany'] }],
    columns: [{ name: 'Year' }, { name: 'Order_Source', caption: 'Order Source' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'In_Stock', caption: 'In Stock' },
    { name: 'Sold', caption: 'Units Sold' }],
    filters: [{ name: 'Product_Categories', caption: 'Product Categories' }]
  }
  let pivotObj: PivotViewComponent;
  let report: string;

  const save = (): void => {
    report = pivotObj.getPersistData();
    console.log('Configuration saved:', report);
  };

  const load = (): void => {
    if (report) {
      pivotObj.loadPersistData(report);
      console.log('Configuration loaded');
    }
  };

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div style={{ flex: 1 }}>
        <PivotViewComponent 
          ref={ (d: PivotViewComponent) => pivotObj = d } 
          id='PivotView' 
          height={350} 
          enablePersistence={true}
          dataSourceSettings={dataSourceSettings}
        />
      </div>
      <div style={{ width: '150px' }}>
        <ButtonComponent cssClass='e-primary' onClick={save}>Save</ButtonComponent>
        <br/>
        <br/>
        <ButtonComponent cssClass='e-primary' onClick={load}>Load</ButtonComponent>
      </div>
    </div>
  );
}
export default App;
```
