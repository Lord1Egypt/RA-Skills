# Data Matrix Generator Reference

## Table of Contents
- [Data Matrix Overview](#data-matrix-overview)
- [Characteristics](#characteristics)
- [Basic Implementation](#basic-implementation)
- [Size Selection](#size-selection)
- [Encoding and Data](#encoding-and-data)
- [Common Use Cases](#common-use-cases)
- [Comparison with Other Codes](#comparison-with-other-codes)
- [Real-World Examples](#real-world-examples)

## Data Matrix Overview

Data Matrix is a 2D barcode that consists of a grid of dark and light dots forming a square or rectangular symbol. It's designed for high-volume, small-scale marking and is widely used in industrial and logistics applications.

### Key Characteristics
- **2D Format:** Square or rectangular grid pattern
- **Compact Size:** High data density in small physical space
- **Industrial Grade:** Designed for harsh printing conditions
- **ISO Standard:** ISO/IEC 16022 compliant
- **Durable:** Works on labels, parts, circuit boards
- **Data Capacity:** Hundreds to thousands of characters

## API Reference

### DataMatrixGeneratorComponent Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | `string` | Yes | Unique identifier for the component instance |
| `value` | `string` | Yes | The data to be encoded in the barcode |
| `width` | `string` | No | Width of the barcode (e.g., "150px", "200px") |
| `height` | `string` | No | Height of the barcode (e.g., "150px", "200px") |
| `foreColor` | `string` | No | Color of the barcode bars (e.g., "red", "#FF0000") |
| `displayText` | `object` | No | Display text customization with `text` property |
| `displayText.text` | `string` | No | Custom text to display with the barcode |

### Basic Component Setup

```tsx
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

<DataMatrixGeneratorComponent
  id="barcode"
  value="Syncfusion"
  width="200px"
  height="150px"
  foreColor="black"
  displayText={{ text: "Barcode Text" }}
/>
```

## Characteristics

### Size Variations

Data Matrix comes in different physical sizes. Syncfusion automatically calculates the optimal size for your data.

| Dimension | Module Count | Typical Use |
|-----------|-------------|-----------|
| 10×10 | 10×10 | Very short text, numeric |
| 12×12 | 12×12 | Short serial numbers |
| 14×14 | 14×14 | Standard product serial |
| 18×18 | 18×18 | Part identification |
| 22×22 | 22×22 | Inventory tracking |
| 32×32 | 32×32 | Large dataset, address |
| 48×48 | 48×48 | Maximum capacity |

### Format Flexibility

```tsx
import React from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function DataMatrixSizes() {
  return (
    <div>
      {/* Very short - compact size */}
      <DataMatrixGeneratorComponent
        id="dm1"
        value="12345"
        width="100px"
        height="100px"
      />

      {/* Medium - standard size */}
      <DataMatrixGeneratorComponent
        id="dm2"
        value="PART-12345-REV-A"
        width="150px"
        height="150px"
      />

      {/* Long data - larger size */}
      <DataMatrixGeneratorComponent
        id="dm3"
        value="Serial:ABC123 Lot:XYZ789 MfgDate:2024-03-15 ExpDate:2026-03-15"
        width="200px"
        height="200px"
      />
    </div>
  );
}
```

## Basic Implementation

### Minimal Data Matrix

```tsx
import React from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function BasicDataMatrix() {
  return (
    <DataMatrixGeneratorComponent
      id="datamatrix"
      value="Syncfusion"
      width="150px"
      height="150px"
    />
  );
}
```

### With Display Text

```tsx
<DataMatrixGeneratorComponent
  id="datamatrix"
  value="PART-12345"
  width="150px"
  height="150px"
  displayText={{
    text: "Part Serial"
  }}
/>
```

### With Custom Color (foreColor)

```tsx
<DataMatrixGeneratorComponent
  id="datamatrix-colored"
  value="PART-12345"
  width="150px"
  height="150px"
  foreColor="red"
/>
```

### In a Container (Common for Labels)

```tsx
<div style={{
  border: '2px solid black',
  padding: '10px',
  textAlign: 'center',
  width: 'fit-content'
}}>
  <h3>Product Label</h3>
  <DataMatrixGeneratorComponent
    id="label-dm"
    value="SKU:12345 LOT:ABC789"
    width="150px"
    height="150px"
  />
  <p style={{ fontSize: '12px', margin: '5px 0' }}>
    SKU: 12345<br/>
    LOT: ABC789<br/>
    MFG: 2024-03
  </p>
</div>
```

## Size Selection

### Guidelines by Data Length

```tsx
// Short (5-10 chars) - 10×10 to 14×14 modules
// Best for: Part numbers, serial codes, simple IDs
<DataMatrixGeneratorComponent
  id="dm-short"
  value="ABC123"
  width="120px"
  height="120px"
/>

// Medium (15-30 chars) - 18×18 to 22×22 modules
// Best for: Product identification, lot tracking
<DataMatrixGeneratorComponent
  id="dm-med"
  value="PART-ABC-123-REV-A"
  width="150px"
  height="150px"
/>

// Long (30-100+ chars) - 32×32 to 48×48 modules
// Best for: Full product info, addresses, complex data
<DataMatrixGeneratorComponent
  id="dm-long"
  value="Manufacturer:Syncfusion Inc, Product:Component, Version:2024.1, SerialNo:SN123456789, MfgDate:2024-03-15"
  width="200px"
  height="200px"
/>
```

## Encoding and Data

### Character Support

Data Matrix supports:
- **Alphanumeric:** 0-9, A-Z, space, and common symbols
- **Special Characters:** Limited special char set
- **Numeric-only:** More efficient for pure numbers
- **ASCII:** Extended ASCII characters possible

### Data Encoding Examples

```tsx
// Simple numeric
<DataMatrixGeneratorComponent
  id="dm-numeric"
  value="123456789"
  width="150px"
  height="150px"
/>

// Alphanumeric product code
<DataMatrixGeneratorComponent
  id="dm-alpha"
  value="PROD-ABC-123-XYZ"
  width="150px"
  height="150px"
/>

// Mixed with hyphens and slashes
<DataMatrixGeneratorComponent
  id="dm-mixed"
  value="ABC-123/DEF-456"
  width="150px"
  height="150px"
/>

// Manufacturing information
<DataMatrixGeneratorComponent
  id="dm-mfg"
  value="MFG:2024-03 EXP:2026-03 LOT:XYZ789"
  width="150px"
  height="150px"
/>

// With custom color customization
<DataMatrixGeneratorComponent
  id="dm-colored"
  value="CUSTOM-CODE-001"
  width="150px"
  height="150px"
  foreColor="darkblue"
/>
```
## Comprehensive API Usage Examples

### Complete Configuration with All Properties

```tsx
import React from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function CompleteDataMatrixExample() {
  return (
    <div style={{ padding: '20px' }}>
      {/* Basic barcode - minimal configuration */}
      <div style={{ marginBottom: '30px' }}>
        <h3>Minimal Configuration</h3>
        <DataMatrixGeneratorComponent
          id="dm-basic"
          value="ABC123"
        />
      </div>

      {/* With dimensions */}
      <div style={{ marginBottom: '30px' }}>
        <h3>With Custom Dimensions</h3>
        <DataMatrixGeneratorComponent
          id="dm-sized"
          value="PART-001"
          width="200px"
          height="200px"
        />
      </div>

      {/* With color and text */}
      <div style={{ marginBottom: '30px' }}>
        <h3>With Color and Display Text</h3>
        <DataMatrixGeneratorComponent
          id="dm-complete"
          value="PRODUCT-2024-ABC-123"
          width="180px"
          height="180px"
          foreColor="navy"
          displayText={{ text: "Product Code" }}
        />
      </div>

      {/* Professional label style */}
      <div style={{ 
        marginBottom: '30px',
        border: '2px solid #000',
        padding: '15px',
        width: 'fit-content',
        backgroundColor: '#f9f9f9'
      }}>
        <h3 style={{ marginTop: '0' }}>Professional Label</h3>
        <div style={{ textAlign: 'center' }}>
          <DataMatrixGeneratorComponent
            id="dm-label"
            value="MFG:2024-03BIN:A5SN:ES123456"
            width="160px"
            height="160px"
            foreColor="black"
            displayText={{ text: "Product Serial" }}
          />
          <div style={{ marginTop: '15px', fontSize: '12px', lineHeight: '1.6' }}>
            <div><strong>Serial Number:</strong> ES123456</div>
            <div><strong>Manufacturing:</strong> March 2024</div>
            <div><strong>Location:</strong> Bin A5</div>
          </div>
        </div>
      </div>
    </div>
  );
}
```
## Common Use Cases

### 1. Product Serialization

```tsx
import React from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function ProductSerial() {
  const productId = 'COMP-2024-001';

  return (
    <div style={{ padding: '10px', border: '1px solid #666' }}>
      <DataMatrixGeneratorComponent
        id="product-dm"
        value={productId}
        width="120px"
        height="120px"
      />
      <p style={{ fontSize: '11px', marginTop: '5px' }}>{productId}</p>
    </div>
  );
}
```

### 2. Inventory Management

```tsx
import React from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function InventoryLabel() {
  const inventoryData = 'SKU:12345LOT:ABC789BIN:A5QTY:50';

  return (
    <div style={{ padding: '15px', backgroundColor: '#f5f5f5' }}>
      <h4>Warehouse Label</h4>
      <DataMatrixGeneratorComponent
        id="inventory-dm"
        value={inventoryData}
        width="150px"
        height="150px"
      />
      <div style={{ fontSize: '12px', marginTop: '10px' }}>
        <p>SKU: 12345</p>
        <p>LOT: ABC789</p>
        <p>BIN: A5</p>
        <p>QTY: 50 units</p>
      </div>
    </div>
  );
}
```

### 3. Aerospace/Automotive Traceability

```tsx
import React from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function AerospaceTraceability() {
  const traceability = 'PN:FAA-12345SN:AE98765MFG:2024MAT:AL7075';

  return (
    <div style={{ padding: '10px', border: '2px solid #000' }}>
      <small style={{ display: 'block', marginBottom: '5px' }}>PART TRACEABILITY</small>
      <DataMatrixGeneratorComponent
        id="aerospace-dm"
        value={traceability}
        width="140px"
        height="140px"
      />
      <small style={{ display: 'block', marginTop: '5px', lineHeight: '1.4' }}>
        PN:FAA-12345<br/>
        SN:AE98765<br/>
        MFG:2024<br/>
        MAT:AL7075
      </small>
    </div>
  );
}
```

### 4. Batch/Lot Tracking

```tsx
import React, { useState } from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function BatchTracking() {
  const [batchNumber] = useState('BATCH-2024-001');
  const [lotCode] = useState('LOT-ABC-789');

  return (
    <div>
      <h3>Production Batch Label</h3>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div style={{ textAlign: 'center' }}>
          <div>Batch</div>
          <DataMatrixGeneratorComponent
            id="batch-dm"
            value={batchNumber}
            width="130px"
            height="130px"
          />
          <small>{batchNumber}</small>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div>Lot</div>
          <DataMatrixGeneratorComponent
            id="lot-dm"
            value={lotCode}
            width="130px"
            height="130px"
          />
          <small>{lotCode}</small>
        </div>
      </div>
    </div>
  );
}
```

## Comparison with Other Codes

| Feature | Data Matrix | QR Code | 1D Barcode |
|---------|------------|---------|-----------|
| **2D Format** | Yes | Yes | No |
| **Physical Size** | Very compact | Compact | Longest |
| **Data Capacity** | High (thousands) | Very High (thousands) | Low (dozens) |
| **Best Use** | Labels, parts, industrial | Marketing, URLs, contact | Retail, logistics |
| **Reader Type** | Industrial scanner or smartphone | Smartphone | Laser/camera scanner |
| **Error Correction** | 30% recovery | 30% recovery | None (checksum only) |
| **Standards** | ISO 16022 | ISO 18004 | Various |
| **Orientation** | Works upside down | Works any angle | Unidirectional |
| **Cost** | Medium | Low | Low |

## Real-World Examples

### Example 1: Electronics Component Labeling

```tsx
import React from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function ElectronicsLabel() {
  return (
    <div style={{
      width: '200px',
      padding: '10px',
      border: '1px solid #000',
      fontFamily: 'monospace'
    }}>
      <small>POWER SUPPLY</small>
      <DataMatrixGeneratorComponent
        id="electronics-dm"
        value="PN:PSU-2400VAC:100-240VSN:ES234567MFG:032024"
        width="120px"
        height="120px"
      />
      <div style={{ fontSize: '9px', lineHeight: '1.3', marginTop: '5px' }}>
        <div>PN: PSU-2400</div>
        <div>VAC: 100-240V</div>
        <div>SN: ES234567</div>
        <div>MFG: 03/2024</div>
      </div>
    </div>
  );
}
```

### Example 2: Pharmaceutical Batch

```tsx
import React from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function PharmaBatch() {
  return (
    <div style={{
      width: '180px',
      padding: '8px',
      border: '2px solid #0066cc',
      textAlign: 'center'
    }}>
      <strong style={{ display: 'block', marginBottom: '5px', fontSize: '11px' }}>
        BATCH LABEL
      </strong>
      <DataMatrixGeneratorComponent
        id="pharma-dm"
        value="LOT:P2024001EXP:2026-03-15MFG:2024-03-15"
        width="110px"
        height="110px"
      />
      <div style={{ fontSize: '10px', marginTop: '5px', lineHeight: '1.4' }}>
        <div>LOT: P2024001</div>
        <div>EXP: 2026-03-15</div>
        <div>MFG: 2024-03-15</div>
      </div>
    </div>
  );
}
```

### Example 3: Logistics/Shipping

```tsx
import React from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function ShippingLabel() {
  const trackingCode = 'TRK:SH2024001LOC:WHF-05';

  return (
    <div style={{
      padding: '15px',
      backgroundColor: '#fffacd',
      border: '1px solid #daa520',
      maxWidth: '250px'
    }}>
      <h4 style={{ margin: '0 0 10px 0' }}>SHIPMENT LABEL</h4>
      <div style={{ marginBottom: '10px' }}>
        <DataMatrixGeneratorComponent
          id="shipping-dm"
          value={trackingCode}
          width="130px"
          height="130px"
        />
      </div>
      <div style={{ fontSize: '12px', fontWeight: 'bold' }}>
        Tracking: SH2024001
      </div>
      <div style={{ fontSize: '11px' }}>
        Location: WHF-05 (Warehouse Floor 5)
      </div>
      <div style={{ fontSize: '10px', marginTop: '8px', color: 'red' }}>
        FRAGILE - HANDLE WITH CARE
      </div>
    </div>
  );
}
```

### Example 4: Dynamic Data Matrix Generator

```tsx
import React, { useState } from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function DynamicDataMatrix() {
  const [partNumber, setPartNumber] = useState('PART-001');
  const [serialNumber, setSerialNumber] = useState('SN12345');

  const dmValue = `PN:${partNumber}SN:${serialNumber}`;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Data Matrix Generator</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <label>
          Part Number:
          <input
            type="text"
            value={partNumber}
            onChange={(e) => setPartNumber(e.target.value)}
            style={{ marginLeft: '10px', padding: '5px' }}
          />
        </label>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label>
          Serial Number:
          <input
            type="text"
            value={serialNumber}
            onChange={(e) => setSerialNumber(e.target.value)}
            style={{ marginLeft: '10px', padding: '5px' }}
          />
        </label>
      </div>

      <div style={{ 
        padding: '20px',
        border: '1px solid #ddd',
        display: 'inline-block'
      }}>
        <DataMatrixGeneratorComponent
          id="dynamic-dm"
          value={dmValue}
          width="150px"
          height="150px"
        />
        <p style={{ fontSize: '12px', marginTop: '10px' }}>
          {dmValue}
        </p>
      </div>
    </div>
  );
}
```
