# Export and Print Features

## Table of Contents
- [Export Functionality](#export-functionality)
  - [Enabling Export](#enabling-export)
  - [Export Methods](#export-methods)
  - [Export with User Interface](#export-with-user-interface)
- [Export Formats](#export-formats)
  - [PNG Export](#png-export)
  - [JPEG Export](#jpeg-export)
  - [PDF Export](#pdf-export)
  - [SVG Export](#svg-export)
- [Export Configuration](#export-configuration)
  - [Custom Export Filename](#custom-export-filename)
  - [Export with Orientation](#export-with-orientation)
  - [Multiple Format Export](#multiple-format-export)
- [Print Functionality](#print-functionality)
  - [Browser Print](#browser-print)
  - [Print Configuration](#print-configuration)
- [Complete Export Example](#complete-export-example)
- [Best Practices](#best-practices)

## Export Functionality

Export Sankey diagrams in various formats for sharing, documentation, or further processing.

### Enabling Export

```tsx
import {
  SankeyComponent, Inject, SankeyExport,
  SankeyNodeDirective, SankeyNodesCollectionDirective,
  SankeyLinkDirective, SankeyLinksCollectionDirective
} from '@syncfusion/ej2-react-charts';

<SankeyComponent
  width="90%"
  height="420px"
  title="Exportable Chart"
>
  {/* nodes and links */}
  <Inject services={[SankeyExport]} />
</SankeyComponent>
```

### Export Methods

```tsx
// Export as PNG (raster image)
chartRef.current?.export('PNG', 'sankey.png');

// Export as JPEG
chartRef.current?.export('JPEG', 'sankey.jpg');

// Export as PDF
chartRef.current?.export('PDF', 'sankey.pdf');

// Export as SVG (vector image)
chartRef.current?.export('SVG', 'sankey.svg');
```

### Export with User Interface

Add export buttons to your component:

```tsx
import React, { useRef } from 'react';
import { SankeyComponent, SankeyExport } from '@syncfusion/ej2-react-charts';

function ExportableSankey() {
  const chartRef = useRef(null);

  const exportChart = (format) => {
    if (chartRef.current) {
      const fileName = `sankey-diagram-${new Date().getTime()}.${format.toLowerCase()}`;
      chartRef.current.export(format, fileName);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '15px' }}>
        <button onClick={() => exportChart('PNG')}>Export as PNG</button>
        <button onClick={() => exportChart('PDF')}>Export as PDF</button>
        <button onClick={() => exportChart('SVG')}>Export as SVG</button>
        <button onClick={() => window.print()}>Print</button>
      </div>

      <SankeyComponent
        ref={chartRef}
        width="90%"
        height="420px"
        title="Energy Flow"
      >
        {/* nodes and links */}
        <Inject services={[SankeyExport]} />
      </SankeyComponent>
    </div>
  );
}

export default ExportableSankey;
```

## Export Formats

### PNG Export

Portable Network Graphics - raster format, widely compatible.

```tsx
const exportAsPNG = () => {
  chartRef.current?.export('PNG', 'diagram.png');
};
```

**Characteristics:**
- Lossless compression
- Transparent background support
- Good for web and email
- Fixed resolution

### JPEG Export

Compressed raster format, smaller file size.

```tsx
const exportAsJPEG = () => {
  chartRef.current?.export('JPEG', 'diagram.jpg');
};
```

**Characteristics:**
- Lossy compression
- Smallest file size
- Best for photographs
- No transparency

### PDF Export

Portable Document Format - ideal for printing and sharing.

```tsx
const exportAsPDF = () => {
  chartRef.current?.export('PDF', 'diagram.pdf');
};
```

**Characteristics:**
- Scalable without quality loss
- Professional appearance
- Print-optimized
- Can include text and metadata

### SVG Export

Scalable Vector Graphics - infinite zoom without quality loss.

```tsx
const exportAsSVG = () => {
  chartRef.current?.export('SVG', 'diagram.svg');
};
```

**Characteristics:**
- Vector format (scalable)
- Editable with design tools
- Smallest file for simple diagrams
- Support for animations

## Export Configuration

### Custom Export Filename

```tsx
const exportWithCustomName = () => {
  const timestamp = new Date().toISOString().split('T')[0];
  chartRef.current?.export('PNG', `energy-flow-${timestamp}.png`);
};
```

### Export with Orientation

```tsx
const exportPDF = () => {
  // For landscape orientation
  chartRef.current?.export('PDF', 'diagram.pdf');
};
```

### Multiple Format Export

```tsx
import React, { useRef } from 'react';

function MultiFormatExport() {
  const chartRef = useRef(null);

  const exportFormats = [
    { format: 'PNG', label: 'PNG Image' },
    { format: 'PDF', label: 'PDF Document' },
    { format: 'SVG', label: 'Vector (SVG)' }
  ];

  const handleExport = (format) => {
    const filename = `sankey-export-${Date.now()}`;
    chartRef.current?.export(format, filename);
  };

  return (
    <div>
      <fieldset>
        <legend>Export Format</legend>
        {exportFormats.map(({ format, label }) => (
          <div key={format}>
            <button onClick={() => handleExport(format)}>
              {label}
            </button>
          </div>
        ))}
      </fieldset>

      <SankeyComponent
        ref={chartRef}
        width="90%"
        height="420px"
        title="Exportable Diagram"
      >
        {/* nodes and links */}
        <Inject services={[SankeyExport]} />
      </SankeyComponent>
    </div>
  );
}

export default MultiFormatExport;
```

## Print Functionality

### Browser Print

Use standard browser print dialog:

```tsx
const printChart = () => {
  window.print();
};
```

### Print Configuration

```tsx
import React, { useRef } from 'react';

function PrintableSankey() {
  const chartRef = useRef(null);
  const printWindow = useRef(null);

  const handlePrint = () => {
    printWindow.current = window.open('', '', 'height=500,width=800');
    printWindow.current?.document.write(
      '<html><head><title>Print Sankey</title></head><body>'
    );
    
    // Get chart SVG or canvas
    const svgElement = chartRef.current?.svgObject;
    if (svgElement) {
      printWindow.current?.document.write(svgElement.outerHTML);
    }
    
    printWindow.current?.document.write('</body></html>');
    printWindow.current?.document.close();
    printWindow.current?.print();
  };

  return (
    <div>
      <button onClick={handlePrint}>Print Chart</button>

      <SankeyComponent
        ref={chartRef}
        width="90%"
        height="420px"
        title="Energy Flow Analysis"
      >
        {/* nodes and links */}
      </SankeyComponent>
    </div>
  );
}

export default PrintableSankey;
```

## Complete Export Example

```tsx
import React from 'react';
import React, { useRef } from 'react';
import { SankeyComponent } from '@syncfusion/ej2-react-charts';
import {
  SankeyComponent, Inject, SankeyTooltip, SankeyLegend,
  SankeyNodeDirective, SankeyExport,
  SankeyNodesCollectionDirective,
  SankeyLinkDirective,
  SankeyLinksCollectionDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function ExportableSankey() {
  const chartRef = useRef(null);

  const exportChart = (format) => {
    if (chartRef.current) {
      const fileName = `sankey-diagram-${new Date().getTime()}.${format.toLowerCase()}`;
      chartRef.current.export(format, fileName);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '15px' }}>
        <button onClick={() => exportChart('PNG')}>Export as PNG</button>
        <button onClick={() => exportChart('PDF')}>Export as PDF</button>
        <button onClick={() => exportChart('SVG')}>Export as SVG</button>
        <button onClick={() => window.print()}>Print</button>
      </div>

      <SankeyComponent
        ref={chartRef}
        width="90%"
        height="420px"
        title="Energy Flow"
      >
          <SankeyNodesCollectionDirective>
            <SankeyNodeDirective id="Solar" label={{ text: 'Solar' }} />
            <SankeyNodeDirective id="Wind" label={{ text: 'Wind' }} />
            <SankeyNodeDirective id="Natural Gas" label={{ text: 'Natural Gas' }} />
            <SankeyNodeDirective id="Generation" label={{ text: 'Generation' }} />
            <SankeyNodeDirective id="Residential" label={{ text: 'Residential' }} />
            <SankeyNodeDirective id="Commercial" label={{ text: 'Commercial' }} />
            <SankeyNodeDirective id="Industrial" label={{ text: 'Industrial' }} />
          </SankeyNodesCollectionDirective>
          <SankeyLinksCollectionDirective>
            <SankeyLinkDirective sourceId="Solar" targetId="Generation" value={450} />
            <SankeyLinkDirective sourceId="Wind" targetId="Generation" value={200} />
            <SankeyLinkDirective sourceId="Natural Gas" targetId="Generation" value={800} />
            <SankeyLinkDirective sourceId="Generation" targetId="Residential" value={300} />
            <SankeyLinkDirective sourceId="Generation" targetId="Commercial" value={400} />
            <SankeyLinkDirective sourceId="Generation" targetId="Industrial" value={350} />
          </SankeyLinksCollectionDirective>
          <Inject services={[SankeyTooltip, SankeyLegend, SankeyExport]} />
          </SankeyComponent>
    </div>
  );
}

export default ExportableSankey;
ReactDOM.render(<ExportableSankey />, document.getElementById("charts"));
```

## Best Practices

1. **Choose appropriate format** - PNG for web, PDF for printing, SVG for editing
2. **Provide filename context** - Include date or data type in filename
3. **Test exports** - Verify quality in different applications
4. **Include metadata** - Add title, date, and source information
5. **Optimize file size** - Use compression for large exports
6. **User-friendly options** - Clear labels and button placement
7. **Batch export** - Allow exporting multiple formats at once
8. **Error handling** - Handle export failures gracefully
