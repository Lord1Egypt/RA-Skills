---
name: sheet-to-doc-skill
description: "Generate Word documents from Word templates and JSON data. Supports basic placeholder replacement ({field} format) and placeholder extraction for data validation. Best for batch-generating contracts, invitations, certificates, and mail-merge style docs."
license: MIT
author: WTSolutions
version: "1.0.0"
homepage: https://sheet-to-doc.wtsolutions.cn
tags: [document-automation, docx, json, office, templates]
compatibility: "Requires Node.js 18+, docxtemplater, pizzip"
---

# Sheet-to-Doc Document Generator Skill

## Examples

- user: "Generate a Word document from this template and data" → use generateDocument tool, upload template and JSON data
- user: "Help me batch generate invitations" → prepare template and JSON data, run the script
- user: "Fill Excel data into Word template" → convert to JSON then generate
- user: "What placeholders does this template need?" → use extractPlaceholders tool to get required fields
- user: "Document generation failed, check the template" → extract placeholders and compare with data keys

## Overview

This skill provides document generation capabilities based on Word templates and JSON data. Users upload Word templates containing placeholders, input JSON data, and the skill automatically replaces placeholders and generates complete Word documents.

**Key Features:**
- **Document Generation**: Replace `{field}` placeholders in Word templates with JSON data
- **Placeholder Extraction**: Extract all placeholder keys from a template to validate data completeness before generation
- **Footer Mark**: Automatically add footer mark to generated documents
- **Error Debugging**: Use placeholder extraction to diagnose data-key mismatches

**⚠️ Note**: This skill is a free simplified version of Sheet-to-Doc, which only supports basic data placeholder replacement. Visit https://s.wtsolutions.cn/sheet-to-doc.html for full version features:
- Batch document generation (each row generates an independent document)
- Use Excel, CSV, JSONL as data source
- Image insertion (`{image|_inline_image}`)
- QR code generation (`{url|_qrcode}`)
- Conditional logic (`{field==value}`)
- Loop processing (`{#data}{/data}`)
- Document encryption
- Remove footer advertisement

## Use Cases

Use this skill when users need to:
- Generate documents from Word templates and JSON data
- Batch generate standardized documents (contracts, invitations, certificates, reports, etc.)
- Fill Excel/spreadsheet data into Word templates
- Create personalized documents (mail merge-like functionality)
- **Debug document generation errors**: Extract placeholders to check if JSON data has all required keys
- **Validate template completeness**: Verify all placeholders are properly defined before distribution
- **Prepare data schema**: Get the list of required fields from a template to create matching data structure

## Prerequisites

1. **Word template file** (.docx format) with `{field}` format placeholders
2. **JSON data** with keys matching the template placeholders
3. **Dependencies**: Run `npm install` to install docxtemplater and pizzip

## Usage Steps

### Step 1: Prepare Template

Create a Word document with `{field}` format placeholders:

```
Dear {name},

We are pleased to inform you that your {application_type} application submitted on {date} has been approved.

Company: {company_name}
Address: {address}
Phone: {phone_number}
```

### Step 2: Extract Placeholders (Optional but Recommended)

Before generating documents, extract the required placeholders from the template to ensure your JSON data has all the necessary keys:

```bash
node scripts/generate.js --extract-placeholders --template path/to/template.docx
```

Or via API:

```javascript
import { extractPlaceholders } from './scripts/generate.js';
const requiredFields = extractPlaceholders('template.docx');
console.log('Required fields:', requiredFields);
```

### Step 3: Prepare Data

Prepare JSON data with keys matching the extracted placeholders:

```json
{
  "name": "John Doe",
  "date": "July 20, 2026",
  "application_type": "Employment",
  "company_name": "Example Tech Co., Ltd.",
  "address": "Tech Park, Chaoyang District, Beijing",
  "phone_number": "+86 10-12345678"
}
```

### Step 4: Validate Data (Recommended)

