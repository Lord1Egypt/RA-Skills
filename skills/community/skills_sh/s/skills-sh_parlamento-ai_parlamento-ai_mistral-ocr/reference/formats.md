# Output Formats

This guide covers the different output formats available with Mistral OCR.

## Default Output: Markdown

The OCR API returns markdown by default in the response:

```json
{
  "pages": [
    {
      "index": 0,
      "markdown": "# Document Title\n\nContent here...",
      "images": [],
      "tables": []
    }
  ]
}
```

Extract with:
```bash
curl ... | jq -r '.pages[].markdown'
```

---

## 1. Plain Text

To get plain text without markdown formatting, post-process the output:

```bash
# Remove markdown formatting
curl ... | jq -r '.pages[].markdown' | sed 's/#//g; s/\*//g; s/\[.*\](.*)/\1/g'
```

Or ask the agent to strip formatting when processing.

### Example Output
```
Company Invoice

Invoice Number: INV-2026-001
Date: January 15, 2026

Bill To:
John Smith
123 Main Street
New York, NY 10001

Items:
Consulting Services - 10 hours - $1,500.00
Software License - 1 year - $299.00

Total: $1,799.00
```

### Best For
- Simple documents
- Data extraction for further processing
- When formatting doesn't matter

---

## 2. Markdown (Default)

Structured text with headings, lists, tables, and emphasis. This is the default output format.

### Example Output
```markdown
# Company Invoice

**Invoice Number:** INV-2026-001
**Date:** January 15, 2026

## Bill To

John Smith
123 Main Street
New York, NY 10001

## Items

| Description | Quantity | Amount |
|-------------|----------|--------|
| Consulting Services | 10 hours | $1,500.00 |
| Software License | 1 year | $299.00 |

**Total: $1,799.00**
```

### Best For
- Documents that need to be readable
- Reports and articles
- Content that will be published

---

## 3. HTML Tables

For documents with complex tables, request HTML format:

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {...},
    "table_format": "html"
  }'
```

This preserves `colspan` and `rowspan` for merged cells.

### Best For
- Complex tables with merged cells
- Financial statements
- Technical specifications

---

## 4. Structured JSON

For structured data extraction (invoices, forms), you can:
1. Use Mistral Document AI Annotations endpoint
2. Post-process the markdown with a language model

### Example: Invoice to JSON

After OCR extraction, parse the markdown into JSON:

```json
{
  "title": "Company Invoice",
  "document_type": "invoice",
  "invoice_number": "INV-2026-001",
  "date": "2026-01-15",
  "bill_to": {
    "name": "John Smith",
    "address": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "zip": "10001"
  },
  "items": [
    {
      "description": "Consulting Services",
      "quantity": "10 hours",
      "amount": 1500.00
    },
    {
      "description": "Software License",
      "quantity": "1 year",
      "amount": 299.00
    }
  ],
  "total": 1799.00,
  "currency": "USD"
}
```

### Best For
- Database import
- API integrations
- Automated processing

---

## 5. CSV (Tables)

Extract tables and convert to CSV:

```bash
# Extract markdown table, convert to CSV
curl ... | jq -r '.pages[].markdown' | \
  grep -E '^\|' | \
  sed 's/|/,/g; s/^,//; s/,$//; s/ *, */,/g'
```

### Example Output
```csv
Description,Quantity,Amount
Consulting Services,10 hours,$1500.00
Software License,1 year,$299.00
```

### Best For
- Spreadsheet import
- Data analysis
- Bulk data extraction

---

## Format Comparison

| Format | Best For | How to Get |
|--------|----------|------------|
| **Markdown** | Documents, reports | Default output |
| **Plain Text** | Simple extraction | Strip markdown formatting |
| **HTML Tables** | Complex tables | `table_format: html` |
| **JSON** | Structured data | Post-process or Document AI |
| **CSV** | Spreadsheet data | Parse markdown tables |

---

## Document-Specific Tips

### Invoices
- OCR extracts well, parse markdown for fields
- Consider Document AI Annotations for structured output

### Contracts
- Multi-page supported, pages combined automatically
- Headings preserved in markdown

### Receipts
- Single page, fast extraction
- Parse line items from markdown tables

### Forms
- Field labels and values preserved
- May need post-processing for key-value pairs

---

## Saving Output

### Save as Markdown file
```bash
curl ... | jq -r '.pages[].markdown' > document.md
```

### Save as text file
```bash
curl ... | jq -r '.pages[].markdown' > document.txt
```

### Save as JSON (raw response)
```bash
curl ... > response.json
```

### Combine multi-page with headers
```bash
curl ... | jq -r '.pages[] | "# Page \(.index + 1)\n\n\(.markdown)\n\n---"' > full_doc.md
```

---

## Tips for Better Results

1. **Use high-quality sources** - Better input = better output
2. **Check table_format** - Use `html` for complex tables
3. **Multi-page handling** - All pages in `.pages[]` array
4. **Post-process as needed** - Convert markdown to desired format
5. **Validate output** - Check JSON is valid, CSV has consistent columns
