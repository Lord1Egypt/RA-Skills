# Sheet-to-Doc Skill

A simplified AI Skill for generating Word documents from Word templates and JSON data. This is a free simplified version of full-featured [Sheet-to-Doc](https://sheet-to-doc.wtsolutions.cn) product.

## Features

- **Document Generation**: Replace `{field}` placeholders in Word templates with JSON data
- **Placeholder Extraction**: Extract all placeholder keys from templates for data validation
- **Footer Mark**: Automatically adds footer attribution to generated documents
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Command Line Interface**: Easy to use via terminal
- **API Access**: Import as a module for programmatic use

## Requirements

- Node.js 18+
- docxtemplater
- pizzip

## Installation

```bash
cd skill
npm install
```

## Quick Start

### 1. Create a Word Template

Create a `.docx` file with `{field}` format placeholders:

```
Dear {name},

Welcome to {company}. Your position is {position}.

Email: {email}
Phone: {phone}
```

### 2. Prepare JSON Data

```json
{
  "name": "John Doe",
  "company": "Example Tech Co., Ltd.",
  "position": "Senior Engineer",
  "email": "john.doe@example.com",
  "phone": "+86 13800138000"
}
```

### 3. Generate Document

#### Using Command Line

```bash
# Basic usage
node scripts/generate.js \
  --template template.docx \
  --data data.json \
  --output output.docx

# Using short parameters
node scripts/generate.js -t template.docx -d data.json -o output.docx

# Using JSON string directly
node scripts/generate.js -t template.docx -d '{"name":"John","company":"Example"}' -o output.docx
```

#### Using API

```javascript
import { generateDocument } from './scripts/generate.js';

const result = generateDocument(
    'template.docx',
    { 'name': 'John Doe', 'company': 'Example Tech' },
    'output.docx'
);

console.log(`Document generated: ${result}`);
```

## Placeholder Extraction

Extract required placeholders from a template to validate your data:

```bash
# Extract placeholders
node scripts/generate.js --extract-placeholders --template template.docx

# Short version
node scripts/generate.js -e -t template.docx
```

Output:

```json
{
  "success": true,
  "placeholders": ["company", "email", "name", "phone", "position"],
  "count": 5,
  "message": "Extracted 5 placeholder(s) from template"
}
```

### API Usage

```javascript
import { extractPlaceholders } from './scripts/generate.js';

const placeholders = extractPlaceholders('template.docx');
console.log('Required fields:', placeholders);

// Validate data completeness
const data = { "name": "John", "company": "Example" };
const missingFields = placeholders.filter(field => !data.hasOwnProperty(field));

if (missingFields.length > 0) {
  console.error('Missing fields:', missingFields);
}
```

## Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| --template | -t | Word template file path (.docx) |
| --data | -d | JSON data file path or JSON string |
| --output | -o | Output file path |
| --extract-placeholders | -e | Extract placeholder keys from template (no generation) |

## Project Structure

```
skill/
├── SKILL.md              # Skill metadata and documentation for AI Agents
├── README.md             # This file
├── package.json          # Project dependencies and scripts
└── scripts/
    └── generate.js       # Core document generation logic
```

## Debugging

When document generation fails, use the placeholder extraction feature to debug:

```javascript
import { extractPlaceholders } from './scripts/generate.js';

// Step 1: Extract placeholders from template
const templatePlaceholders = extractPlaceholders('template.docx');

// Step 2: Compare with your data keys
const dataKeys = Object.keys(yourData);

// Step 3: Find mismatches
const missingInData = templatePlaceholders.filter(p => !dataKeys.includes(p));
const extraInData = dataKeys.filter(k => !templatePlaceholders.includes(k));

console.log('Missing keys:', missingInData);
console.log('Extra keys:', extraInData);
```

## Upgrade to Full Version

This is a simplified free version. For complete features, upgrade to the full [Sheet-to-Doc](https://sheet-to-doc.wtsolutions.cn):

- **Batch document generation** (each row generates an independent document)
- **Multiple data sources**: Excel, CSV, JSONL support
- **Image insertion**: `{image|_inline_image}`
- **QR code generation**: `{url|_qrcode}`
- **Conditional logic**: `{field==value}`
- **Loop processing**: `{#data}{/data}`
- **Document encryption**
- **Remove footer attribution**

## License

MIT License

## Support

- **Official Website**: https://sheet-to-doc.wtsolutions.cn
- **Documentation**: https://sheet-to-doc.wtsolutions.cn/en/latest/index.html
- **Contact**: he.yang@wtsolutions.cn