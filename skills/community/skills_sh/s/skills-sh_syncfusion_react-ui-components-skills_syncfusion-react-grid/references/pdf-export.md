# PDF Export in React Grid

## Table of Contents
- [Overview](#overview)
- [Basic Export](#basic-export)
- [PDF Configuration](#pdf-configuration)
- [Headers and Footers](#headers-and-footers)
- [Server-Side Export](#server-side-export)

## Overview

Export grid data to PDF format with customization for headers, footers, styling, and page layout.

## Basic Export

### Enable PDF Export

```tsx
import { GridComponent, Inject, PdfExport } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} allowPdfExport={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
  <Inject services={[PdfExport]} />
</GridComponent>
```

### Add Export Button

```tsx
<GridComponent
  dataSource={data}
  toolbar={['PdfExport']}
  allowPdfExport={true}
>
  {/* columns */}
  <Inject services={[Toolbar, PdfExport]} />
</GridComponent>
```

### Programmatic Export

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const exportToPdf = () => {
    gridRef.current.pdfExport();
  };

  return (
    <div>
      <button onClick={exportToPdf}>Export to PDF</button>

      <GridComponent ref={gridRef} dataSource={data} allowPdfExport={true}>
        {/* columns */}
        <Inject services={[PdfExport]} />
      </GridComponent>
    </div>
  );
}

export default App;
```

## PDF Configuration

### Set File Name and Title

```tsx
const pdfExportProperties = {
  fileName: 'orders.pdf'
};
gridRef.current.pdfExport(pdfExportProperties);
```

### Page Orientation

```tsx
const pdfExportProperties = {
  fileName: 'orders.pdf',
  pageOrientation: 'Landscape'  // or 'Portrait'
};
gridRef.current.pdfExport(pdfExportProperties);
```

### Page Size

```tsx
const pdfExportProperties = {
  pageOrientation: 'Landscape',
  pageSize: 'A4'  // A4, A3, A5, Letter, Legal, etc.
};
gridRef.current.pdfExport(pdfExportProperties);
```

### Export Selected Records

```tsx
const exportSelectedRows = () => {
  const pdfExportProperties = {
    dataSource: gridRef.current.getSelectedRecords()
  };
  gridRef.current.pdfExport(pdfExportProperties);
};
```

## Headers and Footers

### Add Page Header

```tsx
const pdfExportProperties = {
  header : {
    fromTop: 0,
    height: 60,
    contents: [
      {
        type: 'Text',
        value: 'Orders Report',
        position: { x: 150, y: 50 },
        style: { fontSize: 20, fontFamily: 'Calibri' }
      }
    ]
  }
};

gridRef.current.pdfExport(pdfExportProperties);
```

### Add Page Footer

```tsx
const pdfExportProperties = {
  footer : {
    fromBottom: 160,
    height: 60,
    contents: [
      {
        type: 'Text',
        value: 'Page {$current} of {$total}',
        position: { x: 150, y: 20 },
        style: { fontSize: 10 }
      }
    ]
  }
};

gridRef.current.pdfExport(pdfExportProperties);
```

### Add Custom Logo

```tsx
const pdfExportProperties = {
  header : {
    height: 80,
    contents: [
      {
        type: 'Image',
        src: 'logo.png',
        position: { x: 300, y: 50 },
        width: 50,
        height: 50
      },
      {
        type: 'Text',
        value: 'Company Orders',
        position: { x: 350, y: 50 }
      }
    ]
  }
};

gridRef.current.pdfExport(pdfExportProperties);
```

## Server-Side Export

### Server-Side PDF Export

```tsx
const onActionBegin = (args) => {
  if (args.requestType === 'pdfexport') {
    fetch('/api/grid/export-pdf', {
      method: 'POST',
      body: JSON.stringify(gridRef.current.getCurrentViewRecords())
    })
    .then(response => response.blob())
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'orders.pdf';
      link.click();
    });
  }
};

<GridComponent
  dataSource={data}
  actionBegin={onActionBegin}
  allowPdfExport={true}
>
  {/* columns */}
</GridComponent>
```

### Export with Summary

```tsx
const pdfExportProperties = {
  dataSource: gridRef.current.getCurrentViewRecords(),
  footer : {
    height: 80,
    contents: [
      {
        type: 'Text',
        value: `Total Records: ${gridRef.current.pageSettings.totalRecordsCount}`,
        position: { x: 200, y: 20 }
      },
      {
        type: 'Text',
        value: `Exported on: ${new Date().toLocaleDateString()}`,
        position: { x: 200, y: 40 }
      }
    ]
  }
};

gridRef.current.pdfExport(pdfExportProperties);
```
