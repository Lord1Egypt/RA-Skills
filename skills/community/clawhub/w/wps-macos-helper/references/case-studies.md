# case-studies

## Case 1: Markdown -> docx -> WPS -> PDF

### Goal
User writes content in Markdown, wants editable office output on macOS, then exports final PDF from WPS.

### Recommended route
1. Clean content structure in Markdown.
2. Convert Markdown into docx using a safe document-generation step.
3. Open docx in WPS on macOS.
4. Check title hierarchy, fonts, page size, tables, headers/footers, and page breaks.
5. Export PDF only after visual confirmation.

### Why this route is safer
- Markdown is easier for AI restructuring.
- docx is easier for office editing.
- WPS is best used as the final visual editing layer, not the first restructuring layer.

## Case 2: PDF -> Markdown -> rebuilt docx -> WPS

### Goal
User has a PDF, wants to revise content and continue editing in WPS.

### Recommended route
1. Convert the PDF to Markdown for text extraction.
2. Repair headings, lists, tables, and obvious OCR issues.
3. Rebuild into docx if editable office output is needed.
4. Open in WPS to polish layout and export.

### Key checks
- OCR quality
- table structure integrity
- heading hierarchy
- page size and font substitution after rebuild

## Case 3: Existing docx opens badly in WPS

### Goal
User already has a docx, but WPS on macOS renders it poorly.

### Recommended route
1. Inspect whether styles or direct formatting dominate.
2. Confirm A4 vs Letter page size.
3. Check fonts and section breaks.
4. Simplify complex floating images or wrapped objects.
5. Save a repaired copy instead of overwriting the original.
