---
name: syncfusion-react-barcode
description: "Generate, customize, and export barcodes in React using Syncfusion BarcodeGenerator. Trigger for requests involving Code39 or Code128 barcodes, QR codes, Data Matrix generation, barcode styling (size, color, text, margins), React component setup, props or events, SVG or canvas rendering, and exporting or printing barcode images."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion React Barcode

## When to Use This Skill

Use this skill when you need to:
- Generate barcodes (Code39, Code128, Code11, Code32, Code93, Codabar) in React
- Create QR codes for URLs, contact info, or product identification
- Generate Data Matrix codes for labels, tracking, or inventory
- Customize barcode appearance (size, color, text display)
- Export barcodes as images (JPG, PNG) or base64 strings
- Integrate barcode generation into forms, reports, or applications

## Library Overview: Three Generator Types

Syncfusion React Barcode provides three main components:

1. **BarcodeGeneratorComponent** - Traditional 1D barcodes (Code39, Code128, etc.)
   - Character encoding varies by type
   - Ideal for: Product codes, inventory, retail
   - Readability: High, works with basic scanners

2. **QRCodeGeneratorComponent** - 2D Quick Response codes
   - Versions 1-40 with automatic scaling
   - Ideal for: URLs, contact info, product links, advertising
   - Capacity: Up to thousands of characters

3. **DataMatrixGeneratorComponent** - 2D Data Matrix codes
   - Square/rectangular format, compact size
   - Ideal for: Labels, parts tracking, aerospace/automotive
   - Capacity: Alphanumeric data, efficient encoding

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and dependencies
- Vite/React setup
- Component imports and basic structure
- Parent component initialization

### Barcode Generator Types
📄 **Read:** [references/barcode-generator.md](references/barcode-generator.md)
- Code39, Code39Extended, Code11, Code128, Code32, Code93, Codabar
- When to use each type
- Character set support per type
- Encoding and checksum information
- Implementation examples for each

### QR Code Generator
📄 **Read:** [references/qr-code-generator.md](references/qr-code-generator.md)
- QR Code basics and versions
- Automatic version selection
- Character encoding (numeric, alphanumeric, JIS8)
- Common use cases and patterns
- Implementation with different data types

### Data Matrix Generator
📄 **Read:** [references/data-matrix-generator.md](references/data-matrix-generator.md)
- Data Matrix basics and structure
- Encoding rules and character support
- Size and capacity considerations
- Label and printing applications
- Comparison with other barcode types

### Customization and Styling
📄 **Read:** [references/customization.md](references/customization.md)
- Barcode dimensions (width, height)
- Colors (foreColor, backgroundColor)
- Display text customization
- Examples of size and color variations
- Responsive design patterns

### Export and Integration
📄 **Read:** [references/export-and-integration.md](references/export-and-integration.md)
- Export as image (JPG, PNG)
- Export as base64 string
- Method: exportImage(filename, format)
- Method: exportAsBase64Image(format)
- Integration with forms, APIs, and reports

## Quick Start Examples

### Code39 Barcode
```tsx
import React from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function App() {
  return (
    <BarcodeGeneratorComponent
      id="barcode"
      type="Code39"
      value="SYNCFUSION"
      width="200px"
      height="150px"
    />
  );
}
```

### QR Code
```tsx
import React from 'react';
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function App() {
  return (
    <QRCodeGeneratorComponent
      id="qrcode"
      value="https://www.syncfusion.com"
      width="200px"
      height="200px"
    />
  );
}
```

### Data Matrix
```tsx
import React from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function App() {
  return (
    <DataMatrixGeneratorComponent
      id="datamatrix"
      value="Syncfusion"
      width="200px"
      height="200px"
    />
  );
}
```

## Common Patterns

### Pattern 1: Dynamic Value Generation
```tsx
const [barcodeValue, setBarcodeValue] = React.useState('DEFAULT123');

<BarcodeGeneratorComponent
  type="Code128"
  value={barcodeValue}
  width="200px"
  height="150px"
/>
```

### Pattern 2: Export on Button Click
```tsx
const barcodeRef = React.useRef();

const handleExport = () => {
  barcodeRef.current.exportImage('barcode', 'PNG');
};

<div>
  <BarcodeGeneratorComponent
    ref={barcodeRef}
    type="Code39"
    value="SYNC123"
    width="200px"
    height="150px"
  />
  <button onClick={handleExport}>Download Barcode</button>
</div>
```

### Pattern 3: Styled Container
```tsx
<div style={{ padding: '20px', border: '1px solid #ddd' }}>
  <QRCodeGeneratorComponent
    value="https://example.com"
    width="250px"
    height="250px"
    foreColor="#333"
    backgroundColor="#fff"
  />
</div>
```

## Key Props

| Prop | Description | Used By |
|------|-------------|---------|
| `type` | Barcode type (Code39, Code128, Code11, Code32, Code93, Codabar) | BarcodeGeneratorComponent |
| `value` | Data to encode | All generators |
| `width` | Barcode width (string with px) | All generators |
| `height` | Barcode height (string with px) | All generators |
| `foreColor` | Dark/bar color | All generators |
| `backgroundColor` | Light/space color | All generators |
| `displayText` | Object to customize display text | All generators |
| `id` | Unique component identifier (required for export) | All generators |

## Common Use Cases

1. **Retail & Inventory**: Code128 barcodes for products and SKUs
2. **E-commerce**: QR codes linking to product pages or reviews
3. **Logistics**: Data Matrix for package tracking and labels
4. **Document Management**: QR codes embedding document metadata
5. **Marketing**: Dynamic QR codes with analytics
6. **Healthcare**: Code128/Code39 for specimen/patient labeling
7. **Form Workflows**: Export barcodes for printing or archival

## Next Steps

1. Choose your generator type based on use case
2. Read the getting started guide
3. Review the specific generator documentation
4. Customize appearance as needed
5. Implement export if required for your workflow
