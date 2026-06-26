# Print and Export

Export 3D charts as images (PNG, JPEG, SVG, PDF) or print directly from the browser.

## Table of contents

- [Print Functionality](print-export.md#print-functionality)
  - [Basic Print](print-export.md#basic-print)
  - [Print with Custom IDs](print-export.md#print-with-custom-ids)
- [Export as Image](print-export.md#export-as-image)
  - [Export to PNG](print-export.md#export-to-png)
  - [Export to JPEG](print-export.md#export-to-jpeg)
  - [Export to SVG](print-export.md#export-to-svg)
- [Export to PDF](print-export.md#export-to-pdf)
- [Export with Orientation](print-export.md#export-with-orientation)
- [Export Multiple Charts](print-export.md#export-multiple-charts)
- [Before Export Event](print-export.md#before-export-event)
- [Complete Export Example with Menu](print-export.md#complete-export-example-with-menu)
- [Export Options Comparison](print-export.md#export-options-comparison)
- [Use Cases](print-export.md#use-cases)
- [Best Practices](print-export.md#best-practices)
- [Common Issues](print-export.md#common-issues)

## Print Functionality

### Basic Print

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D, Export3D } from '@syncfusion/ej2-react-charts';

function PrintChart() {
  const chartRef = React.useRef<Chart3DComponent>(null);
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 42 },
    { month: 'Mar', sales: 38 },
    { month: 'Apr', sales: 48 }
  ];

  const handlePrint = () => {
    if (chartRef.current) {
      chartRef.current.print();
    }
  };

  return (
    <div>
      <button onClick={handlePrint}>Print Chart</button>
      <Chart3DComponent
        ref={chartRef}
        id='chart'
        primaryXAxis={{ valueType: 'Category' }}
      >
        <Inject services={[ColumnSeries3D, Category3D, Export3D]} />
        <Chart3DSeriesCollectionDirective>
          <Chart3DSeriesDirective
            dataSource={data}
            xName='month'
            yName='sales'
            type='Column'
          />
        </Chart3DSeriesCollectionDirective>
      </Chart3DComponent>
    </div>
  );
}
```

**Key requirement:** Must inject `Export3D` service for print/export functionality.

### Print with Custom IDs

Print specific charts by ID:

```tsx
const handlePrintSpecific = () => {
  if (chartRef.current) {
    chartRef.current.print(['chart1', 'chart2']);
  }
};
```

## Export as Image

### Export to PNG

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D, Export3D } from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import React, { useRef } from 'react';

function ExportChart() {
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 42 },
    { month: 'Mar', sales: 38 }
  ];

  const chartRef = useRef(null);

  const exportChart = (format) => {
    if (chartRef.current) {
      const fileName = `${new Date().getTime()}.${format.toLowerCase()}`;
      chartRef.current.export(format, fileName);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '15px' }}>
        <button onClick={() => exportChart('PNG')}>Export as PNG</button>
      </div>
      <Chart3DComponent
        ref={chartRef}
        enableExport={true}
        id='chart'
        primaryXAxis={{ valueType: 'Category' }}
      >
        <Inject services={[ColumnSeries3D, Category3D, Export3D]} />
        <Chart3DSeriesCollectionDirective>
          <Chart3DSeriesDirective
            dataSource={data}
            xName='month'
            yName='sales'
            type='Column'
          />
        </Chart3DSeriesCollectionDirective>
      </Chart3DComponent>
    </div>
  );
}

export default ExportChart;
ReactDOM.render(<ExportChart />, document.getElementById('charts'));
```

**SVG benefits:**
- Vector format (scalable without quality loss)
- Smaller file size for simple charts
- Editable in vector graphics software

## Before Export Event

Customize chart before exporting:

```tsx
function CustomizedExport() {
  const chartRef = React.useRef<Chart3DComponent>(null);
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 42 }
  ];

  const beforeExport = (args: any) => {
    console.log('Exporting chart...');
    // Modify chart appearance before export if needed
    args.chart.title = 'Exported Sales Chart - ' + new Date().toLocaleDateString();
  };

  const handleExport = () => {
    if (chartRef.current) {
      chartRef.current.export('PNG', 'SalesChart');
    }
  };

  return (
    <div>
      <button onClick={handleExport}>Export</button>
      <Chart3DComponent
        ref={chartRef}
        id='chart'
        primaryXAxis={{ valueType: 'Category' }}
        beforeExport={beforeExport}
      >
        <Inject services={[ColumnSeries3D, Category3D, Export3D]} />
        <Chart3DSeriesCollectionDirective>
          <Chart3DSeriesDirective
            dataSource={data}
            xName='month'
            yName='sales'
            type='Column'
          />
        </Chart3DSeriesCollectionDirective>
      </Chart3DComponent>
    </div>
  );
}
```

## Complete Export Example with Menu

```tsx
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective, Inject, ColumnSeries3D, Category3D, Export3D } from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import React, { useRef } from 'react';

function PrintChart() {
  const data = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 42 },
    { month: 'Mar', sales: 38 }
  ];

  const chartRef = useRef(null);

  const exportChart = (format) => {
    if (chartRef.current) {
      const fileName = `${new Date().getTime()}.${format.toLowerCase()}`;
      chartRef.current.export(format, fileName);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '15px' }}>
        <button onClick={() => exportChart('PNG')}>Export as PNG</button>
        <button onClick={() => exportChart('PDF')}>Export as PDF</button>
        <button onClick={() => exportChart('SVG')}>Export as SVG</button>
        <button onClick={() => exportChart('JPEG')}>Export as JPEG</button>
        <button onClick={() => window.print()}>Print</button>
      </div>
      <Chart3DComponent
        ref={chartRef}
        enableExport={true}
        id='chart'
        primaryXAxis={{ valueType: 'Category' }}
      >
        <Inject services={[ColumnSeries3D, Category3D, Export3D]} />
        <Chart3DSeriesCollectionDirective>
          <Chart3DSeriesDirective
            dataSource={data}
            xName='month'
            yName='sales'
            type='Column'
          />
        </Chart3DSeriesCollectionDirective>
      </Chart3DComponent>
    </div>
  );
}

export default PrintChart;
ReactDOM.render(<PrintChart />, document.getElementById('charts'));
```

## Export Options Comparison

| Format | Best For | Pros | Cons |
|--------|----------|------|------|
| **PNG** | General use, web sharing | Lossless, supports transparency | Larger file size |
| **JPEG** | Photos, presentations | Smaller file size | Lossy compression, no transparency |
| **SVG** | Print, scaling, editing | Vector (infinite scaling), editable | Limited browser support for complex charts |
| **PDF** | Reports, archiving, printing | Universal format, maintains quality | Larger file size |

## Use Cases

**Reports:**
- Export to PDF for quarterly reports
- Landscape orientation for wide charts
- Include timestamp in filename

**Presentations:**
- Export to PNG/JPEG for PowerPoint
- High resolution for projection
- Transparent background (PNG) for overlay

**Web sharing:**
- PNG for social media, blogs
- SVG for responsive web graphics
- JPEG for faster loading

**Documentation:**
- PDF for archiving analysis
- SVG for technical documentation (editable)

**Printing:**
- Direct print for immediate hardcopy
- PDF export for later printing

## Best Practices

**Filename conventions:**
- Include date: `SalesChart_2023-12-15`
- Include context: `Q4_Revenue_Report`
- Avoid special characters: use underscores, not spaces

**Format selection:**
- Default to PNG for general use
- Use SVG for scalable graphics
- Use PDF for formal reports
- Use JPEG only when file size critical

**Before export:**
- Update title with export date
- Hide/show specific elements
- Adjust colors for print (consider grayscale)

**User experience:**
- Show loading indicator during export
- Confirm successful export
- Provide format selection dropdown

## Common Issues

**Export not working:**
- Ensure `Export3D` service is injected
- Check chart reference is valid
- Verify chart has rendered (use loaded event)

**Exported image blank/corrupted:**
- Wait for chart to fully load before exporting
- Check browser compatibility
- Try different format (e.g., PNG instead of PDF)

**Print preview empty:**
- Ensure chart has rendered
- Check CSS doesn't hide chart on print media
- Verify browser allows popup for print dialog

**File not downloading:**
- Check browser popup blocker settings
- Verify browser allows downloads from site
- Try different format

**TypeScript errors with export:**
- Import proper types: `import { Chart3DComponent } from '@syncfusion/ej2-react-charts';`
- Use correct method signature: `export(type: ExportType, fileName: string, orientation?: number, controls?: any[])`

---

See also: [api-reference.md](api-reference.md) | [usage-example.md](usage-example.md)
