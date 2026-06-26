# PDF Report Generation with pdfkit

Generate professional PDF reports with tables, charts, and formatted layouts using Node.js pdfkit.

## Installation

```bash
npm install pdfkit
```

## Basic Structure

```javascript
const PDFDocument = require('pdfkit');
const fs = require('fs');

const doc = new PDFDocument({ 
  size: 'A4', 
  margin: 45,
  info: {
    Title: 'Report Title',
    Author: 'SDVM',
    Subject: 'Report Subject'
  }
});

doc.pipe(fs.createWriteStream('report.pdf'));

// Page constants
const PAGE_W = 595.28;   // A4 width in points
const MG = 45;           // Margin
const CW = PAGE_W - (MG * 2);  // Content width: 505
const PAGE_H = 841.89;   // A4 height in points
const BOT = PAGE_H - 55; // Bottom limit

// State
let pg = 1;  // Page number
let y = 0;   // Current Y position
```

## Page Management

```javascript
function newPage() {
  doc.addPage();
  pg++;
  y = MG;
  // Header
  doc.fontSize(7).fillColor('#6B7280').text('Your Brand', MG, MG - 12);
  doc.moveTo(MG, MG + 2).lineTo(PAGE_W - MG, MG + 2)
    .strokeColor('#E5E7EB').lineWidth(0.5).stroke();
  y = MG + 12;
}

function footer() {
  doc.fontSize(7).fillColor('#6B7280')
    .text(`Page ${pg}`, MG, PAGE_H - 30, { align: 'center', width: CW });
}

function need(h = 60) {
  if (y + h > BOT) { footer(); newPage(); }
}
```

## Drawing Functions

### Section Title

```javascript
function title(text) {
  need(45);
  doc.fontSize(13).fillColor('#1F2937').text(text, MG, y);
  const tw = doc.widthOfString(text);
  doc.moveTo(MG, y + 16).lineTo(MG + tw + 8, y + 16)
    .strokeColor('#2563EB').lineWidth(1.5).stroke();
  y += 28;
}
```

### Paragraph

```javascript
function para(text, indent = 0) {
  const w = CW - indent;
  doc.fontSize(9);
  const h = doc.heightOfString(text, { width: w });
  need(h + 6);
  doc.fillColor('#1F2937').text(text, MG + indent, y, { width: w, lineGap: 1 });
  y += h + 6;
}
```

### Bullet List

```javascript
function bullet(text, indent = 18) {
  const w = CW - indent;
  doc.fontSize(9);
  const h = doc.heightOfString(text, { width: w });
  need(h + 5);
  doc.fillColor('#2563EB').text('●', MG, y);
  doc.fillColor('#1F2937').text(text, MG + indent, y, { width: w, lineGap: 1 });
  y += h + 5;
}
```

### Info Box (measures text height FIRST, then draws box)

```javascript
function infoBox(text, bg = '#FEF2F2', border = '#DC2626') {
  const pad = 12;
  const w = CW - pad * 2;
  doc.fontSize(9);
  
  // Calculate height FIRST
  const textH = doc.heightOfString(text, { width: w, lineGap: 1 });
  const boxH = textH + pad * 2;
  need(boxH + 10);
  
  // Then draw
  doc.fillColor(bg).rect(MG, y, CW, boxH).fill();
  doc.rect(MG, y, CW, boxH).strokeColor(border).lineWidth(1).stroke();
  doc.fillColor('#1F2937').text(text, MG + pad, y + pad, { width: w, lineGap: 1 });
  y += boxH + 12;
}
```

### Data Table (auto row height calculation)

```javascript
function table(headers, rows, colW) {
  const pad = 6;
  const fs = 8;
  const hdrH = 24;
  
  doc.fontSize(fs);
  
  // Pre-calculate all row heights
  const rowH = rows.map(row => {
    let maxH = 22;
    row.forEach((cell, ci) => {
      const h = doc.heightOfString(cell || '', { 
        width: colW[ci] - pad * 2, 
        lineGap: 1 
      });
      const cellH = h + pad * 2;
      if (cellH > maxH) maxH = cellH;
    });
    return maxH;
  });
  
  const totalH = hdrH + rowH.reduce((a, b) => a + b, 0);
  need(totalH + 15);
  
  let ty = y;
  
  // Draw header
  doc.fillColor('#EFF6FF').rect(MG, ty, CW, hdrH).fill();
  doc.rect(MG, ty, CW, hdrH).strokeColor('#E5E7EB').lineWidth(0.5).stroke();
  let cx = MG + pad;
  headers.forEach((h, i) => {
    doc.fontSize(fs).fillColor('#1F2937')
      .text(h, cx, ty + pad + 2, { width: colW[i] - pad * 2, lineBreak: false });
    cx += colW[i];
  });
  ty += hdrH;
  
  // Draw rows
  rows.forEach((row, ri) => {
    const rh = rowH[ri];
    if (ri % 2 === 0) {
      doc.fillColor('#F9FAFB').rect(MG, ty, CW, rh).fill();
    }
    doc.rect(MG, ty, CW, rh).strokeColor('#E5E7EB').lineWidth(0.5).stroke();
    
    let rx = MG + pad;
    doc.fontSize(fs).fillColor('#1F2937');
    row.forEach((cell, ci) => {
      doc.text(cell || '', rx, ty + pad, { 
        width: colW[ci] - pad * 2,
        lineGap: 1
      });
      rx += colW[ci];
    });
    ty += rh;
  });
  
  y = ty + 10;
}
```

