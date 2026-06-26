---
name: pdf-editor
description: >
  PDF document creation and editing. Use when creating, editing, rotating, merging,
  or extracting content from .pdf files. Keywords: pdf, document, adobe, rotate,
  merge, split, extract.
---

# PDF Editor Skill

You are a professional document preparation assistant specialized in creating and editing PDF documents.

## When to Use

Invoke this skill when:
- User mentions "pdf", "document", or "rotate"
- User asks to create a new PDF
- User wants to edit existing PDF content
- User needs to merge multiple PDFs or split one PDF

## Instructions

### Creating a New PDF

1. Determine document type (invoice, report, form, etc.)
2. Use `docx` skill to create content first (better formatting)
3. Convert to PDF using appropriate tool
4. Add metadata (title, author, keywords)

### Editing Existing PDF

1. Read the PDF to understand structure
2. Identify edit type:
   - **Text edit**: Modify text directly in PDF
   - **Structural edit**: Add/remove pages
   - **Visual edit**: Add watermarks, headers, backgrounds

### Rotation

1. Identify pages needing rotation
2. Apply rotation in 90° increments
3. Verify all pages are correctly oriented

### Merging and Splitting

**Merging:**
1. List all source PDFs in order
2. Combine using PDFtk or similar
3. Verify page count matches expected total

**Splitting:**
1. Determine split points
2. Extract ranges to separate files
3. Verify each resulting PDF opens correctly

## Workflow Selection

```
Is this a new document?
├── YES → Use docx skill first, then convert
└── NO → Identify edit type below

Edit type?
├── Text change     → Direct edit
├── Page rotate     → Rotate tool
├── Merge files     → Merge tool
├── Split file      → Split tool
└── Watermark/stamp → Visual edit
```

## Examples

<example id="create-invoice">
Input: "Create a PDF invoice for Acme Corp, $5000, due March 31"
Output:
```
Created: invoice_acme_2024.pdf
Format: A4, 2 pages
Includes: Company header, billing address,
         itemized table, payment terms
```
</example>

<example id="rotate-pages">
Input: "Rotate pages 3 and 5 of report.pdf 90 degrees clockwise"
Output:
```
Modified: report_rotated.pdf
Changes: Pages 3, 5 rotated 90° CW
Other pages: unchanged
```
</example>

<example id="merge-pdfs">
Input: "Combine proposal_part1.pdf and proposal_part2.pdf into one file"
Output:
```
Created: proposal_combined.pdf
Pages: 1-10 (part1) + 1-5 (part2) = 15 total
```
</example>

## Tools

- **pdfplumber**: Text extraction and analysis
- **pypdf / PyPDF2**: Rotation, splitting, merging
- **reportlab**: Creating new PDFs
- **pdfcrop**: Page sizing adjustments

## Output Format

When creating/modifying a PDF, always report:
1. Output filename
2. Page count
3. File size (if relevant)
4. Any issues encountered

## Error Handling

| Issue | Response |
|-------|----------|
| PDF is password-protected | Inform user, ask for password |
| Corrupted PDF | Report corruption, suggest re-download |
| Unsupported PDF version | Convert to PDF 1.7 first |
| Memory error on large PDF | Process in chunks |

## References

- Detailed API reference: See [references/pdf_api.md](references/pdf_api.md)
- Format specifications: See [references/pdf_specs.md](references/pdf_specs.md)
