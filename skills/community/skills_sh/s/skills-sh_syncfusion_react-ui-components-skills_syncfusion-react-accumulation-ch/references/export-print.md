````markdown
# Export and Print

## Table of Contents
- [Overview](#overview)
- [Enabling Export](#enabling-export)
- [Export to Image](#export-to-image)
- [Export to PDF](#export-to-pdf)
- [Export to SVG](#export-to-svg)
- [Export Customization](#export-customization)
- [Print Chart](#print-chart)
- [Before Export Event](#before-export-event)
- [After Export Event](#after-export-event)

## Overview

The accumulation chart supports exporting to various formats (JPEG, PNG, SVG, PDF) and printing functionality for generating reports, documentation, or offline viewing.

## Enabling Export

Enable export functionality by setting `enableExport` to `true` and injecting the `Export` module:

```tsx
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries,
  Export
} from '@syncfusion/ej2-react-charts';

function ExportableChart() {
  const chartRef = React.useRef<AccumulationChartComponent>(null);
  
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  const handleExport = () => {
    if (chartRef.current) {
      chartRef.current.export('PNG', 'chart');
    }
  };

  return (
    <div>
      <button onClick={handleExport}>Export as PNG</button>
      
      <AccumulationChartComponent 
        id='exportable-chart'
        ref={chartRef}
        title='Browser Market Share'
        enableExport={true}
      >
        <Inject services={[PieSeries, Export]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

**Key points:**
- Set `enableExport={true}` on AccumulationChartComponent
- Inject `Export` module in services
- Use chart ref to call `export()` method
- Specify format and filename in export call

## Export to Image

Export chart to image formats (PNG, JPEG):

```tsx
function ImageExport() {
  const chartRef = React.useRef<AccumulationChartComponent>(null);
  
  const data = [
    { x: 'Product A', y: 45 },
    { x: 'Product B', y: 30 },
    { x: 'Product C', y: 25 }
  ];

  const exportToPNG = () => {
    chartRef.current?.export('PNG', 'sales-chart');
  };

  const exportToJPEG = () => {
    chartRef.current?.export('JPEG', 'sales-chart');
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={exportToPNG}>Export to PNG</button>
        <button onClick={exportToJPEG} style={{ marginLeft: '10px' }}>
          Export to JPEG
        </button>
      </div>
      
      <AccumulationChartComponent 
        id='image-export'
        ref={chartRef}
        title='Product Sales Distribution'
        enableExport={true}
      >
        <Inject services={[PieSeries, Export]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

**Export formats:**
- **PNG**: Portable Network Graphics (lossless, transparent background support)
- **JPEG**: Joint Photographic Experts Group (lossy, smaller file size)

**When to use:**
- PNG: High-quality images, presentations, web use
- JPEG: Smaller file sizes, email attachments, quick sharing

## Export to PDF

Export chart to PDF format:

```tsx
function PDFExport() {
  const chartRef = React.useRef<AccumulationChartComponent>(null);
  
  const data = [
    { quarter: 'Q1', revenue: 35 },
    { quarter: 'Q2', revenue: 28 },
    { quarter: 'Q3', revenue: 42 },
    { quarter: 'Q4', revenue: 31 }
  ];

  const exportToPDF = () => {
    chartRef.current?.export('PDF', 'quarterly-report');
  };

  return (
    <div>
      <button onClick={exportToPDF}>Export to PDF</button>
      
      <AccumulationChartComponent 
        id='pdf-export'
        ref={chartRef}
        title='Quarterly Revenue Distribution'
        subTitle='Fiscal Year 2024'
        enableExport={true}
      >
        <Inject services={[PieSeries, Export]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='quarter'
            yName='revenue'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

**PDF export benefits:**
- Print-ready format
- Preserved layout and quality
- Professional reports
- Universal compatibility

## Export to SVG

Export chart as scalable vector graphics:

```tsx
function SVGExport() {
  const chartRef = React.useRef<AccumulationChartComponent>(null);
  
  const data = [
    { category: 'Mobile', value: 55 },
    { category: 'Desktop', value: 30 },
    { category: 'Tablet', value: 15 }
  ];

  const exportToSVG = () => {
    chartRef.current?.export('SVG', 'device-distribution');
  };

  return (
    <div>
      <button onClick={exportToSVG}>Export to SVG</button>
      
      <AccumulationChartComponent 
        id='svg-export'
        ref={chartRef}
        title='Device Distribution'
        enableExport={true}
      >
        <Inject services={[PieSeries, Export]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='category'
            yName='value'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

**SVG advantages:**
- Infinite scalability without quality loss
- Editable in vector graphics software
- Smaller file size for simple charts
- Perfect for web and print

## Export Customization

Customize export output using the `beforeExport` event:

```tsx
import { IExportEventArgs } from '@syncfusion/ej2-react-charts';

function CustomizedExport() {
  const chartRef = React.useRef<AccumulationChartComponent>(null);
  
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  const onBeforeExport = (args: IExportEventArgs): void => {
    // Customize filename
    args.fileName = `browser-stats-${new Date().toISOString().split('T')[0]}`;
    
    // Add watermark or modifications
    console.log('Exporting chart:', args.type);
    
    // You can cancel export
    // args.cancel = true;
  };

  const exportChart = (format: 'PNG' | 'PDF' | 'JPEG' | 'SVG') => {
    const fileName = `chart-${Date.now()}`;
    chartRef.current?.export(format, fileName);
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => exportChart('PNG')}>PNG</button>
        <button onClick={() => exportChart('JPEG')}>JPEG</button>
        <button onClick={() => exportChart('PDF')}>PDF</button>
        <button onClick={() => exportChart('SVG')}>SVG</button>
      </div>
      
      <AccumulationChartComponent 
        id='customized-export'
        ref={chartRef}
        title='Browser Market Share'
        enableExport={true}
        beforeExport={onBeforeExport}
      >
        <Inject services={[PieSeries, Export]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Print Chart

Print chart using the `print()` method:

```tsx
function PrintableChart() {
  const chartRef = React.useRef<AccumulationChartComponent>(null);
  
  const data = [
    { x: 'Q1', y: 35 },
    { x: 'Q2', y: 28 },
    { x: 'Q3', y: 42 },
    { x: 'Q4', y: 31 }
  ];

  const handlePrint = () => {
    chartRef.current?.print();
  };

  return (
    <div>
      <button onClick={handlePrint}>Print Chart</button>
      
      <AccumulationChartComponent 
        id='printable-chart'
        ref={chartRef}
        title='Quarterly Performance'
        enableExport={true}
      >
        <Inject services={[PieSeries, Export]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

**Print specific charts:**

```tsx
function MultiChartPrint() {
  const chart1Ref = React.useRef<AccumulationChartComponent>(null);
  const chart2Ref = React.useRef<AccumulationChartComponent>(null);

  const printChart1 = () => {
    chart1Ref.current?.print(['chart-1']);
  };

  const printChart2 = () => {
    chart2Ref.current?.print(['chart-2']);
  };

  const printBoth = () => {
    chart1Ref.current?.print(['chart-1', 'chart-2']);
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={printChart1}>Print Chart 1</button>
        <button onClick={printChart2}>Print Chart 2</button>
        <button onClick={printBoth}>Print Both</button>
      </div>
      
      <div style={{ display: 'flex', gap: '20px' }}>
        <AccumulationChartComponent 
          id='chart-1'
          ref={chart1Ref}
          title='Sales by Region'
          enableExport={true}
        >
          <Inject services={[PieSeries, Export]} />
          <AccumulationSeriesCollectionDirective>
            <AccumulationSeriesDirective
              dataSource={[
                { x: 'North', y: 35 },
                { x: 'South', y: 28 },
                { x: 'East', y: 22 },
                { x: 'West', y: 15 }
              ]}
              xName='x'
              yName='y'
            />
          </AccumulationSeriesCollectionDirective>
        </AccumulationChartComponent>

        <AccumulationChartComponent 
          id='chart-2'
          ref={chart2Ref}
          title='Sales by Quarter'
          enableExport={true}
        >
          <Inject services={[PieSeries, Export]} />
          <AccumulationSeriesCollectionDirective>
            <AccumulationSeriesDirective
              dataSource={[
                { x: 'Q1', y: 25 },
                { x: 'Q2', y: 30 },
                { x: 'Q3', y: 28 },
                { x: 'Q4', y: 17 }
              ]}
              xName='x'
              yName='y'
            />
          </AccumulationSeriesCollectionDirective>
        </AccumulationChartComponent>
      </div>
    </div>
  );
}
```

## Before Export Event

Use `beforeExport` event to customize export behavior:

```tsx
import { IExportEventArgs } from '@syncfusion/ej2-react-charts';

function BeforeExportHandler() {
  const chartRef = React.useRef<AccumulationChartComponent>(null);
  
  const data = [
    { x: 'Chrome', y: 61.3 },
    { x: 'Safari', y: 24.6 },
    { x: 'Firefox', y: 14.1 }
  ];

  const onBeforeExport = (args: IExportEventArgs): void => {
    // Add timestamp to filename
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    args.fileName = `browser-chart-${timestamp}`;
    
    // Log export details
    console.log('Exporting as:', args.type);
    console.log('Filename:', args.fileName);
    
    // Conditionally cancel export
    if (!confirm(`Export chart as ${args.type}?`)) {
      args.cancel = true;
    }
  };

  const exportChart = () => {
    chartRef.current?.export('PNG', 'chart');
  };

  return (
    <div>
      <button onClick={exportChart}>Export Chart</button>
      
      <AccumulationChartComponent 
        id='before-export-chart'
        ref={chartRef}
        title='Browser Statistics'
        enableExport={true}
        beforeExport={onBeforeExport}
      >
        <Inject services={[PieSeries, Export]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## After Export Event

Handle post-export operations with `afterExport` event:

```tsx
import { IAfterExportEventArgs } from '@syncfusion/ej2-react-charts';

function AfterExportHandler() {
  const chartRef = React.useRef<AccumulationChartComponent>(null);
  const [exportStatus, setExportStatus] = React.useState('');
  
  const data = [
    { x: 'Category A', y: 45 },
    { x: 'Category B', y: 30 },
    { x: 'Category C', y: 25 }
  ];

  const onAfterExport = (args: IAfterExportEventArgs): void => {
    setExportStatus(`Chart exported successfully as ${args.type}!`);
    
    // Clear message after 3 seconds
    setTimeout(() => setExportStatus(''), 3000);
    
    // You can trigger additional actions here
    // - Send to server
    // - Show download notification
    // - Update analytics
  };

  const exportChart = (format: 'PNG' | 'PDF' | 'JPEG' | 'SVG') => {
    chartRef.current?.export(format, 'chart');
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => exportChart('PNG')}>Export PNG</button>
        <button onClick={() => exportChart('PDF')}>Export PDF</button>
        {exportStatus && (
          <span style={{ 
            marginLeft: '10px', 
            color: 'green',
            fontWeight: 'bold'
          }}>
            {exportStatus}
          </span>
        )}
      </div>
      
      <AccumulationChartComponent 
        id='after-export-chart'
        ref={chartRef}
        title='Category Distribution'
        enableExport={true}
        afterExport={onAfterExport}
      >
        <Inject services={[PieSeries, Export]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='x'
            yName='y'
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}
```

## Complete Export Example

Here's a comprehensive example with all export options:

```tsx
import React, { useRef, useState } from 'react';
import { 
  AccumulationChartComponent,
  AccumulationSeriesCollectionDirective,
  AccumulationSeriesDirective,
  Inject,
  PieSeries,
  AccumulationDataLabel,
  AccumulationLegend,
  Export
} from '@syncfusion/ej2-react-charts';
import { IExportEventArgs, IAfterExportEventArgs } from '@syncfusion/ej2-react-charts';

function ComprehensiveExport() {
  const chartRef = useRef<AccumulationChartComponent>(null);
  const [message, setMessage] = useState('');
  
  const data = [
    { browser: 'Chrome', share: 61.3, fill: '#4285F4' },
    { browser: 'Safari', share: 24.6, fill: '#0088FF' },
    { browser: 'Firefox', share: 14.1, fill: '#FF6600' },
    { browser: 'Edge', share: 5.0, fill: '#0078D4' },
    { browser: 'Others', share: 5.0, fill: '#999999' }
  ];

  const onBeforeExport = (args: IExportEventArgs): void => {
    const date = new Date().toISOString().split('T')[0];
    args.fileName = `browser-market-share-${date}`;
    setMessage(`Exporting as ${args.type}...`);
  };

  const onAfterExport = (args: IAfterExportEventArgs): void => {
    setMessage(`Successfully exported as ${args.type}!`);
    setTimeout(() => setMessage(''), 3000);
  };

  const handleExport = (type: 'PNG' | 'JPEG' | 'SVG' | 'PDF') => {
    chartRef.current?.export(type, 'chart');
  };

  const handlePrint = () => {
    chartRef.current?.print();
  };

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ 
        marginBottom: '15px', 
        display: 'flex', 
        gap: '10px',
        alignItems: 'center'
      }}>
        <button onClick={() => handleExport('PNG')}>
          Export PNG
        </button>
        <button onClick={() => handleExport('JPEG')}>
          Export JPEG
        </button>
        <button onClick={() => handleExport('SVG')}>
          Export SVG
        </button>
        <button onClick={() => handleExport('PDF')}>
          Export PDF
        </button>
        <button onClick={handlePrint}>
          Print
        </button>
        {message && (
          <span style={{ 
            color: '#28a745', 
            fontWeight: 'bold',
            marginLeft: '10px'
          }}>
            {message}
          </span>
        )}
      </div>
      
      <AccumulationChartComponent 
        id='comprehensive-export'
        ref={chartRef}
        title='Browser Market Share 2024'
        subTitle='Desktop and Mobile Combined'
        enableExport={true}
        beforeExport={onBeforeExport}
        afterExport={onAfterExport}
        legendSettings={{ 
          visible: true, 
          position: 'Right' 
        }}
      >
        <Inject services={[
          PieSeries, 
          AccumulationDataLabel, 
          AccumulationLegend,
          Export
        ]} />
        <AccumulationSeriesCollectionDirective>
          <AccumulationSeriesDirective
            dataSource={data}
            xName='browser'
            yName='share'
            pointColorMapping='fill'
            radius='90%'
            dataLabel={{
              visible: true,
              position: 'Outside',
              format: '{point.x}: {point.y}%'
            }}
          />
        </AccumulationSeriesCollectionDirective>
      </AccumulationChartComponent>
    </div>
  );
}

export default ComprehensiveExport;
```

## Common Issues and Solutions

**Issue: Export not working**
- Solution: Ensure `enableExport={true}` is set
- Solution: Verify `Export` module is injected in services
- Solution: Check browser console for errors
- Solution: Ensure chart ref is properly attached

**Issue: Exported file has wrong name**
- Solution: Specify filename in `export()` method
- Solution: Use `beforeExport` event to customize filename
- Solution: Check filename doesn't contain invalid characters

**Issue: Print shows blank page**
- Solution: Ensure chart is fully rendered before printing
- Solution: Check chart has valid data
- Solution: Verify chart dimensions are set
- Solution: Try using element ID in print() method

**Issue: SVG export shows pixelated**
- Solution: SVG should be vector - issue might be with viewer
- Solution: Verify export completed successfully
- Solution: Open SVG in vector graphics software to confirm

**Issue: PDF export fails**
- Solution: Ensure all dependencies are installed
- Solution: Check browser compatibility (modern browsers required)
- Solution: Try simpler chart configuration
- Solution: Check console for specific error messages

## Best Practices

1. **Filename conventions**: Use descriptive names with timestamps
2. **Format selection**: 
   - PNG for general use (balance of quality and size)
   - JPEG for smallest file size (photos/complex charts)
   - SVG for scalability (logos, simple charts)
   - PDF for professional reports
3. **User feedback**: Show loading/success messages during export
4. **Error handling**: Wrap export calls in try-catch blocks
5. **Accessibility**: Provide keyboard shortcuts for export actions
6. **Testing**: Test exports on different browsers and devices
7. **Performance**: Avoid exporting very large or complex charts
8. **File management**: Auto-generate meaningful filenames

````