Compare your JSON data keys with the extracted placeholders to catch mismatches early:

```javascript
import { extractPlaceholders } from './scripts/generate.js';

const requiredFields = extractPlaceholders('template.docx');
const userData = { "name": "John", "company_name": "Example" };

const missingFields = requiredFields.filter(field => !userData.hasOwnProperty(field));
const extraFields = Object.keys(userData).filter(field => !requiredFields.includes(field));

if (missingFields.length > 0) {
  console.error(`❌ Missing required fields: ${missingFields.join(', ')}`);
}
if (extraFields.length > 0) {
  console.warn(`⚠️ Extra fields in data (not in template): ${extraFields.join(', ')}`);
}
```

### Step 5: Run Generation Script

Generate documents using Node.js:

```bash
node scripts/generate.js \
  --template path/to/template.docx \
  --data path/to/data.json \
  --output path/to/output.docx
```

Or use the API:

```javascript
import { generateDocument } from './scripts/generate.js';

const result = generateDocument(
    'template.docx',
    { 'name': 'John Doe', 'age': '30' },
    'output.docx'
);
```

## API Reference

### generateDocument(templatePath, data, outputPath)

**Function**: Generate Word document from template and data

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| templatePath | string | Yes | Word template file path (.docx) |
| data | object | Yes | JSON data object with keys matching template placeholders |
| outputPath | string | Yes | Output file path |

**Returns**:

| Type | Description |
|------|-------------|
| string | Path of the generated file |

**Example**:

```javascript
import { generateDocument } from './scripts/generate.js';

const data = {
    "name": "Jane Smith",
    "department": "Engineering",
    "hire_date": "2026-07-20"
};

const result = generateDocument(
    "contract_template.docx",
    data,
    "contract_jane.docx"
);

console.log(`Document generated successfully: ${result}`);
```

### extractPlaceholders(templatePath)

**Function**: Extract placeholder keys from Word template. This is a critical function for debugging and validation. It scans the document content and footer sections to find all `{field}` format placeholders.

**Purpose**:
- Get the list of required data fields before generating documents
- Debug generation errors by comparing extracted placeholders with JSON data keys
- Validate template structure and ensure all placeholders are properly defined
- Create data schema documentation from templates

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| templatePath | string | Yes | Word template file path (.docx) |

**Returns**:

| Type | Description |
|------|-------------|
| string[] | Sorted array of unique placeholder keys found in the template (document body + footers) |

**Example 1: Basic Extraction**

```javascript
import { extractPlaceholders } from './scripts/generate.js';

const placeholders = extractPlaceholders("contract_template.docx");
console.log("Placeholders in template:", placeholders);
// Output: ["address", "application_type", "company_name", "date", "name", "phone_number"]
```

**Example 2: Data Validation Workflow**

```javascript
import { extractPlaceholders, generateDocument } from './scripts/generate.js';

async function safeGenerateDocument(templatePath, data, outputPath) {
    try {
        const requiredPlaceholders = extractPlaceholders(templatePath);
        const dataKeys = Object.keys(data);

        const missingKeys = requiredPlaceholders.filter(key => !dataKeys.includes(key));
        const extraKeys = dataKeys.filter(key => !requiredPlaceholders.includes(key));

        if (missingKeys.length > 0) {
            throw new Error(`Missing required keys in data: ${missingKeys.join(', ')}. Template requires: ${requiredPlaceholders.join(', ')}`);
        }

        if (extraKeys.length > 0) {
            console.warn(`Warning: These keys exist in data but not in template: ${extraKeys.join(', ')}`);
        }

        const result = generateDocument(templatePath, data, outputPath);
        return { success: true, path: result };

    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Usage
const result = safeGenerateDocument(
    "contract.docx",
    { "name": "John", "company": "Example" },
    "output.docx"
);
```

**Example 3: Error Debugging Scenario**

When document generation fails or placeholders are not replaced, use this workflow:

