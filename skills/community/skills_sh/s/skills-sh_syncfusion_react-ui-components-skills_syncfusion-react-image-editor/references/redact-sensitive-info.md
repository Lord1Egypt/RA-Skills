# Redact Sensitive Information

## Table of Contents

- [Redaction Overview](#redaction-overview)
- [Apply Redaction](#apply-redaction)
- [Redaction Modes](#redaction-modes)
- [Management](#management)
- [Advanced Patterns](#advanced-patterns)

## Redaction Overview

Redaction safely removes or obscures sensitive information from images using blur or pixelation effects.

### Use Cases

- Hide personal information (names, addresses, phone numbers)
- Redact confidential data in documents
- Comply with privacy regulations (GDPR, HIPAA)
- Secure financial information
- Remove license plates or identification numbers

## Apply Redaction

### Blur Redaction

Hide content with blur effect using the redaction API:

```tsx
import { RedactType } from '@syncfusion/ej2-react-image-editor';

function applyBlurRedaction(): void {
  imgObj.drawRedact(RedactType.Blur, 100, 100, 300, 150, 20);
}
```

### Pixelate Redaction

Hide content with pixelation:

```tsx
import { RedactType } from '@syncfusion/ej2-react-image-editor';

function applyPixelRedaction(): void {
  imgObj.drawRedact(RedactType.Pixelate, 100, 100, 300, 150, 8);
}
```

### Use Official Redaction API

Redact sensitive areas using the official API:

```tsx
import { RedactType } from '@syncfusion/ej2-react-image-editor';

function redactArea(x: number, y: number, width: number, height: number): void {
  // Use blur for standard redaction
  imgObj.drawRedact(RedactType.Blur, x, y, width, height, 20);
}

// Usage: Redact a social security number area
redactArea(150, 200, 200, 40);
```

## Redaction Modes

### Full Blur Redaction

Complete coverage with blur:

```tsx
import { RedactType } from '@syncfusion/ej2-react-image-editor';

function fullBlurRedact(x: number, y: number, width: number, height: number): void {
  imgObj.drawRedact(RedactType.Blur, x, y, width, height, 30);
}

// Redact entire name field
fullBlurRedact(50, 75, 400, 40);
```

### Full Pixelate Redaction

Complete coverage with pixelation:

```tsx
import { RedactType } from '@syncfusion/ej2-react-image-editor';

function fullPixelateRedact(x: number, y: number, width: number, height: number): void {
  imgObj.drawRedact(RedactType.Pixelate, x, y, width, height, 10);
}

// Redact entire name field
fullPixelateRedact(50, 75, 400, 40);
```

### Text-Based Redaction

Target specific text:

```tsx
function redactText(searchText: string, x: number, y: number): void {
  const textWidth = searchText.length * 8; // Approximate
  imgObj.drawRectangle(x, y, textWidth + 10, 25, true, '#000000');
}

// Redact email address
redactText('user@email.com', 100, 150);
```

## Management

### Get Redacted Items

Access all redactions:

```tsx
function getRedactions(): void {
  const redacts = imgObj.getRedacts();
  
  console.log('Redacted areas:', redacts.length);
  redacts.forEach((redaction, index) => {
    console.log(`Redaction ${index}:`, {
      id: redaction.id,
      x: redaction.x,
      y: redaction.y,
      width: redaction.width,
      height: redaction.height
    });
  });
}
```

### Delete Redaction

Remove redaction:

```tsx
function deleteRedaction(redactionId: string): void {
  imgObj.deleteRedact(redactionId);
}
```

### Update Redaction

Modify existing redaction:

```tsx
import { RedactSettings } from '@syncfusion/ej2-react-image-editor';

function updateRedaction(redactionId: string, x: number, y: number, width: number, height: number): void {
  // Use updateRedact with proper parameters
  imgObj.updateRedact(redactionId, {
    x: x,
    y: y,
    width: width,
    height: height
  });
}
```

### Clear All Redactions

Remove all redactions:

```tsx
function clearAllRedactions(): void {
  const redacts = imgObj.getRedacts();
  redacts.forEach(redaction => {
    imgObj.deleteRedact(redaction.id);
  });
}
```

## Advanced Patterns

### Automatic Redaction Zones

```tsx
import { RedactType } from '@syncfusion/ej2-react-image-editor';

interface RedactionZone {
  name: string;
  x: number;
  y: number;
  width: number;
  height: number;
}

const redactionZones: RedactionZone[] = [
  { name: 'Name', x: 50, y: 75, width: 400, height: 40 },
  { name: 'SSN', x: 50, y: 120, width: 200, height: 40 },
  { name: 'Phone', x: 50, y: 165, width: 300, height: 40 },
  { name: 'Address', x: 50, y: 210, width: 400, height: 80 }
];

function applyZoneRedactions(): void {
  redactionZones.forEach(zone => {
    imgObj.drawRedact(RedactType.Blur, zone.x, zone.y, zone.width, zone.height, 20);
  });
}
```

### Conditional Redaction

```tsx
interface RedactionRule {
  field: string;
  condition: (value: string) => boolean;
  zones: RedactionZone[];
}

const redactionRules: RedactionRule[] = [
  {
    field: 'email',
    condition: (val) => val.includes('@'),
    zones: [{ name: 'Email', x: 50, y: 150, width: 300, height: 30 }]
  },
  {
    field: 'phone',
    condition: (val) => /\d{3}-\d{3}-\d{4}/.test(val),
    zones: [{ name: 'Phone', x: 50, y: 190, width: 200, height: 30 }]
  },
  {
    field: 'ssn',
    condition: (val) => /\d{3}-\d{2}-\d{4}/.test(val),
    zones: [{ name: 'SSN', x: 50, y: 230, width: 150, height: 30 }]
  }
];

function applyConditionalRedactions(data: Record<string, string>): void {
  redactionRules.forEach(rule => {
    if (rule.condition(data[rule.field])) {
      rule.zones.forEach(zone => {
        imgObj.drawRectangle(zone.x, zone.y, zone.width, zone.height, true, '#000000');
      });
    }
  });
}
```

### Batch Redaction

```tsx
import { RedactType } from '@syncfusion/ej2-react-image-editor';

function batchRedact(redactionList: Array<{ x: number; y: number; width: number; height: number }>): void {
  redactionList.forEach(rect => {
    imgObj.drawRedact(RedactType.Blur, rect.x, rect.y, rect.width, rect.height, 20);
  });
}

// Usage
const redactions = [
  { x: 50, y: 75, width: 400, height: 40 },    // Name
  { x: 50, y: 120, width: 200, height: 40 },   // SSN
  { x: 50, y: 165, width: 300, height: 40 }    // Phone
];

batchRedact(redactions);
```

### Redaction with Tracking

```tsx
import { RedactType } from '@syncfusion/ej2-react-image-editor';

class RedactionTracker {
  private redactions: Array<{ id: string; field: string; timestamp: Date }> = [];
  
  addRedaction(fieldName: string, x: number, y: number, width: number, height: number): void {
    imgObj.drawRedact(RedactType.Blur, x, y, width, height, 20);
    
    const redacts = imgObj.getRedacts();
    const lastRedaction = redacts[redacts.length - 1];
    
    this.redactions.push({
      id: lastRedaction.id,
      field: fieldName,
      timestamp: new Date()
    });
  }
  
  getRedactionHistory(): string {
    return this.redactions
      .map(r => `${r.field} redacted at ${r.timestamp.toISOString()}`)
      .join('\n');
  }
  
  exportAuditLog(): void {
    const log = this.getRedactionHistory();
    console.log('Audit Log:\n' + log);
  }
}

const tracker = new RedactionTracker();
tracker.addRedaction('Name', 50, 75, 400, 40);
tracker.addRedaction('Phone', 50, 165, 300, 40);
tracker.exportAuditLog();
```

### Undo Redactions

```tsx
import { RedactType } from '@syncfusion/ej2-react-image-editor';

const redactionHistory: Array<{ zone: RedactionZone; id: string }> = [];

function redactZoneWithHistory(zone: RedactionZone): void {
  imgObj.drawRedact(RedactType.Blur, zone.x, zone.y, zone.width, zone.height, 20);
  
  const redacts = imgObj.getRedacts();
  const lastRedaction = redacts[redacts.length - 1];
  
  redactionHistory.push({
    zone: zone,
    id: lastRedaction.id
  });
}

function undoLastRedaction(): void {
  if (redactionHistory.length > 0) {
    const lastRedaction = redactionHistory.pop();
    if (lastRedaction) {
      imgObj.deleteRedact(lastRedaction.id);
    }
  }
}

function redoRedaction(): void {
  imgObj.redo();
}
```

### Redaction with Verification

```tsx
import { RedactType } from '@syncfusion/ej2-react-image-editor';

class SecureRedaction {
  private redactedField: Map<string, string> = new Map();
  
  redactWithVerification(fieldName: string, x: number, y: number, width: number, height: number): void {
    // Mark field as redacted
    this.redactedField.set(fieldName, 'redacted');
    
    // Apply visual redaction
    imgObj.drawRedact(RedactType.Blur, x, y, width, height, 20);
  }
  
  isFullyRedacted(requiredFields: string[]): boolean {
    return requiredFields.every(field => this.redactedField.has(field));
  }
  
  canExport(): boolean {
    return this.redactedField.size > 0 && this.isFullyRedacted(Array.from(this.redactedField.keys()));
  }
}

const secureRedaction = new SecureRedaction();
secureRedaction.redactWithVerification('Name', 50, 75, 400, 40);
secureRedaction.redactWithVerification('SSN', 50, 120, 200, 40);

if (secureRedaction.canExport()) {
  // Safe to export
}
```

### Smart Redaction Suggestions

```tsx
interface ContentArea {
  type: 'email' | 'phone' | 'ssn' | 'address' | 'credit_card';
  pattern: RegExp;
  x: number;
  y: number;
  width: number;
  height: number;
}

const contentPatterns: ContentArea[] = [
  {
    type: 'email',
    pattern: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/,
    x: 0,
    y: 0,
    width: 0,
    height: 0
  },
  {
    type: 'phone',
    pattern: /(\d{3}[-.]?\d{3}[-.]?\d{4})/,
    x: 0,
    y: 0,
    width: 0,
    height: 0
  },
  {
    type: 'ssn',
    pattern: /(\d{3}-\d{2}-\d{4})/,
    x: 0,
    y: 0,
    width: 0,
    height: 0
  }
];

function suggestRedactions(content: string): ContentArea[] {
  return contentPatterns.filter(pattern => pattern.pattern.test(content));
}

function applySuggestedRedactions(): void {
  import { RedactType } from '@syncfusion/ej2-react-image-editor';
  
  const suggestions = suggestRedactions('Name: John Doe, Email: john@example.com, Phone: 555-123-4567');
  suggestions.forEach(suggestion => {
    imgObj.drawRedact(RedactType.Blur, suggestion.x, suggestion.y, suggestion.width, suggestion.height, 20);
  });
}
```
