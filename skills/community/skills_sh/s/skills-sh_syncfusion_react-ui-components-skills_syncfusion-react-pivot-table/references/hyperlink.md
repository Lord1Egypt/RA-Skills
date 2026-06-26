# Hyperlink Configuration & Navigation

## Table of Contents
- [Hyperlink for All Cells](#hyperlink-for-all-cells)
- [Hyperlink for Row Headers](#hyperlink-for-row-headers)
- [Hyperlink for Column Headers](#hyperlink-for-column-headers)
- [Hyperlink for Value Cells](#hyperlink-for-value-cells)
- [Hyperlink for Summary Cells](#hyperlink-for-summary-cells)
- [Conditional Hyperlinks](#conditional-hyperlinks)
- [Custom Styling](#custom-styling)

## Hyperlink for All Cells

### Enable Hyperlinks for All Cells

The pivot table provides an option to display hyperlinks across **all cells** currently visible in the table. To enable this functionality, set the [`showHyperlink`](https://ej2.syncfusion.com/react/documentation/api/pivotview/hyperlinkSettingsModel/#showhyperlink) property to **true** within the [`hyperlinkSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/#hyperlinksettings).

Once enabled, hyperlinks will be shown consistently in row headers, column headers, value cells, and summary cells.

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    enableSorting: true,
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    filters: []
  }

  return (
    <PivotViewComponent 
      height={350} 
      id='PivotView' 
      dataSourceSettings={dataSourceSettings} 
      hyperlinkSettings={{
        showHyperlink: true,
        cssClass: 'e-custom-hyperlink'
      }}
    />
  );
}

export default App;
```

## Hyperlink for Row Headers

### Enable Hyperlinks Specific to Row Headers

The pivot table provides a way to display hyperlinks specifically in **row header cells** that are currently visible. To enable this functionality, set the [`showRowHeaderHyperlink`](https://ej2.syncfusion.com/react/documentation/api/pivotview/hyperlinkSettingsModel/#showrowheaderhyperlink) property to **true** within the [`hyperlinkSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/#hyperlinksettings). This ensures that only the row headers will display hyperlinks, while other cell types remain unaffected.

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    enableSorting: true,
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    drilledMembers: [{ name: 'Country', items: ['France'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    filters: []
  }

  return (
    <PivotViewComponent 
      height={350} 
      id='PivotView' 
      dataSourceSettings={dataSourceSettings} 
      hyperlinkSettings={{
        showRowHeaderHyperlink: true,
        cssClass: 'e-custom-hyperlink'
      }}
    />
  );
}

export default App;
```

## Hyperlink for Column Headers

### Enable Hyperlinks for Column Headers

To display hyperlinks specifically in **column header cells**, set the [`showColumnHeaderHyperlink`](https://ej2.syncfusion.com/react/documentation/api/pivotview/hyperlinkSettingsModel/#showcolumnheaderhyperlink) property to **true** within the [`hyperlinkSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/#hyperlinksettings).

```typescript
<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  hyperlinkSettings={{
    showColumnHeaderHyperlink: true,
    cssClass: 'e-custom-hyperlink'
  }}
/>
```

## Hyperlink for Value Cells

### Enable Hyperlinks for Value Cells

To display hyperlinks specifically in **value cells** (data cells), set the [`showValueCellHyperlink`](https://ej2.syncfusion.com/react/documentation/api/pivotview/hyperlinkSettingsModel/#showvaluecellhyperlink) property to **true** within the [`hyperlinkSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/#hyperlinksettings).

```typescript
<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  hyperlinkSettings={{
    showValueCellHyperlink: true,
    cssClass: 'e-custom-hyperlink'
  }}
/>
```

## Hyperlink for Summary Cells

### Enable Hyperlinks for Summary Cells

To display hyperlinks specifically in **summary cells** (totals and grand totals), set the [`showSummaryCellHyperlink`](https://ej2.syncfusion.com/react/documentation/api/pivotview/hyperlinkSettingsModel/#showsummarycellhyperlink) property to **true** within the [`hyperlinkSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/#hyperlinksettings).

```typescript
<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  hyperlinkSettings={{
    showSummaryCellHyperlink: true,
    cssClass: 'e-custom-hyperlink'
  }}
/>
```

## Conditional Hyperlinks

### Hyperlinks Based on Header Text

Configure hyperlinks to appear based on specific header text using the [`headerText`](https://ej2.syncfusion.com/react/documentation/api/pivotview/hyperlinkSettingsModel/#headertext) property:

```typescript
<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  hyperlinkSettings={{
    headerText: 'USA',  // Display hyperlinks for cells with 'USA' header
    cssClass: 'e-custom-hyperlink'
  }}
/>
```

### Hyperlinks with Conditional Settings

Use the [`conditionalSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/hyperlinkSettingsModel/#conditionalsettings) property to apply conditional logic for displaying hyperlinks:

```typescript
<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  hyperlinkSettings={{
    conditionalSettings: [
      {
        measure: 'Sales',
        condition: 'GreaterThan',
        value1: 5000,
        cells: ['rowHeaderCell']
      }
    ],
    cssClass: 'e-custom-hyperlink'
  }}
/>
```

## Custom Styling

### Apply Custom CSS Class to Hyperlinks

You can apply custom styling to hyperlinks using the [`cssClass`](https://ej2.syncfusion.com/react/documentation/api/pivotview/hyperlinkSettingsModel/#cssclass) property in [`hyperlinkSettings`](https://ej2.syncfusion.com/react/documentation/api/pivotview/#hyperlinksettings):

```typescript
<PivotViewComponent
  dataSourceSettings={dataSourceSettings}
  hyperlinkSettings={{
    showHyperlink: true,
    cssClass: 'e-hyperlink-custom'
  }}
/>
```

Add corresponding CSS styles:

```css
.e-hyperlink-custom {
  color: #1976D2;
  text-decoration: underline;
  font-weight: bold;
  cursor: pointer;
}

.e-hyperlink-custom:hover {
  color: #1565C0;
  text-decoration: none;
}
```

## Complete Hyperlink Example

```typescript
function PivotWithHyperlinks() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: sampleData as IDataSet[],
    rows: [{ name: 'Country' }, { name: 'Region' }],
    columns: [{ name: 'Year' }, { name: 'Quarter' }],
    values: [{ name: 'Sales', caption: 'Total Sales' }],
    formatSettings: [{ name: 'Sales', format: 'C0' }]
  };

  const hyperlinkSettings = {
    showHyperlink: true,
    showRowHeaderHyperlink: true,
    showColumnHeaderHyperlink: true,
    showValueCellHyperlink: true,
    showSummaryCellHyperlink: true,
    cssClass: 'e-custom-hyperlink'
  };

  return (
    <PivotViewComponent
      id="hyperlink-pivot"
      dataSourceSettings={dataSourceSettings}
      hyperlinkSettings={hyperlinkSettings}
      height={400}
    />
  );
}

export default PivotWithHyperlinks;
```  hyperlinkSettings={{
    showHyperlink: false
  }}
/>
```
