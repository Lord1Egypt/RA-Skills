---
name: word-docx-formatting-repair-helper
description: Diagnose and repair Microsoft Word DOCX formatting problems, including styles, numbering, section breaks, headers and footers, comments, tracked changes, and OOXML compatibility. Use when Codex is asked to fix or automate Word document formatting, inspect .docx internals, preserve legal or business document layout, or create a repeatable Word cleanup workflow.
---

# Word DOCX Formatting Repair

Use this skill when a Word document looks wrong, a DOCX automation task breaks formatting, or the user needs a reliable plan for repairing Word files without hand-editing every page.

## Workflow

1. Identify the failure mode: visual formatting drift, broken numbering, missing headers, section break chaos, tracked-change/comment problems, template mismatch, or corrupted OOXML.
2. Ask for the DOCX file only when inspection is required. If the user describes the issue clearly, start with a repair plan and note assumptions.
3. Preserve the original file. Work on a copy and avoid flattening tracked changes or comments unless the user explicitly requests it.
4. Inspect the document structure before editing:
   - Use ZIP/OOXML inspection for `word/document.xml`, `word/styles.xml`, `word/numbering.xml`, `word/settings.xml`, relationships, headers, and footers.
   - Use Word-compatible libraries such as `python-docx` only for operations it safely supports.
   - Use direct OOXML edits for unsupported features such as complex numbering, comments, content controls, and some tracked-change structures.
5. Build a repair map that ties each visible problem to its likely source: paragraph style, direct formatting, numbering definition, section property, relationship target, or theme/font setting.
6. Apply the smallest safe change. Prefer style corrections and numbering definitions over rewriting all paragraphs.
7. Validate by reopening or rendering the document when possible, checking page count, headings, numbering sequences, headers/footers, comments, tracked changes, and tables.

## Common Fix Patterns

- **Broken multilevel numbering**: inspect `numbering.xml`, confirm `abstractNum` and `numId` mappings, then relink affected paragraphs instead of replacing visible text.
- **Heading style drift**: compare `styles.xml` against the template, repair style definitions, then remove unnecessary direct formatting from affected paragraphs.
- **Section break problems**: inspect `w:sectPr` placement, page orientation, margins, and header/footer references before moving content.
- **Tracked changes and comments**: never strip `w:ins`, `w:del`, or comment relationships unless the user asks for a clean final copy.
- **Compatibility issues**: check generated OOXML against Word expectations, especially namespaces, relationship IDs, content types, and unsupported library output.

## Outputs

Provide the user with:

- A diagnosis of what is likely wrong and where it lives in the DOCX package.
- A precise repair plan or implemented document/code change.
- A validation note describing how the repaired DOCX was checked.
- Any remaining risks, especially where Word desktop behavior cannot be fully verified locally.

Read `references/requirement-plan.md` only when evidence from the demand-agent run is needed.
