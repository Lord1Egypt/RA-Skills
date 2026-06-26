# Print and Export

This guide covers printing and exporting 3D Circular Charts to various formats including JPEG, PNG, SVG, and PDF.

## Table of contents

- [Overview](print-and-export.md#overview)
- [Print Functionality](print-and-export.md#print-functionality)
  - [Enabling Print](print-and-export.md#enabling-print)
  - [Basic Print Setup](print-and-export.md#basic-print-setup)
  - [Print Method](print-and-export.md#print-method)
  - [Print with ID](print-and-export.md#print-with-id)
- [Export to Image Formats](print-and-export.md#export-to-image-formats)
  - [Module Injection](print-and-export.md#module-injection)
  - [Basic Image Export](print-and-export.md#basic-image-export)
  - [Export Method Signature](print-and-export.md#export-method-signature)
- [Export to PDF](print-and-export.md#export-to-pdf)
  - [Module Injection](print-and-export.md#module-injection-1)
  - [Basic PDF Export](print-and-export.md#basic-pdf-export)
- [Complete Export Example](print-and-export.md#complete-export-example)
- [Troubleshooting](print-and-export.md#troubleshooting)
- [Summary](print-and-export.md#summary)

## Overview

The 3D Circular Chart component provides built-in functionality to print charts directly from the browser and export them to multiple file formats for reports, presentations, and documentation.

## Print Functionality

### Enabling Print

The print feature allows users to print charts directly from the browser without needing screenshots.

### Basic Print Setup

```tsx
import { useRef } from 'react';

function PrintExample() {
  const chartRef = useRef(null);

  const data = [
    { category: 'Product A', sales: 35 },
    { category: 'Product B', sales: 28 },
    { category: 'Product C', sales: 22 },
    { category: 'Product D', sales: 15 }
  ];

  const handlePrint = () => {
    if (chartRef.current) {
      chartRef.current.print();
    }
  };

  return (
    <div>
      <button onClick={handlePrint}>Print Chart</button>
      
      <CircularChart3DComponent
        ref={chartRef}
        id="chart"
        title="Product Sales Distribution"
      >
        <Inject services={[PieSeries3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="category"
            yName="sales"
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>
    </div>
  );
}
```

### Print Method

Call the `print()` method on the chart instance:

```tsx
chartRef.current.print();
```

**What happens**:
1. Browser print dialog opens
2. Chart renders in print-optimized format
3. User can select printer or save as PDF
4. Page margins and orientation can be adjusted

### Print with ID

Alternatively, pass the chart ID to the print method:

```tsx
function PrintWithId() {
  const data = [
    { item: 'A', value: 30 },
    { item: 'B', value: 25 },
    { item: 'C', value: 25 },
    { item: 'D', value: 20 }
  ];

  const handlePrint = () => {
    const chart = document.getElementById('myChart');
    if (chart) {
      chart.ej2_instances[0].print();
    }
  };

  return (
    <div>
      <button onClick={handlePrint}>Print</button>
      
      <CircularChart3DComponent
        id="myChart"
        title="Data Distribution"
      >
        <Inject services={[PieSeries3D]} />
        <CircularChart3DSeriesCollectionDirective>
          <CircularChart3DSeriesDirective
            dataSource={data}
            xName="item"
            yName="value"
          />
        </CircularChart3DSeriesCollectionDirective>
      </CircularChart3DComponent>
    </div>
  );
}
```

## Export to Image Formats

Export charts to JPEG, PNG, or SVG formats.

### Module Injection

First, inject the `CircularChart3DExport` module:

```tsx
import {
  CircularChart3DComponent,
  CircularChart3DSeriesCollectionDirective,
  CircularChart3DSeriesDirective,
  PieSeries3D,
  CircularChart3DExport,  // Import export module
  Inject
} from '@syncfusion/ej2-react-charts';
```

### Basic Image Export

```tsx
import * as ReactDOM from 'react-dom';
import * as React from 'react';
import { useEffect, useRef } from 'react';
import {
  CircularChart3DSeriesDirective,
  CircularChart3DSeriesCollectionDirective,
  Inject,
  CircularChart3DComponent,
  CircularChartDataLabel3D,
  CircularChartLegend3D,
  PieSeries3D,
  CircularChartExport3D,
} from '@syncfusion/ej2-react-charts';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

export let circularData = [
  { x: 'John', y: 10, dataLabelMappingName: '$10k' },
  { x: 'Jake', y: 12, dataLabelMappingName: '$12k' },
  { x: 'Peter', y: 18, dataLabelMappingName: '$18k' },
  { x: 'James', y: 11, dataLabelMappingName: '$11k' },
  { x: 'Mary', y: 9.7, dataLabelMappingName: '$9.7k' },
];

function Print() {
  useEffect(() => {
    const button = document.getElementById('chart-print');
    button.addEventListener('click', onClick);
  }, []);
  let chartInstance = useRef(null);

  
const exportChart = (type: 'JPEG' | 'PDF' | 'SVG') => {
    chartInstance.current?.export(type, 'circular-chart');
  };

  return (
    <div className="control-pane">
      <div className="control-section row">
        <div className="col-lg-9">
          <CircularChart3DComponent
            id="charts"
            ref={chartInstance}
            title="Browser Market Shares in November 2023"
            tilt={-45}
            enableExport={true}
            legendSettings={{ visible: false, position: 'Right' }}
          >
            <Inject
              services={[
                PieSeries3D,
                CircularChartDataLabel3D,
                CircularChartLegend3D,
                CircularChartExport3D,
              ]}
            />
            <CircularChart3DSeriesCollectionDirective>
              <CircularChart3DSeriesDirective
                dataSource={circularData}
                xName="x"
                yName="y"
                dataLabel={{
                  visible: true,
                  position: 'Inside',
                  name: 'x',
                  font: { fontWeight: '600', color: 'white' },
                }}
              ></CircularChart3DSeriesDirective>
            </CircularChart3DSeriesCollectionDirective>
          </CircularChart3DComponent>
        </div>
        <div className="col-lg-3 property-section">
          <ButtonComponent
            id="chart-print"
            iconCss="e-icons e-print-icon"
            cssClass="e-flat"
            isPrimary={true}
          >
            Export
          </ButtonComponent>
        </div>
      </div>
    </div>
  );
}
export default Print;
const root = ReactDOM.createRoot(document.getElementById('charts'));
root.render(<Print />);
```

### Export Method Signature

```tsx
chart.export(type, fileName, orientation, controls, width, height);
```

**Parameters**:
- **`type`**: 'PNG' | 'JPEG' | 'SVG'
- **`fileName`**: Name of the downloaded file (without extension)
- **`orientation`**: (optional) 'Portrait' | 'Landscape'
- **`controls`**: (optional) Array of chart controls
- **`width`**: (optional) Export width in pixels
- **`height`**: (optional) Export height in pixels

### Custom File Names

```tsx
const exportWithCustomName = () => {
  const timestamp = new Date().toISOString().split('T')[0];
  chartRef.current.export('PNG', `sales-report-${timestamp}`);
};

// Downloads as: sales-report-2024-03-23.png
```

### Export Format Comparison

```tsx
function FormatComparison() {
  const chartRef = useRef(null);
  const data = [/* data */];

  const exportOptions = [
    {
      format: 'PNG',
      label: 'PNG (Best for web)',
      description: 'Lossless, supports transparency'
    },
    {
      format: 'JPEG',
      label: 'JPEG (Smaller file size)',
      description: 'Lossy compression, no transparency'
    },
    {
      format: 'SVG',
      label: 'SVG (Vector)',
      description: 'Scalable, best for print'
    }
  ];

  return (
    <div>
      {exportOptions.map((option) => (
        <button
          key={option.format}
          onClick={() => chartRef.current.export(option.format, 'chart')}
          title={option.description}
        >
          {option.label}
        </button>
      ))}
      
      <CircularChart3DComponent ref={chartRef} /* ... */ />
    </div>
  );
}
```

**Parameters**:
- **`fileName`**: (optional) Name of PDF file (without .pdf extension)

## Complete Export Example

```tsx
import * as ReactDOM from 'react-dom';
import * as React from 'react';
import { useRef } from 'react';
import {
  CircularChart3DSeriesDirective,
  CircularChart3DSeriesCollectionDirective,
  Inject,
  CircularChart3DComponent,
  CircularChartLegend3D,
  PieSeries3D,
  CircularChartExport3D
} from '@syncfusion/ej2-react-charts';

export let circularData = [
  { x: 'John', y: 10, dataLabelMappingName: '$10k' },
  { x: 'Jake', y: 12, dataLabelMappingName: '$12k' },
  { x: 'Peter', y: 18, dataLabelMappingName: '$18k' },
  { x: 'James', y: 11, dataLabelMappingName: '$11k' },
  { x: 'Mary', y: 9.7, dataLabelMappingName: '$9.7k' },
];

function Print() {
    const chartRef = useRef(null);

    const data = [
      { category: 'Electronics', revenue: 450000, color: '#2196F3' },
      { category: 'Clothing', revenue: 380000, color: '#4CAF50' },
      { category: 'Home & Garden', revenue: 320000, color: '#FF9800' },
      { category: 'Sports', revenue: 250000, color: '#9C27B0' }
    ];
  
    const handlePrint = () => {
      chartRef.current?.print();
    };
  
    const handleExport = (format) => {
      const timestamp = new Date().toISOString().slice(0, 10);
      const fileName = `revenue-report-${timestamp}`;
      
      if (format === 'PDF') {
        chartRef.current?.pdfExport(fileName);
      } else {
        chartRef.current?.export(format, fileName);
      }
    };
  
    return (
      <div>
        <div style={{
          display: 'flex',
          gap: '10px',
          marginBottom: '20px',
          padding: '10px',
          background: '#f5f5f5',
          borderRadius: '4px'
        }}>
          <button onClick={handlePrint}>
            🖨️ Print
          </button>
          <button onClick={() => handleExport('PNG')}>
            📷 Export PNG
          </button>
          <button onClick={() => handleExport('JPEG')}>
            🖼️ Export JPEG
          </button>
          <button onClick={() => handleExport('SVG')}>
            📐 Export SVG
          </button>
          <button onClick={() => handleExport('PDF')}>
            📄 Export PDF
          </button>
        </div>
        
        <CircularChart3DComponent
          ref={chartRef}
          id="revenue-chart"
          title="Department Revenue - FY 2024"
          subTitle="Total Revenue: $1.4M"
          width="800px"
          height="600px"
          enableExport={true}
          legendSettings={{ visible: true, position: 'Bottom' }}
        >
          <Inject services={[
            PieSeries3D,
            CircularChartLegend3D,
            CircularChartExport3D
          ]} />
          <CircularChart3DSeriesCollectionDirective>
            <CircularChart3DSeriesDirective
              dataSource={data}
              xName="category"
              yName="revenue"
              pointColorMapping="color"
            />
          </CircularChart3DSeriesCollectionDirective>
        </CircularChart3DComponent>
      </div>
    );
}
export default Print;
const root = ReactDOM.createRoot(document.getElementById('charts'));
root.render(<Print />);
```

## Custom Export Dimensions

Control the size of exported images and PDFs.

### Fixed Dimensions

```tsx
const exportLarge = () => {
  chartRef.current.export(
    'PNG',
    'chart-large',
    null,   // orientation
    null,   // controls
    1920,   // width
    1080    // height
  );
};

const exportSmall = () => {
  chartRef.current.export(
    'PNG',
    'chart-thumbnail',
    null,
    null,
    400,    // width
    300     // height
  );
};
```

## Troubleshooting

### Export Not Working

**Problem**: Export button does nothing or throws errors.

**Solutions**:
1. Verify module injection:
   ```tsx
   <Inject services={[PieSeries3D, CircularChart3DExport]} />
   ```
2. Check chart ref is properly set:
   ```tsx
   const chartRef = useRef(null);
   <CircularChart3DComponent ref={chartRef} />
   ```
3. Ensure chart has rendered before exporting

### Print Quality Issues

**Problem**: Printed chart looks pixelated or cut off.

**Solutions**:
1. Set explicit chart dimensions:
   ```tsx
   <CircularChart3DComponent width="800px" height="600px" />
   ```
2. Adjust browser print settings (scale, margins)
3. Use landscape orientation for wide charts

### PDF Export Issues

**Problem**: PDF export not available or errors.

**Solutions**:
1. Inject `CircularChart3DPdfExport` module
2. Check console for licensing errors
3. Verify Syncfusion license is registered

### File Not Downloading

**Problem**: Export method runs but no file downloads.

**Solutions**:
1. Check browser pop-up blocker settings
2. Verify browser allows downloads
3. Check console for JavaScript errors
4. Test in different browser

### Export Menu

```tsx
function ExportMenu() {
  const chartRef = useRef(null);
  const [menuOpen, setMenuOpen] = React.useState(false);

  const exportFormats = [
    { type: 'PNG', icon: '📷', label: 'PNG Image' },
    { type: 'JPEG', icon: '🖼️', label: 'JPEG Image' },
    { type: 'SVG', icon: '📐', label: 'SVG Vector' },
    { type: 'PDF', icon: '📄', label: 'PDF Document' }
  ];

  const handleExport = (format) => {
    if (format === 'PDF') {
      chartRef.current.pdfExport('chart');
    } else {
      chartRef.current.export(format, 'chart');
    }
    setMenuOpen(false);
  };

  return (
    <div>
      <div style={{ position: 'relative' }}>
        <button onClick={() => setMenuOpen(!menuOpen)}>
          Export ▼
        </button>
        
        {menuOpen && (
          <div style={{
            position: 'absolute',
            background: 'white',
            border: '1px solid #ccc',
            borderRadius: '4px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            zIndex: 1000
          }}>
            {exportFormats.map((format) => (
              <button
                key={format.type}
                onClick={() => handleExport(format.type)}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: '8px 16px',
                  textAlign: 'left',
                  border: 'none',
                  background: 'transparent'
                }}
              >
                {format.icon} {format.label}
              </button>
            ))}
          </div>
        )}
      </div>
      
      <CircularChart3DComponent ref={chartRef} /* ... */ />
    </div>
  );
}
```

## Summary

You've learned how to:
- ✅ Print charts directly from the browser
- ✅ Export to image formats (PNG, JPEG, SVG)
- ✅ Export to PDF with pdfExport method
- ✅ Inject required modules (CircularChart3DExport, CircularChart3DPdfExport)
- ✅ Customize export filenames and dimensions
- ✅ Set export orientation (Portrait/Landscape)
- ✅ Troubleshoot common export issues
- ✅ Create user-friendly export interfaces

**Best Practices:**
- Inject appropriate modules for export functionality
- Provide clear export options (PNG for web, PDF for reports)
- Use custom filenames with timestamps
- Set proper dimensions for target use (print, web, social media)
- Show loading states during export
- Handle errors gracefully
- Test exports in different browsers