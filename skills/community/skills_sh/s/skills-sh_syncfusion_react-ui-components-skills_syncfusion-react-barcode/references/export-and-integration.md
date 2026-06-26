# Export and Integration Reference

## Table of Contents
- [Overview](#overview)
- [Export as Image](#export-as-image)
- [Export as Base64 String](#export-as-base64-string)
- [Image Formats](#image-formats)
- [Use Cases](#use-cases)
- [Integration Patterns](#integration-patterns)
- [Error Handling](#error-handling)

## Overview

Syncfusion barcode generators support two primary export mechanisms:

1. **Export as Image** - Download barcode as a file (JPG, PNG)
2. **Export as Base64 String** - Get barcode as encoded data string

Both methods work with all generator types: BarcodeGeneratorComponent, QRCodeGeneratorComponent, and DataMatrixGeneratorComponent.

## Export as Image

### Method: exportImage()

Downloads the barcode as an image file to the user's computer.

**Syntax:**
```typescript
barcodeInstance.exportImage(filename, format)
```

**Parameters:**
- `filename` (string) - Name of the file to download (without extension)
- `format` (string) - Image format: `"JPG"` or `"PNG"`

### Basic Implementation

```tsx
import React, { useRef } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function ExportBarcode() {
  const barcodeRef = useRef();

  const handleExport = () => {
    barcodeRef.current.exportImage('barcode', 'PNG');
  };

  return (
    <div>
      <BarcodeGeneratorComponent
        id="barcode"
        ref={barcodeRef}
        type="Code128"
        value="EXPORT-123"
        width="250px"
        height="100px"
      />
      <button onClick={handleExport}>Download as PNG</button>
    </div>
  );
}
```

### Export with Different Formats

```tsx
import React, { useRef } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function MultiFormatExport() {
  const barcodeRef = useRef();

  const exportPNG = () => {
    barcodeRef.current.exportImage('barcode-export', 'PNG');
  };

  const exportJPG = () => {
    barcodeRef.current.exportImage('barcode-export', 'JPG');
  };

  return (
    <div>
      <BarcodeGeneratorComponent
        id="barcode"
        ref={barcodeRef}
        type="Code128"
        value="FORMAT-SELECT"
        width="250px"
        height="100px"
      />
      
      <div style={{ marginTop: '10px' }}>
        <button onClick={exportPNG} style={{ marginRight: '10px' }}>
          Download PNG
        </button>
        <button onClick={exportJPG}>
          Download JPG
        </button>
      </div>
    </div>
  );
}
```

### Export with Filename Generation

```tsx
import React, { useRef, useState } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function DynamicExport() {
  const barcodeRef = useRef();
  const [productId, setProductId] = useState('PROD-001');

  const handleExport = () => {
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `barcode_${productId}_${timestamp}`;
    barcodeRef.current.exportImage(filename, 'PNG');
  };

  return (
    <div>
      <input
        type="text"
        value={productId}
        onChange={(e) => setProductId(e.target.value)}
        placeholder="Enter product ID"
      />
      
      <BarcodeGeneratorComponent
        id="barcode"
        ref={barcodeRef}
        type="Code128"
        value={productId}
        width="250px"
        height="100px"
      />
      
      <button onClick={handleExport}>
        Export {productId}
      </button>
    </div>
  );
}
```

## Export as Base64 String

### Method: exportAsBase64Image()

Returns the barcode as a base64-encoded string instead of downloading.

**Syntax:**
```typescript
const base64String = await barcodeInstance.exportAsBase64Image(format)
```

**Parameters:**
- `format` (string) - Image format: `"JPG"` or `"PNG"`

**Returns:**
- Promise that resolves to base64 string

### Basic Implementation

```tsx
import React, { useRef } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function ExportBase64() {
  const barcodeRef = useRef();

  const handleExportBase64 = async () => {
    const base64String = await barcodeRef.current.exportAsBase64Image('PNG');
    console.log('Base64 String:', base64String);
    // Result: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
  };

  return (
    <div>
      <BarcodeGeneratorComponent
        id="barcode"
        ref={barcodeRef}
        type="Code128"
        value="BASE64-123"
        width="250px"
        height="100px"
      />
      <button onClick={handleExportBase64}>Get Base64</button>
    </div>
  );
}
```

### Copy Base64 to Clipboard

```tsx
import React, { useRef, useState } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function CopyBase64() {
  const barcodeRef = useRef();
  const [copied, setCopied] = useState(false);

  const handleExportAndCopy = async () => {
    const base64String = await barcodeRef.current.exportAsBase64Image('PNG');
    await navigator.clipboard.writeText(base64String);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div>
      <BarcodeGeneratorComponent
        id="barcode"
        ref={barcodeRef}
        type="Code128"
        value="CLIPCOPY"
        width="250px"
        height="100px"
      />
      <button onClick={handleExportAndCopy}>
        {copied ? '✓ Copied!' : 'Copy Base64'}
      </button>
    </div>
  );
}
```

## Image Formats

### PNG Format

**Best For:**
- Web display
- Transparency support needed
- Lossless compression
- Small file sizes

**Characteristics:**
- Lossless compression
- Supports transparency (alpha channel)
- Better for sharp edges (like barcodes)
- Larger file size than JPG for photos, but smaller for graphics

**Usage:**
```tsx
barcodeRef.current.exportImage('barcode', 'PNG');
// or
const base64 = await barcodeRef.current.exportAsBase64Image('PNG');
```

### JPG Format

**Best For:**
- Document archival
- Photo-based contexts
- Smaller file sizes
- Legacy system compatibility

**Characteristics:**
- Lossy compression
- No transparency support
- Good for continuous tone images
- Smaller files for photos

**Usage:**
```tsx
barcodeRef.current.exportImage('barcode', 'JPG');
// or
const base64 = await barcodeRef.current.exportAsBase64Image('JPG');
```

### Format Comparison

| Feature | PNG | JPG |
|---------|-----|-----|
| **Compression** | Lossless | Lossy |
| **Quality** | Perfect | Minor loss |
| **Transparency** | Yes | No |
| **File Size (Barcode)** | Smaller | Larger |
| **Best For** | Web, digital | Archive, documents |
| **Barcode Clarity** | Excellent | Good |

## Use Cases

### Use Case 1: Print Operations

Export barcodes for printing labels or documents:

```tsx
import React, { useRef } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function PrintableBarcode() {
  const barcodeRef = useRef();

  const handlePrint = async () => {
    // Export as PNG for high quality print
    const base64 = await barcodeRef.current.exportAsBase64Image('PNG');
    
    // Open in new window for printing
    const printWindow = window.open();
    printWindow.document.write(`
      <img src="${base64}" style="max-width: 100%; height: auto;" />
    `);
    printWindow.print();
  };

  return (
    <div>
      <BarcodeGeneratorComponent
        id="print-barcode"
        ref={barcodeRef}
        type="Code128"
        value="PRINT-001"
        width="300px"
        height="120px"
      />
      <button onClick={handlePrint}>Print Barcode</button>
    </div>
  );
}
```

### Use Case 2: API Upload

Send barcode to server for storage or processing:

```tsx
import React, { useRef } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function UploadBarcode() {
  const barcodeRef = useRef();

  const handleUpload = async () => {
    const base64String = await barcodeRef.current.exportAsBase64Image('PNG');

    // Send to server
    const response = await fetch('/api/barcodes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        barcode: base64String,
        productId: 'PROD-123',
        timestamp: new Date().toISOString()
      })
    });

    if (response.ok) {
      alert('Barcode saved successfully');
    }
  };

  return (
    <div>
      <BarcodeGeneratorComponent
        id="upload-barcode"
        ref={barcodeRef}
        type="Code128"
        value="API-UPLOAD"
        width="250px"
        height="100px"
      />
      <button onClick={handleUpload}>Save to Server</button>
    </div>
  );
}
```

### Use Case 3: Email or Message Integration

Embed barcode in email or messages:

```tsx
import React, { useRef } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function EmailBarcode() {
  const barcodeRef = useRef();

  const handleSendEmail = async () => {
    const base64String = await barcodeRef.current.exportAsBase64Image('PNG');

    await fetch('/api/send-email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        to: 'customer@example.com',
        subject: 'Your Order Barcode',
        barcode: base64String,
        orderId: 'ORD-123'
      })
    });

    alert('Email sent with barcode');
  };

  return (
    <div>
      <BarcodeGeneratorComponent
        id="email-barcode"
        ref={barcodeRef}
        type="Code128"
        value="ORD-123"
        width="250px"
        height="100px"
      />
      <button onClick={handleSendEmail}>Send via Email</button>
    </div>
  );
}
```

### Use Case 4: Display in Image Element

Embed base64 barcode in an img tag:

```tsx
import React, { useRef, useState } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function EmbedBarcode() {
  const barcodeRef = useRef();
  const [imageData, setImageData] = useState(null);

  const generateImage = async () => {
    const base64 = await barcodeRef.current.exportAsBase64Image('PNG');
    setImageData(base64);
  };

  return (
    <div>
      <BarcodeGeneratorComponent
        id="embed-barcode"
        ref={barcodeRef}
        type="Code128"
        value="EMBEDDED"
        width="250px"
        height="100px"
        displayText={{ text: 'Generating...' }}
      />
      
      <button onClick={generateImage}>Generate Image</button>

      {imageData && (
        <div style={{ marginTop: '20px' }}>
          <h3>Embedded Result:</h3>
          <img src={imageData} alt="Generated Barcode" />
          <p>
            <code>{imageData.substring(0, 50)}...</code>
          </p>
        </div>
      )}
    </div>
  );
}
```

## Integration Patterns

### Pattern 1: Batch Export

Export multiple barcodes at once:

```tsx
import React, { useRef } from 'react';
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';

export default function BatchExport() {
  const qrRefs = useRef([]);

  const handleBatchExport = async () => {
    const zip = new JSZip();
    const folder = zip.folder('barcodes');

    for (let i = 0; i < qrRefs.current.length; i++) {
      const base64 = await qrRefs.current[i].exportAsBase64Image('PNG');
      const imageData = base64.replace(/^data:image\/png;base64,/, '');
      folder.file(`barcode_${i + 1}.png`, imageData, { base64: true });
    }

    const blob = await zip.generateAsync({ type: 'blob' });
    saveAs(blob, 'barcodes.zip');
  };

  const products = ['PROD-001', 'PROD-002', 'PROD-003'];

  return (
    <div>
      <h3>Batch QR Code Export</h3>
      
      {products.map((product, index) => (
        <QRCodeGeneratorComponent
          key={product}
          id={`qr-${index}`}
          ref={(el) => (qrRefs.current[index] = el)}
          value={`https://example.com/${product}`}
          width="150px"
          height="150px"
        />
      ))}

      <button onClick={handleBatchExport} style={{ marginTop: '20px' }}>
        Export All as ZIP
      </button>
    </div>
  );
}
```

### Pattern 2: Database Storage

Save barcodes to database for retrieval:

```tsx
import React, { useRef } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function DatabaseStorage() {
  const barcodeRef = useRef();

  const handleSaveToDatabase = async () => {
    const base64 = await barcodeRef.current.exportAsBase64Image('PNG');

    await fetch('/api/database/save-barcode', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        productId: 'PROD-123',
        barcodeImage: base64,
        format: 'PNG',
        createdAt: new Date().toISOString()
      })
    });

    alert('Saved to database');
  };

  return (
    <div>
      <BarcodeGeneratorComponent
        id="db-barcode"
        ref={barcodeRef}
        type="Code128"
        value="DB-STORE"
        width="250px"
        height="100px"
      />
      <button onClick={handleSaveToDatabase}>Save to Database</button>
    </div>
  );
}
```

## Error Handling

### Safe Export with Error Handling

```tsx
import React, { useRef, useState } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function SafeExport() {
  const barcodeRef = useRef();
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleExport = async () => {
    setLoading(true);
    setError(null);

    try {
      if (!barcodeRef.current) {
        throw new Error('Barcode component not initialized');
      }

      const base64 = await barcodeRef.current.exportAsBase64Image('PNG');
      
      if (!base64) {
        throw new Error('Failed to generate barcode image');
      }

      // Successfully got data, now do something with it
      console.log('Export successful');

    } catch (err) {
      setError(`Export failed: ${err.message}`);
      console.error('Export error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <BarcodeGeneratorComponent
        id="safe-barcode"
        ref={barcodeRef}
        type="Code128"
        value="SAFE-EXPORT"
        width="250px"
        height="100px"
      />

      <button 
        onClick={handleExport}
        disabled={loading}
        style={{ marginTop: '10px' }}
      >
        {loading ? 'Exporting...' : 'Export Safely'}
      </button>

      {error && (
        <div style={{ 
          marginTop: '10px', 
          padding: '10px', 
          backgroundColor: '#fee',
          color: '#c33',
          borderRadius: '4px'
        }}>
          ⚠️ {error}
        </div>
      )}
    </div>
  );
}
```

### Validation Before Export

```tsx
import React, { useRef, useState } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function ValidatedExport() {
  const barcodeRef = useRef();
  const [barcodeValue, setBarcodeValue] = useState('TEST-123');

  const isValidValue = (value: string) => {
    return value && value.trim().length > 0 && value.length <= 100;
  };

  const handleExport = async () => {
    if (!isValidValue(barcodeValue)) {
      alert('Invalid barcode value');
      return;
    }

    try {
      barcodeRef.current.exportImage('barcode', 'PNG');
    } catch (error) {
      alert('Export failed: ' + error.message);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={barcodeValue}
        onChange={(e) => setBarcodeValue(e.target.value)}
        placeholder="Enter barcode value (1-100 chars)"
        maxLength={100}
      />

      <BarcodeGeneratorComponent
        id="validated-barcode"
        ref={barcodeRef}
        type="Code128"
        value={barcodeValue || 'EMPTY'}
        width="250px"
        height="100px"
      />

      <button 
        onClick={handleExport}
        disabled={!isValidValue(barcodeValue)}
      >
        Export
      </button>
    </div>
  );
}
```
