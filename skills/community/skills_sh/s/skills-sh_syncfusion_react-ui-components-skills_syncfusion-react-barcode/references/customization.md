# Customization and Styling Reference

## Table of Contents
- [Dimensions](#dimensions)
- [Colors](#colors)
- [Display Text](#display-text)
- [Examples by Type](#examples-by-type)
- [Responsive Design](#responsive-design)
- [CSS and Advanced Styling](#css-and-advanced-styling)

## Dimensions

### Width and Height Properties

The `width` and `height` props control the physical size of the barcode. Both values must include units (typically pixels).

#### Size Selection Guidelines

```tsx
import React from 'react';
import { 
  BarcodeGeneratorComponent,
  QRCodeGeneratorComponent,
  DataMatrixGeneratorComponent
} from '@syncfusion/ej2-react-barcode-generator';

// Extra Small - for tight spaces
<BarcodeGeneratorComponent
  id="barcode-xs"
  type="Code128"
  value="SMALL"
  width={"100px"}
  height={"60px"}
/>

// Small - labels and tags
<QRCodeGeneratorComponent
  id="qr-sm"
  value="https://example.com"
  width={"120px"}
  height={"120px"}
/>

// Standard - most common
<BarcodeGeneratorComponent
  id="barcode-std"
  type="Code39"
  value="STANDARD"
  width={"250px"}
  height={"100px"}
/>

// Large - from distance scanning
<QRCodeGeneratorComponent
  id="qr-lg"
  value="https://example.com"
  width={"300px"}
  height={"300px"}
/>

// Extra Large - posters, signage
<DataMatrixGeneratorComponent
  id="dm-xl"
  value="XLARGE"
  width={"400px"}
  height={"400px"}
/>
```

#### Dimension Rules by Type

**Barcodes (1D):**
- Minimum width: 100px (narrow)
- Minimum height: 60px (readable)
- Aspect ratio: Usually 2.5:1 or 3:1 (width:height)

**QR Codes (2D):**
- Always square (width = height)
- Minimum: 100px × 100px
- Recommended: 150-250px for scanning
- Larger for distant scanning: 300-500px

**Data Matrix (2D):**
- Usually square (width = height)
- Minimum: 100px × 100px
- Compact alternative to QR: 120-180px
- Industrial use: 150-200px

### Responsive Sizing

```tsx
import React, { useState, useEffect } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function ResponsiveBarcode() {
  const [barcodeSize, setBarcodeSize] = useState('medium');

  const sizeMap = {
    small: { width: '150px', height: '75px' },
    medium: { width: '250px', height: '100px' },
    large: { width: '350px', height: '150px' }
  };

  return (
    <div>
      <select value={barcodeSize} onChange={(e) => setBarcodeSize(e.target.value)}>
        <option value="small">Small</option>
        <option value="medium">Medium</option>
        <option value="large">Large</option>
      </select>

      <BarcodeGeneratorComponent
        id="responsive-barcode"
        type="Code128"
        value="RESPONSIVE"
        width={sizeMap[barcodeSize].width}
        height={sizeMap[barcodeSize].height}
      />
    </div>
  );
}
```

## Colors

### Color Properties (foreColor and backgroundColor)

```tsx
import React from 'react';
import { 
  BarcodeGeneratorComponent,
  QRCodeGeneratorComponent,
  DataMatrixGeneratorComponent
} from '@syncfusion/ej2-react-barcode-generator';

// Default: Black bars on white background
<BarcodeGeneratorComponent
  id="barcode-default"
  type="Code128"
  value="DEFAULT"
  width={"200px"}
  height={"100px"}
/>

// Custom colors
<BarcodeGeneratorComponent
  id="barcode-custom"
  type="Code128"
  value="CUSTOM"
  width={"200px"}
  height={"100px"}
  foreColor={"#1E3A8A"}    // Dark blue bars
  backgroundColor={"#E0F2FE"}  // Light blue background
/>
```

## Display Text

### Display Text Customization

The `displayText` property allows you to show text below the barcode.

```tsx
import React from 'react';
import { 
  BarcodeGeneratorComponent,
  QRCodeGeneratorComponent
} from '@syncfusion/ej2-react-barcode-generator';

// No display text (default)
<BarcodeGeneratorComponent
  id="barcode1"
  type="Code128"
  value="ABC123"
  width={"250px"}
  height={"100px"}
/>

// With display text
<BarcodeGeneratorComponent
  id="barcode2"
  type="Code128"
  value="ABC123"
  width={"250px"}
  height={"100px"}
  displayText={{
    text: "Product Code"
  }}
/>
```

### Display Text Properties

```tsx
// Basic display text
<BarcodeGeneratorComponent
  id="barcode1"
  type="Code39"
  value="PROD-001"
  width={"250px"}
  height={"100px"}
  displayText={{
    text: "Product ID"
  }}
/>

// Text visibility options
<QRCodeGeneratorComponent
  id="qr1"
  value="https://example.com"
  width={"200px"}
  height={"200px"}
  displayText={{
    text: "Scan here",
    visibility: true
  }}
/>
```

## Examples by Type

### Code128 Customization Examples

```tsx
import React from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function Code128Customization() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
      
      {/* Standard retail */}
      <div>
        <h4>Retail Product</h4>
        <BarcodeGeneratorComponent
          id="barcode1"
          type="Code128"
          value="5901234123457"
          width={"200px"}
          height={"80px"}
          foreColor={"#000000"}
          backgroundColor={"#FFFFFF"}
          displayText={{
            text: "Scan Product"
          }}
        />
      </div>
  );
}
```

### QR Code Customization Examples

```tsx
import React from 'react';
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function QRCodeCustomization() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
      
      {/* Marketing campaign */}
      <div style={{ textAlign: 'center' }}>
        <h4>Marketing Campaign</h4>
        <QRCodeGeneratorComponent
          id="qr1"
          value="https://campaign.example.com/promo2024"
          width={"200px"}
          height={"200px"}
          foreColor={"#FF6B00"}
          backgroundColor={"#FFF5E6"}
          displayText={{
            text: "Scan for offer"
          }}
        />
      </div>
  );
}
```

### Data Matrix Customization Examples

```tsx
import React from 'react';
import { DataMatrixGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function DataMatrixCustomization() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
      
      {/* Industrial standard */}
      <div style={{ border: '1px solid #000', padding: '10px' }}>
        <h4>Industrial</h4>
        <DataMatrixGeneratorComponent
          id="dm1"
          value="PN:12345SN:ABC"
          width={"150px"}
          height={"150px"}
          foreColor={"#000000"}
          backgroundColor={"#FFFFFF"}
          displayText={{
            text: "Part ID"
          }}
        />
      </div>
  );
}
```

## Responsive Design

### Mobile-Friendly Sizing

```tsx
import React, { useState, useEffect } from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function ResponsiveBarcode() {
  const [size, setSize] = useState('medium');

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      if (width < 600) setSize('small');
      else if (width < 1000) setSize('medium');
      else setSize('large');
    };

    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const sizes = {
    small: { width: '150px', height: '75px' },
    medium: { width: '250px', height: '100px' },
    large: { width: '350px', height: '150px' }
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <BarcodeGeneratorComponent
        id="responsive-barcode"
        type="Code128"
        value="RESPONSIVE"
        width={sizes[size].width}
        height={sizes[size].height}
      />
    </div>
  );
}
```

## CSS and Advanced Styling

### Container Styling

```tsx
import React from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function StyledBarcodeContainer() {
  return (
    <div style={{
      padding: '15px',
      border: '2px solid #ddd',
      borderRadius: '8px',
      backgroundColor: '#fafafa',
      display: 'inline-block',
      textAlign: 'center'
    }}>
      <h3 style={{ margin: '0 0 10px 0' }}>Product Label</h3>
      <BarcodeGeneratorComponent
        id="styled-barcode"
        type="Code128"
        value="STYLED"
        width={"250px"}
        height={"100px"}
      />
      <p style={{ margin: '10px 0 0 0', fontSize: '12px', color: '#666' }}>
        Product ID: STYLED
      </p>
    </div>
  );
}
```

### CSS Classes (Custom Styling)

```tsx
import React from 'react';
import { BarcodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function CSSStyledBarcode() {
  const styles = `
    .custom-barcode-wrapper {
      padding: 20px;
      border: 3px solid #1e40af;
      border-radius: 12px;
      background: linear-gradient(135deg, #f0f4f8 0%, #e6f0f8 100%);
      display: inline-block;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .custom-barcode-title {
      font-size: 14px;
      font-weight: bold;
      color: #1e40af;
      margin-bottom: 12px;
    }

    .custom-barcode-value {
      font-family: monospace;
      font-size: 11px;
      color: #64748b;
      margin-top: 8px;
    }
  `;

  return (
    <>
      <style>{styles}</style>
      <div className="custom-barcode-wrapper">
        <div className="custom-barcode-title">Barcode Label</div>
        <BarcodeGeneratorComponent
          id="css-barcode"
          type="Code128"
          value="CSS-STYLED"
          width={"200px"}
          height={"80px"}
        />
        <div className="custom-barcode-value">CSS-STYLED</div>
      </div>
    </>
  );
}
```
