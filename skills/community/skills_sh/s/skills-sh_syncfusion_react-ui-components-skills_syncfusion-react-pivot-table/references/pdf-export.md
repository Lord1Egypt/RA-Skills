# PDF Export Reference - Syncfusion React Pivot Table

## Overview

The Pivot Table supports exporting data to **PDF** format. Enable export by setting `allowPdfExport` to **true** and using the `pdfExport()` method.

### Key Features
- **PDF Export**: Export data to PDF document
- **Multiple Tables**: Export multiple pivot tables to single PDF
- **Table and Chart**: Export both table and chart together
- **Custom Styling**: Apply themes, fonts, headers, footers
- **Virtual Scroll**: Efficient export for large datasets

## Basic Setup

```typescript
import { PivotViewComponent, PDFExport, Inject } from '@syncfusion/ej2-react-pivotview';
import { pivotData } from './datasource';

function App() {
  return (
    <PivotViewComponent
      id="PivotView"
      dataSourceSettings={{ dataSource: pivotData }}
      allowPdfExport={true}
    >
      <Inject services={[PDFExport]} />
    </PivotViewComponent>
  );
}

export default App;
```

## Export Methods

### Basic PDF Export

Call `pdfExport()` method to export data to PDF:

```typescript
function btnClick(): void {
  pivotObj.pdfExport();
}
```

### Export with Properties

Pass export properties to customize the output:

```typescript
let pdfExportProperties: PdfExportProperties = {
  pageOrientation: 'Landscape'
};
pivotObj.pdfExport(pdfExportProperties);
```

## Multiple Pivot Tables

Export multiple pivot tables to a single PDF file:

```typescript
// First table - create new file
pivotObj.pdfExport(pdfExportProperties, true);

// Subsequent tables - append to same file
pivotObj1.pdfExport(pdfExportProperties, false, pdfDoc);
```

## Export Table and Chart

Set `displayOption.view` to **Both** to export table and chart together:

```typescript
let dataSourceSettings = {
  displayOption: { view: 'Both' }
};

// Use exportBothTableAndChart: true in pdfExport
pivotObj.pdfExport(pdfExportProperties, false, null, false, true);
```

## Header and Footer

### Add Text

Use `header` and `footer` properties with content:

```typescript
let pdfExportProperties: PdfExportProperties = {
  header: { contents: [{ type: 'Text', content: 'Company Name' }] },
  footer: { contents: [{ type: 'Text', content: 'Page: ${total}' }] }
};
```

### Add Lines

Add visual separators using line type:

```typescript
header: { contents: [{ type: 'Line' }] }
```

### Add Page Numbers

Add page numbers with format:

```typescript
header: { contents: [{ type: 'PageNumber', format: 'Arabic' }] }
```

### Add Images

Add images using Base64 string:

```typescript
header: { contents: [{ type: 'Image', src: base64String }] }
```

## Document Customization

### File Name

Set custom file name:

```typescript
let pdfExportProperties: PdfExportProperties = {
  fileName: 'report.pdf'
};
```

### Page Orientation

Change orientation (Portrait/Landscape):

```typescript
let pdfExportProperties: PdfExportProperties = {
  pageOrientation: 'Landscape'
};
```

### Page Size

Set page size (Letter, A4, Legal, etc.):

```typescript
let pdfExportProperties: PdfExportProperties = {
  pageSize: 'A4'
};
```

### Custom Dimensions

Set custom width/height via `beforeExport` event:

```typescript
function beforeExport(args: BeforeExportEventArgs): void {
  args.height = '600px';
  args.width = '800px';
}
```

> Note: Requires `enableVirtualization: true` and both `VirtualScroll` and `PDFExport` injected.

### Table Column Count

Control columns per page via `beforeExport`:

```typescript
function beforeExport(args: BeforeExportEventArgs): void {
  args.columnSize = 4;
}
```

## Cell Styling

### Column Width

Set column width using `onPdfCellRender`:

```typescript
function onPdfCellRender(args: PdfCellRenderArgs): void {
  if (args.column.field === 'Sold') {
    args.column.width = 60;
  }
}
```

