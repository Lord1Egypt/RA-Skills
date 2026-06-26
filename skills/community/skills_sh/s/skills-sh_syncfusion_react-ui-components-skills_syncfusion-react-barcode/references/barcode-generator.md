# Barcode Generator Reference

## Table of Contents
- [Overview](#overview)
- [Code39](#code39)
- [Code39 Extended](#code39-extended)
- [Code11](#code11)
- [Code128](#code128)
- [Code32](#code32)
- [Code93](#code93)
- [Codabar](#codabar)
- [Barcode Type Comparison](#barcode-type-comparison)
- [Selection Guide](#selection-guide)

## Overview

BarcodeGeneratorComponent generates traditional 1D (linear) barcodes. Each barcode type has specific character sets, encoding rules, and use cases. Choose the type based on your data and application requirements.

## Code39

### Characteristics
- **Character Set:** Digits 0-9, uppercase letters A-Z, space, minus (-), plus (+), period (.), dollar ($), slash (/), percent (%)
- **Checksum:** Optional (not required for common use)
- **Length:** Variable (can exceed 25 characters)
- **Use Case:** Inventory, general labeling, healthcare

### Implementation

```tsx
import React from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function Code39Example() {
  return (
    <BarcodeGeneratorComponent
      id="barcode-code39"
      type="Code39"
      value="SYNCFUSION"
      width="300px"
      height="150px"
    />
  );
}
```

### When to Use
- Product labeling
- Inventory tracking
- Healthcare identifiers
- Simple alphanumeric data
- Legacy barcode readers

### Common Examples

```tsx
// Product inventory
<BarcodeGeneratorComponent
  id="barcode1"
  type="Code39"
  value="PROD-12345"
  width="250px"
  height="100px"
/>

// Order number
<BarcodeGeneratorComponent
  id="barcode2"
  type="Code39"
  value="ORDER987"
  width="250px"
  height="100px"
/>
```

## Code39 Extended

### Characteristics
- **Character Set:** All ASCII characters (lowercase a-z, special keyboard chars)
- **Advantage:** Supports full ASCII including lowercase and special characters
- **Checksum:** Optional
- **Use Case:** When lowercase or special characters needed

### Implementation

```tsx
import React from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function Code39ExtendedExample() {
  return (
    <BarcodeGeneratorComponent
      id="barcode-code39ext"
      type="Code39Extension"
      value="SyncFusion@123"
      width="300px"
      height="150px"
    />
  );
}
```

### When to Use
- When lowercase letters required
- Special characters in text (email, URLs)
- Mixed case identifiers
- More flexible than standard Code39

### Common Examples

```tsx
// Email address
<BarcodeGeneratorComponent
  id="barcode1"
  type="Code39Extension"
  value="support@syncfusion.com"
  width="300px"
  height="100px"
/>

// Mixed case product code
<BarcodeGeneratorComponent
  id="barcode2"
  type="Code39Extension"
  value="ProdCode-aBc123"
  width="300px"
  height="100px"
/>
```

## Code11

### Characteristics
- **Character Set:** Digits 0-9, hyphen (-)
- **Checksum:** Required (automatic calculation)
- **Length:** 1 to 80 characters
- **Use Case:** Telecommunications, equipment identification

### Implementation

```tsx
import React from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function Code11Example() {
  return (
    <BarcodeGeneratorComponent
      id="barcode-code11"
      type="Code11"
      value="12345-67890"
      width="300px"
      height="150px"
    />
  );
}
```

### When to Use
- Telecommunications equipment
- Numeric with occasional hyphens
- Requires checksum validation
- Legacy equipment integration

### Common Examples

```tsx
// Telecom equipment ID
<BarcodeGeneratorComponent
  id="barcode1"
  type="Code11"
  value="123456789"
  width="250px"
  height="100px"
/>

// Equipment serial with hyphen
<BarcodeGeneratorComponent
  id="barcode2"
  type="Code11"
  value="100000-9"
  width="250px"
  height="100px"
/>
```

## Code128

### Characteristics
- **Character Set:** Full ASCII (128 characters)
- **Checksum:** Always required (automatic)
- **Density:** High - compact representation of data
- **Use Case:** Retail, logistics, shipping, GS1 barcodes

### Implementation

```tsx
import React from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function Code128Example() {
  return (
    <BarcodeGeneratorComponent
      id="barcode-code128"
      type="Code128"
      value="ORDER-2024-001"
      width="300px"
      height="150px"
    />
  );
}
```

### When to Use
- Retail point-of-sale (POS)
- Shipping and logistics
- GS1-128 compliance
- Maximum data density needed
- Modern barcode readers

### Common Examples

```tsx
// Retail SKU
<BarcodeGeneratorComponent
  id="barcode1"
  type="Code128"
  value="5901234123457"
  width="300px"
  height="100px"
/>

// Shipping tracking
<BarcodeGeneratorComponent
  id="barcode2"
  type="Code128"
  value="1Z999AA10123456784"
  width="300px"
  height="100px"
/>

// Order with special chars
<BarcodeGeneratorComponent
  id="barcode3"
  type="Code128"
  value="ORD#2024-ABC-123"
  width="300px"
  height="100px"
/>
```

## Code32

### Characteristics
- **Character Set:** Digits 0-9 (numeric only)
- **Checksum:** Always calculated
- **Format:** Primarily numeric
- **Use Case:** Pharmaceutical, Italian postal system

### Implementation

```tsx
import React from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function Code32Example() {
  return (
    <BarcodeGeneratorComponent
      id="barcode-code32"
      type="Code32"
      value="12345678901"
      width="300px"
      height="150px"
    />
  );
}
```

### When to Use
- Pharmaceutical products
- Numeric identifiers only
- European postal systems
- Regulated industry applications

## Code93

### Characteristics
- **Character Set:** Alphanumeric (0-9, A-Z) and special characters
- **Checksum:** Always included
- **Density:** More compact than Code39
- **Use Case:** General purpose, similar to Code39 but more dense

### Implementation

```tsx
import React from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function Code93Example() {
  return (
    <BarcodeGeneratorComponent
      id="barcode-code93"
      type="Code93"
      value="ABC-12345"
      width="300px"
      height="150px"
    />
  );
}
```

### When to Use
- More compact alternative to Code39
- Alphanumeric data with checksum
- Improved reliability over Code39
- As replacement for Code39 in new systems

### Common Examples

```tsx
// Product batch code
<BarcodeGeneratorComponent
  id="barcode1"
  type="Code93"
  value="BATCH-2024"
  width="250px"
  height="100px"
/>
```

## Codabar

### Characteristics
- **Character Set:** Digits 0-9, hyphen (-), dollar ($), colon (:), period (.), plus (+), slash (/)
- **Checksum:** Modulo 16 (often required)
- **Start/Stop:** Distinct start and stop characters (A, B, C, D)
- **Use Case:** Library cards, blood banks, overnight courier

### Implementation

```tsx
import React from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function CodabarExample() {
  return (
    <BarcodeGeneratorComponent
      id="barcode-codabar"
      type="Codabar"
      value="A12345B"
      width="300px"
      height="150px"
    />
  );
}
```

### When to Use
- Blood bank identification
- Library book codes
- Overnight courier tracking
- Unidirectional scanning requirement

### Common Examples

```tsx
// Blood bank specimen
<BarcodeGeneratorComponent
  id="barcode1"
  type="Codabar"
  value="A123456B"
  width="250px"
  height="100px"
/>

// Library book ID
<BarcodeGeneratorComponent
  id="barcode2"
  type="Codabar"
  value="C987654D"
  width="250px"
  height="100px"
/>
```

## Barcode Type Comparison

| Type | Characters | Checksum | Length | Density | Best For |
|------|-----------|----------|--------|---------|----------|
| **Code39** | 0–9, A–Z, space, -+.$/% | Optional | Variable | Low–Med | General labeling |
| **Code39Extension** | All ASCII | Optional | Variable | Low–Med | With lowercase, special chars |
| **Code11** | 0–9, - | Required | 1–80 | Low | Telecom equipment |
| **Code128** | All ASCII | Required | Variable | High | Retail, logistics, POS |
| **Code32** | 0–9 | Required | Variable | Med | Pharmaceutical, numeric |
| **Code93** | 0–9, A–Z, symbols | Required | Variable | Med | General use, denser than Code39 |
| **Codabar** | 0–9, limited special | Optional | Variable | Low–Med | Blood banks, libraries |

## Selection Guide

### Choose Code39 if:
- Legacy system compatibility needed
- Simple alphanumeric text (uppercase)
- Flexible length requirement

### Choose Code128 if:
- Retail/logistics application
- Maximum data density needed
- Modern barcode reader infrastructure
- Any ASCII character support needed

### Choose Code39 Extended if:
- Need lowercase letters or extended ASCII
- Email addresses or URLs in barcode
- Backward-compatible with Code39 readers

### Choose QR Code if:
- Need to encode URLs or large data
- 2D barcode acceptable
- Smartphone scanning desired

## Real-World Example: Multi-Type Component

```tsx
import React, { useState } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function MultiBarcode() {
  const [barcodeType, setBarcodeType] = useState('Code128');
  const [barcodeValue, setBarcodeValue] = useState('PRODUCT-123');

  return (
    <div style={{ padding: '20px' }}>
      <h2>Barcode Generator</h2>
      
      <div>
        <label>
          Type:
          <select value={barcodeType} onChange={(e) => setBarcodeType(e.target.value)}>
            <option value="Code39">Code39</option>
            <option value="Code39Extension">Code39 Extended</option>
            <option value="Code11">Code11</option>
            <option value="Code128">Code128</option>
            <option value="Code32">Code32</option>
            <option value="Code93">Code93</option>
            <option value="Codabar">Codabar</option>
          </select>
        </label>
      </div>

      <div>
        <label>
          Value:
          <input
            type="text"
            value={barcodeValue}
            onChange={(e) => setBarcodeValue(e.target.value)}
            placeholder="Enter barcode data"
          />
        </label>
      </div>

      <div style={{ marginTop: '20px', border: '1px solid #ddd', padding: '10px' }}>
        <BarcodeGeneratorComponent
          id="dynamic-barcode"
          type={barcodeType}
          value={barcodeValue}
          width="300px"
          height="150px"
        />
      </div>
    </div>
  );
}
```
