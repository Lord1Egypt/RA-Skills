# Excel Export in React Grid

## Table of Contents
- [Overview](#overview)
- [Basic Export](#basic-export)
- [Export Configuration](#export-configuration)
- [Export with Templates](#export-with-templates)
- [Server-Side Export](#server-side-export)

## Overview

Export grid data to Excel format with customization options for formatting, templates, and file naming.

## Basic Export

### Enable Excel Export

```tsx
import { GridComponent, Inject, ExcelExport } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} allowExcelExport={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
  <Inject services={[ExcelExport]} />
</GridComponent>
```

### Add Export Button

```tsx
import { Toolbar } from '@syncfusion/ej2-react-grids';

function App() {

  const gridRef = useRef<GridComponent>(null);

  const toolbarClick = (args: any) => {
    if (args.item.id === 'Grid_excelexport') {
      gridRef.current!.excelExport();
    }
  };
  
  return (
    <GridComponent
      id='Grid'
      dataSource={data}
      toolbar={['ExcelExport']}
      allowExcelExport={true}
      toolbarClick={toolbarClick}
    >
      {/* columns */}
      <Inject services={[Toolbar, ExcelExport]} />
    </GridComponent>
  );
}
```

### Programmatic Export

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const exportToExcel = () => {
    gridRef.current.excelExport();
  };

  return (
    <div>
      <button onClick={exportToExcel}>Export to Excel</button>

      <GridComponent
        ref={gridRef}
        dataSource={data}
        allowExcelExport={true}
      >
        {/* columns */}
        <Inject services={[ExcelExport]} />
      </GridComponent>
    </div>
  );
}

export default App;
```

## Export Configuration

### Set Export File Name

```tsx
const exportToExcel = () => {
  const excelExportProperties = {
    fileName: 'orders.xlsx'
  };
  gridRef.current.excelExport(excelExportProperties);
};
```

### Export Selected Records

```tsx
const exportSelectedRows = () => {
  const excelExportProperties = {
    dataSource: gridRef.current.getSelectedRecords()
  };
  gridRef.current.excelExport(excelExportProperties);
};
```

### Export Filtered Data

```tsx
const exportFilteredData = () => {
  const excelExportProperties = {
    dataSource: gridRef.current.getCurrentViewRecords()
  };
  gridRef.current.excelExport(excelExportProperties);
};
```

### Customize Export Columns

```tsx
const exportToExcel = () => {
  const excelExportProperties = {
    columns: [
      { field: 'OrderID' },
      { field: 'CustomerID' },
      { field: 'Freight' }
    ]
  };
  gridRef.current.excelExport(excelExportProperties);
};
```

## Export with Templates

### Include Column Templates

```
import { ColumnDirective, ColumnsDirective, GridComponent, Inject,
    ExcelExport, Toolbar } from '@syncfusion/ej2-react-grids';
import * as React from 'react';
import { employeeData } from './datasource';

function App() {
    let grid;
    const toolbar = ['ExcelExport'];
    const imageTemplate = (props) => {
        return (
            <div className="image">
                <img
                    src={'data:image/jpeg;base64,' + props.EmployeeImage}
                    alt={props.EmployeeID}
                />
            </div>
        );
    };
    const mailTemplate = (props) => {
        return (
            <div className="link">
                <a href={'mailto:' + props.EmailID}>{props.EmailID}</a>
            </div>
        );
    };
    const toolbarClick = (args) => {
        if (grid && args['item'].id === 'ColumnTemplateGrid_excelexport') {
            grid.excelExport();
        }
    };
    const excelQueryCellInfo = (args) => {
        if (args.column.headerText === 'Employee Image') {
            args.image = {
                base64: args.data.EmployeeImage,
                height: 70,
                width: 70,
            };
        }
        if (args.column.headerText === 'Email ID') {
            args.hyperLink = {
                target: 'mailto:' + args.data.EmailID,
                displayText: args.data.EmailID,
            };
        }
    };
    
    return (
        <GridComponent id="ColumnTemplateGrid" ref={(g) => (grid = g)} dataSource={employeeData}
            toolbar={toolbar} allowExcelExport={true} toolbarClick={toolbarClick} excelQueryCellInfo={excelQueryCellInfo}
            height="260">
            <ColumnsDirective>
                <ColumnDirective headerText="Employee Image" width="180" template={imageTemplate} textAlign="Center" />
                <ColumnDirective field="EmployeeID" headerText="Employee ID" width="125" />
                <ColumnDirective field="FirstName" headerText="Name" width="120" />
                <ColumnDirective field="EmailID" headerText="Email ID" template={mailTemplate} width="170" />
            </ColumnsDirective>
            <Inject services={[Toolbar, ExcelExport]} />
        </GridComponent>
    );
}
export default App;
```

### Custom Export Format

```tsx
const onBeforeExcelExport = (args) => {
  // Customize workbook before export
  args.workbook.worksheets[0].name = 'Orders';
};

<GridComponent
  dataSource={data}
  beforeExcelExport={onBeforeExcelExport}
  allowExcelExport={true}
>
  {/* columns */}
  <Inject services={[ExcelExport]} />
</GridComponent>
```

## Server-Side Export

### Enable Server-Side Excel Export

```tsx
const onActionBegin = (args) => {
  if (args.requestType === 'excel') {
    // Send export request to server
    fetch('/api/grid/export-excel', {
      method: 'POST',
      body: JSON.stringify(args.gridObj.getCurrentViewRecords())
    })
    .then(response => response.blob())
    .then(blob => {
      // Trigger download
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'orders.xlsx';
      a.click();
    });
  }
};

<GridComponent
  dataSource={data}
  actionBegin={onActionBegin}
>
  {/* columns */}
</GridComponent>
```

