# QR Code Generator Reference

## Table of Contents
- [QR Code Overview](#qr-code-overview)
- [Versions and Capacity](#versions-and-capacity)
- [Character Encoding](#character-encoding)
- [Basic Implementation](#basic-implementation)
- [Version Selection](#version-selection)
- [Common Patterns](#common-patterns)
- [Size and Appearance](#size-and-appearance)
- [Real-World Examples](#real-world-examples)

## QR Code Overview

QR (Quick Response) Code is a two-dimensional barcode that encodes information in a grid of dark and light dots. QR codes are ideal for:

- **URLs and Links:** Product pages, social media profiles, contact info
- **Contact Information:** vCard format with name, phone, email
- **Product Marketing:** Connecting print to digital content
- **Inventory & Tracking:** Compact data storage for logistics
- **Mobile-First Solutions:** Smartphone scanning without special apps

### Key Characteristics

- **2D Format:** Square grid pattern (unlike 1D barcodes)
- **Data Capacity:** Thousands of characters possible
- **Error Correction:** Survives partial damage or obscuring
- **Automatic Scaling:** Syncfusion adjusts version based on data length
- **Universal Compatibility:** Works with any smartphone camera

## Versions and Capacity

QR codes come in versions 1 (smallest) through 40 (largest). Syncfusion automatically selects the appropriate version based on data length.

### Version Sizes

| Version | Module Count | Data Capacity (bytes) | Recommended Use |
|---------|-------------|----------------------|------------------|
| 1 | 21×21 | ~17 | Very short text |
| 2 | 25×25 | ~34 | Short text, numbers |
| 5 | 37×37 | ~154 | Phone numbers, short URLs |
| 10 | 57×57 | ~346 | URLs, contact info |
| 15 | 77×77 | ~557 | Longer text, metadata |
| 20 | 97×97 | ~800 | Articles, documents |
| 30 | 137×137 | ~1,663 | Large data blocks |
| 40 | 177×177 | ~2,953 | Maximum capacity |

### Automatic Version Selection

```tsx
import React from 'react';
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function AutoVersionExample() {
  return (
    <div>
      {/* Short text - automatically uses small version */}
      <QRCodeGeneratorComponent
        id="qr1"
        value="Hi"
        width="150px"
        height="150px"
      />

      {/* Medium text - automatically uses medium version */}
      <QRCodeGeneratorComponent
        id="qr2"
        value="https://www.syncfusion.com/products/react"
        width="200px"
        height="200px"
      />

      {/* Long text - automatically uses larger version */}
      <QRCodeGeneratorComponent
        id="qr3"
        value="BEGIN:VCARD
VERSION:3.0
FN:John Doe
TEL:+1-555-123-4567
EMAIL:john@example.com
URL:https://example.com
END:VCARD"
        width="250px"
        height="250px"
      />
    </div>
  );
}
```

## Character Encoding

QR codes support different character encoding modes based on data type:

### 1. Numeric Mode
- **Characters:** 0-9 only
- **Efficiency:** Most compact (3.3 bits per character)
- **Use Case:** Numbers, ZIP codes, phone numbers
- **Example:** "12345"

```tsx
<QRCodeGeneratorComponent
  id="qr-numeric"
  value="5551234567"
  width="200px"
  height="200px"
/>
```

### 2. Alphanumeric Mode
- **Characters:** 0-9, A-Z (uppercase), space, $, %, *, +, -, ., /, :
- **Efficiency:** Medium (5.5 bits per character)
- **Use Case:** Product codes, short text
- **Example:** "PRODUCT-CODE-123"

```tsx
<QRCodeGeneratorComponent
  id="qr-alpha"
  value="ORDER-CODE-ABC123"
  width="200px"
  height="200px"
/>
```

### 3. Byte Mode
- **Characters:** All ASCII characters including lowercase, special chars
- **Efficiency:** Least compact (8 bits per character)
- **Use Case:** URLs, emails, text with mixed case
- **Example:** "https://example.com/page?id=123"

```tsx
<QRCodeGeneratorComponent
  id="qr-bytes"
  value="https://www.example.com/contact?id=123&type=vip"
  width="200px"
  height="200px"
/>
```

### 4. Kanji/JIS8 Mode
- **Characters:** Japanese characters (Kanji, Hiragana, Katakana)
- **Efficiency:** Very compact for Japanese text (13 bits per character)
- **Use Case:** Japanese product info, names

```tsx
<QRCodeGeneratorComponent
  id="qr-kanji"
  value="ありがとうございます"
  width="200px"
  height="200px"
/>
```

## Basic Implementation

### Minimal QR Code

```tsx
import React from 'react';
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function BasicQRCode() {
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

### With Display Text

```tsx
<QRCodeGeneratorComponent
  id="qrcode"
  value="https://www.syncfusion.com"
  width="250px"
  height="250px"
  displayText={{
    text: "Scan for more info"
  }}
/>
```

## Version Selection

### Explicit Version Control (Advanced)

While Syncfusion automatically selects the version, you can influence it by understanding what size code your data requires:

```tsx
// Very short - will use QR v1-3
<QRCodeGeneratorComponent
  id="qr1"
  value="Hi"
  width="120px"
  height="120px"
/>

// Short - will use QR v5-7
<QRCodeGeneratorComponent
  id="qr2"
  value="123-456-7890"
  width="150px"
  height="150px"
/>

// Medium - will use QR v10-15
<QRCodeGeneratorComponent
  id="qr3"
  value="https://www.syncfusion.com/products/react"
  width="200px"
  height="200px"
/>

// Long - will use QR v20+
<QRCodeGeneratorComponent
  id="qr4"
  value="BEGIN:VCARD
VERSION:3.0
FN:John Doe
TEL:+1-555-123-4567
TEL:+1-555-987-6543
EMAIL:john@example.com
EMAIL:john.doe@company.com
TITLE:Software Engineer
ORG:Syncfusion Inc.
URL:https://example.com
NOTE:This is a detailed contact card
END:VCARD"
  width="300px"
  height="300px"
/>
```

## Common Patterns

### Pattern 1: Dynamic QR Code Generation

```tsx
import React, { useState } from 'react';
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function DynamicQRCode() {
  const [url, setUrl] = useState('https://www.syncfusion.com');

  return (
    <div>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter URL or text"
        style={{ width: '100%', padding: '8px', marginBottom: '20px' }}
      />
      
      <QRCodeGeneratorComponent
        id="dynamic-qr"
        value={url}
        width="250px"
        height="250px"
      />
    </div>
  );
}
```

### Pattern 2: QR Code Array (Batch Generation)

```tsx
import React from 'react';
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function QRCodeBatch() {
  const products = [
    { id: 'prod-001', url: 'https://example.com/prod-001' },
    { id: 'prod-002', url: 'https://example.com/prod-002' },
    { id: 'prod-003', url: 'https://example.com/prod-003' },
  ];

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
      {products.map((product) => (
        <div key={product.id} style={{ textAlign: 'center' }}>
          <QRCodeGeneratorComponent
            id={`qr-${product.id}`}
            value={product.url}
            width="200px"
            height="200px"
          />
          <p>{product.id}</p>
        </div>
      ))}
    </div>
  );
}
```

### Pattern 3: Contact Info (vCard)

```tsx
import React from 'react';
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function ContactQRCode() {
  const vcard = `BEGIN:VCARD
VERSION:3.0
FN:Jane Smith
TEL:+1-555-123-4567
EMAIL:jane.smith@company.com
TITLE:Product Manager
ORG:Syncfusion Inc.
URL:https://www.example.com
END:VCARD`;

  return (
    <div style={{ maxWidth: '300px', margin: '0 auto', textAlign: 'center' }}>
      <h3>John's Contact Card</h3>
      <QRCodeGeneratorComponent
        id="contact-qr"
        value={vcard}
        width="200px"
        height="200px"
      />
      <p>Scan to add contact</p>
    </div>
  );
}
```

## Size and Appearance

### Sizing Guidelines

```tsx
// Extra small - short text only
<QRCodeGeneratorComponent
  id="qr-xs"
  value="Hi"
  width="100px"
  height="100px"
/>

// Small - short to medium text
<QRCodeGeneratorComponent
  id="qr-sm"
  value="https://short.url"
  width="150px"
  height="150px"
/>

// Medium - standard size (recommended)
<QRCodeGeneratorComponent
  id="qr-md"
  value="https://www.syncfusion.com/products/react/qrcode"
  width="200px"
  height="200px"
/>

// Large - for distant scanning
<QRCodeGeneratorComponent
  id="qr-lg"
  value="https://www.syncfusion.com/products/react/qrcode"
  width="300px"
  height="300px"
/>

// Extra large - poster/print
<QRCodeGeneratorComponent
  id="qr-xl"
  value="https://www.syncfusion.com/products/react/qrcode"
  width="400px"
  height="400px"
/>
```

### Color Customization

```tsx
// Standard black and white
<QRCodeGeneratorComponent
  id="qr1"
  value="https://example.com"
  width="200px"
  height="200px"
/>

// Custom colors
<QRCodeGeneratorComponent
  id="qr2"
  value="https://example.com"
  width="200px"
  height="200px"
  foreColor="#1E40AF"
  backgroundColor="#F3F4F6"
/>

// Dark theme
<QRCodeGeneratorComponent
  id="qr3"
  value="https://example.com"
  width="200px"
  height="200px"
  foreColor="#FFFFFF"
  backgroundColor="#1F2937"
/>
```

## Real-World Examples

### Example 1: Product Marketing Campaign

```tsx
import React from 'react';
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function ProductPromotion() {
  return (
    <div style={{ maxWidth: '400px', padding: '20px', border: '1px solid #ddd' }}>
      <h2>Scan for Exclusive Offer!</h2>
      <p>Get 20% off when you scan this code:</p>
      
      <QRCodeGeneratorComponent
        id="promo-qr"
        value="https://shop.example.com/promo?code=SAVE20&campaign=email2024"
        width="250px"
        height="250px"
        foreColor="#DC2626"
        backgroundColor="#FEF2F2"
        displayText={{
          text: "www.shop.example.com"
        }}
      />
      
      <p>Valid until December 31, 2024</p>
    </div>
  );
}
```

### Example 2: Event Registration

```tsx
import React from 'react';
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function EventTicket() {
  const ticketData = JSON.stringify({
    eventId: 'SYN2024',
    attendeeId: 'ATT12345',
    email: 'attendee@example.com'
  });

  return (
    <div style={{ maxWidth: '500px', padding: '20px', backgroundColor: '#f0f0f0' }}>
      <h2>Syncfusion Developer Conference 2024</h2>
      <p>Scan at entry:</p>
      
      <QRCodeGeneratorComponent
        id="ticket-qr"
        value={`https://events.syncfusion.com/verify?data=${encodeURIComponent(ticketData)}`}
        width="300px"
        height="300px"
      />
      
      <p>Ticket ID: ATT12345</p>
      <p>Attendee: John Doe</p>
    </div>
  );
}
```

### Example 3: WiFi Connection

```tsx
import React from 'react';
import { QRCodeGeneratorComponent } from '@syncfusion/ej2-react-barcode-generator';

export default function WiFiQRCode() {
  // Standard WiFi format: WIFI:T:WPA;S:networkname;P:password;;
  const wifiCode = 'WIFI:T:WPA;S:GuestNetwork;P:SecurePassword123;;';

  return (
    <div style={{ maxWidth: '300px', textAlign: 'center' }}>
      <h3>Connect to WiFi</h3>
      <QRCodeGeneratorComponent
        id="wifi-qr"
        value={wifiCode}
        width="200px"
        height="200px"
      />
      <p>Scan to connect to: GuestNetwork</p>
    </div>
  );
}
```
