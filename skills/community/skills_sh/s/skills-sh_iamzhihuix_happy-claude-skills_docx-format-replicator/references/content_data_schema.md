# Content Data Schema

This document describes the JSON schema for content data files used by `generate_document.py`.

## Overview

The content data file defines the actual content (text, headings, tables) that will be placed into a Word document using the formatting rules from a format configuration.

## Schema Structure

```json
{
  "metadata": {},
  "sections": []
}
```

## Fields

### metadata

**Type**: `object`
**Description**: Optional metadata about the document content.

**Fields**:
- `title` (string): Document title
- `author` (string): Document author
- `version` (string): Version number
- `date` (string): Document date

**Example**:
```json
"metadata": {
  "title": "Product Research Task Specification",
  "author": "Engineering Team",
  "version": "1.0",
  "date": "2025-01-15"
}
```

### sections

**Type**: `array`
**Description**: Array of content sections that make up the document. Sections are processed in order.

Each section is an object with a `type` field and type-specific properties.

## Section Types

### Heading Section

Create a heading with optional numbering.

**Fields**:
- `type` (string): Must be `"heading"`
- `content` (string): Heading text
- `level` (number): Heading level (1-9)
- `number` (string, optional): Numbering prefix (e.g., "1", "1.1", "1.1.1")

**Example**:
```json
{
  "type": "heading",
  "content": "Introduction",
  "level": 1,
  "number": "1"
}
```

### Paragraph Section

Create a text paragraph.

**Fields**:
- `type` (string): Must be `"paragraph"`
- `content` (string): Paragraph text
- `style_id` (string, optional): Style ID to apply from format config

**Example**:
```json
{
  "type": "paragraph",
  "content": "This document outlines the technical requirements for the product.",
  "style_id": "1"
}
```

### Table Section

Create a table.

**Fields**:
- `type` (string): Must be `"table"`
- `rows` (number): Number of rows
- `columns` (array): Column width definitions (from format config)
- `table_index` (number, optional): Index of table config to use
- `cells` (array): 2D array of cell contents

**Example**:
```json
{
  "type": "table",
  "rows": 3,
  "columns": ["2000", "8000"],
  "table_index": 0,
  "cells": [
    ["Header 1", "Header 2"],
    ["Row 1 Col 1", "Row 1 Col 2"],
    ["Row 2 Col 1", "Row 2 Col 2"]
  ]
}
```

### Page Break Section

Insert a page break.

**Fields**:
- `type` (string): Must be `"page_break"`

**Example**:
```json
{
  "type": "page_break"
}
```

## Complete Example

Here's a complete content data file for a technical document:

```json
{
  "metadata": {
    "title": "New Product Research Task Specification",
    "author": "Research Team",
    "version": "1.0",
    "date": "2025-01-15"
  },
  "sections": [
    {
      "type": "heading",
      "content": "Introduction",
      "level": 1,
      "number": "1"
    },
    {
      "type": "paragraph",
      "content": "This document defines the research and development tasks for the new product initiative."
    },
    {
      "type": "heading",
      "content": "Product Name and Code",
      "level": 1,
      "number": "2"
    },
    {
      "type": "paragraph",
      "content": "Product Name: Advanced Control System"
    },
    {
      "type": "paragraph",
      "content": "Product Code: ACS-2025-01"
    },
    {
      "type": "heading",
      "content": "Technical Specifications",
      "level": 1,
      "number": "3"
    },
    {
      "type": "heading",
      "content": "Electrical Requirements",
      "level": 2,
      "number": "3.1"
    },
    {
      "type": "table",
      "rows": 4,
      "columns": ["3000", "7000"],
      "cells": [
        ["Parameter", "Specification"],
        ["Input Voltage", "220V AC ± 10%"],
        ["Power Consumption", "≤ 500W"],
        ["Frequency", "50Hz ± 2Hz"]
      ]
    },
    {
      "type": "page_break"
    },
    {
      "type": "heading",
      "content": "Testing Requirements",
      "level": 1,
      "number": "4"
    },
    {
      "type": "paragraph",
      "content": "All products must undergo comprehensive testing according to industry standards."
    }
  ]
}
```

## Usage Patterns

### Multi-level Numbering

For documents with nested sections (1, 1.1, 1.1.1):

```json
[
  {"type": "heading", "content": "First Section", "level": 1, "number": "1"},
  {"type": "heading", "content": "Subsection A", "level": 2, "number": "1.1"},
  {"type": "heading", "content": "Sub-subsection", "level": 3, "number": "1.1.1"},
  {"type": "heading", "content": "Subsection B", "level": 2, "number": "1.2"},
  {"type": "heading", "content": "Second Section", "level": 1, "number": "2"}
]
```

### Complex Tables

For tables with merged cells or special formatting, you may need to extend the schema:

```json
{
  "type": "table",
  "rows": 3,
  "columns": ["2000", "4000", "4000"],
  "cells": [
    ["Header 1", "Header 2", "Header 3"],
    ["Data 1", "Data 2", "Data 3"],
    ["Data 4", "Data 5", "Data 6"]
  ],
  "merge_cells": [
    {"row": 0, "col": 1, "row_span": 1, "col_span": 2}
  ]
}
```

### Approval Tables

For documents with approval/review tables (common in technical documents):

```json
{
  "type": "table",
  "table_index": 0,
  "cells": [
    ["Version", "1.0"],
    ["Author", "John Doe"],
    ["Reviewer", "Jane Smith"],
    ["Approver", "Manager Name"],
    ["Date", "2025-01-15"]
  ]
}
```

## Tips

1. **Consistent Numbering**: Ensure numbering is sequential and follows the document hierarchy
2. **Style IDs**: Reference style IDs from the format configuration to maintain consistency
3. **Table Index**: Use the same table_index for tables that should have the same formatting
4. **Empty Paragraphs**: Use empty content strings for spacing: `{"type": "paragraph", "content": ""}`
5. **Special Characters**: Properly escape JSON special characters in content strings

## Extending the Schema

To support additional content types:

1. Define a new section type
2. Add handling in `generate_document.py`
3. Document the new type in this file
4. Provide examples

Common extensions:
- Images (`{"type": "image", "path": "...", "width": "..."}`)
- Lists (`{"type": "list", "items": [...], "style": "bullet"}`)
- Footnotes (`{"type": "footnote", "content": "..."}`)