```javascript
import { extractPlaceholders } from './scripts/generate.js';

async function debugGenerationFailure(templatePath, data) {
    const templatePlaceholders = extractPlaceholders(templatePath);
    const dataKeys = Object.keys(data);

    console.log("\n=== DEBUG REPORT ===");
    console.log("Template placeholders:", templatePlaceholders);
    console.log("Data keys:", dataKeys);

    const missingInData = templatePlaceholders.filter(p => !dataKeys.includes(p));
    const missingInTemplate = dataKeys.filter(k => !templatePlaceholders.includes(k));

    if (missingInData.length > 0) {
        console.error("\n❌ ERROR: These placeholders are in template but missing from data:");
        console.error("   Missing keys:", missingInData);
        console.error("\n   Please add these keys to your JSON data:");
        missingInData.forEach(key => console.error(`   - "${key}": ""`));
    }

    if (missingInTemplate.length > 0) {
        console.warn("\n⚠️ WARNING: These data keys are not used in template:");
        console.warn("   Extra keys:", missingInTemplate);
    }

    if (missingInData.length === 0 && missingInTemplate.length === 0) {
        console.log("\n✅ All keys match! The issue may be elsewhere.");
    }
}
```

**Example 4: Create Data Schema from Template**

```javascript
import { extractPlaceholders } from './scripts/generate.js';

function createDataSchema(templatePath) {
    const placeholders = extractPlaceholders(templatePath);
    const schema = {};
    
    placeholders.forEach(placeholder => {
        if (placeholder.toLowerCase().includes('date')) {
            schema[placeholder] = "YYYY-MM-DD";
        } else if (placeholder.toLowerCase().includes('email')) {
            schema[placeholder] = "user@example.com";
        } else if (placeholder.toLowerCase().includes('phone')) {
            schema[placeholder] = "+86 13800138000";
        } else {
            schema[placeholder] = "";
        }
    });
    
    return schema;
}

// Generate a sample data template
const dataTemplate = createDataSchema("contract.docx");
console.log(JSON.stringify(dataTemplate, null, 2));
```

## Command Line Reference

### Usage

```bash
node scripts/generate.js \
  --template path/to/template.docx \
  --data path/to/data.json \
  --output path/to/output.docx
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| --template / -t | Word template file path |
| --data / -d | JSON data file path or JSON string |
| --output / -o | Output file path |
| --extract-placeholders / -e | Extract placeholder keys from template (no generation). Use this to preview required fields before generating documents. |

### Examples

```bash
# Using JSON file
node scripts/generate.js \
  --template contract.docx \
  --data data.json \
  --output contract_john.docx

# Using JSON string
node scripts/generate.js \
  --template invitation.docx \
  --data '{"name":"Jane Smith","date":"2026-07-20"}' \
  --output invitation_jane.docx

# Using short parameters
node scripts/generate.js \
  -t template.docx \
  -d data.json \
  -o output.docx

# Extract placeholders from template (returns JSON output)
node scripts/generate.js \
  --extract-placeholders \
  --template contract.docx

# Short version for extracting placeholders
node scripts/generate.js -e -t contract.docx

# Extract and save to file for analysis
node scripts/generate.js -e -t contract.docx > placeholders.json
```

### Command Line Output Format

**Success (Extract Placeholders):**
```json
{
  "success": true,
  "placeholders": ["name", "company", "position", "email", "phone"],
  "count": 5,
  "message": "Extracted 5 placeholder(s) from template"
}
```

**Error (Extract Placeholders):**
```json
{
  "success": false,
  "error": "Template file not found: /path/to/missing.docx"
}
```

**Success (Generate Document):**
```
✓ Document generated successfully: output.docx
Tip: Upgrade to Pro version for more features → https://sheet-to-doc.wtsolutions.cn
```

**Error (Generate Document):**
```
✗ Document generation failed: Template file not found: template.docx
```

## Placeholder Format

### Basic Format

Use `{field}` format placeholders in templates:

```
Dear {name},

