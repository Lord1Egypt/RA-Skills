# Export and Print

The Range Navigator component supports exporting to various image formats (PNG, JPEG, SVG, PDF) and printing functionality, allowing users to save or print the visualization for reports, presentations, or documentation.

## Table of contents
- [Export Formats](#export-formats)
- [Basic Export](#basic-export)
  - [Export to PNG](#export-to-png)
  - [Export to JPEG](#export-to-jpeg)
  - [Export to SVG](#export-to-svg)
  - [Export to PDF](#export-to-pdf)
- [Export with Custom Filename](#export-with-custom-filename)
- [Print Functionality](#print-functionality)
  - [Basic Print](#basic-print)
  - [Keyboard Shortcut for Print](#keyboard-shortcut-for-print)
- [Multiple Export Options](#multiple-export-options)
- [Export with Base64](#export-with-base64)
- [Export Events](#export-events)
- [Format Comparison](#format-comparison)
- [Browser Compatibility](#browser-compatibility)
- [Export/Print Method Signatures](#exportprint-method-signatures)
- [Best Practices](#best-practices)
- [Common Use Cases](#common-use-cases)
- [Key Points](#key-points)
- [API Links](#api-links)

## Export Formats

The Range Navigator supports four export formats:

| Format | Extension | Use Case |
|--------|-----------|----------|
| PNG | .png | High-quality raster images with transparency support |
| JPEG | .jpeg/.jpg | Compressed raster images for smaller file sizes |
| SVG | .svg | Scalable vector graphics for infinite scaling |
| PDF | .pdf | Portable document format for printing and sharing |

## Basic Export

### Export to PNG

```tsx
import { useRef } from 'react';
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const rangeNavigatorRef = useRef(null);

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 },
    { date: new Date(2023, 4, 1), value: 120 },
    { date: new Date(2023, 5, 1), value: 125 }
  ];

  const handleExportPNG = () => {
    if (rangeNavigatorRef.current) {
      rangeNavigatorRef.current.export('PNG', 'RangeNavigator');
    }
  };

  return (
    <div>
      <button onClick={handleExportPNG}>Export as PNG</button>
      
      <RangeNavigatorComponent
        ref={rangeNavigatorRef}
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
      >
        <Inject services={[AreaSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Export to JPEG

```tsx
import { useRef } from 'react';
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const rangeNavigatorRef = useRef(null);

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  const handleExportJPEG = () => {
    if (rangeNavigatorRef.current) {
      rangeNavigatorRef.current.export('JPEG', 'RangeNavigator');
    }
  };

  return (
    <div>
      <button onClick={handleExportJPEG}>Export as JPEG</button>
      
      <RangeNavigatorComponent
        ref={rangeNavigatorRef}
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
      >
        <Inject services={[AreaSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Export to SVG

```tsx
import { useRef } from 'react';
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const rangeNavigatorRef = useRef(null);

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  const handleExportSVG = () => {
    if (rangeNavigatorRef.current) {
      rangeNavigatorRef.current.export('SVG', 'RangeNavigator');
    }
  };

  return (
    <div>
      <button onClick={handleExportSVG}>Export as SVG</button>
      
      <RangeNavigatorComponent
        ref={rangeNavigatorRef}
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
      >
        <Inject services={[AreaSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Export to PDF

```tsx
import { useRef } from 'react';
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const rangeNavigatorRef = useRef(null);

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  const handleExportPDF = () => {
    if (rangeNavigatorRef.current) {
      rangeNavigatorRef.current.export('PDF', 'RangeNavigator');
    }
  };

  return (
    <div>
      <button onClick={handleExportPDF}>Export as PDF</button>
      
      <RangeNavigatorComponent
        ref={rangeNavigatorRef}
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
      >
        <Inject services={[AreaSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Export with Custom Filename

Specify a custom filename when exporting:

```tsx
import { useRef } from 'react';
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const rangeNavigatorRef = useRef(null);

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  const handleExport = (format: 'PNG' | 'JPEG' | 'SVG' | 'PDF') => {
    if (rangeNavigatorRef.current) {
      const timestamp = new Date().toISOString().split('T')[0];
      const filename = `Sales_Report_${timestamp}`;
      rangeNavigatorRef.current.export(format, filename);
    }
  };

  return (
    <div>
      <button onClick={() => handleExport('PNG')}>Export PNG</button>
      <button onClick={() => handleExport('JPEG')}>Export JPEG</button>
      <button onClick={() => handleExport('SVG')}>Export SVG</button>
      <button onClick={() => handleExport('PDF')}>Export PDF</button>
      
      <RangeNavigatorComponent
        ref={rangeNavigatorRef}
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
      >
        <Inject services={[AreaSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Print Functionality

### Basic Print

```tsx
import { useRef } from 'react';
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const rangeNavigatorRef = useRef(null);

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  const handlePrint = () => {
    if (rangeNavigatorRef.current) {
      rangeNavigatorRef.current.print();
    }
  };

  return (
    <div>
      <button onClick={handlePrint}>Print</button>
      
      <RangeNavigatorComponent
        ref={rangeNavigatorRef}
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
      >
        <Inject services={[AreaSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Keyboard Shortcut for Print

Print using keyboard shortcut (Ctrl+P):

```tsx
import { useRef, useEffect } from 'react';
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const rangeNavigatorRef = useRef(null);

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (event.ctrlKey && event.key === 'p') {
        event.preventDefault();
        if (rangeNavigatorRef.current) {
          rangeNavigatorRef.current.print();
        }
      }
    };

    document.addEventListener('keydown', handleKeyPress);
    return () => {
      document.removeEventListener('keydown', handleKeyPress);
    };
  }, []);

  const handlePrint = () => {
    if (rangeNavigatorRef.current) {
      rangeNavigatorRef.current.print();
    }
  };

  return (
    <div>
      <button onClick={handlePrint}>Print (or press Ctrl+P)</button>
      
      <RangeNavigatorComponent
        ref={rangeNavigatorRef}
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
      >
        <Inject services={[AreaSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Multiple Export Options

Provide multiple export formats:

```tsx
import { useRef } from 'react';
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  RangeTooltip, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const rangeNavigatorRef = useRef(null);

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 },
    { date: new Date(2023, 4, 1), value: 120 },
    { date: new Date(2023, 5, 1), value: 125 }
  ];

  const handleExport = (format: 'PNG' | 'JPEG' | 'SVG' | 'PDF') => {
    if (rangeNavigatorRef.current) {
      rangeNavigatorRef.current.export(format, 'RangeNavigator');
    }
  };

  const handlePrint = () => {
    if (rangeNavigatorRef.current) {
      rangeNavigatorRef.current.print();
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => handleExport('PNG')}>📷 PNG</button>
        <button onClick={() => handleExport('JPEG')}>🖼️ JPEG</button>
        <button onClick={() => handleExport('SVG')}>📐 SVG</button>
        <button onClick={() => handleExport('PDF')}>📄 PDF</button>
        <button onClick={handlePrint}>🖨️ Print</button>
      </div>
      
      <RangeNavigatorComponent
        ref={rangeNavigatorRef}
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM yyyy"
        tooltip={{ enable: true }}
      >
        <Inject services={[AreaSeries, DateTime, RangeTooltip ]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Export with Base64

Export as Base64 string for embedding or further processing:

```tsx
import { useRef, useState } from 'react';
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const rangeNavigatorRef = useRef(null);
  const [base64Image, setBase64Image] = useState('');

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  const handleExportBase64 = () => {
    if (rangeNavigatorRef.current) {
      // Export and get Base64 string
      const base64 = rangeNavigatorRef.current.export('PNG', 'RangeNavigator', null, true);
      // The Base64 string is returned when the 4th parameter is true
      console.log('Base64:', base64);
      setBase64Image(base64);
    }
  };

  return (
    <div>
      <button onClick={handleExportBase64}>Export as Base64</button>
      
      <RangeNavigatorComponent
        ref={rangeNavigatorRef}
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
      >
        <Inject services={[AreaSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>

      {base64Image && (
        <div style={{ marginTop: '20px' }}>
          <h3>Base64 Preview:</h3>
          <img 
            src={base64Image} 
            alt="Exported Range Navigator" 
            style={{ maxWidth: '100%' }} 
          />
        </div>
      )}
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Export Events

Handle export before and after events:

```tsx
import { useRef } from 'react';
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective,
  IBeforeExportEventArgs,
  IAfterExportEventArgs
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const rangeNavigatorRef = useRef(null);

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  const handleExport = () => {
    if (rangeNavigatorRef.current) {
      rangeNavigatorRef.current.export('PNG', 'RangeNavigator');
    }
  };

  const beforeExport = (args: IBeforeExportEventArgs) => {
    console.log('Before Export:', args);
    // You can modify export settings here
  };

  const afterExport = (args: IAfterExportEventArgs) => {
    console.log('After Export:', args);
    // Perform actions after export completes
  };

  return (
    <div>
      <button onClick={handleExport}>Export</button>
      
      <RangeNavigatorComponent
        ref={rangeNavigatorRef}
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
        beforeExport={beforeExport}
        afterExport={afterExport}
      >
        <Inject services={[AreaSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Format Comparison

| Format | Best For | File Size | Quality | Scalability |
|--------|----------|-----------|---------|-------------|
| **PNG** | Web, presentations, transparency | Medium | High | Fixed resolution |
| **JPEG** | Photos, compressed images | Small | Good | Fixed resolution |
| **SVG** | Print, infinite scaling | Small | Perfect | Infinite |
| **PDF** | Reports, documents, printing | Medium | High | High |

## Browser Compatibility

Export and print features are supported in:
- Chrome
- Firefox
- Safari
- Edge
- Opera

## When to Use Each Format

### PNG
- Web applications
- Presentations
- Need transparency support
- High-quality raster images

### JPEG
- Email attachments (smaller file size)
- Compressed storage
- No transparency needed

### SVG
- Print materials
- Responsive web design
- Infinite scaling needed
- Smallest file size for vector graphics

### PDF
- Reports and documentation
- Professional printing
- Multi-page documents
- Archival purposes

## Export Method Signature

```typescript
export(
  type: 'PNG' | 'JPEG' | 'SVG' | 'PDF',
  fileName: string,
  orientation?: 'Portrait' | 'Landscape',
  controls?: RangeNavigatorComponent[],
  width?: number,
  height?: number,
  isVertical?: boolean
): void
```

## Print Method Signature

```typescript
print(id?: string | string[]): void
```

## Best Practices

1. **Filename Convention**: Use descriptive names with timestamps
2. **Format Selection**: Choose based on use case (see comparison table)
3. **Quality**: PNG/PDF for high quality, JPEG for smaller size
4. **User Choice**: Provide multiple export options
5. **Feedback**: Show success/error messages after export
6. **Accessibility**: Include keyboard shortcuts (Ctrl+P)
7. **Ref Management**: Always use refs to access export methods

## Common Use Cases

### Report Generation
```tsx
// Export as PDF for reports
rangeNavigatorRef.current.export('PDF', 'Monthly_Sales_Report');
```

### Web Sharing
```tsx
// Export as PNG for web sharing
rangeNavigatorRef.current.export('PNG', 'Range_Chart');
```

### High-Quality Print
```tsx
// Export as SVG for print
rangeNavigatorRef.current.export('SVG', 'Print_Ready_Chart');
```

### Email Attachment
```tsx
// Export as JPEG for smaller size
rangeNavigatorRef.current.export('JPEG', 'Chart_Summary');
```

## Key Points

1. **Four Formats**: PNG, JPEG, SVG, PDF support
2. **Easy Export**: Simple `export()` method with format and filename
3. **Print Support**: Built-in `print()` method
4. **Custom Filenames**: Specify names for exported files
5. **Base64 Export**: Option to export as Base64 string
6. **Events**: beforeExport and afterExport event handlers
7. **Keyboard Support**: Ctrl+P for printing
8. **Ref Required**: Use React refs to access export/print methods
9. **Format Selection**: Choose based on use case and requirements
10. **Browser Compatible**: Works across all modern browsers

## API Links

Full Range Navigator API: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

Export/print complex API references:
- Methods: [`export(type, fileName, orientation, controls, width, height, isVertical)`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#export), [`print(id)`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#print)
- Events: [`beforeExport`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#events) and [`afterExport`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#events)
- Notes: use a React `ref` to call export/print methods on the component instance

