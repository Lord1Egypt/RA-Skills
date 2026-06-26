---
name: superdoc
description: Create, edit, and manipulate DOCX files using SuperDoc - a modern document editor with custom rendering pipeline. Use when you need to programmatically work with Word documents for creation, editing, formatting, or template generation. Supports both browser and headless Node.js contexts. Prefer SuperDoc for new document workflows requiring full formatting control; use simpler tools (mammoth, docx-js) for text extraction only. Do NOT use for PDF editing, document analysis/summarization, or OCR tasks.
---

# SuperDoc Skill

SuperDoc is a modern DOCX editor providing programmatic document manipulation with full formatting control.

**Installed:** v1.17.0 at `/usr/local/lib/node_modules/superdoc`

## Quick Start

### Create a new document

```javascript
const { Document, Paragraph, TextRun } = require('superdoc');

const doc = new Document({
  sections: [{
    children: [
      new Paragraph({
        children: [
          new TextRun({ text: "Hello World", bold: true })
        ]
      })
    ]
  }]
});

// Save to file
const fs = require('fs');
const Packer = require('superdoc').Packer;
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('output.docx', buffer);
});
```

### Edit an existing document

```javascript
const { Document } = require('superdoc');
const fs = require('fs');

// Load existing DOCX
const buffer = fs.readFileSync('input.docx');
const doc = await Document.load(buffer);

// Find and replace text
doc.sections[0].children.forEach(para => {
  para.children.forEach(run => {
    if (run.text) {
      run.text = run.text.replace(/Company A/g, 'Company B');
    }
  });
});

// Save modified document
const output = await Packer.toBuffer(doc);
fs.writeFileSync('output.docx', output);
```

### Template generation (batch)

```javascript
const { Document, Paragraph, TextRun } = require('superdoc');
const fs = require('fs');

// Load template
const template = fs.readFileSync('template.docx');

// Generate personalized documents
const clients = require('./clients.json');
for (const client of clients) {
  const doc = await Document.load(template);
  
  // Replace placeholders
  doc.sections[0].children.forEach(para => {
    para.children.forEach(run => {
      if (run.text) {
        run.text = run.text
          .replace('{{NAME}}', client.name)
          .replace('{{EMAIL}}', client.email);
      }
    });
  });
  
  const output = await Packer.toBuffer(doc);
  fs.writeFileSync(`output/${client.id}.docx`, output);
}
```

## Common Workflows

### Document creation flow
1. Import required classes: `Document`, `Paragraph`, `TextRun`, `Packer`
2. Build document structure with sections and paragraphs
3. Apply formatting (bold, italic, fonts, colors)
4. Export using `Packer.toBuffer()` or `Packer.toBlob()`

### Document editing flow
1. Load existing DOCX: `Document.load(buffer)`
2. Navigate structure: `doc.sections[i].children` (paragraphs)
3. Modify content: update `run.text` or formatting properties
4. Save: `Packer.toBuffer(doc)`

### Error handling
Common issues:
- **File not found**: Check path before `fs.readFileSync()`
- **Invalid DOCX**: Wrap `Document.load()` in try-catch
- **Memory limits**: For large batches, process in chunks (max 100 docs at once)

## Headless Node.js Usage

SuperDoc requires browser APIs by default. In CLI/headless contexts:

**Setup (one-time):**
```bash
npm install --global superdoc jsdom
```

**Polyfill browser APIs:**
```javascript
const { JSDOM } = require('jsdom');
const dom = new JSDOM('<!DOCTYPE html>');
global.window = dom.window;
global.document = window.document;
global.localStorage = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {}
};

// Now import SuperDoc
const { Document } = require('superdoc');
```

**Alternative: Use browser tool**
For complex rendering or UI-dependent features, use OpenClaw's `browser` tool to run SuperDoc in a real browser context.

## React Integration

**Install:**
```bash
npm install @superdoc-dev/react
```

**Basic usage:**
```jsx
import { SuperDocEditor } from '@superdoc-dev/react';
import { useState } from 'react';

function App() {
  const [doc, setDoc] = useState(null);
  
  return (
    <SuperDocEditor
      document={doc}
      onChange={setDoc}
      onSave={(buffer) => {
        // Handle save
        const blob = new Blob([buffer], { 
          type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
        });
        // Download or upload blob
      }}
    />
  );
}
```

**Key props:**
- `document`: Document instance or null
- `onChange`: Callback when document changes
- `onSave`: Callback with buffer when user saves
- `toolbar`: Custom toolbar config (optional)

## When NOT to Use SuperDoc

- **PDF editing**: Use pdf-lib or similar
- **Document analysis/summarization**: Use text extraction + LLM
- **OCR**: Use tesseract or cloud OCR services
- **Simple text extraction**: Use mammoth.js (lighter weight)
- **Legacy .doc (not .docx)**: Use LibreOffice or online converters

## Advanced Usage

For detailed API reference, advanced formatting, tracked changes, and custom rendering:
- See [references/superdoc-reference.md](references/superdoc-reference.md)
- Repository: https://github.com/superdoc-dev/superdoc

## Troubleshooting

**"localStorage is not defined"**
→ Add localStorage polyfill (see Headless Usage section)

**"Cannot read property 'children' of undefined"**
→ Document structure may be empty; check `doc.sections.length > 0`

**Large files slow/crash**
→ Process in batches; consider streaming for files >10MB

**Formatting not preserved**
→ Ensure you're modifying properties, not replacing objects