Your application number is: {application_id}

Date: {date}
```

### Data Matching

JSON data keys must match template placeholders exactly (case-sensitive):

```json
{
  "name": "John Doe",
  "application_id": "20260720001",
  "date": "July 20, 2026"
}
```

### Scope

The `extractPlaceholders` function scans:
- **Document body**: Main content of the Word document
- **Footers**: All footer sections in the document

Note: Headers are not currently scanned, as they typically do not contain data-driven placeholders.

## Sample Data

```json
{
  "name": "John Doe",
  "age": "30",
  "gender": "Male",
  "company": "Example Tech Co., Ltd.",
  "department": "Engineering",
  "position": "Senior Engineer",
  "hire_date": "July 20, 2026",
  "phone": "+86 13800138000",
  "email": "john.doe@example.com",
  "address": "Tech Park Building A, Room 1001, Chaoyang District, Beijing"
}
```

## Debugging Workflow

When document generation fails or produces unexpected results, follow this workflow:

### Step 1: Extract Placeholders

```javascript
const placeholders = extractPlaceholders('template.docx');
console.log('Template requires:', placeholders);
```

### Step 2: Check Data Keys

```javascript
const data = { "name": "John", "email": "john@example.com" };
console.log('Data provides:', Object.keys(data));
```

### Step 3: Compare and Identify Issues

```javascript
const missing = placeholders.filter(p => !data.hasOwnProperty(p));
console.log('Missing keys:', missing);
```

### Step 4: Fix Data and Retry

Add missing keys to your JSON data and regenerate the document.

## Skill Version Limitations

| Feature | Skill Version | Full Version |
|---------|-------------|-------------|
| Basic placeholder replacement | ✅ Supported | ✅ Supported |
| Placeholder extraction | ✅ Supported | ✅ Supported |
| Batch document generation | ❌ Not supported | ✅ Supported |
| Image insertion | ❌ Not supported | ✅ Supported |
| QR code generation | ❌ Not supported | ✅ Supported |
| Conditional logic | ❌ Not supported | ✅ Supported |
| Loop processing | ❌ Not supported | ✅ Supported |
| Document encryption | ❌ Not supported | ✅ Supported |
| Footer mark | ✅ Included | Included/Removed |

## Notes

1. **Placeholder format**: Must use `{field}` format, supports English field names
2. **JSON format**: Data must be valid JSON, keys must match placeholders exactly (case-sensitive)
3. **Document limitation**: This skill generates documents with footer marks
4. **Advanced features**: Loop, image, QR code and other advanced features are only available in full version of Sheet-to-Doc.
5. **Placeholder extraction**: Extracts from document body and footers. Use this to validate data completeness before generation.

## Troubleshooting

**Issue 1: Placeholders not replaced**
- Use `extractPlaceholders` to get the exact list of required keys
- Ensure JSON keys match template placeholders exactly (including spaces and case)
- Check JSON format for validity

**Issue 2: Script execution fails**
- Ensure dependencies are installed: `npm install`
- Ensure Node.js version >= 18
- Check that template file is a valid .docx format

**Issue 3: Missing data keys**
- Run `node scripts/generate.js -e -t template.docx` to see required fields
- Compare the output with your JSON data keys
- Add any missing keys to your data

**Issue 4: Extra data keys**
- The skill will ignore extra keys not present in the template
- This is not an error, but you may want to remove unused keys for cleanliness

**Issue 5: Need advanced features**
- Visit https://sheet-to-doc.wtsolutions.cn to upgrade to full version of Sheet-to-Doc.

## Upgrade Guide

Experience full features, visit:
- 🔗 **Official Download**: https://sheet-to-doc.wtsolutions.cn
- 📖 **Help Documentation**: https://sheet-to-doc.wtsolutions.cn/en/latest/index.html
- 📧 **Contact Support**: he.yang@wtsolutions.cn

---

