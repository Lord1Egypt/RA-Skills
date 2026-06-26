# Row and Column Management

## Table of Contents
- [Cell Template](#cell-template)
- [Width and Height](#width-and-height)
- [Row Height](#row-height)
- [Column Width](#column-width)
- [Column Resizing](#column-resizing)
- [Reorder](#reorder)
- [Text Wrap](#text-wrap)
- [Text Align](#text-align)
- [AutoFit](#autofit)

## Cell Template

You can customize how each cell in the Pivot Table looks by using the `cellTemplate` property. With `cellTemplate`, you can render custom HTML content or JSX elements in every cell. This helps you display cell values in any format you prefer, such as adding icons, colors, or other visual elements for better understanding.

> The `cellTemplate` property is triggered whenever the Pivot Table report configuration is updated through code-behind or UI actions such as sorting, filtering, and more. Therefore, binding a large dataset to the Pivot Table while defining a template for this property, or assigning a complex template to it, may lead to flickering issues in the Pivot Table UI.

### Basic Cell Template

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  function cellTemplate(props: any): JSX.Element {
    return (
      <span style={{ padding: '8px' }}>
        {props.cellInfo?.value}
      </span>
    );
  }

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
      cellTemplate={cellTemplate}
    />
  );
}

export default App;
```

### Cell Template with Icons

For example, in the following sample, each cell's value is combined with a trend icon to give users a quick visual reference:

```typescript
import { IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { renewableEnergy } from './datasource';

function App() {
  function cellTemplate(props: any): JSX.Element {
    return (<span className="tempwrap sb-icon-neutral pv-icons"></span>);
  }

  let dataSourceSettings: DataSourceSettingsModel = {
    dataSource: renewableEnergy as IDataSet[],
    expandAll: true,
    enableSorting: true,
    formatSettings: [{ name: 'ProCost', format: 'C0' }],
    rows: [
        { name: 'Year', caption: 'Production Year' }
    ],
    columns: [
        { name: 'EnerType', caption: 'Energy Type' },
        { name: 'EneSource', caption: 'Energy Source' }
    ],
    values: [
        { name: 'ProCost', caption: 'Revenue Growth' }
    ],
    filters: []
  }
  let pivotObj: PivotViewComponent;

  function trend(): void {
    let cTable: HTMLElement[] = [].slice.call(document.getElementsByClassName("e-table"));
    let colLen: number = pivotObj.pivotValues[3].length;
    let cLen: number = cTable[3].children[0].children.length;
    let rLen: number = cTable[3].children[1].children.length;
    let rowIndx: number;

    for (let k: number = 0; k < rLen; k++) {
        if (pivotObj.pivotValues[k] && pivotObj.pivotValues[k][0] !== undefined) {
            rowIndx = ((pivotObj.pivotValues[k][0]) as IAxisSet).rowIndex;
            break;
        }
    }
    let rowHeaders: HTMLElement[] = [].slice.call(cTable[2].children[1].querySelectorAll('td'));
    let rows: IFieldOptions[] = pivotObj.dataSourceSettings.rows as IFieldOptions[];
    if (rowHeaders.length > 1) {
        for (let i: number = 0, Cnt = rows; i < Cnt.length; i++) {
            let fields: any = {};
            let fieldHeaders: any = [];
            for (let j: number = 0, Lnt = rowHeaders; j < Lnt.length; j++) {
                let header: any = rowHeaders[j];
                if (header.className.indexOf('e-gtot') === -1 && header.className.indexOf('e-rowsheader') > -1 && header.getAttribute('fieldname') === rows[i].name) {\n                    var headerName = rowHeaders[j].getAttribute('fieldname') + '_' + rowHeaders[j].textContent;
                    fields[rowHeaders[j].textContent] = j;
                    fieldHeaders.push(rowHeaders[j].textContent);
                }
            }
            if (i === 0) {
                for (let rnt: number = 0, Lnt = fieldHeaders; rnt < Lnt.length; rnt++) {
                    if (rnt !== 0) {
                        let row: number = fields[fieldHeaders[rnt]];
                        let prevRow: number = fields[fieldHeaders[rnt - 1]];
                        for (let j: number = 0, ci = 1; j < cLen && ci < colLen; j++ , ci++) {
                            let node: HTMLElement = cTable[3].children[1].children[row].childNodes[j] as HTMLElement;
                            let prevNode: HTMLElement = cTable[3].children[1].children[prevRow].childNodes[j] as HTMLElement;
                            let ri: any = undefined;
                            let prevRi: any = undefined;
                            if (node) {
                                ri = node.getAttribute("index");
                            }
                            if (prevNode) {
                                prevRi = prevNode.getAttribute("index");
                            }
                            if (ri && ri < [].slice.call(pivotObj.pivotValues).length) {
                                if ((pivotObj.pivotValues[prevRi][ci] as IAxisSet).value > (pivotObj.pivotValues[ri][ci]  as IAxisSet).value &&
                                 node.querySelector('.tempwrap')) {
                                    let trendElement: HTMLElement = node.querySelector('.tempwrap');
                                    trendElement.className = trendElement.className.replace('sb-icon-neutral', 'sb-icon-loss');
                                } else if ((pivotObj.pivotValues[prevRi][ci]  as IAxisSet).value < (pivotObj.pivotValues[ri][ci]  as IAxisSet).value &&
                                 node.querySelector('.tempwrap')) {
                                    let trendElement: HTMLElement = node.querySelector('.tempwrap');
                                    trendElement.className = trendElement.className.replace('sb-icon-neutral', 'sb-icon-profit');
                                }
                            }
                        }
                    }
                }
            }
        }
    }
  }

  return (
    <PivotViewComponent
      ref={(d: PivotViewComponent) => pivotObj = d}
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
      cellTemplate={cellTemplate}
      dataBound={trend}
    />
  );
}

export default App;
```

## Width and Height

Setting appropriate dimensions for the Pivot Table ensures optimal display and better user experience across different screen sizes and layouts. You can define the Pivot Table's dimensions using the `height` and `width` properties to meet your specific requirements.

These dimension properties support multiple formats:

* **Pixel**: Specify exact dimensions using numeric values or pixel units (e.g., `100`, `"100px"`, `"200px"`)
* **Percentage**: Set dimensions relative to the parent container (e.g., `"100%"`, `"200%"`)
* **Auto**: Available only for `height`. When set to **auto**, the Pivot Table expands beyond its parent container height without showing a vertical scrollbar

> **Note:** The Pivot Table maintains a minimum width of **400px** to ensure proper display and functionality, even if a smaller width is specified.

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      width={'100%'}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

## Row Height

Adjusting the row height in the Pivot Table helps make your data easier to view and interact with. You can use the `rowHeight` property within the `gridSettings` options to control how much space each row occupies.

> By default, `rowHeight` is set to **36** pixels for desktop layouts and **48** pixels for mobile layouts.

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { GridSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/gridsettings';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let gridSettings: GridSettings = {
    rowHeight: 60
  } as GridSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      gridSettings={gridSettings}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

## Column Width

Controlling the width of columns allows users to view their data in the Pivot Table more clearly. You can use the `columnWidth` property under `gridSettings`.

> By default, `columnWidth` is set to **110** pixels for all columns except the first one. The first column is assigned a width of **250** pixels if the grouping bar is enabled, or **200** pixels when it is not.

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { GridSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/gridsettings';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let gridSettings: GridSettings = {
    columnWidth: 120
  } as GridSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      gridSettings={gridSettings}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

### Adjust Width Based on Columns

By default, when the component width exceeds the total width of all columns, the columns are automatically stretched to fill the available space. To prevent this, set the `allowAutoResizing` property to **false** in `gridSettings`. This ensures that the Pivot Table adjusts its overall width to match the combined width of all columns.

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { GridSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/gridsettings';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let gridSettings: GridSettings = {
    allowAutoResizing: false
  } as GridSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    rows: [{ name: 'Country' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }]
  }

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      gridSettings={gridSettings}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

## Column Resizing

Column resizing helps users adjust the column widths to better view and compare data. Users can easily resize columns by clicking and dragging the right edge of any column header.

This option is enabled by default. To control column resizing, set the `allowResizing` property in `gridSettings` to **true** or **false** as needed.

> In right-to-left (RTL) mode, users should click and drag the left edge of the header cell to resize the column.

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { GridSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/gridsettings';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let gridSettings: GridSettings = {
    allowResizing: true
  } as GridSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      gridSettings={gridSettings}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

## Reorder

The reorder option provides users with the flexibility to reorganize column headers within the Pivot Table by dragging and dropping them to different positions. To enable this option, set the `allowReordering` property to **true** in `gridSettings`.

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { GridSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/gridsettings';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let gridSettings: GridSettings = {
    allowReordering: true
  } as GridSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      gridSettings={gridSettings}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

## Text Wrap

The Pivot Table allows users to wrap cell content to the next line when the content exceeds the cell width. To enable text wrap, set the `allowTextWrap` property to **true** in `gridSettings`.

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { GridSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/gridsettings';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let gridSettings: GridSettings = {
    allowTextWrap: true
  } as GridSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      gridSettings={gridSettings}
      dataSourceSettings={dataSourceSettings}
    />
  );
}

export default App;
```

## Text Align

Text alignment provides flexibility in positioning content within cells. You can align the content using the `textAlign` and `headerTextAlign` properties in the `columnRender` event under `gridSettings`.

**Available alignment options:**
* `Left` - Positions the content on the left side of the cell
* `Right` - Positions the content on the right side of the cell
* `Center` - Positions the content in the center of the cell
* `Justify` - Distributes the content evenly across the cell width

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { GridSettings } from '@syncfusion/ej2-pivotview/src/pivotview/model/gridsettings';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let gridSettings: GridSettings = {
    columnRender: columnRender.bind(this)
  } as GridSettings;

  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: true,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }

  function columnRender(args: any) {
    for (let i: number = 0; i < args.columns.length; i++) {
      if(args.stackedColumns[0]){
          args.stackedColumns[0].textAlign = "Right";
      }
      if(args.stackedColumns[1]){
          args.stackedColumns[1].textAlign = 'Center';
      }
    }
  }

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
      gridSettings={gridSettings}
    />
  );
}

export default App;
```

## AutoFit

The AutoFit option allows users to easily adjust Pivot Table columns so that each column matches the width of its content. You can use the `autoFitColumns()` method from the grid instance to automatically resize all columns based on their cell content.

```typescript
import { IDataSet, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';

function App() {
  let dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: true,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  }
  let pivotObj: PivotViewComponent;

  function onDataBound() {
    pivotObj.grid.autoFitColumns();
  }

  return (
    <PivotViewComponent
      id='PivotView'
      height={350}
      dataSourceSettings={dataSourceSettings}
      dataBound={onDataBound.bind(this)}
      ref={(pivotView: PivotViewComponent) => pivotObj = pivotView}
    />
  );
}

export default App;
```
