---
name: pdf-export
description: 'PDF Export in React TreeGrid - export configuration, headers and footers, page settings, server-side export, and custom formatting.'
---

# PDF Export

## Table of Contents
- [Basic PDF Export](#basic-pdf-export)
- [Headers and Footers](#headers-and-footers)
- [Server-side Export](#server-side-export)
- [Server-side Export](#server-side-export)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

## Basic PDF Export

Export TreeGrid to PDF:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, PdfExport, Toolbar } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Budget: 10000, Children: [] }
  ];
  const toolbarClick = (args) => {
      if (treegrid && args.item.text === 'PDF Export') {
          treegrid.pdfExport();
      }
  };
  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      toolbar={['PdfExport']}
      allowPdfExporting={true}
      toolbarClick={toolbarClick}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Budget" headerText="Budget" width={120} format="N2" />
      </ColumnsDirective>
      <Inject services={[PdfExport, Toolbar]} />
    </TreeGridComponent>
  );
}
```

### Export configuration

Configure PDF export behavior:

```tsx
const treeGridRef = React.useRef();

const exportPdf = () => {
  const pdfExportProperties = {
    fileName: 'treegrid.pdf',
    orientation: 'Portrait',
    pageSize: 'A4',
    columns: [
      { field: 'TaskID', headerText: 'Task ID', width: 80 },
      { field: 'TaskName', headerText: 'Task Name', width: 160 }
    ]
  };
  
  treeGridRef.current.pdfExport(pdfExportProperties);
};

<TreeGridComponent ref={treeGridRef} dataSource={data} childMapping="Children">
  <ColumnsDirective>
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
  <Inject services={[PdfExport]} />
</TreeGridComponent>
```

## Headers and Footers

Add headers and footers to PDF:

```tsx
const pdfExportProperties = {
  fileName: 'treegrid.pdf',
  header: {
    fromTop: 0,
    height: 60,
    contents: [
      {
        type: 'Text',
        value: 'Project Planning',
        position: { x: 250, y: 50 },
        style: { fontSize: 20, bold: true }
      }
    ]
  },
  footer: {
    fromBottom: 160,
    height: 60,
    contents: [
      {
        type: 'Text',
        value: 'Page #NUMBER# of #TOTALPAGE#',
        position: { x: 250, y: 20 },
        style: { fontSize: 12 }
      }
    ]
  }
};

treeGridRef.current.pdfExport(pdfExportProperties);
```

## Server-side Export

Export via server for large datasets:

```tsx
const serverExportPdf = () => {
  const pdfExportProperties = {
    fileName: 'treegrid.pdf'
  };
  
  // Send to server for processing
  fetch('/api/export/pdf', {
    method: 'POST',
    body: JSON.stringify({ data, properties: pdfExportProperties })
  })
  .then(response => response.blob())
  .then(blob => {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'treegrid.pdf';
    link.click();
  });
};
```

## Key APIs

| Property | Type | Description |
|---|---|---|
| `pdfExport` | method | Export to PDF |
| `fileName` | string | Output file name |
| `orientation` | string | 'Portrait', 'Landscape' |
| `pageSize` | string | 'A4', 'A3', 'Letter', etc. |
| `columns` | array | Columns to export |
| `header` | object | Header configuration |
| `footer` | object | Footer configuration |

## Common Patterns

1. **Multi-level Export**: Export hierarchical data with grouping
2. **Filtered Export**: Export only visible/filtered rows
3. **Formatted Export**: Include cell formatting in PDF

