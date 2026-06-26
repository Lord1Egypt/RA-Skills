# Getting Started with Syncfusion React Barcode

## Table of Contents
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Project Setup](#project-setup)
- [Basic Component Import](#basic-component-import)
- [Component Structure](#component-structure)
- [Common Import Patterns](#common-import-patterns)
- [Next Steps](#next-steps)

## Dependencies

The Syncfusion React barcode component requires the following minimum dependencies:

```json
{
  "@syncfusion/ej2-react-barcode-generator": "latest",
  "@syncfusion/ej2-base": "latest",
  "@syncfusion/ej2-data": "latest",
  "@syncfusion/ej2-barcode-generator": "latest",
  "@syncfusion/ej2-react-base": "latest",
  "@syncfusion/ej2-pdf-export": "latest",
  "@syncfusion/ej2-file-utils": "latest",
  "@syncfusion/ej2-compression": "latest",
  "@syncfusion/ej2-svg-base": "latest"
}
```

**Note:** Most dependencies are installed automatically with `@syncfusion/ej2-react-barcode-generator`.

## Installation

### Step 1: Create a React Project with Vite (Recommended)

Vite provides faster development builds and smaller bundle sizes compared to create-react-app:

```bash
npm create vite@latest my-barcode-app -- --template react
cd my-barcode-app
npm install
```

For TypeScript support:
```bash
npm create vite@latest my-barcode-app -- --template react-ts
cd my-barcode-app
npm install
```

### Step 2: Install Syncfusion Barcode Package

```bash
npm install @syncfusion/ej2-react-barcode-generator
```

This command automatically installs all required dependencies.

### Step 3: Verify Installation

Check `package.json` to confirm:
```json
{
  "dependencies": {
    "@syncfusion/ej2-react-barcode-generator": "^23.x.x",
    "react": "^18.x.x"
  }
}
```

## Project Setup

### Folder Structure

```
my-barcode-app/
├── src/
│   ├── App.jsx          (or App.tsx)
│   ├── main.jsx
│   └── index.css
├── package.json
├── vite.config.js
└── index.html
```

### Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Basic Component Import

### Single Generator Import

For BarcodeGeneratorComponent:
```tsx
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function App() {
  return (
    <BarcodeGeneratorComponent
      id="barcode"
      type="Code39"
      value="SYNCFUSION"
      width={"200px"}
      height={"150px"}
    />
  );
}
```

For QRCodeGeneratorComponent:
```tsx
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function App() {
  return (
    <QRCodeGeneratorComponent
      id="qrcode"
      value="https://www.syncfusion.com"
      width={"200px"}
      height={"200px"}
    />
  );
}
```

For DataMatrixGeneratorComponent:
```tsx
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function App() {
  return (
    <DataMatrixGeneratorComponent
      id="datamatrix"
      value="SyncData123"
      width={"200px"}
      height={"200px"}
    />
  );
}
```

## Component Structure

### Required Props

All barcode generators require:

| Prop | Type | Description | Example |
|------|------|-------------|---------|
| `id` | string | Unique component identifier (needed for export) | `"barcode"` |
| `value` | string | Data to encode in the barcode | `"SYNCFUSION"` |
| `type` | string | Barcode type (BarcodeGeneratorComponent only) | `"Code39"` |
| `width` | string | Width with unit (px recommended) | `"200px"` |
| `height` | string | Height with unit (px recommended) | `"150px"` |

### Basic Example with All Required Props

```tsx
import React from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function BarcodeExample() {
  return (
    <div>
      <h1>My First Barcode</h1>
      <BarcodeGeneratorComponent
        id="barcode1"
        type="Code128"
        value="ORDER-12345"
        width={"300px"}
        height={"100px"}
      />
    </div>
  );
}
```

## Common Import Patterns

### Pattern 1: Single Component

```tsx
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';
```

### Pattern 2: Multiple Generators in One File

```tsx
import { 
  BarcodeGeneratorComponent,
  QRCodeGeneratorComponent,
  DataMatrixGeneratorComponent
} from '@syncfusion/ej2-react-barcode-generator';
```

### Pattern 3: Named Exports in Separate Files

**components/Barcode.tsx**
```tsx
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export const Barcode = ({ value, type = 'Code39' }) => (
  <BarcodeGeneratorComponent
    id={`barcode-${value}`}
    type={type}
    value={value}
    width={"200px"}
    height={"150px"}
  />
);
```

**components/QRCode.tsx**
```tsx
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export const QRCode = ({ value, size = '200px' }) => (
  <QRCodeGeneratorComponent
    id={`qrcode-${Date.now()}`}
    value={value}
    width={size}
    height={size}
  />
);
```

### Pattern 4: Conditional Rendering

```tsx
import React, { useState } from 'react';
import { BarcodeGeneratorComponent, QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function BarcodeSelector() {
  const [barcodeType, setBarcodeType] = useState('barcode');

  return (
    <div>
      <select value={barcodeType} onChange={(e) => setBarcodeType(e.target.value)}>
        <option value="barcode">Barcode (Code128)</option>
        <option value="qrcode">QR Code</option>
      </select>

      {barcodeType === 'barcode' && (
        <BarcodeGeneratorComponent
          id="barcode1"
          type="Code128"
          value="SYNC-123"
          width={"200px"}
          height={"150px"}
        />
      )}

      {barcodeType === 'qrcode' && (
        <QRCodeGeneratorComponent
          id="qrcode1"
          value="https://www.syncfusion.com"
          width={"200px"}
          height={"200px"}
        />
      )}
    </div>
  );
}
```

## Next Steps

1. **Choose your barcode type**: Barcode, QR Code, or Data Matrix
2. **Read barcode-specific documentation**: See [barcode-generator.md](barcode-generator.md), [qr-code-generator.md](qr-code-generator.md), or [data-matrix-generator.md](data-matrix-generator.md)
3. **Customize appearance**: See [customization.md](customization.md) for sizing, colors, and text
4. **Implement export**: See [export-and-integration.md](export-and-integration.md) if you need to download barcodes

## Troubleshooting

**Issue: Component not rendering**
- Ensure all required props are provided (`id`, `value`, `width`, `height`)
- Check that the package is installed: `npm list @syncfusion/ej2-react-barcode-generator`

**Issue: Import errors**
- Verify the exact package name: `@syncfusion/ej2-react-barcode-generator`
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`

**Issue: Barcode appears very small**
- Increase `width` and `height` props (minimum recommended: 150px)
- Ensure values are strings with units: `"200px"` not `200`