### Bar Chart

```javascript
function barChart(items, maxVal) {
  const barH = 24;
  const barMaxW = 300;
  const lblW = 60;
  
  need(items.length * (barH + 10) + 15);
  
  items.forEach(item => {
    const bw = Math.max(0, (item.value / maxVal) * barMaxW);
    
    // Label
    doc.fontSize(9).fillColor('#1F2937')
      .text(item.label, MG, y + 6, { width: lblW });
    
    // Background bar
    doc.fillColor('#F3F4F6')
      .rect(MG + lblW, y, barMaxW, barH).fill();
    
    // Value bar
    if (bw > 0) {
      doc.fillColor(item.color || '#2563EB')
        .rect(MG + lblW, y, bw, barH).fill();
    }
    
    // Value text
    const valText = item.value.toLocaleString();
    doc.fontSize(9)
      .fillColor(bw > 55 ? '#FFFFFF' : '#1F2937')
      .text(valText, MG + lblW + 6, y + 6, { 
        width: Math.max(bw - 12, 40) 
      });
    
    // Percentage (optional)
    if (item.pct) {
      doc.fontSize(8).fillColor('#6B7280')
        .text(item.pct, MG + lblW + barMaxW + 10, y + 7);
    }
    
    y += barH + 10;
  });
  
  // Reset spacing
  y += 5;
}
```

## Color Palette

```javascript
const C = {
  red: '#DC2626',       // Danger, critical alerts
  orange: '#EA580C',    // Warnings
  green: '#16A34A',     // Positive, success
  blue: '#2563EB',      // Primary, links
  gray: '#6B7280',      // Secondary text
  dark: '#1F2937',      // Primary text
  lightGray: '#E5E7EB', // Borders
  lighterGray: '#F3F4F6', // Backgrounds
  white: '#FFFFFF',
  headerBg: '#EFF6FF',  // Table header
  rowAlt: '#F9FAFB',    // Alternating row
  dangerBg: '#FEF2F2'   // Alert box
};
```

## Common Pitfalls

1. **Text overlap** — Always calculate text height BEFORE drawing boxes/containers. Use `doc.heightOfString()` first, then draw the box with that height.

2. **Row height in tables** — Pre-calculate ALL row heights before drawing. Use the maximum height per row across all columns.

3. **Page breaks** — Always call `need()` before drawing any multi-line element (tables, charts, info boxes).

4. **Line gap** — Use `lineGap: 1` option for multi-line text to prevent crowding between lines.

5. **Credit/secret info** — Remove internal API details (credits, keys, tokens) from client-facing reports.

6. **Column widths** — Ensure column widths sum to content width. Test with long text to verify wrapping.

7. **Font sizing** — Keep body text at 9pt minimum for readability in print.

## Complete Example

```javascript
const PDFDocument = require('pdfkit');
const fs = require('fs');

const doc = new PDFDocument({ size: 'A4', margin: 45 });
doc.pipe(fs.createWriteStream('output.pdf'));

const MG = 45, CW = 505, BOT = 786;
let pg = 1, y = MG;

// ... include all helper functions above ...

// Page 1
title('Executive Summary');
infoBox('Status: CRITICAL — 60% negative sentiment detected across platforms.');

title('Key Metrics');
table(
  ['Metric', 'Value', 'Change', 'Status'],
  [
    ['Total Posts', '8,251', '+33%', 'High'],
    ['Negative', '3,300', '+45%', 'Critical'],
    ['Positive', '0', '-100%', 'None'],
  ],
  [120, 80, 80, 225]
);

title('Volume Trend');
barChart([
  { label: 'Day 1', value: 3490, color: '#3B82F6', pct: '33%' },
  { label: 'Day 2', value: 4646, color: '#EF4444', pct: '44%' },
  { label: 'Day 3', value: 115, color: '#9CA3AF', pct: '1%' },
], 4600);

footer();
doc.end();
```
