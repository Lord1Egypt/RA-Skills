# Word DOCX Formatting Repair Helper

## What It Does

Repair and automate Word DOCX formatting, styles, find-and-replace, numbering, tables, and conversion workflows while preserving document structure.

This package was generated from demand signals in run `20260623-040526` and then rewritten for publication with domain-specific workflow guidance instead of generic task scaffolding.

## Best For

Office workers, legal teams, students, documentation maintainers, and operations teams cleaning up structured word documents.

## Workflow Summary

1. Clarify the target format, document count, style guide, required sections, protected content, tracked changes needs, and acceptable tooling.
2. Inspect headings, styles, numbering definitions, tables, fields, hyperlinks, images, footnotes, and section breaks before editing.
3. Choose the safest repair path: Word UI steps, python-docx, Pandoc, LibreOffice conversion, XML-level inspection, or manual style normalization.
4. Plan find-and-replace rules with examples, exclusions, backup strategy, and a dry-run report when batch changes are involved.
5. Apply or describe repairs in small reversible stages, preserving semantic styles instead of hard-coding visual formatting.
6. Render or otherwise verify page flow, headings, numbering, tables, links, and conversion fidelity.

## Deliverables

- A repair plan for DOCX formatting, styles, numbering, or conversion issues.
- Safe find-and-replace rules with exclusions and test cases.
- Script snippets or command steps for local document cleanup.
- A visual or structural verification checklist.

## Quality Bar

- Backups or dry-run reports exist before destructive batch edits.
- Styles and numbering are normalized semantically, not only by visual overrides.
- Document rendering is checked after repair when layout matters.
- Protected content, fields, links, and tracked-change needs are handled explicitly.

## Trigger Examples

- `Use $word-docx-formatting-repair-helper to fix broken numbering in this DOCX.`
- `Design a safe batch find-and-replace workflow for Word documents.`
- `Repair styles before converting this Word file to Markdown.`

## Files

- `SKILL.md`: English skill instructions.
- `SKILL.zh-CN.md`: Chinese skill instructions.
- `README.md`: English user-facing guide.
- `README.zh-CN.md`: Chinese user-facing guide.
- `references/requirement-plan.md`: Demand evidence and scoring details.
- `agents/openai.yaml`: Default invocation metadata.
