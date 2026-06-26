---
name: Word / DOCX
description: Create, read, and edit Word documents (.docx) with support for templates, tables, and styling.
metadata: {"clawdbot":{"emoji":"📘","os":["linux","darwin","win32"]}}
---

## When to Use

User needs to create, read, or edit Word documents (.docx). Supports template filling, table generation, and professional styling.

## Architecture

This skill uses `python-docx` for DOCX manipulation. All processing happens locally.

## Quick Reference

| Topic | File |
|-------|------|
| Generate Quotation | `scripts/generate_quotation_docx.py` |

## Core Rules

### 1. Use Templates for Consistency
When generating documents repeatedly (quotations, proposals), use templates with placeholder text that gets replaced.

### 2. Handle Chinese Filenames Carefully
Use `glob` wildcards or `pathlib` for Chinese filename compatibility:

```python
from pathlib import Path
for f in Path(".").glob("*.docx"):
    doc = Document(str(f))
```

### 3. Tables Need Explicit Styling
Word tables require explicit border and cell styling. Use `Table Grid` style as baseline.

### 4. Section Properties Control Layout
Page margins, orientation, and headers/footers are controlled at section level:

```python
for section in doc.sections:
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
```

### 5. Runs vs Paragraphs
Text formatting happens at run level. A paragraph can contain multiple runs with different styles.

## Common Traps

- **Merged cells** - Only top-left cell holds value in merged ranges
- **Page breaks** - Insert explicitly with `doc.add_page_break()`
- **Images** - Require absolute paths or file-like objects
- **Styles** - Built-in styles vary by Word version; test compatibility

## Dependencies

```bash
pip3 install python-docx
```

## Security & Privacy

**Data that stays local:**
- All file processing happens locally
- No external services called

**This skill does NOT:**
- Send data to external endpoints
- Require network access

## Related Skills

- `read-docx` — Read-only DOCX extraction
- `excel-xlsx` — Excel file handling
- `pdf-text-extractor` — PDF text extraction

## Feedback

- If useful: `clawhub star word-docx`
- Stay updated: `clawhub sync`