### Row Height

Set row height using `onPdfCellRender`:

```typescript
function onPdfCellRender(args: PdfCellRenderArgs): void {
  if (args.cell.value === 'Mountain Bikes') {
    args.cell.height = 30;
  }
}
```

## Theme and Styling

### Apply Theme

Use theme property for colors:

```typescript
let pdfExportProperties: PdfExportProperties = {
  theme: {
    header: { fontColor: '#FF0000' },
    record: { fontColor: '#000000' }
  }
};
```

### Default Fonts

Built-in fonts: Helvetica, TimesRoman, Courier, Symbol, ZapfDingbats

```typescript
import { PdfStandardFont, PdfFontFamily, PdfFontStyle } from '@syncfusion/ej2-pdf-export';

let pdfExportProperties: PdfExportProperties = {
  theme: {
    header: { font: new PdfStandardFont(PdfFontFamily.TimesRoman, 11, PdfFontStyle.Bold) }
  }
};
```

### Custom Fonts

Use Base64 encoded custom fonts:

```typescript
import { PdfTrueTypeFont } from '@syncfusion/ej2-pdf-export';

let pdfExportProperties: PdfExportProperties = {
  theme: {
    header: { font: new PdfTrueTypeFont(base64AlgeriaFont, 11) }
  }
};
```

> Note: The `base64AlgeriaFont` export should be included in your datasource file.

## Virtual Scroll Export

### Basic Virtual Export

With virtualization enabled, PivotEngine export is used automatically:

```typescript
// Requires VirtualScroll and PDFExport injected
<Inject services={[VirtualScroll, PDFExport]} />
```

### Repeat Header

Enable/disable row header repetition:

```typescript
function beforeExport(args: BeforeExportEventArgs): void {
  args.allowRepeatHeader = false;
}
```

### Export All Pages

Control page export behavior:

```typescript
// Export all data (default with virtualization)
dataSourceSettings = { exportAllPages: true };

// Export only current viewport
dataSourceSettings = { exportAllPages: false };
```

## Events

### pdfQueryCellInfo

Triggered for each row/value cell. Arguments: `value`, `column`, `data`, `style`.

```typescript
function pdfQueryCellInfo(args: PdfQueryCellInfoEventArgs): void {
  args.value = 'Modified Value';
  args.style.backColor = '#ffff00';
}
```

### pdfHeaderQueryCellInfo

Triggered for each header cell. Arguments: `cell`, `style`.

```typescript
function pdfHeaderQueryCellInfo(args: PdfHeaderQueryCellInfoEventArgs): void {
  args.style.fontColor = '#0000FF';
}
```

### exportComplete

Triggered after export completes:

```typescript
function exportComplete(args: ExportCompleteEventArgs): void {
  args.promise.then((blobData: Blob) => {
    console.log('Export complete');
  });
}
```

## Performance Tips

1. **Virtualization**: Enable for large datasets
2. **Current Page**: Use `exportAllPages: false` to export only visible data
3. **Blob Data**: Set `isBlob: true` when processing file programmatically

## Best Practices

✅ **Do:**
- Use virtualization for large datasets
- Use `exportAllPages: false` with virtualization for better performance
- Set `isBlob: true` when you need to process the exported file

❌ **Don't:**
- Export millions of records without virtualization
- Forget to inject `PDFExport` module
- Use full URLs - reference API names in backticks like `pdfExport`

## Common Issues

**PDF export not working?**
- Verify `PDFExport` is in the `Inject` services array
- Check `allowPdfExport` is set to **true**

**Large file size?**
- Use `exportAllPages: false` to export only current viewport
- Consider disabling chart export if not needed

**Font not displaying correctly?**
- Ensure custom fonts are Base64 encoded
- Use `PdfTrueTypeFont` class for custom fonts

## Related Features

- **Excel Export**: Export to Excel/CSV format
- **Toolbar**: Export options in toolbar UI
- **Virtualization**: Handle large datasets efficiently
