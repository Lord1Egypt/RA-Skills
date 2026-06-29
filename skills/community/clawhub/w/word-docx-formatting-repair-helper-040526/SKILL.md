---
name: word-docx-formatting-repair-helper
description: >-
  Repair and automate Word DOCX formatting, styles, find-and-replace, numbering, tables, and conversion workflows while preserving document structure. Use when a user asks for DOCX, Microsoft Word, formatting, styles, find replace, or needs practical workflow, code, checklist, documentation, or review support for this job.
---

# Word DOCX Formatting Repair Helper

## Purpose

Use this skill when a DOCX or Word-like document has inconsistent styles, broken numbering, unreliable find-and-replace, conversion issues, table problems, or repeated formatting cleanup.

Audience: office workers, legal teams, students, documentation maintainers, and operations teams cleaning up structured Word documents.

Read `references/requirement-plan.md` when demand evidence, source links, scoring rationale, or review criteria are needed.

## Workflow

1. Clarify the target format, document count, style guide, required sections, protected content, tracked changes needs, and acceptable tooling.
2. Inspect headings, styles, numbering definitions, tables, fields, hyperlinks, images, footnotes, and section breaks before editing.
3. Choose the safest repair path: Word UI steps, python-docx, Pandoc, LibreOffice conversion, XML-level inspection, or manual style normalization.
4. Plan find-and-replace rules with examples, exclusions, backup strategy, and a dry-run report when batch changes are involved.
5. Apply or describe repairs in small reversible stages, preserving semantic styles instead of hard-coding visual formatting.
6. Render or otherwise verify page flow, headings, numbering, tables, links, and conversion fidelity.

## Expected Outputs

- A repair plan for DOCX formatting, styles, numbering, or conversion issues.
- Safe find-and-replace rules with exclusions and test cases.
- Script snippets or command steps for local document cleanup.
- A visual or structural verification checklist.

## Validation

- Backups or dry-run reports exist before destructive batch edits.
- Styles and numbering are normalized semantically, not only by visual overrides.
- Document rendering is checked after repair when layout matters.
- Protected content, fields, links, and tracked-change needs are handled explicitly.

## Triggers

Keywords: `DOCX`, `Microsoft Word`, `formatting`, `styles`, `find replace`, `numbering`, `tables`, `Pandoc`

Example trigger sentences:

- `Use $word-docx-formatting-repair-helper to fix broken numbering in this DOCX.`
- `Design a safe batch find-and-replace workflow for Word documents.`
- `Repair styles before converting this Word file to Markdown.`
