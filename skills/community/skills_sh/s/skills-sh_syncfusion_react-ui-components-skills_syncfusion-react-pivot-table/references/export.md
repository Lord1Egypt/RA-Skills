# Excel, PDF & CSV Export

## Table of Contents
- [Excel Export](#excel-export)
- [CSV Export](#csv-export)
- [Multiple Pivot Table Export](#multiple-pivot-table-export)
- [PDF Export](#pdf-export)
- [Export Events](#export-events)
- [Complete Export Example](#complete-export-example)

## Excel Export

### Basic Excel Export

To export pivot table data to an Excel file (.xlsx format), inject the `ExcelExport` module and set the [`allowExcelExport`](https://ej2.syncfusion.com/react/documentation/api/pivotview/index-default#allowexcelexport) property to **true**. Then, invoke the [`excelExport`](https://ej2.syncfusion.com/react/documentation/api/pivotview/index-default#excelexport) method.

```typescript
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { IDataSet, PivotViewComponent, ExcelExport, Inject } from '@syncfusion/ej2-react-pivotview';
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
  let pivotObj: PivotViewComponent;

  function btnClick(): void {
    pivotObj.excelExport();
  }

  return (
    <div>
      <div className="col-md-9">
        <PivotViewComponent 
          ref={(d: PivotViewComponent) => pivotObj = d} 
          id='PivotView' 
          height={350} 
          dataSourceSettings={dataSourceSettings} 
          allowExcelExport={true}
        >
          <Inject services={[ExcelExport]} />
        </PivotViewComponent>
      </div>
      <div className='col-lg-3 property-section'>
        <ButtonComponent cssClass='e-primary' onClick={btnClick.bind(this)}>
          Export to Excel
        </ButtonComponent>
      </div>
    </div>
  );
}

export default App;
```

## CSV Export

### Basic CSV Export

To export pivot table data to a CSV (comma-separated values) file, invoke the [`csvExport`](https://ej2.syncfusion.com/react/documentation/api/pivotview/index-default#csvexport) method. The CSV format is lightweight and compatible with most spreadsheet applications.

```typescript
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { IDataSet, PivotViewComponent, ExcelExport, Inject } from '@syncfusion/ej2-react-pivotview';
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
  let pivotObj: PivotViewComponent;

  function btnClick(): void {
    pivotObj.csvExport();
  }

  return (
    <div>
      <div className="col-md-9">
        <PivotViewComponent 
          ref={(d: PivotViewComponent) => pivotObj = d} 
          id='PivotView' 
          height={350} 
          dataSourceSettings={dataSourceSettings} 
          allowExcelExport={true}
        >
          <Inject services={[ExcelExport]} />
        </PivotViewComponent>
      </div>
      <div className='col-lg-3 property-section'>
        <ButtonComponent cssClass='e-primary' onClick={btnClick.bind(this)}>
          Export to CSV
        </ButtonComponent>
      </div>
    </div>
  );
}

export default App;
```

## Multiple Pivot Table Export

### Exporting to the Same Worksheet

Multiple Pivot Tables can be exported to a single Excel file on the same worksheet. Use the `multipleExport.type` property set to **AppendToSheet** along with the `pivotTableIds` property to specify which tables to export.

```typescript
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { IDataSet, PivotViewComponent, ExcelExport, Inject } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import * as React from 'react';
import { pivotData } from './datasource';
import { ExcelExportProperties } from '@syncfusion/ej2-grids';

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
  
  let dataSourceSettings1: DataSourceSettingsModel = {
    rows: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    columns: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Amount', caption: 'Sold Amount' }, { name: 'Sold', caption: 'Units Sold' }]
  }
  
  let pivotObj: PivotViewComponent;
  let pivotObj1: PivotViewComponent;

  function btnClick(): void {
    let excelExportProperties: ExcelExportProperties = {
      multipleExport: { type: 'AppendToSheet', blankRows: 2 },
      pivotTableIds: ['PivotView', 'PivotView1']
    };
    pivotObj.excelExport(excelExportProperties, true);
  }

  return (
    <div>
      <div className="col-md-9">
        <PivotViewComponent 
          ref={(d: PivotViewComponent) => pivotObj = d} 
          id='PivotView' 
          height={350} 
          dataSourceSettings={dataSourceSettings} 
          allowExcelExport={true}
        >
          <Inject services={[ExcelExport]} />
        </PivotViewComponent>
      </div>
      <div className="col-md-9">
        <PivotViewComponent 
          ref={(d: PivotViewComponent) => pivotObj1 = d} 
          id='PivotView1' 
          height={350} 
          dataSourceSettings={dataSourceSettings1} 
          allowExcelExport={true}
        >
          <Inject services={[ExcelExport]} />
        </PivotViewComponent>
      </div>
      <div className='col-lg-3 property-section'>
        <ButtonComponent cssClass='e-primary' onClick={btnClick.bind(this)}>
          Export Both Tables
        </ButtonComponent>
      </div>
    </div>
  );
}

export default App;
```

## PDF Export

### Basic PDF Export

To export the pivot table to a PDF file, use the [`pdfExport`](https://ej2.syncfusion.com/react/documentation/api/pivotview/index-default#pdfexport) method. PDF export preserves formatting and layout for professional report generation.

```typescript
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { IDataSet, PivotViewComponent, PdfExport, Inject } from '@syncfusion/ej2-react-pivotview';
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
  let pivotObj: PivotViewComponent;

  function btnClick(): void {
    pivotObj.pdfExport();
  }

  return (
    <div>
      <div className="col-md-9">
        <PivotViewComponent 
          ref={(d: PivotViewComponent) => pivotObj = d} 
          id='PivotView' 
          height={350} 
          dataSourceSettings={dataSourceSettings} 
          allowPdfExport={true}
        >
          <Inject services={[PdfExport]} />
        </PivotViewComponent>
      </div>
      <div className='col-lg-3 property-section'>
        <ButtonComponent cssClass='e-primary' onClick={btnClick.bind(this)}>
          Export to PDF
        </ButtonComponent>
      </div>
    </div>
  );
}

export default App;
```

## Export Events

### Before Export Event

Handle export customization using the `onBeforeExcelExport`, `onBeforePdfExport`, or `onBeforeCsvExport` events:

```typescript
<PivotViewComponent
  onBeforeExcelExport={(args: any) => {
    console.log('Preparing Excel export...');
    // Customize export data before rendering
  }}
  onBeforePdfExport={(args: any) => {
    console.log('Preparing PDF export...');
    // Customize PDF export
  }}
/>
```

### After Export Complete Event

Handle post-export operations using the `onExcelExportComplete`, `onPdfExportComplete`, or `onCsvExportComplete` events:

```typescript
<PivotViewComponent
  onExcelExportComplete={(args: any) => {
    console.log('Excel export completed successfully!');
    // Post-export operations
  }}
/>
```

## Complete Export Example

```typescript
function PivotWithExport() {
  const pivotRef = React.useRef<PivotViewComponent>(null);
  const [exportFormat, setExportFormat] = React.useState('excel');

  const handleExport = () => {
    if (exportFormat === 'excel') {
      pivotRef.current?.excelExport();
    } else if (exportFormat === 'pdf') {
      pivotRef.current?.pdfExport();
    } else if (exportFormat === 'csv') {
      pivotRef.current?.csvExport();
    }
  };

  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: sampleData as IDataSet[],
    rows: [{ name: 'Country' }, { name: 'Region' }],
    columns: [{ name: 'Year' }, { name: 'Quarter' }],
    values: [{ name: 'Sales', caption: 'Total Sales' }],
    formatSettings: [{ name: 'Sales', format: 'C0' }]
  };

  return (
    <>
      <div style={{
        padding: '15px',
        marginBottom: '15px',
        backgroundColor: '#f5f5f5',
        borderRadius: '4px'
      }}>
        <label style={{ marginRight: '15px' }}>
          Export Format:
          <select 
            value={exportFormat}
            onChange={(e) => setExportFormat(e.target.value)}
            style={{ marginLeft: '10px', padding: '5px' }}
          >
            <option value="excel">Excel (.xlsx)</option>
            <option value="pdf">PDF</option>
            <option value="csv">CSV</option>
          </select>
        </label>
        <button 
          onClick={handleExport}
          style={{
            padding: '8px 20px',
            backgroundColor: '#1976D2',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            marginLeft: '10px'
          }}
        >
          Export Now
        </button>
      </div>
      <PivotViewComponent
        ref={pivotRef}
        id="export-pivot"
        dataSourceSettings={dataSourceSettings}
        allowExcelExport={true}
        allowPdfExport={true}
        height={400}
      >
        <Inject services={[ExcelExport, PdfExport]} />
      </PivotViewComponent>
    </>
  );
}

export default PivotWithExport;
```

## Export Format Comparison

| Format | Best For | Advantages | Module Required |
|--------|----------|------------|-----------------|
| Excel (.xlsx) | Data analysis, editing | Sortable, filterable, editable | ExcelExport |
| PDF | Reports, distribution | Professional, fixed layout | PdfExport |
| CSV | Data import, universal use | Lightweight, universal support | ExcelExport |
