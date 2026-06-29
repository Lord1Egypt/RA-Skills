---
name: work-productivity-word-mail-workflow-helper
description: Build and troubleshoot Microsoft Word mail merge and DOCX template workflows with merge fields, content controls, document properties, repeated sections, data sources, and formatting preservation. Use when Codex needs to automate templated Word documents for legal, HR, operations, sales, or administrative workflows.
---

# Word Mail Merge Template Workflow

Use this skill for repeatable Word document assembly: letters, contracts, HR forms, invoices, reports, and other templates that combine structured data with DOCX formatting.

## Workflow

1. Clarify the template model: classic mail merge fields, content controls, bookmarks, custom document properties, placeholder text, or a custom DOCX assembly pipeline.
2. Identify the data source and shape: CSV, Excel, JSON, database rows, one-record-per-document, repeated tables, optional clauses, images, or signatures.
3. Preserve the template. Work from a clean master copy and generate outputs into a separate folder.
4. Choose the safest fill strategy:
   - Use Word mail merge when the user needs Word-native merge behavior.
   - Use content controls for structured templates that should remain editable.
   - Use direct OOXML or a templating library for repeated sections, conditionals, and package-level control.
5. Protect formatting by replacing field values inside existing runs where possible. Avoid rebuilding paragraphs unless the template is simple.
6. Handle edge cases explicitly: missing data, long values, date/number formatting, optional sections, blank rows, page breaks, headers/footers, and tracked changes.
7. Validate generated documents by checking field completion, formatting, page count, section breaks, table rows, filenames, and any required PDF export.

## Common Fix Patterns

- **Fields left unresolved**: distinguish display text from field-code instructions and update fields in Word when needed.
- **Formatting changes after merge**: replace within runs or content controls rather than replacing whole paragraphs.
- **Repeated rows or clauses**: model repeats as tables or block-level OOXML, not simple string replacement.
- **Data formatting**: normalize dates, currency, line breaks, and locale-specific values before merge.
- **Auditability**: keep a manifest of source record IDs and output filenames for batch runs.

## Outputs

Provide:

- A clear template/data mapping.
- A safe generation workflow or implementation.
- A validation checklist for batch output quality.
- Notes about which steps require Word desktop field updates or PDF export.

Read `references/requirement-plan.md` only when the demand-agent evidence is needed.
