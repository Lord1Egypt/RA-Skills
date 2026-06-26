---
name: excel-export
description: 'Excel Export in React TreeGrid - export configuration, cell formatting, headers and footers, server-side export, and custom coloring.'
---

# Excel Export

## Table of Contents
- [Basic Excel Export](#basic-excel-export)
- [Headers and Footers](#headers-and-footers)
- [Cell Formatting](#cell-formatting)
- [Server-side Export](#server-side-export)
- [Common Patterns](#common-patterns)
- [Key APIs](#key-apis)

## Basic Excel Export

Export TreeGrid to Excel:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, ExcelExport, Toolbar } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Budget: 10000, Children: [] }
  ];
  const toolbarClick = (args) => {
        if (treegrid && args.item.text === 'Excel Export') {
            treegrid.excelExport();
        }
    };
  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      toolbar={['ExcelExport']}
      allowExcelExport = {true}
      toolbarClick={toolbarClick}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Budget" headerText="Budget" width={120} format="N2" />
      </ColumnsDirective>
      <Inject services={[ExcelExport, Toolbar]} />
    </TreeGridComponent>
  );
}
```


### Configure Excel export:

```tsx
const treeGridRef = React.useRef();

const exportExcel = () => {
  const excelExportProperties = {
    fileName: 'treegrid.xlsx',
    dataSource: data,
    columns: [
      { field: 'TaskID', headerText: 'Task ID', width: 80 },
      { field: 'TaskName', headerText: 'Task Name', width: 160 },
      { field: 'Budget', headerText: 'Budget', width: 120 }
    ]
  };
  
  treeGridRef.current.excelExport(excelExportProperties);
};

<TreeGridComponent ref={treeGridRef} dataSource={data} childMapping="Children"  allowExcelExport = {true}
  toolbarClick={toolbarClick}>
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[ExcelExport]} />
</TreeGridComponent>
```

## Headers and Footers

Add headers and footers to Excel:

```tsx
const excelExportProperties = {
  fileName: 'treegrid.xlsx',
  header: {
    rows: [
      {
        cells: [
          {
            value: 'Project Planning',
            colSpan: 6,
            style: { bold: true, fontSize: 20 }
          }
        ]
      }
    ]
  },
  footer: {
    rows: [
      {
        cells: [
          {
            value: 'Total Records: ' + data.length,
            colSpan: 6
          }
        ]
      }
    ]
  }
};

treeGridRef.current.excelExport(excelExportProperties);
```

## Cell Formatting

Format cells in export:

```tsx
import { getValue } from '@syncfusion/ej2-base';
import { ColumnDirective, ColumnsDirective, Page, TreeGridComponent } from '@syncfusion/ej2-react-treegrid';
import { ExcelExport, Inject, Toolbar } from '@syncfusion/ej2-react-treegrid';
import * as React from 'react';
import { sampleData } from './datasource';
function App() {
    const toolbarOptions = ['ExcelExport'];
    const pageSettings = { pageSize: 7 };
    let treegrid;
    const toolbarClick = (args) => {
        if (treegrid && args.item.text === 'Excel Export') {
            treegrid.excelExport();
        }
    };
    const excelQueryCellInfo = (args) => {
        if (args.column.field === 'duration') {
            if (getValue('data.duration', args) === 0) {
                args.style = { backColor: '#336c12' };
            }
            else if (getValue('data.duration', args) < 3) {
                args.style = { backColor: '#7b2b1d' };
            }
        }
    };
    const queryCellInfo = (args) => {
        if (args.column.field === 'duration') {
            if (getValue('data.duration', args) === 0) {
                args.cell.style.background = '#336c12';
            }
            else if (getValue('data.duration', args) < 3) {
                args.cell.style.background = '#7b2b1d';
            }
        }
    };
    return <TreeGridComponent dataSource={sampleData} treeColumnIndex={1} childMapping='subtasks' allowPaging={true} pageSettings={pageSettings} allowExcelExport={true} height='220' toolbarClick={toolbarClick} ref={g => treegrid = g} toolbar={toolbarOptions} queryCellInfo={queryCellInfo} excelQueryCellInfo={excelQueryCellInfo}>
        <ColumnsDirective>
            <ColumnDirective field='taskID' headerText='Task ID' width='90' textAlign='Right'/>
            <ColumnDirective field='taskName' headerText='Task Name' width='180'/>
            <ColumnDirective field='startDate' headerText='Start Date' width='90' format='yMd' textAlign='Right' type='date'/>
            <ColumnDirective field='duration' headerText='Duration' width='80' textAlign='Right'/>
        </ColumnsDirective>
        <Inject services={[Page, Toolbar, ExcelExport]}/>
    </TreeGridComponent>;
}
;
export default App;
```

## Server-side Export

Export via server for large datasets:

```tsx
const toolbarClick = (args) => {
    if (grid && args.item.id === 'Treegrid_excelexport') {
        grid.serverExcelExport('Home/ExcelExport');
    }
};
```

## Key APIs

| Property | Type | Description |
|---|---|---|
| `excelExport` | method | Export to Excel |
| `fileName` | string | Output file name |
| `dataSource` | array/object | Data to export |
| `columns` | array | Columns to export |
| `header` | object | Header configuration |
| `footer` | object | Footer configuration |
| `customFormat` | string | Cell number format |

## Common Patterns

1. **Hierarchical Export**: Export with tree structure preserved
2. **Filtered Export**: Export only visible rows
3. **Styled Export**: Include colors, fonts, cell styles

